import random
import time
import sys
"""Bu bir hafıza kartı oyunudur. Burada 16 tane kart var hepside 1 den 16 ya kadar numaralı. iki tane kart numarası girerek onların 
aynı olup olmadığına bakacaksın. eğer aynı ise ekranda oyun bitesiye kadar görülür,değilse 2 saniye görülür ve sonra kaybolur.
her bir kartın arkasında bir harf vardır.iyi oyunlar  """

global degerler,degerler1,degerler2

degerler = [[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]]
degerler1 = [[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]]
sayılar = [["01","02","03","04"],["05","06","07","08"],["09","10","11","12"],["13","14","15","16"]]
def tablo_yap():
    
        for küme in sayılar:
            for s in küme:
                print(s,end=" ")
            print()
            for küme2 in degerler[sayılar.index(küme)]:
                print(küme2,end=" ")
            print()
        
def tablo_sil():
    for i in range(9):
        sys.stdout.write('\033[F')  # Bir satır yukarı
        sys.stdout.write('\033[K')  # Satırı temizle 

def iki_satır_sil():
    for i in range(2):
        sys.stdout.write('\033[F')  # Bir satır yukarı
        sys.stdout.write('\033[K')  # Satırı temizle 
    
def harf_ata():
    harfler = [" A"," B"," C"," D"," E"," F"," G"," H"," A"," B"," C"," D"," E"," F"," G"," H"]
    for küme in degerler1:
        for elemanlar in küme:
            harf = random.choice(harfler)
            elemanlar.append(harf)
            harfler.remove(harf)
    return degerler1


def oyna():
    tablo_yap()
    harf_ata()
    bulunan_kart = 0
    grililmiş_sayılar = []
    while bulunan_kart != 16:
        girdi = input("seçtiğiniz iki kartın numarasını giriniz(arada bir boşluk bırak): ")
        
        try:
            if not " " in girdi:
                raise IndexError
            listegirdi = girdi.split(" ")
            for i in listegirdi:
                if not 1 <= int(i) <= 16:
                    raise Exception
                if len(i) == 1:
                    i = "0" + i
                if i in grililmiş_sayılar:
                   raise InterruptedError
            if len(listegirdi) != 2:
                raise IndexError
            if int(listegirdi[0]) == int(listegirdi[1]):
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            print("aynı sayıyı iki kere giremezsiniz")
            time.sleep(2)
            iki_satır_sil()
            continue
        except InterruptedError:
            print("çiftini daha önceden bulduğunuz bir kart numarasını tekrar giremezsiniz")
            time.sleep(2)
            iki_satır_sil()
            continue
        except IndexError:
            print("lütfen kart numaralarını istenilen şekilde giriniz")
            time.sleep(2)
            iki_satır_sil()
            continue
        except Exception:
            print("böyle bir kart yok lütfen tekrar deneyin")
            time.sleep(2)
            iki_satır_sil()
            continue
        girdiler_ = girdi.split(" ")
        girdiler = []
        for girdi_ in girdiler_:
            if len(girdi_) == 1:
                girdi_ = "0"+girdi_
                girdiler.append(girdi_)
            else:
                girdiler.append(girdi_)

        if degerler1[(int(girdiler[0])-1)//4][(int(girdiler[0])-1)%4] == degerler1[(int(girdiler[1])-1)//4][(int(girdiler[1])-1)%4]:
            degerler[(int(girdiler[0])-1)//4][(int(girdiler[0])-1)%4] = degerler1[(int(girdiler[0])-1)//4][(int(girdiler[0])-1)%4][0]
            degerler[(int(girdiler[1])-1)//4][(int(girdiler[1])-1)%4] = degerler1[(int(girdiler[1])-1)//4][(int(girdiler[1])-1)%4][0]
            tablo_sil()
            tablo_yap()
            bulunan_kart += 2
            grililmiş_sayılar.append(girdiler[0])
            grililmiş_sayılar.append(girdiler[1])
        else:
            degerler[(int(girdiler[0])-1)//4][(int(girdiler[0])-1)%4] = degerler1[(int(girdiler[0])-1)//4][(int(girdiler[0])-1)%4][0]
            degerler[(int(girdiler[1])-1)//4][(int(girdiler[1])-1)%4] = degerler1[(int(girdiler[1])-1)//4][(int(girdiler[1])-1)%4][0]
            tablo_sil()
            tablo_yap()
            print("seçtiğiniz iki kartın numarasını giriniz(arada bir boşluk bırak): ")
            time.sleep(2)
            tablo_sil()
            degerler[(int(girdiler[0])-1)//4][(int(girdiler[0])-1)%4] = []
            degerler[(int(girdiler[1])-1)//4][(int(girdiler[1])-1)%4] = []
            tablo_yap()
            
            
    print("Tebrikler oyunu bitirdiniz!!")
    
    


print("Bu bir hafıza kartı oyunudur. Burada 16 tane kart var hepside 1 den 16 ya kadar numaralı. iki tane kart numarası girerek onların") 
print("aynı olup olmadığına bakacaksın. eğer aynı ise ekranda oyun bitesiye kadar görülür,değilse 2 saniye görülür ve sonra kaybolur.")
print("her bir kartın arkasında bir harf vardır.iyi oyunlar")  

while True:
    start = input("oyuna başlamak için 'm' ye sonra enter tuşuna tıklayın: ")
    if start == "m":
        print("oyun başlıyor....",end="\r")
        time.sleep(2)
        print("3                ",end="\r")
        time.sleep(1)
        print("2                ",end="\r")
        time.sleep(1)
        print("1                ",end="\r")
        time.sleep(1)
        print("Başladı          ")
        
        start_time = time.time()
        oyna()
        finish_time = time.time()
        print(f'"{round(finish_time - start_time)}" saniyede bitirdiniz')
        degerler = [[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]]
        degerler1 = [[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]]
        
        
