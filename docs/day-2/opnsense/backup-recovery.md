# OPNsense — Backup & Recovery Runbook

> **Day 2 — Backup / Recover**

This runbook defines how the `fw01` configuration and firewall service should be protected and recovered.

## Status

**Documented / Planned.** OPNsense is implemented, but recoverability is not considered validated until an actual configuration restore or equivalent recovery test is successfully executed.

---

## 1. Recovery Objective

The recovery objective is to restore firewall functionality, not merely to restore a configuration file.

```text
Configuration backup
        ↓
Restore
        ↓
Boot / apply configuration
        ↓
Interfaces
        ↓
Routing / NAT
        ↓
Firewall policy
        ↓
Client connectivity
```

---

## 2. Configuration Protection

Protect the OPNsense configuration because it may contain sensitive information.

Do not publish configuration backups to GitHub.

Store backups in an appropriately protected location.

---

## 3. When to Back Up

Create or verify a configuration backup:

- Before major firewall changes
- Before interface changes
- Before VLAN changes
- Before major updates
- After significant known-good configuration changes
- At the defined recurring backup interval

---

## 4. Backup Verification

For each backup verify:

- Backup completed.
- File/artifact exists.
- Timestamp is correct.
- Storage is accessible.
- Retention is functioning.
- Sensitive contents remain protected.

A file existing on disk is not proof that recovery will work.

---

## 5. Configuration Restore Test

Use a controlled recovery environment where practical.

Procedure:

1. Select a known-good backup.
2. Record backup date.
3. Restore configuration.
4. Verify interface assignments.
5. Verify addresses.
6. Verify gateways.
7. Verify firewall rules.
8. Verify NAT.
9. Verify DNS/DHCP where applicable.
10. Test management access.
11. Test expected client connectivity.
12. Test blocked traffic.
13. Record the result.

---

## 6. Recovery From Configuration Error

If a firewall change causes loss of connectivity:

1. Determine whether management access remains available.
2. Identify the most recent change.
3. Revert the change if safe.
4. Use the known-good configuration if required.
5. Restore management connectivity.
6. Test critical traffic.
7. Test security boundaries.
8. Record the incident and corrective action.

Avoid making multiple unrelated changes while troubleshooting.

---

## 7. Recovery From VM Failure

If `fw01` itself is unavailable:

1. Check Proxmox VM state.
2. Check virtual NICs.
3. Check VM storage.
4. Check recent host changes.
5. Recover the VM if possible.
6. Restore configuration if required.
7. Validate interfaces.
8. Validate routing/NAT.
9. Validate firewall rules.
10. Validate client connectivity.

---

## 8. Recovery From Host Failure

If the Proxmox host fails:

1. Confirm the host failure.
2. Recover the virtualization platform.
3. Restore `fw01` from the available recovery point.
4. Restore configuration if necessary.
5. Verify interfaces and gateways.
6. Verify management access.
7. Verify critical traffic paths.
8. Verify blocked traffic.

The wider disaster-recovery procedure is documented separately.

---

## 9. Security Validation After Restore

After restoring OPNsense, do not assume that configuration restoration equals security restoration.

Explicitly test:

- WAN management remains restricted.
- Required inbound/outbound traffic works.
- Unauthorized traffic remains blocked.
- NAT behaves as expected.
- DNS/DHCP policy remains correct.
- Management access is restricted.

---

## 10. Recovery Evidence

Record:

```text
Test ID:
Date:
Backup date:
Restore method:
Restore target:
Interface result:
Gateway result:
Firewall result:
NAT result:
DNS/DHCP result:
Positive traffic result:
Negative traffic result:
Result: PASS / FAIL
Issues:
Corrective action:
```

---

## 11. Operational Completion Criteria

OPNsense backup/recovery is validated only when:

1. Configuration backups are produced.
2. Backups are protected.
3. A known-good backup can be retrieved.
4. Configuration can be restored.
5. Interfaces recover.
6. Routing/NAT recover.
7. Firewall rules recover.
8. Management access works.
9. Required traffic works.
10. Unauthorized traffic remains blocked.
11. Evidence is recorded.

## Related Documentation

- [`operations.md`](operations.md)
- [`monitoring.md`](monitoring.md)
- [`../backup/strategy.md`](../backup/strategy.md)
- [`../backup/restore-test.md`](../backup/restore-test.md)
- [`../disaster-recovery/overview.md`](../disaster-recovery/overview.md)
- [`../../day-1/opnsense/configuration.md`](../../day-1/opnsense/configuration.md)
- [`../../day-1/opnsense/validation.md`](../../day-1/opnsense/validation.md)
