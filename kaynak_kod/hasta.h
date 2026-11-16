#ifndef HASTA_H
#define HASTA_H

#define AD_UZUNLUK 64
#define POLIKLINIK_UZUNLUK 48

/*
 * Hasta kaydinin tutuldugu yapi. Tek yonlu bagli listenin dugumu.
 * Agac ayni kayda isaretci ile baglanir, kayit bellekte tek kopya durur.
 */
typedef struct Hasta {
    int tc;                          /* hasta numarasi, arama anahtari */
    char ad[AD_UZUNLUK];
    int yas;
    char poliklinik[POLIKLINIK_UZUNLUK];
    int durum;                       /* 0 bekliyor, 1 muayenede */
    struct Hasta *sonraki;           /* bagli liste baglantisi */
} Hasta;

/*
 * Kayit defteri: tek yonlu bagli liste islemleri.
 * kayit_ekle bellek ayiramazsa listeyi degistirmez ve basarili
 * isaretini 0 yapar; cagiran taraf NULL kayitla islem yapmaz.
 */
Hasta *kayit_ekle(Hasta *bas, int tc, const char *ad, int yas,
                  const char *poliklinik, int *basarili);
Hasta *kayit_sil(Hasta *bas, int tc, Hasta *silinen);
Hasta *kayit_ara(Hasta *bas, int tc);
void   kayit_listele(const Hasta *bas);
int    kayit_say(const Hasta *bas);
void   kayit_serbest(Hasta *bas);

#endif
