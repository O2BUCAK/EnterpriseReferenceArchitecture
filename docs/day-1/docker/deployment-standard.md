# Docker Deployment Standard

> Standard deployment model for containerized workloads on app01.

## Status
**Planned standard.** Docker is planned; this document defines the target deployment convention.

## Application Layout
```
/opt/app-data/<application>/
├── compose.yaml
├── README.md
├── .env.example
├── config/
└── data/
```

Real secrets never enter the repository.

## Naming
- Project: <application>
- Containers: <application>-<service>
- Networks: <application>-frontend / <application>-backend
- Volumes: <application>-<data>

## Network Model
```
Client
  ↓
Nginx
  ↓
frontend network
  ↓
Application
  ↓
backend network
  ↓
PostgreSQL / internal dependency
```
Containers join only networks they require.

## Published Ports
Publish only required ports. Prefer Nginx as the common HTTPS ingress and avoid direct exposure of internal application ports.

## Configuration Standard
- Use supported upstream images.
- Pin versions; use image digests where practical.
- Record image source and version.
- Define health checks where supported.
- Define a suitable restart policy.
- Keep configuration in Git only when it contains no secrets.

## Persistent Data
```
Container → named volume / bind mount → /opt/app-data/<application> → app01 data disk
```
Application state must not depend on anonymous container storage.

## Resource Controls
For each important service record:
```
CPU:
Memory:
Storage:
Health check:
```
Values must remain compatible with the resource matrix.

## Update and Rollback
```
Review release → Stage image → Validate configuration → Deploy → Health check → Application test → Record version/digest
```
Rollback uses the previously validated image and configuration.

## Supply Chain Record
```
Publisher:
Registry:
Repository:
Tag:
Digest:
Security review:
Deployment date:
```

## Deployment Evidence
```
Application:
Version:
Image digest:
Host:
Networks:
Published ports:
Volumes:
Dependencies:
Secret mechanism:
Deployment date:
Validation:
Known deviation:
```

## Related Documentation
- [Dependency Graph](../../architecture/dependency-graph.md)
- [Port Map](../../network/port-map.md)
- [Secrets Management](../../security/secrets-management.md)
