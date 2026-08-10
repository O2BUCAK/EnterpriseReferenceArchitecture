VM Resource Matrix
Enterprise Reference Architecture — FOSS Home Lab
Documentation Notice
All domain names, IP addresses, hostnames, infrastructure identifiers and resource allocations shown in this document are documentation-only examples. They do not represent the actual production or laboratory environment.

1. Physical Host
The reference architecture is designed to run on a Dell Latitude 5540 using Proxmox VE as the hypervisor.
Resource
Specification
Physical Host
Dell Latitude 5540
CPU
13th Gen Intel Core i7-1355U
Physical Cores
10
Logical Threads
12
RAM
32 GB DDR4-3200
Storage
512 GB PCIe NVMe Gen4 x4
Hypervisor
Proxmox VE
Architecture
x86-64 / AMD64

Resource allocation principle
The physical host has limited resources compared with a production enterprise environment. Therefore:
Official minimum requirements are documented separately.
Official recommended requirements are documented separately.
Lab Allocation represents the actual resource target for this reference implementation.
Not all physical resources are assigned to virtual machines.
RAM and storage headroom are intentionally preserved for the Proxmox host and future expansion.
CPU overcommit is permitted at a controlled level because this is a laboratory simulation rather than a production workload.

2. Public Network and DNS Convention
All public documentation uses the reserved example domain:
corp.example.com

Example hostnames:
pve.corp.example.com
fw01.corp.example.com
ipa01.corp.example.com
db01.corp.example.com
docker01.corp.example.com
rhel01.corp.example.com

Example network:
10.10.0.0/16

Initial VLAN allocation:
VLAN
Network
Purpose
10
10.10.10.0/24
Management
20
10.10.20.0/24
Identity / Core
30
10.10.30.0/24
Database
40
10.10.40.0/24
Application

Gateway convention:
10.10.<VLAN>.1


3. VM Summary
VM ID
Hostname
Role
OS
VLAN
Example IP
vCPU
RAM
OS Disk
Data Disk
100
fw01
Firewall / Gateway
OPNsense
—
10.10.x.1
2
2 GB
16 GB
—
101
ipa01
Identity / DNS / Kerberos
Fedora Server
20
10.10.20.10
2
2 GB
16 GB
16 GB
102
db01
Central PostgreSQL
Pardus Server
30
10.10.30.10
4
8 GB
32 GB
96 GB
103
docker01
Container Platform
Ubuntu Server
40
10.10.40.10
4
10 GB
32 GB
128 GB
104
rhel01
Ansible / OpenTofu
RHEL
10
10.10.10.10
2
4 GB
20 GB
20 GB

Initial VM resource allocation
CPU
12 physical/logical host threads
        │
        ├── fw01       2 vCPU
        ├── ipa01      2 vCPU
        ├── db01       4 vCPU
        ├── docker01   4 vCPU
        └── rhel01     2 vCPU
                       ────────
                       14 vCPU

This represents a controlled CPU overcommit ratio of approximately 1.17:1.
The architecture intentionally avoids excessive CPU overcommit because PostgreSQL, Keycloak and the Docker application platform may produce concurrent workloads.

4. RAM Budget
Component
RAM
Physical RAM
32 GB
fw01
2 GB
ipa01
2 GB
db01
8 GB
docker01
10 GB
rhel01
4 GB
VM Allocation
26 GB
Reserved for Proxmox / Headroom
6 GB

RAM allocation principle
The 6 GB unallocated memory is intentional.
It provides:
Proxmox VE operating overhead
filesystem cache
temporary workload spikes
VM management overhead
future experimentation
protection against immediate memory exhaustion
The VM allocation therefore does not consume the entire 32 GB physical memory capacity.

5. Storage Budget
The physical host contains a single 512 GB NVMe device.
The reference architecture uses two virtual disks for Linux VMs:
Disk 1
└── Operating System

Disk 2
└── System / Application Data
    ├── /var
    ├── /home
    └── /tmp

Recommended Linux layout:
Disk 1
└── /
    
Disk 2
└── LVM
    ├── /var
    ├── /home
    └── /tmp

The exact filesystem and LVM allocation will be defined during the OS installation phase.

Storage Allocation
VM
OS Disk
Data Disk
Total
fw01
16 GB
—
16 GB
ipa01
16 GB
16 GB
32 GB
db01
32 GB
96 GB
128 GB
docker01
32 GB
128 GB
160 GB
rhel01
20 GB
20 GB
40 GB
VM Total
116 GB
260 GB
376 GB

This leaves approximately:
512 GB
- 376 GB VM allocation
= 136 GB

before accounting for Proxmox filesystem/storage overhead and other host-level requirements.
The remaining capacity is deliberately retained rather than immediately consumed.

6. VM 100 — fw01
Role
OPNsense Firewall / Router / VLAN Gateway
fw01.corp.example.com

Resource allocation
Resource
Value
vCPU
2
RAM
2 GB
OS Disk
16 GB
Data Disk
Not required
Network
WAN + VLAN interfaces

Official requirements
OPNsense documents:
Level
CPU
RAM
Storage
Minimum
1 GHz dual-core
3 GB
4 GB
Reasonable
1 GHz dual-core
4 GB
40 GB SSD
Recommended
1.5 GHz multi-core
8 GB
120 GB SSD

OPNsense also notes that Squid and other disk-writing features can materially affect resource requirements.
Lab decision
Important: The initial allocation of 2 GB RAM is intentionally below the current official minimum and therefore should not be considered a compliant final allocation.
Because this architecture includes Squid Gateway functionality, the final lab target should be:
fw01
2 vCPU
4 GB RAM
40 GB disk

This corresponds to the official "reasonable" specification and is much more appropriate for the planned feature set.
Therefore, 4 GB RAM / 40 GB storage should be the final matrix value.

7. VM 101 — ipa01
Role
Central Identity and DNS
Services:
FreeIPA
├── LDAP
├── Kerberos
├── DNS
├── Certificate Authority
└── Identity Management

FQDN:
ipa01.corp.example.com

Example realm:
CORP.EXAMPLE.COM

Example IP:
10.10.20.10

Resource allocation
Resource
Value
vCPU
2
RAM
2 GB
OS Disk
16 GB
Data Disk
16 GB
VLAN
20

FreeIPA's official Quick Start documentation states that a minimum of 1.2 GB RAM is required to install with a CA and recommends 2 GB for a demo/test system. It also emphasizes static hostname/DNS prerequisites.
Lab decision
2 vCPU
2 GB RAM
32 GB total storage

is appropriate for the initial single-node laboratory deployment.
FreeIPA's required service ports will be documented separately in the Port Matrix. The project documentation identifies HTTP/HTTPS, LDAP/LDAPS, Kerberos and NTP among the required services.

8. VM 102 — db01
Role
Central PostgreSQL Database Platform
FQDN:
db01.corp.example.com

Example IP:
10.10.30.10

Resource allocation
Resource
Value
vCPU
4
RAM
8 GB
OS Disk
32 GB
Data Disk
96 GB
VLAN
30

Database architecture
                   db01
                     │
          ┌──────────┼──────────┐
          │          │          │
      Keycloak     NetBox    Forgejo
          │          │          │
          └──────────┼──────────┘
                     │
               PostgreSQL

Applications will receive separate databases and database roles.
Example:
netbox_db
netbox_dba

keycloak_db
keycloak_dba

forgejo_db
forgejo_dba

PostgreSQL does not publish a single universal "minimum RAM" value comparable to OPNsense or FreeIPA. Its documentation instead provides workload-oriented configuration guidance. For a dedicated PostgreSQL server with at least 1 GB RAM, PostgreSQL documents 25% of system memory as a reasonable starting point for shared_buffers, while noting that the workload determines the appropriate value.
Lab decision
4 vCPU
8 GB RAM
32 GB OS
96 GB PostgreSQL data

The relatively larger allocation is intentional because db01 is a shared database platform, rather than a single-application database.

9. VM 103 — docker01
Role
Central Application / Container Platform
FQDN:
docker01.corp.example.com

Example IP:
10.10.40.10

Resource allocation
Resource
Value
vCPU
4
RAM
10 GB
OS Disk
32 GB
Data Disk
128 GB
VLAN
40

Planned services
docker01
│
├── Nginx
├── Portainer
├── Teleport CE
├── Keycloak
├── OpenBao
├── NetBox
├── Squid
├── Forgejo
├── Woodpecker CI
├── Wiki.js
└── Project Pulp

Docker Engine's official Linux installation documentation does not specify a universal minimum RAM value for Docker Engine itself. It specifies supported architectures/platforms and Linux prerequisites instead. Docker's separate Docker Desktop documentation does specify 4 GB RAM, but that requirement applies to Docker Desktop rather than Docker Engine on a Linux server.
Therefore, Docker Desktop requirements must not be incorrectly used to size docker01.
Lab decision
4 vCPU
10 GB RAM
32 GB OS
128 GB application/container data

The 10 GB allocation is based on the combined application workload, not on a Docker Engine minimum.
The data disk is primarily intended for:
/var
├── /var/lib/docker
├── container volumes
├── application data
└── logs

Application-specific volume placement will be defined in the Docker Storage Matrix.
Docker's own security guidance recommends enabling AppArmor or SELinux where supported.

10. VM 104 — rhel01
Role
Infrastructure Automation
rhel01.corp.example.com

Services:
Ansible
OpenTofu

Example IP:
10.10.10.10

Resource allocation
Resource
Value
vCPU
2
RAM
4 GB
OS Disk
20 GB
Data Disk
20 GB
VLAN
10

Red Hat's RHEL 10 installation documentation specifies minimum RAM values for installation, with x86_64 local-media installation requiring 1.5 GiB, and at least 10 GiB available disk space.
These are OS installation requirements, not requirements for running a useful Ansible/OpenTofu automation controller.
Lab decision
2 vCPU
4 GB RAM
40 GB total storage

is selected to provide sufficient room for:
RHEL
Ansible
OpenTofu
Git repositories
Python environments
automation artifacts
temporary provisioning data

11. Final Resource Matrix
VM
Hostname
Role
vCPU
RAM
OS Disk
Data Disk
Total Disk
VLAN
fw01
fw01.corp.example.com
Firewall
2
4 GB
40 GB
—
40 GB
—
ipa01
ipa01.corp.example.com
Identity / DNS
2
2 GB
16 GB
16 GB
32 GB
20
db01
db01.corp.example.com
PostgreSQL
4
8 GB
32 GB
96 GB
128 GB
30
docker01
docker01.corp.example.com
Docker Platform
4
10 GB
32 GB
128 GB
160 GB
40
rhel01
rhel01.corp.example.com
Automation
2
4 GB
20 GB
20 GB
40 GB
10
TOTAL




14
28 GB
140 GB
260 GB
400 GB



Physical host comparison
Resource
Physical Capacity
VM Allocation
Remaining
CPU Threads
12
14 vCPU
Controlled overcommit
RAM
32 GB
28 GB
4 GB
NVMe
512 GB
400 GB
~112 GB


12. Resource Allocation Decision
The final initial allocation is therefore:
                        Dell Latitude 5540
                     12 Threads / 32 GB RAM
                              │
              ┌───────────────┴────────────────┐
              │                                │
          Proxmox VE                       VM Layer
              │                                │
              │       ┌────────────────────────┼───────────────┐
              │       │                        │               │
              │     fw01                     ipa01           db01
              │     2C/4G                    2C/2G           4C/8G
              │
              │                                │
              │                         ┌──────┴──────┐
              │                         │             │
              │                     docker01       rhel01
              │                     4C/10G          2C/4G
              │
              └──────────────────────────────────────────────

The architecture deliberately prioritizes:
PostgreSQL availability — central database platform.
Docker host capacity — multiple enterprise applications share the VM.
Proxmox headroom — the host must not be memory-starved.
Security services — FreeIPA receives dedicated resources.
Firewall stability — OPNsense receives the official reasonable specification because Squid is planned.

13. Important Exception — OPNsense Disk Architecture
The two-disk Linux VM standard does not apply literally to OPNsense.
OPNsense is a FreeBSD-based network appliance rather than a conventional Linux server. Its official documentation provides its own storage and RAM guidance, and its filesystem architecture should not be artificially forced into:
/
/var
/home
/tmp

Therefore:
Linux VMs
    ├── Disk 1 → /
    └── Disk 2 → /var /home /tmp

OPNsense
    └── Appliance-specific storage layout

This is an intentional architecture exception.

14. Resource Sizing Philosophy
This matrix does not claim that these allocations are production-ready.
The project has three distinct sizing concepts:
Official Minimum
       ↓
Official Recommended
       ↓
Reference Lab Allocation

The lab allocation is determined by:
official requirements
workload
number of applications
physical host capacity
security architecture
expected concurrency
future expansion
resource isolation
This distinction prevents the common mistake of treating a software vendor's minimum installation requirement as a suitable production or multi-service workload size.

15. Future Expansion
The second stage of the project introduces a separate Windows PC hosting Docker Desktop and additional security, monitoring and IT management workloads.
Stage 2 services include:
Nuclei
Grype
OWASP ZAP
Wazuh
Nextcloud
Zabbix
Prometheus
Grafana
GLPI
Grafana Loki
StackStorm

These services are not included in the current Dell VM Resource Matrix.
Where an application officially supports PostgreSQL, its database workload will be evaluated for use with:
db01.corp.example.com

Applications requiring a specialized datastore will retain their officially supported storage architecture rather than being forced into PostgreSQL.

Official References
OPNsense hardware sizing and requirements: OPNsense Hardware Sizing & Setup
FreeIPA Quick Start and RAM requirements: FreeIPA Quick Start Guide
FreeIPA installation and required services: FreeIPA Install and Deploy
PostgreSQL resource consumption: PostgreSQL Resource Consumption
Docker Engine installation: Docker Engine Documentation
RHEL 10 system requirements: Red Hat Enterprise Linux 10 System Requirements
Pardus releases and system requirements: Pardus Releases

