# from https://github.com/opiproject/lab/blob/main/Documentation/ips.md

# DPU HOST 1
DH1_IP = '172.22.1.1'
DH1_INTERFACES = ['ens1f0np0', 'ens1f1np1']

# AMD/Pensando
PEN_IP = '172.22.3.1'
PEN_INTERFACES = ['enp3s0f1s0', 'enp3s0f0s0']

# DPU HOST 2
DH2_IP = '172.22.1.2'
DH2_INTERFACES = ['ens1f0np0', 'ens1f1np1']

# Nvidia BlueField2
BF2_IP = '172.22.3.2'
BF2_INTERFACES = ['enp3s0f1s0', 'enp3s0f0s0']

# DPU HOST 3
DH3_IP = '172.22.1.3'
#DH3_INTERFACES = ['ens1f0np0', 'ens1f1np1']

# Marvell OCTEON CN106, console only (dh3 ttyUSB0) today
MV_CN106_IP = '172.22.3.3'

# DPU HOST 4
DH4_IP = '172.22.1.4'
DH4_INTERFACES = ['ens2f0', 'ens2f0d1']  # not verified, the E2100 host ports were renamed ens2f0*

# Intel IPU E2100: the ACC is reached through the IMC
IMC_IP = '172.22.4.4'
ACC_IP = '192.168.0.2'
ACC_INTERFACES = ['enp0s1f0d1', 'enp0s1f0d2']

# DPU HOST 5
DH5_IP = '172.22.1.5'
DH5_INTERFACES = ['ens2f0np0', 'ens2f1np1']

# Nvidia BlueField3, assumed to have the BF2 sf layout
BF3_IP = '172.22.3.5'
BF3_INTERFACES = ['enp3s0f1s0', 'enp3s0f0s0']

# DPU HOST 9
DH9_IP = '172.22.1.9'

# Senao SX904 (Intel NetSec Accelerator) in dh9
SX904_IP = '172.22.3.9'
SX904_INTERFACES = ['enp244s0f0np0', 'enp244s0f1np1']

# TGEN SERVER 1
TGEN1_IP = '172.22.1.100'

TGEN1_INTERFACES = ['ens1f0np0', 'ens1f1np1']
#TGEN1_INTERFACES = ['enp138s0f0np0', 'enp138s0f1np1']

# Arista 100G switch between the tgen servers and the dpus
A100G_IP = '172.22.1.250'
A100G_TGEN1_PORTS = ['Ethernet25/1', 'Ethernet26/1']  # TGEN1_INTERFACES
A100G_BF2_PORTS = ['Ethernet4/1', 'Ethernet3/1']  # BF2 p1, p0, facing BF2_INTERFACES
A100G_BF3_PORTS = ['Ethernet10/1', 'Ethernet9/1']  # BF3 p1, p0, facing BF3_INTERFACES
A100G_E2100_PORTS = ['Ethernet7/1', 'Ethernet8/1']  # E2100 phy 0, 1, learned from the ACC vport MACs
# free vlans the tests create to pair a tgen port with a dpu port
A100G_VLANS = [3001, 3002]

# Every dpu and ipu in the lab, and what the tests need to reach and wire it. `interfaces[i]` is
# the dpu's l3 interface behind switch port `switch_ports[i]`; on the nvidia dpus `interfaces[1]`
# also reaches `host_interfaces[0]` and `interfaces[0]` reaches `host_interfaces[1]`. `jump` is the
# host to ssh through, and `skip` says why a dpu cannot run yet.
DPUS = {
    'bf2': {'vendor': 'nvidia', 'ip': BF2_IP, 'interfaces': BF2_INTERFACES, 'switch_ports': A100G_BF2_PORTS,
            'host': DH2_IP, 'host_interfaces': DH2_INTERFACES},
    'bf3': {'vendor': 'nvidia', 'ip': BF3_IP, 'interfaces': BF3_INTERFACES, 'switch_ports': A100G_BF3_PORTS,
            'host': DH5_IP, 'host_interfaces': DH5_INTERFACES},
    'e2100': {'vendor': 'intel', 'ip': ACC_IP, 'jump': IMC_IP, 'interfaces': ACC_INTERFACES,
              'switch_ports': A100G_E2100_PORTS, 'host': DH4_IP, 'host_interfaces': DH4_INTERFACES},
    'dsc2': {'vendor': 'pensando', 'ip': PEN_IP, 'interfaces': PEN_INTERFACES, 'switch_ports': None,
             'host': DH1_IP, 'host_interfaces': DH1_INTERFACES,
             'skip': 'the dsc2 data ports are down and its oob port sends nothing'},
    'cn106': {'vendor': 'marvell', 'ip': MV_CN106_IP, 'interfaces': None, 'switch_ports': None,
              'host': DH3_IP, 'host_interfaces': None,
              'skip': 'the cn106 has no management network, only the dh3 serial console'},
    'sx904': {'vendor': 'intel', 'ip': SX904_IP, 'interfaces': SX904_INTERFACES, 'switch_ports': None,
              'host': DH9_IP, 'host_interfaces': None,
              'skip': 'the sx904 data ports are down and not cabled to the A100G'},
}

# CYPERF SERVER
CYPERF_IP = '172.22.222.9'
