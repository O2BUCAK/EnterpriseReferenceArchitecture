# OPNsense — Operations Runbook

> **Day 2 — Operate**

This runbook defines routine operational activities for `fw01` running OPNsense.

## Status

**Documented.** OPNsense is implemented in the laboratory. Individual operational procedures become validated only after actual execution and evidence collection.

---

## 1. Operational Scope

Covers:

- Firewall health
- Interface health
- Gateway status
- DNS/DHCP where used
- NAT
- Firewall rules
- Administrative access
- Configuration backup
- Updates
- Connectivity troubleshooting

VLAN-specific operations remain Planned until VLAN segmentation is implemented.

---

## 2. Routine Health Check

Review the OPNsense dashboard and confirm:

- System is healthy.
- Interfaces are up.
- Gateways are reachable.
- No unexpected critical alerts exist.
- CPU and memory are reasonable.
- Storage is healthy.
- Time synchronization is healthy.
- Firewall activity is consistent with expectations.

Record unusual behavior before making changes.

---

## 3. Interface Operations

For each interface verify:

```text
Interface
Address
Link state
Gateway
Traffic
Errors
```

If an interface is unexpectedly down:

1. Check Proxmox virtual NIC state.
2. Check OPNsense interface assignment.
3. Check upstream switch/cabling where applicable.
4. Check recent changes.
5. Validate after recovery.

---

## 4. Gateway Operations

Review gateway health and latency.

If a gateway is reported down:

1. Test local interface state.
2. Test gateway reachability.
3. Test upstream connectivity.
4. Check DNS separately.
5. Check recent firewall/NAT changes.

Do not assume a gateway failure is a DNS failure.

---

## 5. Firewall Rule Operations

Before changing a firewall rule:

1. Identify the intended traffic.
2. Identify source and destination.
3. Identify protocol/port.
4. Determine expected action.
5. Determine rule ordering impact.
6. Define rollback.
7. Apply one logical change.
8. Test positive behavior.
9. Test negative behavior where appropriate.
10. Record the change.

Target principle:

```text
Default deny
     ↓
Explicit required access
```

---

## 6. NAT Operations

Review NAT rules when connectivity changes unexpectedly.

Check:

- Source
- Destination
- Translation
- Interface
- Port
- Associated firewall rule

Avoid adding broad NAT rules as a troubleshooting shortcut.

---

## 7. DNS Operations

Where OPNsense provides DNS services, validate:

- Service availability
- Forward resolution
- Expected local records
- Upstream resolution
- DNS policy

For the target architecture, FreeIPA is planned as the future identity/DNS authority. Until implemented, OPNsense DNS behavior should be documented according to the actual lab configuration.

---

## 8. DHCP Operations

If DHCP is enabled:

Review:

- Scope utilization
- Leases
- Reservations
- Gateway
- DNS servers
- Unexpected clients

Do not assume DHCP configuration matches the target VLAN architecture until VLANs are implemented.

---

## 9. Administrative Access

Management access should remain restricted.

Review:

- Administrative accounts
- Authentication method
- Web UI exposure
- SSH exposure if enabled
- Source networks

Do not expose management interfaces to WAN unless there is a documented and secured requirement.

---

## 10. Configuration Backup

After important configuration changes:

1. Save the configuration.
2. Create/verify a backup.
3. Store it in the defined protected location.
4. Record the backup date.
5. Confirm it can be used for recovery.

Never publish a configuration backup containing secrets.

---

## 11. Update Operations

Follow:

```text
Review update
   ↓
Check impact
   ↓
Verify recovery path
   ↓
Apply update
   ↓
Reboot if required
   ↓
Validate interfaces
   ↓
Validate gateways
   ↓
Validate firewall/NAT
   ↓
Validate client connectivity
```

Avoid major changes during an active outage unless required for recovery.

---

## 12. Log Review

Review security and system logs for:

- Repeated firewall denies
- Unexpected WAN traffic
- Authentication failures
- Interface changes
- Gateway failures
- Service failures
- Configuration changes

Do not treat every denied packet as an incident; establish expected baseline behavior first.

---

## 13. Connectivity Incident Procedure

When a client reports connectivity failure:

```text
Client
 ↓
IP configuration
 ↓
Gateway
 ↓
DNS
 ↓
OPNsense rule
 ↓
NAT/routing
 ↓
Destination
```

Test each layer separately.

This prevents changing firewall rules when the actual problem is DNS or routing.

---

## 14. Rule Change Validation

After modifying a rule:

### Positive test

Required traffic should work.

### Negative test

Unapproved traffic should remain blocked.

### Logging test

The expected event should appear in the appropriate log where logging is enabled.

---

## 15. VLAN Operations

After VLAN implementation, maintain:

- VLAN IDs
- Interface assignments
- Gateway addresses
- DHCP scopes
- Firewall policies
- Switch trunk/access mappings
- Management isolation

Until then, VLAN operations are Planned.

---

## 16. Failure Recovery

If `fw01` is unavailable:

1. Determine whether Proxmox or the VM is affected.
2. Check VM state.
3. Check virtual NICs.
4. Review recent firewall changes.
5. Restore configuration if required.
6. Restore the VM from backup if necessary.
7. Validate WAN/LAN connectivity.
8. Validate management access.
9. Validate critical policies.

Do not immediately reset the firewall configuration without determining whether the current configuration can be recovered.

---

## 17. Evidence

For significant operations record:

```text
Date:
Operator:
System: fw01
Change/operation:
Reason:
Affected interface/rule:
Before:
Action:
After:
Validation:
Rollback:
Notes:
```

## Related Documentation

- [`../transition.md`](../transition.md)
- [`../../day-1/opnsense/installation.md`](../../day-1/opnsense/installation.md)
- [`../../day-1/opnsense/configuration.md`](../../day-1/opnsense/configuration.md)
- [`../../day-1/opnsense/validation.md`](../../day-1/opnsense/validation.md)
- [`../../day-1/network/segmentation.md`](../../day-1/network/segmentation.md)
- [`../backup/strategy.md`](../backup/strategy.md)
- [`../backup/restore-test.md`](../backup/restore-test.md)
