#!/usr/bin/env python3
"""Independent recomputation of the acting-loop numbers.

Does not import theory/acting_loop_checks. Stationary moments come from the
scalar Riccati and the Lyapunov equation of the linear plant. Special
functions are the platform math library.
"""
from __future__ import annotations

import math
from decimal import Decimal, getcontext

getcontext().prec = 80

CLAIMED = {
    "factor_a1": "0.171572875254",
    "factor_a12": "0.381966011250",
    "factor_a2": "0.055728090001",
    "delta_half": "-1.096373258863",
    "fraction_q4": "0.856768708291",
    "delta_q4": "0.033889928154",
    "variance": "0.853553390593",
    "stock_open": "0.346573590280",
    "stock_closed": "0.267399998370",
    "derivative": "0.189957517375",
    "tail": "0.000014940159",
    "slope": "1.552284749831",
    "second": "-0.321714500038",
    "spread": "-0.001612560843",
    "threshold": "0.160857250019",
    "sign_gap": "0.031682633557",
    "sign_loss": "4.439079197657",
    "lifetime": "0.655679542419",
}


def show(name, value, claimed=None):
    if claimed is None:
        print(f"{name} = {value}")
        return
    err = abs(float(value) - float(claimed))
    flag = "OK" if err <= 5e-13 else "MISMATCH"
    print(f"{flag}  {name} = {value:.15f}  claimed {claimed}  abs err {err:.3e}")


def riccati_p(u, theta, a=1.0):
    if u == 0.0:
        return theta
    return (-a + math.sqrt(a * a + 2.0 * a * theta * u)) / u


def gain(a, q, rho=1.0, b=1.0):
    return (-a + math.sqrt(a * a + q * b * b / rho)) / b


def moments(a, b, K, p, theta):
    ac = a + b * K
    s = a * (theta - p) / ac
    v = p + s
    return s, v


def alpha():
    return (4.0 - math.pi) / (6.0 * math.pi)


def direct_cost(theta, u, q, a=1.0, b=1.0, rho=1.0, K=None):
    """Heat floor kT*L, probe price, state penalty, actuation price. gamma = 0."""
    p = riccati_p(u, theta, a)
    if K is None:
        K = gain(a, q, rho, b)
    s, v = moments(a, b, K, p, theta)
    L = a * (theta / p - 1.0)
    J = L + alpha() * u + q * v + rho * K * K * s
    return J, p, s, v, L, K


def full_info_factor(a, q=1.0):
    P = -a + math.sqrt(a * a + q)
    return q - 2.0 * a * P


def priced_gap_from_cost(theta, r, q, a=1.0):
    """Sensing-alone cost q*theta minus the closed-loop cost at fraction r."""
    p = r * theta
    # Riccati: u p^2 + 2 a p - 2 a theta = 0
    u = 2.0 * a * (theta - p) / (p * p)
    J, p2, s, v, L, K = direct_cost(theta, u, q, a=a)
    return q * theta - J, u, p2, s, v, L, K


def newton_q4():
    K2 = (math.sqrt(5.0) - 1.0) ** 2
    al = alpha()
    r = 0.85
    for _ in range(60):
        f = K2 * r ** 3 + (2.0 * al - 1.0) * r - 4.0 * al
        fp = 3.0 * K2 * r * r + (2.0 * al - 1.0)
        r -= f / fp
    return r


def phi(z):
    return math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def Phi(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def capped_variance_derivative(v):
    z = 1.0 / math.sqrt(v)
    return (2.0 * Phi(z) - 1.0) - 2.0 * z * phi(z)


def quadrature_min_x2(v, n=4000):
    """E[min(X^2, 1)] for X ~ N(0, v), by a clipped Gauss-Hermite-free grid."""
    # Integrate the standard normal on a wide range.
    z_cap = 1.0 / math.sqrt(v)
    # Simpson on [-12, 12]
    lo, hi, n = -12.0, 12.0, n
    h = (hi - lo) / n
    acc = 0.0
    for i in range(n + 1):
        z = lo + i * h
        w = 4.0 if i % 2 else 2.0
        if i == 0 or i == n:
            w = 1.0
        val = min(v * z * z, 1.0) * phi(z)
        acc += w * val
    return acc * h / 3.0


def second_derivative_fixed_u(theta=1.0, u=4.0, q=1.0, h=1e-5):
    jp = direct_cost(theta + h, u, q)[0]
    j0 = direct_cost(theta, u, q)[0]
    jm = direct_cost(theta - h, u, q)[0]
    return (jp - 2.0 * j0 + jm) / h ** 2


def slope_fixed_u(theta=1.0, u=4.0, q=1.0, h=1e-6):
    return (direct_cost(theta + h, u, q)[0] - direct_cost(theta - h, u, q)[0]) / (2.0 * h)


def minimize_r(theta, q, a=1.0):
    # Grid then Newton on dJ/dr = 0 is unnecessary: sample finely.
    best_r, best_j = None, None
    for i in range(1, 20000):
        r = i / 20000.0
        gap, u, p, s, v, L, K = priced_gap_from_cost(theta, r, q, a)
        J = q * theta - gap
        if best_j is None or J < best_j:
            best_r, best_j = r, J
    return best_r, best_j


def psi(corr):
    # Sign loss uses psi = arccos(correlation) / pi, and the open-loop
    # correlation of the conditional mean is sqrt(1-r)? The prereg writes
    # psi(r) = arccos(sqrt(1-r)) / pi. Under feedback the correlation is
    # sqrt(s/v), and the loss is 16 * arccos(correlation) / pi.
    return math.acos(corr) / math.pi


def cox_numerical():
    # Posterior proportional to (1+x^2) exp(-(1+x^2)) * exp(-x^2/2)
    # = (1+x^2) exp(-1) exp(-1.5 x^2), times the normal constant already
    # in the prior. Prior density includes 1/sqrt(2 pi) exp(-x^2/2).
    # Likelihood lambda exp(-lambda * t) at t=1, lambda=1+x^2.
    def weight(x):
        lam = 1.0 + x * x
        prior = math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
        return lam * math.exp(-lam) * prior

    lo, hi, n = -12.0, 12.0, 20000
    h = (hi - lo) / n
    z0 = z2 = 0.0
    for i in range(n + 1):
        x = lo + i * h
        w = 4.0 if i % 2 else 2.0
        if i == 0 or i == n:
            w = 1.0
        dens = weight(x)
        z0 += w * dens
        z2 += w * x * x * dens
    z0 *= h / 3.0
    z2 *= h / 3.0
    return z2 / z0


def mean_lifetime_quadrature():
    # E[1/(1+X^2)] for X ~ N(0,1)
    lo, hi, n = -20.0, 20.0, 40000
    h = (hi - lo) / n
    acc = 0.0
    for i in range(n + 1):
        x = lo + i * h
        w = 4.0 if i % 2 else 2.0
        if i == 0 or i == n:
            w = 1.0
        acc += w * (1.0 / (1.0 + x * x)) * math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
    return acc * h / 3.0


def minimize_sign(theta):
    al = alpha()

    def J(r):
        return al * 2.0 * (1.0 - r) / (theta * r * r) + (1.0 - r) / r + 16.0 * math.acos(math.sqrt(1.0 - r)) / math.pi

    def g(r):
        # derivative of A/theta + C, A = alpha * 2 (1-r) / r^2
        # d/dr [2 alpha (1-r)/r^2] = 2 alpha (r-2)/r^3
        A_prime = al * 2.0 * (r - 2.0) / r ** 3
        C_prime = -1.0 / r ** 2 + 16.0 / (2.0 * math.pi * math.sqrt(r * (1.0 - r)))
        return A_prime / theta + C_prime

    best_r, best_j = 0.5, J(0.5)
    for i in range(1, 8000):
        r = i / 8000.0
        val = J(r)
        if val < best_j:
            best_r, best_j = r, val
    r = best_r
    for _ in range(40):
        step = 1e-6
        gp = (g(r + step) - g(r - step)) / (2.0 * step)
        nxt = r - g(r) / gp
        if not (1e-6 < nxt < 1.0 - 1e-6):
            break
        if abs(nxt - r) < 1e-14:
            r = nxt
            break
        r = nxt
    return r, J(r)


def main():
    print("alpha", f"{alpha():.16f}")

    for a, key in ((1.0, "factor_a1"), (0.5, "factor_a12"), (2.0, "factor_a2")):
        show(key, full_info_factor(a), CLAIMED[key])
        # large-u numerical check of the full-information cost against 2 a P theta
        P = -a + math.sqrt(a * a + 1.0)
        J, p, s, v, L, K = direct_cost(1.0, 1e8, 1.0, a=a)
        # drop the channel, which is not charged in the full-information gap
        regulation = 1.0 * v + K * K * s
        print(f"    full-info regulation at u=1e8, a={a}: {regulation:.12f} vs {2*a*P:.12f}, p={p:.3e}")

    gap, u, p, s, v, L, K = priced_gap_from_cost(1.0, 0.5, 1.0)
    show("delta_half", gap, CLAIMED["delta_half"])
    print(f"    direct pieces at r=1/2: u={u:.6f} p={p:.6f} v={v:.6f} L={L:.6f} K={K:.6f}")

    # every fraction dearer: sample the gap
    worst = -1e9
    for i in range(1, 1000):
        r = i / 1000.0
        g, *_ = priced_gap_from_cost(1.0, r, 1.0)
        worst = max(worst, g)
    print(f"    stake-1 max gap on a 0.001-grid: {worst:.6e}")

    r4 = newton_q4()
    g4, *_ = priced_gap_from_cost(1.0, r4, 4.0)
    show("fraction_q4", r4, CLAIMED["fraction_q4"])
    show("delta_q4", g4, CLAIMED["delta_q4"])

    Kstar = gain(1.0, 1.0)
    s, v = moments(1.0, 1.0, Kstar, 0.5, 1.0)
    show("variance", v, CLAIMED["variance"])
    print(f"    gain sqrt2-1 = {Kstar:.16f}  exact {math.sqrt(2)-1:.16f}  cap gain = {(0.5)/(0.6-0.5)-1:.1f}")
    I0 = 0.5 * math.log(1.0 / 0.5)
    I1 = 0.5 * math.log(v / 0.5)
    show("stock_open", I0, CLAIMED["stock_open"])
    show("stock_closed", I1, CLAIMED["stock_closed"])
    rho = 20.0 / 21.0
    Qfin = 0.5 * rho / (rho * 1.5 - 1.0)
    print(f"    Qfin = {Qfin:.16f}  10/9 = {10/9:.16f}  equal {abs(Qfin-10/9)<1e-15}")
    # b=0
    for Ktry in (0.0, 1.0, 4.0, 100.0):
        sb, vb = moments(1.0, 0.0, Ktry, 0.5, 1.0)
        print(f"    b=0 K={Ktry}: v={vb:.16f} s={sb:.16f}")

    phip = capped_variance_derivative(v)
    dC = 0.25 * (1.0 - phip)
    show("derivative", dC, CLAIMED["derivative"])
    # numerical derivative of the quadrature through K
    def capped_obj(K):
        ss, vv = moments(1.0, 1.0, K, 0.5, 1.0)
        return quadrature_min_x2(vv) + K * K * ss

    hK = 1e-5
    num = (capped_obj(Kstar + hK) - capped_obj(Kstar - hK)) / (2.0 * hK)
    print(f"    quadrature derivative at the gain: {num:.12f}  Emin at v: {quadrature_min_x2(v):.12f}")
    tail = math.erfc(4.0 / math.sqrt(2.0 * v))
    show("tail", tail, CLAIMED["tail"])
    print(f"    4/sqrt(v) = {4/math.sqrt(v):.6f}")

    # Analytic slope and second derivative at fixed u=4, q=1, a=1.
    # p = (-1 + sqrt(1+8θ))/4, dp/dθ = 1/sqrt(1+8θ)
    # J = (5-2√2) p + 2(√2-1) θ + const, so
    # dJ/dθ = (5-2√2)/sqrt(1+8θ) + 2√2 - 2 = (4√2-1)/3 at θ=1
    # d²J/dθ² = (5-2√2) * (-4) / (1+8θ)^{3/2} = 4(2√2-5)/27 at θ=1
    slope_exact = (4.0 * math.sqrt(2.0) - 1.0) / 3.0
    second_exact = 4.0 * (2.0 * math.sqrt(2.0) - 5.0) / 27.0
    show("slope", slope_exact, CLAIMED["slope"])
    show("second", second_exact, CLAIMED["second"])
    print(f"    finite-difference slope h=1e-6 {slope_fixed_u():.12f}")
    print(f"    finite-difference second h=1e-5 {second_derivative_fixed_u():.12f}")
    spread = (direct_cost(0.9, 4.0, 1.0)[0] + direct_cost(1.1, 4.0, 1.0)[0]) / 2.0 - direct_cost(1.0, 4.0, 1.0)[0]
    show("spread", spread, CLAIMED["spread"])
    d2_closed = 4.0 * (2.0 * math.sqrt(2.0) - 5.0) / 27.0
    thresh = -0.5 * d2_closed
    show("threshold", thresh, CLAIMED["threshold"])
    print(f"    closed-form second {d2_closed:.16f}")

    # Global concavity of the fixed-intensity slice, and the minimizing cost.
    print("-- curvature --")
    for th in (0.25, 0.5, 1.0, 2.0, 4.0, 8.0):
        print(f"    fixed u=4 d2({th}) = {second_derivative_fixed_u(th):.6f}")
    # u=0 is the blind cost q*θ. The r-grid stops short of r=1, so the
    # stake-1 minimum has to be compared with that endpoint directly.
    for q in (1.0, 4.0):
        samples = []
        for th in (0.9, 1.0, 1.1):
            rr, jj = minimize_r(th, q)
            blind = q * th
            if blind < jj:
                rr, jj = 1.0, blind
            samples.append((th, rr, jj))
            print(f"    min-cost q={q} theta={th}: r={rr:.6f} J={jj:.8f} blind={blind:.8f}")
        spread_star = (samples[0][2] + samples[2][2]) / 2.0 - samples[1][2]
        d2_star = (samples[0][2] - 2.0 * samples[1][2] + samples[2][2]) / 0.01
        print(f"    reoptimized spread q={q}: {spread_star:.8e}  second {d2_star:.8e}")

    # Sign grid at theta=8 and the floor, independent Newton.
    r8, j8 = minimize_sign(8.0)
    # floor: minimize C(r) = (1-r)/r + 16 psi(r)
    def C(r):
        return (1.0 - r) / r + 16.0 * math.acos(math.sqrt(1.0 - r)) / math.pi

    best_r, best_c = 0.4, C(0.4)
    for i in range(1, 8000):
        r = i / 8000.0
        val = C(r)
        if val < best_c:
            best_r, best_c = r, val
    print(f"    sign J(8)={j8:.12f} r={r8:.6f} floor={best_c:.12f} gap={j8-best_c:.12f}")
    published_gap = 4.998066177768 - 4.966383544211
    show("sign_gap", j8 - 4.966383544211, CLAIMED["sign_gap"])
    print(f"    published subtraction {published_gap:.12f}")

    corr = math.sqrt(math.sqrt(2.0) - 1.0)
    loss = 16.0 * math.acos(corr) / math.pi
    show("sign_loss", loss, CLAIMED["sign_loss"])
    print(f"    open correlation {math.sqrt(0.5):.6f} closed {corr:.6f}")

    sig2 = 1.0 / 3.0
    var_post = sig2 * (1.0 + 3.0 * sig2) / (1.0 + sig2)
    print(f"    cox closed-form variance {var_post:.16f}")
    print(f"    cox quadrature variance {cox_numerical():.12f}")
    et = math.sqrt(math.pi / 2.0) * math.exp(0.5) * math.erfc(1.0 / math.sqrt(2.0))
    show("lifetime", et, CLAIMED["lifetime"])
    print(f"    lifetime quadrature {mean_lifetime_quadrature():.12f}")

    slope_sign = 2.0 / 3.0 - 8.0 / (3.0 * math.pi)
    print(f"    old slope {slope_sign:.12f} +1/10 {slope_sign+0.1:.12f} +1/2 {slope_sign+0.5:.12f}")


if __name__ == "__main__":
    main()
