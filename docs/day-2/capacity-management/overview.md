# Capacity Management

> **Day 2 — Capacity**

## Status

**Documented / Planned.** Capacity-management requirements are defined. Historical trend collection is not yet implemented as a centralized capability.

## 1. Objective

Ensure the lab has enough CPU, memory, storage and network capacity for current workloads and planned growth.

## 2. Capacity Domains

| Domain | Primary concern |
|---|---|
| CPU | Contention and sustained saturation |
| Memory | Pressure, swapping and allocation |
| Storage | Capacity, growth and I/O |
| Network | Link saturation and errors |
| Backup | Backup-storage growth |

## 3. Current Host Constraint

The current reference host has finite resources. Capacity decisions must consider the total VM estate rather than optimizing a single workload in isolation.

## 4. Review Method

```text
Current utilization
        ↓
Historical trend
        ↓
Growth rate
        ↓
Planned workload
        ↓
Capacity decision
```

## 5. Proxmox Review

Review:

- node CPU;
- memory allocation and utilization;
- storage utilization;
- VM resource consumption;
- unexpected growth;
- backup storage when implemented.

## 6. Capacity Actions

Possible actions:

- right-size a VM;
- remove obsolete resources;
- expand storage;
- redistribute workloads;
- delay a planned deployment;
- add physical capacity.

Resource increases should be based on evidence rather than guesswork.

## 7. Thresholds

Exact thresholds should be established after sufficient baseline data exists.

Avoid treating a single instantaneous value as a capacity incident unless it causes service impact.

## 8. Evidence

```text
Review date:
Resource:
Current state:
Trend:
Expected growth:
Risk:
Decision:
Action:
Review date:
```

## 9. Completion Criteria

Capacity management becomes operationally mature when resource trends are collected, risks are identified before exhaustion, and resource changes are tied to documented evidence.
