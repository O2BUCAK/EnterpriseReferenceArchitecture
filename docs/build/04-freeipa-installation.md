# FreeIPA — Build Runbook

## Purpose
Deploy the identity foundation on `ipa01`.

## Dependencies
Complete Fedora installation and base network validation first.

## Architecture
FreeIPA provides the planned central identity service for Linux authentication, host enrollment, sudo/HBAC policy and identity-related DNS.

```
FreeIPA
 ├─ Users / Groups
 ├─ Host enrollment
 ├─ Kerberos
 ├─ LDAP
 ├─ sudo policy
 ├─ HBAC
 └─ DNS where explicitly selected
```

## Prerequisites
- stable hostname/FQDN
- working forward and reverse DNS
- synchronized time
- approved realm
- approved internal domain
- firewall rules for actual FreeIPA dependencies

Do not guess the realm or domain.

## Installation
1. Update Fedora.
2. Install the FreeIPA server packages appropriate for the selected Fedora release.
3. Follow the official installer for the selected FreeIPA deployment mode.
4. Configure the approved realm/domain.
5. Configure DNS only according to the repository DNS decision.
6. Complete installation.
7. Reboot if required.

## First Validation
Verify:
```bash
hostname -f
timedatectl
systemctl --failed
```

Use the FreeIPA administration tooling appropriate to the installed release to verify server status, Kerberos and LDAP.

## Users and Groups
Create groups before users where possible. Apply the project's account naming convention.

Human accounts and service accounts are different security principals.

Example architecture:
```
ersin_pardus -> human Linux login
postgres_sa   -> PostgreSQL administration/service context
nextcloud_sa  -> application database/service context
```

Do not use a human account as an application's permanent service identity.

## Linux Enrollment
Enroll a test Linux host only after DNS and time validation. Test:
- login
- sudo policy
- HBAC
- group membership
- host enrollment

## Security
Protect the IPA administrator credential and Kerberos material. Never store secrets in Git.

## Completion
[ ] FreeIPA installed
[ ] realm/domain verified
[ ] DNS responsibility verified
[ ] Kerberos works
[ ] LDAP works
[ ] test user works
[ ] host enrollment works
[ ] sudo/HBAC tested
[ ] evidence recorded
