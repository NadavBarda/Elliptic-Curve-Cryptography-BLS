from ellipticCurves import EllipticCurve
from ellipticCurvesFpk import EllipticCurveFpk
from ellipticUtils import find_largest_prime_factor
from poly_util import find_k, find_irreducible_poly
from findQ import find_Q, default_q_filter
from hash import generate_point_with_details
from miller import reduced_tate_pairing
from fpUtil import is_prime

def run_bls_workflow(p: int, a: int, b: int, priv_key: int, message: str) -> dict:
    print(f"[BLS Workflow] Starting verification for prime p={p}")
    if not is_prime(p):
        print(f"[BLS Workflow] Error: {p} is not a prime number.")
        return {"error": f"{p} is not a prime number."}
        
    try:
        print("[BLS Workflow] Initializing Base Elliptic Curve...")
        curve = EllipticCurve(a, b, p)
    except AssertionError as e:
        print(f"[BLS Workflow] Error: Curve initialization failed - {str(e)}")
        return {"error": f"Curve error: {str(e)}"}
        
    try:
        print("[BLS Workflow] Calculating base Curve Order (WARNING: May be extremely slow for large p)...")
        order = curve.calc_order()
        print(f"[BLS Workflow] Base Curve Order calculated: {order}")
        
        print("[BLS Workflow] Finding largest prime factor 'r' of the curve order...")
        r = find_largest_prime_factor(curve)
        print(f"[BLS Workflow] Largest prime factor r={r}")
        
        print("[BLS Workflow] Calculating mapping embedding degree 'k'...")
        k = find_k(r, p)
        print(f"[BLS Workflow] Found k={k}")
        if k is None or k > 20: 
            print("[BLS Workflow] Error: embedding degree k is too large.")
            return {"error": f"Requires embedding degree k={k} which is too large for this interactive demo."}
            
        print("[BLS Workflow] Deriving Irreducible Polynomial for field extension...")
        p_poly = find_irreducible_poly(curve)
        print(f"[BLS Workflow] Found irreducible polynomial: {p_poly}")
        
        print("[BLS Workflow] Initializing Extension Field Elliptic Curve (EllipticCurveFpk)...")
        curve_fpk = EllipticCurveFpk(a, b, p_poly)
            
        print(f"[BLS Workflow] Finding point Q on Fpk with subgroup order {r}...")
        Q_fpk = find_Q(curve_fpk, r, default_q_filter)
        print("[BLS Workflow] Successfully found point Q.")
        
        print("[BLS Workflow] Hashing message to base curve point (H_m)...")
        hash_details = generate_point_with_details(message, curve)
        P_base = hash_details["H_m"]
        print(f"[BLS Workflow] Point H_m derived.")
        
        print("[BLS Workflow] Generating Signature (S) and Public Key (Pk)...")
        S = P_base * priv_key
        Pk = Q_fpk * priv_key
        
        print("[BLS Workflow] Computing reduced Tate pairing 1 (e_r(S, Q))...")
        pair1 = reduced_tate_pairing(S, Q_fpk, r)
        
        print("[BLS Workflow] Computing reduced Tate pairing 2 (e_r(H_m, Pk))...")
        pair2 = reduced_tate_pairing(P_base, Pk, r)
        print("[BLS Workflow] Pairings evaluated. Verification complete!")
        
        return {
            "success": True,
            "pair1": str(pair1.val),
            "pair2": str(pair2.val),
            "match": (pair1 == pair2),
            "intermediates": {
                "order_Fp": order,
                "order_Fpk": curve_fpk.calc_order(),
                "r": r,
                "k": k,
                "cofactor": hash_details["cofactor"],
                "x_pre": str(hash_details["x_pre"])[:50] + "..." if len(str(hash_details["x_pre"])) > 50 else str(hash_details["x_pre"]),
                "x_post": hash_details["x_final"],
                "P_temp": f"({hash_details['P_temp'].x.val}, {hash_details['P_temp'].y.val})",
                "H_m": f"({P_base.x.val}, {P_base.y.val})",
                "sigma": f"({S.x.val}, {S.y.val})",
                "f_x": str(p_poly),
                "Q": f"(\n   X: {Q_fpk.x.val},\n   Y: {Q_fpk.y.val}\n)"
            }
        }
    except Exception as e:
        import traceback
        return {"error": f"Calculation logic failed: {str(e)}\n\nTrace: {traceback.format_exc()}"}
