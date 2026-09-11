# Day 1 Documentation Standard

> Standard structure for documenting how an infrastructure component is built, configured, secured, integrated, and validated.

Every Day 1 technology should follow the same lifecycle so that the repository documents **how the platform is established**, not merely how software is installed.

## Standard Lifecycle

```text
Plan
 ↓
Prerequisites
 ↓
Install
 ↓
Configure
 ↓
Secure
 ↓
Integrate
 ↓
Validate
 ↓
Document Evidence
```

## Required Sections

### 1. Purpose

What the component provides and why it exists in the reference architecture.

### 2. Scope

What is and is not covered by the procedure.

### 3. Prerequisites

Hardware, VM resources, network connectivity, DNS, NTP, storage, dependencies, and required access.

### 4. Installation

Exact installation procedure appropriate for the lab.

### 5. Base Configuration

Hostname, addressing, storage, repositories, service configuration, and other baseline settings.

### 6. Security Baseline

Least privilege, administrative access, exposed services, TLS, firewall requirements, secrets handling, and hardening.

### 7. Integration

Dependencies and communication with other components in the architecture.

### 8. Validation

Concrete tests that prove the component is working as intended.

```text
[ ] Service is running
[ ] DNS works
[ ] NTP is synchronized
[ ] Network flows are correct
[ ] Authentication works
[ ] Required ports are reachable
[ ] Logs are generated
[ ] Security controls are effective
```

### 9. Implementation Status

Use the repository status convention. Do not claim **Implemented** until the procedure has actually been executed and validated in the lab.

### 10. Evidence

Where practical, record command output, screenshots, configuration references, test results, or links to relevant lab evidence.

## Component-Specific Extensions

The common structure may be extended when required. Examples:

- Proxmox: cluster, storage, VM lifecycle, node maintenance
- OPNsense: interfaces, VLANs, NAT, firewall policy, DNS/DHCP
- FreeIPA: realm, replication, HBAC, SUDO, certificates
- PostgreSQL: roles, authentication, backup, recovery
- Docker: images, networks, volumes, Compose, reverse proxy

## Rule

> **Installation alone is never sufficient evidence of an Implemented component.**
