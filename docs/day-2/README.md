# Day 2 — Operate & Maintain

> **Day 2** defines how the infrastructure is operated, maintained, secured, recovered, and continuously improved after deployment.

Day 2 is the operational lifecycle of the architecture. It answers the question:

> **How do we keep this infrastructure healthy tomorrow, next week, next month, and throughout its lifecycle?**

## Lifecycle

```text
Monitor
   ↓
Operate
   ↓
Maintain
   ↓
Secure
   ↓
Backup
   ↓
Recover
   ↓
Improve
```

## Current Status

Day 2 is an **operational framework and planned workstream** at the current project stage. It must not be interpreted as evidence that all operational procedures have already been implemented in the lab.

| Area | Status |
|---|---|
| Daily operations | **Planned** |
| Weekly operations | **Planned** |
| Monthly maintenance | **Planned** |
| Monitoring & alerting | **Planned** |
| Patch management | **Planned** |
| Backup & restore testing | **Planned** |
| Disaster recovery | **Planned** |
| Security operations | **Planned** |
| Identity operations | **Planned** |
| Change management | **Planned** |
| Incident management | **Planned** |
| Capacity management | **Planned** |
| Troubleshooting runbooks | **Planned** |
| Lifecycle management | **Planned** |
| Operational documentation | **Planned** |

## Planned Day 2 Structure

### 01 — Daily Operations

- Infrastructure health
- VM and service availability
- Storage health
- Firewall status
- Authentication failures
- Database health
- Container health
- Critical alerts

### 02 — Weekly Operations

- Health review
- Backup review
- Security event review
- Capacity review
- Certificate review
- Known issue review
- Operational checklist

### 03 — Monthly Operations

- OS and application maintenance
- Patch review
- Certificate lifecycle review
- User and privilege review
- Backup restore test
- Capacity trends
- Documentation review

### 04 — Monitoring & Observability

- Availability
- Performance
- Capacity
- Logs
- Security events
- Alerting
- Service-level health

### 05 — Patch Management

The process should follow:

```text
Identify
   ↓
Assess
   ↓
Test
   ↓
Approve
   ↓
Deploy
   ↓
Validate
   ↓
Document
```

### 06 — Backup & Restore

- Backup scope
- Backup frequency
- Retention
- Storage location
- Encryption
- Backup verification
- Restore procedures
- Periodic restore testing

> **A successful backup job is not proof of recoverability. Restore testing is required.**

### 07 — Disaster Recovery

Planned scenarios include:

- Proxmox host failure
- Firewall failure
- Identity service failure
- Database failure
- VM corruption
- Storage failure
- Application failure

Each scenario should have a documented recovery procedure, validation criteria, and rollback considerations.

### 08 — Security Operations

- Log review
- Authentication review
- Privilege review
- Firewall rule review
- Certificate management
- Vulnerability management
- Secrets management
- Security incident response

### 09 — Identity Operations

- User lifecycle
- Group management
- Host management
- Access review
- Privilege review
- HBAC / sudo policy review
- Certificate lifecycle
- Dormant account review

### 10 — Change Management

Operational changes should follow a controlled lifecycle:

```text
Request
   ↓
Assess
   ↓
Plan
   ↓
Implement
   ↓
Validate
   ↓
Document
```

### 11 — Incident Management

```text
Detection
   ↓
Classification
   ↓
Investigation
   ↓
Mitigation
   ↓
Recovery
   ↓
Root Cause Analysis
   ↓
Preventive Action
```

Incident documentation should capture what happened, evidence collected, actions taken, service impact, root cause, and preventive measures.

### 12 — Capacity Management

Track trends for:

- CPU
- Memory
- Storage
- I/O
- Network
- VM density
- Database resources

Capacity decisions should be based on **trend, cause, forecast, and action**, rather than a single utilization value.

### 13 — Troubleshooting

The reference troubleshooting methodology is:

```text
Problem
   ↓
Scope
   ↓
Symptoms
   ↓
Evidence
   ↓
Hypothesis
   ↓
Test
   ↓
Root Cause
   ↓
Fix
   ↓
Validation
   ↓
Documentation
```

### 14 — Lifecycle Management

```text
Plan
   ↓
Deploy
   ↓
Operate
   ↓
Maintain
   ↓
Upgrade
   ↓
Replace
   ↓
Retire
```

This applies to operating systems, VMs, applications, databases, certificates, and infrastructure components.

### 15 — Operational Documentation

Operational knowledge should be maintained as reusable documentation:

- Runbooks
- Standard Operating Procedures (SOPs)
- Checklists
- Troubleshooting guides
- Recovery procedures
- Known issues
- Change records
- Incident records
- Validation evidence

## Day 2 Principle

> **Running infrastructure is not the end of the project. Operating, maintaining, recovering, and improving it is part of the architecture.**
