# OPNsense — Troubleshooting Runbook

> **Day 2 — Troubleshooting**

## Status

**Documented.** These scenarios are defined for the implemented `fw01`. They are not evidence that each failure scenario has been deliberately reproduced in the lab.

## 1. Troubleshooting Order

```text
Proxmox VM
 ↓
OPNsense interfaces
 ↓
Gateway
 ↓
Routing / NAT
 ↓
Firewall policy
 ↓
DNS / DHCP
 ↓
Client
```

## 2. Web UI Unavailable

1. Confirm `fw01` VM state in Proxmox.
2. Confirm virtual NICs.
3. Test management-path connectivity.
4. Check OPNsense system health.
5. Check interface assignments.
6. Review recent configuration changes.
7. Use console access if web management is unavailable.
8. Validate management access after recovery.

Do not reset the firewall configuration as the first troubleshooting action.

## 3. Internet Connectivity Failure

Determine whether the failure affects:

- one client;
- multiple clients;
- the LAN;
- WAN;
- all destinations;
- only DNS names.

Then test:

```text
Client IP
 ↓
LAN gateway
 ↓
WAN gateway
 ↓
Public IP destination
 ↓
DNS resolution
```

This separates routing, upstream connectivity and DNS failures.

## 4. Gateway Down

1. Check interface/link state.
2. Check gateway address.
3. Test gateway reachability.
4. Check upstream connectivity.
5. Review recent interface/routing changes.
6. Validate recovery.

Do not change firewall rules when the gateway itself is unavailable unless evidence points to policy as the cause.

## 5. Traffic Unexpectedly Blocked

1. Identify source and destination.
2. Identify protocol and port.
3. Confirm intended policy.
4. Review matching firewall logs.
5. Check rule ordering.
6. Check interface assignment.
7. Check NAT/routing where relevant.
8. Make one controlled change.
9. Test required traffic.
10. Test that unrelated traffic remains blocked.

## 6. Traffic Unexpectedly Allowed

Treat this as a security-sensitive incident.

1. Identify the exact traffic flow.
2. Confirm source/destination.
3. Review matching firewall rule.
4. Review NAT and routing.
5. Check whether the behavior is expected.
6. Restrict the flow if necessary.
7. Validate both allowed and blocked paths.
8. Record evidence.

Do not solve an unexpected allow by adding unrelated broad deny rules without understanding the traffic path.

## 7. DNS Failure

Separate DNS from general connectivity.

Test:

```text
Gateway reachable?
        ↓
Public IP reachable?
        ↓
DNS server reachable?
        ↓
Name resolution working?
```

Review DNS service state and configured upstream servers where applicable.

## 8. DHCP Failure

If DHCP is enabled:

1. Confirm service state.
2. Check scope availability.
3. Check leases.
4. Check interface assignment.
5. Check client VLAN/interface when VLANs are implemented.
6. Test lease acquisition.
7. Validate gateway and DNS values.

## 9. NAT Failure

Check:

- outbound interface;
- source network;
- destination;
- translation rule;
- associated firewall rule;
- routing.

Avoid creating permissive NAT rules solely to make a test pass.

## 10. Firewall Rule Change Causes Lockout

If management access is lost immediately after a rule change:

1. Determine whether console access remains available.
2. Identify the last change.
3. Revert the known-bad change if safe.
4. Restore management access.
5. Validate critical traffic.
6. Validate management restrictions.
7. Record the incident.

Future rule changes should have a known rollback path before implementation.

## 11. VM Failure

If `fw01` is unavailable:

1. Check Proxmox VM state.
2. Check virtual disks.
3. Check virtual NICs.
4. Check host resource availability.
5. Review recent changes.
6. Recover the VM.
7. Restore configuration if required.
8. Validate interfaces, gateways and policy.

## 12. Recovery Validation

A recovered firewall must pass both functional and security checks:

- management access works;
- WAN/LAN interfaces work;
- gateway is healthy;
- required traffic works;
- unauthorized traffic remains blocked;
- NAT behaves as intended;
- DNS/DHCP work where applicable;
- configuration persists after restart when relevant.

## 13. Evidence

```text
Incident:
Timestamp:
Affected path:
Symptom:
Firewall evidence:
Network evidence:
Recent change:
Action:
Result:
Root cause:
Recovery:
Preventive action:
```

## Related Documentation

- [`operations.md`](operations.md)
- [`monitoring.md`](monitoring.md)
- [`backup-recovery.md`](backup-recovery.md)
- [`../troubleshooting/methodology.md`](../troubleshooting/methodology.md)
- [`../incident-management/process.md`](../incident-management/process.md)
