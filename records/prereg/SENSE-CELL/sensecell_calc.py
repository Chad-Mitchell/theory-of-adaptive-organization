"""SENSE-CELL locked calculator (pure functions; no data I/O). Run `python3 sensecell_calc.py` for self-tests.
Lan et al. 2012 (Nat Phys 8:422; PMC3378065): best-performance (BP) line eps = eps0*exp(-alpha*dW), alpha=(kR+kB)/(2kB),
a0=kR/(kR+kB) => alpha = 1/(2(1-a0)); dW = dissipation per receptor per methylation time (kT)."""
import math
KAPPA = 0.15           # mirrored-rule margin (same kappa as the locked causal / pass rules)
DG0 = 29.0             # kT per SAM methylation cycle (Lan 2012, text near Fig 4b)
EFF = 0.20             # Lan's stated 'modest 20% efficiency' (dW/dG0) giving ~99% accuracy
EPS_ANCHOR = 0.01      # '~99% accuracy' at that efficiency

def eps0_anchor(alpha):
    """eps0 from the text anchor: dW=EFF*DG0 on the BP line gives eps=EPS_ANCHOR."""
    return EPS_ANCHOR * math.exp(alpha * EFF * DG0)

def alpha_from_a0(a0):
    return 1.0 / (2.0 * (1.0 - a0))

def dW_bp(eps, eps0, alpha):
    """minimum dissipation (kT per cycle) for relative adaptation error eps on the BP line; 0 if eps>=eps0."""
    return max(0.0, math.log(eps0 / eps) / alpha)

def beta_phys(eps, eps0, alpha, dg0=DG0):
    w = dW_bp(eps, eps0, alpha)
    return math.inf if w <= 0 else dg0 / w

def theta_eff(eps, eps0, convention="amplitude"):
    """local price exponent of precision at fixed adaptation speed: dln(dW)/dln(P).
    amplitude: P=1/eps -> 1/ln(eps0/eps) (conservative: larger); variance: P=1/eps^2 -> half of that."""
    L = math.log(eps0 / eps)
    if L <= 0: return math.inf
    return 1.0 / L if convention == "amplitude" else 0.5 / L

def verdict_band_upper(lo, hi, edge, kappa=KAPPA):
    """Claim 'quantity <= edge' (interval [lo,hi]). Mirrored rule: PASS needs hi <= edge*(1-kappa);
    FAIL needs lo >= edge*(1+kappa); else INCONCLUSIVE."""
    if hi <= edge * (1 - kappa): return "PASS"
    if lo >= edge * (1 + kappa): return "FAIL"
    return "INCONCLUSIVE"

if __name__ == "__main__":
    a = 1.0
    assert abs(dW_bp(0.01, eps0_anchor(a), a) - EFF * DG0) < 1e-9
    assert abs(beta_phys(0.01, eps0_anchor(a), a) - 5.0) < 1e-9      # by construction at the anchor
    assert abs(theta_eff(0.1, math.e) - 1/math.log(math.e/0.1)) < 1e-12
    assert verdict_band_upper(2, 8, 10) == "PASS" and verdict_band_upper(11, 30, 10) == "INCONCLUSIVE" and verdict_band_upper(12, 30, 10) == "FAIL"
    assert verdict_band_upper(5, 9, 10) == "INCONCLUSIVE"
    print("self-tests ok")
