#ifndef KUYRUK_H
#define KUYRUK_H

#define BEKLEYEN_AD_UZUNLUK 64

/* Sirada bekleyen hasta kaydi. Kuyruk dugumu. */
typedef struct Bekleyen {
    int tc;
    char ad[BEKLEYEN_AD_UZUNLUK];
    struct Bekleyen *sonraki;
} Bekleyen;

/*
 * Kuyruk yapisi. Bas ve son isaretcisi birlikte tutuluyor, boylece
 * eleman ekleme O(1) oluyor. Tek isaretci olsaydi her eklemede
 * listenin sonuna kadar yurumek gerekirdi.
 */
typedef struct Kuyruk {
    Bekleyen *on;
    Bekleyen *arka;
    int adet;
} Kuyruk;

void kuyruk_baslat(Kuyruk *k);
void kuyruk_ekle(Kuyruk *k, int tc, const char *ad);
int  kuyruk_cikar(Kuyruk *k, int *tc, char *ad);
void kuyruk_listele(const Kuyruk *k);
void kuyruk_serbest(Kuyruk *k);

#endif
