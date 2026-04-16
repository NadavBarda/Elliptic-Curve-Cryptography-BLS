from __future__ import annotations
from Fp import Fp
from Fpk import Fpk
from poly import Poly
import ellipticCurves

from ellipticUtils import isValidPoint

class EllipticCurveFpk:
    def __init__(self, a, b, p_poly: Poly):
        """
        a and b can be int, Fp, or Fpk. They will be normalized to Fpk.
        p_poly is the irreducible polynomial defining the extension field F_{p^k}
        """
        p = p_poly.p
        
        # Helper to slowly transition a and b as Fpk basis objects
        def to_fpk(val):
            if isinstance(val, Fpk):
                return val
            elif isinstance(val, Fp):
                return Fpk(Poly([val], p), p_poly)
            else:
                return Fpk(Poly([Fp(val, p)], p), p_poly)
                
        self.a = to_fpk(a)
        self.b = to_fpk(b)
        self.p_poly = p_poly
        self.p = p
        self.order = None
        
        # Smoothness over Fpk: 4a^3 + 27b^2 != 0
        disc = 4 * (self.a ** 3) + 27 * (self.b ** 2)
        assert disc != 0, "Curve must be Smooth"

    def calc_order(self):
        if self.order:
            return self.order
            
       
        # Compute original parameters for N_1 setup
        a_int = self.a.val.coeffs[0].val if len(self.a.val.coeffs) > 0 else 0
        b_int = self.b.val.coeffs[0].val if len(self.b.val.coeffs) > 0 else 0
        
        base_curve = ellipticCurves.EllipticCurve(a_int, b_int, self.p)
        N1 = base_curve.calc_order()
        t = self.p + 1 - N1
        
        k = self.p_poly.degree
        V_prev2 = 2
        V_prev1 = t
        if k == 1:
            Vk = V_prev1
        else:
            for _ in range(2, k + 1):
                Vk = t * V_prev1 - self.p * V_prev2
                V_prev2 = V_prev1
                V_prev1 = Vk
                
        self.order = (self.p ** k) + 1 - Vk
        return self.order

    def __eq__(self, other):
        if not isinstance(other, EllipticCurveFpk):
            return False
        return (self.a == other.a and 
                self.b == other.b and 
                self.p_poly == other.p_poly)

    def __repr__(self):
        return f"EllipticCurveFpk(y^2 = x^3 + ({self.a.val})x + ({self.b.val}))"

class EllipticCurveElementFpk:
    def __init__(self, x:Fpk, y:Fpk, elliptic: EllipticCurveFpk):
        if x is not None and not isinstance(x, Fpk):
            raise TypeError("x must be Fpk or None")
        if y is not None and not isinstance(y, Fpk):
            raise TypeError("y must be Fpk or None")
            
        assert isValidPoint(x, y, elliptic), "Point does not live on the Fpk elliptic curve"

        self.x = x
        self.y = y
        self.elliptic = elliptic
        self.order = None

    def inverse(self):
        if self.x is None:
            return EllipticCurveElementFpk(None, None, self.elliptic)
            
        return EllipticCurveElementFpk(self.x, self.y * -1, self.elliptic)

    def __add__(self, other):
        from ellipticUtils import calc_point_add
        return calc_point_add(self, other)

    def __sub__(self, other):
        if not isinstance(other, EllipticCurveElementFpk):
            raise TypeError("Can only subtract EllipticCurveElementFpk")
        return self + other.inverse()

    def __rmul__(self, k: int):
        return self.__mul__(k)
    
    def __mul__(self, k: int):
        from ellipticUtils import calc_point_mul
        return calc_point_mul(self, k)

    def __eq__(self, other):
        if not isinstance(other, EllipticCurveElementFpk):
            return False

        return (self.x == other.x and 
                self.y == other.y and 
                self.elliptic == other.elliptic)
