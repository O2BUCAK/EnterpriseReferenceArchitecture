# 🏛️ Enterprise Reference Architecture (FOSS Home Lab)

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Hypervisor: Proxmox VE](https://img.shields.io/badge/Hypervisor-Proxmox_VE-orange.svg)](https://www.proxmox.com)
[![Security: Zero Plaintext](https://img.shields.io/badge/Security-Zero_Plaintext-red.svg)](#-mimari-prensipler-ve-guvenlik-standartlari)
[![IAM: FreeIPA + Keycloak](https://img.shields.io/badge/IAM-FreeIPA_%2B_Keycloak-green.svg)](#)
[![Database: Pardus PostgreSQL](https://img.shields.io/badge/DB-Pardus_PostgreSQL-blue.svg)](#)

Açık kaynaklı (FOSS) yazılımlar kullanılarak uçtan uca tasarlanmış, **"Zero Trust"**, **"Zero Plaintext"** ve **"Mikro-segmentasyon"** prensiplerine dayanan **Kurumsal IT & Siber Güvenlik Referans Mimarisi Simülasyonu**.

Bu proje; bir şirketin tüm IT, Kimlik Yönetimi (IAM), Sır Yönetimi (Secret Management), Otomasyon (IaC), Ayrıcalıklı Erişim (PAM/Bastion), Veritabanı ve Güvenlik/İzleme (SecOps) süreçlerini **Dell Latitude 5540** donanımı üzerinde simüle etmek üzere kurgulanmıştır.

---

## 📐 Mimari Prensipler ve Güvenlik Standartları

1. **Zero Plaintext (Sıfır Düz Metin Şifre):** Hiçbir konfigürasyon dosyasında veya kod içinde şifre tutulmaz. Tüm şifreler, sertifikalar ve API token'ları **OpenBao (Vault)** üzerinden dinamik çekilir.
2. **Merkezi Kimlik ve Erişim Yönetimi (IAM & SSO):**
   * **Active Directory Domain:** `corp.example.com` (FreeIPA / Red Hat IdM).
   * **Web SSO / OIDC:** Keycloak (FreeIPA LDAP entegrasyonu ile).
   * **PAM / SSH Bastion:** Teleport CE (Kısa ömürlü sertifika tabanlı erişim).
3. **Merkezi Veritabanı Mimarisi:** Tüm servislerin (Nextcloud, Keycloak, Netbox, Wazuh, Zabbix vb.) veritabanı ihtiyacı **Pardus Server üzerindeki merkezi PostgreSQL** sunucusundan karşılanır.
4. **Kurumsal İsimlendirme Standartları:**
   * **Uygulama Servis Hesapları (AD):** `x_sa` *(Örn: keycloak_sa)*
   * **Uygulama Veritabanları (DB):** `x_db` *(Örn: netbox_db)*
   * **Veritabanı Kullanıcıları (DB Users):** `x_dba` *(Örn: netbox_dba)*
5. **Disk İzolasyon Standartı:** Tüm sanal makinelerde (VM) OS diski ile veri diskleri ayrıştırılmıştır. `/var`, `/home` ve `/tmp` dizinleri I/O performansını artırmak ve log dolmalarında sistemi korumak için **ayrı sanal disklerde** barındırılır.
6. **Ağ Segmentasyonu ve FQDN Yönetimi:** Mikro-segmentasyon OPNsense ile sağlanır. Port çakışmalarını önlemek için hiçbir servise doğrudan IP:Port ile değil, **Nginx Reverse Proxy** arkasında FQDN üzerinden erişilir.

---

## 💻 Donanım ve Altyapı Özellikleri

| Bileşen | Detay |
| :--- | :--- |
| **Fiziksel Donanım** | Dell Latitude 5540 |
| **İşlemci (CPU)** | 13th Gen Intel® Core™ i7-1355U (10 Fiziksel Çekirdek / 12 vCPU Thread) |
| **Bellek (RAM)** | 32 GB SODIMM DDR4 (2 x 16 GB - 3200 MT/s) |
| **Depolama (SSD)** | 512 GB PCIe NVMe Gen4 x4 NVMe SSD |
| **Hypervisor** | Proxmox VE |
| **Firewall / Gateway** | OPNsense (VLAN & Routing Engine) |

---

## 🌐 Ağ ve Sistem Topolojisi

```text
                               [ DIŞ DÜNYA / İSTEMCİ ]
                                          │
                                          ▼ (HTTPS: 443 / SSH: Teleport)
===================================================================================
[ KATMAN 1: GÜVENLİK VE AĞ GEÇİDİ - OPNsense Firewall ] (VLAN Gateway: 10.0.x.1)
  - Tüm ağın NTP Kaynağı (Port: 123)
  - Unbound DNS Forwarder (İç sorguları FreeIPA'e yönlendirir)
===================================================================================
       │
       ├─► [ VLAN 10: YÖNETİM (MGMT) - 10.0.10.0/24 ]
       │    ├─ Proxmox VE Host (pve.corp.example.com) [Port: 8006]
       │    └─ RHEL VM (Ansible & OpenTofu IaC Engine)
       │
       ├─► [ VLAN 20: KİMLİK VE CORE (CORE) - 10.0.20.0/24 ]
       │    └─ Fedora VM (FreeIPA - corp.example.com) [10.0.20.2]
       │        ├─ DNS (53 TCP/UDP) ──► Tüm sistemlerin DNS merkezi
       │        ├─ Kerberos (88) ────► SSSD ve Sistem girişleri
       │        └─ LDAPS (636) ──────► Keycloak & Vault Kullanıcı Sorguları
       │
       ├─► [ VLAN 30: VERİTABANI (DATA) - 10.0.30.0/24 ]
       │    └─ Pardus VM (PostgreSQL Merkezi DB) [10.0.30.2]
       │        ├─ Disk 1 (OS), Disk 2 (/var), Disk 3 (/home), Disk 4 (/tmp)
       │        └─ PostgreSQL (5432) ──► Sadece VLAN 40 ve Windows PC IP'sine açık
       │
       └─► [ VLAN 40: UYGULAMA (APP) - 10.0.40.0/24 ]
            └─ Ubuntu Docker Host [10.0.40.2]
                 ├─ Nginx Reverse Proxy (80/443)
                 ├─ OpenBao / Vault (8200) - "Zero Plaintext"
                 ├─ Keycloak SSO (8080)
                 ├─ Teleport CE Bastion (3080/3022)
                 ├─ Squid Gateway (3128) - İç ağ paket çıkış kapısı
                 └─ Netbox, Forgejo + Woodpecker CI, Wiki.js, Project Pulp
```

---

## 👨‍💻 Mimar & Geliştirici (Author)

Bu **Enterprise Reference Architecture** laboratuvar simülasyonu, kurumsal bilgi güvenliği ve sistem yönetimi standartları göz önüne alınarak tasarlanmıştır.

* **Geliştirici:** Ersin ÖZBUCAK
* **Web Sitesi / İletişim:** [www.ozbucak.com.tr](https://www.ozbucak.com.tr)
* **LinkedIn:** [Ersin ÖZBUCAK](https://www.linkedin.com/in/ersinozbucak/)
