import os

os.chdir("desktop")
dosyalar=[]

for dosya in os.listdir("lineer"):
    if os.path.isfile(dosya) == True:
        dosyalar.append(dosya)
print(dosyalar)        

