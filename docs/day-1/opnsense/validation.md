# OPNsense — Validation

> **Day 1 — Validate**

This document defines the validation procedure for `fw01`, the OPNsense firewall used by the Enterprise Reference Architecture.

Validation proves that the firewall performs its intended network-security functions. A successful login to the web interface is only one validation point; it does not prove routing, NAT, DNS, firewall policy, or management isolation are correct.

## Status

**Validation procedure.** OPNsense is implemented in the laboratory. The target VLAN and inter-VLAN architecture is **Planned** until configured and tested end-to-end.

---

## 1. Validation Model

```text
Configure
   ↓
Observe
   ↓
Functional Test
   ↓
Negative Test
   ↓
Reboot / Persistence Test
   ↓
Evidence
```

Every important control should have both:

- A positive test: expected traffic succeeds.
- A negative test: traffic that should not exist is blocked.

---

## 2. Validation Prerequisites

Before starting:

- OPNsense boots normally.
- WAN and LAN interfaces are identified.
- A separate management computer is available.
- A test client is available on the LAN.
- Upstream connectivity is available if Internet tests are required.
- Current configuration backup exists before disruptive tests.

Do not perform destructive tests against the only operational firewall without a recovery path.

---

## 3. Interface Validation

Confirm the interfaces in OPNsense and compare them with the Proxmox VM NIC configuration.

Record:

```text
WAN:
LAN:
VLAN interfaces:
MAC addresses:
Proxmox NIC mapping:
```

### Pass Criteria

- WAN maps to the intended upstream network.
- LAN maps to the intended internal network.
- No interface is accidentally connected to the wrong security zone.

---

## 4. Boot and System Health

After boot, verify:

- System reaches the normal OPNsense interface.
- No unexpected boot errors are present.
- CPU and memory usage are reasonable for the workload.
- Required services are running.
- No unexpected gateway or interface errors exist.

Record the OPNsense version as evidence.

---

## 5. Management Access Test

This is a mandatory test from a **third computer**, not merely from the Proxmox console.

Topology:

```text
Management PC
      |
      | HTTPS
      v
    LAN
      |
  OPNsense
```

Test:

1. Connect the management PC to the intended LAN/management network.
2. Open the OPNsense HTTPS management address.
3. Authenticate.
4. Verify the expected firewall hostname and system information.

### Pass Criteria

- Web interface is reachable.
- Correct firewall is reached.
- Authentication works.
- Access occurs through the intended management network.

---

## 6. WAN Connectivity Test

From a LAN test client, verify that outbound connectivity works when it is intended to be allowed.

Test in layers:

```text
LAN client
   ↓
Default gateway
   ↓
OPNsense WAN
   ↓
Upstream gateway
   ↓
External IP
   ↓
DNS name
```

Use separate tests for:

- Gateway reachability
- IP connectivity
- DNS resolution
- HTTPS connectivity

This helps identify whether a failure is caused by routing, NAT, DNS, or the remote service.

---

## 7. DNS Validation

From a LAN client, test DNS independently.

Example:

```bash
nslookup example.com
```

or an equivalent DNS query tool available on the client.

Validate:

- Client has the expected DNS server.
- DNS requests reach the intended resolver.
- Valid external names resolve.
- Invalid names fail predictably.

When FreeIPA becomes part of the lab, internal DNS validation must be extended to cover the identity namespace.

---

## 8. DHCP Validation

If OPNsense provides DHCP for the test network:

1. Disconnect/reconnect the test client or renew its lease.
2. Verify address allocation.
3. Verify subnet mask/prefix.
4. Verify default gateway.
5. Verify DNS server.
6. Verify lease information in OPNsense.

Example client-side checks:

```bash
ip addr
ip route
```

### Negative Check

Confirm that an unintended network does not receive addresses from the DHCP scope.

---

## 9. Firewall Positive Tests

For each explicitly permitted flow, test the real traffic.

Example:

| Flow | Expected | Result |
|---|---|---|
| LAN → DNS | Allow | |
| LAN → HTTPS Internet | Allow | |
| Management PC → OPNsense HTTPS | Allow | |
| Required infrastructure flow | Allow | |

Do not mark a rule validated merely because it exists in the configuration.

---

## 10. Firewall Negative Tests

Test traffic that should be denied.

Examples:

| Flow | Expected |
|---|---|
| WAN → OPNsense management | Deny |
| WAN → Internal client | Deny unless explicitly published |
| Unapproved internal service | Deny |
| Unapproved management source | Deny |

Use safe test traffic and avoid scanning or generating unnecessary load against networks outside the lab.

---

## 11. WAN Management Exposure Test

This is a critical security check.

From an external/untrusted test position, verify that administrative services are not unintentionally exposed.

At minimum confirm that the OPNsense management interface is not reachable from WAN unless there is an explicitly documented requirement and restrictive rule.

Expected result:

```text
Untrusted/WAN
      |
      X
      |
OPNsense Management
```

If management is reachable from WAN unexpectedly, treat the configuration as a validation failure.

---

## 12. NAT Validation

Validate outbound NAT from a LAN client.

Expected path:

```text
10.x.x.x client
      ↓
OPNsense
      ↓
WAN address
      ↓
Internet
```

Confirm that outbound connections work where allowed.

If port forwarding is configured, validate it separately using both:

- Expected source → published service
- Unauthorized source → published service

Do not expose management services merely to simplify testing.

---

## 13. Routing Validation

Review the routing table and gateway status.

Validate:

- Default route is correct.
- Internal routes exist where required.
- No unintended routes exist.
- Gateway is considered healthy.

When VLANs are implemented, perform a route test for each intended network.

---

## 14. VLAN Validation — Planned

The target architecture contains VLANs for:

```text
VLAN 10 → Management
VLAN 20 → Identity
VLAN 30 → Database
VLAN 40 → Application
```

Validation must be end-to-end:

```text
Client / VM
    ↓
Switch
    ↓
Proxmox
    ↓
OPNsense VLAN interface
    ↓
Firewall policy
    ↓
Destination
```

For every VLAN validate:

- Correct tag
- Correct gateway
- Correct subnet
- DHCP/static addressing
- DNS behavior
- Internet policy
- Inter-VLAN policy
- Management isolation

Do not mark VLANs validated from the OPNsense interface list alone.

---

## 15. Inter-VLAN Firewall Validation — Planned

The target security model uses explicit service flows between zones.

Examples:

```text
Management → Identity        Required services only
Application → Database      Required DB port only
Database → Internet         Deny by default
Application → Management    Deny unless required
Identity → Database         Only documented dependencies
```

For each permitted dependency:

```text
Expected allowed flow → PASS
Unexpected lateral flow → BLOCK
```

Record the exact source, destination, protocol, and port used in the test.

---

## 16. Logging Validation

Generate a controlled firewall event and verify that the event can be found in the appropriate log view.

Test both:

- A permitted flow where logging is enabled.
- A blocked flow.

Confirm that logs contain enough information to identify:

- Source
- Destination
- Protocol/port where available
- Action
- Timestamp

Time synchronization must be correct for logs to be useful during incident investigation.

---

## 17. Configuration Backup Validation

Create a configuration backup before major changes and verify that the backup process completes successfully.

The existence of a backup file is not proof of recoverability.

A complete recovery test belongs to the Day 2 backup/restore process and should be performed in a controlled environment.

Record:

```text
Backup date:
Configuration revision:
Backup destination:
Encryption/protection:
Restore test status:
```

Never commit configuration exports containing secrets to Git.

---

## 18. Reboot Persistence Test

After configuration is complete, perform a controlled reboot when appropriate.

Before reboot, record:

- Interface state
- Gateway state
- Firewall configuration revision
- DHCP state
- DNS state
- Important routes

After reboot, repeat:

```text
Web management
WAN connectivity
LAN connectivity
DNS
DHCP
Firewall policy
NAT
Gateway health
```

### Pass Criteria

All required functions return without manual reconfiguration.

---

## 19. Failure / Recovery Test

Perform a safe, controlled failure test.

Examples:

- Temporarily disconnect a test client's network.
- Disable a non-critical test rule and restore it.
- Test expected behavior when the upstream gateway is unavailable, if the lab allows it safely.

The goal is to answer:

```text
Can the failure be detected?
Can the cause be identified?
Can service be restored?
Is the recovery procedure documented?
```

Do not intentionally break the only management path without console or other recovery access.

---

## 20. Validation Evidence

Record validation results in a consistent format.

```text
Validation ID: OPN-D1-001
Date:
Host / VM:
Test:
Expected:
Actual:
Result: PASS / FAIL / N/A
Evidence:
Notes:
```

Useful evidence includes:

- OPNsense screenshots
- Firewall rule/task information
- Client routing information
- DNS results
- DHCP lease information
- Connectivity test results
- Logs
- Configuration revision
- Reboot test result

Remove sensitive information before publishing evidence.

---

## 21. Validation Matrix

| Area | Test | Status |
|---|---|---|
| Boot | Normal boot | ⬜ |
| Interfaces | WAN/LAN mapping | ⬜ |
| Management | Third-computer HTTPS access | ⬜ |
| WAN | Upstream connectivity | ⬜ |
| DNS | Client DNS resolution | ⬜ |
| DHCP | Address assignment | ⬜ / N/A |
| Firewall | Positive flows | ⬜ |
| Firewall | Negative flows | ⬜ |
| WAN security | Management not exposed | ⬜ |
| NAT | Outbound connectivity | ⬜ |
| Routing | Expected routes | ⬜ |
| VLANs | End-to-end VLAN tests | ⬜ / Planned |
| Inter-VLAN | Allow/deny matrix | ⬜ / Planned |
| Logging | Block/pass evidence | ⬜ |
| Backup | Configuration backup | ⬜ |
| Persistence | Post-reboot behavior | ⬜ |
| Recovery | Controlled failure test | ⬜ |

---

## 22. Implementation Status

| Capability | Status |
|---|---|
| OPNsense VM | Implemented |
| Basic WAN/LAN firewall | Implemented / verify current lab state |
| Third-computer management | Validate with this procedure |
| DNS | Verify current lab configuration |
| DHCP | Verify current lab configuration |
| NAT | Verify current lab configuration |
| VLAN segmentation | Planned |
| Inter-VLAN policy | Planned |
| Centralized logging | Planned |
| Identity integration | Planned |
| Automation / IaC | Planned |

This table must reflect actual laboratory evidence rather than the target architecture.

---

## 23. Day 1 Completion Criteria

OPNsense validation is complete when:

1. WAN and LAN interfaces are correctly identified.
2. Management works from a separate computer.
3. DNS behaves as designed.
4. DHCP behaves as designed where enabled.
5. Required outbound connectivity works.
6. NAT behavior is understood and tested.
7. Firewall allow rules have been functionally tested.
8. Firewall deny rules have been negatively tested.
9. WAN management exposure has been checked.
10. Logs provide useful evidence for relevant events.
11. Configuration backup is available.
12. Configuration survives reboot.
13. Any VLAN/inter-VLAN features are clearly marked Planned until actually validated.
14. Evidence and deviations are documented.

> **A firewall is validated when its intended traffic is proven to work and its unintended traffic is proven not to work.**

## Related Documentation

- [`installation.md`](installation.md) — OPNsense installation
- [`configuration.md`](configuration.md) — OPNsense configuration baseline
- [`../../network/network.md`](../../network/network.md) — Network architecture
- [`../../security/security.md`](../../security/security.md) — Security architecture
- [`../../day-1/documentation-standard.md`](../documentation-standard.md) — Day 1 documentation standard
- [`../../day-2/README.md`](../../day-2/README.md) — Day 2 operations
