# PostgreSQL — Validation

> **Day 1 — Validate**

This document defines the validation procedure for PostgreSQL on `db01` after installation and configuration.

## Status

**Planned.** PostgreSQL is not currently implemented in the laboratory. Test results become project evidence only after the procedures are executed against the actual deployment.

---

## 1. Validation Principle

PostgreSQL validation must prove more than service startup.

```text
Host
 ↓
Storage
 ↓
PostgreSQL service
 ↓
Authentication
 ↓
Authorization
 ↓
Network access
 ↓
Application connection
 ↓
Backup / recovery
```

A green systemd service is not sufficient evidence that the database platform is operational.

---

## 2. Prerequisites

Confirm:

- `db01` is running.
- OS installation is complete.
- Database storage is mounted.
- DNS is functional.
- NTP is synchronized.
- PostgreSQL is installed.
- Current configuration is backed up where appropriate.
- A controlled test client exists.
- An application test client will be available once `app01` is implemented.

---

## 3. Host Validation

Verify:

```bash
hostnamectl
hostname --fqdn
ip address
ip route
```

Expected:

- Correct hostname
- Correct FQDN
- Correct database VLAN address
- Correct default gateway

Record actual values in the evidence log.

---

## 4. Storage Validation

Verify the two-disk model.

```bash
lsblk
df -h
mount
```

Confirm:

- OS disk contains the operating system.
- Database data resides on the intended second disk/filesystem.
- The PostgreSQL service account owns required files.
- Free capacity is sufficient.

### Pass Criteria

Database storage is persistent, mounted correctly, writable by PostgreSQL, and has sufficient free space.

---

## 5. NTP Validation

Check:

```bash
timedatectl
chronyc tracking
chronyc sources -v
```

### Pass Criteria

The system clock is synchronized against the intended NTP source.

---

## 6. PostgreSQL Service Health

Check the PostgreSQL service using the service-management mechanism provided by the selected distribution.

Validate:

- Service is active.
- Service starts without persistent errors.
- Service survives a normal restart.
- Logs contain no unresolved startup errors.

Record the installed PostgreSQL version.

---

## 7. Local Database Connection

From `db01`, establish a controlled local administrative connection.

Validate:

- Server accepts local connection.
- Expected PostgreSQL version is returned.
- Expected cluster/database exists.
- Administrative identity is correct.

Do not record passwords in evidence.

### Pass Criteria

Local administrative access succeeds using the intended authentication mechanism.

---

## 8. Listening Socket Validation

Verify which addresses and ports PostgreSQL actually listens on.

Example approach:

```bash
ss -lntp
```

Confirm that PostgreSQL is not unintentionally exposed on all interfaces.

Expected target:

```text
Required interface(s) → listening
Unnecessary interfaces → not exposed
```

---

## 9. Authentication Validation

Test the configured PostgreSQL authentication policy.

Perform controlled tests for:

1. Valid administrative credentials.
2. Invalid credentials.
3. Valid application role when created.
4. Invalid/unauthorized role.

### Pass Criteria

Valid identities authenticate and invalid identities are rejected according to policy.

---

## 10. Authorization Validation

Test database privileges separately from authentication.

Example:

```text
Application role
    ↓
Required database objects       ALLOW
Unrelated privileged objects    DENY
Administrative functions        DENY unless explicitly required
```

Do not use a superuser for the authorization test.

### Pass Criteria

The application role has exactly the intended permissions and no unnecessary administrative privileges.

---

## 11. Database and Role Lifecycle Test

For a controlled test database/role:

```text
Create
 ↓
Connect
 ↓
Perform permitted operation
 ↓
Verify denied operation
 ↓
Remove/revoke
 ↓
Confirm access is gone
```

This validates that administrative operations have the expected effect.

Remove temporary objects after testing unless they are part of the intended configuration.

---

## 12. Network Connectivity Test

From the authorized application network, test TCP connectivity to PostgreSQL.

Reference:

```text
Application VLAN
      |
      | TCP 5432
      v
10.10.30.10
```

Use a real PostgreSQL client or an equivalent TCP test.

### Pass Criteria

Authorized application traffic reaches PostgreSQL.

---

## 13. Negative Network Test

From an unauthorized VLAN, test the same PostgreSQL endpoint.

Expected:

```text
Unauthorized VLAN → db01:5432 = DENY
```

This test should verify the complete security boundary, including OPNsense and host-level controls where used.

### Pass Criteria

Unauthorized clients cannot establish a PostgreSQL connection.

---

## 14. Application-to-Database Validation

When `app01` is implemented, perform an actual application database connection.

Target:

```text
app01
VLAN 40
   |
   | PostgreSQL connection
   v
 db01
VLAN 30
```

Validate:

- DNS resolution.
- TCP connectivity.
- TLS behavior where enabled.
- Authentication.
- Database selection.
- Required application query/write operation.

### Pass Criteria

The application can perform its required database operations without unnecessary access.

---

## 15. TLS Validation

If TLS is configured, verify:

- Connection uses TLS.
- Server certificate is valid.
- Certificate hostname matches the intended endpoint.
- Client trust chain is correct.
- Invalid/untrusted certificates are rejected according to policy.

Do not publish private certificate material.

---

## 16. Logging Validation

Generate controlled events and confirm logging behavior.

Test:

- Successful connection
- Failed authentication
- Database error
- Administrative operation
- Application connection

Record where the logs are stored and how they are retained.

### Pass Criteria

Important database events can be identified and correlated with time and operation.

---

## 17. Backup Validation

Run the documented backup procedure.

Verify:

- Backup completes.
- Backup artifact is readable.
- Backup is stored at the intended destination.
- Backup protection is appropriate.
- Retention behavior is understood.

Do not treat a successful command exit code as complete recovery validation.

---

## 18. Restore Validation

Restore a controlled backup into an isolated/test database or environment according to the documented recovery procedure.

Validate:

```text
Backup
  ↓
Restore
  ↓
Database starts/opens
  ↓
Expected objects exist
  ↓
Expected data exists
  ↓
Application-compatible query works
```

### Pass Criteria

The documented recovery procedure can produce a usable database state.

Full recovery testing should also be incorporated into Day 2 backup/restore procedures.

---

## 19. Configuration Persistence

After a controlled PostgreSQL restart, verify:

- Listen configuration persists.
- Authentication configuration persists.
- Roles/databases remain available.
- Logging remains active.
- Network access behaves identically.

A configuration that works only until restart is not validated.

---

## 20. Host Reboot Validation

Perform a controlled reboot of `db01`.

After reboot verify:

- Network
- DNS
- NTP
- Storage mounts
- PostgreSQL service
- Local connection
- Network access policy
- Application connection when available

### Pass Criteria

PostgreSQL returns to the expected operational state without manual emergency intervention.

---

## 21. Capacity Validation

Record:

```text
Filesystem usage:
Database size:
WAL usage:
Free disk:
Memory usage:
Connection count:
Configured connection limit:
```

The goal is not to optimize prematurely, but to establish a baseline for future Day 2 capacity reviews.

---

## 22. Failure / Recovery Validation

Use safe controlled scenarios.

Examples:

- Restart PostgreSQL.
- Temporarily stop a test connection.
- Test behavior after a configuration reload.
- Restore a test database from backup.
- Temporarily block the application-to-database firewall rule and verify expected failure.

Do not intentionally corrupt the only database or remove production-equivalent data merely to demonstrate failure handling.

---

## 23. Security Boundary Validation

The final security test should demonstrate layered enforcement.

```text
Unauthorized client
      ↓
Network segmentation
      ↓
OPNsense policy
      ↓
Host firewall
      ↓
PostgreSQL listen policy
      ↓
pg_hba.conf
      ↓
Database privileges
      ↓
DENY
```

And for an authorized request:

```text
app01
 ↓
Network policy      ALLOW
 ↓
Host policy         ALLOW
 ↓
PostgreSQL auth     ALLOW
 ↓
Database privilege  ALLOW
 ↓
Required operation  SUCCESS
```

This is the practical demonstration of defense in depth.

---

## 24. Evidence Record

For each significant test record:

```text
Validation ID:
Date:
Source:
Destination:
Database:
Role:
Operation:
Expected:
Actual:
Result: PASS / FAIL / N/A
Evidence:
Notes:
```

Remove credentials and other secrets before storing evidence in GitHub.

---

## 25. Validation Matrix

| Area | Test | Status |
|---|---|---|
| Host | Hostname/FQDN | ⬜ |
| Storage | Two-disk layout | ⬜ |
| Storage | Database data filesystem | ⬜ |
| NTP | Time synchronization | ⬜ |
| Service | PostgreSQL health | ⬜ |
| Version | PostgreSQL version | ⬜ |
| Local | Administrative connection | ⬜ |
| Network | Listening addresses | ⬜ |
| Auth | Valid authentication | ⬜ |
| Auth | Invalid authentication | ⬜ |
| AuthZ | Application role | ⬜ |
| Network | Authorized TCP 5432 | ⬜ |
| Network | Unauthorized TCP 5432 | ⬜ |
| Application | Real DB connection | ⬜ / Planned |
| TLS | TLS validation | ⬜ / N/A |
| Logging | Database events | ⬜ |
| Backup | Backup creation | ⬜ |
| Recovery | Restore test | ⬜ |
| Persistence | Service restart | ⬜ |
| Persistence | Host reboot | ⬜ |
| Capacity | Baseline metrics | ⬜ |
| Failure | Controlled recovery | ⬜ |
| E2E | Application workflow | ⬜ / Planned |

---

## 26. Completion Criteria

PostgreSQL can be marked **Validated** only when:

1. Host and storage configuration are correct.
2. PostgreSQL starts and remains healthy.
3. Local administrative access works.
4. Listening exposure matches the design.
5. Authentication behavior is correct.
6. Authorization follows least privilege.
7. Authorized network access works.
8. Unauthorized network access is blocked.
9. Application connectivity works once the application exists.
10. TLS behavior is validated where enabled.
11. Logging provides useful evidence.
12. Backup completes successfully.
13. Restore is successfully tested or explicitly deferred to Day 2 with a documented reason.
14. Configuration survives restart and reboot.
15. Capacity baseline is recorded.
16. Evidence is recorded.

> **PostgreSQL is validated when the database is usable, restricted, recoverable, and demonstrably integrated with its intended consumer.**

## Related Documentation

- [`installation.md`](installation.md) — PostgreSQL installation
- [`configuration.md`](configuration.md) — PostgreSQL configuration
- [`../network/segmentation.md`](../network/segmentation.md) — Network segmentation
- [`../network/validation.md`](../network/validation.md) — Network validation
- [`../../architecture/storage.md`](../../architecture/storage.md) — Storage architecture
- [`../../security/security.md`](../../security/security.md) — Security architecture
- [`../documentation-standard.md`](../documentation-standard.md) — Day 1 documentation standard
