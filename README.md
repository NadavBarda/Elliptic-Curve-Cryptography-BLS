<div align="center">
  <h1>🛡️ Pure Python Elliptic Curve Cryptography & BLS Signatures</h1>
  <p>
    An educational, dependency-free Python implementation of Elliptic Curves over Finite Fields ($F_p$) and Extension Fields ($F_{p^k}$), featuring Miller's algorithm, the Reduced Tate Pairing, and a complete BLS Signature workflow.
  </p>
</div>

---

## ✨ Features

- **Base Field Arithmetic:** Custom types for integer operations over modulo fields ($F_p$).
- **Polynomial Arithmetic:** Full implementation for operations over polynomials, utilized to dynamically build Extension Fields ($F_{p^k}$) from irreducible polynomials.
- **Elliptic Curves over $F_p$ & $F_{p^k}$:** Fully implemented point addition, point doubling, and scalar multiplication optimized with shared math calculations.
- **Miller's Algorithm:** Mathematical looping and point tangents evaluations to process algebraic pairings.
- **Reduced Tate Pairing ($e_r(P, Q)$):** Bilinear mapping between a cyclic sub-group of $G_1$ (on $F_p$) and $G_2$ (on $F_{p^k}$) down to the multiplicative subset.
- **BLS Signature Scheme:** Verifiable, robust pairing-based cryptographic protocol demonstration.
- **Server Wrapper:** Includes a lightweight HTTP visual interface to experiment with the trace outputs interactively.

## 📁 Repository Structure

```text
├── Fp.py / Fpk.py           # Finite Field and Extension Field class models
├── poly.py / poly_util.py   # Polynomial arithmetic and irreducible polynomial searching
├── ellipticCurves.py        # Elliptic Curves mathematics over base field Fp
├── ellipticCurvesFpk.py     # Elliptic Curves projected over Extension Field Fp^k
├── ellipticUtils.py         # Shared arithmetic logic (slope calc, point tracking)
├── hash.py                  # Map/Hash a string sequence down to an Elliptic Curve point
├── miller.py                # Implementation of geometric Line Evaluation and Miller Loop
├── findQ.py                 # Utilities to dynamically query points and map matching dimensions
├── bls_workflow.py          # The core pipeline encapsulating BLS Signature generations/checks
├── server.py                # Simple HTTP server endpoint for UI pairing verifications
└── main.py                  # CLI demonstration workflow execution
```

## 🚀 Quick Start

### Prerequisites
The codebase explicitly avoids overarching, large third-party crypto-lib dependencies to strictly adhere to pure Python algorithmic transparency.
Requires **Python 3.8+**.

### Running the CLI Demonstration
Execute the core script to watch the mathematics unroll:

```bash
python main.py
```
*Observe terminal traces outputting field expansions, curve mapping logic, Miller accumulations, and successful verifications.*

### Running the Local Interactive Web UI
Spin up the local visual pairing interface:

```bash
python server.py
```
Open your browser to `http://localhost:8000` to interact with custom configurations, curves, and secret keys!

## 🧠 Educational Mentions

This implementation is intended strictly for algorithm exploration, instructional cryptography, and pairing comprehension. As a pure Python environment written transparently over basic types, it naturally trades production resistance (such as resistance to Side-Channel Attacks, Constant-time execution checks, or natively compiled extensions) for absolute formula clarity.

