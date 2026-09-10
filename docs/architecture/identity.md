# Identity Architecture

> Target identity architecture for the Enterprise Reference Architecture.

## Status

**Planned architecture.**

This document describes the intended identity model. The identity components listed below must not be interpreted as implemented until they are actually installed, configured, and tested in the lab.

## Status Convention

| Status | Meaning |
|---|---|
| **Implemented** | Installed, configured, and tested in the lab |
| **Planned** | Defined in the architecture but not yet implemented |
| **Future** | Deferred to a later phase |
| **Documented** | Design decision only |

---

## Purpose

The identity architecture is designed around centralized identity, least privilege, Zero Trust, separation of authentication from application authorization, and auditable access.

The architecture intentionally avoids dependence on Microsoft Active Directory and favors FOSS technologies.

---

## Identity Components

| Component | Intended Role | Status |
|---|---|---|
| **FreeIPA** | Central infrastructure identity, LDAP, Kerberos and host identity | **Planned** |
| **Keycloak** | Application identity provider and SSO | **Planned** |
| **OpenBao** | Secrets management | **Planned** |
| **Teleport CE** | Privileged infrastructure access | **Planned** |
| **NetBox** | Infrastructure and network source of truth | **Planned** |
| **Ansible** | Identity-aware infrastructure automation | **Planned** |
| **PostgreSQL** | Application data storage | **Planned** |

---

## Identity Authority — Planned

### FreeIPA

FreeIPA is the planned primary infrastructure identity platform.

The intended `ipa01` VM will provide centralized user and group management, LDAP, Kerberos, host enrollment, host-based access control, sudo policy management, SSH key management, certificate management, and Linux identity services.

`ipa01` is an architectural definition, not a statement that the VM is currently deployed.

---

## Application Identity — Planned

### Keycloak

Keycloak is planned as the application-oriented identity and Single Sign-On platform.

Applications should integrate through standards such as:

* OpenID Connect (OIDC)
* OAuth 2.0
* SAML 2.0 where required

Where appropriate, Keycloak is intended to use FreeIPA/LDAP as an external identity source.

---

## Planned Authentication Flow

```text
User
  |
  v
Application
  |
  v
Keycloak
  |
  v
FreeIPA / Identity Source
```

The exact flow will be validated during implementation.

---

## Linux Host Identity — Planned

Linux servers participating in centralized identity are intended to be enrolled into FreeIPA.

Local accounts may remain necessary for initial installation, emergency recovery, break-glass access, or system-specific requirements.

---

## Administrative Access — Planned

Teleport CE is planned as the controlled administrative access layer.

```text
Administrator
      |
      v
  Teleport CE
      |
      +----> Linux Hosts
      +----> Infrastructure Services
```

The access model, authentication method, and auditing capabilities will be validated when Teleport is implemented.

---

## Service Identities — Planned

Applications and automation should use dedicated service identities rather than personal accounts.

Examples include:

```text
svc-keycloak
svc-netbox
svc-woodpecker
svc-ansible
svc-backup
```

These are design examples only.

---

## Secrets Management — Planned

OpenBao is planned for centralized management of passwords, API tokens, database credentials, certificates, encryption keys, and service credentials.

The intended separation is:

```text
FreeIPA   -> Infrastructure Identity
Keycloak  -> Application SSO
OpenBao   -> Secrets
Teleport  -> Privileged Access
```

No claim is made that these services are currently deployed.

---

## Groups and Authorization — Design

Authorization should be based on groups and roles rather than individual permissions wherever practical.

Example groups:

```text
Users
 |
 +-- Infrastructure-Admins
 +-- Network-Admins
 +-- Database-Admins
 +-- Application-Admins
 +-- ReadOnly-Admins
```

These are planned authorization structures, not current lab accounts.

---

## Identity Lifecycle — Design

```text
Create
  |
Assign Groups/Roles
  |
Authenticate
  |
Authorize
  |
Audit
  |
Review
  |
Disable
  |
Remove
```

The lifecycle will be validated and refined during implementation.

---

## Break-Glass Access — Design

Emergency access should remain possible if centralized identity is unavailable.

Break-glass access should be limited, separately protected, documented, and audited after use.

---

## Dependencies

```text
                    FreeIPA (Planned)
                           |
                    +------+------+
                    |             |
                    v             v
             Linux Hosts      Keycloak
                                  |
                                  v
                            Applications

                    OpenBao (Planned)
                           |
              +------------+------------+
              |            |            |
              v            v            v
         Applications  Automation    Services

                   Teleport CE (Planned)
                           |
                           v
                   Administrative Access
```

---

## Security Considerations

The target identity architecture is intended to reduce credential theft, privilege escalation, unauthorized administrative access, service-account abuse, hard-coded credentials, excessive permissions, orphaned accounts, and uncontrolled local accounts.

Controls such as MFA, RBAC, centralized logging, short-lived credentials, access reviews, secure secret storage, and administrative session auditing should be implemented and validated as the lab progresses.

---

## Design Summary

| Layer | Technology | Status |
|---|---|---|
| Infrastructure Identity | FreeIPA | **Planned** |
| Application Identity | Keycloak | **Planned** |
| Secrets | OpenBao | **Planned** |
| Privileged Access | Teleport CE | **Planned** |

This document defines the **target identity architecture**, not the current implementation state.
