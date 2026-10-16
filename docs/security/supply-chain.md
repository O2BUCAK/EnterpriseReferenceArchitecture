# Software Supply Chain and FOSS Inventory

## Status
**Planned / partially implemented.**

## Objectives
Track component and upstream project, exact deployed version, license, source/package origin, security advisories, and SBOM mapping.

## Version Governance
- Prefer supported upstream releases.
- Record exact versions for deployed components.
- Avoid floating versions in reproducible deployment definitions.
- Review security advisories before upgrades.
- Document material version changes.
- Prefer immutable image digests for deployed containers.

## SBOM
CI generates an SPDX-format SBOM as a workflow artifact. An SBOM is point-in-time component evidence and does not replace vulnerability management.

## Dependency Review
Pull requests that change dependency manifests should be checked for known vulnerable dependencies.

## GitHub Actions Supply Chain
Third-party actions should be reviewed before use. Prefer immutable commit references over mutable tags where practical. Dependabot monitors action updates.

## Container Supply Chain
When containers are introduced, record image name/version, source registry, immutable digest, image SBOM, and vulnerability-scan result.

## Evidence
Recommended evidence includes SBOM artifacts, component inventory, version records, dependency-review results, image-scan results, license review, and upgrade records.
