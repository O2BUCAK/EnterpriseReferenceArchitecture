# ADR 0008: Single Application Host for Current Lab

## Status
**Accepted**

## Context
The modest hardware constraint favors operational simplicity while still demonstrating container isolation, ingress, identity, secrets, and application dependencies.

## Decision
Use a single app01 Docker host for the current reference implementation.

## Consequences
### Positive
- Clear architectural boundary.
- Easier documentation and validation.
- Appropriate for the current modest-hardware lab.

### Trade-offs
- The chosen model may require integration work.
- The current design does not attempt production-scale availability.

## Implementation Note
Workloads can be split into additional hosts later when security, performance, or availability requirements justify it.

## Related Documentation
- [Architecture Overview](../architecture/overview.md)
- [Security Architecture](../security/security.md)
