# Security Validation and Evidence

## Status
**Validation framework.**

Security documentation is not evidence that a control works. A control is **Validated** only after the test has been executed and evidence recorded.

## Test Record
Record test ID, date, component, control, objective, precondition, procedure, expected result, actual result, PASS/FAIL/N/A, evidence location, and known deviation.

## Minimum Tests
### Network
- Unauthorized inter-VLAN connection denied
- Required application-to-database connection succeeds
- Management access restricted
- Unapproved WAN management denied

### Identity
- Authorized identity authenticates
- Unauthorized identity is denied
- Privilege policy matches group membership
- Break-glass access is controlled

### PostgreSQL
- Application role has only intended database/schema access
- Application does not use a superuser
- Unauthorized source is rejected
- Unauthorized database role is rejected

### Docker
- Unauthorized users cannot obtain Docker administrative control
- Unnecessary host ports are absent
- Container privileges are reviewed
- Persistent data survives container recreation

### Secrets
- Repository contains no real credentials
- Scanner detects a synthetic test secret
- Pre-commit blocks a synthetic test secret
- CI blocks a synthetic test secret

### Supply Chain
- SBOM generation succeeds
- Dependency review runs
- Container versions/digests are recorded
- Security advisories are reviewed before material upgrades

## Evidence Location
Use docs/security/evidence/ for non-sensitive evidence. Never commit passwords, tokens, private keys, cookies, personal data, or sensitive logs.

## Status Rules
- Planned — designed but not tested
- Implemented — configured
- Validated — configured and evidence exists
- Failed — test executed and expected control did not pass
- N/A — not applicable with documented reason
