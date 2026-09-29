# Architecture Decision & Trade-off Methodology

> Enterprise Reference Architecture — Design Methodology

## Purpose

Architecture decisions should be explicit, reviewable, and tied to project constraints.

The project uses **Architecture Decision Records (ADRs)** for durable decisions. This document defines the common decision and trade-off method used when creating or reviewing an ADR.

## Decision Flow

```text
Requirement
    ↓
Constraints
    ↓
Problem / Decision to Make
    ↓
Candidate Options
    ↓
Evaluation Criteria
    ↓
Trade-offs
    ↓
Decision
    ↓
Consequences
    ↓
Validation / Review
```

## Required Questions

Every material architecture decision should answer:

1. What problem are we solving?
2. What constraints apply?
3. What options were considered?
4. Why was the selected option chosen?
5. What trade-offs are accepted?
6. What new dependencies or risks are introduced?
7. How will the decision be validated?
8. Under what conditions should the decision be revisited?

## Evaluation Criteria

Use only criteria that matter for the specific decision. Typical criteria include:

| Criterion | Question |
|---|---|
| Functional fit | Does the option satisfy the requirement? |
| Security | Does it fit Zero Trust, Zero Plaintext and least privilege principles? |
| Complexity | How much operational and integration complexity does it add? |
| Resource cost | Is it appropriate for the available CPU, memory and storage? |
| Maintainability | Can the system be operated and troubleshot predictably? |
| Reproducibility | Can the design be documented and reproduced? |
| FOSS alignment | Does it fit the FOSS-first principle? |
| Dependency impact | Does it introduce or strengthen shared dependencies? |
| Performance | Does measured or expected workload justify it? |
| Growth path | Can it evolve when requirements change? |

Not every decision requires every criterion.

## Trade-off Rule

A trade-off is not a claim that one option is universally better.

Document:

```text
Benefit gained
vs.
Cost / risk / complexity accepted
```

Example:

> Centralized PostgreSQL creates a clear shared data layer and simplifies administration, while increasing the impact of a database-layer outage for dependent applications.

## Decision Scope

Use an ADR when a change:

- materially changes architecture;
- introduces or removes a shared dependency;
- changes a security boundary;
- changes a persistence model;
- changes a platform technology;
- changes a design constraint or operating assumption.

Routine configuration changes do not require a new ADR unless they change an architectural decision.

## Validation

After implementation, update the ADR or related evidence with:

```text
Implementation status:
Validation performed:
Observed result:
Known deviations:
Decision still valid?:
Review trigger:
```

A design decision must remain clearly separated from implementation evidence.

## Related Documentation

- [Architecture Decision Records](../adr/README.md)
- [Architecture Overview](overview.md)
- [Capacity Management](../day-2/capacity-management/overview.md)
- [Dependency Graph](dependency-graph.md)
