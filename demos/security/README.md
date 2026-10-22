# IPSec demo

- Nvidia
- Marvell
- Intel

## Automated test

`test_ipsec.py` runs once per dpu in `demos/testbed.py` `DPUS`. On each dpu it starts the
opi-strongswan-bridge, loads an IPsec tunnel with the OPI gRPC API, and runs CyPerf
(agent 26.1.3.876, `cyperf` 26.1.2 from PyPI) through the tunnel.

| vendor | dpus       | strongSwan runs on | reached through |
|--------|------------|--------------------|-----------------|
| nvidia | bf2, bf3   | the Arm            | ssh             |
| intel  | e2100      | the ACC            | ssh via the IMC |

The gRPC port is forwarded over the ssh session, so the dpu firewall does not matter.

Nothing takes a password:

- ssh uses the key in `OPI_SSH_KEY` (default `~/.ssh/id_rsa`), which must already be
  installed on the server, every dpu and the A100G `arista` user. A dpu without it is skipped.
- CyPerf uses an offline token: generate it in the controller UI and save it in
  `~/.cyperf/offline-token` (chmod 600), or point `CYPERF_TOKEN_FILE` at it. The
  `CYPERF_OFFLINE_TOKEN` variable is read as well.

```Shell
pip3 install -r demos/security/requirements.txt
pytest -s -rs demos/security/test_ipsec.py
```
