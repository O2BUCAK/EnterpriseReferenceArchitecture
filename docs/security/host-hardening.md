# Host Hardening Baseline

> Common hardening baseline for infrastructure hosts and appliances in the Enterprise Reference Architecture.

## Status

**Documented / Planned baseline.**

This document defines the reference hardening controls. A control becomes **Implemented** or **Validated** only after it is applied to the laboratory system and evidence is recorded.

Monitoring and backup are intentionally outside the current hardening scope.

## Scope

Primary infrastructure roles:

| Component | Host | Baseline |
|---|---|---|
| Proxmox VE | Hypervisor nodes | Proxmox hardening |
| OPNsense | `fw01` | Firewall/appliance hardening |
| FreeIPA | `ipa01` | Linux + identity hardening |
| PostgreSQL | `db01` | Linux + database hardening |
| Docker | `app01` | Linux + container-host hardening |
| Automation | `auto01` | Linux + automation hardening |

---

## Hardening Model

The baseline is layered:

```text
Physical / Hypervisor
        ↓
Network / Firewall
        ↓
Operating System
        ↓
Administrative Access
        ↓
Service Configuration
        ↓
Application / Container
        ↓
Identity / Secrets
        ↓
Validation Evidence
```

A control should not be considered complete because a configuration file exists. The resulting security boundary must also be tested.

---

# 1. Common Linux Host Baseline

Applies to `ipa01`, `db01`, `app01`, and `auto01`.

## 1.1 Operating System

- [ ] Supported OS release
- [ ] Supported kernel
- [ ] Security updates applied
- [ ] Correct repositories configured
- [ ] Hostname follows project naming standard
- [ ] FQDN resolves correctly
- [ ] Forward DNS validated
- [ ] Reverse DNS validated
- [ ] Unnecessary packages removed where practical
- [ ] Unnecessary services disabled

## 1.2 Time Synchronization

- [ ] Chrony or approved time service installed
- [ ] Corporate / approved NTP source configured
- [ ] Time synchronization active
- [ ] Time offset verified
- [ ] Time source is reachable from the correct network

> Consistent time is required for authentication, TLS validation and reliable audit timestamps.

## 1.3 Administrative Access

- [ ] Administrative access restricted to management paths
- [ ] Named administrator accounts used where practical
- [ ] `root` SSH login disabled unless explicitly required
- [ ] SSH public-key authentication enabled
- [ ] SSH password authentication disabled where operationally appropriate
- [ ] `PermitEmptyPasswords no`
- [ ] SSH protocol remains version 2
- [ ] Sudo used for privileged operations
- [ ] Sudo permissions follow least privilege
- [ ] Shared administrative accounts avoided
- [ ] Stale accounts removed or disabled
- [ ] Administrative credentials stored securely

### SSH baseline

Reference controls:

```text
Protocol 2
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
PermitEmptyPasswords no
```

> Exact directives may vary by distribution and should be validated against the supported OpenSSH version before deployment.

## 1.4 Services and Listening Sockets

- [ ] `systemctl list-unit-files` reviewed
- [ ] Unnecessary services disabled
- [ ] Listening sockets reviewed with `ss -lntup`
- [ ] Each listening service has a documented owner/purpose
- [ ] Services bind only to required addresses
- [ ] Unused network daemons removed or disabled
- [ ] Host firewall enabled where appropriate
- [ ] Host firewall rules align with OPNsense policy

## 1.5 Filesystems and Permissions

The project follows the two-disk VM model:

```text
Disk 1 → Operating System
Disk 2 → /var, /home, /tmp and role-specific data
```

Hardening controls:

- [ ] `/var`, `/home`, and `/tmp` placed according to storage standard
- [ ] Sensitive configuration files have restrictive permissions
- [ ] Service accounts own only required files
- [ ] No world-readable credential files
- [ ] SUID/SGID files reviewed where appropriate
- [ ] Writable directories reviewed
- [ ] Temporary storage permissions validated
- [ ] Mount options reviewed where operationally compatible

> Mount options such as `nodev`, `nosuid`, and `noexec` should be used only after validating application compatibility.

## 1.6 Kernel and System Controls

Where appropriate to the workload:

- [ ] Kernel/sysctl baseline reviewed
- [ ] IP forwarding disabled on hosts that do not route traffic
- [ ] Source routing disabled where appropriate
- [ ] ICMP redirect behavior reviewed
- [ ] Reverse-path filtering reviewed
- [ ] Core-dump policy reviewed
- [ ] Kernel module exposure reduced where justified

Do not apply generic sysctl values blindly; each control must be validated for the host role.

## 1.7 Logging

- [ ] Authentication logs available
- [ ] System logs available
- [ ] Log rotation configured
- [ ] Security-sensitive events retained according to project scope
- [ ] Logs do not contain secrets
- [ ] Time source is synchronized

Centralized monitoring/observability is outside the current implementation scope.

---

# 2. Proxmox VE Hardening

Applies to each Proxmox node.

## 2.1 Platform

- [ ] Proxmox VE supported release
- [ ] Security updates applied
- [ ] Correct package repositories configured
- [ ] Hostname/FQDN correct
- [ ] DNS resolution correct
- [ ] Corporate NTP configured
- [ ] Chrony active
- [ ] Cluster time consistency verified

## 2.2 Management Access

- [ ] Proxmox Web UI reachable only from management path
- [ ] SSH reachable only from management path
- [ ] Root access restricted
- [ ] Named Proxmox administrative identities used where practical
- [ ] SSH keys used for host administration
- [ ] Password-based SSH disabled where operationally appropriate
- [ ] Privileged access is least privilege
- [ ] Unnecessary management exposure removed

## 2.3 Host Services

- [ ] Unnecessary services reviewed
- [ ] Listening ports reviewed
- [ ] Proxmox cluster services identified and documented
- [ ] Guest-agent requirement documented per VM
- [ ] Unused features disabled where practical

## 2.4 VM Security Defaults

For Linux VMs where supported:

- [ ] QEMU Guest Agent enabled
- [ ] VirtIO interfaces used according to standard
- [ ] VirtIO SCSI single used according to standard
- [ ] UEFI/OVMF used according to standard
- [ ] VM network placement matches VLAN design
- [ ] No unnecessary virtual hardware attached
- [ ] VM console access restricted to administrators
- [ ] VM privileged features documented when required

---

# 3. OPNsense / fw01 Hardening

## 3.1 Management

- [ ] Web UI limited to management network
- [ ] WAN administration disabled
- [ ] SSH disabled unless explicitly required
- [ ] HTTPS used for Web UI
- [ ] Strong administrative authentication configured
- [ ] Default/unused administrative accounts removed or disabled
- [ ] Administration follows least privilege

## 3.2 Firewall

- [ ] Default-deny model applied
- [ ] Inter-VLAN traffic explicitly controlled
- [ ] WAN inbound traffic explicitly controlled
- [ ] Unused firewall rules removed
- [ ] Broad `any-to-any` rules avoided
- [ ] Rule descriptions identify reason and scope
- [ ] Security-relevant firewall decisions logged where appropriate

## 3.3 Network Services

- [ ] DNS behavior documented
- [ ] DNS recursion/exposure limited to intended clients
- [ ] NTP service restricted to intended networks
- [ ] Unused services/plugins disabled
- [ ] Administrative services not exposed to untrusted networks

---

# 4. FreeIPA / ipa01 Hardening

When FreeIPA is implemented:

- [ ] Host baseline completed
- [ ] FreeIPA admin access restricted
- [ ] Kerberos policies reviewed
- [ ] Password policy defined
- [ ] Administrative groups separated
- [ ] Sudo rules follow least privilege
- [ ] LDAP exposure restricted to approved sources
- [ ] LDAPS/TLS used where required
- [ ] DNS service exposure restricted
- [ ] Host enrollment controlled
- [ ] Bootstrap credentials rotated
- [ ] Break-glass credentials separately protected

---

# 5. PostgreSQL / db01 Hardening

When PostgreSQL is implemented:

- [ ] Host baseline completed
- [ ] PostgreSQL listens only on required addresses
- [ ] Port 5432 restricted at network layer
- [ ] `pg_hba.conf` uses least privilege
- [ ] Dedicated application roles created
- [ ] Applications do not use PostgreSQL superuser
- [ ] Default/example credentials removed
- [ ] TLS enabled where required
- [ ] Administrative connections restricted
- [ ] PostgreSQL configuration permissions reviewed
- [ ] Database extensions reviewed before enabling them

Target access chain:

```text
OPNsense
   ↓
Host firewall
   ↓
PostgreSQL listen policy
   ↓
pg_hba.conf
   ↓
Database roles/privileges
```

---

# 6. Docker / app01 Hardening

## 6.1 Docker Host

- [ ] Host baseline completed
- [ ] Docker packages from trusted repositories
- [ ] Docker daemon access restricted
- [ ] Docker socket access restricted
- [ ] Untrusted users not added to the docker administrative group
- [ ] Unused Docker plugins/features removed
- [ ] Published ports reviewed

## 6.2 Container Baseline

Where supported by the application:

- [ ] Run as non-root
- [ ] Drop unnecessary Linux capabilities
- [ ] Use `no-new-privileges:true`
- [ ] Prefer read-only root filesystem
- [ ] Minimize host bind mounts
- [ ] Avoid `privileged: true`
- [ ] Avoid host network mode unless justified
- [ ] Explicit Docker networks used
- [ ] Resource limits reviewed
- [ ] Health checks defined where practical
- [ ] Images pinned to known versions
- [ ] Image source/publisher documented
- [ ] Unused published ports removed

## 6.3 Application Exposure

Preferred pattern:

```text
Client
  ↓
TCP 443
  ↓
Nginx
  ↓
Docker application network
  ↓
Application
```

Direct exposure of internal application ports should be avoided unless there is a documented requirement.

---

# 7. Automation / auto01 Hardening

When Ansible/OpenTofu is implemented:

- [ ] Host baseline completed
- [ ] Dedicated automation identity used
- [ ] SSH keys protected
- [ ] Automation credentials not embedded in playbooks
- [ ] Secrets retrieved from approved secret mechanism
- [ ] Ansible privilege escalation limited to required tasks
- [ ] OpenTofu state protected
- [ ] State files do not expose credentials
- [ ] Git repository contains no real secrets
- [ ] Automation changes are reviewable and reproducible

---

# 8. Secrets Hardening

Applies across all components.

- [ ] No passwords in Git
- [ ] No API tokens in Git
- [ ] No private keys in Git
- [ ] No real credential-bearing `.env` files committed
- [ ] No secrets in screenshots
- [ ] No secrets in public documentation
- [ ] Service identities are dedicated
- [ ] Bootstrap credentials rotated
- [ ] Secret access follows least privilege
- [ ] Secret rotation procedure documented

See [Secrets Management](secrets-management.md).

---

# 9. Network Hardening

Hardening must align with the network and firewall documents:

- [ ] Management network isolated
- [ ] Identity network isolated
- [ ] Database network isolated
- [ ] Application network isolated
- [ ] Inter-VLAN default deny
- [ ] Only documented flows allowed
- [ ] Infrastructure management ports not exposed to WAN
- [ ] PostgreSQL not exposed to WAN
- [ ] LDAP/Kerberos not exposed to WAN
- [ ] Docker published ports reviewed
- [ ] Egress requirements documented

See:

- [Network Architecture](../network/network.md)
- [Firewall Rule Set](../network/firewall-rule-set.md)
- [Port Map](../network/port-map.md)

---

# 10. Public Repository Hardening

Because this is a public GitHub repository:

- [ ] Example values use non-sensitive placeholders
- [ ] Internal credentials excluded
- [ ] Private keys excluded
- [ ] Sensitive logs excluded
- [ ] Real production addresses omitted where inappropriate
- [ ] Secrets management rules reflected in documentation
- [ ] `.gitignore` reviewed
- [ ] Before committing, search for accidental credentials

Recommended local review:

```text
git status
git diff --check
git diff
```

Secret scanning should also be added when practical.

---

# 11. Validation Method

Every hardening control should have a test.

| Area | Positive Test | Negative Test | Evidence |
|---|---|---|---|
| SSH | Approved admin connects | Unapproved source denied | Command/output |
| Root SSH | Approved sudo workflow works | Direct root SSH denied | Command/output |
| Firewall | Required flow works | Unauthorized flow blocked | Rule + test |
| VLAN | Required VLAN path works | Cross-VLAN unauthorized path blocked | Connectivity test |
| PostgreSQL | Approved app connects | Unapproved source denied | Connection test |
| Docker | Required service reachable | Unnecessary published port absent | Port/listener test |
| Identity | Authorized login works | Unauthorized login denied | Authentication test |
| Secrets | Authorized retrieval works | Unauthorized retrieval denied | Access test |
| NTP | Host synchronized | Invalid/out-of-policy source rejected | Chrony output |

Configuration screenshots alone are not sufficient evidence.

---

# 12. Hardening Status Matrix

| Domain | Priority | Status |
|---|---|---|
| Proxmox VE | Critical | Planned / validate per node |
| OPNsense | Critical | Planned / validate |
| Linux OS baseline | High | Planned |
| SSH / administrative access | Critical | Planned |
| Service minimization | High | Planned |
| Filesystem permissions | High | Planned |
| Host firewall alignment | High | Planned |
| Docker host | High | Planned |
| Container security | High | Planned |
| FreeIPA security | High | Planned |
| PostgreSQL security | Critical | Planned |
| Secrets handling | Critical | Planned |
| Network segmentation | Critical | Planned / requires validation |
| Public repository security | High | Ongoing |
| Monitoring | Out of scope | Intentionally excluded |
| Backup | Out of scope | Intentionally excluded |

---

# 13. Hardening Acceptance Criteria

A component is **hardened** only when:

1. The applicable baseline has been applied.
2. Administrative access is restricted and tested.
3. Unnecessary services and listeners have been reviewed.
4. Network exposure matches the Port Map and Firewall Rule Set.
5. Least-privilege access is validated.
6. Secrets are not exposed.
7. Positive and negative security tests pass.
8. Deviations are documented.
9. Validation evidence is recorded.

## Validation Record

```text
Component:
Host:
OS / Version:
Role:
Hardening baseline:
Date:
Administrator:
Controls applied:
Controls validated:
Evidence:
Known deviations:
Risk / rationale:
Next review:
```

---

## Related Documentation

- [Security Architecture](security.md)
- [Secrets Management](secrets-management.md)
- [Network Architecture](../network/network.md)
- [Firewall Rule Set](../network/firewall-rule-set.md)
- [Port Map](../network/port-map.md)
- [VM Design](../vm-design/vm-design.md)
- [Day 1 Security Baseline](../day-1/security/baseline.md)

---

## Summary

The hardening baseline provides a common security standard across the architecture while preserving the project's status discipline.

**Designing a control is not the same as implementing it.**

The repository should only mark a hardening control as **Implemented** or **Validated** after the corresponding laboratory configuration and evidence exist.
