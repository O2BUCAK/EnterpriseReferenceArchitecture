# Proxmox VE — Validation

> **Day 1 — Validate**

This document defines how the Proxmox VE host is validated after installation and baseline configuration.

The objective is not simply to confirm that the web interface opens. Validation must demonstrate that the host can reliably provide its intended infrastructure functions and that important dependencies are healthy.

## Status

**Validation procedure.** Proxmox VE is implemented in the laboratory. The checks below define the evidence required before individual configuration items are considered validated.

---

## 1. Validation Model

Use the following lifecycle:

```text
Configuration
     ↓
Health Check
     ↓
Functional Test
     ↓
Failure / Boundary Test
     ↓
Evidence
     ↓
Validation Status
```

A configuration should not be marked **Validated** solely because a command completed successfully.

---

## 2. Validation Scope

Validation covers:

1. Host identity
2. CPU and memory
3. Network
4. DNS
5. Time synchronization
6. Package repositories
7. Proxmox services
8. Storage
9. Web administration
10. VM lifecycle
11. QEMU Guest Agent
12. Administrative access
13. Firewall baseline
14. Reboot persistence
15. Documentation evidence

---

## 3. Host Identity Validation

Check:

```bash
hostnamectl
hostname -f
```

Expected:

- Hostname matches the intended node name.
- FQDN is stable.
- No unexpected hostname changes occur after reboot.

### Result

```text
[ ] Pass
[ ] Fail
[ ] Not Applicable
```

Evidence:

```text
Hostname:
FQDN:
Validation date:
```

---

## 4. CPU and Memory Validation

Review the host's available resources:

```bash
lscpu
free -h
```

The current laboratory reference host is a Dell Latitude 5540 with an Intel Core i7-1355U and 32 GiB RAM. The resource matrix intentionally leaves capacity available for the Proxmox host rather than allocating all resources to guests.

Validation should confirm:

- CPU is correctly detected.
- Expected memory is available.
- No unexpected memory pressure exists immediately after boot.
- Proxmox reports resources consistently with the operating system.

Do not treat theoretical hardware specifications as runtime validation evidence.

---

## 5. Network Validation

Inspect interfaces and routing:

```bash
ip addr
ip route
ip link show vmbr0
```

Test the management gateway:

```bash
ping -c 4 <gateway>
```

Test name resolution:

```bash
getent hosts example.com
```

### Functional Validation

Confirm from a separate management computer that:

- Proxmox web interface is reachable.
- SSH is reachable if intentionally enabled.
- The management address remains reachable after reboot.
- VM network connectivity works when a test VM is running.

### VLAN Validation

VLAN functionality is only considered validated after an end-to-end test involving the relevant physical switch, Proxmox bridge, VM configuration, OPNsense interface, and firewall policy.

The target VLAN architecture is currently planned rather than implemented.

---

## 6. DNS Validation

DNS must be tested independently from general Internet connectivity.

Examples:

```bash
getent hosts example.com
getent hosts <proxmox-fqdn>
```

If DNS fails, identify whether the failure is caused by:

```text
Host configuration
      ↓
Resolver
      ↓
Gateway / network
      ↓
DNS server
      ↓
Authoritative source
```

### Pass Criteria

- External name resolution works when required.
- Internal names resolve when the internal DNS architecture is implemented.
- The Proxmox FQDN resolves correctly.

---

## 7. NTP / Time Validation

Time synchronization is a mandatory validation item.

Run:

```bash
timedatectl
```

Confirm:

- Correct timezone
- System clock is accurate
- Network time synchronization is active
- Expected time source is being used

Where the installed synchronization implementation provides additional diagnostics, use those diagnostics to confirm the actual synchronization state.

### Why This Matters

Incorrect time can cause failures in:

- TLS certificates
- Authentication
- Kerberos
- Distributed systems
- Cluster membership
- Logs and incident investigation

A host with incorrect time should not be treated as healthy merely because Proxmox services are running.

---

## 8. Package Repository Validation

Run:

```bash
apt update
```

Review the output for:

- Repository errors
- Signature errors
- Unsupported release references
- DNS failures
- Expired metadata
- Unexpected repositories

Then review the installed Proxmox version:

```bash
pveversion -v
```

### Pass Criteria

- Repository configuration matches the intended support model.
- Package metadata can be refreshed successfully.
- Proxmox packages are consistent with the installed release.

---

## 9. Proxmox Service Health

Check for failed services:

```bash
systemctl --failed
```

Review important Proxmox services as appropriate for the current node configuration.

Useful commands include:

```bash
systemctl status pveproxy
systemctl status pvedaemon
systemctl status pvestatd
```

A service being active is necessary but not always sufficient. Review logs when there is evidence of errors or degraded behavior.

Example:

```bash
journalctl -u pveproxy --since "1 hour ago"
```

---

## 10. Storage Validation

Check storage status:

```bash
pvesm status
```

Also inspect the underlying filesystem and block-device state where appropriate:

```bash
lsblk
findmnt
```

### Validate

- [ ] Expected storage is online
- [ ] Storage has sufficient free capacity
- [ ] VM disk storage is writable
- [ ] ISO storage works where configured
- [ ] No unexpected filesystem errors exist

### Capacity Test

Create a small disposable test VM or use an existing non-production test workload to confirm that a VM disk can be created, attached, and used successfully.

Do not consume significant capacity merely to prove storage functionality.

---

## 11. Web Interface Validation

From a separate management computer, open:

```text
https://<proxmox-host>:8006/
```

Validate:

- Login page loads.
- Correct node is displayed.
- Node status is healthy.
- CPU/memory/storage values are visible.
- Tasks can be viewed.
- No unexpected critical alerts are present.

The web interface being reachable from the same host does not prove remote management connectivity.

---

## 12. VM Lifecycle Validation

A Proxmox host should be tested with an actual guest lifecycle.

Use a disposable test VM where possible.

### Test Sequence

```text
Create VM
   ↓
Install / boot OS
   ↓
Start VM
   ↓
Verify console
   ↓
Verify network
   ↓
Verify QEMU Guest Agent
   ↓
Shutdown
   ↓
Start
   ↓
Reboot Proxmox host
   ↓
Verify VM state
```

Record:

```text
Test VM ID:
Guest OS:
CPU:
RAM:
OS disk:
Network bridge:
VLAN (if any):
QEMU Guest Agent:
Result:
```

---

## 13. QEMU Guest Agent Validation

For VMs where the guest agent is part of the standard configuration, validate both sides:

```text
Proxmox configuration
        ↕
QEMU Guest Agent
        ↕
Guest operating system
```

A VM configuration flag alone does not prove that the agent is installed and responding inside the guest.

Validation should confirm that Proxmox can obtain guest information from the running VM where supported.

---

## 14. Administrative Access Validation

Test access from the intended management workstation.

### Web

- [ ] HTTPS access works
- [ ] Correct administrative account can authenticate
- [ ] Permission level is appropriate

### SSH

If SSH is intentionally enabled:

- [ ] Access works from the management network
- [ ] Authentication method is documented
- [ ] Unauthorized source access is restricted where applicable
- [ ] Authentication events are logged

### Lockout Protection

Before changing authentication or firewall restrictions, verify that an alternative management path exists.

---

## 15. Firewall Validation

If the Proxmox firewall is enabled, validate both permitted and denied traffic.

For every important rule, test:

```text
Expected allowed flow → succeeds
Expected denied flow  → fails
```

Record:

| Test | Expected | Actual | Result |
|---|---|---|---|
| Management access | Allowed | | |
| SSH from management | Allowed if enabled | | |
| Untrusted management source | Denied | | |
| Required VM traffic | Allowed | | |
| Unapproved traffic | Denied | | |

Do not infer firewall correctness from the existence of rules alone.

---

## 16. Reboot Persistence Test

A Day 1 configuration is not complete until important settings survive reboot.

Before reboot, record the current state.

Reboot:

```bash
reboot
```

After the host returns, validate:

```bash
hostnamectl
ip addr
ip route
timedatectl
pvesm status
systemctl --failed
```

Also test the web interface from a separate management computer.

### Pass Criteria

- Host boots normally.
- Management network returns.
- DNS works.
- NTP synchronizes.
- Proxmox services start.
- Storage is available.
- Expected VMs behave according to their configured startup policy.

---

## 17. Failure and Boundary Testing

Validation should include at least one controlled negative or boundary test where practical.

Examples:

- Stop a disposable VM and verify expected Proxmox status.
- Disconnect a test VM from its expected network and verify the failure is observable.
- Temporarily test an intentionally blocked firewall flow.
- Verify behavior when a non-critical storage path is unavailable, if the lab topology allows safe testing.

Do not perform destructive tests on the only operational host without a recovery plan.

The purpose is to demonstrate that failures are detectable and diagnosable, not to create unnecessary outages.

---

## 18. Validation Evidence

Each completed validation should produce lightweight evidence.

Recommended evidence types:

- Command output
- Proxmox screenshots
- Task logs
- Test VM details
- Before/after configuration records
- Connectivity test results
- Reboot test result
- Date and operator

Example:

```text
Validation ID: PVE-D1-001
Date:
Host:
Test:
Expected result:
Actual result:
Status: PASS / FAIL
Evidence:
Notes:
```

Do not commit secrets or sensitive infrastructure credentials as evidence.

---

## 19. Overall Validation Matrix

| Area | Test | Status |
|---|---|---|
| Host identity | Hostname/FQDN | ⬜ |
| Hardware | CPU/RAM detection | ⬜ |
| Network | Management connectivity | ⬜ |
| Bridge | `vmbr0` operation | ⬜ |
| DNS | Name resolution | ⬜ |
| NTP | Time synchronization | ⬜ |
| Packages | Repository/update test | ⬜ |
| Services | Proxmox service health | ⬜ |
| Storage | Storage availability | ⬜ |
| Web UI | Remote management | ⬜ |
| VM lifecycle | Create/start/stop/reboot | ⬜ |
| Guest Agent | Agent response | ⬜ |
| Access | Administrative authentication | ⬜ |
| Firewall | Allow/deny behavior | ⬜ / N/A |
| Persistence | Post-reboot validation | ⬜ |
| Evidence | Records captured | ⬜ |

Use `PASS`, `FAIL`, or `N/A` when converting this matrix into an actual lab validation record.

---

## 20. Implementation Status

The project deliberately separates platform implementation from validation evidence.

| Component | Implementation | Validation |
|---|---|---|
| Proxmox VE | Implemented | Validate with this procedure |
| `vmbr0` | Implemented as part of current Proxmox setup where configured | Verify actual lab state |
| VLAN segmentation | Planned | Not validated |
| OPNsense integration | Implemented as a VM | Validate relevant flows |
| FreeIPA | Planned | Not applicable yet |
| PostgreSQL | Planned | Not applicable yet |
| Docker platform | Planned | Not applicable yet |
| Automation / IaC | Planned | Not applicable yet |

The table must be updated only when the laboratory state changes and evidence exists.

---

## 21. Day 1 Validation Completion Criteria

Proxmox Day 1 validation can be considered complete when:

1. Host identity is correct.
2. Management networking is functional.
3. DNS works as designed.
4. Time synchronization is healthy.
5. Repositories are valid.
6. Proxmox services are healthy.
7. Storage is available and has sufficient capacity.
8. Remote management works from the intended management path.
9. A disposable VM successfully completes the required lifecycle tests.
10. Important configuration survives reboot.
11. Security controls behave as expected where implemented.
12. Evidence has been recorded.
13. Any deviations are documented.

> **A green Proxmox dashboard is not, by itself, validation.**

---

## Related Documentation

- [`installation.md`](installation.md) — Proxmox installation
- [`configuration.md`](configuration.md) — Proxmox configuration baseline
- [`../documentation-standard.md`](../documentation-standard.md) — Day 1 documentation standard
- [`../../vm-design/vm-design.md`](../../vm-design/vm-design.md) — VM standards
- [`../../network/network.md`](../../network/network.md) — Network architecture
- [`../../security/security.md`](../../security/security.md) — Security architecture
- [`../../day-2/README.md`](../../day-2/README.md) — Day 2 operations
