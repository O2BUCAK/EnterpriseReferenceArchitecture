# OpenTofu

## Status
**Planned.**

This directory reserves the future location for OpenTofu infrastructure code. It does not claim that infrastructure is currently provisioned by this directory.

When implementation begins:
- Pin provider/module versions.
- Protect state because it may contain sensitive values.
- Keep state outside the public repository unless explicitly proven safe.
- Run tofu fmt -check and tofu validate in CI.
- Run secret and IaC security scanning.
- Require reviewed pull requests for material infrastructure changes.
