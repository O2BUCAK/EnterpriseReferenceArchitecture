# Network Segmentation — Validation

> **Day 1 — Validate**

This document defines the validation procedure for the segmented network architecture after VLAN, routing, and firewall configuration has been implemented.

## Status

**Planned.** This procedure becomes applicable when VLAN segmentation is actually implemented in the laboratory.

The current architecture defines VLAN 10 Management, VLAN 20 Identity, VLAN 30 Database, and VLAN 40 Application. These remain target-design values until end-to-end testing proves otherwise. fileciteturn13file0L2-L2

---

## 1. Validation Principle

Network validation must prove four things:

```text
Correct segmentation
        +
Correct routing
        +
Correct allowed traffic
        +
Correctly blocked traffic
```

A VLAN appearing in a switch, Proxmox, or OPNsense interface list is not sufficient evidence that the architecture works.

---

## 2. Validation Topology

```text
                    OPNsense
                       |
                  VLAN trunk
                       |
                    Proxmox
                       |
                Physical switch
                       |
        +--------------+--------------+
        |              |              |
     VLAN 10        VLAN 20        VLAN 30/40
   Management       Identity       DB / App
```

Validation should test the complete path rather than individual devices in isolation.

---

## 3. Test Matrix

Prepare a test matrix before making restrictive firewall changes.

| Test ID | Source | Destination | Expected | Actual | Result |
|---|---|---|---|---|---|
| NET-001 | VLAN 10 | Gateway | Allow | | |
| NET-002 | VLAN 20 | Gateway | Allow | | |
| NET-003 | VLAN 30 | Gateway | Allow | | |
| NET-004 | VLAN 40 | Gateway | Allow | | |
| NET-005 | Management | Proxmox | Allow | | |
| NET-006 | Management | OPNsense | Allow | | |
| NET-007 | Application | Database service | Allow | | |
| NET-008 | Application | Database other ports | Deny | | |
| NET-009 | Database | Management | Deny | | |
| NET-010 | Untrusted | Management | Deny | | |

Actual tests should be expanded when real services are implemented.

---

## 4. Physical Switch Validation

Confirm the VLAN configuration on the managed switch.

Validate:

- VLAN 10 exists.
- VLAN 20 exists.
- VLAN 30 exists.
- VLAN 40 exists.
- Trunk carries required VLANs.
- Access ports are assigned to the correct VLAN.
- No unintended VLAN is permitted on the trunk.

Test each relevant access port with a suitable endpoint.

### Pass Criteria

An endpoint connected to an access port receives connectivity appropriate to that VLAN and cannot accidentally appear in another VLAN.

---

## 5. Proxmox Bridge Validation

Verify that the Proxmox networking path carries the intended VLAN tags.

Validate:

- Correct physical NIC is connected.
- Correct bridge is used.
- VLAN-aware behavior is configured if required.
- VM VLAN tags match the design.

Do not infer successful VLAN transport from the presence of a VLAN field in the VM configuration.

A test VM must demonstrate actual connectivity through the intended VLAN.

---

## 6. OPNsense VLAN Validation

For each VLAN, verify:

- Interface exists.
- VLAN ID is correct.
- IP address is correct.
- Subnet is correct.
- Interface is enabled.
- Gateway behavior is correct.

Reference:

```text
VLAN 10 → 10.10.10.1/24
VLAN 20 → 10.10.20.1/24
VLAN 30 → 10.10.30.1/24
VLAN 40 → 10.10.40.1/24
```

These are reference values; the validation record must contain the actual deployed values.

---

## 7. Same-VLAN Connectivity

From a test endpoint in each VLAN, verify reachability to its own gateway.

Example:

```bash
ping -c 4 <vlan-gateway>
```

Expected:

```text
VLAN 10 client → 10.10.10.1  PASS
VLAN 20 client → 10.10.20.1  PASS
VLAN 30 client → 10.10.30.1  PASS
VLAN 40 client → 10.10.40.1  PASS
```

A failure here should be investigated before testing inter-VLAN routing.

---

## 8. DHCP Validation

Where DHCP is enabled, renew the lease on a test endpoint in each VLAN.

Verify:

- Address belongs to the expected subnet.
- Gateway is the correct OPNsense interface.
- DNS is the intended resolver.
- Lease originates from the expected DHCP service.

Expected example:

```text
VLAN 20 client
Address: 10.10.20.x
Gateway: 10.10.20.1
```

Do not use the same DHCP scope across isolated VLANs.

---

## 9. DNS Validation by VLAN

Test DNS independently from routing.

For each VLAN:

1. Check assigned DNS server.
2. Resolve an external name where Internet DNS is expected.
3. Resolve an internal name when internal DNS exists.
4. Confirm that DNS traffic follows the intended security policy.

When FreeIPA is implemented, include:

- Forward lookup
- Reverse lookup
- Identity hostnames
- Required service records

---

## 10. Internet Connectivity by VLAN

Not all VLANs should automatically have unrestricted Internet access.

Test each VLAN against the intended policy.

Example:

| VLAN | Internet | Expected |
|---|---|---|
| Management | Controlled | Defined |
| Identity | Controlled | Defined |
| Database | Restricted | Deny by default |
| Application | Controlled | Defined |

For each permitted VLAN test:

```text
Client → Gateway → WAN → External destination
```

For restricted VLANs, test an expected denied flow as well.

---

## 11. Inter-VLAN Routing Validation

Test only documented dependencies.

Example:

```text
Application VLAN
10.10.40.0/24
       |
       | TCP 5432
       v
Database VLAN
10.10.30.0/24
```

Expected:

- TCP 5432 from the intended application host to the database host: **Allow**
- Other unnecessary database ports: **Deny**
- Application VLAN access to management services: **Deny unless explicitly required**

Use actual application requirements once `app01` and `db01` are implemented.

---

## 12. Management Isolation Test

From every non-management VLAN, test access to management services.

Expected:

```text
Identity → Proxmox       DENY
Database → Proxmox       DENY
Application → Proxmox    DENY
```

The Management VLAN should have the explicitly required administrative access.

This test is one of the most important demonstrations that segmentation provides a security boundary rather than merely a different IP range.

---

## 13. Database Isolation Test

When `db01` exists, verify that database services are accessible only from explicitly authorized clients.

Example:

```text
app01 → db01:5432       ALLOW
random VLAN → db01:5432 DENY
random VLAN → db01:*    DENY
```

Do not expose PostgreSQL to every internal network simply because it is an internal service.

---

## 14. VLAN Tag Integrity Test

Verify that endpoints cannot access the wrong VLAN by simply changing their local configuration.

Where practical, test:

- Correct tagged traffic
- Correct untagged access-port behavior
- Incorrect VLAN tag
- Unauthorized VLAN access

Expected result:

```text
Correct VLAN → expected network
Incorrect VLAN → no unintended access
```

Do not conduct intrusive VLAN-hopping tests against networks outside the lab.

---

## 15. Firewall Rule Validation

For every important rule, test both directions where meaningful.

Example:

| Rule | Positive test | Negative test |
|---|---|---|
| App → DB 5432 | Connection succeeds | DB other ports blocked |
| Management → Proxmox | HTTPS succeeds | Other VLAN blocked |
| Management → OPNsense | HTTPS succeeds | WAN blocked |
| Database → Internet | N/A if denied | Connection blocked |

Record the exact test command or application used.

---

## 16. Logging Validation

Generate a controlled blocked connection.

Then confirm that OPNsense records the event with useful information.

Expected evidence should identify, where available:

- Source IP
- Destination IP
- Protocol
- Port
- Action
- Timestamp

Generate at least one permitted event where logging is enabled and compare the two records.

---

## 17. Failure Isolation Test

A segmented design should allow the impact of a failure to be understood.

Safe examples:

- Disconnect a test endpoint from one VLAN.
- Disable a test client interface.
- Temporarily block a non-critical test rule.

Verify that unrelated networks remain operational.

Example:

```text
Application test failure
        ↓
Management network remains reachable
```

Do not intentionally disable the only firewall or management path.

---

## 18. Reboot Persistence

After the network configuration is stable, perform a controlled reboot sequence where appropriate.

Validate after reboot:

- Switch VLANs remain configured.
- Proxmox networking returns.
- OPNsense VLAN interfaces return.
- Gateways are reachable.
- DHCP works.
- DNS works.
- Firewall rules are active.
- Required inter-VLAN flows work.

A network that works only until reboot is not validated.

---

## 19. End-to-End Validation

The final validation should test real workloads rather than only ping.

Target future example:

```text
Management PC
      |
      v
Management VLAN
      |
      +----> Proxmox
      +----> OPNsense

Application VM
      |
      v
Application VLAN
      |
      | TCP 5432
      v
Database VM
      |
      v
Database VLAN
```

This demonstrates that the architecture works at the service level while preserving segmentation.

---

## 20. Evidence Record

Use one record per important test.

```text
Validation ID:
Date:
Source:
Destination:
Protocol/Port:
Expected:
Actual:
Result: PASS / FAIL / N/A
Firewall rule:
Evidence:
Notes:
```

Keep evidence free of credentials and unnecessary sensitive infrastructure information.

---

## 21. Validation Matrix

| Area | Validation | Status |
|---|---|---|
| Switch | VLAN definitions | ⬜ |
| Switch | Trunk configuration | ⬜ |
| Proxmox | VLAN transport | ⬜ |
| OPNsense | VLAN interfaces | ⬜ |
| Gateways | Per-VLAN gateway | ⬜ |
| DHCP | Per-VLAN addressing | ⬜ / N/A |
| DNS | Per-VLAN DNS | ⬜ |
| Internet | Policy by VLAN | ⬜ |
| Routing | Inter-VLAN routes | ⬜ |
| Firewall | Allowed flows | ⬜ |
| Firewall | Denied flows | ⬜ |
| Management | Isolation | ⬜ |
| Database | Service isolation | ⬜ / Planned |
| Logging | Firewall evidence | ⬜ |
| Failure | Isolation behavior | ⬜ |
| Persistence | Post-reboot | ⬜ |
| E2E | Real service flow | ⬜ / Planned |

---

## 22. Completion Criteria

Network segmentation can be marked **Validated** only when:

1. Each VLAN is proven to exist end-to-end.
2. Each VLAN receives the expected addressing.
3. Each gateway is reachable from its VLAN.
4. DNS behavior is correct.
5. Internet access follows the intended policy.
6. Required inter-VLAN flows work.
7. Unrequired inter-VLAN flows are blocked.
8. Management interfaces are isolated from untrusted networks.
9. Firewall logs provide useful evidence.
10. Configuration survives reboot.
11. A real application dependency is tested once the relevant workloads exist.
12. Evidence is recorded.

> **Segmentation is validated by traffic behavior, not by configuration screenshots alone.**

## Related Documentation

- [`../../network/network.md`](../../network/network.md) — Target network architecture
- [`segmentation.md`](segmentation.md) — Network segmentation build procedure
- [`../opnsense/configuration.md`](../opnsense/configuration.md) — OPNsense configuration
- [`../opnsense/validation.md`](../opnsense/validation.md) — OPNsense validation
- [`../proxmox/configuration.md`](../proxmox/configuration.md) — Proxmox configuration
- [`../proxmox/validation.md`](../proxmox/validation.md) — Proxmox validation
- [`../documentation-standard.md`](../documentation-standard.md) — Day 1 documentation standard
