import os

x = input("İlgili klasörün yol adresini yapıştırın: ").strip().rstrip("\\")

def dosya_bul(x):
    dosyalar = []

    for dosya in os.listdir(x):
        if os.path.isfile(os.path.join(x, dosya)):
            dosyalar.append(dosya)

    for dosya in dosyalar:
        if "." not in dosya:
            uzanti = "diger"
        else:
            uzanti = dosya.split(".")[-1].lower()

        hedef_klasor = os.path.join(x, uzanti)

        if not os.path.exists(hedef_klasor):
            os.mkdir(hedef_klasor)

        os.rename(
            os.path.join(x, dosya),
            os.path.join(hedef_klasor, dosya)
        )

dosya_bul(x)
