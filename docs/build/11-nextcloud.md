# Nextcloud — Application Build Runbook

## Purpose
Deploy Nextcloud using the existing application platform and shared database architecture.

## Dependencies
- db01 PostgreSQL and Redis
- app01 Docker
- Nginx/ingress
- DNS
- required identity integration if selected

## Architecture
```
Client
  |
Nginx
  |
Nextcloud
  +---- PostgreSQL db01:5432
  +---- Redis db01:6379
```

## Database
Create a dedicated Nextcloud database and roles. Do not use the PostgreSQL superuser for application connections.

Use the project's account separation model:
- database: nextcloud_db
- application role: nextcloud_sa
- database administration role: nextcloud_dba where required

Use credentials supplied through the approved secret mechanism.

## Redis
Configure Redis according to the selected Nextcloud version and deployment documentation. Restrict Redis to the application path; do not expose 6379 publicly.

## Docker
Create a dedicated Nextcloud compose/project directory. Persist application data on the intended app/data filesystem.

## Nginx
Expose Nextcloud through the planned ingress. Do not expose PostgreSQL or Redis through the reverse proxy.

## Validation
- login page loads;
- HTTPS works;
- Nextcloud connects to PostgreSQL;
- Redis integration works;
- files survive container restart;
- database connection uses the dedicated role;
- backend ports are not WAN-exposed.

## Completion
[ ] application deployed
[ ] dedicated DB created
[ ] dedicated DB role used
[ ] Redis configured
[ ] HTTPS ingress works
[ ] persistence tested
[ ] security exposure reviewed
