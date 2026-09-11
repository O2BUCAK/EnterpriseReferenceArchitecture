# Security Operations Overview

> **Day 2 — Security Operations**

## Status

**Documented / Planned.** Security operations requirements are defined. The broader security stack is not yet fully implemented.

## 1. Objective

Maintain the security posture established during Day 1 and detect/respond to changes that could weaken it.

## 2. Operating Principles

- Zero Trust
- Zero Plaintext
- Least Privilege
- Defense in Depth
- Microsegmentation
- Secure by Default

## 3. Daily Security Review

For implemented components review:

- unexpected administrative activity;
- firewall events;
- service failures;
- configuration changes;
- exposed management services;
- unusual resource behavior.

## 4. Proxmox

Review:

- administrative access;
- VM changes;
- host updates;
- firewall state;
- storage anomalies;
- unexpected services.

## 5. OPNsense

Review:

- firewall events;
- WAN exposure;
- interface/gateway changes;
- NAT changes;
- administrative access;
- configuration changes.

## 6. Planned Security Services

The architecture includes planned services such as:

- FreeIPA
- Keycloak
- Teleport CE
- OpenBao

These remain Planned until deployed and validated.

## 7. Change Review

Security-sensitive changes should have:

- reason;
- affected boundary;
- expected traffic/behavior;
- rollback;
- positive validation;
- negative validation.

## 8. Incident Handling

Security-related anomalies should be handled through the incident-management process and documented with sufficient evidence to reproduce the investigation.

## 9. Public Repository Hygiene

Never publish:

- passwords;
- tokens;
- private keys;
- real infrastructure secrets;
- sensitive firewall exports;
- confidential logs.

Use documentation-only example domains and addresses where appropriate.
