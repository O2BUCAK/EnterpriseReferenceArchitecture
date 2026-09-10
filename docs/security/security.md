# Security Architecture

> A high-level overview of the security architecture, principles, controls, and trust boundaries implemented across the Enterprise Reference Architecture.

## Purpose

This document describes the security architecture of the Enterprise Reference Architecture.
The environment is designed as a small-scale enterprise security reference platform that demonstrates how identity, network security, secrets management, access control, segmentation, and infrastructure automation can work together.

The design follows enterprise security principles while remaining practical enough to operate on modest hardware.

---

## Security Principles

### Zero Trust

No system, user, or network segment is implicitly trusted. Access should be explicitly authenticated, explicitly authorized, limited to the required scope, logged and auditable, and re-evaluated when appropriate.

### Zero Plaintext

Sensitive credentials and secrets should not be stored directly in source code, configuration files, Docker Compose files, Git repositories, automation playbooks, documentation, or committed environment files.
Secrets management is handled through dedicated infrastructure such as OpenBao.

### Least Privilege

Every account, service, and automation process should receive only the permissions required to perform its function.

### Defense in Depth

Security controls are distributed across network, firewall, identity, authentication, authorization, secrets management, host security, application security, logging/auditing, and automation layers.

### Secure by Default

Services should be deployed with restrictive defaults. Unnecessary ports, services, accounts, permissions, and network paths should remain disabled.

---

## Security Zones and Trust Boundaries

The environment uses network segmentation to establish security boundaries between management, identity, application, database, security/administrative, and external/WAN domains.

Segmentation is enforced primarily through the firewall and network policy. The database network is treated as a **network security segment**, not as an application VLAN.

Traffic between security zones should be explicitly allowed according to service requirements. Default-deny behavior is preferred over broad network access.

---

## Firewall and Network Security

OPNsense provides the primary network security boundary and is responsible for inter-VLAN traffic control, WAN connectivity, NAT, routing, firewall policies, network segmentation, administrative access restrictions, VPN functionality where required, and network-level logging.

Firewall rules should follow a default-deny model wherever practical and be based on source network, destination network, protocol, destination port, and required service function.

---

## Identity and Authentication

FreeIPA provides centralized identity and authentication services, including users, groups, host identities, Kerberos, LDAP, centralized access policies, and certificate management.

The architecture intentionally does not depend on Microsoft Active Directory. Local emergency or break-glass accounts may exist where operationally necessary, but their use should be restricted and audited.

---

## Application Authentication

Keycloak provides application-oriented identity and authentication capabilities including SSO, OpenID Connect, OAuth 2.0, SAML, identity federation, and centralized authentication policies.

Applications should avoid implementing independent authentication systems when centralized identity integration is practical.

---

## Privileged Access

Teleport is used as a controlled access layer for administrative connectivity.
Administrative access should be authenticated, authorized, auditable, limited by role and target system, and protected by strong authentication.

Direct exposure of SSH, RDP, database administration interfaces, or other management services to untrusted networks should be avoided.

---

## Secrets Management

OpenBao provides centralized secrets management for passwords, API tokens, application credentials, database credentials, certificates, encryption keys, and service credentials.

Secrets must not be committed to Git repositories.
Example configuration files should contain placeholders only.

---

## Container Security

Application workloads running on Docker should be isolated according to their function.
Security considerations include minimal container images, non-root containers where supported, restricted capabilities, limited filesystem access, explicit network connectivity, secure secret delivery, regular image updates, and avoidance of unnecessary published ports.

Docker isolation does not replace host or network-level security controls.

---

## Database Security

The PostgreSQL server is located in a dedicated database security segment.
Database access should be restricted to explicitly authorized application or administrative sources and should not be directly accessible from untrusted networks, general user networks, or the public Internet.

Application services should use dedicated database accounts rather than unrestricted administrative accounts.

---

## Host Security

Each infrastructure host should follow a hardened operating system baseline appropriate to its role.
Recommended controls include minimal package installation, regular security updates, firewall configuration, secure SSH configuration, strong authentication, restricted administrative access, disabling unnecessary services, centralized logging where practical, and time synchronization.

---

## Infrastructure Automation Security

Ansible and OpenTofu automate infrastructure deployment and configuration. Automation introduces privileged access and must therefore be treated as a security-sensitive component.

Automation credentials should use dedicated service identities, follow least privilege, avoid embedded passwords, retrieve secrets securely, be rotated periodically, and be protected from unauthorized modification.

Automation repositories must never contain production-like credentials or private keys.

---

## Certificate and TLS Security

Encrypted communication should be preferred whenever supported.
TLS should be used for web applications, administrative interfaces, APIs, authentication services, and other services carrying sensitive information.

Certificates and private keys should be managed securely. Private keys must never be committed to version control.
Internal services may use an internal certificate authority where appropriate.

---

## Logging and Auditing

Security-relevant activity should be logged whenever practical.
Important events include authentication attempts, failed authentication, privilege escalation, administrative access, firewall events, configuration changes, secrets access, infrastructure changes, and application security events.

Logs should provide enough information for troubleshooting and investigation without unnecessarily exposing sensitive information. Logs themselves should be treated as sensitive infrastructure data.

---

## Backup and Recovery Security

Backups are part of the security architecture.
Backup protection should include access control, encryption where appropriate, restricted administrative access, integrity verification, and regular recovery testing.

A backup that cannot be restored reliably should not be considered a successful backup.

---

## Security Monitoring

The architecture is designed to support future integration of centralized logging, intrusion detection, vulnerability scanning, configuration compliance, security event correlation, endpoint monitoring, and container image scanning.

Security monitoring should evolve alongside the infrastructure rather than being treated as a separate system.

---

## Security Lifecycle

Security is treated as a continuous process. The environment should periodically review identity and access permissions, firewall rules, exposed services, operating system updates, container images, application dependencies, secrets and credentials, certificates, backup integrity, and administrative accounts.

Changes should be documented and, where practical, implemented through automation.

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

The goal is not to claim that the lab represents a fully production-hardened enterprise environment. It provides a practical reference architecture for understanding and demonstrating modern enterprise security principles using primarily open-source technologies.
