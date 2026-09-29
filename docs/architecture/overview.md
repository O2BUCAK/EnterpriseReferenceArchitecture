# Architecture Overview

> High-level reference architecture for the Enterprise Reference Architecture (FOSS Home Lab).

## Purpose

This document describes the **target architecture** of the project. It is a design document and must not be interpreted as proof that every component shown has been deployed in the laboratory.

The lab is implemented incrementally. Components not yet built are marked **Planned**.

## Status Convention

| Status | Meaning |
|---|---|
| **Implemented** | Installed, configured, and tested in the lab |
| **Planned** | Defined by the architecture but not yet implemented |
| **Future** | Deferred to a later phase |
| **Documented** | Design decision only; no implementation claim |

> A component is **Implemented** only after actual laboratory validation.

## Architectural Model

The target architecture is organized into separate infrastructure and network domains:

```text
                         Internet / WAN
                              |
                              v
                       +--------------+
                       |    fw01      |
                       |   OPNsense   |
                       +------+-------+
                              |
                     Planned segmentation
                              |
        +-------------+-------+--------+-------------+
        |             |                |             |
        v             v                v             v
   VLAN 10        VLAN 20          VLAN 30       VLAN 40
   Management     Identity         Database      Application
        |             |                |             |
      auto01        ipa01            db01          app01
     Planned       Planned          Planned        Planned
        |             |                |             |
     Ansible       FreeIPA       PostgreSQL      Docker
     OpenTofu                                      Planned
```

The diagram represents the **target design**. At the current project stage, only components explicitly listed as Implemented in the repository status should be considered deployed.

## System Design Methodology

The architecture uses three complementary practices inspired by system-design methodology:

1. **Architecture decisions and trade-offs** — material choices are documented with constraints, alternatives, consequences, and validation criteria.
2. **Cache architecture** — caching is treated as an explicit workload decision rather than an automatic platform dependency.
3. **Bottleneck analysis** — performance investigations are evidence-driven and correlated with actual workload impact.

Queue-based asynchronous processing is **not currently selected as a mandatory platform capability**. See the [Asynchronous Architecture & Queue Decision Guide](async-architecture.md) for the criteria that would justify introducing it.

## Availability and Failure Domain Scope

The current reference architecture intentionally does **not** target hardware-level high availability or multi-host failure-domain design.

The single-host constraint is documented in [ADR 0008](../adr/0008-single-app-host.md).

This does not prevent documenting service dependencies and failure propagation; it means the architecture does not introduce additional hardware solely to provide host-level redundancy.

## Core Components

| Component | Role | Status |
|---|---|---|
| `fw01` | Firewall, routing and segmentation | **Implemented** |
| `ipa01` | FreeIPA identity services | **Planned** |
| `db01` | PostgreSQL and Redis services | **Planned** |
| `app01` | Docker application platform | **Planned** |
| `auto01` | Ansible and OpenTofu automation | **Planned** |

The VM names and roles are architectural definitions. Their presence in this table does not imply that the VM has already been provisioned.

## Network Architecture

The target network contains four logical segments:

| VLAN | Purpose | Primary Workload | Status |
|---|---|---|---|
| VLAN 10 | Management | Infrastructure management / automation | Planned architecture |
| VLAN 20 | Core / Identity | FreeIPA | Planned |
| VLAN 30 | Database | PostgreSQL / Redis | Planned |
| VLAN 40 | Applications | Docker workloads | Planned |

Inter-segment communication is intended to be controlled by OPNsense using explicit, least-privilege firewall policies.

Detailed network design is documented in [`../network/network.md`](../network/network.md).

## Application Platform

`app01` is the **planned** application platform. The design targets Docker-based services such as Nginx, Portainer, Teleport CE, Keycloak, OpenBao, NetBox, Squid, Forgejo, Woodpecker CI, Wiki.js, and Project Pulp.

These services are **Planned** unless separately documented as Implemented after laboratory validation.

## Data Layer

`db01` is the **planned** PostgreSQL and Redis data/cache layer. Application workloads are designed to access database and cache services through explicitly permitted network flows.

The database and cache architecture are documented independently from the application platform.

## Identity and Access

`ipa01` and the surrounding identity architecture are **Planned** at the current project stage.

The target design uses:

* FreeIPA for infrastructure identity
* Keycloak for application-oriented SSO
* OpenBao for secrets management
* Teleport CE for privileged access

These are architectural targets and are not implementation claims.

## Automation and Infrastructure as Code

`auto01`, Ansible, and OpenTofu are **Planned**.

The lab has not yet reached the Automation & IaC implementation phase. The architecture documents the intended future design so that automation can be introduced consistently when that phase is reached.

## Security Architecture

Security is a cross-cutting **design principle** throughout the architecture.

The main principles are:

* **Zero Trust**
* **Zero Plaintext**
* **Microsegmentation**
* **Least Privilege**
* **Defense in Depth**
* **Secure by Default**

The principles are documented independently from implementation status.

## Architectural Principles

1. **FOSS-first**
2. **Security by design**
3. **Separation of concerns**
4. **Least privilege**
5. **Network segmentation**
6. **Automation first**
7. **Infrastructure as Code**
8. **Documentation as code**
9. **Practicality**
10. **Reproducibility**
11. **Evidence-driven architecture decisions**
12. **Explicit trade-offs**
13. **Measured performance and capacity**

These are design principles; their presence in this document does not mean every related capability has already been implemented.

## Related Documentation

| Documentation | Description |
|---|---|
| [Architecture Decision & Trade-off Methodology](architecture-decisions.md) | Decision and trade-off method |
| [Cache Architecture](cache.md) | Cache design and Redis usage |
| [Bottleneck Analysis](bottleneck-analysis.md) | Performance and constraint analysis |
| [Asynchronous Architecture & Queue Decision Guide](async-architecture.md) | Criteria for future queue adoption |
| [`../network/network.md`](../network/network.md) | Network architecture and segmentation |
| [`../security/security.md`](../security/security.md) | Security architecture and controls |
| [`../vm-design/vm-design.md`](../vm-design/vm-design.md) | VM design standards |
| [`../resource-matrix/vm-resource-matrix.md`](../resource-matrix/vm-resource-matrix.md) | Resource planning |
| [`../project/story.md`](../project/story.md) | Project background |

> This document describes the **reference design**. Actual implementation status must be taken from the explicit status sections and implementation evidence in the repository.
