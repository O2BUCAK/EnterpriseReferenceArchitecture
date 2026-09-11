# Day 1 — Documentation Index

Day 1 documents how each infrastructure component is **built, configured, secured, integrated, and validated**.

## Documentation Standard

See [`documentation-standard.md`](documentation-standard.md) for the common structure.

## Documentation Map

| Component | Document | Status |
|---|---|---|
| Proxmox VE | [`proxmox/installation.md`](proxmox/installation.md) | **Implemented** |
| Proxmox VE | [`proxmox/configuration.md`](proxmox/configuration.md) | **Implemented** |
| Proxmox VE | [`proxmox/validation.md`](proxmox/validation.md) | **Implemented / Validation evidence required** |
| OPNsense | [`opnsense/installation.md`](opnsense/installation.md) | **Implemented** |
| OPNsense | [`opnsense/configuration.md`](opnsense/configuration.md) | **Implemented** |
| OPNsense | [`opnsense/validation.md`](opnsense/validation.md) | **Implemented / Validation evidence required** |
| Network | [`network/segmentation.md`](network/segmentation.md) | **Planned** |
| Network | [`network/validation.md`](network/validation.md) | **Planned** |
| FreeIPA | [`freeipa/installation.md`](freeipa/installation.md) | **Planned** |
| FreeIPA | [`freeipa/configuration.md`](freeipa/configuration.md) | **Planned** |
| FreeIPA | [`freeipa/validation.md`](freeipa/validation.md) | **Planned** |
| PostgreSQL | [`postgresql/installation.md`](postgresql/installation.md) | **Planned** |
| PostgreSQL | [`postgresql/configuration.md`](postgresql/configuration.md) | **Planned** |
| PostgreSQL | [`postgresql/validation.md`](postgresql/validation.md) | **Planned** |
| Docker / Application Platform | [`docker/installation.md`](docker/installation.md) | **Planned** |
| Docker / Application Platform | [`docker/configuration.md`](docker/configuration.md) | **Planned** |
| Docker / Application Platform | [`docker/validation.md`](docker/validation.md) | **Planned** |
| Security | [`security/baseline.md`](security/baseline.md) | **Documented / Planned** |
| Validation | [`validation/day-1-checklist.md`](validation/day-1-checklist.md) | **Planned** |

## Status Convention

- **Implemented** — actually installed/configured in the lab.
- **Validated** — implemented and explicitly verified through tests with evidence.
- **Planned** — target architecture or future implementation.
- **Documented** — design/process is documented but is not necessarily implemented.
- **Future** — intentionally deferred beyond the current scope.

> Documentation does not change implementation status. A component remains Planned until it is actually built and tested in the lab.
