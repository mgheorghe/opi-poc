import json
import os
import sys
import netmiko
import paramiko
import pytest
import snappi

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from testbed import *

# repo checkout used for the docker compose files, the CI workspace or this clone
HOME_FOLDER = os.environ.get('GITHUB_WORKSPACE',
                             os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
# private key used to ssh as root into the server, dpu and dpu host
SSH_KEY = os.environ.get('OPI_SSH_KEY', os.path.expanduser('~/.ssh/id_rsa'))

# systemd >= 257 (Ubuntu 26.04) wraps every shell prompt in OSC 3008 escapes with a fresh uuid,
# which netmiko cannot match; its profile script skips TERM=dumb, but netmiko asks for vt100
_invoke_shell = paramiko.SSHClient.invoke_shell
paramiko.SSHClient.invoke_shell = lambda self, term='vt100', *args, **kwargs: \
    _invoke_shell(self, 'dumb', *args, **kwargs)


@pytest.fixture
def dpu():
    dpu_info = {
        'device_type': 'linux',
        'host': BF2_IP,
        'username': 'root',
        'use_keys': True,
        'key_file': SSH_KEY
    }
    dpu_connect = netmiko.ConnectHandler(**dpu_info)
    #prompt = dpu_connect.find_prompt()
    # a killed run skips the teardown; drop its 200-203.0.0.1 addresses, or their routes win
    dpu_connect.send_command('ip -4 addr flush to 200.0.0.0/6')
    dpu_connect.send_command('ip addr add 200.0.0.1/24 dev %s' % BF2_INTERFACES[0])
    dpu_connect.send_command('ip addr add 201.0.0.1/24 dev %s' % BF2_INTERFACES[1])
    # pf0hpf/pf1hpf are ovs ports, so the arm kernel never receives on them; the sf on the same
    # ovs bridge is the arm's l3 interface towards each host pf
    dpu_connect.send_command('ip addr add 202.0.0.1/24 dev %s' % BF2_INTERFACES[1])
    dpu_connect.send_command('ip addr add 203.0.0.1/24 dev %s' % BF2_INTERFACES[0])
    dpu_connect.send_command('sysctl net.ipv4.ip_forward=1')
    dpu_connect.send_command('iptables -P FORWARD ACCEPT')
    dpu_connect.send_command('arp -s 200.0.0.2 80:09:02:02:00:01')
    dpu_connect.send_command('arp -s 201.0.0.2 80:09:02:02:00:02')
    dpu_connect.send_command('arp -s 202.0.0.2 80:09:02:02:00:03')
    dpu_connect.send_command('arp -s 203.0.0.2 80:09:02:02:00:04')
    # idealy replace as many of those ssh commands with OPI API as they become available

    # iptables -P INPUT ACCEPT
    # iptables -P FORWARD ACCEPT
    # iptables -P OUTPUT ACCEPT
    # iptables -t nat -F
    # iptables -t mangle -F
    # iptables -F
    # iptables -X

    yield dpu_connect

    dpu_connect.send_command('ip addr del 200.0.0.1/24 dev %s' % BF2_INTERFACES[0])
    dpu_connect.send_command('ip addr del 201.0.0.1/24 dev %s' % BF2_INTERFACES[1])
    dpu_connect.send_command('ip addr del 202.0.0.1/24 dev %s' % BF2_INTERFACES[1])
    dpu_connect.send_command('ip addr del 203.0.0.1/24 dev %s' % BF2_INTERFACES[0])
    dpu_connect.send_command('ip neigh flush 200.0.0.0/8')
    dpu_connect.send_command('ip neigh flush 201.0.0.0/8')
    dpu_connect.send_command('ip neigh flush 202.0.0.0/8')
    dpu_connect.send_command('ip neigh flush 203.0.0.0/8')
    dpu_connect.disconnect()


@pytest.fixture
def server():
    server_info = {
        'device_type': 'linux',
        'host': TGEN1_IP,
        'username': 'root',
        'use_keys': True,
        'key_file': SSH_KEY
    }
    server_connect = netmiko.ConnectHandler(**server_info)
    output = server_connect.send_command('docker compose -f %s/demos/tgen/deployment/tgen.yml up -d' % HOME_FOLDER, read_timeout=30)
    print(output)

    yield server_connect

    output = server_connect.send_command('docker compose -f %s/demos/tgen/deployment/tgen.yml down' % HOME_FOLDER, read_timeout=30)
    print(output)
    server_connect.disconnect()


@pytest.fixture
def host():
    # needs reboot 
    # mst start
    # mlxconfig -d /dev/mst/mt41686_pciconf0 s INTERNAL_CPU_MODEL=1
    # mlxconfig -d /dev/mst/mt41686_pciconf0.1 s INTERNAL_CPU_MODEL=1
    # mlxconfig -d /dev/mst/mt41686_pciconf0 s INTERNAL_CPU_MODEL=0
    # mlxconfig -d /dev/mst/mt41686_pciconf0.1 s INTERNAL_CPU_MODEL=0
    host_info = {
        'device_type': 'linux',
        'host': DH2_IP,
        'username': 'root',
        'use_keys': True,
        'key_file': SSH_KEY
    }
    host_connect = netmiko.ConnectHandler(**host_info)

    scp_conn = netmiko.SCPConn(host_connect)
    scp_conn.scp_put_file('%s/demos/tgen/deployment/tgen.yml' % HOME_FOLDER, '~/tgen.yaml')
    scp_conn.scp_put_file('%s/demos/tgen/deployment/.env' % HOME_FOLDER, '~/.env')

    output = host_connect.send_command('docker compose -f ~/tgen.yaml up -d', read_timeout=30)
    print(output)

    yield host_connect

    output = host_connect.send_command('docker compose -f ~/tgen.yaml down', read_timeout=30)
    print(output)
    host_connect.disconnect()


@pytest.fixture
def switch():
    '''
    Yields a function that moves switch ports into a vlan, so each test wires the tgen ports to the
    dpu ports it needs. The original vlans are restored afterwards; the config is never saved.
    '''
    switch_info = {
        'device_type': 'arista_eos',
        'host': A100G_IP,
        'username': 'arista',
        'use_keys': True,
        'key_file': SSH_KEY
    }
    switch_connect = netmiko.ConnectHandler(**switch_info)
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


def test_server_to_server_via_dpu(dpu, server, switch):
    # server:p2 reaches the dpu on 201.0.0.0/24, the dpu routes it back to server:p1 on 200.0.0.0/24
    switch(A100G_VLANS[0], [A100G_TGEN1_PORTS[0], A100G_BF2_PORTS[0]])
    switch(A100G_VLANS[1], [A100G_TGEN1_PORTS[1], A100G_BF2_PORTS[1]])

    tgen = snappi.api(location=f'https://{TGEN1_IP}:8443', verify=False)
    cfg = tgen.config()
    p1 = cfg.ports.port(name='server:p1', location=f'{TGEN1_IP}:5555')[-1]
    p2 = cfg.ports.port(name='server:p2', location=f'{TGEN1_IP}:5556')[-1]

    # add layer 1 property to configure same speed on both ports
    ly = cfg.layer1.layer1(name='ly')[-1]
    ly.port_names = [p1.name, p2.name]
    ly.speed = ly.SPEED_10_GBPS

    # enable packet capture on both ports
    cp = cfg.captures.capture(name='cp')[-1]
    cp.port_names = [p1.name, p2.name]

    flow = cfg.flows.flow(name='flow server:p2 -> server:p1')[-1]
    flow.tx_rx.port.tx_name = p2.name
    flow.tx_rx.port.rx_names = [p1.name]
    flow.size.fixed = 256
    flow.duration.fixed_packets.packets = 1000
    flow.rate.pps = 1000
    eth2, ip2, udp2 = flow.packet.ethernet().ipv4().udp()
    eth2.src.value = '00:1B:6E:00:00:01'
    eth2.dst.value = dpu_mac(dpu, '201.0.0.2')
    ip2.src.value = '201.0.0.2'
    ip2.dst.value = '200.0.0.2'
    inc2 = udp2.src_port.increment
    inc2.start, inc2.step, inc2.count = 6000, 4, 10
    udp2.dst_port.values = [8000, 8044, 8060, 8074, 8082, 8084]

    print('Pushing traffic configuration ...')
    tgen.set_config(cfg)

    print('Starting transmit on all configured flows ...')
    forwarded = dpu_forwarded(dpu)
    cs = tgen.control_state()
    cs.traffic.flow_transmit.state = cs.traffic.flow_transmit.START
    tgen.set_control_state(cs)

    #import pdb
    #pdb.set_trace()

    print('Checking metrics on all configured ports ...')
    print('Expected\tTotal Tx\tTotal Rx')
    assert wait_for(lambda: metrics_ok(tgen)), 'Metrics validation failed!'
    # the frames must have been routed by the dpu, not looped back through the switch
    assert dpu_forwarded(dpu) - forwarded >= flow.duration.fixed_packets.packets, 'The dpu did not route the traffic!'


def test_server_to_dpuhost_via_dpu(dpu, server, host, switch):
    # server:p1 reaches the dpu on 200.0.0.0/24, the dpu routes it to host:p1 through ovsbr1 and pf0hpf
    switch(A100G_VLANS[0], [A100G_TGEN1_PORTS[1], A100G_BF2_PORTS[0]])

    tgen = snappi.api(location=f'https://{TGEN1_IP}:8443', verify=False)
    cfg = tgen.config()
    p1 = cfg.ports.port(name='host:p1', location=f'{DH2_IP}:5555')[-1]
    p2 = cfg.ports.port(name='server:p1', location=f'{TGEN1_IP}:5556')[-1]

    # add layer 1 property to configure same speed on both ports
    ly = cfg.layer1.layer1(name='ly')[-1]
    ly.port_names = [p1.name, p2.name]
    ly.speed = ly.SPEED_10_GBPS

    # enable packet capture on both ports
    cp = cfg.captures.capture(name='cp')[-1]
    cp.port_names = [p1.name, p2.name]

    flow = cfg.flows.flow(name='flow server:p2 -> host:p1')[-1]
    flow.tx_rx.port.tx_name = p2.name
    flow.tx_rx.port.rx_names = [p1.name]
    flow.size.fixed = 256
    flow.duration.fixed_packets.packets = 1000
    flow.rate.pps = 1000
    eth2, ip2, udp2 = flow.packet.ethernet().ipv4().udp()
    eth2.src.value = '00:1B:6E:00:00:01'
    eth2.dst.value = dpu_mac(dpu, '200.0.0.2')
    ip2.src.value = '200.0.0.2'
    ip2.dst.value = '202.0.0.2'
    inc2 = udp2.src_port.increment
    inc2.start, inc2.step, inc2.count = 6000, 4, 10
    udp2.dst_port.values = [8000, 8044, 8060, 8074, 8082, 8084]

    print('Pushing traffic configuration ...')
    tgen.set_config(cfg)

    print('Starting transmit on all configured flows ...')
    forwarded = dpu_forwarded(dpu)
    cs = tgen.control_state()
    cs.traffic.flow_transmit.state = cs.traffic.flow_transmit.START
    tgen.set_control_state(cs)

    print('Checking metrics on all configured ports ...')
    print('Expected\tTotal Tx\tTotal Rx')
    assert wait_for(lambda: metrics_ok(tgen)), 'Metrics validation failed!'
    # the frames must have been routed by the dpu, not looped back through the switch
    assert dpu_forwarded(dpu) - forwarded >= flow.duration.fixed_packets.packets, 'The dpu did not route the traffic!'


def test_dpuhost_to_dpuhost_via_dpu(dpu, host, switch):
    # host:p2 reaches the dpu on 203.0.0.0/24, the dpu routes it to host:p1 on 202.0.0.0/24; ovs
    # floods the routed frames out the uplinks too, so park each uplink alone in a vlan
    switch(A100G_VLANS[0], [A100G_BF2_PORTS[0]])
    switch(A100G_VLANS[1], [A100G_BF2_PORTS[1]])

    tgen = snappi.api(location=f'https://{DH2_IP}:8443', verify=False)
    cfg = tgen.config()
    p1 = cfg.ports.port(name='host:p1', location=f'{DH2_IP}:5555')[-1]
    p2 = cfg.ports.port(name='host:p2', location=f'{DH2_IP}:5556')[-1]

    # add layer 1 property to configure same speed on both ports
    ly = cfg.layer1.layer1(name='ly')[-1]
    ly.port_names = [p1.name, p2.name]
    ly.speed = ly.SPEED_10_GBPS

    # enable packet capture on both ports
    cp = cfg.captures.capture(name='cp')[-1]
    cp.port_names = [p1.name, p2.name]

    flow = cfg.flows.flow(name='flow host:p2 -> host:p1')[-1]
    flow.tx_rx.port.tx_name = p2.name
    flow.tx_rx.port.rx_names = [p1.name]
    flow.size.fixed = 256
    flow.duration.fixed_packets.packets = 1000
    flow.rate.pps = 1000
    eth2, ip2, udp2 = flow.packet.ethernet().ipv4().udp()
    eth2.src.value = '00:1B:6E:00:00:01'
    eth2.dst.value = dpu_mac(dpu, '203.0.0.2')
    ip2.src.value = '203.0.0.2'
    ip2.dst.value = '202.0.0.2'
    inc2 = udp2.src_port.increment
    inc2.start, inc2.step, inc2.count = 6000, 4, 10
    udp2.dst_port.values = [8000, 8044, 8060, 8074, 8082, 8084]

    print('Pushing traffic configuration ...')
    tgen.set_config(cfg)

    print('Starting transmit on all configured flows ...')
    forwarded = dpu_forwarded(dpu)
    cs = tgen.control_state()
    cs.traffic.flow_transmit.state = cs.traffic.flow_transmit.START
    tgen.set_control_state(cs)

    print('Checking metrics on all configured ports ...')
    print('Expected\tTotal Tx\tTotal Rx')
    assert wait_for(lambda: metrics_ok(tgen)), 'Metrics validation failed!'
    # the frames must have been routed by the dpu, not looped back through the switch
    assert dpu_forwarded(dpu) - forwarded >= flow.duration.fixed_packets.packets, 'The dpu did not route the traffic!'


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


def metrics_ok(api):
    # create a port metrics request and filter based on port names
    cfg = api.get_config()

    req = api.metrics_request()
    req.port.port_names = [p.name for p in cfg.ports]
    # include only sent and received packet counts
    req.port.column_names = [req.port.FRAMES_TX, req.port.FRAMES_RX]
    # fetch port metrics
    res = api.get_metrics(req)
    # calculate total frames sent across all ports and received on the flows' rx ports only, so
    # frames that loop back to the sender do not count as delivered
    rx_ports = {n for f in cfg.flows for n in f.tx_rx.port.rx_names}
    total_tx = sum([m.frames_tx for m in res.port_metrics])
    total_rx = sum([m.frames_rx for m in res.port_metrics if m.name in rx_ports])
    expected = sum([f.duration.fixed_packets.packets for f in cfg.flows])

    print('%d\t\t%d\t\t%d' % (expected, total_tx, total_rx))

    return expected == total_tx and total_rx >= expected


def wait_for(func, timeout=10, interval=0.2):
    '''
    Keeps calling the `func` until it returns true or `timeout` occurs
    every `interval` seconds.
    '''
    import time

    start = time.time()

    while time.time() - start <= timeout:
        if func():
            return True
        time.sleep(interval)

    print('Timeout occurred !')
    return False
