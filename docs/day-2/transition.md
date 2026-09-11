# Day 1 → Day 2 Transition

> **From Build to Operations**

Day 1 establishes a working and validated infrastructure. Day 2 establishes the operational discipline required to keep that infrastructure secure, observable, recoverable, and maintainable.

## Status

**Documented / Planned.** This document defines the transition model. Operational processes should be marked Implemented only after they are actually used and evidenced in the lab.

---

## 1. Why the Transition Matters

An infrastructure is not finished when installation is complete.

The lifecycle used by this project is:

```text
Design
  ↓
Build
  ↓
Configure
  ↓
Validate
  ↓
Operate
  ↓
Maintain
  ↓
Recover
  ↓
Improve
```

Day 1 answers:

> **Can we build and validate the platform?**

Day 2 answers:

> **Can we operate and recover the platform repeatedly?**

---

## 2. Day 1 Exit Gate

A component should not enter normal Day 2 operation merely because installation succeeded.

Minimum Day 1 exit criteria:

1. Installation completed.
2. Base configuration completed.
3. Security baseline applied.
4. Dependencies integrated.
5. Positive tests passed.
6. Negative/security tests passed where applicable.
7. Reboot persistence verified.
8. Backup approach documented.
9. Recovery expectations documented.
10. Evidence recorded.
11. Known deviations recorded.
12. Implementation status updated honestly.

---

## 3. Component State Model

Use the project status vocabulary consistently.

| State | Meaning |
|---|---|
| Planned | Target architecture or future work |
| Documented | Design/procedure exists, implementation not implied |
| Implemented | Actually installed/configured in the lab |
| Validated | Implemented and explicitly tested |
| Future | Deliberately deferred beyond the current roadmap |

**Implemented must never be inferred from documentation alone.**

---

## 4. Day 1 Deliverables

For each implemented component, Day 1 should produce:

```text
Installation record
Configuration record
Security baseline
Validation record
Evidence
Known deviations
Backup/recovery prerequisites
Operational ownership
```

These become the inputs to Day 2.

---

## 5. Operational Handover Record

For every validated component, create an operational handover record.

Reference:

```text
Component:
Hostname / VM:
Role:
Status:
Owner:
Dependencies:
Management path:
Normal state:
Health checks:
Critical ports:
Backup:
Restore procedure:
Patch procedure:
Known failure modes:
Escalation path:
Last validation:
Next review:
```

This can later be represented in NetBox, Wiki.js, or another operational system, but those systems are Planned until implemented.

---

## 6. Day 1 to Day 2 Mapping

| Day 1 | Day 2 |
|---|---|
| Install | Operate |
| Configure | Maintain |
| Secure | Security Operations |
| Integrate | Monitor |
| Validate | Health Checks |
| Evidence | Operational Records |
| Backup preparation | Backup execution |
| Recovery design | Recovery testing |
| Known deviations | Change management |

---

## 7. Proxmox Transition

Day 1 establishes the Proxmox platform.

Day 2 must operate:

- Host health
- Storage health
- VM lifecycle
- Resource usage
- Updates
- Administrative access
- Backup
- Restore
- Configuration changes
- Hardware/resource capacity

Current implementation status remains dependent on actual lab evidence.

---

## 8. OPNsense Transition

Day 1 establishes firewall and routing behavior.

Day 2 must operate:

- Interface health
- Gateway status
- Firewall rules
- NAT
- DNS behavior
- DHCP where used
- Configuration backup
- Log review
- Firmware updates
- Rule changes
- Connectivity incidents

The eventual VLAN policy should become an operational control, not merely a design document.

---

## 9. Network Transition

Once segmentation is implemented and validated, Day 2 must include:

- VLAN health
- Gateway availability
- Inter-VLAN policy review
- Port mapping
- DHCP/DNS dependencies
- Network change control
- Connectivity troubleshooting
- Unauthorized traffic review

Until implemented, Network remains Planned.

---

## 10. FreeIPA Transition

Once FreeIPA is implemented and validated, Day 2 should cover:

- User lifecycle
- Group lifecycle
- Host enrollment
- Kerberos health
- DNS health
- Certificate lifecycle where enabled
- Sudo/access policies
- Administrative accounts
- Backup/restore
- Authentication incidents

FreeIPA is currently Planned.

---

## 11. PostgreSQL Transition

Once PostgreSQL is implemented and validated, Day 2 should cover:

- Database availability
- Connection health
- Storage usage
- WAL behavior
- Logs
- Role lifecycle
- Access review
- Backups
- Restore tests
- Updates
- Capacity
- Performance baseline

PostgreSQL is currently Planned.

---

## 12. Docker Transition

Once Docker is implemented and validated, Day 2 should cover:

- Container health
- Image lifecycle
- Application updates
- Network changes
- Persistent storage
- Resource usage
- Log rotation
- Backup
- Restore
- Failed-container recovery
- Security review
- Image provenance

Docker is currently Planned.

---

## 13. Operational Health Model

Each service should have a defined health model:

```text
Availability
    ↓
Service health
    ↓
Dependency health
    ↓
Performance
    ↓
Security state
    ↓
Capacity
    ↓
Recoverability
```

A service being reachable does not prove that it is healthy.

---

## 14. Routine Operations

Day 2 should distinguish routine work by frequency.

### Daily / Regular

- Review critical alerts.
- Check service health.
- Review important errors.
- Confirm backup jobs where implemented.

### Weekly

- Review capacity.
- Review security events.
- Review failed jobs.
- Review pending updates.
- Review operational anomalies.

### Monthly / Periodic

- Test restores.
- Review access.
- Review firewall rules.
- Review certificates.
- Review documentation.
- Review capacity trends.
- Review lifecycle status.

Actual frequencies should be adjusted after observing the lab rather than invented solely for documentation.

---

## 15. Change Management

Operational changes should follow:

```text
Request
  ↓
Impact assessment
  ↓
Backup / rollback preparation
  ↓
Change
  ↓
Validation
  ↓
Evidence
  ↓
Documentation update
```

A successful technical change that leaves documentation incorrect is not a complete change.

---

## 16. Incident Management

For an incident:

1. Identify the affected service.
2. Establish scope.
3. Protect evidence.
4. Restore service safely.
5. Validate dependencies.
6. Document the cause if known.
7. Record corrective action.
8. Update the runbook if the incident revealed a gap.

Do not turn an incident into undocumented trial-and-error configuration.

---

## 17. Backup and Recovery Transition

Day 1 defines how a service should be recoverable.

Day 2 proves that recovery remains possible.

Target cycle:

```text
Backup
  ↓
Verify
  ↓
Restore test
  ↓
Validate
  ↓
Record result
  ↓
Improve procedure
```

Restore testing is therefore an operational activity, not merely a backup configuration task.

---

## 18. Observability Transition

Day 1 identifies required signals.

Day 2 continuously uses them.

Target signals:

- Availability
- CPU
- Memory
- Storage
- Network
- Authentication
- Firewall events
- Application errors
- Database health
- Backup status

Centralized observability remains Planned until implemented.

---

## 19. Documentation as an Operational Control

Operational documentation must remain synchronized with the lab.

When the implementation changes:

```text
Lab change
   ↓
Validation
   ↓
Evidence
   ↓
Documentation update
```

Do not document an architecture that the lab no longer follows as if it were current implementation.

---

## 20. Day 2 Readiness Criteria

A component is ready for normal Day 2 operation when:

- Its purpose is documented.
- Its dependencies are known.
- Its health checks are defined.
- Its normal state is understood.
- Its administrative path is known.
- Its backup method is known.
- Its recovery procedure exists.
- Its security controls are known.
- Its update procedure exists.
- Its common failure modes are documented.
- Its current status is backed by evidence.

---

## 21. Project-Level Transition Gate

The complete lab can move from Day 1 build mode toward Day 2 operational mode when the core implemented architecture has passed its component validation gates.

This does **not** require every planned service to exist.

Instead, the project should operate what has actually been built while keeping future architecture clearly marked as Planned.

---

## Related Documentation

- [`README.md`](README.md) — Day 2 overview
- [`index.md`](index.md) — Day 2 documentation index
- [`documentation-standard.md`](documentation-standard.md) — Day 2 documentation standard
- [`../day-1/README.md`](../day-1/README.md) — Day 1 overview
- [`../day-1/documentation-standard.md`](../day-1/documentation-standard.md) — Day 1 documentation standard
- [`../day-1/validation/day-1-checklist.md`](../day-1/validation/day-1-checklist.md) — Day 1 acceptance checklist
