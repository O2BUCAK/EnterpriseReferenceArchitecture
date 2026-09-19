# ADR 0002: Network Segmentation

## Status
**Accepted**

## Context
Segmentation reduces unnecessary lateral communication and makes least-privilege firewall policy explicit.

## Decision
Separate management, identity, database, and application workloads into dedicated network segments.

## Consequences
### Positive
- Clear architectural boundary.
- Easier documentation and validation.
- Appropriate for the current modest-hardware lab.

### Trade-offs
- The chosen model may require integration work.
- The current design does not attempt production-scale availability.

## Implementation Note
OPNsense is the primary inter-VLAN enforcement point; Docker networks provide an additional application-layer boundary.

## Related Documentation
- [Architecture Overview](../architecture/overview.md)
- [Security Architecture](../security/security.md)
