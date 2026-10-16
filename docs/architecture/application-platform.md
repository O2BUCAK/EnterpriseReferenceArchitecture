# Application Platform Architecture

## Status

**Planned.** The Docker application platform has not yet been implemented in the laboratory. This document describes the target design and does not claim deployment or validation.

## Purpose

Provide a FOSS-first application runtime on `app01`, with controlled ingress, explicit network boundaries, persistent application data, and dedicated database services.

## Logical Flow

```text
Client
  |
  v
OPNsense / network policy
  |
  v
Nginx reverse proxy (planned)
  |
  v
Application containers on app01
  |
  +----> PostgreSQL on db01 (only for applications requiring it)
  |
  +----> Redis on db01 (only for approved cache/session use cases)
```

The diagram describes intended traffic flow, not currently active connectivity.

## Responsibilities

- **OPNsense:** route and filter traffic between network segments.
- **Nginx:** planned HTTP(S) ingress and reverse proxy for explicitly published applications.
- **Docker Engine / Compose:** run application workloads on `app01`.
- **PostgreSQL:** provide database services on `db01`; applications use dedicated least-privileged database roles rather than a database superuser.
- **Redis:** provide cache or session services only where an application has a documented requirement.
- **OpenBao:** planned secret-management integration; credentials must not be committed to Git or embedded in images.

## Network and Exposure Rules

- Publish only explicitly approved ingress ports.
- Do not expose database or cache ports to untrusted networks.
- Permit application-to-database/cache traffic only from documented source segments and required ports.
- Restrict administrative interfaces to the management network.
- Keep container networks and host-published ports aligned with the repository port map and firewall rules.

## Storage and Configuration

- Keep persistent application data on the designated application data disk.
- Store non-sensitive deployment configuration in version control.
- Keep real secrets outside the repository and retrieve them through the approved secret-management approach when implemented.
- Record deployed image versions and immutable digests where practical.

## Security and Operations

Before a workload is considered validated, record evidence for:
- image provenance and version;
- required ports and network reachability;
- container privileges and host mounts;
- persistent-data behavior;
- application health and dependency connectivity;
- TLS and ingress behavior where applicable;
- resource usage and logs;
- backup/restore only when that capability is within the current implementation scope.

Backup and disaster recovery remain outside the current hardware-constrained validation scope unless explicitly brought into scope later.

## Related Documentation

- [Architecture overview](overview.md)
- [Dependency graph](dependency-graph.md)
- [Network architecture](../network/network.md)
- [Port map](../network/port-map.md)
- [Docker installation](../day-1/docker/installation.md)
- [Docker configuration](../day-1/docker/configuration.md)
- [Docker validation](../day-1/docker/validation.md)
- [Secrets management](../security/secrets-management.md)
