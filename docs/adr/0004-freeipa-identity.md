# ADR 0004: FreeIPA for Infrastructure Identity

## Status
**Accepted**

## Context
FreeIPA integrates identity, authentication, DNS, certificates, and Linux administration concepts in a FOSS platform.

## Decision
Use FreeIPA as the planned infrastructure identity and Kerberos/LDAP platform.

## Consequences
### Positive
- Clear architectural boundary.
- Easier documentation and validation.
- Appropriate for the current modest-hardware lab.

### Trade-offs
- The chosen model may require integration work.
- The current design does not attempt production-scale availability.

## Implementation Note
Application SSO remains a separate concern handled by Keycloak.

## Related Documentation
- [Architecture Overview](../architecture/overview.md)
- [Security Architecture](../security/security.md)
