# Proxmox VE — Installation & Initial Host Baseline

> **Day 1 — Build & Configure**

This document defines the installation and initial host baseline for Proxmox VE in the Enterprise Reference Architecture lab.

The procedure covers the transition from a bare-metal system to a usable, consistently configured Proxmox VE host. It includes installation, initial networking, hostname/DNS, time synchronization, repositories, updates, storage verification, access, and post-installation validation.

## Status

**Implemented in the laboratory:** Proxmox VE installation and use as the virtualization platform.

This document is also a **reference procedure**. Individual configuration steps are only considered validated when they have been explicitly tested in the current lab.

> **Rule:** A procedure being documented does not by itself prove that every setting has been applied in the laboratory.

---

## 1. Purpose

The Proxmox host provides the virtualization foundation for the reference architecture.

The target host is responsible for:

- Running the planned infrastructure VMs
- Providing virtual networking
- Providing VM storage
- Providing the management plane for the laboratory
- Providing a consistent platform for later Day 1 and Day 2 activities

The current physical lab reference host is a Dell Latitude 5540 with 32 GiB RAM and a 512 GB NVMe SSD. The hardware is a practical lab platform, not a production server specification.

---

## 2. Prerequisites

### 2.1 Hardware

Recommended baseline for this lab:

| Resource | Reference |
|---|---|
| CPU | 64-bit Intel/AMD processor with hardware virtualization |
| RAM | 32 GiB in current lab |
| Storage | 512 GB NVMe in current lab |
| Network | At least one reliable network interface |
| Firmware | UEFI |

Proxmox VE's official documentation recommends the ISO installer for new installations and requires a 64-bit CPU with hardware virtualization support for KVM workloads. citeturn0search0

### 2.2 Before Installation

Confirm:

- [ ] Proxmox VE installation ISO is available
- [ ] Important data has been backed up
- [ ] The target disk has been identified
- [ ] Hardware virtualization is enabled in firmware
- [ ] Boot mode is set to UEFI
- [ ] Network connection is available
- [ ] A management IP plan exists
- [ ] Hostname/FQDN has been decided
- [ ] DNS records or local name resolution can be provided
- [ ] Time zone has been decided
- [ ] NTP source has been decided

> **Important:** The installation target disk will normally be repartitioned by the installer. Do not use the procedure against a disk containing data that must be preserved.

---

## 3. Firmware Baseline

Before booting the installer, review the system firmware.

### 3.1 UEFI

Use UEFI boot mode rather than legacy BIOS when supported by the hardware.

### 3.2 CPU Virtualization

Ensure the processor's hardware virtualization capability is enabled.

For Intel systems this is normally exposed as Intel Virtualization Technology (VT-x). Additional I/O virtualization features such as VT-d may also be enabled when supported and useful for future workloads.

### 3.3 Boot Order

Temporarily place the installation media before the target disk in the boot order.

After installation, return the internal disk to the normal boot position.

### 3.4 Firmware Updates

Firmware should be reasonably current before the host enters regular operation. Firmware updates should be treated as a controlled maintenance activity rather than performed blindly during the operating-system installation.

---

## 4. Installation Media

Use the official Proxmox VE ISO installer.

The ISO installation method is the recommended installation path for new installations. The installer includes the underlying Debian system and required Proxmox VE packages. citeturn0search0

### Installation Flow

```text
Boot ISO
  ↓
Accept License
  ↓
Select Target Disk
  ↓
Select Location / Time Zone / Keyboard
  ↓
Configure Management Network
  ↓
Create Initial Administrator Password
  ↓
Review Configuration
  ↓
Install
  ↓
Reboot
```

---

## 5. Installer Configuration

### 5.1 Target Disk

Select the intended system disk.

For the current lab, the primary NVMe device is the Proxmox host storage device.

The exact partitioning/storage design should be chosen according to the actual hardware and future storage requirements. Do not document an exact partition layout as implemented unless it has been verified on the host.

### 5.2 Location and Time Zone

Select the actual laboratory time zone and appropriate keyboard layout.

Correct time zone configuration is important for readable logs and operational troubleshooting, but it is not a replacement for network time synchronization.

### 5.3 Hostname

Use a stable, role-based hostname.

Example:

```text
pve01.corp.example.com
```

`corp.example.com` is a documentation-only domain used by this project. Replace it with the actual internal domain when implementing the lab.

The hostname should not be changed casually after the host has entered service.

### 5.4 Management Network

Configure the primary management interface with:

- Static management address where appropriate
- Correct subnet mask/prefix
- Correct default gateway
- Correct DNS resolver(s)
- Correct hostname/FQDN

Example reference:

```text
Hostname: pve01.corp.example.com
IP:       10.10.10.10/24
Gateway:  10.10.10.1
DNS:      10.10.10.1
```

> The addresses above are reference values only. They must not be interpreted as the current laboratory addressing unless separately validated.

---

## 6. First Boot

After installation:

1. Remove the installation media.
2. Boot the Proxmox host.
3. Confirm the host reaches the login prompt.
4. Confirm the management interface is available.
5. Connect to the Proxmox web interface from the management workstation.

The normal web management endpoint is:

```text
https://<proxmox-host>:8006/
```

Use the hostname or management IP that was actually configured.

---

## 7. Hostname and DNS Verification

The host must have consistent local hostname resolution and a usable FQDN.

Check the configured hostname:

```bash
hostnamectl
hostname -f
```

Check local name resolution:

```bash
getent hosts pve01.corp.example.com
```

Check DNS resolution:

```bash
getent hosts example.com
```

The exact public test domain is only an example. Use a trusted resolver and an appropriate internal record during the actual lab validation.

### Validation Criteria

- [ ] Short hostname is correct
- [ ] FQDN is correct
- [ ] Host can resolve its own name
- [ ] DNS resolver is reachable
- [ ] External DNS resolution works where required
- [ ] Forward and reverse DNS are consistent where internal DNS supports it

---

## 8. Time Synchronization / NTP

Correct system time is a foundational infrastructure requirement.

Time affects:

- TLS certificate validation
- Authentication systems
- Kerberos in future FreeIPA deployment
- Log correlation
- Cluster operations
- Monitoring
- Troubleshooting

Do not treat the manually selected installer time as sufficient operational time synchronization.

### 8.1 Verify Current Time

```bash
timedatectl
```

Check that:

- The configured time zone is correct.
- The system clock is synchronized.
- A valid time synchronization service is active.

### 8.2 NTP Source

The lab should use an explicitly defined NTP source.

Possible architecture choices include:

1. A trusted internal NTP source
2. A controlled upstream NTP service
3. A future dedicated infrastructure time service

The project should use one clearly defined source rather than configuring different hosts independently without an operational standard.

### 8.3 Validation

Example checks:

```bash
timedatectl status
```

If the selected time service provides a detailed synchronization command, use the corresponding tool to verify the active peer/source.

Validation must establish that synchronization is actually working rather than merely that an NTP configuration exists.

---

## 9. Repository Configuration

After installation, verify the configured Proxmox package repositories.

The repository configuration must match the intended support/subscription model for the lab.

Do not leave a production-oriented repository configuration in place if the environment is intentionally using the no-subscription repository model, and do not mix repository definitions without understanding their support implications.

### Verification

Review the configured repositories and confirm that:

- [ ] Required Proxmox repository is enabled
- [ ] Unsupported/unintended repository entries are absent
- [ ] Debian base repositories are appropriate for the installed Proxmox release
- [ ] Repository configuration is internally consistent

> Repository configuration is release-specific. Always use the repository definitions appropriate for the installed Proxmox VE version rather than copying an old configuration from another release.

---

## 10. Initial System Update

Before creating the first production-like workloads, update the host through the supported package-management mechanism.

Typical Debian/Proxmox package commands include:

```bash
apt update
apt full-upgrade
```

Review the proposed changes before confirming them.

After the update:

- Reboot when required.
- Confirm the host returns cleanly.
- Confirm the Proxmox services are healthy.
- Re-check network connectivity.
- Re-check time synchronization.

### Update Principle

> The host should enter regular operation from a known and maintained package state.

---

## 11. Proxmox Web Interface Baseline

After first login, review the node configuration through the web interface.

Verify:

- Node name
- System time
- Network interfaces
- DNS configuration
- Repositories
- Storage definitions
- System updates
- Task history
- Node health

The web interface is the primary administrative interface for the lab, but command-line verification should be used where it provides stronger evidence.

---

## 12. Network Baseline

The host should use a dedicated management network design.

The reference architecture reserves **VLAN 10** for management, but VLAN segmentation remains **Planned** until configured and validated in the laboratory. citeturn5file0L1-L2

The target architecture is:

```text
Management Network
       |
     vmbr0
       |
    Proxmox
       |
  Management Access
```

When VLAN segmentation is implemented, management traffic should be explicitly assigned to the management segment and protected by the firewall policy.

### Do Not Assume

The existence of `vmbr0` does not mean VLAN segmentation is implemented.

The repository distinguishes the current Proxmox implementation from the planned network architecture. citeturn11file0L1-L2

---

## 13. Storage Baseline

Review the Proxmox storage configuration before creating VMs.

Confirm:

- [ ] Local storage is available
- [ ] ISO storage is available
- [ ] VM disk storage is available
- [ ] Expected capacity is available
- [ ] Storage content types are appropriate
- [ ] No unexpected storage errors are reported

The project uses a two-disk VM design for Linux workloads:

```text
SCSI 0 → Operating System
SCSI 1 → Role-specific Data
```

The VM design specifies a 20 GiB baseline OS disk and a second disk for `/var`, `/home`, `/tmp`, and role-specific data, with larger data disks for PostgreSQL and Docker workloads. citeturn4file0L1-L2

This is a **VM design standard**, not a requirement to repartition the Proxmox host itself in the same way.

---

## 14. Initial Security Baseline

The host should be brought into a secure baseline before it becomes a dependency for additional infrastructure.

### 14.1 Administrative Access

Use a dedicated administrative identity model appropriate for the lab.

Avoid sharing administrative credentials between people.

Do not place passwords, API tokens, private keys, or other secrets in the Git repository.

### 14.2 Management Exposure

Administrative access should be limited to the trusted management path.

The target architecture follows least privilege, Zero Trust, Zero Plaintext, and defense-in-depth principles. citeturn10file0L1-L2

### 14.3 SSH

SSH should only be enabled and exposed as required.

When SSH is used operationally:

- Use key-based authentication where appropriate.
- Restrict access to trusted management sources.
- Avoid unnecessary exposure to untrusted networks.
- Keep the service patched.
- Review authentication logs.

Do not disable an access method until an alternative administrative path has been tested.

### 14.4 Updates

Keep the Proxmox host maintained through its supported update process.

Security maintenance belongs to both Day 1 and Day 2. Installation creates the baseline; ongoing patch management maintains it.

---

## 15. QEMU Guest Agent — VM Standard

The QEMU Guest Agent should be enabled for supported guest VMs according to the project's VM standard.

It improves Proxmox's ability to interact with the guest operating system for supported operations such as obtaining guest information and performing coordinated actions.

This setting belongs to the **VM configuration stage**, not the bare-metal Proxmox installation itself.

---

## 16. Cluster Considerations

The current lab is based on a single Proxmox host.

Do not configure a Proxmox cluster simply because the target architecture may eventually include multiple nodes.

A future multi-node design may include:

- Multiple Proxmox nodes
- Quorum
- Shared or distributed storage
- High availability
- Cluster networking
- Dedicated migration traffic

These capabilities are outside the current single-host implementation stage.

---

## 17. Post-Installation Validation

The host should not be considered Day 1 complete until the following checks pass.

### Host

- [ ] Proxmox boots normally
- [ ] Node name is correct
- [ ] CPU virtualization is available
- [ ] Expected RAM is visible
- [ ] Expected storage is visible

### Network

- [ ] Management interface is up
- [ ] Management IP is correct
- [ ] Default gateway is reachable
- [ ] DNS resolution works
- [ ] Proxmox web interface is reachable

### Time

- [ ] Correct time zone
- [ ] Clock synchronized
- [ ] Expected NTP source active

### Package Management

- [ ] Repository configuration reviewed
- [ ] Package metadata refresh succeeds
- [ ] System is updated
- [ ] Required reboot completed if applicable

### Proxmox

- [ ] Node appears healthy
- [ ] Storage is available
- [ ] ISO storage is available
- [ ] VM storage is available
- [ ] No unexpected critical task errors

### Security

- [ ] Administrative access tested
- [ ] Unnecessary exposure avoided
- [ ] Secrets are not stored in repository files
- [ ] Management access path is understood

---

## 18. Evidence to Record

For a reproducible lab, record enough evidence to demonstrate that the baseline was actually established.

Recommended evidence:

```text
Hostname / FQDN
Management IP
Gateway
DNS resolver
NTP source
Proxmox version
Kernel version
Repository model
Storage configuration
Network configuration
Validation results
Known deviations
```

Sensitive information such as passwords, private keys, API tokens, and secrets must never be committed as evidence.

---

## 19. Known Lab Status

The repository currently identifies **Proxmox VE as Implemented** and OPNsense as an implemented VM. The broader VLAN segmentation, FreeIPA, PostgreSQL, Docker platform, and automation layers remain planned until separately implemented and validated. citeturn7file0L1-L2

Therefore this document should be read in two ways:

1. As documentation of the Proxmox installation baseline that has been established in the project.
2. As the standard procedure that future re-installations or additional Proxmox hosts should follow.

Any deviation from this procedure should be documented rather than silently becoming a new undocumented standard.

---

## 20. Day 1 Completion Criteria

Proxmox installation is considered **Day 1 complete** when:

```text
Installation
    ↓
Hostname / DNS
    ↓
Management Network
    ↓
Time Synchronization
    ↓
Repository Configuration
    ↓
System Update
    ↓
Storage Verification
    ↓
Security Baseline
    ↓
Validation
    ↓
Evidence Recorded
```

> **Installation is not the finish line. A Proxmox host becomes a usable infrastructure foundation only after its management, networking, time, package state, storage, security baseline, and validation have been established.**

## Related Documentation

- [`../../architecture/overview.md`](../../architecture/overview.md) — Target architecture
- [`../../network/network.md`](../../network/network.md) — Network architecture
- [`../../security/security.md`](../../security/security.md) — Security architecture
- [`../../vm-design/vm-design.md`](../../vm-design/vm-design.md) — VM design standard
- [`../../resource-matrix/vm-resource-matrix.md`](../../resource-matrix/vm-resource-matrix.md) — Resource planning
- [`../documentation-standard.md`](../documentation-standard.md) — Day 1 documentation standard
