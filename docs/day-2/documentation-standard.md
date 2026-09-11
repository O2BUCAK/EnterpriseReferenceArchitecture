# Day 2 Documentation Standard

> Standard structure for documenting how an infrastructure component is operated, maintained, secured, recovered, and improved after deployment.

Day 2 documentation focuses on **repeatable operations** rather than one-time installation.

## Standard Lifecycle

```text
Observe
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
Review
 ↓
Improve
```

## Required Sections

### 1. Operational Purpose

What service or capability is operated and what business or infrastructure function it supports.

### 2. Ownership & Responsibility

Define the operational responsibility and required administrative access without embedding secrets or credentials.

### 3. Health Checks

Define the checks that establish whether the component is healthy.

Include daily, weekly, and monthly checks where appropriate.

### 4. Routine Operations

Document normal recurring tasks such as maintenance, user administration, certificate renewal, service checks, and capacity review.

### 5. Monitoring & Alerting

Define what should be monitored, what constitutes an abnormal condition, and which alerts require action.

### 6. Patch & Upgrade Management

Document the process for assessing, testing, applying, validating, and recording updates.

### 7. Backup & Restore

Document backup scope, frequency, retention, verification, restore procedure, and restore testing.

### 8. Security Operations

Document recurring access reviews, log review, privilege review, vulnerability management, certificate management, and security events.

### 9. Troubleshooting

Use a repeatable evidence-driven workflow:

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

### 10. Incident & Recovery Procedures

Describe what to do when normal operation fails. Include impact assessment, mitigation, recovery, validation, and post-incident actions.

### 11. Change Management

Operational changes should identify the reason, expected impact, implementation plan, validation, rollback considerations, and documentation requirements.

### 12. Capacity & Performance

Track relevant resource trends and define thresholds or indicators that trigger investigation or capacity planning.

### 13. Lifecycle Management

Document upgrade, replacement, retirement, and decommissioning procedures.

### 14. Validation Evidence

Record the evidence that demonstrates the operational procedure works. Restore tests and recovery drills should be explicitly recorded.

### 15. Implementation Status

Use the repository status convention. A documented runbook is not evidence that the procedure has already been executed in the lab.

## Runbook Principle

> **A good operational document should allow another administrator to perform the task safely without relying on undocumented tribal knowledge.**
