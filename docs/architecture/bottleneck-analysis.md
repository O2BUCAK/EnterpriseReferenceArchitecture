# Bottleneck Analysis

> Enterprise Reference Architecture — Performance & Capacity Methodology

## Purpose

A bottleneck is a resource or dependency that limits the observed performance, throughput, or stability of a workload.

Bottleneck analysis should be evidence-driven. A high utilization value alone does not establish a bottleneck unless it correlates with service impact or degraded workload performance.

## Analysis Flow

```text
Observed symptom
      ↓
Define affected workload
      ↓
Measure baseline
      ↓
Check dependency chain
      ↓
Identify constrained resource
      ↓
Correlate with service impact
      ↓
Test hypothesis
      ↓
Choose remediation
      ↓
Validate again
```

## Bottleneck Domains

| Domain | Typical indicators |
|---|---|
| CPU | sustained saturation, CPU ready/steal, run queue |
| Memory | pressure, swap, reclaim, allocation failure |
| Storage | latency, IOPS pressure, throughput, queue depth |
| Network | packet loss, errors, saturation, latency |
| Database | slow queries, locks, connection pressure, I/O |
| Cache | low hit rate, eviction pressure, memory pressure |
| Application | worker exhaustion, thread/connection pools, queueing |
| Dependency | upstream latency, timeouts, unavailable service |

## Important Rule

Do not jump directly from:

```text
High utilization → bottleneck
```

Use:

```text
Measurement
   +
Workload impact
   +
Correlation
   +
Repeatable observation
   =
Supported bottleneck hypothesis
```

## Dependency-Aware Troubleshooting

Start from the infrastructure layer and move upward:

```text
Physical Host
     ↓
Proxmox
     ↓
Network / OPNsense
     ↓
VM
     ↓
Operating System
     ↓
Identity / DNS / NTP
     ↓
Database / Cache
     ↓
Container Platform
     ↓
Application
```

The dependency graph should be checked before attributing an application symptom to the application itself.

## Bottleneck Record

For a meaningful investigation, capture:

```text
Date:
Workload:
Observed symptom:
Affected component:
Baseline:
Measurement:
Dependency path:
Hypothesis:
Test:
Result:
Root cause / supported cause:
Action:
Validation:
Follow-up:
```

## Capacity Relationship

Bottleneck analysis and capacity management are related but not identical.

- **Capacity management** asks whether available resources are sufficient for current and expected demand.
- **Bottleneck analysis** asks what is limiting the observed workload right now.

See [Capacity Management](../day-2/capacity-management/overview.md).

## Typical Example

```text
Application latency increases
        ↓
Measure application response time
        ↓
Check database latency
        ↓
Check PostgreSQL CPU / I/O / locks
        ↓
Check VM resource pressure
        ↓
Check host contention
        ↓
Compare with baseline
```

Only after the evidence supports the hypothesis should a remediation be selected.

## Remediation Categories

Depending on evidence, actions may include:

- optimize a query or application path;
- right-size a VM;
- remove unnecessary workload;
- adjust resource allocation;
- change cache behavior;
- change storage layout;
- reduce unnecessary network traffic;
- introduce asynchronous processing;
- split a workload only when the measured constraint justifies added complexity.

## Related Documentation

- [Capacity Management](../day-2/capacity-management/overview.md)
- [Dependency Graph](dependency-graph.md)
- [Troubleshooting Methodology](../day-2/troubleshooting/methodology.md)
