# Troubleshooting Methodology

> **Day 2 — Troubleshooting**

## Status

**Documented.** This is the common troubleshooting methodology. Component-specific procedures remain in their respective runbooks.

## 1. Core Principle

Troubleshooting should move from observation to evidence, not from symptom directly to configuration changes.

```text
Observe
  ↓
Define the symptom
  ↓
Identify scope
  ↓
Check dependencies
  ↓
Collect evidence
  ↓
Form a hypothesis
  ↓
Test one change
  ↓
Validate
  ↓
Document
```

## 2. Define the Symptom

Record:

- what is failing;
- when it started;
- who/what is affected;
- whether the failure is continuous or intermittent;
- what changed immediately before the failure.

## 3. Establish Scope

Determine whether the problem is:

- one VM;
- multiple VMs;
- the hypervisor;
- the firewall;
- the network;
- storage;
- an external dependency.

## 4. Check Dependencies

Use a dependency chain:

```text
Physical host
    ↓
Proxmox
    ↓
VM
    ↓
OS
    ↓
Network
    ↓
Service
    ↓
Application
```

Do not troubleshoot an application before confirming that its underlying VM and network are healthy.

## 5. Evidence Sources

Use appropriate evidence such as:

- service status;
- system logs;
- Proxmox task history;
- firewall logs;
- interface state;
- DNS results;
- routing state;
- resource utilization;
- recent configuration changes.

## 6. Change Discipline

During troubleshooting:

- make one logical change at a time;
- record the original state;
- know the rollback before changing configuration;
- avoid destructive actions until evidence supports them.

## 7. Validate the Fix

A fix is not complete when the error disappears from the screen.

Validate:

- intended functionality;
- dependent services;
- security boundaries;
- persistence after restart when relevant.

## 8. Close the Incident

Record:

```text
Symptom:
Root cause:
Evidence:
Resolution:
Validation:
Preventive action:
Documentation updated:
```

## 9. Common Lab Boundaries

### Proxmox

Start with host, VM state, storage and network before investigating the guest application.

### OPNsense

Start with interface and gateway state, then routing/NAT, then firewall rules, then DNS/DHCP where applicable.

### Planned Components

FreeIPA, PostgreSQL, Docker and automation components should use the same layered methodology after they are implemented.
