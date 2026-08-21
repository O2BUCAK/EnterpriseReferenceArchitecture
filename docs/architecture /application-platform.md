# Application Platform Architecture

> A practical application platform design for hosting, securing, and operating enterprise services within the Enterprise Reference Architecture.

## Purpose

This document defines the application platform used by the Enterprise Reference Architecture.
The platform provides a centralized environment for hosting infrastructure and application services while maintaining clear separation between application workloads, databases, identity services, security controls, and automation.
The design follows a **FOSS-first**, **security-by-design**, and **least-privilege** approach. Services are selected to demonstrate enterprise patterns without requiring enterprise-scale hardware.
The application platform is primarily hosted on `app01`, while persistent application data is stored according to the storage architecture and database workloads are separated onto `db01`.

---

## Platform Principles

The application platform follows these principles:

* **FOSS-first** — Prefer mature open-source technologies where practical.
* **Least privilege** — Services receive only the access they require.
* **Zero Trust** — Network location alone does not imply trust.
* **Zero Plaintext** — Secrets and credentials should not be stored directly in application configuration.
* **Service isolation** — Application services are separated using container networks and access policies.
* **Database separation** — Application containers do not host the primary database workloads.
* **Centralized identity** — Authentication and authorization should integrate with the platform identity layer where supported.
* **Infrastructure as Code** — Platform configuration should be reproducible through automation.
* **Observability** — Services should provide sufficient logging and operational visibility.
* **Reproducibility** — Applications should be deployable consistently across environments.
* **Modest hardware compatibility** — The architecture should remain practical on a small lab system.

---

## Platform Overview

The application platform is centered around `app01`.

```text
                         ┌───────────────────────────┐
                         │          Users            │
                         └─────────────┬─────────────┘
                                       │
                                       ▼
                         ┌───────────────────────────┐
                         │         fw01              │
                         │        OPNsense           │
                         └─────────────┬─────────────┘
                                       │
                                       ▼
                         ┌───────────────────────────┐
                         │          app01             │
                         │       Ubuntu Server       │
                         │                           │
                         │       Docker Engine       │
                         ├───────────────────────────┤
                         │ Nginx                     │
                         │ Keycloak                  │
                         │ OpenBao                    │
                         │ Teleport CE               │
                         │ NetBox                    │
                         │ Squid Gateway             │
                         │ Forgejo                   │
                         │ Woodpecker CI             │
                         │ Wiki.js                   │
                         │ Portainer                  │
                         │ Project Pulp               │
                         └─────────────┬─────────────┘
                                       │
                         ┌─────────────┴─────────────┐
                         │                           │
                         ▼                           ▼
                ┌──────────────────┐       ┌──────────────────┐
                │      ipa01       │       │       db01       │
                │     FreeIPA      │       │     PostgreSQL   │
                └──────────────────┘       └──────────────────┘
```

The diagram represents logical relationships rather than unrestricted network connectivity.
Firewall rules, service-specific policies, and network segmentation determine which communication paths are actually permitted.

---

## Application Host: app01

`app01` is an Ubuntu Server virtual machine responsible for hosting containerized application services.
Docker provides the application runtime, while individual services are isolated through separate containers and logical Docker networks.

### Primary Responsibilities

* Application hosting
* Reverse proxy
* Identity-aware application integration
* Secrets management
* Administrative access
* Network gateway services
* Source code management
* CI/CD
* Documentation
* Infrastructure inventory
* Container management
* Package and artifact management

### Hosted Services

| Service       | Primary Role                               |
| ------------- | ------------------------------------------ |
| Nginx         | Reverse proxy and HTTP entry point         |
| Portainer     | Container administration                   |
| Teleport CE   | Secure infrastructure access               |
| Keycloak      | Application identity and SSO               |
| OpenBao       | Secrets management                         |
| NetBox        | Network and infrastructure source of truth |
| Squid         | Controlled proxy/gateway services          |
| Forgejo       | Git repository hosting                     |
| Woodpecker CI | CI/CD automation                           |
| Wiki.js       | Technical documentation                    |
| Project Pulp  | Repository and content management          |

These services are logically separated even though they share the same VM.

---

## Container Architecture

Docker is used as the application runtime on `app01`.
Each application is deployed as an independent container or service stack where appropriate.

A simplified model is:

```text
app01
│
├── Docker Engine
│
├── Management Network
│   ├── Portainer
│   └── Teleport
│
├── Identity / Security Network
│   ├── Keycloak
│   └── OpenBao
│
├── Application Network
│   ├── Nginx
│   ├── Wiki.js
│   ├── NetBox
│   └── Forgejo
│
├── CI/CD Network
│   └── Woodpecker CI
│
└── Infrastructure / Gateway Network
    ├── Squid
    └── Project Pulp
```

These networks are **logical Docker network boundaries**. They should not be confused with physical or routed VLANs.
Network access between containers should be explicitly defined according to service requirements.

---

## Reverse Proxy

Nginx provides the primary HTTP/HTTPS entry point for applications hosted on `app01`.
Instead of exposing every application directly, services should generally be accessed through the reverse proxy.

```text
Client
   │
   ▼
HTTPS
   │
   ▼
Nginx
   │
   ├──► Keycloak
   ├──► NetBox
   ├──► Forgejo
   ├──► Wiki.js
   ├──► Portainer
   └──► Other approved services
```

This provides a centralized point for:

* TLS termination
* Host-based routing
* HTTP security controls
* Application exposure
* Access logging
* Consistent external endpoints

Applications that require direct network exposure should be explicitly justified.

---

## Identity Integration

Application authentication should be centralized where supported.
Keycloak provides the application-facing identity and SSO layer, while FreeIPA remains the infrastructure identity service.

The intended relationship is:

```text
                     ┌──────────────┐
                     │    FreeIPA   │
                     │   Identity   │
                     └──────┬───────┘
                            │
                            ▼
                     ┌──────────────┐
                     │   Keycloak   │
                     │ SSO / OIDC   │
                     └──────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
           NetBox         Forgejo       Wiki.js
```

The exact integration mechanism depends on application capabilities and should be documented separately during implementation.
Applications should avoid maintaining independent user databases when centralized identity integration is practical.

---

## Secrets Management

OpenBao is the designated secrets management platform.
Sensitive information should not be committed to Git repositories or stored in plaintext configuration files.

Examples include:

* Database passwords
* API tokens
* Application credentials
* TLS private keys
* CI/CD secrets
* Service credentials

The intended model is:

```text
Application
     │
     │ authenticated request
     ▼
  OpenBao
     │
     ▼
 Secret / Credential
```

Where direct OpenBao integration is not available, secrets should be injected through an appropriate secure mechanism rather than committed to source control.

---

## Database Integration

Application services use `db01` for persistent PostgreSQL workloads where PostgreSQL is required.
The application platform therefore separates:

**Application tier**

```text
app01
Docker containers
```

from:

**Database tier**

```text
db01
PostgreSQL
```

This separation provides clearer boundaries for:

* Database administration
* Backup
* Storage management
* Access control
* Resource allocation
* Troubleshooting
* Future scalability

Only applications that require database access should be permitted to communicate with PostgreSQL.

---

## Source Control and CI/CD

Forgejo provides Git repository hosting.
Woodpecker CI provides automated build and deployment workflows.

The intended workflow is:

```text
Developer
   │
   ▼
Forgejo
   │
   │ Git push
   ▼
Woodpecker CI
   │
   ├── Test
   ├── Build
   ├── Validate
   └── Deploy
          │
          ▼
      Application
```

CI/CD credentials should be managed through OpenBao or another approved secret-management mechanism.
Build and deployment pipelines should avoid embedding credentials directly in repository files.

---

## Infrastructure Source of Truth

NetBox provides a centralized source of truth for infrastructure information.

It is intended to document:

* IP addresses
* Networks
* VLANs
* Virtual machines
* Devices
* Interfaces
* Services
* Relationships
* Infrastructure metadata

The goal is to prevent infrastructure information from becoming dependent on manually maintained spreadsheets or undocumented configuration.
Where practical, automation should consume information from NetBox rather than duplicating infrastructure data.

---

## Administrative Access

Teleport CE provides controlled administrative access to infrastructure systems.

Administrative access should follow the principle:

```text
Administrator
      │
      ▼
   Teleport
      │
      ├──► Linux systems
      ├──► Application services
      └──► Other approved infrastructure
```

Direct administrative exposure should be minimized.
Teleport is therefore part of the security boundary rather than simply another application hosted on `app01`.

---

## Proxy and Gateway Services

Squid provides controlled proxy functionality where required.

Potential use cases include:

* Controlled outbound HTTP/HTTPS access
* Application-specific proxy requirements
* Testing network restrictions
* Demonstrating enterprise proxy architecture

Proxy access should be explicitly controlled through firewall and service policies.

---

## Documentation Platform

Wiki.js provides centralized technical documentation for the environment.

Documentation should cover:

* Operational procedures
* Service configuration
* Troubleshooting
* Architecture decisions
* Runbooks
* Maintenance procedures

The Git repository remains the authoritative location for architecture documentation and infrastructure-as-code artifacts.
Wiki.js complements the repository with operational and collaborative documentation.

---

## Artifact and Package Management

Project Pulp provides repository and content management capabilities.
It can be used to demonstrate enterprise-style management of software packages, repositories, and content artifacts.

This separates the concept of:

```text
Source Code
     │
     ▼
Forgejo
```

from:

```text
Packages / Artifacts / Content
     │
     ▼
Project Pulp
```

This distinction becomes important as the platform evolves toward automated software delivery.

---

## Platform Security Boundaries

Security is enforced at multiple layers.

### Network Layer

Implemented through:

* OPNsense firewall policies
* Network segmentation
* Restricted inter-network communication
* Controlled ingress and egress

### Host Layer

Implemented through:

* Linux permissions
* Service isolation
* Firewall configuration
* Minimal installed packages
* Regular updates

### Container Layer

Implemented through:

* Separate Docker networks
* Minimal container privileges
* Restricted exposed ports
* Non-root containers where supported
* Resource limits where appropriate

### Application Layer

Implemented through:

* Centralized authentication
* Role-based access control
* TLS
* Application-specific authorization

### Secret Layer

Implemented through:

* OpenBao
* Short-lived credentials where supported
* Avoidance of plaintext secrets
* Controlled secret access

---

## Service Exposure Model

Services should follow a default-deny exposure model.

```text
                 Internet / User Network
                          │
                          ▼
                       fw01
                          │
                          ▼
                        Nginx
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          Service A    Service B    Service C
```

Applications should not expose arbitrary container ports directly to external networks.
Each exposed service must have a documented purpose and an explicitly permitted access path.

---

## Persistence

Containers should be treated as replaceable application instances.
Persistent data must be stored outside the container's writable layer.

Examples include:

* Application databases
* Configuration requiring persistence
* Git repositories
* Documentation
* OpenBao data
* Application uploads
* Package repositories

Persistent storage must follow the storage architecture defined for the platform.
Application-specific storage requirements should be documented before deployment.

---

## Backup Considerations

The application platform contains several stateful services and therefore requires service-aware backup planning.

Priority data includes:

1. OpenBao data
2. PostgreSQL databases
3. Forgejo repositories and data
4. NetBox data
5. Wiki.js content
6. Application configuration
7. Project Pulp repositories and metadata

Backups should not rely exclusively on VM snapshots.
Application-consistent backup procedures should be defined for stateful services.

---

## Resource Management

Because the architecture runs on modest hardware, resource allocation must be deliberate.

The platform should prioritize:

* Identity services
* Database services
* Security services
* Core application services

Non-critical workloads should not consume resources required by core infrastructure.
Docker containers should use resource limits where necessary to prevent a single workload from exhausting the host.

---

## Operational Model

The application platform follows a layered operational model:

```text
Infrastructure
      │
      ▼
Proxmox
      │
      ▼
Virtual Machines
      │
      ├── fw01
      ├── ipa01
      ├── db01
      ├── app01
      └── auto01
              │
              ▼
        Docker Platform
              │
              ▼
        Application Services
```

Each layer has a defined responsibility.
Changes should be made at the lowest appropriate layer rather than bypassing the architecture.

---

## Automation

`auto01` provides the primary automation platform using Ansible and OpenTofu.

The intended relationship is:

```text
OpenTofu
   │
   └── Infrastructure provisioning

Ansible
   │
   └── OS and service configuration

Forgejo
   │
   └── Source control

Woodpecker CI
   │
   └── Automated validation and execution
```

Application deployment should progressively move from manual configuration toward reproducible automation.

---

## Design Goals

The application platform is designed to demonstrate how a small infrastructure environment can implement enterprise-oriented patterns without requiring enterprise-scale infrastructure.

The primary goals are:

* Centralized application hosting
* Strong service isolation
* Centralized identity
* Secure secret management
* Dedicated database infrastructure
* Controlled administrative access
* Git-based configuration and application management
* Automated CI/CD
* Infrastructure source of truth
* Reproducible deployments
* Clear security boundaries

The platform intentionally favors **architectural clarity and operational discipline over maximum application density**.

---

## Related Architecture Documents

* [Architecture Overview](./overview.md)
* [Network Architecture](./network.md)
* [Security Architecture](./security.md)
* [Identity Architecture](./identity.md)
* [Storage Architecture](./storage.md)
* [VM Design](./vm-design.md)
* [Automation Architecture](./automation.md)

---

## Future Improvements

Potential future enhancements include:

* Centralized observability and metrics
* Distributed logging
* Automated certificate management
* Container image scanning
* Software supply-chain security
* Automated backup verification
* GitOps-oriented application deployment
* Policy-as-code
* Automated vulnerability management
* Service-level health checks
* Disaster recovery testing

These capabilities can be introduced incrementally without changing the fundamental application platform design.
