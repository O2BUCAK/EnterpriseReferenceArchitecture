# 📐 Mimari Tasarım Kararları (Architecture Decision Records - ADR)

Bu belge, **Enterprise Reference Architecture (FOSS Home Lab)** projesinin temelini oluşturan mühendislik ve güvenlik kararlarını, seçilen teknolojileri ve bu seçimlerin arkasındaki kurumsal (NIST, ISO 27001) standartlara dayalı gerekçeleri açıklar.

---

## 1. Zero Plaintext ve Merkezi Sır Yönetimi (Secret Management)

* **Karar:** Hiçbir yapılandırma dosyasında, betikte (script), Git reposunda veya terminal geçmişinde (history) düz metin (plaintext) şifre, API anahtarı veya sertifika barındırılmayacaktır.
* **Seçilen Teknoloji:** OpenBao (HashiCorp Vault'un açık kaynaklı FOSS forku).
* **Gerekçe:** Kurumsal ortamlardaki veri sızıntılarının (data breaches) en büyük nedeni kaynak kodlarına veya yapılandırma dosyalarına gömülmüş (hardcoded) şifrelerdir. Sisteme kimlik doğrulaması yapacak tüm servisler (Örn: Netbox, Woodpecker CI) veritabanı şifrelerini OpenBao'dan dinamik olarak çekecek şekilde tasarlanmıştır.

## 2. Ağ Segmentasyonu ve Güvenlik Duvarı İzolasyonu

* **Karar:** Sunucular "Flat Network" (Düz Ağ) yapısında çalıştırılmayacak; Görevlerine ve kritiklik seviyelerine göre VLAN'lara bölünecektir.
* **Seçilen Teknoloji:** OPNsense (VLAN Gateway & Firewall).
* **Gerekçe:** "Sıfır Güven" (Zero Trust) modeline göre iç ağdaki bir makineye dahi güvenilmez. Uygulama katmanındaki (Docker) bir konteyner ele geçirilse dahi, mikro-segmentasyon kuralları gereği Veritabanı katmanına (PostgreSQL) sadece belirli IP'lerden ve 5432 portundan kısıtlı erişim izni verilir (Implicit Deny). Dışarıdan iç ağa doğrudan yönlendirme (routing) yasaktır; tüm erişimler VPN veya Teleport CE (Bastion) üzerinden sağlanır.

## 3. Merkezi Kimlik ve Erişim Yönetimi (IAM & SSO)

* **Karar:** Her sunucuda veya uygulamada ayrı ayrı kullanıcı (local user) açılmayacak; kimlik doğrulama işlemleri merkezi bir otorite üzerinden gerçekleştirilecektir.
* **Seçilen Teknoloji:** Core IAM için FreeIPA (Kerberos & LDAP); Web SSO için Keycloak (OIDC/SAML).
* **Gerekçe:** Kullanıcıların işten ayrılması veya rol değiştirmesi durumunda erişimlerinin tek bir noktadan anında kesilebilmesi kurumsal güvenliğin temelidir. FreeIPA, ağdaki cihazların (Linux makineler) ve servis hesaplarının merkezini oluştururken, Keycloak; Netbox, Wiki.js, Portainer gibi modern web uygulamalarına "Tek Oturum Açma (SSO)" yeteneği kazandırır.

## 4. Evrensel (Universal) Veritabanı ve Ayrıştırılmış Disk Mimarisi

* **Karar:** Uygulamaların kendi içlerindeki gömülü (SQLite) veritabanları yerine, tüm veriler merkezi, yedeklenebilir ve izole edilmiş bir SQL kümesinde tutulacaktır. Ayrıca I/O (Okuma/Yazma) yoğunluğu olan dizinler ana işletim sisteminden (OS) ayrı disklere bölünecektir.
* **Seçilen Teknoloji:** Pardus Server üzerinde Merkezi PostgreSQL.
* **Gerekçe (Merkezi DB):** Veritabanlarının tek merkezde olması, yedekleme (Backup), felaket kurtarma (Disaster Recovery) ve versiyon güncellemelerini kolaylaştırır.
* **Gerekçe (Disk İzolasyonu):** Pardus VM kurulumunda `/`, `/var`, `/home` ve `/tmp` dizinleri ayrı sanal SCSI disklere bağlanmıştır. Bu kurumsal pratik (Best Practice), PostgreSQL'in aşırı log üretmesi veya veri şişmesi durumunda ana işletim sisteminin (Root `/`) dolup çökmesini engeller (Availability).

## 5. Tam Otomasyon ve Altyapının Kod Olarak Yönetilmesi (IaC)

* **Karar:** Altyapı bileşenleri (VM'ler, Ağ, Paketler) manuel olarak arayüzden değil, deklaratif kod blokları ile yapılandırılacaktır.
* **Seçilen Teknoloji:** RHEL VM üzerinde Ansible (Configuration Management) ve OpenTofu (Provisioning).
* **Gerekçe:** Kurumsal ortamlarda "İstenebilir ve Tekrarlanabilir Durum" (Desired State) esastır. Bir sunucu çöktüğünde veya yenisi gerektiğinde insan hatasını sıfıra indirmek ve saniyeler içinde yeni makineyi "Production-Ready" (Üretime Hazır) hale getirmek ancak IaC ile mümkündür. Ayrıca kodların CI/CD pipeline'ından (Woodpecker CI) geçerek test edilmesi sağlanır.

## 6. Sadece FQDN ile Trafik Yönlendirme ve Port Çakışmalarını Önleme

* **Karar:** Uygulamalara IP:PORT (Örn: `10.0.40.2:8000`) mantığı ile bağlanılmayacak, her servisin kurumsal bir etki alanı adı (FQDN) olacaktır (Örn: `netbox.corp.example.com`).
* **Seçilen Teknoloji:** Nginx Reverse Proxy ve FreeIPA (Unbound DNS entegrasyonu ile).
* **Gerekçe:** Ubuntu Docker host üzerinde aynı anda 10'dan fazla servis koşmaktadır (Netbox, Wiki.js vb.). Port çakışmalarını (Port Conflicts) engellemek ve trafiği 80/443 (HTTP/HTTPS) portlarında standartlaştırmak için Nginx ters vekil (Reverse Proxy) olarak konumlandırılmıştır. Nginx, gelen alan adına göre trafiği arka planda doğru konteynerin yerel portuna yönlendirir ve TLS (SSL) sonlandırmasını tek merkezden yaparak güvenliği artırır.

## 7. Container Engine (Konteyner Motoru) Seçimi

* **Karar:** Daemon-less (Podman) yapıların avantajlarına rağmen, lab ortamının ana ekosistemi ve entegrasyon hızı gözetilerek endüstri standardı olan araç tercih edilmiştir.
* **Seçilen Teknoloji:** Docker Engine & Docker Compose.
* **Gerekçe:** Nginx, Portainer, Keycloak ve OpenBao gibi çekirdek mimari bileşenlerinin topluluk desteği, sorun giderme (troubleshooting) dokümantasyonları ve Compose dosyası standartları büyük ölçüde Docker mimarisi üzerine kuruludur. Zaman ve odak yönetimi açısından, ekosistemle %100 uyumlu olan Docker tercih edilmiş; güvenlik endişeleri ise OPNsense ve Teleport (Bastion) seviyesinde çözülmüştür.

## 8. Sınırlı Kaynak (Donanım) Optimizasyonu

* **Karar:** Kullanılacak donanımın (Dell Latitude 5540 - 32GB RAM, 12 vCPU thread) sınırları dahilinde kalmak için "Ağır (Java tabanlı) veya Monolitik" ticari sistemler yerine, aynı görevi yapan ultra hafif, Go/Rust/Python tabanlı modern FOSS araçlar seçilmiştir.
* **Örnekler:**
    * *GitLab (8GB RAM)* yerine ➔ **Forgejo + Woodpecker CI (~200MB RAM)**
    * *OpenVAS/Nessus (8GB RAM)* yerine ➔ **Nuclei + Grype + OWASP ZAP (On-Demand, düşük RAM)**
    * *Nexus/Artifactory (4GB+ RAM)* yerine ➔ **Project Pulp (~2GB RAM)**
* **Gerekçe:** Ev laboratuvarı (Home Lab) konseptinde sürdürülebilirliği sağlamak ve sistemde "Out-of-Memory (OOM)" hataları yaşamamak için Fiyat/Performans ve Kaynak/Performans metrikleri dikkate alınmıştır.
