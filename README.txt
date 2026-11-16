HASTANE HASTA SIRA VE BEKLEME SISTEMI
BLG203 Veri Yapilari Donem Projesi - Ara Teslim
Cengiz Kilic - 251205027 - Yapay Zeka ve Makine Ogrenmesi

------------------------------------------------------------------------
1. PROJENIN AMACI
------------------------------------------------------------------------
Hastane kayitlarini TXT/CSV dosyasindan okuyup bellekte bagli liste ve
kuyruk veri yapilariyla yonetmek. Program yeni hasta ekleme, siradaki
hastayi cagirma, hasta arama ve farkli veri boyutlarinda arama
performansinin olculmesini saglar.

Kullanilan veri yapilari (dersin 1-7. hafta konulari):
  - Tek yonlu bagli liste : hasta kayit defteri
  - Kuyruk (FIFO)         : muayene bekleme sirasi
  - Ikili arama agaci     : numaraya gore arama, sirali listeleme
  - Yigit                 : son islemi geri alma
  - Dairesel bagli liste  : nobetci poliklinik turu

------------------------------------------------------------------------
2. DERLEME
------------------------------------------------------------------------
Derleyici : gcc 16.2.0 (MinGW-W64, x86_64-ucrt-posix-seh)
Dil       : C11
Komut satiri (proje kok dizininde calistirin):

    gcc -std=c11 -Wall -Wextra -O2 -o hastane.exe kaynak_kod/*.c

Derleme sonucunda uyari uretmez. Visual Studio kullanilacaksa tum .c
dosyalari tek projeye eklenip Console Application olarak derlenebilir.
MSVC icin /W4 anahtari onerilir.

------------------------------------------------------------------------
3. CALISTIRMA
------------------------------------------------------------------------
    hastane.exe                            -> 1200 kayitlik veri ile acilir
    hastane.exe veri/demo_hastalar.csv     -> 12 kayitlik demo verisi
    hastane.exe --benchmark                -> deneysel olcumu calistirir

Onemli: program veri dosyasini calisma dizinine gore arar, bu nedenle
proje kok dizininden calistirilmalidir.

------------------------------------------------------------------------
4. MENU
------------------------------------------------------------------------
 1) Hasta kaydi ekle
 2) Hasta kaydi sil
 3) Numaraya gore hasta ara (agac)
 4) Kayitlari sirali listele (agac)
 5) Kayitlari liste sirasinda goster (bagli liste)
 6) Siraya hasta ekle (kuyruk)
 7) Siradaki hastayi cagir
 8) Muayeneyi bitir
 9) Son islemi geri al (yigit)
10) Agaci ekrana ciz
11) Nobetci poliklinik turu (dairesel liste)
12) Muayene sirasini goster
 0) Cikis (kayitlar dosyaya yazilir)

------------------------------------------------------------------------
5. VERI DOSYASI BICIMI
------------------------------------------------------------------------
Alanlar noktali virgul ile ayrilir, ilk satir basliktir:

    tc;ad;yas;poliklinik;durum
    30001;Ayse Yilmaz;54;Dahiliye;0
    30002;Emine Aydin;31;Dermatoloji;0

durum: 0 bekliyor, 1 muayenede

Dosya: veri/hastalar.csv (1200 kayit), veri/demo_hastalar.csv (12 kayit)
Yeniden uretmek icin: python veri/veri_uret.py

------------------------------------------------------------------------
6. DOSYA DUZENI
------------------------------------------------------------------------
kaynak_kod/   12 kaynak dosya (derlenmis dosya yoktur)
veri/         test verileri ve veri ureteci
olcum/        benchmark.csv, deneysel olcum ciktisi (klasorde 03_Olcum)
00_Kapak/     rapor, UML ve ekran goruntusu uretecleri
Rapor.pdf               ara rapor (10 sayfa)
UML.pdf                 UML yapi diyagrami (1 sayfa)
04_YONERGE_UYUM_KONTROL_LISTESI.md  yonerge madde madde kontrol

------------------------------------------------------------------------
7. GITHUB DEPOSU (herkese acik)
------------------------------------------------------------------------
https://github.com/gecekargosu/blg203-hastane-sira

Depoda kaynak kodun commit gecmisi, rapor ve UML dosyasi bulunur.
Hoca kontrol icin dogrudan bu baglantidan inceleyebilir.

------------------------------------------------------------------------
8. DEMO VIDEOSU
------------------------------------------------------------------------
Final tesliminde eklenecek 5-8 dakikalik ekran kaydi bagi:
(baglanti final tesliminden once buraya yazilacak)
