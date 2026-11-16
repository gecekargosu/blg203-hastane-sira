/*
 * Hastane Hasta Sira ve Bekleme Sistemi
 * BLG203 Veri Yapilari donem projesi, Cengiz Kilic 251205027
 *
 * Kullanilan veri yapilari, hafta 1-7 konulari:
 *   - Tek yonlu bagli liste : hasta kayit defteri
 *   - Ikili arama agaci     : numaraya gore hizli arama, sirali listeleme
 *   - Kuyruk                : muayene bekleme sirasi, ilk gelen ilk cikar
 *   - Yigit                 : son islemi geri alma
 *   - Dairesel bagli liste  : nobetci poliklinik turu
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <errno.h>
#include <time.h>

#include "hasta.h"
#include "agac.h"
#include "yigit.h"
#include "kuyruk.h"
#include "dairesel.h"
#include "dosya.h"

#define YAS_UST 130
#define VERI_YOLU "veri/hastalar.csv"
#define GIRDI_UZUNLUK 128

static double simdi_ms(void);
static void menuyu_yaz(void);
static int sayi_oku(const char *soru, int *hedef);
static void metin_oku(const char *soru, char *hedef, int uzunluk);
static Hasta *hasta_ekle_akis(Hasta *kayitlar, AgacDugum **agac, Islem **yigit);
static Hasta *hasta_sil_akis(Hasta *kayitlar, AgacDugum **agac, Islem **yigit, Kuyruk *kuyruk);
static void benchmark(void);

/* Girdi akisi bittiginde 1 olur. Menu dongusu bu bayragi gorup
   sonsuz donguye girmeden kayitlari yazip temiz kapanir. */
static int girdi_bitti = 0;

int main(int argc, char **argv) {
    Hasta *kayitlar = NULL;
    AgacDugum *agac = NULL;
    Islem *yigit = NULL;
    Kuyruk kuyruk;
    Poliklinik *poliklinikSon = NULL;
    int kayit = 0;
    const char *veriYolu = VERI_YOLU;

    /* Olcum modu: raporun deneysel bolumu icin */
    if (argc > 1 && strcmp(argv[1], "--benchmark") == 0) {
        benchmark();
        return 0;
    }

    /* Istege bagli veri dosyasi: hastane.exe veri/demo_hastalar.csv */
    if (argc > 1) {
        veriYolu = argv[1];
    }

    kuyruk_baslat(&kuyruk);

    kayit = dosya_oku(veriYolu, &kayitlar, &agac);
    if (kayit < 0) {
        printf("Uyari: %s bulunamadi. Bos kayitla basliyoruz.\n", veriYolu);
    } else {
        printf("%d hasta kaydi yuklendi.\n", kayit);
    }

    poliklinikSon = poliklinik_ekle(poliklinikSon, 1, "Dahiliye");
    poliklinikSon = poliklinik_ekle(poliklinikSon, 2, "Kardiyoloji");
    poliklinikSon = poliklinik_ekle(poliklinikSon, 3, "Ortopedi");
    poliklinikSon = poliklinik_ekle(poliklinikSon, 4, "Cocuk Sagligi");
    poliklinikSon = poliklinik_ekle(poliklinikSon, 5, "Goz Hastaliklari");

    int calisiyor = 1;
    while (calisiyor) {
        int secim = 0;
        menuyu_yaz();
        if (!sayi_oku("Seciminiz: ", &secim)) {
            if (girdi_bitti) {
                printf("Giris akisi bitti, kayitlar dosyaya yazilip cikiliyor.\n");
                break;
            }
            printf("Gecersiz giris. Menudeki bir numarayi girin.\n");
            continue;
        }

        switch (secim) {
        case 1:
            kayitlar = hasta_ekle_akis(kayitlar, &agac, &yigit);
            break;

        case 2:
            kayitlar = hasta_sil_akis(kayitlar, &agac, &yigit, &kuyruk);
            break;

        case 3: {
            int tc = 0;
            if (!sayi_oku("Hasta numarasi: ", &tc)) {
                printf("Gecersiz numara.\n");
                break;
            }
            AgacDugum *bulunan = agac_ara(agac, tc);
            if (bulunan == NULL) {
                printf("Kayit bulunamadi: %d\n", tc);
            } else {
                printf("%5d | %-28s | %3d yas | %-22s | %s\n",
                       bulunan->hasta->tc, bulunan->hasta->ad, bulunan->hasta->yas,
                       bulunan->hasta->poliklinik,
                       bulunan->hasta->durum ? "muayenede" : "bekliyor");
            }
            break;
        }

        case 4:
            printf("---- SIRALI LISTE (agac, kucukten buyuge) ----\n");
            agac_sirali(agac);
            printf("Dugum sayisi: %d, agac yuksekligi: %d\n",
                   agac_dugum_say(agac), agac_yukseklik(agac));
            break;

        case 5:
            kayit_listele(kayitlar);
            break;

        case 6: {
            int tc = 0;
            if (!sayi_oku("Siraya eklenecek hasta no: ", &tc) || tc <= 0) {
                printf("Gecersiz numara.\n");
                break;
            }
            AgacDugum *dugum = agac_ara(agac, tc);
            if (dugum == NULL) {
                printf("Hasta kaydi bulunamadi, siraya alinmadi.\n");
                break;
            }
            if (dugum->hasta->durum == 1) {
                printf("Hasta su anda muayenede, yeniden siraya alinamaz.\n");
                break;
            }
            if (kuyruk_iceriyor(&kuyruk, tc)) {
                printf("Hasta zaten sirada bekliyor.\n");
                break;
            }
            if (kuyruk_ekle(&kuyruk, tc, dugum->hasta->ad)) {
                printf("Hasta siraya alindi. Sirada %d hasta var.\n", kuyruk.adet);
            } else {
                printf("Hasta siraya alinamadi.\n");
            }
            break;
        }

        case 7: {
            int tc = 0;
            char ad[BEKLEYEN_AD_UZUNLUK];
            if (kuyruk_cikar(&kuyruk, &tc, ad)) {
                AgacDugum *dugum = agac_ara(agac, tc);
                if (dugum != NULL) {
                    dugum->hasta->durum = 1;
                }
                printf("Siradaki hasta cagrildi: %d %s (muayeneye alindi)\n", tc, ad);
            } else {
                printf("Sirada bekleyen hasta yok.\n");
            }
            break;
        }

        case 8: {
            int tc = 0;
            if (!sayi_oku("Muayenesi bitecek hasta no: ", &tc)) {
                printf("Gecersiz numara.\n");
                break;
            }
            AgacDugum *dugum = agac_ara(agac, tc);
            if (dugum == NULL) {
                printf("Hasta kaydi bulunamadi.\n");
            } else if (dugum->hasta->durum == 0) {
                printf("Bu hasta su anda muayenede degil.\n");
            } else {
                dugum->hasta->durum = 0;
                printf("Muayene tamamlandi: %d\n", tc);
            }
            break;
        }

        case 9: {
            Islem cikan;
            cikan.tur = (IslemTuru)0;
            yigit = yigit_al(yigit, &cikan);
            if (yigit == NULL && cikan.tur == 0) {
                printf("Geri alinacak islem yok.\n");
                break;
            }
            if (cikan.tur == ISLEM_EKLE) {
                /* Once agac dugumu kaldirilir. AgacDugum hasta isaretcisi uzerinden tc
                 * okudugu icin kayit_sil'den sonra cagrilirsa serbest birakilmis
                 * bellege erisilir (use-after-free). */
                agac = agac_sil(agac, cikan.yedek.tc);
                kayitlar = kayit_sil(kayitlar, cikan.yedek.tc, NULL);
                if (kuyruk_sil(&kuyruk, cikan.yedek.tc)) {
                    printf("Hasta muayene sirasindan da cikarildi.\n");
                }
                printf("Geri alindi: %d numarali kayit eklemesi iptal edildi.\n", cikan.yedek.tc);
            } else {
                int eklendi = 0;
                kayitlar = kayit_ekle(kayitlar, cikan.yedek.tc, cikan.yedek.ad,
                                      cikan.yedek.yas, cikan.yedek.poliklinik, &eklendi);
                if (!eklendi) {
                    printf("Geri alinamadi, bellek yetersiz.\n");
                    break;
                }
                Hasta *geri = kayit_ara(kayitlar, cikan.yedek.tc);
                if (geri != NULL) {
                    geri->durum = cikan.yedek.durum;
                    agac = agac_ekle(agac, geri);
                }
                printf("Geri alindi: %d numarali silme islemi iptal edildi.\n", cikan.yedek.tc);
                if (cikan.yedek.durum == 1) {
                    printf("Kayit muayenede durumunda geri geldi.\n");
                }
            }
            break;
        }

        case 10:
            printf("---- AGAC GORUNUMU (yatay) ----\n");
            agac_ciz(agac);
            break;

        case 11:
            poliklinik_listele(poliklinikSon);
            poliklinikSon = poliklinik_ilerle(poliklinikSon);
            printf("Bugunun nobetci poliklinigi: %s\n", poliklinikSon->ad);
            break;

        case 12:
            kuyruk_listele(&kuyruk);
            break;

        case 0:
            calisiyor = 0;
            break;

        default:
            printf("Gecersiz secim. Menudeki bir numarayi girin.\n");
            break;
        }
    }

    kayit = dosya_yaz(veriYolu, kayitlar);
    printf("%d kayit dosyaya yazildi. Program kapatiliyor.\n", kayit);

    /* Bellek temizligi: her yapi kendi dugumlerini birakir */
    yigit_serbest(yigit);
    kuyruk_serbest(&kuyruk);
    poliklinik_serbest(poliklinikSon);
    agac_serbest(agac);
    kayit_serbest(kayitlar);
    return 0;
}

static void menuyu_yaz(void) {
    printf("\n=== HASTANE HASTA SIRA VE BEKLEME SISTEMI ===\n");
    printf(" 1) Hasta kaydi ekle\n");
    printf(" 2) Hasta kaydi sil\n");
    printf(" 3) Numaraya gore hasta ara (agac)\n");
    printf(" 4) Kayitlari sirali listele (agac)\n");
    printf(" 5) Kayitlari liste sirasinda goster (bagli liste)\n");
    printf(" 6) Siraya hasta ekle (kuyruk)\n");
    printf(" 7) Siradaki hastayi cagir\n");
    printf(" 8) Muayeneyi bitir\n");
    printf(" 9) Son islemi geri al (yigit)\n");
    printf("10) Agaci ekrana ciz\n");
    printf("11) Nobetci poliklinik turu (dairesel liste)\n");
    printf("12) Muayene sirasini goster\n");
    printf(" 0) Cikis\n");
}

/* Milisaniye cozunurluklu saat. clock() yerine kullanildi,
   cunku clock() Windows'ta 15 ms adimlarla ilerliyor. */
static double simdi_ms(void) {
    struct timespec ts;
    timespec_get(&ts, TIME_UTC);
    return (double)ts.tv_sec * 1000.0 + (double)ts.tv_nsec / 1000000.0;
}

/*
 * Kullanicidan sayi okur. Harf girilirse 0 doner ve program cokmez,
 * cagiran taraf uyari yazip menuye geri doner.
 */
static int sayi_oku(const char *soru, int *hedef) {
    char satir[GIRDI_UZUNLUK];
    char *son = NULL;
    long long deger;

    printf("%s", soru);
    if (fgets(satir, GIRDI_UZUNLUK, stdin) == NULL) {
        girdi_bitti = 1;
        return 0;
    }
    /* Satir tampona sigmadiysa kalan karakterleri at, sonraki giris kaymasin */
    if (strchr(satir, '\n') == NULL) {
        int c;
        while ((c = getchar()) != '\n' && c != EOF) {
            /* bosalt */
        }
    }

    /* Windows uzerinde long 32 bit oldugu icin strtol tasan degeri
     * LONG_MAX'a sabitler ve hata sessizce kaybolur. strtoll ile 64 bit
     * cozumleyip aralik denetimi elle yapiliyor. */
    errno = 0;
    deger = strtoll(satir, &son, 10);
    if (errno == ERANGE) {
        return 0;                       /* tasma */
    }
    if (son == satir) {
        return 0;                       /* hic sayi yok */
    }
    while (*son == ' ' || *son == '\t' || *son == '\r' || *son == '\n') {
        son++;
    }
    if (*son != '\0') {
        return 0;                       /* 12abc gibi girdiler reddedilir */
    }
    if (deger < INT_MIN || deger > INT_MAX) {
        return 0;                       /* tasma */
    }
    *hedef = (int)deger;
    return 1;
}

static void metin_oku(const char *soru, char *hedef, int uzunluk) {
    char satir[GIRDI_UZUNLUK];
    printf("%s", soru);
    if (fgets(satir, GIRDI_UZUNLUK, stdin) == NULL) {
        girdi_bitti = 1;
        hedef[0] = '\0';
        return;
    }
    /* Uzun girislerde satir sonuna kadar okuyup tamponu bosalt */
    if (strchr(satir, '\n') == NULL) {
        int c;
        while ((c = getchar()) != '\n' && c != EOF) {
            /* bosalt */
        }
    }
    satir[strcspn(satir, "\r\n")] = '\0';
    snprintf(hedef, (size_t)uzunluk, "%.*s", uzunluk - 1, satir);
}

static Hasta *hasta_ekle_akis(Hasta *kayitlar, AgacDugum **agac, Islem **yigit) {
    int tc = 0;
    int yas = 0;
    char ad[AD_UZUNLUK];
    char poliklinik[POLIKLINIK_UZUNLUK];
    int eklendi = 0;
    int yigitOk = 0;
    Hasta *eklenen = NULL;

    if (!sayi_oku("Hasta no: ", &tc) || tc <= 0) {
        printf("Gecersiz numara, kayit eklenmedi.\n");
        return kayitlar;
    }
    if (agac_ara(*agac, tc) != NULL) {
        printf("Bu numara zaten kayitli, tekrar eklenmedi.\n");
        return kayitlar;
    }

    metin_oku("Hasta adi soyadi: ", ad, AD_UZUNLUK);
    if (ad[0] == '\0') {
        printf("Hasta adi bos olamaz, kayit eklenmedi.\n");
        return kayitlar;
    }
    if (!sayi_oku("Yas: ", &yas) || yas < 0 || yas > YAS_UST) {
        printf("Gecersiz yas, kayit eklenmedi.\n");
        return kayitlar;
    }
    metin_oku("Poliklinik: ", poliklinik, POLIKLINIK_UZUNLUK);
    if (poliklinik[0] == '\0') {
        printf("Poliklinik bos olamaz, kayit eklenmedi.\n");
        return kayitlar;
    }

    kayitlar = kayit_ekle(kayitlar, tc, ad, yas, poliklinik, &eklendi);
    if (!eklendi) {
        printf("Kayit eklenemedi.\n");
        return kayitlar;
    }
    eklenen = kayit_ara(kayitlar, tc);
    if (eklenen == NULL) {
        printf("Kayit eklenemedi.\n");
        return kayitlar;
    }
    *agac = agac_ekle(*agac, eklenen);
    *yigit = yigit_ekle(*yigit, ISLEM_EKLE, eklenen, &yigitOk);
    printf("Hasta kaydi eklendi: %d\n", tc);
    if (!yigitOk) {
        printf("Uyari: geri alma kaydi tutulamadi.\n");
    }
    return kayitlar;
}

static Hasta *hasta_sil_akis(Hasta *kayitlar, AgacDugum **agac, Islem **yigit, Kuyruk *kuyruk) {
    int tc = 0;
    int yigitOk = 0;
    int sirada = 0;
    int muayenede = 0;
    Hasta yedek;
    Hasta *bulunan = NULL;

    if (!sayi_oku("Silinecek hasta no: ", &tc) || tc <= 0) {
        printf("Gecersiz numara.\n");
        return kayitlar;
    }

    bulunan = kayit_ara(kayitlar, tc);
    if (bulunan == NULL) {
        printf("Kayit bulunamadi.\n");
        return kayitlar;
    }

    sirada = kuyruk_iceriyor(kuyruk, tc);
    muayenede = bulunan->durum;
    /* Ayni gerekce: agac dugumu serbest birakilmadan once kaldirilmali. */
    *agac = agac_sil(*agac, tc);
    kayitlar = kayit_sil(kayitlar, tc, &yedek);
    if (sirada) {
        (void)kuyruk_sil(kuyruk, tc);
    }
    *yigit = yigit_ekle(*yigit, ISLEM_SIL, &yedek, &yigitOk);
    printf("Hasta kaydi silindi: %d (geri alinabilir)\n", tc);
    if (sirada) {
        printf("Hasta muayene sirasindan da cikarildi.\n");
    }
    if (muayenede) {
        printf("Uyari: silinen hasta muayenede gorunuyordu.\n");
    }
    if (!yigitOk) {
        printf("Uyari: geri alma kaydi tutulamadi.\n");
    }
    return kayitlar;
}

/*
 * Deneysel olcum. Ayni is yuku hem bagli listeye hem agaca verilir,
 * sureler karsilastirilir. Cikti CSV bicimindedir, rapor tablosu bu
 * veriden uretilir.
 */
static void benchmark(void) {
    const int boyutlar[3] = {1000, 10000, 100000};
    int i, j;
    FILE *csv = fopen("03_Olcum/benchmark.csv", "w");

    printf("boyut;ekleme_liste_ms;ekleme_agac_ms;arama_liste_ms;arama_agac_ms;agac_yukseklik\n");
    if (csv != NULL) {
        fprintf(csv, "boyut;ekleme_liste_ms;ekleme_agac_ms;arama_liste_ms;arama_agac_ms;agac_yukseklik\n");
    } else {
        printf("Uyari: 03_Olcum/benchmark.csv yazilamadi, sonuclar yalnizca ekranda.\n");
    }

    for (i = 0; i < 3; i++) {
        int n = boyutlar[i];
        Hasta *kayitlar = NULL;
        AgacDugum *agac = NULL;
        int *numaralar = (int *)malloc(sizeof(int) * (size_t)n);
        double bas, son;
        double eklemeListe, eklemeAgac, aramaListe, aramaAgac;

        if (numaralar == NULL) {
            printf("Bellek yetersiz.\n");
            return;
            if (csv != NULL) {
                fclose(csv);
            }
        }

        /* Karisik sirada numara uret, aksi halde agac zincire doner */
        for (j = 0; j < n; j++) {
            numaralar[j] = (j * 7919) % (n * 3) + 1;
        }

        bas = simdi_ms();
        for (j = 0; j < n; j++) {
            int eklendi = 0;
            kayitlar = kayit_ekle(kayitlar, numaralar[j], "Deneme", 30, "Dahiliye", &eklendi);
            if (!eklendi) {
                break;
            }
        }
        son = simdi_ms();
        eklemeListe = son - bas;

        /* Agaca ekleme icin listenin tamamini gezmek gerekmiyor,
           dugum isaretcisini tutan bir dizi kullaniyoruz */
        Hasta **isaretciler = (Hasta **)malloc(sizeof(Hasta *) * (size_t)n);
        if (isaretciler == NULL) {
            printf("Bellek yetersiz.\n");
            free(numaralar);
            agac_serbest(agac);
            kayit_serbest(kayitlar);
            if (csv != NULL) {
                fclose(csv);
            }
            return;
        }
        Hasta *gezen = kayitlar;
        for (j = n - 1; j >= 0; j--) {
            isaretciler[j] = gezen;
            gezen = gezen->sonraki;
        }

        bas = simdi_ms();
        for (j = 0; j < n; j++) {
            agac = agac_ekle(agac, isaretciler[j]);
        }
        son = simdi_ms();
        eklemeAgac = son - bas;

        bas = simdi_ms();
        for (j = 0; j < n; j++) {
            (void)kayit_ara(kayitlar, numaralar[j]);
        }
        son = simdi_ms();
        aramaListe = son - bas;

        bas = simdi_ms();
        for (j = 0; j < n; j++) {
            (void)agac_ara(agac, numaralar[j]);
        }
        son = simdi_ms();
        aramaAgac = son - bas;

        printf("%d;%.3f;%.3f;%.3f;%.3f;%d\n", n, eklemeListe, eklemeAgac,
               aramaListe, aramaAgac, agac_yukseklik(agac));
        if (csv != NULL) {
            fprintf(csv, "%d;%.3f;%.3f;%.3f;%.3f;%d\n", n, eklemeListe, eklemeAgac,
                    aramaListe, aramaAgac, agac_yukseklik(agac));
        }

        free(isaretciler);
        free(numaralar);
        agac_serbest(agac);
        kayit_serbest(kayitlar);
    }
    if (csv != NULL) {
        fclose(csv);
        printf("Olcumler 03_Olcum/benchmark.csv dosyasina yazildi.\n");
    }
}
