# Asynchronous Architecture & Queue Decision Guide

> Enterprise Reference Architecture — Decision Guide

## Status

**Decision pending.**

The current architecture does not select a queue or message broker as a mandatory platform component.

This document defines when asynchronous processing should be introduced and what evidence is required before adding a queue.

## Why This Is Deferred

A queue introduces another shared infrastructure component, operational state, failure modes, monitoring requirements, authentication flows, retry behavior, and message lifecycle management.

For the current modest-hardware reference architecture, asynchronous processing should therefore be introduced only when a concrete workload requires it.

## Signals That May Justify a Queue

Consider asynchronous processing when one or more of these requirements are demonstrated:

- work is long-running and should not block a synchronous request;
- work can be retried independently;
- producer and consumer rates can differ significantly;
- bursts need controlled buffering;
- multiple workers should process independent jobs;
- eventual consistency is acceptable;
- external systems require decoupling;
- back-pressure is needed.

## Signals That May Not Justify a Queue

A queue may be unnecessary when:

- the workload is small and infrequent;
- synchronous processing is sufficient;
- there is only one consumer and no burst problem;
- failure handling is simple enough without a broker;
- the queue would add more operational complexity than the workload requires.

## Decision Sequence

```text
Concrete workload
      ↓
Measure duration / rate / burst behavior
      ↓
Check synchronous design
      ↓
Identify actual limitation
      ↓
Define retry + ordering + durability requirements
      ↓
Evaluate alternatives
      ↓
ADR if a shared queue is justified
```

## Required Design Questions

Before selecting a queue technology, document:

| Question | Required decision |
|---|---|
| Delivery | At-most-once, at-least-once, or other semantics |
| Ordering | Is message ordering required? |
| Durability | Must messages survive process/node restart? |
| Retry | How are failures retried? |
| Idempotency | Can consumers safely process duplicates? |
| Dead letters | What happens to repeatedly failing messages? |
| Back-pressure | How are bursts handled? |
| Retention | How long are messages retained? |
| Security | How are producers/consumers authenticated and authorized? |
| Monitoring | Which queue depth and failure metrics are required? |

## Current Position

Do **not** deploy a queue solely to make the architecture look more distributed.

A queue should enter the reference architecture only after an actual workload exposes a requirement that a simpler synchronous model cannot satisfy adequately.

When that happens, create a dedicated ADR covering the workload, alternatives, trade-offs, selected technology, and operational model.

## Related Documentation

- [Architecture Decision & Trade-off Methodology](architecture-decisions.md)
- [Bottleneck Analysis](bottleneck-analysis.md)
- [Dependency Graph](dependency-graph.md)
