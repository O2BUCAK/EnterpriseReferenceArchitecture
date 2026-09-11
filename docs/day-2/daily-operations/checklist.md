# Daily Operations Checklist

> **Day 2 — Daily Operations**

## Status

**Documented.** This checklist defines the intended daily operational routine. It is not evidence that the routine has already been executed on a recurring basis.

## 1. Scope

The daily review covers the infrastructure currently implemented in the lab:

- Proxmox VE
- OPNsense (`fw01`)

Planned components are excluded from operational status until deployed.

## 2. Daily Health Check

### Proxmox

- [ ] Node is reachable.
- [ ] No unexpected critical alerts.
- [ ] CPU load reviewed.
- [ ] Memory utilization reviewed.
- [ ] Storage utilization reviewed.
- [ ] Expected VMs are running.
- [ ] Failed services reviewed.
- [ ] Time synchronization reviewed.

### OPNsense

- [ ] `fw01` is reachable.
- [ ] WAN/LAN interfaces are operational.
- [ ] Gateway status is healthy.
- [ ] Unexpected firewall events reviewed.
- [ ] DNS/DHCP health reviewed where applicable.
- [ ] CPU/RAM/storage reviewed.
- [ ] Recent configuration changes reviewed.

## 3. Exceptions

Investigate when:

- a node or firewall is unavailable;
- storage consumption changes unexpectedly;
- a VM repeatedly restarts;
- a gateway becomes unavailable;
- unexpected firewall activity appears;
- time synchronization fails;
- a service reports degraded health.

Do not make unrelated configuration changes while investigating an incident.

## 4. Evidence

For a recurring operational process, record only meaningful exceptions and required evidence rather than collecting screenshots without purpose.

Suggested record:

```text
Date:
Operator:
Systems checked:
Exceptions:
Actions:
Validation:
Follow-up:
```

## 5. Completion Criteria

The daily operational check is complete when all implemented components have been reviewed and any anomaly has either been resolved, documented, or escalated.

## Related Runbooks

- [`../proxmox/operations.md`](../proxmox/operations.md)
- [`../proxmox/monitoring.md`](../proxmox/monitoring.md)
- [`../opnsense/operations.md`](../opnsense/operations.md)
- [`../opnsense/monitoring.md`](../opnsense/monitoring.md)
