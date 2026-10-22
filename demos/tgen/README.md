# OPI testing demo/poc

## hardware

- server with Ubuntu 22.04
  - Nvidia BlueField2
- server with Ubuntu 22.04
  - 100G NIC

## topologies

### covered

any combination of host or server traffic originated to any of the 4 ports and targeted to any of the 4 ports (it could come back to itself)
![testbed diagram](./images/opi-lab-scenarios.drawio.svg)

server to dpu, dpu forwarding to the other port and back to the server
![test_server_to_server_via_dpu](./images/opi-lab-server2server.drawio.svg)

server to dpu and dpu to the host
![test_server_to_dpuhost_via_dpu](./images/opi-lab-server2host.drawio.svg)

host to the dpu, dpu forwarding to the other vf port and back to the host
![test_dpuhost_to_dpuhost_via_dpu](./images/opi-lab-host2host.drawio.svg)

same scenarios as above but having the traffic inside the ipsec tunnel
![ipsec scenarios](./images/opi-lab-scenarios-ipsec.drawio.svg)

### not covered

same scenarios as above but having traffic generator endpoints also on the dpu (possible if dpu cores are x86 or arm and docker can be installed)
![tgen on dpu](./images/opi-lab-scenarios-with-dpu.drawio.svg)

## testing framework

- to automate the opi cases it is preferred to use [python](https://www.python.org) language
- as test framework it is preferred to use [pytest](https://docs.pytest.org)
- for ssh connectivity it is suggested to use [netmiko](https://github.com/ktbyers/netmiko) package instead of [paramiko](https://www.paramiko.org), it uses paramiko and provides drivers for many devices + ability to write plugins

## traffic generator

Open Traffic Generator (OTG) is an open standard, specifying declarative and vendor neutral API for testing Layer 2-7 network devices and applications (at any scale).

- [open traffic generator website](https://otg.dev)
- [open traffic generator implementation](https://github.com/open-traffic-generator)
- [snappi api library for otg](https://pypi.org/project/snappi)

## versions

the demo is pinned to [Ixia-c release v1.62.0-1](https://github.com/open-traffic-generator/ixia-c/releases/tag/v1.62.0-1), the community edition needs no license for these 2 port tests

| Component               | Version   | Pinned in          |
|-------------------------|-----------|--------------------|
| keng-controller         | 1.62.0-1  | `deployment/.env`  |
| ixia-c-traffic-engine   | 1.8.0.544 | `deployment/.env`  |
| keng-app-usage-reporter | 0.0.1-52  | `deployment/.env`  |
| snappi                  | 1.62.0    | `requirements.txt` |

to move to a newer release, take the versions from its release notes and update both files together

## to run the test

```Shell

git clone https://github.com/opiproject/opi-poc.git

pip install --no-cache-dir -r ./opi-poc/demos/tgen/requirements.txt

pytest -s ./opi-poc/demos/tgen/test_tgen_demo.py

```

the test logs in as root over ssh to the server, the dpu and the dpu host (ips in [testbed.py](../testbed.py)) with the private key in `OPI_SSH_KEY`, default `~/.ssh/id_rsa`

the server starts [tgen.yml](./deployment/tgen.yml) from the same repo path as the runner (`GITHUB_WORKSPACE` in ci, otherwise this clone), so run the test on the server or keep a checkout at the same path there; the dpu host gets `tgen.yml` and `.env` copied over scp

## notes, todo, etc

to debug traffic flow

```Shell
tcpdump -n -e -i enp3s0f1s0
```

setting the way DPU interacts with host requires a reboot

```Shell
mst start
mlxconfig -d /dev/mst/mt41686_pciconf0 s INTERNAL_CPU_MODEL=1
mlxconfig -d /dev/mst/mt41686_pciconf0.1 s INTERNAL_CPU_MODEL=1
```

the dpu fixture sets `ip_forward`, the iptables FORWARD policy and static arp entries, teardown only removes the ips and flushes arp

the ipsec variant of these scenarios lives in [demos/security/nvidia](../security/nvidia), it assumes docker is installed on the dpu

```Shell
systemctl start docker
docker run --rm --network host --mount src=/var/run,target=/var/run,type=bind --name opi-strongswan-bridge -d ghcr.io/opiproject/opi-strongswan-bridge:main /opi-vici-bridge -port=50151
```

care must be taken to prevent test traffic going out on management interface
