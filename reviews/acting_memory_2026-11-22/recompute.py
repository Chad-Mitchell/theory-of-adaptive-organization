#!/usr/bin/env python3
"""Independent recomputation of the acting-memory load-bearing numbers.

This file does not import theory/acting_memory_checks/acting_checks.py.
The cost is the one defined in theory/ACTING_MEMORY_2026-11-22.md and
theory/acting_memory_checks/PREREG.md. Pi is the Brent-Salamin AGM,
checked against 4*atan(1). Arccos is an arctan series. The Gaussian
tail is the erf series, checked against mpmath. Minima are checked two
ways, a derivative-free golden search and a bisection of the derivative.
"""

from decimal import Decimal, getcontext, ROUND_HALF_EVEN
import sys

import mpmath as mp

getcontext().prec = 80
getcontext().rounding = ROUND_HALF_EVEN

ZERO = Decimal(0)
ONE = Decimal(1)
TWO = Decimal(2)
EPS = Decimal(10) ** (-70)


def sqrt(x):
    return x.sqrt()


def exp(x):
    return x.exp()


def ln(x):
    return x.ln()


def pi_agm():
    """Brent-Salamin quadratic algorithm."""
    a = ONE
    b = ONE / sqrt(TWO)
    t = Decimal("0.25")
    p = ONE
    for _ in range(12):
        a_next = (a + b) / TWO
        b_next = sqrt(a * b)
        t = t - p * (a - a_next) ** 2
        a, b, p = a_next, b_next, TWO * p
    return (a + b) ** 2 / (4 * t)


def atan_small(x):
    """atan series for |x| <= 1."""
    x2 = x * x
    term = x
    total = x
    n = 1
    while True:
        term *= -x2
        add = term / (2 * n + 1)
        total += add
        n += 1
        if add.copy_abs() < EPS:
            return total


def atan(x):
    if x < 0:
        return -atan(-x)
    if x == 0:
        return ZERO
    if x > 1:
        return PI / TWO - atan(ONE / x)
    # Half-angle reduction keeps the series argument at most 1/2,
    # so the Leibniz endpoint x=1 is never summed directly.
    if x > Decimal("0.5"):
        return TWO * atan(x / (ONE + sqrt(ONE + x * x)))
    return atan_small(x)


def acos(x):
    if x == 0:
        return PI / TWO
    if x == 1:
        return ZERO
    if x == -1:
        return PI
    return atan(sqrt(ONE - x * x) / x)


PI = pi_agm()
PI_ATAN = 4 * atan(ONE)

# Frozen point from the preregistration, section 3.
A_REVERT = ONE
KT = ONE
W = Decimal(16)
ALPHA = (4 - PI) / (6 * PI)
B_RESERVE = Decimal(16)
EPS_R = ONE / Decimal(20)
DELTA = ONE / Decimal(10)
U_FIXED = Decimal(4)


def psi(r):
    return acos(sqrt(ONE - r)) / PI


def psi_prime(r):
    return ONE / (TWO * PI * sqrt(r * (ONE - r)))


def psi_second(r):
    q = r * (ONE - r)
    return -(ONE - TWO * r) / (4 * PI * q * sqrt(q))


def A_of(r):
    """Probe price of holding the fraction r. alpha * 2 a (1-r) / r^2."""
    return ALPHA * TWO * A_REVERT * (ONE - r) / (r * r)


def A_prime(r):
    return TWO * ALPHA * (r - TWO) / (r ** 3)


def A_second(r):
    return 4 * ALPHA * (3 - r) / (r ** 4)


def heat(r):
    return KT * A_REVERT * (ONE - r) / r


def heat_prime(r):
    return -KT * A_REVERT / (r * r)


def heat_second(r):
    return TWO * KT * A_REVERT / (r ** 3)


def sign_loss(r):
    return W * psi(r)


def C_of(r):
    return heat(r) + sign_loss(r)


def C_prime(r):
    return heat_prime(r) + W * psi_prime(r)


def C_second(r):
    return heat_second(r) + W * psi_second(r)


def J_sign(r, theta):
    return A_of(r) / theta + C_of(r)


def J_r(r, theta):
    return A_prime(r) / theta + C_prime(r)


def J_rr(r, theta):
    return A_second(r) / theta + C_second(r)


def golden_min(f, lo, hi):
    """Derivative-free minimum. Interval shrinks by the golden ratio."""
    invphi = (sqrt(Decimal(5)) - ONE) / TWO
    invphi2 = invphi * invphi
    a, b = lo, hi
    h = b - a
    c = a + invphi2 * h
    d = a + invphi * h
    yc, yd = f(c), f(d)
    while h > EPS:
        if yc < yd:
            b = d
            d = c
            yd = yc
            h = invphi * h
            c = a + invphi2 * h
            yc = f(c)
        else:
            a = c
            c = d
            yc = yd
            h = invphi * h
            d = a + invphi * h
            yd = f(d)
    r = (a + b) / TWO
    return r, f(r)


def bisect_min(theta, lo=Decimal("1e-6"), hi=Decimal("1") - Decimal("1e-8")):
    """The unique root of dJ/dr, which is the minimizer when the slope
    changes from negative to positive."""
    glo = J_r(lo, theta)
    ghi = J_r(hi, theta)
    if not (glo < 0 < ghi):
        raise RuntimeError(f"derivative does not change - to + on ({lo},{hi}) at theta={theta}: {glo}, {ghi}")
    for _ in range(300):
        mid = (lo + hi) / TWO
        gm = J_r(mid, theta)
        if gm < 0:
            lo, glo = mid, gm
        else:
            hi, ghi = mid, gm
    r = (lo + hi) / TWO
    return r, J_sign(r, theta)


def minimize_sign(theta, agree=False):
    r_b, j_b = bisect_min(theta)
    if J_rr(r_b, theta) <= 0:
        raise RuntimeError(f"not a local minimum at theta={theta}")
    if agree:
        r_g, j_g = golden_min(lambda r: J_sign(r, theta), Decimal("0.02"), Decimal("0.98"))
        if (r_b - r_g).copy_abs() > Decimal("1e-30") or (j_b - j_g).copy_abs() > Decimal("1e-30"):
            raise RuntimeError(f"minimizers disagree at theta={theta}: {r_b} vs {r_g}")
    return r_b, j_b


def r_prime(r, theta):
    """dr*/d theta from differentiating the first-order condition."""
    return A_prime(r) / (theta * (A_second(r) + theta * C_second(r)))


def along_path(theta):
    r, _ = minimize_sign(theta)
    rp = r_prime(r, theta)
    probe = (A_prime(r) * rp * theta - A_of(r)) / (theta * theta)
    heat_s = heat_prime(r) * rp
    sign_s = W * psi_prime(r) * rp
    return probe, heat_s, sign_s, r


def fd_along_path(theta, h=Decimal("1e-18")):
    """Central differences of the three pieces, Richardson on two steps."""

    def piece(th):
        r, _ = bisect_min(th)
        return A_of(r) / th, heat(r), sign_loss(r), J_sign(r, th)

    def deriv(step):
        p_hi, h_hi, s_hi, j_hi = piece(theta + step)
        p_lo, h_lo, s_lo, j_lo = piece(theta - step)
        return (
            (p_hi - p_lo) / (TWO * step),
            (h_hi - h_lo) / (TWO * step),
            (s_hi - s_lo) / (TWO * step),
            (j_hi - j_lo) / (TWO * step),
        )

    d1 = deriv(h)
    d2 = deriv(TWO * h)

    def rich(i):
        return (4 * d1[i] - d2[i]) / 3

    return rich(0), rich(1), rich(2), rich(3)


def second_derivative(theta, h=Decimal("1e-12")):
    def jstar(th):
        return bisect_min(th)[1]

    def raw(step):
        return (jstar(theta + step) - TWO * jstar(theta) + jstar(theta - step)) / (step * step)

    s1, s2 = raw(h), raw(TWO * h)
    return (4 * s1 - s2) / 3


def closed_second_at_one():
    c_prime = Decimal(16) / PI - 4
    return 8 * ALPHA - (c_prime ** 2) / (160 * ALPHA + 16)


def spread_reoptimized(theta, delta):
    j_lo = minimize_sign(theta * (ONE - delta), agree=True)[1]
    j_hi = minimize_sign(theta * (ONE + delta), agree=True)[1]
    j_mid = minimize_sign(theta, agree=True)[1]
    return (j_lo + j_hi) / TWO - j_mid


def erf_series(z):
    """erf from its power series. Accurate for the arguments used here."""
    if z < 0:
        return -erf_series(-z)
    z2 = z * z
    n = 0
    term = z
    total = z
    while True:
        term *= -z2 * (2 * n + 1) / ((n + 1) * (2 * n + 3))
        total += term
        n += 1
        if term.copy_abs() < EPS:
            break
    return TWO / sqrt(PI) * total


def erfc_series(z):
    return ONE - erf_series(z)


def erfc_mpmath(z):
    """Library cross-check. The reported digits come from erf_series."""
    mp.mp.dps = 50
    return Decimal(mp.nstr(mp.erfc(mp.mpf(str(z))), 45, strip_zeros=False))


def erfcinv_newton(y, erfc_fn):
    z = ONE
    for _ in range(40):
        f = erfc_fn(z) - y
        df = -TWO / sqrt(PI) * exp(-z * z)
        step = f / df
        z -= step
        if step.copy_abs() < EPS:
            return z
    return z


def phi_inv(p, erfc_fn):
    """Solve Phi(x) = p by Newton, with Phi built from erfc_fn."""

    def phi(x):
        return ONE - erfc_fn(x / sqrt(TWO)) / TWO

    x = Decimal(2)
    for _ in range(40):
        f = phi(x) - p
        # density
        dens = exp(-x * x / TWO) / sqrt(TWO * PI)
        step = f / dens
        x -= step
        if step.copy_abs() < EPS:
            return x
    return x


def riccati_p(u, theta):
    return (-A_REVERT + sqrt(A_REVERT ** 2 + TWO * A_REVERT * theta * u)) / u


def learning_rate(u, theta):
    return (-A_REVERT + sqrt(A_REVERT ** 2 + TWO * A_REVERT * theta * u)) / TWO


def J_fixed_u(theta, u):
    p = riccati_p(u, theta)
    r = p / theta
    return ALPHA * u + KT * learning_rate(u, theta) + W * psi(r), r, learning_rate(u, theta)


def fixed_u_slope(theta, u, h=Decimal("1e-16")):
    def raw(step):
        jp, _, _ = J_fixed_u(theta + step, u)
        jm, _, _ = J_fixed_u(theta - step, u)
        return (jp - jm) / (TWO * step)

    return (4 * raw(h) - raw(TWO * h)) / 3


def square_cost_p(p, theta):
    """Mean-square cost at posterior variance p. u = 2a (theta-p) / p^2."""
    if p == theta:
        return W * theta
    u = TWO * A_REVERT * (theta - p) / (p * p)
    ell = A_REVERT * (theta / p - ONE)
    return ALPHA * u + KT * ell + W * p


def square_dcost(p, theta):
    return -4 * ALPHA * theta / (p ** 3) + (TWO * ALPHA - theta) / (p * p) + W


def minimize_square(theta, p_cap):
    hi = theta if p_cap >= theta else p_cap
    lo = Decimal("1e-6")
    # Interior critical point of the unconstrained cost, by bisection on (0, theta).
    # dJ/dp is -infinity at 0 and positive for large p, so one root.
    left, right = lo, theta - Decimal("1e-12")
    if square_dcost(left, theta) >= 0:
        p_star = left
    else:
        for _ in range(300):
            mid = (left + right) / TWO
            if square_dcost(mid, theta) < 0:
                left = mid
            else:
                right = mid
        p_star = (left + right) / TWO
    p_use = p_star if p_star <= hi else hi
    # Derivative-free check on the same closed admissible interval.
    r_g, j_g = golden_min(lambda p: square_cost_p(p, theta), lo, hi)
    j_use = square_cost_p(p_use, theta)
    if (j_use - j_g).copy_abs() > Decimal("1e-20"):
        raise RuntimeError(f"squared minimizers disagree at theta={theta}: {j_use} vs {j_g}")
    return p_use, j_use, p_star


def minimize_C():
    return golden_min(C_of, Decimal("0.05"), Decimal("0.9"))


def crossing_of_five():
    """Solve J*(theta) = 5. J* decreases from 8 to inf C < 5."""
    lo, hi = Decimal(7), Decimal(8)
    for _ in range(250):
        mid = (lo + hi) / TWO
        if bisect_min(mid)[1] > 5:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / TWO


def q10(x):
    return x.quantize(Decimal("1e-10"), rounding=ROUND_HALF_EVEN)


def fmt(x, places=18):
    q = Decimal(10) ** (-places)
    return format(x.quantize(q, rounding=ROUND_HALF_EVEN), "f")


def compare(name, got, claimed):
    claimed_d = Decimal(claimed)
    diff = got - claimed_d
    ok = diff.copy_abs() <= Decimal("5e-13")
    status = "MATCH" if ok else "DIFFER"
    print(f"{status}  {name}")
    print(f"    recomputed {fmt(got)}")
    print(f"    note       {claimed}")
    print(f"    difference {fmt(diff, 20)}")
    return ok


def main():
    print("pi_agm ", fmt(PI, 40))
    print("pi_atan", fmt(PI_ATAN, 40))
    if (PI - PI_ATAN).copy_abs() > Decimal("1e-60"):
        raise SystemExit("pi algorithms disagree")
    known_pi = Decimal("3.1415926535897932384626433832795028841971")
    if (PI - known_pi).copy_abs() > Decimal("1e-40"):
        raise SystemExit("pi does not match the known expansion")

    half = Decimal("0.5")
    psi_half = psi(half)
    print("psi(1/2) - 1/4", fmt(psi_half - Decimal("0.25"), 40))
    if (psi_half - Decimal("0.25")).copy_abs() > Decimal("1e-60"):
        raise SystemExit("psi(1/2) is not 1/4")

    # Closed form at the critical point, and the numerical minimizer.
    closed = 5 + TWO * (4 - PI) / (3 * PI)
    slope_closed = -A_of(half)
    slope_fixed_formula = TWO / 3 - 8 / (3 * PI)
    print("closed J        ", fmt(closed, 30))
    print("J via psi       ", fmt(J_sign(half, ONE), 30))
    print("slope -A        ", fmt(slope_closed, 30))
    print("slope 2/3-8/3pi ", fmt(slope_fixed_formula, 30))
    if (closed - J_sign(half, ONE)).copy_abs() > Decimal("1e-50"):
        raise SystemExit("closed cost and psi cost disagree")
    if (slope_closed - slope_fixed_formula).copy_abs() > Decimal("1e-50"):
        raise SystemExit("envelope slope and fixed-intensity formula disagree")

    r_star, j_star = minimize_sign(ONE, agree=True)
    print("minimizer at theta=1", fmt(r_star, 30), fmt(j_star, 30))
    if (r_star - half).copy_abs() > Decimal("1e-30"):
        raise SystemExit("minimizer at theta=1 is not 1/2")

    probe, heat_s, sign_s, _ = along_path(ONE)
    fd_p, fd_h, fd_s, fd_j = fd_along_path(ONE)
    print("analytic split", fmt(probe), fmt(heat_s), fmt(sign_s), fmt(probe + heat_s + sign_s))
    print("finite-diff   ", fmt(fd_p), fmt(fd_h), fmt(fd_s), fmt(fd_j))
    for a, b in ((probe, fd_p), (heat_s, fd_h), (sign_s, fd_s)):
        if (a - b).copy_abs() > Decimal("1e-20"):
            raise SystemExit("along-path analytic and finite difference disagree")

    d2_fd = second_derivative(ONE)
    d2_closed = closed_second_at_one()
    print("second fd    ", fmt(d2_fd, 30))
    print("second closed", fmt(d2_closed, 30))
    if (d2_fd - d2_closed).copy_abs() > Decimal("1e-16"):
        raise SystemExit("second derivative methods disagree")
    # Algebraic sign: (4-pi)(44+pi) / (6 pi (10-pi)).
    sign_poly = (4 - PI) * (44 + PI)
    print("sign polynomial 44+pi factor", fmt(sign_poly, 20))

    spread = spread_reoptimized(ONE, DELTA)
    a_slice = A_of(half)
    spread_fixed = a_slice * DELTA ** 2 / (ONE - DELTA ** 2)
    spread_fixed_direct = (
        J_sign(half, ONE - DELTA) + J_sign(half, ONE + DELTA)
    ) / TWO - J_sign(half, ONE)
    print("spread reopt ", fmt(spread, 30))
    print("spread fixed ", fmt(spread_fixed, 30), fmt(spread_fixed_direct, 30))

    print("-- grid --")
    grid = []
    prev = None
    for text in ("0.125", "0.25", "0.5", "1", "2", "4", "8"):
        theta = Decimal(text)
        r_t, j_t = minimize_sign(theta, agree=True)
        grid.append((theta, r_t, j_t))
        print(f"theta={text} r={fmt(r_t)} J={fmt(j_t)}")
        if prev is not None and not (j_t < prev):
            raise SystemExit("grid is not strictly decreasing")
        if not (j_t < 8):
            raise SystemExit("grid value is not below 8")
        prev = j_t

    erfc1_series = erfc_series(ONE)
    erfc1_lib = erfc_mpmath(ONE)
    print("erfc series", fmt(erfc1_series, 30))
    print("erfc mpmath", fmt(erfc1_lib, 30))
    if (erfc1_series - erfc1_lib).copy_abs() > Decimal("1e-30"):
        raise SystemExit("erfc series and mpmath disagree")

    z_series = erfcinv_newton(EPS_R, erfc_series)
    phi_series = phi_inv(Decimal("0.975"), erfc_series)
    phi_from_z = sqrt(TWO) * z_series
    mp.mp.dps = 50
    phi_lib = Decimal(mp.nstr(mp.sqrt(2) * mp.erfinv(mp.mpf("0.95")), 45, strip_zeros=False))
    print("erfcinv series", fmt(z_series, 30))
    print("Phi^{-1}      ", fmt(phi_series, 30))
    print("sqrt(2)*z     ", fmt(phi_from_z, 30))
    print("Phi mpmath    ", fmt(phi_lib, 30))
    if (phi_series - phi_from_z).copy_abs() > Decimal("1e-25"):
        raise SystemExit("normal inverse and erfcinv disagree")
    if (phi_series - phi_lib).copy_abs() > Decimal("1e-25"):
        raise SystemExit("normal inverse and mpmath disagree")

    p_cap = B_RESERVE / (W * phi_series ** 2)
    p_cap_erfc = B_RESERVE / (W * TWO * z_series ** 2)
    print("p_cap", fmt(p_cap, 30), fmt(p_cap_erfc, 30))
    if (p_cap - p_cap_erfc).copy_abs() > Decimal("1e-20"):
        raise SystemExit("p_cap routes disagree")

    print("-- admissible squared --")
    square_values = []
    for text in ("0.5", "1", "2", "4"):
        theta = Decimal(text)
        p_use, j_use, p_star = minimize_square(theta, p_cap)
        square_values.append(j_use)
        print(f"theta={text} p_used={fmt(p_use)} p_unconst={fmt(p_star)} J={fmt(j_use)}")

    j_u, r_u, l_u = J_fixed_u(Decimal(4), U_FIXED)
    slope_u4 = fixed_u_slope(Decimal(4), U_FIXED)
    slope_u1 = fixed_u_slope(ONE, U_FIXED)
    print("fixed u=4 theta=4 r", fmt(r_u, 30))
    print("learning rate      ", fmt(l_u, 30))
    print("slope theta=4      ", fmt(slope_u4, 30))
    print("slope theta=1      ", fmt(slope_u1, 30))
    # Closed learning rate (-1 + sqrt(33)) / 2.
    l_closed = (-ONE + sqrt(Decimal(33))) / TWO
    print("learning closed    ", fmt(l_closed, 30))
    if (l_u - l_closed).copy_abs() > Decimal("1e-30"):
        raise SystemExit("learning rate and closed form disagree")

    naked = -ONE / (TWO * sqrt(TWO * PI * ONE))
    naked4 = -ONE / (TWO * sqrt(TWO * PI * Decimal(4)))
    print("naked slope theta=1", fmt(naked, 30))
    print("naked slope theta=4", fmt(naked4, 30))

    r_c, c_min = minimize_C()
    # Polish C with a derivative bisection and compare.
    lo, hi = Decimal("0.05"), Decimal("0.9")
    for _ in range(300):
        mid = (lo + hi) / TWO
        if C_prime(mid) < 0:
            lo = mid
        else:
            hi = mid
    r_c2 = (lo + hi) / TWO
    c_min2 = C_of(r_c2)
    print("inf C", fmt(r_c, 30), fmt(c_min, 30))
    print("inf C bisect", fmt(r_c2, 30), fmt(c_min2, 30))
    if (c_min - c_min2).copy_abs() > Decimal("1e-24"):
        raise SystemExit("inf C methods disagree")

    cross = crossing_of_five()
    j_cross = minimize_sign(cross)[1]
    print("crossing", fmt(cross, 30), "J", fmt(j_cross, 30))

    print("-- comparisons --")
    checks = []
    checks.append(compare("J(theta=1)", j_star, "5.182159696490"))
    checks.append(compare("envelope slope", slope_closed, "-0.182159696490"))
    checks.append(compare("along-path probe", probe, "-0.130861161564"))
    checks.append(compare("along-path heat", heat_s, "0.187741986525"))
    checks.append(compare("along-path sign", sign_s, "-0.239040521451"))
    checks.append(compare("J*(theta=1/8)", grid[0][2], "5.911577251205"))
    checks.append(compare("J*(theta=8)", grid[-1][2], "4.998066177768"))
    checks.append(compare("second derivative", d2_closed, "0.313020858054"))
    checks.append(compare("reoptimized spread", spread, "0.001577268119"))
    for value, claimed in zip(
        square_values,
        ("5.316961792302", "8.000711319618", "13.186217779633", "23.557230699662"),
    ):
        checks.append(compare("admissible squared", value, claimed))
    checks.append(compare("naked slope", naked, "-0.199471140201"))
    checks.append(compare("erfc(1)", erfc1_series, "0.157299207050"))
    checks.append(compare("learning rate u=4 theta=4", l_u, "2.372281323269"))
    checks.append(compare("inf C", c_min2, "4.966383544211"))
    # The note prints 7.5267. The task's ten-decimal figure is the
    # rounded value of the root, not a twelve-decimal claim.
    checks.append(compare("crossing rounded to 10 decimals", q10(cross), "7.5267230646"))
    checks.append(compare("p_cap", p_cap, "0.260317771627"))
    checks.append(compare("Phi^{-1}(0.975)", phi_series, "1.959963984540"))
    checks.append(compare("erfcinv(1/20)", z_series, "1.385903824350"))

    # Extra figures printed in the note, same tolerance.
    note_grid = {
        "0.125": ("0.671238475860", "5.911577251205"),
        "0.25": ("0.597650549677", "5.584150440609"),
        "0.5": ("0.540374322719", "5.343143969081"),
        "1": ("0.5", "5.182159696490"),
        "2": ("0.474155421441", "5.083843454099"),
        "4": ("0.458964128271", "5.028073368003"),
        "8": ("0.450597167920", "4.998066177768"),
    }
    for theta, r_t, j_t in grid:
        key = format(theta.normalize(), "f")
        if key == "1":
            key = "1"
        cr, cj = note_grid[key]
        checks.append(compare(f"r*(theta={key})", r_t, cr))
        checks.append(compare(f"J*(theta={key})", j_t, cj))
    checks.append(compare("fixed-r spread", spread_fixed, "0.001839996934"))
    checks.append(compare("passive fraction", r_u, "0.296535165409"))
    checks.append(compare("passive slope theta=4", slope_u4, "0.177466031352"))
    checks.append(compare("inf C location", r_c2, "0.441594095399"))
    short = 5 - grid[-1][2]
    checks.append(compare("shortfall below 5", short, "0.001933822232"))

    print("P(loss=16)", fmt(psi_half, 20))
    print("P(loss>16) 0 by the loss set {0, 16}")
    print("passive slope at theta=4 is positive:", slope_u4 > 0)
    print("naked slope at theta=4 is negative:", naked4 < 0)
    print("second derivative positive:", d2_closed > 0)
    print("spread penalty positive:", spread > 0)
    loss16_ok = (psi_half - Decimal("0.25")).copy_abs() < Decimal("1e-30")
    slope_pos = slope_u4 > 0
    all_ok = all(checks) and loss16_ok and slope_pos
    print("ALL_MATCH" if all_ok else "SOME_DIFFER")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
