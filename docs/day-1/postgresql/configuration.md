# PostgreSQL — Configuration

> **Day 1 — Configure & Secure**

This document defines the target configuration baseline for PostgreSQL on `db01`.

## Status

**Planned.** PostgreSQL is not currently implemented in the laboratory.

All values below are reference values or configuration principles until they are actually deployed and validated.

---

## 1. Configuration Objectives

The database configuration should provide:

- Least-privilege access
- Controlled network exposure
- Predictable storage behavior
- Secure authentication
- Appropriate connection limits
- Useful logging
- Recoverable data
- Operationally understandable defaults

---

## 2. Database Host

Reference:

```text
Host: db01
VLAN: 30 — Database
IP:   10.10.30.10
Port: 5432
```

The actual values must be recorded after implementation.

---

## 3. Configuration Files

Use the configuration locations provided by the selected PostgreSQL package and Pardus release.

Typical PostgreSQL configuration areas include:

```text
postgresql.conf
pg_hba.conf
```

Do not assume a hard-coded filesystem path across different PostgreSQL/Pardus releases. Determine the active configuration paths from the running instance.

---

## 4. Listen Address

PostgreSQL should listen only where required.

Target principle:

```text
Required application interface → listen
Unnecessary interfaces         → do not expose
```

Avoid a broad listen configuration simply to simplify initial testing.

After changing the setting, verify the active listening sockets.

---

## 5. Port

The default PostgreSQL port is:

```text
TCP 5432
```

If the port is changed, document the reason and update:

- OPNsense rules
- Host firewall rules
- Application configuration
- Monitoring
- Documentation

A non-default port is not a substitute for access control.

---

## 6. Client Authentication

`pg_hba.conf` should express the intended authentication policy explicitly.

Target concept:

```text
Connection source
      ↓
Database
      ↓
Role
      ↓
Authentication method
      ↓
Allow / Deny
```

Avoid overly broad entries such as unrestricted access from the entire network unless explicitly justified.

When remote application access is enabled, restrict the source network or host as narrowly as practical.

---

## 7. Administrative Role

The PostgreSQL superuser should be reserved for database administration.

Do not use the superuser as the application's normal connection identity.

Target:

```text
DB administration → administrative role
Application       → dedicated application role
```

Administrative credentials must remain outside GitHub.

---

## 8. Application Roles

Create a dedicated role for each application that needs PostgreSQL.

Example:

```text
app_<name>
```

Grant only the permissions required by that application.

Avoid:

```text
SUPERUSER
CREATEDB
CREATEROLE
```

unless a documented operational requirement exists.

---

## 9. Database Ownership

Where practical, application databases should have a dedicated owner rather than the global administrative account.

Conceptual model:

```text
Application DB
      |
      +-- owner: application database role
      +-- application connection role
```

Separate migration/administration privileges from runtime application privileges where the application supports it.

---

## 10. Network Security

Database access should be enforced at multiple layers:

```text
Network segmentation
       ↓
OPNsense firewall
       ↓
Host firewall where applicable
       ↓
PostgreSQL listen policy
       ↓
pg_hba.conf
       ↓
Database privileges
```

Defense in depth is intentional.

---

## 11. Target Traffic Policy

Reference policy:

| Source | Destination | Port | Policy |
|---|---|---:|---|
| Application | `db01` | 5432 | Allow when required |
| Management | `db01` | 5432 | Restricted |
| Identity | `db01` | 5432 | Deny unless required |
| Internet | `db01` | 5432 | Deny |
| Other VLANs | `db01` | 5432 | Deny |

The exact rule should be based on actual application requirements.

---

## 12. PostgreSQL Host Firewall

Where a host firewall is used, allow only the intended database service and administrative path.

The host firewall must not contradict OPNsense policy.

For example:

```text
OPNsense: Application → db01:5432 = ALLOW
Host firewall: Application → 5432   = ALLOW
PostgreSQL: application source       = ALLOW
```

All three layers should express the same intended access boundary.

---

## 13. TLS Configuration

Evaluate TLS for remote PostgreSQL connections, especially across network boundaries.

Document:

- Whether TLS is required
- Server certificate source
- CA/trust model
- Client certificate requirements if used
- Certificate renewal
- Verification policy

The goal is to avoid relying solely on network isolation as the confidentiality mechanism.

Private keys must never be stored in the repository.

---

## 14. Connection Limits

Configure connection limits based on the actual application workload.

Do not select a high value merely because the lab has available RAM.

Document:

```text
max_connections:
Expected application connections:
Administrative reserve:
Connection pooling:
```

If a connection pooler is introduced later, update this design accordingly.

---

## 15. Memory and Performance Baseline

The initial configuration should be conservative for the lab's 8 GiB reference VM.

Potential settings to evaluate include:

- `shared_buffers`
- `work_mem`
- `maintenance_work_mem`
- `effective_cache_size`
- checkpoint-related settings
- WAL settings

Do not apply tuning copied from large production systems without measuring the actual workload.

Configuration changes should be documented with the reason and observed result.

---

## 16. Storage Configuration

PostgreSQL data should reside on the dedicated second disk.

Target:

```text
OS disk
└── Operating system

Data disk
└── PostgreSQL data
```

Monitor:

- Capacity
- Filesystem usage
- I/O latency where available
- WAL growth
- Backup storage

Avoid filling the database filesystem to 100%.

---

## 17. WAL and Recovery

WAL is essential to PostgreSQL recovery behavior.

Document the selected recovery model and any WAL retention requirements.

At minimum, determine:

- WAL location
- Backup interaction
- Retention behavior
- Disk capacity implications
- Recovery objectives

Do not enable advanced replication/PITR features merely because they are available. Implement them when the recovery objective requires them.

---

## 18. Logging

Configure logging to support:

- Authentication troubleshooting
- Connection analysis
- Database errors
- Operational troubleshooting
- Security investigation

Avoid logging sensitive application data unnecessarily.

Define rotation and retention as part of Day 2 operations.

---

## 19. Timezone

Use an explicitly documented timezone strategy.

The system timezone and PostgreSQL timezone behavior should not be left ambiguous.

Applications should store and process timestamps consistently according to their requirements.

Document any application-specific exception.

---

## 20. Database Creation Standard

For every new application database record:

```text
Application:
Database name:
Owner:
Runtime role:
Migration role:
Required extensions:
Encoding:
Locale:
Backup policy:
Retention:
Data classification:
```

Do not create databases without identifying their owner and recovery requirements.

---

## 21. Extensions

Install PostgreSQL extensions only when required by an application or operational function.

For each extension record:

- Name
- Version
- Reason
- Security implications
- Backup/restore considerations
- Application dependency

Avoid accumulating unused extensions.

---

## 22. Secrets Management

Database credentials should not be stored in:

- Git repositories
- Public documentation
- Docker Compose files committed without secret handling
- Shell history where avoidable
- Screenshots

The future identity/secrets architecture may use dedicated services such as OpenBao, but that component is currently planned rather than implemented.

Until then, use a secure local secret-handling approach appropriate to the lab.

---

## 23. Backup Configuration

Define a backup strategy before production-like application data is introduced.

At minimum document:

```text
Backup type:
Schedule:
Destination:
Retention:
Encryption/protection:
Restore procedure:
Validation frequency:
```

Perform both logical and physical recovery planning where the workload requires it.

---

## 24. Change Procedure

For PostgreSQL configuration changes:

1. Record current configuration.
2. Identify the reason.
3. Confirm expected impact.
4. Back up relevant configuration.
5. Make one logical change.
6. Validate configuration syntax/health.
7. Restart/reload only as required.
8. Test the affected service.
9. Record the result.
10. Define rollback if the change fails.

Do not modify several unrelated parameters at once when investigating a problem.

---

## 25. Configuration Evidence

Record actual implemented settings after deployment:

```text
PostgreSQL version:
Listen addresses:
Port:
Authentication model:
Application roles:
Connection limit:
Data directory:
WAL configuration:
TLS status:
Logging configuration:
Backup method:
Firewall rule reference:
Known deviations:
```

Do not publish credentials or private keys.

---

## 26. Configuration Completion Criteria

Configuration is complete for Day 1 when:

- Network exposure is explicitly defined.
- PostgreSQL authentication is configured.
- Administrative and application roles are separated.
- Database privileges follow least privilege.
- Storage layout is correct.
- Logging is configured.
- TLS decision is documented.
- Connection/resource settings are documented.
- Backup configuration is defined.
- Firewall policy matches the database access model.
- Configuration has passed validation.
- Evidence is recorded.

## Related Documentation

- [`installation.md`](installation.md) — PostgreSQL installation
- [`validation.md`](validation.md) — PostgreSQL validation
- [`../network/segmentation.md`](../network/segmentation.md) — Network segmentation
- [`../network/validation.md`](../network/validation.md) — Network validation
- [`../../architecture/storage.md`](../../architecture/storage.md) — Storage architecture
- [`../../security/security.md`](../../security/security.md) — Security architecture
- [`../documentation-standard.md`](../documentation-standard.md) — Day 1 documentation standard
