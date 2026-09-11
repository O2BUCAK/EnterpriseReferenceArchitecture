# Day 1 — Build & Configure

> **Day 1** defines how the reference architecture is built, configured, and validated.

Day 1 is the transition from **architecture design to a working infrastructure**.

The objective is not simply to install software, but to establish a repeatable baseline that can later be operated and maintained.

## Lifecycle

```text
Architecture
    ↓
Installation
    ↓
Base Configuration
    ↓
Security Baseline
    ↓
Service Configuration
    ↓
Integration
    ↓
Validation
    ↓
Day 1 Complete
```

## Current Status

Only laboratory work that has actually been completed and validated may be marked **Implemented**.

At the current project stage:

| Area | Status |
|---|---|
| Proxmox VE | **Implemented** |
| OPNsense | **Implemented** |
| Network segmentation | **Planned** |
| FreeIPA | **Planned** |
| PostgreSQL | **Planned** |
| Docker application platform | **Planned** |
| Identity integration | **Planned** |
| Automation / IaC | **Planned** |

## Planned Day 1 Structure

### 01 — Proxmox

- Installation
- Host configuration
- Networking
- DNS and NTP
- Storage
- VM standards
- Updates
- Basic hardening
- Validation

### 02 — OPNsense

- Installation
- WAN/LAN configuration
- VLAN design
- DHCP/DNS
- NAT
- Firewall policy
- Administrative access
- Logging
- Validation

### 03 — Network

- VLANs
- IP addressing
- Routing
- Inter-VLAN policy
- Management access
- Connectivity validation

### 04 — FreeIPA

- Installation
- Realm and DNS
- Users and groups
- Hosts
- HBAC
- Sudo rules
- Certificates
- Client enrollment

### 05 — PostgreSQL

- Installation
- Initial configuration
- Roles and permissions
- Database creation
- Authentication
- Network access
- Security baseline

### 06 — Docker / Application Platform

- Ubuntu application VM
- Docker Engine
- Compose
- Persistent storage
- Container networking
- Reverse proxy
- Planned FOSS services

### 07 — Identity Integration

- Infrastructure authentication
- Application SSO
- Privileged access
- Service identities

### 08 — Security Baseline

- Least privilege
- Network segmentation
- Administrative access
- TLS
- Secrets handling
- Logging

### 09 — Validation

Every Day 1 component must have explicit validation criteria before it can be considered **Implemented**.

Example:

```text
[ ] DNS resolution
[ ] NTP synchronization
[ ] Network connectivity
[ ] Firewall policy
[ ] Authentication
[ ] Service availability
[ ] Storage availability
[ ] Logging
[ ] Backup readiness
```

## Day 1 Principle

> **A system is not complete when installation finishes. It is complete when its configuration has been validated and documented.**

Day 2 begins only after the relevant Day 1 baseline is established.
