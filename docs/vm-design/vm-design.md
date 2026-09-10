# VM Design

> Virtual machine design standards for the Enterprise Reference Architecture.

## Purpose

This document defines the **reference design** for virtual machines, resource allocation, storage layout and Proxmox configuration.

> [!IMPORTANT]
> This document describes architecture and planned sizing. It is **not a live inventory**.
>
> **Implemented in the laboratory:** Proxmox VE and the OPNsense firewall VM.
>
> The remaining VMs and application services described below are **Planned** unless explicitly documented as implemented.

---

## Virtualization Platform

The virtualization platform is **Proxmox VE**.

```text
Physical Host
└── Proxmox VE
    ├── fw01       [Implemented]
    ├── ipa01      [Planned]
    ├── db01       [Planned]
    ├── app01      [Planned]
    └── auto01     [Planned]
```

The target design separates firewalling, identity, database, application and automation responsibilities.

---

# VM Design Matrix

| VM | Operating System | Primary Role | Status |
|---|---|---|---|
| `fw01` | OPNsense | Firewall, routing and network security | **Implemented** |
| `ipa01` | Fedora Server | FreeIPA identity and authentication | **Planned** |
| `db01` | Pardus Server | PostgreSQL database | **Planned** |
| `app01` | Ubuntu Server | Docker application platform | **Planned** |
| `auto01` | RHEL | Ansible and OpenTofu automation | **Planned** |

Each VM has a clearly defined primary responsibility. The architecture intentionally avoids combining unrelated infrastructure services into a single VM.

---

# Naming Convention

VM names use the role-based convention `<role><number>`.

```text
fw01
ipa01
db01
app01
auto01
```

The old names `docker01` and `rhel01` are deprecated. They must not be used in new documentation or configuration.

---

# VM Role Design

## fw01 — Firewall

**Status: Implemented**

`fw01` is the OPNsense firewall/router VM used for the network-security role. The Linux VM storage model does not apply to this appliance.

Reference allocation: **2 vCPU / 4 GiB RAM / 40 GiB storage**.

## ipa01 — Identity

**Status: Planned**

`ipa01` is the planned Fedora Server VM for FreeIPA. Planned responsibilities include identity management, authentication, authorization, Kerberos, LDAP, host enrollment and identity-related DNS integration.

Reference sizing: **2 vCPU / 2 GiB RAM / 20 GiB OS disk + 20 GiB data disk**.

## db01 — Database

**Status: Planned**

`db01` is the planned Pardus Server VM for PostgreSQL.

Reference sizing: **4 vCPU / 8 GiB RAM / 20 GiB OS disk + 50 GiB data disk**.

The PostgreSQL data directory is planned for the second disk. A third dedicated PostgreSQL disk is not part of the current architecture.

## app01 — Application Platform

**Status: Planned**

`app01` is the planned Ubuntu Server VM for the Docker application platform.

Planned services include Nginx, Portainer, Teleport CE, Keycloak, OpenBao, NetBox, Squid Gateway, Forgejo, Woodpecker CI, Wiki.js and Project Pulp.

These services are **planned**, not current implementation claims.

Reference sizing: **4 vCPU / 10 GiB RAM / 20 GiB OS disk + 50 GiB data disk**.

Persistent application data is planned for the second disk.

## auto01 — Automation

**Status: Planned**

`auto01` is the planned RHEL VM for Ansible and OpenTofu.

Automation has **not yet been implemented in the laboratory**. The VM remains a planned architecture component.

Reference sizing: **2 vCPU / 4 GiB RAM / 20 GiB OS disk + 20 GiB data disk**.

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
| SCSI Controller | VirtIO SCSI single |
| QEMU Guest Agent | Enabled |
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

## Disk 1 — Operating System

Default size: **20 GiB**.

```text
Disk 1
├── EFI System Partition
├── /boot
└── vg_os
    └── lv_root
```

## Disk 2 — System / Application Data

Default baseline: **20 GiB**.

```text
Disk 2
└── vg_data
    ├── lv_var
    ├── lv_home
    ├── lv_tmp
    └── Role-specific Data
```

`/var`, `/home` and `/tmp` are intentionally placed on **Disk 2**. Workloads such as PostgreSQL and Docker therefore keep their persistent data outside the OS disk.

### Reference sizing

| Workload | OS Disk | Data Disk |
|---|---:|---:|
| General Linux VM | 20 GiB | 20 GiB |
| `ipa01` | 20 GiB | 20 GiB |
| `auto01` | 20 GiB | 20 GiB |
| `db01` | 20 GiB | 50 GiB |
| `app01` | 20 GiB | 50 GiB |

---

# CPU Standard

Linux VMs use one socket and CPU type `host`. Reference allocations are:

| VM | vCPU |
|---|---:|
| `ipa01` | 2 |
| `db01` | 4 |
| `app01` | 4 |
| `auto01` | 2 |

`fw01` is sized separately according to firewall and routing workload.

---

# Memory Standard

Reference allocations are:

| VM | RAM |
|---|---:|
| `ipa01` | 2 GiB |
| `db01` | 8 GiB |
| `app01` | 10 GiB |
| `auto01` | 4 GiB |

`app01` receives a larger allocation because multiple application services are planned for the VM. `db01` can be increased after workload testing.

---

# Network Standard

Linux VMs use VirtIO networking on `vmbr0`.

Network placement follows the network architecture:

| VLAN | Purpose |
|---:|---|
| 10 | Management |
| 20 | Identity / Core |
| 30 | Database |
| 40 | Application |

VM isolation is supplemented by VLAN segmentation and firewall policies through `fw01`.

---

# Application Isolation

Multiple applications are planned for `app01`, but they should not automatically have unrestricted communication with each other. Docker networks should provide application-level segmentation.

Services should communicate only with the systems and ports required for their operation.

---

# Resource Allocation Principles

Because the architecture targets a single physical host:

1. Start with conservative resource allocations.
2. Keep host headroom available.
3. Increase resources based on observed utilization.
4. Avoid unnecessary reservations.
5. Give database and application workloads additional resources when justified.
6. Keep infrastructure services lightweight.
7. Treat resource allocation as a tunable reference, not a fixed production specification.

---

# Security Considerations

VM separation is one layer of the security architecture. Additional planned controls include network segmentation, firewall policies, least privilege, identity-based access, restricted administrative access, secret management, encrypted communication and minimal exposed services.

Sensitive credentials must not be stored directly in Git repositories, Docker Compose files, VM configuration files or infrastructure-as-code repositories.

---

# Backup and Recovery

VM snapshots are useful for testing, maintenance, short-term rollback and configuration changes, but they are not a complete backup strategy.

Critical persistent data will include PostgreSQL databases, application data, identity data, Git repositories, configuration, infrastructure definitions and secrets once those workloads are implemented.

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

Infrastructure provisioning and configuration automation with Ansible and OpenTofu is a **planned future stage**. It is not currently implemented in the laboratory.

---

# Future Expansion

Potential future capabilities include multiple Proxmox nodes, identity replicas, PostgreSQL replication, application replicas, load balancing, centralized monitoring and high availability.

These capabilities are outside the current implementation scope.

---

# Design Summary

```text
Standard Linux VM

SCSI 0
└── 20 GiB
    └── Operating System

SCSI 1
└── 20 GiB baseline
    ├── /var
    ├── /home
    ├── /tmp
    └── Role-specific Data
```

Workload-specific sizing:

```text
db01
20 GiB OS + 50 GiB PostgreSQL Data

app01
20 GiB OS + 50 GiB Application Data
```

This design keeps the infrastructure simple enough for modest hardware while maintaining clear separation between operating-system files and persistent workload data.
