# Application Platform — Build Runbook

## Purpose
Deploy the common application platform on `app01`.

## Dependencies
Complete 05 database and 06 Docker builds.

## Platform
The repository plans services including:
- Nginx
- Portainer CE
- Teleport CE
- Keycloak
- OpenBao
- NetBox
- Squid
- Forgejo
- Woodpecker CI
- Wiki.js
- Project Pulp where selected

Do not install every planned service automatically. Deploy a service only when its dependency and security requirements are documented.

## Common Pattern
```
Client
  |
Nginx / ingress
  |
Application container
  |
+----> PostgreSQL db01
+----> Redis db01 when required
+----> FreeIPA when required
```

## Compose Standards
Each application should have:
- dedicated directory;
- version-pinned images where practical;
- explicit networks;
- persistent volumes;
- non-secret configuration in Git;
- secrets supplied through the approved secret mechanism;
- health checks where supported;
- documented ports;
- documented dependencies.

## Database Dependencies
Use the database server on db01. Do not create ad-hoc PostgreSQL containers when the architecture requires the shared database service.

Keycloak, for example, requires its documented PostgreSQL and Redis dependencies if the selected deployment uses Redis.

## Reverse Proxy
Nginx is the intended ingress layer for web applications. Backend application ports should not be published to WAN unnecessarily.

## Validation
For each deployed application:
1. container starts;
2. health check passes;
3. dependency connection works;
4. expected ingress works;
5. unauthorized path is blocked;
6. logs are reviewed;
7. persistent data survives restart.

## Completion
[ ] Docker platform ready
[ ] ingress defined
[ ] each deployed service documented
[ ] dependencies documented
[ ] secrets excluded from Git
[ ] application health validated
