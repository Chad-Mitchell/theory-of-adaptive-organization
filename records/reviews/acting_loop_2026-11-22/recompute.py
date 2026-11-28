"""Independent recomputation of the acting-loop load-bearing numbers.

This file does not import theory/acting_loop_checks or theory/acting_memory_checks.
Every closed form is differentiated or solved here. A second evaluation uses the
state equations, quadrature, or a finite difference.

Run from the repo root:
  nice -n 19 python3 reviews/acting_loop_2026-11-22/recompute.py
"""

from __future__ import annotations

import math
from decimal import Decimal, ROUND_HALF_UP

import mpmath as mp
import numpy as np
import sympy as sp
from scipy import optimize, stats

mp.mp.dps = 80

NOTES = {
    "factor_a1": "0.171572875254",
    "factor_a_half": "0.381966011250",
    "factor_a2": "0.055728090001",
    "gap_stake1_r_half": "-1.096373258863",
    "fraction_stake4": "0.856768708291",
    "gap_stake4": "0.033889928154",
    "variance": "0.853553390593",
    "stock_open": "0.346573590280",
    "stock_closed": "0.267399998370",
    "cap_derivative": "0.189957517375",
    "tail": "0.000014940159",
    "second_derivative": "-0.321714500038",
    "threshold": "0.160857250019",
    "slope": "1.552284749831",
    "spread": "-0.001612560843",
    "sign_gap": "0.031682633557",
    "sign_floor": "4.966383544211",
    "sign_j8": "4.998066177768",
    "sign_loss": "4.439079197657",
    "cox_life": "0.655679542419",
    "sign_slope_tenth": "-0.082159696490",
    "sign_slope_half": "0.317840303510",
}


def close(x, y, tol: str = "1e-30") -> bool:
    return abs(as_mp(x) - as_mp(y)) < mp.mpf(tol)


def as_mp(x) -> mp.mpf:
    if isinstance(x, mp.mpf):
        return x
    return mp.mpf(str(x))


def r12(x) -> str:
    raw = mp.nstr(as_mp(x), 50, strip_zeros=False, min_fixed=-50, max_fixed=50)
    quant = Decimal(raw).quantize(Decimal("1e-12"), rounding=ROUND_HALF_UP)
    return format(quant, ".12f")


def report(name: str, got, note_key: str | None = None) -> bool:
    got_s = r12(got)
    if note_key is None:
        print(f"  {name} = {got_s}")
        return True
    note = NOTES[note_key]
    diff = abs(mp.mpf(got) - mp.mpf(note))
    ok = got_s == note
    flag = "MATCH" if ok else "DIFF"
    print(f"  {flag}  {name}")
    print(f"         computed {got_s}   note {note}   abs {mp.nstr(diff, 6)}")
    return ok


def main() -> None:
    ok = True
    a, q, rho, b, theta = sp.symbols("a q rho b theta", positive=True)
    p, K = sp.symbols("p K", positive=True)

    print("factors, from q - 2 a P with P = -a + sqrt(a^2 + q) at q = 1")
    P = -a + sp.sqrt(a**2 + q)
    factor = sp.simplify(q - 2 * a * P)
    factor_q1 = sp.simplify(factor.subs(q, 1))
    general = sp.simplify(1 - 2 * a / (a + sp.sqrt(a**2 + 1)))
    assert sp.simplify(factor_q1 - general) == 0
    closed = {
        1: sp.simplify(3 - 2 * sp.sqrt(2)),
        sp.Rational(1, 2): sp.simplify((3 - sp.sqrt(5)) / 2),
        2: sp.simplify(1 - 4 / (2 + sp.sqrt(5))),
    }
    for aval, key in ((1, "factor_a1"), (sp.Rational(1, 2), "factor_a_half"), (2, "factor_a2")):
        got = factor_q1.subs(a, aval)
        assert sp.simplify(got - closed[aval]) == 0
        assert got > 0
        ok &= report(f"full-information factor a={aval}", got.evalf(40), key)
        direct = (1 - 2 * aval / (aval + sp.sqrt(aval**2 + 1))).evalf(40)
        assert abs(got.evalf(40) - direct) < sp.Float("1e-30")

    alpha = (4 - mp.pi) / (6 * mp.pi)
    print("priced gaps, direct state cost against the closed form")
    gap_half = direct_gap(q=1, a=1, theta=1, r=mp.mpf("1/2"), alpha=alpha)
    form_half = closed_gap(q=1, a=1, theta=1, r=mp.mpf("1/2"), alpha=alpha)
    assert abs(gap_half - form_half) < mp.mpf("1e-30")
    exact_half = mp.mpf("1/2") * (3 - 2 * mp.sqrt(2) - 2 - 8 * alpha)
    assert abs(form_half - exact_half) < mp.mpf("1e-30")
    ok &= report("priced gap at stake 1, r=1/2", form_half, "gap_stake1_r_half")

    bracket_limit = (3 - 2 * mp.sqrt(2)) - 1 - 2 * alpha
    print(f"  stake-1 bracket as r -> 1: {r12(bracket_limit)} (negative: {bracket_limit < 0})")
    worst = max(closed_gap(q=1, a=1, theta=1, r=mp.mpf(r), alpha=alpha) for r in [i / 200 for i in range(1, 200)])
    print(f"  stake-1 grid max of Delta on k/200: {r12(worst)} (all negative: {worst < 0})")
    if not (bracket_limit < 0 and worst < 0):
        ok = False

    K4 = -1 + mp.sqrt(5)
    K4_sq = K4**2
    coeff = [float(K4_sq), 0.0, float(2 * alpha - 1), float(-4 * alpha)]
    numpy_roots = [z.real for z in np.roots(coeff) if abs(z.imag) < 1e-10 and 0 < z.real < 1]
    if len(numpy_roots) != 1:
        raise RuntimeError(f"numpy cubic roots {numpy_roots}")
    root = bisect(lambda r: K4_sq * r**3 + (2 * alpha - 1) * r - 4 * alpha, mp.mpf("0.5"), mp.mpf("0.99"))
    if abs(root - mp.mpf(numpy_roots[0])) > mp.mpf("1e-12"):
        raise RuntimeError("numpy root disagrees with the bisection")
    gap4 = direct_gap(q=4, a=1, theta=1, r=root, alpha=alpha)
    gap4_form = closed_gap(q=4, a=1, theta=1, r=root, alpha=alpha)
    assert abs(gap4 - gap4_form) < mp.mpf("1e-28")
    neighbors = [
        direct_gap(q=4, a=1, theta=1, r=root + mp.mpf(h), alpha=alpha) for h in ("-1e-4", "1e-4")
    ]
    minimizes = gap4 > neighbors[0] and gap4 > neighbors[1]
    print(f"  stake-4 stationary fraction minimizes the closed-loop cost: {minimizes}")
    if not minimizes or not (gap4 > 0):
        ok = False
    ok &= report("priced fraction at stake 4", root, "fraction_stake4")
    ok &= report("priced gap at stake 4", gap4, "gap_stake4")

    print("variance, mutual information, and the separated gain")
    gain = -1 + mp.sqrt(2)
    v = (2 + mp.sqrt(2)) / 4
    s = mp.sqrt(2) / 4
    p_half = mp.mpf("1/2")
    # Lyapunov: Riccati gives u_o p^2 = 2 a (theta - p), and E[m e] = 0, so s = a(theta-p)/(a+bK).
    uo = 4
    assert abs(uo * p_half**2 - 2 * (1 - p_half)) < mp.mpf("1e-30")
    s_lyap = (uo * p_half**2 / 2) / (1 + gain)
    assert abs(s_lyap - s) < mp.mpf("1e-30")
    assert abs(p_half + s - v) < mp.mpf("1e-30")
    ok &= report("state variance at K=sqrt(2)-1, p=1/2", v, "variance")
    stock_open = mp.mpf("1/2") * mp.log(2)
    stock_closed = mp.mpf("1/2") * mp.log(v / p_half)
    assert abs(stock_closed - mp.mpf("1/2") * mp.log(1 + mp.power(2, mp.mpf("-1/2")))) < mp.mpf("1e-30")
    ok &= report("mutual information, no feedback", stock_open, "stock_open")
    ok &= report("mutual information, with feedback", stock_closed, "stock_closed")
    print(f"  separated gain = sqrt(2)-1 = {r12(gain)}")
    if sp.simplify((-a + sp.sqrt(a**2 + q * b**2 / rho)) / b - (-1 + sp.sqrt(2))).subs({a: 1, q: 1, b: 1, rho: 1}) != 0:
        ok = False
    # Stationarity of q v + rho K^2 s at fixed p. The critical-point equation has no p.
    ac = a + b * K
    s_sym = a * (theta - p) / ac
    v_sym = p + s_sym
    reg = q * v_sym + rho * K**2 * s_sym
    dK = sp.together(sp.diff(reg, K))
    numer = sp.numer(sp.together(dK))
    crit = sp.simplify(sp.solve(numer, K)[0])
    claimed = (-a + sp.sqrt(a**2 + q * b**2 / rho)) / b
    assert sp.simplify(crit - claimed) == 0
    assert p not in crit.free_symbols and theta not in crit.free_symbols
    print("  gain critical point has no p and no theta: True")

    print("cap, capped-loss derivative, and the Gaussian tail")
    # v = 1/2 + 1/(2(1+K)) <= 3/5 iff K >= 4.
    cap_gain_exact = sp.Rational(1, 2) / (sp.Rational(3, 5) - sp.Rational(1, 2)) - 1
    v_at_4_exact = sp.Rational(1, 2) + 1 / (2 * (1 + cap_gain_exact))
    assert cap_gain_exact == 4
    assert sp.simplify(v_at_4_exact - sp.Rational(3, 5)) == 0
    cap_gain = as_mp(cap_gain_exact)
    print("  tight-cap gain = 4 exactly; v(4) = 3/5 exactly")
    deriv_closed = capped_derivative(v)
    deriv_diff = finite_difference_capped(float(gain))
    print(f"  finite-difference derivative {deriv_diff:.12f}")
    if abs(deriv_closed - mp.mpf(deriv_diff)) > mp.mpf("1e-9"):
        ok = False
        print("  DIFF finite difference disagrees with the analytic derivative")
    quad_phi = expectation_min_sq(v)
    closed_phi = phi_closed(v)
    if abs(quad_phi - closed_phi) > mp.mpf("1e-12"):
        ok = False
        print("  DIFF quadrature of E[min(X^2,1)] disagrees with the closed form")
    ok &= report("capped-loss derivative at the Riccati gain", deriv_closed, "cap_derivative")
    quad_d = quadratic_derivative(float(gain))
    print(f"  quadratic derivative at the same gain {quad_d:.3e}")
    if abs(quad_d) > 1e-9:
        ok = False
    tail = mp.erfc(4 / mp.sqrt(2 * v))
    tail_scipy = 2 * stats.norm.sf(4 / math.sqrt(float(v)))
    print(f"  scipy tail {tail_scipy:.12f}")
    if abs(tail - mp.mpf(tail_scipy)) > mp.mpf("1e-12"):
        ok = False
    ok &= report("P(X^2 > 16)", tail, "tail")
    inside = tail < mp.mpf("1/20")
    print(f"  tail inside 1/20, so B=16 does not bind: {inside}")
    if not inside:
        ok = False

    print("fixed intensity u_o=4: slope, curvature, threshold, spread")
    slope, curv, spread = fixed_intensity_shape(alpha)
    ok &= report("slope dJ/d theta", slope, "slope")
    ok &= report("second derivative", curv, "second_derivative")
    ok &= report("convex-gap threshold", -curv / 2, "threshold")
    ok &= report("spread at half-width 1/10", spread, "spread")
    num_slope, num_curv = numerical_derivatives()
    print(f"  numerical slope {r12(num_slope)}  numerical curvature {r12(num_curv)}")
    if abs(num_slope - slope) > mp.mpf("1e-10") or abs(num_curv - curv) > mp.mpf("1e-8"):
        ok = False
        print("  DIFF numerical derivatives disagree")
    # Curvature of this slice is negative at every theta > 0: L'' < 0 and the K factor is positive.
    Ksq = gain**2
    factor_L = 1 + Ksq / 2
    print(f"  curvature factor on L is {r12(factor_L)} > 0, and L'' = -8/(1+8 theta)^(3/2) < 0")
    if not (factor_L > 0):
        ok = False

    print("Q_fin, the exogenous shrunk-spring formula, at r=1/2 and lambda=20")
    qfin = q_fin(r=mp.mpf("1/2"), lam=20, a=1)
    qfin_exact = sp.simplify(q_fin_sym())
    assert qfin_exact == sp.Rational(10, 9)
    print(f"  Q_fin = {r12(qfin)} and the rational value is 10/9; the formula has no K")

    print("sign grid: minimize A(r)/theta + C(r), gap against inf C")
    grid = [mp.mpf(x) for x in ("1/8", "1/4", "1/2", "1", "2", "4", "8")]
    floor_r = bisect(lambda r: c_prime(r), mp.mpf("0.2"), mp.mpf("0.7"))
    floor = c_of(floor_r)
    rows = []
    for th in grid:
        rr = bisect(lambda r, th=th: j_prime(r, th), mp.mpf("0.2"), mp.mpf("0.9"))
        jj = j_of(rr, th)
        rows.append((th, rr, jj))
        if not (jj > floor):
            ok = False
    j8 = rows[-1][2]
    gap = j8 - floor
    ok &= report("sign floor inf C", floor, "sign_floor")
    ok &= report("sign cost J*(8)", j8, "sign_j8")
    ok &= report("sign-grid gap J*(8) - inf C", gap, "sign_gap")
    for th, rr, jj in rows:
        print(f"  grid theta={th} r*={r12(rr)} J*={r12(jj)}")
    decreasing = all(rows[i][2] > rows[i + 1][2] for i in range(len(rows) - 1))
    print(f"  grid strictly decreasing and above the floor: {decreasing and all(jj > floor for _, _, jj in rows)}")
    if not decreasing:
        ok = False

    print("sign loss under feedback")
    corr = mp.sqrt(s / v)
    assert abs(corr - mp.sqrt(gain)) < mp.mpf("1e-30")
    loss = 16 * mp.acos(corr) / mp.pi
    loss_open = 16 * mp.acos(1 / mp.sqrt(2)) / mp.pi
    print(f"  sensing-alone sign loss at correlation 1/sqrt(2): {r12(loss_open)} (4 exactly: {close(loss_open, 4)})")
    if not close(loss_open, 4):
        ok = False
    ok &= report("feedback sign loss", loss, "sign_loss")
    if not (loss > 4):
        ok = False

    print("Cox posterior variance and mean lifetime")
    var_post = cox_variance_exact()
    var_quad = cox_variance_quadrature()
    print(f"  quadrature posterior variance {r12(var_quad)}")
    if not close(var_post, mp.mpf("1/2")) or abs(var_quad - mp.mpf("1/2")) > mp.mpf("1e-12"):
        ok = False
        print("  DIFF Cox variance is not 1/2")
    else:
        print("  MATCH  Cox posterior variance = 1/2 exactly")
    life = mp.sqrt(mp.pi / 2) * mp.e ** mp.mpf("1/2") * mp.erfc(1 / mp.sqrt(2))
    life_quad = cox_lifetime_quadrature()
    print(f"  quadrature lifetime {r12(life_quad)}")
    if abs(life - life_quad) > mp.mpf("1e-12"):
        ok = False
        print("  DIFF lifetime quadrature disagrees with the erfc expression")
    ok &= report("Cox mean lifetime", life, "cox_life")
    if not (life > mp.mpf("1/2")):
        ok = False

    print("b = 0 minimum")
    b0_ok = check_b0(alpha)
    print(f"  b=0 minimum is J = q*theta + gamma1*theta: {b0_ok}")
    if not b0_ok:
        ok = False

    base = mp.mpf(2) / 3 - 8 / (3 * mp.pi)
    ok &= report("old sign slope plus 1/10", base + mp.mpf("1/10"), "sign_slope_tenth")
    ok &= report("old sign slope plus 1/2", base + mp.mpf("1/2"), "sign_slope_half")

    print("RESULT", "ALL MATCH" if ok else "DISCREPANCY")
    if not ok:
        raise SystemExit(1)


def direct_gap(q, a, theta, r, alpha):
    P = -a + mp.sqrt(a**2 + q)
    K = P
    p = r * theta
    uo = 2 * a * (theta - p) / p**2
    L = a * (theta / p - 1)
    s = a * (theta - p) / (a + K)
    v = p + s
    J = L + alpha * uo + q * v + K**2 * s
    return q * theta - J


def closed_gap(q, a, theta, r, alpha):
    P = -a + mp.sqrt(a**2 + q)
    G = (q - 2 * a * P) * theta
    return (1 - r) * (G - a / r - 2 * alpha * a / (theta * r**2))


def bisect(fn, lo, hi) -> mp.mpf:
    flo, fhi = fn(lo), fn(hi)
    if flo == 0:
        return lo
    if fhi == 0:
        return hi
    if flo * fhi > 0:
        raise RuntimeError(f"root not bracketed: f({lo})={flo}, f({hi})={fhi}")
    for _ in range(400):
        mid = (lo + hi) / 2
        fmid = fn(mid)
        if fmid == 0 or hi - lo < mp.mpf("1e-40"):
            return mid
        if flo * fmid < 0:
            hi, fhi = mid, fmid
        else:
            lo, flo = mid, fmid
    return (lo + hi) / 2


def phi_prime(v):
    z = 1 / mp.sqrt(v)
    dens = mp.exp(-z**2 / 2) / mp.sqrt(2 * mp.pi)
    cdf = mp.mpf("1/2") * (1 + mp.erf(z / mp.sqrt(2)))
    return (2 * cdf - 1) - 2 * z * dens


def phi_closed(v):
    """E[min(X^2, 1)] for X ~ N(0, v), reduced by parts to the normal cdf."""
    z = 1 / mp.sqrt(v)
    dens = mp.exp(-z**2 / 2) / mp.sqrt(2 * mp.pi)
    cdf = mp.mpf("1/2") * (1 + mp.erf(z / mp.sqrt(2)))
    inner = -z * dens + cdf - mp.mpf("1/2")
    return 2 * v * inner + 2 * (1 - cdf)


def capped_derivative(v):
    return (1 - phi_prime(v)) / 4


def expectation_min_sq(v) -> mp.mpf:
    v = as_mp(v)

    def dens(x):
        return mp.exp(-(x**2) / (2 * v)) / mp.sqrt(2 * mp.pi * v)

    inside = mp.quad(lambda x: (x**2) * dens(x), [-1, 1])
    outside = mp.quad(lambda x: dens(x), [1, mp.inf]) + mp.quad(lambda x: dens(x), [mp.ninf, -1])
    return inside + outside


def finite_difference_capped(K: float) -> float:
    def objective(kk: float) -> float:
        s = 0.5 / (1 + kk)
        v = 0.5 + s
        return float(phi_closed(mp.mpf(v))) + kk * kk * s

    h = 1e-6
    return (objective(K + h) - objective(K - h)) / (2 * h)


def quadratic_derivative(K: float) -> float:
    def objective(kk: float) -> float:
        s = 0.5 / (1 + kk)
        v = 0.5 + s
        return v + kk * kk * s

    h = 1e-6
    return (objective(K + h) - objective(K - h)) / (2 * h)


def primitive_J(theta, alpha):
    """Closed-loop cost at fixed u_o = 4, q = rho = a = b = kT = 1, gamma = 0."""
    s_theta = mp.sqrt(1 + 8 * theta)
    p = (-1 + s_theta) / 4
    L = (-1 + s_theta) / 2
    K = -1 + mp.sqrt(2)
    s = (theta - p) / (1 + K)
    v = p + s
    return L + alpha * 4 + v + K**2 * s


def fixed_intensity_shape(alpha):
    K = -1 + mp.sqrt(2)
    curv_exact = 4 * (2 * mp.sqrt(2) - 5) / 27
    slope_exact = (4 * mp.sqrt(2) - 1) / 3
    # Cross-check the closed forms by differentiating the primitive with mpmath.
    h = mp.mpf("1e-8")
    J0 = primitive_J(1, alpha)
    Jp = primitive_J(1 + h, alpha)
    Jm = primitive_J(1 - h, alpha)
    slope_num = (Jp - Jm) / (2 * h)
    curv_num = (Jp - 2 * J0 + Jm) / h**2
    if abs(slope_num - slope_exact) > mp.mpf("1e-10") or abs(curv_num - curv_exact) > mp.mpf("1e-8"):
        raise RuntimeError("primitive derivatives do not match the closed forms")
    delta = mp.mpf("1/10")
    spread = (primitive_J(1 - delta, alpha) + primitive_J(1 + delta, alpha)) / 2 - J0
    # K is used so a refactor that drops the gain cannot silently pass.
    if K <= 0:
        raise RuntimeError("gain")
    return slope_exact, curv_exact, spread


def numerical_derivatives():
    """SymPy differentiation of the primitive cost, independent of the printed closed form."""
    th = sp.symbols("theta", positive=True)
    s_th = sp.sqrt(1 + 8 * th)
    p = (-1 + s_th) / 4
    L = (-1 + s_th) / 2
    K = -1 + sp.sqrt(2)
    s = (th - p) / (1 + K)
    v = p + s
    alpha = (4 - sp.pi) / (6 * sp.pi)
    J = L + alpha * 4 + v + K**2 * s
    d1 = sp.diff(J, th).subs(th, 1).evalf(40)
    d2 = sp.diff(J, th, 2).subs(th, 1).evalf(40)
    return mp.mpf(str(d1)), mp.mpf(str(d2))


def q_fin(r, lam, a):
    rho_l = lam / (a + lam)
    return a * (1 - r) * rho_l / (rho_l * (1 + r) - 1)


def q_fin_sym():
    r, lam, a = sp.Rational(1, 2), 20, 1
    rho_l = sp.Rational(lam, a + lam)
    return sp.simplify(a * (1 - r) * rho_l / (rho_l * (1 + r) - 1))


def c_prime(r):
    return -1 / r**2 + 8 / (mp.pi * mp.sqrt(r * (1 - r)))


def c_of(r):
    return (1 - r) / r + 16 * mp.acos(mp.sqrt(1 - r)) / mp.pi


def j_prime(r, theta):
    alpha = (4 - mp.pi) / (6 * mp.pi)
    return 2 * alpha * (r - 2) / (theta * r**3) + c_prime(r)


def j_of(r, theta):
    alpha = (4 - mp.pi) / (6 * mp.pi)
    A = alpha * 2 * (1 - r) / r**2
    return A / theta + c_of(r)


def cox_variance_exact() -> mp.mpf:
    # Posterior weight (1 + x^2) times N(0, 1/3). Variance is the ratio of Gaussian moments.
    sig2 = sp.Rational(1, 3)
    var = sp.simplify(sig2 * (1 + 3 * sig2) / (1 + sig2))
    if var != sp.Rational(1, 2):
        raise RuntimeError(var)
    return mp.mpf(var)


def cox_variance_quadrature() -> mp.mpf:
    def weight(x):
        return (1 + x**2) * mp.exp(-mp.mpf("3/2") * x**2)

    m0 = mp.quad(weight, [mp.ninf, mp.inf])
    m2 = mp.quad(lambda x: (x**2) * weight(x), [mp.ninf, mp.inf])
    return m2 / m0


def cox_lifetime_quadrature() -> mp.mpf:
    def integrand(x):
        return (1 / (1 + x**2)) * mp.exp(-(x**2) / 2) / mp.sqrt(2 * mp.pi)

    return mp.quad(integrand, [mp.ninf, mp.inf])


def check_b0(alpha) -> bool:
    a_s, b_s, K_s, p_s, th_s = sp.symbols("a b K p theta", positive=True)
    v = sp.simplify(p_s + a_s * (th_s - p_s) / (a_s + b_s * K_s))
    if sp.simplify(v.subs(b_s, 0) - th_s) != 0:
        return False
    # Numerical scan. At b = 0 the variance is theta, so any probe or gain adds a nonnegative price.
    q, theta, gamma1 = 4, mp.mpf(2), mp.mpf("1/10")
    target = q * theta + gamma1 * theta

    def cost(uo, K):
        if uo <= 0:
            return target
        p = (-1 + mp.sqrt(1 + 2 * theta * uo)) / uo
        L = theta / p - 1
        return L + gamma1 * theta + alpha * uo + q * theta + K**2 * (theta - p)

    samples = []
    for uo in (0, mp.mpf("1e-6"), mp.mpf("0.1"), 1, 4, 20):
        for K in (0, mp.mpf("0.1"), 1, 4):
            samples.append(cost(mp.mpf(uo), mp.mpf(K)))
    if min(samples) != target:
        return False
    if any(c < target - mp.mpf("1e-30") for c in samples):
        return False
    interior = [c for c in samples if c != target]
    if not interior or min(interior) <= target:
        return False

    def objective(x):
        return float(cost(mp.mpf(x[0]), mp.mpf(x[1])))

    opt = optimize.minimize(objective, [0.2, 0.2], bounds=[(0, 30), (0, 30)])
    if not opt.success:
        return False
    return abs(opt.fun - float(target)) < 1e-9 and abs(opt.x[0]) < 1e-4


if __name__ == "__main__":
    main()
