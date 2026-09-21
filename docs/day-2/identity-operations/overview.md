# Identity Operations

> **Day 2 Operational Reference — Planned**

This document defines the operational model for the planned FreeIPA-based identity platform.

## Status

**Documented / Planned.** FreeIPA is not currently implemented in the laboratory. The procedures below become operational requirements when `ipa01` is deployed and validated.

## Scope

Identity operations cover:

- FreeIPA service health
- Identity and group administration
- Host enrollment
- Kerberos authentication
- LDAP / LDAPS access
- Identity-related DNS
- Sudo policy
- Certificate services where enabled
- Administrative access review
- Identity lifecycle and deprovisioning

## Reference Component

| Component | Role | Status |
|---|---|---|
| `ipa01` | FreeIPA identity / DNS | **Planned** |
| VLAN | 20 | **Planned** |
| Example IP | `10.10.20.10` | **Documented** |
| Example FQDN | `ipa01.corp.example.com` | **Documented** |

These values are documentation examples and are not implementation evidence.

## Operational Principles

1. Apply least privilege to users, groups and service identities.
2. Prefer centralized identity over local accounts where practical.
3. Review privileged memberships regularly.
4. Disable or remove identities that are no longer required.
5. Protect Kerberos, LDAP and certificate material.
6. Do not store passwords or secrets in the repository.
7. Validate DNS and time synchronization before troubleshooting authentication.
8. Record significant identity changes and their validation evidence.

## Dependency Order

When troubleshooting identity-dependent services, validate in this order:

```text
Network connectivity
      ↓
Time synchronization
      ↓
DNS resolution
      ↓
FreeIPA service health
      ↓
Kerberos / LDAP
      ↓
Host enrollment
      ↓
Application authentication
```

## Day 2 Checks

### Daily

- Confirm FreeIPA service availability.
- Check authentication-related errors.
- Verify DNS resolution for managed hosts.
- Review unexpected administrative activity.

### Weekly

- Review privileged group membership.
- Review failed authentication events.
- Check host enrollment state.
- Review certificate/service-account issues where applicable.

### Monthly

- Review inactive accounts.
- Review administrative access.
- Review identity-related firewall rules.
- Verify documentation against the implemented configuration.

## Related Documentation

- [Identity Architecture](../../architecture/identity.md)
- [Network Architecture](../../network/network.md)
- [DNS Architecture](../../network/dns.md)
- [Security Architecture](../../security/security.md)
- [Host Hardening](../../security/host-hardening.md)
- [Day 1 FreeIPA Configuration](../../day-1/freeipa/configuration.md)

> **Status discipline:** This runbook documents the target operating model. It does not make FreeIPA or any dependent capability Implemented or Validated.
