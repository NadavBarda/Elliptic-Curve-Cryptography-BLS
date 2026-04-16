from ellipticUtils import find_largest_prime_factor
from ellipticCurves import EllipticCurveElement
from ellipticCurves import EllipticCurve
from Fp import Fp



def hash_message_to_int(message: str) -> int:
    encoding = "cp1255"
    bytes_msg = message.encode(encoding)
    n = len(bytes_msg)
    tot = 0
    for i, byte_val in enumerate(bytes_msg):
        yn = 256 ** (n-1-i)
        tot += byte_val * yn
    return tot

def generate_num_from_message(message:str, p:int):
    tot = hash_message_to_int(message)
    return Fp(tot % p, p)


def is_live_in_eliptic(x:Fp, eliptic: EllipticCurve):
    p = x.p
    z = x**3 + eliptic.a*x + eliptic.b

    # z = y^2 so z must to have y that exist in Fp
    # z = 0 is not good beacue y= 0 not live in the Efp*
    if z**((p-1)//2) == Fp(1, p): 
        return z
    return None


def generate_point_with_details(message: str, elliptic: EllipticCurve) -> dict:
    p = elliptic.p
    # Integer manipulation for unreduced message digest
    tot = hash_message_to_int(message)
        
    x_pre = tot
    x_post = tot % p
    
    curr_x = Fp(x_post, p)
    z = is_live_in_eliptic(curr_x, elliptic)
    while not z:
        curr_x += 1
        z = is_live_in_eliptic(curr_x, elliptic)
        
    y_val = z**((p+1)//4)
    P_temp = EllipticCurveElement(curr_x, y_val, elliptic)
    
    order = elliptic.calc_order()
    r = find_largest_prime_factor(elliptic)
    cofactor = order // r
    P_base = P_temp * cofactor
    
    return {
        "x_pre": x_pre,
        "x_mod_p": x_post,
        "x_final": curr_x.val,
        "P_temp": P_temp,
        "r": r,
        "cofactor": cofactor,
        "H_m": P_base
    }

def generate_point(message: str, elliptic: EllipticCurve):
    details = generate_point_with_details(message, elliptic)
    return details["H_m"]
