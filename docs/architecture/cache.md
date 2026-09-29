# Cache Architecture

> Enterprise Reference Architecture — Cache Design

## Status

**Planned / Reference Architecture.**

Redis is planned on `db01` for applications with an explicit cache or cache-related requirement.

## Purpose

Caching is used only when there is a measurable or clear architectural reason to reduce repeated work, latency, or load on a backing service.

A cache is **not** automatically added to every application.

## Design Principles

1. Cache only data that is suitable for caching.
2. Treat the system of record separately from the cache.
3. Give each cache use case an explicit owner and purpose.
4. Define TTL and invalidation behavior.
5. Document stale-data tolerance.
6. Avoid turning Redis into an implicit dependency of every application.
7. Prefer the simplest cache model that satisfies the requirement.
8. Validate the effect with evidence before increasing cache complexity.

## Selected Platform

The current architecture plans a centralized Redis service on `db01`.

```text
Application
     |
     | cache request
     v
   Redis
     |
     | cache miss
     v
PostgreSQL / Source of Truth
```

Redis is a supporting state/cache layer. Persistent application data remains owned by the appropriate database or application subsystem.

## Cache-Aside Pattern

The default application pattern is cache-aside:

```text
Read
 ↓
Application
 ↓
Redis
 ├── HIT  → return cached value
 └── MISS → read source of truth
              ↓
           populate cache
              ↓
           return value
```

Write behavior must explicitly define how cache entries are invalidated or refreshed.

## Cache Metadata Standard

For every cache use case, document:

| Field | Required definition |
|---|---|
| Key format | How entries are named |
| Value | What is stored |
| Source of truth | Authoritative data source |
| TTL | Expiration period |
| Invalidation | What causes eviction / refresh |
| Staleness | Maximum acceptable staleness |
| Size | Expected memory footprint |
| Failure behavior | What happens if Redis is unavailable? |
| Security | Whether data may contain sensitive information |
| Ownership | Which application owns the keyspace |

## Failure Behavior

Applications must define behavior when Redis is unavailable.

Possible designs include:

```text
Redis unavailable
      |
      +--> Fall back to source of truth
      |
      +--> Degrade optional feature
      |
      +--> Fail request
```

The selected behavior depends on the application requirement and must be documented.

## Current Application Mapping

Based on the current reference dependency model:

| Application | Redis | Decision |
|---|---|---|
| NetBox | Yes | Explicit requirement in the selected architecture |
| Keycloak | No | Do not add Redis solely because Redis exists |
| OpenBao | No | Uses selected internal storage architecture |
| Teleport CE | No | No default Redis dependency selected |
| Squid | No | No Redis dependency selected |

This mapping must be revalidated against the selected application versions before implementation.

## Anti-Patterns

Avoid:

- caching everything;
- indefinite TTLs without a reason;
- storing the only copy of important persistent data in Redis;
- undocumented invalidation;
- sharing keys between unrelated applications;
- adding Redis only because it is already available.

## Validation

Before declaring a cache design implemented, record:

```text
Application:
Use case:
Expected access pattern:
TTL:
Hit/miss observations:
Memory usage:
Failure behavior tested:
Result:
```

## Related Documentation

- [Dependency Graph](dependency-graph.md)
- [Centralized PostgreSQL ADR](../adr/0007-centralized-postgresql.md)
- [VM Resource Matrix](../resource-matrix/vm-resource-matrix.md)
