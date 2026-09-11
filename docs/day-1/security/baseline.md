# Day 1 Security Baseline

> **Secure by Default**

This document defines the minimum security baseline that must be applied while building the Enterprise Reference Architecture.

## Status

**Documented / Planned.** The security architecture is defined, but most controls depend on components that have not yet been implemented.

Currently implemented infrastructure components are limited to Proxmox VE and OPNsense. The remaining controls must not be presented as implemented until they are configured and validated in the lab.

---

## 1. Security Objectives

The baseline follows these principles:

- Zero Trust
- Zero Plaintext
- Least Privilege
- Defense in Depth
- Microsegmentation
- Secure by Default
- Explicit Access
- Minimize Attack Surface
- Recoverability
- Evidence-based validation

Security is treated as an architectural property, not as a final installation step.

---

## 2. Security Boundaries

Target boundaries are:

```text
Internet
   ↓
OPNsense
   ↓
VLAN boundaries
   ↓
VM host boundaries
   ↓
Container network boundaries
   ↓
Application boundaries
   ↓
Database / Identity / Secrets
```

Each boundary should have an explicit policy.

---

## 3. Network Security

Target VLANs:

| VLAN | Role | Network | Status |
|---|---|---|---|
| 10 | Management | `10.10.10.0/24` | Planned |
| 20 | Identity | `10.10.20.0/24` | Planned |
| 30 | Database | `10.10.30.0/24` | Planned |
| 40 | Application | `10.10.40.0/24` | Planned |

Target policy:

```text
Inter-VLAN traffic = DENY by default
Required service   = explicit ALLOW
```

VLAN segmentation remains Planned until implemented and validated end-to-end.

---

## 4. Management Access

Management interfaces should be reachable only from trusted administrative paths.

Target controls:

- Dedicated Management VLAN
- Restricted Proxmox management
- Restricted OPNsense management
- Restricted Portainer access
- Restricted database administration
- Restricted identity administration

Management access should never be opened broadly simply for convenience.

---

## 5. Proxmox Security

Minimum target controls:

- Keep the host updated.
- Use controlled administrative accounts.
- Restrict SSH.
- Use HTTPS for management.
- Review permissions and roles.
- Enable appropriate firewall controls.
- Protect backups.
- Synchronize time.
- Minimize exposed services.

Proxmox is implemented, but each security control must still be validated against the actual host before being marked validated.

---

## 6. OPNsense Security

Minimum target controls:

- Default-deny firewall policy where appropriate
- Restricted management access
- No unnecessary WAN administration
- Explicit outbound policy where required
- Explicit inter-VLAN policy
- Logging of security-relevant traffic
- Configuration backup
- Time synchronization
- Controlled DNS behavior

OPNsense is implemented. VLAN and inter-VLAN controls remain Planned until deployed and tested.

---

## 7. Linux VM Security

For each Linux VM:

- Use a supported OS release.
- Apply security updates.
- Configure hostname and time synchronization.
- Disable unnecessary services.
- Restrict administrative access.
- Use least privilege.
- Avoid plaintext credentials.
- Configure host firewall where appropriate.
- Record deviations from the baseline.

---

## 8. Identity Security

FreeIPA is planned as the central FOSS identity platform.

Target capabilities:

- Central identity
- Groups
- Host enrollment
- Kerberos authentication
- LDAP directory services
- Certificate services where enabled
- Sudo policy
- Administrative separation

Until FreeIPA is implemented, it must not be described as the active identity provider.

---

## 9. Application Identity

Keycloak is planned for application identity and authentication integration.

Target principles:

- Centralized authentication where appropriate
- Explicit application clients
- Least privilege
- Restricted administration
- TLS
- Auditable authentication events

Keycloak is Planned.

---

## 10. Secrets Management

OpenBao is planned as the secrets-management component.

Secrets include:

- Passwords
- API tokens
- Private keys
- Service credentials
- Database credentials
- Certificates

Rules:

```text
Secret → secret store / secure runtime mechanism
Secret ≠ Git repository
Secret ≠ public documentation
Secret ≠ screenshot
```

OpenBao is Planned and must not be represented as an implemented control.

---

## 11. Database Security

PostgreSQL is planned on `db01`.

Target controls:

- Restricted listen addresses
- `pg_hba.conf` least privilege
- Dedicated application roles
- No application use of the superuser
- Network restriction to required sources
- TLS where required
- Logging
- Backup
- Restore testing

PostgreSQL is Planned.

---

## 12. Docker Security

The Docker platform is planned on `app01`.

Target controls:

- Restricted Docker administration
- Trusted images
- Documented versions
- No unnecessary privileged containers
- Least-required Linux capabilities
- Minimal host mounts
- Network segmentation
- Limited published ports
- Resource controls
- Health checks
- Log rotation
- Secure secret handling

Docker is Planned.

---

## 13. Container Image Security

For every important image record:

```text
Publisher:
Registry:
Image:
Version:
Digest where appropriate:
Update procedure:
```

Do not deploy unknown images merely because they appear functional.

Review image updates before deployment.

---

## 14. Administrative Privilege

Separate administrative responsibilities where practical.

Examples:

```text
Infrastructure Admin
        ↓
Proxmox / OPNsense

Identity Admin
        ↓
FreeIPA / Keycloak

Database Admin
        ↓
PostgreSQL

Application Admin
        ↓
Docker / Applications
```

The lab does not need to artificially reproduce every enterprise organizational boundary, but the architecture should demonstrate the principle of least privilege.

---

## 15. Logging and Audit

Security-relevant events should be recorded.

Target sources:

- OPNsense firewall
- Proxmox
- Linux hosts
- FreeIPA
- PostgreSQL
- Docker
- Applications
- Identity systems

Centralized logging/observability is Planned unless separately implemented.

---

## 16. Time Synchronization

Consistent time is a security dependency.

All systems should synchronize against the defined NTP hierarchy.

Validate:

```text
Proxmox
  ↓
VMs
  ↓
Applications
  ↓
Logs / authentication
```

Incorrect time can break Kerberos, TLS validation, logs, and incident analysis.

---

## 17. Patch Management

Day 1 installation must start from an updated supported base.

Target process:

```text
Check updates
    ↓
Review impact
    ↓
Backup if required
    ↓
Apply updates
    ↓
Reboot if required
    ↓
Validate
```

Recurring patch management belongs to Day 2.

---

## 18. Backup Security

Backups must be treated as sensitive infrastructure.

Protect against:

- Unauthorized access
- Accidental deletion
- Corruption
- Credential exposure
- Ransomware-like scenarios

Document:

- Backup location
- Access control
- Retention
- Encryption where appropriate
- Restore procedure

A backup that cannot be restored is not sufficient evidence of recoverability.

---

## 19. Public Repository Security

This project is intended for public GitHub publication.

Never commit:

- Passwords
- API tokens
- Private keys
- Real certificates containing sensitive material
- Internal credentials
- Personal access tokens
- Production IPs where disclosure is inappropriate
- Sensitive logs

Use documentation examples such as `corp.example.com` where appropriate.

---

## 20. Change Security

Security-sensitive changes should be documented before implementation where practical.

Examples:

- Firewall policy
- VLAN policy
- Identity policy
- Privileged access
- Database access
- Docker published ports
- Secrets configuration
- TLS configuration

For each significant change record:

```text
Change:
Reason:
Risk:
Affected systems:
Rollback:
Validation:
Evidence:
```

---

## 21. Security Validation

Security controls must include positive and negative tests.

Examples:

| Control | Positive test | Negative test |
|---|---|---|
| Firewall | Required service works | Unauthorized service blocked |
| VLAN | Required path works | Unapproved VLAN path blocked |
| Database | App can connect | Unapproved source denied |
| Management | Admin can connect | Untrusted source denied |
| Docker | Required container works | Unnecessary exposure absent |
| Identity | Authorized login works | Unauthorized access denied |

A configuration screenshot alone is not sufficient validation evidence.

---

## 22. Day 1 Security Completion Criteria

The Day 1 security baseline is complete when:

1. Network boundaries are documented.
2. Management access is defined.
3. Firewall policy is defined.
4. Host security baseline is defined.
5. Identity security model is defined.
6. Database security model is defined.
7. Container security model is defined.
8. Secrets handling is defined.
9. Logging requirements are defined.
10. Time synchronization is defined.
11. Backup security is defined.
12. Public repository security requirements are applied.
13. Positive and negative security tests are defined.
14. Implemented controls have actual lab evidence.

## Related Documentation

- [`../../architecture/overview.md`](../../architecture/overview.md) — Architecture overview
- [`../../architecture/network.md`](../../architecture/network.md) — Network architecture
- [`../../security/security.md`](../../security/security.md) — Security architecture
- [`../opnsense/configuration.md`](../opnsense/configuration.md) — OPNsense configuration
- [`../network/segmentation.md`](../network/segmentation.md) — Network segmentation
- [`../freeipa/configuration.md`](../freeipa/configuration.md) — FreeIPA configuration
- [`../postgresql/configuration.md`](../postgresql/configuration.md) — PostgreSQL configuration
- [`../docker/configuration.md`](../docker/configuration.md) — Docker configuration
