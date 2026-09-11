# Proxmox VE — Monitoring

> **Day 2 — Observe**

This document defines the monitoring model for the Proxmox VE host and its virtual machines.

## Status

**Documented / Planned.** Proxmox is implemented, but centralized monitoring is not currently implemented in the lab.

---

## 1. Monitoring Objectives

Monitoring should answer:

- Is the host available?
- Are expected VMs running?
- Is capacity sufficient?
- Is storage healthy?
- Is the network healthy?
- Are failures developing before users notice them?

---

## 2. Monitoring Layers

```text
Physical Host
     ↓
Proxmox Node
     ↓
VM Resources
     ↓
Guest OS
     ↓
Application
```

A healthy Proxmox node does not prove that every guest application is healthy.

---

## 3. Host Availability

Monitor:

- Node availability
- Uptime
- Proxmox service state
- System load
- Failed systemd units

Example checks:

```bash
uptime
systemctl --failed
systemctl status pveproxy
systemctl status pvedaemon
```

---

## 4. CPU

Monitor:

- Host CPU utilization
- Sustained load
- VM CPU pressure
- CPU contention

Investigate sustained abnormal utilization rather than reacting to short-lived peaks.

---

## 5. Memory

Monitor:

- Host memory usage
- VM allocation
- Available memory
- Swap activity where applicable

Memory exhaustion is particularly important on the current 32 GiB lab host.

---

## 6. Storage

Monitor:

- Storage availability
- Capacity
- Disk utilization
- VM disk growth
- Backup storage growth
- Snapshot accumulation

Example:

```bash
df -h
pvesm status
```

Define warning and critical thresholds during actual lab operation based on observed capacity.

---

## 7. Network

Monitor:

- Physical interface state
- Bridge state
- Packet errors where observable
- VM connectivity
- Gateway reachability

VLAN-specific monitoring becomes applicable after VLAN segmentation is implemented.

---

## 8. VM State

Track expected VM state.

Example inventory:

| VM | Expected state | Current architecture status |
|---|---|---|
| `fw01` | Running | Implemented |
| `ipa01` | Planned | Planned |
| `db01` | Planned | Planned |
| `app01` | Planned | Planned |
| `auto01` | Planned | Planned |

Do not generate operational alerts for services that have not yet been deployed.

---

## 9. QEMU Guest Agent

Where enabled, use the QEMU Guest Agent to improve guest visibility and lifecycle operations.

Agent availability should be treated as a useful signal, not as proof that the application is healthy.

---

## 10. Alerting Principles

Alerts should be actionable.

Prefer:

```text
Condition
  ↓
Severity
  ↓
Impact
  ↓
Action
```

Avoid creating alerts that produce noise without an operational response.

---

## 11. Suggested Initial Signals

| Signal | Purpose |
|---|---|
| Node unavailable | Host failure |
| High CPU | Capacity/performance |
| Low available memory | Capacity risk |
| Storage capacity | Prevent outage |
| Storage unavailable | Data availability |
| Unexpected VM stopped | Service availability |
| Proxmox service failure | Management availability |
| Network interface failure | Connectivity |
| Backup failure | Recoverability |

Backup monitoring becomes active after backup is implemented.

---

## 12. Centralized Monitoring

A centralized monitoring platform is planned for the broader architecture.

Possible future components should be selected based on actual requirements rather than added solely for tool count.

Until then, Proxmox and guest-native checks provide the baseline.

---

## 13. Operational Response

When an alert occurs:

1. Confirm the alert.
2. Determine scope.
3. Check recent changes.
4. Inspect dependencies.
5. Collect evidence.
6. Recover safely.
7. Validate.
8. Document the event.

Do not silence recurring alerts without addressing the underlying cause.

---

## 14. Monitoring Evidence

For important events record:

```text
Timestamp:
Signal:
Severity:
Affected node/VM:
Observed value:
Expected value:
Impact:
Action:
Result:
Follow-up:
```

## Related Documentation

- [`operations.md`](operations.md)
- [`../monitoring/overview.md`](../monitoring/overview.md)
- [`../incident-management/process.md`](../incident-management/process.md)
- [`../capacity-management/overview.md`](../capacity-management/overview.md)
