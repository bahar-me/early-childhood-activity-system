# Yapay Zeka ve LLM Entegrasyonu

Bu projede yapay zeka modülü, okul öncesi öğretmenlerinin etkinlikleri sınıf profiline, öğrenme hedeflerine ve pedagojik ihtiyaçlara göre uyarlayabilmesini desteklemek amacıyla geliştirilmiştir.

## Yapay Zeka Mimarisi

Sistem, çok katmanlı bir yapay zeka mimarisi kullanmaktadır. Bu mimari sayesinde farklı yapay zeka kaynakları arasında geçiş yapılabilmekte ve sistem sürekliliği sağlanmaktadır.

Kullanılan yapay zeka katmanları şunlardır:

1. Gemini API
2. Ollama Local LLM
3. Mock AI Fallback

Bu yaklaşım sayesinde sistem hem bulut tabanlı büyük dil modellerini hem de yerel olarak çalışan yapay zeka modellerini desteklemektedir.

## Gemini API Entegrasyonu

Gemini API, öğretmenin etkinlik uyarlama isteğini işlemek için kullanılan birincil yapay zeka servisidir. Öğretmenin girdiği uyarlama talebi ve mevcut etkinlik bilgileri modele gönderilir.

Model tarafından üretilen cevap yapılandırılmış JSON formatında alınır ve frontend tarafına aktarılır.

Yapay zeka tarafından oluşturulan içerikler şunlardır:

* Etkinlik başlığı
* Etkinlik açıklaması
* Gerekli materyaller
* Uygulama adımları
* Öğrenme hedefleri
* Değerlendirme soruları
* Farklılaştırma önerileri
* Aile ve toplum katılımı önerileri
* Öğrenme çıktısı özeti

Bu yapı sayesinde öğretmenler mevcut etkinlikleri farklı yaş gruplarına, öğrenme ihtiyaçlarına ve sınıf koşullarına göre hızlı bir şekilde uyarlayabilmektedir.

## Ollama Local LLM Entegrasyonu

Gemini API servisinin kullanılamadığı durumlarda sistem otomatik olarak Ollama üzerinden çalışan yerel büyük dil modeline geçiş yapmaktadır.

Bu projede yerel model olarak:

```text
llama3.2
```

kullanılmıştır.

Yerel model desteği sayesinde sistem internet bağlantısına veya harici yapay zeka servislerine tamamen bağımlı olmadan çalışabilmektedir.

Bu yaklaşım aynı zamanda veri gizliliği ve sistem sürekliliği açısından da avantaj sağlamaktadır.

## Fallback Mekanizması

Sistemin yapay zeka akışı aşağıdaki şekilde tasarlanmıştır:

```text
Gemini API
      |
      v
Başarısız olursa
      |
      v
Ollama Local LLM
      |
      v
Başarısız olursa
      |
      v
Mock AI Fallback
```

Bu yapı sayesinde herhangi bir yapay zeka servisinde hata oluşması durumunda sistem tamamen durmamakta ve alternatif katmana geçerek hizmet vermeye devam etmektedir.

## Kullanılan Teknolojiler

* Google Gemini API
* Ollama
* Llama 3.2
* Flask REST API
* JSON Tabanlı Veri Aktarımı

## Sonuç

Geliştirilen yapay zeka mimarisi, bulut tabanlı ve yerel büyük dil modellerini birlikte kullanabilen esnek bir yapı sunmaktadır. Çok katmanlı fallback mekanizması sayesinde sistem dayanıklılığı artırılmış ve yapay zeka servislerinde oluşabilecek kesintilerin kullanıcı deneyimini olumsuz etkilemesi engellenmiştir.

Bu yapı, okul öncesi eğitim alanında etkinlik uyarlama süreçlerini hızlandırmakta ve öğretmenlere yapay zeka destekli karar desteği sağlamaktadır.
