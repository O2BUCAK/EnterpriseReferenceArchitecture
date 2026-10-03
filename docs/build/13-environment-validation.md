# Environment Validation — End-to-End Acceptance Runbook

## Purpose
Prove that the Enterprise Reference Architecture has been built as documented.

## Rule
A component is **Implemented** only after configuration and validation evidence exist.

## Layer 1 — Proxmox
[ ] host boots
[ ] management network works
[ ] DNS works
[ ] NTP synchronized
[ ] storage healthy
[ ] VM creation standard verified

## Layer 2 — OPNsense
[ ] WAN works
[ ] LAN management works
[ ] NAT behaves as designed
[ ] WAN management blocked
[ ] firewall logging reviewed

## Layer 3 — VLANs
[ ] VLAN 10 gateway works
[ ] VLAN 20 gateway works
[ ] VLAN 30 gateway works
[ ] VLAN 40 gateway works
[ ] inter-VLAN default deny works

## Layer 4 — Identity
[ ] ipa01 resolves
[ ] Kerberos works
[ ] LDAP works
[ ] test Linux enrollment works
[ ] sudo/HBAC works
[ ] denied access test works

## Layer 5 — Database
[ ] db01 resolves
[ ] PostgreSQL listens only where required
[ ] app01 -> db01:5432 works
[ ] unauthorized source -> 5432 is blocked
[ ] Redis works only for approved application sources
[ ] unauthorized source -> 6379 is blocked

## Layer 6 — Application
[ ] app01 Docker works
[ ] ingress works
[ ] deployed services start
[ ] health checks pass
[ ] persistent data survives restart
[ ] backend ports are not WAN-exposed

## Layer 7 — Automation
[ ] auto01 resolves
[ ] Ansible reaches intended hosts
[ ] OpenTofu initializes
[ ] plan is reviewable
[ ] state is protected

## Layer 8 — DNS
[ ] forward lookups work
[ ] reverse lookups work
[ ] resolver authority is documented
[ ] hosts use intended DNS

## Negative Security Tests
Test and record:
- WAN -> Proxmox 8006: BLOCK
- WAN -> OPNsense management: BLOCK
- WAN -> SSH: BLOCK
- WAN -> PostgreSQL 5432: BLOCK
- WAN -> Redis 6379: BLOCK
- unauthorized VLAN -> DB: BLOCK
- unauthorized host -> FreeIPA privileged service: BLOCK

## Evidence
Record:
- date/time;
- component;
- source;
- destination;
- protocol/port;
- expected result;
- actual result;
- evidence location;
- deviation.

Never record secrets.

## Final Acceptance
The environment is accepted only when every required test is either PASS or explicitly documented as a known deviation with status.

## Follow-on
After acceptance, use the Day-2 documentation for operations, maintenance and troubleshooting.
