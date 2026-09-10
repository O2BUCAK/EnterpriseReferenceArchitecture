# Security Architecture

> Security principles and target controls for the Enterprise Reference Architecture.

## Status

**Documented / Planned architecture.**

This document describes the security model and intended controls. It does not claim that all controls or security services are currently implemented in the lab.

## Status Convention

| Status | Meaning |
|---|---|
| **Implemented** | Installed, configured, and tested in the lab |
| **Planned** | Defined in the architecture but not yet implemented |
| **Future** | Deferred to a later phase |
| **Documented** | Design decision only |

---

## Purpose

The security architecture defines how identity, network security, access control, secrets management, segmentation, host security, application security, logging, and future automation should work together.

---

## Security Principles

### Zero Trust

No system, user, or network segment should be implicitly trusted. Access should be authenticated, authorized, limited to the required scope, and auditable.

### Zero Plaintext

Sensitive credentials and secrets should not be stored directly in source code, configuration files, Docker Compose files, Git repositories, documentation, or committed environment files.

### Least Privilege

Accounts, services, and automation processes should receive only the permissions required for their function.

### Defense in Depth

Security should be distributed across network, firewall, identity, authentication, authorization, secrets, host, application, and logging layers.

### Secure by Default

Unnecessary ports, services, accounts, permissions, and network paths should remain disabled.

---

## Network Security — Partly Implemented / Target Design

OPNsense is an **Implemented** component of the lab. The broader VLAN segmentation and policy model documented here represents the target architecture and should only be marked implemented after it has been configured and validated in the lab.

The target model uses default-deny inter-VLAN communication and explicit service-specific rules.

---

## Identity and Authentication — Planned

The target identity model uses FreeIPA for infrastructure identity and Keycloak for application-oriented authentication and SSO.

Both are **Planned** unless separately validated as implemented.

---

## Privileged Access — Planned

Teleport CE is a planned controlled administrative access layer.

Direct exposure of management interfaces to untrusted networks should be avoided.

---

## Secrets Management — Planned

OpenBao is planned for centralized secrets management.

Secrets must never be committed to the public repository, regardless of whether OpenBao has yet been implemented.

---

## Container Security — Planned

Docker is a planned application platform. When implemented, container workloads should use minimal images, non-root execution where supported, restricted capabilities, limited filesystem access, explicit networks, secure secret delivery, and controlled published ports.

Docker isolation does not replace host or network security.

---

## Database Security — Planned

PostgreSQL on `db01` is a planned database layer.

The target architecture places database services in a dedicated network segment and permits access only from explicitly authorized sources.

---

## Host Security — Design

Each future infrastructure host should follow a hardened baseline appropriate to its role, including security updates, secure administrative access, restricted services, logging, and time synchronization.

The exact controls will be documented and validated during implementation.

---

## Infrastructure Automation Security — Future / Planned

Ansible and OpenTofu are planned but the lab has **not yet reached the Automation & IaC phase**.

When implemented, automation credentials must use dedicated identities, least privilege, secure secret retrieval, and version-controlled configuration without embedded credentials.

---

## Certificate and TLS Security — Design

Encrypted communication should be preferred wherever supported. Certificates and private keys must be protected and must never be committed to version control.

---

## Logging and Auditing — Future / Planned

Security-relevant events should be logged as the architecture matures, including authentication, privilege changes, firewall events, configuration changes, secrets access, and infrastructure changes.

Centralized logging and security monitoring are future capabilities unless explicitly validated as implemented.

---

## Backup and Recovery Security — Future / Planned

Backups should use appropriate access control, encryption where required, integrity verification, and regular recovery testing.

A backup strategy is a future operational capability unless implementation evidence exists.

---

## Security Monitoring — Future

Future capabilities may include centralized logging, intrusion detection, vulnerability scanning, configuration compliance, security event correlation, endpoint monitoring, and container image scanning.

---

## Security Objectives

The architecture aims to demonstrate:

* Centralized identity
* Strong authentication
* Least-privilege access
* Network segmentation
* Default-deny firewall policies
* Secure administrative access
* Centralized secrets management
* Encrypted communications
* Container isolation
* Protected database access
* Auditable infrastructure changes
* Reproducible security configuration

These are architectural objectives. They should not be presented as completed capabilities until they are implemented and validated in the lab.

---

## Summary

The security documentation intentionally separates **security design** from **security implementation**.

The project does not claim a control is implemented merely because the architecture specifies it. Implementation status must be established through actual laboratory deployment and validation.
