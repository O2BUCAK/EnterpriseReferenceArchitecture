# Enterprise Reference Architecture

A practical, open-source enterprise IT reference architecture and homelab project designed to simulate a small enterprise environment with a strong focus on **security, identity, networking, infrastructure automation, containerization, and operational practices**.

The project is built primarily with **Free and Open Source Software (FOSS)** and is designed to be documented and reproducible without exposing private infrastructure details.

> **Project status:** Active development
> **Environment:** Virtualized homelab / lab environment
> **Documentation:** Public
> **Sensitive infrastructure data:** Intentionally excluded

---

## Overview

**Enterprise Reference Architecture** is a hands-on infrastructure project that demonstrates how several enterprise IT building blocks can be integrated into a coherent architecture.

The environment is based on a small virtualized infrastructure consisting of:

* Network security and routing
* Centralized identity management
* Relational database services
* Containerized application services
* Infrastructure automation
* Infrastructure as Code

The architecture is intentionally designed to provide practical experience with technologies commonly encountered in modern infrastructure, platform engineering, DevOps, and security-oriented environments.

---

## Architecture

The current reference architecture consists of five primary virtual machines:

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
                     Internal Network
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
   │    ipa01    │   │    db01     │   │    app01    │
   │   Fedora    │   │   Pardus    │   │   Ubuntu    │
   │   FreeIPA   │   │ PostgreSQL  │   │   Docker    │
   │   Identity  │   │  Database   │   │ Application │
   └─────────────┘   └─────────────┘   └─────────────┘
                                             │
                                             │
                                      Container Platform
                                             │
                                             ▼
                                      ┌─────────────┐
                                      │    auto01   │
                                      │    RHEL     │
                                      │   Ansible   │
                                      │   OpenTofu  │
                                      └─────────────┘
```

The diagram represents the logical architecture rather than exposing real network addresses or other environment-specific information.

---

## Design Principles

The architecture follows several core principles.

### Security First

Security is treated as an architectural concern rather than a separate component.

Key principles include:

* Least privilege
* Network segmentation
* Explicit service-to-service communication
* Centralized identity
* Secure administration
* No plaintext secrets in source control
* Separation of infrastructure and application responsibilities
* Minimal exposure of externally accessible services

### Zero Trust Approach

The project follows a practical Zero Trust mindset:

> Never implicitly trust a system simply because it is located inside the internal network.

Authentication, authorization, segmentation, and explicit communication paths are preferred over implicit internal trust.

### Zero Plaintext

Sensitive information must never be committed to the public repository.

Examples include:

* Passwords
* API tokens
* SSH private keys
* TLS private keys
* Recovery codes
* Database credentials
* VPN credentials
* Cloud credentials
* Internal IP information that should remain private

Example or placeholder values should be used in public documentation.

### Automation First

Manual configuration is used primarily for initial bootstrap and troubleshooting.

Repeatable configuration should progressively move toward:

* Ansible
* OpenTofu
* Shell scripting
* Container definitions
* CI/CD automation

### Reproducibility

The architecture should be understandable and reproducible by another engineer without requiring access to the original private environment.

---

# Infrastructure Components

## fw01 — Network Security Gateway

**Operating system / platform:** OPNsense

`fw01` provides the network security and routing layer of the environment.

Primary responsibilities include:

* Firewalling
* Routing
* Network segmentation
* NAT
* DHCP where required
* DNS forwarding/resolution where appropriate
* VPN capabilities where required
* Traffic control
* Network security policy enforcement

`fw01` is the primary security boundary between the external network and the internal lab environment.

---

## ipa01 — Identity Management

**Operating system:** Fedora
**Primary service:** FreeIPA

`ipa01` provides centralized identity and authentication services for Linux-oriented infrastructure.

Responsibilities include:

* Identity management
* User and group management
* Host enrollment
* Kerberos authentication
* LDAP directory services
* Centralized access control
* Policy management

The purpose of this system is to demonstrate centralized enterprise identity rather than maintaining independent local accounts on every server.

---

## db01 — Database Platform

**Operating system:** Pardus
**Database:** PostgreSQL

`db01` provides the relational database layer for applications requiring persistent SQL storage.

Primary responsibilities include:

* PostgreSQL database services
* Application database storage
* Database access control
* Persistent data management
* Backup and recovery procedures
* Database monitoring and operational practices

The database server is intentionally separated from the application/container host.

### Storage Design

The current design uses two virtual disks.

**Disk 1 — Operating System**

```text
EFI
└── /boot

LVM
└── vg_os
    ├── lv_root
    ├── lv_var
    ├── lv_home
    └── lv_tmp
```

**Disk 2 — Database Data**

```text
LVM
└── vg_data
    └── lv_pg_data
```

This separation provides a clearer distinction between operating-system storage and PostgreSQL data.

---

## app01 — Application and Container Platform

**Operating system:** Ubuntu
**Container platform:** Docker

`app01` provides the primary application and container execution environment.

The platform is designed to host multiple FOSS services while maintaining logical separation between applications.

Planned/current application services include:

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

The exact deployment state may change as the project evolves.

Application containers should not automatically receive unrestricted access to every infrastructure service.

Where appropriate, communication should be explicitly defined through dedicated Docker networks and firewall policies.

---

## auto01 — Automation and Infrastructure as Code

**Operating system:** RHEL
**Primary tools:**

* Ansible
* OpenTofu

`auto01` is the automation and infrastructure management node.

Responsibilities include:

* Configuration management
* Infrastructure automation
* Provisioning workflows
* Repeatable system configuration
* Infrastructure as Code
* Operational scripts
* Automation testing

The goal is to reduce configuration drift and demonstrate infrastructure management using declarative and repeatable processes.

---

# Virtualization

The environment runs on a Proxmox VE virtualization platform.

The virtual machines are logically separated according to their responsibilities.

| VM       | OS / Platform | Primary Role          |
| -------- | ------------- | --------------------- |
| `fw01`   | OPNsense      | Firewall / Router     |
| `ipa01`  | Fedora        | FreeIPA / Identity    |
| `db01`   | Pardus        | PostgreSQL            |
| `app01`  | Ubuntu        | Docker / Applications |
| `auto01` | RHEL          | Ansible / OpenTofu    |

The exact CPU, memory, storage, IP addressing, VLAN identifiers, and other environment-specific parameters are intentionally documented separately where appropriate.

---

# Network Architecture

Network design is based on segmentation and explicit communication requirements.

The logical model separates:

```text
External / WAN
      │
      ▼
    fw01
      │
      ├── Management
      ├── Infrastructure
      ├── Application
      └── Database
```

Actual addressing information is intentionally excluded from the public repository.

Public documentation should use:

* Documentation IP ranges
* Placeholder hostnames
* `example.com`
* RFC-reserved example values
* Generic configuration examples

Real production or home-network addressing must never be committed.

Detailed network documentation will be maintained under:

```text
docs/network/
```

---

# Security Architecture

Security controls are implemented at multiple layers.

## Network Layer

* Firewall policies
* Network segmentation
* Restricted management access
* Explicit service communication
* Limited exposure of administrative interfaces

## Identity Layer

* Centralized authentication
* Role-based access
* Least privilege
* Controlled administrative access

## Host Layer

* Minimal installed services
* SSH hardening
* Firewall configuration
* System updates
* Logging
* Secure configuration baselines

## Application Layer

* Container isolation
* Restricted network access
* Secrets management
* Authentication and authorization
* Minimal service exposure

## Repository Layer

The public repository must never contain:

* Credentials
* Secrets
* Private keys
* Production configuration
* Personal information
* Private IP addresses where inappropriate
* Internal DNS records
* VPN configuration containing secrets
* Cloud credentials
* Access tokens

---

# Secrets Management

Secrets should not be stored directly in Git.

The architecture includes **OpenBao** as a FOSS secrets-management component.

Sensitive values should be injected into applications and automation workflows rather than hard-coded into:

* Docker Compose files
* Ansible playbooks
* OpenTofu configuration
* Shell scripts
* Documentation

For examples, use placeholders such as:

```text
YOUR_SECRET
CHANGE_ME
example-password
```

These values must never represent real credentials.

---

# Automation

Automation is a core part of the project.

The repository will contain separate automation layers:

```text
ansible/
opentofu/
scripts/
docker/
```

### Ansible

Used primarily for:

* OS configuration
* Package installation
* Service configuration
* User and permission management
* Hardening
* Application prerequisites
* Repeatable operational tasks

### OpenTofu

Used for Infrastructure as Code where appropriate.

Potential responsibilities include:

* Infrastructure provisioning
* VM definitions
* Network-related infrastructure
* Repeatable resource configuration

### Scripts

Small operational tasks may be implemented using:

```text
scripts/
├── bash/
└── powershell/
```

Scripts should remain focused, documented, and safe to execute.

---

# Container Platform

Docker is used as the application container platform.

The goal is to maintain clear boundaries between:

* Application containers
* Infrastructure services
* Database services
* Management interfaces
* Security-sensitive services

Example logical structure:

```text
app01
│
├── Reverse Proxy
│
├── Application Services
│
├── Management Services
│
├── Identity Services
│
└── CI/CD Services
```

Container network design and service dependencies are documented separately.

---

# Repository Structure

```text
EnterpriseReferenceArchitecture/
│
├── docs/
│   ├── architecture/
│   ├── network/
│   ├── security/
│   ├── vm-design/
│   └── operations/
│
├── ansible/
│
├── opentofu/
│
├── docker/
│
├── scripts/
│   ├── bash/
│   └── powershell/
│
└── README.md
```

### `docs/architecture/`

Contains high-level architecture documentation and diagrams.

### `docs/network/`

Contains logical network architecture, segmentation, traffic flows, and addressing examples.

### `docs/security/`

Contains security architecture, threat considerations, hardening standards, and security controls.

### `docs/vm-design/`

Contains VM specifications, storage layouts, operating-system standards, and installation procedures.

### `docs/operations/`

Contains operational procedures, maintenance, backup, recovery, monitoring, and troubleshooting documentation.

### `ansible/`

Contains Ansible inventories, roles, playbooks, variables, and automation components.

### `opentofu/`

Contains Infrastructure as Code configurations.

### `docker/`

Contains container definitions, Compose configurations, network definitions, and application deployment configuration.

### `scripts/`

Contains supporting Bash and PowerShell automation.

---

# Documentation Standards

Documentation should be:

* Reproducible
* Version controlled
* Explicit about assumptions
* Free from sensitive information
* Written for another engineer to understand
* Supported by diagrams where appropriate

Environment-specific information should be replaced with documented placeholders.

For example:

```text
https://service.example.com
```

rather than an actual private or personal domain.

---

# Public Repository Security Rules

Before every public commit, verify that the repository does not contain:

```text
[ ] Passwords
[ ] API tokens
[ ] SSH private keys
[ ] TLS private keys
[ ] Database credentials
[ ] VPN secrets
[ ] Cloud credentials
[ ] Personal information
[ ] Real internal IP addressing where inappropriate
[ ] Private DNS information
[ ] Backup credentials
[ ] Recovery codes
```

Secret detection and repository security tooling should be added as the project matures.

---

# Project Roadmap

## Phase 1 — Architecture Foundation

* [x] Proxmox virtualization platform
* [x] `fw01`
* [x] `ipa01`
* [x] `db01`
* [x] `app01`
* [x] `auto01`
* [ ] Architecture documentation
* [ ] Network documentation
* [ ] VM documentation
* [ ] Security documentation

## Phase 2 — Core Services

* [ ] FreeIPA integration
* [ ] PostgreSQL deployment
* [ ] Docker platform
* [ ] Centralized administration
* [ ] Initial application deployment
* [ ] Backup strategy

## Phase 3 — Automation

* [ ] Ansible repository structure
* [ ] Ansible roles
* [ ] System configuration automation
* [ ] OpenTofu structure
* [ ] Infrastructure provisioning
* [ ] Automated validation

## Phase 4 — Security

* [ ] Network segmentation
* [ ] Firewall policies
* [ ] Centralized identity
* [ ] Secrets management
* [ ] Administrative access controls
* [ ] Host hardening
* [ ] Container security
* [ ] Security testing

## Phase 5 — Operations

* [ ] Monitoring
* [ ] Centralized logging
* [ ] Backup automation
* [ ] Disaster recovery procedure
* [ ] Service health checks
* [ ] Documentation of operational procedures

## Phase 6 — CI/CD

* [ ] Forgejo
* [ ] Woodpecker CI
* [ ] Automated configuration validation
* [ ] Infrastructure validation
* [ ] Container image workflows
* [ ] Documentation validation

---

# Project Goals

This project is intended to demonstrate practical knowledge in:

* Linux system administration
* Enterprise infrastructure
* Network architecture
* Identity management
* Firewall administration
* PostgreSQL administration
* Containerization
* Infrastructure as Code
* Configuration management
* Automation
* Secrets management
* CI/CD
* Security engineering
* Operational documentation

The long-term objective is to evolve the environment from a manually configured homelab into an increasingly **automated, documented, secure, and reproducible infrastructure platform**.

---

# Disclaimer

This project is a personal laboratory and educational environment.

It is **not intended to represent a production-ready enterprise deployment**.

Architectural decisions are made to balance:

* Learning value
* Security
* Resource constraints
* Reproducibility
* Operational realism

Production environments require additional considerations such as high availability, redundant infrastructure, formal change management, compliance requirements, enterprise backup systems, disaster recovery, monitoring, and dedicated security controls.

---

# License

License information will be added when the project's licensing strategy is finalized.
