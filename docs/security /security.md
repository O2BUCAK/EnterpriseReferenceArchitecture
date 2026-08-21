# Security Architecture

> A high-level overview of the security architecture, principles, controls, and trust boundaries implemented across the Enterprise Reference Architecture.

## Purpose

This document describes the security architecture of the Enterprise Reference Architecture.
The environment is designed as a small-scale enterprise security reference platform that demonstrates how identity, network security, secrets management, access control, segmentation, and infrastructure automation can work together.
The design follows enterprise security principles while remaining practical enough to operate on modest hardware.

---

## Security Principles

The architecture is built around the following principles:

### Zero Trust

No system, user, or network segment is implicitly trusted.

Access should be:

* Explicitly authenticated
* Explicitly authorized
* Limited to the required scope
* Logged and auditable
* Re-evaluated when appropriate

Network location alone is not considered sufficient proof of trust.

### Zero Plaintext

Sensitive credentials and secrets should not be stored directly in:

* Source code
* Configuration files
* Docker Compose files
* Git repositories
* Automation playbooks
* Documentation
* Environment files committed to version control

Secrets management is handled through dedicated infrastructure such as OpenBao.

### Least Privilege

Every account, service, and automation process should receive only the permissions required to perform its function.
Administrative access should be separated from normal user access whenever practical.

### Defense in Depth

Security controls are distributed across multiple layers:

1. Network
2. Firewall
3. Identity
4. Authentication
5. Authorization
6. Secrets management
7. Host security
8. Application security
9. Logging and auditing
10. Automation

A failure of one control should not automatically result in unrestricted access to the environment.

### Secure by Default

Services should be deployed with restrictive defaults.

Unnecessary:

* Ports
* Services
* Accounts
* Permissions
* Network paths

should remain disabled.

---

## Security Zones and Trust Boundaries

The environment uses network segmentation to establish security boundaries between infrastructure domains.

The primary security boundaries include:

* Management infrastructure
* Identity services
* Application services
* Database services
* Security and administrative services
* External/WAN connectivity

Segmentation is enforced primarily through the firewall and network policy.
The database network is treated as a **network security segment**, not as an application VLAN. Database systems should not be directly reachable from untrusted or user-facing networks.
Traffic between security zones should be explicitly allowed according to service requirements.
Default-deny behavior is preferred over broad network access.

---

## Firewall and Network Security

OPNsense provides the primary network security boundary.

The firewall is responsible for:

* Inter-VLAN traffic control
* WAN connectivity
* NAT
* Routing
* Firewall policies
* Network segmentation
* Administrative access restrictions
* VPN functionality where required
* Network-level logging

Firewall rules should follow a default-deny model wherever practical.

Rules should be based on:

* Source network
* Destination network
* Protocol
* Destination port
* Required business/service function

Broad rules such as unrestricted access between internal networks should be avoided.

---

## Identity and Authentication

FreeIPA provides centralized identity and authentication services.

The identity platform is responsible for:

* User identities
* Groups
* Host identities
* Kerberos authentication
* LDAP directory services
* Centralized access policies
* Certificate management

The architecture intentionally does not depend on Microsoft Active Directory.
Identity should be centralized where practical instead of maintaining independent local accounts across every system.
Local emergency or break-glass accounts may exist where operationally necessary, but their use should be restricted and audited.

---

## Application Authentication

Keycloak provides application-oriented identity and authentication capabilities.

Keycloak can provide:

* Single Sign-On
* OpenID Connect
* OAuth 2.0
* SAML
* Application identity federation
* Centralized authentication policies

Applications should avoid implementing independent authentication systems when centralized identity integration is practical.
This reduces duplicated credentials and simplifies access management.

---

## Privileged Access

Teleport is used as a controlled access layer for administrative connectivity.
The objective is to avoid exposing administrative services directly whenever possible.

Administrative access should be:

* Authenticated
* Authorized
* Auditable
* Limited by role
* Limited by target system
* Protected by strong authentication

Direct exposure of SSH, RDP, database administration interfaces, or other management services to untrusted networks should be avoided.

---

## Secrets Management

OpenBao provides centralized secrets management.

Sensitive information such as:

* Passwords
* API tokens
* Application credentials
* Database credentials
* Certificates
* Encryption keys
* Service credentials

should be stored in the secrets management system rather than in application configuration or source control.
Applications and automation should retrieve secrets dynamically when practical.

### Secret Handling Rules

Secrets must not be committed to Git repositories.

Examples of prohibited practices include:

```text
DB_PASSWORD=SuperSecretPassword
API_TOKEN=xxxxxxxx
PRIVATE_KEY=...
```

inside committed configuration files.
Example configuration files should contain placeholders only.

---

## Container Security

Application workloads running on Docker should be isolated according to their function.

Container security considerations include:

* Minimal container images
* Non-root containers where supported
* Restricted capabilities
* Limited filesystem access
* Explicit network connectivity
* Secrets supplied through secure mechanisms
* Regular image updates
* Avoiding unnecessary published ports

Docker networks should be used to provide logical separation between application components.
Container isolation does not replace host or network-level security controls.

---

## Database Security

The PostgreSQL database server is located in a dedicated database security segment.
Database access should be restricted to explicitly authorized application or administrative sources.
The database should not be directly accessible from:

* Untrusted networks
* General user networks
* The public Internet

Security controls include:

* Network-level access restrictions
* PostgreSQL authentication
* Role-based database permissions
* Least-privilege service accounts
* Protected database credentials
* Logging and auditing
* Backup protection

Application services should use dedicated database accounts rather than unrestricted administrative accounts.

---

## Host Security

Each infrastructure host should follow a hardened operating system baseline appropriate to its role.

Recommended controls include:

* Minimal package installation
* Regular security updates
* Firewall configuration
* Secure SSH configuration
* Strong authentication
* Restricted administrative access
* Removal or disabling of unnecessary services
* Centralized logging where practical
* Time synchronization

Operating system security remains important even when applications are containerized.

---

## Infrastructure Automation Security

Ansible and OpenTofu are used to automate infrastructure deployment and configuration.
Automation introduces privileged access and must therefore be treated as a security-sensitive component.

Automation credentials should:

* Use dedicated service identities
* Follow least privilege
* Avoid embedded passwords
* Retrieve secrets securely
* Be rotated periodically
* Be protected from unauthorized modification

Automation repositories must never contain production-like credentials or private keys.
Infrastructure changes should preferably be version-controlled and reviewable.

---

## Certificate and TLS Security

Encrypted communication should be preferred whenever supported.

TLS should be used for:

* Web applications
* Administrative interfaces
* APIs
* Authentication services
* Other services carrying sensitive information

Certificates and private keys should be managed securely.
Private keys must never be committed to version control.
Internal services may use an internal certificate authority where appropriate.

---

## Logging and Auditing

Security-relevant activity should be logged whenever practical.

Important events include:

* Authentication attempts
* Failed authentication
* Privilege escalation
* Administrative access
* Firewall policy events
* Configuration changes
* Secrets access
* Infrastructure changes
* Application security events

Logs should provide enough information to support troubleshooting and security investigation without unnecessarily exposing sensitive information.
Logs themselves should be treated as sensitive infrastructure data.

---

## Backup and Recovery Security

Backups are considered part of the security architecture.

Backup protection should include:

* Access control
* Encryption where appropriate
* Restricted administrative access
* Integrity verification
* Regular recovery testing

A backup that cannot be restored reliably should not be considered a successful backup.
Critical configuration and infrastructure definitions should be reproducible through version-controlled automation wherever practical.

---

## Security Monitoring

The architecture is designed to support future integration of additional monitoring and security tooling.

Potential capabilities include:

* Centralized log management
* Intrusion detection
* Vulnerability scanning
* Configuration compliance
* Security event correlation
* Endpoint monitoring
* Container image scanning

Security monitoring should evolve alongside the infrastructure rather than being treated as a separate system.

---

## Security Lifecycle

Security is treated as a continuous process rather than a one-time configuration task.

The environment should periodically review:

1. Identity and access permissions
2. Firewall rules
3. Exposed services
4. Operating system updates
5. Container images
6. Application dependencies
7. Secrets and credentials
8. Certificates
9. Backup integrity
10. Administrative accounts

Changes should be documented and, where practical, implemented through automation.

---

## Security Objectives

The architecture aims to demonstrate the following security capabilities:

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

The goal is not to claim that the lab represents a fully production-hardened enterprise environment.

Instead, it provides a practical reference architecture for understanding and demonstrating how modern enterprise security principles can be implemented using primarily open-source technologies.
