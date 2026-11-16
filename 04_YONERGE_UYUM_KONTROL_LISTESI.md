# BLG203 Veri Yapıları — Yönerge Uyum Kontrol Listesi

Proje: **Hastane Hasta Sıra ve Bekleme Sistemi**
Öğrenci: Cengiz Kılıç — 251205027
Belge: `BLG203_Veri_Yapilari_Donem_Projesi_Yonergesi.docx` maddelerinin tek tek karşılanma durumu.
Son güncelleme: 16 Kasım 2026 (ara teslim)

İşaretler: **VAR** karşılandı · **KISMEN** ara sürümde karşılandı, finalde tamamlanacak · **FINAL** final tesliminde yapılacak (ara raporda zorunlu değil)

---

## 1. Genel Kurallar (Yönerge Bölüm 2)

| # | Kural | Durum | Kanıt |
|---|-------|-------|-------|
| 1 | Hazır veri yapısı kütüphanesi yasak, yapılar sıfırdan yazılmalı | VAR | Yalnızca `stdio.h`, `stdlib.h`, `string.h`, `time.h` kullanıldı. Beş yapı da `kaynak_kod/` altında elle yazıldı |
| 2 | Düğüm tabanlı yapılar işaretçi ve dinamik bellek ile kurulmalı, bellek serbest bırakılmalı | VAR | `malloc`/`free` eşleşmesi tam. Kapanışta `yigit_serbest`, `kuyruk_serbest`, `poliklinik_serbest`, `agac_serbest`, `kayit_serbest` sırayla çağrılıyor |
| 3 | Menü tabanlı konsol uygulaması | VAR | 12 seçenekli menü, `main.c` |
| 4 | Veri en az bir dosyadan okunmalı, en az 1000 kayıt | VAR | `veri/hastalar.csv` 1200 kayıt, `dosya.c` ile okunuyor |
| 5 | Anlamlı isimler, açıklama satırları, modüler yapı | VAR | 7 modül (12 dosya), her işlevin başında Türkçe açıklama |

## 2. Zorunlu Teknik Gereksinimler (Yönerge Bölüm 3)

| # | Gereksinim | Durum | Açıklama |
|---|-----------|-------|----------|
| 1 | Kalıtım | FINAL | C dilinde ortak alanları taşıyan yapının içe gömülmesiyle kurulacak (ayakta/yatan hasta). Raporda planlandı |
| 2 | Çok biçimlilik | FINAL | Fonksiyon işaretçisi tablosu ile muayene ücreti/süresi hesabı |
| 3 | Soyut sınıf | FINAL | Gövdesiz işaretçilerden oluşan taban yapı |
| 4 | Arayüz | FINAL | `Raporlanabilir` karşılığı işaretçi tablosu |
| 5 | Dosya okuma/yazma | VAR | Açılışta okuma, kapanışta yazma, dosya yoksa uyarı ve çökmeme |
| 6 | UML sınıf diyagramı | VAR | `UML.pdf`, 6 yapı, alanlar, işlevler, ilişkiler |
| 7 | Yapıların gerçek görevi olması | VAR | Her yapı bir iş akışı adımını karşılıyor, bölüm 3'te gerekçeli |

> Not: Yönergede 3. bölüm nesne yönelimli örneklerle (kalıtım, arayüz) yazılmış, dil ise C olarak belirtilmiş. Raporda bu gereksinimlerin C karşılıkları tablo hâlinde açıklandı.

## 3. Ara Rapor İçeriği (Yönerge Bölüm 4.2)

| # | Beklenen | Durum | Yer |
|---|----------|-------|-----|
| 1 | Problem tanımı ve kullanılacak veri yapıları listesi, her birinin görevi (1–2 sayfa) | VAR | Rapor 1 ve 3. bölüm |
| 2 | Temel işlemleri (ekleme, silme, arama) içeren çalışan ilk sürüm | VAR | 12 kaynak dosya, derleme 0 uyarı, menü uçtan uca test edildi |
| 3 | Kalan işler ve iş bölümü planı | VAR | Rapor 10 ve 12. bölüm |

## 4. Rapor Yapısı (Yönerge Bölüm 5)

| Beklenen başlık | Durum | Yer |
|---|---|---|
| Kapak: ders adı, proje adı, grup numarası, üye bilgileri, teslim tarihi | VAR | Sayfa 1 (bireysel proje, üye bilgisi öğrenci) |
| Problem Tanımı | VAR | 1 |
| Veri Yapısı Tasarımı (düğüm yapısı, şekil, neden bu yapı, alternatif karşılaştırma) | VAR | 3.1–3.7 |
| Algoritmalar (sözde kod) | VAR | 4.1–4.5 |
| Karmaşıklık Analizi (tablo) | VAR | 5 |
| Deneysel Sonuçlar (1000 / 10000 / 100000, grafik, yorum) | VAR | 6 (gerçek ölçüm) |
| Ekran Görüntüleri | VAR | 7 (üç görsel) |
| Karşılaşılan Sorunlar ve Çözümler | VAR | 9 |
| Grup İçi İş Bölümü | VAR | 10 (bireysel) |
| Kaynakça | VAR | 13 |
| 8–15 sayfa, 11 punto, 1,15 satır aralığı | VAR | Gövde 9 sayfa, Times New Roman 11 pt, 1,15 |
| Yapay Zekâ Kullanım Beyanı (Bölüm 8'de isteniyor) | VAR | 11 |

## 5. Ek Puan Kalemleri (Yönerge Bölüm 7 — tavan +10)

| # | Kalem | Durum | Kanıt |
|---|-------|-------|-------|
| 1 | Veri yapılarının görselleştirilmesi (ağacın ekrana çizilmesi) | **VAR** | Menü 10, `agac_ciz`, Şekil 4 |
| 2 | Dengeli ağaç (AVL) veya Trie gibi ileri yapı | FINAL | 12. bölüm planı, 9–10. hafta |
| 3 | İkiden fazla sıralama algoritmasının karşılaştırılması | FINAL | 11. hafta planı |
| 4 | Sürüm kontrolü (Git/GitHub) ve düzenli commit geçmişi | **KISMEN** | Yerel git deposu kuruldu, commit geçmişi başlatıldı. GitHub'a gönderme komutu aşağıda |
| 5 | Bellek sızıntısının araçla gösterilmesi (Valgrind) | FINAL | Windows'ta Valgrind yok, WSL üzerinden 12. hafta |

Kazanılması hedeflenen ek puan: görselleştirme ve sürüm kontrolü hazır, kalan iki kalem finalde eklenecek.

Git deposunu GitHub'a göndermek için (tek komut, kullanıcı çalıştıracak):

```
git remote add origin https://github.com/gecekargosu/blg203-hastane-sira.git
git push -u origin main
```

## 6. Teslim Öncesi Kontrol Listesi (Yönerge Bölüm 10)

| Madde | Durum |
|-------|-------|
| Hazır koleksiyon/STL kütüphanesi kullanılmadı | ☑ |
| Bölüm 3'teki zorunlu gereksinimlerin tamamı | ☑ 3'ü ara sürümde karşılandı (dosya, UML, sıfırdan gerçekleme), 4'ü finalde (tablo 2) |
| Program README talimatıyla başka bilgisayarda derlenip çalışıyor | ☑ gcc C11, uyarısız derleme |
| Veri dosyaları ZIP içinde ve doğru okunuyor | ☑ 1200 kayıt yüklendi |
| Raporda karmaşıklık tablosu ve performans grafikleri var | ☑ |
| Raporda iş bölümü tablosu ve yapay zekâ beyanı var | ☑ |
| Demo videosu bağlantısı erişime açık | ☐ finalde |
| ZIP doğru isimlendirildi ve zamanında yüklendi | ☑ `Cengiz_Kilic_251205027_Yapay_Zeka_ve_Makine_Ogrenmesi_Ara_Teslim.zip` |

## 7. Doğrulanan Teknik Kontroller

- `gcc -std=c11 -Wall -Wextra -O2` → 0 hata, 0 uyarı
- Menü akışı: ekleme, silme, arama, sıralı listeleme, kuyruğa ekleme, sıradaki hastayı çağırma (FIFO doğrulandı), muayene bitirme, geri alma, ağaç çizimi, poliklinik turu
- Hatalı girişler: sayı yerine harf, menüde olmayan numara, olmayan hasta numarası → program çökmüyor
- Veri dosyası yok → uyarı verip boş kayıtla devam ediyor
- 1200 kayıt yüklendi, kapanışta 1200 kayıt geri yazıldı
- Ölçüm: 1000 / 10 000 / 100 000 hasta, arama süresi liste 1,38 → 39 404 ms, ağaç 0,024 → 11,417 ms
