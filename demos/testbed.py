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

# TGEN SERVER 1
TGEN1_IP = '172.22.1.100'

TGEN1_INTERFACES = ['ens1f0np0', 'ens1f1np1']
#TGEN1_INTERFACES = ['enp138s0f0np0', 'enp138s0f1np1']

# Arista 100G switch between the tgen servers and the dpus
A100G_IP = '172.22.1.250'
A100G_TGEN1_PORTS = ['Ethernet25/1', 'Ethernet26/1']  # TGEN1_INTERFACES
A100G_BF2_PORTS = ['Ethernet3/1', 'Ethernet4/1']  # BF2 p0, p1
# free vlans the tests create to pair a tgen port with a dpu port
A100G_VLANS = [3001, 3002]

# CYPERF SERVER
CYPERF_IP = '172.22.222.9'
