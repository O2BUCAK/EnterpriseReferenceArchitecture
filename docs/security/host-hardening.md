# Host Hardening Baseline

> Common security baseline for Linux infrastructure hosts.

## Status
**Planned baseline.** Apply and validate per host.

## Scope
Primary Linux hosts:
```
ipa01
db01
app01
auto01
```

## Baseline
### OS
- Supported release
- Security updates applied
- Correct repositories
- Hostname and FQDN correct

### Time and DNS
- Approved NTP source configured
- Time synchronization active
- Forward and reverse DNS validated

### Administrative Access
- SSH restricted to management paths
- Root SSH disabled unless explicitly required
- Named administrative accounts where practical
- Sudo for privileged operations
- SSH keys preferred
- Password authentication disabled where operationally appropriate

### Services
- Unnecessary services disabled
- Listening sockets reviewed
- Host firewall enabled where appropriate
- Services bound to intended addresses

### Filesystems and Permissions
- Sensitive directories use restrictive permissions
- Service accounts have only required filesystem access
- /var, /home, and /tmp follow the storage standard
- SUID/SGID and writable paths reviewed where appropriate

### Logging
- Authentication/system logs available
- Rotation configured
- Security-relevant events retained according to scope

Monitoring is intentionally outside the current implementation scope.

### Role-specific
- PostgreSQL: 5432 restricted to approved sources.
- Docker: Docker administration and published ports restricted.
- FreeIPA: DNS/Kerberos/LDAP restricted to approved sources.
- Automation: protect SSH keys and IaC state.

### Secrets
- No secrets in Git.
- No world-readable credential files.
- Dedicated service identities.
- Rotate bootstrap credentials.

## Validation Record
```
Host:
OS:
Kernel:
Hostname:
DNS:
NTP:
SSH:
Firewall:
Listening services:
Packages reviewed:
Filesystem permissions:
Secrets reviewed:
Validation date:
Known deviations:
```

## Acceptance
A host is hardened only after baseline controls are applied, administrative access is tested, services and ports are reviewed, DNS/NTP are validated, security boundaries are tested, and deviations are documented.

## Related Documentation
- [Security Architecture](security.md)
- [Storage Architecture](../architecture/storage.md)
- [Network Architecture](../network/network.md)
- [Firewall Rule Set](../network/firewall-rule-set.md)
