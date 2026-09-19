# ADR 0006: OpenBao for Secrets Management

## Status
**Accepted**

## Context
Centralized secret storage supports Zero Plaintext, least privilege, rotation, and controlled service access.

## Decision
Use OpenBao as the planned centralized secrets-management platform.

## Consequences
### Positive
- Clear architectural boundary.
- Easier documentation and validation.
- Appropriate for the current modest-hardware lab.

### Trade-offs
- The chosen model may require integration work.
- The current design does not attempt production-scale availability.

## Implementation Note
Secrets must not be committed to Git regardless of OpenBao implementation status.

## Related Documentation
- [Architecture Overview](../architecture/overview.md)
- [Security Architecture](../security/security.md)
