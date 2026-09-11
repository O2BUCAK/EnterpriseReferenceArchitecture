# Lifecycle Management

> **Day 2 — Lifecycle**

## Status

**Documented / Planned.** Lifecycle management is defined as a target operating process.

## 1. Lifecycle Model

```text
Plan
 ↓
Deploy
 ↓
Operate
 ↓
Maintain
 ↓
Review
 ↓
Improve
 ↓
Retire
```

## 2. Lifecycle States

| State | Meaning |
|---|---|
| Planned | Architecture or future workload |
| Implemented | Actually deployed/configured |
| Validated | Implemented and explicitly tested |
| Operated | Subject to recurring operational practice |
| Retired | Removed from active architecture |

The project should never infer an operational state from documentation alone.

## 3. Review Questions

For each component ask:

- Is it still required?
- Is it healthy?
- Is it patched?
- Is it backed up?
- Can it be recovered?
- Is access still appropriate?
- Does the architecture documentation match reality?

## 4. Proxmox

Review the host and VM estate for:

- obsolete VMs;
- unused resources;
- old snapshots;
- storage growth;
- lifecycle state;
- recovery readiness.

## 5. OPNsense

Review:

- interfaces;
- gateways;
- firewall rules;
- NAT rules;
- DNS/DHCP configuration;
- administrative access;
- obsolete configuration.

## 6. Retirement

Before removing a component:

1. Identify dependencies.
2. Confirm backup/recovery requirements.
3. Remove consumers safely.
4. Remove the component.
5. Validate remaining services.
6. Update documentation.

## 7. Architecture Drift

Compare actual lab state with the documented architecture regularly.

If a component exists in the design but not in the lab, keep it **Planned**.

If a component exists in the lab but is absent from documentation, document it before considering the architecture complete.
