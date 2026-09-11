# FreeIPA — Installation

> **Day 1 — Install**

This document defines the planned installation procedure for the FreeIPA identity platform used by the Enterprise Reference Architecture.

## Status

**Planned.** FreeIPA has not yet been installed or validated in the laboratory.

The target identity host is `ipa01`, planned on VLAN 20. The network segmentation itself is also currently planned. Do not treat the reference IP address, hostname, or DNS model below as evidence of an existing deployment.

---

## 1. Purpose

FreeIPA will provide the FOSS-first identity foundation for the lab, including:

- Identity management
- Authentication
- Authorization foundations
- Kerberos
- LDAP directory services
- Host enrollment
- Certificate services where required
- DNS integration where appropriate
- Centralized identity administration

FreeIPA is intended to become the primary Linux identity service for the reference architecture.

---

## 2. Target Host

| Attribute | Reference value |
|---|---|
| Hostname | `ipa01` |
| Role | FreeIPA Identity Server |
| OS | Fedora Server |
| VLAN | 20 — Identity |
| Example IP | `10.10.20.10` |
| Example FQDN | `ipa01.corp.example.com` |
| vCPU | 2 |
| RAM | 2 GiB |
| OS disk | 20 GiB |
| Data disk | 20 GiB |
| Status | Planned |

`corp.example.com` and the IP address are documentation examples only.

---

## 3. Prerequisites

### Infrastructure

- Proxmox VM capability is operational.
- `fw01` is operational.
- The Identity VLAN exists and has been validated, or an equivalent temporary test network is explicitly documented.
- DNS is available for the installation process.
- NTP/time synchronization is available.
- The VM has stable network connectivity.

### FreeIPA Requirements

Before installation, determine:

- Fully qualified hostname
- DNS domain
- Kerberos realm
- Static IP address
- Reverse DNS requirement
- Forward DNS ownership
- NTP source
- Administrative recovery procedure

Time synchronization is particularly important because Kerberos authentication is time-sensitive.

---

## 4. VM Preparation

Create `ipa01` using the project's two-disk Linux VM standard.

Reference:

```text
CPU:       2 vCPU
RAM:       2 GiB
OS disk:   20 GiB
Data disk: 20 GiB
NIC:       VirtIO
Bridge:    vmbr0
Firmware:  UEFI / OVMF
SCSI:      VirtIO SCSI Single
QEMU GA:   Enabled
```

The final VLAN tag should be applied only after the network segmentation layer is implemented.

---

## 5. Operating System Installation

Install the supported Fedora Server release selected for the lab.

During installation:

1. Configure the correct timezone.
2. Configure keyboard/layout.
3. Use the intended hostname.
4. Configure the OS disk according to the VM standard.
5. Prepare the second disk for role-specific data where required.
6. Create the administrative account.
7. Enable networking.
8. Install only required packages initially.

Do not expose the server directly to the Internet for convenience.

---

## 6. Hostname Configuration

The server must use a stable FQDN before FreeIPA installation.

Reference:

```text
Hostname: ipa01
FQDN:     ipa01.corp.example.com
```

Verify:

```bash
hostnamectl
hostname --fqdn
getent hosts ipa01.corp.example.com
```

The returned values must match the final DNS design.

---

## 7. Network Configuration

Configure a stable address for `ipa01`.

Reference:

```text
Address:  10.10.20.10/24
Gateway:  10.10.20.1
```

Do not copy the example values blindly into the production/lab configuration. Record the actual assigned values in the implementation evidence.

Validate:

```bash
ip address
ip route
ping -c 4 <gateway>
```

---

## 8. DNS Preparation

FreeIPA depends heavily on correct DNS behavior.

Before installation, confirm:

- Forward lookup for the FreeIPA hostname works.
- Reverse lookup is planned and available where required.
- The chosen DNS server is authoritative for the required internal namespace, or the required records can be created there.
- No conflicting DNS ownership exists.

Example checks:

```bash
getent hosts ipa01.corp.example.com
host ipa01.corp.example.com
host <ipa01-ip>
```

Do not proceed with an inconsistent hostname/DNS configuration merely to complete the installer.

---

## 9. Time Synchronization

Configure NTP/chrony before installing FreeIPA.

Verify:

```bash
timedatectl
chronyc tracking
chronyc sources -v
```

The host should report synchronized time against the lab's intended NTP source.

Record the actual source in the implementation evidence.

---

## 10. Package Preparation

Update the operating system before installing FreeIPA packages.

Recommended sequence:

```text
Repository configuration
        ↓
System update
        ↓
Reboot if required
        ↓
Verify hostname
        ↓
Verify DNS
        ↓
Verify time
        ↓
Install FreeIPA packages
```

Avoid installing unrelated services on the identity server.

---

## 11. FreeIPA Package Installation

Install the FreeIPA server components required by the selected deployment model.

The exact package names and installation method should follow the supported Fedora release documentation selected for the lab.

After package installation, verify that the expected FreeIPA installer is available before proceeding.

Do not mark FreeIPA as installed in the project status merely because the packages are present.

---

## 12. FreeIPA Server Deployment

Run the supported FreeIPA server installation procedure using the final:

- Hostname
- Domain
- Kerberos realm
- DNS design
- NTP design
- Administrator credentials

Reference naming model:

```text
Host:   ipa01.corp.example.com
Domain: corp.example.com
Realm:  CORP.EXAMPLE.COM
```

These values are examples and must be replaced with the final documented lab values if the architecture changes.

Credentials must never be committed to GitHub.

---

## 13. DNS Integration

If FreeIPA is selected to provide authoritative internal DNS, configure the DNS role as part of the deployment.

If an existing DNS service remains authoritative, document the delegation/forwarding arrangement instead.

The final architecture must have one clearly defined owner for internal identity-related DNS records.

---

## 14. Initial Administrative Validation

After installation, verify that:

- FreeIPA services start successfully.
- The server hostname is correct.
- Kerberos is operational.
- LDAP is operational.
- DNS behavior is correct if FreeIPA DNS is enabled.
- The administrative interface is reachable from the intended management path.

The installation is not complete until these checks pass.

---

## 15. Initial Security Baseline

Immediately after installation:

- Change any temporary/bootstrap credentials where applicable.
- Use strong administrative credentials.
- Restrict administrative access to trusted management paths.
- Do not expose LDAP/Kerberos administration services to untrusted networks.
- Enable only required services.
- Confirm host firewall policy.
- Confirm time synchronization.
- Establish a backup plan before significant identity data is created.

Secrets must remain outside the repository.

---

## 16. First Host Enrollment Preparation

The first enrolled Linux client should be a controlled test system.

Target flow:

```text
ipa01
  |
  | DNS / Kerberos / LDAP
  v
Test Linux client
```

Do not begin broad client enrollment until the identity server has passed its own validation tests.

---

## 17. Evidence

Record:

```text
VM ID:
Hostname:
FQDN:
OS release:
FreeIPA version:
IP address:
Gateway:
DNS servers:
NTP source:
Kerberos realm:
DNS ownership:
Installation date:
Configuration deviations:
Validation reference:
```

Capture screenshots only where they add useful evidence. Avoid storing credentials, private keys, or sensitive exports.

---

## 18. Installation Completion Criteria

FreeIPA installation can be considered **Installed** when:

1. `ipa01` exists as the intended VM.
2. The operating system is installed.
3. Hostname and FQDN are correct.
4. Network configuration is stable.
5. DNS prerequisites are satisfied.
6. Time synchronization is operational.
7. FreeIPA server components are installed.
8. The FreeIPA server deployment completes successfully.
9. Core FreeIPA services start correctly.
10. Initial administrative access works.
11. Evidence is recorded.

It can only be marked **Validated** after the dedicated validation procedure has passed.

## Related Documentation

- [`../network/segmentation.md`](../network/segmentation.md) — Network segmentation
- [`../network/validation.md`](../network/validation.md) — Network validation
- [`../proxmox/configuration.md`](../proxmox/configuration.md) — Proxmox configuration
- [`../../architecture/identity.md`](../../architecture/identity.md) — Identity architecture
- [`../../security/security.md`](../../security/security.md) — Security architecture
- [`configuration.md`](configuration.md) — FreeIPA configuration
- [`validation.md`](validation.md) — FreeIPA validation
