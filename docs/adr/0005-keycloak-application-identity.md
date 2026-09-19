# ADR 0005: Keycloak for Application SSO

## Status
**Accepted**

## Context
Separating application SSO from infrastructure identity provides a clear trust and responsibility boundary.

## Decision
Use Keycloak as the planned application-oriented identity and SSO layer.

## Consequences
### Positive
- Clear architectural boundary.
- Easier documentation and validation.
- Appropriate for the current modest-hardware lab.

### Trade-offs
- The chosen model may require integration work.
- The current design does not attempt production-scale availability.

## Implementation Note
Applications should integrate through supported protocols such as OIDC/OAuth2 or SAML where appropriate.

## Related Documentation
- [Architecture Overview](../architecture/overview.md)
- [Security Architecture](../security/security.md)
