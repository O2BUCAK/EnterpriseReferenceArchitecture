# Git Governance

## Status
**Planned control.** Repository administration settings must enforce the target rules below.

## Protected main
Target controls:
- Pull request required for changes to main
- Required CI status checks
- Force-push disabled
- Branch deletion disabled
- Direct pushes restricted
- Signed commits preferred and, when practical, required
- CODEOWNERS review for security-sensitive paths

## Pull Request Gate
A change should pass documentation validation, secret scanning, dependency review, SBOM generation where applicable, IaC validation where applicable, and security tests where applicable.

## Commit Signing
The project prefers verified SSH or GPG signed commits. A signed commit proves control of the signing key; it does not prove that the code is secure or correct.

## Repository Ruleset
Recommended main ruleset:
- Require pull request
- Require required CI checks
- Require conversation resolution
- Block force pushes
- Block branch deletion
- Restrict bypass permissions
- Require signed commits when practical

The GitHub ruleset is repository-hosting configuration and must be enabled in repository settings.
