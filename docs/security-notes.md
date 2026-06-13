# Güvenlik Notları

Bu projede kullanıcı kimlik doğrulaması, yetkilendirme, veri güvenliği ve API erişimi güvenli yazılım geliştirme prensiplerine uygun şekilde tasarlanmıştır.

## Kimlik Doğrulama (Authentication)

Sistemde JWT (JSON Web Token) tabanlı kimlik doğrulama kullanılmaktadır.

Başarılı giriş sonrasında kullanıcıya:

* Access Token
* Refresh Token

oluşturulmaktadır.

Access token korunan API uç noktalarına erişim için kullanılırken, refresh token yeni access token üretmek amacıyla kullanılmaktadır.

## Yetkilendirme (Authorization)

Sistem rol tabanlı yetkilendirme mekanizması kullanmaktadır.

Desteklenen roller:

* System Admin
* School Admin
* Teacher

Her kullanıcı yalnızca kendi rolüne ait işlemleri gerçekleştirebilmektedir.

Örneğin:

* Öğretmen okul oluşturamaz, güncelleyemez veya silemez.
* School Admin yalnızca kendi okuluna ait işlemleri gerçekleştirebilir.
* System Admin sistem genelindeki yönetim işlemlerine erişebilir.

Bu yapı yetkisiz erişimlerin önlenmesini sağlamaktadır.

## Parola Güvenliği

Kullanıcı parolaları veritabanında düz metin olarak saklanmamaktadır.

Parolalar:

* Werkzeug Security
* Güvenli hash algoritmaları

kullanılarak hashlenmekte ve yalnızca hash değerleri veritabanına kaydedilmektedir.

Ayrıca sistemde minimum parola uzunluğu kontrolü uygulanmaktadır.

## JWT Güvenliği

JWT tokenları için:

* Access Token süresi: 15 dakika
* Refresh Token süresi: 7 gün

olarak yapılandırılmıştır.

Sistem ayrıca refresh token iptal (revocation) mekanizmasını desteklemektedir. Kullanıcı çıkış yaptığında ilgili refresh token geçersiz hale getirilmektedir.

## API Güvenliği

Korunan endpointlerde aşağıdaki kontroller uygulanmaktadır:

* JWT doğrulaması
* Rol doğrulaması
* Yetki kontrolü
* Kaynak erişim kontrolü

Yetkisiz veya geçersiz token ile yapılan istekler reddedilmektedir.

## Ortam Değişkenleri (Environment Variables)

Gizli bilgiler doğrudan kaynak kod içerisinde tutulmamaktadır.

Aşağıdaki bilgiler `.env` dosyası üzerinden yönetilmektedir:

* SECRET_KEY
* JWT_SECRET_KEY
* GEMINI_API_KEY
* Ollama yapılandırmaları

Örnek:

```env
SECRET_KEY=********
JWT_SECRET_KEY=********
GEMINI_API_KEY=********
OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

Bu yaklaşım hassas bilgilerin kaynak kodundan ayrılmasını sağlamaktadır.

## CORS Güvenliği

API erişimi yalnızca izin verilen istemcilerle sınırlandırılmıştır.

Geliştirme ortamında belirlenen güvenilir istemci adresleri dışında gelen istekler kabul edilmemektedir.

Bu yapı istenmeyen çapraz kaynak erişimlerini azaltmaktadır.

## Yapay Zeka Güvenliği

LLM çıktıları doğrudan sisteme kontrolsüz şekilde aktarılmamaktadır.

Yapay zeka çıktıları:

* JSON formatında doğrulanır.
* Zorunlu alan kontrollerinden geçirilir.
* Beklenen veri yapısına uygunluk açısından kontrol edilir.

Bu yaklaşım hatalı veya beklenmeyen model çıktılarının sisteme zarar vermesini önlemektedir.

## Gelecek Güvenlik Geliştirmeleri

İlerleyen sürümlerde aşağıdaki güvenlik geliştirmelerinin eklenmesi planlanmaktadır:

* HTTPS zorunluluğu
* Rate limiting
* API anahtarı erişim kontrolü
* Gelişmiş input validation
* Merkezi loglama sistemi
* Hata izleme mekanizması
* Audit log kayıtları
* Prompt injection saldırılarına karşı ek koruma mekanizmaları

## Sonuç

Proje; JWT tabanlı kimlik doğrulama, rol tabanlı yetkilendirme, parola hashleme, refresh token yönetimi, ortam değişkenleri kullanımı ve yapay zeka çıktı doğrulama mekanizmaları ile temel güvenlik gereksinimlerini karşılayan bir yapı sunmaktadır.
