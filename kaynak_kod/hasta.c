#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "hasta.h"

/*
 * Yeni hasta kaydini listenin basina ekler. Basa ekleme sabit zamanli
 * oldugu icin toplu yuklemede tercih edildi. Kullaniciya gosterilen
 * sirali liste agac uzerinden uretilir.
 */
Hasta *kayit_ekle(Hasta *bas, int tc, const char *ad, int yas, const char *poliklinik) {
    Hasta *yeni = (Hasta *)malloc(sizeof(Hasta));
    if (yeni == NULL) {
        printf("Bellek yetersiz, kayit eklenemedi.\n");
        return bas;
    }
    yeni->tc = tc;
    snprintf(yeni->ad, AD_UZUNLUK, "%s", ad);
    yeni->yas = yas;
    snprintf(yeni->poliklinik, POLIKLINIK_UZUNLUK, "%s", poliklinik);
    yeni->durum = 0;
    yeni->sonraki = bas;
    return yeni;
}

/*
 * Numarasi verilen kaydi listeden cikarir. Cikarilan dugumun icerigi
 * cagirana kopyalanir, boylece geri alma yigiti bu bilgiyi saklayabilir.
 * Dugumun kendisi burada serbest birakilir.
 */
Hasta *kayit_sil(Hasta *bas, int tc, Hasta *silinen) {
    Hasta *gezen = bas;
    Hasta *onceki = NULL;

    while (gezen != NULL && gezen->tc != tc) {
        onceki = gezen;
        gezen = gezen->sonraki;
    }

    if (gezen == NULL) {
        return bas;
    }

    if (silinen != NULL) {
        *silinen = *gezen;
        silinen->sonraki = NULL;
    }

    if (onceki == NULL) {
        bas = gezen->sonraki;
    } else {
        onceki->sonraki = gezen->sonraki;
    }

    free(gezen);
    return bas;
}

/* Dogrusal arama. En kotu durumda O(n). */
Hasta *kayit_ara(Hasta *bas, int tc) {
    Hasta *gezen = bas;
    while (gezen != NULL) {
        if (gezen->tc == tc) {
            return gezen;
        }
        gezen = gezen->sonraki;
    }
    return NULL;
}

/* Listenin tamamini ekrana yazar. */
void kayit_listele(const Hasta *bas) {
    const Hasta *gezen = bas;
    int sayac = 0;

    printf("---- HASTA KAYIT DEFTERI (bagli liste sirasi) ----\n");
    while (gezen != NULL) {
        printf("%5d | %-28s | %3d yas | %-22s | %s\n",
               gezen->tc, gezen->ad, gezen->yas, gezen->poliklinik,
               gezen->durum ? "muayenede" : "bekliyor");
        gezen = gezen->sonraki;
        sayac++;
    }
    printf("Toplam kayit: %d\n", sayac);
}

/* Listedeki dugum sayisi. */
int kayit_say(const Hasta *bas) {
    int sayac = 0;
    const Hasta *gezen = bas;
    while (gezen != NULL) {
        sayac++;
        gezen = gezen->sonraki;
    }
    return sayac;
}

/*
 * Program kapanirken butun dugumleri serbest birakir.
 * Bellek sizintisi olmamasi icin her ayirmanin karsiligi burada.
 */
void kayit_serbest(Hasta *bas) {
    Hasta *gezen = bas;
    Hasta *sonraki = NULL;
    while (gezen != NULL) {
        sonraki = gezen->sonraki;
        free(gezen);
        gezen = sonraki;
    }
}
