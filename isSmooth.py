
from Fp import Fp
def isSmooth(a: Fp,b:Fp):
    return 4 * a ** 3 + 27 * b ** 2 != 0




if __name__ == '__main__' :   
    p = 103
    A = Fp(1,p)
    B = Fp(0,p)
    res = isSmooth(A,B)
    print(res)