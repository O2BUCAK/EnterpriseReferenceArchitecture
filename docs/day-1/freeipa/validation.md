# FreeIPA — Validation

> **Day 1 — Validate**

This document defines the validation procedure for `ipa01` after the FreeIPA identity platform has been installed and configured.

## Status

**Planned.** FreeIPA is not currently implemented in the laboratory. The tests below become evidence only after they are actually executed against the lab deployment.

---

## 1. Validation Principle

FreeIPA validation must prove the complete identity dependency chain:

```text
Network
  ↓
DNS
  ↓
NTP
  ↓
Kerberos
  ↓
LDAP / Directory
  ↓
Identity
  ↓
Host Enrollment
  ↓
Authentication / Authorization
```

A successful web login alone is not sufficient validation.

---

## 2. Validation Prerequisites

Before testing FreeIPA, confirm:

- `ipa01` is running.
- Hostname and FQDN are correct.
- The Identity VLAN is operational.
- DNS is operational.
- NTP/chrony is synchronized.
- FreeIPA services are running.
- A controlled Linux test client is available.
- Current configuration has been backed up where appropriate.

---

## 3. Host Identity Validation

On `ipa01`, verify:

```bash
hostnamectl
hostname --fqdn
ip address
ip route
```

Expected:

```text
Hostname: ipa01
FQDN:     ipa01.<documented-domain>
Address:  <documented static address>
Gateway:  <documented gateway>
```

### Pass Criteria

The host identity matches the documented deployment and DNS records.

---

## 4. DNS Validation

Test forward and reverse resolution.

Example:

```bash
host ipa01.<domain>
host <ipa01-ip>
getent hosts ipa01.<domain>
```

Validate:

- Forward lookup
- Reverse lookup
- FreeIPA service records where applicable
- Internal client resolution

### Pass Criteria

The expected records resolve consistently from both `ipa01` and the test client.

---

## 5. NTP Validation

Verify time synchronization.

```bash
timedatectl
chronyc tracking
chronyc sources -v
```

Record:

```text
NTP source:
Stratum:
System clock synchronized:
Last successful synchronization:
```

### Pass Criteria

The host reports synchronized time and uses the intended time source.

Kerberos-dependent tests should not continue if significant clock synchronization problems exist.

---

## 6. FreeIPA Service Health

Verify the FreeIPA services using the supported administrative tools for the installed release.

Check:

- Directory service
- Kerberos
- DNS if enabled
- Certificate services if enabled
- Web interface
- Required FreeIPA system services

The exact service names may vary by supported release.

### Pass Criteria

Required services are running without persistent startup or dependency errors.

---

## 7. Kerberos Validation

Test Kerberos authentication using a controlled administrative or test identity.

Example workflow:

```text
Obtain Kerberos ticket
        ↓
Verify ticket
        ↓
Use ticket for authenticated FreeIPA operation
```

Use the supported FreeIPA/Kerberos commands for the installed release.

Record:

```text
Principal:
Realm:
Ticket obtained: PASS / FAIL
Ticket validity: PASS / FAIL
```

### Pass Criteria

A valid ticket can be obtained and verified without clock, DNS, or realm errors.

---

## 8. LDAP / Directory Validation

Verify that the directory service responds correctly to authenticated administrative queries.

Test:

- Directory availability
- Base search
- User lookup
- Group lookup
- Authentication-backed query

Do not expose directory credentials in test logs or documentation.

### Pass Criteria

Expected directory objects can be queried and returned correctly.

---

## 9. Administrative Access Validation

Test the FreeIPA administration interface from the intended Management VLAN/path.

Validate:

- HTTPS access
- Correct certificate
- Administrative authentication
- Expected permissions
- No access from prohibited network segments

### Positive Test

```text
Management client → FreeIPA administration
Expected: ALLOW
```

### Negative Test

```text
Untrusted VLAN → FreeIPA administration
Expected: DENY
```

The exact network policy depends on the deployed segmentation architecture.

---

## 10. User and Group Validation

Create a controlled test identity only when required for validation.

Test:

1. User creation.
2. Group creation.
3. Group membership.
4. Authentication.
5. Removal/revocation.

Example conceptual flow:

```text
Create test-user
      ↓
Add to test-group
      ↓
Authenticate
      ↓
Verify group membership
      ↓
Remove test-user
```

### Pass Criteria

Identity lifecycle operations behave as expected and changes are reflected in the directory.

Remove temporary test identities after validation unless they serve a documented operational purpose.

---

## 11. Linux Client Enrollment Validation

Use a controlled Fedora/Linux test VM.

Validate:

- Client DNS configuration
- Time synchronization
- FreeIPA discovery
- Host enrollment
- Kerberos authentication
- Identity lookup

Target:

```text
Linux test client
       |
       +-- DNS
       +-- NTP
       +-- Kerberos
       +-- LDAP
       |
       v
     ipa01
```

### Pass Criteria

The client enrolls successfully and can resolve the expected identity information.

---

## 12. Identity Lookup Validation

From an enrolled client, test identity resolution through the configured identity stack.

Examples may include:

```bash
id <test-user>
getent passwd <test-user>
getent group <test-group>
```

Use the commands appropriate to the configured NSS/SSSD integration.

### Pass Criteria

The expected user/group information is returned from the centralized identity service.

---

## 13. Authentication Validation

Test a controlled user authentication flow on the enrolled Linux client.

Validate:

- Correct credentials succeed.
- Invalid credentials fail.
- Disabled/removed identities cannot authenticate.
- Authentication events are logged.

Do not record passwords in evidence.

### Pass Criteria

Authentication behavior matches the intended identity policy.

---

## 14. Authorization / Privilege Validation

If centralized sudo or privilege rules are configured, test both allowed and denied operations.

Example:

```text
infra-admin → permitted administrative action   ALLOW
normal-user → privileged administrative action  DENY
```

Do not use broad unrestricted privileges as a substitute for testing the actual policy.

---

## 15. Certificate Validation

If FreeIPA certificate services are enabled, validate:

- Certificate issuance
- Certificate subject/SAN
- Validity period
- Trust chain
- Service use
- Renewal behavior where practical

Do not commit private keys or certificate material that exposes the lab.

---

## 16. Network Policy Validation

Confirm that only intended networks can reach FreeIPA services.

Reference model:

| Source | FreeIPA services | Expected |
|---|---|---|
| Management | Administration | Allow |
| Identity clients | Required identity services | Allow |
| Application | Only if dependency exists | Restricted |
| Database | Only if dependency exists | Restricted |
| Internet | Identity services | Deny |

The exact service/port matrix must be recorded after implementation.

---

## 17. Logging Validation

Perform controlled identity operations and confirm useful logs are generated.

Test events:

- Successful authentication
- Failed authentication
- Administrative change
- User/group change
- Host enrollment

Record where the evidence is available and how long it is retained.

### Pass Criteria

Important identity events can be correlated with time, identity, and operation.

---

## 18. Backup Validation

Verify that the configured FreeIPA backup process produces a usable backup artifact.

Do not consider:

```text
Backup job completed = Recovery validated
```

A controlled restore test is required.

### Pass Criteria

The backup is created successfully, protected appropriately, and the documented restore procedure is executable.

Full restore testing should be incorporated into Day 2 recovery procedures.

---

## 19. Reboot Persistence

Perform a controlled reboot of `ipa01` after configuration is stable.

After reboot verify:

- Network
- DNS
- NTP
- FreeIPA services
- Kerberos
- LDAP
- Web administration
- Test-client identity lookup
- Test authentication

### Pass Criteria

Required identity services recover automatically and function without manual emergency intervention.

---

## 20. Failure / Recovery Validation

Use safe, controlled failure scenarios.

Examples:

- Temporarily stop a non-critical test service.
- Introduce a controlled DNS failure in an isolated test scenario.
- Test behavior after a FreeIPA service restart.
- Restore a test configuration from documented backup where appropriate.

Observe the dependency chain rather than immediately changing multiple settings.

Do not intentionally corrupt the only production-equivalent identity database.

---

## 21. End-to-End Validation

The final test should demonstrate a real identity-dependent workflow.

Example:

```text
Test Linux client
       |
       | DNS
       v
     ipa01
       |
       | Kerberos / LDAP / SSSD
       v
Centralized identity
       |
       v
User authentication
       |
       v
Authorized Linux session
```

This is stronger evidence than a successful installation screen.

---

## 22. Validation Evidence

Record one entry for each important test:

```text
Validation ID:
Date:
Host:
Source:
Destination:
Operation:
Expected:
Actual:
Result: PASS / FAIL / N/A
Evidence:
Notes:
```

Redact:

- Passwords
- Private keys
- Recovery secrets
- Sensitive tokens
- Unnecessary personal data

---

## 23. Validation Matrix

| Area | Test | Status |
|---|---|---|
| Host | FQDN | ⬜ |
| Network | Identity VLAN connectivity | ⬜ |
| DNS | Forward lookup | ⬜ |
| DNS | Reverse lookup | ⬜ |
| NTP | Clock synchronization | ⬜ |
| Services | FreeIPA health | ⬜ |
| Kerberos | Ticket acquisition | ⬜ |
| LDAP | Directory query | ⬜ |
| Admin | Web administration | ⬜ |
| Identity | User/group lifecycle | ⬜ |
| Client | Host enrollment | ⬜ |
| NSS/SSSD | Identity lookup | ⬜ |
| Auth | User authentication | ⬜ |
| AuthZ | Privilege policy | ⬜ / N/A |
| Certificates | Certificate workflow | ⬜ / N/A |
| Network | Service restriction | ⬜ |
| Logging | Audit evidence | ⬜ |
| Backup | Backup creation | ⬜ |
| Recovery | Restore test | ⬜ |
| Persistence | Post-reboot | ⬜ |
| E2E | Real identity workflow | ⬜ |

---

## 24. Completion Criteria

FreeIPA can be marked **Validated** only when:

1. Host identity is correct.
2. DNS works in both required directions.
3. Time synchronization is stable.
4. Core FreeIPA services are healthy.
5. Kerberos authentication works.
6. LDAP directory queries work.
7. Administrative access is restricted and functional.
8. User/group lifecycle works.
9. At least one controlled Linux client enrolls successfully.
10. Centralized identity lookup works.
11. Authentication works as designed.
12. Authorization rules are tested where implemented.
13. Network restrictions behave as expected.
14. Important identity events are logged.
15. Backup is operational.
16. Recovery has been tested or explicitly deferred to Day 2 with a documented reason.
17. Configuration survives reboot.
18. Evidence has been recorded.

> **FreeIPA is validated when identity works as an operational service, not merely when the installer reports success.**

## Related Documentation

- [`installation.md`](installation.md) — FreeIPA installation
- [`configuration.md`](configuration.md) — FreeIPA configuration
- [`../network/segmentation.md`](../network/segmentation.md) — Network segmentation
- [`../network/validation.md`](../network/validation.md) — Network validation
- [`../../architecture/identity.md`](../../architecture/identity.md) — Identity architecture
- [`../../security/security.md`](../../security/security.md) — Security architecture
- [`../documentation-standard.md`](../documentation-standard.md) — Day 1 documentation standard
