# BLG203 — Hoca Ne İstedi, Bizde Var mı (Ara Teslim Denetimi)

Denetim tarihi: 16 Kasım 2026
Kaynak: `BLG203_Veri_Yapilari_Donem_Projesi_Yonergesi.docx` (154 satır, tamamı okundu)
Proje: Hastane Hasta Sıra ve Bekleme Sistemi · Cengiz Kılıç 251205027 · C

Bu belge yönergedeki her maddeyi tek tek denetler. `04_YONERGE_UYUM_KONTROL_LISTESI.md` maddeleri sayar, bu belge ise **kanıtı ve eksiği** yazar.

---

## 1. Konu bildirimiyle uyum

Ders sorumlusuna bildirilen konu metni: *Hastane Hasta Sıra ve Bekleme Sistemi. Hastane kayıtlarını TXT/CSV dosyasından okuyarak C dilinde sıfırdan yazılacak bağlı liste (linked list) ve kuyruk (Queue - FIFO) veri yapıları ile bellekte yönetmeyi amaçlar. Program; yeni hasta ekleme, sıradaki hastayı çağırma, hasta arama ve farklı veri boyutlarında arama/listeleme performansının (zaman karmaşıklığı) ölçülmesini sağlayacaktır.*

| Bildirilen iş | Kodda | Kanıt |
|---|---|---|
| CSV/TXT dosyasından okuma | **VAR** | `dosya.c`, `veri/hastalar.csv` 1200 kayıt |
| Bağlı liste | **VAR** | `hasta.c`, tek yönlü liste |
| Kuyruk (FIFO) | **VAR** | `kuyruk.c`, baş + son işaretçili |
| Yeni hasta ekleme | **VAR** | Menü 1 |
| Sıradaki hastayı çağırma | **VAR** | Menü 7, FIFO test edildi |
| Hasta arama | **VAR** | Menü 3 (ağaç), menü 5 (liste) |
| Farklı boyutlarda arama performansı ölçümü | **VAR** | `--benchmark`: 1000 / 10 000 / 100 000 hasta |

Bildirimde olmayan ama eklenen yapılar: ikili arama ağacı (arama performansını ölçebilmek için), yığıt (geri alma) ve dairesel liste (poliklinik turu). Bu üçü raporda gerekçelendi ve hafta 1–7 kapsamında. Hoca "kullanılmış olmak için eklenmiş yapı tam puan almaz" dediği için her birinin raporda gerçek görevi yazılı.

---

## 2. Ara rapor içeriği (Yönerge 4.2)

| # | İstenen | Durum | Kanıt |
|---|---------|-------|-------|
| 1 | Problem tanımı + veri yapıları listesi ve görevleri (1–2 sayfa) | **VAR** | `01_Ara_Rapor.pdf`, 1. ve 3. bölüm (3 sayfaya yakın) |
| 2 | Temel işlemleri içeren çalışan ilk sürüm | **VAR** | 12 kaynak dosya, `-Wall -Wextra` ile 0 uyarı, menü uçtan uca test edildi |
| 3 | Kalan işler ve iş bölümü planı | **VAR** | 10. ve 12. bölüm, 8 maddelik plan tablosu |

---

## 3. Zorunlu 7 gereksinim (Yönerge Bölüm 3)

**Önemli tespit:** Yönerge programlama dili olarak **C** diyor, ancak 3. bölümdeki gereksinimler nesne yönelimli diller için yazılmış (kalıtım, soyut sınıf, arayüz, `List<Arac>` örneği). C dilinde bu kavramların birebir karşılığı yoktur, ancak yapı ve fonksiyon işaretçisiyle kurulabilir. Raporda bu eşleştirme tablo hâlinde verildi.

| # | Gereksinim | Durum | Açıklama |
|---|-----------|-------|----------|
| 1 | Kalıtım | FINAL | C'de ortak alanların içe gömülmesiyle kurulacak (ayakta/yatan hasta) |
| 2 | Çok biçimlilik | FINAL | Fonksiyon işaretçisi tablosu, muayene ücreti/süresi |
| 3 | Soyut sınıf | FINAL | Gövdesiz işaretçi tablosu + NULL denetimi |
| 4 | Arayüz | FINAL | `Raporlanabilir` karşılığı işaretçi yapısı |
| 5 | Dosya okuma/yazma | **VAR** | `dosya.c`, 1200 kayıt okunuyor, kapanışta yazılıyor, dosya yoksa uyarı |
| 6 | UML sınıf diyagramı | **VAR** | `02_UML_Diyagrami.pdf`, 6 yapı, alanlar, işlevler, ilişkiler, tek sayfa |
| 7 | Yapıların sıfırdan yazılması | **VAR** | Yalnızca `stdio.h`, `stdlib.h`, `string.h`, `time.h` |

**Skor: 3 tam, 4 finalde.** Bu dört madde C dilinde yapay durmaması için finalde hasta türleri (ayakta/yatan) üzerinden kurulacak, plan 12. bölümde.

---

## 4. Rapor yapısı (Yönerge Bölüm 5)

| Hocanın istediği başlık | Durum | Yer |
|---|---|---|
| Kapak: ders adı, proje adı, grup numarası, üye, teslim tarihi | **VAR** | Sayfa 1 |
| Problem tanımı | **VAR** | 1 |
| Veri yapısı tasarımı (düğüm yapısı, şekil, gerekçe, alternatif) | **VAR** | 3.1–3.7, her yapı için kutu şema + alternatif tablo |
| Algoritmalar (sözde kod) | **VAR** | 4.1–4.5 |
| Karmaşıklık analizi tablosu | **VAR** | 5. bölüm, 6 işlem × 5 yapı |
| Deneysel sonuçlar (1000/10 000/100 000, grafik, yorum) | **VAR** | 6. bölüm, gerçek ölçüm + çubuk grafik |
| Ekran görüntüleri | **VAR** | 7. bölüm, 3 görsel |
| Karşılaşılan sorunlar ve çözümler | **VAR** | 9. bölüm, 7 madde |
| İş bölümü tablosu | **VAR** | 10. bölüm |
| Kaynakça | **VAR** | 13. bölüm |
| 8–15 sayfa, 11–12 punto, 1,15 aralık | **VAR** | 9 gövde sayfa, 11 punto, 1,15 |

---

## 5. Ek puan (Yönerge Bölüm 7, tavan +10)

| # | Kalem | Durum | Kanıt |
|---|-------|-------|-------|
| 1 | Görselleştirme (ağacın ekrana çizilmesi) | **VAR** | Menü 10, `agac_ciz`, Şekil 4 |
| 2 | AVL / Trie gibi ileri yapı | FINAL | 9–10. hafta |
| 3 | İkiden fazla sıralama algoritması | FINAL | 11. hafta |
| 4 | Git/GitHub, düzenli commit | **KISMEN** | Yerel depo kuruldu, 1 commit. GitHub'a gönderme komutu `04_...` dosyasında |
| 5 | Valgrind ile bellek sızıntısı kanıtı | FINAL | Windows'ta Valgrind yok, WSL ile 12. hafta |

Bugün kesinleşen: görselleştirme (≈2 puan). Git gönderilirse +≈2 puan, toplam ~4. Finalde AVL + sıralama + Valgrind ile tavan hedefleniyor.

---

## 6. Doğrulanan teknik kontroller (bu denetimde çalıştırıldı)

| Kontrol | Sonuç |
|---|---|
| `gcc -std=c11 -Wall -Wextra -O2` | 0 hata, 0 uyarı |
| 1200 kayıtla açılış | Yüklendi, kapanışta 1200 kayıt geri yazıldı |
| FIFO düzeni | 30003 → 30001 → 30012 sırası korundu |
| Hatalı giriş (harf, olmayan menü, olmayan hasta) | Çökme yok, uyarı verip menüye döndü |
| Dosya yok | Uyarı + boş kayıtla devam |
| Ölçüm | Arama: liste 1,38 → 39 404 ms, ağaç 0,024 → 11,417 ms (1000 → 100 000) |
| ZIP içeriği | 21 dosya, derlenmiş dosya yok |

---

## 7. Riskler ve yapılacaklar

| # | Risk / eksik | Etki | Önlem |
|---|---|---|---|
| 1 | Nesne yönelimli 4 gereksinim C'de yapay durma riski | Tasarım puanı | Hasta türleri üzerinden kurulacak, sunumda gerekçesi anlatılacak |
| 2 | Kuyruk için ampirik ölçüm yok (sabit zamanlı) | Hoca "ölçüm nerede" diyebilir | Rapor 6. bölümde karmaşıklık kanıtı yazıldı |
| 3 | Git deposu GitHub'a gönderilmedi | Ek puan kanıtsız | Tek komut, `04_...` dosyasında |
| 4 | AVL, sıralama karşılaştırması, Valgrind finalde | Ek puanın 6 puanı | 9–12. hafta planı hazır |
| 5 | Sunum ve video | Final zorunluluğu | 17 Aralık |

---

## 8. Tek cümlelik sonuç

Ara raporun üç beklentisi de karşılandı, kod 0 uyarıyla derleniyor ve tüm menü akışları çalışıyor; eksik olan tek şey C dilinde kurulacak 4 nesne yönelimli gereksinim ile 3 ek puan kalemi, hepsinin tarihi plan tablosunda yazılı.
