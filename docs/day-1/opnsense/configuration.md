# OPNsense — Configuration Baseline

> **Day 1 — Build & Configure**

This document defines the baseline configuration for `fw01`, the OPNsense firewall in the Enterprise Reference Architecture.

## Status

**Reference procedure.** OPNsense is implemented in the laboratory. VLAN segmentation, inter-VLAN policy, and the complete target security architecture remain **Planned** until configured and validated in the lab.

## 1. Configuration Goals

The firewall configuration should provide:

- Controlled WAN/LAN routing
- Secure management access
- DNS and NTP foundations
- Explicit firewall policy
- Controlled NAT
- Future VLAN segmentation
- Logging suitable for troubleshooting
- A predictable configuration that can be backed up and restored

Security principle:

> Default deny where practical; explicitly allow required traffic.

## 2. Interface Model

Reference topology:

```text
                    Upstream
                       |
                      WAN
                       |
                  +---------+
                  | OPNsense|
                  |  fw01   |
                  +---------+
                       |
                      LAN
                       |
                    vmbr0
                       |
             Management / Lab clients
```

Future segmented topology:

```text
                     OPNsense
                         |
          +--------------+--------------+
          |              |              |
       VLAN 10        VLAN 20        VLAN 30/40
      Management      Identity       DB / App
```

## 3. Interface Assignment

Do not rely on interface names alone. Confirm the actual MAC address and Proxmox NIC mapping.

Record:

| Role | OPNsense interface | Proxmox NIC | Network |
|---|---|---|---|
| WAN | `<actual>` | `<NIC>` | Upstream |
| LAN | `<actual>` | `<NIC>` | Internal |
| VLAN trunk | Planned | Planned | Future |

A wrong interface assignment can create both connectivity and security problems, so this should be documented before firewall rules are created.

## 4. LAN Management

The LAN side is the trusted administration path for the initial lab.

Reference example:

```text
LAN:     10.10.10.1/24
Network: 10.10.10.0/24
```

These are reference architecture values. Use the actual laboratory address when implementing.

The management computer should be able to reach the OPNsense LAN address.

## 5. WAN Configuration

Configure WAN according to the actual upstream network:

- DHCP
- Static address
- PPPoE
- Other supported upstream method

Document:

```text
WAN mode:
Address:
Prefix:
Gateway:
DNS:
MTU (if non-default):
```

Do not publish real public addresses in project documentation unless they are intentionally part of the public design.

## 6. DNS

Define DNS intentionally rather than accepting an undocumented default.

The firewall may provide DNS forwarding/resolution for the lab depending on the final architecture.

Future target:

```text
Clients
   ↓
OPNsense / DNS service
   ↓
Internal DNS
   ↓
External resolution where required
```

When FreeIPA is introduced, DNS responsibilities must be explicitly defined so that the identity environment does not have competing authoritative configurations.

## 7. NTP / Time

Configure reliable time synchronization on OPNsense.

Validate:

- Correct timezone
- Reachable time source
- Synchronization active
- Correct system time

Time synchronization is particularly important before introducing identity, certificates, and distributed services.

Do not hard-code a private NTP server address into public documentation.

## 8. DHCP

DHCP should be enabled only on networks where OPNsense is intended to provide DHCP.

Document:

```text
Network:
Range:
Gateway:
DNS:
Lease duration:
Static mappings:
```

For infrastructure systems such as firewalls, identity servers, databases, and management hosts, prefer stable addressing and document reservations/static configuration.

The final DHCP responsibility for each VLAN should be decided before the VLAN is implemented.

## 9. Firewall Policy

Firewall rules should describe **business/technical intent**, not merely ports.

Each rule should document:

| Field | Description |
|---|---|
| Source | Network / host |
| Destination | Network / host |
| Protocol | TCP / UDP / ICMP / etc. |
| Port | Required service |
| Direction | Inbound / outbound |
| Action | Pass / Block |
| Logging | Required or not |
| Reason | Why the flow exists |

Example target policy:

```text
Management → Infrastructure management     ALLOW
Management → Required services              ALLOW
Application → Database required ports       ALLOW
Database → Internet                         DENY
Untrusted → Management                      DENY
Untrusted → Internal networks                DENY
```

These are target policy examples, not claims about current lab rules.

## 10. WAN Management Protection

Administrative access should not be exposed directly to WAN.

Verify that management services such as the web interface and SSH are not unnecessarily reachable from the external interface.

Use the LAN/management network for administration.

Where remote administration is eventually required, introduce an explicit secure access mechanism rather than opening management ports broadly.

## 11. NAT

Document NAT behavior separately from firewall policy.

Typical lab requirement:

```text
Internal networks → WAN → outbound NAT
```

Review whether automatic outbound NAT is appropriate before changing to a manual mode.

Port forwards should be created only when there is a defined service requirement.

Every port forward should have:

- Explicit destination
- Explicit source restriction where possible
- Required protocol/port
- Documented business/technical reason
- Logging where appropriate
- Review/expiry expectation

Avoid exposing infrastructure management services through NAT.

## 12. VLAN Architecture — Planned

The target architecture defines:

| VLAN | Purpose | Network |
|---:|---|---|
| 10 | Management | 10.10.10.0/24 |
| 20 | Identity | 10.10.20.0/24 |
| 30 | Database | 10.10.30.0/24 |
| 40 | Application | 10.10.40.0/24 |

Implementation requires coordination between:

```text
Physical switch
      ↓
Proxmox bridge
      ↓
OPNsense VLAN interface
      ↓
Firewall policy
      ↓
VM network assignment
```

Do not mark the VLAN architecture implemented until traffic has been tested end-to-end.

## 13. Inter-VLAN Security Model — Planned

The target model is default-deny between security zones.

Example:

```text
Management ───────→ Infrastructure services
Identity ──────────→ Required authentication/DNS flows
Application ───────→ Database service only
Database ──────────→ No unrestricted outbound access
Application ───────→ No unrestricted lateral access
```

The actual service ports should be defined from the requirements of the implemented applications rather than opened in advance.

## 14. Network Address Translation and Routing Validation Preparation

Before introducing multiple VLANs, define:

- Gateway per network
- DHCP ownership
- DNS ownership
- Inter-VLAN routes
- NAT behavior
- Firewall policy
- Management path

This avoids the common situation where routing works but security policy is undefined.

## 15. Logging

Enable logging for security-relevant and operationally useful events.

At minimum review:

- Firewall blocks
- Firewall passes where useful for troubleshooting
- Authentication events
- System events
- Gateway events
- Configuration changes
- DNS/DHCP events where applicable

Logging volume should be considered. Excessive logging can make troubleshooting harder and consume unnecessary storage.

## 16. Gateway Monitoring

Monitor upstream gateways where the environment depends on Internet or external connectivity.

Record:

```text
Gateway:
Monitoring method:
Probe:
Failure threshold:
Expected recovery behavior:
```

The goal is to distinguish:

```text
Firewall failure
     vs
Upstream gateway failure
     vs
DNS failure
     vs
Remote service failure
```

## 17. Configuration Backup

The OPNsense configuration should be backed up before significant changes.

Backup scope should include the configuration necessary to rebuild the firewall, while secrets and private configuration exports must be protected appropriately.

Recommended operational sequence:

```text
Backup current configuration
        ↓
Make change
        ↓
Validate
        ↓
Keep evidence
        ↓
Update documentation
```

A configuration backup is not the same as a complete disaster-recovery solution. Restore testing remains a Day 2 requirement.

## 18. Safe Change Procedure

For network/security changes:

1. Record current state.
2. Define expected behavior.
3. Create/verify configuration backup.
4. Make one logical change at a time.
5. Apply configuration.
6. Test management access.
7. Test affected traffic.
8. Test an expected denied flow where relevant.
9. Review logs.
10. Document the result.

Never make multiple unrelated firewall/network changes simultaneously when troubleshooting.

## 19. Third-Computer Management Test

A dedicated test from a separate computer is required to prove that the firewall is not merely accessible from the configuration session itself.

Test:

```text
Management PC
     |
     | HTTPS
     v
OPNsense LAN address
```

Validate:

- Web UI loads.
- Authentication works.
- Expected certificate behavior is understood.
- The client is on the intended management network.
- WAN-side access is not unintentionally available.

If the test fails, document the failure before changing multiple settings.

## 20. Security Baseline

At minimum:

- Change default administrative credentials.
- Use HTTPS for management.
- Restrict management to trusted networks.
- Keep OPNsense updated according to a defined maintenance process.
- Avoid unnecessary services.
- Avoid broad WAN exposure.
- Review firewall rules periodically.
- Back up configuration before major changes.
- Protect configuration backups.
- Do not store secrets in Git.

## 21. Configuration Evidence

Record:

```text
OPNsense version:
Hostname:
WAN interface:
LAN interface:
LAN address:
WAN mode:
DNS configuration:
NTP configuration:
DHCP networks:
Firewall policy version/date:
NAT mode:
VLAN status:
Last configuration backup:
Known deviations:
```

Use example values in public documentation when the real values would disclose private infrastructure details.

## 22. Configuration Completion Criteria

The baseline is complete when:

1. WAN and LAN roles are unambiguous.
2. Management access works from the intended LAN/management computer.
3. DNS is intentionally configured.
4. NTP is synchronized.
5. DHCP is intentionally configured or explicitly disabled where not required.
6. Firewall policy is documented.
7. WAN management exposure has been reviewed.
8. NAT behavior is understood.
9. Logging is available for troubleshooting.
10. Configuration backup is possible.
11. Major configuration changes follow a repeatable procedure.
12. VLAN and inter-VLAN features are explicitly marked Planned until validated.

## Related Documentation

- [`installation.md`](installation.md) — OPNsense installation
- [`validation.md`](validation.md) — OPNsense validation
- [`../../network/network.md`](../../network/network.md) — Network architecture
- [`../../security/security.md`](../../security/security.md) — Security architecture
- [`../../vm-design/vm-design.md`](../../vm-design/vm-design.md) — VM standards
- [`../../day-2/README.md`](../../day-2/README.md) — Day 2 operations
