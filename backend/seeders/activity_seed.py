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