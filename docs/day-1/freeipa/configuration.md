# FreeIPA — Configuration

> **Day 1 — Configure & Secure**

This document defines the configuration baseline for the FreeIPA identity platform in the Enterprise Reference Architecture.

## Status

**Planned.** FreeIPA is not currently implemented in the laboratory.

The configuration below describes the target state and must not be interpreted as evidence of a deployed identity service.

---

## 1. Configuration Objectives

The FreeIPA configuration should provide:

- Central Linux identity
- Kerberos authentication
- LDAP directory services
- Controlled host enrollment
- Consistent identity-based access
- Internal DNS integration where selected
- Certificate capabilities where required
- Administrative separation
- Auditable identity operations

The service should be integrated only after the network layer is stable.

---

## 2. Naming Model

Reference naming:

```text
Host:   ipa01.corp.example.com
Domain: corp.example.com
Realm:  CORP.EXAMPLE.COM
```

The final values must be recorded as implementation evidence. Public repository documentation must not expose sensitive internal naming if the deployment uses non-public information.

---

## 3. Network Placement

FreeIPA belongs to the Identity VLAN.

Reference:

```text
VLAN 20
Network: 10.10.20.0/24
Gateway: 10.10.20.1
ipa01:   10.10.20.10
```

Management access should originate from the Management VLAN through explicitly permitted firewall rules.

---

## 4. DNS Configuration

DNS is a critical dependency of FreeIPA.

Define clearly whether FreeIPA will:

1. Provide authoritative DNS for the internal identity namespace, or
2. Integrate with an existing authoritative DNS service.

Avoid split ownership of the same DNS namespace.

Required records should include the FreeIPA host and appropriate reverse records.

Validate both directions before enrolling clients.

---

## 5. Kerberos Configuration

FreeIPA uses Kerberos for authentication.

The Kerberos realm should follow the documented identity namespace convention.

Reference:

```text
Realm: CORP.EXAMPLE.COM
```

Time synchronization must remain operational across all participating hosts.

A Kerberos authentication failure should first be investigated for:

- Clock skew
- DNS errors
- Incorrect hostname
- Incorrect realm
- Credential problems
- Service availability

---

## 6. Identity Structure

Create a simple directory structure before adding large numbers of users or systems.

Suggested conceptual groups:

```text
admins
infrastructure
developers
applications
read-only
```

The exact groups should be created only when an actual authorization requirement exists.

Do not create groups merely because they appear in a reference architecture.

---

## 7. User and Group Management

Use groups to manage authorization rather than assigning permissions individually whenever practical.

Target model:

```text
User
  ↓
Group membership
  ↓
Role / authorization
  ↓
Resource access
```

Administrative accounts should be separated from normal user identities where operationally appropriate.

Document:

- Group purpose
- Membership criteria
- Resource access
- Owner
- Review frequency

---

## 8. Host Enrollment

Linux hosts should be enrolled only after:

- DNS works
- NTP works
- Kerberos works
- FreeIPA is validated
- Network firewall rules permit the required services

Target:

```text
Linux host
    |
    +-- DNS
    +-- Kerberos
    +-- LDAP
    +-- FreeIPA enrollment
    |
    v
  ipa01
```

Use a controlled test VM first.

---

## 9. Access Control

The identity platform should support least-privilege administration.

Separate:

- Identity administration
- Infrastructure administration
- Application administration
- Read-only access

Do not grant global administrative privileges simply because they make initial testing easier.

---

## 10. Sudo / Privileged Access Model

When Linux hosts are integrated, privileged access should be managed through centrally defined policies where appropriate.

Example conceptual model:

```text
infra-admins
      |
      +--> permitted sudo commands
      |
      +--> selected hosts
```

Avoid blanket unrestricted sudo policies unless explicitly justified.

Any privileged command policy must be documented and validated against the actual operational requirement.

---

## 11. Certificate Services

FreeIPA can provide certificate-management capabilities where required.

Certificate services should be introduced only when an actual service requires them.

Potential future consumers include:

- Internal web services
- Infrastructure endpoints
- Application services
- Secure service-to-service communication

Private keys must never be committed to the repository.

---

## 12. Service Exposure

Firewall policy should restrict access to FreeIPA services to the networks that require them.

Conceptually:

```text
Management → FreeIPA administration       ALLOW
Identity clients → FreeIPA services       ALLOW
Database → FreeIPA                      DENY unless required
Application → FreeIPA                   DENY unless required
Internet → FreeIPA                      DENY
```

The actual service/port matrix must be based on the deployed FreeIPA configuration and client requirements.

---

## 13. Client DNS and Authentication Dependency

An enrolled Linux host should use the intended internal DNS service and maintain correct time synchronization.

The dependency chain is:

```text
Network
   ↓
DNS
   ↓
NTP
   ↓
Kerberos
   ↓
LDAP / Identity
   ↓
Host authentication
```

If an earlier dependency fails, troubleshooting should begin there rather than changing identity policies blindly.

---

## 14. Administrative Interface

The FreeIPA web interface and command-line administration tools should be reachable only through trusted management paths.

Validate:

- HTTPS access
- Administrative authentication
- Certificate validity
- Network restriction
- Audit visibility

Do not expose the administration interface directly to the Internet.

---

## 15. Logging and Auditing

Identity operations should produce sufficient evidence for troubleshooting and security review.

Review, where applicable:

- Authentication failures
- Administrative changes
- Host enrollment
- Group membership changes
- Privilege policy changes
- Certificate operations

Logs should have a defined retention approach consistent with the lab's operational requirements.

---

## 16. Backup Configuration

FreeIPA contains identity data that must be recoverable.

Define:

- Backup method
- Backup location
- Backup schedule
- Retention
- Encryption/protection
- Restore procedure
- Restore validation frequency

A backup should not be considered useful until a restore has been tested.

Backup and recovery become part of the Day 2 operational lifecycle.

---

## 17. Change Management

Identity changes can affect multiple systems.

Before changing:

- DNS configuration
- Kerberos realm configuration
- Authentication policies
- Group membership
- Privileged access
- Certificates

record:

```text
Change:
Reason:
Expected impact:
Backup/recovery point:
Validation:
Rollback:
Result:
```

---

## 18. Security Baseline

Minimum target baseline:

- Stable FQDN
- Correct DNS
- Correct time synchronization
- HTTPS administration
- Restricted administrative access
- Least-privilege groups
- No unnecessary services
- Controlled host enrollment
- Backup and restore procedure
- Auditable changes
- No credentials in Git

---

## 19. Configuration Evidence

Record actual values only after implementation:

```text
FreeIPA version:
Hostname:
FQDN:
Domain:
Realm:
IP address:
DNS mode:
NTP source:
Admin access path:
Client enrollment policy:
Backup method:
Firewall policy reference:
Known deviations:
```

Sensitive values should be redacted from public documentation.

---

## 20. Configuration Completion Criteria

FreeIPA configuration can be considered complete for Day 1 when:

1. DNS ownership is defined.
2. Hostname/FQDN are correct.
3. Time synchronization is stable.
4. Kerberos is operational.
5. LDAP is operational.
6. Required groups and initial administrative model exist.
7. Management access is restricted.
8. Required client network access is explicitly permitted.
9. Logging is operational.
10. Backup configuration is defined.
11. The configuration has passed the validation procedure.
12. Evidence is recorded.

## Related Documentation

- [`installation.md`](installation.md) — FreeIPA installation
- [`validation.md`](validation.md) — FreeIPA validation
- [`../network/segmentation.md`](../network/segmentation.md) — Network segmentation
- [`../network/validation.md`](../network/validation.md) — Network validation
- [`../../architecture/identity.md`](../../architecture/identity.md) — Identity architecture
- [`../../security/security.md`](../../security/security.md) — Security architecture
- [`../documentation-standard.md`](../documentation-standard.md) — Day 1 documentation standard
