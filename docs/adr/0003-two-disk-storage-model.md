# ADR 0003: Two-Disk Linux Storage Model

## Status
**Accepted**

## Context
This provides predictable VM deployment, storage separation, and simple expansion while respecting modest lab hardware.

## Decision
Use Disk 1 for the operating system and Disk 2 for /var, /home, /tmp, and role-specific persistent data.

## Consequences
### Positive
- Clear architectural boundary.
- Easier documentation and validation.
- Appropriate for the current modest-hardware lab.

### Trade-offs
- The chosen model may require integration work.
- The current design does not attempt production-scale availability.

## Implementation Note
LVM is used for flexible logical-volume allocation.

## Related Documentation
- [Architecture Overview](../architecture/overview.md)
- [Security Architecture](../security/security.md)
