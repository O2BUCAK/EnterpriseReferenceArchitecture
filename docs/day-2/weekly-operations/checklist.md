# Weekly Operations Checklist

> **Day 2 — Weekly Operations**

## Status

**Documented.** The checklist defines the target weekly review process. It is not evidence of recurring execution.

## 1. Platform Review

### Proxmox

- [ ] Review node health and failed services.
- [ ] Review CPU, memory and storage trends.
- [ ] Review VM inventory and unexpected state changes.
- [ ] Review snapshots and remove obsolete ones where appropriate.
- [ ] Review backup status when backup infrastructure is available.
- [ ] Review pending updates.
- [ ] Review administrative access and recent changes.

### OPNsense

- [ ] Review gateway health and uptime.
- [ ] Review interface errors and abnormal traffic.
- [ ] Review firewall events for anomalies.
- [ ] Review DNS/DHCP operation where enabled.
- [ ] Review configuration changes.
- [ ] Confirm configuration backup availability when implemented.
- [ ] Review pending updates.

## 2. Security Review

- [ ] Review unexpected authentication activity.
- [ ] Review administrative changes.
- [ ] Review exposed management services.
- [ ] Confirm no secrets were added to repository documentation.
- [ ] Review firewall rule changes.

## 3. Capacity Review

Review trends for:

- CPU
- Memory
- Storage
- VM growth
- Backup storage

Investigate sustained pressure rather than reacting to isolated peaks.

## 4. Documentation Review

- [ ] Update runbooks after meaningful changes.
- [ ] Record unresolved operational issues.
- [ ] Update implementation status only when lab evidence supports the change.
- [ ] Record lessons learned.

## 5. Completion Criteria

The weekly review is complete when health, security, capacity, backup readiness and documentation have been reviewed for all implemented components.
