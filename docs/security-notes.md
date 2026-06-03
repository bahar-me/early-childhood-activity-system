# Güvenlik Notları

Bu projede kullanıcı girişleri, yetkilendirme ve API erişimi güvenli olacak şekilde tasarlanmıştır.

## Kimlik Doğrulama

Kullanıcı girişi JWT tabanlı kimlik doğrulama ile yapılmaktadır. Giriş başarılı olduğunda kullanıcıya access token ve refresh token verilir.

## Yetkilendirme

Sistemde rol tabanlı yetkilendirme bulunmaktadır.

Roller:

* System Admin
* School Admin
* Teacher

Her kullanıcı yalnızca kendi rolüne uygun işlemleri yapabilir. Örneğin öğretmen rolündeki kullanıcı okul oluşturma, güncelleme veya silme işlemlerini yapamaz.

## Parola Güvenliği

Kullanıcı parolaları düz metin olarak saklanmaz. Parolalar hashlenerek veritabanına kaydedilir.

## API Güvenliği

Korunan endpointlerde JWT kontrolü yapılmaktadır. Yetkisiz veya token olmadan yapılan istekler reddedilir.

## Ortam Değişkenleri

Gizli bilgiler `.env` dosyasında tutulur. API anahtarları ve yapılandırma bilgileri doğrudan kod içine yazılmaz.

Örnek:

```env
GEMINI_API_KEY=...
OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

## Yapay Zeka Güvenliği

LLM çıktıları doğrudan sisteme kontrolsüz şekilde alınmaz. Modelden beklenen çıktı JSON formatında tanımlanır. Ayrıca enum alanları ve zorunlu alanlar kontrol edilerek sistemin bozulması engellenir.

## Gelecek Güvenlik Geliştirmeleri

* HTTPS kullanımı
* Rate limiting
* API key erişim kontrolü
* Daha ayrıntılı input validation
* Loglama ve hata izleme
* Prompt injection riskine karşı ek kontroller
