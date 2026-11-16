#ifndef DOSYA_H
#define DOSYA_H

#include "hasta.h"
#include "agac.h"

/*
 * Dosyadan hasta kayitlarini yukler. Kayitlar hem bagli listeye hem
 * agaca eklenir, boylece iki yapi ayni kayitlari paylasir.
 * Donus degeri yuklenen kayit sayisidir, dosya yoksa -1.
 */
int dosya_oku(const char *yol, Hasta **kayitlar, AgacDugum **agac);

/* Kayitlari ayni bicimde dosyaya yazar. Yazilan kayit sayisini doner. */
int dosya_yaz(const char *yol, const Hasta *kayitlar);

#endif
