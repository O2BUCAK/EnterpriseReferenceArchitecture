# Fedora VM — Build Runbook

## Purpose
Build the Fedora Linux guest that becomes the foundation for the FreeIPA identity service.

## Dependencies
Complete 01 Proxmox and 02 OPNsense first.

## VM
Target: `ipa01`.

Use the repository VM standard: UEFI/OVMF where supported, q35, VirtIO networking, VirtIO SCSI, QEMU Guest Agent where supported, OS disk SCSI 0 and role-specific data disk SCSI 1.

Reference allocation: 2 vCPU, 2 GiB RAM, 20 GiB OS disk, 20 GiB data disk, VLAN 20.

## Installation
1. Obtain the Fedora Server ISO for the selected release.
2. Verify checksum.
3. Create `ipa01` in Proxmox.
4. Attach the ISO.
5. Configure the NIC for the intended Identity network.
6. Install Fedora.
7. During installation create the required LVM layout according to the current VM design.
8. Set timezone and hostname.
9. Configure the static address assigned to `ipa01`.
10. Reboot and remove the ISO.

## First Boot
Run:
```bash
hostnamectl
ip addr
ip route
timedatectl
lsblk
df -h
```

Verify hostname, address, route, storage and time.

## Updates
Update the guest using the repository-approved package repositories. Reboot if required.

## Identity Preparation
Before FreeIPA:
- hostname and FQDN must resolve correctly;
- forward and reverse DNS requirements must be understood;
- time synchronization must be working;
- required firewall flows must exist;
- the final realm/domain must be decided.

Do not install FreeIPA until these prerequisites pass validation.

## Completion
[ ] Fedora boots
[ ] static network works
[ ] DNS prerequisites work
[ ] time synchronized
[ ] storage verified
[ ] updates applied
[ ] hostname/FQDN verified
[ ] ready for 04-freeipa-installation.md
