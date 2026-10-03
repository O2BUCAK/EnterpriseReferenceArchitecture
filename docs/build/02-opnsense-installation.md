# OPNsense fw01 — Build & Installation Runbook

> Build — 02

This document builds the OPNsense firewall VM fw01 on Proxmox and establishes the network foundation for the Enterprise Reference Architecture.

## 1. Purpose

The purpose of fw01 is to provide the laboratory network-security boundary:

- WAN / upstream connectivity
- LAN / management connectivity
- routing
- NAT
- firewall enforcement
- DNS/NTP foundation where intentionally provided
- future VLAN segmentation

This runbook starts from the working Proxmox host produced by Build 01.

## 2. Implementation Boundary

Current repository status:

**Implemented**
- Proxmox VE
- fw01 OPNsense VM

**Planned until configured and end-to-end validated**
- VLAN 10 Management
- VLAN 20 Identity
- VLAN 30 Database
- VLAN 40 Application
- inter-VLAN firewall policy

Therefore this build has two phases:

    Phase A — Base Firewall
      WAN
      LAN / Management
      Routing
      NAT
      Secure administration

    Phase B — Segmented Network
      VLAN 10
      VLAN 20
      VLAN 30
      VLAN 40
      Inter-VLAN policy

Do not mark Phase B implemented simply because the VLANs are documented.

## 3. Required Reading

- Proxmox Build: 01-proxmox-installation.md
- VM Design: ../vm-design/vm-design.md
- Network Architecture: ../network/network.md
- Firewall Rule Set: ../network/firewall-rule-set.md
- Port Map: ../network/port-map.md
- OPNsense Day-1 Installation
- OPNsense Configuration Baseline
- OPNsense Validation

## 4. Target Topology

### Initial topology

    Upstream Network
          |
         WAN
          |
       +------+
       | fw01 |
       | OPNs |
       +------+
          |
         LAN
          |
        vmbr0
          |
    Management PC

### Target topology

    Internet
       |
      WAN
       |
    OPNsense
       |
    VLAN trunk
       |
    +--+------+------+ 
    |  |      |     |
   10 20     30    40
  MGMT ID     DB    APP
   |  |       |     |
 auto01 ipa01 db01 app01

The repository currently treats VLAN segmentation as planned architecture.

## 5. Reference Network Model

| VLAN | Name | Network | Gateway | Status |
|---:|---|---|---|---|
| 10 | Management | 10.10.10.0/24 | 10.10.10.1 | Planned |
| 20 | Identity | 10.10.20.0/24 | 10.10.20.1 | Planned |
| 30 | Database | 10.10.30.0/24 | 10.10.30.1 | Planned |
| 40 | Application | 10.10.40.0/24 | 10.10.40.1 | Planned |

Reference hosts:

| Host | Role | Address |
|---|---|---|
| fw01 | OPNsense | 10.10.10.1 |
| ipa01 | FreeIPA | 10.10.20.10 |
| db01 | PostgreSQL / Redis | 10.10.30.10 |
| app01 | Docker | 10.10.40.10 |
| auto01 | Ansible / OpenTofu | 10.10.10.20 |

These are architecture reference values, not evidence of the live configuration.

## 6. Prerequisites

### Proxmox

- Proxmox Build 01 completed.
- Proxmox management access works.
- VM storage is available.
- OPNsense ISO is available.
- ISO checksum is verified.

### Network

Obtain the real values before configuration:

    WAN mode:
    WAN address:
    WAN prefix:
    WAN gateway:
    WAN DNS:
    LAN address:
    LAN network:
    Management workstation address:

Do not guess these values.

### Recovery

Keep Proxmox console access available throughout firewall installation. Interface, VLAN or firewall changes can disconnect the web session.

## 7. Create fw01 in Proxmox

Create a VM using the project VM standard where applicable.

| Resource | Value |
|---|---:|
| VM name | fw01 |
| vCPU | 2 |
| RAM | 4 GiB |
| Disk | 40 GiB |
| Firmware | UEFI where supported/tested |
| Machine | q35 where supported |
| NIC 1 | WAN |
| NIC 2 | LAN |

OPNsense is an appliance and therefore does not use the Linux two-disk standard.

## 8. Configure Virtual NICs

Create two clearly identifiable virtual NICs.

| Proxmox NIC | Purpose | Bridge |
|---|---|---|
| NIC 1 | WAN | Upstream/WAN bridge |
| NIC 2 | LAN | Internal management bridge |

Do not assume vmbr0 is WAN or LAN.

Record the MAC addresses:

    WAN NIC:
    MAC:

    LAN NIC:
    MAC:

The MAC-to-role mapping is installation evidence.

A swapped WAN/LAN mapping can cause loss of management access, incorrect routing/NAT and unintended exposure.

## 9. Install OPNsense

Attach the verified OPNsense ISO to fw01 and boot from it.

Follow the installer workflow appropriate to the exact OPNsense release:

    Boot ISO
       |
    Installer
       |
    Select target
       |
    Installation
       |
    Reboot
       |
    Remove ISO
       |
    First boot

Do not leave the VM permanently dependent on the installation ISO.

## 10. First Boot and Interface Assignment

Open the Proxmox console.

Confirm OPNsense boots from the virtual disk.

Use the OPNsense console to identify interfaces.

Do not rely only on names such as vtnet0/vtnet1. Compare:

- OPNsense interface
- Proxmox NIC
- MAC address
- intended network

Record:

| Role | OPNsense interface | MAC | Proxmox NIC |
|---|---|---|---|
| WAN | Actual value | Actual value | NIC 1 |
| LAN | Actual value | Actual value | NIC 2 |

Only after this mapping is confirmed should the interface assignment be finalized.

## 11. Configure Initial LAN

The repository uses this reference model:

    LAN network: 10.10.10.0/24
    OPNsense LAN: 10.10.10.1

If the live laboratory network uses these values, configure them accordingly.

If it uses another approved address, use that value and record the deviation.

Do not configure 10.10.10.1 if that address is already in use.

## 12. Management Workstation Test

Place the management workstation on the initial LAN.

Conceptually:

    OPNsense LAN 10.10.10.1/24
             |
        Management PC

Test reachability to the actual LAN address.

Then access the HTTPS Web UI.

The administration interface must not be exposed through WAN.

## 13. Initial Web Configuration

At first login:

1. Change any default administrative credential still present.
2. Set hostname.
3. Set domain according to the actual DNS design.
4. Configure DNS deliberately.
5. Configure timezone.
6. Configure NTP.
7. Review WAN.
8. Review LAN.
9. Apply configuration.

Do not store credentials in Git.

## 14. WAN Configuration

Configure WAN according to the real upstream environment:

- DHCP
- static addressing
- PPPoE
- another supported method

Record:

    WAN mode:
    Address:
    Prefix:
    Gateway:
    DNS:
    MTU:

Do not publish real public IP addresses unless they are intentionally part of the public architecture.

## 15. DNS and NTP

Verify DNS resolution and time synchronization.

Time is a prerequisite for:

- FreeIPA/Kerberos
- TLS
- logs
- monitoring
- distributed services

The project plans FreeIPA for identity-related DNS capabilities. Do not create competing authoritative DNS arrangements without documenting their responsibilities.

The actual NTP source must come from the approved environment design.

## 16. DHCP

Enable DHCP only on networks where OPNsense is intended to provide it.

For infrastructure systems, prefer stable addressing.

Record:

    Network:
    Pool:
    Gateway:
    DNS:
    Lease duration:
    Reservations:

Avoid overlap between static addresses and DHCP pools.

## 17. Initial Firewall Policy

The target security model is:

    Default Deny
         |
    Explicit Source
         |
    Explicit Destination
         |
    Explicit Protocol
         |
    Explicit Port
         |
    Explicit Reason

Do not create broad ANY-to-ANY allow rules simply to simplify troubleshooting.

If a temporary diagnostic rule is required, document it and remove it after testing.

## 18. WAN Management Protection

Verify that WAN does not provide unintended access to:

- OPNsense Web UI
- SSH
- Proxmox 8006
- PostgreSQL 5432
- FreeIPA
- Portainer
- OpenBao
- other infrastructure services

The repository target policy blocks infrastructure management from WAN.

## 19. Outbound NAT

For the initial lab, outbound NAT may be required for internal clients to reach the upstream network.

Conceptually:

    Internal network
          |
       OPNsense
          |
      Outbound NAT
          |
         WAN

Verify the actual NAT mode.

Do not create inbound port forwards merely because outbound Internet access works.

## 20. VLAN Phase

Only after the base firewall has been validated should VLANs be introduced.

Target:

| VLAN | Purpose | Network |
|---:|---|---|
| 10 | Management | 10.10.10.0/24 |
| 20 | Identity | 10.10.20.0/24 |
| 30 | Database | 10.10.30.0/24 |
| 40 | Application | 10.10.40.0/24 |

Implementation requires coordination between:

    Upstream switch
         |
    Proxmox bridge
         |
      fw01 NIC
         |
    OPNsense VLANs
         |
    Firewall policy
         |
       VMs

Do not create VLAN interfaces without first confirming that the connected Proxmox bridge and upstream network support the intended tagged traffic.

## 21. VLAN Trunk Safety

When VLANs are enabled:

1. Confirm physical/upstream switch configuration.
2. Confirm Proxmox bridge configuration.
3. Confirm VLAN-aware behavior.
4. Confirm OPNsense parent interface.
5. Create one VLAN first.
6. Test gateway access.
7. Test routing.
8. Test expected allowed traffic.
9. Test expected denied traffic.
10. Continue with the next VLAN.

Do not introduce all four VLANs simultaneously while troubleshooting a new network.

## 22. Target Firewall Zones

    MGMT_NET      10.10.10.0/24
    IDENTITY_NET  10.10.20.0/24
    DB_NET        10.10.30.0/24
    APP_NET       10.10.40.0/24
    WAN           Upstream

The default inter-zone relationship is:

    ZONE -> ZONE = DENY

Examples of documented exceptions:

    MGMT -> Proxmox       TCP 8006
    MGMT -> Linux         TCP 22
    APP  -> DB            TCP 5432
    APP  -> DB            TCP 6379 when required
    APP  -> IPA           Required identity ports

The complete rule model remains in the Firewall Rule Set document.

## 23. Configuration Backup

Before major firewall changes:

1. Export/backup the OPNsense configuration.
2. Protect the backup.
3. Make one logical change.
4. Validate.
5. Document.

A configuration export can contain sensitive information. Do not commit an unredacted export to Git.

## 24. Validation

### Base firewall

- [ ] fw01 boots without ISO.
- [ ] WAN interface is correct.
- [ ] LAN interface is correct.
- [ ] MAC-to-NIC mapping is documented.
- [ ] LAN management works.
- [ ] WAN connectivity works where required.
- [ ] DNS works.
- [ ] NTP is synchronized.
- [ ] Administrative credentials are secured.
- [ ] WAN management exposure is blocked.
- [ ] Outbound NAT behavior is understood.
- [ ] Configuration backup exists.

### Positive tests

| Test | Expected |
|---|---|
| Management PC -> OPNsense HTTPS | PASS |
| OPNsense -> approved DNS | PASS |
| OPNsense -> approved NTP | PASS |
| Internal client -> Internet where permitted | PASS |

### Negative tests

| Test | Expected |
|---|---|
| WAN -> OPNsense management | BLOCK |
| WAN -> SSH | BLOCK |
| WAN -> Proxmox 8006 | BLOCK |
| WAN -> PostgreSQL 5432 | BLOCK |
| WAN -> FreeIPA | BLOCK |

### VLAN validation

After Phase B is implemented, test both expected allowed and expected denied flows for every VLAN.

A VLAN interface existing in OPNsense is not sufficient evidence that segmentation works.

## 25. Evidence Record

Record:

    VM:
    VM ID:
    OPNsense version:
    Hostname:
    WAN interface:
    WAN MAC:
    LAN interface:
    LAN MAC:
    WAN mode:
    LAN address:
    DNS:
    NTP:
    NAT mode:
    VLAN status:
    Firewall policy version:
    Validation date:
    Known deviations:

Never record passwords, private keys, API tokens, recovery codes or unredacted sensitive configuration exports.

## 26. Failure Handling

If management access is lost:

1. Open the Proxmox console for fw01.
2. Verify interface assignments.
3. Verify LAN address.
4. Verify route configuration.
5. Check the management workstation network.
6. Check the relevant firewall rule.
7. Restore the last known-good configuration if appropriate.
8. Re-test from a separate management workstation.

Record the failure and recovery steps.

## 27. Completion Criteria

### Phase A — Base firewall

    [ ] fw01 VM created
    [ ] OPNsense ISO verified
    [ ] WAN/LAN NICs identified
    [ ] OPNsense installed
    [ ] ISO detached
    [ ] WAN configured
    [ ] LAN configured
    [ ] Web management verified
    [ ] DNS verified
    [ ] NTP verified
    [ ] NAT verified
    [ ] WAN management blocked
    [ ] Configuration backup created
    [ ] Positive tests passed
    [ ] Negative tests passed
    [ ] Evidence recorded

### Phase B — Segmentation

    [ ] Upstream VLAN path verified
    [ ] Proxmox VLAN handling verified
    [ ] VLAN 10 implemented
    [ ] VLAN 20 implemented
    [ ] VLAN 30 implemented
    [ ] VLAN 40 implemented
    [ ] Gateway addresses validated
    [ ] Inter-VLAN default deny validated
    [ ] Required exceptions implemented
    [ ] Positive flow tests passed
    [ ] Negative flow tests passed
    [ ] Evidence recorded

## 28. Next Build Stage

After fw01 is installed and the base network is validated:

**03 — FreeIPA / Identity Foundation**

Dependency chain:

    Proxmox
       |
    fw01 / OPNsense
       |
    Network foundation
       |
    ipa01 / FreeIPA
       |
       +--> DNS / Identity
       +--> db01
       +--> app01
       +--> auto01

FreeIPA must not be treated as the source of truth for DNS until its installation and DNS design have been explicitly implemented and validated.

## 29. Related Documentation

- 01-proxmox-installation.md
- ../network/network.md
- ../network/firewall-rule-set.md
- ../network/port-map.md
- ../vm-design/vm-design.md
- ../day-1/opnsense/installation.md
- ../day-1/opnsense/configuration.md
- ../day-1/opnsense/validation.md

---

## Implementation Status

This file is a Build/Reinstallation Runbook.

It does not change implementation status. OPNsense being documented or installed does not by itself prove that VLAN segmentation or every firewall rule has been implemented and validated.
