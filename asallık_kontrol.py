x = input("enter the integer: ")
liste1 = []
for i in x:
    if not i in "1234567890":
        print("this is not an integer! please, enter an integer")
        x = 0
        break
if x == 0:
    print("try again")
else:       
    s = int(x)
    
    for a in range(2,s):
        if s % a == 0:
            print(f"{x} bir asal sayı değildir") 
            liste1.append(s)
            break
    if liste1 == []:
        print(f"{x} bir asal sayıdır")       