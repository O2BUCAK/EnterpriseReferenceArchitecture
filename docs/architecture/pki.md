# PKI and Certificate Architecture

> Target certificate architecture for the Enterprise Reference Architecture.

## Status
**Planned architecture.** This defines the target model and is not an implementation claim.

## Purpose
Provide trusted encrypted communication while keeping private keys and certificate material outside Git and public documentation.

## Trust Model
```
Certificate Authorities
├── Internal PKI
│   ├── FreeIPA-managed services
│   └── Internal service TLS
└── Public CA / ACME
    └── Public HTTPS
```

FreeIPA integrated CA is the preferred internal PKI option when it meets the service requirement. Publicly exposed HTTPS must use a publicly trusted CA.

## Target Consumers
| Component | Certificate use |
|---|---|
| FreeIPA | Internal CA and service certificates |
| Nginx | TLS termination |
| Keycloak | HTTPS |
| Teleport | Proxy/node trust as required |
| OpenBao | API/UI TLS |
| PostgreSQL | TLS where required |
| Other applications | Internal TLS where appropriate |

## Private Key Rules
- Never commit private keys.
- Never publish real certificates containing sensitive material.
- Never store secrets in committed environment files.
- Protect service key files with service-appropriate permissions.
- Rotate and revoke compromised material.

## Lifecycle
```
Request → Issue → Deploy → Validate → Renew → Replace → Revoke / Retire
```

Certificate ownership and renewal responsibility must be documented per service.

## Naming
Internal examples use `corp.example.com`:
```
ipa01.corp.example.com
db01.corp.example.com
app01.corp.example.com
auto01.corp.example.com
```
These are documentation placeholders.

## Validation Record
```
Service:
Hostname:
Issuer:
SANs:
Validity:
Private-key location:
Renewal method:
Deployment method:
Validation:
Known deviation:
```

## Related Documentation
- [DNS Architecture](../network/dns.md)
- [Secrets Management](../security/secrets-management.md)
- [Security Architecture](../security/security.md)
- [Port Map](../network/port-map.md)
