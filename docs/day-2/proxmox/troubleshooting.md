# Proxmox VE — Troubleshooting Runbook

> **Day 2 — Troubleshooting**

## Status

**Documented.** These scenarios are defined for the implemented Proxmox platform. They are not evidence that each failure scenario has been deliberately reproduced in the lab.

## 1. Troubleshooting Order

```text
Host
 ↓
Proxmox services
 ↓
Storage
 ↓
Network
 ↓
VM state
 ↓
Guest OS
 ↓
Application
```

Collect evidence before making changes.

## 2. Proxmox Web UI Unavailable

1. Confirm host network reachability.
2. Check `pveproxy` and `pvedaemon`.
3. Check system resources.
4. Check failed systemd units.
5. Review recent changes and logs.
6. Restore the management service only after identifying the likely cause.
7. Validate web access and VM operation.

Useful checks:

```bash
systemctl status pveproxy
systemctl status pvedaemon
systemctl --failed
ss -lntp
```

## 3. VM Will Not Start

Check in order:

1. VM configuration.
2. Required storage.
3. Disk availability.
4. Network device configuration.
5. Recent task errors.
6. Host resource availability.

Do not repeatedly start a failing VM without examining the task error.

## 4. VM Suddenly Stops

Determine whether the stop was:

- administrative;
- guest-initiated;
- resource-related;
- storage-related;
- host-related;
- caused by an external failure.

Review Proxmox task history and host logs before restarting.

## 5. Storage Nearing Capacity

1. Confirm which storage is affected.
2. Check filesystem utilization.
3. Identify large VM disks, snapshots or backup artifacts.
4. Check recent growth.
5. Remove only known-obsolete data according to retention rules.
6. Expand storage or redistribute workloads if required.
7. Validate affected VMs.

Never delete unknown files simply to recover free space.

## 6. Network Connectivity Failure

Use the dependency chain:

```text
Physical NIC
 ↓
Proxmox bridge
 ↓
VM NIC
 ↓
OPNsense
 ↓
Gateway
 ↓
Destination
```

Check one layer at a time. VLAN-specific troubleshooting applies only after VLAN segmentation is implemented.

## 7. Host Resource Exhaustion

If CPU or memory pressure is sustained:

1. Identify the consuming VM/process.
2. Determine whether the behavior is expected.
3. Check for recent changes.
4. Check for runaway workloads.
5. Reduce unnecessary load where safe.
6. Right-size or redistribute workloads based on evidence.

Do not increase every VM's resources as the first response.

## 8. Time Synchronization Failure

Check:

```bash
timedatectl
systemctl status chrony
```

Verify:

- configured time source;
- network reachability;
- service state;
- system clock;
- effect on dependent services.

Time synchronization is an infrastructure dependency, not merely a cosmetic setting.

## 9. Recovery Decision

Use the least destructive option that restores service reliably:

```text
Service restart
    ↓
VM restart
    ↓
Configuration rollback
    ↓
Backup restore
    ↓
Rebuild
```

The appropriate level depends on evidence and impact.

## 10. Validation After Recovery

Validate:

- Proxmox management;
- affected VM state;
- storage;
- network;
- guest OS;
- required service;
- security controls;
- persistence after restart when relevant.

## 11. Evidence

```text
Incident:
Timestamp:
Symptom:
Scope:
Evidence:
Hypothesis:
Action:
Result:
Root cause:
Recovery:
Preventive action:
```

## Related Documentation

- [`operations.md`](operations.md)
- [`monitoring.md`](monitoring.md)
- [`backup-recovery.md`](backup-recovery.md)
- [`../troubleshooting/methodology.md`](../troubleshooting/methodology.md)
- [`../incident-management/process.md`](../incident-management/process.md)
