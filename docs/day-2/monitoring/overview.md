# Monitoring & Observability Overview

> **Day 2 — Monitoring**

## Status

**Documented / Planned.** Monitoring requirements are defined, but a centralized observability platform has not yet been implemented in the lab.

## 1. Purpose

Monitoring should answer four questions:

1. Is the infrastructure available?
2. Is it healthy?
3. Is it behaving as expected?
4. Is there enough evidence to investigate an incident?

A dashboard alone is not observability.

## 2. Current Scope

Currently implemented:

- Proxmox VE
- OPNsense

Planned:

- Centralized metrics
- Centralized logs
- Alerting
- Service-level health checks
- Historical trend analysis

## 3. Monitoring Layers

```text
Infrastructure
    ↓
Host / Hypervisor
    ↓
Network / Firewall
    ↓
VM / OS
    ↓
Service
    ↓
Application
    ↓
User-facing function
```

Each layer should have an observable health signal.

## 4. Proxmox Signals

Monitor:

- Node availability
- CPU utilization
- Memory utilization
- Storage utilization
- VM state
- Failed services
- Network interface state
- Backup status when implemented
- Time synchronization

See [`../proxmox/monitoring.md`](../proxmox/monitoring.md).

## 5. OPNsense Signals

Monitor:

- Firewall availability
- WAN/LAN interfaces
- Gateway state
- CPU/RAM/storage
- Firewall events
- DNS/DHCP health where enabled
- Configuration changes
- System logs

See [`../opnsense/monitoring.md`](../opnsense/monitoring.md).

## 6. Alert Principles

Alerts should be:

- actionable;
- meaningful;
- tied to an operational response;
- resistant to unnecessary noise.

Example:

```text
Condition → Alert → Investigation → Action → Validation
```

Do not create alerts that have no defined response.

## 7. Evidence

When investigating an issue, capture:

- timestamp;
- affected system;
- observed symptom;
- relevant metrics;
- relevant logs;
- action taken;
- post-change state.

Never include credentials or secrets in evidence.

## 8. Implementation Boundary

The existence of this document does not mean centralized monitoring has been deployed.

The monitoring stack becomes **Implemented** only after deployment, configuration and validation in the lab.
