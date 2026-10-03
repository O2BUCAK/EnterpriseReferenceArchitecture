# Ubuntu app01 — Docker Build Runbook

## Purpose
Build the Ubuntu VM `app01` as the Docker application platform.

## Dependencies
Complete 01 Proxmox, 02 OPNsense and identity/network prerequisites.

## VM
Reference:
- 4 vCPU
- 10 GiB RAM
- 20 GiB OS disk
- 50 GiB data disk
- VLAN 40
- hostname `app01`

Create both disks before installation. Apply the project's Linux guest LVM/data-disk convention.

## Ubuntu Installation
1. Verify the Ubuntu Server ISO.
2. Create `app01`.
3. Add OS and data disks.
4. Install Ubuntu Server.
5. Set hostname/FQDN.
6. Configure static network.
7. Configure DNS/NTP.
8. Reboot and remove ISO.

Validate hostname, network, time, disks and free space.

## Identity
Install and configure the project's approved FreeIPA client integration. Test a human administrative login and sudo policy before relying on centralized identity.

## Docker
Install Docker Engine and the Compose tooling from the repository-approved source for the selected Ubuntu release.

Validate:
```bash
docker version
docker compose version
systemctl status docker
```

Run a harmless test container, then remove it.

## Data
Keep persistent application data on the intended data filesystem where the application design requires it. Do not blindly place all application data in the OS filesystem.

## Network
Docker provides application-level isolation in addition to the OPNsense VLAN boundary. Do not treat a Docker network as a replacement for the firewall.

## Security
- avoid unnecessary published ports;
- expose ingress through the planned reverse proxy;
- do not publish database ports;
- protect the Docker socket;
- use least privilege for containers where supported.

## Completion
[ ] Ubuntu installed
[ ] disks verified
[ ] FreeIPA client works
[ ] Docker installed
[ ] Compose works
[ ] test container works
[ ] data filesystem ready
[ ] no unnecessary published ports
