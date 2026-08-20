# Enterprise Reference Architecture

## Corporate Reference Architecture

> A FOSS-first enterprise IT reference architecture built on modest hardware,
> designed as a practical Home Lab and learning environment.

---

## Table of Contents

- [About the Project](#about-the-project)
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

The **Enterprise Reference Architecture** is a practical, open-source infrastructure project that demonstrates how modern enterprise IT concepts can be designed and implemented using FOSS technologies.
The environment is built as a **self-hosted reference architecture and learning lab**, using modest hardware to model concepts commonly found in larger enterprise environments.
The project focuses on:

* **Network segmentation and microsegmentation**
* **Identity and access management**
* **Zero Trust and Zero Plaintext principles**
* **Infrastructure as Code and automation**
* **Containerized application platforms**
* **Centralized secrets management**
* **Security-oriented infrastructure design**
* **Architecture documentation and reproducibility**

The goal is not to reproduce an entire enterprise environment, but to create a **small, understandable, and reproducible architecture** that demonstrates how these technologies and principles can work together.

> **Secure by design. Automated where practical. Documented by default.**

For detailed architecture decisions, implementation details, diagrams, and operational documentation, see the [`docs/`](docs/) directory.


## The Story Behind the Project

This project grew from a long-term journey through IT support, systems,
infrastructure, and automation.

[Read the story behind the project →](docs/project/story.md)
...

## Architecture Overview

The environment follows a layered enterprise architecture built around network segmentation, centralized identity, containerized applications, dedicated database services, and infrastructure automation.
At the foundation, OPNsense provides network routing, firewalling, and VLAN-based segmentation. Core services are provided by FreeIPA, while application workloads run on Docker and persistent data is handled by PostgreSQL.
Automation and infrastructure management are handled through Ansible and OpenTofu, with security services such as OpenBao, Keycloak, and Teleport supporting secrets management, authentication, and secure access.
The detailed architecture, network design, infrastructure components, and security model are documented separately in the repository.

**Architecture documentation:** [`docs/architecture/`](docs/architecture/)
...

## Key Technologies

* **Virtualization:** Proxmox VE
* **Network Security:** OPNsense, VLAN-based segmentation
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

The architecture follows **FOSS-first**, **Zero Trust**, **Zero Plaintext**, **network segmentation**, and **automation-first** principles.
...

## Project Structure
## Project Structure

The repository is organized to keep the high-level architecture easy to understand while moving implementation details into dedicated documentation.

```text
EnterpriseReferenceArchitecture/
├── README.md
├── LICENSE
│
├── docs/
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── network.md
│   │   ├── security.md
│   │   └── services.md
│   │
│   ├── infrastructure/
│   │   ├── virtualization.md
│   │   ├── storage.md
│   │   └── systems.md
│   │
│   ├── operations/
│   │   ├── monitoring.md
│   │   ├── backup.md
│   │   └── automation.md
│   │
│   └── decisions/
│       └── adr/
│
├── diagrams/
│   ├── architecture/
│   ├── network/
│   └── security/
│
├── automation/
│   ├── ansible/
│   └── opentofu/
│
└── examples/
    └── configurations/
```

The repository follows a documentation-first approach: **README.md provides the project overview, while `docs/` contains detailed architecture and implementation documentation.**
...

## Roadmap
## Roadmap

The project is developed incrementally, with each phase building toward a more complete enterprise-style environment.

* [x] **Foundation** — Define the reference architecture, network segmentation, core principles, and infrastructure standards.
* [x] **Core Infrastructure** — Deploy Proxmox, OPNsense, FreeIPA, PostgreSQL, and the management environment.
* [ ] **Application Platform** — Deploy the core FOSS services on the application platform, including identity, secrets management, networking, source control, and documentation.
* [ ] **Automation & IaC** — Introduce Ansible and OpenTofu for repeatable infrastructure provisioning and configuration management.
* [ ] **Security & Zero Trust** — Implement centralized identity, privileged access, secrets management, secure service-to-service communication, and further network segmentation.
* [ ] **Observability & Operations** — Add monitoring, logging, alerting, backup, and operational workflows.
* [ ] **CI/CD & Platform Engineering** — Build automated application delivery pipelines and establish platform engineering practices.
* [ ] **AI Infrastructure** — Explore GPU-enabled workloads, model serving, AI automation, and infrastructure patterns for self-hosted AI platforms.
* [ ] **Documentation & Validation** — Continuously document architectural decisions, implementation details, lessons learned, and validation results.

> **Note:** The roadmap is intentionally iterative. Components may be added, replaced, or redesigned as the architecture evolves and new technologies are evaluated.
...

## Lessons Learned
## Lessons Learned

Building this architecture has reinforced several practical lessons:

* **Start with architecture, not individual tools.** A clear separation of network, identity, application, data, and management layers makes technology choices easier.
* **Security should be designed in from the beginning.** Network segmentation, Zero Trust principles, and secret management are much harder to retrofit later.
* **Simple hardware can still support enterprise concepts.** Good architecture is more important than expensive infrastructure for learning and experimentation.
* **FOSS requires integration work.** Open-source technologies provide great flexibility, but interoperability, documentation, and operational consistency require deliberate effort.
* **Automation is a force multiplier.** Infrastructure as Code and configuration management reduce repetitive work and make the environment reproducible.
* **Documentation is part of the architecture.** A design that cannot be explained, reproduced, and maintained is not really a reference architecture.
* **Reference architectures should evolve.** The goal is not to build a perfect environment, but to create a practical foundation that can be continuously improved.

> This project is intentionally built as a learning environment. Some design decisions may change as new technologies, requirements, and lessons are introduced.
...

## Contributing

Contributions, ideas, documentation improvements, and constructive feedback are welcome.
This project is primarily a personal **Enterprise IT Reference Architecture** and Home Lab learning environment. The goal is to keep it practical, reproducible, FOSS-first, and useful to others exploring enterprise infrastructure concepts.

### How to Contribute

You can contribute by:

* Improving documentation or architecture diagrams
* Fixing errors or outdated information
* Suggesting better FOSS alternatives or architectural approaches
* Sharing practical implementation experience
* Improving automation, configuration examples, or deployment documentation

For larger changes, please open an issue first to discuss the proposed approach before submitting a pull request.

### Contribution Principles

Please keep contributions aligned with the project's core principles:

* **FOSS-first**
* **Security by design**
* **Zero Trust**
* **Zero Plaintext**
* **Network segmentation**
* **Infrastructure as Code**
* **Reproducibility**
* **Practical enterprise-oriented design**

Contributions should favor clear, maintainable, and understandable solutions over unnecessary complexity.

### Pull Requests

Please keep pull requests focused and explain:

1. What was changed
2. Why the change was needed
3. How it was tested or validated
4. Any architectural or operational implications

By contributing, you agree that your contributions may be incorporated into the project under its existing license.
...

## License
## License

This project is licensed under the [MIT License](LICENSE).
You are free to use, modify, and distribute the project, subject to the terms of the license.
