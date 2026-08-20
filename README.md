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

...

## Roadmap

...

## Lessons Learned

...

## Contributing

...

## License
