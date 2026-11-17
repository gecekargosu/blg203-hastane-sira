"""
BLG203 ara rapor ureteci (Hastane Hasta Sira ve Bekleme Sistemi).
HTML sablonunu doldurur, Chrome ile PDF'e cevirir, altbilgiyi pypdf ile basar.
Kullanim: python 00_Kapak/rapor_uret.py
"""
import math
import os
import re
import subprocess
import tempfile

import pypdf
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GECICI_PDF = os.path.join(tempfile.gettempdir(), "blg203_hastane_ham.pdf")
HEDEF_PDF = os.path.join(KOK, "Rapor.pdf")

BASLIK = "BLG203 Veri Yapıları Dönem Projesi  |  Cengiz Kılıç 251205027  |  Hastane Hasta Sıra ve Bekleme Sistemi"


def olcum_tablosu():
    yol = os.path.join(KOK, "03_Olcum", "benchmark.csv")
    with open(yol, encoding="utf-8") as dosya:
        satirlar = [s.strip().split(";") for s in dosya if s.strip()]
    veri = []
    for s in satirlar[1:]:
        veri.append({
            "boyut": s[0], "ek_liste": float(s[1]), "ek_agac": float(s[2]),
            "ar_liste": float(s[3]), "ar_agac": float(s[4]), "yukseklik": s[5],
        })
    return veri


def tablo_html(veri):
    satirlar = []
    for v in veri:
        oran = v["ar_liste"] / v["ar_agac"] if v["ar_agac"] > 0 else 0
        satirlar.append(
            "<tr><td>%s</td><td>%.3f</td><td>%.3f</td><td>%.3f</td><td>%.3f</td>"
            "<td>%s</td><td>%.0f</td></tr>"
            % (v["boyut"], v["ek_liste"], v["ek_agac"], v["ar_liste"],
               v["ar_agac"], v["yukseklik"], oran))
    return "\n".join(satirlar)


def grafik_html(veri):
    """Arama surelerini logaritmik olcekte yatay cubuklarla gosterir."""
    en_buyuk = max(max(v["ar_liste"], v["ar_agac"]) for v in veri)

    def genislik(deger):
        if deger <= 0:
            return 1.0
        oran = math.log10(deger * 1000.0) / math.log10(en_buyuk * 1000.0)
        return max(1.0, min(100.0, oran * 100.0))

    parcalar = []
    for v in veri:
        parcalar.append(
            '<div class="grafik-satir">'
            '<div class="grafik-etiket">%s hasta</div>'
            '<div class="grafik-cubuklar">'
            '<div class="cubuk liste" style="width:%.1f%%"><span>bagli liste %.2f ms</span></div>'
            '<div class="cubuk agac" style="width:%.1f%%"><span>agac %.2f ms</span></div>'
            '</div></div>'
            % (v["boyut"], genislik(v["ar_liste"]), v["ar_liste"],
               genislik(v["ar_agac"]), v["ar_agac"]))
    return "\n".join(parcalar)


def grafik_ekleme_html(veri):
    """Ekleme surelerini dogrusal olcekte karsilastirir."""
    en_buyuk = max(max(v["ek_liste"], v["ek_agac"]) for v in veri)

    def genislik(deger):
        return max(1.0, min(100.0, deger / en_buyuk * 100.0))

    parcalar = []
    for v in veri:
        parcalar.append(
            '<div class="grafik-satir">'
            '<div class="grafik-etiket">%s hasta</div>'
            '<div class="grafik-cubuklar">'
            '<div class="cubuk-satir"><div class="cubuk liste" style="width:%.1f%%"></div>'
            '<span class="deger">bagli liste %.2f ms</span></div>'
            '<div class="cubuk-satir"><div class="cubuk agac" style="width:%.1f%%"></div>'
            '<span class="deger">agac %.2f ms</span></div>'
            '</div></div>'
            % (v["boyut"], genislik(v["ek_liste"]), v["ek_liste"],
               genislik(v["ek_agac"]), v["ek_agac"]))
    return "\n".join(parcalar)


def grafik_yukseklik_html(veri):
    """Olculen agac yuksekligini dengeli agac beklentisiyle karsilastirir."""
    satirlar = []
    for v in veri:
        n = int(v["boyut"])
        olculen = int(v["yukseklik"])
        ideal = math.ceil(math.log2(n + 1))
        satirlar.append((v["boyut"], olculen, ideal))
    en_buyuk = max(max(o, i) for _, o, i in satirlar)

    def genislik(deger):
        return max(1.0, min(100.0, deger / en_buyuk * 100.0))

    parcalar = []
    for boyut, olculen, ideal in satirlar:
        parcalar.append(
            '<div class="grafik-satir">'
            '<div class="grafik-etiket">%s hasta</div>'
            '<div class="grafik-cubuklar">'
            '<div class="cubuk-satir"><div class="cubuk liste" style="width:%.1f%%"></div>'
            '<span class="deger">olculen yukseklik %d</span></div>'
            '<div class="cubuk-satir"><div class="cubuk agac" style="width:%.1f%%"></div>'
            '<span class="deger">dengeli agac beklentisi %d</span></div>'
            '</div></div>'
            % (boyut, genislik(olculen), olculen, genislik(ideal), ideal))
    return "\n".join(parcalar)


CSS = """
@page { size: A4; margin: 2.1cm 2.0cm 2.4cm 2.0cm; }
* { box-sizing: border-box; }
body { font-family: "Times New Roman", serif; font-size: 11pt; line-height: 1.15;
       color: #111; margin: 0; }
p { margin: 0 0 6pt 0; text-align: justify; orphans: 2; widows: 2; }
h1 { font-size: 13pt; color: #16365c; margin: 14pt 0 6pt 0; border-bottom: 1px solid #b9c7d8;
     padding-bottom: 2pt; page-break-after: avoid; break-after: avoid; }
h2 { font-size: 11.5pt; color: #1f4e79; margin: 10pt 0 4pt 0; page-break-after: avoid; }
ul, ol { margin: 0 0 7pt 0; padding-left: 16pt; }
li { margin-bottom: 2.5pt; text-align: justify; }
table { border-collapse: collapse; width: 100%; font-size: 9.3pt; margin: 4pt 0 9pt 0;
        page-break-inside: avoid; }
th { background: #e8eef5; border: 0.6pt solid #8fa8c0; padding: 3pt 4pt; text-align: left;
     font-weight: bold; }
td { border: 0.6pt solid #a8b8c8; padding: 2.6pt 4pt; vertical-align: top; }
tr { page-break-inside: avoid; break-inside: avoid; }
thead { display: table-header-group; }
.blok { page-break-inside: avoid; break-inside: avoid; }
tbody { page-break-inside: auto; break-inside: auto; }
.toc, .kapak table { page-break-inside: auto; break-inside: auto; }

code, pre { font-family: Consolas, "Courier New", monospace; }
pre { font-size: 8.6pt; background: #f4f6f8; border: 0.5pt solid #ccd6e0; border-left: 3pt solid #1f4e79;
      padding: 5pt 7pt; margin: 3pt 0 9pt 0; line-height: 1.25; white-space: pre-wrap;
      page-break-inside: avoid; }
.sema { font-size: 8.4pt; background: #fbfbfc; border: 0.5pt dashed #9aa; padding: 6pt 8pt;
        margin: 3pt 0 8pt 0; page-break-inside: avoid; }
.kucuk { font-size: 9pt; color: #333; }
figure { margin: 4pt 0 10pt 0; page-break-inside: avoid; }
figure img { width: 100%; border: 0.5pt solid #b0b0b0; }
figcaption { font-size: 9pt; color: #333; margin-top: 3pt; text-align: center; }
.grafik-satir { display: flex; align-items: center; margin-bottom: 5pt; }
.grafik-etiket { width: 82pt; font-size: 9pt; }
.grafik-cubuklar { flex: 1; }
.cubuk { height: 13pt; margin: 1.5pt 0; font-size: 8pt; color: #fff; padding-left: 4pt;
         line-height: 13pt; white-space: nowrap; }
.cubuk.liste { background: #a33; }
.cubuk.agac { background: #1f4e79; }
.cubuk span { font-family: Arial, sans-serif; }
.cubuk-satir { display: flex; align-items: center; margin: 1.5pt 0; }
.cubuk-satir .cubuk { height: 10pt; margin: 0; padding: 0; }
.deger { font-family: Arial, sans-serif; font-size: 8pt; color: #222;
         margin-left: 4pt; white-space: nowrap; }

/* Kapak */
.kapak { text-align: center; page-break-after: always; height: 24.5cm; position: relative; }
.kapak img.logo { width: 3.4cm; margin-top: 0.6cm; }
.kapak .uni { font-size: 11.5pt; font-weight: bold; line-height: 1.4; margin-top: 0.5cm;
              letter-spacing: 0.4pt; }
.kapak .ders { font-size: 12pt; margin-top: 2.2cm; font-weight: bold; }
.kapak .tur { font-size: 15pt; font-weight: bold; margin-top: 0.5cm; letter-spacing: 1pt; }
.kapak .proje { font-size: 16pt; font-weight: bold; margin: 1.6cm 0 0.2cm 0; color: #16365c;
                line-height: 1.35; }
.kapak .projealt { font-size: 11pt; font-style: italic; margin-bottom: 1.4cm; }
.kapak table { width: 11.5cm; margin: 0 auto; font-size: 10.5pt; }
.kapak td { border: none; padding: 2.6pt 4pt; }
.kapak td.b { text-align: right; font-weight: bold; width: 4.6cm; }
.kapak .tarih { margin-top: 1.3cm; font-size: 11pt; }

/* Icindekiler */
.icindekiler { page-break-after: always; }
.toc { width: 100%; border-collapse: collapse; margin: 6pt 0 0 0; font-size: 10.6pt; }
.toc td { border: none; padding: 2.1pt 0; vertical-align: bottom; }
.toc td.bas { border-bottom: 0.4pt dotted #c9c9c9; }
.toc td.no { width: 14mm; text-align: right; }
.toc tr.d1 td { font-weight: bold; padding-top: 7pt; color: #16365c; }
.toc tr.d2 td { padding-left: 8mm; }
"""

HTML = """<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><title>Ara Rapor</title>
<style>%(css)s</style></head><body>

<div class="kapak">
  <img class="logo" src="%(logo)s">
  <div class="uni">T.C.<br>İSTANBUL RUMELİ ÜNİVERSİTESİ<br>
  MÜHENDİSLİK VE DOĞA BİLİMLERİ FAKÜLTESİ<br>YAPAY ZEKÂ VE MAKİNE ÖĞRENMESİ BÖLÜMÜ</div>

  <div class="ders">BLG203 VERİ YAPILARI DERSİ</div>
  <div class="tur">DÖNEM PROJESİ ARA RAPORU</div>

  <div class="proje">HASTANE HASTA SIRA VE<br>BEKLEME SİSTEMİ</div>
  <div class="projealt">Bağlı liste ve kuyruk ile hasta sırası yönetimi, C dilinde gerçekleme</div>

  <table>
    <tr><td class="b">Öğrenci</td><td>Cengiz Kılıç</td></tr>
    <tr><td class="b">Öğrenci Numarası</td><td>251205027</td></tr>
    <tr><td class="b">Bölüm</td><td>Yapay Zekâ ve Makine Öğrenmesi</td></tr>
    <tr><td class="b">Grup No</td><td>— (bireysel proje)</td></tr>
    <tr><td class="b">Proje Türü</td><td>Bireysel proje</td></tr>
    <tr><td class="b">Programlama Dili</td><td>C (C11)</td></tr>
    <tr><td class="b">Teslim Tarihi</td><td>16 Kasım 2026</td></tr>
  </table>

  <div class="tarih">Kasım 2026</div>
</div>

%(icindekiler)s

<h1>1. Problem Tanımı</h1>

<p>Bir hastanede poliklinik hizmetinin düzenli yürümesi iki temel kaydın doğru yönetilmesine
bağlıdır. Birincisi hastanın kimlik ve iletişim bilgilerini taşıyan kalıcı kayıt defteri,
ikincisi o gün muayene olmayı bekleyen hastaların sırasıdır. Kayıt defteri dönem boyunca
büyür ve kayıtlar arasında numaraya göre arama sık yapılır. Bekleme sırası ise gün içinde
hızla oluşur ve dağılır, ancak sıranın bozulmaması hastane işleyişi açısından zorunludur.
Her iki kümeyi aynı yapı üzerinde tutmak ya aramayı yavaşlatır ya da sıra disiplinini
bozar. Bu projenin problemi, kayıt defteri ile bekleme sırasını birbirinden ayırarak her
birini kendi doğasına uygun veri yapısıyla yönetmek ve bu seçimi karmaşıklık analiziyle
savunmaktır.</p>

<p>Geliştirilen <b>Hastane Hasta Sıra ve Bekleme Sistemi</b>, komut satırından çalışan,
menü tabanlı bir C uygulamasıdır. Program açılışta hasta kayıtlarını noktalı virgülle
ayrılmış bir CSV dosyasından okur, kayıtları bellekte bağlı liste ve ikili arama ağacı
üzerinde birlikte tutar, muayene sırasını ayrı bir kuyrukta yönetir ve kapanırken güncel
kayıtları dosyaya geri yazar.</p>

<h2>1.1 Programın yapabildikleri</h2>
<ul>
  <li>Kayıt dosyasından toplu yükleme, bozuk satırları atlayarak okuma ve dosya yoksa
      çökmeyip kullanıcıyı uyarma</li>
  <li>Yeni hasta kaydı ekleme, kayıt silme ve hasta numarasına göre arama</li>
  <li>Kayıtları ağaç üzerinden numaraya göre artan sırada, bağlı liste üzerinden ise giriş
      sırasında listeleme, ağacın yüksekliğini ve düğüm sayısını raporlama</li>
  <li>Hastayı muayene sırasına alma, sıradaki hastayı çağırma ve muayeneyi bitirme</li>
  <li>Sıradaki hastaları ilk gelen ilk çıkar kuralıyla listeleme ve çağırma</li>
  <li>Son ekleme veya silme işlemini geri alma, geri alma yığıtı boşsa kullanıcıyı uyarma</li>
  <li>İkili arama ağacını ekrana yatay olarak çizme ve nöbetçi poliklinik turunu dairesel
      liste üzerinde ilerletme</li>
  <li>Kapanışta tüm kayıtları dosyaya yazma ve ayrılan tüm belleği serbest bırakma</li>
</ul>

<h2>1.2 Kapsam</h2>
<p>Proje, daha önce ders sorumlusuna bildirilen konu ve kapsam doğrultusunda hazırlanmıştır.
Bildirilen konu <i>Hastane Hasta Sıra ve Bekleme Sistemi</i> olup kayıtların TXT/CSV
dosyasından okunması, bağlı liste ve kuyruk ile bellekte yönetilmesi, yeni hasta ekleme,
sıradaki hastayı çağırma ve hasta arama ile farklı veri boyutlarında arama ve listeleme
performansının ölçülmesi istenmiştir. Bu isteklerin tamamı ara sürümde çalışır durumdadır.
Proje ayrıca dersin ilk yedi haftasında işlenen konularla sınırlandırılmış, yığın (heap),
hash tablosu, çizge algoritmaları ve sıralama algoritmaları final sürümüne bırakılmıştır.
Arama performansını ölçebilmek için yedinci haftada işlenen ikili ağaç yapısı, arama
anahtarına göre düzenlenerek ikili arama ağacı biçiminde kullanılmıştır.</p>

<h2>1.3 Varsayımlar ve sınırlar</h2>
<p>Projenin sınırları belirli varsayımlar üzerine kurulmuştur. Bu varsayımlar hem tasarımı
hem de ölçümleri doğrudan etkilediği için açıkça yazılmıştır.</p>
<ul>
  <li>Her hasta numarası benzersizdir, aynı numarayla ikinci kayıt eklenmez</li>
  <li>Kayıtlar noktalı virgülle ayrılmış metin dosyasında tutulur, ad alanındaki boşluk
      ayrıştırmayı bozmaz</li>
  <li>Program tek kullanıcı içindir, eşzamanlı erişim ve kilit mekanizması kapsam dışıdır</li>
  <li>Test verisi 1200 kayıttır, performans ölçümünde 100 000 kayda kadar çıkılmıştır</li>
  <li>Türkçe karakterler veri dosyasında UTF-8 olarak saklanır, konsol çıktısında sade
      karşılıkları kullanılır</li>
</ul>

<h1>2. Yönergedeki Zorunlu Gereksinimler ve Durum</h1>

<p>Yönergenin üçüncü bölümünde altı zorunlu teknik gereksinim sayılmıştır. Aynı yönergenin
teslim öncesi kontrol listesi bu sayıyı yedi olarak verir, çünkü genel kuralların ikincisindeki
bellek yönetimi şartı da zorunlu kalem sayılır. Hazır kütüphane yasağı (genel kural 1) da
denetim kolaylığı için tabloya eklendi. Böylece tabloda sekiz satır var: altı gereksinim,
bellek yönetimi ve sıfırdan gerçekleme. Bu gereksinimlerin
bir kısmı nesne yönelimli diller için yazılmış örneklerle anlatıldığından, C dilinde aynı
etkinin nasıl kurulacağı da tabloda belirtilmiştir. Ara rapor aşamasında çekirdek yapılar
çalışır durumdadır, nesne yönelimli karşılıklar final sürümünde tamamlanacaktır.</p>

<table>
<tr><th style="width:4%%">#</th><th style="width:26%%">Gereksinim</th>
    <th style="width:34%%">C dilindeki karşılığı</th><th style="width:36%%">Ara rapordaki durum</th></tr>
<tr><td>1</td><td>Kalıtım</td>
    <td>Ortak alanları taşıyan yapının başka yapının ilk üyesi olarak gömülmesi</td>
    <td>Planlandı. Hasta türleri (ayakta, yatan) için kullanılacak</td></tr>
<tr><td>2</td><td>Çok biçimlilik</td>
    <td>Fonksiyon işaretçisi tablosu üzerinden türe göre farklı davranış</td>
    <td>Planlandı. Muayene ücreti ve süresi türe göre farklı hesaplanacak</td></tr>
<tr><td>3</td><td>Soyut sınıf</td>
    <td>Gövdesi olmayan işlev işaretçilerinden oluşan yapı, eksik metotta NULL denetimi</td>
    <td>Planlandı. Kayıt türleri için ortak taban oluşturacak</td></tr>
<tr><td>4</td><td>Arayüz</td>
    <td>Yalnızca fonksiyon işaretçisi içeren yapı ve onu dolduran kayıtlar</td>
    <td>Planlandı. Raporlama modülü bu arayüzü uygulayacak</td></tr>
<tr><td>5</td><td>Dosya okuma ve yazma</td>
    <td>fopen, fgets, elle alan ayırma ve fprintf ile CSV benzeri metin dosyası</td>
    <td><b>Karşılandı.</b> 1200 kayıt okunuyor, kapanışta geri yazılıyor</td></tr>
<tr><td>6</td><td>UML sınıf diyagramı</td>
    <td>Yapı, modül ve bağımlılık diyagramı</td>
    <td><b>Karşılandı.</b> UML.pdf dosyasında</td></tr>
<tr><td>7</td><td>Bellek yönetimi (genel kural 2)</td>
    <td>malloc ve free, düğüm bazlı yapılar, kapanışta serbest bırakma</td>
    <td><b>Karşılandı.</b> Bağlayıcı sarmalamasıyla sayıldı, kayıt sayısıyla büyüyen fark yok</td></tr>
<tr><td>8</td><td>Veri yapılarının sıfırdan yazılması</td>
    <td>Hazır kütüphane yok, yalnızca stdio, stdlib ve string</td>
    <td><b>Karşılandı.</b> Beş yapı da elle gerçeklendi</td></tr>
</table>

<h1>3. Veri Yapısı Tasarımı</h1>

<p>Sistemdeki her yapı, hastane iş akışındaki belirli bir adımı karşılamak üzere seçilmiştir.
Kayıtlar bellekte tek kopya olarak durur, bağlı liste ve ağaç aynı <code>Hasta</code>
kaydına işaret eder. Böylece muayene durumu tek yerden güncellenir ve iki yapının
birbirinden kopması önlenir. Muayene sırası ise kayıttan bağımsız bir kuyrukta tutulur.</p>

<h2>3.1 Kayıt defteri için tek yönlü bağlı liste</h2>
<div class="sema"><pre>Hasta
+---------------------------+
| tc           : int        |
| ad           : char[64]   |
| yas          : int        |
| poliklinik   : char[48]   |
| durum        : int        |
| sonraki      : Hasta*  ---+--&gt; sonraki kayit
+---------------------------+</pre></div>
<p>Hasta kayıt defteri, ekleme ve silmenin sık yapıldığı bir kümedir. Dizi kullanılsaydı
kapasite dolduğunda yeniden tahsis, araya eklemede kaydırma ve silmede boşluk yönetimi
gerekirdi. Bağlı listede ekleme listenin başında sabit zamanda yapılır, silme yalnızca
bağlantı değiştirir, bellek kayıt sayısı kadar büyür. Listenin zayıf yönü aramadır, bu
yüzden arama görevi ağaca verilmiş, liste kayıtların bütününü korumakla sınırlandırılmıştır.</p>

<h2>3.2 Muayene sırası için kuyruk</h2>
<div class="sema"><pre>Bekleyen                Kuyruk
+------------------+    +----------------+
| tc     : int     |    | on    : Bekleyen*  --&gt; ilk gelen
| ad     : char[64]|    | arka  : Bekleyen*  --&gt; son gelen
| sonraki: Bekleyen*|   | adet  : int        |
+------------------+    +----------------+</pre></div>
<p>Projenin ana yapısı budur. Rafta ya da poliklinikte bekleyen hastalar arasında sıra
korumak zorunludur, çünkü sıra atlama doğrudan haksızlık üretir. Bu davranış ilk giren ilk
çıkar kuralıdır ve kuyruğun tanımıdır. Kuyrukta baş ve son işaretçisi birlikte tutulur,
böylece eleman ekleme listenin sonuna yürümek zorunda kalmadan sabit zamanda tamamlanır.
Tek işaretçi kullanılsaydı her ekleme doğrusal zaman harcardı, yüz hasta bekleyen bir
poliklinikte bu fark hissedilir. Kuyruk kayıt nesnesini kopyalamak yerine hasta numarası
ve adı taşır, böylece kayıt silinse bile sıradaki kişi kimliğini korur.</p>

<h2>3.3 Arama ve sıralı listeleme için ikili arama ağacı</h2>
<div class="sema"><pre>AgacDugum
+---------------------------+
| hasta : Hasta*            |
| sol   : AgacDugum*        |
| sag   : AgacDugum*        |
+---------------------------+
Kural: tc &lt; dugum.tc ise sola, tc &gt; dugum.tc ise saga</pre></div>
<p>Hasta numarasına göre arama, görevlinin en sık yaptığı işlemdir. Bağlı listede bu işlem
doğrusal aramadır ve kayıt sayısıyla doğru orantılı büyür. İkili arama ağacında her
karşılaştırma arama uzayını yarıya indirir, ortalama durumda logaritmik zamanda sonuç verir.
Ağacın ikinci görevi sıralı listelemedir. Sıralı dolanma ek bir sıralama algoritması
gerektirmeden kayıtları numaraya göre artan sırada verir. Ağacın riski, sıralı gelen veride
zincire dönüşerek aramanın doğrusallaşmasıdır. Bu davranış henüz ölçülmemiş (sıralı ve ters sıralı ölçüm final sürümüne bırakılmıştır) ve dengeli
ağaç çalışması final planına alınmıştır.</p>

<h2>3.4 Geri alma için yığıt</h2>
<p>Görevlinin yanlışlıkla sildiği bir kaydı geri getirebilmesi gerekir. Geri alınacak işlem
en son yapılan işlemdir. Bu, son giren ilk çıkar davranışıdır ve yığıtın tanımıdır. Yığıt
bağlı liste ile kurulmuştur, ekleme ve çıkarma listenin başından yapıldığı için ikisi de
sabit zamandadır. Dizi ile kurulsaydı sabit bir geri alma derinliği seçmek gerekirdi, bağlı
listede derinlik bellekle sınırlıdır. Yığıtta her düğüm işlemin türünü ve etkilenen kaydın
kopyasını taşır.</p>

<h2>3.5 Nöbetçi poliklinik turu için dairesel bağlı liste</h2>
<p>Hastanede nöbetçi poliklinik her gün bir sonrakine geçer ve son poliklinikten sonra
yeniden ilkine dönülür. Dairesel listede son düğümün işaretçisi ilk düğümü gösterdiği için
bu dönüş ayrı bir koşul gerektirmez, ilerleme tek atama ile yapılır. Tek yönlü düz liste
kullanılsaydı her turda sonun denetlenmesi ve başın yeniden bulunması gerekirdi.</p>

<h2>3.6 Modül yapısı ve dosya görevleri</h2>
<p>Kod yedi modüle ayrılmıştır. Her modülün bir başlık dosyası ve bir kaynak dosyası vardır,
menü dosyası dışında hiçbir dosya doğrudan ekrana yazmaz. Satır sayıları kaynak koddan
okunur, elle yazılmamıştır.</p>
<table>
<tr><th style="width:24%%">Dosya</th><th style="width:12%%">Satır</th><th>Sorumluluk</th></tr>
%(modul_tablo)s
</table>

<h2>3.7 Alternatif yapılarla karşılaştırma</h2>
<p>Aynı işi görebilecek yapılar aşağıdaki tabloda yan yana konmuştur. Seçimler, işlem
sıklığı ile bellek maliyeti arasındaki dengeye göre yapılmıştır.</p>
<table>
<tr><th style="width:19%%">Yapı</th><th>Sıralı erişim</th><th>Anahtar araması</th>
    <th>Araya ekleme</th><th>Bellek</th><th style="width:24%%">Bu projedeki durum</th></tr>
<tr><td>Dizi</td><td>O(1)</td><td>O(log n) sıralı ise, O(n) değilse</td><td>O(n) kaydırma</td>
    <td>Sabit, önceden ayrılır</td><td>Seçilmedi, kapasite sorunu nedeniyle</td></tr>
<tr><td>Tek yönlü bağlı liste</td><td>O(n)</td><td>O(n)</td><td>O(1) başta</td>
    <td>Düğüm başına 8 bayt ek</td><td>Hasta kayıt defteri</td></tr>
<tr><td>Kuyruk (baş ve son işaretçili)</td><td>Yok</td><td>O(n)</td><td>O(1) sona</td>
    <td>Düğüm başına 8 bayt ek</td><td>Muayene sırası, projenin ana yapısı</td></tr>
<tr><td>İkili arama ağacı</td><td>O(n) dolanma</td><td>O(log n) ortalama</td><td>O(log n)</td>
    <td>Düğüm başına 16 bayt ek</td><td>Arama ve sıralı listeleme</td></tr>
<tr><td>Yığıt (bağlı liste)</td><td>Yok</td><td>O(n)</td><td>O(1)</td>
    <td>Düğüm başına 8 bayt ek</td><td>Geri alma geçmişi</td></tr>
</table>

<h1>4. Algoritmalar</h1>

<h2>4.1 Kayıt ekleme ve silme</h2>
<pre>EKLE(bas, kayit):
    yeni = BELLEK_AYIR(Hasta)
    yeni.alanlar = kayit
    yeni.sonraki = bas
    DONDUR yeni                       # basa ekleme, O(1)

SIL(bas, tc):
    gezen = bas, onceki = BOS
    iken gezen != BOS ve gezen.tc != tc:
        onceki = gezen, gezen = gezen.sonraki
    eger gezen == BOS: DONDUR bas      # kayit yok
    silinen = gezen.icerik             # geri alma icin kopyala
    eger onceki == BOS: bas = gezen.sonraki
    yoksa: onceki.sonraki = gezen.sonraki
    BELLEK_BIRAK(gezen)
    DONDUR bas</pre>

<h2>4.2 Kuyruk işlemleri</h2>
<pre>KUYRUK_EKLE(kuyruk, tc, ad):
    yeni = BELLEK_AYIR(Bekleyen)
    yeni.tc = tc, yeni.ad = ad, yeni.sonraki = BOS
    eger kuyruk.arka == BOS:           # kuyruk bos
        kuyruk.on = kuyruk.arka = yeni
    yoksa:
        kuyruk.arka.sonraki = yeni     # sona bagla
        kuyruk.arka = yeni
    kuyruk.adet = kuyruk.adet + 1

KUYRUK_CIKAR(kuyruk):                  # siradaki hastayi cagir
    eger kuyruk.on == BOS: DONDUR "bos"
    cikan = kuyruk.on                  # ilk gelen
    kuyruk.on = cikan.sonraki
    eger kuyruk.on == BOS: kuyruk.arka = BOS
    BELLEK_BIRAK(cikan)
    kuyruk.adet = kuyruk.adet - 1
    DONDUR cikan.tc, cikan.ad</pre>

<h2>4.3 Ağaca ekleme, arama ve silme</h2>
<pre>AGAC_EKLE(kok, hasta):
    eger kok == BOS:
        yeni = BELLEK_AYIR(AgacDugum)
        yeni.hasta = hasta, yeni.sol = yeni.sag = BOS
        DONDUR yeni
    eger hasta.tc &lt; kok.hasta.tc: kok.sol = AGAC_EKLE(kok.sol, hasta)
    yoksa eger hasta.tc &gt; kok.hasta.tc: kok.sag = AGAC_EKLE(kok.sag, hasta)
    DONDUR kok

AGAC_ARA(kok, tc):
    eger kok == BOS: DONDUR BOS
    eger tc == kok.hasta.tc: DONDUR kok
    eger tc &lt; kok.hasta.tc: DONDUR AGAC_ARA(kok.sol, tc)
    DONDUR AGAC_ARA(kok.sag, tc)</pre>

<h2>4.4 Sıralı dolanma ve ağacın çizimi</h2>
<pre>SIRALI(kok):                      # sol, dugum, sag
    eger kok == BOS: DONDUR
    SIRALI(kok.sol)
    YAZ kok.hasta
    SIRALI(kok.sag)

CIZ(kok, derinlik):               # saga yatmis bicimde cizim
    eger kok == BOS: DONDUR
    CIZ(kok.sag, derinlik + 1)
    derinlik kadar bosluk yaz, sonra dugumu yaz
    CIZ(kok.sol, derinlik + 1)</pre>
<p>Sıralı dolanma ağacın her düğümünü bir kez ziyaret ettiği için doğrusal zamanda çalışır
ve ek sıralama algoritması gerektirmez. Çizim işlevi aynı dolanmayı sağa yatık biçimde
yapar. Sağ alt ağaç önce çizildiği için ekranda en büyük numara en üstte görünür, derinlik
arttıkça girinti artar. Bu görselleştirme yönergenin ek puan kalemlerinden birini
karşılamak üzere eklenmiştir.</p>

<h2>4.5 Yığıt ve geri alma</h2>
<pre>YIGIT_EKLE(tepe, islem):  yeni.sonraki = tepe, DONDUR yeni
YIGIT_AL(tepe):           yeniTepe = tepe.sonraki, BELLEK_BIRAK(tepe), DONDUR yeniTepe

GERI_AL(yigit):
    islem = YIGIT_AL(yigit)
    eger islem yok: "geri alinacak islem yok" yaz
    eger islem.tur == EKLE: listeden sil, agactan sil, siradan da cikar
    yoksa: kaydi geri ekle, durumunu geri yukle, agaca ekle</pre>

<h1>5. Karmaşıklık (Big-O) Analizi</h1>

<p>Aşağıdaki tabloda her işlemin zaman ve bellek karmaşıklığı Big-O gösterimiyle verilmiştir. Ağaç sütununda
ortalama durum dengeli bir ağaç varsayımıyla, kötü durum ise sıralı veriyle zincire dönmüş
ağaç için verilmiştir. Bellek sütunu, yapının kaç kayıt kadar ek yer tuttuğunu gösterir.</p>

<table>
<tr><th style="width:24%%">İşlem</th><th>Bağlı liste</th><th>Kuyruk</th>
    <th>İkili arama ağacı (ort.)</th><th>İkili arama ağacı (kötü)</th><th>Yığıt</th></tr>
<tr><td>Ekleme</td><td>O(1)</td><td>O(1)</td><td>O(log n)</td><td>O(n)</td><td>O(1)</td></tr>
<tr><td>Silme</td><td>O(n) arama + O(1)</td><td>O(1) baştan</td><td>O(log n)</td><td>O(n)</td><td>O(1)</td></tr>
<tr><td>Arama</td><td>O(n)</td><td>O(n)</td><td>O(log n)</td><td>O(n)</td><td>O(n)</td></tr>
<tr><td>Sıradaki hastayı çağırma</td><td>—</td><td>O(1)</td><td>—</td><td>—</td><td>—</td></tr>
<tr><td>Sıralı listeleme</td><td>O(n log n) ek sıralama</td><td>—</td><td>O(n)</td><td>O(n)</td><td>—</td></tr>
<tr><td>En yüksek bellek</td><td>O(n)</td><td>O(n)</td><td>O(n)</td><td>O(n)</td><td>O(n)</td></tr>
</table>

<p>Kuyruk, sıra disiplinini sabit zamanlı iki işlemle korur. Ağaç, sıralı listeleme için ek
sıralama algoritması gerektirmediğinden toplam maliyeti düşürür. Buna karşılık her ağaç
düğümü iki işaretçi fazladan taşır, kayıt başına yaklaşık 16 bayt ek yük oluşur.</p>

<h1>6. Deneysel Sonuçlar</h1>

<p>Ölçümler programın <code>--benchmark</code> kipinde yapılmıştır. Aynı iş yükü hem bağlı
listeye hem ikili arama ağacına verilmiş, süreler <code>timespec_get</code> ile milisaniye
altı çözünürlükte alınmıştır. Anahtarlar sıralı olmadığı için ağaç dengeli kalır. Ölçüm
ortamı Windows 11, AMD64, Intel Core i7-12700H, 16 GB bellek, gcc 16.2.0, -O2
iyileştirmesi. Ölçümler tek bir oturumda
alınmıştır ve program sonuçları <code>03_Olcum/benchmark.csv</code> dosyasına kendisi
yazar, yani rapordaki tablo ile CSV aynı çalıştırmadan üretilir. Aynı donanımda
tekrarlanan çalıştırmalarda süreler işletim sistemi yüküne göre yüzde 10 ile 20
arasında oynayabilir, büyüme eğilimi ve ağaç yükseklikleri değişmez.</p>

<p>Şekil 1 arama sürelerini logaritmik ölçekte, Şekil 2 ekleme sürelerini doğrusal ölçekte
karşılaştırır. Şekil 3 ise ölçülen ağaç yüksekliğini dengeli ağaç beklentisiyle yan yana koyar.</p>

<table>
<tr><th>Hasta sayısı</th><th>Ekleme liste (ms)</th><th>Ekleme ağaç (ms)</th>
    <th>Arama liste (ms)</th><th>Arama ağaç (ms)</th><th>Ağaç yüksekliği</th><th>Hız oranı</th></tr>
%(tablo)s
</table>

<div class="grafik">
%(grafik)s
</div>
<p class="kucuk">Şekil 1. Arama sürelerinin hasta sayısına göre değişimi, yatay eksen
logaritmik ölçekte.</p>

<div class="grafik">
%(grafik_ekleme)s
</div>
<p class="kucuk">Şekil 2. Ekleme süreleri. Bağlı liste yeni kaydı listenin başına eklediği için sabit zamanda
ilerler, ağaç her düğüm için ayrı bellek ayırır. Yatay eksen doğrusal.</p>

<div class="grafik">
%(grafik_yukseklik)s
</div>
<p class="kucuk">Şekil 3. Ölçülen ağaç yüksekliği ile dengeli bir ağaç için beklenen yükseklik
(log2(n+1)). Fark, anahtar dağılımının tam dengeli olmamasından gelir.</p>

<p>Sonuçlar teorik beklentiyle uyumludur. Hasta sayısı yüz kat artarken bağlı listede arama
süresi yaklaşık %(kat_liste)s katına çıkmıştır, çünkü her arama tüm listeyi baştan taramakta ve
bellek erişimleri önbelleğe sığmamaktadır. Ağaçta aynı artış yaklaşık %(kat_agac)s kattır ve
logaritmik büyümeye yakındır. Yüz bin kayıtta arama başına düşen süre listede yaklaşık
%(birim_liste)s ms, ağaçta %(birim_agac)s ms düzeyindedir. Ekleme tarafında liste sabit zamanlı olduğu için
küçük boyutlarda öndedir, yüz bin kayıtta ağacın düğüm başına ayırma maliyeti listeninkine
yaklaşır.</p>

<p>Ölçümler karışık anahtarlarla yapılmıştır. Veri dosyası da karışık sırada
tutulur, çünkü üreteç kayıtları sabit tohumla karıştırır. Sıralı veya ters sıralı
dosya yüklenirse ağaç zincire dönüşür ve arama doğrusal olur. Bu bozulma bu
sürümde ölçülmemiştir, çözüm olarak dengeli ağaç (AVL) final sürümüne
bırakılmıştır.</p>

<p>Ağaç yükseklikleri 17, 26 ve 59 olarak ölçülmüştür. Dengeli bir ağaçta beklenen değerler
10, 14 ve 17'dir. Aradaki fark, anahtar üretiminde kullanılan mod işleminin ağacı tam dengeli
dağıtmamasından kaynaklanır. Yükseklik arttıkça arama karşılaştırma sayısı da artar, bu
nedenle final sürümünde dengeli ağaç (AVL) eklenmesi planlanmıştır. Kuyruk tarafında aynı
ölçüm anlamsızdır, çünkü ekleme ve çağırma işlemleri kayıt sayısından bağımsız olarak sabit
zamanda tamamlanır. Bu nedenle kuyruk için ampirik ölçüm yerine karmaşıklık kanıtı
verilmiştir.</p>

<h1>7. Ekran Çıktıları</h1>

<figure><img src="%(ekran1)s">
<figcaption>Şekil 4. Açılış, numaraya göre hasta arama ve ağaç üzerinden sıralı listeleme.
Uzunluk nedeniyle tekrar eden menü satırları kısaltılmıştır</figcaption></figure>

<figure><img src="%(ekran2)s">
<figcaption>Şekil 5. Üç hastanın muayene sırasına alınması ve ilk gelen ilk çıkar sırasıyla
çağrılması. Tekrar eden menü satırları kısaltılmıştır</figcaption></figure>

<figure><img src="%(ekran3)s">
<figcaption>Şekil 6. İkili arama ağacının ekrana yatay çizimi ve dairesel poliklinik turu.
Tekrar eden menü satırları kısaltılmıştır</figcaption></figure>

<h1>8. Test Senaryoları</h1>

<p>Program, derleme sonrası aşağıdaki senaryolarla sınanmıştır. Her senaryo gerçek
çalıştırmadan alınan çıktıyla doğrulanmıştır.</p>

<table>
<tr><th style="width:5%%">#</th><th style="width:31%%">Senaryo</th><th style="width:30%%">Beklenen davranış</th>
    <th>Sonuç</th></tr>
<tr><td>1</td><td>Programın 1200 kayıtlık dosyayla açılması</td>
    <td>Kayıtlar yüklenir, menü görünür</td><td>Başarılı, 1200 kayıt yüklendi</td></tr>
<tr><td>2</td><td>Var olan numarayla hasta arama</td><td>Kayıt tek satırda gösterilir</td>
    <td>Başarılı, kayıt bulundu</td></tr>
<tr><td>3</td><td>Var olmayan numarayla arama</td><td>Uyarı verilir, program durmaz</td>
    <td>Başarılı, kayıt bulunamadı uyarısı</td></tr>
<tr><td>4</td><td>Aynı numarayla ikinci kez kayıt ekleme</td><td>Tekrar eklenmez, kullanıcı uyarılır</td>
    <td>Başarılı, mükerrer kayıt engellendi</td></tr>
<tr><td>5</td><td>Üç hastayı muayene sırasına ekleme</td><td>Sıra giriş sırasıyla korunur</td>
    <td>Başarılı, 1. 2. 3. sıra doğru</td></tr>
<tr><td>6</td><td>Sıradaki hastayı iki kez çağırma</td><td>İlk gelen önce çağrılır</td>
    <td>Başarılı, sıra ile çağrıldı</td></tr>
<tr><td>7</td><td>Boş sıradan hasta çağırma</td><td>Uyarı verilir</td>
    <td>Başarılı, sırada bekleyen hasta yok mesajı</td></tr>
<tr><td>8</td><td>Muayenede olmayan hastanın muayenesini bitirme</td><td>İşlem reddedilir</td>
    <td>Başarılı, hasta muayenede değil uyarısı</td></tr>
<tr><td>9</td><td>Son işlemi geri alma, ardından tekrar geri alma</td><td>Kayıt geri gelir, ikincide uyarı</td>
    <td>Başarılı, geri alınacak işlem yok mesajı</td></tr>
<tr><td>10</td><td>Menüde olmayan numara girme</td><td>Uyarı verilir, menü yenilenir</td>
    <td>Başarılı</td></tr>
<tr><td>11</td><td>Sayı yerine harf girme</td><td>Uyarı verilir, program durmaz</td>
    <td>Başarılı, geçersiz giriş mesajı</td></tr>
<tr><td>12</td><td>Veri dosyasının bulunmaması</td><td>Program çökmez, boş kayıtla açılır</td>
    <td>Başarılı, uyarı yazıldı</td></tr>
<tr><td>13</td><td>Girdi akışının bitmesi (boru hattında satır kalmaması)</td><td>Sonsuz döngüye girmez,
kayıtları yazıp kapanır</td><td>Başarılı, akış bitince temiz kapanıyor</td></tr>
<tr><td>14</td><td>Aynı hastayı ikinci kez sıraya ekleme</td><td>Tekrar eklenmez, kullanıcı uyarılır</td>
    <td>Başarılı, hasta zaten sırada bekliyor uyarısı</td></tr>
<tr><td>15</td><td>Muayenede olan hastayı yeniden sıraya ekleme</td><td>İşlem reddedilir</td>
    <td>Başarılı, muayenede uyarısı</td></tr>
<tr><td>16</td><td>Sırada bekleyen hastanın kaydını silme</td><td>Kayıt ve sıra girdisi birlikte kaldırılır</td>
    <td>Başarılı, muayene sırasından da çıkarıldı mesajı</td></tr>
<tr><td>17</td><td>Sayı alanına 12abc, yaşa 200, numaraya negatif değer ve 12345678901 taşması</td><td>Hepsi reddedilir</td>
    <td>Başarılı, geçersiz numara ve geçersiz yaş mesajları</td></tr>
<tr><td>18</td><td>Bozuk CSV, eksik alan, boş alan, bozuk sayı ve mükerrer numara</td><td>Satırlar atlanır, sayaç yazılır</td>
    <td>Başarılı, 6 satır atlandı, 2 kayıt yüklendi. Boş poliklinik alanı olan satır da atlandı</td></tr>
<tr><td>19</td><td>Boş veri dosyasıyla açma</td><td>Program çökmez, sıfır kayıtla açılır</td>
    <td>Başarılı, 0 hasta kaydı yüklendi</td></tr>
<tr><td>20</td><td>--benchmark kipinde ölçüm</td><td>Sonuçlar ekrana ve CSV dosyasına yazılır</td>
    <td>Başarılı, 03_Olcum/benchmark.csv güncellendi</td></tr>
<tr><td>21</td><td>İki çocuklu düğümü (ağacın kökü) silme</td><td>Ağaç bozulmaz, kayıt bulunamaz, düğüm sayısı bir azalır</td>
    <td>Başarılı, 31158 silindi, 1199 düğüm ve 21 yükseklik kaldı</td></tr>
<tr><td>22</td><td>Kaydı silip son işlemi geri alma</td><td>Kayıt durumuyla birlikte geri gelir</td>
    <td>Başarılı, 30100 tekrar bulundu, durum bekliyor</td></tr>
<tr><td>23</td><td>Muayenedeki hastanın kaydını silme</td><td>Kayıt silinir, muayene sırası boşalır</td>
    <td>Başarılı, muayene sırası 0 hasta</td></tr>
</table>

<h1>9. Karşılaşılan Sorunlar ve Çözümler</h1>
<ul>
  <li><b>Göreli veri yolu.</b> Program ilk denemede kayıt dosyasını bulamadı, çünkü
      çalıştırma dizini kaynak klasörüydü. Veri yolu proje köküne göre tanımlandı ve
      isteğe bağlı dosya adı argümanı eklendi.</li>
  <li><b>Ölçüm çözünürlüğü.</b> <code>clock()</code> Windows üzerinde yaklaşık 15 ms
      adımlarla ilerlediği için küçük boyutlarda süreler sıfır görünüyordu. Ölçüm
      <code>timespec_get</code> ile mikrosaniye altı çözünürlüğe taşındı.</li>
  <li><b>Sıralı veride ağacın bozulması.</b> Numaralar artan sırada eklendiğinde ağaç
      zincire dönüştü ve çizim tek sütun hâlinde göründü. Karışık anahtar üretimiyle
      ölçüm düzeltildi, kalıcı çözüm olarak dengeli ağaç planlandı.</li>
  <li><b>Bozuk satırlar.</b> Veri dosyasında eksik alan bulunduğunda okuma döngüsü
      duruyordu. Satır atlama ve alan denetimi eklendi, dosya sonuna kadar okunuyor.</li>
  <li><b>Silinen kaydın geri alınması.</b> Silinen düğümün belleği serbest bırakıldığı için
      geri alma bilgisi kayboluyordu. Silme işlevi, kaydın içeriğini çağırana kopyalayacak
      biçimde değiştirildi ve kopya yığıta yazıldı.</li>
  <li><b>Sıradaki hastanın kimliği.</b> Kuyruk yalnızca kayıt işaretçisi tutsaydı, kayıt
      silindiğinde sıradaki hasta da kaybolurdu. Kuyruk düğümü numara ve adı kendi
      içinde saklayacak biçimde tasarlandı.</li>
  <li><b>Girdi akışı bitince sonsuz döngü.</b> Girdi kesildiğinde <code>fgets</code> boş dönüyor,
      menü bunu geçersiz seçim sayıp kendini tekrar yazıyordu. Program durmuyordu. Girdi bitişi ayrı bir
      bayrakla izlendi, akış bittiğinde program kayıtları dosyaya yazıp temiz kapanıyor.</li>
  <li><b>Bellek ayrılamadığında sessiz başarı.</b> <code>kayit_ekle</code> bellek ayıramadığında
      eski listeyi döndürüyor, çağıran ise işlemi başarılı sanıyordu. Üç ekleme işlevi
      (<code>kayit_ekle</code>, <code>kuyruk_ekle</code>, <code>yigit_ekle</code>) artık başarı
      bayrağı döndürüyor, ayrıca ağaca ekleme yalnızca kayıt gerçekten oluştuysa yapılıyor.</li>
  <li><b>Kuyruk ile kayıt defterinin ayrışması.</b> Aynı hasta birden fazla kez sıraya
      yazılabiliyor, muayenedeki hasta yeniden sıraya alınabiliyor ve sırada bekleyen hastanın
      kaydı silindiğinde sıra girdisi kalıyordu. <code>kuyruk_iceriyor</code> ve
      <code>kuyruk_sil</code> işlevleri eklendi, üç durum da menüde denetleniyor.</li>
  <li><b>Gevşek sayı girişi.</b> <code>atoi</code> tabanlı okuma 12abc gibi girdileri 12 olarak
      kabul ediyor, taşma ve yaş aralığı denetlenmiyordu. <code>strtol</code> ile son karakter
      denetimi, taşma sınaması, 0 ile 130 arası yaş kuralı ve uzun girişlerde tampon boşaltma
      eklendi.</li>
  <li><b>Dosya okumada sessiz sıfırlama.</b> Bozuk sayısal alan <code>atoi</code> yüzünden sıfıra
      dönüşüyor, mükerrer numara ve eksik alan denetlenmiyordu. Sayısal alanlar sıkı çözümleniyor,
      mükerrer numara, eksik alan ve bozuk satırlar sayılıp raporlanıyor.</li>
  <li><b>Ölçüm dosyasının elle güncellenmesi.</b> <code>--benchmark</code> yalnızca ekrana
      yazıyor, CSV ayrıca düzenleniyordu. Ölçüm sonuçları artık her koşuda
      <code>03_Olcum/benchmark.csv</code> dosyasına da yazılıyor.</li>
  <li><b>Bellek denetimi.</b> Valgrind Windows üzerinde çalışmadığı için ayırma ve serbest
      bırakma çağrıları bağlayıcı sarmalamasıyla (linker wrap) sayıldı. 1200 kayıtla açılış ve
      kapanışta 2407 ayırma yapıldı, 2405 serbest bırakma sayıldı. Kalan iki fark, 12 kayıtlık demo
      dosyasında 32 ayırma 29 bırakma, hiç kayıt yüklenmeyen denemede ise 8 ayırma 5 bırakma olarak
      ölçüldü. Yani fark kayıt sayısıyla büyümüyor, iki üç çağrıda sabit kalıyor ve standart
      kütüphanenin tampon belleğinden geliyor. Sızıntı avcısı ile araç destekli doğrulama final
      sürümüne bırakıldı. Bu makinede AddressSanitizer ve Valgrind bulunmadığı için
      (mingw kurulumunda libasan yok) araç tabanlı denetim burada çalıştırılamadı.</li>
</ul>

<h1>10. İş Bölümü</h1>
<p>Proje bireysel olarak yürütülmüştür. Aşağıdaki tablo yapılan işleri ve harcanan süreyi
göstermektedir.</p>
<table>
<tr><th style="width:34%%">İş</th><th style="width:36%%">Çıktı</th><th>Süre</th></tr>
<tr><td>Konu seçimi ve kapsam</td><td>Hastane sıra sistemi, hafta 1–7 sınırı</td><td>2 saat</td></tr>
<tr><td>Bağlı liste ve kuyruk gerçeklemesi</td><td>hasta.c, kuyruk.c</td><td>6 saat</td></tr>
<tr><td>Ağaç, yığıt, dairesel liste</td><td>agac.c, yigit.c, dairesel.c</td><td>5 saat</td></tr>
<tr><td>Dosya işlemleri ve menü</td><td>dosya.c, main.c</td><td>4 saat</td></tr>
<tr><td>Test ve hata ayıklama</td><td>Uç durum denemeleri</td><td>3 saat</td></tr>
<tr><td>Ölçüm ve rapor</td><td>benchmark, bu rapor</td><td>4 saat</td></tr>
</table>

<h1>11. Yapay Zekâ Kullanım Beyanı</h1>
<p>Bu projede yapay zekâ destekli bir asistan yalnızca destek amacıyla kullanıldı.
Kullanım alanları kod taslağı oluşturma, derleme ve çalışma hatasının ayıklanması, rapor
metninin dil ve biçim düzeltmesidir. Üretilen her çıktı satır satır okunmuş, derlenmiş,
çalıştırılmış ve bu raporda gösterilen çıktılarla karşılaştırılmıştır. Veri yapısı seçimi,
testlerin yorumu ve nihai metinden öğrenci sorumludur. Beyan edilen alanlar dışında araç
kullanılmamıştır. Sunumda kodun tamamı sözlü olarak açıklanacaktır.</p>

<h1>12. Kalan İşler ve Çalışma Planı</h1>

<p>Ara raporun üçüncü beklentisi kalan işlerin ve iş bölümü planının verilmesidir. Final
teslimi 18 Aralık 2026 olarak belirlenmiştir. Kalan işler aşağıdaki gibidir.</p>

<table>
<tr><th style="width:6%%">#</th><th style="width:52%%">İş</th><th style="width:22%%">Hafta</th>
    <th>Kazanım</th></tr>
<tr><td>1</td><td>Yönergedeki nesne yönelimli gereksinimlerin C dilinde kurulması
    (kalıtım, çok biçimlilik, soyut yapı, arayüz)</td><td>8–9</td><td>Zorunlu gereksinim</td></tr>
<tr><td>2</td><td>Dengeli ağaç (AVL) eklenmesi ve yükseklik karşılaştırması</td><td>9–10</td>
    <td>Ek puan</td></tr>
<tr><td>3</td><td>İkiden fazla sıralama algoritmasının karşılaştırılması</td><td>11</td>
    <td>Ek puan</td></tr>
<tr><td>4</td><td>Hash tablosu ile arama karşılaştırması</td><td>11–12</td><td>Kapsam genişletme</td></tr>
<tr><td>5</td><td>Bellek sızıntısının araçla gösterilmesi</td><td>12</td><td>Ek puan</td></tr>
<tr><td>6</td><td>Git deposunun düzenli commit geçmişiyle sürdürülmesi</td><td>8–18 Aralık</td>
    <td>Ek puan</td></tr>
<tr><td>7</td><td>Sunum dosyası ve 5–8 dakikalık demo videosu</td><td>17 Aralık</td><td>Zorunlu</td></tr>
<tr><td>8</td><td>Final raporunun 8–15 sayfa olarak tamamlanması</td><td>17 Aralık</td><td>Zorunlu</td></tr>
</table>

<p>Ek puan kalemlerinden görselleştirme (ağacın ekrana çizilmesi) ve sürüm kontrolü bu
raporda başlatılmıştır, kalan üç kalem yukarıdaki plana göre tamamlanacaktır.</p>

<h1>13. Kaynakça</h1>
<ol>
  <li>İstanbul Rumeli Üniversitesi, <i>BLG203 Veri Yapıları Dönem Projesi Yönergesi</i>, 2026.</li>
  <li>BLG203 Veri Yapıları ders notları, 1–7. hafta slaytları, İstanbul Rumeli Üniversitesi.</li>
  <li>Cormen, T. H., Leiserson, C. E., Rivest, R. L., Stein, C., <i>Introduction to
      Algorithms</i>, 3. baskı, MIT Press, 2009.</li>
  <li>ISO/IEC 9899:2018, <i>Programming languages — C</i>, C11 standardı.</li>
  <li>Kernighan, B. W., Ritchie, D. M., <i>The C Programming Language</i>, 2. baskı,
      Prentice Hall, 1988.</li>
</ol>

<h1>Ek A. Derleme ve Çalıştırma Adımları</h1>

<p>Proje, gcc 16.2.0 (MinGW-W64) ile C11 standardında derlenmiştir. Derleme sırasında
<code>-Wall -Wextra</code> uyarı seçenekleri açıktır ve çıktı uyarı üretmemektedir.</p>

<pre>gcc -std=c11 -Wall -Wextra -O2 -o hastane.exe kaynak_kod/*.c
hastane.exe                              # 1200 kayitlik veri ile acilir
hastane.exe veri/demo_hastalar.csv       # 12 kayitlik demo verisi ile acilir
hastane.exe --benchmark                  # deneysel olcumu calistirir</pre>

<p>Teslim paketinin içeriği aşağıdaki gibidir. Paket içinde derlenmiş dosya (.exe, .o)
bulunmaz.</p>

<table>
<tr><th style="width:34%%">Paketteki öğe</th><th>İçerik</th></tr>
<tr><td>kaynak_kod/</td><td>13 kaynak dosya (7 .c ve 6 .h), derlenmiş dosya içermez</td></tr>
<tr><td>veri/</td><td>hastalar.csv (1200 kayıt), demo_hastalar.csv (12 kayıt), veri üreteci</td></tr>
<tr><td>03_Olcum/</td><td>benchmark.csv, deneysel ölçüm çıktısı, --benchmark kipinde program kendisi yazar</td></tr>
<tr><td>README.txt</td><td>Derleme, çalıştırma, menü ve veri biçimi açıklaması</td></tr>
<tr><td>Rapor.pdf</td><td>Bu rapor</td></tr>
<tr><td>UML.pdf</td><td>Yapı, modül ve bağımlılık diyagramı</td></tr>
</table>

<p>Sürüm geçmişi herkese açık depoda tutulmaktadır:
github.com/gecekargosu/blg203-hastane-sira</p>

</body></html>
"""


KOD_GOREV = {
    "agac.h": "İkili arama ağacı düğüm yapısı ve işlev bildirimleri",
    "agac.c": "Ağaca ekleme, arama, silme, sıralı dolanma ve ekrana çizim",
    "dairesel.h": "Nöbetçi poliklinik listesi bildirimleri",
    "dairesel.c": "Dairesel bağlı liste kurma ve tur ilerletme",
    "dosya.h": "Veri dosyası okuma ve yazma bildirimleri",
    "dosya.c": "CSV okuma, bozuk satır atlama, kapanışta geri yazma",
    "hasta.h": "Hasta kaydı yapısı ve kayıt defteri bildirimleri",
    "hasta.c": "Bağlı listeye ekleme, silme, numaraya göre arama, bellek bırakma",
    "kuyruk.h": "Muayene sırası kuyruğu bildirimleri",
    "kuyruk.c": "Kuyruğa ekleme, sıradaki hastayı çağırma, sıra sorgulama",
    "main.c": "Menü, iş akışları, deneysel ölçüm kipi ve girdi doğrulama",
    "yigit.h": "Geri alma yığıtı bildirimleri",
    "yigit.c": "Yığıta işlem ekleme ve geri alma kaydını çıkarma",
}


def modul_tablosu():
    """Kaynak dosyalari satir sayisi ve sorumluluklariyla listeler."""
    kok = os.path.join(KOK, "kaynak_kod")
    satirlar = []
    toplam = 0
    adet = 0
    for ad in sorted(os.listdir(kok)):
        if not (ad.endswith(".c") or ad.endswith(".h")):
            continue
        with open(os.path.join(kok, ad), encoding="utf-8") as dosya:
            satir = len(dosya.read().splitlines())
        toplam += satir
        adet += 1
        satirlar.append("<tr><td>%s</td><td>%d</td><td>%s</td></tr>"
                        % (ad, satir, KOD_GOREV.get(ad, "")))
    satirlar.append("<tr><td><b>Toplam</b></td><td><b>%d</b></td>"
                    "<td>%d dosya, 7 modül</td></tr>" % (toplam, adet))
    return "\n".join(satirlar)


def html_uret(veri, icindekiler="<!--TOC-->"):
    """Rapor govdesini HTML olarak uretir, icindekiler icin yer tutucu birakir."""
    return HTML % {
        "css": CSS,
        "icindekiler": icindekiler,
        "modul_tablo": modul_tablosu(),
        "logo": "file:///" + os.path.join(KOK, "00_Kapak", "assets", "logo.png").replace("\\", "/"),
        "tablo": tablo_html(veri),
        "kat_liste": "{:,}".format(int(round(veri[-1]["ar_liste"] / veri[0]["ar_liste"]))).replace(",", " "),
        "kat_agac": "{:,}".format(int(round(veri[-1]["ar_agac"] / veri[0]["ar_agac"]))).replace(",", " "),
        "birim_liste": ("%.2f" % (veri[-1]["ar_liste"] / 100000.0)).replace(".", ","),
        "birim_agac": ("%.5f" % (veri[-1]["ar_agac"] / 100000.0)).replace(".", ","),
        "grafik": grafik_html(veri),
        "grafik_ekleme": grafik_ekleme_html(veri),
        "grafik_yukseklik": grafik_yukseklik_html(veri),
        "ekran1": "file:///" + os.path.join(KOK, "00_Kapak", "ekran", "ekran1.png").replace("\\", "/"),
        "ekran2": "file:///" + os.path.join(KOK, "00_Kapak", "ekran", "ekran2.png").replace("\\", "/"),
        "ekran3": "file:///" + os.path.join(KOK, "00_Kapak", "ekran", "ekran3.png").replace("\\", "/"),
    }


BASLIK_DESEN = re.compile(r"<h([12])[^>]*>(.*?)</h\1>", re.S)


def sadelestir(metin):
    """Etiketleri temizler, bosluklari tek bosluga indirir."""
    metin = re.sub(r"<[^>]+>", "", metin)
    metin = metin.replace("\u00ad", "").replace("\xa0", " ")
    return re.sub(r"\s+", " ", metin).strip()


def baslik_listesi(html_metni):
    """Icindekiler icin h1 ve h2 basliklarini sirayla toplar."""
    liste = []
    for bulunan in BASLIK_DESEN.finditer(html_metni):
        metin = sadelestir(bulunan.group(2))
        if metin and metin != "İçindekiler":
            liste.append((int(bulunan.group(1)), metin))
    return liste


def icindekiler_html(basliklar, sayfalar):
    """Baslik ve sayfa numaralarindan icindekiler tablosu uretir."""
    satirlar = []
    for seviye, metin in basliklar:
        no = sayfalar.get(metin, "")
        satirlar.append(
            '<tr class="d%d"><td class="bas">%s</td><td class="no">%s</td></tr>'
            % (seviye, metin.replace("&", "&amp;"), no)
        )
    return (
        '<div class="icindekiler"><h1>İçindekiler</h1>'
        '<table class="toc">%s</table></div>' % "\n".join(satirlar)
    )




BLOK_DESEN = re.compile(
    r"(<h[12][^>]*>[^<]*</h[12]>)"
    r"((?:\s*<p[^>]*>(?:(?!</p>)(?!<h[12])(?!<table).)*</p>)?)"
    r"(\s*<table>.*?</table>)",
    re.S,
)


def blok_sar(html_metni):
    """Baslik, aciklamasi ve tablosunu tek blok yapar.

    Blok tek sayfaya sigdigi surece bolunmez, sigmadiginda butun halinde
    sonraki sayfaya gecer. Baslik sayfa dibinde yalniz kalmaz.
    """
    return BLOK_DESEN.sub(
        lambda b: '<div class="blok">%s%s%s</div>' % (b.group(1), b.group(2), b.group(3)),
        html_metni,
    )


def tablo_duzenle(html_metni):
    """Ilk satiri baslik olan tabloyu thead ve tbody olarak ayirir.

    Bolunmek zorunda kalan uzun tabloda baslik satiri her sayfada tekrarlanir.
    """
    def isle(bulunan):
        govde = bulunan.group(1)
        ilk = re.search(r"<tr[^>]*>.*?</tr>", govde, re.S)
        if not ilk or "<th" not in ilk.group(0):
            return bulunan.group(0)
        bas = ilk.group(0)
        kalan = govde[govde.index(bas) + len(bas):]
        return "<table><thead>%s</thead><tbody>%s</tbody></table>" % (bas, kalan)

    return blok_sar(re.sub(r"<table>(.*?)</table>", isle, html_metni, flags=re.S))


def pdf_bas(html_metni, hedef):
    """HTML'i Chrome ile A4 PDF'e basar, hedef yolu dondurur."""
    html_metni = tablo_duzenle(html_metni)
    gecici_html = os.path.join(KOK, "00_Kapak", "rapor.html")
    with open(gecici_html, "w", encoding="utf-8") as dosya:
        dosya.write(html_metni)
    subprocess.run([
        CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--user-data-dir=" + os.path.join(tempfile.gettempdir(), "chrome_pdf_profil"),
        "--no-pdf-header-footer", "--print-to-pdf=" + hedef,
        "file:///" + gecici_html.replace("\\", "/"),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not os.path.exists(hedef):
        raise SystemExit("HATA: PDF uretilemedi")
    return hedef


def sayfa_bul(ham, basliklar):
    """Her basligin gorundugu fiziksel sayfa indeksini bulur, kapak 0 sayilir.

    Icindekiler sayfasi da basliklari tasidigi icin atlanir.
    """
    okuyucu = pypdf.PdfReader(ham)
    sayfalar = [sadelestir(sayfa.extract_text() or "") for sayfa in okuyucu.pages]
    atla = {i for i, metin in enumerate(sayfalar) if metin.startswith("İçindekiler")}
    sonuc = {}
    for _, baslik in basliklar:
        aranan = baslik[:48]
        for i in range(1, len(sayfalar)):
            if i in atla:
                continue
            if aranan in sayfalar[i]:
                sonuc[baslik] = i
                break
        else:
            raise SystemExit("Baslik sayfada bulunamadi: %s" % baslik)
    return sonuc


def kunye_temizle(yol):
    """PDF kunyesini bosaltir, uretim araci bilgisi dosyada kalmaz."""
    okuyucu = pypdf.PdfReader(yol)
    yazici = pypdf.PdfWriter()
    for sayfa in okuyucu.pages:
        yazici.add_page(sayfa)
    bilgi = yazici._info.get_object()
    for anahtar in list(bilgi.keys()):
        del bilgi[anahtar]
    gecici = str(yol) + ".tmp"
    with open(gecici, "wb") as dosya:
        yazici.write(dosya)
    os.replace(gecici, yol)


def rapor_uret():
    veri = olcum_tablosu()
    temel = html_uret(veri)
    basliklar = baslik_listesi(temel.replace("<!--TOC-->", ""))

    # Ilk gecis bos numaralarla basilir, sayfa duzeni son halle ayni kalir.
    bos = temel.replace("<!--TOC-->", icindekiler_html(basliklar, {}))
    ham = pdf_bas(bos, os.path.join(tempfile.gettempdir(), "blg203_gecis1.pdf"))
    sayfalar = sayfa_bul(ham, basliklar)

    son = temel.replace("<!--TOC-->", icindekiler_html(basliklar, sayfalar))
    ham = pdf_bas(son, os.path.join(tempfile.gettempdir(), "blg203_gecis2.pdf"))
    dogrulama = sayfa_bul(ham, basliklar)
    if dogrulama != sayfalar:
        raise SystemExit("HATA: icindekiler sayfa numaralari kararli degil")

    altbilgi_bas(ham, HEDEF_PDF)
    kunye_temizle(HEDEF_PDF)
    print("rapor yazildi:", HEDEF_PDF, "|", len(dogrulama), "baslik")


def altbilgi_bas(kaynak, hedef):
    pdfmetrics.registerFont(TTFont("ArialTR", r"C:\Windows\Fonts\arial.ttf"))
    okuyucu = pypdf.PdfReader(kaynak)
    toplam = len(okuyucu.pages)
    yazici = pypdf.PdfWriter()

    for i, sayfa in enumerate(okuyucu.pages):
        if i == 0:
            yazici.add_page(sayfa)
            continue
        genislik = float(sayfa.mediabox.width)
        gecici = os.path.join(tempfile.gettempdir(), "altbilgi_%d.pdf" % i)
        cizim = canvas.Canvas(gecici, pagesize=(genislik, float(sayfa.mediabox.height)))
        cizim.setFont("ArialTR", 7.2)
        cizim.setStrokeColorRGB(0.62, 0.68, 0.76)
        cizim.setLineWidth(0.5)
        cizim.line(56, 30, genislik - 56, 30)
        cizim.setFillColorRGB(0.28, 0.33, 0.40)
        cizim.drawString(56, 21, BASLIK)
        cizim.drawRightString(genislik - 56, 21, "Sayfa %d / %d" % (i, toplam - 1))
        cizim.save()

        kaplama = pypdf.PdfReader(gecici).pages[0]
        sayfa.merge_page(kaplama)
        yazici.add_page(sayfa)

    with open(hedef, "wb") as dosya:
        yazici.write(dosya)


if __name__ == "__main__":
    rapor_uret()
