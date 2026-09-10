# Identity Architecture

> Identity architecture for the Enterprise Reference Architecture, covering centralized identity, authentication, authorization, service identities, and privileged access.

## Purpose

This document defines the identity architecture of the Enterprise Reference Architecture.
The identity platform is designed around **centralized identity, least privilege, Zero Trust, and separation of authentication from application authorization**.
The architecture uses open-source technologies and avoids dependence on a traditional Microsoft Active Directory domain.

---

## Identity Principles

The identity architecture follows these principles:

* **Centralized Identity** — User identities are managed from a single authoritative identity service.
* **Single Sign-On (SSO)** — Applications should use centralized authentication where practical.
* **Least Privilege** — Users and services receive only the permissions required for their responsibilities.
* **Zero Trust** — Authentication and authorization are continuously evaluated rather than implicitly trusted based on network location.
* **No Shared Accounts** — Individual administrative and user identities are preferred over shared credentials.
* **No Plaintext Secrets** — Passwords, API keys, tokens, and service credentials must not be stored in plaintext configuration files.
* **Separation of Duties** — Identity administration, infrastructure administration, and application administration should be logically separated.
* **Service Identity Isolation** — Applications and automation use dedicated service identities rather than personal accounts.
* **Auditable Access** — Authentication and privileged access should produce logs that can be reviewed and correlated.

---

## Identity Components

| Component | Role |
|---|---|
| **FreeIPA** | Central identity, authentication, authorization, Kerberos, LDAP, and host identity |
| **Keycloak** | Application-focused identity provider and SSO using modern protocols |
| **OpenBao** | Secrets management and machine/application credentials |
| **Teleport CE** | Secure privileged access to infrastructure |
| **NetBox** | Source of truth for infrastructure and network inventory |
| **Ansible** | Identity-aware infrastructure automation |
| **PostgreSQL** | Application data storage; authentication is delegated to the appropriate identity layer where supported |

---

## Identity Authority

### FreeIPA

FreeIPA is the primary infrastructure identity platform.

It provides centralized user and group management, LDAP directory services, Kerberos authentication, host enrollment, host-based access control, sudo policy management, SSH key management, certificate management, and centralized identity for Linux systems.

The primary identity server is `ipa01`, running on Fedora Linux.

FreeIPA is responsible primarily for **infrastructure identity**, rather than directly managing every application's user database.

---

## Application Identity

### Keycloak

Keycloak provides application-oriented identity and Single Sign-On.

Applications should integrate with Keycloak using standards such as:

* OpenID Connect (OIDC)
* OAuth 2.0
* SAML 2.0 where required

The application identity flow is:

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
Identity / Authentication
```

Where appropriate, Keycloak can use FreeIPA/LDAP as an external identity source.

This creates a separation between infrastructure identity and application identity, allowing the two domains to evolve independently.

---

## Authentication Flow

A typical user authentication flow is:

```text
                    +----------------+
                    |     User       |
                    +-------+--------+
                            |
                            v
                    +-------+--------+
                    |  Application   |
                    +-------+--------+
                            |
                            v
                    +-------+--------+
                    |   Keycloak     |
                    +-------+--------+
                            |
                            v
                    +-------+--------+
                    |    FreeIPA     |
                    +----------------+
```

The exact flow depends on the application.
Applications that support OIDC should preferably authenticate through Keycloak rather than implementing independent authentication systems.

---

## Linux Host Identity

Linux servers participating in centralized identity should be enrolled into FreeIPA.
Infrastructure access should be controlled through identity and policy rather than manually maintained local accounts wherever practical.

Local accounts may still exist for initial installation, emergency recovery, break-glass access, or system-specific requirements. Such accounts must be tightly controlled and documented.

---

## Administrative Access

Administrative access is separated from normal application access.

The preferred administrative path is:

```text
Administrator
      |
      v
  Teleport
      |
      +--------> Linux Hosts
      |
      +--------> Infrastructure Services
```

Teleport provides a controlled access layer for privileged infrastructure connections and supports centralized access control and auditing.

---

## Privileged Identity

Privileged access follows these principles:

1. Administrative accounts are separate from normal user identities.
2. Privileged access is granted only when required.
3. Access should be attributable to an individual.
4. Direct root access is minimized.
5. Sudo policies are centrally managed where possible.
6. Administrative sessions should be auditable.
7. Credentials should not be permanently embedded in scripts or configuration files.

---

## Service Identities

Applications and automation should not use personal user accounts.
Each significant service should have a dedicated identity.

Examples:

```text
svc-keycloak
svc-netbox
svc-woodpecker
svc-ansible
svc-backup
```

Service credentials should be stored and distributed through **OpenBao** where supported.

---

## Secrets Management

Identity and secrets management are deliberately separated.
FreeIPA manages identities and authentication.
Keycloak manages application-oriented authentication and SSO.
OpenBao manages secrets.

```text
+------------------+
|     FreeIPA      |
| Identity/Auth    |
+--------+---------+
         |
         v
+------------------+
|    Keycloak      |
| Application SSO  |
+------------------+

+------------------+
|     OpenBao      |
| Secrets / Keys   |
+------------------+
```

Passwords, API tokens, certificates, database credentials, and other sensitive values should be stored in OpenBao whenever practical.

---

## Groups and Authorization

Authorization should be based on groups and roles rather than individual permissions whenever possible.

Example infrastructure groups:

```text
Users
 |
 +-- Infrastructure-Admins
 +-- Network-Admins
 +-- Database-Admins
 +-- Application-Admins
 +-- ReadOnly-Admins
```

Applications can implement their own roles through Keycloak, for example `platform-admin`, `application-admin`, `developer`, `auditor`, and `readonly`.

Group and role names should remain consistent across systems to simplify administration and auditing.

---

## Identity Lifecycle

The identity lifecycle follows:

```text
Create
  |
  v
Assign Groups/Roles
  |
  v
Authenticate
  |
  v
Authorize
  |
  v
Audit
  |
  v
Review
  |
  v
Disable
  |
  v
Remove
```

When a user leaves the environment, access should be revoked from the central identity system first. Dependent application and privileged access should then be reviewed.

---

## Break-Glass Access

Emergency access must remain possible even if the central identity platform is unavailable.

Break-glass access should:

* Be limited to emergency use
* Use dedicated credentials
* Be protected separately from normal credentials
* Be documented
* Be audited after use
* Not be used for routine administration

The existence of break-glass access must not become a reason to bypass centralized identity.

---

## Identity and Network Segmentation

Identity services are located within the infrastructure security model rather than being treated as universally trusted services.

The architecture separates user, server, management, database, application, and security/infrastructure networks.
Network location alone does not grant access.

Firewall policies should explicitly permit only the required communication between these services.

---

## Identity Dependencies

```text
                    +----------------+
                    |    FreeIPA     |
                    +-------+--------+
                            |
                +-----------+-----------+
                |                       |
                v                       v
           Linux Hosts              Keycloak
                                        |
                                        v
                                  Applications

                    +----------------+
                    |    OpenBao     |
                    +-------+--------+
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
          Applications   Automation    Services

                    +----------------+
                    |   Teleport     |
                    +-------+--------+
                            |
                            v
                    Administrative
                       Access
```

---

## Security Considerations

The identity architecture must protect against credential theft, password reuse, privilege escalation, unauthorized administrative access, service account abuse, token leakage, hard-coded credentials, excessive permissions, orphaned accounts, and uncontrolled local accounts.

Recommended controls include strong authentication policies, MFA where supported, centralized logging, short-lived credentials where practical, role-based access control, regular access reviews, secure secret storage, administrative session auditing, and network-level access controls.

---

## Operational Guidelines

Identity-related configuration should be managed as infrastructure code wherever practical.

Changes should be:

1. Defined in version-controlled configuration.
2. Reviewed before deployment.
3. Applied through automation where practical.
4. Tested before production-like deployment.
5. Logged and auditable.

Credentials must never be committed to the public repository.
Public documentation should use placeholders such as `example.com` rather than real internal domains, usernames, addresses, or credentials.

---

## Design Summary

| Layer | Technology | Responsibility |
|---|---|---|
| Infrastructure Identity | FreeIPA | Users, groups, hosts, Kerberos, LDAP, Linux access |
| Application Identity | Keycloak | SSO, OIDC/OAuth2, application authentication |
| Secrets | OpenBao | Passwords, tokens, keys, certificates, application secrets |
| Privileged Access | Teleport CE | Controlled administrative access and session auditing |

The resulting model keeps **identity, application authentication, secrets, and privileged access as distinct security domains**, while allowing them to work together as a coherent enterprise identity architecture.
