# Pardus db01 — PostgreSQL + Redis Build Runbook

## Purpose
Build the database VM `db01` running Pardus Server with PostgreSQL and Redis.

## Dependencies
Complete Proxmox, OPNsense and the identity foundation first.

## VM
Reference:
- 4 vCPU
- 8 GiB RAM
- 20 GiB OS disk
- 50 GiB data disk
- VLAN 30
- hostname `db01`

The second disk is added during VM creation. During Pardus installation, create the required LVM volumes on the intended disks according to the repository disk design.

## Pardus Installation
1. Create `db01`.
2. Add both disks before OS installation.
3. Attach the verified Pardus Server ISO.
4. Install Pardus.
5. Create the documented LVM layout during installation.
6. Set hostname/FQDN.
7. Configure static IP.
8. Configure DNS and NTP.
9. Reboot and remove ISO.

Validate:
```bash
hostnamectl
ip addr
ip route
timedatectl
lsblk
df -h
```

## Administrative Identity
Human administration uses the FreeIPA account assigned to the administrator, for example `ersin_pardus`, with sudo where authorized.

PostgreSQL administration is intentionally separate.

Use `postgres_sa` for the PostgreSQL administrative/service context defined by this project.

Do not confuse:
```
Linux login != PostgreSQL role != application DB account
```

## PostgreSQL
1. Install the repository-approved PostgreSQL version.
2. Initialize the cluster.
3. Configure listen address according to the network design.
4. Restrict access with PostgreSQL authentication and `pg_hba.conf`.
5. Enable the service.
6. Test local administration using the approved PostgreSQL administrative identity.
7. Create application-specific databases and roles only when the application is actually deployed.

Example role separation:
- `postgres_sa`: administrative/service context
- `nextcloud_db`: database
- `nextcloud_sa`: application connection role
- `nextcloud_dba`: application database administration role where required

Never give an application unnecessary superuser privileges.

## Redis
1. Install the repository-approved Redis package.
2. Bind only to required interfaces.
3. Protect Redis according to the selected Redis release.
4. Do not expose 6379 to WAN.
5. Permit access only from applications that require it.

## Validation
```bash
systemctl --failed
ss -lntup
```

Test PostgreSQL from db01 and from an authorized application source after firewall rules are implemented. Test Redis similarly.

## Completion
[ ] Pardus installed
[ ] both disks/LVM verified
[ ] FreeIPA login tested
[ ] PostgreSQL installed
[ ] PostgreSQL access restricted
[ ] postgres_sa model applied
[ ] Redis installed/restricted
[ ] firewall flows validated
[ ] evidence recorded
