from Fp import Fp
from fpUtil import get_prime_factors

def isSmooth(a: Fp, b: Fp):
    return 4 * a ** 3 + 27 * b ** 2 != 0

def isValidPoint(x, y, elliptic):
    if x is None and y is None: return True

    rightSide = x ** 3 + elliptic.a * x + elliptic.b
    leftSide = y ** 2
    return leftSide == rightSide

def find_largest_prime_factor(eliptic):
    order = eliptic.calc_order()
    factors = get_prime_factors(order)

    return factors[-1]

def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)

    # if ls == -1 (p-1) so there is no y such that y^2 = a so we remove the already added 1
    # if ls == 0 that mean the only y is 0
    #  if ls == 1 that mean there exist 2 point

    if ls == p - 1:
        return -1
    return ls

def get_curve_order(curve):
    p = curve.p
    a = curve.a.val
    b = curve.b.val
    
    # N = p + 1 + sum(Legendre(x^3 + ax + b, p))
    total_sum = 0
    for x in range(p):
        rhs = (x**3 + a*x + b) % p
        total_sum += legendre_symbol(rhs, p)
        
    return p + 1 + total_sum

def get_biggest_factor(curve):
    return find_largest_prime_factor(curve)

def calc_point_slope(p1, p2):
    if p1 == p2:
        return (3 * (p1.x**2) + p1.elliptic.a) / (2 * p1.y)
    else:
        return (p2.y - p1.y) / (p2.x - p1.x)

def calc_point_add(p1, p2):
    assert p1.elliptic == p2.elliptic, "Curves must match"
    
    if p1.x is None: 
        return p2
    if p2.x is None: 
        return p1

    if p1.x == p2.x and p1.y == (p2.y * -1):
        return p1.__class__(None, None, p1.elliptic)

    gama = calc_point_slope(p1, p2)
    
    new_x = gama**2 - p1.x - p2.x
    new_y = gama * (p1.x - new_x) - p1.y

    return p1.__class__(new_x, new_y, p1.elliptic)

def calc_point_mul(point, k: int):
    if k == 0:
        return point.__class__(None, None, point.elliptic)
    if k < 0:
        return point.inverse() * abs(k)

    result = point.__class__(None, None, point.elliptic)
    addend = point

    while k > 0:
        if k & 1:
            result = result + addend
        addend = addend + addend
        k >>= 1

    return result
