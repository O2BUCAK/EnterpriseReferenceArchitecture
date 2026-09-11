# Patch Management Process

> **Day 2 — Maintain**

## Status

**Documented / Planned.** The process is defined; recurring patch execution and evidence have not yet been established as an operational practice in the lab.

## 1. Objective

Apply security and maintenance updates in a controlled, reversible and validated manner.

## 2. Patch Lifecycle

```text
Identify
  ↓
Assess
  ↓
Plan
  ↓
Backup / Recovery Check
  ↓
Apply
  ↓
Validate
  ↓
Document
```

## 3. Assessment

Before patching determine:

- affected component;
- security or maintenance impact;
- dependencies;
- expected downtime;
- rollback/recovery method;
- available backup;
- validation tests.

## 4. Proxmox

For the Proxmox host:

1. Review available updates.
2. Check current host health.
3. Confirm VM recovery path.
4. Apply updates during a controlled maintenance window.
5. Reboot if required.
6. Validate Proxmox services.
7. Validate important VMs.
8. Record evidence.

## 5. OPNsense

For `fw01`:

1. Review update information.
2. Export/confirm configuration backup.
3. Check gateway and interface health.
4. Apply the update.
5. Reboot if required.
6. Validate WAN/LAN connectivity.
7. Validate firewall policy.
8. Validate DNS/DHCP where applicable.
9. Record evidence.

## 6. Linux Guests

When Linux guests are implemented:

- patch the OS according to its supported package management model;
- review service impact;
- validate networking and time synchronization;
- validate dependent services after reboot.

## 7. Rollback

Do not assume every update can be simply downgraded.

Rollback should use the documented recovery mechanism appropriate to the component, such as configuration restore, VM backup restore, package rollback where supported, or rebuilding from a known-good state.

## 8. Evidence

```text
Date:
System:
Current version:
Target version:
Reason:
Backup/recovery confirmed:
Change:
Validation:
Result:
Rollback required:
Notes:
```

## 9. Completion Criteria

A patch operation is complete only when the update is applied, the system is healthy, intended services work, and evidence is recorded.
