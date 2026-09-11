# Backup Strategy

> **Day 2 — Protect**

## Status

**Documented / Planned.** Backup requirements are defined. A complete backup platform and recurring restore-tested backup regime are not yet implemented in the lab.

## 1. Objective

Backups exist to provide a reliable recovery path after:

- accidental deletion;
- configuration errors;
- VM corruption;
- host failure;
- storage failure;
- security incidents.

## 2. Backup Principles

- Backup is separate from the production workload.
- Backup retention is intentional.
- Sensitive backup data is protected.
- Backup success is monitored.
- Restore is tested.
- Recovery objectives are documented.

## 3. Proxmox Backup Scope

Target backup scope includes:

- critical VMs;
- VM configuration/state required for recovery;
- important application data;
- OPNsense `fw01` configuration through its supported configuration backup mechanism.

Snapshots are not considered backups.

## 4. OPNsense Configuration Backup

The firewall configuration should have a protected recovery copy before significant changes.

At minimum the recovery record should identify:

- configuration date;
- affected firewall version;
- reason for backup;
- storage location;
- restore procedure.

Never commit configuration exports containing secrets to the public repository.

## 5. Retention Model

The exact retention schedule should be selected according to the lab's storage capacity and recovery objectives.

A useful baseline is:

```text
Short-term → frequent recovery points
Long-term  → fewer retained copies
```

Do not retain every backup indefinitely.

## 6. Backup Verification

A backup should be considered usable only after verification of:

- job completion;
- artifact existence;
- readable metadata;
- expected size/contents;
- retention behavior;
- restore capability through testing.

## 7. Restore Testing

Restore tests should be performed in an isolated or controlled environment when possible.

Minimum test sequence:

```text
Select backup
    ↓
Restore
    ↓
Boot / start service
    ↓
Validate configuration
    ↓
Validate network
    ↓
Validate service
    ↓
Record evidence
```

See [`restore-test.md`](restore-test.md).

## 8. Security

Protect backup data against unauthorized access and accidental exposure.

Public repository documentation must contain no:

- passwords;
- API tokens;
- private keys;
- configuration secrets;
- sensitive backup artifacts.

## 9. Completion Criteria

Backup capability becomes operationally mature when backups run according to policy, failures are detected, retention is understood, and restore tests demonstrate recoverability.
