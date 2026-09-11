# Enterprise Reference Architecture

> A FOSS-first enterprise IT reference architecture built on modest hardware, designed as a practical Home Lab and learning environment.

---

## From Architecture to Operations

The project follows the complete infrastructure lifecycle:

```text
Design → Build → Configure → Validate → Operate → Maintain → Recover → Improve
```

The architecture distinguishes between **Day 1 — Build & Configure** and **Day 2 — Operate & Maintain**.

- **Day 1:** Build, configure, secure, integrate, and validate the infrastructure.
- **Day 2:** Operate, monitor, maintain, secure, recover, and continuously improve it.

> **An infrastructure is not finished when installation is complete.**

---

## Status Convention

This repository deliberately separates **architecture design** from **actual laboratory implementation**.

| Status | Meaning |
|---|---|
| **Implemented** | Actually installed, configured, and tested in the lab |
| **Validated** | Implemented and explicitly verified against defined validation criteria |
| **Planned** | Defined in the architecture but not yet implemented in the lab |
| **Future** | Intentionally deferred for a later phase |
| **Documented** | A design or operational description; it does not imply implementation |

> **Rule:** A component or procedure must not be described as **Implemented** unless it has actually been carried out and validated in the lab.

---

## Table of Contents

- [About the Project](#about-the-project)
- [Day 1 — Build & Configure](#day-1--build--configure)
- [Day 2 — Operate & Maintain](#day-2--operate--maintain)
- [Current Implementation Status](#current-implementation-status)
- [The Story Behind the Project](#the-story-behind-the-project)
- [Architecture Overview](#architecture-overview)
- [Key Technologies](#key-technologies)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [Lessons Learned](#lessons-learned)
- [Contributing](#contributing)
- [License](#license)

---

## About the Project

The **Enterprise Reference Architecture** is a practical, open-source infrastructure project for learning how modern enterprise IT concepts can be designed, implemented, and operated using FOSS technologies.

The project separates architectural design from laboratory implementation. Technologies and operational procedures may therefore appear in the architecture before they are actually deployed or performed in the laboratory.

The project focuses on:

* Network segmentation and microsegmentation
* Identity and access management
* Zero Trust and Zero Plaintext principles
* Infrastructure as Code and automation
* Containerized application platforms
* Centralized secrets management
* Security-oriented infrastructure design
* Day 1 deployment practices
* Day 2 operations and maintenance
* Operational runbooks and repeatable procedures
* Architecture documentation and reproducibility

> **Secure by design. Automated where practical. Operated deliberately. Documented by default.**

---

## Day 1 — Build & Configure

Day 1 covers the transition from architecture design to a working and validated infrastructure.

1. Proxmox installation and base configuration
2. OPNsense installation and network foundation
3. Network segmentation and connectivity
4. FreeIPA identity platform
5. PostgreSQL database platform
6. Docker application platform
7. Identity integration
8. Security baseline
9. Validation and implementation evidence

**Day 1 documentation:** [`docs/day-1/`](docs/day-1/)

---

## Day 2 — Operate & Maintain

Day 2 covers the operational lifecycle after deployment.

1. Daily operations
2. Weekly operational reviews
3. Monthly maintenance
4. Monitoring and observability
5. Patch management
6. Backup and restore testing
7. Disaster recovery
8. Security operations
9. Identity operations
10. Change management
11. Incident management
12. Capacity management
13. Troubleshooting methodology and runbooks
14. Lifecycle management
15. Operational documentation

**Day 2 documentation:** [`docs/day-2/`](docs/day-2/)

Day 2 is currently a **planned operational framework**. Procedures will move toward **Implemented** only after they are actually performed and validated in the lab.

---

## Current Implementation Status

The lab is being built incrementally. The current project stage has **not yet reached the Automation & IaC phase**.

### Implemented

* **Proxmox VE** — virtualization platform
* **OPNsense** — firewall/router VM

### Planned

* FreeIPA on `ipa01`
* PostgreSQL on `db01`
* Docker platform on `app01`
* Keycloak
* OpenBao
* Teleport CE
* NetBox
* Forgejo
* Woodpecker CI
* Wiki.js
* Project Pulp
* Ansible
* OpenTofu
* Day 2 monitoring and operational workflows

This list will be updated as each component or operational capability is actually implemented and validated in the lab.

---

## The Story Behind the Project

This project grew from a long-term journey through IT support, systems, infrastructure, and automation.

[Read the story behind the project →](docs/project/story.md)

---

## Architecture Overview

The target architecture is organized around network segmentation, centralized identity, a containerized application platform, dedicated database services, and a future automation layer.

**Architecture documentation:** [`docs/`](docs/)

---

## Key Technologies

### Implemented in the lab

* **Virtualization:** Proxmox VE
* **Network Security:** OPNsense

### Planned architecture

* **Identity & Access:** FreeIPA, Keycloak, Teleport
* **Secrets Management:** OpenBao
* **Operating Systems:** Fedora, Ubuntu, RHEL, Pardus
* **Containerization:** Docker
* **Automation & IaC:** Ansible, OpenTofu
* **Infrastructure Management:** NetBox
* **CI/CD & Development:** Forgejo, Woodpecker CI
* **Web & Application Delivery:** Nginx
* **Database:** PostgreSQL
* **Documentation & Knowledge:** Wiki.js
* **Package & Artifact Management:** Pulp

The architecture follows **FOSS-first**, **Zero Trust**, **Zero Plaintext**, network segmentation, and automation-first principles.

---

## Project Structure

```text
EnterpriseReferenceArchitecture/
├── README.md
├── LICENSE
├── ansible/                 # Planned
├── docs/
│   ├── architecture/       # Reference architecture
│   ├── day-1/              # Build & Configure
│   ├── day-2/              # Operate & Maintain
│   ├── network/
│   ├── security/
│   ├── vm-design/
│   ├── resource-matrix/
│   └── project/
└── ...
```

Implementation directories should only be populated as their corresponding laboratory phase is actually reached.

---

## Roadmap

* [x] **Architecture Foundation** — Reference architecture, principles, network model, VM/storage standards, and documentation structure.
* [ ] **Day 1 — Core Infrastructure** — Implement the remaining planned identity and database workloads in the lab.
* [ ] **Day 1 — Application Platform** — Deploy the planned FOSS application services.
* [ ] **Day 1 — Automation & IaC** — Introduce Ansible and OpenTofu. **Not reached yet.**
* [ ] **Day 1 — Security & Zero Trust Implementation** — Validate and implement the planned identity, privileged access, secrets, and segmentation controls.
* [ ] **Day 2 — Observability & Operations** — Add monitoring, logging, alerting, backup, and operational workflows.
* [ ] **Day 2 — Reliability & Recovery** — Implement restore testing, disaster recovery procedures, incident runbooks, and operational validation.
* [ ] **Day 2 — Lifecycle Management** — Establish patching, change, capacity, access, and lifecycle management practices.
* [ ] **CI/CD & Platform Engineering** — Build automated application delivery pipelines.
* [ ] **AI Infrastructure** — Explore GPU-enabled workloads, model serving, AI automation, and self-hosted AI platform patterns.
* [ ] **Documentation & Validation** — Continuously document actual implementation results, operational evidence, and lessons learned.

> Roadmap entries describe project phases. A roadmap item being documented does **not** mean that its components have already been implemented.

---

## Lessons Learned

* **Start with architecture, not individual tools.**
* **Keep implementation status honest.**
* **Installation is only Day 1.** Real infrastructure work continues through Day 2 operations.
* **Security should be designed in from the beginning.**
* **Simple hardware can still support enterprise concepts.**
* **FOSS requires integration work.**
* **Automation is a force multiplier when the lab reaches that phase.**
* **Operations need repeatable procedures, not tribal knowledge.**
* **Backup is incomplete until restore has been tested.**
* **Documentation is part of the architecture.**
* **Reference architectures should evolve based on actual testing and operational experience.**

---

## Contributing

Contributions, ideas, documentation improvements, and constructive feedback are welcome.

Please clearly distinguish between:

* implemented and tested functionality,
* planned architecture,
* future ideas, and
* documentation-only or operational design decisions.

For larger changes, open an issue first to discuss the proposed approach.

---

## License

This project is licensed under the [MIT License](LICENSE).
