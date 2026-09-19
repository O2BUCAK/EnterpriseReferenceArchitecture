# ADR 0001: FOSS-First Technology Selection

## Status
**Accepted**

## Context
This aligns the project with transparency, learning value, portability, and the project's FOSS-first purpose.

## Decision
Use FOSS-first technologies for the reference architecture.

## Consequences
### Positive
- Clear architectural boundary.
- Easier documentation and validation.
- Appropriate for the current modest-hardware lab.

### Trade-offs
- The chosen model may require integration work.
- The current design does not attempt production-scale availability.

## Implementation Note
A proprietary component may still be considered when a specific requirement cannot reasonably be met by the selected FOSS stack.

## Related Documentation
- [Architecture Overview](../architecture/overview.md)
- [Security Architecture](../security/security.md)
