from fpUtil import inverse


class Fp:
    def __init__(self, value: int, p: int):
        self.p = p
        self.val = value % p

    def __add__(self, other):
        if not isinstance(other, (int, Fp)): return NotImplemented
        other_val = other.val if isinstance(other, Fp) else other
        return Fp(self.val + other_val, self.p)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if not isinstance(other, (int, Fp)): return NotImplemented
        other_val = other.val if isinstance(other, Fp) else other
        return Fp(self.val - other_val, self.p)

    def __rsub__(self, other):
        if not isinstance(other, (int, Fp)): return NotImplemented
        other_val = other.val if isinstance(other, Fp) else other
        return Fp(other_val - self.val, self.p)

    def __mul__(self, other):
        if not isinstance(other, (int, Fp)): return NotImplemented
        other_val = other.val if isinstance(other, Fp) else other
        return Fp(self.val * other_val, self.p)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not isinstance(other, (int, Fp)): return NotImplemented
        # Division by zero check
        other_val = other.val if isinstance(other, Fp) else other
        if other_val == 0:
            raise ZeroDivisionError("Modular division by zero")
        inv = inverse(other_val, self.p)
        return self.__mul__(inv)

    def __pow__(self, exp: int):
        if exp == 0:
            return Fp(1, self.p)
        if exp < 0:
            inv = inverse(self.val, self.p)
            return Fp(inv, self.p) ** abs(exp)

        half = self ** (exp // 2)
        res = half * half

        if exp % 2:
            res = res * self
        
        return res

    def __eq__(self, other):
        if isinstance(other, int):
            return self.val == (other % self.p)
        return isinstance(other, Fp) and self.val == other.val and self.p == other.p

    def __repr__(self):
        return str(self.val)