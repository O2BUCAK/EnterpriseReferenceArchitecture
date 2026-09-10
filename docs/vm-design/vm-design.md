# VM Design

> Virtual machine design standards for the Enterprise Reference Architecture.

## Purpose

This document defines the virtual machine architecture, resource allocation, storage layout, and Proxmox configuration standards used by the Enterprise Reference Architecture.
The environment demonstrates enterprise infrastructure principles on modest hardware while maintaining clear separation between network security, identity, database, application, and automation workloads.

The VM design follows separation of responsibilities, least privilege, predictable resource allocation, consistent storage architecture, network segmentation, workload-specific storage sizing, infrastructure automation, reproducibility, and efficient use of limited hardware resources.

---

## Virtualization Platform

The virtualization platform is **Proxmox VE**.

```text
Physical Host
└── Proxmox VE
    ├── fw01
    ├── ipa01
    ├── db01
    ├── app01
    └── auto01
```

Proxmox is responsible for VM lifecycle management, virtual CPU and memory allocation, virtual networking, virtual storage, VM isolation, backup/snapshot capabilities, and QEMU Guest Agent integration.

---

# VM Inventory

| VM | Operating System | Primary Role |
|---|---|---|
| `fw01` | OPNsense | Firewall, routing and network security |
| `ipa01` | Fedora | FreeIPA identity and authentication |
| `db01` | Pardus | PostgreSQL database |
| `app01` | Ubuntu Server | Docker application platform |
| `auto01` | RHEL | Ansible and OpenTofu automation |

Each VM has a clearly defined primary responsibility. The architecture intentionally avoids combining unrelated infrastructure services into a single VM.

---

# Naming Convention

VM names use the role-based convention `<role><number>`.

Examples: `fw01`, `ipa01`, `db01`, `app01`, `auto01`.

The numeric suffix allows additional instances such as `ipa02`, `db02`, or `app02` if future requirements call for redundancy or horizontal scaling.

---

# VM Role Design

## fw01 — Firewall

`fw01` provides firewalling, routing, NAT, network segmentation, inter-network policy enforcement, DHCP where required, and DNS forwarding/resolution where required using OPNsense.

`fw01` is a dedicated network appliance and does **not** follow the standard Linux VM storage profile.

## ipa01 — Identity

`ipa01` provides centralized identity and authentication using FreeIPA, including identity management, authentication, authorization, Kerberos, LDAP, host enrollment, identity-related DNS integration, and centralized access control.

Storage baseline: 20 GiB OS disk + 20 GiB data disk.

## db01 — Database

`db01` provides centralized PostgreSQL services, database administration, storage, backup, and recovery.

```text
disk 0 — 20 GiB
└── Operating System

disk 1 — 50 GiB
└── vg_data
    └── lv_pg_data
```

The PostgreSQL data directory is stored on the dedicated data logical volume. A third dedicated PostgreSQL disk is intentionally not part of the current architecture.

## app01 — Application Platform

`app01` provides the Ubuntu Server and Docker application platform hosting Nginx, Portainer, Teleport CE, Keycloak, OpenBao, NetBox, Squid, Forgejo, Woodpecker CI, Wiki.js, and Project Pulp.

```text
disk 0 — 20 GiB
└── Operating System

disk 1 — 50 GiB
└── Docker / application persistent data
```

Persistent application data should use the second disk whenever practical.

## auto01 — Automation

`auto01` provides Ansible, OpenTofu, configuration management, infrastructure provisioning, repeatable deployments, and maintenance automation.

Storage baseline: 20 GiB OS disk + 20 GiB data disk.

---

# Standard Linux VM Profile

Linux-based VMs use a common Proxmox configuration baseline.

| Setting | Standard |
|---|---|
| VM Name | Role-based |
| VM ID | Automatic |
| ISO Storage | `local` |
| Guest Type | Linux |
| Machine | `q35` |
| BIOS | OVMF (UEFI) |
| EFI Disk | Enabled |
| Pre-Enroll keys | Disabled |
| SCSI Controller | VirtIO SCSI single |
| QEMU Agent | Enabled |
| CPU Sockets | 1 |
| CPU Type | `host` |
| Network Model | VirtIO |
| Bridge | `vmbr0` |

The VM ID is assigned automatically by Proxmox.

---

# Storage Standard

The project uses a **two-disk VM standard** for Linux workloads.

```text
VM
├── SCSI 0 — Operating System
└── SCSI 1 — Role-specific Data
```

## Disk 0 — Operating System

Default size: **20 GiB**.

Logical structure:

```text
Disk 0
├── EFI System Partition
├── /boot
└── vg_os
    └── lv_root
```

`/var`, `/home`, and `/tmp` are intentionally kept outside the root filesystem according to the storage architecture.

## Disk 1 — Role-specific Data

Default baseline: **20 GiB**.

```text
Disk 1
└── vg_data
    ├── lv_var
    ├── lv_home
    ├── lv_tmp
    └── Role-Specific Data
```

Database and Docker workloads use larger second disks.

### Current sizing

| Workload | OS Disk | Data Disk |
|---|---:|---:|
| General Linux VM | 20 GiB | 20 GiB |
| `ipa01` | 20 GiB | 20 GiB |
| `auto01` | 20 GiB | 20 GiB |
| `db01` | 20 GiB | 50 GiB |
| `app01` | 20 GiB | 50 GiB |

---

# CPU Standard

Linux VMs use one socket and CPU type `host`. CPU cores are workload-dependent.

Suggested baseline:

| VM | vCPU |
|---|---:|
| `ipa01` | 2 |
| `db01` | 2–4 |
| `app01` | 4 |
| `auto01` | 2 |

`fw01` is sized separately according to firewall and routing workload.

---

# Memory Standard

Memory allocation is workload-dependent.

Suggested baseline:

| VM | RAM |
|---|---:|
| `ipa01` | 4 GiB |
| `db01` | 4–8 GiB |
| `app01` | 8–12 GiB |
| `auto01` | 4 GiB |

`app01` receives the highest allocation because it hosts multiple Docker services. `db01` can receive additional memory as PostgreSQL workloads increase.

---

# Network Standard

Linux VMs use VirtIO networking on `vmbr0`.

Network placement is determined by the network architecture. VM isolation is supplemented by network segmentation and firewall policies enforced through `fw01`.

The Proxmox firewall may be enabled when a specific requirement exists.

---

# Application Isolation

Multiple applications may run on `app01`, but they should not automatically have unrestricted communication with each other. Docker networks provide application-level segmentation.

Services should communicate only with the systems and ports required for their operation.

This supports least privilege, Zero Trust principles, reduced lateral movement, and clear service boundaries.

---

# Resource Allocation Principles

Because the architecture runs on a single physical host:

1. Start with conservative resource allocations.
2. Monitor actual utilization.
3. Increase resources based on observed workload.
4. Avoid unnecessary CPU and memory reservations.
5. Give additional resources to database and application workloads when required.
6. Keep infrastructure services lightweight.
7. Prefer workload-based sizing over arbitrary allocation.

Resource allocation is a tunable configuration rather than a fixed architectural requirement.

---

# Security Considerations

VM separation is one layer of the overall security architecture.
Additional controls include network segmentation, firewall policies, least privilege, identity-based access, service isolation, restricted administrative access, secret management, encrypted communication, and minimal exposed services.

Sensitive credentials should not be stored directly in Git repositories, Docker Compose files, VM configuration files, or infrastructure-as-code repositories.

---

# Backup and Recovery

VM snapshots are useful for testing, maintenance, short-term rollback, and configuration changes, but they are not a complete backup strategy.

Critical persistent data includes PostgreSQL databases, application data, identity data, Git repositories, configuration, infrastructure definitions, and secrets.

Application-aware backups should be used for critical workloads where appropriate.

---

# VM Lifecycle

```text
Design
   ↓
Provision
   ↓
Configure
   ↓
Secure
   ↓
Deploy
   ↓
Monitor
   ↓
Backup
   ↓
Maintain
   ↓
Decommission
```

The project should progressively automate VM provisioning and configuration using Ansible and OpenTofu to reduce manual configuration and configuration drift.

---

# Future Expansion

The current environment is intentionally designed for a single Proxmox host.

Potential future capabilities include multiple Proxmox nodes, identity replicas, PostgreSQL replication, application replicas, load balancing, centralized monitoring, and high availability.

These capabilities are outside the scope of the current implementation.

---

# Design Summary

```text
Standard Linux VM

SCSI 0
└── 20 GiB
    └── Operating System

SCSI 1
└── 20 GiB baseline
    └── Role-specific Data
```

Workload-specific sizing:

```text
db01
20 GiB OS + 50 GiB PostgreSQL Data

app01
20 GiB OS + 50 GiB Application Data
```

This approach keeps the infrastructure simple enough to run on modest hardware while maintaining clear separation between operating-system files and persistent workload data.
