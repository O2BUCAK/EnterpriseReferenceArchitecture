# Incident Management Process

> **Day 2 — Incident Management**

## Status

**Documented.** The incident process is defined for future operational use. No claim is made that a formal incident-management process is currently active.

## 1. Objective

Restore normal service safely while preserving enough evidence to understand the cause and prevent recurrence.

## 2. Incident Lifecycle

```text
Detect
  ↓
Triage
  ↓
Contain
  ↓
Recover
  ↓
Validate
  ↓
Document
  ↓
Improve
```

## 3. Triage

Determine:

- affected system;
- service impact;
- scope;
- severity;
- recent changes;
- immediate safety concerns.

## 4. Proxmox Incident

Initial checks:

1. Is the node reachable?
2. Are Proxmox services healthy?
3. Is storage available?
4. Are affected VMs running?
5. Is the network operational?
6. Did a recent change precede the incident?

## 5. OPNsense Incident

Initial checks:

1. Is `fw01` reachable?
2. Are interfaces operational?
3. Is the gateway available?
4. Is traffic being blocked unexpectedly?
5. Are DNS/DHCP services affected?
6. Was a firewall/NAT/configuration change recently made?

## 6. Containment

Containment must minimize further impact without creating an uncontrolled configuration state.

Examples include:

- isolating a failed VM;
- reverting a known-bad configuration change;
- restricting affected traffic;
- restoring a known-good configuration.

## 7. Recovery

Use the least destructive recovery option that reliably restores service.

Potential recovery mechanisms:

- service restart;
- VM restart;
- configuration rollback;
- backup restore;
- rebuilding a failed component.

## 8. Validation

After recovery verify:

- service availability;
- network connectivity;
- expected application behavior;
- security controls;
- persistence after restart where relevant.

## 9. Incident Record

```text
Incident ID:
Date/time:
Affected component:
Impact:
Detection:
Root cause:
Containment:
Recovery:
Validation:
Follow-up:
Documentation updated:
```

## 10. Post-Incident Improvement

A resolved incident should be reviewed for:

- missing monitoring;
- missing backup/recovery capability;
- documentation gaps;
- configuration weaknesses;
- repeatability of the failure.
