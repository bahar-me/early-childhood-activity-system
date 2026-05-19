import json

from backend.app import create_app
from backend.extensions import db
from backend.models.activity import Activity


ACTIVITIES = [
    {
        "title": "Gökkuşağı ile Sayma",
        "subject": "Math",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Renkli nesneler ve gruplama çalışmalarıyla 1-10 arası sayıları öğrenme etkinliği.",
        "materials": ["Renkli ponponlar veya bloklar", "Sayı kartları", "Sınıflandırma kapları"],
        "instructions": [
            "1-10 arasındaki sayı kartlarını sırayla göster",
            "Çocuklardan her sayı için uygun sayıda renkli nesne saymalarını iste",
            "Nesneleri renklerine göre ayırıp her grubu say",
            "Rakamları ve miktarları birlikte tanıma çalışması yap",
        ],
        "learning_goals": [
            "1-10 arası sayı tanıma",
            "Birebir eşleştirme",
            "Renkleri ayırt etme",
            "Sınıflandırma ve gruplama becerisi",
        ],
    },
    {
        "title": "Harf ve Ses Macerası",
        "subject": "Language",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Çocukların kelimelerin başlangıç seslerini ayırt ettiği etkileşimli bir ses farkındalığı oyunu.",
        "materials": ["Resim kartları", "Harf kartları", "Ses kutusu veya sepet"],
        "instructions": [
            "Bir harf göster ve çıkardığı sesi örnekle",
            "3-4 resim kartı göster",
            "Çocuklardan hangi resimlerin hedef sesle başladığını bulmalarını iste",
            "Doğru cevapları hareket ya da kısa bir şarkıyla kutla",
        ],
        "learning_goals": [
            "Ses farkındalığı",
            "Başlangıç seslerini ayırt etme",
            "Harf-ses ilişkisini kurma",
            "Kelime dağarcığını geliştirme",
        ],
    },
    {
        "title": "Doğa Kolajı Oluşturma",
        "subject": "Art",
        "duration": "30-45min",
        "group_size": "Individual",
        "description": "Dışarıdan toplanan doğal malzemelerle yaratıcı bir sanat çalışması yapma etkinliği.",
        "materials": ["Fon kartonu veya renkli kâğıt", "Yapıştırıcı", "Doğal malzemeler (yaprak, dal, çiçek)", "Keçeli kalemler"],
        "instructions": [
            "Çocuklarla kısa bir doğa yürüyüşü yaparak malzemeler topla",
            "Doğada bulunan renkler, dokular ve şekiller hakkında konuş",
            "Her çocuğa kâğıt ve yapıştırıcı ver",
            "Çocukların malzemeleri istedikleri gibi yerleştirip yapıştırmalarını sağla",
            "İsterlerse keçeli kalemlerle ek detaylar eklemelerine izin ver",
        ],
        "learning_goals": [
            "İnce motor becerileri",
            "Yaratıcı ifade",
            "Doğa farkındalığı",
            "Doku keşfi",
        ],
    },
    {
        "title": "Batar mı Yüzer mi Deneyi",
        "subject": "Science",
        "duration": "30-45min",
        "group_size": "Small Group",
        "description": "Farklı nesneleri suda test ederek batma ve yüzme kavramlarını keşfetme etkinliği.",
        "materials": ["Su masası veya büyük kap", "Çeşitli nesneler (oyuncak, mantar, taş, sünger vb.)", "Grafik kâğıdı", "Havlu"],
        "instructions": [
            "Batan ve yüzen kavramlarını tanıt",
            "Her nesneyi gösterip çocuklardan tahmin yapmalarını iste",
            "Nesneleri tek tek test edip sonucu tabloya kaydet",
            "Bazı nesnelerin neden battığı, bazılarının neden yüzdüğü hakkında konuş",
            "Çocukların materyallerle serbestçe deneme yapmalarına fırsat ver",
        ],
        "learning_goals": [
            "Bilimsel tahmin yapma",
            "Gözlem becerileri",
            "Batma-yüzme kavramını anlama",
            "Eleştirel düşünme",
        ],
    },
    {
        "title": "Müzikli Donma Oyunu",
        "subject": "Music",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Müzik çalarken dans etme, müzik durduğunda donma oyunu ile dinleme ve beden kontrolünü geliştirme etkinliği.",
        "materials": ["Müzik çalar", "Farklı şarkılar", "Geniş hareket alanı"],
        "instructions": [
            "Kuralları açıkla: müzik çalarken dans edilir, müzik durunca hareketsiz kalınır",
            "Önce daha yavaş şarkılarla alıştırma yap",
            "Daha sonra tempoyu yavaş yavaş artır",
            "Tek ayak üstünde don ya da komik bir pozisyonda don gibi küçük görevler ekle",
            "Çocukların danslarını ve donma anlarını birlikte kutla",
        ],
        "learning_goals": [
            "Dinleme becerileri",
            "Öz denetim",
            "Kaba motor kontrolü",
            "Yönergelere uyma",
        ],
    },
    {
        "title": "Engel Parkuru Macerası",
        "subject": "Physical",
        "duration": "30-45min",
        "group_size": "Whole Class",
        "description": "Eğlenceli bir engel parkurunda ilerleyerek kaba motor becerilerini geliştirme etkinliği.",
        "materials": ["Huniler", "Hula hooplar", "Tünel", "Denge tahtası veya bant çizgisi", "Fasulye torbaları"],
        "instructions": [
            "İstasyonları hazırla: hunilerin üzerinden atlama, tünelden sürünerek geçme, denge çizgisinde yürüme, halkaların içinde zıplama",
            "Her istasyonu çocuklara örnek olarak göster",
            "Çocukların parkuru tek tek ya da küçük gruplar halinde tamamlamasını sağla",
            "Her katılımcıyı motive et ve cesaretlendir",
            "İsteyen çocukların parkuru birden fazla kez denemesine fırsat ver"
        ],
        "learning_goals": [
            "Kaba motor gelişimi",
            "Denge ve koordinasyon",
            "Birden fazla adımdan oluşan yönergeleri takip etme",
            "Sıra bekleme becerisi"
        ],
    },
    {
        "title": "Duygu Yüzlerini Eşleştirme",
        "subject": "Social-Emotional",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Yüz ifadeleri kartları ve ayna kullanarak farklı duyguları tanıma ve konuşma etkinliği.",
        "materials": ["Duygu kartları veya görseller", "Ayna", "Duygularla ilgili kitaplar (isteğe bağlı)"],
        "instructions": [
            "Her duygu kartını göster ve duygunun adını söyle",
            "Çocuklardan aynaya bakarak aynı yüz ifadesini yapmalarını iste",
            "Bu duyguyu hangi durumlarda hissedebileceğimiz hakkında konuş",
            "Çocukların kendi deneyimlerinden örnekler paylaşmasına fırsat ver",
            "Duygu kartlarını eşleştirme çalışması yap"
        ],
        "learning_goals": [
            "Duygu kelime dağarcığı",
            "Öz farkındalık",
            "Empati geliştirme",
            "Sosyal beceriler"
        ],
    },
    {
        "title": "Şekil Avı",
        "subject": "Math",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Sınıf ortamında şekilleri bulup tanıma etkinliği.",
        "materials": ["Şekil kartları", "Altlık ve kâğıt", "Boya kalemleri veya keçeli kalemler"],
        "instructions": [
            "Temel şekilleri gözden geçir: daire, kare, üçgen, dikdörtgen",
            "Her çocuğa bir altlık ve kâğıt ver",
            "Sınıf içinde şekil avına çık",
            "Bulunan şekilleri çizerek ya da işaretleyerek kaydet",
            "Her şekilden kaç tane bulunduğunu birlikte say"
        ],
        "learning_goals": [
            "Şekilleri tanıma",
            "Mekânsal farkındalık",
            "Gözlem becerileri",
            "Sayma ve işaretleme becerisi"
        ],
    },
    {
        "title": "Hikâye Zamanı Tiyatrosu",
        "subject": "Language",
        "duration": "30-45min",
        "group_size": "Whole Class",
        "description": "Basit materyaller ve drama yoluyla sevilen bir hikâyeyi canlandırma etkinliği.",
        "materials": ["Hikâye kitabı", "Basit aksesuarlar veya kostümler", "Canlandırma için uygun alan"],
        "instructions": [
            "Önce hikâyeyi çocuklara sesli olarak oku",
            "Karakterler ve olay örgüsü hakkında konuş",
            "Çocuklara roller dağıt",
            "Önemli sahneleri birlikte prova et",
            "Hikâyeyi birlikte canlandır",
            "İstersen rolleri değiştirip tekrar canlandır"
        ],
        "learning_goals": [
            "Hikâyeyi anlama",
            "Konuşma ve dinleme becerileri",
            "Dramatik ifade",
            "İş birliği ve takım çalışması"
        ],
    },
    {
        "title": "Oyun Hamuru Tasarımları",
        "subject": "Art",
        "duration": "30-45min",
        "group_size": "Individual",
        "description": "Oyun hamuru ile serbest keşif yaparak ince motor becerilerini ve yaratıcılığı geliştirme etkinliği.",
        "materials": ["Oyun hamuru (farklı renklerde)", "Merdaneler", "Kurabiye kalıpları", "Plastik şekillendirme araçları", "Çalışma matları"],
        "instructions": [
            "Her çocuk için oyun hamuru ve araçların bulunduğu bireysel çalışma alanları hazırla",
            "Yuvarlama, kesme ve şekillendirme tekniklerini örnekle göster",
            "Çocukların serbestçe keşfetmesine ve üretmesine fırsat ver",
            "Yaptıkları çalışmaları sözlü olarak anlatmaları için teşvik et",
            "İstersen tamamlanan çalışmaları sergile"
        ],
        "learning_goals": [
            "İnce motor gücü",
            "El-göz koordinasyonu",
            "Yaratıcı düşünme",
            "Betimleyici dil kullanımı"
        ],
    },
    {
        "title": "Bitki Büyümesini Gözlemleme",
        "subject": "Science",
        "duration": "45-60min",
        "group_size": "Small Group",
        "description": "Tohum ekerek zaman içindeki büyümeyi gözlemleme ve değişimleri kaydetme etkinliği.",
        "materials": ["Tohumlar (özellikle fasulye uygundur)", "Şeffaf bardaklar", "Toprak", "Su", "Gözlem kâğıtları", "Boya kalemleri"],
        "instructions": [
            "Bitkilerin büyümek için nelere ihtiyaç duyduğunu konuş",
            "Şeffaf bardaklara toprak koyup tohumları ek",
            "Uygun miktarda sulama yap",
            "Bardakları güneş alan bir yere yerleştir",
            "Her hafta gözlem yapıp gördüklerini çiz",
            "Bitkinin büyümesini ölç ve karşılaştır"
        ],
        "learning_goals": [
            "Yaşam döngüsünü anlama",
            "Bilimsel gözlem becerisi",
            "Veri toplama",
            "Sorumluluk ve bakım becerisi"
        ],
    },
    {
        "title": "Ritim Kalıpları",
        "subject": "Music",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Beden perküsyonu ve basit müzik aletleriyle ritim kalıpları oluşturma ve tekrar etme etkinliği.",
        "materials": ["Basit ritim çalgıları", "Ritim kartları (isteğe bağlı)"],
        "instructions": [
            "Önce beden perküsyonu ile başla (alkış, ayak vurma, parmak şıklatma)",
            "Basit bir ritim örüntüsü göster (örneğin alkış-alkış-ayak vur)",
            "Çocuklardan ritmi tekrar etmelerini iste",
            "Daha sonra çocukların kendi ritimlerini oluşturmalarına fırsat ver",
            "Farklılık için müzik aletleri ekle",
            "Grup halinde ardışık ritim zincirleri oluştur"
        ],
        "learning_goals": [
            "Örüntü farkındalığı",
            "Ritim ve tempo duygusu",
            "İşitsel hafıza",
            "Yaratıcı ifade"
        ],
    },
    {
        "title": "Yoga ve Farkındalık",
        "subject": "Physical",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Sakinleşmeyi ve beden farkındalığını destekleyen hafif yoga hareketleri ve nefes egzersizleri etkinliği.",
        "materials": ["Yoga matları veya havlular", "Sakin müzik", "Duruş görsel kartları (isteğe bağlı)"],
        "instructions": [
            "Sakin ve rahat bir ortam oluştur",
            "Derin nefes egzersizleri ile başla",
            "Hayvan temalı duruşları tanıt (kedi, köpek, ağaç, kelebek)",
            "Her duruşu birkaç nefes süresince koru",
            "Etkinliği kısa bir gevşeme bölümüyle bitir",
            "Çocuklarla bedenlerinin nasıl hissettiği hakkında konuş"
        ],
        "learning_goals": [
            "Beden farkındalığı",
            "Esneklik ve denge",
            "Öz denetim",
            "Farkındalık uygulaması"
        ],
    },
    {
        "title": "Arkadaşlık Çemberi",
        "subject": "Social-Emotional",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Paylaşım ve güzel sözler yoluyla sınıf içi aidiyet duygusunu güçlendirme etkinliği.",
        "materials": ["Konuşma çubuğu veya bir nesne", "İsteğe bağlı: arkadaşlık temalı kitap"],
        "instructions": [
            "Çocuklarla çember şeklinde otur",
            "Konuşma nesnesini sırayla dolaştır",
            "Her çocuktan bir arkadaşı hakkında olumlu bir şey söylemesini iste",
            "Nazik sözler ve iltifat kullanımı üzerinde dur",
            "İyi bir arkadaşın hangi özelliklere sahip olabileceği hakkında konuş",
            "Etkinliği bir arkadaşlık şarkısı ya da kısa bir tezahüratla bitir"
        ],
        "learning_goals": [
            "Nezaket ve empati",
            "Konuşma ve dinleme becerileri",
            "Olumlu akran ilişkileri",
            "Özgüveni destekleme"
        ],
    },
    {
        "title": "Desen Bloklarıyla Tasarımlar",
        "subject": "Math",
        "duration": "30-45min",
        "group_size": "Individual",
        "description": "Renkli geometrik bloklarla örüntüler ve tasarımlar oluşturma etkinliği.",
        "materials": ["Desen blokları", "Tasarım kartları (isteğe bağlı)", "Kâğıt", "Kurşun kalem"],
        "instructions": [
            "Farklı blok şekillerini çocuklara tanıt",
            "Basit örüntülerin nasıl oluşturulacağını göster",
            "İsteyen çocuklar için kopyalanacak tasarım kartları ver",
            "Serbest oluşturma zamanı tanı",
            "Simetri ve örüntü tekrarına dikkat çek",
            "Çocuklardan yaptıkları tasarımları anlatmalarını iste"
        ],
        "learning_goals": [
            "Geometrik şekilleri tanıma",
            "Örüntü oluşturma",
            "Mekânsal akıl yürütme",
            "Problem çözme becerisi"
        ],
    },
    {
        "title": "Kukla Gösterisi Hazırlama",
        "subject": "Language",
        "duration": "45-60min",
        "group_size": "Small Group",
        "description": "Basit kuklalar yaparak kısa bir hikâye ya da canlandırma hazırlama etkinliği.",
        "materials": ["Kâğıt poşetler veya çoraplar", "El işi malzemeleri (kalem, kâğıt, yapıştırıcı)", "Kukla sahnesi veya masa"],
        "instructions": [
            "Kukla yapımı için gerekli malzemeleri çocuklara dağıt",
            "Çocukların kendi kuklalarını tasarlamalarına yardımcı ol",
            "Birlikte kısa hikâye fikirleri üret",
            "Kuklaları hareket ettirme ve seslendirme çalışması yap",
            "Hazırlanan gösteriyi sınıfa sun",
            "Gösteriden sonra hikâyeler hakkında konuş"
        ],
        "learning_goals": [
            "Yaratıcı hikâye anlatımı",
            "Sözlü dil gelişimi",
            "İş birliği",
            "Sunum becerileri"
        ],
    },
    {
        "title": "Renk Karıştırma Sihri",
        "subject": "Art",
        "duration": "30-45min",
        "group_size": "Small Group",
        "description": "Ana ve ara renkleri, boyaları karıştırarak keşfetme etkinliği.",
        "materials": ["Ana renk boyalar (kırmızı, sarı, mavi)", "Palet veya tabaklar", "Fırçalar", "Kâğıt", "Önlük"],
        "instructions": [
            "Önce ana renkleri gözden geçir",
            "İki rengin karıştırılmasını örnek olarak göster",
            "Hangi yeni rengin oluşacağını çocuklarla tahmin et",
            "Çocukların kendi karışımlarını denemelerine fırsat ver",
            "Karıştırdıkları renklerle resim yapmalarını sağla",
            "Bir renk karışım tablosu oluştur"
        ],
        "learning_goals": [
            "Renk bilgisi temelleri",
            "Tahmin ve gözlem becerisi",
            "İnce motor gelişimi",
            "Bilimsel süreç farkındalığı"
        ],
    },
    {
        "title": "Mıknatıs Keşfi",
        "subject": "Science",
        "duration": "30-45min",
        "group_size": "Small Group",
        "description": "Hangi nesnelerin mıknatıs tarafından çekildiğini keşfetme etkinliği.",
        "materials": ["Mıknatıslar", "Çeşitli nesneler (metal, plastik, tahta, kâğıt)", "Ayırma matı", "Kayıt kâğıdı"],
        "instructions": [
            "Mıknatıs ve manyetizma kavramını tanıt",
            "Bir nesneyi nasıl test edeceğini örnekle göster",
            "Çocuklardan hangi nesnelerin mıknatısa tepki vereceğini tahmin etmelerini iste",
            "Nesneleri tek tek test et",
            "Nesneleri mıknatısa yapışanlar ve yapışmayanlar olarak ayır",
            "Sonuçları birlikte kaydet"
        ],
        "learning_goals": [
            "Bilimsel sorgulama",
            "Maddelerin özelliklerini tanıma",
            "Tahmin etme ve test etme",
            "Sınıflandırma becerileri"
        ],
    },
    {
        "title": "Çalgı Geçidi",
        "subject": "Music",
        "duration": "30-45min",
        "group_size": "Whole Class",
        "description": "Farklı ritim çalgılarıyla yürüyerek müzik ve hareketi birleştirme etkinliği.",
        "materials": ["Çeşitli ritim çalgıları", "Yürüyüş müziği", "Hareket etmek için uygun alan"],
        "instructions": [
            "Her çalgıyı tanıt ve çıkardığı sesi dinlet",
            "Birlikte çalma denemesi yap",
            "Çocuklarla bir geçit sırası oluştur",
            "Müzik eşliğinde yürüyerek çalgıları çal",
            "Farklı tempolar dene (yavaş, hızlı)",
            "Çalgıları değiştirerek etkinliği tekrar et"
        ],
        "learning_goals": [
            "Ritim ve tempo farkındalığı",
            "Çalgıları tanıma",
            "Koordinasyon",
            "Müzikal ifade"
        ],
    },
    {
        "title": "Denge Becerisi Oyunu",
        "subject": "Physical",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Farklı eğlenceli görevlerle denge becerisini geliştirme etkinliği.",
        "materials": ["Denge tahtası veya bant çizgisi", "Fasulye torbaları", "Yastıklar veya yer işaretleri", "Zamanlayıcı (isteğe bağlı)"],
        "instructions": [
            "Basit denge duruşlarıyla ısınma yap",
            "Denge çizgisinde öne ve arkaya doğru yürü",
            "Başının üzerinde fasulye torbasıyla yürümeyi dene",
            "Tek ayak üstünde durup say",
            "Çocukların kendi denge görevlerini oluşturmalarına fırsat ver",
            "Birbirlerini destekleyip motive etmelerini teşvik et"
        ],
        "learning_goals": [
            "Denge ve vücut kontrolü",
            "Merkez kas gücü",
            "Odaklanma ve dikkat",
            "Beden farkındalığı"
        ],
    },
    {
        "title": "Sayı Treni",
        "subject": "Math",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Vagonlara sayı kartları yerleştirerek sayı sıralamasını öğrenme etkinliği.",
        "materials": ["Karton tren vagonları", "Sayı kartları", "Mandallar veya yapıştırıcı", "Renkli kalemler"],
        "instructions": [
            "Tren vagonlarını sırayla çocukların önüne yerleştir",
            "Sayı kartlarını karışık şekilde göster",
            "Çocuklardan kartları doğru sırayla vagonlara yerleştirmelerini iste",
            "Tren tamamlandıktan sonra sayıları birlikte tekrar et",
            "İstersen bazı kartları çıkarıp eksik sayıyı bulma çalışması yap"
        ],
        "learning_goals": [
            "Sayı sıralaması",
            "1-10 arası sayı tanıma",
            "Dikkat ve odaklanma",
            "Görsel sıralama becerisi"
        ],
    },
    {
        "title": "Eksik Sayıyı Bul",
        "subject": "Math",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Sayı dizilerinde eksik bırakılan rakamları bulma etkinliği.",
        "materials": ["Sayı kartları", "Kâğıt şeritler", "Kalem", "Mıknatıs veya yapıştırıcı"],
        "instructions": [
            "Sayı dizilerini sırayla hazırla",
            "Bazı sayıları eksik bırak",
            "Çocuklardan eksik sayıyı tahmin etmelerini iste",
            "Doğru kartı yerine yerleştirerek kontrol et",
            "Farklı sayı dizileriyle çalışmayı tekrar et"
        ],
        "learning_goals": [
            "Sayı dizisini anlama",
            "Eksik öğeyi bulma",
            "Mantıksal düşünme",
            "Sayı farkındalığı"
        ],
    },
    {
        "title": "Büyük mü Küçük mü",
        "subject": "Math",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Nesneleri boyutlarına göre karşılaştırma ve sınıflandırma etkinliği.",
        "materials": ["Farklı boyutlarda bloklar", "Karşılaştırma kartları", "Sepetler veya kutular"],
        "instructions": [
            "Farklı boyutlardaki nesneleri çocuklara göster",
            "Büyük ve küçük kavramlarını örnekle açıkla",
            "Çocuklardan nesneleri boyutlarına göre ayırmalarını iste",
            "Birlikte hangi nesnenin daha büyük ya da daha küçük olduğunu konuş",
            "İstersen orta boy nesneleri de ekleyerek etkinliği genişlet"
        ],
        "learning_goals": [
            "Büyük-küçük kavramı",
            "Karşılaştırma becerisi",
            "Sınıflandırma",
            "Matematiksel dil kullanımı"
        ],
    },
    {
        "title": "Desen Tamamlama Kartları",
        "subject": "Math",
        "duration": "15-30min",
        "group_size": "Individual",
        "description": "Renk ve şekil örüntülerini fark ederek eksik bölümleri tamamlama etkinliği.",
        "materials": ["Desen kartları", "Renkli çıkartmalar veya şekiller", "Kalem"],
        "instructions": [
            "Basit örüntü kartlarını çocuklara göster",
            "Desenin nasıl tekrar ettiğini birlikte incele",
            "Eksik bırakılan kısmı bulmalarını iste",
            "Uygun renk veya şekille deseni tamamlat",
            "Daha sonra çocukların kendi desenlerini oluşturmalarına fırsat ver"
        ],
        "learning_goals": [
            "Örüntü farkındalığı",
            "Görsel dikkat",
            "Tahmin becerisi",
            "Matematiksel düşünme"
        ],
    },
    {
        "title": "Nesne Say ve Eşleştir",
        "subject": "Math",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Nesne gruplarını sayarak doğru sayı kartıyla eşleştirme etkinliği.",
        "materials": ["Küçük oyuncaklar veya düğmeler", "Sayı kartları", "Tepsi veya masa alanı"],
        "instructions": [
            "Masaya farklı miktarlarda nesne grupları yerleştir",
            "Her grup için çocukların nesneleri saymasını iste",
            "Doğru sayı kartını bulup yanına koymalarını sağla",
            "Sayma işlemini birlikte kontrol et",
            "Farklı nesnelerle etkinliği tekrarla"
        ],
        "learning_goals": [
            "Sayma becerisi",
            "Birebir eşleştirme",
            "Sayı-sembol ilişkisi",
            "Dikkat geliştirme"
        ],
    },
    {
        "title": "Şekil Yolculuğu",
        "subject": "Math",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Belirli şekilleri takip ederek sınıf içinde hareket etme etkinliği.",
        "materials": ["Yere yapıştırılacak şekil kartları", "Şekil afişleri", "Müzik (isteğe bağlı)"],
        "instructions": [
            "Sınıf zeminine farklı şekiller yerleştir",
            "Her şeklin adını birlikte tekrar et",
            "Çocuklardan öğretmenin söylediği şeklin üzerine gitmelerini iste",
            "Doğru şekle gelen çocuklarla şeklin özelliklerini konuş",
            "İstersen müzikle hareket ekleyerek oyunu eğlenceli hale getir"
        ],
        "learning_goals": [
            "Şekil tanıma",
            "Mekansal farkındalık",
            "Dinleme becerisi",
            "Hareketle öğrenme"
        ],
    },
    {
        "title": "Sayı Kulesi Yapımı",
        "subject": "Math",
        "duration": "15-30min",
        "group_size": "Individual",
        "description": "Verilen sayı kadar blok kullanarak kule oluşturma etkinliği.",
        "materials": ["Bloklar veya legolar", "Sayı kartları", "Çalışma alanı"],
        "instructions": [
            "Her çocuğa bloklar ve sayı kartları ver",
            "Bir sayı kartı seçmelerini iste",
            "Kartta yazan sayı kadar blokla kule kurmalarını söyle",
            "Kuleleri birlikte sayarak kontrol et",
            "Daha sonra en yüksek ve en alçak kuleleri karşılaştır"
        ],
        "learning_goals": [
            "Sayı miktar ilişkisi",
            "İnce motor becerisi",
            "Karşılaştırma",
            "Planlama ve dikkat"
        ],
    },
    {
        "title": "Renkli Boncuk Sıralama",
        "subject": "Math",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Boncukları renklerine ve sayılarına göre sıralama etkinliği.",
        "materials": ["Renkli boncuklar veya düğmeler", "Kaplar", "Maşa veya kaşık", "Renk kartları"],
        "instructions": [
            "Boncukları karışık şekilde ortaya koy",
            "Renk kartlarını çocuklara göster",
            "Boncukları renklerine göre ayırmalarını iste",
            "Her kaptaki boncukları birlikte say",
            "Hangi renkten daha fazla veya daha az olduğunu konuş"
        ],
        "learning_goals": [
            "Renk sınıflandırma",
            "Sayma becerisi",
            "Karşılaştırma yapma",
            "İnce motor gelişimi"
        ],
    },
    {
        "title": "Takvimde Sayılar",
        "subject": "Math",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Takvim üzerinden gün numaralarını tanıma ve sıralama etkinliği.",
        "materials": ["Sınıf takvimi", "Sayı kartları", "Mıknatıslı tahtası veya pano"],
        "instructions": [
            "Takvimi çocuklarla birlikte incele",
            "Bugünün tarihini göster",
            "Önceki ve sonraki günü bulmalarını iste",
            "Sayıların sırayla nasıl ilerlediğini konuş",
            "Bazı günleri kapatıp eksik sayıları tahmin etmelerini iste"
        ],
        "learning_goals": [
            "Sayı sıralaması",
            "Gün ve tarih farkındalığı",
            "Tahmin etme",
            "Dikkat geliştirme"
        ],
    },
    {
        "title": "Kaç Adım Uzaklıkta",
        "subject": "Math",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Sınıf içindeki nesnelere kaç adımda ulaşıldığını ölçme etkinliği.",
        "materials": ["Sınıf içi hedef nesneler", "Kâğıt", "Kalem", "Ölçüm çizelgesi"],
        "instructions": [
            "Sınıfta hedef olarak birkaç nesne seç",
            "Çocuklardan başlangıç noktasından hedefe kadar adım saymalarını iste",
            "Her denemede adım sayılarını kaydet",
            "Hangi nesnenin daha yakın ya da daha uzak olduğunu konuş",
            "Sonuçları birlikte karşılaştır"
        ],
        "learning_goals": [
            "Standart olmayan ölçme",
            "Sayma becerisi",
            "Karşılaştırma yapma",
            "Mekansal farkındalık"
        ],
    },
    {
        "title": "Kafiye Avı",
        "subject": "Language",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Benzer sesle biten kelimeleri bulup eşleştirme etkinliği.",
        "materials": ["Resim kartları", "Kafiye eşleştirme kartları", "Sepet veya masa alanı"],
        "instructions": [
            "Çocuklara iki örnek kelime söyleyerek kafiye kavramını tanıt",
            "Resim kartlarını sırayla göster",
            "Benzer sesle biten kelimeleri birlikte bul",
            "Kartları eşleştirmelerini iste",
            "İstersen çocukların yeni kafiyeli kelimeler söylemesine fırsat ver"
        ],
        "learning_goals": [
            "Ses farkındalığı",
            "Kafiye tanıma",
            "Dinleme becerisi",
            "Kelime dağarcığını geliştirme"
        ],
    },
    {
        "title": "Resimden Hikaye Kur",
        "subject": "Language",
        "duration": "30-45min",
        "group_size": "Whole Class",
        "description": "Görsellerden yola çıkarak basit hikayeler oluşturma etkinliği.",
        "materials": ["Resim kartları", "Büyük hikaye kağıdı", "Kalemler"],
        "instructions": [
            "Çocuklara birkaç resim kartı göster",
            "Görsellerde neler olduğunu birlikte konuş",
            "Resimlere göre bir hikaye başlangıcı oluştur",
            "Çocukların sırayla hikayeye cümle eklemesini iste",
            "Hikayeyi birlikte tamamlayıp tekrar anlat"
        ],
        "learning_goals": [
            "Sözlü anlatım becerisi",
            "Sıralı düşünme",
            "Hayal gücü kullanımı",
            "Dinleme ve konuşma"
        ],
    },
    {
        "title": "Ses Kutusunu Bul",
        "subject": "Language",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Belirli bir sesle başlayan nesneleri bulma ve ayırt etme etkinliği.",
        "materials": ["Ses kutuları veya sepetler", "Küçük nesneler/resimler", "Harf kartları"],
        "instructions": [
            "Bir hedef sesi seç ve harf kartıyla göster",
            "Çeşitli nesneleri veya resimleri çocukların önüne yerleştir",
            "Hedef sesle başlayanları bulmalarını iste",
            "Doğru nesneleri ilgili kutuya koy",
            "Sonunda nesneleri tekrar birlikte adlandır"
        ],
        "learning_goals": [
            "Başlangıç sesini ayırt etme",
            "Harf-ses ilişkisi",
            "Kelime farkındalığı",
            "Dikkat becerisi"
        ],
    },
    {
        "title": "Hikaye Sıralama Kartları",
        "subject": "Language",
        "duration": "15-30min",
        "group_size": "Individual",
        "description": "Olay kartlarını doğru sıraya dizerek hikaye akışını anlama etkinliği.",
        "materials": ["Sıralama kartları", "Masa veya pano", "Yapıştırıcı (isteğe bağlı)"],
        "instructions": [
            "Çocuklara karışık olay kartlarını göster",
            "Kartlarda neler olduğunu birlikte incele",
            "Olayların önce-sonra ilişkisini konuş",
            "Kartları doğru sıraya dizmelerini iste",
            "Sıralanan kartlara göre hikayeyi anlattır"
        ],
        "learning_goals": [
            "Olay sıralama becerisi",
            "Hikaye anlama",
            "Mantıksal düşünme",
            "Sözlü ifade"
        ],
    },
    {
        "title": "Kelime Sepeti",
        "subject": "Language",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Belirli bir tema ile ilgili kelimeler üretme ve paylaşma etkinliği.",
        "materials": ["Sepet veya kutu", "Tema kartları", "Resimler"],
        "instructions": [
            "Bir tema seç (örneğin hayvanlar, yiyecekler, oyuncaklar)",
            "Tema kartını çocuklara göster",
            "Sırayla herkesin bu temaya ait bir kelime söylemesini iste",
            "Söylenen kelimeleri tekrar ederek pekiştir",
            "İstersen kelimeleri resimlerle eşleştir"
        ],
        "learning_goals": [
            "Kelime dağarcığını geliştirme",
            "Tematik kavram öğrenimi",
            "Sıra alma becerisi",
            "Sözlü ifade"
        ],
    },
    {
        "title": "Kim Konuşuyor",
        "subject": "Language",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Sesleri dinleyerek konuşan kişiyi veya nesneyi tahmin etme etkinliği.",
        "materials": ["Perde veya ayırıcı alan", "Basit nesneler", "Ses çıkarabilecek materyaller"],
        "instructions": [
            "Çocuklardan gözlerini kapatmalarını ya da perdeye bakmalarını iste",
            "Bir ses çıkar ya da kısa bir kelime söyle",
            "Çocuklardan sesin kimden veya nereden geldiğini tahmin etmelerini iste",
            "Doğru cevabı birlikte kontrol et",
            "Farklı seslerle oyunu sürdür"
        ],
        "learning_goals": [
            "İşitsel ayırt etme",
            "Dinleme becerisi",
            "Dikkat toplama",
            "Dil farkındalığı"
        ],
    },
    {
        "title": "Cümleyi Tamamla",
        "subject": "Language",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Yarım bırakılan cümleleri anlamlı şekilde tamamlama etkinliği.",
        "materials": ["Cümle kartları", "Resim destek kartları", "Tahta veya pano"],
        "instructions": [
            "Basit yarım cümleler hazırla",
            "Her cümleyi çocuklara sırayla oku",
            "Cümlenin sonunu nasıl tamamlayabileceklerini düşünmelerini iste",
            "Farklı cevapları birlikte paylaş",
            "En uygun tamamlamayı tekrar et"
        ],
        "learning_goals": [
            "Cümle kurma becerisi",
            "Anlamlı ifade geliştirme",
            "Dinleme ve düşünme",
            "Kelime seçimi"
        ],
    },
    {
        "title": "Rol Kartları ile Konuşma",
        "subject": "Language",
        "duration": "30-45min",
        "group_size": "Small Group",
        "description": "Farklı karakter kartlarıyla kısa konuşmalar ve canlandırmalar yapma etkinliği.",
        "materials": ["Karakter kartları", "Basit aksesuarlar", "Oyun alanı"],
        "instructions": [
            "Çocuklara farklı karakter kartları dağıt",
            "Her karakterin kim olabileceği hakkında konuş",
            "İkili veya küçük grup konuşmaları oluştur",
            "Kısa canlandırmalar yapmalarını teşvik et",
            "Etkinlik sonunda karakterler hakkında sohbet et"
        ],
        "learning_goals": [
            "Sözlü iletişim",
            "Rol alma becerisi",
            "Yaratıcı düşünme",
            "Karşılıklı konuşma becerisi"
        ],
    },
    {
        "title": "Resimli Kelime Eşleştirme",
        "subject": "Language",
        "duration": "15-30min",
        "group_size": "Individual",
        "description": "Resimleri doğru kelimelerle eşleştirme etkinliği.",
        "materials": ["Resim kartları", "Kelime kartları", "Cırt cırtlı pano veya masa"],
        "instructions": [
            "Çocuklara resim ve kelime kartlarını göster",
            "Resimde ne gördüklerini söylemelerini iste",
            "Doğru kelime kartını seçip resimle eşleştirmelerini sağla",
            "Eşleştirmeleri birlikte kontrol et",
            "Kartları değiştirerek tekrar deneme yap"
        ],
        "learning_goals": [
            "Kelime tanıma",
            "Görsel-sözel eşleştirme",
            "Kelime dağarcığı geliştirme",
            "Dikkat becerisi"
        ],
    },
    {
        "title": "Günün Kelimesi",
        "subject": "Language",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Seçilen yeni bir kelimeyi gün boyunca kullanarak pekiştirme etkinliği.",
        "materials": ["Kelime kartı", "Resim desteği", "Pano veya tahta"],
        "instructions": [
            "Günün yeni kelimesini çocuklara tanıt",
            "Kelimenin anlamını basit örneklerle açıkla",
            "Kelimeyi cümle içinde kullan",
            "Çocuklardan gün içinde kelimeyi tekrar etmelerini iste",
            "Etkinlik sonunda kelimeyi kimlerin kullandığını birlikte hatırla"
        ],
        "learning_goals": [
            "Yeni kelime öğrenme",
            "Kelimeyi bağlam içinde kullanma",
            "Sözlü ifade becerisi",
            "Dil gelişimini destekleme"
        ],
    },
    {
        "title": "Parmak Boyası Bahçesi",
        "subject": "Art",
        "duration": "30-45min",
        "group_size": "Small Group",
        "description": "Parmak boyası kullanarak çiçekler ve bahçe görüntüleri oluşturma etkinliği.",
        "materials": ["Parmak boyası", "Büyük kâğıtlar", "Önlük", "Islak mendil"],
        "instructions": [
            "Çocuklara parmak boyalarını ve renkleri tanıt",
            "Kağıt üzerine çiçek, yaprak ve güneş gibi basit örnekler göster",
            "Çocukların parmaklarıyla serbest şekilde boyama yapmalarına fırsat ver",
            "Renkleri karıştırarak yeni görüntüler oluşturmalarını teşvik et",
            "Etkinlik sonunda resimler hakkında konuş"
        ],
        "learning_goals": [
            "Yaratıcı ifade",
            "Renk farkındalığı",
            "Duyu temelli keşif",
            "İnce motor kontrolü"
        ],
    },
    {
        "title": "Yaprak Baskısı",
        "subject": "Art",
        "duration": "30-45min",
        "group_size": "Individual",
        "description": "Doğadan toplanan yapraklarla baskı yaparak desen oluşturma etkinliği.",
        "materials": ["Yapraklar", "Boya", "Fırça", "Kağıt", "Önlük"],
        "instructions": [
            "Farklı şekil ve boyutlardaki yaprakları çocuklara göster",
            "Yaprakların bir yüzüne boya sür",
            "Boyalı yüzeyi kağıda bastır",
            "Farklı yapraklarla tekrar ederek desenler oluştur",
            "Oluşan izleri birlikte incele ve karşılaştır"
        ],
        "learning_goals": [
            "Doğal materyallerle sanat çalışması yapma",
            "Desen farkındalığı",
            "Gözlem becerisi",
            "Yaratıcılık"
        ],
    },
    {
        "title": "Kağıt Tabak Maskeleri",
        "subject": "Art",
        "duration": "30-45min",
        "group_size": "Small Group",
        "description": "Kağıt tabakları süsleyerek maskeler tasarlama etkinliği.",
        "materials": ["Kağıt tabaklar", "Makas", "Yapıştırıcı", "Keçeli kalemler", "Renkli kağıtlar", "Lastik ip"],
        "instructions": [
            "Kağıt tabakların göz kısmını öğretmen rehberliğinde hazırla",
            "Çocukların maskelerini istedikleri gibi süslemelerini sağla",
            "Renkli kağıtlarla saç, kulak veya farklı detaylar ekle",
            "Maskelerin kenarlarına lastik ip tak",
            "Tamamlanan maskelerle kısa bir tanıtım yap"
        ],
        "learning_goals": [
            "Yaratıcı tasarım",
            "İnce motor becerileri",
            "Parça-bütün ilişkisi kurma",
            "Kendini ifade etme"
        ],
    },
    {
        "title": "Pamukla Bulut Resmi",
        "subject": "Art",
        "duration": "15-30min",
        "group_size": "Individual",
        "description": "Pamuk kullanarak gökyüzü ve bulut temalı resim yapma etkinliği.",
        "materials": ["Mavi fon kağıdı", "Pamuk", "Yapıştırıcı", "Boya kalemleri"],
        "instructions": [
            "Çocuklarla gökyüzü ve bulutlar hakkında kısa bir sohbet et",
            "Pamuk parçalarını küçük parçalara ayır",
            "Pamukları kağıda yapıştırarak bulut şekilleri oluştur",
            "İsteyen çocukların güneş, kuş veya yağmur gibi ek detaylar çizmesine izin ver",
            "Çalışmaları birlikte incele"
        ],
        "learning_goals": [
            "Malzeme kullanımı becerisi",
            "Hayal gücü",
            "Görsel düzenleme",
            "İnce motor gelişimi"
        ],
    },
    {
        "title": "Geri Dönüşüm Heykelleri",
        "subject": "Art",
        "duration": "30-45min",
        "group_size": "Small Group",
        "description": "Atık materyallerle üç boyutlu sanat çalışmaları oluşturma etkinliği.",
        "materials": ["Kart kutular", "Plastik kapaklar", "Rulo kartonlar", "Yapıştırıcı", "Bant", "Boya kalemleri"],
        "instructions": [
            "Farklı geri dönüşüm materyallerini çocuklara tanıt",
            "Bu malzemelerle neler yapılabileceği hakkında fikir üret",
            "Çocukların kendi heykel veya model tasarımlarını oluşturmalarına fırsat ver",
            "Parçaları yapıştırarak bir araya getirmelerini sağla",
            "Etkinlik sonunda herkes yaptığı çalışmayı anlatsın"
        ],
        "learning_goals": [
            "Üç boyutlu düşünme",
            "Yaratıcılık",
            "Geri dönüşüm farkındalığı",
            "Problem çözme becerisi"
        ],
    },
    {
        "title": "Sünger Baskı Desenleri",
        "subject": "Art",
        "duration": "30-45min",
        "group_size": "Small Group",
        "description": "Sünger baskı tekniğiyle tekrar eden desenler oluşturma etkinliği.",
        "materials": ["Şekilli süngerler", "Boya", "Kağıt", "Önlük", "Tepsi"],
        "instructions": [
            "Süngerlerin farklı şekillerini çocuklara göster",
            "Süngeri boyaya batırıp kağıda nasıl bastıracağını örnekle",
            "Çocukların tekrar eden baskılarla desen oluşturmalarını sağla",
            "Farklı renkleri kullanarak çalışmayı zenginleştir",
            "Desenleri birlikte inceleyip benzerlikleri konuş"
        ],
        "learning_goals": [
            "Desen oluşturma",
            "Renk kullanımı",
            "Tekrar eden yapı farkındalığı",
            "El-göz koordinasyonu"
        ],
    },
    {
        "title": "Duygu Renkleri Posteri",
        "subject": "Art",
        "duration": "30-45min",
        "group_size": "Whole Class",
        "description": "Duyguları renklerle ilişkilendirerek ortak bir poster hazırlama etkinliği.",
        "materials": ["Büyük poster kağıdı", "Boyalar veya keçeli kalemler", "Duygu kartları"],
        "instructions": [
            "Farklı duygu kartlarını çocuklarla incele",
            "Her duygu için hangi rengin uygun olabileceğini konuş",
            "Posteri bölümlere ayır",
            "Çocukların seçtikleri duyguyu ilgili renkle ifade etmelerini sağla",
            "Etkinlik sonunda poster üzerine birlikte sohbet et"
        ],
        "learning_goals": [
            "Duyguları ifade etme",
            "Renk-duygu ilişkisi kurma",
            "Grup çalışması", 
            "Yaratıcı anlatım"
        ],
    },
    {
        "title": "Kolaj Şehir Manzarası",
        "subject": "Art",
        "duration": "30-45min",
        "group_size": "Small Group",
        "description": "Kesme ve yapıştırma tekniğiyle şehir manzarası oluşturma etkinliği.",
        "materials": ["Renkli kağıtlar", "Makas", "Yapıştırıcı", "Fon kartonu", "Keçeli kalemler"],
        "instructions": [
            "Şehirde gördüğümüz binalar ve yollar hakkında konuş",
            "Renkli kağıtlardan dikdörtgen, kare ve üçgen şekiller kes",
            "Bu şekilleri kullanarak binalar ve yollar oluştur",
            "İstersen pencere, araba, ağaç gibi detaylar ekle",
            "Tamamlanan şehir manzaralarını birlikte incele"
        ],
        "learning_goals": [
            "Kesme-yapıştırma becerisi",
            "Mekansal düzenleme",
            "Şekilleri kullanma",
            "Yaratıcı tasarım"
        ],
    },
    {
        "title": "Hayalimdeki Şapka",
        "subject": "Art",
        "duration": "30-45min",
        "group_size": "Individual",
        "description": "Karton ve süsleme malzemeleriyle özgün bir şapka tasarlama etkinliği.",
        "materials": ["Karton şeritler", "Renkli kağıtlar", "Çıkartmalar", "Yapıştırıcı", "Zımba veya bant"],
        "instructions": [
            "Şapkanın temel kısmını öğretmen desteğiyle hazırla",
            "Çocuklardan şapkalarını istedikleri gibi süslemelerini iste",
            "Renkli kağıt, çıkartma ve şekiller eklemelerine fırsat ver",
            "Hazırlanan şapkaları sırayla takıp tanıtmalarını sağla",
            "Etkinlik sonunda küçük bir şapka yürüyüşü yap"
        ],
        "learning_goals": [
            "Tasarım becerisi",
            "Kendini ifade etme",
            "İnce motor gelişimi",
            "Yaratıcılık"
        ],
    },
    {
        "title": "Mozaik Kağıt Resmi",
        "subject": "Art",
        "duration": "30-45min",
        "group_size": "Individual",
        "description": "Küçük kağıt parçalarıyla mozaik görünümünde resim oluşturma etkinliği.",
        "materials": ["Renkli kağıt parçaları", "Yapıştırıcı", "Fon kartonu", "Kurşun kalem"],
        "instructions": [
            "Önce basit bir şekil veya resim çiz",
            "Renkli kağıtları küçük parçalara ayır",
            "Parçaları çizimin içine yapıştırarak doldur",
            "Farklı renklerle mozaik görüntüsü oluştur",
            "Tamamlanan çalışmaları sergile"
        ],
        "learning_goals": [
            "Parça-bütün ilişkisi kurma",
            "Dikkat ve sabır",
            "Renk uyumu oluşturma",
            "İnce motor becerileri"
        ],
    },
    {
        "title": "Gölge Avcıları",
        "subject": "Science",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Işık ve gölge ilişkisini keşfetmeye yönelik gözlem etkinliği.",
        "materials": ["El feneri", "Küçük oyuncaklar", "Beyaz duvar veya büyük kağıt", "Karartılabilir alan"],
        "instructions": [
            "Çocuklara ışık kaynağını ve nesneleri göster",
            "El fenerini nesnelere tutarak gölgeleri incele",
            "Nesne yaklaştıkça ve uzaklaştıkça gölgenin nasıl değiştiğini gözlemle",
            "Çocukların farklı nesnelerle denemeler yapmasına fırsat ver",
            "Hangi gölgenin büyük, küçük ya da uzun olduğunu birlikte konuş"
        ],
        "learning_goals": [
            "Işık ve gölge ilişkisini fark etme",
            "Gözlem yapma",
            "Karşılaştırma becerisi",
            "Bilimsel merak geliştirme"
        ],
    },
    {
        "title": "Suyun Yolculuğu",
        "subject": "Science",
        "duration": "30-45min",
        "group_size": "Small Group",
        "description": "Suyun farklı yüzeylerde nasıl aktığını keşfetme etkinliği.",
        "materials": ["Su", "Plastik tepsi", "Eğimli yüzeyler", "Sünger", "Küçük kaplar"],
        "instructions": [
            "Çocuklara suyu farklı yüzeylere dökerek örnek göster",
            "Suyun düz ve eğimli yüzeyde nasıl hareket ettiğini incele",
            "Süngerin suyu nasıl çektiğini gözlemle",
            "Çocukların kendi tahminlerini söylemelerini iste",
            "Hangi yüzeyde suyun daha hızlı veya yavaş aktığını birlikte konuş"
        ],
        "learning_goals": [
            "Su hareketini gözlemleme",
            "Tahmin yapma",
            "Neden-sonuç ilişkisi kurma",
            "Bilimsel keşif becerisi"
        ],
    },
    {
        "title": "Hava Dolu mu Boş mu",
        "subject": "Science",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Havanın görünmese de yer kapladığını fark etmeye yönelik etkinlik.",
        "materials": ["Balonlar", "Boş bardak", "Su dolu kap", "Peçete"],
        "instructions": [
            "Çocuklara havanın görünmediğini ama var olduğunu söyle",
            "Balonu şişirerek içindeki havayı göster",
            "Bardağın içine peçete koy ve ters çevirerek suya batır",
            "Peçetenin neden ıslanmadığını birlikte incele",
            "Havanın bardakta yer kapladığı sonucuna ulaşmaları için rehberlik et"
        ],
        "learning_goals": [
            "Havanın varlığını fark etme",
            "Gözlem becerisi",
            "Tahmin ve sonuç çıkarma",
            "Bilimsel kavramları anlamlandırma"
        ],
    },
    {
        "title": "Buzun Erime Yarışı",
        "subject": "Science",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Buzun farklı koşullarda nasıl eridiğini gözlemleme etkinliği.",
        "materials": ["Buz küpleri", "Tabaklar", "Tuz", "Ilık su", "Bez"],
        "instructions": [
            "Her gruba birkaç buz küpü ver",
            "Birini olduğu gibi bırak, birine tuz serpiştir, birine ılık su damlat",
            "Hangisinin daha hızlı eriyeceğini tahmin etmelerini iste",
            "Değişimi birlikte gözlemle",
            "Sonuçlar hakkında sohbet et"
        ],
        "learning_goals": [
            "Erime kavramını gözlemleme",
            "Tahmin yapma",
            "Karşılaştırma becerisi",
            "Bilimsel süreç farkındalığı"
        ],
    },
    {
        "title": "Toprakta Neler Var",
        "subject": "Science",
        "duration": "30-45min",
        "group_size": "Small Group",
        "description": "Toprağın içinde bulunan küçük parçaları ve doğal öğeleri inceleme etkinliği.",
        "materials": ["Toprak örnekleri", "Büyüteç", "Beyaz kağıt", "Küçük çubuklar", "Tepsi"],
        "instructions": [
            "Çocuklara farklı toprak örnekleri göster",
            "Toprağı tepsiye dökerek yay",
            "Büyüteç yardımıyla içindeki küçük taş, yaprak veya kök parçalarını incele",
            "Bulduklarını beyaz kağıt üzerinde ayır",
            "Toprağın neden önemli olduğu hakkında konuş"
        ],
        "learning_goals": [
            "Doğal materyalleri inceleme",
            "Gözlem becerisi",
            "Sınıflandırma yapma",
            "Doğa farkındalığı"
        ],
    },
    {
        "title": "Ses Titreşimi Deneyi",
        "subject": "Science",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Sesin titreşimle oluştuğunu keşfetmeye yönelik etkinlik.",
        "materials": ["Lastik bant", "Kutu", "Metal tepsi", "Kaşık"],
        "instructions": [
            "Lastik bandı kutunun etrafına geçir",
            "Lastik banda hafifçe dokunup sesi dinlet",
            "Titreşimi hissetmeleri için çocuklara deneme fırsatı ver",
            "Metal tepsiye kaşıkla vurup çıkan sesi dinlet",
            "Sesin nasıl oluştuğu hakkında konuş"
        ],
        "learning_goals": [
            "Ses ve titreşim ilişkisini fark etme",
            "Dinleme ve gözlem yapma",
            "Bilimsel keşif",
            "Neden-sonuç ilişkisi kurma"
        ],
    },
    {
        "title": "Yağmur Bulutu Kavanozu",
        "subject": "Science",
        "duration": "30-45min",
        "group_size": "Small Group",
        "description": "Bulut ve yağmur oluşumunu basit bir modelle gözlemleme etkinliği.",
        "materials": ["Şeffaf kavanoz", "Su", "Tıraş köpüğü", "Mavi gıda boyası veya suluboya"],
        "instructions": [
            "Kavanozu suyla doldur",
            "Üzerine tıraş köpüğü ekleyerek bulut gibi görünmesini sağla",
            "Üste boya damlat",
            "Boyanın aşağı doğru inmesini çocuklarla birlikte gözlemle",
            "Bulutlar ve yağmur hakkında basit açıklamalar yap"
        ],
        "learning_goals": [
            "Hava olaylarını gözlemleme",
            "Görsel model üzerinden öğrenme",
            "Tahmin yapma",
            "Bilimsel merak geliştirme"
        ],
    },
    {
        "title": "Meyve Çekirdeği İncelemesi",
        "subject": "Science",
        "duration": "15-30min",
        "group_size": "Individual",
        "description": "Farklı meyvelerin içindeki çekirdekleri karşılaştırma etkinliği.",
        "materials": ["Elma, portakal, biber gibi farklı meyveler", "Tabak", "Plastik bıçak (öğretmen kullanır)", "Büyüteç"],
        "instructions": [
            "Meyveleri çocuklara göster ve tahminlerini sor",
            "Meyveleri öğretmen rehberliğinde aç",
            "İçlerindeki çekirdekleri çıkarıp incele",
            "Hangi meyvede daha çok ya da daha az çekirdek olduğunu karşılaştır",
            "Çekirdeğin bitki için ne işe yaradığı hakkında konuş"
        ],
        "learning_goals": [
            "Bitki yapısını tanıma",
            "Karşılaştırma becerisi",
            "Gözlem yapma",
            "Doğa farkındalığı"
        ],
    },
    {
        "title": "Renkli Süt Deneyi",
        "subject": "Science",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Süt, boya ve sabun kullanarak renk hareketlerini gözlemleme etkinliği.",
        "materials": ["Süt", "Gıda boyası", "Sıvı sabun", "Tabak", "Pamuklu çubuk"],
        "instructions": [
            "Tabağa biraz süt dök",
            "Sütün üzerine farklı renklerde boya damlat",
            "Pamuklu çubuğu sıvı sabuna batır",
            "Çubuğu boyalı süte dokundur ve renklerin hareketini izle",
            "Çocuklardan gördüklerini anlatmalarını iste"
        ],
        "learning_goals": [
            "Kimyasal değişimi gözlemleme",
            "Renk hareketlerini inceleme",
            "Tahmin ve gözlem yapma",
            "Bilimsel merak geliştirme"
        ],
    },
    {
        "title": "Ağır mı Hafif mi",
        "subject": "Science",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Farklı nesneleri ağırlık açısından karşılaştırma etkinliği.",
        "materials": ["Farklı nesneler", "Basit terazi", "Karşılaştırma kartları"],
        "instructions": [
            "Çocuklara farklı nesneleri göster",
            "Hangisinin ağır, hangisinin hafif olabileceğini tahmin etmelerini iste",
            "Nesneleri terazide karşılaştır",
            "Sonuçları birlikte incele",
            "Benzer büyüklükte ama farklı ağırlıktaki nesneler hakkında konuş"
        ],
        "learning_goals": [
            "Ağırlık farkını anlama",
            "Tahmin etme",
            "Karşılaştırma yapma",
            "Gözlem becerisi"
        ],
    },
    {
        "title": "Hızlı mı Yavaş mı",
        "subject": "Music",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Müziğin hızına göre hareket ederek tempo farkını keşfetme etkinliği.",
        "materials": ["Müzik çalar", "Hızlı ve yavaş tempolu şarkılar", "Geniş hareket alanı"],
        "instructions": [
            "Çocuklara hızlı ve yavaş müzik örnekleri dinlet",
            "Yavaş müzikte yavaş hareket etmelerini iste",
            "Hızlı müzik başladığında hareketlerini hızlandırmalarını söyle",
            "Müzik durduğunda oldukları yerde donmalarını iste",
            "Etkinlik sonunda hangi müziğin daha hızlı ya da yavaş olduğunu konuş"
        ],
        "learning_goals": [
            "Tempo farkındalığı",
            "Dinleme becerisi",
            "Hareket koordinasyonu",
            "Müzikal kavramları tanıma"
        ],
    },
    {
        "title": "Sesli Sessiz Oyunu",
        "subject": "Music",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Sesli ve sessiz çalma arasında geçiş yaparak dikkat ve ritim becerisi geliştirme etkinliği.",
        "materials": ["Ritim çalgıları", "Dur-kalk kartları veya işaretleri"],
        "instructions": [
            "Çocuklara sesli ve sessiz çalma kavramlarını açıkla",
            "Bir işaret verdiğinde yüksek sesle, diğer işarette yumuşak sesle çalmalarını iste",
            "İşaretleri karışık sırayla göster",
            "Bazen tamamen durmalarını isteyerek dikkatlerini ölç",
            "Etkinlik sonunda hangi seslerin daha güçlü veya yumuşak duyulduğunu konuş"
        ],
        "learning_goals": [
            "Ses yüksekliğini ayırt etme",
            "Dikkat toplama",
            "Yönerge takip etme",
            "Ritim duygusu geliştirme"
        ],
    },
    {
        "title": "Hayvan Sesleri Orkestrası",
        "subject": "Music",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Hayvan seslerini taklit ederek ritmik bir müzik çalışması yapma etkinliği.",
        "materials": ["Hayvan kartları", "Basit ritim çalgıları", "Geniş alan"],
        "instructions": [
            "Hayvan kartlarını çocuklara göster",
            "Her hayvanın çıkardığı sesi birlikte taklit et",
            "Bazı hayvan seslerini ritim çalgılarıyla eşleştir",
            "Gruplar halinde sırayla ses çıkararak küçük bir orkestra oluştur",
            "Etkinlik sonunda hangi hayvan seslerinin daha hızlı, yavaş veya güçlü olduğunu konuş"
        ],
        "learning_goals": [
            "İşitsel farkındalık",
            "Ritim oluşturma",
            "Taklit becerisi",
            "Grup içinde uyum sağlama"
        ],
    },
    {
        "title": "Davulunu Dinle",
        "subject": "Music",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Basit davul ritimlerini dinleyip tekrar ederek işitsel hafıza geliştirme etkinliği.",
        "materials": ["Küçük davullar veya kutular", "Ritim çubukları (isteğe bağlı)"],
        "instructions": [
            "Basit bir ritim çal ve çocukların dinlemesini sağla",
            "Aynı ritmi tekrar etmelerini iste",
            "Ritimleri kısa ve anlaşılır şekilde sırayla artır",
            "Çocukların kendi ritimlerini oluşturmalarına fırsat ver",
            "Birbirlerinin ritmini dinleyip tekrar etmelerini sağla"
        ],
        "learning_goals": [
            "İşitsel hafıza",
            "Ritim tekrarı",
            "Dikkat ve odaklanma",
            "Müzikal ifade"
        ],
    },
    {
        "title": "Müzikle Duygu Yüzleri",
        "subject": "Music",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Farklı müzik türlerini dinleyerek hissettirdiği duyguları ifade etme etkinliği.",
        "materials": ["Müzik çalar", "Farklı türlerde kısa müzikler", "Duygu kartları"],
        "instructions": [
            "Çocuklara kısa müzik parçaları dinlet",
            "Her müzikten sonra nasıl hissettiklerini sor",
            "Uygun duygu kartını seçmelerini iste",
            "Müziğe uygun yüz ifadeleri veya hareketler yapmalarını teşvik et",
            "Müziğin duygularımızı nasıl etkileyebileceği hakkında konuş"
        ],
        "learning_goals": [
            "Müzik ve duygu ilişkisini fark etme",
            "Duygu ifade etme",
            "Dinleme becerisi",
            "Yaratıcı tepki verme"
        ],
    },
    {
        "title": "Çıngırak Yapımı ve Çalma",
        "subject": "Music",
        "duration": "30-45min",
        "group_size": "Individual",
        "description": "Basit malzemelerle çıngırak yapıp ritim çalışması yapma etkinliği.",
        "materials": ["Küçük plastik şişeler veya kaplar", "Pirinç veya mercimek", "Bant", "Renkli kağıt ve çıkartmalar"],
        "instructions": [
            "Her çocuğa küçük bir kap veya şişe ver",
            "İçine az miktarda pirinç veya mercimek koy",
            "Kapağı güvenli şekilde kapat ve bantla sabitle",
            "Çocukların çıngıraklarını süslemelerine fırsat ver",
            "Hazırlanan çıngıraklarla basit ritimler oluştur"
        ],
        "learning_goals": [
            "Ses üretme keşfi",
            "Ritim becerisi",
            "Yaratıcı tasarım",
            "İnce motor gelişimi"
        ],
    },
    {
        "title": "Şarkının Sonunu Tahmin Et",
        "subject": "Music",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Bilinen şarkıları dinleyip eksik bırakılan bölümleri tamamlamaya çalışma etkinliği.",
        "materials": ["Müzik çalar veya öğretmen sesi", "Bilinen çocuk şarkıları"],
        "instructions": [
            "Çocukların bildiği kısa bir şarkı seç",
            "Şarkıyı söylerken bazı yerlerde dur",
            "Eksik kalan kısmı çocukların tamamlamasını iste",
            "Doğru tamamlanan bölümleri birlikte tekrar et",
            "Farklı şarkılarla etkinliği sürdür"
        ],
        "learning_goals": [
            "İşitsel hafıza",
            "Şarkı sözlerini hatırlama",
            "Dikkat becerisi",
            "Müzikal katılım"
        ],
    },
    {
        "title": "Ritimle İsim Söyleme",
        "subject": "Music",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Çocukların isimlerini ritimle söyleyerek grup içi katılım sağlama etkinliği.",
        "materials": ["El çırpma", "Basit ritim çalgıları (isteğe bağlı)"],
        "instructions": [
            "Çocuklarla çember şeklinde otur",
            "Bir çocuğun adını heceleyerek ritimle söyle",
            "Grubun aynı ritmi tekrar etmesini iste",
            "Her çocuk için sırayla devam et",
            "İstersen çocukların kendi ritimlerini de eklemelerine fırsat ver"
        ],
        "learning_goals": [
            "Ritim farkındalığı",
            "İsim tanıma",
            "Grup katılımı",
            "İşitsel tekrar becerisi"
        ],
    },
    {
        "title": "Müzikli Hikaye Yolculuğu",
        "subject": "Music",
        "duration": "30-45min",
        "group_size": "Small Group",
        "description": "Bir hikayeyi müzik ve ses efektleriyle destekleyerek anlatma etkinliği.",
        "materials": ["Kısa hikaye metni", "Basit ritim çalgıları", "Ses çıkaran materyaller"],
        "instructions": [
            "Kısa ve basit bir hikaye seç",
            "Hikayedeki bölümlere uygun sesler belirle",
            "Çocuklara hangi bölümde hangi sesi çıkaracaklarını göster",
            "Hikayeyi anlatırken çocukların seslerle eşlik etmesini sağla",
            "Etkinlik sonunda en sevdikleri sesleri konuş"
        ],
        "learning_goals": [
            "Dinleme ve anlama",
            "Müzikle anlatımı destekleme",
            "Yaratıcı katılım",
            "Grup içinde iş birliği"
        ],
    },
    {
        "title": "Melodi Takibi",
        "subject": "Music",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Basit ses dizilerini dinleyip benzer şekilde tekrar etme etkinliği.",
        "materials": ["Ksilofon, zil veya basit ses araçları", "Sessiz çalışma alanı"],
        "instructions": [
            "İki veya üç sesten oluşan kısa bir melodi çal",
            "Çocuklardan dikkatlice dinlemelerini iste",
            "Aynı sırayı tekrar etmeye çalışmalarını sağla",
            "Melodi dizilerini yavaş yavaş çeşitlendir",
            "İsteyen çocukların kendi kısa dizilerini oluşturmalarına fırsat ver"
        ],
        "learning_goals": [
            "Ses sırasını fark etme",
            "İşitsel dikkat",
            "Melodi takibi",
            "Müziksel hafıza"
        ],
    },
    {
        "title": "Renkli Halka Sıçraması",
        "subject": "Physical",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Yerdeki renkli halkalar arasında sıçrayarak denge ve koordinasyon geliştirme etkinliği.",
        "materials": ["Renkli halkalar veya yere yapıştırılmış daireler", "Geniş hareket alanı"],
        "instructions": [
            "Renkli halkaları yere farklı aralıklarla yerleştir",
            "Çocuklara halkaların içine sırayla zıplamayı göster",
            "Tek ayak, çift ayak veya belirli renklere sıçrama gibi yönergeler ver",
            "Çocukların parkuru dikkatle tamamlamasını sağla",
            "İstersen halkaların sırasını değiştirerek etkinliği tekrar et"
        ],
        "learning_goals": [
            "Denge geliştirme",
            "Koordinasyon becerisi",
            "Yönerge takip etme",
            "Kaba motor gelişimi"
        ],
    },
    {
        "title": "Yavaş Hızlı Yürü",
        "subject": "Physical",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Verilen komutlara göre yavaş, hızlı, büyük ve küçük adımlarla yürüme etkinliği.",
        "materials": ["Geniş hareket alanı", "Müzik (isteğe bağlı)"],
        "instructions": [
            "Çocuklara yavaş ve hızlı yürüme örnekleri göster",
            "Büyük adım, küçük adım, sessiz adım gibi komutlar ver",
            "Komutlara göre yürüyüşlerini değiştirmelerini iste",
            "İstersen müzik eşliğinde hareket temposunu değiştir",
            "Etkinlik sonunda hangi yürüyüşün daha kolay veya zor olduğunu konuş"
        ],
        "learning_goals": [
            "Beden kontrolü",
            "Dinleme becerisi",
            "Hareket farkındalığı",
            "Kaba motor koordinasyonu"
        ],
    },
    {
        "title": "Topu Hedefe Yuvarla",
        "subject": "Physical",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Topları belirlenen hedefe yuvarlayarak el-göz koordinasyonu geliştirme etkinliği.",
        "materials": ["Yumuşak toplar", "Hedef kutuları veya huniler", "Yer işaretleri"],
        "instructions": [
            "Çocuklara hedef alanı göster",
            "Topu elleriyle nasıl yuvarlayacaklarını örnekle göster",
            "Sırayla herkesin topu hedefe yuvarlamasını iste",
            "Yakın ve uzak mesafelerde denemeler yap",
            "İstersen farklı boydaki toplarla etkinliği çeşitlendir"
        ],
        "learning_goals": [
            "El-göz koordinasyonu",
            "Hedefe yönelme becerisi",
            "Dikkat geliştirme",
            "Kaba motor becerileri"
        ],
    },
    {
        "title": "Hayvan Yürüyüşleri",
        "subject": "Physical",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Farklı hayvan hareketlerini taklit ederek beden farkındalığı geliştirme etkinliği.",
        "materials": ["Hayvan kartları", "Geniş hareket alanı"],
        "instructions": [
            "Çocuklara farklı hayvan kartları göster",
            "Ayı gibi yürüme, tavşan gibi zıplama, yılan gibi sürünme gibi örnekler ver",
            "Çocuklardan karttaki hayvan gibi hareket etmelerini iste",
            "Hareketleri sırayla veya karışık şekilde tekrar et",
            "Etkinlik sonunda en sevdikleri hayvan yürüyüşünü seçmelerini iste"
        ],
        "learning_goals": [
            "Beden farkındalığı",
            "Taklit becerisi",
            "Kaba motor gelişimi",
            "Yaratıcı hareket"
        ],
    },
    {
        "title": "Denge Yolu",
        "subject": "Physical",
        "duration": "15-30min",
        "group_size": "Individual",
        "description": "Yerde oluşturulan çizgi veya yol üzerinde dengeli yürüyüş yapma etkinliği.",
        "materials": ["Bant çizgisi veya denge tahtası", "Yer işaretleri"],
        "instructions": [
            "Yere düz veya hafif kıvrımlı bir denge yolu oluştur",
            "Çocuklara çizginin üzerinde dikkatle yürümeyi göster",
            "Kollar açık şekilde dengede kalmalarını iste",
            "İstersen topuk-burun yürüme gibi küçük görevler ekle",
            "Her çocuğun kendi hızında denemesine fırsat ver"
        ],
        "learning_goals": [
            "Denge becerisi",
            "Beden kontrolü",
            "Odaklanma",
            "Koordinasyon"
        ],
    },
    {
        "title": "Yastık Adaları",
        "subject": "Physical",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Yere yerleştirilen minder ve yastıklar arasında adım atlayarak ilerleme etkinliği.",
        "materials": ["Minderler veya yastıklar", "Geniş alan"],
        "instructions": [
            "Minderleri yere aralıklı şekilde yerleştir",
            "Çocuklara minderleri ada gibi hayal etmelerini söyle",
            "Yere basmadan adadan adaya geçmelerini iste",
            "Daha sonra aralıkları değiştirerek etkinliği zorlaştır",
            "İstersen denge ve sıçrama görevleri ekle"
        ],
        "learning_goals": [
            "Sıçrama becerisi",
            "Denge ve koordinasyon",
            "Mekansal farkındalık",
            "Kaba motor gelişimi"
        ],
    },
    {
        "title": "Kuyruk Yakalama Oyunu",
        "subject": "Physical",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Bel kısmına takılan kumaş parçalarını koruma ve yakalama oyunu.",
        "materials": ["Kumaş şeritler veya kurdeleler", "Geniş hareket alanı"],
        "instructions": [
            "Her çocuğun bel kısmına bir kumaş şerit yerleştir",
            "Amaçlarının kendi kuyruğunu korurken başkasının kuyruğunu almaya çalışmak olduğunu açıkla",
            "Oyunu güvenli alan içinde başlat",
            "Belirli süre sonunda kimin elinde kaç kuyruk olduğunu say",
            "Etkinlik sonunda güvenli hareket etmenin önemini konuş"
        ],
        "learning_goals": [
            "Hız ve çeviklik",
            "Alan farkındalığı",
            "Kurallı oyun oynama",
            "Kaba motor gelişimi"
        ],
    },
    {
        "title": "Tünelden Geç",
        "subject": "Physical",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Tünel veya masa altından sürünerek geçme etkinliği.",
        "materials": ["Oyun tüneli veya masa ve örtü", "Yer minderleri"],
        "instructions": [
            "Çocuklara tünelin başlangıç ve bitiş noktasını göster",
            "Sürünerek nasıl geçileceğini örnekle göster",
            "Sırayla tünele girip çıkmalarını sağla",
            "İstersen çıkışta küçük bir hedefe dokunma görevi ver",
            "Etkinliği birkaç tur tekrarla"
        ],
        "learning_goals": [
            "Sürünme becerisi",
            "Kas koordinasyonu",
            "Alan kullanımı",
            "Kaba motor gelişimi"
        ],
    },
    {
        "title": "Balon Havada Kalsın",
        "subject": "Physical",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Balonu yere düşürmeden hareket ettirme etkinliği.",
        "materials": ["Balonlar", "Açık alan"],
        "instructions": [
            "Her çocuk ya da grup için bir balon ver",
            "Balonu sadece elleriyle havada tutmaya çalışmalarını iste",
            "Balon yere düştüğünde yeniden başlat",
            "İstersen iki çocuk birlikte tek balonla çalışma yapabilir",
            "Hangi grubun balonu daha uzun süre havada tuttuğunu gözlemle"
        ],
        "learning_goals": [
            "El-göz koordinasyonu",
            "Refleks geliştirme",
            "Dikkat ve takip becerisi",
            "Grup içinde iş birliği"
        ],
    },
    {
        "title": "Taklit ve Don Oyunu",
        "subject": "Physical",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Öğretmenin hareketlerini taklit edip belirli anda donma etkinliği.",
        "materials": ["Geniş alan", "Müzik (isteğe bağlı)"],
        "instructions": [
            "Çocuklara zıplama, dönme, eğilme gibi basit hareketler göster",
            "Herkesin seni taklit etmesini iste",
            "Bir anda don komutu ver ve hareketi durdurmalarını iste",
            "Farklı hız ve yönlerde hareketlerle oyunu sürdür",
            "Etkinlik sonunda en eğlenceli hareketleri tekrar et"
        ],
        "learning_goals": [
            "Taklit becerisi",
            "Öz denetim",
            "Dinleme ve dikkat",
            "Kaba motor gelişimi"
        ],
    },
    {
        "title": "Duygu Termometresi",
        "subject": "Social-Emotional",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Çocukların o andaki duygularını fark edip ifade etmelerine yardımcı olan etkinlik.",
        "materials": ["Duygu termometresi posteri", "Yüz ifadeleri kartları", "Mandallar veya isim kartları"],
        "instructions": [
            "Duygu termometresini çocuklara tanıt",
            "Mutlu, üzgün, heyecanlı, kızgın gibi duyguları birlikte tekrar et",
            "Her çocuğun kendi ismini ya da mandalını o anki duygusuna uygun yere koymasını iste",
            "İsteyen çocukların neden böyle hissettiğini paylaşmasına fırsat ver",
            "Etkinlik sonunda duyguların gün içinde değişebileceği hakkında konuş"
        ],
        "learning_goals": [
            "Duygu farkındalığı",
            "Kendini ifade etme",
            "Duyguları adlandırma",
            "Öz farkındalık geliştirme"
        ],
    },
    {
        "title": "Nazik Sözler Sepeti",
        "subject": "Social-Emotional",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Olumlu ve nazik ifadeleri kullanma alışkanlığı kazandırmaya yönelik etkinlik.",
        "materials": ["Sepet veya kutu", "Nazik söz kartları", "Resim kartları"],
        "instructions": [
            "Lütfen, teşekkür ederim, affedersin gibi nazik sözleri çocuklarla konuş",
            "Kartları sırayla sepetten çek",
            "Her karttaki ifadeyi hangi durumda kullanabileceğimizi tartış",
            "Çocuklardan küçük canlandırmalarla bu sözleri kullanmalarını iste",
            "Gün içinde bu sözleri kullanmaları için teşvik et"
        ],
        "learning_goals": [
            "Nazik iletişim kurma",
            "Sosyal farkındalık",
            "Uygun dil kullanımı",
            "Akran ilişkilerini güçlendirme"
        ],
    },
    {
        "title": "Sıra Bende Sıra Sende",
        "subject": "Social-Emotional",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Sıra bekleme ve paylaşma becerisini destekleyen oyun etkinliği.",
        "materials": ["Top veya oyuncak", "Sıra kartları (isteğe bağlı)"],
        "instructions": [
            "Çocuklarla küçük bir çember oluştur",
            "Bir nesneyi sırayla elden ele dolaştır",
            "Nesne kimdeyse kısa bir cevap vermesini veya küçük bir hareket yapmasını iste",
            "Diğer çocukların sırasını beklemesini hatırlat",
            "Etkinlik sonunda sıra beklemenin neden önemli olduğunu konuş"
        ],
        "learning_goals": [
            "Sıra bekleme becerisi",
            "Paylaşma alışkanlığı",
            "Sabır geliştirme",
            "Grup içinde uyum sağlama"
        ],
    },
    {
        "title": "Arkadaşına Yardım Et",
        "subject": "Social-Emotional",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Yardımlaşma ve iş birliğini destekleyen eşli etkinlik.",
        "materials": ["Bloklar", "Yapboz parçaları veya basit görev materyalleri"],
        "instructions": [
            "Çocukları ikili gruplara ayır",
            "Her çifte birlikte tamamlayabilecekleri küçük bir görev ver",
            "Birbirlerine nasıl yardım edebileceklerini konuş",
            "Görev sırasında iş birliğini ve destekleyici davranışları gözlemle",
            "Etkinlik sonunda kimin nasıl yardım ettiğini birlikte paylaş"
        ],
        "learning_goals": [
            "Yardımlaşma becerisi",
            "İş birliği yapma",
            "Empati geliştirme",
            "Olumlu sosyal etkileşim"
        ],
    },
    {
        "title": "Ayna Duyguları",
        "subject": "Social-Emotional",
        "duration": "15-30min",
        "group_size": "Individual",
        "description": "Ayna kullanarak yüz ifadeleri üzerinden duyguları tanıma etkinliği.",
        "materials": ["Ayna", "Duygu kartları"],
        "instructions": [
            "Çocuklara duygu kartlarını sırayla göster",
            "Her duygu için aynada aynı yüz ifadesini yapmalarını iste",
            "Hangi duygunun nasıl göründüğünü birlikte incele",
            "Çocukların kendi örneklerini paylaşmasına fırsat ver",
            "Etkinlik sonunda hangi duyguyu yapmanın daha kolay olduğunu konuş"
        ],
        "learning_goals": [
            "Yüz ifadelerini fark etme",
            "Duyguları tanıma",
            "Öz farkındalık",
            "Duygu ifadesi geliştirme"
        ],
    },
    {
        "title": "Sorun Çözme Kartları",
        "subject": "Social-Emotional",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Günlük küçük çatışma ve sorunlara çözüm üretmeyi destekleyen etkinlik.",
        "materials": ["Sorun durumu kartları", "Çözüm görselleri", "Pano"],
        "instructions": [
            "Çocuklara basit sosyal durum kartları göster",
            "Örneğin oyuncak paylaşmama veya sıraya girememe gibi durumları birlikte konuş",
            "Bu durumda neler yapılabileceğini çocuklardan dinle",
            "Uygun çözüm yollarını görsellerle eşleştir",
            "Etkinlik sonunda sakin düşünmenin önemini vurgula"
        ],
        "learning_goals": [
            "Sorun çözme becerisi",
            "Sosyal durumları değerlendirme",
            "Duyguları yönetme",
            "Uygun çözüm üretme"
        ],
    },
    {
        "title": "Teşekkür Çiçeği",
        "subject": "Social-Emotional",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Minnettarlık ve teşekkür etme alışkanlığını geliştiren grup etkinliği.",
        "materials": ["Büyük çiçek posteri", "Yaprak veya taç yaprak kağıtları", "Kalemler"],
        "instructions": [
            "Teşekkür etmenin ne anlama geldiğini çocuklarla konuş",
            "Her çocuğun kime veya neye teşekkür etmek istediğini düşünmesini iste",
            "Bu düşünceyi taç yapraklara yaz veya resmet",
            "Tüm yaprakları büyük çiçeğin üzerine yerleştir",
            "Etkinlik sonunda teşekkür etmenin insanları nasıl hissettirdiğini konuş"
        ],
        "learning_goals": [
            "Minnettarlık geliştirme",
            "Olumlu düşünme",
            "Kendini ifade etme",
            "Sosyal-duygusal farkındalık"
        ],
    },
    {
        "title": "Birlikte Nefes Al",
        "subject": "Social-Emotional",
        "duration": "15-30min",
        "group_size": "Whole Class",
        "description": "Basit nefes egzersizleriyle sakinleşme ve duyguları düzenleme etkinliği.",
        "materials": ["Rahat oturma alanı", "İsteğe bağlı yumuşak müzik", "Nefes kartları"],
        "instructions": [
            "Çocuklarla rahat şekilde otur",
            "Burundan nefes alıp ağızdan vermeyi örnekle göster",
            "Balon şişiriyormuş gibi derin nefes alma oyunu yap",
            "Nefes alırken ve verirken sayma çalışması yap",
            "Etkinlik sonunda bedenlerinin nasıl hissettiğini konuş"
        ],
        "learning_goals": [
            "Sakinleşme becerisi",
            "Öz düzenleme",
            "Beden farkındalığı",
            "Duygusal denge geliştirme"
        ],
    },
    {
        "title": "Arkadaşını Dinle",
        "subject": "Social-Emotional",
        "duration": "15-30min",
        "group_size": "Small Group",
        "description": "Bir arkadaşını dikkatle dinleme ve söylediklerini hatırlama etkinliği.",
        "materials": ["Konuşma nesnesi veya küçük top"],
        "instructions": [
            "Çocukları küçük gruplara ayır",
            "Konuşma nesnesi kimdeyse onun konuşacağını açıkla",
            "Her çocuk kısa bir şey paylaştıktan sonra diğer çocuklara ne söylediğini sor",
            "Dikkatle dinlemenin önemini vurgula",
            "Etkinlik sonunda iyi bir dinleyicinin neler yaptığı hakkında konuş"
        ],
        "learning_goals": [
            "Aktif dinleme becerisi",
            "Saygılı iletişim",
            "Dikkat geliştirme",
            "Akranlarla olumlu etkileşim"
        ],
    },
    {
        "title": "Mutlu Anılar Panosu",
        "subject": "Social-Emotional",
        "duration": "30-45min",
        "group_size": "Whole Class",
        "description": "Çocukların mutlu oldukları anları paylaşarak olumlu dugular üzerine düşünme etkinliği.",
        "materials": ["Büyük pano veya karton", "Kağıtlar", "Boya kalemleri", "Yapıştırıcı"],
        "instructions": [
            "Mutlu hissettiren anlar hakkında kısa bir sohbet başlat",
            "Her çocuktan mutlu olduğu bir anı çizmesini iste",
            "İsteyen çocukların resmini anlatmasına fırsat ver",
            "Tüm resimleri pano üzerine yerleştir",
            "Mutlu anıları paylaşmanın bize nasıl iyi hissettirdiğini konuş"
        ],
        "learning_goals": [
            "Olumlu duygu farkındalığı",
            "Kendini ifade etme",
            "Akran paylaşımı",
            "Sosyal bağ kurma"
        ],
    },
]



def seed_activities():
    app = create_app()

    with app.app_context():
        added_count = 0

        for item in ACTIVITIES:
            existing = Activity.query.filter_by(title=item["title"]).first()
            if existing:
                continue

            activity = Activity(
                title=item["title"],
                subject=item["subject"],
                duration=item["duration"],
                group_size=item["group_size"],
                description=item["description"],
                materials=json.dumps(item["materials"], ensure_ascii=False),
                instructions=json.dumps(item["instructions"], ensure_ascii=False),
                learning_goals=json.dumps(item["learning_goals"], ensure_ascii=False),
            )

            db.session.add(activity)
            added_count += 1

        db.session.commit()
        print(f"{added_count} activity added.")


if __name__ == "__main__":
    seed_activities()