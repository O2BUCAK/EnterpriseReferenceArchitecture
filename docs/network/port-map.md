# Port Map

> Port and service reference for the Enterprise Reference Architecture.

## Status

**Documented / Planned architecture.**

This document defines the expected service ports for the target architecture. It does not mean that every listed service is currently deployed.

The repository currently identifies **Proxmox VE** and **OPNsense** as implemented. FreeIPA, PostgreSQL, Docker and the application services remain planned until they are installed and validated in the laboratory.

---

## 1. Purpose

The Port Map provides a single reference for:

- Service listening ports
- Protocols
- Source and destination relationships
- Management access
- Inter-VLAN communication
- Firewall rule design
- Container published ports
- Future application exposure

The Port Map is a **service reference**, not a direct firewall configuration.

> **Rule:** A port should only be allowed when there is a documented source, destination and technical requirement for the communication.

---

## 2. Network Zones

The target architecture uses four primary network segments:

| VLAN | Name | Network | Primary Workloads |
|---:|---|---|---|
| 10 | Management | `10.10.10.0/24` | Proxmox, OPNsense, automation |
| 20 | Identity | `10.10.20.0/24` | FreeIPA |
| 30 | Database | `10.10.30.0/24` | PostgreSQL |
| 40 | Application | `10.10.40.0/24` | Docker and application services |

These networks are part of the target architecture and remain planned until separately implemented and validated.

---

## 3. Infrastructure Management Ports

| Service | Host | Port | Protocol | Purpose | Status |
|---|---|---:|---|---|---|
| Proxmox VE Web UI | Proxmox node | 8006 | TCP | HTTPS management | Implemented |
| SSH | Proxmox / Linux hosts | 22 | TCP | Administrative access | Role dependent |
| OPNsense Web UI | `fw01` | 443 | TCP | HTTPS management | Implemented |
| DNS | OPNsense / FreeIPA | 53 | TCP/UDP | Name resolution | Planned |
| NTP | OPNsense / infrastructure | 123 | UDP | Time synchronization | Required |
| ICMP | Infrastructure | — | ICMP | Connectivity / diagnostics | Controlled |

Management interfaces should only be reachable from the intended management path.

---

## 4. FreeIPA — `ipa01`

FreeIPA is the planned identity platform on VLAN 20.

| Service | Port | Protocol | Purpose |
|---|---:|---|---|
| DNS | 53 | TCP/UDP | Internal DNS |
| Kerberos | 88 | TCP/UDP | Authentication |
| Kerberos password change | 464 | TCP/UDP | Password operations |
| LDAP | 389 | TCP | Directory services |
| LDAPS | 636 | TCP | Secure directory services |
| Kerberos administration | 749 | TCP | Kerberos administration |
| HTTPS | 443 | TCP | FreeIPA administration |
| HTTP | 80 | TCP | HTTP / redirect where required |

### Expected access

| Source | Destination | Ports | Policy |
|---|---|---|---|
| Management VLAN | `ipa01` | 443 | ALLOW |
| Identity clients | `ipa01` | 53, 88, 389, 464, 636 | ALLOW as required |
| Application VLAN | `ipa01` | Required identity/DNS ports only | RESTRICTED |
| Database VLAN | `ipa01` | Required dependency only | DENY by default |
| Internet | `ipa01` | Any | DENY |

---

## 5. PostgreSQL — `db01`

PostgreSQL is the planned database platform on VLAN 30.

| Service | Port | Protocol | Purpose |
|---|---:|---|---|
| PostgreSQL | 5432 | TCP | Application database access |
| SSH | 22 | TCP | Restricted administration |

### Expected access

| Source | Destination | Port | Policy |
|---|---|---:|---|
| Application VLAN | `db01` | 5432 | ALLOW |
| Management VLAN | `db01` | 5432 | RESTRICTED |
| Identity VLAN | `db01` | 5432 | DENY unless required |
| Internet | `db01` | 5432 | DENY |
| Other VLANs | `db01` | 5432 | DENY by default |

PostgreSQL should not be exposed directly to the Internet.

---

## 6. Application Platform — `app01`

`app01` is the planned Ubuntu/Docker application platform on VLAN 40.

The target architecture includes:

- Nginx
- Portainer
- Teleport CE
- Keycloak
- OpenBao
- NetBox
- Squid
- Forgejo
- Woodpecker CI
- Wiki.js
- Project Pulp

All services below are **planned** unless separately validated.

> **Port model:** Container ports and host-published ports are intentionally separated. Multiple containers may listen on the same internal port, but two containers cannot bind the same host IP/port. Internal application services should normally remain unpublished and be reached through Nginx or another explicitly documented ingress path. `**` indicates a deployment-specific binding that must be validated before implementation.

| Service | Container / Published Port | Protocol | Purpose |
|---|---:|---|---|
| Nginx HTTP | 80 | 80 | TCP | HTTP |
| Nginx HTTPS | 443 | 443 | TCP | HTTPS / reverse proxy |
| Portainer | 9443 | 9443 | TCP | Docker management |
| Portainer Agent | 9001 | 9001 | TCP | Docker agent |
| Teleport Proxy | 3080 | internal only | TCP | Web / proxy access |
| Teleport SSH Proxy | 3023 | 3023 | TCP | SSH proxy |
| Teleport Reverse Tunnel | 3024 | 3024 | TCP | Reverse tunnel |
| Teleport Kubernetes | 3026 | 3026 | TCP | Kubernetes access, if enabled |
| Keycloak | 8080 | internal only | TCP | Application SSO |
| Keycloak HTTPS | 8443 | internal only | TCP | Secure application SSO |
| OpenBao | 8200 | internal only | TCP | Secrets management API/UI |
| NetBox | 8000 | internal only | TCP | IPAM / DCIM |
| Forgejo Web | 3000 | internal only | TCP | Git web interface |
| Forgejo SSH | 2222 | 2222 | TCP | Git over SSH |
| Woodpecker Server | 8000 | internal only | TCP | CI/CD |
| Wiki.js | 3000 | internal only | TCP | Documentation |
| Squid | 3128 | 3128** | TCP | HTTP/HTTPS proxy |
| Project Pulp | 443 | internal only | TCP | Repository / artifact services |

> Multiple applications may use the same internal container port. Docker network isolation and published host ports must be documented separately when the application platform is implemented.

---

## 7. Recommended Application Exposure

The preferred external application pattern is:

```text
Client
  |
  | TCP 443
  v
Nginx
  |
  +----> Keycloak
  |
  +----> NetBox
  |
  +----> Forgejo
  |
  +----> Wiki.js
  |
  +----> Other HTTPS applications
```

Where practical, application services should **not** be individually exposed to external networks.

Preferred model:

```text
Internet / User Network
          |
        TCP 443
          |
        Nginx
          |
    Docker networks
          |
    Application services
```

This reduces the number of externally exposed ports and centralizes TLS/reverse-proxy handling.

---

## 8. Application → Database

Applications requiring PostgreSQL should use:

| Source | Destination | Port | Protocol |
|---|---|---:|---|
| `app01` | `db01` | 5432 | TCP |

No application should receive unrestricted access to PostgreSQL.

Database access should be restricted at multiple layers where practical:

```text
OPNsense firewall
      ↓
Host firewall
      ↓
PostgreSQL listen policy
      ↓
pg_hba.conf
      ↓
Database privileges
```

---

## 9. Application → Identity

Application-to-FreeIPA communication should be enabled only when an application actually requires it.

Possible services include:

| Source | Destination | Port | Purpose |
|---|---|---:|---|
| `app01` | `ipa01` | 53 | DNS |
| `app01` | `ipa01` | 88 | Kerberos |
| `app01` | `ipa01` | 389 | LDAP |
| `app01` | `ipa01` | 636 | LDAPS |
| `app01` | `ipa01` | 464 | Kerberos password operations |

These are **not blanket allow rules**. Enable only the ports required by the deployed application and identity integration.

---

## 10. Management Access Matrix

| Source | Destination | Port | Purpose | Policy |
|---|---|---:|---|---|
| Management VLAN | Proxmox | 8006 | Proxmox UI | ALLOW |
| Management VLAN | OPNsense | 443 | Firewall UI | ALLOW |
| Management VLAN | Linux VMs | 22 | SSH | RESTRICTED |
| Management VLAN | `ipa01` | 443 | FreeIPA administration | ALLOW |
| Management VLAN | `db01` | 5432 | PostgreSQL administration | RESTRICTED |
| Management VLAN | `app01` | 443 | Application gateway | ALLOW |
| Management VLAN | `app01` | 9443 | Portainer | RESTRICTED |
| Internet | Infrastructure management | Any | Direct management | DENY |

Remote administrative access should use a dedicated secure access mechanism rather than exposing management interfaces directly to WAN.

---

## 11. Internet Exposure Matrix

The target architecture follows a minimal-exposure model.

| Service | Internet Exposure |
|---|---|
| Nginx HTTPS | Only when a public application is intentionally provided |
| Nginx HTTP | Prefer redirect to HTTPS where required |
| Proxmox 8006 | **DENY** |
| OPNsense 443 | **DENY** |
| SSH 22 | **DENY** |
| PostgreSQL 5432 | **DENY** |
| FreeIPA LDAP 389 | **DENY** |
| FreeIPA LDAPS 636 | **DENY** |
| Kerberos 88 | **DENY** |
| Portainer 9443 | **DENY** |
| OpenBao 8200 | **DENY** |
| NetBox 8000 | **DENY directly** |
| Forgejo 3000 | **DENY directly** |
| Wiki.js 3000 | **DENY directly** |
| Squid 3128 | **DENY** |

Public application access should preferably terminate at Nginx on TCP 443.

---

## 12. Core Firewall Principle

The target inter-VLAN policy is:

```text
VLAN → VLAN = DENY
```

Required communication is explicitly permitted:

```text
Management → Infrastructure       ALLOW
Application → Database:5432        ALLOW
Identity clients → FreeIPA         ALLOW
Application → Identity             RESTRICTED
Database → Internet                DENY
Internet → Infrastructure          DENY
```

The exact firewall rules must be derived from the services actually deployed.

---

## 13. Port Classification

### Tier 1 — Infrastructure Management

| Port | Service |
|---:|---|
| 22 | SSH |
| 443 | HTTPS management |
| 8006 | Proxmox |

### Tier 2 — Identity

| Port | Service |
|---:|---|
| 53 | DNS |
| 88 | Kerberos |
| 389 | LDAP |
| 464 | Kerberos password change |
| 636 | LDAPS |
| 749 | Kerberos administration |

### Tier 3 — Database

| Port | Service |
|---:|---|
| 5432 | PostgreSQL |

### Tier 4 — Application

| Port | Service |
|---:|---|
| 80 | HTTP |
| 443 | HTTPS |
| 2222 | Forgejo SSH |
| 3000 | Forgejo / Wiki.js |
| 3023 | Teleport SSH proxy |
| 3024 | Teleport reverse tunnel |
| 3026 | Teleport Kubernetes |
| 3128 | Squid |
| 8000 | NetBox / Woodpecker |
| 8080 | Keycloak |
| 8200 | OpenBao |
| 8443 | Keycloak HTTPS |
| 9001 | Portainer Agent |
| 9443 | Portainer |

---

## 14. Port Exposure Rules

1. Do not expose a port only because a service supports it.
2. Define the source and destination before opening a port.
3. Prefer encrypted protocols.
4. Do not expose infrastructure management ports to WAN.
5. Do not expose PostgreSQL directly to the Internet.
6. Do not expose LDAP/Kerberos directly to the Internet.
7. Prefer Nginx as the application ingress point.
8. Use Docker networks for application-level isolation.
9. Document every published Docker port.
10. Remove unused published ports.
11. Review firewall rules when services are added or removed.
12. Validate both positive and negative traffic flows.

---

## 15. Implementation Evidence

When a service is actually deployed, record:

```text
Service:
Host:
Container:
Listen address:
Host port:
Container port:
Protocol:
Source networks:
Destination:
Firewall rule:
TLS:
Authentication:
Status:
Validation reference:
Known deviations:
```

Do not publish passwords, API tokens, private keys or other secrets.

---

## 16. Status Convention

| Status | Meaning |
|---|---|
| **Implemented** | Installed, configured and tested in the lab |
| **Validated** | Implemented and explicitly verified |
| **Planned** | Defined by the architecture but not deployed |
| **Future** | Deferred to a later phase |
| **Documented** | Design/reference information only |

A port must not be marked **Implemented** merely because it is listed in this document.

---

## 17. Related Documentation

- [Network Architecture](network.md)
- [Security Architecture](../security/security.md)
- [Architecture Overview](../architecture/overview.md)
- [VM Design](../vm-design/vm-design.md)
- [FreeIPA Installation](../day-1/freeipa/installation.md)
- [FreeIPA Validation](../day-1/freeipa/validation.md)
- [PostgreSQL Configuration](../day-1/postgresql/configuration.md)
- [OPNsense Configuration](../day-1/opnsense/configuration.md)

---

## Summary

The Port Map establishes a single reference for service communication in the Enterprise Reference Architecture.

The intended security model is:

```text
Default Deny
     ↓
Explicit Source
     ↓
Explicit Destination
     ↓
Explicit Protocol
     ↓
Explicit Port
     ↓
Explicit Reason
     ↓
Logging / Validation
```

> **A port is not an access requirement by itself. The required communication flow is the actual security boundary.**
