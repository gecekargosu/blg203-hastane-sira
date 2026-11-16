"""
Test verisi ureteci.
Hastane kayit defteri icin 1200 kayitlik CSV dosyasi olusturur.
Yonerge en az 1000 kayit istedigi icin bu sayi secildi.
Bicim: tc;ad;yas;poliklinik;durum
Kullanim: python veri_uret.py
"""
import random

ADLAR = [
    "Ayse Yilmaz", "Mehmet Demir", "Fatma Kaya", "Ali Celik", "Zeynep Sahin",
    "Hasan Yildiz", "Emine Aydin", "Mustafa Ozturk", "Hatice Arslan", "Ibrahim Dogan",
    "Elif Kilic", "Murat Aslan", "Merve Koc", "Yusuf Kurt", "Sevgi Ozdemir",
    "Ahmet Tas", "Sultan Erdem", "Burak Aksoy", "Nurcan Polat", "Kerem Bozkurt",
    "Gul Yalcin", "Serkan Korkmaz", "Derya Unal", "Osman Gunes", "Pinar Tekin",
    "Ercan Yavuz", "Selma Kaya", "Tolga Bulut", "Melis Sarac", "Hakan Uysal",
]

POLIKLINIKLER = [
    "Dahiliye", "Kardiyoloji", "Ortopedi", "Cocuk Sagligi", "Goz Hastaliklari",
    "Kulak Burun Bogaz", "Dermatoloji", "Noroloji", "Gogus Hastaliklari", "Uroloji",
]

ortam = random.Random(31)
satirlar = ["tc;ad;yas;poliklinik;durum"]
for i in range(1200):
    tc = 30001 + i
    ad = ADLAR[(i * 11) % len(ADLAR)]
    yas = 1 + ortam.randint(0, 88)
    poliklinik = POLIKLINIKLER[(i * 5) % len(POLIKLINIKLER)]
    durum = 1 if ortam.random() < 0.08 else 0
    satirlar.append("%d;%s;%d;%s;%d" % (tc, ad, yas, poliklinik, durum))

with open("hastalar.csv", "w", encoding="utf-8") as dosya:
    dosya.write("\n".join(satirlar) + "\n")

print("hastalar.csv yazildi, kayit sayisi:", len(satirlar) - 1)
