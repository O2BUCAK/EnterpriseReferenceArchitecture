# DNS Architecture

> Target DNS architecture for the Enterprise Reference Architecture.

## Status
**Planned architecture.** OPNsense is implemented; the FreeIPA DNS model remains planned.

## Purpose
DNS is an infrastructure dependency for identity, Kerberos, TLS, service discovery, administration, and application access.

## Roles
| Layer | Component | Responsibility |
|---|---|---|
| Internal authoritative DNS | FreeIPA | Internal forward/reverse zones |
| Network resolver / forwarding | OPNsense | Recursive/forwarding services where appropriate |
| External authoritative DNS | Public DNS provider | Public names |

Avoid competing authoritative sources for the same internal zone.

## Internal Namespace
Documentation placeholder:
```
corp.example.com
```

Example records:
```
ipa01.corp.example.com  -> 10.10.20.10
db01.corp.example.com   -> 10.10.30.10
app01.corp.example.com  -> 10.10.40.10
auto01.corp.example.com -> 10.10.10.20
```

## Forward and Reverse DNS
Both directions must be maintained:
```
Name → A/AAAA → Address
Address → PTR → Name
```

## Resolver Flow
Target internal flow:
```
Client / VM
   ↓
Configured internal resolver
   ↓
FreeIPA DNS
   ↓
Upstream DNS for external names
```

The final placement of resolver services is validated during implementation.

## DNS Security
- Do not expose internal authoritative DNS to the Internet.
- Restrict recursive resolution to trusted networks.
- Keep forward/reverse records consistent.
- Document split-DNS behavior where used.
- DNS does not replace firewall enforcement.

## Validation Record
```
Zone:
Authoritative server:
Forward lookup:
Reverse lookup:
External lookup:
Client resolver:
Expected:
Actual:
Evidence:
```

## Related Documentation
- [Network Architecture](network.md)
- [Firewall Rule Set](firewall-rule-set.md)
- [Port Map](port-map.md)
- [Identity Architecture](../architecture/identity.md)
- [PKI Architecture](../architecture/pki.md)
