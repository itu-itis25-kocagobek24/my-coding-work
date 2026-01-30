import requests
from bs4 import BeautifulSoup as BS
import time
import random

#global değerler
my_banks = []
bank_names = []
buy_prices = []
sell_prices = []
makaslar = []
my_url = "https://altin.doviz.com/gumus"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0",
    "Accept-Language":"tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer":"https://www.google.com/",
    "Connection":"keep-alive"
}
rf = lambda:random.randint(1,5) #request frequency

def my_gumus_gostergem():
    global my_banks
    global bank_names 
    global buy_prices
    global sell_prices
    global makaslar
    global my_url
    bank_names = []
    buy_prices = []
    sell_prices = []
    makaslar = []
    my_request = requests.get(my_url,headers=headers)
    my_html = BS(my_request.text,'html.parser')
    my_class = my_html.find_all("table")
    my_body = my_class[1].find_all("tbody")
    for i in my_body:
        satırlar = i.find_all("tr")
        for satır in satırlar:
            bölmeler = satır.find_all("td")
            my_bank = []
            for bölme in bölmeler:
                if not bölme == bölmeler[0]:
                    my_bank.append(bölme.string)

                else:
                    src = bölme.find("a").find("img")["src"]
                    src_ = src.split("/")[-1]
                    bank_name = src_.split(".")[0]
                    my_bank.append(bank_name)
            my_banks.append(my_bank)
    bank_names = [banks[0] for banks in my_banks]
    buy_prices = [float(banks[1].replace(".","").replace(",",".")) for banks in my_banks]
    sell_prices = [float(banks[2].replace(".","").replace(",",".")) for banks in my_banks]
    makaslar = [float(banks[3].replace(",",".")) for banks in my_banks] 
    my_banks = []
    return bank_names 
bank_names = my_gumus_gostergem()

def bankanın_verisi(banka):
    global bank_names
    if not banka in bank_names:
        raise KeyError("this bank name is not found")
    global my_url
    my_url_ = f"https://altin.doviz.com/{banka}/gumus"
    my_request = requests.get(my_url,headers=headers)
    my_html = BS(my_request.text,'html.parser')
    my_list = my_html.find("a",href=my_url_).parent.parent.find_all("td")[1:4]
    my_data = [float(i.string.replace(".","").replace(",",".")) for i in my_list[:2]]
    my_data.append(float(my_list[2].string.replace(",",".")))
    return my_data
    

def banka_isimlerini_göster():
    for names in bank_names:
        print(names)
    input_ = input()
    for _ in range(len(bank_names) + 1):
        print("\033[F\033[K",end="")


    

def gumus_alış_takip(): 
    bank_name = input("bankanın adını giriniz: ")
    takip_günü = float(input("kaç gün takip edilsin: "))
    takip_second = takip_günü*24*60*60
    takip_değişimi = float(input("kaç liralık değişimde haber almak istersin: "))
    buy_price = bankanın_verisi(bank_name)[0]
    start_time = time.ctime()
    start_second = time.time()
    while True:
        time.sleep(rf())
        buy_price_ = bankanın_verisi(bank_name)[0]
        fark_ = buy_price_ - buy_price
        fark = abs(fark_)
        if fark >= takip_değişimi:
            finish_time = time.ctime()
            print("{} liradan {} liraya {}".format(buy_price,buy_price_,"YÜKSELDİ" if fark_ > 0 else "DÜŞTÜ"))
            print(f"{fark:.2f} lira {"YÜKSELDİ" if fark_ > 0 else "DÜŞTÜ"}")
            print("{} tarihinden {} tarihine kadar sürdü".format(start_time,finish_time))
            break
        if takip_second <= time.time() - start_second:
            print(f"güncel durum: {buy_price_}")
            print("{:.2f} lira {}".format(fark,"YÜKSELDİ" if fark_ > 0 else "DÜŞTÜ"))
            print(f"{takip_günü} günlük süre doldu")
            break
    input("rastgele tıkla")
    print("\033[F\033[K"*7,end="")


def gumus_satış_takip():
    bank_name = input("bankanın adını giriniz: ")
    takip_günü = float(input("kaç gün takip edilsin: "))
    takip_second = takip_günü*24*60*60
    takip_değişimi = float(input("kaç liralık değişimde haber almak istersin: "))
    sell_price = bankanın_verisi(bank_name)[1]
    start_time = time.ctime()
    start_second = time.time()
    while True:
        time.sleep(rf())
        sell_price_= bankanın_verisi(bank_name)[1]
        fark_ = sell_price_- sell_price
        fark = abs(fark_)
        if fark >= takip_değişimi:
            finish_time = time.ctime()
            print("{} liradan {} liraya {}".format(sell_price,sell_price_,"YÜKSELDİ" if fark_ > 0 else "DÜŞTÜ"))
            print(f"{fark:.2f} değişim oldu")
            print("{} tarihinden {} tarihine kadar sürdü".format(start_time,finish_time))
            break
        if takip_second <= time.time() - start_second:
            print(f"güncel durum: {sell_price_}")
            print("{:.2f} lira {}".format(fark,"YÜKSELDİ" if fark_ > 0 else "DÜŞTÜ"))
            print(f"{takip_günü} günlük süre doldu")
            break
    input("rastgele tıkla")
    print("\033[F\033[K"*7,end="")


        
        
        

def spesifisk_info():
    my_gumus_gostergem()
    en_az_satış = min(sell_prices)
    en_ucuz_satan = bank_names[sell_prices.index(en_az_satış)]
    print(f"en ucuz satan: {en_ucuz_satan} bankası : {en_az_satış} lira")
    en_çok_alış = max(buy_prices)
    en_pahalı_satan = bank_names[buy_prices.index(en_çok_alış)]
    print(f"en pahalı alan: {en_pahalı_satan} : {en_çok_alış} lira")
    en_büyük_makas = max(makaslar)
    en_küçük_makas = min(makaslar)
    BMbank = bank_names[makaslar.index(en_büyük_makas)]
    KMbank = bank_names[makaslar.index(en_küçük_makas)]
    print(f"en büyük makas {BMbank.upper()} da : {en_büyük_makas}")
    print(f"en küçük makas {KMbank.upper()} da : {en_küçük_makas}")  
    sil = input()
    print("\033[F\033[K"*5,end="")






if __name__ == "__main__":
    while True:
        print("özel bilgiler için 'info' yaz")
        print("sistemdeki bankaların isimlerini görmek için 'bankalar' yaz")
        print("alışı takip etmek için 'Atakip' yaz")
        print("satışı takip etmek için 'Stakip' yaz")
        process = input("yaz :: ")
        print("\033[F\033[K" * 6,end="")
        if process == "info": spesifisk_info()
        elif process == "bankalar": banka_isimlerini_göster()
        elif process == "Atakip":gumus_alış_takip()
        elif process == "Stakip":gumus_satış_takip()
        else: print("işlem hatalı"),time.sleep(0.5)
        

