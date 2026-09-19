# ADR 0007: Centralized PostgreSQL Database Layer

## Status
**Accepted**

## Context
A dedicated database layer simplifies network policy, resource planning, administration, and dependency documentation.

## Decision
Use a dedicated PostgreSQL VM as the planned database layer instead of embedding a database inside every application deployment.

## Consequences
### Positive
- Clear architectural boundary.
- Easier documentation and validation.
- Appropriate for the current modest-hardware lab.

### Trade-offs
- The chosen model may require integration work.
- The current design does not attempt production-scale availability.

## Implementation Note
Applications access only the databases and ports they require.

## Related Documentation
- [Architecture Overview](../architecture/overview.md)
- [Security Architecture](../security/security.md)
