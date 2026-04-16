import random
from typing import Callable, Any, Optional, List

from Fp import Fp
from Fpk import Fpk
from poly import Poly
from ellipticCurvesFpk import EllipticCurveElementFpk, EllipticCurveFpk


def ts_square_root_fpk(n: Fpk, p: int, p_poly: Poly) -> Optional[Fpk]:
    """
    Computes the square root of n in the extension field F_{p^k} using the
    Tonelli-Shanks algorithm. 
    
    Returns None if n is not a quadratic residue.
    """
    k: int = p_poly.degree
    q: int = p ** k
    
    zero: Fpk = Fpk(Poly([Fp(0, p)], p), p_poly)
    one: Fpk = Fpk(Poly([Fp(1, p)], p), p_poly)
    
    if n == zero:
        return zero
        
    if n ** ((q - 1) // 2) != one:
        return None
        
    if q % 4 == 3:
        return n ** ((q + 1) // 4)
        
    Q: int = q - 1
    S: int = 0
    while Q % 2 == 0:
        Q //= 2
        S += 1
        
    z: Fpk = one
    while True:
        z_coeffs: List[Fp] = [Fp(random.randint(0, p - 1), p) for _ in range(k)]
        z = Fpk(Poly(z_coeffs, p), p_poly)
        if z != zero and z ** ((q - 1) // 2) != one:
            break
            
    M: int = S
    c: Fpk = z ** Q
    t: Fpk = n ** Q
    R: Fpk = n ** ((Q + 1) // 2)
    
    while True:
        if t == one:
            return R
        elif t == zero:
            return zero
            
        t2i: Fpk = t
        i: int = 0
        for i in range(1, M):
            t2i = t2i * t2i
            if t2i == one:
                break
                
        b: Fpk = c ** (1 << (M - i - 1))
        M = i
        c = b * b
        t = t * c
        R = R * b


def get_random_point(curve: EllipticCurveFpk) -> EllipticCurveElementFpk:
    """
    Generates a random point explicitly on a given EllipticCurveFpk securely natively.
    """
    p: int = curve.p
    k: int = curve.p_poly.degree
    
    while True:
        x_coeffs: List[Fp] = [Fp(random.randint(0, p - 1), p) for _ in range(k)]
        x_val: Fpk = Fpk(Poly(x_coeffs, p), curve.p_poly)
        
        # Evaluate y^2 = x^3 + ax + b
        rhs: Fpk = x_val**3 + curve.a * x_val + curve.b
        
        y_val: Optional[Fpk] = ts_square_root_fpk(rhs, p, curve.p_poly)
        if y_val is not None:
            if random.choice([True, False]):
                minus_one: Fpk = Fpk(Poly([Fp(-1, p)], p), curve.p_poly)
                y_val = y_val * minus_one
            return EllipticCurveElementFpk(x_val, y_val, curve)


def find_Q(curve: EllipticCurveFpk, r: int, f: Callable[[EllipticCurveElementFpk], Any]) -> EllipticCurveElementFpk:
    """
    Finds a point Q of exact expected order r such that S is not the point at infinity (O),
    and is neither a zero nor a pole of the evaluation function natively natively.
    
    :param curve: The extended field EllipticCurveFpk wrapper curve instance.
    :param r: The target point integer order dimension mapping.
    :param f: Any rational evaluation function callable natively.
    """
    order: int = curve.calc_order()
    
    if order % r != 0:
        raise ValueError(f"r ({r}) must divide the curve order ({order})")
        
    coprime_factor: int = order
    while coprime_factor % r == 0:
        coprime_factor //= r
        
    while True:
        P: EllipticCurveElementFpk = get_random_point(curve)
        
        S: EllipticCurveElementFpk = P * coprime_factor
        
        if S.x is None:
            continue
        
        while True:
            S_next: EllipticCurveElementFpk = S * r
            if S_next.x is None:
                break
            S = S_next
        
        xq = S.x ** curve.p 
        yq = S.y ** curve.p

        pi = EllipticCurveElementFpk(xq, yq, curve)
        Q = pi - S

        if Q.x is None:
            continue
            
        try:
            val: Any = f(Q)
            # Account for native explicit Python mappings vs Object wrappers explicitly natively
            if val == 0 or getattr(val, 'val', None) == 0 or getattr(val, 'degree', None) == -1:
                continue
        except ZeroDivisionError:
            continue
        except Exception:
            continue
            
        return Q

def default_q_filter(Q):
    if Q.x is None: 
        raise ZeroDivisionError("Pole")
    # arbitrary logic, skip elements where x == 1
    if Q.x.val.degree == 0 and Q.x.val.coeffs[0].val == 1:
        return 0
    return 1