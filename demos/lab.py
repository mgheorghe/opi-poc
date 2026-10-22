'''
Fixtures and helpers shared by the demos: ssh to the lab devices, pick a dpu from testbed.DPUS,
and wire the A100G switch for each test.
'''
import json
import os
import socket
import threading
import time
import netmiko
import paramiko
import pytest

from testbed import *

# repo checkout used for the docker compose files, the CI workspace or this clone
HOME_FOLDER = os.environ.get('GITHUB_WORKSPACE',
                             os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
# private key used to ssh as root into the server, dpu and dpu host
SSH_KEY = os.environ.get('OPI_SSH_KEY', os.path.expanduser('~/.ssh/id_rsa'))

# systemd >= 257 (Ubuntu 26.04) wraps every shell prompt in OSC 3008 escapes with a fresh uuid,
# which netmiko cannot match; its profile script skips TERM=dumb, but netmiko asks for vt100
_invoke_shell = paramiko.SSHClient.invoke_shell
paramiko.SSHClient.invoke_shell = lambda self, term='vt100', *args, **kwargs: \
    _invoke_shell(self, 'dumb', *args, **kwargs)


def connect(host, jump=None, device_type='linux', username='root'):
    '''
    Opens a netmiko session with the ssh key, through the `jump` host when one is given.
    '''
    info = {
        'device_type': device_type,
        'host': host,
        'username': username,
        'use_keys': True,
        'key_file': SSH_KEY
    }
    hop = None
    if jump:
        # netmiko does not check host keys either; the IMC key changes on every reflash
        hop = paramiko.SSHClient()
        hop.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        hop.connect(jump, username=username, key_filename=SSH_KEY, timeout=10)
        info['sock'] = hop.get_transport().open_channel('direct-tcpip', (host, 22), ('', 0))
    connection = netmiko.ConnectHandler(**info)
    if hop:
        disconnect = connection.disconnect
        connection.disconnect = lambda: (disconnect(), hop.close())
    return connection


def connect_or_skip(host, jump=None, what=None):
    '''
    Same as `connect`, but skips the test when the host takes no passwordless ssh.
    '''
    try:
        return connect(host, jump)
    except (netmiko.NetmikoAuthenticationException, netmiko.NetmikoTimeoutException,
            paramiko.SSHException, OSError) as e:
        pytest.skip('%s: no passwordless ssh to root@%s%s: %s' % (
            what or host, host, ' via %s' % jump if jump else '', str(e).splitlines()[0]))


@pytest.fixture(params=sorted(DPUS))
def lab_dpu(request):
    '''
    Yields one testbed.DPUS entry, with its name, so each test runs once per dpu.
    '''
    info = dict(DPUS[request.param], name=request.param)
    if info.get('skip'):
        pytest.skip('%s: %s' % (info['name'], info['skip']))
    yield info


@pytest.fixture
def switch():
    '''
    Yields a function that moves switch ports into a vlan, so each test wires the tgen ports to the
    dpu ports it needs. The original vlans are restored afterwards; the config is never saved.
    '''
    switch_connect = connect(A100G_IP, device_type='arista_eos', username='arista')
    switch_connect.enable()
    saved_vlans = {}
    new_vlans = []
    portfast_ports = []

    def access_vlan(vlan, ports):
        if 'not found' in switch_connect.send_command('show vlan %d' % vlan):
            new_vlans.append(vlan)
            switch_connect.send_config_set(['vlan %d' % vlan])
        for port in ports:
            if port not in saved_vlans:
                info = json.loads(switch_connect.send_command('show interfaces %s switchport | json' % port))
                info = info['switchports'][port]['switchportInfo']
                assert info['mode'] == 'access', '%s is not an access port' % port
                saved_vlans[port] = info['accessVlanId']
                # a port that changes vlan restarts stp and discards for 20s before auto edge kicks
                # in; portfast makes these host facing ports forward at once
                if 'portfast' not in switch_connect.send_command('show running-config interfaces %s' % port):
                    portfast_ports.append(port)
                    switch_connect.send_config_set(['interface %s' % port, 'spanning-tree portfast'])
            switch_connect.send_config_set(['interface %s' % port, 'switchport access vlan %d' % vlan])
        for port in ports:
            assert wait_for(lambda: 'forwarding' in switch_connect.send_command('show spanning-tree interface %s' % port),
                            timeout=40, interval=1), '%s is not forwarding' % port

    yield access_vlan

    for port, vlan in saved_vlans.items():
        switch_connect.send_config_set(['interface %s' % port, 'switchport access vlan %d' % vlan])
    for port in portfast_ports:
        switch_connect.send_config_set(['interface %s' % port, 'default spanning-tree portfast'])
    for vlan in new_vlans:
        switch_connect.send_config_set(['no vlan %d' % vlan])
    switch_connect.disconnect()


def forward(connection, port, host='127.0.0.1'):
    '''
    Forwards a local port through the ssh `connection` to `host`:`port` on its far side, so the test
    reaches a dpu service whatever the dpu firewall and however the dpu is reached (the IPU ACC sits
    behind its IMC). Returns the local port and a function that stops forwarding.
    '''
    transport = connection.remote_conn.get_transport()
    listener = socket.socket()
    listener.bind(('127.0.0.1', 0))
    listener.listen(4)

    def pipe(src, dst):
        try:
            while data := src.recv(65536):
                dst.sendall(data)
        except OSError:
            pass
        finally:
            src.close()
            dst.close()

    def accept():
        while True:
            try:
                client, peer = listener.accept()
            except OSError:
                return
            channel = transport.open_channel('direct-tcpip', (host, port), peer)
            threading.Thread(target=pipe, args=(client, channel), daemon=True).start()
            threading.Thread(target=pipe, args=(channel, client), daemon=True).start()

    threading.Thread(target=accept, daemon=True).start()
    return listener.getsockname()[1], listener.close


def dpu_routing(dpu_connect, addresses):
    '''
    Makes the dpu a router between the `addresses` ({'200.0.0.1/24': interface}) and returns a
    function that undoes it. firewalld (the intel ipus run it) is stopped and started again.
    '''
    # a killed run skips the teardown; drop its 200-203.0.0.1 addresses, or their routes win
    dpu_connect.send_command('ip -4 addr flush to 200.0.0.0/6')
    for address, interface in addresses.items():
        dpu_connect.send_command('ip link set up dev %s' % interface)
        dpu_connect.send_command('ip addr add %s dev %s' % (address, interface))
    firewalld = dpu_connect.send_command('systemctl is-active firewalld').strip() == 'active'
    if firewalld:
        dpu_connect.send_command('systemctl stop firewalld')
    dpu_connect.send_command('sysctl net.ipv4.ip_forward=1')
    dpu_connect.send_command('iptables -P FORWARD ACCEPT')

    def undo():
        for address, interface in addresses.items():
            dpu_connect.send_command('ip addr del %s dev %s' % (address, interface))
        dpu_connect.send_command('ip neigh flush to 200.0.0.0/6 nud all')
        if firewalld:
            dpu_connect.send_command('systemctl start firewalld')

    return undo


def dpu_mac(dpu_connect, peer_ip):
    '''
    Returns the MAC of the dpu interface facing `peer_ip`, used as the flow destination so the
    dpu routes the traffic. The sf and hpf MACs change whenever the dpu is reflashed.
    '''
    route = dpu_connect.send_command('ip -o route get %s' % peer_ip)
    dev = route.split(' dev ')[1].split()[0]
    return dpu_connect.send_command('cat /sys/class/net/%s/address' % dev).strip()


def dpu_forwarded(dpu_connect):
    '''
    Returns the dpu's Ip ForwDatagrams counter, which grows only when the arm kernel routes a packet.
    '''
    names, values = [line.split() for line in dpu_connect.send_command('grep ^Ip: /proc/net/snmp').splitlines()]
    return int(values[names.index('ForwDatagrams')])


def wait_for(func, timeout=10, interval=0.2):
    '''
    Keeps calling the `func` until it returns true or `timeout` occurs
    every `interval` seconds.
    '''
    start = time.time()

    while time.time() - start <= timeout:
        if func():
            return True
        time.sleep(interval)

    print('Timeout occurred !')
    return False
