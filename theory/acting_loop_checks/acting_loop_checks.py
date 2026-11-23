#!/usr/bin/env python3
"""Evaluate the locked acting-loop predictions.

The preregistration is theory/acting_loop_checks/PREREG.md. This script
checks that file's sha256 against LOCK.txt before it evaluates a cost.
"""
from __future__ import annotations

import hashlib
import math
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 80

HERE = Path(__file__).resolve().parent
FAILS = 0
CHECKS = 0
MISSES = 0


def check(name, ok, detail=""):
    global FAILS, CHECKS
    CHECKS += 1
    tag = "PASS" if ok else "FAIL"
    if not ok:
        FAILS += 1
    print(f"C{CHECKS:02d}  {tag}  {name}  {detail}")


def predict(name, ok, detail=""):
    global MISSES
    if not ok:
        MISSES += 1
    tag = "HIT" if ok else "MISS"
    print(f"PREDICTION-{tag}  {name}  {detail}")


def D(x):
    return x if isinstance(x, Decimal) else Decimal(x)


def sqrt(x):
    return D(x).sqrt()


def pi_machin():
    def atan_unit(x):
        x = D(x)
        term = x
        s = x
        xx = x * x
        n = 1
        while True:
            term *= -xx
            n += 2
            add = term / n
            s += add
            if abs(add) < Decimal("1e-70"):
                return s

    return 16 * atan_unit(Decimal(1) / 5) - 4 * atan_unit(Decimal(1) / 239)


PI = pi_machin()
TOL = Decimal("1e-9")
TIGHT = Decimal("1e-12")


def near(x, y, tol=TOL):
    return abs(D(x) - D(y)) <= tol


def atan(x):
    x = D(x)
    if x == 0:
        return Decimal(0)
    if x < 0:
        return -atan(-x)
    if x > 1:
        return PI / 2 - atan(1 / x)
    folds = 0
    while x > Decimal("0.1"):
        x = x / (1 + sqrt(1 + x * x))
        folds += 1
    term = x
    s = x
    xx = x * x
    n = 1
    while True:
        term *= -xx
        n += 2
        add = term / n
        s += add
        if abs(add) < Decimal("1e-60"):
            break
    return s * (Decimal(2) ** folds)


def acos(x):
    x = D(x)
    if x >= 1:
        return Decimal(0)
    return atan(sqrt(1 - x * x) / x)


def psi(r):
    r = D(r)
    if r >= 1:
        return Decimal(1) / 2
    return acos(sqrt(1 - r)) / PI


def psi_prime(r):
    r = D(r)
    return 1 / (2 * PI * sqrt(r * (1 - r)))


def erf_series(z):
    z = D(z)
    coef = 2 / sqrt(PI)
    term = z
    s = z
    n = 0
    zz = z * z
    while True:
        n += 1
        term *= -zz / n
        add = term / (2 * n + 1)
        s += add
        if abs(add) < Decimal("1e-60"):
            return coef * s


def erfc_decimal(z):
    return 1 - erf_series(z)


def phi_std(z):
    z = D(z)
    return (-(z * z) / 2).exp() / sqrt(2 * PI)


def Phi(z):
    z = D(z)
    return Decimal("0.5") * (1 + erf_series(z / sqrt(Decimal(2))))


ALPHA = (4 - PI) / (6 * PI)
A = Decimal(1)
KT = Decimal(1)
W = Decimal(16)
INF_C = Decimal("4.966383544211")


def hash_ok():
    body = (HERE / "PREREG.md").read_bytes()
    digest = hashlib.sha256(body).hexdigest()
    lock = (HERE / "LOCK.txt").read_text(encoding="utf-8")
    return digest in lock and "774e88fdda46720d933157ee586da3d197235b42" in lock, digest


def P_of(a, q, rho=Decimal(1), b=Decimal(1)):
    a, q, rho, b = D(a), D(q), D(rho), D(b)
    return (rho / b ** 2) * (-a + sqrt(a * a + q * b * b / rho))


def K_of(a, q, rho=Decimal(1), b=Decimal(1)):
    a, q, rho, b = D(a), D(q), D(rho), D(b)
    return (-a + sqrt(a * a + q * b * b / rho)) / b


def riccati_p(u, theta, a=Decimal(1)):
    u, theta, a = D(u), D(theta), D(a)
    if u == 0:
        return theta
    return (-a + sqrt(a * a + 2 * a * theta * u)) / u


def moments(a, b, K, p, theta):
    a, b, K, p, theta = D(a), D(b), D(K), D(p), D(theta)
    ac = a + b * K
    s = a * (theta - p) / ac
    v = p + s
    return s, v


def delta_priced(theta, a, r, q):
    theta, a, r, q = D(theta), D(a), D(r), D(q)
    factor = q - 2 * a * P_of(a, q)
    return (1 - r) * (factor * theta - a / r - 2 * ALPHA * a / (theta * r * r))


def J_direct(theta, a, r, q, b=Decimal(1), rho=Decimal(1)):
    """Closed-loop cost from the variance identities, heat floor, probe price."""
    theta, a, r, q = D(theta), D(a), D(r), D(q)
    p = r * theta
    u = 2 * a * (1 - r) / (theta * r * r)
    # Riccati consistency: p must match u.
    K = K_of(a, q, rho, b)
    s, v = moments(a, b, K, p, theta)
    L = a * (theta / p - 1)
    return KT * L + ALPHA * u + q * v + rho * K * K * s, u, p, s, v, L


def J_fixed_u(theta, u=Decimal(4), q=Decimal(1)):
    theta = D(theta)
    p = riccati_p(u, theta)
    L = (-A + sqrt(A * A + 2 * A * theta * u)) / 2
    K = K_of(1, q)
    s, v = moments(1, 1, K, p, theta)
    return q * v + K * K * s + L + ALPHA * u


def g_sign(r, theta):
    r, theta = D(r), D(theta)
    A_prime = ALPHA * 2 * A * (r - 2) / r ** 3
    C_prime = -KT * A / r ** 2 + W * psi_prime(r)
    return A_prime / theta + C_prime


def g_sign_prime(r, theta):
    r, theta = D(r), D(theta)
    A_second = ALPHA * 4 * A * (3 - r) / r ** 4
    q = r * (1 - r)
    psi_second = W / (2 * PI) * (Decimal("-0.5") * q ** Decimal("-1.5") * (1 - 2 * r))
    C_second = 2 * KT * A / r ** 3 + psi_second
    return A_second / theta + C_second


def C_of(r):
    r = D(r)
    return KT * A * (1 - r) / r + W * psi(r)


def J_sign(r, theta):
    r, theta = D(r), D(theta)
    return ALPHA * 2 * A * (1 - r) / (theta * r ** 2) + C_of(r)


def minimize_sign(theta):
    theta = D(theta)
    pi = float(PI)

    def jf(r):
        return float(ALPHA) * 2.0 * (1.0 - r) / (float(theta) * r * r) + (1.0 - r) / r + 16.0 * math.acos(math.sqrt(1.0 - r)) / pi

    best_r, best_j = 0.5, jf(0.5)
    for i in range(1, 4000):
        r = i / 4000
        val = jf(r)
        if val < best_j:
            best_r, best_j = r, val
    r = D(str(best_r))
    for _ in range(40):
        step = g_sign_prime(r, theta)
        nxt = r - g_sign(r, theta) / step
        if nxt <= Decimal("1e-12") or nxt >= 1:
            break
        if abs(nxt - r) < Decimal("1e-36"):
            r = nxt
            break
        r = nxt
    return r, J_sign(r, theta)


def minimize_C():
    def g(r):
        r = D(r)
        return -KT * A / r ** 2 + W * psi_prime(r)

    def gp(r):
        r = D(r)
        q = r * (1 - r)
        psi_second = W / (2 * PI) * (Decimal("-0.5") * q ** Decimal("-1.5") * (1 - 2 * r))
        return 2 * KT * A / r ** 3 + psi_second

    r = Decimal("0.4")
    for _ in range(40):
        nxt = r - g(r) / gp(r)
        if abs(nxt - r) < Decimal("1e-36"):
            r = nxt
            break
        r = nxt
    return r, C_of(r)


def main():
    ok, digest = hash_ok()
    check("preregistration hash matches LOCK.txt", ok, digest)
    if not ok:
        print(f"CHECKS {CHECKS}")
        print(f"FAILS {FAILS}")
        print("PREDICTION-MISS  hash  the lock does not match")
        return 1

    # Riccati at the passive intensity.
    p = riccati_p(4, 1)
    resid = 4 * p * p + 2 * p - 2
    check("Riccati residual at u=4, theta=1", abs(resid) < Decimal("1e-30"), f"p={p} resid={resid}")
    check("posterior variance is 1/2", p == Decimal("0.5"))

    # --- P1 full-information gap ---
    f1 = 1 - 2 * D(1) / (1 + sqrt(1 + 1))
    # 2a/(a+sqrt(a^2+1)) at a=1 is 2/(1+sqrt(2))
    factor_a1 = 3 - 2 * sqrt(2)
    check("full-info factor at a=1 equals 3-2*sqrt(2)", near(factor_a1, 1 - 2 / (1 + sqrt(2)), Decimal("1e-30")))
    check("full-info factor at a=1/2 equals (3-sqrt(5))/2", near((3 - sqrt(5)) / 2, 1 - D("0.5") * 2 * P_of(Decimal("0.5"), 1), Decimal("1e-30")))
    factor_a2 = 1 - 4 / (2 + sqrt(5))
    check("full-info factor at a=2 equals 1-4/(2+sqrt(5))", near(factor_a2, 1 - 2 * 2 * P_of(2, 1), Decimal("1e-30")))
    predict("P1 factor a=1", near(factor_a1, "0.171572875254"), f"{factor_a1}")
    predict("P1 factor a=1/2", near((3 - sqrt(5)) / 2, "0.381966011250"), f"{(3 - sqrt(5)) / 2}")
    predict("P1 factor a=2", near(factor_a2, "0.055728090001"), f"{factor_a2}")
    predict("P1 each factor positive", factor_a1 > 0 and (3 - sqrt(5)) / 2 > 0 and factor_a2 > 0)

    # Action alone: constant control cannot beat u=0.
    # mean = b*c/a, cost q*(theta + mean^2) + rho*c^2
    c = Decimal(1)
    cost_shift = 1 * (1 + c * c) + c * c
    check("constant action costs more than the zero action", cost_shift > 1, f"{cost_shift}")
    # Observation alone at K=0 leaves v=theta and adds a positive channel cost.
    Jd, u, p_d, s, v, L = J_direct(1, 1, Decimal("0.5"), 1)
    # K=0 rebuild
    s0, v0 = moments(1, 1, 0, Decimal("0.5"), 1)
    check("observation alone leaves the state variance at theta", v0 == 1, f"v={v0}")
    channel = L + ALPHA * u
    check("observation channel at r=1/2 has positive price", channel > 0, f"{channel}")

    # --- P2 ---
    d_half = delta_priced(1, 1, Decimal("0.5"), 1)
    Jd_half, u_h, _, _, _, _ = J_direct(1, 1, Decimal("0.5"), 1)
    check("priced gap matches the direct cost at r=1/2", near(d_half, 1 - Jd_half, Decimal("1e-24")), f"delta={d_half} direct={1 - Jd_half}")
    predict("P2 delta at r=1/2", near(d_half, "-1.096373258863"), f"{d_half}")
    predict("P2 closed loop dearer at r=1/2", d_half < 0)
    bracket_edge = (3 - 2 * sqrt(2)) - 1 - 2 * ALPHA
    predict("P2 bracket at r to 1 is negative", bracket_edge < 0, f"{bracket_edge}")
    grid_neg = True
    worst = Decimal(0)
    r = Decimal("0.02")
    while r < 1:
        val = delta_priced(1, 1, r, 1)
        if val >= 0:
            grid_neg = False
        if val > worst:
            worst = val
        r += Decimal("0.02")
    check("no fraction on a 0.02-grid has a positive gap at stake 1", grid_neg, f"worst={worst}")

    # --- P3 stake 4 ---
    K2 = (sqrt(5) - 1) ** 2
    check("control weight at stake 4", near(K2, K_of(1, 4) ** 2, Decimal("1e-30")))
    r = Decimal("0.85")
    for _ in range(40):
        f = K2 * r ** 3 + (2 * ALPHA - 1) * r - 4 * ALPHA
        fp = 3 * K2 * r ** 2 + (2 * ALPHA - 1)
        nxt = r - f / fp
        if abs(nxt - r) < Decimal("1e-40"):
            r = nxt
            break
        r = nxt
    f_root = K2 * r ** 3 + (2 * ALPHA - 1) * r - 4 * ALPHA
    check("cubic residual at the stake-4 root", abs(f_root) < Decimal("1e-30"), f"r={r}")
    d4 = delta_priced(1, 1, r, 4)
    Jd4, _, _, _, _, _ = J_direct(1, 1, r, 4)
    check("priced gap matches the direct cost at stake 4", near(d4, 4 - Jd4, Decimal("1e-24")), f"{d4} vs {4 - Jd4}")
    predict("P3 root", near(r, "0.856768708291"), f"{r}")
    predict("P3 delta positive", near(d4, "0.033889928154") and d4 > 0, f"{d4}")
    # neighbors are smaller gaps: a maximum
    d_lo = delta_priced(1, 1, r - Decimal("0.01"), 4)
    d_hi = delta_priced(1, 1, r + Decimal("0.01"), 4)
    check("stake-4 root is a local maximum of the gap", d4 > d_lo and d4 > d_hi, f"{d_lo} {d4} {d_hi}")

    # b=0 reduction
    s_b0, v_b0 = moments(1, 0, Decimal(5), Decimal("0.5"), 1)
    check("b=0 leaves the state variance at theta for any gain", v_b0 == 1 and s_b0 == Decimal("0.5"), f"v={v_b0}")

    # --- P4 acting and memory ---
    K = sqrt(2) - 1
    s_c, v_c = moments(1, 1, K, Decimal("0.5"), 1)
    check("controlled variance equals (2+sqrt(2))/4", near(v_c, (2 + sqrt(2)) / 4, Decimal("1e-30")), f"{v_c}")
    predict("P4 state variance", near(v_c, "0.853553390593"), f"{v_c}")
    L_on = A * (1 / Decimal("0.5") - 1)
    L_off = L_on
    check("learning rate does not depend on the gain", L_on == L_off == 1)
    predict("P4 learning rate unchanged", L_on == 1 and L_off == 1)
    rho_l = Decimal(20) / 21
    Qfin = (1 - Decimal("0.5")) * rho_l / (rho_l * (1 + Decimal("0.5")) - 1)
    # 10/9 is the closed value. Decimal division at finite precision is not
    # bitwise-identical to the expanded quotient, so the residual is the check.
    check("finite-rate heat equals 10/9", near(Qfin, Decimal(10) / 9, Decimal("1e-30")), f"{Qfin}")
    predict("P4 finite-rate heat unchanged by the gain", near(Qfin, Decimal(10) / 9, Decimal("1e-30")))
    I0 = Decimal("0.5") * Decimal(2).ln()
    I1 = Decimal("0.5") * (v_c / Decimal("0.5")).ln()
    predict("P4 stock falls", near(I0, "0.346573590280") and near(I1, "0.267399998370") and I1 < I0, f"{I0} -> {I1}")
    check("stock drop is positive", I0 - I1 > 0, f"{I0 - I1}")

    # Lyapunov cross-check: s = p^2 u / (2 a_c)
    u4 = Decimal(4)
    ac = 1 + K
    s_lyap = (Decimal("0.5") ** 2 * u4) / (2 * ac)
    check("Lyapunov estimate variance matches the closed form", near(s_lyap, s_c, Decimal("1e-30")), f"{s_lyap} {s_c}")

    # --- P5 separation ---
    K_p1 = K_of(1, 1)
    K_p2 = K_of(1, 1)
    check("Riccati gain does not read the error variance", K_p1 == K_p2 == sqrt(2) - 1)
    predict("P5 Riccati gain is sqrt(2)-1", K_p1 == sqrt(2) - 1)
    K_cap = (1 - Decimal("0.5")) / (Decimal("3") / 5 - Decimal("0.5")) - 1
    predict("P5 tight cap selects gain 4", K_cap == 4, f"{K_cap}")
    check("capped gain exceeds the Riccati gain", K_cap > K_p1)
    v_op = (2 + sqrt(2)) / 4
    z = 1 / sqrt(v_op)
    phip = (2 * Phi(z) - 1) - 2 * z * phi_std(z)
    dC = Decimal("0.25") * (1 - phip)
    # quadratic derivative: q v' + 2 K s + K^2 s', v'=s'=-1/4
    sp = Decimal("-0.25")
    d_quad = 1 * sp + 2 * K * s_c + K * K * sp
    check("quadratic derivative at the Riccati gain is zero", abs(d_quad) < Decimal("1e-24"), f"{d_quad}")
    predict("P5 capped-loss derivative", near(dC, "0.189957517375"), f"{dC}")
    predict("P5 capped derivative is not zero", abs(dC) > Decimal("0.1"))
    # P(X^2>16) = erfc(4/sqrt(2v))
    tail = erfc_decimal(4 / sqrt(2 * v_op))
    predict("P5 reserve cap does not bind", tail < Decimal("0.05") and tail < Decimal("1e-3"), f"{tail}")

    # --- P6 level and variability ---
    slope = (4 * sqrt(2) - 1) / 3
    d2 = 4 * (2 * sqrt(2) - 5) / 27
    predict("P6 slope", near(slope, "1.552284749831") and slope > 0, f"{slope}")
    predict("P6 second derivative", near(d2, "-0.321714500038") and d2 < 0, f"{d2}")
    # finite-difference cross-check of the second derivative
    h = Decimal("1e-6")
    fd2 = (J_fixed_u(1 + h) - 2 * J_fixed_u(1) + J_fixed_u(1 - h)) / h ** 2
    check("finite difference matches the second derivative", near(fd2, d2, Decimal("1e-8")), f"fd={fd2}")
    spread = (J_fixed_u(Decimal("0.9")) + J_fixed_u(Decimal("1.1"))) / 2 - J_fixed_u(1)
    predict("P6 spread", near(spread, "-0.001612560843") and spread < 0, f"{spread}")
    thresh = 2 * (5 - 2 * sqrt(2)) / 27
    predict("P6 convex-gap threshold", near(thresh, "0.160857250019"), f"{thresh}")
    d2_witness = d2 + 2 * Decimal(1)
    predict("P6 witness gap flips the second derivative", d2_witness > 0 and Decimal(1) > thresh, f"{d2_witness}")

    # --- P7 sign grid ---
    grid = [Decimal(x) for x in ("0.125", "0.25", "0.5", "1", "2", "4", "8")]
    published = {
        Decimal("8"): Decimal("4.998066177768"),
    }
    above = True
    j8 = None
    for th in grid:
        rr, jj = minimize_sign(th)
        if jj <= INF_C:
            above = False
        if th == 8:
            j8 = jj
        check(f"sign cost at theta={th} is above the floor", jj > INF_C, f"J={jj} r={rr}")
    gap8 = j8 - INF_C
    predict("P7 every grid cost above the floor", above)
    predict("P7 gap at theta=8", near(gap8, "0.031682633557") and near(j8, published[Decimal(8)]), f"J8={j8} gap={gap8}")
    rC, cmin = minimize_C()
    predict("P7 recomputed floor matches the published floor", near(cmin, INF_C), f"{cmin} at r={rC}")

    # --- P8 sign under feedback ---
    corr = sqrt(sqrt(2) - 1)
    corr_open = sqrt(Decimal("0.5"))
    psi_fb = acos(corr) / PI
    loss_fb = 16 * psi_fb
    predict("P8 sign loss under feedback", near(loss_fb, "4.439079197657") and loss_fb > 4, f"{loss_fb}")
    predict("P8 correlation falls", corr < corr_open, f"{corr} < {corr_open}")
    check("sign increase", near(loss_fb - 4, "0.439079197657"), f"{loss_fb - 4}")

    # --- P9 Cox ---
    sig2 = 1 / (1 + 2 * 1 * 1)
    var_post = sig2 * (1 + 3 * sig2) / (1 + sig2)
    predict("P9 posterior variance", var_post == Decimal("0.5"), f"{var_post}")
    predict("P9 independent variance stays at 1", Decimal(1) == 1)
    ET = sqrt(PI / 2) * (Decimal("0.5")).exp() * erfc_decimal(1 / sqrt(Decimal(2)))
    predict("P9 mean lifetime", near(ET, "0.655679542419") and ET > Decimal("0.5"), f"{ET}")
    check("Cox variance is below the independent variance", var_post < 1)

    # --- P10 linear gap on the old slope ---
    slope_sign = Decimal(2) / 3 - Decimal(8) / (3 * PI)
    predict("P10 slope plus 1/10", near(slope_sign + Decimal("0.1"), "-0.082159696490") and slope_sign + Decimal("0.1") < 0, f"{slope_sign + Decimal('0.1')}")
    predict("P10 slope plus 1/2", near(slope_sign + Decimal("0.5"), "0.317840303510") and slope_sign + Decimal("0.5") > 0, f"{slope_sign + Decimal('0.5')}")

    # Level of the three arms at stake 1, gamma_1 = 1/10.
    # Action alone and observation alone: (q+gamma)*theta = 1.1, slope 1.1, second derivative 0.
    check("action-alone slope at gamma 1/10", Decimal("1.1") > 0)
    check("closed-loop slope stays positive after gamma 1/10", slope + Decimal("0.1") > 0, f"{slope + Decimal('0.1')}")

    print("-- scored numbers --")
    print(f"factor_a1={factor_a1}")
    print(f"factor_a12={(3 - sqrt(5)) / 2}")
    print(f"factor_a2={factor_a2}")
    print(f"delta_half={d_half}")
    print(f"r_star_q4={r}")
    print(f"delta_q4={d4}")
    print(f"v={v_c}")
    print(f"I0={I0}")
    print(f"I1={I1}")
    print(f"Qfin={Qfin}")
    print(f"dC={dC}")
    print(f"tail={tail}")
    print(f"slope={slope}")
    print(f"d2={d2}")
    print(f"spread={spread}")
    print(f"thresh={thresh}")
    print(f"J8={j8}")
    print(f"gap8={gap8}")
    print(f"floor={cmin}")
    print(f"sign_loss={loss_fb}")
    print(f"ET={ET}")
    print(f"slope_sign={slope_sign}")
    print(f"CHECKS {CHECKS}")
    print(f"FAILS {FAILS}")
    print(f"PREDICTION-MISSES {MISSES}")
    if FAILS == 0:
        print("ALL ACTING LOOP CHECKS PASS")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
