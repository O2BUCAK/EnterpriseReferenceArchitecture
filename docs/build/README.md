# Build Runbooks

These documents are the reproducible installation/build layer of the Enterprise Reference Architecture.

## Build Philosophy

The build runbooks answer:

> How can someone rebuild the environment from the beginning and obtain the documented architecture?

They do not replace architecture decisions or Day-2 operational procedures.

## Build Order

| # | Document | Purpose |
|---:|---|---|
| 00 | [Prerequisites](00-prerequisites.md) | Common inputs, prerequisites and build order |
| 01 | [Proxmox](01-proxmox-installation.md) | Bare-metal hypervisor |
| 02 | [OPNsense](02-opnsense-installation.md) | Firewall and network foundation |
| 03 | [Fedora](03-fedora-installation.md) | Fedora guest for FreeIPA |
| 04 | [FreeIPA](04-freeipa-installation.md) | Identity foundation |
| 05 | [Pardus + PostgreSQL + Redis](05-pardus-postgresql-redis.md) | Database platform |
| 06 | [Ubuntu + Docker](06-ubuntu-docker.md) | Application host |
| 07 | [Application Platform](07-application-platform.md) | Common container platform |
| 08 | [Identity Integration](08-identity-integration.md) | Linux/application identity integration |
| 09 | [DNS](09-dns-implementation.md) | DNS implementation and validation |
| 10 | [Automation](10-automation-host.md) | RHEL + Ansible + OpenTofu |
| 11 | [Nextcloud](11-nextcloud.md) | Example application deployment |
| 12 | [Security Baseline](12-security-baseline.md) | Cross-platform security controls |
| 13 | [Environment Validation](13-environment-validation.md) | End-to-end acceptance |

## Status Rule

A component is not considered **Implemented** merely because a build procedure exists.

Use:

- **Planned** — design exists, implementation not completed.
- **Implemented** — installed/configured.
- **Validated** — implementation tested with evidence.
- **Future** — intentionally deferred.

## Dependency Chain

```
00 Prerequisites
      |
01 Proxmox
      |
02 OPNsense
      |
03 Fedora
      |
04 FreeIPA
      |
05 Pardus / PostgreSQL / Redis
      |
06 Ubuntu / Docker
      |
07 Application Platform
      |
08 Identity Integration
      |
09 DNS
      |
10 Automation
      |
11 Applications
      |
12 Security Baseline
      |
13 End-to-End Validation
```

## Related Documentation

- `docs/architecture/` — what the architecture is and why.
- `docs/day-1/` — component-level build/configuration reference.
- `docs/day-2/` — operation and maintenance.
- `docs/network/` — network, ports and firewall policy.
- `docs/security/` — security architecture.
- `docs/vm-design/` — VM standards and resource allocation.

## Documentation Rule

If an implementation differs from the architecture:

1. record the deviation;
2. validate the actual implementation;
3. update the appropriate architecture/design document after the decision is accepted.

Do not silently make the build runbook describe an unreviewed deviation as the intended architecture.
