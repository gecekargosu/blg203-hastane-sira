#include <stdio.h>
#include <stdlib.h>
#include "agac.h"

/*
 * Ikili arama agacina ekleme. Kucuk numaralar sola, buyukler saga gider.
 * Ortalama durumda logaritmik, sirali veri gelirse agac zincire donusur ve
 * arama dogrusal olur. Bu davranis deneysel bolumde olculmustur.
 */
AgacDugum *agac_ekle(AgacDugum *kok, Hasta *h) {
    if (kok == NULL) {
        AgacDugum *yeni = (AgacDugum *)malloc(sizeof(AgacDugum));
        if (yeni == NULL) {
            printf("Bellek yetersiz, agac dugumu acilamadi.\n");
            return NULL;
        }
        yeni->hasta = h;
        yeni->sol = NULL;
        yeni->sag = NULL;
        return yeni;
    }

    if (h->tc < kok->hasta->tc) {
        kok->sol = agac_ekle(kok->sol, h);
    } else if (h->tc > kok->hasta->tc) {
        kok->sag = agac_ekle(kok->sag, h);
    }
    /* Ayni numara varsa tekrar eklenmez, kayit numarasi benzersiz. */
    return kok;
}

/* Numaraya gore arama. Ortalama O(log n). */
AgacDugum *agac_ara(AgacDugum *kok, int tc) {
    if (kok == NULL) {
        return NULL;
    }
    if (tc == kok->hasta->tc) {
        return kok;
    }
    if (tc < kok->hasta->tc) {
        return agac_ara(kok->sol, tc);
    }
    return agac_ara(kok->sag, tc);
}

/*
 * Silme islemi uc durumu ayirir. Yaprak dugum, tek cocuklu dugum ve
 * iki cocuklu dugum. Iki cocuk varsa sag alt agacin en kucuk dugumu
 * yerine konur, bu standart yaklasimdir.
 */
AgacDugum *agac_sil(AgacDugum *kok, int tc) {
    if (kok == NULL) {
        return NULL;
    }

    if (tc < kok->hasta->tc) {
        kok->sol = agac_sil(kok->sol, tc);
    } else if (tc > kok->hasta->tc) {
        kok->sag = agac_sil(kok->sag, tc);
    } else {
        if (kok->sol == NULL) {
            AgacDugum *sag = kok->sag;
            free(kok);
            return sag;
        }
        if (kok->sag == NULL) {
            AgacDugum *sol = kok->sol;
            free(kok);
            return sol;
        }
        AgacDugum *enKucuk = kok->sag;
        while (enKucuk->sol != NULL) {
            enKucuk = enKucuk->sol;
        }
        kok->hasta = enKucuk->hasta;
        kok->sag = agac_sil(kok->sag, enKucuk->hasta->tc);
    }
    return kok;
}

/* Sirali dolasma: kucukten buyuge, yani hasta numarasina gore artan. */
void agac_sirali(const AgacDugum *kok) {
    if (kok == NULL) {
        return;
    }
    agac_sirali(kok->sol);
    printf("%5d | %-28s | %3d yas | %-22s | %s\n",
           kok->hasta->tc, kok->hasta->ad, kok->hasta->yas, kok->hasta->poliklinik,
           kok->hasta->durum ? "muayenede" : "bekliyor");
    agac_sirali(kok->sag);
}

/*
 * Agaci ekrana yatay cizer. Ek puan icin eklenen gorsellestirme.
 * Sag alt agac ustte, sol alt agac altta gorunur.
 */
static void ciz_yardimci(const AgacDugum *kok, int derinlik) {
    if (kok == NULL) {
        return;
    }
    ciz_yardimci(kok->sag, derinlik + 1);
    for (int i = 0; i < derinlik; i++) {
        printf("        ");
    }
    printf("[%d] %s\n", kok->hasta->tc, kok->hasta->ad);
    ciz_yardimci(kok->sol, derinlik + 1);
}

void agac_ciz(const AgacDugum *kok) {
    if (kok == NULL) {
        printf("Agac bos.\n");
        return;
    }
    ciz_yardimci(kok, 0);
}

/* Agacin yuksekligi. Tek dugumde 1 doner, bos agacta 0. */
int agac_yukseklik(const AgacDugum *kok) {
    if (kok == NULL) {
        return 0;
    }
    int sol = agac_yukseklik(kok->sol);
    int sag = agac_yukseklik(kok->sag);
    return 1 + (sol > sag ? sol : sag);
}

/* Agactaki dugum sayisi. */
int agac_dugum_say(const AgacDugum *kok) {
    if (kok == NULL) {
        return 0;
    }
    return 1 + agac_dugum_say(kok->sol) + agac_dugum_say(kok->sag);
}

/* Butun agac dugumlerini serbest birakir. Hasta kayitlarina dokunmaz. */
void agac_serbest(AgacDugum *kok) {
    if (kok == NULL) {
        return;
    }
    agac_serbest(kok->sol);
    agac_serbest(kok->sag);
    free(kok);
}
