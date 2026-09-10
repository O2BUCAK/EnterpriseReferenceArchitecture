# Network Architecture

> Target network architecture and segmentation model for the Enterprise Reference Architecture.

## Status

**Documented / Planned architecture.**

OPNsense is implemented in the lab. The VLANs, addressing scheme, and traffic policies in this document describe the reference design unless separately validated as implemented.

## Status Convention

| Status | Meaning |
|---|---|
| **Implemented** | Installed, configured, and tested in the lab |
| **Planned** | Defined in the architecture but not yet implemented |
| **Future** | Deferred to a later phase |
| **Documented** | Design decision only |

---

## Purpose

The target network follows a segmented, security-first model in which infrastructure roles are separated into dedicated network segments and communication is explicitly controlled.

---

## Network Topology — Target Design

```text
                         Internet
                            |
                       [ OPNsense ]
                       Implemented
                            |
                 Planned VLAN segmentation
                            |
       +----------+---------+---------+----------+
       |          |                   |          |
   VLAN 10    VLAN 20              VLAN 30    VLAN 40
 Management   Identity             Database   Application
       |          |                   |          |
     auto01     ipa01               db01       app01
    Planned    Planned             Planned     Planned
```

The diagram is a reference design. Only explicitly validated laboratory components should be treated as implemented.

---

## VLAN and IP Addressing — Reference Model

| VLAN | Name | Network | Purpose | Status |
|---:|---|---|---|---|
| 10 | Management | `10.10.10.0/24` | Infrastructure management and future automation | Planned |
| 20 | Identity | `10.10.20.0/24` | FreeIPA and identity services | Planned |
| 30 | Database | `10.10.30.0/24` | PostgreSQL | Planned |
| 40 | Application | `10.10.40.0/24` | Docker/application workloads | Planned |

These addresses are documentation examples and may change during implementation.

### Gateway Convention

The reference design uses `.1` as the gateway address for each VLAN.

---

## Network Segments

### VLAN 10 — Management

Planned use for Proxmox management, OPNsense management, administrative interfaces, and future Ansible/OpenTofu management.

### VLAN 20 — Identity

Planned use for `ipa01` and FreeIPA services.

### VLAN 30 — Database

Planned use for `db01` and PostgreSQL services.

### VLAN 40 — Application

Planned use for `app01` and the Docker application platform.

Planned services include Nginx, Portainer, Teleport CE, Keycloak, OpenBao, NetBox, Squid, Forgejo, Woodpecker CI, Wiki.js, and Project Pulp.

---

## Inter-VLAN Traffic — Target Policy

The intended default policy is:

```text
VLAN → VLAN = DENY
```

Required communication will be explicitly permitted according to actual service requirements.

Example target flow:

```text
Application VLAN
      |
      | TCP 5432
      v
Database VLAN
```

The exact firewall rules must be based on the services actually deployed.

---

## Firewall Policy Model

OPNsense is the intended enforcement point for north-south and east-west traffic.

The target policy model is:

1. Deny by default.
2. Identify source and destination.
3. Identify protocol and port.
4. Allow only required traffic.
5. Log relevant events.
6. Review rules as the lab evolves.

The presence of a rule in this document does not mean the rule has already been configured.

---

## Docker Network Segmentation — Planned

When Docker is implemented on `app01`, Docker networks should provide an additional logical isolation layer between workloads.

```text
VLAN
  ↓
Firewall Policy
  ↓
Docker Network
  ↓
Application
```

---

## DNS Architecture — Target Design

FreeIPA is planned to provide identity-related DNS capabilities. OPNsense is implemented and may provide network-level DNS forwarding/resolution as appropriate.

Public documentation uses `example.com` placeholders.

---

## Address Assignment — Reference Examples

| Host | Role | VLAN | Example IP | Status |
|---|---|---:|---|---|
| `fw01` | OPNsense | — | `10.10.10.1` | **Implemented** |
| `ipa01` | FreeIPA | 20 | `10.10.20.10` | **Planned** |
| `db01` | PostgreSQL | 30 | `10.10.30.10` | **Planned** |
| `app01` | Docker platform | 40 | `10.10.40.10` | **Planned** |
| `auto01` | Ansible/OpenTofu | 10 | `10.10.10.20` | **Planned** |

Example addresses are part of the reference design and may change during implementation.

---

## Future Expansion

Potential future network segments include DMZ, monitoring, backup, CI/CD, user/client, security tooling, dedicated storage, and VPN clients.

Additional VLANs should only be introduced when they provide a clear security or operational benefit.

---

## Summary

This document defines the **target network architecture**. OPNsense is implemented in the lab; the remaining network topology and segmentation model should be considered planned until actually configured and validated.
