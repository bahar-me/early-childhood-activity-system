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
        "assessment_questions": [
            "Hangi rengi saymak senin için daha kolaydı?",
            "Nesneleri sayarken karışmamak için neler yaptın?",
            "Bir daha oynasak hangi sayıya kadar saymak isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az nesne ve 1-5 arası sayılarla başlanabilir. Hazır olan çocuklar için 10'dan büyük sayılar, iki grubu karşılaştırma veya eksik sayıyı bulma gibi ek görevler verilebilir.",
        "family_community_notes": "Ailelere, evde düğme, kaşık, oyuncak gibi günlük nesnelerle kısa sayma ve renk gruplama oyunları oynamaları önerilebilir. Çocuklardan evde saydıkları nesnelerden birini sınıfta anlatmaları istenebilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların sayma, birebir eşleştirme, renk ayırt etme ve gruplama becerilerini destekler. Somut nesnelerle yapılan çalışma sayesinde temel matematiksel farkındalık güçlenir."
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
        "assessment_questions": [
            "Hangi resimlerin aynı sesi paylaştığını hatırlıyor musun?",
            "Başka hangi kelimeler bu sesle başlıyor olabilir?",
            "Bugün hangi sesi en kolay buldun?",
            "Resimlerden hangisinin sesi seni şaşırttı?",
            "Bu oyunu evde ailenle oynasak hangi harfi seçerdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az kart ve belirgin görseller kullanılabilir. Hazır olan çocuklara aynı sesle başlayan yeni kelimeler söyleme, sesleri karşılaştırma veya kısa cümle kurma fırsatı verilebilir.",
        "family_community_notes": "Ailelere, evde seçilen sesle başlayan eşyaları birlikte bulma oyunu oynamaları önerilebilir. Çocuklardan evde keşfettikleri bir kelimeyi ertesi gün sınıfta paylaşmaları istenebilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların ses farkındalığını, başlangıç seslerini ayırt etme becerisini ve harf-ses ilişkisini destekler. Oyun temelli yapı, dinleme ve sözel ifade becerilerini de güçlendirir."
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
        "assessment_questions": [
            "Hangi malzemeleri kullandın ve neden seçtin?",
            "Yaparken hangi renkleri ve dokuları fark ettin?",
            "Bu kolajda en çok neyi seviyorsun?",
            "Başka hangi doğal malzemeleri eklemek isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha büyük parçalar ve sınırlı sayıda malzeme sunulabilir. Hazır olan çocuklar için daha ayrıntılı düzenleme, belirli bir tema oluşturma veya yaptığı çalışmayı anlatma görevi eklenebilir.",
        "family_community_notes": "Ailelere, çocuklarıyla birlikte kısa bir doğa yürüyüşü yaparak yaprak, taş veya dal gibi güvenli materyaller toplamaları önerilebilir. Çocuklar evde topladıkları bir doğal nesneyi sınıfta tanıtabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların yaratıcı ifade, ince motor kontrolü, doğa farkındalığı ve görsel düzenleme becerilerini destekler. Doğal materyallerle çalışma, çocukların doku ve biçim özelliklerini keşfetmelerine fırsat verir."
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
        "assessment_questions": [
            "Hangi nesnelerin batacağını tahmin ettin ve neden?",
            "Test ettiğimiz nesnelerden hangileri yüzdü, hangileri battı?",
            "Neden bazı nesneler yüzdü, bazıları battı sence?",
            "Bu deneyde en çok neyi öğrendin?",
            "Bir daha denesek hangi nesneyi suya koymak isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az nesneyle ve belirgin fark gösteren materyallerle çalışılabilir. Hazır olan çocuklar için yeni nesneler ekleme, tahminlerini nedenleriyle açıklama ve sonuçları karşılaştırma görevi verilebilir.",
        "family_community_notes": "Ailelere, evde güvenli malzemelerle lavabo veya kap içinde küçük batma-yüzme denemeleri yapmaları önerilebilir. Çocuklardan evde denedikleri bir nesnenin sonucunu sınıfta paylaşmaları istenebilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların tahmin etme, gözlem yapma, karşılaştırma ve sonuç çıkarma becerilerini destekler. Somut deneyim yoluyla batma ve yüzme kavramları anlaşılır hale gelir."
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
        "assessment_questions": [
            "Müzik durduğunda nasıl hissettin?",
            "En sevdiğin şarkıda dans etmek nasıldı?",
            "Donma görevlerini yaparken zorlandığın bir şey oldu mu?",
            "Bu oyunu tekrar oynasak hangi şarkıyı seçerdin?",
            "Hangi pozisyonda donmak seni en çok güldürdü?",
            "Müziği dikkatle dinlemek için neler yaptın?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha yavaş tempo ve daha basit yönergeler kullanılabilir. Hazır olan çocuklar için tek ayak üzerinde donma, belirli pozlar oluşturma veya arkadaşlarına liderlik etme gibi ek görevler verilebilir.",
        "family_community_notes": "Ailelere, evde kısa müzik aç-kapat oyunları oynayarak çocuklarıyla birlikte donma hareketleri yapmaları önerilebilir. Çocuklar evde denedikleri komik bir donma pozunu sınıfta gösterebilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların dinleme becerisi, öz denetim, yönerge takibi ve kaba motor kontrolünü destekler. Müzik ve hareketin birlikte kullanılması dikkat ve beden farkındalığını güçlendirir."
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
        "assessment_questions": [
            "Hangi istasyon senin için en kolaydı, hangisi daha zordu?",
            "Parkuru tamamlarken nasıl hissettin?",
            "Denge çizgisinde yürürken neye dikkat ettin?",
            "Bu parkuru tekrar denesek hangi istasyonu daha iyi yapmak isterdin?",
            "Bir daha denesek parkura hangi hareketi eklemek isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için parkur daha kısa tutulabilir ve bazı istasyonlar sadeleştirilebilir. Hazır olan çocuklar için süre tutma, ek hareketler ekleme veya parkuru ikinci kez farklı şekilde tamamlama fırsatı sunulabilir.",
        "family_community_notes": "Ailelere, evde yastık, bant çizgisi veya küçük kutularla güvenli bir mini parkur kurmaları önerilebilir. Çocuklardan evde tamamladıkları bir hareketi sınıfta anlatmaları istenebilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların kaba motor becerileri, denge, koordinasyon ve yönerge takibi becerilerini destekler. Hareketli istasyonlar, çocukların dikkatini ve fiziksel özgüvenini artırır."
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
        "assessment_questions": [
            "Hangi duyguyu aynada yaparken en çok eğlendin?",
            "Bu duyguyu hangi durumlarda hissedebileceğimizi hatırlıyor musun?",
            "Kendi deneyimlerinden bu duyguyu yaşadığın bir anı paylaşabilir misin?",
            "Bu oyunu evde ailenle oynasak hangi duyguyu seçerdin?",
            "Aynaya bakınca hangi yüz ifadesini yapmayı sevdin?",
            "Sen en son ne zaman böyle hissettin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az duygu kartı ve net yüz ifadeleri kullanılabilir. Hazır olan çocuklar için duyguların nedenlerini açıklama, arkadaşının duygusunu tahmin etme veya kısa canlandırma yapma fırsatı verilebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte gün içinde hissedilen duygular hakkında konuşmaları ve aynada yüz ifadeleri yapma oyunu oynamaları önerilebilir. Çocuklar evde konuştukları bir duyguyu sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların duygu tanıma, öz farkındalık, empati ve sözel ifade becerilerini destekler. Yüz ifadeleri ve aynayla çalışma, duyguların somut olarak fark edilmesini kolaylaştırır."
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
        "assessment_questions": [
            "Hangi şekilleri bulmayı en çok sevdin?",
            "Bulduğun şekillerden hangisi senin için daha kolaydı, hangisi daha zordu?",
            "Bu oyunu tekrar oynasak hangi şekli bulmak isterdin?",
            "Sınıfta başka hangi nesnelerin bu şekle benzediğini fark ettin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az şekil kartı ve basit şekiller kullanılabilir. Hazır olan çocuklar için şekillerin özelliklerini açıklama, farklı şekilleri eşleştirme veya şekillendirme fırsatı verilebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte sınıf içinde öğrendikleri şekilleri bulmaları ve tanımlamaları önerilebilir. Çocuklar evde konuştukları bir şekli sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların şekil tanıma, mekânsal farkındalık, gözlem becerileri ve sayma becerilerini destekler. Şekil avı etkinliği, çocukların görsel algılayışlarını ve problem çözme becerilerini geliştirmeye yardımcı olur."
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
        "assessment_questions": [
            "Hikâyeyi anladığını nasıl hissediyorsun?",
            "Hangi karakter seni en çok etkiledi?",
            "Bu hikâyeyi başka bir sonuca sahip olacak şekilde yeniden hayal edebilir misin?",
            "Hikâyede geçen olayları sıralayabilir misin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için hikâyeyi daha basit dille anlatmak ve rolleri daha az sayıda karakterle sınırlamak uygun olur. Hazır olan çocuklar için hikâyeyi yeniden yorumlama, karakterlerle rol yapma veya yeni bir sonuca sahip olacak şekilde yeniden canlandırma fırsatı verilebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte hikâyeyi okumaları ve karakterler hakkında konuşmaları önerilebilir. Çocuklar evde konuştukları bir sahneyi sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların hikâye anlama, konuşma ve dinleme becerilerini, dramatik ifade becerilerini ve iş birliği yapma becerilerini destekler. Hikâye Zamanı Tiyatrosu etkinliği, çocukların hayal gücünü ve sosyal becerilerini geliştirmeye yardımcı olur."
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
        "assessment_questions": [
            "Oyun hamuruyla en çok ne yapmayı sevdin?",
            "Hamuru şekillendirirken hangi hareketleri kullandın?",
            "Yaptığın tasarımı bize nasıl anlatırsın?",
            "Bir dahaki sefere oyun hamuruyla ne yapmak isterdin?",
            "Hangi renkleri ve araçları kullanmayı tercih ettin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha yumuşak hamur, büyük kalıplar ve basit şekillendirme araçları kullanılabilir. Hazır olan çocuklar için belirli bir tema seçme, daha ayrıntılı figürler oluşturma veya yaptığı tasarımı arkadaşlarına anlatma fırsatı verilebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte oyun hamuru, kil veya güvenli ev yapımı hamurla basit şekiller oluşturmaları önerilebilir. Çocuklardan evde yaptıkları bir tasarımı sınıfta anlatmaları istenebilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların ince motor becerilerini, el-göz koordinasyonunu, yaratıcı düşünmesini ve sözel ifade becerilerini destekler. Oyun hamuruyla çalışma, çocukların parmak kaslarını güçlendiririrken hayal güçlerini somut ürünlere dönüştürmelerine fırsat verir."
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
        "assessment_questions": [
            "Tohum ekmeden önce bitkilerin büyümesi için neler gerektiğini hatırlıyor musun?",
            "Bitkinin büyümesini gözlemlerken neler gördün?",
            "Bitkinin büyümesi için ne kadar su verdiğimize dikkat ettin mi?",
            "Bu deneyde en çok neyi öğrendin?",
            "Bir daha denesek hangi tür tohumu ekmek isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha büyük tohumlar ve daha az gözlem yapma fırsatı sunulabilir. Hazır olan çocuklar için farklı türde tohumlar ekme, büyüme hızlarını karşılaştırma veya bitkinin farklı bölümlerini çizme gibi ek görevler verilebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte küçük bir bitki yetiştirmeleri ve büyüme sürecini gözlemlemeleri önerilebilir. Çocuklar evde yetiştirdikleri bitki hakkında sınıfta paylaşım yapabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların yaşam döngüsü, bilimsel gözlem, veri toplama ve sorumluluk becerilerini destekler. Tohum ekme ve büyüme sürecini izleme, çocukların doğa ve canlılar hakkında farkındalıklarını artırır."
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
        "assessment_questions": [
            "Hangi ritmi tekrar etmek senin için daha kolaydı?",
            "Kendi ritmini oluştururken ne düşündün?",
            "Bu etkinlikte en çok neyi sevdin?",
            "Bu oyunu evde ailenle oynasak hangi ritmi yapardın?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha basit ritim kalıpları ve daha yavaş tempo kullanılabilir. Hazır olan çocuklar için daha karmaşık ritimler oluşturma, farklı müzik aletleri deneme veya grup içinde liderlik yapma fırsatı verilebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte basit ritim oyunları oynamaları ve günlük nesnelerle ritim yapmaları önerilebilir. Çocuklar evde oluşturdukları bir ritmi sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların örüntü farkındalığı, ritim ve tempo duygusu, işitsel hafıza ve yaratıcı ifade becerilerini destekler. Ritim kalıpları oluşturma, çocukların müzikle etkileşim kurmalarını ve kendilerini ifade etmelerini sağlar."
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
        "assessment_questions": [
            "Hangi yoga duruşunu yaparken kendini en rahat hissettin?",
            "Derin nefes alıp verirken ne hissettin?",
            "Bu etkinlikte en çok neyi sevdin?",
            "Bu yoga hareketlerini evde ailenle birlikte yapmayı ister misin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha basit duruşlar ve daha kısa süreler kullanılabilir. Hazır olan çocuklar için daha karmaşık duruşlar, nefes teknikleri veya kısa bir meditasyon bölümü ekleme fırsatı verilebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte basit yoga hareketleri yapmaları ve nefes egzersizleri uygulamaları önerilebilir. Çocuklar evde denedikleri bir yoga duruşunu sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların beden farkındalığı, esneklik, denge, öz denetim ve farkındalık uygulama becerilerini destekler. Yoga ve nefes egzersizleri, çocukların sakinleşmelerine ve bedenlerini tanımalarına yardımcı olur."
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
        "assessment_questions": [
            "Bir arkadaşın seni nasıl hissettiriyor?",
            "İyi bir arkadaşın hangi davranışları gösterir?",
            "Seni mutlu eden bir arkadaşlık durumu var mı? Ne oldu?",
            "Arkadaşların seni nasıl destekliyor?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha basit arkadaşlık senaryoları ve daha fazla yönlendirme kullanılabilir. Hazır olan çocuklar için daha karmaşık sosyal durumlar ve tartışmalar için fırsatlar verilebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte arkadaşlık becerilerini geliştirecek oyunlar oynamaları ve sosyal etkileşimleri teşvik etmeleri önerilebilir. Çocuklar evde yaşadıkları sosyal deneyimleri sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların nezaket, empati, konuşma ve dinleme becerileri, olumlu akran ilişkileri ve özgüvenlerini destekler. Arkadaşlık temalı aktiviteler, çocukların sosyal becerilerini ve duygusal zekâlarını geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Hangi blokları kullanarak tasarımını yaptın?",
            "Tasarımında bir örüntü var mı? Varsa nasıl oluşturduğunu anlatabilir misin?",
            "Bu etkinlikte en çok neyi sevdin?",
            "Bu tasarımı evde tekrar yapmayı ister misin?"
        ],  
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha büyük bloklar ve daha basit tasarım kartları kullanılabilir. Hazır olan çocuklar için daha karmaşık örüntüler oluşturma, simetri ekleme veya kendi tasarım kartlarını yapma fırsatı verilebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte desen blokları veya benzeri materyallerle tasarımlar yapmaları önerilebilir. Çocuklar evde yaptıkları bir tasarımı sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların geometrik şekilleri tanıma, örüntü oluşturma, mekânsal akıl yürütme ve problem çözme becerilerini destekler. Desen bloklarıyla çalışma, çocukların matematiksel düşünme ve yaratıcılıklarını geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Kuklanı yaparken hangi malzemeleri kullandın?",
            "Kuklanın hikâyesi ne hakkında?",
            "Bu etkinlikte en çok neyi sevdin?",
            "Bu kukla gösterisini evde ailenle birlikte yapmayı ister misin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha basit kukla yapımı ve daha fazla yönlendirme sağlanabilir. Hazır olan çocuklar için daha karmaşık kuklalar yapma, hikâyeyi detaylandırma veya gösteride liderlik yapma fırsatı verilebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte basit kuklalar yapmaları ve kısa bir hikâye oluşturmaları önerilebilir. Çocuklar evde hazırladıkları bir kukla gösterisini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların yaratıcı hikâye anlatımı, sözlü dil gelişimi, iş birliği ve sunum becerilerini destekler. Kukla gösterisi hazırlama, çocukların hayal güçlerini kullanarak kendilerini ifade etmelerine ve sosyal becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Hangi renkleri karıştırdın ve hangi yeni rengi elde ettin?",
            "Renk karıştırırken ne hissettin?",
            "Bu etkinlikte en çok neyi sevdin?",
            "Bu renk karıştırma deneyini evde ailenle birlikte yapmayı ister misin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az renk seçeneği ve daha basit karışım yönergeleri kullanılabilir. Hazır olan çocuklar için daha karmaşık renk karışımları yapma, renk teorisi hakkında konuşma veya kendi renk karışım tablolarını oluşturma fırsatı verilebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte renk karıştırma deneyleri yapmaları ve yeni renkler keşfetmeleri önerilebilir. Çocuklar evde yaptıkları bir renk karışımını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların renk bilgisi temelleri, tahmin ve gözlem becerisi, ince motor gelişimi ve bilimsel süreç farkındalığını destekler. Renk karıştırma sihri, çocukların renklerle etkileşim kurmalarını ve yaratıcılıklarını geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Hangi nesneler mıknatısa yapıştı, hangileri yapışmadı?",
            "Bu sonuçları tahmin ederken ne düşündün?",
            "Bu etkinlikte en çok neyi sevdin?",
            "Bu mıknatıs keşfini evde ailenle birlikte yapmayı ister misin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az nesne seçeneği ve daha belirgin mıknatıs tepkileri kullanılabilir. Hazır olan çocuklar için daha karmaşık nesneler test etme, sonuçları grafikleştirme veya mıknatısın çekim gücünü ölçme gibi ek görevler verilebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte mıknatıslar ve çeşitli nesnelerle deneyler yapmaları önerilebilir. Çocuklar evde yaptıkları bir mıknatıs keşfini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların bilimsel sorgulama, maddelerin özelliklerini tanıma, tahmin etme ve test etme, sınıflandırma becerilerini destekler. Mıknatıs keşfi, çocukların fiziksel dünyayı anlamalarına ve bilimsel düşünme becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Hangi çalgıyı çalarken en çok eğlendin?",
            "Müzik eşliğinde yürürken ne hissettin?",
            "Bu etkinlikte en çok neyi sevdin?",
            "Bu çalgı geçidini evde ailenle birlikte yapmayı ister misin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha basit çalgılar ve daha yavaş tempolar kullanılabilir. Hazır olan çocuklar için daha karmaşık çalgılar, farklı ritim kalıpları deneme veya grup içinde liderlik yapma fırsatı verilebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte basit ritim çalgıları yapmaları ve müzik eşliğinde hareket etmeleri önerilebilir. Çocuklar evde yaptıkları bir çalgı geçidini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların ritim ve tempo farkındalığı, çalgıları tanıma, koordinasyon ve müzikal ifade becerilerini destekler. Çalgı geçidi etkinliği, çocukların müzikle etkileşim kurmalarını ve kendilerini ifade etmelerini sağlar."
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
        "assessment_questions": [
            "Denge becerinizi nasıl geliştirdiniz?",
            "En çok hangi denge görevini sevdiniz?",
            "Etkinlik sırasında seni en çok ne şaşırttı?",
            "Yaptığın çalışmada en çok hangi ayrıntıyı sevdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte denge becerilerini geliştirmek için basit denge oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları denge etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların denge ve vücut kontrolü, merkez kas gücü, odaklanma ve dikkat, beden farkındalığı becerilerini destekler. Denge becerisi oyunu, çocukların fiziksel yeteneklerini ve koordinasyonlarını geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Sayı sıralamasını nasıl öğrendiniz?",
            "En çok hangi sayı sıralama görevini sevdiniz?",
            "Etkinlik sırasında seni en çok ne şaşırttı?",
            "Evde ailenizle birlikte sayı sıralama becerilerinizi geliştirmek için ne yapabilirsiniz?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte sayı sıralama becerilerini geliştirmek için basit sayı sıralama oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları sayı sıralama etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların sayı sıralaması, 1-10 arası sayı tanıma, dikkat ve odaklanma, görsel sıralama becerilerini destekler. Sayı treni etkinliği, çocukların matematiksel düşünme becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Sayı dizisini nasıl öğrendiniz?",
            "En çok hangi eksik sayı bulma görevini sevdiniz?",
            "Etkinlik sırasında seni en çok ne şaşırttı?",
            "Yaptığın çalışmada en çok hangi ayrıntıyı sevdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte sayı dizisi becerilerini geliştirmek için basit sayı dizisi oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları sayı dizisi etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların sayı dizisini anlama, eksik öğeyi bulma, mantıksal düşünme ve sayı farkındalığı becerilerini destekler. Eksik sayı bulma etkinliği, çocukların matematiksel düşünme becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Büyük-küçük kavramını nasıl öğrendiniz?",
            "En çok hangi karşılaştırma görevini sevdiniz?",
            "Etkinlik sırasında seni en çok ne şaşırttı?",
            "Evde ailenizle birlikte büyük-küçük kavramını geliştirmek için ne yapabilirsiniz?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte büyük-küçük kavramını geliştirmek için basit karşılaştırma oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları karşılaştırma etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların büyük-küçük kavramını anlama, karşılaştırma becerisi, sınıflandırma ve matematiksel dil kullanımı becerilerini destekler. Büyük-Küçük karşılaştırma etkinliği, çocukların matematiksel düşünme becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Örüntü farkındalığını nasıl öğrendiniz?",
            "En çok hangi desen tamamlama görevini sevdiniz?",
            "Etkinlik sırasında seni en çok ne şaşırttı?",
            "Yaptığın çalışmada en çok hangi ayrıntıyı sevdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte örüntü farkındalığını geliştirmek için basit örüntü oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları örüntü etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların örüntü farkındalığını anlama, görsel dikkat, tahmin becerisi ve matematiksel düşünme becerilerini destekler. Desen tamamlama etkinliği, çocukların matematiksel düşünme becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Sayı-sembol ilişkisini nasıl öğrendiniz?",
            "En çok hangi nesne eşleştirme görevini sevdiniz?",
            "Bu etkinlikte en çok neyi öğrendiniz?",
            "Evde ailenizle birlikte sayı-sembol ilişkisini geliştirmek için ne yapabilirsiniz?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte sayı-sembol ilişkisini geliştirmek için basit sayı-sembol oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları sayı-sembol etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların sayı-sembol ilişkisini anlama, birebir eşleştirme, sayma ve dikkat geliştirme becerilerini destekler. Nesne say ve eşleştir etkinliği, çocukların matematiksel düşünme becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Şekil tanıma becerisini nasıl geliştirdiniz?",
            "En çok hangi şekil eşleştirme görevini sevdiniz?",
            "Hangi bölümü tekrar yapmak isterdin?",
            "Yaptığın çalışmada en çok hangi ayrıntıyı sevdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte şekil tanıma becerisini geliştirmek için basit şekil oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları şekil etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların şekil tanıma becerilerini, mekansal farkındalığını, dinleme becerilerini ve hareketle öğrenme becerilerini destekler. Şekil Yolculuğu etkinliği, çocukların matematiksel düşünme becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Sayı miktar ilişkisini nasıl öğrendiniz?",
            "En çok hangi kule oluşturma görevini sevdiniz?",
            "Hangi bölümü tekrar yapmak isterdin?",
            "Evde ailenizle birlikte sayı miktar ilişkisini geliştirmek için ne yapabilirsiniz?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte sayı miktar ilişkisini geliştirmek için basit sayı miktar oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları sayı miktar etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların sayı miktar ilişkisini anlama, ince motor becerilerini ve karşılaştırma becerilerini destekler. Sayı Kulesi Yapımı etkinliği, çocukların matematiksel düşünme becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Renk sınıflandırma becerisini nasıl geliştirdiniz?",
            "En çok hangi renk eşleştirme görevini sevdiniz?",
            "Bu etkinlikte en çok neyi öğrendiniz?",
            "Yaptığın çalışmada en çok hangi ayrıntıyı sevdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte renk sınıflandırma becerisini geliştirmek için basit renk oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları renk etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların renk sınıflandırma becerilerini, sayma becerilerini ve karşılaştırma becerilerini destekler. Renkli Boncuk Sıralama etkinliği, çocukların matematiksel düşünme becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Sayı sıralamasını nasıl öğrendiniz?",
            "En çok hangi gün sıralama görevini sevdiniz?",
            "Hangi bölümü tekrar yapmak isterdin?",
            "Evde ailenizle birlikte gün ve tarih farkındalığını geliştirmek için ne yapabilirsiniz?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte gün ve tarih farkındalığını geliştirmek için basit takvim oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları takvim etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların gün ve tarih farkındalığını, sayı sıralamasını ve tahmin etme becerilerini destekler. Takvimde Sayılar etkinliği, çocukların matematiksel düşünme becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Kaç adım uzaklık ölçme becerisini nasıl geliştirdiniz?",
            "En çok hangi hedefe adım sayma görevini sevdiniz?",
            "Hangi bölümü tekrar yapmak isterdin?",
            "Yaptığın çalışmada en çok hangi ayrıntıyı sevdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha kısa mesafeler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha uzun mesafeler ve farklı hedefler ekleyerek zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte standart olmayan ölçme becerilerini geliştirmek için basit adım sayma oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları ölçme etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların standart olmayan ölçme becerilerini, sayma becerilerini, karşılaştırma yapma becerilerini ve mekansal farkındalıklarını destekler. Kaç Adım Uzaklıkta etkinliği, çocukların matematiksel düşünme becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Kafiye kavramını nasıl öğrendiniz?",
            "En çok hangi kafiye eşleştirme görevini sevdiniz?",
            "Etkinlik sırasında seni en çok ne şaşırttı?",
            "Evde ailenizle birlikte kafiye farkındalığınızı geliştirmek için ne yapabilirsiniz?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte kafiye farkındalığını geliştirmek için basit kafiye oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları kafiye etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların ses farkındalığını, kafiye tanıma becerilerini, dinleme becerilerini ve kelime dağarcıklarını destekler. Kafiye Avı etkinliği, çocukların dil ve sözlü iletişim becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Hikaye kurma becerisini nasıl geliştirdiniz?",
            "En çok hangi hikaye kurma görevini sevdiniz?",
            "Bu çalışmada zorlandığın bir yer oldu mu?",
            "Yaptığın çalışmada en çok hangi ayrıntıyı sevdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte hikaye kurma becerilerini geliştirmek için basit hikaye oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları hikaye etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların sözlü anlatım becerilerini, sıralı düşünme becerilerini, hayal gücünü ve dinleme-behavior becerilerini destekler. Resimden Hikaye Kur etkinliği, çocukların dil ve sözlü iletişim becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Ses ayırt etme becerisini nasıl geliştirdiniz?",
            "En çok hangi ses ayırt etme görevini sevdiniz?",
            "Bu çalışmada zorlandığın bir yer oldu mu?",
            "Evde ailenizle birlikte ses ayırt etme becerilerinizi geliştirmek için ne yapabilirsiniz?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte ses ayırt etme becerilerini geliştirmek için basit ses oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları ses etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların başlangıç sesini ayırt etme becerilerini, harf-ses ilişkisini, kelime farkındalığını ve dikkat becerilerini destekler. Ses Kutusunu Bul etkinliği, çocukların dil ve sözlü iletişim becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Hikaye sıralama becerisini nasıl geliştirdiniz?",
            "En çok hangi hikaye sıralama görevini sevdiniz?",
            "Bu çalışmada zorlandığın bir yer oldu mu?",
            "Yaptığın çalışmada en çok hangi ayrıntıyı sevdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte hikaye sıralama becerilerini geliştirmek için basit hikaye oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları hikaye etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların olay sıralama becerilerini, hikaye anlama becerilerini, mantıksal düşünme becerilerini ve sözlü ifade becerilerini destekler. Hikaye Sıralama Kartları etkinliği, çocukların dil ve sözlü iletişim becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Kelime dağarcığınızı nasıl geliştirdiniz?",
            "En çok hangi kelime üretme görevini sevdiniz?",
            "Bu çalışmada zorlandığın bir yer oldu mu?",
            "Yaptığın çalışmada en çok hangi ayrıntıyı sevdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte kelime dağarcığını geliştirmek için basit kelime oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları kelime etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların kelime dağarcığını geliştirme becerilerini, tematik kavram öğrenimlerini, sıra alma becerilerini ve sözlü ifade becerilerini destekler. Kelime Sepeti etkinliği, çocukların dil ve sözlü iletişim becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Ses ayırt etme becerisini nasıl geliştirdiniz?",
            "En çok hangi ses ayırt etme görevini sevdiniz?",
            "Bu çalışmada zorlandığın bir yer oldu mu?",
            "Yaptığın çalışmada en çok hangi ayrıntıyı sevdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte ses ayırt etme becerilerini geliştirmek için basit ses oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları ses etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların başlangıç sesini ayırt etme becerilerini, harf-ses ilişkisini, kelime farkındalığını ve dikkat becerilerini destekler. Ses Kutusunu Bul etkinliği, çocukların dil ve sözlü iletişim becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Cümle kurma becerisini nasıl geliştirdiniz?",
            "En çok hangi cümle tamamlama görevini sevdiniz?",
            "Bu çalışmada zorlandığın bir yer oldu mu?",
            "Evde ailenizle birlikte cümle kurma becerilerinizi geliştirmek için ne yapabilirsiniz?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte cümle kurma becerilerini geliştirmek için basit cümle oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları cümle etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların cümle kurma becerilerini, anlamlı ifade geliştirme becerilerini, dinleme ve düşünme becerilerini ve kelime seçimi becerilerini destekler. Cümleyi Tamamla etkinliği, çocukların dil ve sözlü iletişim becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Rol alma becerisini nasıl geliştirdiniz?",
            "En çok hangi karakterle konuşma görevini sevdiniz?",
            "Bu çalışmada zorlandığın bir yer oldu mu?",
            "Başlamadan önce ne tahmin etmiştin, sonuç nasıl oldu?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha basit karakterler ve daha fazla rehberlik sağlanabilir. Hazır olan çocuklar için daha karmaşık karakterler ve özgür canlandırmalar teşvik edilebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte rol alma becerilerini geliştirmek için basit rol oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları rol etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların sözlü iletişim becerilerini, rol alma becerilerini, yaratıcı düşünme becerilerini ve karşılıklı konuşma becerilerini destekler. Rol Kartları ile Konuşma etkinliği, çocukların dil ve sosyal iletişim becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Kelime tanıma becerisini nasıl geliştirdiniz?",
            "En çok hangi resim-kelime eşleştirmesini sevdiniz?",
            "Bu çalışmada zorlandığın bir yer oldu mu?",
            "Başlamadan önce ne tahmin etmiştin, sonuç nasıl oldu?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte kelime tanıma becerilerini geliştirmek için basit kelime oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları kelime etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların kelime tanıma becerilerini, görsel-sözel eşleştirme becerilerini, kelime dağarcığı gelişimini ve dikkat becerilerini destekler. Resimli Kelime Eşleştirme etkinliği, çocukların dil ve sözlü iletişim becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Yeni kelime öğrenme becerisini nasıl geliştirdiniz?",
            "En çok hangi cümlede kelimeyi kullandınız?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Başlamadan önce ne tahmin etmiştin, sonuç nasıl oldu?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte yeni kelimeleri öğrenmek için basit kelime oyunları oynamaları önerilebilir. Çocuklar evde yaptıkları kelime etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların yeni kelime öğrenme becerilerini, kelimeyi bağlam içinde kullanma becerilerini, sözlü ifade becerilerini ve dil gelişimini destekler. Günün Kelimesi etkinliği, çocukların dil ve sosyal iletişim becerilerini geliştirmelerine yardımcı olur."
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
        "assessment_questions": [
            "Yaratıcı ifade becerisini nasıl geliştirdiniz?",
            "En çok hangi resmi oluşturdunuz?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Başlamadan önce ne tahmin etmiştin, sonuç nasıl oldu?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte yaratıcı ifade becerilerini geliştirmek için basit resim etkinlikleri yapmaları önerilebilir. Çocuklar evde yaptıkları resim etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların yaratıcı ifade becerilerini, renk farkındalığını, duyu temelli keşif becerilerini ve ince motor kontrolünü destekler. Parmak Boyası Bahçesi etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Doğal materyallerle sanat çalışması yaparken ne öğrendiniz?",
            "En çok hangi deseni oluşturdunuz?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Başlamadan önce ne tahmin etmiştin, sonuç nasıl oldu?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte doğadan nesneler kullanarak sanat çalışmalarında bulunmaları önerilebilir. Çocuklar evde yaptıkları sanat etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların doğal materyallerle sanat çalışması yapma becerilerini, desen farkındalığını, gözlem becerilerini ve yaratıcılığını destekler. Yaprak Baskısı etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Yaratıcı tasarım becerisini nasıl geliştirdiniz?",
            "En çok hangi maskeyi oluşturdunuz?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Evde ailenizle birlikte maskeler yapmak için ne yapabilirsiniz?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte yaratıcı tasarım becerilerini geliştirmek için basit maskeler yapmaları önerilebilir. Çocuklar evde yaptıkları maskeleri sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların yaratıcı tasarım becerilerini, ince motor becerilerini, parça-bütün ilişkisi kurma becerilerini ve kendini ifade etme becerilerini destekler. Kağıt Tabak Maskeleri etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Doğal materyallerle sanat çalışması yaparken ne öğrendiniz?",
            "En çok hangi resmi oluşturdunuz?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Başlamadan önce ne tahmin etmiştin, sonuç nasıl oldu?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte doğadan nesneler kullanarak sanat çalışmalarında bulunmaları önerilebilir. Çocuklar evde yaptıkları sanat etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların doğal materyallerle sanat çalışması yapma becerilerini, desen farkındalığını, gözlem becerilerini ve yaratıcılığını destekler. Pamukla Bulut Resmi etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Geri dönüşüm malzemeleriyle sanat çalışması yaparken ne öğrendiniz?",
            "En çok hangi heykeli oluşturdunuz?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Evde ailenizle birlikte atık malzemeler kullanarak sanat çalışmalarında bulunabilirsiniz?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte geri dönüşüm malzemeleriyle sanat çalışmalarında bulunmaları önerilebilir. Çocuklar evde yaptıkları sanat etkinliklerini sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların geri dönüşüm malzemeleriyle sanat çalışması yapma becerilerini, üç boyutlu düşünme becerilerini, yaratıcılığını ve problem çözme becerilerini destekler. Geri Dönüşüm Heykelleri etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Sünger baskı tekniğiyle çalışırken ne öğrendiniz?",
            "En çok hangi deseni oluşturdunuz?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Başlamadan önce ne tahmin etmiştin, sonuç nasıl oldu?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte sünger baskıları yapmaları önerilebilir. Çocuklar evde yaptıkları baskıları sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların sünger baskı tekniğini öğrenmesini, desen oluşturma becerilerini, renk kullanımı becerilerini ve el-göz koordinasyonunu destekler. Sünger Baskı Desenleri etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Duygularınızı renklerle nasıl ifade ettiniz?",
            "En çok hangi duyguyu hissettiniz?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Evde ailenizle birlikte duygularınızı renklerle ilişkilendirebilirsiniz?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte duygularınızı renklerle ilişkilendirebilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların duyguları ifade etme becerilerini, renk-duygu ilişkisi kurma becerilerini ve yaratıcı anlatım becerilerini destekler. Duygu Renkleri Posteri etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Şehir manzarası oluşturma etkinliğinde ne öğrendiniz?",
            "En çok hangi bina ve yolu oluşturdunuz?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Başlamadan önce ne tahmin etmiştin, sonuç nasıl oldu?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte şehir manzaraları oluşturmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların kesme-yapıştırma becerilerini, mekansal düzenleme becerilerini, şekilleri kullanma becerilerini ve yaratıcı tasarım becerilerini destekler. Kolaj Şehir Manzarası etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Şapka tasarlama etkinliğinde ne öğrendiniz?",
            "En çok hangi süslemeyi oluşturdunuz?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Evde ailenizle birlikte şapka tasarlayabilirsiniz?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte şapkalar tasarlamaları önerilebilir. Çocuklar evde yaptıkları şapkaları sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların tasarım becerilerini, kendini ifade etme becerilerini, ince motor gelişimini ve yaratıcılığını destekler. Hayalimdeki Şapka etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Mozaik kağıt resmi etkinliğinde ne öğrendiniz?",
            "En çok hangi renkleri kullandınız?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Başlamadan önce ne tahmin etmiştin, sonuç nasıl oldu?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte mozaik resimler oluşturmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların parça-bütün ilişkisi kurma becerilerini, dikkat ve sabır becerilerini, renk uyumu oluşturma becerilerini ve ince motor gelişimini destekler. Mozaik Kağıt Resmi etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Işık ve gölge ilişkisini keşfetme etkinliğinde ne öğrendiniz?",
            "En çok hangi nesnelerin gölgesini gözlemlediniz?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Başlamadan önce ne tahmin etmiştin, sonuç nasıl oldu?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte ışık ve gölge etkinlikleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların ışık ve gölge ilişkisini fark etme becerilerini, gözlem yapma becerilerini, karşılaştırma becerilerini ve bilimsel merak geliştirme becerilerini destekler. Işık ve Gölge İlişkisi etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Suyun yolculuğu etkinliğinde ne öğrendiniz?",
            "En çok hangi yüzeyde suyun hareketini gözlemlediniz?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Evde ailenizle birlikte su hareketi etkinlikleri yapabilirsiniz?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte su hareketi etkinlikleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların su hareketini gözlemleme becerilerini, tahmin yapma becerilerini, neden-sonuç ilişkisi kurma becerilerini ve bilimsel keşif becerilerini destekler. Suyun Yolculuğu etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Hava dolu mu boş mu etkinliğinde ne öğrendiniz?",
            "En çok hangi nesnelerin havasını gözlemlediniz?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Bu etkinlikte hangi malzeme en çok ilgini çekti?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte hava etkinlikleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların havanın varlığını fark etme becerilerini, gözlem yapma becerilerini, tahmin ve sonuç çıkarma becerilerini ve bilimsel kavramları anlamlandırma becerilerini destekler. Hava Dolu mu Boş mu etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Buzun erime yarışı etkinliğinde ne öğrendiniz?",
            "En çok hangi koşullarda buzun eridiğini gözlemlediniz?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Bu etkinlikte hangi malzeme en çok ilgini çekti?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte buz erime etkinlikleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların buzun erime sürecini gözlemleme becerilerini, tahmin yapma becerilerini, karşılaştırma becerilerini ve bilimsel süreç farkındalığını destekler. Buzun Erime Yarışı etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Toprakta neler var etkinliğinde ne öğrendiniz?",
            "En çok hangi parçacıkları gözlemlediniz?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Bu etkinlikte hangi malzeme en çok ilgini çekti?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte toprak inceleme etkinlikleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların toprak içindeki küçük parçaları gözlemleme becerilerini, tahmin yapma becerilerini, sınıflandırma becerilerini ve doğa farkındalığını destekler. Toprakta Neler Var etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Ses titreşimi etkinliğinde ne öğrendiniz?",
            "En çok hangi nesnelerin titreşimini gözlemlediniz?",
            "Bu etkinlikte en çok neyi öğrendiniz?",
            "Bu etkinlikte hangi malzeme en çok ilgini çekti?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte ses titreşimi etkinlikleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların ses ve titreşim ilişkisini fark etme becerilerini, dinleme ve gözlem yapma becerilerini, bilimsel keşif becerilerini ve neden-sonuç ilişkisi kurma becerilerini destekler. Ses Titreşimi Deneyi etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Yağmur bulutu kavanozu etkinliğinde ne öğrendiniz?",
            "En çok hangi koşullarda bulut oluştuğunu gözlemlediniz?",
            "Arkadaşına bu etkinliği nasıl anlatırsın?",
            "Bu etkinlikte hangi malzeme en çok ilgini çekti?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte yağmur bulutu etkinlikleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların bulut ve yağmur oluşumlarını gözlemleme becerilerini, tahmin yapma becerilerini, karşılaştırma becerilerini ve bilimsel süreç farkındalığını destekler. Yağmur Bulutu Kavanozu etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Meyve çekirdeği inceleme etkinliğinde ne öğrendiniz?",
            "En çok hangi meyvenin çekirdeklerini gözlemlediniz?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bu etkinlikte hangi malzeme en çok ilgini çekti?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte meyve çekirdeği etkinlikleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların meyve çekirdeklerini gözlemleme becerilerini, tahmin yapma becerilerini, karşılaştırma becerilerini ve doğa farkındalığını destekler. Meyve Çekirdeği İncelemesi etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Renkli süt deneyi etkinliğinde ne öğrendiniz?",
            "En çok hangi renklerin hareketini gözlemlediniz?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bu etkinlikte hangi malzeme en çok ilgini çekti?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte renkli süt etkinlikleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların kimyasal değişimi gözlemleme becerilerini, renk hareketlerini inceleme becerilerini, tahmin ve gözlem yapma becerilerini ve bilimsel merak geliştirme becerilerini destekler. Renkli Süt Deneyi etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Ağır mı hafif mi etkinliğinde ne öğrendiniz?",
            "En çok hangi nesnelerin ağırlığını gözlemlediniz?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bu etkinlikte hangi malzeme en çok ilgini çekti?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte ağırlık karşılaştırma etkinlikleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların ağırlık farkını anlama becerilerini, tahmin etme becerilerini, karşılaştırma yapma becerilerini ve gözlem becerilerini destekler. Ağır mı Hafif mi etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Hızlı mı Yavaş mı etkinliğinde ne öğrendiniz?",
            "En çok hangi müziklerin tempolarını gözlemlediniz?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bu etkinlikte hangi malzeme en çok ilgini çekti?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte hız ve yavaş müzik etkinlikleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların müzikal tempoları farkındalığıni, dinleme becerilerini, hareket koordinasyonunu ve müzikal kavramları tanıma becerilerini destekler. Hızlı mı Yavaş mı etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Sesli Sessiz Oyunu etkinliğinde ne öğrendiniz?",
            "En çok hangi seslerin yüksek veya yumuşak olduğunu gözlemlediniz?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bu etkinlikte hangi malzeme en çok ilgini çekti?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte sesli sessiz oyunları yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların ses yüksekliğini ayırt etme becerilerini, dikkat toplama becerilerini, yönerge takip etme becerilerini ve ritim duygusu geliştirme becerilerini destekler. Sesli Sessiz Oyunu etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Hayvan Sesleri Orkestrası etkinliğinde ne öğrendiniz?",
            "En çok hangi hayvan seslerini gözlemlediniz?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bu etkinlikte hangi malzeme en çok ilgini çekti?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte hayvan sesleri orkestrası yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların işitsel farkındalıklarını, ritim oluşturma becerilerini, taklit becerilerini ve grup içinde uyum sağlama becerilerini destekler. Hayvan Sesleri Orkestrası etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Davulunu Dinle etkinliğinde ne öğrendiniz?",
            "En çok hangi ritimleri gözlemlediniz?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bu etkinlikte hangi malzeme en çok ilgini çekti?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte davul ritimleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların işitsel hafızalarını, ritim tekrarı becerilerini, dikkat ve odaklanma becerilerini ve müzikal ifade becerilerini destekler. Davulunu Dinle etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Müzikle Duygu Yüzleri etkinliğinde ne öğrendiniz?",
            "En çok hangi duyguları hissettiniz?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bu etkinlikte hangi malzeme en çok ilgini çekti?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte müzikle duygu ifade etme aktiviteleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların müzik ve duygu ilişkisini fark etme becerilerini, duygu ifade etme becerilerini, dinleme becerilerini ve yaratıcı tepki verme becerilerini destekler. Müzikle Duygu Yüzleri etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Çıngırak Yapımı ve Çalma etkinliğinde ne öğrendiniz?",
            "En çok hangi ritimleri gözlemlediniz?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Evde ailenizle birlikte çıngıraklar yapabilirsiniz?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte çıngırak yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların ses üretme keşfi becerilerini, ritim becerilerini, yaratıcı tasarım becerilerini ve ince motor gelişimlerini destekler. Çıngırak Yapımı ve Çalma etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Şarkının Sonunu Tahmin Et etkinliğinde ne öğrendiniz?",
            "En çok hangi şarkıları hatırladınız?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bir dahaki sefere neyi farklı yapmak isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte şarkı sözlerini tamamlamak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların işitsel hafızalarını, şarkı sözlerini hatırlama becerilerini, dikkat becerilerini ve müzikal katılım becerilerini destekler. Şarkının Sonunu Tahmin Et etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Ritimle İsim Söyleme etkinliğinde ne öğrendiniz?",
            "En çok hangi isimleri hatırladınız?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bir dahaki sefere neyi farklı yapmak isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte isimleri ritimle söylemek için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların ritim farkındalıklarını, isim tanıma becerilerini, grup katılımı becerilerini ve işitsel tekrar becerilerini destekler. Ritimle İsim Söyleme etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Müzikli Hikaye Yolculuğu etkinliğinde ne öğrendiniz?",
            "En çok hangi müzikal etkileri gözlemlediniz?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bir dahaki sefere neyi farklı yapmak isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte hikayeler anlatmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların dinleme ve anlama becerilerini, müzikle anlatımı destekleme becerilerini, yaratıcı katılım becerilerini ve grup içinde iş birliği becerilerini destekler. Müzikli Hikaye Yolculuğu etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Melodi Takibi etkinliğinde ne öğrendiniz?",
            "En çok hangi ses sıralarını hatırladınız?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bir dahaki sefere neyi farklı yapmak isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte melodi takibi yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların ses sırasını fark etme becerilerini, işitsel dikkat becerilerini, melodi takibi becerilerini ve müziksel hafıza becerilerini destekler. Melodi Takibi etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Renkli Halka Sıçraması etkinliğinde ne öğrendiniz?",
            "En çok hangi renkleri hatırladınız?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bir dahaki sefere neyi farklı yapmak isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte renkli halka sıçraması yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların denge becerilerini, koordinasyon becerilerini, yönerge takip etme becerilerini ve kaba motor gelişimlerini destekler. Renkli Halka Sıçraması etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Yavaş Hızlı Yürü etkinliğinde ne öğrendiniz?",
            "En çok hangi yürüyüş türlerini gözlemlediniz?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bir dahaki sefere neyi farklı yapmak isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte yavaş hızlı yürüme aktiviteleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların beden kontrolü becerilerini, dinleme becerilerini, hareket farkındalığı becerilerini ve kaba motor koordinasyonlarını destekler. Yavaş Hızlı Yürü etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Topu Hedefe Yuvarla etkinliğinde ne öğrendiniz?",
            "En çok hangi hedefleri başarıyla tamamladınız?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bir dahaki sefere neyi farklı yapmak isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte topu hedefe yuvarlama aktiviteleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların el-göz koordinasyonunu, hedefe yönelme becerisini, dikkat geliştirme becerilerini ve kaba motor becerilerini destekler. Topu Hedefe Yuvarla etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Hayvan Yürüyüşleri etkinliğinde ne öğrendiniz?",
            "En çok hangi hayvan yürüyüşlerini gözlemlediniz?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bir dahaki sefere neyi farklı yapmak isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte hayvan yürüyüşleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların beden farkındalığı becerilerini, taklit becerilerini, kaba motor gelişimlerini ve yaratıcı hareket becerilerini destekler. Hayvan Yürüyüşleri etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Denge Yolu etkinliğinde ne öğrendiniz?",
            "En çok hangi dengeli yürüyüşleri gözlemlediniz?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bir dahaki sefere neyi farklı yapmak isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte denge yolu aktiviteleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların dengeli yürüyüş becerilerini, beden kontrolünü, odaklanma becerilerini ve koordinasyonlarını destekler. Denge Yolu etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Yastık Adaları etkinliğinde ne öğrendiniz?",
            "En çok hangi adaları geçtiniz?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bir dahaki sefere neyi farklı yapmak isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte yastık adası aktiviteleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların sıçrama becerilerini, dengesini ve koordinasyonlarını, mekansal farkındalığını ve kaba motor gelişimlerini destekler. Yastık Adaları etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Kuyruk Yakalama Oyunu etkinliğinde ne öğrendiniz?",
            "En çok hangi kuyrukları korudunuz?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bir dahaki sefere neyi farklı yapmak isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte kuyruk yakalama oyunları yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların hız ve çeviklik becerilerini, alan farkındalığını, kurallı oyun oynama becerilerini ve kaba motor gelişimlerini destekler. Kuyruk Yakalama Oyunu etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Tünelden Geç etkinliğinde ne öğrendiniz?",
            "En çok hangi tünelleri geçtiniz?",
            "Bugün öğrendiğin şeyi günlük hayatta nerede kullanabilirsin?",
            "Bir dahaki sefere neyi farklı yapmak isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte tünelden geçme aktiviteleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların sürünme becerilerini, kas koordinasyonunu, alan kullanımını ve kaba motor gelişimlerini destekler. Tünelden Geç etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Balon Havada Kalsın etkinliğinde ne öğrendiniz?",
            "En çok hangi balonları havada tuttunuz?",
            "Bu etkinlikte en çok neyi öğrendiniz?",
            "Bir dahaki sefere neyi farklı yapmak isterdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte balon havada kalsın aktiviteleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların el-göz koordinasyonunu, reflekslerini, dikkat ve takip becerilerini ve grup içinde iş birliğini destekler. Balon Havada Kalsın etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Taklit ve Don Oyunu etkinliğinde ne öğrendiniz?",
            "En çok hangi hareketleri taklit ettiniz?",
            "Bu etkinlikte en çok neyi öğrendiniz?",
            "Bu etkinliği daha eğlenceli yapmak için ne eklerdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte taklit ve don oyunları yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların taklit becerilerini, öz denetimini, dinleme ve dikkat becerilerini ve kaba motor gelişimlerini destekler. Taklit ve Don Oyunu etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Duygu Termometresi etkinliğinde ne öğrendiniz?",
            "En çok hangi duyguları fark ettiniz?",
            "Bu etkinlikte en çok neyi öğrendiniz?",
            "Bu etkinliği daha eğlenceli yapmak için ne eklerdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte duygularını ifade etme aktiviteleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların duygu farkındalığını, kendini ifade etme becerilerini, duyguları adlandırma becerilerini ve öz farkındalık geliştirme becerilerini destekler. Duygu Termometresi etkinliği, çocukların görsel ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Nazik Sözler Sepeti etkinliğinde ne öğrendiniz?",
            "En çok hangi nazik sözleri öğrendiniz?",
            "Bu etkinlikte en çok neyi öğrendiniz?",
            "Evde ailenizle birlikte nazik sözler kullanabilirsiniz?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte nazik sözleri kullanmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların nazik iletişim kurma becerilerini, sosyal farkındalığını, uygun dil kullanımı becerilerini ve akran ilişkilerini güçlendirme becerilerini destekler. Nazik Sözler Sepeti etkinliği, çocukların sosyal ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Sıra Bende Sıra Sende etkinliğinde ne öğrendiniz?",
            "En çok hangi sırayı beklediniz?",
            "Bu etkinlikte en çok neyi öğrendiniz?",
            "Bu etkinliği daha eğlenceli yapmak için ne eklerdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte sıra bekleme oyunları yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların sıra bekleme becerilerini, paylaşma alışkanlıklarını, sabır geliştirme becerilerini ve grup içinde uyum sağlama becerilerini destekler. Sıra Bende Sıra Sende etkinliği, çocukların sosyal ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Arkadaşına Yardım Et etkinliğinde ne öğrendiniz?",
            "En çok hangi yardımlaşma becerisini öğrendiniz?",
            "Bu etkinlikte en çok neyi öğrendiniz?",
            "Bu etkinliği daha eğlenceli yapmak için ne eklerdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte yardımlaşma oyunları yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların yardım isteme ve verme becerilerini, iş birliği yapma becerilerini, empati geliştirme becerilerini ve olumlu sosyal etkileşimleri destekler. Arkadaşına Yardım Et etkinliği, çocukların sosyal ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Ayna Duyguları etkinliğinde ne öğrendiniz?",
            "En çok hangi duyguları tanıdınız?",
            "Bu etkinlikte en çok neyi öğrendiniz?",
            "Bu etkinliği daha eğlenceli yapmak için ne eklerdin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte duygularını ifade etme aktiviteleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların yüz ifadelerini fark etme becerilerini, duyguları tanıma becerilerini, öz farkındalıklarını ve duygu ifadesi geliştirme becerilerini destekler. Ayna Duyguları etkinliği, çocukların sosyal ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Sorun Çözme Kartları etkinliğinde ne öğrendiniz?",
            "En çok hangi sorun çözme stratejilerini öğrendiniz?",
            "Bu etkinlikte en çok neyi öğrendiniz?",
            "Bu etkinliği daha eğlenceli yapmak için ne eklersin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte sorunlarla başa çıkma aktiviteleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların sorun çözme becerilerini, sosyal durumları değerlendirme becerilerini, duyguları yönetme becerilerini ve uygun çözüm üretme becerilerini destekler. Sorun Çözme Kartları etkinliği, çocukların sosyal ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Teşekkür Çiçeği etkinliğinde ne öğrendiniz?",
            "En çok kime veya neye teşekkür etmek istediğinizi öğrendiniz?",
            "Bu etkinlikte en çok neyi öğrendiniz?",
            "Bu etkinliği daha eğlenceli yapmak için ne eklersin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha az zorlukta görevler ve daha fazla tekrar yapılabilir. Hazır olan çocuklar için daha karmaşık görevler ve zorluk seviyeleri artırılabilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte teşekkür etme aktiviteleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların minnettarlık geliştirme becerilerini, olumlu düşünme becerilerini, kendini ifade etme becerilerini ve sosyal-duygusal farkındalıklarını destekler. Teşekkür Çiçeği etkinliği, çocukların sosyal ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Birlikte Nefes Al etkinliğinde ne öğrendiniz?",
            "En çok hangi nefes egzersizlerini beğendiniz?",
            "Bu etkinlikte en çok neyi öğrendiniz?",
            "Bu etkinliği daha eğlenceli yapmak için ne eklersin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha basit nefes egzersizleri ve daha fazla rehberlik sağlanabilir. Hazır olan çocuklar için daha uzun nefes tutma süreleri veya görselleştirme teknikleri eklenebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte nefes egzersizleri yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların sakinleşme becerilerini, öz düzenleme becerilerini, beden farkındalıklarını ve duygusal denge geliştirme becerilerini destekler. Birlikte Nefes Al etkinliği, çocukların sosyal ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Arkadaşını Dinle etkinliğinde ne öğrendiniz?",
            "En çok hangi arkadaşınızın söylediklerini hatırladınız?",
            "Bu etkinlikte en çok neyi öğrendiniz?",
            "Bu etkinliği daha eğlenceli yapmak için ne eklersin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha kısa paylaşımlar ve daha fazla rehberlik sağlanabilir. Hazır olan çocuklar için daha uzun paylaşımlar ve daha karmaşık sorular eklenebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte dinleme oyunları yapmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların aktif dinleme becerilerini, saygılı iletişim becerilerini, dikkat geliştirme becerilerini ve akranlarla olumlu etkileşim becerilerini destekler. Arkadaşını Dinle etkinliği, çocukların sosyal ve duyuşsal gelişimlerine yardımcı olur."
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
        "assessment_questions": [
            "Mutlu Anılar Panosu etkinliğinde ne öğrendiniz?",
            "En çok hangi mutlu anınızı çizdiniz?",
            "Bu etkinlikte en çok neyi öğrendiniz?",
            "Bu etkinliği daha eğlenceli yapmak için ne eklersin?"
        ],
        "differentiation_notes": "Daha fazla desteğe ihtiyaç duyan çocuklar için daha kısa paylaşımlar ve daha fazla rehberlik sağlanabilir. Hazır olan çocuklar için daha uzun paylaşımlar ve daha karmaşık sorular eklenebilir.",
        "family_community_notes": "Ailelere, evde çocuklarıyla birlikte mutlu anları paylaşmak için malzemeler sağlayabilirsiniz. Çocuklar evde yaptıkları çalışmalarını sınıfta paylaşabilir.",
        "learning_outcomes_summary": "Bu etkinlik, çocukların olumlu duygu farkındalıklarını, kendini ifade etme becerilerini, akran paylaşımı becerilerini ve sosyal bağ kurma becerilerini destekler. Mutlu Anılar Panosu etkinliği, çocukların sosyal ve duyuşsal gelişimlerine yardımcı olur."
    },
]



def seed_activities():
    app = create_app()

    with app.app_context():
        added_count = 0

        for item in ACTIVITIES:
            existing = Activity.query.filter_by(title=item["title"]).first()
            if existing:
                existing.subject = item["subject"]
                existing.duration = item["duration"]
                existing.group_size = item["group_size"]
                existing.description = item["description"]
                existing.materials = json.dumps(item["materials"], ensure_ascii=False)
                existing.instructions = json.dumps(item["instructions"], ensure_ascii=False)
                existing.learning_goals = json.dumps(item["learning_goals"], ensure_ascii=False)

                existing.assessment_questions = json.dumps(item.get("assessment_questions", []), ensure_ascii=False)
                existing.differentiation_notes = item.get("differentiation_notes")
                existing.family_community_notes = item.get("family_community_notes")
                existing.learning_outcomes_summary = item.get("learning_outcomes_summary")

                existing.source_type = "seed"
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
                assessment_questions=json.dumps(item.get("assessment_questions", []), ensure_ascii=False),
                differentiation_notes=item.get("differentiation_notes"),
                family_community_notes=item.get("family_community_notes"),
                learning_outcomes_summary=item.get("learning_outcomes_summary"),
            )

            db.session.add(activity)
            added_count += 1

        db.session.commit()
        print(f"{added_count} etkinlik eklendi.")


if __name__ == "__main__":
    seed_activities()