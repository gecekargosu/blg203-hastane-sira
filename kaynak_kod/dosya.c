#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include "dosya.h"

#define SATIR_UZUNLUK 256
#define YAS_UST 130

/*
 * Metnin tamami sayi mi? Bossa, sonda harf varsa (12abc) veya deger
 * int araligini asiyorsa 0 doner. atoi sessizce sifir urettigi icin
 * alanlar bu kati kuralla okunur.
 */
static int sayi_alani(const char *metin, int *hedef) {
    char *son = NULL;
    long deger;

    if (metin == NULL) {
        return 0;
    }
    while (*metin == ' ' || *metin == '\t') {
        metin++;
    }
    if (*metin == '\0') {
        return 0;
    }
    deger = strtol(metin, &son, 10);
    if (son == metin) {
        return 0;
    }
    while (*son == ' ' || *son == '\t') {
        son++;
    }
    if (*son != '\0') {
        return 0;
    }
    if (deger < INT_MIN || deger > INT_MAX) {
        return 0;
    }
    *hedef = (int)deger;
    return 1;
}

/*
 * Dosya bicimi: tc;ad;yas;poliklinik;durum
 * Alanlar noktali virgul ile ayrilir, boylece ad alanindaki bosluk ve
 * virgul ayristirmayi bozmaz.
 *
 * Kurallar:
 *  - Baslik satiri "tc;" ile basliyorsa atlanir, degilse veri sayilir.
 *  - Hasta numarasi pozitif tam sayi olmali ve tekrar etmemelidir.
 *  - Ad ve poliklinik bos olamaz, yas 0 ile 130 arasinda olmali.
 *  - Bozuk satir programi durdurmaz, atlanir ve sayisi bildirilir.
 *
 * Dosya bulunamazsa -1 doner ve cagiran taraf bos kayitla devam eder.
 */
int dosya_oku(const char *yol, Hasta **kayitlar, AgacDugum **agac) {
    FILE *dosya = fopen(yol, "r");
    char satir[SATIR_UZUNLUK];
    int sayac = 0;
    int atlanan = 0;
    int ilkSatir = 1;

    if (dosya == NULL) {
        return -1;
    }

    while (fgets(satir, SATIR_UZUNLUK, dosya) != NULL) {
        char *tcMetin;
        char *ad;
        char *yasMetin;
        char *poliklinik;
        char *durumMetin;
        int tc = 0;
        int yas = 0;
        int durum = 0;
        int eklendi = 0;
        Hasta *eklenen = NULL;

        if (ilkSatir && strncmp(satir, "tc;", 3) == 0) {
            ilkSatir = 0;
            continue;               /* baslik satiri */
        }
        ilkSatir = 0;

        tcMetin = strtok(satir, ";");
        ad = strtok(NULL, ";");
        yasMetin = strtok(NULL, ";");
        poliklinik = strtok(NULL, ";");
        durumMetin = strtok(NULL, ";\r\n");

        if (tcMetin == NULL || ad == NULL || poliklinik == NULL) {
            atlanan++;
            continue;
        }
        if (!sayi_alani(tcMetin, &tc) || tc <= 0) {
            atlanan++;
            continue;
        }
        if (ad[0] == '\0' || poliklinik[0] == '\0') {
            atlanan++;
            continue;
        }
        if (yasMetin != NULL && yasMetin[0] != '\0') {
            if (!sayi_alani(yasMetin, &yas) || yas < 0 || yas > YAS_UST) {
                atlanan++;
                continue;
            }
        }
        if (durumMetin != NULL && durumMetin[0] != '\0') {
            int okunan = 0;
            if (!sayi_alani(durumMetin, &okunan) || (okunan != 0 && okunan != 1)) {
                okunan = 0;         /* gecersiz durum "bekliyor" sayilir */
            }
            durum = okunan;
        }
        if (agac_ara(*agac, tc) != NULL) {
            atlanan++;              /* mukerrer hasta numarasi */
            continue;
        }

        *kayitlar = kayit_ekle(*kayitlar, tc, ad, yas, poliklinik, &eklendi);
        if (!eklendi) {
            atlanan++;
            break;                  /* bellek bitti, okumayi surdurmenin anlami yok */
        }
        eklenen = kayit_ara(*kayitlar, tc);
        if (eklenen != NULL) {
            eklenen->durum = durum;
            *agac = agac_ekle(*agac, eklenen);
        }
        sayac++;
    }

    fclose(dosya);
    if (atlanan > 0) {
        printf("Uyari: %d satir gecersiz veya mukerrer oldugu icin atlandi.\n", atlanan);
    }
    return sayac;
}

/* Kayitlari dosyaya yazar. Her kayit tek satir. */
int dosya_yaz(const char *yol, const Hasta *kayitlar) {
    FILE *dosya = fopen(yol, "w");
    const Hasta *gezen = kayitlar;
    const Hasta **isaretciler = NULL;
    int sayac = 0;
    int i;

    if (dosya == NULL) {
        printf("Dosya yazilamadi: %s\n", yol);
        return -1;
    }

    /* Liste basa ekleme yaptigi icin kayitlar tersten dolasilir. Dosya da
     * tersten yazilirsa dosyadaki sira bir sonraki acilista aynen korunur.
     * Liste sirasinda yazmak dosyayi her oturumda ters cevirirdi. */
    while (gezen != NULL) {
        const Hasta **yeni = (const Hasta **)realloc(isaretciler,
                                                     sizeof(Hasta *) * (size_t)(sayac + 1));
        if (yeni == NULL) {
            free(isaretciler);
            fclose(dosya);
            printf("Bellek yetersiz, dosya yazilamadi: %s\n", yol);
            return -1;
        }
        isaretciler = yeni;
        isaretciler[sayac] = gezen;
        sayac++;
        gezen = gezen->sonraki;
    }

    fprintf(dosya, "tc;ad;yas;poliklinik;durum\n");
    for (i = sayac - 1; i >= 0; i--) {
        fprintf(dosya, "%d;%s;%d;%s;%d\n",
                isaretciler[i]->tc, isaretciler[i]->ad, isaretciler[i]->yas,
                isaretciler[i]->poliklinik, isaretciler[i]->durum);
    }
    free(isaretciler);

    fclose(dosya);
    return sayac;
}
