#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dairesel.h"

/*
 * Dairesel listeye eleman ekleme. Isaretci son elemani gosterir,
 * son->sonraki her zaman ilk elemandir. Bu sayede hem basa hem sona
 * sabit zamanda erisilir.
 */
Poliklinik *poliklinik_ekle(Poliklinik *son, int kod, const char *ad) {
    Poliklinik *yeni = (Poliklinik *)malloc(sizeof(Poliklinik));
    if (yeni == NULL) {
        printf("Bellek yetersiz, poliklinik eklenemedi.\n");
        return son;
    }
    yeni->kod = kod;
    snprintf(yeni->ad, POLIKLINIK_AD_UZUNLUK, "%s", ad);

    if (son == NULL) {
        yeni->sonraki = yeni;       /* tek eleman kendine doner */
        return yeni;
    }

    yeni->sonraki = son->sonraki;   /* yeni eleman basi gosterir */
    son->sonraki = yeni;            /* eski son yeniye baglanir */
    return yeni;
}

/*
 * Nobetci poliklinik her gun bir sonrakine gecer. Dairesel liste
 * sayesinde son poliklinikten sonra basa donulur, ayri bir kontrol
 * gerekmez.
 */
Poliklinik *poliklinik_ilerle(Poliklinik *son) {
    if (son == NULL) {
        return NULL;
    }
    return son->sonraki;
}

void poliklinik_listele(const Poliklinik *son) {
    const Poliklinik *gezen = NULL;

    if (son == NULL) {
        printf("Poliklinik listesi bos.\n");
        return;
    }

    printf("---- POLIKLINIK TURU (dairesel) ----\n");
    gezen = son->sonraki;
    do {
        printf("  poliklinik %2d : %s\n", gezen->kod, gezen->ad);
        gezen = gezen->sonraki;
    } while (gezen != son->sonraki);
}

int poliklinik_say(const Poliklinik *son) {
    const Poliklinik *gezen = NULL;
    int sayac = 0;

    if (son == NULL) {
        return 0;
    }
    gezen = son->sonraki;
    do {
        sayac++;
        gezen = gezen->sonraki;
    } while (gezen != son->sonraki);
    return sayac;
}

/*
 * Dairesel listeyi serbest birakir. Son elemanin sonraki alani basa
 * dondugu icin dongu, basa geri gelince kirilir.
 */
void poliklinik_serbest(Poliklinik *son) {
    Poliklinik *bas = NULL;
    Poliklinik *gezen = NULL;
    Poliklinik *sonraki = NULL;

    if (son == NULL) {
        return;
    }
    bas = son->sonraki;
    gezen = bas;
    do {
        sonraki = gezen->sonraki;
        free(gezen);
        gezen = sonraki;
    } while (gezen != bas);
}
