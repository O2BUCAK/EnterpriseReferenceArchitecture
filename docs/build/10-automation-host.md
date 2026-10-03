# auto01 — Ansible + OpenTofu Build Runbook

## Purpose
Build the automation host for infrastructure-as-code and configuration automation.

## VM
Reference:
- 2 vCPU
- 4 GiB RAM
- 20 GiB OS disk
- 20 GiB data disk
- VLAN 10
- hostname `auto01`

The repository architecture references RHEL for this role.

## Installation
1. Create the VM.
2. Add OS/data disks.
3. Install the approved RHEL version.
4. Configure hostname, static IP, DNS and NTP.
5. Enroll in FreeIPA when the identity layer is ready.
6. Apply sudo/HBAC policy.

## Ansible
Install the approved Ansible version from the organization's approved source.

Create:
```
inventory/
group_vars/
host_vars/
playbooks/
roles/
```

Keep secrets outside normal Git variables. Use the approved secret mechanism.

Test connectivity to one non-production target before running a larger playbook.

## OpenTofu
Install the approved OpenTofu release.

Keep state in the location defined by the architecture. Do not place sensitive state in a public repository.

Before applying infrastructure changes:
1. initialize;
2. validate;
3. plan;
4. review;
5. apply;
6. validate the result.

## SSH
Use centralized identity where supported, dedicated keys where required, and least privilege.

## Completion
[ ] RHEL installed
[ ] identity integration works
[ ] Ansible installed
[ ] inventory works
[ ] test playbook works
[ ] OpenTofu installed
[ ] state location defined
[ ] plan/apply workflow validated
