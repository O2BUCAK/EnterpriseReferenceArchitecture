# Architecture Overview

> A high-level overview of the Enterprise Reference Architecture and how its major infrastructure domains fit together.

## Purpose

This document provides a high-level view of the architecture implemented by the project.
The environment is designed as a small-scale enterprise IT reference architecture that demonstrates how networking, security, identity, applications, databases, and infrastructure automation can be integrated into a cohesive platform.
The architecture is intentionally designed to run on modest hardware while following principles commonly found in larger enterprise environments.

---

## Architectural Model

The environment is organized into several logical infrastructure and network domains:

```text
┌─────────────────────────────────────────────────────────────┐
│                        Internet / WAN                       │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │    OPNsense     │
                     │ Firewall / Edge │
                     └────────┬────────┘
                              │
                    Network Segmentation
                              │
        ┌─────────────┬───────┼────────┬─────────────┐
        │             │       │        │             │
        ▼             ▼       ▼        ▼             │
┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│ Management   │ │   Core   │ │ Database │ │ Applications │
│   VLAN 10    │ │ VLAN 20  │ │ VLAN 30  │ │   VLAN 40    │
│              │ │          │ │          │ │              │
│    auto01    │ │  ipa01   │ │  db01    │ │    app01     │
│ Ansible      │ │ FreeIPA  │ │PostgreSQL│ │    Docker    │
│ OpenTofu     │ │ Identity │ │          │ │   Services   │
└──────────────┘ └──────────┘ └──────────┘ └──────────────┘
                                      ▲              │
                                      │              │
                                      └──────────────┘
                                  Controlled Database Access
```

The architecture separates infrastructure responsibilities into distinct network segments rather than operating all services within a single trusted network.
Each VLAN represents an independent security and trust boundary. Communication between segments is controlled by OPNsense and should be explicitly permitted only when required by the architecture.
The **Database VLAN (VLAN 30)** is an independent network segment. Application workloads in **VLAN 40** may access database services only through explicitly defined firewall and network policies.

---

## Core Components

| Component | Role                                        | Network  |
| --------- | ------------------------------------------- | -------- |
| `fw01`    | Firewall, routing, and network segmentation | OPNsense |
| `auto01`  | Infrastructure automation and IaC           | VLAN 10  |
| `ipa01`   | Identity and core services                  | VLAN 20  |
| `db01`    | PostgreSQL database services                | VLAN 30  |
| `app01`   | Containerized application platform          | VLAN 40  |

Each system has a defined responsibility, allowing the architecture to demonstrate separation of concerns and controlled communication between infrastructure domains.

---

## Network Architecture

The network is divided into dedicated VLANs according to infrastructure roles.

| VLAN    | Purpose       | Primary Workload                         |
| ------- | ------------- | ---------------------------------------- |
| VLAN 10 | Management    | Infrastructure management and automation |
| VLAN 20 | Core Services | Identity and supporting services         |
| VLAN 30 | Database      | PostgreSQL                               |
| VLAN 40 | Applications  | Containerized applications               |

OPNsense acts as the network security boundary and controls traffic between these segments.
The goal is not simply to create VLANs, but to demonstrate **controlled communication between security zones based on workload requirements**.
Detailed network topology, addressing, VLAN configuration, and firewall policies are documented separately.

---

## Application Platform

The application layer is hosted on `app01` using Docker.
The platform is intended to host infrastructure and enterprise-oriented services covering areas such as:

* Reverse proxy and web services
* Identity and authentication
* Secrets management
* Privileged access
* Infrastructure inventory
* Source control and CI/CD
* Documentation and knowledge management
* Network and infrastructure management

Applications are treated as independent workloads rather than being installed directly into the host operating system wherever practical.
The application platform is intentionally separated from the database layer. Persistent application data requiring PostgreSQL is stored on `db01`.

---

## Data Layer

Persistent database services are separated from the application platform.
`db01` provides PostgreSQL database services on the dedicated **Database VLAN (VLAN 30)**.
The database layer is an independent architectural and network domain. Application workloads running on **VLAN 40** communicate with the database layer only through explicitly permitted network flows.

```text
Application Layer
VLAN 40
      │
      │ Explicitly permitted database access
      ▼
Database Layer
VLAN 30
```

This separation demonstrates a common enterprise architecture pattern in which application workloads and database services are isolated from one another.
The database storage design and PostgreSQL-specific configuration are documented separately under the infrastructure documentation.

---

## Identity and Access

Identity is treated as a central architectural capability rather than an application-specific feature.
`ipa01` provides the core identity services through FreeIPA. Additional services can integrate with the identity layer for authentication and authorization where appropriate.
The architecture includes dedicated capabilities for:

* Identity management
* Authentication and authorization
* Secrets management
* Privileged access
* Service-to-service credentials

This supports the project's **Zero Trust** and **Zero Plaintext** principles.

---

## Automation and Infrastructure as Code

Infrastructure management is separated from application workloads.
`auto01` provides the automation layer using:
* **Ansible** for configuration and operational automation
* **OpenTofu** for infrastructure as code
The objective is to make infrastructure changes reproducible, documented, and increasingly automated rather than dependent on manual configuration.
Automation is treated as an architectural capability that spans the infrastructure rather than as a workload belonging to a single application segment.

---

## Security Architecture

Security is implemented as a cross-cutting architectural concern.
The main security principles are:

### Zero Trust

Network location alone does not establish trust.
Access should be explicitly permitted based on identity, role, service requirements, and network policy.

### Zero Plaintext

Sensitive credentials and secrets should not be stored or transmitted in plaintext where secure alternatives are available.
OpenBao is used as the foundation for centralized secrets management.

### Microsegmentation

Infrastructure roles are separated into dedicated network segments.
Communication between segments should be limited to explicitly required flows.

### Least Privilege

Users, services, and infrastructure components should receive only the access required to perform their intended functions.

---

## Architectural Principles

The project follows these principles throughout the design:

1. **FOSS-first** — Prefer free and open-source software where practical.
2. **Security by design** — Security requirements are considered during architecture design rather than added later.
3. **Separation of concerns** — Infrastructure responsibilities are divided by function.
4. **Least privilege** — Access is limited to what is required.
5. **Network segmentation** — Infrastructure domains are isolated through VLANs and firewall policies.
6. **Automation first** — Repetitive infrastructure operations should become automated.
7. **Infrastructure as Code** — Infrastructure configuration should be reproducible and reviewable.
8. **Documentation as code** — Architecture and operational knowledge should live alongside the implementation.
9. **Practicality** — Enterprise concepts should remain achievable on modest hardware.
10. **Reproducibility** — The environment should be understandable and rebuildable by another engineer.

---

## Related Documentation

Detailed implementation documents are maintained separately from this overview.

| Documentation                                                                | Description                                                |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------- |
| [`network.md`](network.md)                                                   | Network topology, VLANs, segmentation, and firewall design |
| [`security.md`](security.md)                                                 | Security architecture, controls, and security principles   |
| [`services.md`](services.md)                                                 | Core infrastructure and application services               |
| [`../infrastructure/virtualization.md`](../infrastructure/virtualization.md) | Virtualization platform and virtual machine architecture   |
| [`../infrastructure/storage.md`](../infrastructure/storage.md)               | Storage architecture and disk layout                       |
| [`../infrastructure/systems.md`](../infrastructure/systems.md)               | Operating systems and system-level configuration           |
| [`../operations/automation.md`](../operations/automation.md)                 | Automation and infrastructure management                   |
| [`../operations/monitoring.md`](../operations/monitoring.md)                 | Monitoring and observability                               |
| [`../operations/backup.md`](../operations/backup.md)                         | Backup and recovery architecture                           |

> This document describes the architecture at a high level. Implementation-specific decisions, configuration details, and operational procedures should be documented in the corresponding domain documentation.
