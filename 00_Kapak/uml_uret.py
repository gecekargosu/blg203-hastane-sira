"""
UML yapi semasi ureteci (C dili surumu).
Yapi kutulari, alanlari, islevleri ve aralarindaki iliskileri tek sayfada cizer.
Kullanim: python 00_Kapak/uml_uret.py
"""
import os
import subprocess
import tempfile

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEDEF = os.path.join(KOK, "UML.pdf")

KUTU_GENISLIK = 330
SATIR_YUKSEKLIK = 15
BASLIK_YUKSEKLIK = 26


def kutu(x, y, baslik, alanlar, islevler):
    """Yapi kutusu uretir, yuksekligini dondurur."""
    icerik = []
    yukseklik = BASLIK_YUKSEKLIK + 6 + len(alanlar) * SATIR_YUKSEKLIK
    if islevler:
        yukseklik += 8 + len(islevler) * SATIR_YUKSEKLIK
    yukseklik += 8

    icerik.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#ffffff" '
                  'stroke="#1f4e79" stroke-width="1.4"/>' % (x, y, KUTU_GENISLIK, yukseklik))
    icerik.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#1f4e79"/>'
                  % (x, y, KUTU_GENISLIK, BASLIK_YUKSEKLIK))
    icerik.append('<text x="%d" y="%d" class="kbaslik">%s</text>'
                  % (x + 10, y + 18, baslik))

    cy = y + BASLIK_YUKSEKLIK + 16
    for alan in alanlar:
        icerik.append('<text x="%d" y="%d" class="alan">%s</text>' % (x + 10, cy, alan))
        cy += SATIR_YUKSEKLIK

    if islevler:
        cy += 4
        icerik.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#9ab" stroke-width="0.7"/>'
                      % (x, cy - 8, x + KUTU_GENISLIK, cy - 8))
        for islev in islevler:
            icerik.append('<text x="%d" y="%d" class="islev">%s</text>' % (x + 10, cy + 4, islev))
            cy += SATIR_YUKSEKLIK

    return "\n".join(icerik), yukseklik


def ok(x1, y1, x2, y2, etiket="", kesik=False, etiket_x=None, etiket_y=None):
    stil = 'stroke="#7a1f1f" stroke-width="1.3" fill="none"'
    if kesik:
        stil += ' stroke-dasharray="6,4"'
    parca = ['<path d="M %d %d L %d %d" %s marker-end="url(#ok)"/>' % (x1, y1, x2, y2, stil)]
    if etiket:
        ex = etiket_x if etiket_x is not None else (x1 + x2) / 2
        ey = etiket_y if etiket_y is not None else (y1 + y2) / 2 - 6
        parca.append('<text x="%d" y="%d" class="etiket">%s</text>' % (ex, ey, etiket))
    return "\n".join(parca)


def uret():
    parcalar = []

    # 1) Hasta (kayit defteri)
    k, h = kutu(390, 40, "Hasta  (bagli liste dugumu)",
                ["+ tc : int", "+ ad : char[64]", "+ yas : int",
                 "+ poliklinik : char[48]", "+ durum : int", "+ sonraki : Hasta*"],
                ["+ kayit_ekle(...) : Hasta*", "+ kayit_sil(...) : Hasta*",
                 "+ kayit_ara(bas, tc) : Hasta*", "+ kayit_listele(bas)",
                 "+ kayit_say(bas) : int", "+ kayit_serbest(bas)"])
    parcalar.append(k)

    # 2) Kuyruk
    k, h2 = kutu(40, 330, "Kuyruk",
                 ["+ on : Bekleyen*", "+ arka : Bekleyen*", "+ adet : int"],
                 ["+ kuyruk_baslat(k)", "+ kuyruk_ekle(k, tc, ad) : int",
                  "+ kuyruk_iceriyor(k, tc) : int", "+ kuyruk_sil(k, tc) : int",
                  "+ kuyruk_cikar(k) : int", "+ kuyruk_listele(k)",
                  "+ kuyruk_serbest(k)"])
    parcalar.append(k)

    # 3) Bekleyen
    k, h3 = kutu(390, 330, "Bekleyen  (kuyruk dugumu)",
                 ["+ tc : int", "+ ad : char[64]", "+ sonraki : Bekleyen*"], [])
    parcalar.append(k)

    # 4) AgacDugum
    k, h4 = kutu(730, 330, "AgacDugum",
                 ["+ hasta : Hasta*", "+ sol : AgacDugum*", "+ sag : AgacDugum*"],
                 ["+ agac_ekle(...) : AgacDugum*", "+ agac_ara(kok, tc)",
                  "+ agac_sil(kok, tc)", "+ agac_sirali(kok)",
                  "+ agac_ciz(kok)", "+ agac_yukseklik(kok) : int",
                  "+ agac_dugum_say(kok) : int", "+ agac_serbest(kok)"])
    parcalar.append(k)

    # 5) Islem (yigit)
    k, h5 = kutu(40, 560, "Islem  (yigit dugumu)",
                 ["+ tur : IslemTuru", "+ yedek : Hasta", "+ sonraki : Islem*"],
                 ["+ yigit_ekle(...) : Islem*", "+ yigit_al(tepe) : Islem*",
                  "+ yigit_bos(tepe) : int", "+ yigit_serbest(tepe)"])
    parcalar.append(k)

    # 6) Poliklinik (dairesel)
    k, h6 = kutu(730, 560, "Poliklinik  (dairesel dugum)",
                 ["+ kod : int", "+ ad : char[40]", "+ sonraki : Poliklinik*"],
                 ["+ poliklinik_ekle(...)", "+ poliklinik_ilerle(son)",
                  "+ poliklinik_listele(son)", "+ poliklinik_say(son) : int",
                  "+ poliklinik_serbest(son)"])
    parcalar.append(k)

    # 7) dosya.c ve main.c akis islevleri
    k, h7 = kutu(390, 555, "dosya.c ve main.c  (akis islevleri)", [],
                 ["+ dosya_oku(...) : int", "+ dosya_yaz(...) : int",
                  "+ hasta_ekle_akis(...)", "+ hasta_sil_akis(...)",
                  "+ benchmark(...)"])
    parcalar.append(k)

    # Iliskiler
    parcalar.append(ok(320, 375, 386, 375, "1..*  bekleyen", etiket_x=300, etiket_y=368))
    parcalar.append(ok(520, 330, 520, 262, "tc ile basvuru", kesik=True, etiket_x=524, etiket_y=298))
    parcalar.append(ok(820, 330, 720, 250, "1 hasta (isaretci)", etiket_x=740, etiket_y=300))
    parcalar.append(ok(40, 600, 18, 600, ""))
    parcalar.append('<path d="M 40 600 L 18 600 L 18 60 L 386 60" stroke="#7a1f1f" '
                    'stroke-width="1.3" stroke-dasharray="6,4" fill="none" marker-end="url(#ok)"/>')
    parcalar.append('<text x="24" y="330" class="etiket" transform="rotate(-90 24 330)">'
                    'yedek : Hasta (kopya)</text>')

    # Poliklinik kendine donen ok
    parcalar.append('<path d="M 1060 600 C 1120 600 1120 660 1060 660" stroke="#7a1f1f" '
                    'stroke-width="1.3" fill="none" marker-end="url(#ok)"/>')
    parcalar.append('<text x="1075" y="640" class="etiket">sonraki</text>')

    # Aciklama kutusu
    aciklama = """
    <rect x="40" y="40" width="310" height="240" fill="#f7f9fb" stroke="#9ab" stroke-width="0.8"/>
    <text x="54" y="64" class="kbaslik2">Okuma anahtari</text>
    <text x="54" y="88" class="kucuk">C dilinde erisim belirleyici olmadigi icin</text>
    <text x="54" y="106" class="kucuk">butun alan ve islevler + (public) isaretlidir.</text>
    <text x="54" y="132" class="kbaslik2">Iliski turleri</text>
    <text x="54" y="154" class="kucuk">duz ok  : isaretci ile baglanti</text>
    <text x="54" y="172" class="kucuk">kesik ok: anahtar (tc) ile basvuru</text>
    <text x="54" y="198" class="kbaslik2">Kullanilan yapilar</text>
    <text x="54" y="220" class="kucuk">bagli liste, kuyruk, ikili arama agaci,</text>
    <text x="54" y="238" class="kucuk">yigit, dairesel bagli liste</text>
    <text x="54" y="262" class="kucuk">BLG203 - Cengiz Kilic 251205027</text>
    """
    parcalar.append(aciklama)

    svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1140 780"
     width="272mm" height="168mm" style="display:block">
  <defs>
    <marker id="ok" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
      <path d="M 0 0 L 10 4 L 0 8 z" fill="#7a1f1f"/>
    </marker>
  </defs>
  <style>
    .kbaslik { font: bold 13px "Segoe UI", Arial; fill: #ffffff; }
    .kbaslik2 { font: bold 11px "Segoe UI", Arial; fill: #1f4e79; }
    .alan { font: 11px Consolas, monospace; fill: #16324a; }
    .islev { font: 10.5px Consolas, monospace; fill: #4a3b1f; }
    .etiket { font: 10px "Segoe UI", Arial; fill: #7a1f1f; }
    .kucuk { font: 9.6px "Segoe UI", Arial; fill: #333; }
  </style>
  %s
</svg>
""" % "\n".join(parcalar)

    html = """<!doctype html><html><head><meta charset="utf-8">
<style>
  @page { size: A4 landscape; margin: 6mm; }
  body { margin: 0; font-family: "Segoe UI", Arial; }
  h1 { font-size: 13pt; color: #16365c; margin: 0 0 1mm 0; }
  .alt { font-size: 9pt; color: #444; margin-bottom: 1.5mm; }
</style></head><body>
<h1>Hastane Hasta Sıra ve Bekleme Sistemi - UML Yapı Diyagramı</h1>
<div class="alt">BLG203 Veri Yapıları Dönem Projesi, Cengiz Kılıç 251205027. Yapılar, alanlar,
işlevler ve ilişkiler C gerçeklemesiyle birebir uyumludur.</div>
%s
</body></html>""" % svg

    gecici_html = os.path.join(KOK, "00_Kapak", "uml.html")
    with open(gecici_html, "w", encoding="utf-8") as dosya:
        dosya.write(html)

    subprocess.run([
        CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--user-data-dir=" + os.path.join(tempfile.gettempdir(), "chrome_pdf_profil"),
        "--no-pdf-header-footer", "--print-to-pdf=" + HEDEF,
        "file:///" + gecici_html.replace("\\", "/"),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("uml yazildi:", HEDEF)


if __name__ == "__main__":
    uret()
