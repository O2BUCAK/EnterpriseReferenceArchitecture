# Resource Sheet

> **Enterprise Reference Architecture — FOSS Home Lab**

> [!IMPORTANT]
> **Reference / Planning Document**
>
> This Resource Sheet defines the resource model for the Enterprise Reference Architecture.
> It is not a live inventory and must not be interpreted as proof that every resource is currently deployed.
>
> Only resources explicitly marked **Implemented** have been installed and tested in the laboratory.

---

## 1. Purpose

The Resource Sheet provides a single reference for the infrastructure resources required by the architecture.

It complements:

- [VM Resource Matrix](vm-resource-matrix.md) — VM-level sizing and storage design
- [VM Design](../vm-design/vm-design.md) — VM configuration standards
- [Network Architecture](../network/network.md) — network segmentation
- [Port Map](../network/port-map.md) — service communication requirements
- [Security Architecture](../security/security.md) — security controls

The Resource Sheet answers:

```text
What resources exist?
What resources are required?
Where are they used?
How much capacity do they consume?
What is implemented today?
What remains planned?
```

---

## 2. Status Model

| Status | Meaning |
|---|---|
| **Implemented** | Installed, configured and tested in the laboratory |
| **Validated** | Implemented and explicitly verified against defined criteria |
| **Planned** | Defined by the reference architecture but not yet implemented |
| **Future** | Deferred to a later project phase |
| **Documented** | Design/reference information only |

---

## 3. Resource Layers

```text
Physical Hardware
      ↓
Virtualization
      ↓
Virtual Machines
      ↓
Container Platform
      ↓
Application Services
      ↓
Network / Storage / Identity Dependencies
```

---

## 4. Physical Resource

| Resource | Specification | Status |
|---|---|---|
| Physical Host | Dell Latitude 5540 | **Implemented** |
| CPU | Intel Core i7-1355U | **Implemented** |
| Physical Cores | 10 | **Implemented** |
| Logical Threads | 12 | **Implemented** |
| RAM | 32 GB DDR4-3200 | **Implemented** |
| Primary Storage | 512 GB PCIe NVMe Gen4 x4 | **Implemented** |
| Architecture | x86-64 / AMD64 | **Implemented** |
| Hypervisor | Proxmox VE | **Implemented** |

### Database Services

`db01` hosts the centralized stateful services:

```text
db01
├── PostgreSQL
└── Redis
```

Redis is provided for applications that explicitly require cache/background-task functionality.

### Reference Capacity

```text
CPU       10 physical cores
Threads   12 logical
RAM       32 GB
Storage   512 GB NVMe
```

---

## 5. Virtualization Resources

| Resource | Role | Status |
|---|---|---|
| Proxmox VE | Hypervisor | **Implemented** |
| VM networking | VirtIO / vmbr0 | Planned standard |
| QEMU Guest Agent | Linux VM baseline | Planned standard |
| UEFI / OVMF | Linux VM baseline | Planned standard |
| VirtIO SCSI single | Linux VM baseline | Planned standard |
| CPU type `host` | Linux VM baseline | Planned standard |

---

## 6. Virtual Machine Resources

| VM | Role | OS | vCPU | RAM | OS Disk | Data Disk | Total Disk | VLAN | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `fw01` | Firewall / Gateway | OPNsense | 2 | 4 GB | 40 GB | — | 40 GB | — | **Implemented** |
| `ipa01` | Identity / DNS | Fedora Server | 2 | 2 GB | 20 GB | 20 GB | 40 GB | 20 | **Planned** |
| `db01` | PostgreSQL + Redis | Pardus Server | 4 | 8 GB | 20 GB | 50 GB | 70 GB | 30 | **Planned** |
| `app01` | Docker Application Platform | Ubuntu Server | 4 | 10 GB | 20 GB | 50 GB | 70 GB | 40 | **Planned** |
| `auto01` | Automation | RHEL | 2 | 4 GB | 20 GB | 20 GB | 40 GB | 10 | **Planned** |
| **TOTAL** | | | **14** | **28 GB** | **120 GB** | **140 GB** | **260 GB** | | **Reference** |

---

## 7. Capacity Allocation

| Resource | Allocated | Physical Capacity | Reference Utilization |
|---|---:|---:|---:|
| vCPU | 14 | 12 logical threads | ~117% |
| RAM | 28 GB | 32 GB | 87.5% |
| Virtual Disk | 260 GB | 512 GB | ~50.8% |

Host memory headroom:

```text
32 GB - 28 GB = 4 GB
```

CPU oversubscription:

```text
14 vCPU / 12 logical threads ≈ 1.17 : 1
```

These are reference planning values, not performance guarantees.

---

## 8. Storage Resources

### Linux two-disk model

```text
Linux VM
├── Disk 1 — OS
│   ├── EFI
│   ├── /boot
│   └── vg_os
│       └── lv_root
│
└── Disk 2 — Data
    └── vg_data
        ├── lv_var
        ├── lv_home
        ├── lv_tmp
        └── Role-specific data
```

| Workload | Disk 1 | Disk 2 | Main Data |
|---|---:|---:|---|
| General Linux | 20 GiB | 20 GiB | Standard filesystems |
| FreeIPA | 20 GiB | 20 GiB | Identity data |
| PostgreSQL | 20 GiB | 50 GiB | `lv_pg_data` |
| Docker | 20 GiB | 50 GiB | `lv_app_data` |
| Automation | 20 GiB | 20 GiB+ | Automation data |

---

## 9. Network Resources

| VLAN | Name | Network | Primary Resource |
|---:|---|---|---|
| 10 | Management | `10.10.10.0/24` | Proxmox / automation |
| 20 | Identity | `10.10.20.0/24` | FreeIPA |
| 30 | Database | `10.10.30.0/24` | PostgreSQL |
| 40 | Application | `10.10.40.0/24` | Docker applications |

### Reference host addresses

| Host | Role | Address | Status |
|---|---|---|---|
| `fw01` | OPNsense | `10.10.10.1` | **Implemented** |
| `ipa01` | FreeIPA | `10.10.20.10` | Planned |
| `db01` | PostgreSQL | `10.10.30.10` | Planned |
| `app01` | Docker | `10.10.40.10` | Planned |
| `auto01` | Automation | `10.10.10.20` | Planned |

These addresses are documentation examples.

---

## 10. Container Platform Resources

### app01

| Resource | Allocation |
|---|---:|
| vCPU | 4 |
| RAM | 10 GB |
| OS Disk | 20 GB |
| Data Disk | 50 GB |
| Network | VLAN 40 |
| Status | **Planned** |

### Planned services

| Service | Function | Status |
|---|---|---|
| Nginx | Reverse proxy / ingress | Planned |
| Portainer | Docker management | Planned |
| Teleport CE | Privileged access | Planned |
| Keycloak | Application SSO | Planned |
| OpenBao | Secrets management | Planned |
| NetBox | IPAM / DCIM | Planned |
| Squid | Proxy | Planned |
| Forgejo | Git platform | Planned |
| Woodpecker CI | CI/CD | Planned |
| Wiki.js | Documentation | Planned |
| Project Pulp | Repository / artifact management | Planned |

Container resource limits should be determined from observed workload after deployment.

---

## 11. Database Resources

### db01

| Resource | Allocation | Status |
|---|---:|---|
| vCPU | 4 | Planned |
| RAM | 8 GB | Planned |
| OS Disk | 20 GB | Planned |
| Data Disk | 50 GB | Planned |
| PostgreSQL | Database platform | Planned |
| Network | VLAN 30 | Planned |

Database access model:

```text
Application
    ↓
Firewall policy
    ↓
db01:5432
    ↓
PostgreSQL
    ↓
Least-privileged database identity
```

---

## 12. Identity Resources

### ipa01

| Resource | Allocation | Status |
|---|---:|---|
| vCPU | 2 | Planned |
| RAM | 2 GB | Planned |
| OS Disk | 20 GB | Planned |
| Data Disk | 20 GB | Planned |
| Network | VLAN 20 | Planned |
| FreeIPA | Identity platform | Planned |
| DNS | Identity-related DNS | Planned |
| Kerberos | Authentication | Planned |
| LDAP / LDAPS | Directory services | Planned |

---

## 13. Automation Resources

### auto01

| Resource | Allocation | Status |
|---|---:|---|
| vCPU | 2 | Planned |
| RAM | 4 GB | Planned |
| OS Disk | 20 GB | Planned |
| Data Disk | 20 GB | Planned |
| Network | VLAN 10 | Planned |
| Ansible | Configuration management | Planned |
| OpenTofu | Infrastructure as Code | Planned |

The lab has not yet reached the Automation & IaC phase.

---

## 14. Firewall Resources

### fw01

| Resource | Allocation | Status |
|---|---:|---|
| Platform | OPNsense | **Implemented** |
| vCPU | 2 | **Implemented allocation** |
| RAM | 4 GB | **Implemented allocation** |
| Storage | 40 GB | **Implemented allocation** |
| Role | Firewall / routing / segmentation | **Implemented** |

---

## 15. Resource Dependency Map

```text
Dell Latitude 5540
        |
    Proxmox VE
        |
   +----+---------------------------+
   |    |      |      |             |
 fw01  ipa01  db01   app01        auto01
   |     |      |      |             |
OPNsense FreeIPA PostgreSQL Docker  Ansible
                         |
                  Application Services
```

---

## 16. Dependency Summary

| Resource | Depends On | Used By |
|---|---|---|
| Proxmox VE | Physical host | All VMs |
| fw01 | Proxmox | Network / security |
| ipa01 | Proxmox + VLAN 20 | Identity-dependent services |
| db01 | Proxmox + VLAN 30 | Application services |
| app01 | Proxmox + VLAN 40 | Container workloads |
| auto01 | Proxmox + VLAN 10 | Future automation |
| PostgreSQL | db01 | Stateful applications |
| Docker | app01 | Application services |
| FreeIPA | ipa01 | Infrastructure identity |
| OpenBao | app01 | Secret-dependent services |
| Keycloak | app01 + PostgreSQL | Application SSO |
| Forgejo | app01 + PostgreSQL / storage | Git workflows |
| Wiki.js | app01 + PostgreSQL / storage | Documentation |
| NetBox | app01 + PostgreSQL / storage | Infrastructure inventory |

---

## 17. Current Resource Status

| Resource | Status |
|---|---|
| Dell Latitude 5540 host | **Implemented** |
| Proxmox VE | **Implemented** |
| OPNsense / fw01 | **Implemented** |
| FreeIPA / ipa01 | Planned |
| PostgreSQL / db01 | Planned |
| Docker / app01 | Planned |
| Ansible / OpenTofu / auto01 | Planned |
| Planned application containers | Planned |
| Full VLAN implementation | Planned / requires validation |
| Full target security controls | Planned / requires validation |

---

## 18. Document Responsibilities

| Document | Responsibility |
|---|---|
| **Resource Sheet** | Overall physical, virtual, storage, network and platform resource view |
| **VM Resource Matrix** | Detailed VM sizing and storage allocation |
| **VM Design** | VM configuration standards |
| **Port Map** | Service and port dependencies |
| **Firewall Rule Set** | Network traffic enforcement |
| **Storage Architecture** | Disk and filesystem design |
| **Security Architecture** | Security principles and controls |

---

## Related Documentation

- [VM Resource Matrix](vm-resource-matrix.md)
- [VM Design](../vm-design/vm-design.md)
- [Network Architecture](../network/network.md)
- [Port Map](../network/port-map.md)
- [Firewall Rule Set](../network/firewall-rule-set.md)
- [Storage Architecture](../architecture/storage.md)
- [Security Architecture](../security/security.md)
- [Architecture Overview](../architecture/overview.md)

---

## Summary

Reference totals:

```text
vCPU:       14
RAM:        28 GB
VM storage: 260 GB
Host RAM:   32 GB
Host disk:  512 GB
```

> **The Resource Sheet describes the target resource model. Implementation status must always be confirmed from laboratory evidence.**
