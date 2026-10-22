'''
IPsec demo: two CyPerf agents on the server reach each other through the dpu. The client agent
builds an IKEv2 tunnel to strongSwan on the dpu, which the test configures with the OPI IPsec gRPC
API (opi-strongswan-bridge), and the dpu routes the decrypted traffic to the server agent.

    client agent 200.0.0.2 == ipsec ==> 200.0.0.1 dpu 201.0.0.1 --> 201.0.0.2 server agent
    (inner 40.0.0.0/24)

The CyPerf controller takes an offline (refresh) token, never a password. Generate one in the
controller UI and put it in ~/.cyperf/offline-token (chmod 600) on the machine running the test,
or point CYPERF_TOKEN_FILE at it; the CYPERF_OFFLINE_TOKEN variable is read as well.
'''
import os
import sys
import cyperf
import grpc
import pytest
import urllib3
from pydpu.proto.v1 import ipsec_pb2
from pydpu.proto.v1 import ipsec_pb2_grpc

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from lab import *

DEPLOYMENT = '%s/demos/security/deployment/cyperf_with_ipsec.yml' % HOME_FOLDER
CYPERF_CONFIG = os.path.join(HOME_FOLDER, 'demos/security/cyperf-ipsec-config.zip')
CYPERF_TOKEN_FILE = os.environ.get('CYPERF_TOKEN_FILE', os.path.expanduser('~/.cyperf/offline-token'))
# the cyperf_with_ipsec.yml container hostnames, which is how the controller lists the agents
CYPERF_AGENTS = {'client': 'opi-cyperf-client', 'server': 'opi-cyperf-server'}
VICI_BRIDGE = 'ghcr.io/opiproject/opi-strongswan-bridge:main'
VICI_BRIDGE_PORT = 50151

# what differs per smartnic; the interfaces, switch ports and jump host come from testbed.DPUS
VARIANTS = {
    # strongSwan runs on the arm
    'nvidia': {'strongswan': 'strongswan'},
    # strongSwan runs on the ACC, which is only reachable through the IMC; the 2024 demo also set
    # the phy type on the IMC (iset-cli set-phy-capabilities), not needed while the links are up
    'intel': {'strongswan': 'strongswan'},
}

TUNNEL = ipsec_pb2.Connection(
    name='tun1_0_0',
    version='2',
    local_addrs=[ipsec_pb2.Addrs(addr='200.0.0.1')],
    remote_addrs=[ipsec_pb2.Addrs(addr='200.0.0.2')],
    local_auth=ipsec_pb2.LocalAuth(auth=ipsec_pb2.AUTH_TYPE_PSK, id='200.0.0.1'),
    remote_auth=ipsec_pb2.RemoteAuth(auth=ipsec_pb2.AUTH_TYPE_PSK, id='200.0.0.2'),
    children=[ipsec_pb2.Child(
        name='tun1_0_0',
        esp_proposals=ipsec_pb2.Proposals(
            crypto_alg=[ipsec_pb2.CRYPTO_ALGORITHM_AES128],
            integ_alg=[ipsec_pb2.INTEG_ALGORITHM_SHA1]
        ),
        # the cyperf config emulates 40.0.0.0/24 behind the client agent
        remote_ts=ipsec_pb2.TrafficSelectors(ts=[ipsec_pb2.TrafficSelectors.TrafficSelector(cidr='40.0.0.0/24')]),
        local_ts=ipsec_pb2.TrafficSelectors(ts=[ipsec_pb2.TrafficSelectors.TrafficSelector(cidr='201.0.0.0/24')]),
    )],
    proposals=ipsec_pb2.Proposals(
        crypto_alg=[ipsec_pb2.CRYPTO_ALGORITHM_AES128],
        integ_alg=[ipsec_pb2.INTEG_ALGORITHM_SHA384],
        dhgroups=[ipsec_pb2.DH_GROUPS_MODP1536]
    )
)


@pytest.fixture
def dpu(lab_dpu):
    variant = VARIANTS.get(lab_dpu['vendor'])
    if variant is None:
        pytest.skip('%s: no ipsec recipe for %s dpus yet' % (lab_dpu['name'], lab_dpu['vendor']))
    if not lab_dpu['switch_ports']:
        pytest.skip('%s: not cabled to the A100G' % lab_dpu['name'])
    dpu_connect = connect_or_skip(lab_dpu['ip'], lab_dpu.get('jump'), lab_dpu['name'])
    interfaces = lab_dpu['interfaces']
    undo = dpu_routing(dpu_connect, {'200.0.0.1/24': interfaces[0], '201.0.0.1/24': interfaces[1]})

    # the bridge drives charon through its vici socket in /var/run
    if 'charon.vici' not in dpu_connect.send_command('ls /var/run'):
        dpu_connect.send_command('systemctl start %s' % variant['strongswan'])
    assert wait_for(lambda: 'charon.vici' in dpu_connect.send_command('ls /var/run'), timeout=30, interval=1), \
        '%s: strongSwan (charon) is not running' % lab_dpu['name']
    runtime = 'docker' if 'docker' in dpu_connect.send_command('command -v docker') else 'podman'
    dpu_connect.send_command('systemctl start %s' % runtime)
    dpu_connect.send_command('%s rm -f opi-strongswan-bridge' % runtime)
    output = dpu_connect.send_command('%s run --rm -d --network host --mount src=/var/run,target=/var/run,type=bind '
                                      '--name opi-strongswan-bridge %s /opi-vici-bridge -port=%d'
                                      % (runtime, VICI_BRIDGE, VICI_BRIDGE_PORT), read_timeout=120)
    print(output)
    # the grpc port goes through the ssh session, so neither the dpu firewall nor the IMC hop matter
    port, stop_forward = forward(dpu_connect, VICI_BRIDGE_PORT)
    channel = grpc.insecure_channel('127.0.0.1:%d' % port)
    grpc.channel_ready_future(channel).result(timeout=30)

    yield ipsec_pb2_grpc.IPsecServiceStub(channel)

    channel.close()
    stop_forward()
    dpu_connect.send_command('%s stop opi-strongswan-bridge' % runtime)
    undo()
    dpu_connect.disconnect()


@pytest.fixture(scope='session')
def cyperf_api():
    token = os.environ.get('CYPERF_OFFLINE_TOKEN')
    if not token and os.path.exists(CYPERF_TOKEN_FILE):
        token = open(CYPERF_TOKEN_FILE).read().strip()
    if not token:
        pytest.skip('no CyPerf offline token in %s or CYPERF_OFFLINE_TOKEN' % CYPERF_TOKEN_FILE)
    urllib3.disable_warnings()
    configuration = cyperf.Configuration(host='https://%s' % CYPERF_IP, refresh_token=token)
    configuration.verify_ssl = False
    with cyperf.ApiClient(configuration) as api:
        try:
            cyperf.AgentsApi(api).get_agents()
        except (urllib3.exceptions.HTTPError, OSError) as e:
            pytest.skip('the CyPerf controller %s does not answer: %s' % (CYPERF_IP, e))

        yield api


@pytest.fixture(scope='session')
def agents(cyperf_api):
    '''
    Starts the client and server agents on the server, each owning one server port, and returns
    {'client': (agent, interface), 'server': (agent, interface)} once the controller lists them.
    '''
    server_connect = connect(TGEN1_IP)
    output = server_connect.send_command('docker compose --progress plain -f %s up -d' % DEPLOYMENT, read_timeout=120)
    print(output)
    interfaces = dict(zip(CYPERF_AGENTS, TGEN1_INTERFACES))
    for role, interface in interfaces.items():
        container = 'cyperf-%s' % role
        pid = server_connect.send_command("docker inspect -f '{{.State.Pid}}' %s" % container).strip()
        server_connect.send_command('ip link set %s netns %s' % (interface, pid))
        output = server_connect.send_command(
            'docker exec %s bash -c "cyperfagent interface test set %s; ip link set up dev %s; '
            'cyperfagent controller set %s --skip-identity-verification"'
            % (container, interface, interface, CYPERF_IP), read_timeout=60)
        print(output)

    agents_api = cyperf.AgentsApi(cyperf_api)
    online = {}

    def registered():
        online.update({agent.hostname: agent for agent in agents_api.get_agents(exclude_offline='true')})
        return all(hostname in online for hostname in CYPERF_AGENTS.values())

    assert wait_for(registered, timeout=180, interval=5), 'The CyPerf agents did not register with %s!' % CYPERF_IP

    yield {role: (online[hostname], interfaces[role]) for role, hostname in CYPERF_AGENTS.items()}

    # compose down hands the ports back to the server once the agent namespaces are gone
    output = server_connect.send_command('docker compose --progress plain -f %s down' % DEPLOYMENT, read_timeout=120)
    print(output)
    server_connect.disconnect()


def test_ipsec_api(dpu):
    # the OPI ipsec api alone, which runs without the CyPerf controller
    print(dpu.IPsecVersion(ipsec_pb2.IPsecVersionRequest()))
    dpu.IPsecLoadConn(ipsec_pb2.IPsecLoadConnRequest(connection=TUNNEL))
    try:
        print(dpu.IPsecStats(ipsec_pb2.IPsecStatsRequest()))
    finally:
        dpu.IPsecUnloadConn(ipsec_pb2.IPsecUnloadConnRequest(name=TUNNEL.name))


def test_server_to_server_via_ipsec_and_dpu(lab_dpu, cyperf_api, agents, dpu, switch):
    switch(A100G_VLANS[0], [A100G_TGEN1_PORTS[0], lab_dpu['switch_ports'][0]])
    switch(A100G_VLANS[1], [A100G_TGEN1_PORTS[1], lab_dpu['switch_ports'][1]])

    print(dpu.IPsecVersion(ipsec_pb2.IPsecVersionRequest()))
    print(dpu.IPsecStats(ipsec_pb2.IPsecStatsRequest()))

    print('configuring the tunnel')
    dpu.IPsecLoadConn(ipsec_pb2.IPsecLoadConnRequest(connection=TUNNEL))
    try:
        test = run_cyperf(cyperf_api, {'IP Network 1': agents['client'], 'IP Network 2': agents['server']}, duration=30)
        print(dpu.IPsecStats(ipsec_pb2.IPsecStatsRequest()))
        verify_stats(cyperf_api, test)
    finally:
        dpu.IPsecUnloadConn(ipsec_pb2.IPsecUnloadConnRequest(name=TUNNEL.name))


def run_cyperf(api, assignments, duration):
    '''
    Runs the CyPerf config with the `assignments` ({segment name: (agent, interface)}) for
    `duration` seconds of sustain time and returns the finished test.
    '''
    configs_api = cyperf.ConfigurationsApi(api)
    sessions_api = cyperf.SessionsApi(api)
    operations_api = cyperf.TestOperationsApi(api)
    config = configs_api.start_configs_import(CYPERF_CONFIG).await_completion()[0]
    session = sessions_api.create_sessions([cyperf.Session(config_url=config['configUrl'])])[0]
    try:
        session_config = sessions_api.get_session_config(session_id=session.id, include='Config, TrafficProfiles').config
        for segment in session_config.network_profiles[0].ip_network_segment:
            agent, interface = assignments[segment.name]
            segment.agent_assignments = cyperf.AgentAssignments(by_id=[cyperf.AgentAssignmentDetails(
                agent_id=agent.id, id=agent.id, interfaces=[interface])])
            segment.update()
        objective = session_config.traffic_profiles[0].objectives_and_timeline.primary_objective
        objective.timeline[1].duration = duration
        objective.update()

        print('Starting the CyPerf test ...')
        operations_api.start_test_run_start(session_id=session.id).await_completion()
        test = None

        def stopped():
            nonlocal test
            test = sessions_api.get_session_test(session_id=session.id)
            print('CyPerf test %s: %s of %s s' % (test.status, test.test_elapsed, test.test_duration))
            return test.status == 'STOPPED'

        if not wait_for(stopped, timeout=duration + 300, interval=5):
            operations_api.start_test_run_stop(session_id=session.id).await_completion()
            pytest.fail('The CyPerf test did not stop on its own!')
        assert test.test_elapsed >= test.test_duration, 'The CyPerf test stopped after %s of %s s!' % (
            test.test_elapsed, test.test_duration)
        return test
    finally:
        sessions_api.delete_session(session.id)
        configs_api.delete_config(config['id'])


def stat_rows(api, test, name):
    '''
    Returns the last snapshot of the `name` statistic as one {column: value} dict per row.
    '''
    stats_api = cyperf.StatisticsApi(api)
    names = [stat.name for stat in stats_api.get_result_stats(test.test_id) if name in stat.name]
    assert names, 'No %s statistic!' % name
    stat = stats_api.get_result_stat_by_id(test.test_id, names[0])
    assert stat.snapshots, 'The %s statistic is empty!' % name
    return [dict(zip(stat.columns, [cell.actual_instance for cell in row])) for row in stat.snapshots[-1].values]


def verify_stats(api, test):
    tunnels = stat_rows(api, test, 'ipsec-tunnels-total')
    print(tunnels)
    for row in tunnels:
        assert int(row['Sessions Failed']) == 0 and int(row['Sessions Initiated']) == int(row['Sessions Succeeded']), \
            'IPsec tunnels failed: %s' % row
        assert int(row['Sessions Succeeded']) > 0, 'No IPsec tunnel came up: %s' % row

    actions = stat_rows(api, test, 'client-action-statistics')
    print(actions)
    for row in actions:
        assert int(row['Action Failed']) == 0 and int(row['Action Started']) == int(row['Action Succeeded']), \
            'Client actions failed: %s' % row
