"""R3: lean versus robust in CT22's own model (theory/ROBUSTNESS.md §5); R2-e: ambiguity there.

Model (THEORY B.9 CT22, `theory/meq_checks/meq_derive.py`): diffusion reserve, check interval tau,
m = y - c/tau - w sigma^2 tau/2, s^2 = s0^2 + w^2 sigma^4 tau^3/3, theta = 2m/s^2 (diffusion
approximation of the Lundberg exponent); certified iff theta >= ln(1/eps)/B.
"""
import math
import numpy as np
from scipy.optimize import brentq, minimize_scalar

Y, C, W, SG, S0, EPS = 1.0, 0.05, 1.0, 1.0, 0.3, 1e-3


def theta(t, sg=SG):
    m = Y - C / t - W * sg ** 2 * t / 2
    return 2 * m / (S0 ** 2 + W ** 2 * sg ** 4 * t ** 3 / 3)


def cost(t, sg=SG):
    return C / t + W * sg ** 2 * t / 2


def tau_star(B, sg_cert=SG, sg_obj=SG):
    """Cheapest (under sg_obj) interval certified under sg_cert; None if none is certified.
    theta is quasiconcave in tau, so the certified set is an interval around its argmax tS;
    the cost is convex with minimum tE; the answer is tE or the interval end nearest tE (exact root)."""
    need = math.log(1 / EPS) / B
    tS = minimize_scalar(lambda t: -theta(t, sg_cert), bounds=(1e-3, 3), method="bounded",
                         options={"xatol": 1e-12}).x
    if theta(tS, sg_cert) < need:
        return None
    tE = math.sqrt(2 * C / (W * sg_obj ** 2))
    if theta(tE, sg_cert) >= need:
        return tE
    g = lambda t: theta(t, sg_cert) - need
    return brentq(g, tS, tE, xtol=1e-15) if tE > tS else brentq(g, tE, tS, xtol=1e-15)


def margin_sigma(B, t):
    """Largest fractional rise delta in sigma for which design t stays certified (0 if binding)."""
    need = math.log(1 / EPS) / B
    if theta(t) < need - 1e-12:
        return None
    g = lambda d: theta(t, SG * (1 + d)) - need
    if g(0) <= 1e-12:
        return 0.0
    hi = 1e-3
    while g(hi) > 0:
        hi *= 2
    return brentq(g, 0, hi)


def run():
    res = {}
    tE = math.sqrt(2 * C / (W * SG ** 2))
    tS = minimize_scalar(lambda t: -theta(t), bounds=(1e-3, 3), method="bounded").x
    Bmin = math.log(1 / EPS) / theta(tS); Bslack = math.log(1 / EPS) / theta(tE)
    res["Bmin,Bslack"] = (round(Bmin, 4), round(Bslack, 4))
    # R3-a: the cost-minimizing design's margin against a rise in sigma is zero whenever ruin binds,
    # positive and rising in B once slack.
    marg = {}
    for B in [0.49, 0.5, 0.505, 0.52, 0.6, 1.0, 5.0]:
        t = tau_star(B)
        marg[B] = round(margin_sigma(B, t), 6)
    res["a_sigma_margin_by_B"] = marg
    # first-order violation at a binding point: bound e^{-theta B} with sigma +1% exceeds eps
    B = 0.5; t = tau_star(B)
    res["a_bound_at_binding_sigma+1%"] = math.exp(-theta(t, SG * 1.01) * B) / EPS
    # R3-b: an unmodeled jump of size X > B at rate lam: P(ruin by T) >= 1 - e^{-lam T}, any design here
    lam, T = 1e-3, 1e4
    res["b_ruin_floor_unmodeled_jump"] = 1 - math.exp(-lam * T)
    # R2-e: ambiguity sigma in [SG, SG(1+u)]; theta falls in sigma, so the worst case is the top.
    viol = 0
    for t in [0.1, 0.2, 0.3, 0.4]:
        th = [theta(t, SG * (1 + d)) for d in np.linspace(0, 0.3, 31)]
        viol += any(b > a for a, b in zip(th, th[1:]))
    res["e_theta_decreasing_in_sigma_violations"] = viol
    rows = {}
    for u in [0, 0.005, 0.01, 0.015, 0.02]:
        sgm = SG * (1 + u)
        tSu = minimize_scalar(lambda t: -theta(t, sgm), bounds=(1e-3, 3), method="bounded").x
        Bmin_u = math.log(1 / EPS) / theta(tSu, sgm)
        tB = tau_star(0.51, sg_cert=sgm)
        rows[u] = dict(Bmin=round(Bmin_u, 4), tau_at_B0p51=None if tB is None else round(tB, 5),
                       fitted_cost=None if tB is None else round(cost(tB), 5))
    res["e_robust_by_u"] = rows
    tl = [r["tau_at_B0p51"] for r in rows.values()]
    res["e_tau_nonincreasing_in_u"] = all(b <= a + 1e-12 for a, b in zip(tl, tl[1:]))
    jl = [r["fitted_cost"] for r in rows.values()]
    res["e_cost_nondecreasing_in_u"] = all(b >= a - 1e-12 for a, b in zip(jl, jl[1:]))
    return res


if __name__ == "__main__":
    for k, v in run().items():
        print(k, "=", v)
