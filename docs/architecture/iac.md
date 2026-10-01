# Infrastructure as Code

## Status
**Planned.** The laboratory has not yet reached the Automation & IaC implementation phase.

## Scope
- OpenTofu for declarative infrastructure provisioning
- Ansible for operating-system and role configuration
- Version-controlled and reviewable changes
- Runtime secret retrieval rather than embedded credentials

## Target Repository Model
infra/tofu/ for OpenTofu and ansible/ for Ansible. The exact layout may change after first implementation.

## IaC Security Controls
- No plaintext credentials in OpenTofu, YAML, inventory, or playbooks.
- Protect state because it may contain sensitive values.
- Provider/module versions should be constrained.
- Run format and validation checks.
- Use dedicated least-privileged automation identities.
- Require reviewed pull requests for material infrastructure changes.
- Keep sensitive lab values outside public documentation.

## Future CI Gates
- OpenTofu fmt check
- OpenTofu validate
- Ansible YAML validation
- Ansible lint
- Secret scanning
- IaC security scanning

This document does not claim that IaC is implemented.
