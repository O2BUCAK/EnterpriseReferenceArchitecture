# Proxmox VE — Backup & Recovery Runbook

> **Day 2 — Backup / Recover**

This runbook defines the backup and recovery model for the Proxmox platform.

## Status

**Documented / Planned.** The procedures are defined, but a successful restore test must be executed before recoverability is considered validated.

---

## 1. Recovery Objective

The objective is not merely to have backup files. The objective is to restore a usable VM and prove that it works.

```text
Backup
  ↓
Integrity check
  ↓
Restore
  ↓
Boot
  ↓
Network
  ↓
Service
  ↓
Functional validation
```

---

## 2. What Must Be Recoverable

At minimum consider:

- VM configuration
- Virtual disks
- Network configuration
- Application state
- Database state where applicable
- Required secrets/certificates through their secure recovery process
- Documentation required to operate the restored service

---

## 3. Backup Strategy

Define for each VM:

```text
VM:
Criticality:
Backup frequency:
Retention:
Backup target:
Encryption:
Expected restore time:
Restore validation:
```

Do not assume every VM requires identical retention.

---

## 4. Pre-Change Backup

Before high-risk changes:

1. Identify the affected VM.
2. Confirm current backup availability.
3. Create a new backup if required.
4. Verify the backup completed.
5. Record the change and recovery point.

Snapshots may be useful for short-term rollback but are not a substitute for independent backups.

---

## 5. Backup Validation

A completed job is only the first check.

Verify:

- Job status
- Artifact existence
- Expected size
- Storage availability
- Retention behavior
- Ability to access the artifact

Where supported, use integrity verification.

---

## 6. Restore Test

Use an isolated or controlled target where practical.

Procedure:

1. Select a known backup.
2. Record its date/version.
3. Restore the VM.
4. Confirm disk attachment.
5. Confirm network configuration.
6. Boot the VM.
7. Verify guest OS health.
8. Verify services.
9. Verify application data.
10. Record the result.

---

## 7. Restore Success Criteria

A restore passes when:

- VM boots successfully.
- Expected storage is available.
- Network is functional.
- Required services start.
- Application data is present.
- Authentication works where applicable.
- Functional checks pass.
- No unexpected dependency is missing.

---

## 8. Recovery From Host Failure

If the Proxmox host becomes unavailable:

1. Confirm the failure scope.
2. Protect backup media/storage.
3. Recover the Proxmox platform or alternate virtualization host.
4. Restore critical VMs in dependency order.
5. Restore network services first where required.
6. Restore identity/database/application services according to dependency.
7. Validate end-to-end operation.

Target dependency order:

```text
Network / Firewall
       ↓
Identity / DNS
       ↓
Database
       ↓
Application
```

Actual order may change according to the implemented architecture.

---

## 9. Recovery From VM Failure

For a single VM failure:

1. Determine whether the failure is guest, storage, network, or application related.
2. Attempt safe guest recovery if appropriate.
3. Review recent changes.
4. Restore from backup if required.
5. Validate dependencies.
6. Record the incident.

Do not destroy the failed VM before preserving evidence when troubleshooting is valuable.

---

## 10. Backup Security

Protect backups against unauthorized access and accidental deletion.

Where practical:

- Restrict backup access.
- Separate backup credentials.
- Encrypt sensitive backups.
- Avoid exposing backup storage unnecessarily.
- Maintain retention that protects against accidental deletion.

---

## 11. Recovery Evidence

Record every restore test:

```text
Test ID:
Date:
VM:
Backup date:
Backup location:
Restore target:
Boot result:
Network result:
Service result:
Data result:
Functional result:
RTO observed:
Issues:
Corrective action:
Result: PASS / FAIL
```

---

## 12. Operational Completion Criteria

Backup/recovery is operationally validated only when:

1. Backups execute successfully.
2. Backup artifacts can be verified.
3. Retention works as intended.
4. A restore has been performed.
5. The restored VM boots.
6. Services recover.
7. Application data is present.
8. Functional validation passes.
9. Evidence is recorded.
10. Any recovery gaps have corrective actions.

## Related Documentation

- [`operations.md`](operations.md)
- [`monitoring.md`](monitoring.md)
- [`../backup/strategy.md`](../backup/strategy.md)
- [`../backup/restore-test.md`](../backup/restore-test.md)
- [`../disaster-recovery/overview.md`](../disaster-recovery/overview.md)
