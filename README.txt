HASTANE HASTA SIRA VE BEKLEME SİSTEMİ
BLG203 Veri Yapıları Dönem Projesi, Ara Teslim
Cengiz Kılıç, 251205027, Yapay Zekâ ve Makine Öğrenmesi

------------------------------------------------------------------------
1. PROJENİN AMACI
------------------------------------------------------------------------
Hastane kayıtlarını TXT/CSV dosyasından okuyup bellekte bağlı liste, kuyruk
ve ağaç veri yapılarıyla yönetmek. Program yeni hasta ekleme, sıradaki
hastayı çağırma, hasta arama ve farklı veri boyutlarında arama
performansının ölçülmesini sağlar.

Kullanılan veri yapıları (dersin 1-7. hafta konuları):
  - Tek yönlü bağlı liste : hasta kayıt defteri
  - Kuyruk (FIFO)         : muayene bekleme sırası
  - İkili arama ağacı     : numaraya göre arama, sıralı listeleme
  - Yığıt                 : son işlemi geri alma
  - Dairesel bağlı liste  : nöbetçi poliklinik turu

------------------------------------------------------------------------
2. DERLEME
------------------------------------------------------------------------
Derleyici : gcc 16.2.0 (MinGW-W64, x86_64-ucrt-posix-seh)
Dil       : C11
Komut satırı (proje kök dizininde çalıştırın):

    gcc -std=c11 -Wall -Wextra -O2 -o hastane.exe kaynak_kod/*.c

Derleme uyarı üretmez. Visual Studio kullanılacaksa tüm .c dosyaları tek
projeye eklenip Console Application olarak derlenebilir. MSVC için /W4
anahtarı önerilir.

------------------------------------------------------------------------
3. ÇALIŞTIRMA
------------------------------------------------------------------------
    hastane.exe                            -> 1200 kayıtlık veri ile açılır
    hastane.exe veri/demo_hastalar.csv     -> 12 kayıtlık demo verisi
    hastane.exe --benchmark                -> deneysel ölçümü çalıştırır

Önemli: program veri dosyasını çalışma dizinine göre arar, bu nedenle proje
kök dizininden çalıştırılmalıdır.

------------------------------------------------------------------------
4. MENÜ
------------------------------------------------------------------------
 1) Hasta kaydı ekle
 2) Hasta kaydı sil
 3) Numaraya göre hasta ara (ağaç)
 4) Kayıtları sıralı listele (ağaç)
 5) Kayıtları liste sırasında göster (bağlı liste)
 6) Sıraya hasta ekle (kuyruk)
 7) Sıradaki hastayı çağır
 8) Muayeneyi bitir
 9) Son işlemi geri al (yığıt)
10) Ağacı ekrana çiz
11) Nöbetçi poliklinik turu (dairesel liste)
12) Muayene sırasını göster
 0) Çıkış (kayıtlar dosyaya yazılır)

------------------------------------------------------------------------
5. VERİ DOSYASI BİÇİMİ
------------------------------------------------------------------------
Alanlar noktalı virgül ile ayrılır, ilk satır başlıktır:

    tc;ad;yas;poliklinik;durum
    30001;Ayşe Yılmaz;54;Dahiliye;0
    30002;Emine Aydın;31;Dermatoloji;0

durum: 0 bekliyor, 1 muayenede

Dosya: veri/hastalar.csv (1200 kayıt), veri/demo_hastalar.csv (12 kayıt)
Yeniden üretmek için: python veri/veri_uret.py

Okuma sırasında eksik alan, bozuk sayı veya mükerrer numara taşıyan satırlar
atlanır ve atlanan satır sayısı ekrana yazılır. Ad veya poliklinik içindeki
noktalı virgül yazılırken virgüle çevrilir, böylece dosya biçimi bozulmaz.
Kayıtlar dosyada karışık sırada tutulur, sıralı dosya ikili arama ağacını
zincire çevirdiği için üreteç kayıtları sabit tohumla karıştırır.

Giriş kuralı: numara pozitif tam sayı, yaş 0 ile 130 arası olmalıdır. 12abc
gibi harf karışık girdiler, boş ad ve boş poliklinik reddedilir.

------------------------------------------------------------------------
6. DOSYA DÜZENİ
------------------------------------------------------------------------
kaynak_kod/   13 kaynak dosya, 7 .c ve 6 .h (derlenmiş dosya yoktur)
veri/         hastalar.csv (1200 kayıt), demo_hastalar.csv (12 kayıt), veri_uret.py
03_Olcum/     benchmark.csv, --benchmark kipinde program tarafından yazılır
README.txt    bu dosya
Rapor.pdf     ara rapor (14 sayfa)
UML.pdf       yapı, modül ve bağımlılık diyagramı

Raporun ve UML'nin üreteç betikleri ile ekran görüntüleri depoda 00_Kapak/
klasöründe tutulur, teslim ZIP'ine konmaz. ZIP içeriği yukarıdaki yedi ögeden
oluşur.

------------------------------------------------------------------------
7. KODLAMA
------------------------------------------------------------------------
Kaynak dosyalar ASCII tutulmuştur, böylece bölge ayarı ve konsol kodlaması
farklı olan makinelerde derleme ve çıktı bozulmaz. Veri dosyaları UTF-8
kodludur. Belgeler tam Türkçe karakter kullanır.

------------------------------------------------------------------------
8. GITHUB DEPOSU
------------------------------------------------------------------------
https://github.com/gecekargosu/blg203-hastane-sira

Depoya herkes erişebilir. Depoda kaynak kodun commit geçmişi, rapor ve UML
dosyası bulunur.

------------------------------------------------------------------------
9. DEMO VİDEOSU
------------------------------------------------------------------------
Final tesliminde eklenecek 5-8 dakikalık ekran kaydı bağlantısı:
(bağlantı final tesliminden önce buraya yazılacak)
