# Docker / Application Platform — Validation

> **Day 1 — Validate**

This document defines the validation procedure for the Docker application platform on `app01`.

## Status

**Planned.** Docker and the target application stack are not currently implemented in the laboratory.

Only executed tests against the actual lab may be recorded as implementation evidence.

---

## 1. Validation Principle

A Docker host is not validated merely because `docker ps` returns containers.

Validation must prove:

```text
Host
 ↓
Docker Engine
 ↓
Storage
 ↓
Networking
 ↓
Security boundary
 ↓
Application health
 ↓
Persistence
 ↓
Backup / recovery
```

---

## 2. Prerequisites

Confirm:

- `app01` is running.
- OS configuration is complete.
- Storage is mounted.
- DNS and NTP work.
- Docker Engine is installed.
- Docker Compose functionality is available.
- A controlled test container can be used.
- Network segmentation is available or a documented temporary network is being used.

---

## 3. Host Validation

Verify:

```bash
hostnamectl
hostname --fqdn
ip address
ip route
```

Confirm the host uses the intended Application VLAN and gateway.

---

## 4. Storage Validation

Verify the two-disk model:

```bash
lsblk
df -h
mount
```

Confirm:

- OS resides on the first disk.
- Docker/application persistent data resides on the intended second disk.
- Required filesystems mount after reboot.
- Sufficient free space exists.

### Pass Criteria

Container data is persistent and does not depend on an unintended ephemeral filesystem.

---

## 5. Docker Engine Health

Verify:

- Docker daemon is active.
- Docker CLI can communicate with the daemon.
- Version is documented.
- Service restarts successfully.
- Service starts after reboot.

Example:

```bash
docker version
docker info
```

Use the actual installed version as evidence.

---

## 6. Administrative Access Validation

Test who can administer Docker.

Validate:

- Authorized administrator can manage containers.
- Unauthorized local user cannot obtain Docker administrative control.
- Portainer, if implemented, follows the same administrative security model.

### Pass Criteria

Docker administration is limited to explicitly authorized identities.

---

## 7. Basic Container Lifecycle Test

Run a controlled test image.

Validate:

```text
Pull
 ↓
Create
 ↓
Start
 ↓
Inspect
 ↓
Stop
 ↓
Remove
```

### Pass Criteria

The complete lifecycle works without unexpected host or network errors.

Remove temporary test containers afterward.

---

## 8. Persistent Storage Test

Create a controlled test container with persistent storage.

Test:

```text
Write data
   ↓
Stop container
   ↓
Remove/recreate container
   ↓
Read data
```

### Pass Criteria

Data survives container recreation.

This proves persistent storage behavior rather than merely container startup.

---

## 9. Docker Network Validation

Create or use the intended test networks.

Validate:

- Container receives expected address.
- Containers can communicate when placed on the same intended network.
- Containers cannot communicate when no network path exists.
- Published ports behave as documented.

Avoid exposing every test container directly to the host network.

---

## 10. Published Port Validation

Enumerate host-published ports.

Example:

```bash
docker ps
ss -lntp
```

Compare actual ports against the documented service exposure.

### Pass Criteria

No undocumented application port is reachable from the network.

---

## 11. Reverse Proxy Validation

When Nginx is implemented, test:

```text
Client
  ↓
OPNsense
  ↓
Nginx
  ↓
Application
```

Validate:

- Expected hostname resolves.
- TLS works where enabled.
- Correct upstream is selected.
- Unconfigured applications are not exposed.
- Backend containers are not unnecessarily published directly.

---

## 12. Application Health Validation

For every deployed service verify more than container state.

Test:

```text
Container running
      ↓
Health check
      ↓
HTTP/API response
      ↓
Dependency connectivity
      ↓
Functional operation
```

A container marked `Up` but returning application errors should be considered unhealthy.

---

## 13. Application-to-PostgreSQL Validation

When `db01` and an application requiring PostgreSQL exist, test the real dependency.

Target:

```text
Application container
       |
       | TCP 5432
       v
      db01
```

Validate:

- DNS resolution.
- Network path.
- Firewall policy.
- PostgreSQL authentication.
- Application database operation.

### Negative Test

Attempt the same database connection from a container or network that should not have access.

Expected:

```text
Unauthorized source → DENY
```

---

## 14. Container Security Validation

Inspect deployed containers for unnecessary privileges.

Review:

- Privileged mode
- Host network mode
- Host filesystem mounts
- Device mappings
- Linux capabilities
- Container user
- Read-only filesystem opportunities

### Pass Criteria

Each elevated capability has a documented reason.

---

## 15. Image Validation

For each important service record:

```text
Image:
Tag:
Digest:
Registry:
```

Verify that the running container corresponds to the documented image/version.

Do not accept an unexpected image source merely because the service starts.

---

## 16. Resource Validation

Record baseline resource usage.

Check:

```text
CPU usage
Memory usage
Disk usage
Container count
```

Confirm that configured resource limits behave as expected where limits are used.

The objective is to prevent one container from exhausting the entire 10 GiB reference VM.

---

## 17. Health Check Validation

Where health checks are configured, intentionally test a healthy and unhealthy condition in a controlled environment.

Validate:

```text
Healthy application → healthy
Broken dependency   → unhealthy/degraded
Recovered dependency→ healthy
```

Do not mark an application healthy solely because its process is running.

---

## 18. Logging Validation

Generate controlled application/container events.

Verify:

- Logs are produced.
- Rotation works.
- Retention is defined.
- Sensitive information is not unnecessarily logged.
- Application errors can be correlated with container events.

Centralized logging remains a planned future capability unless implemented separately.

---

## 19. TLS Validation

For services exposed through HTTPS:

- Verify certificate validity.
- Verify hostname/SAN.
- Verify certificate trust.
- Confirm HTTP-to-HTTPS behavior if configured.
- Confirm private keys are not exposed through container logs or repository files.

---

## 20. Backup Validation

For each stateful application:

1. Create a documented backup.
2. Verify the artifact exists.
3. Verify the artifact can be read.
4. Confirm the backup includes required application state.

Do not confuse image availability with application recovery.

---

## 21. Restore Validation

Perform a controlled restore into an isolated/test environment where practical.

Target:

```text
Backup
  ↓
Restore
  ↓
Start service
  ↓
Health check
  ↓
Verify persistent data
  ↓
Functional test
```

### Pass Criteria

The documented recovery procedure produces a usable application state.

Full recurring restore testing belongs in Day 2 operations.

---

## 22. Reboot Persistence

Reboot `app01` under controlled conditions.

After reboot verify:

- Docker starts.
- Networks return.
- Persistent volumes are available.
- Required containers restart according to policy.
- Health checks become healthy.
- Reverse proxy works.
- Application dependencies work.
- Firewall exposure remains correct.

---

## 23. Failure / Recovery Test

Use safe scenarios such as:

- Restart a representative container.
- Stop and restart a dependency.
- Temporarily block a non-critical application dependency.
- Recreate a stateless test container.
- Restore a test application's persistent data.

Observe whether recovery follows the documented procedure.

Do not intentionally destroy the only copy of application data.

---

## 24. Management Isolation Test

Verify that administrative interfaces are not reachable from untrusted networks.

Reference:

```text
Management VLAN → management interface  ALLOW
Application VLAN → management interface DENY unless required
Internet → management interface         DENY
```

Apply the same principle to Portainer and other administrative services.

---

## 25. End-to-End Application Test

The final Day 1 test should use a real application path.

Example:

```text
Client
  ↓
OPNsense
  ↓
Nginx
  ↓
Application container
  ↓
PostgreSQL
  ↓
Persistent data
```

Validate the complete request, authentication, application operation, database transaction, and response.

This is the strongest evidence that the application platform is integrated rather than merely installed.

---

## 26. Evidence Record

Record each significant test:

```text
Validation ID:
Date:
Service:
Source:
Destination:
Expected:
Actual:
Result: PASS / FAIL / N/A
Image/version:
Evidence:
Notes:
```

Remove secrets from logs and screenshots before committing evidence.

---

## 27. Validation Matrix

| Area | Test | Status |
|---|---|---|
| Host | Host identity | ⬜ |
| Storage | Persistent data disk | ⬜ |
| Docker | Engine health | ⬜ |
| Docker | Admin access | ⬜ |
| Lifecycle | Container start/stop | ⬜ |
| Storage | Data persistence | ⬜ |
| Network | Container networking | ⬜ |
| Network | Published ports | ⬜ |
| Proxy | Nginx routing | ⬜ / Planned |
| App | Application health | ⬜ / Planned |
| Database | App → PostgreSQL | ⬜ / Planned |
| Security | Container privileges | ⬜ |
| Images | Version/source | ⬜ |
| Resources | CPU/memory baseline | ⬜ |
| Health | Health checks | ⬜ / Planned |
| Logging | Container/application logs | ⬜ |
| TLS | HTTPS validation | ⬜ / Planned |
| Backup | Backup creation | ⬜ |
| Recovery | Restore test | ⬜ |
| Persistence | Host reboot | ⬜ |
| Failure | Controlled recovery | ⬜ |
| Security | Management isolation | ⬜ |
| E2E | Client → App → DB | ⬜ / Planned |

---

## 28. Completion Criteria

The Docker/application platform can be marked **Validated** only when:

1. Docker Engine is healthy.
2. Administrative access is restricted.
3. Container lifecycle works.
4. Persistent storage survives container recreation.
5. Network behavior matches the design.
6. Published ports are documented and restricted.
7. Containers use appropriate privileges.
8. Images and versions are documented.
9. Resource behavior is understood.
10. Health checks work where implemented.
11. Logging works as intended.
12. TLS is validated where required.
13. Backup succeeds.
14. Restore is successfully tested or explicitly deferred to Day 2 with a documented reason.
15. Configuration survives host reboot.
16. Management interfaces are isolated.
17. A real application dependency works once the application and database are implemented.
18. Evidence is recorded.

> **The application platform is validated when containers are secure, persistent, reachable only as intended, operationally observable, and recoverable.**

## Related Documentation

- [`installation.md`](installation.md) — Docker/application platform installation
- [`configuration.md`](configuration.md) — Docker/application platform configuration
- [`../network/segmentation.md`](../network/segmentation.md) — Network segmentation
- [`../network/validation.md`](../network/validation.md) — Network validation
- [`../postgresql/configuration.md`](../postgresql/configuration.md) — PostgreSQL configuration
- [`../postgresql/validation.md`](../postgresql/validation.md) — PostgreSQL validation
- [`../../architecture/application-platform.md`](../../architecture/application-platform.md) — Application platform architecture
- [`../../security/security.md`](../../security/security.md) — Security architecture
- [`../documentation-standard.md`](../documentation-standard.md) — Day 1 documentation standard
