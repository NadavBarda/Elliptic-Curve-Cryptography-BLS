from __future__ import annotations
from Fp import Fp
from ast import List
from typing import List



class Poly:
    def __init__(self, A: List[Fp], p=None):
        # 1. Strip leading zeros (highest degree coefficients)
        # We stop before the last element to ensure '0' is represented as [0]
        while len(A) > 1 and A[-1].val == 0:
            A.pop()
            
        self.coeffs = A
        self.degree = len(A) - 1
        self.p = p if p is not None else (A[0].p if A else None)
    

    def __repr__(self):
        # A nice way to see the polynomial: a_n*x^n + ... + a_0
        terms = []
        superscripts = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', 
                        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'}
        
        def to_sup(n):
            return "".join(superscripts.get(char, char) for char in str(n))

        for i, c in enumerate(self.coeffs):
            if c.val == 0 and len(self.coeffs) > 1:
                continue
                
            if i == 0:
                terms.append(f"{c.val}")
            elif i == 1:
                if c.val == 1:
                    terms.append("x")
                else:
                    terms.append(f"{c.val}x")
            else:
                if c.val == 1:
                    terms.append(f"x{to_sup(i)}")
                else:
                    terms.append(f"{c.val}x{to_sup(i)}")
                    
        if not terms:
            return "0"
            
        return " + ".join(reversed(terms))
    
    def __add__(self, other: Poly):
        max_len = max(len(self.coeffs), len(other.coeffs))
        new_coeffs = []
        for i in range(max_len):
            v1 = self.coeffs[i] if i < len(self.coeffs) else Fp(0, self.p)
            v2 = other.coeffs[i] if i < len(other.coeffs) else Fp(0, other.p)
            new_coeffs.append(v1 + v2)
        return Poly(new_coeffs, self.p)
    
    def __sub__(self, other: Poly):
        max_len = max(len(self.coeffs), len(other.coeffs))
        new_coeffs = []
        for i in range(max_len):
            v1 = self.coeffs[i] if i < len(self.coeffs) else Fp(0, self.p)
            v2 = other.coeffs[i] if i < len(other.coeffs) else Fp(0, other.p)
            new_coeffs.append(v1 - v2)
        return Poly(new_coeffs, self.p)

    def __eq__(self, other):
        if isinstance(other, Poly):
            return self.p == other.p and self.coeffs == other.coeffs
        elif isinstance(other, int):
            if self.degree > 0:
                return False
            return self.coeffs[0].val == (other % self.p)
        return False

    def __mul__(self, other: Poly):

        assert isinstance(other, Poly) and self.p == other.p

        res_len = len(self.coeffs) + len(other.coeffs) - 1
        new_coeffs = [Fp(0, self.p) for _ in range(res_len)]
        
        for i, a1 in enumerate(self.coeffs):
            for j, a2 in enumerate(other.coeffs):
                new_coeffs[i + j] += (a1 * a2)
        return Poly(new_coeffs, self.p)
    
    def __divmod__(self, other: Poly):
        # 1. Basic checks
        if other.degree == -1 or (other.degree == 0 and other.coeffs[0].val == 0): # The zero polynomial
            raise ZeroDivisionError("division by zero polynomial")
        
        p = self.p
        # Copy coefficients to work on them
        remainder_coeffs = [c for c in self.coeffs]
        quotient_coeffs = [Fp(0, p)] * max(0, self.degree - other.degree + 1)

        # 2. Long Division Algorithm
        # While the remainder's degree is >= the divisor's degree
        while len(remainder_coeffs) >= len(other.coeffs):
            if len(remainder_coeffs) == 1 and remainder_coeffs[0].val == 0:
                break
                
            # Calculate the leading term of the quotient
            lead_r = remainder_coeffs[-1]
            lead_d = other.coeffs[-1]
            
            # Using your Fp.__truediv__ here
            factor = lead_r / lead_d
            
            # Find the position/degree shift
            degree_diff = len(remainder_coeffs) - len(other.coeffs)
            quotient_coeffs[degree_diff] = factor
            
            # Subtract (factor * x^diff * other) from remainder
            for i in range(len(other.coeffs)):
                remainder_coeffs[i + degree_diff] -= factor * other.coeffs[i]
            
            # Remove the high-degree zero term we just eliminated
            while len(remainder_coeffs) > 1 and remainder_coeffs[-1].val == 0:
                remainder_coeffs.pop()

        # If remainder is empty, it's the zero polynomial
        if not remainder_coeffs:
            remainder_coeffs = [Fp(0, p)]

        return Poly(quotient_coeffs, p), Poly(remainder_coeffs, p)

    def __mod__(self, other: Poly):
        _, remainder = divmod(self, other)
        return remainder

    def __floordiv__(self, other: Poly):
        quotient, _ = divmod(self, other)
        return quotient
    
    def __pow__(self, exp: int, mod: Poly = None):
        res = Poly([Fp(1, self.p)], self.p)
        base = self
        while exp > 0:
            if exp % 2 == 1:
                res = (res * base)
                if mod is not None:
                    res = res % mod
            base = (base * base)
            if mod is not None:
                base = base % mod
            exp //= 2
        return res


