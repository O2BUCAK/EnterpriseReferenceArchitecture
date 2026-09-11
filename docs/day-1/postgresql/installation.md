# PostgreSQL — Installation

> **Day 1 — Install**

This document defines the planned installation procedure for the PostgreSQL database platform used by the Enterprise Reference Architecture.

## Status

**Planned.** PostgreSQL has not yet been installed and validated as `db01` in the laboratory.

The target database host is planned for VLAN 30. Network segmentation and the application workload that will consume PostgreSQL are also currently planned.

---

## 1. Purpose

PostgreSQL will provide the relational database platform for applications deployed in the lab.

The design goal is to provide:

- Dedicated database workload isolation
- Controlled network access
- Stable storage layout
- Authentication and authorization controls
- Backup and restore capability
- Operational observability
- Reproducible configuration

---

## 2. Target Host

| Attribute | Reference value |
|---|---|
| Hostname | `db01` |
| Role | PostgreSQL Database Server |
| OS | Pardus Server |
| VLAN | 30 — Database |
| Example IP | `10.10.30.10` |
| Example FQDN | `db01.corp.example.com` |
| vCPU | 4 |
| RAM | 8 GiB |
| OS disk | 20 GiB |
| Data disk | 50 GiB |
| Status | Planned |

The hostname, IP address, and domain are reference values and must be replaced with actual implementation values.

---

## 3. Prerequisites

### Infrastructure

- Proxmox is operational.
- The database VM can be created.
- Database VLAN is implemented or a documented temporary network is available.
- DNS is available.
- NTP/time synchronization is available.
- A backup destination is available or planned.

### Application Dependency

Before opening database access, identify the application that will consume PostgreSQL.

Reference future dependency:

```text
app01
VLAN 40
   |
   | TCP 5432
   v
 db01
VLAN 30
```

Do not expose PostgreSQL broadly simply because an application will eventually need it.

---

## 4. VM Preparation

Create `db01` according to the project's two-disk standard.

Reference:

```text
CPU:       4 vCPU
RAM:       8 GiB
OS disk:   20 GiB
Data disk: 50 GiB
NIC:       VirtIO
Bridge:    vmbr0
Firmware:  UEFI / OVMF
SCSI:      VirtIO SCSI Single
QEMU GA:   Enabled
```

The larger second disk is intentional because database data, WAL, backups, and operational growth should not compete directly with the OS filesystem.

---

## 5. Operating System Installation

Install the selected Pardus Server release.

During installation:

1. Configure timezone.
2. Configure keyboard/layout.
3. Set the intended hostname.
4. Install the OS on the first disk.
5. Prepare the second disk for database/application data.
6. Configure a stable network address.
7. Create the required administrative account.
8. Install only required base packages.

The exact partitioning layout must be recorded after implementation.

---

## 6. Storage Preparation

The second disk is the database data disk.

Target concept:

```text
SCSI 0
└── Operating System

SCSI 1
└── Database / application data
```

The project VM standard also intends `/var`, `/home`, and `/tmp` to be placed on the second disk where applicable to the selected OS layout.

For PostgreSQL, ensure the final PostgreSQL data directory resides on storage designed for database workload and has sufficient capacity.

Do not blindly move directories before confirming the distribution's PostgreSQL packaging and service behavior.

---

## 7. Hostname and DNS

Configure a stable FQDN before database service configuration.

Reference:

```text
Hostname: db01
FQDN:     db01.corp.example.com
```

Verify:

```bash
hostnamectl
hostname --fqdn
getent hosts db01.corp.example.com
```

Use the actual final domain after the identity/DNS architecture is implemented.

---

## 8. Network Configuration

Configure a stable database address.

Reference:

```text
Address: 10.10.30.10/24
Gateway: 10.10.30.1
```

Validate:

```bash
ip address
ip route
ping -c 4 <gateway>
```

The database host should not be directly exposed to the Internet.

---

## 9. Time Synchronization

Configure the system's NTP/chrony service before PostgreSQL deployment.

Verify:

```bash
timedatectl
chronyc tracking
chronyc sources -v
```

Record the actual NTP source in implementation evidence.

---

## 10. Operating System Preparation

Before PostgreSQL installation:

1. Configure repositories.
2. Update the OS.
3. Reboot if required.
4. Confirm hostname.
5. Confirm DNS.
6. Confirm time synchronization.
7. Confirm storage mounts.
8. Confirm available capacity.

Example checks:

```bash
df -h
lsblk
mount
```

---

## 11. PostgreSQL Installation

Install the PostgreSQL version supported by the selected Pardus release and the application's compatibility requirements.

Do not select a major version solely because it is newer. Record the reason for the selected version.

After installation verify:

- PostgreSQL packages are present.
- The database service exists.
- The service starts.
- The expected data directory exists.
- The installed version is documented.

---

## 12. Initial Database Initialization

Initialize the PostgreSQL cluster using the distribution-supported mechanism.

Verify:

```text
Cluster initialized
Database service started
Local administrative access available
```

Do not immediately create application databases before the baseline configuration and backup approach are defined.

---

## 13. Initial Configuration

The initial configuration should establish:

- Listen address policy
- Port
- Authentication method
- Local administration
- Connection limits
- Logging
- Timezone behavior
- Memory/workload settings appropriate to the lab

The default PostgreSQL port is:

```text
TCP 5432
```

Only required clients should be able to reach it through the firewall.

---

## 14. Authentication Configuration

Use PostgreSQL's supported authentication mechanisms deliberately.

The final configuration must document:

- Local administrative authentication
- Application authentication
- Administrative roles
- Application roles
- Password policy where applicable
- TLS requirements where applicable

Avoid using the PostgreSQL superuser for application connections.

---

## 15. Application Database Preparation

Create an application-specific database and role only when an application has been selected.

Target model:

```text
Application
    |
    v
Application DB role
    |
    v
Application database
```

Do not give an application role PostgreSQL superuser privileges.

Example conceptual separation:

```text
postgres          → administrative role
app_<name>        → application role
<application_db>  → application database
```

Actual names should follow the application's requirements.

---

## 16. Network Access Control

PostgreSQL should listen only on interfaces required by the architecture.

Target policy:

```text
Application VLAN → db01:5432      ALLOW
Management VLAN  → db01:5432      Restricted
Identity VLAN    → db01:5432      DENY unless required
Internet         → db01:5432      DENY
Other VLANs      → db01:5432      DENY
```

The exact policy must be implemented through OPNsense and PostgreSQL host-level controls where appropriate.

---

## 17. TLS / Encryption in Transit

If PostgreSQL connections cross a network security boundary, evaluate TLS requirements.

For the target architecture, the application-to-database path is an inter-VLAN connection and should be treated as a controlled network boundary.

Document:

- TLS enabled/disabled
- Certificate source
- Trust model
- Client verification requirements
- Renewal procedure

Do not commit private keys or sensitive certificate material.

---

## 18. Logging

Enable sufficient PostgreSQL logging for troubleshooting and security review without generating unnecessary noise.

Potential areas:

- Connection attempts
- Authentication failures
- Administrative operations
- Long-running queries
- Errors
- Checkpoint/WAL-related events as operationally useful

Define retention separately as part of Day 2 operations.

---

## 19. Backup Preparation

PostgreSQL must have a documented recovery strategy before it becomes an application dependency.

Define:

- Logical backup method
- Physical/base backup strategy where appropriate
- Backup destination
- Schedule
- Retention
- Encryption/protection
- Restore process
- Restore validation

A successful backup command is not proof of recoverability.

---

## 20. Security Baseline

Minimum target baseline:

- No Internet exposure
- Restricted TCP 5432 access
- No application use of superuser
- Strong administrative credentials
- Controlled local access
- Appropriate PostgreSQL authentication
- Logging enabled
- Backup defined
- Restore procedure defined
- OS and PostgreSQL packages maintained
- Secrets outside Git

---

## 21. Resource and Capacity Baseline

Record after implementation:

```text
CPU:
RAM:
OS disk:
Database disk:
Filesystem:
PostgreSQL version:
Configured connection limit:
Expected workload:
```

The 50 GiB reference database disk is a starting point, not a guarantee of capacity.

Capacity should be reviewed as the application platform grows.

---

## 22. Initial Health Check

After installation verify:

- Service starts successfully.
- Local connection works.
- Database cluster is healthy.
- Data directory is writable by the PostgreSQL service account.
- Storage has sufficient free capacity.
- Logs show no persistent errors.
- Network exposure matches the intended policy.

The database should pass these checks before an application is connected.

---

## 23. Evidence

Record:

```text
VM ID:
Hostname:
FQDN:
OS release:
PostgreSQL version:
IP address:
Gateway:
Data filesystem:
Data directory:
NTP source:
Listening addresses:
Listening port:
Authentication method:
Firewall policy:
Backup method:
Installation date:
Known deviations:
Validation reference:
```

Never record database passwords, private keys, or secrets in public documentation.

---

## 24. Installation Completion Criteria

PostgreSQL installation can be considered **Installed** when:

1. `db01` exists with the intended VM resources.
2. The operating system is installed.
3. Storage is correctly mounted.
4. Hostname and network configuration are correct.
5. DNS and NTP are operational.
6. PostgreSQL packages are installed.
7. The database cluster is initialized.
8. PostgreSQL starts successfully.
9. Local administrative access works.
10. Initial security and logging configuration is applied.
11. Backup planning is documented.
12. Evidence is recorded.

It can only be marked **Validated** after the dedicated validation procedure passes.

## Related Documentation

- [`configuration.md`](configuration.md) — PostgreSQL configuration
- [`validation.md`](validation.md) — PostgreSQL validation
- [`../network/segmentation.md`](../network/segmentation.md) — Network segmentation
- [`../network/validation.md`](../network/validation.md) — Network validation
- [`../proxmox/configuration.md`](../proxmox/configuration.md) — Proxmox configuration
- [`../../architecture/storage.md`](../../architecture/storage.md) — Storage architecture
- [`../../security/security.md`](../../security/security.md) — Security architecture
- [`../documentation-standard.md`](../documentation-standard.md) — Day 1 documentation standard
