from fpUtil import get_prime_factors
from fpUtil import is_prime
from Fp import Fp

from ellipticUtils import isSmooth, isValidPoint, get_curve_order

class EllipticCurve :
    
    def __init__(self,a,b,p:int):
        fa = Fp(a,p)
        fb = Fp(b,p)
        
        assert isSmooth(fa,fb) and is_prime(p), "must be Smooth"

        self.a = fa
        self.b = fb
        self.p = p
        self.order = None
    
    def calc_order(self):

        if self.order :
            return self.order
        
        self.order = get_curve_order(self)
        return self.order
        

    def __eq__(self, other):
        
        if not isinstance(other, EllipticCurve):
            return False
        
        # Two curves are equal if a, b, and p are the same
        return (self.a == other.a and 
                self.b == other.b and 
                self.p == other.p)

    def __repr__(self):
        return f"EllipticCurve(y^2 = x^3 + {self.a}x + {self.b} mod {self.p})"


class EllipticCurveElement :
    
    def __init__(self,x,y,elliptic):
        assert isValidPoint(x,y,elliptic), "dont live on the elliptic"

        self.x = x
        self.y = y
        self.elliptic = elliptic
        self.order = None
    
    def calc_order(self):
        if self.order :
            return self.order

        id = EllipticCurveElement(None,None,self.elliptic)
        

        group_order = self.elliptic.calc_order()
        factors = get_prime_factors(group_order)

        order = group_order

        # p-1 = q1^k1 * q2^k2...
        # o(a) = q1^k2' * q2^k2' ...

        # so if  a^(p-1 / factor) == 1
        # it mean that o(a) is at most p-1/facotr 


        for factor in factors :
            while self * (order// factor) == id :
                order //= factor
        
        self.order = order
        return self.order

              
    def inverse(self):
        if self.x == None :
            return EllipticCurveElement(None,None,self.elliptic)

        return EllipticCurveElement(self.x,-self.y,self.elliptic)
    
    def __add__(self, other):
        from ellipticUtils import calc_point_add
        return calc_point_add(self, other)

    def __rmul__(self, k: int):
        return self.__mul__(k)
    
    def __mul__(self, k: int):
        from ellipticUtils import calc_point_mul
        return calc_point_mul(self, k)



    def __eq__(self, other):
        
        if not isinstance(other, EllipticCurveElement):
            return False

        return (self.x == other.x and 
                self.y == other.y and 
                self.elliptic == other.elliptic)
        
