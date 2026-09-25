# Firewall Rule Set

> Reference firewall policy for the Enterprise Reference Architecture.
>
> **Scope:** OPNsense `fw01`, four-zone target network, least-privilege inter-VLAN traffic, controlled WAN exposure.

---

## Status

**Documented / Planned architecture.**

OPNsense is implemented in the laboratory. The firewall rules in this document describe the **target rule set** for the segmented architecture and must not be treated as configured until each rule has been implemented and validated in the lab.

---

## 1. Purpose

This document translates the Network Architecture and Port Map into an explicit firewall policy.

The design follows:

- Default deny
- Least privilege
- Explicit source and destination
- Explicit protocol and port
- Minimal WAN exposure
- Controlled east-west traffic
- Centralized enforcement at OPNsense
- Logging for security-relevant decisions

> **Rule principle:** If a communication flow is not explicitly required and documented, it should not be allowed.

---

## 2. Network Zones

| Alias | VLAN | Network | Primary Role |
|---|---:|---|---|
| `MGMT_NET` | 10 | `10.10.10.0/24` | Management and automation |
| `IDENTITY_NET` | 20 | `10.10.20.0/24` | FreeIPA |
| `DB_NET` | 30 | `10.10.30.0/24` | PostgreSQL + Redis |
| `APP_NET` | 40 | `10.10.40.0/24` | Docker/application platform |
| `WAN` | — | Upstream | Internet / external network |

Reference hosts:

| Host | Address | Zone | Status |
|---|---|---|---|
| `fw01` | `10.10.10.1` | Management | Implemented |
| `ipa01` | `10.10.20.10` | Identity | Planned |
| `db01` | `10.10.30.10` | Database | Planned |
| `app01` | `10.10.40.10` | Application | Planned |
| `auto01` | `10.10.10.20` | Management | Planned |

> Addresses are reference values and may change during implementation.

---

## 3. Firewall Processing Model

Rules should be evaluated from specific to general.

Recommended logical order:

```text
1. Explicit infrastructure management rules
2. Explicit identity service rules
3. Explicit application-to-database rules
4. Explicit application-to-identity rules
5. Explicit approved outbound service rules
6. Explicit WAN port forwards / public ingress
7. Explicit deny / cleanup rules
8. Interface default deny
```

Avoid broad rules such as:

```text
ANY → ANY → ANY → PASS
```

A broad allow rule defeats the segmentation model.

---

## 4. Object / Alias Standard

Use aliases instead of repeatedly entering individual addresses and ports.

### Network aliases

| Alias | Value |
|---|---|
| `MGMT_NET` | `10.10.10.0/24` |
| `IDENTITY_NET` | `10.10.20.0/24` |
| `DB_NET` | `10.10.30.0/24` |
| `APP_NET` | `10.10.40.0/24` |
| `RFC1918_NETS` | All private RFC1918 networks used by the lab |

### Host aliases

| Alias | Value |
|---|---|
| `IPA01` | `10.10.20.10` |
| `DB01` | `10.10.30.10` |
| `APP01` | `10.10.40.10` |
| `AUTO01` | `10.10.10.20` |

### Port aliases

| Alias | Ports | Purpose |
|---|---|---|
| `MGMT_HTTPS` | 443, 8006 | OPNsense / Proxmox administration |
| `SSH` | 22 | Linux administration |
| `DNS` | 53 TCP/UDP | DNS |
| `NTP` | 123 UDP | Time synchronization |
| `FREEIPA_AUTH` | 88 TCP/UDP, 464 TCP/UDP | Kerberos |
| `FREEIPA_LDAP` | 389 TCP, 636 TCP | LDAP / LDAPS |
| `FREEIPA_ADMIN` | 749 TCP | Kerberos administration |
| `POSTGRESQL` | 5432 TCP | PostgreSQL |
| `REDIS` | 6379 TCP | Redis |
| `WEB` | 80, 443 TCP | HTTP / HTTPS |
| `APP_ADMIN` | 9443 TCP | Portainer |
| `TELEPORT` | 3023, 3024, 3026 TCP | Teleport |
| `KEYCLOAK` | 8080, 8443 TCP | Keycloak |
| `OPENBAO` | 8200 TCP | OpenBao |
| `GIT` | 2222, 3000 TCP | Forgejo |
| `NETBOX_WP` | 8000 TCP | NetBox / application web |
| `SQUID` | 3128 TCP | Proxy |

Only create aliases for ports that are actually required by an implemented service.

---

## 5. WAN Inbound Policy

### Default

| Rule ID | Source | Destination | Service | Action | Log |
|---|---|---|---|---|---|
| WAN-IN-001 | Any | WAN address | Any | **BLOCK** | Yes |

No unsolicited WAN traffic should reach internal networks.

### Public HTTPS — future / conditional

Only when a public application is intentionally published:

| Rule ID | Source | Destination | Service | Action | Log |
|---|---|---|---|---|---|
| WAN-IN-010 | Any | `APP01` via NAT | TCP 443 | **PASS** | Yes |

Recommended pattern:

```text
Internet
   |
 TCP 443
   v
OPNsense NAT
   |
   v
Nginx / application ingress
   |
   +--> Internal applications
```

Do not publish backend application ports directly when Nginx can provide the ingress point.

### WAN management must remain blocked

| Service | Action |
|---|---|
| OPNsense Web UI 443 | **BLOCK** |
| Proxmox 8006 | **BLOCK** |
| SSH 22 | **BLOCK** |
| PostgreSQL 5432 | **BLOCK** |
| FreeIPA 88/389/464/636/749 | **BLOCK** |
| Portainer 9443 | **BLOCK** |
| OpenBao 8200 | **BLOCK** |
| Squid 3128 | **BLOCK** |

---

## 6. Management VLAN Rules

Management is the administrative control zone.

### Allowed management access

| Rule ID | Source | Destination | Service | Action | Log | Reason |
|---|---|---|---|---|---|---|
| MGMT-001 | `MGMT_NET` | `fw01` | TCP 443 | PASS | Yes | Firewall management |
| MGMT-002 | `MGMT_NET` | Proxmox nodes | TCP 8006 | PASS | Yes | Proxmox management |
| MGMT-003 | `MGMT_NET` | Linux VMs | TCP 22 | PASS | Yes | Restricted administration |
| MGMT-004 | `MGMT_NET` | `IPA01` | TCP 443 | PASS | Yes | FreeIPA administration |
| MGMT-005 | `MGMT_NET` | `DB01` | TCP 5432 | PASS | Yes | Database administration |
| MGMT-006 | `MGMT_NET` | `APP01` | TCP 443 | PASS | Yes | Application gateway |
| MGMT-007 | `MGMT_NET` | `APP01` | TCP 9443 | PASS | Yes | Portainer administration |

### Management outbound

| Rule ID | Source | Destination | Service | Action | Reason |
|---|---|---|---|---|---|
| MGMT-010 | `MGMT_NET` | WAN | DNS / HTTPS / NTP as required | PASS | Administrative updates and name/time services |

Do not use unrestricted `MGMT_NET → WAN ANY` unless there is a specific lab requirement.

---

## 7. Identity VLAN Rules

`ipa01` provides identity and DNS services.

### Client / application access to FreeIPA

| Rule ID | Source | Destination | Service | Action | Reason |
|---|---|---|---|---|---|
| IDP-001 | `MGMT_NET` | `IPA01` | TCP 443 | PASS | Administration |
| IDP-002 | Authorized clients | `IPA01` | DNS | PASS | Internal name resolution |
| IDP-003 | Authorized clients | `IPA01` | Kerberos | PASS | Authentication |
| IDP-004 | Authorized clients | `IPA01` | LDAP/LDAPS | PASS | Directory access |
| IDP-005 | Authorized clients | `IPA01` | Kerberos password | PASS | Password operations |

Use application-specific source aliases where possible instead of allowing the entire `APP_NET` to every FreeIPA service.

### Identity VLAN outbound

| Rule ID | Source | Destination | Service | Action | Reason |
|---|---|---|---|---|---|
| IDP-010 | `IPA01` | Approved DNS / NTP / update destinations | Required services | PASS | System maintenance |
| IDP-011 | `IPA01` | WAN | Any other traffic | **BLOCK** | Minimize outbound access |

---

## 8. Database VLAN Rules

The database zone is intentionally restrictive.

### Application database access

| Rule ID | Source | Destination | Service | Action | Log | Reason |
|---|---|---|---|---|---|---|
| DB-001 | `APP01` | `DB01` | TCP 5432 | PASS | Yes | Application database access |
| DB-003 | `APP01` | `DB01` | TCP 6379 | PASS when required | Yes | Application Redis access |

### Management database access

| Rule ID | Source | Destination | Service | Action | Log | Reason |
|---|---|---|---|---|---|---|
| DB-002 | `MGMT_NET` | `DB01` | TCP 5432 | PASS | Yes | Administrative database access |

### Database isolation

| Rule ID | Source | Destination | Service | Action |
|---|---|---|---|---|
| DB-010 | `IDENTITY_NET` | `DB_NET` | Any | **BLOCK** |
| DB-011 | `APP_NET` | `DB_NET` | Any except DB-001 | **BLOCK** |
| DB-012 | `DB_NET` | `MGMT_NET` | Any | **BLOCK** unless explicitly required |
| DB-013 | `DB_NET` | `IDENTITY_NET` | Any | **BLOCK** |
| DB-014 | `DB_NET` | `WAN` | Any | **BLOCK** by default |

> PostgreSQL access should also be restricted by PostgreSQL configuration and `pg_hba.conf`. The network rule is only one enforcement layer.

---

## 9. Application VLAN Rules

`app01` hosts the planned Docker application platform.

### Management access

| Rule ID | Source | Destination | Service | Action |
|---|---|---|---|---|
| APP-001 | `MGMT_NET` | `APP01` | TCP 443 | PASS |
| APP-002 | `MGMT_NET` | `APP01` | TCP 9443 | PASS |
| APP-003 | `MGMT_NET` | `APP01` | TCP 22 | PASS where required |

### Application → Database

| Rule ID | Source | Destination | Service | Action |
|---|---|---|---|---|
| APP-010 | `APP01` | `DB01` | TCP 5432 | PASS |
| APP-011 | `APP01` | `DB01` | TCP 6379 | PASS when required |

### Application → Identity

Enable only when a deployed application requires the service.

| Rule ID | Source | Destination | Service | Action |
|---|---|---|---|---|
| APP-020 | Specific application / `APP01` | `IPA01` | DNS 53 | PASS |
| APP-021 | Specific application / `APP01` | `IPA01` | Kerberos 88 | PASS when required |
| APP-022 | Specific application / `APP01` | `IPA01` | LDAP/LDAPS | PASS when required |
| APP-023 | Specific application / `APP01` | `IPA01` | Kerberos password 464 | PASS when required |

Do not enable the entire identity port set simply because FreeIPA is present.

### Application outbound access

| Rule ID | Source | Destination | Service | Action | Reason |
|---|---|---|---|---|---|
| APP-030 | `APP01` | Approved update / container registries | HTTPS | PASS | Updates and image retrieval |
| APP-031 | `APP01` | Approved DNS | DNS | PASS | Name resolution |
| APP-032 | `APP01` | Approved NTP | NTP | PASS | Time synchronization |

All other unsolicited outbound traffic should be blocked unless a specific workload requires it.

---

## 10. East-West Default Deny Matrix

The following matrix represents the **default state before exception rules**.

| Source → Destination | Management | Identity | Database | Application |
|---|---:|---:|---:|---:|
| Management | Local / explicit | Allow required | Allow required | Allow required |
| Identity | Deny by default | Local | Deny | Deny unless required |
| Database | Deny | Deny | Local | Deny |
| Application | Deny | Restricted | TCP 5432 only | Local / Docker controls |

This ensures that lateral movement is not enabled merely because routing exists.

---

## 11. Inter-VLAN Exception Summary

The minimum target flows are:

```text
MGMT → fw01                  TCP 443
MGMT → Proxmox               TCP 8006
MGMT → Linux hosts           TCP 22
MGMT → ipa01                 TCP 443
MGMT → db01                  TCP 5432
MGMT → app01                 TCP 443 / 9443

Authorized clients → ipa01  DNS / Kerberos / LDAP as required

app01 → db01                TCP 5432

app01 → ipa01               Only identity ports required by deployed apps
```

Everything else remains denied unless an additional documented dependency exists.

---

## 12. DNS and NTP Policy

Time and name resolution are infrastructure dependencies and should be explicitly defined.

### DNS

| Source | Destination | Port | Action |
|---|---|---:|---|
| Management | Approved DNS | 53 TCP/UDP | PASS |
| Identity | Approved DNS | 53 TCP/UDP | PASS |
| Database | Approved DNS | 53 TCP/UDP | PASS only if required |
| Application | Approved DNS | 53 TCP/UDP | PASS |

### NTP

| Source | Destination | Port | Action |
|---|---|---:|---|
| Infrastructure VMs | Approved NTP source | UDP 123 | PASS |

Prefer the project / organization NTP source where available.

---

## 13. ICMP Policy

ICMP should not be treated as unrestricted application traffic.

Recommended model:

| Rule ID | Source | Destination | Type | Action |
|---|---|---|---|---|
| ICMP-001 | `MGMT_NET` | Infrastructure | Echo / required diagnostics | PASS |
| ICMP-002 | Infrastructure | Required gateways | Required diagnostic ICMP | PASS |
| ICMP-003 | Other VLANs | Management | Any | BLOCK unless explicitly required |

Use ICMP where it supports troubleshooting, monitoring, or path-MTU behavior without creating an unnecessary trust relationship.

---

## 14. NAT Policy

### Outbound NAT

Expected baseline:

```text
MGMT_NET
IDENTITY_NET
DB_NET
APP_NET
      |
      v
Outbound NAT
      |
     WAN
```

Outbound NAT should support required Internet access for updates and approved services.

### Port forwards

Port forwards should be exceptional.

Before creating a port forward, document:

```text
Service:
Public protocol:
Public port:
Internal host:
Internal port:
Source restriction:
Reason:
TLS:
Authentication:
Logging:
Review / removal condition:
```

Never create a generic forward such as:

```text
WAN ANY → INTERNAL ANY
```

---

## 15. Public Application Exposure

When public access is required, use a reverse-proxy model.

Preferred:

```text
Internet
   |
 TCP 443
   |
OPNsense NAT
   |
 Nginx
   |
+--+-----------------------+
|                          |
Keycloak / NetBox /        |
Forgejo / Wiki.js / ...    |
```

Avoid exposing these ports directly to WAN:

- 3000
- 3023
- 3024
- 3128
- 5432
- 8000
- 8080
- 8200
- 8443
- 9001
- 9443

The exact exposure decision remains service-specific.

---

## 16. Logging Policy

Log events that are useful for security monitoring and troubleshooting.

### Log

- WAN blocks
- WAN public application passes
- Inter-VLAN exception passes
- Database access rules
- Management access rules
- Important explicit blocks
- Unexpected outbound blocks

### Avoid excessive logging

Do not automatically log every internal packet at every rule if this produces large volumes without operational value.

A practical approach is:

```text
Security-sensitive rule → Log
Troubleshooting rule → Log during testing
Routine high-volume allow → Log selectively
Default deny → Log at a useful boundary
```

Where centralized logging is implemented, forward firewall events to the logging platform according to project policy.

---

## 17. Rule Naming Convention

Use deterministic IDs so the rule set can be discussed, reviewed, and reproduced.

Recommended:

```text
WAN-IN-xxx
MGMT-xxx
IDP-xxx
DB-xxx
APP-xxx
ICMP-xxx
NAT-xxx
```

Examples:

```text
APP-010  app01 → db01 : TCP/5432
MGMT-002 MGMT_NET → Proxmox : TCP/8006
WAN-IN-010 Internet → Nginx : TCP/443
```

---

## 18. Rule Change Procedure

Every firewall change should follow:

```text
Requirement
    ↓
Source
    ↓
Destination
    ↓
Protocol
    ↓
Port
    ↓
Security reason
    ↓
Rule ID
    ↓
Implement
    ↓
Test allow flow
    ↓
Test deny flow
    ↓
Review logs
    ↓
Update documentation
```

One logical change should be made at a time during troubleshooting.

Before significant changes:

1. Back up the OPNsense configuration.
2. Record the current rule state.
3. Make the change.
4. Validate management access.
5. Validate the intended flow.
6. Validate an expected denied flow.
7. Update this document.

---

## 19. Validation Matrix

A rule is not considered **Validated** merely because it exists.

### Positive tests

| Test | Expected |
|---|---|
| Management PC → OPNsense 443 | PASS |
| Management PC → Proxmox 8006 | PASS |
| Management PC → Linux SSH 22 | PASS where required |
| app01 → db01:5432 | PASS |
| Authorized client → FreeIPA required ports | PASS |
| WAN → published Nginx:443 | PASS only when intentionally published |

### Negative tests

| Test | Expected |
|---|---|
| WAN → Proxmox 8006 | BLOCK |
| WAN → OPNsense 443 | BLOCK |
| WAN → SSH 22 | BLOCK |
| WAN → PostgreSQL 5432 | BLOCK |
| WAN → FreeIPA | BLOCK |
| app01 → db01:22 | BLOCK unless explicitly required |
| Identity → db01:5432 | BLOCK |
| Database → Management | BLOCK unless explicitly required |
| Database → WAN | BLOCK by default |

---

## 20. Security Review Checklist

Before marking the policy validated, confirm:

- [ ] Default deny is active.
- [ ] WAN management access is blocked.
- [ ] Proxmox 8006 is not exposed to WAN.
- [ ] SSH is not exposed to WAN.
- [ ] PostgreSQL 5432 is not exposed to WAN.
- [ ] FreeIPA services are not exposed to WAN.
- [ ] Inter-VLAN traffic is denied by default.
- [ ] Application → Database is limited to documented PostgreSQL/Redis ports.
- [ ] Redis 6379 is allowed only for applications that explicitly require it.
- [ ] Application → Identity is limited to actual application requirements.
- [ ] Management access is restricted to the management zone.
- [ ] Public services, when required, terminate at the intended ingress point.
- [ ] Unused port forwards are removed.
- [ ] Firewall logs are reviewed.
- [ ] Expected allowed flows have been tested.
- [ ] Expected denied flows have been tested.
- [ ] OPNsense configuration backup exists before major changes.
- [ ] Documentation matches the actual configuration.

---

## 21. Implementation Evidence

For each implemented rule, record:

```text
Rule ID:
Description:
Source:
Destination:
Protocol:
Port:
Interface:
Action:
NAT / Port Forward:
Logging:
Date implemented:
Date validated:
Test source:
Test destination:
Expected result:
Actual result:
Known deviations:
```

Do not publish secrets, tokens, private keys, public IPs that are not intentionally part of the design, or other sensitive infrastructure details.

---

## 22. Status Convention

| Status | Meaning |
|---|---|
| **Implemented** | Rule exists in OPNsense |
| **Validated** | Rule exists and traffic behavior has been tested |
| **Planned** | Required by target architecture but not configured |
| **Future** | Deferred |
| **Documented** | Design/reference only |

A rule listed here is **Planned** until configuration evidence exists.

---

## Related Documentation

- [Network Architecture](network.md)
- [Port Map](port-map.md)
- [Security Architecture](../security/security.md)
- [OPNsense Configuration](../day-1/opnsense/configuration.md)
- [Architecture Overview](../architecture/overview.md)
- [VM Design](../vm-design/vm-design.md)

---

## Summary

The target firewall policy is:

```text
                    DEFAULT DENY
                         |
        +----------------+----------------+
        |                |                |
     North-South      East-West       Management
        |                |                |
   Minimal WAN      Explicit flows    MGMT only
        |                |                |
     TCP 443        app → db:5432     Admin services
                    app → ipa:*       explicitly allowed
```

The intended security boundary is not the existence of a VLAN or a port.

```text
Source
  ↓
Destination
  ↓
Protocol
  ↓
Port
  ↓
Reason
  ↓
Allow / Deny
  ↓
Logging
  ↓
Validation
```

> **Default deny is the baseline. Every exception should have a documented reason and a testable communication flow.**
