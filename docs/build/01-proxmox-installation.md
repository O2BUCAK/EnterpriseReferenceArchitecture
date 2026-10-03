# Proxmox VE — Build & Reinstallation Runbook

> **Build — 01**
>
> This document is the reproducible installation procedure for the Proxmox VE foundation of the Enterprise Reference Architecture.

## 1. Purpose

Use this runbook to build a Proxmox VE host from bare metal and prepare it for the project's virtual infrastructure.

The result of this procedure is a Proxmox host that is:

- bootable and updated;
- reachable through its management network;
- correctly identified by hostname/DNS;
- synchronized to the project's time source;
- ready to create the project's VMs;
- aligned with the VM, network and security standards documented in this repository.

This document is intentionally more procedural than the existing Day-1 reference documentation. It is written so that a technician who has not previously built this laboratory can follow the sequence from beginning to end.

## 2. Relationship to the Architecture

The Proxmox host is the foundation of the target platform:

```text
Physical Host
    |
    v
Proxmox VE
    |
    +-- fw01    OPNsense
    +-- ipa01   Fedora / FreeIPA
    +-- db01    Pardus / PostgreSQL / Redis
    +-- app01   Ubuntu / Docker
    +-- auto01  RHEL / Ansible / OpenTofu
```

Current repository status is important:

- Proxmox VE is implemented in the laboratory.
- `fw01` is implemented.
- `ipa01`, `db01`, `app01` and `auto01` are architectural targets and must not be described as implemented until installed and validated.

See [VM Design](../vm-design/vm-design.md).

## 3. Required Reading

Before starting, read:

1. [Architecture Overview](../architecture/overview.md)
2. [Network Architecture](../network/network.md)
3. [VM Design](../vm-design/vm-design.md)
4. [VM Resource Matrix](../resource-matrix/vm-resource-matrix.md)
5. [Security Architecture](../security/security.md)
6. [Existing Day-1 Proxmox Installation Reference](../day-1/proxmox/installation.md)
7. [Existing Proxmox Configuration Baseline](../day-1/proxmox/configuration.md)
8. [Proxmox Validation](../day-1/proxmox/validation.md)

The existing Day-1 documents contain the project's reference baseline. This runbook converts that baseline into a clean rebuild sequence.

## 4. Prerequisites

### 4.1 Hardware

The current laboratory reference host is:

| Item | Reference |
|---|---|
| Host | Dell Latitude 5540 |
| CPU | Intel Core i7-1355U |
| RAM | 32 GiB |
| Storage | 512 GB NVMe |
| Hypervisor | Proxmox VE |

The hardware is a laboratory platform, not a production-server specification.

### 4.2 Required Materials

Prepare:

- Proxmox VE ISO appropriate for the release being deployed;
- a USB installation medium or supported boot mechanism;
- the physical host;
- a network connection;
- access to the management network;
- the intended management IP information;
- the intended hostname/FQDN;
- the intended DNS resolver;
- the intended NTP source;
- the repository version/commit that is being reproduced.

Do not invent an IP address merely to make the installation continue. If the address has not been decided, stop and obtain the value from the network design.

### 4.3 Data Warning

The Proxmox installation can repartition/erase the selected installation disk.

**Do not start installation until the target disk has been positively identified and any required data has been backed up.**

## 5. Project Network Values

The repository defines the following **reference network model**:

| VLAN | Purpose | Network | Gateway |
|---:|---|---|---|
| 10 | Management | `10.10.10.0/24` | `10.10.10.1` |
| 20 | Identity | `10.10.20.0/24` | `10.10.20.1` |
| 30 | Database | `10.10.30.0/24` | `10.10.30.1` |
| 40 | Application | `10.10.40.0/24` | `10.10.40.1` |

**Important:** the repository explicitly marks this VLAN/IP model as planned until it is configured and validated in the laboratory.

The reference examples include:

| Host | Role | Reference IP |
|---|---|---|
| `fw01` | OPNsense | `10.10.10.1` |
| `ipa01` | FreeIPA | `10.10.20.10` |
| `db01` | PostgreSQL | `10.10.30.10` |
| `app01` | Docker | `10.10.40.10` |
| `auto01` | Automation | `10.10.10.20` |

These are **reference values**, not proof of the live laboratory configuration.

## 6. Installation Sequence

Follow this order:

```text
1. Verify hardware
       |
2. Verify ISO
       |
3. Configure firmware
       |
4. Boot Proxmox installer
       |
5. Install Proxmox
       |
6. Configure management network
       |
7. First boot
       |
8. Verify hostname/DNS
       |
9. Configure time synchronization
       |
10. Configure repositories
       |
11. Update host
       |
12. Verify storage
       |
13. Configure/verify management network
       |
14. Apply security baseline
       |
15. Run validation
       |
16. Record evidence
       |
17. Proceed to OPNsense
```

Do not proceed to VM deployment if the host-level validation fails.

# 7. Step-by-Step Installation

## 7.1 Verify the Installation ISO

Obtain the Proxmox VE ISO from the official Proxmox distribution channel.

Verify the downloaded checksum against the checksum published for the exact ISO.

On Windows PowerShell:

```powershell
Get-FileHash .\proxmox-ve-<version>.iso -Algorithm SHA256
```

On Linux:

```bash
sha256sum proxmox-ve-<version>.iso
```

Compare the result character-for-character with the published checksum.

**Expected result:** the calculated SHA-256 matches the official checksum for the exact file.

Do not continue with an unverified ISO.

## 7.2 Prepare the Boot Medium

Write the verified ISO to the installation medium using a trusted imaging tool.

If Ventoy is used, copy the verified ISO to the Ventoy data partition and boot the ISO from Ventoy.

The installation medium is only a temporary boot mechanism. Remove it after installation so the machine boots from the installed system.

## 7.3 Configure Firmware

Enter the host's UEFI/firmware setup.

Verify:

- UEFI boot mode is enabled;
- CPU hardware virtualization is enabled;
- Intel VT-x/AMD-V is enabled where applicable;
- I/O virtualization such as VT-d/IOMMU can be enabled where supported and required;
- the installation medium is available in the boot order.

Do not change unrelated firmware settings without a reason.

Save the changes and boot from the Proxmox installation medium.

## 7.4 Start the Proxmox Installer

At the Proxmox boot menu, select the normal installation option.

Proceed through the license screen.

When asked for the installation disk, select the **intended Proxmox system disk**.

### Disk decision

The current lab reference host uses a 512 GB NVMe device.

The repository's two-disk standard applies to **Linux guest VMs**. It does not mean that the Proxmox host must contain two disks.

Do not create an artificial third-disk design merely to satisfy the VM standard.

## 7.5 Select Location and Keyboard

Select:

- the actual country/locale;
- the correct time zone;
- the keyboard layout used by the administrator.

**Expected result:** the installer displays the expected local time and keyboard layout.

## 7.6 Configure the Proxmox Host Identity

Enter a stable hostname/FQDN.

Use the repository's actual naming standard and the hostname that has been assigned to the physical host.

Example format:

```text
pve01.<internal-domain>
```

Do not copy `corp.example.com` from an example into the real environment.

The repository uses placeholder domains in public documentation.

## 7.7 Configure the Management Network

The installer will request:

- management interface;
- IP address;
- CIDR/prefix;
- gateway;
- DNS server;
- hostname/FQDN.

For the reference architecture, management belongs to VLAN 10.

Reference network:

```text
VLAN:       10
Network:    10.10.10.0/24
Gateway:    10.10.10.1
```

The actual Proxmox management address must be the address assigned to the physical host.

**Do not assign `10.10.10.1` to Proxmox if `fw01` is using that address as the gateway.**

This distinction matters:

```text
10.10.10.1       -> reference gateway / fw01
10.10.10.x       -> Proxmox management host
```

## 7.8 Set the Initial Administrator Password

Create the initial Proxmox administrative credential.

Use a unique, strong credential.

Do not:

- put the password in Git;
- put the password in this document;
- reuse a password from another system;
- send the password through an unprotected channel.

If the project later adopts an external identity/administrative access mechanism for Proxmox, migrate to that model deliberately and validate the alternative access path before disabling the original one.

## 7.9 Review the Installer Summary

Before selecting **Install**, verify:

- target disk;
- hostname/FQDN;
- management interface;
- IP address;
- gateway;
- DNS;
- time zone;
- keyboard layout.

If any value is wrong, go back and correct it.

## 7.10 Complete Installation

Start the installation.

Wait until the installer reports completion.

Remove the installation medium.

Reboot.

**Expected result:** the machine boots from the installed Proxmox system and reaches the local login prompt.

# 8. First Boot

Log in locally once to confirm that the host is functional.

Run:

```bash
hostnamectl
ip addr
ip route
timedatectl
```

Record the output as installation evidence if required.

## 8.1 Verify the Hostname

Run:

```bash
hostnamectl
hostname -f
```

The FQDN must match the hostname assigned during installation.

## 8.2 Verify Network Connectivity

Run:

```bash
ip addr
ip route
ping -c 3 <gateway>
```

Then test DNS:

```bash
getent hosts <internal-dns-name>
getent hosts example.com
```

Replace the placeholders with actual values.

**Expected result:**

- management interface is UP;
- expected IP is present;
- default route exists;
- gateway is reachable;
- DNS queries return expected results.

## 8.3 Open the Web Interface

From an approved management workstation:

```text
https://<proxmox-management-address>:8006/
```

Do not expose port 8006 directly to the Internet.

The repository's target policy treats Proxmox administration as a management-plane service.

# 9. Configure Time Synchronization

Correct time is required before deploying identity services, because FreeIPA/Kerberos depends on consistent system time.

Check:

```bash
timedatectl
```

The repository's operational environment has previously used Chrony/NTP as the time-synchronization model.

If Chrony is the selected implementation, verify it with:

```bash
chronyc tracking
chronyc sources -v
```

The actual NTP source must come from the environment's approved time-service design.

**Expected result:**

- correct time zone;
- clock synchronized;
- expected NTP source reachable;
- no unexplained large offset.

Do not mark NTP as configured merely because a service is installed. Validate synchronization.

# 10. Configure Package Repositories

Repository configuration is release-specific.

Use only repository definitions appropriate for the exact Proxmox VE release being installed.

Do not blindly copy a repository configuration from an older Proxmox release.

Verify configured repositories before updating:

```bash
grep -R "^[^#].*deb " /etc/apt/sources.list /etc/apt/sources.list.d/ 2>/dev/null
```

Then:

```bash
apt update
```

Review errors carefully.

**Expected result:** package metadata refresh completes without repository errors.

# 11. Update Proxmox

Run:

```bash
apt full-upgrade
```

Review the packages before accepting the changes.

If the update requires a reboot:

```bash
reboot
```

After reboot, repeat:

```bash
pveversion
timedatectl
ip addr
ip route
```

Then reconnect to the web interface.

# 12. Verify Proxmox Services

Check the core service state:

```bash
systemctl --failed
systemctl status pveproxy
systemctl status pvedaemon
systemctl status pvestatd
```

If a service is failed, do not continue blindly. Investigate the failure first.

**Expected result:** no unexpected failed Proxmox services.

# 13. Verify Storage

From the shell:

```bash
pvesm status
lsblk
df -h
```

From the Web UI:

**Datacenter → Storage**

Verify that the expected storage definitions exist and are available for their intended content types.

The project VM standard expects:

```text
Linux VM
 |
 +-- SCSI 0 -> OS
 |
 +-- SCSI 1 -> role-specific data
```

This is a **guest VM standard**, not the physical Proxmox disk layout.

# 14. Establish the VM Creation Standard

Before creating project VMs, use the following reference baseline from the repository.

| Setting | Standard |
|---|---|
| Guest type | Linux |
| Machine | q35 |
| BIOS | OVMF / UEFI |
| EFI disk | Enabled |
| SCSI controller | VirtIO SCSI single |
| QEMU Guest Agent | Enabled |
| CPU sockets | 1 |
| CPU type | host |
| Network model | VirtIO |
| Bridge | vmbr0 |
| OS disk | SCSI 0 |
| Data disk | SCSI 1 |

Reference VM sizing:

| VM | vCPU | RAM | OS | Data | VLAN |
|---|---:|---:|---:|---:|---:|
| `fw01` | 2 | 4 GiB | appliance | 40 GiB | management/uplink |
| `ipa01` | 2 | 2 GiB | 20 GiB | 20 GiB | 20 |
| `db01` | 4 | 8 GiB | 20 GiB | 50 GiB | 30 |
| `app01` | 4 | 10 GiB | 20 GiB | 50 GiB | 40 |
| `auto01` | 2 | 4 GiB | 20 GiB | 20 GiB | 10 |

These are reference allocations. Increase resources only when testing or observed workload justifies it.

# 15. Network Design Before VM Creation

The target topology is:

```text
                    Internet
                       |
                    OPNsense
                      fw01
                       |
                 VLAN-aware network
                       |
       +---------------+---------------+---------------+
       |               |               |               |
    VLAN 10         VLAN 20         VLAN 30         VLAN 40
  Management        Identity        Database       Application
       |               |               |               |
     auto01           ipa01           db01           app01
```

The repository currently describes these VLANs as planned until actually configured and validated.

Therefore:

**Do not configure VLAN 20/30/40 on the host merely because this document contains their reference values.**

The correct implementation sequence is:

1. Build Proxmox.
2. Build `fw01`.
3. Configure and validate the network foundation.
4. Then attach subsequent VMs to their intended VLANs.

# 16. Security Baseline

Before treating the host as the infrastructure foundation:

### Administrative access

- Use dedicated administrative identities.
- Do not share credentials.
- Do not commit credentials to Git.
- Restrict management access to the management path.

### Network exposure

The target policy is:

```text
Internet
   X
   |
Proxmox / OPNsense / SSH management
```

Management services should not be directly exposed to WAN.

### Firewall

The target architecture follows default-deny and explicit-flow principles.

A network rule should identify:

```text
Source
  +
Destination
  +
Protocol
  +
Port
  +
Reason
```

Do not open a port just because an application documentation page lists it.

# 17. QEMU Guest Agent

Enable QEMU Guest Agent for supported project VMs.

For a Linux guest, the agent must also be installed and enabled inside the guest.

The sequence is:

```text
Proxmox VM option
       +
Guest package/service
       |
       v
QEMU Guest Agent operational
```

Validate the guest-agent state before depending on guest-aware Proxmox operations.

# 18. Proxmox Host Validation

Run all checks before declaring the installation complete.

## 18.1 Identity

```bash
hostnamectl
hostname -f
```

- [ ] Hostname correct
- [ ] FQDN correct
- [ ] Name resolution works

## 18.2 Network

```bash
ip addr
ip route
```

- [ ] Management interface UP
- [ ] Correct IP
- [ ] Correct prefix
- [ ] Correct gateway
- [ ] DNS works

## 18.3 Time

```bash
timedatectl
chronyc tracking
chronyc sources -v
```

- [ ] Correct timezone
- [ ] Synchronized
- [ ] Expected source available

## 18.4 Package State

```bash
apt update
pveversion
```

- [ ] Repository refresh succeeds
- [ ] No unintended repository errors
- [ ] Expected Proxmox version installed

## 18.5 Services

```bash
systemctl --failed
systemctl status pveproxy pvedaemon pvestatd
```

- [ ] No unexpected failed services
- [ ] Web/API services operational

## 18.6 Storage

```bash
pvesm status
lsblk
df -h
```

- [ ] Expected storage visible
- [ ] Storage has sufficient free space
- [ ] VM disk creation is possible

## 18.7 Web Access

From the management workstation:

```text
https://<proxmox-management-address>:8006/
```

- [ ] Login succeeds
- [ ] Correct node is visible
- [ ] Storage is visible
- [ ] No unexplained critical task failures

# 19. Failure Handling

If a validation step fails:

1. Stop.
2. Record the command and complete output.
3. Identify whether the failure is hardware, network, DNS, time, repository, storage or Proxmox related.
4. Correct the root cause.
5. Repeat the failed validation.
6. Record the deviation if the final configuration differs from the reference design.

Do not hide a deviation by changing the documentation to match an unreviewed implementation.

# 20. Evidence Record

After successful validation, record:

```text
Host:
Hostname:
FQDN:
Proxmox version:
Kernel:
Management interface:
Management IP:
Gateway:
DNS:
NTP source:
Storage:
Repository model:
Installation date:
Repository commit reproduced:
Known deviations:
Validation result:
```

Never record:

- passwords;
- private keys;
- API tokens;
- recovery codes;
- other secrets.

# 21. Completion Criteria

Proxmox is ready for the next build stage only when:

```text
[ ] Installation completed
[ ] Correct disk selected
[ ] Hostname/FQDN verified
[ ] Management network verified
[ ] DNS verified
[ ] Time synchronization verified
[ ] Repositories verified
[ ] System updated
[ ] Proxmox services healthy
[ ] Storage verified
[ ] Security baseline applied
[ ] Validation evidence recorded
```

Then proceed to:

**02 — OPNsense Installation**

The next component must be installed and validated before relying on the planned VLAN segmentation for `ipa01`, `db01`, `app01` and `auto01`.

# 22. Related Documents

- [Architecture Overview](../architecture/overview.md)
- [Network Architecture](../network/network.md)
- [Port Map](../network/port-map.md)
- [VM Design](../vm-design/vm-design.md)
- [VM Resource Matrix](../resource-matrix/vm-resource-matrix.md)
- [Security Architecture](../security/security.md)
- [Proxmox Day-1 Installation Reference](../day-1/proxmox/installation.md)
- [Proxmox Day-1 Configuration](../day-1/proxmox/configuration.md)
- [Proxmox Validation](../day-1/proxmox/validation.md)
- [OPNsense Installation](../day-1/opnsense/installation.md)
- [Day-1 Build Index](../day-1/index.md)

---

## Implementation Status

This file is a **Build/Reinstallation Runbook**.

It does not change the implementation status of any component. A procedure being documented is not evidence that the corresponding configuration has been implemented or validated in the laboratory.
