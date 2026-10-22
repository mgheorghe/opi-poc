import functools
import os
import sys
import pytest
import snappi

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from lab import *


@pytest.fixture
def dpu(lab_dpu):
    if not lab_dpu['switch_ports']:
        pytest.skip('%s: not cabled to the A100G' % lab_dpu['name'])
    dpu_connect = connect_or_skip(lab_dpu['ip'], lab_dpu.get('jump'), lab_dpu['name'])
    interfaces = lab_dpu['interfaces']
    # on the nvidia dpus pf0hpf/pf1hpf are ovs ports, so the arm kernel never receives on them; the
    # sf on the same ovs bridge is the arm's l3 interface towards each host pf
    undo = dpu_routing(dpu_connect, {
        '200.0.0.1/24': interfaces[0],
        '201.0.0.1/24': interfaces[1],
        '202.0.0.1/24': interfaces[1],
        '203.0.0.1/24': interfaces[0],
    })
    # the traffic is one way, so give the dpu a next hop mac for each tgen address
    dpu_connect.send_command('ip neigh replace 200.0.0.2 lladdr 80:09:02:02:00:01 dev %s nud permanent' % interfaces[0])
    dpu_connect.send_command('ip neigh replace 201.0.0.2 lladdr 80:09:02:02:00:02 dev %s nud permanent' % interfaces[1])
    dpu_connect.send_command('ip neigh replace 202.0.0.2 lladdr 80:09:02:02:00:03 dev %s nud permanent' % interfaces[1])
    dpu_connect.send_command('ip neigh replace 203.0.0.2 lladdr 80:09:02:02:00:04 dev %s nud permanent' % interfaces[0])
    # idealy replace as many of those ssh commands with OPI API as they become available

    yield dpu_connect

    undo()
    dpu_connect.disconnect()


@pytest.fixture
def server():
    server_connect = connect(TGEN1_IP)
    output = server_connect.send_command('docker compose -f %s/demos/tgen/deployment/tgen.yml up -d' % HOME_FOLDER, read_timeout=30)
    print(output)
    wait_for_controller(server_connect, '%s/demos/tgen/deployment/tgen.yml' % HOME_FOLDER)

    yield server_connect

    output = server_connect.send_command('docker compose -f %s/demos/tgen/deployment/tgen.yml down' % HOME_FOLDER, read_timeout=30)
    print(output)
    server_connect.disconnect()


@pytest.fixture
def host(lab_dpu):
    # needs reboot 
    # mst start
    # mlxconfig -d /dev/mst/mt41686_pciconf0 s INTERNAL_CPU_MODEL=1
    # mlxconfig -d /dev/mst/mt41686_pciconf0.1 s INTERNAL_CPU_MODEL=1
    # mlxconfig -d /dev/mst/mt41686_pciconf0 s INTERNAL_CPU_MODEL=0
    # mlxconfig -d /dev/mst/mt41686_pciconf0.1 s INTERNAL_CPU_MODEL=0
    if lab_dpu['vendor'] != 'nvidia':
        pytest.skip('%s: the path from the dpu to its host is only mapped for the nvidia dpus' % lab_dpu['name'])
    host_connect = connect_or_skip(lab_dpu['host'], what='%s host' % lab_dpu['name'])

    scp_conn = netmiko.SCPConn(host_connect)
    scp_conn.scp_put_file('%s/demos/tgen/deployment/tgen.yml' % HOME_FOLDER, '~/tgen.yaml')
    scp_conn.scp_put_file('%s/demos/tgen/deployment/.env' % HOME_FOLDER, '~/.env')
    # the host pf names differ per dpu host, the shell environment wins over .env
    compose = 'IFC1=%s IFC2=%s docker compose -f ~/tgen.yaml' % tuple(lab_dpu['host_interfaces'])

    output = host_connect.send_command('%s up -d' % compose, read_timeout=30)
    print(output)
    wait_for_controller(host_connect, '~/tgen.yaml')

    yield host_connect

    output = host_connect.send_command('%s down' % compose, read_timeout=30)
    print(output)
    host_connect.disconnect()


def test_server_to_server_via_dpu(lab_dpu, dpu, server, switch):
    # server:p2 reaches the dpu on 201.0.0.0/24, the dpu routes it back to server:p1 on 200.0.0.0/24
    switch(A100G_VLANS[0], [A100G_TGEN1_PORTS[0], lab_dpu['switch_ports'][0]])
    switch(A100G_VLANS[1], [A100G_TGEN1_PORTS[1], lab_dpu['switch_ports'][1]])

    tgen = tgen_api(f'https://{TGEN1_IP}:8443')
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


def test_server_to_dpuhost_via_dpu(lab_dpu, host, dpu, server, switch):
    # server:p1 reaches the dpu on 200.0.0.0/24, the dpu routes it to host:p1 through ovsbr1 and pf0hpf
    switch(A100G_VLANS[0], [A100G_TGEN1_PORTS[1], lab_dpu['switch_ports'][0]])

    tgen = tgen_api(f'https://{TGEN1_IP}:8443')
    cfg = tgen.config()
    p1 = cfg.ports.port(name='host:p1', location=f'{lab_dpu["host"]}:5555')[-1]
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


def test_dpuhost_to_dpuhost_via_dpu(lab_dpu, host, dpu, switch):
    # host:p2 reaches the dpu on 203.0.0.0/24, the dpu routes it to host:p1 on 202.0.0.0/24; ovs
    # floods the routed frames out the uplinks too, so park each uplink alone in a vlan
    switch(A100G_VLANS[0], [lab_dpu['switch_ports'][0]])
    switch(A100G_VLANS[1], [lab_dpu['switch_ports'][1]])

    tgen = tgen_api(f'https://{lab_dpu["host"]}:8443')
    cfg = tgen.config()
    p1 = cfg.ports.port(name='host:p1', location=f'{lab_dpu["host"]}:5555')[-1]
    p2 = cfg.ports.port(name='host:p2', location=f'{lab_dpu["host"]}:5556')[-1]

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


def wait_for_controller(connect, compose_file):
    '''
    Waits until the controller has registered with the usage reporter. A set_config sent before
    that is applied to the ports but never answered.
    '''
    assert wait_for(lambda: 'App usage reporting service is up' in connect.send_command(
        'docker compose -f %s logs controller' % compose_file), timeout=60, interval=1), 'The controller did not come up!'


def tgen_api(location):
    '''
    Returns a snappi api whose http requests time out, so a request the controller never answers
    fails the test instead of hanging it. snappi sets no timeout on the http transport.
    '''
    tgen = snappi.api(location=location, verify=False)
    tgen._transport._session.request = functools.partial(tgen._transport._session.request, timeout=60)
    return tgen


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
