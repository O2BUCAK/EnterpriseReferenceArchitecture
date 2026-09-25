# Dependency Graph

> **Enterprise Reference Architecture — FOSS Home Lab**

## Status

**Reference / Planned Architecture**

This document describes the intended service and infrastructure dependency model. It does **not** imply that every component is currently deployed.

At the current project stage:

- **Implemented:** Proxmox VE and OPNsense / `fw01`
- **Planned:** `ipa01`, `db01`, `app01`, `auto01` and the application services

The graph should therefore be read as a **target dependency model**, with implementation status shown explicitly on the nodes.

---

## 1. Purpose

The Dependency Graph answers:

- Which infrastructure component depends on which other component?
- Which services are infrastructure dependencies?
- Which applications depend on PostgreSQL?
- Which services depend on identity?
- Which components provide access, secrets, automation or ingress?
- What is the expected failure propagation path?

This is complementary to the [Port Map](../network/port-map.md) and [Firewall Rule Set](../network/firewall-rule-set.md).

> **Dependency is not the same as network reachability.** A firewall rule may permit traffic without the destination becoming a functional dependency.

---

## 2. High-Level Dependency Graph

```mermaid
flowchart TD

    HW["Physical Host<br/>Dell Latitude 5540<br/>Implemented"]
    PVE["Proxmox VE<br/>Virtualization<br/>Implemented"]

    FW["fw01<br/>OPNsense<br/>Firewall / Routing<br/>Implemented"]

    IPA["ipa01<br/>FreeIPA<br/>Identity / DNS / Kerberos<br/>Planned"]
    DB["db01<br/>PostgreSQL + Redis<br/>Database / Cache<br/>Planned"]
    APP["app01<br/>Docker Platform<br/>Planned"]
    AUTO["auto01<br/>Ansible + OpenTofu<br/>Planned"]

    NGINX["Nginx<br/>Ingress / Reverse Proxy<br/>Planned"]
    PORT["Portainer<br/>Docker Management<br/>Planned"]
    TPORT["Teleport CE<br/>Privileged Access<br/>Planned"]
    KC["Keycloak<br/>Application SSO<br/>Planned"]
    BAO["OpenBao<br/>Secrets Management<br/>Planned"]
    NETBOX["NetBox<br/>IPAM / DCIM<br/>Planned"]
    FORGE["Forgejo<br/>Git Platform<br/>Planned"]
    WOOD["Woodpecker CI<br/>CI/CD<br/>Planned"]
    WIKI["Wiki.js<br/>Documentation<br/>Planned"]
    SQUID["Squid<br/>Proxy<br/>Planned"]
    PULP["Project Pulp<br/>Repository / Artifacts<br/>Planned"]

    HW --> PVE

    PVE --> FW
    PVE --> IPA
    PVE --> DB
    PVE --> APP
    PVE --> AUTO

    FW --> IPA
    FW --> DB
    FW --> APP
    FW --> AUTO

    APP --> NGINX
    APP --> PORT
    APP --> TPORT
    APP --> KC
    APP --> BAO
    APP --> NETBOX
    APP --> FORGE
    APP --> WOOD
    APP --> WIKI
    APP --> SQUID
    APP --> PULP

    KC -->|persistent data| DB
    KC -.->|identity integration| IPA

    NETBOX -->|PostgreSQL| DB
    NETBOX -->|Redis| DB
    FORGE -.->|deployment-dependent DB| DB
    WIKI -->|PostgreSQL| DB

    WOOD -.->|source / webhook integration| FORGE
    WOOD -.->|deployment automation| AUTO

    NGINX -.->|reverse proxy / upstream| KC
    NGINX -.->|reverse proxy / upstream| NETBOX
    NGINX -.->|reverse proxy / upstream| FORGE
    NGINX -.->|reverse proxy / upstream| WIKI
    NGINX -.->|reverse proxy / upstream| PULP

    TPORT -.->|conditional identity integration| IPA
    TPORT -.->|privileged access| FW
    TPORT -.->|privileged access| DB
    TPORT -.->|privileged access| APP
    TPORT -.->|privileged access| AUTO

    BAO -.->|identity integration| IPA

    AUTO --> PVE
    AUTO --> FW
    AUTO --> IPA
    AUTO --> DB
    AUTO --> APP

    SQUID --> FW

    classDef impl stroke-width:3px;
    classDef planned stroke-dasharray: 5 5;

    class HW,PVE,FW impl;
    class IPA,DB,APP,AUTO,NGINX,PORT,TPORT,KC,BAO,NETBOX,FORGE,WOOD,WIKI,SQUID,PULP planned;
```

---

## 3. Dependency Layers

The architecture is easier to understand when dependencies are viewed from the bottom upward:

```text
Physical Hardware
        ↓
Proxmox VE
        ↓
Network / Firewall
        ↓
Virtual Machines
        ↓
Core Infrastructure Services
        ↓
Shared Platform Services
        ↓
Application Services
        ↓
Automation / Operations
```

### Layer 1 — Physical / Virtualization

```text
Dell Latitude 5540
        ↓
Proxmox VE
```

All target VMs depend on the physical host and Proxmox VE.

### Layer 2 — Network

```text
Proxmox
   ↓
fw01 / OPNsense
   ↓
VLAN segmentation
   ↓
VM communication
```

The target network separates Management, Identity, Database and Application zones.

### Layer 3 — Core Infrastructure

```text
ipa01
  └── FreeIPA
      ├── Identity
      ├── DNS
      └── Kerberos

db01
  └── PostgreSQL
      └── Application data

app01
  └── Docker platform

auto01
  └── Ansible + OpenTofu
```

---

## 4. Core VM Dependencies

| Component | Depends On | Provides To |
|---|---|---|
| `fw01` | Proxmox | Network routing, segmentation and security enforcement |
| `ipa01` | Proxmox + network + stable DNS/time | Infrastructure identity and authentication |
| `db01` | Proxmox + network + storage | PostgreSQL databases |
| `app01` | Proxmox + network + storage | Containerized application platform |
| `auto01` | Proxmox + network | Infrastructure automation |

---

## 5. Identity Dependency Model

The intended identity chain is:

```text
User
  ↓
Application
  ↓
Keycloak
  ↓
FreeIPA
```

FreeIPA is the planned primary infrastructure identity source.

### Keycloak

Keycloak is intended to provide application-oriented SSO.

```text
Keycloak
   ↓
FreeIPA / LDAP
```

Keycloak additionally depends on PostgreSQL for persistent application data:

```text
Keycloak
   ↓
PostgreSQL
```

Therefore:

```text
Keycloak
   ├──→ FreeIPA
   └──→ PostgreSQL
```

### Teleport CE

Teleport is intended to provide controlled administrative access.

```text
Administrator
      ↓
Teleport
      ↓
Infrastructure / Hosts
```

The target identity model allows Teleport to integrate with the planned identity architecture.

---

## 6. Database and Cache Dependency Model

`db01` is the shared stateful platform for PostgreSQL and Redis.

```mermaid
flowchart LR
    DB["db01<br/>PostgreSQL"]
    REDIS["db01<br/>Redis"]

    KC["Keycloak"]
    NB["NetBox"]
    FG["Forgejo"]
    WK["Wiki.js"]

    KC -->|PostgreSQL| DB
    NB -->|PostgreSQL| DB
    NB -->|Redis| REDIS
    FG -.->|deployment-dependent| DB
    WK -->|PostgreSQL| DB
```

### PostgreSQL

| Application | PostgreSQL | Relationship |
|---|---|---|
| Keycloak | Yes | Runtime / persistent data |
| NetBox | Yes | Runtime / persistent data |
| Wiki.js | Yes | Runtime / persistent data in selected deployment |
| Forgejo | Conditional | Deployment-dependent |

### Redis

Redis is deployed centrally on `db01` for applications that explicitly require it.

| Application | Redis | Relationship |
|---|---|---|
| NetBox | Yes | Required in the selected architecture |
| Keycloak | No | Uses Keycloak's supported cache mechanism |
| OpenBao | No | Integrated Raft storage |
| Teleport CE | No | No default Redis dependency |
| Squid | No | External cache/database not required |

> **Design rule:** A central Redis service does not become a dependency of every application. Only an explicit application requirement creates a runtime dependency.

### OpenBao Storage

OpenBao does **not** depend on PostgreSQL or Redis in the selected architecture.

```text
OpenBao
   ↓
Integrated Raft Storage
```

This keeps OpenBao independently operable from the shared database/cache layer.

### Teleport Storage

Teleport's storage model remains deployment-specific. The single-node reference deployment should use its supported embedded storage model; an HA design must be validated against the selected Teleport version and storage configuration.

---

## 7. Application Ingress Dependencies

Nginx is the planned common application ingress point.

```text
Client
  ↓
OPNsense / Firewall
  ↓
Nginx
  ↓
Application
```

Target application routing:

```text
Nginx
 ├──→ Keycloak
 ├──→ NetBox
 ├──→ Forgejo
 ├──→ Wiki.js
 └──→ Other approved HTTPS applications
```

The purpose is to avoid exposing every application directly.

---

## 8. Secrets Dependency

OpenBao is the planned central secrets-management layer.

```text
Application / Service
        ↓
     OpenBao
        ↓
Credentials / Tokens / Secrets
```

Planned consumers include application services, automation, database credentials, service credentials, and certificates or sensitive material where appropriate.

OpenBao itself is hosted on `app01` in the current reference design.

> OpenBao is a **security dependency**, not merely another application container.

---

## 9. Automation Dependency

`auto01` is the future automation control plane.

```mermaid
flowchart LR
    AUTO["auto01<br/>Ansible + OpenTofu"]

    PVE["Proxmox VE"]
    FW["fw01"]
    IPA["ipa01"]
    DB["db01"]
    APP["app01"]

    AUTO -. "future automation" .-> PVE
    AUTO -. "future automation" .-> FW
    AUTO -. "future automation" .-> IPA
    AUTO -. "future automation" .-> DB
    AUTO -. "future automation" .-> APP
```

Planned responsibilities include:

```text
Provision
Configure
Harden
Deploy
Validate
Maintain
```

Automation is deliberately shown as a **future dependency/controller relationship**, because the repository states that the Automation & IaC phase has not yet been reached.

---

## 10. CI/CD Dependency

The planned development flow is:

```text
Developer
   ↓
Forgejo
   ↓
Woodpecker CI
   ↓
Build / Test
   ↓
Deployment
```

Therefore:

```text
Woodpecker
   ├──→ Forgejo
   └──→ auto01 / deployment targets
```

CI runners should receive only the permissions required for their jobs.

They should not obtain unrestricted access to Management, Identity or Database networks.

---

## 11. Documentation Dependency

Wiki.js is the planned operational documentation platform.

```text
Wiki.js
   ↓
PostgreSQL
```

However, critical documentation should not depend exclusively on Wiki.js:

```text
Git Repository
     ↓
Critical Architecture / Runbooks
     ↓
Wiki.js
```

The repository remains the recoverable source for the project's core documentation.

---

## 12. Infrastructure Source-of-Truth Dependency

NetBox is planned as the infrastructure and network source of truth.

```text
NetBox
 ├── IPAM
 ├── DCIM
 ├── Device / VM inventory
 └── Network documentation
```

Future relationship:

```text
Network / Infrastructure
        ↓
      NetBox
        ↓
Automation / Documentation
```

NetBox should not create a parallel unmanaged inventory model.

---

## 13. Proxy / Egress Dependency

Squid is planned as a controlled HTTP/HTTPS proxy.

```text
Application / Clients
        ↓
      Squid
        ↓
     OPNsense
        ↓
       WAN
```

Squid must not become a bypass path around the OPNsense security model.

---

## 14. Failure Propagation

A dependency graph is most useful when considering failures.

### Proxmox failure

```text
Proxmox
   ↓
fw01 + ipa01 + db01 + app01 + auto01
   ↓
All dependent services
```

### `fw01` failure

```text
fw01
   ↓
Inter-VLAN communication
   ↓
Cross-zone service dependencies
```

### FreeIPA failure

Potential impact:

```text
FreeIPA
   ↓
Authentication / Identity-dependent services
   ├── Keycloak integration
   ├── Linux host identity
   └── Administrative identity flows
```

Local break-glass access should remain available for recovery.

### PostgreSQL failure

Potential impact:

```text
PostgreSQL
   ├── Keycloak
   ├── NetBox
   ├── Forgejo
   └── Wiki.js
```

Affected applications may remain running but lose persistent application functionality depending on their architecture.

### `app01` failure

Potential impact:

```text
app01
   ├── Nginx
   ├── Keycloak
   ├── OpenBao
   ├── Teleport
   ├── NetBox
   ├── Forgejo
   ├── Woodpecker
   ├── Wiki.js
   ├── Squid
   └── Project Pulp
```

Because multiple services are intentionally consolidated on `app01`, it is a significant failure domain in the current modest-hardware design.

---

## 15. Application Dependency Matrix

This matrix separates **runtime dependencies** from integrations, ingress relationships and operational access.

| Source | Dependency | Type | Required | Status |
|---|---|---|---|---|
| Keycloak | PostgreSQL | Runtime / persistent data | Yes | Planned |
| Keycloak | FreeIPA | Identity integration | Conditional | Planned |
| Keycloak | Redis | Runtime dependency | No | Not selected |
| NetBox | PostgreSQL | Runtime / persistent data | Yes | Planned |
| NetBox | Redis | Runtime / cache / background tasks | Yes | Planned |
| Wiki.js | PostgreSQL | Runtime / persistent data | Yes | Planned |
| Forgejo | PostgreSQL | Deployment-dependent | Conditional | Planned |
| Woodpecker CI | Forgejo | Source / webhook integration | Conditional | Planned |
| Woodpecker CI | auto01 | Deployment automation | Conditional | Planned |
| Nginx | Backend applications | Reverse-proxy integration | Conditional | Planned |
| Teleport CE | FreeIPA | Identity integration | Conditional | Planned |
| Teleport CE | External DB | Storage dependency | No | Not selected |
| OpenBao | Integrated Raft | Internal storage | Yes | Planned |
| OpenBao | PostgreSQL | External storage | No | Not selected |
| OpenBao | Redis | External cache/storage | No | Not selected |
| Squid | External DB | Logging/reporting | No | Not selected |

### Application dependency rules

1. Runtime dependency means the application requires it for normal operation.
2. Integration dependency does not necessarily prevent the application from starting.
3. Reverse-proxy relationships are not application runtime dependencies.
4. Privileged-access relationships are operational access paths, not storage dependencies.
5. Optional HA/storage components must not be represented as mandatory dependencies.
6. Shared PostgreSQL and Redis are dependencies only for applications with explicit requirements.

---

## 16. Direct vs Transitive Dependencies

### Direct dependency

A service requires the dependency to perform its normal operation.

Example:

```text
Keycloak → PostgreSQL
```

### Transitive dependency

The service indirectly depends on another component through an intermediate service.

Example:

```text
Application
   ↓
Keycloak
   ↓
FreeIPA
```

The application may therefore have a transitive dependency on FreeIPA when Keycloak authentication is required.

This distinction is important during troubleshooting.

---

## 17. Dependency Classification

| Dependency Type | Examples |
|---|---|
| Compute | Proxmox VE |
| Network | OPNsense / VLANs |
| Identity | FreeIPA |
| Database | PostgreSQL |
| Platform | Docker |
| Ingress | Nginx |
| Secrets | OpenBao |
| Privileged Access | Teleport |
| Inventory | NetBox |
| Source Control | Forgejo |
| CI/CD | Woodpecker |
| Documentation | Wiki.js |
| Proxy / Egress | Squid |
| Repository / Artifacts | Project Pulp |
| Automation | Ansible / OpenTofu |

---

## 18. Dependency Design Principles

1. Keep dependencies explicit.
2. Avoid unnecessary cross-zone communication.
3. Prefer dedicated service identities.
4. Keep database access application-specific.
5. Centralize ingress where practical.
6. Do not bypass OPNsense with alternate egress paths.
7. Treat secrets management as a security dependency.
8. Keep break-glass access independent of centralized identity.
9. Document both direct and transitive dependencies.
10. Revalidate dependencies whenever an application or version changes.
11. Do not treat a planned dependency as implemented.
12. Record implementation evidence separately from the reference graph.

---

## 19. Troubleshooting Order

When a service fails, follow the dependency direction from the bottom upward:

```text
Physical Host
     ↓
Proxmox
     ↓
Network / OPNsense
     ↓
VM
     ↓
Operating System
     ↓
Identity / DNS / NTP
     ↓
Database
     ↓
Container Platform
     ↓
Application Dependency
     ↓
Application
```

This prevents application-level troubleshooting from masking an infrastructure dependency failure.

---

## 20. Implementation Evidence

When a dependency becomes implemented, record:

```text
Source service:
Dependency:
Dependency type:
Host:
Protocol:
Port:
Authentication:
Required for:
Failure behavior:
Validation:
Status:
Known deviations:
```

Do not document a dependency as **Implemented** merely because it exists in the target architecture.

---

## Related Documentation

- [Architecture Overview](overview.md)
- [Identity Architecture](identity.md)
- [Storage Architecture](storage.md)
- [VM Design](../vm-design/vm-design.md)
- [Network Architecture](../network/network.md)
- [Port Map](../network/port-map.md)
- [Firewall Rule Set](../network/firewall-rule-set.md)
- [Resource Sheet](../resource-matrix/resource-sheet.md)
- [VM Resource Matrix](../resource-matrix/vm-resource-matrix.md)
- [Security Architecture](../security/security.md)

---

## Summary

The target dependency model is:

```text
Physical Host
      ↓
Proxmox VE
      ↓
OPNsense / Network
      ↓
VMs
      ↓
+-------------------+-------------------+
|                   |                   |
FreeIPA          PostgreSQL          Docker
|                   |                   |
+---------+---------+---------+---------+
          |                   |
      Identity            Applications
          |                   |
      Keycloak             Nginx
      Teleport             OpenBao
                          NetBox
                          Forgejo
                          Woodpecker
                          Wiki.js
                          Squid
                          Pulp
```

> **The graph represents the target architecture. Implementation status must always be confirmed using laboratory evidence.**
