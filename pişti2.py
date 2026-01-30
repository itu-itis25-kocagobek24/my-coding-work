"♠️♥️♣️♦️"
from colorama import Fore,Back,Style
import random
import time


def valueToKey(dict,value):
    """aynı value birden fazla olabilir bu ilk value nun keyini atar"""
    for keys in dict.keys():
        if dict[keys] == value:
            return keys
def aynımı(dict_):
    """sözlüğün bütün valueları aynımı diye bakar ama stringe çevirir """
    return len(set(str(value) for value in dict_.values())) == 1

    
def kartları_yap():
    kartlar={}
    for i in range(2,11) :
    
        kart1 = Back.WHITE + Fore.BLACK + f"{i}♣️ " + Style.RESET_ALL
        kart2 = Back.WHITE + Fore.RED + f"{i}♥️ " + Style.RESET_ALL
        kart3 = Back.WHITE + Fore.RED + f"{i}♦️ " + Style.RESET_ALL
        kart4 = Back.WHITE + Fore.BLACK + f"{i}♠️ " + Style.RESET_ALL
        kartlar[kart1] = i
        kartlar[kart2] = i
        kartlar[kart3] = i
        kartlar[kart4] = i
    for i in ["A","J","K","Q"]:
        
        kart1 = Back.WHITE + Fore.BLACK + i + "♣️ " + Style.RESET_ALL
        kart2 = Back.WHITE + Fore.RED + i + "♥️ " + Style.RESET_ALL
        kart3 = Back.WHITE + Fore.RED + i + "♦️ " + Style.RESET_ALL 
        kart4 = Back.WHITE + Fore.BLACK + i + "♠️ " + Style.RESET_ALL
        kartlar[kart1] = i
        kartlar[kart2] = i
        kartlar[kart3] = i
        kartlar[kart4] = i

    kartlar_real = {}
    for kart,values in kartlar.items():
        kartlar_real[kart] = values

    return kartlar,kartlar_real



def oyun_oyna(kartlar,kartlar_real):

    playerPC_memory = []
    orta_kartlar = []
    tur = 0
    PC_cards = []
    ME_cards = []
    playerPC = {}
    playerME = {}
    PC_puan = 0
    ME_puan = 0

    def kart_göster(kartlar_):
        if kartlar_ == orta_kartlar:
            print("orta kartlar: ",end="")
            if len(orta_kartlar) > 0:
                for kart in kartlar_:
                    if kart == orta_kartlar[-1]:
                        time.sleep(0.5)
                        print(kart,end=" ")
                        continue
                    print(kart,end=" ")
        elif kartlar_ == playerME:
            print("senin kartların: ",end="")
            for kart in kartlar_.keys():
                print(kart,end=" ")

    
    def puan_hesapla(liste):
        puan = 0
        liste1 = []
        for i in liste:
            if i == "PP":
                puan += 25
                liste1.append("PP")
            elif i == "P":
                puan += 10
                liste1.append("P")
            elif kartlar_real[i] == "J" or kartlar_real[i] == "A":
                liste1.append(i)
                puan += 1
            elif "2" in i and "♣️" in i:
                liste1.append(i)
                puan  += 2
            elif "10" in i and "♦️" in i:
                liste1.append(i)
                puan += 3
        liste = [k for k in liste if k != "P" and k != "PP"]
        liste1.append(f"{len(liste)} kart")
        if len(liste) > 26:
            puan += 3
        liste = []
        return puan,liste,liste1


    def kart_dağıt():
        oyuncu = {}
        kart4 = random.sample(list(kartlar.keys()),4)
        
        for i in kart4:
            oyuncu[i] = kartlar[i]
            del kartlar[i]
        return oyuncu
    
    
    
    
    
    def kart_atma_PC():

        kartlarvaluelist = list(playerPC.values())
        atılacak_kart = "bos"

        if len(playerPC.keys()) == 1:
            atılacak_kart = list(playerPC.keys())[0]
        
        elif len(orta_kartlar) == 0:
            rastgele_atılacaklar = []
            sayac = 0
            for kartvalue in kartlarvaluelist:
                if not kartvalue == "J":
                    rastgele_atılacaklar.append(kartvalue)
                    if playerPC_memory.count(kartvalue) > sayac:
                        sayac = playerPC_memory.count(kartvalue)
                        atılacak_kart = valueToKey(playerPC,kartvalue)

            if sayac == 0:
                value_ = random.choice(rastgele_atılacaklar)
                atılacak_kart = valueToKey(playerPC,value_)
            
  
        elif kartlar_real[orta_kartlar[-1]] in kartlarvaluelist:
            atılacak_kart = valueToKey(playerPC,kartlar_real[orta_kartlar[-1]])
            
        #Joker nasıl atılır !!!!!!!!!!!!!!!!!!!!!!!!!!!!
        elif "J" in playerPC.values():
            if len(orta_kartlar) >= 8:
                atılacak_kart = valueToKey(playerPC,"J")
            elif len(playerPC.keys()) >= 3:
                for kartvalue in kartlarvaluelist:
                    if kartvalue == "J":
                        continue
                    çıkansayısı = playerPC_memory.count(kartvalue)
                    eldekisayısı = kartlarvaluelist.count(kartvalue)
                    if tur < 4 and  çıkansayısı < 2 and eldekisayısı == 1 and len(orta_kartlar) > 3:
                        atılacak_kart = valueToKey(playerPC,"J")
                        break
                    if tur > 3 and çıkansayısı < 3 and not çıkansayısı + eldekisayısı == 4:
                        atılacak_kart = valueToKey(playerPC,"J")
                        break
        
        
        if atılacak_kart == "bos":
            playerPC_memory_ = playerPC_memory.copy()
            playerPC_memory_ += kartlarvaluelist
            rastgele_atılacaklar = []
            sayac = 0
            for kartvalue in kartlarvaluelist:
                rastgele_atılacaklar.append(kartvalue)
                if kartvalue == "J":
                    continue
                çıkansayısı = playerPC_memory_.count(kartvalue)
                eldekisayısı = kartlarvaluelist.count(kartvalue)
                if çıkansayısı + eldekisayısı == 4:
                    atılacak_kart = valueToKey(playerPC,kartvalue)
                    break
                if çıkansayısı > sayac:
                    atılacak_kart = valueToKey(playerPC,kartvalue)
                    sayac = çıkansayısı
            if atılacak_kart == "bos":
                value = random.choice(rastgele_atılacaklar)
                atılacak_kart = valueToKey(playerPC,value)
              

        playerPC_memory.append(kartlar_real[atılacak_kart])
        del playerPC[atılacak_kart]
        time.sleep(0.5)
        print("\r\033[K",end="")
        return atılacak_kart

            
        

    
    
    def kart_atma_ME():
        """kartı oyuncu atacak"""
        print()
        kart_göster(playerME)
        print()
        atılacak_kart_no = input("kaçıncı kartı atacaksınız: ")
        try:
            atılacak_kart_no = int(atılacak_kart_no)
            if not 0 < atılacak_kart_no <= len(list(playerME.keys())):
                print("lütfen geçerli bir rakam girin")
                time.sleep(2)
                print("\033[F\033[K",end="")
                print("\033[F\033[K",end="")
                print("\033[F\033[K",end="")
                print("\033[F\033[999C",end="")
                return kart_atma_ME()
        except ValueError as e:
            print("lütfen bir rakam giriniz")
            time.sleep(2)
            print("\033[F\033[K",end="")
            print("\033[F\033[K",end="")
            print("\033[F\033[K",end="")
            print("\033[F\033[999C",end="")
            return kart_atma_ME()

        print("\033[F\033[K",end="") 
        print("\033[F\033[K",end="")    
        atılacak_kart = list(playerME.keys())[atılacak_kart_no - 1]
        del playerME[atılacak_kart]
        playerPC_memory.append(atılacak_kart)
        time.sleep(0.5)
        print("\033[F\033[K",end="")
        return atılacak_kart
    
    def kart_alma(atılan_kart,player_cards,orta_kartlar):
        orta_kartlar.append(atılan_kart)
        kart_göster(orta_kartlar) 
        if len(orta_kartlar) == 1:
            return orta_kartlar
        elif kartlar_real[atılan_kart] == kartlar_real[orta_kartlar[-2]]:
            if len(orta_kartlar) == 2:
                player_cards += orta_kartlar
                if kartlar_real[orta_kartlar[-2]] == "J":
                    orta_kartlar = []
                    player_cards.append("PP")
                    print(" helal len !!! jokere bastın",end="")
                else:
                    orta_kartlar = []
                    player_cards.append("P")
                    print(" pişti!!! 🎖️",end="")
            else:
                player_cards += orta_kartlar
                orta_kartlar = []

        elif kartlar_real[atılan_kart] == "J":
            player_cards += orta_kartlar
            orta_kartlar = []
        time.sleep(0.5)
        if orta_kartlar == []:
            print("\r\033[K",end="")
            kart_göster(orta_kartlar)
        return orta_kartlar

            
        
              


                    
        
    print()
    print()
    print()
    print()
    print()
      
        
    oyuncular = ["playerPC","playerME"]
    first_player = random.choice(oyuncular)
    if first_player == "playerPC":
        print("ilk oyuncu PC")
    else:
        print("ilk oyuncu sensin ")
    oyuncular.remove(first_player)
    while True:
        seviye_ = input('yeni oyuna başlamak için "START" yaz: ')

        if seviye_.upper() == "START":
            print("3")
            time.sleep(1)
            print("\033[F\033[K",end="")
            print("2")
            time.sleep(1)
            print("\033[F\033[K",end="")
            print("1")
            time.sleep(1)
            print("\033[F\033[K",end="")
            print("yeni oyun başladı! iyi oyunlar😊")
        else:
            time.sleep(0.5)
            print("\033[F\033[K",end="")
            print("\033[F\033[K",end="")
            print("\033[F\033[K",end="")
            print("\033[F\033[K",end="")
            print("\033[F\033[K",end="")
            print("\033[F\033[K",end="")
            print("\033[F\033[K",end="")
            break
        
        time.sleep(1)
        for sil in range(8):
            print("\033[F\033[K",end="")
        



        orta_kartlar = random.sample(list(kartlar.keys()),4)
        print("orta kartlar: ",end="")
        for i in orta_kartlar:
            time.sleep(0.3)
            del kartlar[i]
            print(i,end=" ")
        time.sleep(0.4)

        

        
        for i in range(6):
            playerPC = kart_dağıt()
            playerME = kart_dağıt()
            if aynımı(playerME) or aynımı(playerPC):
                print("bilgisayarın kartları: ",end="")
                for kart in playerPC.keys():
                    print(kart,end=" ")
                print("\nsenin kartlar: ",end="")
                for kart in playerME.keys():
                    print(kart,end=" ")
                print("\nBU EL İPTAL !!!")
                time.sleep(3)
                PC_cards = []
                ME_cards = []
                orta_kartlar = []
                playerPC_memory.append("iptal")
                break


            if first_player == "playerPC":
                for x in range(4):
                    atılan_kart = kart_atma_PC()
                    orta_kartlar = kart_alma(atılan_kart,PC_cards,orta_kartlar)
                    atılan_kart = kart_atma_ME()
                    orta_kartlar = kart_alma(atılan_kart,ME_cards,orta_kartlar)
            if first_player == "playerME":
                for x in range(4):
                    atılan_kart = kart_atma_ME()
                    if i == 0 and x == 0:
                        print("\r\033[K",end=" ")
                    orta_kartlar = kart_alma(atılan_kart,ME_cards,orta_kartlar)
                    atılan_kart = kart_atma_PC()
                    orta_kartlar = kart_alma(atılan_kart,PC_cards,orta_kartlar)
        if len(orta_kartlar) > 0:
            if len(orta_kartlar) % 2 == 1:
                if first_player == "playerME":
                    ME_cards += orta_kartlar
                else:
                    PC_cards += orta_kartlar
            else:
                if first_player == "playerME":
                    PC_cards += orta_kartlar
                else:
                    ME_cards += orta_kartlar
        print("\r\033[K",end="")

                 
        pc_puan,PC_cards,pc_cards = puan_hesapla(PC_cards)
        me_puan,ME_cards,me_cards = puan_hesapla(ME_cards)
        print("senin puan kartların: ",end=" ")
        for i in me_cards:
            print(i,end="  ")
        print() 
        print("bilgisayarın puan kartları: ",end=" ")
        for i in pc_cards:
            print(i,end=" ") 
        print()
        if "iptal" in playerPC_memory:
            for sil in range(5):
                print("\033[F\033[K",end="")
            print()
            print()
        
        print(f"bigisayarın bu elde aldığı puan: {pc_puan}")
        print(f"senin bu elde aldığın puan: {me_puan}")
        PC_puan += pc_puan
        ME_puan += me_puan
        print(f"totalde   bilgisayar: {PC_puan}  sen: {ME_puan}")
        time.sleep(1.5)
        
        player_ = first_player
        first_player = oyuncular[0]
        oyuncular.append(player_)
        oyuncular.remove(first_player)
        playerPC_memory = []
        kartlar = {}
        for kart_,value_ in kartlar_real.items():
            kartlar[kart_] = value_

        

     

kartlar,kartlar_real = kartları_yap()
oyun_oyna(kartlar,kartlar_real)









 


        
