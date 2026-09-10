# Enterprise Reference Architecture

> A FOSS-first enterprise IT reference architecture built on modest hardware, designed as a practical Home Lab and learning environment.

---

## Status Convention

This repository deliberately separates **architecture design** from **actual laboratory implementation**.

| Status | Meaning |
|---|---|
| **Implemented** | Actually installed, configured, and tested in the lab |
| **Planned** | Defined in the architecture but not yet implemented in the lab |
| **Future** | Intentionally deferred for a later phase |
| **Documented** | A design decision or architectural description; it does not imply implementation |

> **Rule:** A component must not be described as **Implemented** unless it has actually been built and validated in the lab. Architectural presence alone means **Planned**.

---

## Table of Contents

- [About the Project](#about-the-project)
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

The **Enterprise Reference Architecture** is a practical, open-source infrastructure project for learning how modern enterprise IT concepts can be designed and implemented using FOSS technologies.

The project separates architectural design from laboratory implementation. Technologies may therefore appear in the architecture before they are actually deployed.

The project focuses on:

* Network segmentation and microsegmentation
* Identity and access management
* Zero Trust and Zero Plaintext principles
* Infrastructure as Code and automation
* Containerized application platforms
* Centralized secrets management
* Security-oriented infrastructure design
* Architecture documentation and reproducibility

The goal is not to claim a production-ready enterprise environment, but to build a small, understandable, reproducible architecture incrementally.

> **Secure by design. Automated where practical. Documented by default.**

---

## Current Implementation Status

The lab is being built incrementally. The current project stage has **not yet reached the Automation & IaC phase**.

### Implemented

Only components that have actually been installed and tested in the laboratory are listed here.

* **Proxmox VE** — virtualization platform
* **OPNsense** — firewall/router VM

### Planned

The following are architectural targets and are **not to be interpreted as currently deployed**:

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

This list will be updated as each component is actually implemented and validated in the lab.

---

## The Story Behind the Project

This project grew from a long-term journey through IT support, systems, infrastructure, and automation.

[Read the story behind the project →](docs/project/story.md)

---

## Architecture Overview

The target architecture is organized around network segmentation, centralized identity, a containerized application platform, dedicated database services, and a future automation layer.

Some of these capabilities are **planned architecture**, not current implementation. The documentation intentionally uses status labels so that the design does not overstate the state of the lab.

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
├── ansible/          # Planned
├── docs/
│   ├── architecture/
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

The project is developed incrementally.

* [x] **Architecture Foundation** — Reference architecture, principles, network model, VM/storage standards, and documentation structure.
* [ ] **Core Infrastructure** — Implement the remaining planned identity and database workloads in the lab.
* [ ] **Application Platform** — Deploy the planned FOSS application services.
* [ ] **Automation & IaC** — Introduce Ansible and OpenTofu. **Not reached yet.**
* [ ] **Security & Zero Trust Implementation** — Validate and implement the planned identity, privileged access, secrets, and segmentation controls.
* [ ] **Observability & Operations** — Add monitoring, logging, alerting, backup, and operational workflows.
* [ ] **CI/CD & Platform Engineering** — Build automated application delivery pipelines.
* [ ] **AI Infrastructure** — Explore GPU-enabled workloads, model serving, AI automation, and self-hosted AI platform patterns.
* [ ] **Documentation & Validation** — Continuously document actual implementation results, lessons learned, and validation evidence.

> Roadmap entries describe project phases. A roadmap item being documented does **not** mean that its components have already been implemented.

---

## Lessons Learned

* **Start with architecture, not individual tools.**
* **Keep implementation status honest.** A design document must not be mistaken for deployment evidence.
* **Security should be designed in from the beginning.**
* **Simple hardware can still support enterprise concepts.**
* **FOSS requires integration work.**
* **Automation is a force multiplier when the lab reaches that phase.**
* **Documentation is part of the architecture.**
* **Reference architectures should evolve based on actual testing.**

---

## Contributing

Contributions, ideas, documentation improvements, and constructive feedback are welcome.

Please clearly distinguish between:

* implemented and tested functionality,
* planned architecture,
* future ideas, and
* documentation-only design decisions.

For larger changes, open an issue first to discuss the proposed approach.

---

## License

This project is licensed under the [MIT License](LICENSE).
