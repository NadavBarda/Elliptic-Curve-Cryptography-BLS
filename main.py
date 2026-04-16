from ellipticCurves import EllipticCurve
from ellipticCurvesFpk import EllipticCurveFpk
from ellipticUtils import find_largest_prime_factor
from poly_util import find_k, find_irreducible_poly
from findQ import find_Q, default_q_filter
from hash import generate_point
from miller import miller_loop, reduced_tate_pairing

def main():
    print("Testing find_Q across Field Extents...")
    
    p = 103
    a = 1
    b = 0
    curve = EllipticCurve(a, b, p)
    
    curve.calc_order()
    r = find_largest_prime_factor(curve)
    
    # Extension Field (F_{p^k}) setup
    k = find_k(r, p)
    print(f"\n[Extension Field (F_{p}^{k})] Deriving Irreducible Poly for r={r} k={k}...")
    # we know k=13 requires k=2 for p=103. Let's find irred_poly
    p_poly = find_irreducible_poly(curve)
    
    print(f"Irreducible Poly: {p_poly}")
    curve_fpk = EllipticCurveFpk(a, b, p_poly)
    
    order_fpk = curve_fpk.calc_order()
    print(f"Curve order in Fpk is: {order_fpk}")
    
    print(f"Looking for Extended Point Q with order {r}...")
    Q_fpk = find_Q(curve_fpk, r, default_q_filter)
    
    print("Found Extended Q:")
    print(f"  X: {Q_fpk.x.val}")
    print(f"  Y: {Q_fpk.y.val}")
    
    # Verify order
    test_identity = Q_fpk * r
    assert test_identity.x is None, f"Q * {r} is not O"
    assert Q_fpk.x is not None, "Q shouldn't be O"
    
    print("\n[Miller Loop] Evaluating pairing traces over pairing-friendly configuration...")
    
    
    P_base = generate_point("Hello Miller", curve)
    print(f"Generated hashed point P: ({P_base.x}, {P_base.y})")
    
    f_res = miller_loop(P_base, Q_fpk, r)
    print(f"Miller Loop Evaluated Result: {f_res.val}")
    
    print("\n[BLS Verification] Testing bilinear property of the reduced Tate pairing...")
    private_key = 42
    print(f"Using private key (x) = {private_key}")
    
    # S = x * H(m)  (Signature generation)
    S = P_base * private_key
    
    # Pk = x * Q  (Public Key generation)
    Pk = Q_fpk * private_key
    
    # Verification: e_r(S, Q) == e_r(H(m), Pk)
    # Computes e_r(x*H(m), Q)
    pair1 = reduced_tate_pairing(S, Q_fpk, r)
    print(f"e_r(x*H(m), Q) = {pair1.val}")
    
    # Computes e_r(H(m), x*Q)
    pair2 = reduced_tate_pairing(P_base, Pk, r)
    print(f"e_r(H(m), x*Q) = {pair2.val}")
    
    is_valid = (pair1 == pair2)
    print(f"\nSignatures match? {is_valid}")
    assert is_valid, "BLS verification failed: pairings do not match!"

    print("\nAll verifications passed! Output Q Fpk is perfectly correct and mappings paired efficiently.")

if __name__ == '__main__':
    main()
