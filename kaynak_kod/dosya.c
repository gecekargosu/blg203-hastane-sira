#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dosya.h"

#define SATIR_UZUNLUK 256

/*
 * Dosya bicimi: tc;ad;yas;poliklinik;durum
 * Alanlar noktali virgul ile ayrilir, boylece ad alanindaki bosluk ve
 * virgul ayristirmayi bozmaz.
 *
 * Dosya bulunamazsa program cokmez, -1 doner ve cagiran taraf
 * kullaniciya mesaj verip bos kayitla devam eder.
 */
int dosya_oku(const char *yol, Hasta **kayitlar, AgacDugum **agac) {
    FILE *dosya = fopen(yol, "r");
    char satir[SATIR_UZUNLUK];
    int sayac = 0;

    if (dosya == NULL) {
        return -1;
    }

    /* Baslik satiri varsa atla */
    if (fgets(satir, SATIR_UZUNLUK, dosya) == NULL) {
        fclose(dosya);
        return 0;
    }

    while (fgets(satir, SATIR_UZUNLUK, dosya) != NULL) {
        char *tcMetin = strtok(satir, ";");
        char *ad = strtok(NULL, ";");
        char *yasMetin = strtok(NULL, ";");
        char *poliklinik = strtok(NULL, ";");
        char *durumMetin = strtok(NULL, ";\r\n");

        if (tcMetin == NULL || ad == NULL || poliklinik == NULL) {
            continue;   /* bozuk satiri atla, program durmaz */
        }

        int tc = atoi(tcMetin);
        int yas = (yasMetin != NULL) ? atoi(yasMetin) : 0;
        int durum = (durumMetin != NULL) ? atoi(durumMetin) : 0;

        *kayitlar = kayit_ekle(*kayitlar, tc, ad, yas, poliklinik);
        Hasta *eklenen = kayit_ara(*kayitlar, tc);
        if (eklenen != NULL) {
            eklenen->durum = durum;
            *agac = agac_ekle(*agac, eklenen);
        }
        sayac++;
    }

    fclose(dosya);
    return sayac;
}

/* Kayitlari dosyaya yazar. Her kayit tek satir. */
int dosya_yaz(const char *yol, const Hasta *kayitlar) {
    FILE *dosya = fopen(yol, "w");
    const Hasta *gezen = kayitlar;
    int sayac = 0;

    if (dosya == NULL) {
        printf("Dosya yazilamadi: %s\n", yol);
        return -1;
    }

    fprintf(dosya, "tc;ad;yas;poliklinik;durum\n");
    while (gezen != NULL) {
        fprintf(dosya, "%d;%s;%d;%s;%d\n",
                gezen->tc, gezen->ad, gezen->yas, gezen->poliklinik, gezen->durum);
        gezen = gezen->sonraki;
        sayac++;
    }

    fclose(dosya);
    return sayac;
}
