from itertools import permutations as pe
from math import perm 

def getMatris():
    matris = []
    matris_ = input("matrisi gir (örnek: 1 3 4,9 7 6,1 3 5): ")
    rows = matris_.split(",")
    for row in rows:
        row = row.strip()
        row = row.split(" ")
        matris.append(row)
    return matris

def is_even_permutation(p):
    inv = 0
    n = len(p)
    for i in range(n):
        for j in range(i+1, n):
            if p[i] > p[j]:
                inv += 1
    return inv % 2 == 0

    


def determinant(matris):
    rowcount = len(matris)
    for rows in matris:
        if not len(rows) == rowcount:
            print("this is not a square matrix, it is not invertible")
            return False
    columncount = rowcount
    determinant = 0
    for columns in pe(range(columncount)):
        determinant_ = 1
        row = 0
        for j in columns:
            determinant_ *= int(matris[row][j])
            row += 1
            j += 1
        if is_even_permutation(columns):
            determinant += determinant_
        else:
            determinant -= determinant_
    return determinant

matris = getMatris()
print("\ndeterminant: ",determinant(matris))

def get_cofaktor(matris):
    cofaktor = [row[ : ] for row in matris] 
    rowcount = len(matris)
    columncount = rowcount
    for i in range(rowcount):
        for j in range(columncount):
            matris_ = [row[ : ] for row in matris]
            for rows in matris_:
                rows.remove(rows[j])
            matris_.remove(matris_[i])
            determinant_ = determinant(matris_)
            if (i + j) % 2 == 1:
                determinant_ *= -1
            cofaktor[i][j] = determinant_
    return cofaktor
 
def inverter(matris):
    determinant_ = determinant(matris)
    if determinant_ == 0:
        print("the determinant is zero, it cannot be invertible")
        return False
    cofaktor = get_cofaktor(matris)
    invert = [row[ : ] for row in matris]
    rowcount = len(matris)
    columncount = rowcount
    for i in range(rowcount):
        for j in range(columncount):
            invert[i][j] = cofaktor[j][i] / determinant_
    return invert


invert = inverter(matris)
if bool(invert) == True:
    print("\ninverse matris :\n")
    for i in invert:
        print(i)
    print()
        





    
    