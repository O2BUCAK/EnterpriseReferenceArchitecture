# Operational Runbook Standard

> **Day 2 — Documentation as an Operational Control**

## Status

**Documented.** This standard defines how future operational runbooks should be written and maintained.

## 1. Purpose

A runbook should allow a known operator to perform a routine task, investigate a common failure, or recover a service without relying on undocumented tribal knowledge.

## 2. Required Sections

Operational runbooks should contain, where applicable:

1. Purpose
2. Status
3. Scope
4. Preconditions
5. Procedure
6. Validation
7. Rollback/Recovery
8. Security considerations
9. Evidence
10. Completion criteria
11. Related documentation

## 3. Status Discipline

Use status labels carefully:

- **Documented** — procedure exists in the repository.
- **Planned** — intended future capability/process.
- **Implemented** — actually deployed/configured in the lab.
- **Validated** — implemented and explicitly tested.

Writing a procedure never changes the implementation state of the underlying system.

## 4. Procedure Quality

Prefer:

- ordered steps;
- explicit prerequisites;
- clear expected results;
- safe rollback;
- positive and negative validation;
- evidence requirements.

Avoid:

- unexplained commands;
- assumed prerequisites;
- credentials in examples;
- claims without evidence;
- destructive steps without warnings.

## 5. Evidence

Evidence should prove the result, not merely prove that a command was typed.

Useful evidence can include:

- command output;
- service state;
- relevant UI state;
- connectivity test;
- backup/restore result;
- firewall positive/negative test.

## 6. Change Control

When an operational procedure changes:

1. Update the runbook.
2. Validate the procedure when practical.
3. Record important lessons learned.
4. Keep architecture documentation consistent with the real lab.

## 7. Security

Never place secrets in runbooks committed to the public repository.

Use placeholders such as:

```text
<ADMIN_USER>
<HOSTNAME>
<IP_ADDRESS>
<SECRET>
```

## 8. Runbook Acceptance

A runbook is considered useful when another technically competent operator can understand its prerequisites, execute it safely, verify the result and recover from a failure without undocumented assumptions.
