# Disaster Recovery Overview

> **Day 2 — Recover**

## Status

**Documented / Planned.** The recovery model is defined, but a complete disaster-recovery exercise has not yet been executed in the lab.

## 1. Objective

Provide a controlled path from infrastructure failure to restored service.

## 2. Recovery Layers

```text
Physical Host
      ↓
Proxmox
      ↓
VM
      ↓
Operating System
      ↓
Network
      ↓
Service
      ↓
Application
```

Recovery should validate each required dependency rather than assuming that restoring a VM automatically restores the complete service.

## 3. Failure Scenarios

Target scenarios include:

- Proxmox host failure;
- VM failure;
- storage failure;
- OPNsense configuration failure;
- accidental VM deletion;
- network configuration error;
- corrupted service state.

## 4. Recovery Priorities

The recovery order should follow service dependencies.

For the current architecture, the firewall/network foundation is a prerequisite for dependent workloads.

Planned identity, database, application and automation services are not considered operational recovery targets until they are implemented.

## 5. Recovery Procedure

```text
Detect failure
    ↓
Assess impact
    ↓
Stabilize / contain
    ↓
Select recovery point
    ↓
Restore
    ↓
Validate infrastructure
    ↓
Validate service
    ↓
Validate security
    ↓
Document
```

## 6. Recovery Objectives

RTO/RPO values should be defined per service once the service is implemented and its business/technical importance is understood.

Do not invent recovery targets solely for documentation completeness.

## 7. Recovery Testing

Recovery capability is not considered validated until an actual recovery test demonstrates that:

- the recovery artifact is usable;
- the system can be restored;
- required services operate;
- security controls remain effective;
- the procedure is repeatable.

## 8. Evidence

```text
Scenario:
Date:
Recovery point:
Start time:
End time:
Restored system:
Validation:
Security validation:
Problems:
Lessons learned:
```

## 9. Improvement

Every recovery test should identify improvements to:

- backup;
- monitoring;
- documentation;
- automation;
- architecture;
- operational procedures.
