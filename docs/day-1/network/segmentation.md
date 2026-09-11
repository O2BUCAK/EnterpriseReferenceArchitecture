# Network Segmentation — Installation & Build

> **Day 1 — Build & Configure**

This document defines the procedure for implementing the target VLAN and network-segmentation architecture of the Enterprise Reference Architecture.

## Status

**Planned.** The network segmentation described here has not yet been implemented and validated in the laboratory.

The current lab has OPNsense implemented, but the VLAN topology, addressing model, and inter-VLAN policy remain target architecture until end-to-end validation is completed. fileciteturn13file0L2-L2

---

## 1. Objective

Create isolated network security zones for:

- Management
- Identity
- Database
- Application

The target model is:

```text
                         Internet
                            |
                         OPNsense
                            |
                         VLAN trunk
                            |
                      Proxmox / Switch
                            |
       +----------+---------+---------+----------+
       |          |                   |          |
   VLAN 10    VLAN 20              VLAN 30    VLAN 40
 Management   Identity             Database   Application
```

The design follows a default-deny, least-privilege approach.

---

## 2. Reference Network Plan

| VLAN | Name | Network | Gateway | Target workload |
|---:|---|---|---|---|
| 10 | Management | `10.10.10.0/24` | `10.10.10.1` | Proxmox, management |
| 20 | Identity | `10.10.20.0/24` | `10.10.20.1` | `ipa01` |
| 30 | Database | `10.10.30.0/24` | `10.10.30.1` | `db01` |
| 40 | Application | `10.10.40.0/24` | `10.10.40.1` | `app01` |

These are reference values. Actual implementation values must be recorded after the physical lab is configured.

---

## 3. Prerequisites

Before implementation, confirm:

### Physical Network

- Managed switch supports IEEE 802.1Q VLANs.
- Required VLAN IDs can be created.
- The switch supports the required tagged/trunk configuration.
- The management path has a recovery method.

### Proxmox

- `vmbr0` is operational.
- Physical NIC mapping is known.
- VLAN-aware bridging requirements are understood.
- A local/console recovery path is available.

### OPNsense

- `fw01` is operational.
- WAN and LAN interfaces are known.
- Current configuration backup exists.
- Firewall configuration can be restored if required.

### Test Clients

At least one test endpoint should be available to validate each network segment.

---

## 4. Implementation Order

Implement segmentation in this order:

```text
1. Physical switch VLANs
        ↓
2. Proxmox bridge / VLAN handling
        ↓
3. OPNsense VLAN interfaces
        ↓
4. OPNsense gateways
        ↓
5. DHCP or static addressing
        ↓
6. Firewall policy
        ↓
7. VM/client VLAN assignment
        ↓
8. Connectivity tests
        ↓
9. Negative/security tests
        ↓
10. Evidence
```

Do not move directly to restrictive firewall rules before confirming that the management recovery path works.

---

## 5. Physical Switch Configuration

Create the required VLANs on the managed switch.

Reference VLANs:

```text
10  Management
20  Identity
30  Database
40  Application
```

Define which switch ports are:

- Access ports
- Trunk/tagged ports
- Management ports

Document the physical port map:

| Port | Mode | VLANs | Purpose |
|---|---|---|---|
| `<port>` | Trunk | 10,20,30,40 | Proxmox/OPNsense path |
| `<port>` | Access | 10 | Management client |
| `<port>` | Access | 20 | Identity test |
| `<port>` | Access | 30 | Database test |
| `<port>` | Access | 40 | Application test |

Use actual switch ports during implementation.

---

## 6. Proxmox VLAN Handling

Configure the Proxmox networking path so that required VLAN tags can reach `fw01` and the appropriate VMs.

The intended logical path is:

```text
Physical NIC
     ↓
  vmbr0
     ↓
VLAN-tagged traffic
     ↓
OPNsense / VMs
```

Before making changes remotely:

1. Record current network configuration.
2. Confirm local console access.
3. Apply one network change at a time.
4. Validate management connectivity.
5. Continue only after recovery is confirmed.

Do not mark the bridge as VLAN-aware in project status until the actual configuration has been applied and tested.

---

## 7. OPNsense VLAN Interfaces

Create VLAN interfaces on the physical/virtual parent interface that carries the trunk.

Reference:

```text
Parent interface
      |
      +-- VLAN 10
      +-- VLAN 20
      +-- VLAN 30
      +-- VLAN 40
```

For each VLAN define:

```text
VLAN ID:
Interface name:
Description:
IPv4 address:
Subnet:
Gateway role:
DHCP role:
DNS role:
```

Example:

```text
VLAN 20
Address: 10.10.20.1/24
```

Use actual addresses during implementation.

---

## 8. Gateway Configuration

The OPNsense interface for each VLAN becomes the default gateway for that network.

Reference:

```text
VLAN 10 → 10.10.10.1
VLAN 20 → 10.10.20.1
VLAN 30 → 10.10.30.1
VLAN 40 → 10.10.40.1
```

After configuring each gateway, test from an endpoint in the corresponding VLAN before continuing.

---

## 9. Address Assignment

Choose DHCP or static addressing intentionally.

Infrastructure services should generally use stable addresses.

Reference:

| Host | VLAN | Example IP |
|---|---:|---|
| `fw01` | 10 | `10.10.10.1` |
| `ipa01` | 20 | `10.10.20.10` |
| `db01` | 30 | `10.10.30.10` |
| `app01` | 40 | `10.10.40.10` |
| `auto01` | 10 | `10.10.10.20` |

These are design examples, not implementation evidence.

---

## 10. DHCP Configuration

If OPNsense provides DHCP, define a separate scope for each VLAN.

Example:

```text
VLAN 20
Network: 10.10.20.0/24
Gateway: 10.10.20.1
DNS:     <defined DNS service>
Range:   <documented range>
```

Avoid overlapping DHCP scopes.

For infrastructure VMs, use static addressing or documented DHCP reservations according to the final design.

---

## 11. DNS Dependencies

Each VLAN must have a defined DNS path.

Before FreeIPA exists, use the currently implemented DNS design.

When `ipa01` is implemented:

```text
Client
  ↓
Internal DNS / FreeIPA
  ↓
External forwarding where required
```

Do not introduce competing authoritative DNS services without documenting which system owns the namespace.

---

## 12. Inter-VLAN Firewall Policy

Start with a default-deny model.

Initial conceptual policy:

| Source | Destination | Policy |
|---|---|---|
| Management | Infrastructure | Allow required management |
| Identity | Required infrastructure | Allow required services |
| Application | Database | Allow required DB service only |
| Database | Internet | Deny by default |
| Application | Management | Deny by default |
| Identity | Database | Deny unless dependency exists |
| Any | Any | Deny unless explicitly required |

Do not create broad `any → any` exceptions simply to make troubleshooting easier.

---

## 13. Application → Database Example

When `app01` and `db01` are eventually implemented, the required application-to-database path should be narrowly defined.

Example:

```text
app01
10.10.40.10
    |
    | TCP 5432
    v
10.10.30.10
 db01
```

The firewall should not permit the entire Application VLAN to access every service on the Database VLAN merely because PostgreSQL is required.

---

## 14. Management Isolation

Management access should originate from the Management VLAN or another explicitly trusted administrative path.

Target:

```text
Management
    |
    +----> Proxmox
    +----> OPNsense
    +----> Infrastructure administration
```

Untrusted VLANs should not be able to access management interfaces unless explicitly required.

---

## 15. Internet Access Policy

Not every network needs unrestricted Internet access.

Target principle:

```text
Management → Controlled
Identity   → Controlled
Database   → Restricted / preferably none by default
Application→ Controlled
```

The exact policy depends on application requirements.

Document each exception with its reason and required destination/port.

---

## 16. Implementation Safety

Network segmentation can disconnect the administrator from the entire lab.

Before implementation:

- Keep Proxmox console access available.
- Keep OPNsense console access available.
- Record current IP addresses.
- Save OPNsense configuration.
- Record current Proxmox network configuration.
- Change one layer at a time.
- Test after each layer.

Recommended sequence:

```text
Switch
 ↓
Proxmox
 ↓
OPNsense
 ↓
Test VLAN
 ↓
Remaining VLANs
 ↓
Firewall restrictions
```

---

## 17. Evidence to Capture

Record:

```text
Switch VLAN configuration:
Trunk port:
Proxmox bridge configuration:
OPNsense VLAN interfaces:
Gateway addresses:
DHCP scopes:
Firewall rules:
Test endpoints:
Implementation date:
Known deviations:
```

Screenshots can be useful, but configuration text and test results should also be recorded where possible.

Never commit credentials, private keys, or sensitive configuration exports.

---

## 18. Build Completion Criteria

Network segmentation is ready for validation when:

- All required VLANs exist on the physical switch.
- Required trunk links carry the VLANs.
- Proxmox passes the required VLAN traffic.
- OPNsense interfaces exist for the intended VLANs.
- Each VLAN has the correct gateway.
- Address assignment works.
- Test endpoints can reach their own gateway.
- Firewall rules are defined.
- Management recovery has been confirmed.

At this stage the network is **built**, but should not yet be considered fully validated.

## Related Documentation

- [`../../network/network.md`](../../network/network.md) — Target network architecture
- [`../opnsense/configuration.md`](../opnsense/configuration.md) — OPNsense configuration
- [`../opnsense/validation.md`](../opnsense/validation.md) — OPNsense validation
- [`../proxmox/configuration.md`](../proxmox/configuration.md) — Proxmox configuration
- [`../proxmox/validation.md`](../proxmox/validation.md) — Proxmox validation
- [`../documentation-standard.md`](../documentation-standard.md) — Day 1 documentation standard
