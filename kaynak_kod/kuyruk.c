#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "kuyruk.h"

void kuyruk_baslat(Kuyruk *k) {
    k->on = NULL;
    k->arka = NULL;
    k->adet = 0;
}

/* Numarasi verilen hasta kuyrukta bekliyor mu? */
int kuyruk_iceriyor(const Kuyruk *k, int tc) {
    const Bekleyen *gezen = k->on;
    while (gezen != NULL) {
        if (gezen->tc == tc) {
            return 1;
        }
        gezen = gezen->sonraki;
    }
    return 0;
}

/*
 * Kuyrugun sonuna ekleme. Ilk gelen ilk cikar kurali geregi
 * hastalar bu sirada cagrilir. Ayni numara ikinci kez eklenmez,
 * boylece kayit defteri ile sira birbirinden kopmaz.
 * Bellek ayrilamazsa 0 doner ve cagiran taraf kullaniciya bildirir.
 */
int kuyruk_ekle(Kuyruk *k, int tc, const char *ad) {
    Bekleyen *yeni;

    if (kuyruk_iceriyor(k, tc)) {
        return 0;
    }
    yeni = (Bekleyen *)malloc(sizeof(Bekleyen));
    if (yeni == NULL) {
        printf("Bellek yetersiz, hasta siraya eklenemedi.\n");
        return 0;
    }
    yeni->tc = tc;
    snprintf(yeni->ad, BEKLEYEN_AD_UZUNLUK, "%s", ad);
    yeni->sonraki = NULL;

    if (k->arka == NULL) {
        k->on = yeni;
        k->arka = yeni;
    } else {
        k->arka->sonraki = yeni;
        k->arka = yeni;
    }
    k->adet++;
    return 1;
}

/*
 * Siradan cikarma. Kayit defterinden silinen hasta kuyrukta
 * beklemesin diye kullanilir. Bulunursa 1, bulunamazsa 0 doner.
 */
int kuyruk_sil(Kuyruk *k, int tc) {
    Bekleyen *gezen = k->on;
    Bekleyen *onceki = NULL;

    while (gezen != NULL && gezen->tc != tc) {
        onceki = gezen;
        gezen = gezen->sonraki;
    }
    if (gezen == NULL) {
        return 0;
    }
    if (onceki == NULL) {
        k->on = gezen->sonraki;
    } else {
        onceki->sonraki = gezen->sonraki;
    }
    if (k->arka == gezen) {
        k->arka = onceki;
    }
    free(gezen);
    k->adet--;
    return 1;
}

/*
 * Kuyrugun basindan cikarma. Bos kuyrukta 0 doner, cagiran taraf
 * kullaniciya mesaj verir. Program cokmez.
 */
int kuyruk_cikar(Kuyruk *k, int *tc, char *ad) {
    if (k->on == NULL) {
        return 0;
    }
    Bekleyen *cikan = k->on;
    *tc = cikan->tc;
    if (ad != NULL) {
        snprintf(ad, BEKLEYEN_AD_UZUNLUK, "%s", cikan->ad);
    }
    k->on = cikan->sonraki;
    if (k->on == NULL) {
        k->arka = NULL;
    }
    free(cikan);
    k->adet--;
    return 1;
}

void kuyruk_listele(const Kuyruk *k) {
    const Bekleyen *gezen = k->on;
    int sira = 1;

    printf("---- MUAYENE SIRASI (%d hasta) ----\n", k->adet);
    if (gezen == NULL) {
        printf("Sirada bekleyen hasta yok.\n");
        return;
    }
    while (gezen != NULL) {
        printf("%2d. sirada | %5d | %s\n", sira, gezen->tc, gezen->ad);
        gezen = gezen->sonraki;
        sira++;
    }
}

/* Butun kuyruk dugumlerini serbest birakir. */
void kuyruk_serbest(Kuyruk *k) {
    Bekleyen *gezen = k->on;
    Bekleyen *sonraki = NULL;
    while (gezen != NULL) {
        sonraki = gezen->sonraki;
        free(gezen);
        gezen = sonraki;
    }
    k->on = NULL;
    k->arka = NULL;
    k->adet = 0;
}
