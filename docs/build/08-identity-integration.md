# Identity Integration — Build Runbook

## Purpose
Connect Linux hosts and selected applications to the FreeIPA identity foundation.

## Dependency
04-freeipa-installation.md must be completed and validated.

## Linux Hosts
For each Linux host:
1. configure DNS;
2. install the approved FreeIPA client packages;
3. enroll the host;
4. verify identity lookup;
5. configure sudo policy;
6. configure HBAC;
7. test login from a non-root session.

Validation examples:
```bash
id <test-user>
getent passwd <test-user>
getent group <test-group>
```

## Account Separation
Maintain these boundaries:
```
Human identity
    |
    +--> Linux login / sudo

Service identity
    |
    +--> application/database operation
```

A human account must not become a shared service credential.

## Applications
Only integrate an application with FreeIPA when the application's supported LDAP/Kerberos/OIDC/SAML mechanism and the architecture require it.

Keycloak may act as an application identity broker. Do not assume every application should query FreeIPA directly.

## Privilege
Grant only the required groups and sudo/HBAC rules. Test both an allowed login and a denied login.

## Completion
[ ] Linux host enrollment works
[ ] user/group lookup works
[ ] sudo policy tested
[ ] HBAC tested
[ ] service accounts separated
[ ] application identity flows documented
