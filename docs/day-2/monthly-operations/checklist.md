# Monthly Operations Checklist

> **Day 2 — Monthly Operations**

## Status

**Documented.** This defines the target monthly operational review and is not evidence of completed recurring execution.

## 1. Infrastructure Review

- [ ] Review Proxmox capacity trends.
- [ ] Review VM inventory against the architecture.
- [ ] Review storage capacity and growth.
- [ ] Review OPNsense availability and gateway history.
- [ ] Review network changes.
- [ ] Review backup and recovery readiness.

## 2. Security Review

- [ ] Review administrative accounts and privileges.
- [ ] Review firewall policy changes.
- [ ] Review management-plane exposure.
- [ ] Review patch status.
- [ ] Review security-related incidents.
- [ ] Confirm public documentation contains no credentials or sensitive data.

## 3. Backup and Recovery Review

- [ ] Review backup success/failure history.
- [ ] Review retention.
- [ ] Confirm backup storage capacity.
- [ ] Review the latest restore-test evidence when restore testing is implemented.
- [ ] Identify recovery procedures that still require validation.

## 4. Capacity and Lifecycle

- [ ] Review CPU and memory growth.
- [ ] Review disk growth.
- [ ] Identify obsolete VMs, snapshots or configurations.
- [ ] Compare actual infrastructure against the target architecture.
- [ ] Record capacity risks.

## 5. Documentation and Improvement

- [ ] Review runbooks for accuracy.
- [ ] Update procedures after significant changes.
- [ ] Record lessons learned.
- [ ] Identify the next improvement priorities.
- [ ] Keep implementation status aligned with actual lab state.

## 6. Monthly Record

```text
Period:
Operator:
Infrastructure state:
Security findings:
Capacity findings:
Backup/recovery findings:
Changes:
Open issues:
Improvement actions:
```

## 7. Completion Criteria

The monthly review is complete when infrastructure, security, recovery, capacity and documentation have been reviewed and resulting actions have owners or a documented decision.
