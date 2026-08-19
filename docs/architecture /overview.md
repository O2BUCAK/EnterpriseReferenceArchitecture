# Architecture Overview

## 1. Purpose

This document describes the high-level architecture of the **Enterprise Reference Architecture** homelab environment.

The architecture is designed to simulate a small enterprise infrastructure using open-source technologies while providing a practical environment for learning and demonstrating:

* Linux system administration
* Network and firewall architecture
* Identity management
* Database services
* Container platforms
* Infrastructure automation
* Infrastructure as Code
* Security architecture
* Operational practices

This document defines the **logical architecture and component relationships**.

Detailed network addressing, VLANs, firewall rules, VM storage layouts, and operational procedures are documented separately.

---

# 2. Architecture Goals

The architecture has the following primary goals:

1. Build a realistic but resource-efficient enterprise infrastructure.
2. Separate infrastructure responsibilities by function.
3. Centralize identity and access management.
4. Separate database workloads from application workloads.
5. Provide a dedicated automation and Infrastructure as Code platform.
6. Run application workloads through a container platform.
7. Establish clear security boundaries.
8. Minimize unnecessary trust between systems.
9. Make infrastructure configuration repeatable.
10. Document the environment so that it can be reproduced without access to private infrastructure information.

---

# 3. High-Level Architecture

The current environment consists of five primary virtual machines:

| VM       | Platform | Primary Role                    |
| -------- | -------- | ------------------------------- |
| `fw01`   | OPNsense | Firewall / Router               |
| `ipa01`  | Fedora   | Identity / FreeIPA              |
| `db01`   | Pardus   | PostgreSQL Database             |
| `app01`  | Ubuntu   | Docker Application Platform     |
| `auto01` | RHEL     | Automation / Ansible / OpenTofu |

The logical relationship between these systems is:

```text
                         Internet
                            │
                            ▼
                     ┌─────────────┐
                     │    fw01     │
                     │  OPNsense   │
                     │ Firewall /  │
                     │   Router    │
                     └──────┬──────┘
                            │
                    ┌───────┴────────┐
                    │    Internal    │
                    │    Network     │
                    └───────┬────────┘
                            │
       ┌────────────┬───────┼────────┬────────────┐
       │            │       │        │            │
       ▼            ▼       ▼        ▼            ▼
   ┌───────┐    ┌───────┐ ┌───────┐ ┌───────┐
   │ ipa01 │    │ db01  │ │ app01 │ │auto01 │
   │Fedora │    │Pardus │ │Ubuntu │ │ RHEL  │
   │FreeIPA│    │Postgre│ │ Docker│ │Ansible│
   │       │    │ SQL   │ │       │ │OpenTofu│
   └───────┘    └───────┘ └───┬───┘ └───────┘
                               │
                         ┌─────┴─────┐
                         │   Docker  │
                         │ Containers│
                         └───────────┘
```

The diagram represents the logical architecture.

Actual IP addresses, VLAN identifiers, DNS records, credentials, and other environment-specific information are intentionally excluded from public documentation.

---

# 4. Component Architecture

## 4.1 fw01 — Network Security Gateway

### Platform

**OPNsense**

### Role

`fw01` is the primary network security and routing component.

### Responsibilities

* Firewall
* Routing
* NAT
* Network segmentation
* DHCP where required
* DNS forwarding/resolution where appropriate
* VPN capabilities where required
* Traffic filtering
* Security policy enforcement

### Architectural Position

`fw01` is positioned at the boundary between the external network and the internal infrastructure.

```text
External Network
       │
       ▼
     fw01
       │
       ▼
Internal Infrastructure
```

All internal systems should use explicit network policies rather than assuming unrestricted communication.

Detailed network segmentation and firewall policies are documented under:

```text
docs/network/
```

---

# 5. ipa01 — Identity Platform

## Platform

**Fedora Linux**

## Primary Service

**FreeIPA**

## Role

`ipa01` provides centralized identity management for Linux-oriented infrastructure.

### Responsibilities

* User management
* Group management
* Host management
* Kerberos authentication
* LDAP directory services
* Centralized authentication
* Access control
* Identity-based administration

### Architectural Position

`ipa01` acts as a shared infrastructure service.

Other systems may consume identity services from `ipa01` where appropriate.

```text
                 ipa01
              ┌─────────┐
              │ FreeIPA │
              └────┬────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
      Hosts      Users      Access
```

The architecture does not assume that every service must depend on FreeIPA.

Service dependencies should be explicitly defined according to operational requirements.

---

# 6. db01 — Database Platform

## Platform

**Pardus Linux**

## Database

**PostgreSQL**

## Role

`db01` provides persistent relational database services.

### Responsibilities

* PostgreSQL
* Application database storage
* Database access control
* Persistent data management
* Database backup
* Database recovery
* Database administration

### Architectural Position

The database platform is intentionally separated from the application platform.

```text
        app01
          │
          │ Database connection
          ▼
        db01
          │
          ▼
      PostgreSQL
```

This separation provides:

* Clear workload boundaries
* Independent database management
* Reduced application/database coupling
* Easier backup management
* Better operational visibility
* A more realistic enterprise architecture

---

# 7. app01 — Application Platform

## Platform

**Ubuntu Linux**

## Container Platform

**Docker**

## Role

`app01` is the primary application and container host.

Applications are deployed as containers where appropriate.

### Planned / Current Services

The application platform may host services such as:

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

The exact deployment state is expected to evolve during the project.

### Architectural Position

`app01` is a container host, not a general-purpose database server.

```text
                       app01
                         │
                 ┌───────┴───────┐
                 │     Docker    │
                 └───────┬───────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
      Application    Management      Platform
      Containers     Containers     Services
```

Container-to-container and container-to-infrastructure communication should be explicitly defined.

---

# 8. auto01 — Automation Platform

## Platform

**RHEL**

## Tools

* Ansible
* OpenTofu

## Role

`auto01` is the dedicated infrastructure automation and Infrastructure as Code host.

### Responsibilities

* Configuration management
* Ansible execution
* Infrastructure automation
* Infrastructure as Code
* Provisioning workflows
* Operational scripts
* Configuration validation
* Automation testing

### Architectural Position

`auto01` is an independent infrastructure node connected to the internal network.

It is **not a child of `app01` and is not part of the Docker application hierarchy**.

```text
                    Internal Network
                           │
             ┌─────────────┴─────────────┐
             │                           │
           app01                       auto01
             │                           │
          Docker                  Ansible / OpenTofu
             │                           │
        Containers                Infrastructure
```

`auto01` may manage other systems through controlled administrative channels.

Examples include:

```text
auto01
  │
  ├── Ansible ──────► ipa01
  │
  ├── Ansible ──────► db01
  │
  ├── Ansible ──────► app01
  │
  └── OpenTofu ─────► Infrastructure
```

Automation access should follow least-privilege principles.

---

# 9. Component Relationships

The primary logical relationships are:

| Source           | Target               | Purpose                          |
| ---------------- | -------------------- | -------------------------------- |
| External Network | `fw01`               | Network boundary                 |
| `fw01`           | Internal Network     | Routing / Security               |
| `ipa01`          | Internal Systems     | Identity services                |
| `app01`          | `db01`               | Application database access      |
| `auto01`         | Infrastructure Nodes | Configuration management         |
| `auto01`         | Infrastructure       | IaC / provisioning               |
| `app01`          | Docker Containers    | Application execution            |
| Containers       | `ipa01`              | Identity services where required |
| Containers       | `db01`               | Database services where required |

These relationships describe intended logical dependencies rather than unrestricted network connectivity.

Actual permitted traffic should be defined through network and firewall policy.

---

# 10. Trust Boundaries

The architecture uses multiple logical trust boundaries.

## Boundary 1 — External / Internal

```text
Internet
   │
   │
  fw01
   │
   ▼
Internal Infrastructure
```

`fw01` provides the primary boundary.

---

## Boundary 2 — Infrastructure / Application

Infrastructure services and application workloads should not automatically trust each other.

For example:

```text
Infrastructure
 ├── ipa01
 └── db01

Application
 └── app01
```

Access should be explicitly permitted where required.

---

## Boundary 3 — Automation

`auto01` has elevated administrative capabilities.

Therefore:

```text
auto01
   │
   ├──► ipa01
   ├──► db01
   └──► app01
```

Automation credentials and privileges must be carefully controlled.

Compromise of `auto01` could potentially affect multiple systems.

---

## Boundary 4 — Container Platform

Containers running on `app01` should not automatically have access to:

* Host management interfaces
* Internal infrastructure
* Database services
* Identity services
* Other containers

Access should be granted only when required.

---

# 11. Data Flow

A typical application request follows a logical flow similar to:

```text
Client
  │
  ▼
fw01
  │
  ▼
app01
  │
  ├──────────────► ipa01
  │                 Identity
  │
  └──────────────► db01
                    PostgreSQL
```

The exact traffic flow depends on the application.

Not every application requires access to every infrastructure service.

---

# 12. Management Flow

Administrative operations are centered around `auto01`.

```text
Administrator
      │
      ▼
    auto01
      │
      ├────────► ipa01
      │
      ├────────► db01
      │
      └────────► app01
```

Where practical, administrative changes should be performed through automation rather than manually repeated configuration.

The intended operational model is:

```text
Configuration
      │
      ▼
   GitHub
      │
      ▼
   Ansible / OpenTofu
      │
      ▼
 Infrastructure
```

This creates a version-controlled infrastructure workflow.

---

# 13. Storage Architecture

Storage is designed according to workload requirements.

The general VM storage model separates:

* Operating system storage
* Application/data storage
* Database data

For `db01`, the current design uses two virtual disks:

```text
Disk 1
│
├── EFI
├── /boot
└── LVM
    └── vg_os
        ├── lv_root
        ├── lv_var
        ├── lv_home
        └── lv_tmp

Disk 2
│
└── LVM
    └── vg_data
        └── lv_pg_data
```

Detailed VM storage definitions are maintained under:

```text
docs/vm-design/
```

---

# 14. Security Model

The architecture follows these security principles:

### Least Privilege

Systems and users receive only the permissions required for their responsibilities.

### Explicit Communication

Infrastructure services should communicate through defined and documented paths.

### Network Segmentation

Network segmentation will be introduced according to workload and trust boundaries.

### Centralized Identity

Identity should be centrally managed where practical.

### Secrets Separation

Credentials and secrets must not be stored in Git.

### Secure Administration

Administrative interfaces should not be unnecessarily exposed.

### Infrastructure as Code

Infrastructure configuration should progressively become version-controlled and reproducible.

---

# 15. Public Documentation Security

This repository is public.

Therefore, architecture documentation intentionally avoids exposing private environment information.

The following must not be committed:

* Passwords
* API tokens
* SSH private keys
* TLS private keys
* Database credentials
* VPN secrets
* Cloud credentials
* Personal information
* Private network details where inappropriate
* Real internal DNS records
* Recovery codes

Public documentation should use safe placeholders.

Example:

```text
service.example.com
```

instead of a real private or personal hostname.

---

# 16. Current Architecture Scope

The current architecture consists of:

```text
Virtualization
└── Proxmox VE
    │
    ├── fw01
    │   └── OPNsense
    │
    ├── ipa01
    │   └── Fedora + FreeIPA
    │
    ├── db01
    │   └── Pardus + PostgreSQL
    │
    ├── app01
    │   └── Ubuntu + Docker
    │
    └── auto01
        └── RHEL + Ansible + OpenTofu
```

This architecture is intentionally small enough to operate on a constrained homelab environment while still representing multiple enterprise infrastructure concepts.

---

# 17. Future Architecture Evolution

The architecture is expected to evolve incrementally.

Potential future improvements include:

* VLAN-based segmentation
* Dedicated management network
* Dedicated application network
* Database network isolation
* Centralized logging
* Monitoring
* Backup infrastructure
* High-availability experiments
* Automated provisioning
* CI/CD pipelines
* Security testing
* Policy-as-Code
* Automated compliance checks
* Infrastructure testing

Future additions should preserve the project's core principles of security, separation of responsibilities, automation, and reproducibility.

---

# 18. Related Documentation

Detailed documentation will be maintained in the following areas:

```text
docs/
├── architecture/
├── network/
├── security/
├── vm-design/
└── operations/
```

### Architecture

High-level system architecture and component relationships.

### Network

VLANs, subnets, routing, firewall policies, traffic flows, and network segmentation.

### Security

Threat model, security controls, hardening, trust boundaries, and security procedures.

### VM Design

VM resources, operating-system installation, storage layout, and system configuration.

### Operations

Backup, recovery, monitoring, maintenance, troubleshooting, and operational procedures.
