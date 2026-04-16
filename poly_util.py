import random
from ellipticUtils import find_largest_prime_factor
from ellipticCurves import EllipticCurve
from fpUtil import get_prime_factors
from Fp import Fp
from poly import Poly

def gcd_poly(a: Poly, b: Poly):
    if a.degree == -1 or (a.degree == 0 and len(a.coeffs) > 0 and a.coeffs[0].val == 0):
        return b
    return gcd_poly(b % a, a)

def extended_gcd_poly(a: Poly, b: Poly):
    """
    Computes the extended Greatest Common Divisor of two polynomials a and b.
    Returns (gcd, x, y) such that a*x + b*y = gcd.
    """
    if a.degree == -1 or (a.degree == 0 and len(a.coeffs) > 0 and a.coeffs[0].val == 0):
        p = b.p if b.p is not None else a.p
        return b, Poly([Fp(0, p)], p), Poly([Fp(1, p)], p)
    
    gcd, x1, y1 = extended_gcd_poly(b % a, a)
    
    x = y1 - (b // a) * x1
    y = x1
    
    return gcd, x, y

def is_irreducible(poly: Poly):
    """
    Checks if a polynomial is irreducible over Fp using Rabin's Test.
    Degree of poly is k.
    """
    p = poly.coeffs[0].p
    k = poly.degree
    
    # 1. Check if poly divides x^(p^k) - x
    # This ensures all irreducible factors have degrees that divide k.
    x = Poly([Fp(0, p), Fp(1, p)])
    if pow(x, p**k, poly) != x:
        return False

    # 2. Check that gcd(poly, x^(p^(k/qi)) - x) == 1 for all prime factors qi of k.
    # This ensures no factors have a degree smaller than k.
    prime_factors = get_prime_factors(k)
    for q in prime_factors:
        exponent = p**(k // q)
        # Calculate (x^(p^(k/q)) mod poly)
        x_p_kq = pow(x, exponent, poly)
        
        # Calculate GCD(poly, x^(p^(k/q)) - x)
        check_poly = x_p_kq - x
        common_factor = gcd_poly(check_poly, poly)
        
        # If the GCD is not a constant (degree > 0), poly is reducible
        if common_factor.degree > 0:
            return False

    return True

def find_k(r:int, p:int):
    k = 2
    while (p**k - 1) % r != 0:
        k += 1
    return k

def generate_random_poly(k: int, p: int):
    # Generates a random monic polynomial of degree k over Fp
    coeffs = [Fp(random.randint(0, p-1), p) for _ in range(k)]
    coeffs.append(Fp(1, p))
    return Poly(coeffs, p)

def find_irreducible_poly(eleptic_curve : EllipticCurve):
    r = find_largest_prime_factor(eleptic_curve)
    k = find_k(r, eleptic_curve.p)

    while True:
        poly = generate_random_poly(k, eleptic_curve.p)
        if is_irreducible(poly):
            return poly
