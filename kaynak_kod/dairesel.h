#ifndef DAIRESEL_H
#define DAIRESEL_H

#define POLIKLINIK_AD_UZUNLUK 40

/* Dairesel listenin dugumu. Son elemanin sonraki alani basa doner. */
typedef struct Poliklinik {
    int kod;
    char ad[POLIKLINIK_AD_UZUNLUK];
    struct Poliklinik *sonraki;
} Poliklinik;

Poliklinik *poliklinik_ekle(Poliklinik *son, int kod, const char *ad);
Poliklinik *poliklinik_ilerle(Poliklinik *son);
void poliklinik_listele(const Poliklinik *son);
int  poliklinik_say(const Poliklinik *son);
void poliklinik_serbest(Poliklinik *son);

#endif
