# Network Architecture

> Network architecture and segmentation model for the Enterprise Reference Architecture.

## Purpose

This document describes the network architecture, segmentation model, addressing scheme, and traffic flow principles used by the Enterprise Reference Architecture.
The design follows a **segmented, security-first approach** where infrastructure roles are separated into dedicated network segments and communication between segments is explicitly controlled.
The network is designed to demonstrate enterprise networking principles while remaining practical for a small-scale lab environment.

---

## Design Principles

The network architecture follows these principles:

* **Network segmentation** — Infrastructure roles are separated into dedicated VLANs.
* **Least privilege** — Network communication is allowed only when required.
* **Default deny** — Inter-VLAN traffic is denied unless explicitly permitted.
* **Centralized routing and firewalling** — Inter-VLAN routing and security policies are handled by OPNsense.
* **Administrative isolation** — Management access is separated from normal application traffic.
* **Database isolation** — Database services are placed in a dedicated network segment.
* **Service separation** — Application workloads are separated from identity, database, and management infrastructure.
* **FOSS-first** — The network design relies primarily on open-source technologies.

---

## Network Topology

The environment uses OPNsense as the primary firewall and Layer 3 gateway.

```text
                         Internet
                            |
                         [ OPNsense ]
                            |
                     +------+------+
                     |             |
                 VLAN 10        VLAN 20
                 Management     Identity
                     |             |
                  infra01       ipa01
                                   
                     +------+------+
                            |
                +-----------+-----------+
                |                       |
             VLAN 30                 VLAN 40
          Application              Database
                |                       |
              app01                   db01
                |
        Docker application networks
```

The physical and virtual infrastructure is hosted on Proxmox.

OPNsense provides:

* Firewalling
* Inter-VLAN routing
* DHCP where required
* DNS forwarding/resolution where appropriate
* VPN connectivity where required
* Network security policy enforcement

---

## VLAN and IP Addressing

The following addressing scheme is used as the reference network model.

| VLAN | Name        | Network         | Primary Purpose                          |
| ---: | ----------- | --------------- | ---------------------------------------- |
|   10 | Management  | `10.10.10.0/24` | Infrastructure and administrative access |
|   20 | Identity    | `10.10.20.0/24` | FreeIPA and identity-related services    |
|   30 | Application | `10.10.30.0/24` | Application and service workloads        |
|   40 | Database    | `10.10.40.0/24` | PostgreSQL and database services         |

> VLAN numbers and addresses are part of the reference design and may be adapted when deploying the architecture in another environment.

### Gateway Convention

Each VLAN uses the `.1` address as its default gateway:

| VLAN | Gateway      |
| ---: | ------------ |
|   10 | `10.10.10.1` |
|   20 | `10.10.20.1` |
|   30 | `10.10.30.1` |
|   40 | `10.10.40.1` |

---

## Network Segments

### VLAN 10 — Management

The Management network is used for administrative access to infrastructure components.

Typical systems include:

* Proxmox management
* OPNsense management
* Administrative interfaces
* Infrastructure administration tools
* Ansible/OpenTofu management

Management traffic should not be exposed to ordinary application networks.

---

### VLAN 20 — Identity

The Identity network contains centralized identity and authentication services.

Primary workload:

* `ipa01` — FreeIPA

FreeIPA provides services such as:

* Identity management
* Authentication
* Authorization
* DNS integration
* Kerberos
* LDAP

Only systems that require identity services should be permitted to communicate with this segment.

---

### VLAN 30 — Application

The Application network hosts application and platform services.

Primary workload:

* `app01` — Ubuntu Server
* Docker-based application stack

Services may include:

* Nginx
* Portainer
* Teleport Community Edition
* Keycloak
* OpenBao
* NetBox
* Squid Gateway
* Forgejo
* Woodpecker CI
* Wiki.js
* Project Pulp

Although these services share the application host, Docker networks are used to provide additional logical isolation between workloads.

---

### VLAN 40 — Database

The Database network is dedicated to database services.

Primary workload:

* `db01` — Pardus
* PostgreSQL

The database network is treated as a **separate security and network segmentation zone**, not as an application VLAN.
Application services access PostgreSQL through explicitly permitted firewall rules.
Direct access from general user or management networks should not be permitted unless there is a defined administrative requirement.

---

## Inter-VLAN Traffic

Traffic between VLANs is controlled by OPNsense.

The default policy is:

```text
VLAN → VLAN = DENY
```

Required communication is then explicitly allowed.
A simplified communication model is:

```text
Management
    |
    +----> Infrastructure Management

Application
    |
    +----> Identity
    |
    +----> Database

Identity
    |
    +----> Required Infrastructure Services

Database
    |
    +----> Required Application Services
```

The exact firewall rules should be based on **service requirements rather than broad network trust**.

For example:

```text
VLAN 30 → VLAN 40
TCP 5432
ALLOW
```

allows PostgreSQL access from the Application segment while avoiding unrestricted access between the two networks.

---

## Firewall Policy Model

OPNsense acts as the enforcement point for north-south and east-west traffic.

The policy model follows:

1. Deny by default.
2. Identify the required source and destination.
3. Identify the required protocol and port.
4. Allow only the required traffic.
5. Log security-relevant traffic.
6. Review and refine rules as the environment evolves.

Example:

| Source  | Destination | Service                    | Action     |
| ------- | ----------- | -------------------------- | ---------- |
| VLAN 30 | VLAN 40     | PostgreSQL `5432/TCP`      | Allow      |
| VLAN 30 | VLAN 20     | Required Identity Services | Allow      |
| VLAN 10 | VLAN 30     | Administration             | Allow      |
| VLAN 10 | VLAN 40     | Administration             | Restricted |
| VLAN 40 | VLAN 30     | Unsolicited Traffic        | Deny       |
| VLAN 30 | VLAN 40     | All Other Traffic          | Deny       |

The final rule set should be maintained according to the actual services deployed.

---

## Docker Network Segmentation

VLAN segmentation provides isolation at the network infrastructure level.
Docker networks provide an additional layer of logical segmentation inside `app01`.

```text
                    app01
                      |
              +-------+-------+
              | Docker Host   |
              +-------+-------+
                      |
        +-------------+-------------+
        |             |             |
     Network A     Network B     Network C
        |             |             |
     Web Apps      Identity      Internal
```

Containers should communicate through dedicated Docker networks where practical.
Applications should not automatically have unrestricted access to every other container.

This provides defense in depth:

```text
Physical / Virtual Network
            ↓
          VLAN
            ↓
       Firewall Policy
            ↓
       Docker Network
            ↓
       Application
```

---

## DNS Architecture

DNS is an important part of the architecture because several infrastructure services depend on reliable name resolution.
FreeIPA provides the identity-related DNS infrastructure, while OPNsense provides network-level DNS forwarding and resolution capabilities where appropriate.

Public documentation uses the placeholder domain:

```text
example.com
```

Actual internal domains should be selected according to the deployment environment.

---

## Address Assignment

Infrastructure servers use static IP addressing or controlled reservations.

Example:

| Host     | Role               | VLAN | Example IP    |
| -------- | ------------------ | ---: | ------------- |
| `fw01`   | OPNsense           |   10 | `10.10.10.1`  |
| `ipa01`  | FreeIPA            |   20 | `10.10.20.10` |
| `app01`  | Application Server |   30 | `10.10.30.10` |
| `db01`   | PostgreSQL         |   40 | `10.10.40.10` |
| `auto01` | Automation         |   10 | `10.10.10.20` |

The exact addresses may change during implementation.

---

## Security Considerations

The network architecture is designed around several security assumptions:

* No VLAN should automatically trust another VLAN.
* Database services should not be directly exposed to users.
* Administrative interfaces should remain isolated.
* Application services should use explicit database connections.
* Firewall rules should be service-specific.
* Credentials and secrets should not be stored in plaintext.
* Network segmentation should complement, rather than replace, application-level security.
* Logs should be collected for important security events.
* Management access should preferably use secure administrative channels such as SSH, HTTPS, or Teleport.

Network segmentation is therefore considered one layer of a broader defense-in-depth strategy.

---

## Future Expansion

The network model can be expanded without changing its fundamental architecture.

Potential future segments include:

* DMZ
* Monitoring
* Backup
* CI/CD
* User/Client
* Security tooling
* Dedicated storage
* VPN clients

Additional VLANs should only be introduced when they provide a meaningful security, operational, or architectural benefit.

---

## Summary

The network architecture provides a foundation for the rest of the Enterprise Reference Architecture.

Its primary goals are:

* Clear separation of infrastructure roles
* Controlled east-west communication
* Centralized firewall enforcement
* Database isolation
* Administrative isolation
* Defense in depth
* Practical enterprise-style segmentation on modest hardware

The architecture intentionally favors **simple, explicit, and auditable network policies** over unnecessary complexity.
