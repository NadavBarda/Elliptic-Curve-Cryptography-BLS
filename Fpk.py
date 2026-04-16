from poly_util import extended_gcd_poly
from poly import Poly
from Fp import Fp

class Fpk:

    def __init__(self,poly:Poly,p:Poly):
        self.val = poly % p
        self.p = p

    def _promote(self, other):
        if isinstance(other, Fpk):
            return other
        if isinstance(other, int):
            return Fpk(Poly([Fp(other, self.p.p)], self.p.p), self.p)
        if isinstance(other, Fp):
            return Fpk(Poly([other], self.p.p), self.p)
        return NotImplemented

    def __add__(self,other):
        other = self._promote(other)
        if other is NotImplemented: return NotImplemented
        assert self.p == other.p
        return Fpk(self.val + other.val, self.p)
    
    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        other = self._promote(other)
        if other is NotImplemented: return NotImplemented
        assert self.p == other.p
        return Fpk(self.val - other.val, self.p)

    def __rsub__(self, other):
        other = self._promote(other)
        if other is NotImplemented: return NotImplemented
        assert self.p == other.p
        return Fpk(other.val - self.val, self.p)
    
    def __mul__(self,other):
        other = self._promote(other)
        if other is NotImplemented: return NotImplemented
        assert self.p == other.p
        return Fpk(self.val * other.val,self.p)

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self,other):
        other = self._promote(other)
        if other is NotImplemented: return NotImplemented
        assert self.p == other.p

        gcd, inv, _ = extended_gcd_poly(other.val, self.p)
        inv = inv // gcd
        
        return self * Fpk(inv, self.p)

    def __rtruediv__(self, other):
        other = self._promote(other)
        if other is NotImplemented: return NotImplemented
        return other.__truediv__(self)
    
    def __pow__(self,k:int):
        return Fpk(pow(self.val, k, self.p), self.p)
    
    def __eq__(self, other):
        other = self._promote(other)
        if other is NotImplemented:
            return False
        return self.val == other.val and self.p == other.p

