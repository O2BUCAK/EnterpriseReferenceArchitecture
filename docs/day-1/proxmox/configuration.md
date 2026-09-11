# Proxmox VE — Host Configuration Baseline

> **Day 1 — Build & Configure**

This document defines the configuration baseline applied after the Proxmox VE installation described in [`installation.md`](installation.md).

The goal is to turn a newly installed Proxmox host into a predictable infrastructure platform. Installation establishes the operating system; this document establishes the **operational baseline**.

## Status

**Reference procedure.** Proxmox VE is implemented in the laboratory, while individual configuration items are considered implemented only when they have been actually applied and validated.

---

## 1. Configuration Principles

The Proxmox host should follow these principles:

1. Stable hostname and network identity
2. Reliable DNS resolution
3. Reliable time synchronization
4. Controlled package repositories
5. Minimal exposed management services
6. Predictable storage configuration
7. Consistent VM configuration
8. Least-privilege administrative access
9. Configuration changes documented before becoming the new standard
10. Changes validated after implementation

---

## 2. Host Identity

The Proxmox node should have a stable hostname and FQDN.

Reference example:

```text
Hostname: pve01
FQDN:     pve01.corp.example.com
```

`corp.example.com` is a documentation-only example domain used by this project.

Verify:

```bash
hostnamectl
hostname -f
```

### Configuration Criteria

- [ ] Hostname follows the project naming convention
- [ ] FQDN resolves correctly
- [ ] Reverse resolution is correct where supported
- [ ] Hostname does not change unexpectedly after reboot

---

## 3. Management Network

The Proxmox management plane should use a stable management address.

The target architecture reserves VLAN 10 for management. Network segmentation is currently a **planned architecture capability**, not a blanket implementation claim. citeturn5file0L1-L2

Reference model:

```text
Management VLAN
      |
    vmbr0
      |
   Proxmox
```

Example values:

```text
Address:  10.10.10.10/24
Gateway:  10.10.10.1
DNS:      10.10.10.1
```

Use the actual laboratory addressing during implementation.

### Verify Interface State

```bash
ip addr
ip route
```

Confirm:

- [ ] Correct interface is connected
- [ ] Correct management address is configured
- [ ] Default route is correct
- [ ] Gateway is reachable
- [ ] Management interface survives reboot

> **Warning:** Do not change the active management bridge remotely without a tested recovery path. A network mistake can immediately disconnect the administrator from the host.

---

## 4. Linux Bridge Baseline

Proxmox normally uses a Linux bridge to connect VMs to the physical network.

Reference topology:

```text
Physical NIC
     |
   vmbr0
     |
 +---+----------------+
 |                    |
Host               VMs
```

The exact bridge configuration depends on whether the host is operating as an access endpoint, VLAN-aware trunk endpoint, or another topology.

### Current Architecture Direction

The project intends to use `vmbr0` as the primary VM bridge and OPNsense as the virtual network-security gateway.

Do not describe VLAN-aware bridging or trunk configuration as implemented until it has been configured and tested.

### Validation

```bash
ip link show vmbr0
bridge link
```

Also validate VM connectivity from an actual guest rather than relying only on host-side interface state.

---

## 5. VLAN-Aware Networking — Planned

The target network architecture contains:

| VLAN | Purpose | Status |
|---:|---|---|
| 10 | Management | Planned |
| 20 | Identity | Planned |
| 30 | Database | Planned |
| 40 | Application | Planned |

The intended design is to provide controlled segmentation through OPNsense and VLANs. citeturn5file0L1-L2

When the physical network supports VLAN trunking, the Proxmox bridge can be configured for VLAN-aware VM networking.

Implementation must include:

1. Physical switch configuration
2. Proxmox bridge configuration
3. VM VLAN assignment
4. OPNsense interface/VLAN configuration
5. Firewall policy
6. End-to-end connectivity testing

The presence of a VLAN ID in architecture documentation is not evidence that the VLAN exists on the physical network.

---

## 6. DNS Configuration

DNS is an infrastructure dependency and should be treated as part of the host baseline.

Verify the resolver configuration using the tools appropriate to the installed Proxmox/Debian release.

Useful checks:

```bash
resolvectl status
getent hosts example.com
getent hosts pve01.corp.example.com
```

The exact resolver implementation can vary by release and configuration. Avoid hard-coding commands that assume a particular resolver daemon is installed.

### DNS Requirements

- Host can resolve required external names
- Host can resolve required internal names
- Host's own FQDN is resolvable
- DNS configuration remains correct after reboot
- DNS failures can be diagnosed independently of the application layer

---

## 7. Time Synchronization

Time synchronization must be continuously maintained.

Verify:

```bash
timedatectl
```

The result should show an active synchronization mechanism and a synchronized system clock.

The project has previously encountered clock-skew issues during infrastructure work. Therefore NTP validation is treated as a **hard prerequisite**, not an optional tuning step.

### Operational Rule

> Every infrastructure node should have a known and reliable time source before identity, certificates, logging, clustering, or security-sensitive services are introduced.

### Validation

Record:

```text
Time zone:
Synchronization state:
Active time source:
Last successful synchronization:
```

Do not expose internal NTP server addresses in public documentation unless they are intentionally part of the public design.

---

## 8. Repository and Package Management

Review repository configuration before applying updates.

The configuration should be consistent with the installed Proxmox VE release and the chosen subscription/support model.

Typical maintenance workflow:

```bash
apt update
apt full-upgrade
```

Review package changes before confirming them.

### Repository Rules

- Do not mix incompatible Proxmox repository configurations.
- Do not blindly copy repository files from another Proxmox release.
- Keep Debian and Proxmox repositories aligned with the installed release.
- Review repository changes as infrastructure changes.

### Validation

```bash
apt update
```

A successful update operation with no repository errors is required before treating the package baseline as healthy.

---

## 9. System Updates

A newly installed host should be brought to a maintained package state before additional workloads are deployed.

Recommended sequence:

```text
Review repositories
      ↓
apt update
      ↓
Review available upgrades
      ↓
apt full-upgrade
      ↓
Reboot if required
      ↓
Validate Proxmox
      ↓
Validate network
      ↓
Validate time
```

After reboot:

```bash
pveversion -v
systemctl --failed
```

Check the web interface and node health as well.

---

## 10. Proxmox Storage Configuration

Review the storage configuration before creating workloads.

The storage model should clearly distinguish:

- ISO images
- VM disks
- Container data if used
- Backups
- Templates
- Other supported content types

Inspect the configuration and capacity through the Proxmox interface and command line as appropriate.

Example:

```bash
pvesm status
```

### Storage Principles

1. Do not fill the storage device to the point where host operation becomes unreliable.
2. Monitor free capacity.
3. Keep backup storage conceptually separate from primary VM storage where possible.
4. Do not treat snapshots as backups.
5. Document storage changes.

The current lab uses a single 512 GB NVMe reference host, so capacity management is especially important. The resource matrix deliberately reserves host capacity rather than allocating all storage to VMs. citeturn9file0L1-L2

---

## 11. VM Configuration Standard

All Linux VMs should follow the project VM standard unless a role-specific exception is documented.

Reference baseline:

| Setting | Standard |
|---|---|
| CPU sockets | 1 |
| CPU type | `host` |
| Network model | VirtIO |
| Bridge | `vmbr0` |
| SCSI controller | VirtIO SCSI single |
| BIOS | UEFI / OVMF |
| EFI disk | Enabled |
| QEMU Guest Agent | Enabled |

The project uses a two-disk Linux VM model:

```text
SCSI 0 → OS
SCSI 1 → Role-specific data
```

The second disk is intended for `/var`, `/home`, `/tmp`, and role-specific persistent data. PostgreSQL and Docker workloads receive larger data disks. citeturn4file0L1-L2

### Principle

> VM configuration should be predictable enough that a newly created VM does not become a unique snowflake.

---

## 12. VM Lifecycle Defaults

Before creating a VM, define:

- Hostname
- Operating system
- CPU allocation
- RAM allocation
- OS disk
- Data disk
- Network placement
- VLAN where applicable
- Guest Agent requirement
- Backup requirement
- Initial administrator access

After creation:

```text
Provision
   ↓
Install OS
   ↓
Configure Network
   ↓
Configure DNS/NTP
   ↓
Apply Security Baseline
   ↓
Install Guest Agent
   ↓
Validate
   ↓
Document
```

---

## 13. Administrative Access

Administrative access should be restricted to the trusted management path.

### Web Interface

The standard management endpoint is:

```text
https://<proxmox-host>:8006/
```

Use the configured hostname rather than publishing management endpoints through an untrusted reverse proxy.

### SSH

SSH should be exposed only where operationally required.

Recommended baseline:

- Prefer key-based authentication for administrative SSH access.
- Restrict source networks where practical.
- Do not expose SSH directly to the public Internet.
- Review authentication logs.
- Keep OpenSSH patched.
- Test an alternative administrative path before making restrictive changes.

Do not make security changes that could lock out the only administrator without a recovery path.

---

## 14. Proxmox Firewall

The Proxmox firewall can provide another policy layer, but it should not be enabled or configured blindly.

The project uses OPNsense as the primary network-security enforcement point, while Proxmox host/VM firewalling can provide defense in depth.

The target security model is based on default-deny principles and explicit allowed flows. citeturn10file0L1-L2

When Proxmox firewall rules are introduced, document:

- Scope: Datacenter / Node / VM
- Source
- Destination
- Protocol
- Port
- Direction
- Logging requirement
- Reason for rule

Every rule should have an identifiable purpose.

---

## 15. Certificates and HTTPS

Proxmox management is accessed over HTTPS.

For a lab, the default certificate may be sufficient during initial setup, but certificate warnings should not simply be ignored as the permanent operational model.

Future certificate management should provide:

- Trusted certificate issuance
- Renewal process
- Private-key protection
- Monitoring of certificate expiry

The project's security architecture requires protection of private keys and prohibits committing secrets to the repository. citeturn10file0L1-L2

---

## 16. Permissions and Roles

Avoid using a single all-powerful identity for every operational task.

The target model should distinguish administrative responsibilities where practical.

Future identity integration is planned through FreeIPA and related access-control components. Until then, local Proxmox administration should still follow least privilege where the platform allows it.

Do not store administrative passwords in Git.

---

## 17. Logging

Logs are essential for troubleshooting and Day 2 operations.

At minimum, verify that the host can provide:

- Authentication events
- System events
- Service failures
- Package/update activity
- Proxmox task history
- Firewall events where configured

Useful checks include:

```bash
journalctl -p warning..alert
systemctl --failed
```

Do not assume that local logs alone constitute centralized logging. Centralized observability remains a future/planned capability in this project.

---

## 18. Backup Preparation

Before production-like workloads are introduced, define how the Proxmox environment will be backed up.

Important distinction:

```text
Snapshot ≠ Backup
Backup ≠ Restore
Successful Backup ≠ Proven Recovery
```

A future backup design should address:

- VM backup scope
- Retention
- Backup destination
- Encryption where required
- Backup verification
- Restore testing
- Recovery documentation

The Day 2 documentation standard explicitly treats restore testing as necessary evidence of recoverability.

---

## 19. Configuration Change Procedure

Changes to the Proxmox host should follow a simple change discipline:

```text
Identify reason
      ↓
Assess impact
      ↓
Record current state
      ↓
Make change
      ↓
Validate
      ↓
Record result
      ↓
Update documentation
```

For changes affecting network connectivity, storage, authentication, or the boot process, establish a recovery path before making the change.

---

## 20. Configuration Validation Checklist

### Identity

- [ ] Hostname correct
- [ ] FQDN correct
- [ ] DNS resolution verified

### Network

- [ ] Management address correct
- [ ] Gateway reachable
- [ ] `vmbr0` operational
- [ ] VM connectivity verified
- [ ] VLAN configuration validated if implemented

### Time

- [ ] Correct time zone
- [ ] NTP synchronization active
- [ ] Expected time source verified

### Packages

- [ ] Repositories reviewed
- [ ] `apt update` successful
- [ ] Host updated
- [ ] Required reboot completed

### Storage

- [ ] Storage online
- [ ] ISO storage available
- [ ] VM storage available
- [ ] Capacity reviewed
- [ ] No unexpected storage errors

### Proxmox

- [ ] Node healthy
- [ ] Web interface accessible
- [ ] No failed systemd units requiring investigation
- [ ] VM configuration standard available

### Security

- [ ] Management access restricted
- [ ] SSH exposure reviewed
- [ ] Administrative permissions reviewed
- [ ] No secrets committed to repository
- [ ] Firewall strategy documented

---

## 21. Configuration Evidence

Record the following after the baseline is established:

```text
Proxmox version:
Kernel:
Hostname:
FQDN:
Management IP:
Gateway:
DNS:
NTP source:
Storage:
Bridge:
Repository model:
Validation date:
Known deviations:
```

Do not record:

- Passwords
- Private keys
- API tokens
- Recovery secrets
- Sensitive internal credentials

Public documentation should use example values instead.

---

## 22. Day 1 Completion Criteria

The Proxmox configuration baseline is complete when:

```text
Host Identity
      ↓
Network
      ↓
DNS
      ↓
NTP
      ↓
Repositories
      ↓
Updates
      ↓
Storage
      ↓
VM Standard
      ↓
Access Control
      ↓
Security Baseline
      ↓
Validation
      ↓
Evidence
```

At that point the host is ready to support the next Day 1 component without relying on undocumented configuration.

---

## Related Documentation

- [`installation.md`](installation.md) — Proxmox installation
- [`../documentation-standard.md`](../documentation-standard.md) — Day 1 documentation standard
- [`../../architecture/overview.md`](../../architecture/overview.md) — Target architecture
- [`../../network/network.md`](../../network/network.md) — Network architecture
- [`../../security/security.md`](../../security/security.md) — Security architecture
- [`../../vm-design/vm-design.md`](../../vm-design/vm-design.md) — VM standards
- [`../../resource-matrix/vm-resource-matrix.md`](../../resource-matrix/vm-resource-matrix.md) — Resource planning
