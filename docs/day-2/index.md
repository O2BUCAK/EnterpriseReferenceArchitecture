# Day 2 — Documentation Index

Day 2 documents how the infrastructure is **operated, monitored, maintained, secured, recovered, and improved** after deployment.

Day 2 begins with the operational handover from Day 1. See [`transition.md`](transition.md) for the transition and readiness model.

## Documentation Standard

See [`documentation-standard.md`](documentation-standard.md) for the common operational structure.

## Operational Documentation

| Operational Area | Document | Status |
|---|---|---|
| Day 1 → Day 2 Transition | [`transition.md`](transition.md) | **Documented** |
| Daily Operations | [`daily-operations/checklist.md`](daily-operations/checklist.md) | **Documented** |
| Weekly Operations | [`weekly-operations/checklist.md`](weekly-operations/checklist.md) | **Documented** |
| Monthly Operations | [`monthly-operations/checklist.md`](monthly-operations/checklist.md) | **Documented** |
| Monitoring | [`monitoring/overview.md`](monitoring/overview.md) | **Documented / Planned** |
| Patch Management | [`patch-management/process.md`](patch-management/process.md) | **Documented / Planned** |
| Backup | [`backup/strategy.md`](backup/strategy.md) | **Documented / Planned** |
| Restore | [`backup/restore-test.md`](backup/restore-test.md) | **Documented / Planned** |
| Disaster Recovery | [`disaster-recovery/overview.md`](disaster-recovery/overview.md) | **Documented / Planned** |
| Security Operations | [`security-operations/overview.md`](security-operations/overview.md) | **Documented / Planned** |
| Identity Operations | `identity-operations/overview.md` | **Planned** |
| Change Management | [`change-management/process.md`](change-management/process.md) | **Documented** |
| Incident Management | [`incident-management/process.md`](incident-management/process.md) | **Documented** |
| Capacity Management | [`capacity-management/overview.md`](capacity-management/overview.md) | **Documented / Planned** |
| Troubleshooting | [`troubleshooting/methodology.md`](troubleshooting/methodology.md) | **Documented** |
| Lifecycle Management | [`lifecycle-management/overview.md`](lifecycle-management/overview.md) | **Documented / Planned** |
| Operational Documentation | [`documentation/runbook-standard.md`](documentation/runbook-standard.md) | **Documented** |

## Component Runbooks

### Proxmox VE

| Area | Document | Status |
|---|---|---|
| Operations | [`proxmox/operations.md`](proxmox/operations.md) | **Documented** |
| Monitoring | [`proxmox/monitoring.md`](proxmox/monitoring.md) | **Documented** |
| Troubleshooting | [`proxmox/troubleshooting.md`](proxmox/troubleshooting.md) | **Documented** |
| Backup & Recovery | [`proxmox/backup-recovery.md`](proxmox/backup-recovery.md) | **Documented / Planned** |

### OPNsense

| Area | Document | Status |
|---|---|---|
| Operations | [`opnsense/operations.md`](opnsense/operations.md) | **Documented** |
| Monitoring | [`opnsense/monitoring.md`](opnsense/monitoring.md) | **Documented** |
| Troubleshooting | [`opnsense/troubleshooting.md`](opnsense/troubleshooting.md) | **Documented** |
| Backup & Recovery | [`opnsense/backup-recovery.md`](opnsense/backup-recovery.md) | **Documented / Planned** |

> **Status discipline:** A runbook being documented does not make the underlying capability Implemented or Validated. Current lab implementation remains limited to Proxmox VE and OPNsense.

## Current Operational Scope

The current lab has only Proxmox VE and OPNsense implemented. Therefore, operational procedures for FreeIPA, PostgreSQL, Docker, identity integration and automation remain future operational targets until those components are actually deployed and validated.
