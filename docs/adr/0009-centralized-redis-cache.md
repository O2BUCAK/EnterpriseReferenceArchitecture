# ADR 0009: Centralized Redis for Explicit Cache Dependencies

## Status
**Accepted**

## Context

The reference architecture includes applications that require Redis for cache or cache-related functionality. A separate Redis instance per application would increase resource usage and operational duplication on the current modest-hardware lab.

At the same time, Redis must not become an implicit dependency of every application simply because a shared Redis service exists.

## Decision

Use a centralized Redis service on `db01` for applications with an explicit Redis requirement.

Applications must receive access only to the Redis resources they require.

The cache architecture follows these principles:

- Redis is a supporting cache/data service, not a universal application dependency.
- Each application must have a documented Redis use case.
- Cache keys and ownership must be separated by application.
- TTL and invalidation behavior must be defined.
- Failure behavior when Redis is unavailable must be documented.
- Sensitive data must not be placed in Redis without an explicit security assessment.

## Consequences

### Positive

- Avoids unnecessary Redis instances on modest hardware.
- Creates a clear shared cache boundary.
- Simplifies resource planning and administration.
- Makes Redis dependencies explicit in the dependency graph.

### Trade-offs

- Multiple applications share the same Redis service and resource pool.
- Redis becomes a shared infrastructure dependency for applications that use it.
- Application isolation must be enforced through configuration and access control.
- A Redis service failure can affect multiple dependent applications.

## Current Application Mapping

| Application | Redis | Reason |
|---|---|---|
| NetBox | Yes | Explicit requirement in the selected architecture |
| Keycloak | No | No Redis dependency selected |
| OpenBao | No | Uses its selected internal storage architecture |
| Teleport CE | No | No Redis dependency selected |
| Squid | No | No Redis dependency selected |

This mapping must be revalidated against the selected application versions before implementation.

## Implementation Note

Redis is planned on `db01`. It must not be marked **Implemented** until it has been installed, configured, and validated in the laboratory.

## Revisit Trigger

Revisit this decision if:

- measured Redis resource consumption becomes a capacity constraint;
- application isolation requirements change;
- an application requires a Redis topology incompatible with the shared model;
- availability or recovery requirements change;
- the number or workload of Redis consumers materially increases.

## Related Documentation

- [Cache Architecture](../architecture/cache.md)
- [Dependency Graph](../architecture/dependency-graph.md)
- [Resource Matrix](../resource-matrix/vm-resource-matrix.md)
