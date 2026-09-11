# Backup & Restore Test Procedure

> **Day 2 — Recover**

## Status

**Documented / Planned.** The procedure is defined. It must not be marked Validated until an actual restore test is executed and evidence is retained.

## 1. Objective

Prove that a backup can be converted into a working system or configuration, rather than merely proving that a backup job completed.

## 2. Test Preparation

Before testing:

- identify the backup;
- record its creation date;
- identify the source system;
- define the expected result;
- define the validation tests;
- ensure the test environment will not disrupt the live system.

## 3. Proxmox VM Restore

Target procedure:

1. Select a known backup.
2. Restore to the intended test location.
3. Confirm VM configuration.
4. Start the restored VM.
5. Validate boot.
6. Validate network behavior.
7. Validate required services.
8. Compare the restored state with the expected backup point.
9. Record evidence.

## 4. OPNsense Configuration Restore

Target procedure:

1. Select a known-good configuration backup.
2. Confirm the target `fw01` instance.
3. Restore configuration using the supported OPNsense mechanism.
4. Reboot or reload services when required.
5. Validate interfaces.
6. Validate gateway connectivity.
7. Validate DNS/DHCP where applicable.
8. Validate firewall policy.
9. Confirm management access.
10. Record evidence.

## 5. Negative Validation

Recovery testing should also prove that recovery did not introduce an unsafe state.

Examples:

- management access remains restricted;
- unintended WAN management is not exposed;
- firewall deny rules remain effective;
- expected network boundaries remain intact.

## 6. Evidence

```text
Test date:
Operator:
Backup identifier:
Source system:
Restore target:
Restore result:
Services validated:
Security controls validated:
Problems found:
Recovery duration:
Evidence location:
```

Do not store secrets or sensitive configuration exports in the public repository.

## 7. Acceptance Criteria

A restore test passes when:

- the backup can be restored;
- the restored system reaches the expected state;
- intended services operate;
- security boundaries remain correct;
- evidence is recorded.

Only then may the relevant recovery capability be marked **Validated**.
