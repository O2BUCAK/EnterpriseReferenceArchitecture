# Build Prerequisites

## Purpose
Common preparation for rebuilding the Enterprise Reference Architecture from bare metal.

## Read First
- Architecture overview
- Network architecture
- VM design and resource matrix
- Security architecture
- Port map
- Existing Day-1 and Day-2 documentation

## Required Inputs
Before installation, record the approved values for:
- Proxmox hostname/FQDN
- management IP/prefix/gateway
- internal domain
- DNS authority
- NTP source
- VLAN IDs
- VM IDs
- storage locations
- repository commit being reproduced

Do not invent missing values.

## Reference Network
| VLAN | Purpose | Network | Gateway |
|---:|---|---|---|
| 10 | Management | 10.10.10.0/24 | 10.10.10.1 |
| 20 | Identity | 10.10.20.0/24 | 10.10.20.1 |
| 30 | Database | 10.10.30.0/24 | 10.10.30.1 |
| 40 | Application | 10.10.40.0/24 | 10.10.40.1 |

These are repository reference values; the network document marks them Planned until implemented and validated.

## Build Order
00 prerequisites → 01 Proxmox → 02 OPNsense → 03 Fedora → 04 FreeIPA → 05 Pardus/PostgreSQL/Redis → 06 Ubuntu/Docker → 07 application platform → 08 identity integration → 09 DNS → 10 automation → 11 applications → 12 security baseline → 13 validation.

## Rules
- Verify ISO checksums.
- Never commit passwords, tokens, private keys or unredacted sensitive exports.
- Validate each layer before building the next.
- Record deviations instead of silently changing architecture documentation.
