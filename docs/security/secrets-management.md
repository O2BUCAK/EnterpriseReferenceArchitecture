# Secrets Management

> Target secrets lifecycle for the Enterprise Reference Architecture.

## Status
**Planned architecture.** OpenBao is the selected target secrets-management platform.

## Objective
Keep credentials, tokens, private keys, and encryption material out of Git, public documentation, Compose files, screenshots, and uncontrolled configuration.

## Secret Classes
| Class | Examples | Target handling |
|---|---|---|
| Human credentials | Admin passwords | Identity / secure credential store |
| Service credentials | DB/API accounts | OpenBao |
| Tokens | API / CI tokens | OpenBao |
| Private keys | TLS/signing keys | OpenBao or tightly protected service storage |
| Bootstrap secrets | Initial credentials | Temporary, then rotate |
| Encryption material | Application keys | OpenBao / service secure storage |

## Lifecycle
```
Identify → Create → Store → Retrieve → Use → Rotate → Revoke → Retire
```

## Access Model
Use dedicated identities with least privilege:
```
svc-netbox   → netbox/*
svc-forgejo  → forgejo/*
svc-keycloak → keycloak/*
svc-ansible  → approved automation paths
```

A service must never receive unrestricted access to the complete secret store unless explicitly justified.

## Bootstrap and Break-Glass
Bootstrap credentials are temporary and must be rotated after installation. Break-glass credentials are separately protected, limited to recovery, and reviewed after use.

## Git Rules
Never commit:
- passwords
- tokens
- private keys
- real credential-bearing .env files
- unredacted secret-bearing logs

Use placeholders and .env.example.

## CI/CD
```
Forgejo → Woodpecker → approved secret mechanism → Build / Deploy
```
CI jobs receive only the secrets required for the specific job, and logs must not print secret values.

## Rotation Record
```
Secret:
Owner:
Reason:
Old credential disabled:
New credential issued:
Consumers updated:
Validation:
Completion date:
```

## Validation
A secret-control test must prove:
1. Authorized service can retrieve the required secret.
2. Unauthorized service cannot retrieve it.
3. Secret is absent from Git.
4. Secret is absent from normal logs.
5. Rotation removes or disables the old credential as intended.

## Related Documentation
- [PKI Architecture](../architecture/pki.md)
- [Identity Architecture](../architecture/identity.md)
- [Security Architecture](security.md)
- [Docker Deployment Standard](../day-1/docker/deployment-standard.md)
