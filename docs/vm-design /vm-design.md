# VM Design

> Virtual machine design standards for the Enterprise Reference Architecture.

## Purpose

This document defines the virtual machine architecture, resource allocation, storage layout, and Proxmox configuration standards used by the Enterprise Reference Architecture.
The environment is designed to demonstrate enterprise infrastructure principles on modest hardware while maintaining clear separation between network security, identity, database, application, and automation workloads.

The VM design follows these principles:

* Separation of responsibilities
* Least privilege
* Predictable resource allocation
* Consistent storage architecture
* Network segmentation
* Workload-specific storage sizing
* Infrastructure automation
* Reproducibility
* Efficient use of limited hardware resources

---

## Virtualization Platform

The virtualization platform is **Proxmox VE**.
The physical host provides compute, memory, storage, and network resources to the virtual machines.

```text
Physical Host
└── Proxmox VE
    ├── fw01
    ├── ipa01
    ├── db01
    ├── app01
    └── auto01
```

Proxmox is responsible for:

* VM lifecycle management
* Virtual CPU and memory allocation
* Virtual networking
* Virtual storage
* VM isolation
* Backup and snapshot capabilities
* Guest integration through the QEMU Guest Agent

---

# VM Inventory

The initial architecture consists of five primary virtual machines.

| VM       | Operating System | Primary Role                           |
| -------- | ---------------- | -------------------------------------- |
| `fw01`   | OPNsense         | Firewall, routing and network security |
| `ipa01`  | Fedora           | FreeIPA identity and authentication    |
| `db01`   | Pardus           | PostgreSQL database                    |
| `app01`  | Ubuntu Server    | Docker application platform            |
| `auto01` | RHEL             | Ansible and OpenTofu automation        |

Each VM has a clearly defined primary responsibility.
The architecture intentionally avoids combining unrelated infrastructure services into a single VM.

---

# Naming Convention

VM names use a role-based naming convention:

```text
<role><number>
```

Examples:

```text
fw01
ipa01
db01
app01
auto01
```

The numeric suffix allows additional instances to be introduced without changing the naming model.

For example:

```text
ipa02
db02
app02
```

could be introduced if future requirements call for redundancy or horizontal scaling.

---

# VM Role Design

## fw01 — Firewall

`fw01` provides the network security and routing layer using OPNsense.

Primary responsibilities:

* Firewalling
* Routing
* NAT
* Network segmentation
* Inter-network policy enforcement
* DHCP where required
* DNS forwarding/resolution where required

`fw01` is treated as a dedicated network appliance and does **not** follow the standard Linux VM storage profile.

---

## ipa01 — Identity

`ipa01` provides centralized identity and authentication using FreeIPA.

Primary responsibilities:

* Identity management
* Authentication
* Authorization
* Kerberos
* LDAP
* Host enrollment
* Identity-related DNS integration
* Centralized access control

Identity services are isolated from application and database workloads.

### Storage

```text
Disk 0 — 20 GiB
└── Operating System

Disk 1 — 20 GiB
└── FreeIPA / role-specific persistent data
```

---

## db01 — Database

`db01` provides the centralized PostgreSQL database platform.

Primary responsibilities:

* PostgreSQL
* Application database services
* Database storage
* Database administration
* Database backup and recovery

The database VM does not host Docker application workloads.

### Storage

`db01` uses the standard two-disk model with an increased data disk size.

```text
Disk 0 — 20 GiB
├── EFI
├── /boot
└── vg_os
    ├── lv_root
    ├── lv_var
    ├── lv_home
    └── lv_tmp

Disk 1 — 50 GiB
└── vg_data
    └── lv_pg_data
```

The PostgreSQL data directory is stored on `lv_pg_data`.
A third dedicated PostgreSQL disk is intentionally **not used** in the current architecture.
This keeps the storage design simple while providing a dedicated data volume separate from the operating system.

---

## app01 — Application Platform

`app01` provides the main application platform using Ubuntu Server and Docker.

Applications include:

* Nginx
* Portainer
* Teleport Community Edition
* Keycloak
* OpenBao
* NetBox
* Squid Gateway
* Forgejo
* Woodpecker CI
* Wiki.js
* Project Pulp

### Storage

Because `app01` hosts multiple containerized services, its data disk is larger than the default VM data disk.

```text
Disk 0 — 20 GiB
├── EFI
├── /boot
└── vg_os
    ├── lv_root
    ├── lv_var
    ├── lv_home
    └── lv_tmp

Disk 1 — 50 GiB
└── Docker / application persistent data
```

The operating-system disk is kept separate from persistent application data.
Docker volumes and other persistent application data should use the second disk whenever practical.

---

## auto01 — Automation

`auto01` provides the infrastructure automation layer.

Primary responsibilities:

* Ansible
* OpenTofu
* Configuration management
* Infrastructure provisioning
* Repeatable deployments
* Infrastructure maintenance automation

Automation is intentionally separated from the infrastructure it manages.

### Storage

```text
Disk 0 — 20 GiB
└── Operating System

Disk 1 — 20 GiB
└── Automation-related persistent data
```

---

# Standard Linux VM Profile

Linux-based VMs use a common Proxmox configuration baseline.

## General

| Setting       | Standard         |
| ------------- | ---------------- |
| VM Name       | Role-based       |
| VM ID         | Automatic        |
| ISO Storage   | `local`          |
| Guest Type    | Linux            |
| Guest Version | 6.x - 2.6 Kernel |

The VM ID is assigned automatically by Proxmox.

---

## System

| Setting         | Standard           |
| --------------- | ------------------ |
| Machine         | `q35`              |
| BIOS            | OVMF (UEFI)        |
| EFI Disk        | Enabled            |
| EFI Storage     | Proxmox VM storage |
| Pre-Enroll keys | Disabled           |
| SCSI Controller | VirtIO SCSI single |
| QEMU Agent      | Enabled            |

### Rationale

`q35` provides a modern virtual machine chipset model.
UEFI is used as the standard firmware interface.
The VirtIO SCSI controller provides efficient virtual storage connectivity.
The QEMU Guest Agent improves guest integration and allows Proxmox to obtain guest-level information.

---

# Storage Standard

The project uses a **two-disk VM standard** for Linux workloads.

```text
VM
├── SCSI 0 — Operating System
└── SCSI 1 — Role-specific Data
```

This provides a clear separation between the operating system and persistent workload data.

---

## Disk 0 — Operating System

The default operating-system disk is:

```text
20 GiB
```

Proxmox configuration:

| Setting      | Value              |
| ------------ | ------------------ |
| Bus / Device | SCSI 0             |
| Storage      | Proxmox VM storage |
| Disk Size    | 20 GiB             |
| Cache        | Write back         |
| Discard      | Enabled            |
| IO Thread    | Enabled            |

The operating-system disk follows this logical structure:

```text
Disk 0
├── EFI System Partition
├── /boot
└── vg_os
    ├── lv_root
    ├── lv_var
    ├── lv_home
    └── lv_tmp
```

The exact logical volume sizes depend on the operating system and workload.

---

## Disk 1 — Role-specific Data

The default data disk is:

```text
20 GiB
```

Proxmox configuration:

| Setting      | Value              |
| ------------ | ------------------ |
| Bus / Device | SCSI 1             |
| Storage      | Proxmox VM storage |
| Disk Size    | 20 GiB baseline    |
| Cache        | Write back         |
| Discard      | Enabled            |
| IO Thread    | Enabled            |

The data disk size can be increased when the workload requires additional persistent storage.

### Standard sizing

| Workload         | OS Disk |  Data Disk |
| ---------------- | ------: | ---------: |
| General Linux VM |  20 GiB |     20 GiB |
| `ipa01`          |  20 GiB |     20 GiB |
| `auto01`         |  20 GiB |     20 GiB |
| `db01`           |  20 GiB | **50 GiB** |
| `app01`          |  20 GiB | **50 GiB** |

The sizing is intentionally conservative and can be expanded as the project grows.

---

# Database Storage Model

The PostgreSQL VM follows a dedicated database storage layout.

```text
db01
│
├── SCSI 0 — 20 GiB
│   ├── EFI
│   ├── /boot
│   └── vg_os
│       ├── lv_root
│       ├── lv_var
│       ├── lv_home
│       └── lv_tmp
│
└── SCSI 1 — 50 GiB
    └── vg_data
        └── lv_pg_data
```

The database data is therefore separated from the operating system.
The current architecture deliberately avoids a third PostgreSQL disk.

---

# Docker Storage Model

The Docker application platform uses a dedicated second disk for persistent application data.

```text
app01
│
├── SCSI 0 — 20 GiB
│   ├── EFI
│   ├── /boot
│   └── vg_os
│
└── SCSI 1 — 50 GiB
    └── Docker / Application Data
```

The second disk is intended for persistent data such as:

* Docker volumes
* Application configuration
* Application databases where appropriate
* Uploaded files
* Repository data
* Service-specific persistent storage

The operating-system disk should not be used as the primary location for growing application data when the workload can be placed on the dedicated data disk.

---

# CPU Standard

Linux VMs use:

| Setting  | Standard       |
| -------- | -------------- |
| Sockets  | 1              |
| CPU Type | `host`         |
| Cores    | Role-dependent |

A typical starting point is:

```text
Sockets: 1
Cores: 4
CPU Type: host
```

The actual CPU allocation is adjusted according to workload.

Suggested baseline:

| VM       | vCPU |
| -------- | ---: |
| `ipa01`  |    2 |
| `db01`   |  2–4 |
| `app01`  |    4 |
| `auto01` |    2 |

`fw01` is sized separately according to its firewall and routing workload.

---

# Memory Standard

Memory allocation is workload-dependent.

A typical Linux VM starting profile is:

```text
Memory: 8192 MiB
Minimum Memory: 4096 MiB
Ballooning: Enabled
```

Suggested baseline:

| VM       |      RAM |
| -------- | -------: |
| `ipa01`  |    4 GiB |
| `db01`   |  4–8 GiB |
| `app01`  | 8–12 GiB |
| `auto01` |    4 GiB |

`app01` receives the highest allocation because it hosts multiple Docker services.
`db01` can receive additional memory when PostgreSQL workloads increase.

---

# Network Standard

Linux VMs use:

| Setting          | Standard                 |
| ---------------- | ------------------------ |
| Bridge           | `vmbr0`                  |
| Model            | VirtIO (paravirtualized) |
| Proxmox Firewall | Disabled by default      |

Network placement is determined by the network architecture.
VM isolation is supplemented by network segmentation and firewall policies enforced through `fw01`.

The Proxmox firewall may be enabled when a specific requirement exists.

---

# Application Isolation

Multiple applications may run on `app01`, but they should not automatically have unrestricted communication with each other.
Docker networks provide application-level segmentation.

```text
app01
│
├── Nginx
│
├── Keycloak
├── OpenBao
├── NetBox
├── Forgejo
├── Wiki.js
└── Other Services
       │
       └── Controlled access to db01
```

Services should communicate only with the systems and ports required for their operation.

This supports:

* Least privilege
* Zero Trust principles
* Reduced lateral movement
* Clear service boundaries

---

# Resource Allocation Principles

Because the architecture runs on a single physical host, resources must be allocated carefully.

The following principles apply:

1. Start with conservative resource allocations.
2. Monitor actual utilization.
3. Increase resources based on observed workload.
4. Avoid unnecessary CPU and memory reservations.
5. Give additional resources to database and application workloads when required.
6. Keep infrastructure services lightweight.
7. Prefer workload-based sizing over arbitrary resource allocation.

Resource allocation is therefore considered a tunable configuration rather than a fixed architectural requirement.

---

# Storage Principles

The storage architecture follows five main principles.

### 1. Two-Disk Standard

Linux VMs use two virtual disks.

### 2. OS/Data Separation

The operating system and persistent workload data are stored separately.

### 3. 20 GiB Baseline

Both disks use 20 GiB as the default baseline.

### 4. Workload-Based Expansion

Database and application workloads receive larger data disks when required.

### 5. No Unnecessary Disks

Additional disks should only be introduced when there is a clearly justified architectural requirement.

---

# Security Considerations

VM separation is one layer of the overall security architecture.

Additional controls include:

* Network segmentation
* Firewall policies
* Least privilege
* Identity-based access
* Service isolation
* Restricted administrative access
* Secret management
* Encrypted communication
* Minimal exposed services

Sensitive credentials should not be stored directly in:

* Git repositories
* Docker Compose files
* VM configuration files
* Infrastructure-as-code repositories

Secrets should be managed through the project's secret-management architecture.

---

# Backup and Recovery

VM snapshots can be useful for:

* Testing
* Maintenance
* Short-term rollback
* Configuration changes

Snapshots should not be treated as a complete backup strategy.

Critical persistent data includes:

* PostgreSQL databases
* Application data
* Identity data
* Git repositories
* Configuration
* Infrastructure definitions
* Secrets

Application-aware backups should be used for critical workloads where appropriate.

---

# VM Lifecycle

The expected VM lifecycle is:

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

The project should progressively automate VM provisioning and configuration using Ansible and OpenTofu.
This reduces manual configuration and configuration drift.

---

# Future Expansion

The current environment is intentionally designed for a single Proxmox host.

```text
Current
└── Proxmox Host
    ├── fw01
    ├── ipa01
    ├── db01
    ├── app01
    └── auto01
```

The architecture can later evolve toward multiple virtualization nodes and redundant services.

Potential future capabilities include:

* Multiple Proxmox nodes
* Identity service replicas
* PostgreSQL replication
* Application replicas
* Load balancing
* Centralized monitoring
* High availability

These capabilities are outside the scope of the current implementation.

---

# Design Summary

The Enterprise Reference Architecture uses a simple and consistent **two-disk VM standard**.

```text
Standard Linux VM

SCSI 0
└── 20 GiB
    └── Operating System

SCSI 1
└── 20 GiB baseline
    └── Role-specific Data
```

Workload-specific sizing is applied where required:

```text
db01
20 GiB OS + 50 GiB PostgreSQL Data

app01
20 GiB OS + 50 GiB Application Data
```

This approach keeps the infrastructure simple enough to run on modest hardware while maintaining clear separation between operating-system files and persistent workload data.
The VM design provides a consistent foundation for security, automation, storage management, and future infrastructure expansion.
