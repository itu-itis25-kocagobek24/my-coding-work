x = input("enter the integer: ")
liste1 = []
for i in x:
    if not i in "1234567890":
        raise ValueError("this is not an integer")
s = int(x)
if s =< 1:
    print("you should enter an approvable number")
else:       
    for a in range(2,s):
        if s % a == 0:
            print(f"{x} bir asal sayı değildir") 
            liste1.append(s)
            break
    if liste1 == []:

        print(f"{x} bir asal sayıdır")       
