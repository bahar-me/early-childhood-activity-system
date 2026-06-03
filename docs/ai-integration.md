# Yapay Zeka ve LLM Entegrasyonu

Bu projede yapay zeka modülü, öğretmenlerin etkinlikleri sınıf profiline ve pedagojik ihtiyaçlara göre uyarlayabilmesini desteklemek amacıyla geliştirilmiştir.

## Kullanılan Yaklaşım

Sistemde üç aşamalı bir yapay zeka akışı kullanılmaktadır:

1. **Gemini API**
2. **Ollama Local LLM**
3. **Mock AI Fallback**

Bu yapı sayesinde sistem hem dış API tabanlı LLM servislerini hem de local çalışan bir LLM modelini desteklemektedir.

## Gemini API Kullanımı

Gemini API, öğretmenin yazdığı uyarlama isteğine göre mevcut etkinliği yeniden düzenlemek için kullanılmaktadır. Modelden dönen cevap JSON formatında alınır ve etkinlik taslağı olarak frontend tarafına gönderilir.

Üretilen alanlar:

* Başlık
* Açıklama
* Materyaller
* Uygulama adımları
* Öğrenme hedefleri
* Değerlendirme soruları
* Farklılaştırma önerisi
* Aile / toplum katılımı önerisi
* Öğrenme çıktısı özeti

## Local LLM / Ollama Kullanımı

Dış API servisinin kullanılamadığı durumlarda sistem, Ollama üzerinden local çalışan LLM modeline geçer. Bu projede local model olarak `llama3.2` kullanılmıştır.

Local LLM desteği sayesinde sistem internet bağlantısına veya dış servis erişimine tamamen bağımlı olmadan da yapay zeka destekli etkinlik uyarlama işlemi gerçekleştirebilir.

## Fallback Yapısı

Sistemin yapay zeka akışı şu şekildedir:

```text
Gemini API
↓ hata olursa
Ollama Local LLM
↓ hata olursa
Mock AI
```

Bu yapı uygulamanın dayanıklılığını artırır. Yapay zeka servisi çalışmasa bile sistem mock cevap üreterek temel işlevini sürdürebilir.

## Sonuç

Bu yapı sayesinde proje hem hazır LLM API kullanımını hem de local LLM kullanımını destekleyen esnek bir yapay zeka mimarisine sahiptir.
