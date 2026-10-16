# Security Policy

## Scope
This repository contains a FOSS-first enterprise reference architecture and laboratory documentation. Security issues may affect documentation, automation, infrastructure-as-code, CI/CD workflows, or security guidance.

## Reporting a Vulnerability
Do not disclose credentials, tokens, private keys, personal data, or other sensitive material in public issues. Use GitHub's private vulnerability reporting mechanism when available. If private reporting is unavailable, open a minimal issue without sensitive details and request a private contact path.

## Secret Exposure
If a secret is accidentally committed:
1. Treat it as compromised.
2. Revoke or rotate it immediately.
3. Remove it from the working tree and repository history as appropriate.
4. Review related systems for unauthorized use.
5. Record the incident and corrective action.

Removing a secret from the latest commit is not sufficient if it existed in Git history.

## Security Controls
The repository uses or plans to use:
- Git governance and protected main
- Secret scanning
- Pre-commit checks
- CI security gates
- Dependency review
- SBOM generation
- FOSS component inventory
- Automated documentation validation
- IaC validation
- Signed commits
- Security validation evidence

Planned controls are not implementation claims until validation evidence exists.

## Supported Scope
This repository is a laboratory/reference architecture. It is not a production service and does not provide a production security support commitment.
