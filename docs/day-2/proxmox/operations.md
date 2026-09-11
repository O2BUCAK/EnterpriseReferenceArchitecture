# Proxmox VE — Operations Runbook

> **Day 2 — Operate**

This runbook defines routine operational activities for the Proxmox VE platform.

## Status

**Documented.** Proxmox VE is implemented in the laboratory. Individual procedures become operationally validated only after they are executed and evidence is recorded.

---

## 1. Operational Scope

This runbook covers:

- Host health
- VM lifecycle
- Resource review
- Storage review
- Network review
- Administrative access
- Updates
- Backup readiness
- Configuration changes
- Routine troubleshooting

It does not claim that every procedure has already been executed.

---

## 2. Start-of-Day Health Check

Review the Proxmox UI and confirm:

- Node is online.
- No unexpected critical alerts exist.
- CPU load is reasonable.
- Memory usage is reasonable.
- Storage is available.
- VMs expected to run are running.
- Network interfaces are healthy.
- Time synchronization is healthy.

CLI checks may include:

```bash
pveversion
pvesh get /nodes
systemctl --failed
uptime
free -h
df -h
```

Record anomalies rather than immediately changing configuration.

---

## 3. VM Lifecycle Operations

### Start

Before starting a VM:

1. Confirm the VM is expected to run.
2. Confirm required storage is available.
3. Confirm network prerequisites.
4. Start the VM.
5. Verify guest health.

### Stop

Prefer graceful guest shutdown.

Use forced stop only when normal shutdown is unavailable or unsafe.

### Restart

Use graceful reboot where possible.

After restart verify:

- Guest boot
- Network
- Services
- Time
- Application health

---

## 4. Resource Operations

Review:

- CPU allocation vs actual use
- Memory allocation vs actual use
- Storage consumption
- VM disk growth
- Host pressure

Do not increase VM resources automatically because of a temporary spike.

First identify the cause and trend.

---

## 5. Storage Operations

Regularly inspect:

```bash
lsblk
df -h
pvesm status
```

Investigate:

- Unexpected disk growth
- Storage nearing capacity
- Failed storage paths
- Snapshot accumulation
- Backup growth

Avoid deleting snapshots or backup artifacts without understanding their dependency and retention role.

---

## 6. Snapshot Operations

Snapshots are useful for short-term change protection but are not a replacement for backups.

Before creating a snapshot:

- Identify the change.
- Confirm storage capacity.
- Define expected snapshot lifetime.

After the change:

- Validate the VM.
- Remove the snapshot when no longer required.

Do not keep old snapshots indefinitely.

---

## 7. Network Operations

Review:

- Bridge state
- Physical interface state
- VM connectivity
- VLAN configuration when implemented
- Firewall behavior

Current architecture uses `vmbr0` as the reference VM bridge.

VLAN segmentation remains Planned until implemented and validated.

---

## 8. Administrative Access

Use the minimum required administrative privilege.

Review:

- Proxmox accounts
- Roles
- API tokens where used
- SSH access
- Management network exposure

Do not share administrative credentials.

---

## 9. Update Operations

Follow this sequence:

```text
Review available updates
        ↓
Check impact
        ↓
Confirm backup/recovery path
        ↓
Apply update
        ↓
Reboot if required
        ↓
Validate host
        ↓
Validate important VMs
```

Avoid performing a major platform update during an active incident unless required for recovery.

---

## 10. Backup Operations

Before significant changes, confirm that the affected VM has a usable recovery path.

When backup is implemented, verify:

- Job completed
- Backup artifact exists
- Storage is available
- Retention is working
- Restore procedure is known

A successful backup job should not automatically be interpreted as a successful restore.

---

## 11. Configuration Change Procedure

For significant Proxmox changes:

1. Record the reason.
2. Identify affected VMs.
3. Determine rollback.
4. Create a backup/snapshot if appropriate.
5. Make one logical change at a time.
6. Validate.
7. Record evidence.
8. Update documentation.

Avoid undocumented changes directly in production-like configuration.

---

## 12. Routine VM Provisioning

When creating a new VM:

1. Use the VM naming convention.
2. Follow the two-disk standard.
3. Apply reference CPU/RAM values.
4. Configure VirtIO networking.
5. Configure UEFI/OVMF where required.
6. Enable QEMU Guest Agent.
7. Assign the intended network.
8. Record the VM ID.
9. Install the OS.
10. Complete Day 1 validation before operational handover.

---

## 13. Failed VM Procedure

If a VM is unexpectedly unavailable:

1. Confirm host health.
2. Confirm VM state.
3. Check recent changes.
4. Check storage.
5. Check network.
6. Review guest/host logs.
7. Attempt graceful recovery where safe.
8. Restore from backup if required.
9. Validate dependencies.
10. Record the incident.

Do not repeatedly reboot without collecting evidence.

---

## 14. Capacity Review

Track trends rather than only current values.

Important signals:

- Host memory pressure
- CPU contention
- Storage utilization
- VM growth
- Backup storage growth

The current host has finite resources. Capacity decisions should consider the entire lab, not one VM in isolation.

---

## 15. Evidence

For significant operations record:

```text
Date:
Operator:
VM/node:
Change or operation:
Reason:
Before state:
Action:
After state:
Validation:
Rollback:
Notes:
```

Do not record secrets.

---

## 16. Operational Completion Criteria

This runbook is considered operationally mature when:

- Routine health checks are executed.
- VM lifecycle procedures are repeatable.
- Storage is reviewed.
- Updates follow a controlled process.
- Backup and restore procedures are tested.
- Administrative access is reviewed.
- Significant changes have evidence.
- Common failure modes have recovery procedures.

## Related Documentation

- [`../transition.md`](../transition.md)
- [`../documentation-standard.md`](../documentation-standard.md)
- [`../../day-1/proxmox/installation.md`](../../day-1/proxmox/installation.md)
- [`../../day-1/proxmox/configuration.md`](../../day-1/proxmox/configuration.md)
- [`../../day-1/proxmox/validation.md`](../../day-1/proxmox/validation.md)
- [`../backup/strategy.md`](../backup/strategy.md)
- [`../backup/restore-test.md`](../backup/restore-test.md)
