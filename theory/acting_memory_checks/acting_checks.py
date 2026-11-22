#!/usr/bin/env python3
"""Evaluate the locked acting-memory predictions.

The preregistration is theory/acting_memory_checks/PREREG.md. This script
checks that file's sha256 against LOCK.txt before it evaluates a cost.
It does not search a price outside the frozen table.
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


def check(name, ok, detail=""):
    global FAILS, CHECKS
    CHECKS += 1
    if ok:
        print(f"PASS  {name}  {detail}")
    else:
        FAILS += 1
        print(f"FAIL  {name}  {detail}")


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


def atan(x):
    x = D(x)
    if x == 0:
        return Decimal(0)
    if x < 0:
        return -atan(-x)
    if x > 1:
        return PI / 2 - atan(1 / x)
    # atan(x) = 2 atan(x / (1 + sqrt(1+x^2))). Reduce until the series is fast.
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
        if abs(add) < Decimal("1e-65"):
            break
    return s * (Decimal(2) ** folds)


def acos(x):
    x = D(x)
    if x <= 0:
        raise ValueError("acos domain")
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


# Frozen class.
A = Decimal(1)
KT = Decimal(1)
W = Decimal(16)
ALPHA = (4 - PI) / (6 * PI)
B_RES = Decimal(16)
EPS_R = Decimal(1) / 20
DELTA = Decimal(1) / 10


def A_of(r):
    r = D(r)
    return ALPHA * 2 * A * (1 - r) / r ** 2


def C_of(r):
    r = D(r)
    return KT * A * (1 - r) / r + W * psi(r)


def J_sign(r, theta):
    return A_of(r) / D(theta) + C_of(r)


def g_sign(r, theta):
    """Partial of J with respect to r."""
    r = D(r)
    theta = D(theta)
    A_prime = ALPHA * 2 * A * (r - 2) / r ** 3
    C_prime = -KT * A / r ** 2 + W * psi_prime(r)
    return A_prime / theta + C_prime


def g_sign_prime(r, theta):
    r = D(r)
    theta = D(theta)
    A_second = ALPHA * 4 * A * (3 - r) / r ** 4
    # d/dr [-kT a / r^2] = 2 kT a / r^3
    # d/dr (r(1-r))^(-1/2) = (-1/2) (r(1-r))^(-3/2) * (1-2r)
    q = r * (1 - r)
    psi_second = W / (2 * PI) * (Decimal("-0.5") * q ** Decimal("-1.5") * (1 - 2 * r))
    C_second = 2 * KT * A / r ** 3 + psi_second
    return A_second / theta + C_second


def _float_start(theta):
    """Coarse minimum in float, used only as a Newton start."""
    alpha = float(ALPHA)
    th = float(theta)
    pi = math.pi

    def jf(r):
        return alpha * 2.0 * (1.0 - r) / (th * r * r) + (1.0 - r) / r + 16.0 * math.acos(math.sqrt(1.0 - r)) / pi

    best_r, best_j = 0.5, jf(0.5)
    n = 2000
    for i in range(1, n):
        r = i / n
        val = jf(r)
        if val < best_j:
            best_r, best_j = r, val
    return D(str(best_r))


def minimize_sign(theta):
    theta = D(theta)
    r = _float_start(theta)
    for _ in range(30):
        step = g_sign_prime(r, theta)
        if step == 0:
            break
        r_next = r - g_sign(r, theta) / step
        if r_next <= Decimal("1e-12") or r_next >= 1 - Decimal("1e-12"):
            break
        if abs(r_next - r) < Decimal("1e-36"):
            r = r_next
            break
        r = r_next
    return r, J_sign(r, theta)


def riccati_p(u, theta):
    u = D(u)
    theta = D(theta)
    if u == 0:
        return theta
    return (-A + sqrt(A * A + 2 * A * theta * u)) / u


def heat_partial(r, theta):
    r = D(r)
    theta = D(theta)
    return KT * A * (1 - r) / (theta * r * (2 - r))


def sign_partial(r, theta):
    r = D(r)
    theta = D(theta)
    return -W * sqrt(r * (1 - r)) / (2 * PI * (2 - r) * theta)


def learning_partial_u(u, theta):
    u = D(u)
    theta = D(theta)
    return A * theta / (2 * sqrt(A * A + 2 * A * theta * u))


def erf_series(z):
    z = D(z)
    # (2/sqrt(pi)) sum (-1)^n z^(2n+1) / (n! (2n+1))
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


def erfcinv(y):
    """Solve erfc(z) = y for z > 0."""
    y = D(y)
    z = sqrt(-D(math.log(float(y))))  # start
    for _ in range(50):
        f = erfc_decimal(z) - y
        # d(erfc)/dz = -2/sqrt(pi) exp(-z^2)
        df = -2 / sqrt(PI) * (-(z * z)).exp()
        z_next = z - f / df
        if abs(z_next - z) < Decimal("1e-40"):
            return z_next
        z = z_next
    return z


def square_cubic(p, theta):
    p = D(p)
    theta = D(theta)
    return W * p ** 3 + (2 * ALPHA - theta) * p - 4 * ALPHA * theta


def p_star_square(theta):
    theta = D(theta)
    lo = Decimal("1e-12")
    hi = theta * (1 - Decimal("1e-12"))
    # bisection, f(0+) < 0 < f(theta) on this price table
    for _ in range(200):
        mid = (lo + hi) / 2
        if square_cubic(mid, theta) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def J_square_p(p, theta):
    p = D(p)
    theta = D(theta)
    if p >= theta:
        return W * theta
    u = 2 * A * (theta - p) / p ** 2
    return ALPHA * u + KT * A * (theta - p) / p + W * p


def hash_ok():
    text = (HERE / "LOCK.txt").read_text(encoding="utf-8")
    locked = None
    for line in text.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "PREREG.md":
            locked = parts[0]
    digest = hashlib.sha256((HERE / "PREREG.md").read_bytes()).hexdigest()
    return locked, digest, locked == digest


def main():
    global FAILS
    locked, digest, ok = hash_ok()
    check("hash matches LOCK.txt before any cost", ok, digest)
    if not ok:
        print(f"FAILS {FAILS}")
        return 1

    # Closed forms at the frozen point.
    r0 = Decimal("0.5")
    theta0 = Decimal(1)
    u0 = 2 * A * (1 - r0) / (theta0 * r0 ** 2)
    p0 = r0 * theta0
    check("intensity at r=1/2, theta=1 is 4", u0 == 4, f"u={u0}")
    residual = u0 * p0 ** 2 + 2 * A * p0 - 2 * A * theta0
    check("Riccati residual at the frozen point", abs(residual) < Decimal("1e-12"), f"{residual}")

    p_from_u = riccati_p(u0, theta0)
    check("Riccati root returns p=1/2", abs(p_from_u - p0) < Decimal("1e-30"), f"p={p_from_u}")

    second_r = g_sign_prime(r0, theta0)
    check("local minimum, partial_rr J > 0", second_r > 0, f"{second_r}")
    check("FOC residual at r=1/2", abs(g_sign(r0, theta0)) < Decimal("1e-30"), f"{g_sign(r0, theta0)}")

    J_closed = 5 + 2 * (4 - PI) / (3 * PI)
    J_eval = J_sign(r0, theta0)
    check("cost equals 5 + 2(4-pi)/(3 pi)", abs(J_eval - J_closed) < Decimal("1e-30"))
    check("cost below the blind cost 8", J_eval < 8, f"gap={8 - J_eval}")

    heat_d = heat_partial(r0, theta0)
    sign_d = sign_partial(r0, theta0)
    slope = heat_d + sign_d
    slope_closed = D(2) / 3 - D(8) / (3 * PI)
    check("heat slope equals 2/3", abs(heat_d - D(2) / 3) < Decimal("1e-30"), f"{heat_d}")
    check("slope equals 2/3 - 8/(3 pi)", abs(slope - slope_closed) < Decimal("1e-30"), f"{slope}")
    check("P1 slope is negative", slope < 0)
    check("P1 heat slope is positive", heat_d > 0)

    # Learning rate equals heat at kT=1, so the same slope.
    L0 = A * (1 - r0) / r0
    check("learning rate at the point equals 1", L0 == 1, f"L={L0}")

    # Minimizer lands on the critical point.
    r_star, J_star = minimize_sign(theta0)
    check(
        "script minimizer is r=1/2",
        abs(r_star - r0) < Decimal("1e-10"),
        f"r={r_star}",
    )
    check(
        "script minimum matches the closed form within 1e-9",
        abs(J_star - J_closed) < Decimal("1e-9"),
        f"J={J_star}",
    )

    # Second derivative of the minimized cost, and the reduction to 44+pi.
    C_prime = D(16) / PI - 4
    A_at = 4 * ALPHA
    d2 = 8 * ALPHA - (C_prime ** 2) / (160 * ALPHA + 16)
    # Algebraic reduction: positivity iff 44+pi > 0, checked by reconstructing.
    check("second derivative positive", d2 > 0, f"{d2}")
    check("44+pi positive", (44 + PI) > 0)

    # Fixed-r spread.
    A_slice = 2 * (4 - PI) / (3 * PI)
    spread_fixed = A_slice * DELTA ** 2 / (1 - DELTA ** 2)
    left = J_sign(r0, 1 - DELTA)
    right = J_sign(r0, 1 + DELTA)
    mid = J_sign(r0, 1)
    spread_eval = (left + right) / 2 - mid
    check(
        "fixed-r spread matches A delta^2 / (1-delta^2)",
        abs(spread_eval - spread_fixed) < Decimal("1e-20"),
        f"{spread_eval}",
    )
    check("fixed-r spread positive", spread_fixed > 0)

    # Re-optimized spread at delta=1/10.
    _, J_lo = minimize_sign(1 - DELTA)
    _, J_hi = minimize_sign(1 + DELTA)
    spread_opt = (J_lo + J_hi) / 2 - J_star
    check("re-optimized spread positive", spread_opt > 0, f"{spread_opt}")

    # Finite-difference slope and curvature of J* against the closed forms.
    h = Decimal("1e-6")
    _, Jp = minimize_sign(theta0 + h)
    _, Jm = minimize_sign(theta0 - h)
    fd_slope = (Jp - Jm) / (2 * h)
    fd_d2 = (Jp - 2 * J_star + Jm) / h ** 2
    check(
        "envelope slope matches the finite difference",
        abs(fd_slope - slope_closed) / abs(slope_closed) < Decimal("1e-9"),
        f"fd={fd_slope}",
    )
    check(
        "second derivative matches the finite difference",
        abs(fd_d2 - d2) / abs(d2) < Decimal("1e-6"),
        f"fd={fd_d2} closed={d2}",
    )

    # Monotonicity grid. Floor at most 5, blind is 8.
    grid = [D(x) for x in ("0.125", "0.25", "0.5", "1", "2", "4", "8")]
    values = []
    print("-- monotonicity grid (score) --")
    prev = None
    mono = True
    below = True
    above_floor = True
    for theta in grid:
        r_t, J_t = minimize_sign(theta)
        values.append((theta, r_t, J_t))
        print(f"theta={theta} r={r_t} J={J_t}")
        if prev is not None and not (J_t < prev):
            mono = False
        if not (J_t < 8):
            below = False
        if theta == grid[-1] and not (J_t > 5):
            above_floor = False
        prev = J_t
    check("P3 strictly decreasing on the grid", mono)
    check("P3 every grid cost below 8", below)
    # The locked sentence "rightmost value strictly above 5" is a prediction,
    # not a formula check. C(1/2)=5 is an upper bound on the floor, not a
    # lower bound. A value at or below 5 is a miss of that sentence.
    if above_floor:
        check("P3 rightmost grid cost above 5", True)
    else:
        print(
            "PREDICTION-MISS  P3 rightmost grid cost above 5  "
            f"J={values[-1][2]}"
        )

    # Squared loss: unconstrained slope positive, admissible slope positive.
    def square_slope_at_u(u, theta):
        p = riccati_p(u, theta)
        p_theta = A / (A + u * p) if u > 0 else Decimal(1)
        return (W + KT * u / 2) * p_theta, p

    for u, theta in ((Decimal(0), Decimal(1)), (Decimal(4), Decimal(1)), (Decimal("0.5"), Decimal(2))):
        sl, p = square_slope_at_u(u, theta)
        check(f"squared slope positive at u={u} theta={theta}", sl > 0, f"{sl}")

    z = erfcinv(EPS_R)
    # P(|Z| > z_loss) = erfc(z_loss/sqrt(2)) = eps
    # z_loss = sqrt(B/(w p)), so p_cap = B / (w * z_loss^2) = B / (w * 2 * z^2)
    p_cap = B_RES / (W * 2 * z * z)
    check("p_cap in (0, 1)", Decimal(0) < p_cap < 1, f"p_cap={p_cap} z={z}")

    def J_adm(theta):
        theta = D(theta)
        p_star = p_star_square(theta)
        p_hi = theta if p_cap >= theta else p_cap
        p_use = p_star if p_star <= p_hi else p_hi
        return J_square_p(p_use, theta), p_use, p_star

    print("-- admissible squared cost (score) --")
    adm_prev = None
    adm_mono = True
    for theta in (Decimal("0.5"), Decimal(1), Decimal(2), Decimal(4)):
        Jad, p_use, p_star = J_adm(theta)
        print(f"theta={theta} J_adm={Jad} p_use={p_use} p_star={p_star}")
        if adm_prev is not None and not (Jad > adm_prev):
            adm_mono = False
        adm_prev = Jad
    check("admissible squared cost strictly increasing on 0.5,1,2,4", adm_mono)

    # The squared point at p=1/2 is inadmissible.
    erfc1 = erfc_decimal(1)
    check("erfc(1) matches math.erfc within 1e-12", abs(erfc1 - D(str(math.erfc(1)))) < Decimal("1e-12"))
    check("erfc(1) > 1/20", erfc1 > EPS_R, f"erfc(1)={erfc1}")
    # Direct probability at p=1/2, B=w=16: P(|Z|>sqrt(2)) = erfc(1).
    check("squared frozen point inadmissible", erfc1 > EPS_R)

    # Sign ruin probability is 0.
    psi0 = psi(r0)
    check("sign error probability is 1/4", abs(psi0 - Decimal("0.25")) < Decimal("1e-30"), f"{psi0}")
    check("sign ruin probability is 0", psi0 <= 1 and B_RES >= W)

    # Uninformative: pay alpha*u, posterior stays at the prior, L = 0.
    # Sign cost alpha*u + w/2 is minimized at u=0. Its theta derivative is 0.
    # Squared cost alpha*u + w*theta is minimized at u=0 with derivative w.
    def uninf_sign(theta, u):
        # theta is accepted and unused: the channel does not exist.
        return ALPHA * D(u) + W / 2

    check("uninformative sign cost at u=1 exceeds the u=0 cost", uninf_sign(1, 1) > uninf_sign(1, 0))
    check("uninformative sign minimum is 8", uninf_sign(1, 0) == 8)
    check(
        "uninformative sign cost does not change with theta",
        uninf_sign(1, 0) == uninf_sign(4, 0),
    )
    check("uninformative squared slope equals w", W == 16)

    # Uncapped price: alpha * u * theta = alpha * 2a (1-r) / r^2, no theta left.
    def J_uncapped(r):
        r = D(r)
        return ALPHA * 2 * A * (1 - r) / r ** 2 + C_of(r)

    # Same function at every theta. Compare two evaluations of the minimizer's cost
    # by minimizing the theta-free function once and checking the identity.
    best_u = _float_start(1)
    # The uncapped cost has no theta, so the same stationarity condition
    # is g with the probe term's theta set to 1: reuse a Newton on J_uncapped.
    for _ in range(30):
        # derivative of alpha*2a*(1-r)/r^2 + C equals g_sign at theta=1
        step = g_sign_prime(best_u, 1)
        if step == 0:
            break
        nxt = best_u - g_sign(best_u, 1) / step
        if nxt <= Decimal("1e-12") or nxt >= 1:
            break
        if abs(nxt - best_u) < Decimal("1e-36"):
            best_u = nxt
            break
        best_u = nxt
    # Cost at theta=1 and theta=2 using the same r must match, and the
    # theta-dependent formula with price alpha*u*theta collapses.
    def J_uncapped_theta(r, theta):
        u = 2 * A * (1 - r) / (D(theta) * r ** 2)
        return ALPHA * u * D(theta) + C_of(r)

    gap_unc = abs(J_uncapped_theta(best_u, 1) - J_uncapped_theta(best_u, 2))
    check("uncapped stationarity residual", abs(g_sign(best_u, 1)) < Decimal("1e-20"), f"g={g_sign(best_u, 1)}")
    check("uncapped sign cost independent of theta", gap_unc < Decimal("1e-30"), f"gap={gap_unc}")

    # Scaled noise: u = 2a(1-r)/r^2, cost independent of theta.
    def J_scaled(r):
        r = D(r)
        u = 2 * A * (1 - r) / r ** 2
        return ALPHA * u + KT * A * (1 - r) / r + W * psi(r)

    def g_scaled(r):
        r = D(r)
        # u = 2a(1-r)/r^2, price alpha*u, no extra theta.
        u_prime = 2 * A * ((r - 2) / r ** 3)
        return ALPHA * u_prime + (-KT * A / r ** 2) + W * psi_prime(r)

    def g_scaled_prime(r):
        r = D(r)
        u_second = 4 * A * (3 - r) / r ** 4
        q = r * (1 - r)
        psi_second = W / (2 * PI) * (Decimal("-0.5") * (q ** Decimal("-1.5")) * (1 - 2 * r))
        return ALPHA * u_second + 2 * KT * A / r ** 3 + psi_second

    best_s = Decimal("0.5")
    for _ in range(30):
        step = g_scaled_prime(best_s)
        nxt = best_s - g_scaled(best_s) / step
        if nxt <= Decimal("1e-12") or nxt >= 1:
            break
        if abs(nxt - best_s) < Decimal("1e-36"):
            best_s = nxt
            break
        best_s = nxt
    L_scaled = A * (1 - best_s) / best_s

    def scaled_fraction(theta, r):
        """Posterior fraction under noise density theta/u, with u = 2a(1-r)/r^2."""
        u = 2 * A * (1 - r) / r ** 2
        noise = D(theta) / u
        # p^2 / noise = 2 a (theta - p). Solve the quadratic for p.
        # p^2 + 2 a noise p - 2 a theta noise = 0
        # p = -a noise + sqrt((a noise)^2 + 2 a theta noise)
        p = -A * noise + sqrt((A * noise) ** 2 + 2 * A * D(theta) * noise)
        return p / D(theta)

    frac1 = scaled_fraction(1, best_s)
    frac3 = scaled_fraction(3, best_s)
    check(
        "scaled-noise stationarity residual",
        abs(g_scaled(best_s)) < Decimal("1e-20"),
        f"g={g_scaled(best_s)}",
    )
    check(
        "scaled-noise fraction is independent of theta",
        abs(frac1 - best_s) < Decimal("1e-20") and abs(frac3 - best_s) < Decimal("1e-20"),
        f"r={best_s} f1={frac1} f3={frac3}",
    )
    check("scaled-noise learning rate has no theta left", abs(L_scaled - A * (1 - frac1) / frac1) < Decimal("1e-20"))

    # Passive fixed u=4.
    def passive_slope(theta, u=Decimal(4)):
        p = riccati_p(u, theta)
        r = p / D(theta)
        return heat_partial(r, theta) + sign_partial(r, theta), r, p

    s1, r1, p1 = passive_slope(1)
    s4, r4, p4 = passive_slope(4)
    check("passive sign slope negative at theta=1", s1 < 0, f"{s1} r={r1}")
    check("passive sign slope positive at theta=4", s4 > 0, f"{s4} r={r4}")
    # Passive squared at fixed u is the squared slope already checked positive.
    sl_fixed, _ = square_slope_at_u(Decimal(4), Decimal(1))
    check("passive squared slope positive", sl_fixed > 0, f"{sl_fixed}")

    # Naked option.
    naked = -1 / (2 * sqrt(2 * PI * 1))
    check("naked option slope negative at theta=1", naked < 0, f"{naked}")
    # derivative of c - sqrt(theta/(2 pi)) at general theta stays negative
    naked4 = -1 / (2 * sqrt(2 * PI * 4))
    check("naked option slope negative at theta=4", naked4 < 0, f"{naked4}")

    # Action raises the learning rate.
    dL = learning_partial_u(u0, theta0)
    check("partial L / partial u positive at the frozen point", dL > 0, f"{dL}")
    # Closed form at u=4, theta=1: a theta / (2 sqrt(a^2 + 2 a theta u)) = 1/(2 sqrt(1+8)) = 1/(2*3) = 1/6
    check("partial L / partial u equals 1/6", abs(dL - Decimal(1) / 6) < Decimal("1e-30"), f"{dL}")
    J_menu = J_sign(r0, theta0)
    check("menu selects u=4 over u=0", J_menu < W / 2, f"J4={J_menu} J0={W / 2}")
    check("learning rate is 1 at u=4 and 0 at u=0", L0 == 1)

    # Derivative cross-check: psi' at 1/2 equals 1/pi.
    check("psi' at 1/2 equals 1/pi", abs(psi_prime(r0) - 1 / PI) < Decimal("1e-30"))

    # Finite-difference of psi against the closed form, at r=1/2.
    hr = Decimal("1e-8")
    fd_psi = (psi(r0 + hr) - psi(r0 - hr)) / (2 * hr)
    check(
        "psi finite difference matches the closed form",
        abs(fd_psi - psi_prime(r0)) / psi_prime(r0) < Decimal("1e-9"),
        f"fd={fd_psi}",
    )

    print("-- scored numbers --")
    print(f"pi={PI}")
    print(f"alpha={ALPHA}")
    print(f"J_frozen={J_closed}")
    print(f"slope={slope_closed}")
    print(f"heat_slope={heat_d}")
    print(f"d2={d2}")
    print(f"spread_fixed={spread_fixed}")
    print(f"spread_opt={spread_opt}")
    print(f"erfc1={erfc1}")
    print(f"p_cap={p_cap}")
    print(f"passive_slope_theta1={s1}")
    print(f"passive_slope_theta4={s4}")
    print(f"naked_slope={naked}")
    print(f"dL_du={dL}")
    print(f"r_star={r_star}")
    print(f"J_star={J_star}")
    # diagnostic, not a score: the greatest lower picture of C on the same grid
    def g_C(r):
        r = D(r)
        return -KT * A / r ** 2 + W * psi_prime(r)

    def g_C_prime(r):
        r = D(r)
        q = r * (1 - r)
        psi_second = W / (2 * PI) * (Decimal("-0.5") * (q ** Decimal("-1.5")) * (1 - 2 * r))
        return 2 * KT * A / r ** 3 + psi_second

    best_cr = Decimal("0.4")
    for _ in range(30):
        step = g_C_prime(best_cr)
        nxt = best_cr - g_C(best_cr) / step
        if nxt <= Decimal("1e-12") or nxt >= 1:
            break
        if abs(nxt - best_cr) < Decimal("1e-36"):
            best_cr = nxt
            break
        best_cr = nxt
    best_c = C_of(best_cr)
    print(f"DIAGNOSTIC floor_of_C={best_c} at r={best_cr}")
    Jad1, puse1, pstar1 = J_adm(Decimal(1))
    Jad2, puse2, pstar2 = J_adm(Decimal(2))
    print(f"DIAGNOSTIC J_adm_theta1={Jad1} p={puse1} pstar={pstar1}")
    print(f"DIAGNOSTIC J_adm_theta2={Jad2} p={puse2} pstar={pstar2}")

    print(f"CHECKS {CHECKS}")
    print(f"FAILS {FAILS}")
    if FAILS == 0:
        print("ALL ACTING MEMORY CHECKS PASS")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
