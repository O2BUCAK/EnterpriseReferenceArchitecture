# Docker / Application Platform — Installation

> **Day 1 — Install**

This document defines the planned installation procedure for the Docker-based application platform on `app01`.

## Status

**Planned.** Docker and the application platform have not yet been implemented or validated in the laboratory.

The services listed in the architecture are target components. Their presence in this document does not mean they are deployed.

---

## 1. Purpose

`app01` will provide the container platform for selected FOSS services in the reference architecture.

Target platform responsibilities:

- Container runtime
- Application lifecycle
- Persistent application data
- Internal application networking
- Reverse proxy
- Container administration
- Application isolation
- Service-to-service communication
- Backup/recovery preparation

The platform is intentionally separated from the database workload on `db01`.

---

## 2. Target Host

| Attribute | Reference value |
|---|---|
| Hostname | `app01` |
| Role | Docker Application Platform |
| OS | Ubuntu Server |
| VLAN | 40 — Application |
| Example IP | `10.10.40.10` |
| Example FQDN | `app01.corp.example.com` |
| vCPU | 4 |
| RAM | 10 GiB |
| OS disk | 20 GiB |
| Data disk | 50 GiB |
| Status | Planned |

The IP and domain are reference values only.

---

## 3. Target Application Stack

The architecture currently identifies the following planned services:

| Service | Purpose | Status |
|---|---|---|
| Nginx | Reverse proxy / HTTP entry point | Planned |
| Portainer | Container administration | Planned |
| Teleport CE | Access platform | Planned |
| Keycloak | Identity integration | Planned |
| OpenBao | Secrets management | Planned |
| NetBox | Network/IPAM/DCIM | Planned |
| Squid | Proxy/gateway use cases | Planned |
| Forgejo | Git service | Planned |
| Woodpecker CI | CI/CD | Planned |
| Wiki.js | Documentation platform | Planned |
| Project Pulp | Repository/content management | Planned |

Install services incrementally. Do not deploy the entire target stack before the base platform has been validated.

---

## 4. Prerequisites

Before Docker installation:

- Proxmox is operational.
- `app01` can be created.
- Application VLAN is implemented or a documented temporary network exists.
- DNS is available.
- NTP/time synchronization is available.
- The second data disk is available.
- Backup storage is defined.
- The required service ports are documented.
- PostgreSQL dependency is understood before applications requiring it are deployed.

---

## 5. VM Preparation

Create `app01` according to the project VM standard.

Reference:

```text
CPU:       4 vCPU
RAM:       10 GiB
OS disk:   20 GiB
Data disk: 50 GiB
NIC:       VirtIO
Bridge:    vmbr0
Firmware:  UEFI / OVMF
SCSI:      VirtIO SCSI Single
QEMU GA:   Enabled
```

The second disk provides application/container data capacity and should not be treated as disposable container storage.

---

## 6. Operating System Installation

Install the selected Ubuntu Server release.

During installation:

1. Configure timezone.
2. Configure keyboard/layout.
3. Configure hostname.
4. Install the OS on the first disk.
5. Prepare the second disk for persistent application data.
6. Configure a stable network address.
7. Create the administrative account.
8. Enable only required base services.

Record the actual OS release in the evidence record.

---

## 7. Storage Preparation

Use the second disk for persistent application data.

Target concept:

```text
SCSI 0
└── Operating System

SCSI 1
└── Container / Application data
```

The project standard intends `/var`, `/home`, and `/tmp` to be placed on the second disk where appropriate to the selected OS layout.

Before choosing Docker data paths, determine the final filesystem layout and document it.

---

## 8. Hostname, DNS and Time

Configure a stable host identity before application deployment.

Reference:

```text
Hostname: app01
FQDN:     app01.corp.example.com
```

Verify:

```bash
hostnamectl
hostname --fqdn
getent hosts app01.corp.example.com
```

Configure and verify NTP/chrony:

```bash
timedatectl
chronyc tracking
chronyc sources -v
```

---

## 9. Operating System Baseline

Before installing Docker:

1. Configure supported repositories.
2. Update the operating system.
3. Reboot if required.
4. Verify DNS.
5. Verify NTP.
6. Verify storage.
7. Verify administrative access.
8. Remove or disable unnecessary services.

Do not expose the Docker host directly to the Internet.

---

## 10. Docker Installation

Install Docker Engine using a supported installation method for the selected Ubuntu release.

Avoid mixing unrelated Docker package sources without documenting the reason.

After installation verify:

- Docker daemon is running.
- Docker starts after reboot.
- Administrative Docker access is restricted.
- Container networking is operational.
- Image pulls work through the intended network path.

Use the supported Docker Compose implementation required by the selected Docker release.

---

## 11. Docker Administration Model

Docker administration effectively provides high privileges on the host.

Therefore:

- Do not give Docker administrative access to arbitrary users.
- Keep host administration separate from application administration where practical.
- Treat membership in the Docker administrative group as privileged access.
- Record who can deploy containers.

Portainer, if implemented, must not become an unaudited alternative path around the host security model.

---

## 12. Docker Data Layout

Define a predictable structure for persistent application data.

Example:

```text
/srv/
└── containers/
    ├── nginx/
    ├── portainer/
    ├── keycloak/
    ├── openbao/
    ├── netbox/
    ├── forgejo/
    └── ...
```

The exact path is a reference convention and can be changed during implementation.

Separate:

- Compose/configuration files
- Persistent application data
- Logs where separately stored
- Backup artifacts

Do not place important persistent data only inside an ephemeral container layer.

---

## 13. Container Image Policy

Use trusted, documented image sources.

For each production-like container record:

```text
Image:
Registry:
Version/tag:
Digest where appropriate:
Purpose:
Update strategy:
Data location:
Network(s):
Dependencies:
```

Avoid deploying unverified images from unknown publishers.

Pinning versions or digests should be considered where reproducibility is important.

---

## 14. Compose Project Standard

Each logical application stack should have its own clearly identified Compose project or equivalent deployment unit.

Recommended conceptual structure:

```text
application/
├── compose.yaml
├── .env.example
├── README.md
├── config/
└── data/
```

Secrets must not be stored in `.env.example` or committed configuration.

Use placeholders and document how secrets are supplied securely.

---

## 15. Container Networking

Do not place every container into a single unrestricted network.

Target model:

```text
VLAN 40
   ↓
Docker host
   ↓
Reverse proxy network
   ↓
Application networks
   ↓
Database dependency where required
```

Create dedicated Docker networks according to actual application dependencies.

Example:

```text
frontend
backend
management
```

Only connect a container to the networks it actually needs.

---

## 16. Reverse Proxy

Nginx is the planned HTTP reverse proxy.

Target flow:

```text
Client
  ↓
OPNsense policy
  ↓
Nginx
  ↓
Application container
```

The reverse proxy should provide a controlled entry point instead of exposing every application container directly.

Document:

- Listener
- Hostname
- Upstream
- TLS certificate
- Authentication requirement
- Network source

---

## 17. Application-to-Database Connectivity

Applications requiring PostgreSQL should communicate with `db01` through the documented firewall path.

Target:

```text
app01 / application container
           |
           | TCP 5432
           v
          db01
```

Do not place PostgreSQL inside `app01` merely to avoid network configuration.

The separate database VM is an intentional architecture boundary.

---

## 18. Management Services

Portainer, NetBox, Forgejo, Wiki.js, and other administrative applications should have explicit access policies.

Management interfaces should not automatically be exposed to every application client.

Target principle:

```text
Management VLAN
      ↓
Controlled access
      ↓
Application management interfaces
```

---

## 19. Secrets

Container deployments frequently require credentials, tokens, certificates, and API keys.

Never commit these to GitHub.

Do not place real secrets in:

- `compose.yaml`
- `.env`
- README files
- screenshots
- shell history
- public configuration examples

OpenBao is planned as a future secrets-management component. It must not be described as an implemented dependency until it is actually deployed and validated.

---

## 20. Resource Limits

Containers should have reasonable resource expectations.

For critical services, document where practical:

```text
CPU limit:
Memory limit:
Storage expectation:
Restart policy:
Health check:
Dependencies:
```

Do not assign unlimited resources to every container on a 10 GiB reference VM.

---

## 21. Health Checks

Applications should expose meaningful health checks where supported.

A container being `running` does not necessarily mean the application is healthy.

Target:

```text
Container running
      ↓
Process healthy
      ↓
Service responsive
      ↓
Dependency available
```

Record application-specific health checks during deployment.

---

## 22. Logging

Define where container logs are collected and how they are rotated.

At minimum determine:

- Container log driver
- Rotation policy
- Retention
- Application log location
- Central logging plan

Centralized observability is a planned future capability unless separately implemented.

---

## 23. Backup Preparation

Persistent application data must have a backup strategy.

Back up as appropriate:

- Application data
- Compose/configuration files
- Database dependencies
- Certificates
- Application-specific state

Do not assume an image can recreate application data.

A restore test is required before considering an application recoverable.

---

## 24. Initial Application Deployment Order

Do not deploy the complete target stack simultaneously.

Recommended sequence:

```text
Docker Engine
      ↓
Basic test container
      ↓
Persistent-volume test
      ↓
Docker network test
      ↓
Nginx
      ↓
One representative application
      ↓
Application → PostgreSQL dependency
      ↓
Management services
      ↓
Identity/secrets integrations
      ↓
Remaining services
```

This makes failures easier to isolate.

---

## 25. Initial Security Baseline

Minimum target baseline:

- Docker host is not directly Internet-exposed.
- Docker administration is restricted.
- Images come from trusted sources.
- Versions are documented.
- Persistent data uses the second disk.
- Containers use least-required networks.
- Host and container privileges are minimized.
- Secrets are external to Git.
- Management interfaces are restricted.
- Backups are defined.
- Logs are retained appropriately.

---

## 26. Evidence

Record:

```text
VM ID:
Hostname:
FQDN:
OS release:
Docker version:
Compose version:
Data filesystem:
Data path:
Container networks:
Exposed ports:
Reverse proxy:
Backup method:
Firewall policy:
Image policy:
Installation date:
Known deviations:
Validation reference:
```

Do not publish secrets or private keys.

---

## 27. Installation Completion Criteria

Docker/application platform installation can be considered **Installed** when:

1. `app01` exists with the intended resources.
2. OS installation is complete.
3. Storage is correctly configured.
4. Hostname, DNS, and NTP are correct.
5. Docker Engine is installed.
6. Docker service starts successfully.
7. Docker survives reboot.
8. A controlled test container can start and stop.
9. Persistent storage works.
10. Container networking works.
11. Administrative access is restricted.
12. Initial backup approach is documented.
13. Evidence is recorded.

The application platform should be marked **Validated** only after the dedicated validation procedure passes.

## Related Documentation

- [`configuration.md`](configuration.md) — Docker/application platform configuration
- [`validation.md`](validation.md) — Docker/application platform validation
- [`../network/segmentation.md`](../network/segmentation.md) — Network segmentation
- [`../network/validation.md`](../network/validation.md) — Network validation
- [`../postgresql/installation.md`](../postgresql/installation.md) — PostgreSQL installation
- [`../postgresql/validation.md`](../postgresql/validation.md) — PostgreSQL validation
- [`../../architecture/application-platform.md`](../../architecture/application-platform.md) — Application platform architecture
- [`../../security/security.md`](../../security/security.md) — Security architecture
- [`../documentation-standard.md`](../documentation-standard.md) — Day 1 documentation standard
