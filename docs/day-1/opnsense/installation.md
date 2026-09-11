# OPNsense — Installation

> **Day 1 — Build & Configure**

This document defines the installation procedure for the OPNsense firewall used as `fw01` in the Enterprise Reference Architecture.

## Status

**Implemented.** OPNsense is currently deployed as a virtual machine in the laboratory. The procedure below is the documented reference process; individual settings are considered validated only when they have been tested and evidence has been recorded.

## 1. Purpose

The firewall provides the network-security boundary for the lab and is intended to become the enforcement point for routing, segmentation, NAT, firewall policy, and selected infrastructure services.

The target architecture uses OPNsense with these logical areas:

- Management
- Identity
- Database
- Application
- WAN / upstream connectivity

VLAN segmentation beyond the currently implemented lab state remains **Planned**.

## 2. Prerequisites

Before installation:

- Proxmox VE is installed and operational.
- `fw01` VM has been created according to the VM design.
- OPNsense ISO is available.
- At least two virtual network interfaces are available for WAN and LAN.
- A management computer is available for testing access.
- The upstream network information is known if WAN connectivity is required.

## 3. VM Baseline

Reference `fw01` allocation:

| Resource | Value |
|---|---:|
| vCPU | 2 |
| Memory | 4 GiB |
| OS disk | 40 GiB |
| NIC 1 | WAN |
| NIC 2 | LAN / internal network |
| Guest type | Other / BSD-compatible |

Use the actual VM design as the authoritative source if the resource allocation changes.

## 4. Create the VM

Create the VM in Proxmox and attach the OPNsense ISO.

Recommended baseline:

- UEFI where supported by the selected OPNsense release and VM design.
- VirtIO network interfaces where supported and tested.
- Separate WAN and LAN interfaces.
- QEMU Guest Agent only where supported and useful for the selected firewall configuration.

The two network interfaces must be clearly identified in Proxmox before installation.

## 5. Installation

Boot the VM from the OPNsense installation media.

Follow the installer workflow:

```text
Boot ISO
  ↓
Installer
  ↓
Select installation target
  ↓
Select filesystem / installation options
  ↓
Install
  ↓
Reboot
  ↓
Remove ISO
  ↓
First boot
```

Do not continue with production-like configuration until the VM boots successfully from its installed disk.

## 6. Initial Console Configuration

After first boot, use the OPNsense console to identify the available interfaces and assign them correctly.

Conceptually:

```text
WAN  → upstream / Internet side
LAN  → trusted management side
```

Do not assume interface names such as `vtnet0` or `vtnet1` without checking the actual VM.

Confirm:

- WAN interface is connected to the intended Proxmox network.
- LAN interface is connected to the intended internal network.
- LAN has an administrative address.
- The management computer can reach the LAN address.

## 7. Initial Web Access

From a management computer on the LAN side, access the OPNsense web interface using HTTPS.

Use the address assigned during initial console configuration.

At first login:

1. Change default administrative credentials if still present.
2. Complete the initial setup wizard.
3. Confirm hostname and DNS settings.
4. Confirm timezone.
5. Review WAN settings.
6. Review LAN settings.
7. Apply configuration.

Do not expose the administrative interface to the WAN interface.

## 8. Initial Configuration Review

After the wizard, review:

- System hostname
- DNS servers
- Timezone
- NTP
- WAN addressing
- LAN addressing
- Gateway configuration
- Firewall rules
- NAT behavior
- Administrative access

The installation is not considered complete simply because the web interface is accessible.

## 9. First-Boot Validation

Confirm:

```text
[ ] OPNsense boots without installer media
[ ] Correct WAN interface is assigned
[ ] Correct LAN interface is assigned
[ ] LAN management access works
[ ] WAN connectivity works where required
[ ] DNS resolution works
[ ] System time is correct
[ ] Administrative credentials are secured
[ ] No unintended WAN management access exists
```

## 10. Evidence

Record:

```text
VM ID:
OPNsense version:
Hostname:
WAN interface:
LAN interface:
LAN address:
WAN mode:
Installation date:
Validation date:
Known deviations:
```

Never store passwords, API keys, certificates with private keys, or other secrets in the repository.

## 11. Completion Criteria

OPNsense installation is complete when:

1. The installed system boots normally.
2. WAN and LAN interfaces are correctly identified.
3. The administrator can reach the web interface from the intended management network.
4. Basic network connectivity works as expected.
5. Default administrative credentials are no longer in use.
6. No management interface is unintentionally exposed to WAN.
7. Installation evidence has been recorded.

## Related Documentation

- [`configuration.md`](configuration.md) — OPNsense configuration baseline
- [`validation.md`](validation.md) — OPNsense validation
- [`../../network/network.md`](../../network/network.md) — Network architecture
- [`../../security/security.md`](../../security/security.md) — Security architecture
- [`../../vm-design/vm-design.md`](../../vm-design/vm-design.md) — VM standards
