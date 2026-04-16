from functools import lru_cache
from typing import Optional

from Fp import Fp
from Fpk import Fpk
from poly import Poly
from ellipticCurves import EllipticCurveElement
from ellipticCurvesFpk import EllipticCurveElementFpk

def line_eval(T: EllipticCurveElement, P_eval: EllipticCurveElement, Q: EllipticCurveElementFpk, p_poly: Poly) -> Fpk:
    """
    Evaluates the generic line tracking function l_{T, P_eval}(Q) / v_{T+P_eval}(Q).
    
    :param T: The current running sum point in E(Fp).
    :param P_eval: The point to add in E(Fp).
    :param Q: The target evaluation point mathematically in E(Fpk).
    :param p_poly: The field defining irreducible polynomial.
    """
    p = p_poly.p
    
    # Check for Vertical Line directly
    if T.x == P_eval.x and T.y == (P_eval.y * Fp(-1, p)):
        # Computes Q.x - T.x
        return Q.x - T.x
        
    from ellipticUtils import calc_point_slope
    gamma = calc_point_slope(T, P_eval)
        
    x3 = gamma**2 - T.x - P_eval.x
    
    # Num: Q.y - T.y - gamma * (Q.x - T.x)
    L = Q.y - T.y - gamma * (Q.x - T.x)
    # Den: Q.x - x3
    V = Q.x - x3
    
    return L / V

def miller_loop(P: EllipticCurveElement, Q: EllipticCurveElementFpk, r: int) -> Fpk:
    """
    Executes the Miller Loop algorithm generically evaluating f_{r, P}(Q).
    Mathematically constructs the scalar mapped line accumulation.
    
    :param P: Base curve cyclic mapped point E(Fp).
    :param Q: Extended field pairing point mapped into E(Fpk).
    :param r: The prime order boundary for Weil / Tate combinations.
    :return: An Fpk element reflecting the accumulated polynomial map.
    """
    p_poly = Q.elliptic.p_poly
    p = p_poly.p
    
    # Binary representation of r, skipping the '0b' prefix and the leading 1 bit
    r_bin = bin(r)[3:]
    
    T = P
    f = Fpk(Poly([Fp(1, p)], p), p_poly)
    
    for bit in r_bin:
        # Double Step
        f = (f**2) * line_eval(T, T, Q, p_poly)
        T = T + T
        
        # Add Step
        if bit == '1':
            f = f * line_eval(T, P, Q, p_poly)
            T = T + P
            
    return f

def reduced_tate_pairing(P: EllipticCurveElement, Q: EllipticCurveElementFpk, r: int) -> Fpk:
    """
    Computes the reduced Tate pairing e_r(P, Q) = f_{r, P}(Q)^((p^k - 1) / r).
    """
    f = miller_loop(P, Q, r)
    p_poly = Q.elliptic.p_poly
    p = p_poly.p
    k = p_poly.degree
    
    # Calculate exponent: (p^k - 1) // r
    exponent = (p**k - 1) // r
    
    return f ** exponent
