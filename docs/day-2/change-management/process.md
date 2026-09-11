# Change Management Process

> **Day 2 — Change Management**

## Status

**Documented.** This process defines how infrastructure changes should be planned and controlled. It is not evidence of a formal change-management system being operated in the lab.

## 1. Change Lifecycle

```text
Request
  ↓
Assess impact
  ↓
Plan
  ↓
Backup / Rollback
  ↓
Implement
  ↓
Validate
  ↓
Document
  ↓
Close
```

## 2. Change Classification

### Standard

Low-risk, repeatable and documented changes.

### Normal

Changes requiring impact assessment, validation and rollback planning.

### Emergency

Changes required to restore service or address an immediate security/availability risk.

Emergency changes should still be documented after stabilization.

## 3. Required Information

```text
Change:
Reason:
Affected component:
Risk:
Dependencies:
Maintenance window:
Backup:
Rollback:
Validation:
Expected result:
```

## 4. Proxmox Changes

Examples:

- VM resource changes
- network changes
- storage changes
- host updates
- VM creation/deletion

Use the Proxmox operations runbook and validate affected workloads afterward.

## 5. OPNsense Changes

Examples:

- firewall rules
- NAT
- interfaces
- gateway settings
- DNS/DHCP
- system updates

Before firewall changes, identify the management access path and rollback method.

## 6. Validation

A change is successful only when the intended behavior works and unintended behavior remains blocked.

For security-sensitive changes, include both positive and negative tests.

## 7. Documentation

Update architecture documentation when a change alters the intended design.

Update runbooks when a change alters an operational procedure.

Do not change an **Implemented** status unless the new state has actually been deployed and validated.
