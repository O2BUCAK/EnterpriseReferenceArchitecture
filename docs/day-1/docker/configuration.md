# Docker / Application Platform — Configuration

> **Day 1 — Configure & Secure**

This document defines the target configuration baseline for the Docker application platform on `app01`.

## Status

**Planned.** Docker and the target application stack are not currently implemented in the laboratory.

---

## 1. Configuration Objectives

The platform should provide:

- Predictable container lifecycle
- Persistent application data
- Network isolation
- Controlled service exposure
- Least-privilege container execution
- Reproducible deployments
- Health-aware operations
- Secure administration
- Backup/recovery readiness

---

## 2. Host Baseline

Reference:

```text
Host:      app01
VLAN:      40 — Application
CPU:       4 vCPU
RAM:       10 GiB
OS disk:   20 GiB
Data disk: 50 GiB
```

These values describe the target VM and are not implementation evidence.

---

## 3. Docker Daemon Configuration

Configure Docker according to the supported installation and operational requirements of the selected Ubuntu release.

Document important daemon settings such as:

- Data root
- Logging driver
- Log rotation
- Registry configuration
- DNS behavior where customized
- Network defaults where customized
- Resource-related settings

Do not change daemon defaults without recording the reason.

---

## 4. Docker Data Root

Container persistent state should reside on the second disk where the final storage design permits.

Target concept:

```text
OS disk
└── Ubuntu

Data disk
└── Docker/application persistent state
```

The exact Docker data root must be determined during implementation and recorded as evidence.

---

## 5. Persistent Storage

Separate ephemeral container layers from persistent application data.

Prefer explicit volumes or bind mounts for stateful services.

For each stateful service document:

```text
Service:
Volume/bind mount:
Host path:
Container path:
Backup requirement:
Restore procedure:
```

A container image is not a backup of application state.

---

## 6. Compose Project Standard

Use a consistent structure for application stacks.

Reference:

```text
services/<application>/
├── compose.yaml
├── README.md
├── .env.example
├── config/
└── data/
```

Do not commit `.env` files containing real credentials.

The README for each stack should explain dependencies, ports, storage, networks, backup, and recovery.

---

## 7. Image Versioning

Do not use an undocumented floating image tag for critical services where reproducibility matters.

For each service record:

```text
Image:
Version/tag:
Digest:
Source registry:
Release date:
Upgrade procedure:
Rollback procedure:
```

Use a deliberate update policy rather than automatically pulling arbitrary latest images.

---

## 8. Container Network Model

Use separate Docker networks according to application dependencies.

Reference:

```text
                     Nginx
                       |
                 frontend network
                       |
              +--------+--------+
              |                 |
         application        management
              |
         backend network
              |
          external DB
```

A container should join only the networks it requires.

Avoid a single flat Docker network for all services.

---

## 9. Network Exposure

Container ports should not be published to the host unless required.

Prefer:

```text
Client
  ↓
OPNsense
  ↓
Nginx
  ↓
Internal container network
  ↓
Application
```

instead of:

```text
Client → every application container
```

Document every host-published port.

---

## 10. Reverse Proxy Configuration

Nginx is the planned common HTTP entry point.

For each proxied application document:

```text
Hostname:
Listener:
Upstream:
Protocol:
TLS:
Authentication:
Allowed source networks:
```

Do not expose an application's administrative port simply because the reverse proxy exists.

---

## 11. TLS

External and internal HTTP services should use a documented TLS strategy.

The final implementation may use certificates issued by the selected internal certificate authority or another trusted mechanism.

Document:

- Certificate issuer
- SANs
- Renewal process
- Trust chain
- Minimum TLS policy
- Private-key storage

Never commit private keys.

---

## 12. Portainer

Portainer is planned as a container management interface.

If implemented, treat it as a privileged management application.

Access should be restricted to the Management VLAN or another explicitly trusted administrative path.

Portainer must not bypass:

- Network security policy
- Host privilege controls
- Change management
- Audit requirements

---

## 13. Teleport CE

Teleport CE is a planned access/security component.

If implemented, its placement and exposure must be documented separately from the base Docker host.

Access policy should define:

- Administrative entry point
- Identity source
- Target hosts
- Allowed protocols
- Session/audit requirements

It remains **Planned** until deployed and validated.

---

## 14. Keycloak

Keycloak is planned as an application identity/integration component.

If deployed, it should be treated as an identity dependency rather than a generic application container.

Document:

- Realm model
- Client registration
- Authentication flows
- Admin access
- Database dependency
- TLS
- Backup

Keycloak must not be described as the existing identity provider until it is implemented and validated.

---

## 15. OpenBao

OpenBao is planned as the secrets-management layer.

The target dependency is:

```text
Application
    ↓
Secret retrieval
    ↓
OpenBao
```

Until OpenBao is implemented, application credentials must use another secure mechanism appropriate to the lab.

Never replace secure secret handling with plaintext configuration for convenience.

---

## 16. NetBox

NetBox is planned for network/IPAM/DCIM documentation and inventory.

It should become the authoritative source for the lab's network inventory once implemented and populated.

Avoid creating conflicting manually maintained IPAM records without documenting the source of truth.

---

## 17. Forgejo and Woodpecker CI

Forgejo is planned as the Git service and Woodpecker CI as the CI/CD platform.

Target concept:

```text
Developer
   ↓
Forgejo
   ↓
Woodpecker CI
   ↓
Build / Test
   ↓
Deployment
```

CI runners must receive only the privileges required for their jobs.

Do not connect CI runners to sensitive management networks without a documented requirement.

---

## 18. Wiki.js

Wiki.js is planned as an operational/documentation platform.

It should consume the same documentation standards used throughout the project and should not become the only copy of critical recovery procedures.

Critical runbooks must remain recoverable independently of the Wiki.js service.

---

## 19. Project Pulp

Project Pulp is planned as a repository/content management component.

Its deployment should be evaluated based on actual repository-management requirements and storage capacity.

Do not allocate large persistent storage without a documented content-retention requirement.

---

## 20. Squid

Squid is a planned proxy/gateway component.

If implemented, its traffic path must be explicitly documented so that it does not unintentionally become an unrestricted egress path around OPNsense policy.

---

## 21. Container Privileges

Avoid privileged containers unless absolutely required.

Review:

- `privileged`
- Host networking
- Host PID/IPC namespaces
- Host filesystem mounts
- Device mappings
- Linux capabilities
- User identity

Remove unnecessary capabilities and host mounts.

---

## 22. Container Users

Where supported, run application processes as non-root users.

Document exceptions for applications that require elevated privileges.

The container's internal user model does not replace host-level security controls.

---

## 23. Resource Controls

The `app01` VM has a finite 10 GiB reference memory allocation.

For each significant service document expected resource usage.

Where supported, configure:

- Memory limits
- CPU limits
- Restart policy
- Health check

Avoid allowing one application to consume all host resources.

---

## 24. Health Checks

Every important service should have a meaningful health check where supported.

Distinguish:

```text
Container running
≠
Application healthy
≠
Application dependency healthy
```

Document the health endpoint or command for each deployed service.

---

## 25. Logging

Configure container log rotation to prevent uncontrolled disk consumption.

For each application determine:

```text
Log source:
Driver:
Rotation:
Retention:
Centralization:
Sensitive-data handling:
```

Centralized observability remains a planned architecture capability unless separately implemented.

---

## 26. Backup and Recovery

For every stateful container document:

- Data locations
- Configuration locations
- Database dependency
- Backup method
- Backup frequency
- Retention
- Restore procedure
- Restore validation

For stateless services, document how configuration and images can recreate the service.

---

## 27. Update Strategy

Application updates should follow a controlled process:

```text
Review release
    ↓
Check compatibility
    ↓
Backup state
    ↓
Pull selected version
    ↓
Deploy/update
    ↓
Health check
    ↓
Functional validation
    ↓
Rollback if required
```

Do not automatically upgrade every application merely because a new image exists.

---

## 28. Security Baseline

Minimum target baseline:

- Host management restricted
- Docker administration restricted
- No unnecessary published ports
- No unnecessary privileged containers
- Trusted image sources
- Documented image versions
- Persistent data on intended storage
- Network segmentation
- TLS where required
- Secrets external to Git
- Resource limits where appropriate
- Health checks
- Logging and rotation
- Backup/recovery plan

---

## 29. Configuration Evidence

Record actual deployed values:

```text
Docker version:
Compose version:
Docker data root:
Data filesystem:
Published ports:
Docker networks:
Running services:
Image versions:
Resource limits:
Health checks:
Reverse proxy:
TLS:
Backup method:
Known deviations:
```

Do not publish secrets or private keys.

---

## 30. Configuration Completion Criteria

The Docker/application platform configuration is complete for Day 1 when:

1. Host networking is correct.
2. Docker storage is correctly placed.
3. Administration is restricted.
4. Container networks are intentionally designed.
5. Published ports are documented.
6. Persistent storage is defined.
7. Image/version policy is documented.
8. Reverse proxy behavior is defined.
9. Security controls are applied.
10. Resource and health policies are defined where appropriate.
11. Backup/recovery requirements are documented.
12. Validation passes.
13. Evidence is recorded.

## Related Documentation

- [`installation.md`](installation.md) — Docker/application platform installation
- [`validation.md`](validation.md) — Docker/application platform validation
- [`../network/segmentation.md`](../network/segmentation.md) — Network segmentation
- [`../network/validation.md`](../network/validation.md) — Network validation
- [`../postgresql/configuration.md`](../postgresql/configuration.md) — PostgreSQL configuration
- [`../../architecture/application-platform.md`](../../architecture/application-platform.md) — Application platform architecture
- [`../../security/security.md`](../../security/security.md) — Security architecture
- [`../documentation-standard.md`](../documentation-standard.md) — Day 1 documentation standard
