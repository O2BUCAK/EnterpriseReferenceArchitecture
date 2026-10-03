# Security Baseline — Build Runbook

## Purpose
Apply a consistent minimum security baseline after the infrastructure components are installed.

## Scope
Proxmox, OPNsense, Fedora/FreeIPA, Pardus/db01, Ubuntu/app01, RHEL/auto01 and deployed applications.

## Identity
- centralized identity where supported;
- separate human and service accounts;
- least privilege;
- no shared administrative credentials;
- sudo/HBAC reviewed.

## Network
- default deny between zones;
- management restricted to Management network;
- no WAN exposure for infrastructure administration;
- only documented application ports allowed;
- PostgreSQL/Redis restricted to required sources.

## Host
- supported packages/releases;
- regular patch process;
- time synchronization;
- host firewall where appropriate;
- SSH hardened according to operational requirements;
- unnecessary services disabled.

## Secrets
Never store passwords, private keys, API tokens or production credentials in Git.

Use secret scanning, pre-commit scanning and CI scanning where available.

## Containers
- pin images where practical;
- avoid privileged containers unless justified;
- minimize published ports;
- protect Docker socket;
- separate application networks;
- keep persistent data separate from ephemeral containers.

## Git / Supply Chain
The repository due-diligence baseline includes:
- CI/CD security;
- dependency/SBOM;
- branch protection/rulesets;
- SECURITY.md;
- automated security scanning;
- signed commits;
- IaC;
- secret scanning;
- dependency/version governance.

Backup/DR is intentionally outside the current laboratory scope where hardware does not support it.

## Validation
Every baseline item must have evidence or an explicit Planned/Future status. Do not mark a control implemented because a configuration file exists; test the control.
