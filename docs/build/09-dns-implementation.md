# DNS Implementation — Build Runbook

## Purpose
Implement and validate the DNS architecture across OPNsense, FreeIPA and project hosts.

## Important
The repository currently describes DNS as a target design. The authoritative responsibility must be decided before marking this document implemented.

## Target Responsibilities
OPNsense may provide network-level forwarding/resolution.

FreeIPA is planned to provide identity-related DNS capabilities.

There must be one documented authoritative source for each internal zone.

## Build Sequence
1. Confirm internal domain.
2. Confirm forward zone.
3. Confirm reverse zones.
4. Confirm gateway/DNS behavior on OPNsense.
5. Deploy FreeIPA.
6. Configure FreeIPA DNS if selected.
7. Configure clients to use the approved resolver path.
8. Test forward lookup.
9. Test reverse lookup.
10. Test external resolution where required.

## Required Records
Infrastructure records should include the actual project hosts:
- fw01
- ipa01
- db01
- app01
- auto01

Use the actual approved addresses, not examples copied from this document.

## Validation
From each Linux host:
```bash
hostname -f
getent hosts <internal-host>
getent hosts <internal-fqdn>
```

Test reverse resolution for infrastructure addresses.

## Failure Rules
Do not solve DNS failures by adding arbitrary entries to /etc/hosts on every server. Fix the authoritative DNS design.

## Completion
[ ] authoritative zone identified
[ ] forward lookup works
[ ] reverse lookup works
[ ] OPNsense resolver role documented
[ ] FreeIPA DNS role documented
[ ] all infrastructure hosts resolve
[ ] clients use intended DNS path
