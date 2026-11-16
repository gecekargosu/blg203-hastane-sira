#ifndef YIGIT_H
#define YIGIT_H

#include "hasta.h"

/* Geri alinabilecek islem turleri */
typedef enum {
    ISLEM_EKLE = 1,
    ISLEM_SIL = 2
} IslemTuru;

/*
 * Geri alma yigiti. Yapilan her degisiklik, tersini uygulayabilmek
 * icin gereken bilgiyle birlikte burada saklanir.
 */
typedef struct Islem {
    IslemTuru tur;
    Hasta yedek;            /* eklenen ya da silinen kaydin kopyasi */
    struct Islem *sonraki;  /* yigit baglantisi */
} Islem;

Islem *yigit_ekle(Islem *tepe, IslemTuru tur, const Hasta *h);
Islem *yigit_al(Islem *tepe, Islem *cikan);
int    yigit_bos(const Islem *tepe);
void   yigit_serbest(Islem *tepe);

#endif
