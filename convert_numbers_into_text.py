number = input("bir sayı giriniz: ")

try:
    int(number)
except ValueError:
    raise ValueError("lütfen sayı giriniz!!")

if number == "0":
    print("sıfır")
else:
    if number.startswith("0"):
        number = str(int(number))   
    isim = ""
    birler = {"1":"bir","2":"iki","3":"üç","4":"dört","5":"beş","6":"altı","7":"yedi","8":"sekiz","9":"dokuz"}
    onlar = {"1":"on","2":"yirmi","3":"otuz","4":"kırk","5":"elli","6":"altmış","7":"yetmiş","8":"seksen","9":"doksan"}
    büyükler = {"2":"bin","5":"milyon","8":"milyar","11":"tirilyon"}
    number_reverse = number[::-1]
    length = len(number)
    for i in range(length):
        the_number = number_reverse[i]
        i_str = str(i)
        if the_number != "0":
            if i%3 == 0:
                isim = " " + birler[the_number] + isim
                
            elif i%3 == 1:
                isim = " " + onlar[the_number] + isim

            else:
                isim = " yüz" + isim
                if the_number != "1":
                    isim = " " + birler[the_number] + isim
                if i + 1 != length and not number_reverse[i+1:i+4] == "000":
                    isim = " " + büyükler[i_str] + isim
        else:
            if i_str in büyükler and not number_reverse[i+1:i+4] == "000":
                isim = " " + büyükler[i_str] + isim

    if length == 4 and number.startswith("1"):
        isim = isim[4:]
    
    print(isim)


            
