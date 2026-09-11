# OPNsense — Monitoring

> **Day 2 — Observe**

This document defines the monitoring model for `fw01`.

## Status

**Documented / Planned.** OPNsense is implemented, but centralized monitoring is not currently implemented.

---

## 1. Monitoring Objectives

Monitoring should identify:

- Firewall availability
- Interface failures
- Gateway failures
- Resource pressure
- Unexpected traffic
- Authentication failures
- Configuration anomalies
- Connectivity degradation

---

## 2. Monitoring Layers

```text
Proxmox VM
   ↓
OPNsense OS
   ↓
Interfaces
   ↓
Gateways
   ↓
Firewall/NAT
   ↓
DNS/DHCP
   ↓
Client connectivity
```

---

## 3. Availability

Monitor:

- `fw01` availability
- Web UI availability from the management path
- Firewall service health
- Network interface state

A reachable web interface does not prove that forwarding and firewall policy are healthy.

---

## 4. Resource Monitoring

Track:

- CPU
- Memory
- Storage
- System load
- Log growth

Investigate sustained abnormal values rather than isolated spikes.

---

## 5. Interface Monitoring

For each interface monitor:

- Link state
- Traffic volume
- Errors/drops where available
- Unexpected state changes

An interface failure should be correlated with Proxmox and upstream network state.

---

## 6. Gateway Monitoring

Monitor:

- Gateway availability
- Latency
- Packet loss where available
- State transitions

Distinguish:

```text
Gateway unavailable
≠
DNS unavailable
≠
Destination unavailable
```

---

## 7. Firewall Events

Review:

- Repeated denies
- Unexpected inbound traffic
- Unexpected outbound traffic
- Rule changes
- Authentication failures

Use the architecture to establish what traffic is expected before treating a deny as suspicious.

---

## 8. NAT Monitoring

Monitor significant NAT behavior when troubleshooting connectivity.

Unexpected connectivity changes should trigger review of:

- NAT rule changes
- Firewall rule changes
- Routing
- Interface assignment

---

## 9. DNS/DHCP Monitoring

Where enabled, monitor:

- DNS service availability
- DNS resolution failures
- DHCP service availability
- Scope utilization
- Unexpected lease growth

The eventual FreeIPA DNS architecture will change the operational ownership of DNS.

---

## 10. Management Security Monitoring

Track:

- Failed administrative logins
- Successful administrative access where auditable
- Unexpected management-source addresses
- Configuration changes

Management interfaces should remain restricted to intended administrative networks.

---

## 11. Alerting Principles

Alerts must be actionable.

Example:

```text
Gateway down
   ↓
Check interface
   ↓
Check upstream
   ↓
Check routing/NAT
   ↓
Recover
   ↓
Validate
```

Avoid alerting on every expected firewall deny.

---

## 12. Centralized Monitoring

A centralized monitoring platform is planned for the wider architecture.

Until implemented, use OPNsense-native dashboards and logs as the operational baseline.

---

## 13. Evidence

For important events record:

```text
Timestamp:
Signal:
Severity:
Interface/gateway/service:
Observed state:
Expected state:
Impact:
Action:
Result:
Follow-up:
```

## Related Documentation

- [`operations.md`](operations.md)
- [`../monitoring/overview.md`](../monitoring/overview.md)
- [`../incident-management/process.md`](../incident-management/process.md)
