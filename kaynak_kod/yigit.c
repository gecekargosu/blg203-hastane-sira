#include <stdio.h>
#include <stdlib.h>
#include "yigit.h"

/*
 * Yigita eleman ekleme. Yigit bagli liste ile kuruldu, ekleme ve
 * cikarma listenin basindan yapildigi icin ikisi de sabit zamandadir.
 * Dizi ile kurulsaydi sabit bir geri alma derinligi secmek gerekirdi.
 */
Islem *yigit_ekle(Islem *tepe, IslemTuru tur, const Hasta *h) {
    Islem *yeni = (Islem *)malloc(sizeof(Islem));
    if (yeni == NULL) {
        printf("Bellek yetersiz, islem kaydi tutulamadi.\n");
        return tepe;
    }
    yeni->tur = tur;
    yeni->yedek = *h;
    yeni->yedek.sonraki = NULL;
    yeni->sonraki = tepe;
    return yeni;
}

/* Yigitin tepesindeki kaydi cikarir ve icerigini cagirana verir. */
Islem *yigit_al(Islem *tepe, Islem *cikan) {
    if (tepe == NULL) {
        return NULL;
    }
    Islem *yeniTepe = tepe->sonraki;
    if (cikan != NULL) {
        *cikan = *tepe;
        cikan->sonraki = NULL;
    }
    free(tepe);
    return yeniTepe;
}

int yigit_bos(const Islem *tepe) {
    return tepe == NULL;
}

void yigit_serbest(Islem *tepe) {
    Islem *gezen = tepe;
    Islem *sonraki = NULL;
    while (gezen != NULL) {
        sonraki = gezen->sonraki;
        free(gezen);
        gezen = sonraki;
    }
}
