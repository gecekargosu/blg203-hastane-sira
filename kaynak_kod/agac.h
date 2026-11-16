#ifndef AGAC_H
#define AGAC_H

#include "hasta.h"

/*
 * Ikili arama agaci dugumu. Dugum hastayi isaretci ile tutar,
 * boylece ayni kayit hem listede hem agacta tek kopya olarak durur.
 */
typedef struct AgacDugum {
    Hasta *hasta;
    struct AgacDugum *sol;
    struct AgacDugum *sag;
} AgacDugum;

AgacDugum *agac_ekle(AgacDugum *kok, Hasta *h);
AgacDugum *agac_ara(AgacDugum *kok, int tc);
AgacDugum *agac_sil(AgacDugum *kok, int tc);
void agac_sirali(const AgacDugum *kok);
void agac_ciz(const AgacDugum *kok);
int  agac_yukseklik(const AgacDugum *kok);
int  agac_dugum_say(const AgacDugum *kok);
void agac_serbest(AgacDugum *kok);

#endif
