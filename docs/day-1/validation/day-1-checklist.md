# Day 1 — Validation Checklist

> **System Acceptance Checklist**

This checklist is the final Day 1 acceptance gate for the Enterprise Reference Architecture.

## Status

**Planned.** This is the acceptance framework. A check can be marked complete only after the corresponding lab test has actually been executed and evidence recorded.

---

## 1. Acceptance Model

Day 1 follows:

```text
Plan
 ↓
Prerequisites
 ↓
Install
 ↓
Configure
 ↓
Secure
 ↓
Integrate
 ↓
Validate
 ↓
Evidence
 ↓
Day 1 Acceptance
```

Installation alone does not constitute acceptance.

---

## 2. Status Rules

Use the following states:

- `[ ]` Not tested
- `[x]` Tested and passed
- `[!]` Tested and failed
- `[N/A]` Not applicable with documented reason
- `Planned` — not yet implemented

Do not mark a target architecture component as passed merely because its documentation exists.

---

# 3. Platform Foundation

## Proxmox VE

- [ ] Host boots successfully
- [ ] CPU virtualization is available
- [ ] RAM is correctly detected
- [ ] Storage is healthy
- [ ] Hostname/FQDN is correct
- [ ] DNS works
- [ ] NTP/time synchronization works
- [ ] Repositories are correctly configured
- [ ] Updates complete successfully
- [ ] `vmbr0` operates correctly
- [ ] Proxmox web interface is reachable from the intended management path
- [ ] SSH access follows the security policy
- [ ] QEMU Guest Agent works for guest VMs
- [ ] Firewall behavior is tested
- [ ] Reboot persistence is confirmed
- [ ] Evidence recorded

**Current project status:** Implemented, with individual validation items requiring lab evidence.

---

# 4. Firewall

## OPNsense / `fw01`

- [ ] VM boots successfully
- [ ] WAN interface is correct
- [ ] LAN interface is correct
- [ ] LAN management access works
- [ ] Third-computer management access works
- [ ] WAN connectivity works
- [ ] DNS works
- [ ] NTP works
- [ ] DHCP works where enabled
- [ ] Required outbound traffic works
- [ ] Unauthorized inbound traffic is blocked
- [ ] WAN management exposure is denied
- [ ] NAT behavior is correct
- [ ] Routing behavior is correct
- [ ] Firewall logging is available
- [ ] Configuration backup is created
- [ ] Configuration restore procedure is documented/tested as applicable
- [ ] Reboot persistence is confirmed
- [ ] Evidence recorded

**Current project status:** Implemented.

---

# 5. Network Segmentation

## VLAN Architecture

- [ ] VLAN 10 — Management implemented
- [ ] VLAN 20 — Identity implemented
- [ ] VLAN 30 — Database implemented
- [ ] VLAN 40 — Application implemented
- [ ] Proxmox VLAN transport validated
- [ ] OPNsense VLAN interfaces validated
- [ ] Each VLAN gateway responds
- [ ] DHCP behavior is correct where enabled
- [ ] DNS behavior is correct
- [ ] Internet policy is correct per VLAN
- [ ] Inter-VLAN default deny is proven
- [ ] Explicit allowed service paths are proven
- [ ] Management isolation is proven
- [ ] Database isolation is proven
- [ ] VLAN tag integrity is proven
- [ ] Failure isolation is tested
- [ ] Reboot persistence is confirmed
- [ ] Evidence recorded

**Current project status:** Planned.

---

# 6. FreeIPA / Identity

- [ ] `ipa01` VM created
- [ ] Fedora Server installed
- [ ] Hostname/FQDN correct
- [ ] Static network configuration correct
- [ ] DNS forward lookup works
- [ ] DNS reverse lookup works
- [ ] NTP works
- [ ] FreeIPA services are healthy
- [ ] Kerberos authentication works
- [ ] LDAP query works
- [ ] Admin authentication works
- [ ] User creation works
- [ ] Group creation works
- [ ] User/group authorization works
- [ ] Linux client enrollment works
- [ ] SSSD/NSS integration works
- [ ] Login using centralized identity works
- [ ] Sudo/privileged policy works where configured
- [ ] Certificate services validated where enabled
- [ ] Backup procedure exists
- [ ] Restore procedure tested where required
- [ ] Evidence recorded

**Current project status:** Planned.

---

# 7. PostgreSQL

## `db01`

- [ ] VM created with reference resources
- [ ] Pardus Server installed
- [ ] Two-disk storage model implemented
- [ ] Hostname/FQDN correct
- [ ] Network configuration correct
- [ ] DNS works
- [ ] NTP works
- [ ] PostgreSQL service starts
- [ ] Local database connection works
- [ ] Listening address is correct
- [ ] Port 5432 exposure is restricted
- [ ] Authentication policy works
- [ ] Application role works
- [ ] Application does not use PostgreSQL superuser
- [ ] Unauthorized role is denied
- [ ] Authorized application source can connect
- [ ] Unauthorized network source is denied
- [ ] TLS validated where required
- [ ] Logging works
- [ ] Backup succeeds
- [ ] Restore succeeds
- [ ] Reboot persistence confirmed
- [ ] Evidence recorded

**Current project status:** Planned.

---

# 8. Docker / Application Platform

## `app01`

- [ ] VM created with reference resources
- [ ] Ubuntu Server installed
- [ ] Two-disk storage model implemented
- [ ] Hostname/FQDN correct
- [ ] Network configuration correct
- [ ] DNS works
- [ ] NTP works
- [ ] Docker Engine installed
- [ ] Docker service is healthy
- [ ] Docker starts after reboot
- [ ] Compose functionality works
- [ ] Authorized administrator can manage Docker
- [ ] Unauthorized user cannot obtain Docker administrative control
- [ ] Test container lifecycle works
- [ ] Persistent storage survives container recreation
- [ ] Docker networks behave as designed
- [ ] Published ports are documented
- [ ] Undocumented ports are absent
- [ ] Container privileges are reviewed
- [ ] Image source/version is documented
- [ ] Resource baseline is recorded
- [ ] Health checks work where implemented
- [ ] Logging and rotation work
- [ ] Backup strategy is documented
- [ ] Restore is tested
- [ ] Evidence recorded

**Current project status:** Planned.

---

# 9. Application Services

The following are target services and must remain Planned until actually deployed:

- [ ] Nginx
- [ ] Portainer
- [ ] Teleport CE
- [ ] Keycloak
- [ ] OpenBao
- [ ] NetBox
- [ ] Squid
- [ ] Forgejo
- [ ] Woodpecker CI
- [ ] Wiki.js
- [ ] Project Pulp

For every implemented service:

- [ ] Installation evidence exists
- [ ] Configuration evidence exists
- [ ] Health check passes
- [ ] Network exposure is validated
- [ ] Authentication/authorization is validated
- [ ] Persistent state is validated
- [ ] Backup is validated
- [ ] Restore is validated or formally deferred with rationale
- [ ] Reboot behavior is validated
- [ ] Failure/recovery behavior is validated

---

# 10. Security Acceptance

- [ ] Default-deny firewall policy is proven where required
- [ ] Management access is restricted
- [ ] WAN administration is blocked unless explicitly required
- [ ] Inter-VLAN policy is restrictive
- [ ] Database access is restricted
- [ ] Docker administration is restricted
- [ ] Unnecessary container privileges are absent
- [ ] Unnecessary published ports are absent
- [ ] Secrets are not stored in Git
- [ ] Administrative roles follow least privilege
- [ ] Time synchronization works
- [ ] Security-relevant logs exist
- [ ] Backups are protected
- [ ] Public documentation contains no secrets
- [ ] Positive security tests pass
- [ ] Negative security tests pass

---

# 11. End-to-End Validation

Once the required components are implemented, execute the complete dependency chain.

Target:

```text
Client
  ↓
OPNsense
  ↓
Application VLAN
  ↓
Nginx / Application
  ↓
Identity / Authentication
  ↓
PostgreSQL
  ↓
Persistent Data
```

Validate:

- [ ] Client reaches intended service
- [ ] Unintended service is inaccessible
- [ ] DNS resolves correctly
- [ ] TLS works where required
- [ ] Authentication works
- [ ] Authorization works
- [ ] Application transaction succeeds
- [ ] Database transaction succeeds
- [ ] Persistent data is retained
- [ ] Relevant logs are generated
- [ ] Backup can be produced
- [ ] Recovery procedure is known

---

# 12. Failure and Recovery

Perform controlled failure tests after the platform is stable.

- [ ] Restart a VM and verify recovery
- [ ] Restart a representative container
- [ ] Stop/start a service dependency
- [ ] Verify firewall rule persistence
- [ ] Verify network configuration persistence
- [ ] Verify persistent application data
- [ ] Execute a test restore
- [ ] Record recovery time where useful
- [ ] Document unexpected behavior

Do not perform destructive tests against the only copy of important data.

---

# 13. Evidence Standard

Every completed validation should have evidence.

Recommended evidence record:

```text
Test ID:
Date:
Component:
Objective:
Precondition:
Test procedure:
Expected result:
Actual result:
PASS / FAIL / N/A:
Evidence location:
Known deviation:
Operator:
```

Evidence may include:

- Command output
- Configuration excerpt
- Screenshot
- Log entry
- Network test result
- Backup artifact verification
- Restore result

Never publish secrets, tokens, passwords, private keys, or sensitive personal information.

---

# 14. Day 1 Acceptance Gate

Day 1 should not be declared complete until:

1. All implemented components pass their applicable validation.
2. All planned components are clearly identified as Planned.
3. No architecture-only item is represented as implemented.
4. Required network paths work.
5. Required security boundaries are proven.
6. Unauthorized paths are proven blocked.
7. Identity dependencies work where implemented.
8. Database dependencies work where implemented.
9. Application dependencies work where implemented.
10. Persistence is proven.
11. Backup/recovery requirements are documented.
12. Evidence exists for completed tests.
13. Deviations from the reference architecture are documented.

> **Day 1 is accepted when the infrastructure is not only installed, but configured, secured, integrated, validated, and supported by evidence.**

## Related Documentation

- [`../README.md`](../README.md) — Day 1 overview
- [`../documentation-standard.md`](../documentation-standard.md) — Day 1 documentation standard
- [`../proxmox/validation.md`](../proxmox/validation.md) — Proxmox validation
- [`../opnsense/validation.md`](../opnsense/validation.md) — OPNsense validation
- [`../network/validation.md`](../network/validation.md) — Network validation
- [`../freeipa/validation.md`](../freeipa/validation.md) — FreeIPA validation
- [`../postgresql/validation.md`](../postgresql/validation.md) — PostgreSQL validation
- [`../docker/validation.md`](../docker/validation.md) — Docker validation
- [`../security/baseline.md`](../security/baseline.md) — Security baseline
- [`../../architecture/overview.md`](../../architecture/overview.md) — Architecture overview
