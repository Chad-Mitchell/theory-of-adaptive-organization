#!/usr/bin/env python3
"""Independent recomputation of the antifragility turnover numbers.

Reads no module from theory/antifragility_checks. The formulas are the ones
locked in PREREG.md and ADDENDUM.md: homogeneous mean-field cost, the
birth-death chain for R-select, heat proportional to quality, and the ruin
event epsilon > 3/2.
"""
from __future__ import annotations

import math
from fractions import Fraction

import numpy as np

V = 4.0
N = 4
C = 0.5
H = 0.5
W = 1.5
QH = 1.0
QL = 0.25
PI = 0.5
MUT = 0.25
B_CASH = 0.5
DELTA = 1.0
KT = 1.0
A_RATE = 1.0
G = np.array(
    [0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.7, 1, 1.5, 2, 3, 4, 6, 8, 12, 20],
    dtype=float,
)
EPS_CAP = 1.5
EPS_R = 0.05
M_RUIN = 400_000
SEED = 20261123


def stock(q, c=C):
    return 0.5 * KT * math.log(1.0 + V * c * q)


def B_of(q, c=C):
    return B_CASH + stock(q, c)


def j_hom(sigma, n=N, c=C, q=1.0, delta=DELTA, b=None, use_stock=True):
    """Mean-field cost of n identical units. Returns J and pieces."""
    if b is None:
        b = B_CASH
    Q = KT * A_RATE * V * c * q
    B = (b + stock(q, c)) if use_stock else b
    heat = n * Q
    upkeep = n * H
    if delta == 0.0:
        phi = n * c * q
        eps = V / (1.0 + V * phi)
        build = n * max(sigma, 0.0) * B
        return heat + upkeep + build + W * eps, {
            "heat": heat, "upkeep": upkeep, "build": build, "eps": eps,
            "phi": phi, "B": B, "Q_flow": KT * A_RATE * V * phi,
            "H_J": heat + n * max(sigma, 0.0) * (stock(q, c) if use_stock else 0.0),
        }
    r = sigma / (sigma + delta)
    phi = n * c * q * r
    eps = V / (1.0 + V * phi)
    build = n * sigma * B
    q_flow = KT * A_RATE * V * phi
    h_j = heat + n * sigma * (stock(q, c) if use_stock else 0.0)
    return heat + upkeep + build + W * eps, {
        "heat": heat, "upkeep": upkeep, "build": build, "eps": eps,
        "phi": phi, "B": B, "Q_flow": q_flow, "H_J": h_j, "r": r,
    }


def sigma_star_from_derivative(n=N, c=C, q=1.0, delta=DELTA):
    B = B_of(q, c)
    Gamma = V * n * c * q
    # J = n(Q+h) + n B sigma + w v (sigma+delta) / ((1+Gamma) sigma + delta)
    # J' = n B - w v Gamma delta / ((1+Gamma) sigma + delta)^2
    # zero when ((1+Gamma) sigma + delta)^2 = w v Gamma delta / (n B)
    rhs = W * V * Gamma * delta / (n * B)
    root = math.sqrt(rhs)
    sigma = (root - delta) / (1.0 + Gamma)
    return sigma, B, rhs


def sigma_star_u_formula(n=N, c=C, q=1.0, delta=DELTA):
    B = B_of(q, c)
    Gamma = V * n * c * q
    disc_lo = math.sqrt(W * V * Gamma)
    disc_hi = math.sqrt(n * B * delta)
    u = (disc_lo - disc_hi) / (Gamma * disc_hi + disc_lo)
    sigma = delta * u / (1.0 - u)
    return u, sigma, B, disc_lo, disc_hi


def j_second_addendum(sigma, n=N, c=C, q=1.0, delta=DELTA):
    Gamma = V * n * c * q
    r = sigma / (sigma + delta)
    return (
        2.0 * W * V * Gamma * delta
        / ((1.0 + Gamma * r) ** 2 * (sigma + delta) ** 3)
        * (1.0 + Gamma * delta / ((1.0 + Gamma * r) * (sigma + delta)))
    )


def j_second_simplified(sigma, n=N, c=C, q=1.0, delta=DELTA):
    """864/(9 sigma+1)^3 at the frozen identical-unit numbers; general form too."""
    Gamma = V * n * c * q
    return (
        2.0 * W * V * Gamma * delta * (1.0 + Gamma)
        / ((1.0 + Gamma) * sigma + delta) ** 3
    )


def stationary_select(n=N, eta=0.0, qh=QH, ql=QL, pi=PI, m=MUT):
    """Exact stationary weights on k = 0..n for sigma > 0. Scale cancels."""
    eta_f = Fraction(eta).limit_denominator(8)
    pi_f = Fraction(pi).limit_denominator(16)
    m_f = Fraction(m).limit_denominator(16)
    qh_f = Fraction(qh).limit_denominator(16)
    ql_f = Fraction(ql).limit_denominator(16)
    fac_h = eta_f + (1 - eta_f) * qh_f / qh_f
    fac_l = eta_f + (1 - eta_f) * qh_f / ql_f
    ups = []
    downs = []
    for k in range(n):
        copy_h = Fraction(k, n - 1)
        ups.append((n - k) * fac_l * (m_f * pi_f + (1 - m_f) * copy_h))
    for k in range(1, n + 1):
        copy_l = Fraction(n - k, n - 1)
        downs.append(k * fac_h * (m_f * (1 - pi_f) + (1 - m_f) * copy_l))
    weights = [Fraction(1)]
    for k in range(1, n + 1):
        weights.append(weights[-1] * ups[k - 1] / downs[k - 1])
    total = sum(weights)
    probs = [w / total for w in weights]
    bal = max(abs(probs[k] * downs[k - 1] - probs[k - 1] * ups[k - 1]) for k in range(1, n + 1))
    return probs, ups, downs, bal, fac_h, fac_l


def ek_of(probs):
    return sum(Fraction(k) * p for k, p in enumerate(probs))


def heat_of(ek, n=N, c=C, qh=QH, ql=QL):
    sum_q = ek * qh + (n - ek) * ql
    return KT * A_RATE * V * c * sum_q


def build_select(probs, sigma, c=C, n=N, eta=0.0, qh=QH, ql=QL, m=MUT, pi=PI):
    if sigma == 0.0:
        return 0.0
    lam_h = sigma * (eta + (1.0 - eta) * qh / qh)
    lam_l = sigma * (eta + (1.0 - eta) * qh / ql)
    bh = B_of(qh, c)
    bl = B_of(ql, c)
    total = 0.0
    for k, p in enumerate(probs):
        pf = float(p)
        if k >= 1:
            p_new_h = m * pi + (1.0 - m) * (k - 1) / (n - 1)
            p_new_l = m * (1.0 - pi) + (1.0 - m) * (n - k) / (n - 1)
            total += pf * k * lam_h * (p_new_h * bh + p_new_l * bl)
        if n - k >= 1:
            p_new_h = m * pi + (1.0 - m) * k / (n - 1)
            p_new_l = m * (1.0 - pi) + (1.0 - m) * (n - k - 1) / (n - 1)
            total += pf * (n - k) * lam_l * (p_new_h * bh + p_new_l * bl)
    return total


def phi_select(ek, sigma, c=C, n=N, delta=DELTA, eta=0.0, qh=QH, ql=QL):
    if delta == 0.0:
        ah = al = 1.0
    elif sigma == 0.0:
        ah = al = 0.0
    else:
        lam_h = sigma * (eta + (1.0 - eta) * qh / qh)
        lam_l = sigma * (eta + (1.0 - eta) * qh / ql)
        ah = lam_h / (lam_h + delta)
        al = lam_l / (lam_l + delta)
    return float(ek) * c * qh * ah + (n - float(ek)) * c * ql * al


def j_hetero(sigma, probs, ek, c=C, at_zero_binomial=None):
    """Locked coupling: precision and heat both scale with q."""
    if sigma == 0.0 and at_zero_binomial is not None:
        ek_use = at_zero_binomial
        probs_use = None
        build = 0.0
    else:
        ek_use = ek
        probs_use = probs
        build = build_select(probs_use, sigma, c=c)
    heat = float(heat_of(ek_use, c=c))
    upkeep = N * H
    phi = phi_select(ek_use, sigma, c=c)
    eps = V / (1.0 + V * phi)
    j = heat + upkeep + build + W * eps
    return j, {
        "heat": heat, "upkeep": upkeep, "build": build, "eps": eps,
        "phi": phi, "ek": float(ek_use), "J": j,
        "Q_flow": KT * A_RATE * V * phi,
    }


def binomial_ek(n=N, pi=PI):
    return Fraction(n) * Fraction(pi).limit_denominator()


def fixed_heat_j(sigma, probs, ek, c=C):
    """Diagnostic: every unit pays the cap heat. q scales aim and hazard only.

    Installed precision is c. Stock is the stock of that precision, the same
    for every rebuild. Effective precision is c * q * alpha.
    """
    heat = N * KT * A_RATE * V * c
    upkeep = N * H
    if sigma == 0.0:
        build = 0.0
        phi = 0.0
        ek_use = binomial_ek()
    else:
        ek_use = ek
        # failure flux times one stock
        # reuse build_select's flux by charging B(q) = stock(c) + b for both q
        # implemented directly
        lam_h = sigma * (QH / QH)
        lam_l = sigma * (QH / QL)
        B = B_CASH + stock(1.0, c)  # installed precision c, aim does not change the stock
        # stock(1, c) = 0.5 log(1+v c), which is the installed channel
        total_flux = 0.0
        for k, p in enumerate(probs):
            total_flux += float(p) * (k * lam_h + (N - k) * lam_l)
        build = total_flux * B
        phi = phi_select(ek_use, sigma, c=c)
    eps = V / (1.0 + V * phi)
    j = heat + upkeep + build + W * eps
    return j, heat, build, eps, phi


def ruin_identical(sigma, c, rng, m=M_RUIN):
    """P(eps>1.5) and E[eps] for n i.i.d. alignments. Heat and build are closed."""
    if sigma == 0.0:
        eps = np.full(m, V)
        p = 1.0
        mean_eps = V
    else:
        u = rng.random((m, N))
        alpha = u ** (DELTA / sigma)
        phi = c * 1.0 * alpha.sum(axis=1)
        eps = V / (1.0 + V * phi)
        p = float(np.mean(eps > EPS_CAP))
        mean_eps = float(eps.mean())
    Jmf, parts = j_hom(sigma, c=c)
    J = parts["heat"] + parts["upkeep"] + parts["build"] + W * mean_eps
    return p, mean_eps, J, Jmf


def ruin_types(sigma, probs, c, rng, rule, m=M_RUIN, eta=0.0):
    """Sample k, then alignments. rule 'select' uses quality-dependent hazard."""
    cdf = np.cumsum([float(p) for p in probs])
    cdf[-1] = 1.0
    if sigma == 0.0 or DELTA == 0.0 and sigma == 0.0:
        eps = np.full(m, V / (1.0 + V * 0.0))
        # at sigma 0 and delta>0, alpha=0
        p = 1.0 if V > EPS_CAP else 0.0
        mean_eps = float(eps[0])
        return p, mean_eps
    uk = rng.random(m)
    k = np.searchsorted(cdf, uk, side="left")
    U = rng.random((m, N))
    qh, ql = QH, QL
    lam_h = sigma * (eta + (1.0 - eta) * qh / qh)
    lam_l = sigma * (eta + (1.0 - eta) * qh / ql)
    phi = np.zeros(m)
    # vectorized by grouping would be faster; this loop over k is 5 groups
    for kk in range(N + 1):
        mask = k == kk
        if not np.any(mask):
            continue
        block = U[mask]
        acc = np.zeros(mask.sum())
        if kk:
            acc = acc + c * qh * (block[:, :kk] ** (DELTA / lam_h)).sum(axis=1)
        if kk < N:
            acc = acc + c * ql * (block[:, kk:] ** (DELTA / lam_l)).sum(axis=1)
        phi[mask] = acc
    eps = V / (1.0 + V * phi)
    return float(np.mean(eps > EPS_CAP)), float(eps.mean())


def main():
    print("INDEPENDENT RECOMPUTATION")
    B = B_of(1.0)
    print("B %.12f" % B)
    u, sig_u, B2, lo, hi = sigma_star_u_formula()
    sig_d, B3, rhs = sigma_star_from_derivative()
    print("u* %.12f sigma_u %.12f sigma_deriv %.12f |diff| %.3e" % (u, sig_u, sig_d, abs(sig_u - sig_d)))
    print("sqrt(w v Gamma)=%.12f sqrt(n B delta)=%.12f" % (lo, hi))
    Jstar, parts = j_hom(sig_d)
    J0, _ = j_hom(0.0)
    print("J(sigma*) %.12f J(0) %.12f gap %.12f" % (Jstar, J0, J0 - Jstar))
    # derivative at 0
    # loss piece derivative at 0 is -w v Gamma / delta * something wait
    # J'(0) = n (B - w v^2 c q / delta)
    jp0 = N * (B - W * V * V * C * 1.0 / DELTA)
    print("J'(0) %.12f threshold %.12f" % (jp0, W * V * V * C / DELTA))
    # second derivative identity
    sigmas = np.geomspace(1e-4, 20.0, 64)
    rels = []
    vals = []
    for s in sigmas:
        a = j_second_addendum(float(s))
        b = j_second_simplified(float(s))
        rels.append(abs(a - b) / b)
        vals.append(b)
    s0 = 0.0
    # at 0 the addendum formula has r=0
    a0 = j_second_addendum(0.0) if False else None
    # r=0 is fine: formula uses r
    a0 = (
        2.0 * W * V * (V * N * C) * DELTA
        / ((1.0 + 0.0) ** 2 * (DELTA) ** 3)
        * (1.0 + (V * N * C) * DELTA / ((1.0) * DELTA))
    )
    b0 = j_second_simplified(0.0)
    print("J''(0) addendum %.12f simplified %.12f 864 %.12f" % (a0, b0, 864.0))
    print("max rel addendum vs simplified on log grid %.3e" % max(rels))
    print("min J'' on log grid %.12f at s=%.6f" % (min(vals), sigmas[int(np.argmin(vals))]))
    # closed 864/(9s+1)^3 at s=20
    print("864/181**3 %.12f" % (864.0 / 181.0 ** 3))
    # Delta2
    half = 0.5 * (j_hom(sig_d / 2.0)[0] + j_hom(1.5 * sig_d)[0]) - Jstar
    print("Delta2 %.12f" % half)
    # Jensen
    def gap(xs, fn):
        vals = [fn(x) for x in xs]
        return 0.5 * (vals[0] + vals[1]) - fn(0.5 * (xs[0] + xs[1]))
    print("Jensen J {1,2} %.12f" % gap((1.0, 2.0), lambda s: j_hom(s)[0]))
    print("Jensen J {0,2} %.12f" % gap((0.0, 2.0), lambda s: j_hom(s)[0]))
    print("Jensen Qf {1,2} %.12f" % gap((1.0, 2.0), lambda s: j_hom(s)[1]["Q_flow"]))
    print("Jensen Qf {0,2} %.12f" % gap((0.0, 2.0), lambda s: j_hom(s)[1]["Q_flow"]))
    Gamma = V * N * C
    def qmatch(s):
        return KT * A_RATE * Gamma * (s + DELTA) / s
    print("Jensen Qm {1,2} %.12f" % gap((1.0, 2.0), qmatch))
    # endpoints
    for s in (0.05, 20.0):
        J, p = j_hom(s)
        print("A0 s=%.2f J=%.10f HJ=%.10f Qf=%.10f Qm=%.10f" % (s, J, p["H_J"], p["Q_flow"], qmatch(s)))
    # n=1
    u1, s1, _, _, _ = sigma_star_u_formula(n=1)
    J1, _ = j_hom(s1, n=1)
    J10, _ = j_hom(0.0, n=1)
    print("n=1 sigma* %.12f J %.12f J0 %.12f" % (s1, J1, J10))
    # A14
    def phi_star(r):
        if r <= KT * A_RATE / (W * V):
            return 0.0
        return (1.0 / (V * N * r)) * (math.sqrt(W * V * r / (KT * A_RATE)) - 1.0)
    def Hstar(r):
        if r <= KT * A_RATE / (W * V):
            return 0.0
        return math.sqrt(KT * A_RATE * W * V / r) - KT * A_RATE / r
    rs = [i / 200 for i in range(1, 200)]
    phis = [phi_star(r) for r in rs]
    print("A14 phi_max %.12f at r=%.6f H(2/3)=%.12f" % (max(phis), rs[int(np.argmax(phis))], Hstar(2.0 / 3.0)))
    # nearest grid to 2/3
    r_near = min(rs, key=lambda r: abs(r - 2.0 / 3.0))
    print("A14 nearest r %.6f phi %.12f H %.12f cap_binds %s" % (
        r_near, phi_star(r_near), Hstar(r_near), max(phis) >= C))

    probs, ups, downs, bal, fac_h, fac_l = stationary_select()
    ek = ek_of(probs)
    ek_b = binomial_ek()
    print("balance residual %s" % bal)
    print("fac %s %s" % (fac_h, fac_l))
    print("probs " + " ".join("%.10f" % float(p) for p in probs))
    print("E[k] %.12f heat_sel %.12f heat_bin %.12f" % (float(ek), float(heat_of(ek)), float(heat_of(ek_b))))
    # jump
    j_jump, pj = j_hetero(1e-6, probs, ek)
    j0h, p0 = j_hetero(0.0, probs, ek, at_zero_binomial=ek_b)
    print("J(0) %.12f heat0 %.12f eps0 %.12f" % (j0h, p0["heat"], p0["eps"]))
    print("J(1e-6) %.12f heat %.12f eps %.12f build %.6e" % (j_jump, pj["heat"], pj["eps"], pj["build"]))
    # fine min on (0, inf)
    grid = np.linspace(0.001, 4.0, 8001)
    js = []
    for s in grid:
        js.append(j_hetero(float(s), probs, ek)[0])
    idx = int(np.argmin(js))
    print("hetero fine min s=%.6f J=%.12f above J0 by %.12f" % (grid[idx], js[idx], js[idx] - j0h))
    # exact-looking point 0.25 and neighbors
    for s in (0.2, 0.25, 0.3):
        j, p = j_hetero(s, probs, ek)
        print("A2 s=%.2f J=%.12f heat=%.12f build=%.12f eps=%.12f phi=%.12f" % (
            s, j, p["heat"], p["build"], p["eps"], p["phi"]))
    # second differences on i/20
    fine = [i / 20 for i in range(1, 401)]
    jf = [j_hetero(s, probs, ek)[0] for s in fine]
    d2 = [jf[i + 1] - 2 * jf[i] + jf[i - 1] for i in range(1, len(jf) - 1)]
    print("A2 min second diff %.6e at s=%.4f" % (min(d2), fine[1 + int(np.argmin(d2))]))
    # H_J increasing: heat constant, stock rate = build - cash portion
    # continuous heat flat already printed
    heats = [j_hetero(s, probs, ek)[1]["heat"] for s in (0.05, 1.0, 20.0)]
    print("A2 heat span %.3e values %s" % (max(heats) - min(heats), " ".join("%.10f" % h for h in heats)))

    # c scan, locked coupling, does any cap put the positive-branch min under J(0)?
    print("\n== c scan, locked coupling, mean-field ==")
    best_gap = None
    for c in np.linspace(0.02, 0.5, 49):
        # stationary law does not depend on c
        j0, _ = j_hetero(0.0, probs, ek, c=float(c), at_zero_binomial=ek_b)
        # coarse then local
        ss = np.linspace(0.02, 6.0, 600)
        jj = [j_hetero(float(s), probs, ek, c=float(c))[0] for s in ss]
        k = int(np.argmin(jj))
        gap = jj[k] - j0
        if best_gap is None or gap < best_gap[0]:
            best_gap = (gap, float(c), float(ss[k]), jj[k], j0)
        if abs(c - 0.5) < 1e-9 or gap < 0:
            print("c=%.4f J0=%.6f Jmin=%.6f s=%.4f gap=%.6f" % (c, j0, jj[k], ss[k], gap))
    print("most negative gap c=%.4f gap=%.6f s=%.4f Jmin=%.6f J0=%.6f" % (
        best_gap[1], best_gap[0], best_gap[2], best_gap[3], best_gap[4]))

    def gap_of(c):
        j0, _ = j_hetero(0.0, probs, ek, c=c, at_zero_binomial=ek_b)
        a, b = 0.05, 2.0
        invphi = (math.sqrt(5.0) - 1.0) / 2.0
        x1 = b - invphi * (b - a)
        x2 = a + invphi * (b - a)
        f1 = j_hetero(x1, probs, ek, c=c)[0]
        f2 = j_hetero(x2, probs, ek, c=c)[0]
        for _ in range(50):
            if f1 < f2:
                b, x2, f2 = x2, x1, f1
                x1 = b - invphi * (b - a)
                f1 = j_hetero(x1, probs, ek, c=c)[0]
            else:
                a, x1, f1 = x1, x2, f2
                x2 = a + invphi * (b - a)
                f2 = j_hetero(x2, probs, ek, c=c)[0]
        s = 0.5 * (a + b)
        jmin = j_hetero(s, probs, ek, c=c)[0]
        return jmin - j0, s, jmin, j0

    def root_between(lo, hi):
        glo = gap_of(lo)[0]
        for _ in range(24):
            mid = 0.5 * (lo + hi)
            g = gap_of(mid)[0]
            if (g < 0) == (glo < 0):
                lo, glo = mid, g
            else:
                hi = mid
        return 0.5 * (lo + hi)

    print("gap root low %.5f high %.5f" % (root_between(0.05, 0.10), root_between(0.40, 0.50)))
    for c in (0.06972, 0.22, 0.44683, 0.5):
        g, s, jmin, j0 = gap_of(c)
        print("gap c=%.5f s=%.5f Jmin=%.6f J0=%.6f gap=%+.6f" % (c, s, jmin, j0, g))

    # fixed-heat counterfactual
    print("\n== fixed installed heat, q is aim only ==")
    j0f, heatf, _, _, _ = fixed_heat_j(0.0, probs, ek)
    ss = np.linspace(0.02, 6.0, 600)
    jj = []
    for s in ss:
        jj.append(fixed_heat_j(float(s), probs, ek)[0])
    k = int(np.argmin(jj))
    print("J(0)=%.6f heat=%.6f Jmin=%.6f s=%.4f gap=%.6f" % (j0f, heatf, jj[k], ss[k], jj[k] - j0f))
    # refine
    lo_s = max(0.01, float(ss[max(0, k - 2)]))
    hi_s = float(ss[min(len(ss) - 1, k + 2)])
    ss2 = np.linspace(lo_s, hi_s, 400)
    jj2 = [fixed_heat_j(float(s), probs, ek)[0] for s in ss2]
    k2 = int(np.argmin(jj2))
    print("refined s=%.6f J=%.8f" % (ss2[k2], jj2[k2]))
    print("-- fixed-heat admissible (eps law = informative; heat is n*kT*a*v*c) --")
    rng_f = np.random.Generator(np.random.PCG64(SEED + 7))
    adm_f = []
    for s in G:
        j, heat, build, eps_mf, phi = fixed_heat_j(float(s), probs, ek)
        if s == 0.0:
            p, mean_eps = 1.0, V
        else:
            p, mean_eps = ruin_types(float(s), probs, C, rng_f, "select", eta=0.0, m=200_000)
        J = heat + N * H + build + W * mean_eps
        flag = "ADM" if p <= EPS_R else "no"
        print("s=%.4f P=%.5f Jmc=%.4f Jmf=%.4f %s" % (s, p, J, j, flag))
        if p <= EPS_R:
            adm_f.append((J, float(s), p, j))
    adm_f.sort()
    print("fixed-heat admissible argmin s=%.4f Jmc=%.4f P=%.5f Jmf=%.4f" % (
        adm_f[0][1], adm_f[0][0], adm_f[0][2], adm_f[0][3]))

    # ruin table
    print("\n== ruin table M=%d seed=%d ==" % (M_RUIN, SEED))
    rng = np.random.Generator(np.random.PCG64(SEED))
    print("phi threshold %.10f" % (1.0 / EPS_CAP - 1.0 / V))
    print("-- identical --")
    adm = []
    for s in G:
        p, mean_eps, J, Jmf = ruin_identical(float(s), C, rng)
        flag = "ADM" if p <= EPS_R + 1e-15 else "no"
        print("s=%.4f P=%.6f Jmc=%.6f Jmf=%.6f eps=%.6f %s" % (s, p, J, Jmf, mean_eps, flag))
        if p <= EPS_R + 1e-15:
            adm.append((J, float(s), p))
    if adm:
        adm.sort()
        print("identical admissible argmin s=%.4f J=%.6f P=%.6f" % (adm[0][1], adm[0][0], adm[0][2]))

    # refresh / uninformative binomial, eta=1 so lam equal
    print("-- uninformative binomial eta=1 --")
    # binomial probabilities
    bin_p = []
    pi_f = Fraction(1, 2)
    for k in range(N + 1):
        bin_p.append(math.comb(N, k) * float(pi_f ** k * (1 - pi_f) ** (N - k)))
    adm = []
    for s in G:
        if s == 0.0:
            p, mean_eps = 1.0, V
        else:
            p, mean_eps = ruin_types(float(s), bin_p, C, rng, "refresh", eta=1.0)
        # mean-field pieces at eta=1, ek=2
        ek2 = binomial_ek()
        heat = float(heat_of(ek2))
        # build: every failure draws from prior. flux = n * sigma since eta=1 lam=sigma
        if s == 0.0:
            build = 0.0
            phi = 0.0
        else:
            eb = PI * B_of(QH) + (1 - PI) * B_of(QL)
            build = N * float(s) * eb
            phi = phi_select(ek2, float(s), eta=1.0)
        eps_mf = V / (1.0 + V * phi)
        Jmf = heat + N * H + build + W * eps_mf
        J = heat + N * H + build + W * mean_eps
        flag = "ADM" if p <= EPS_R else "no"
        print("s=%.4f P=%.6f Jmc=%.6f Jmf=%.6f %s" % (s, p, J, Jmf, flag))
        if p <= EPS_R:
            adm.append((J, float(s), p))
    if adm:
        adm.sort()
        print("uninformative admissible argmin s=%.4f J=%.6f P=%.6f" % (adm[0][1], adm[0][0], adm[0][2]))

    print("-- informative select --")
    adm = []
    for s in G:
        if s == 0.0:
            p, mean_eps = 1.0, V
            jmf, parts = j_hetero(0.0, probs, ek, at_zero_binomial=ek_b)
        else:
            p, mean_eps = ruin_types(float(s), probs, C, rng, "select", eta=0.0)
            jmf, parts = j_hetero(float(s), probs, ek)
        J = parts["heat"] + parts["upkeep"] + parts["build"] + W * mean_eps
        flag = "ADM" if p <= EPS_R else "no"
        print("s=%.4f P=%.6f Jmc=%.6f Jmf=%.6f %s" % (s, p, J, jmf, flag))
        if p <= EPS_R:
            adm.append((J, float(s), p))
    if adm:
        adm.sort()
        print("informative admissible argmin s=%.4f J=%.6f P=%.6f" % (adm[0][1], adm[0][0], adm[0][2]))

    # quality-observed: every replacement installs qH, so for sigma>0 the chain
    # absorbs at k=n. Mean-field: all units quality 1, same as homogeneous.
    # At sigma=0 types stay binomial. Ruin at sigma>0 equals identical units.
    print("-- quality observed: sigma>0 is the identical-unit chain (all qH) --")
    print("Jmf at s=1", j_hom(1.0)[0])

    # phi scan under the cap, identical units, diagnostic
    print("\n== phi scan identical, under the cap, diagnostic ==")
    rng2 = np.random.Generator(np.random.PCG64(SEED + 1))
    phis = [0.11, 0.12, 0.15, 0.2, 0.25, 0.35, 0.5]
    for phi in phis:
        best = None
        for s in G:
            if s == 0.0:
                continue
            p, mean_eps, J, Jmf = ruin_identical(float(s), phi, rng2, m=120_000)
            if p <= EPS_R:
                if best is None or J < best[0]:
                    best = (J, float(s), p, Jmf)
        if best is None:
            print("phi=%.4f no admissible grid point" % phi)
        else:
            print("phi=%.4f admissible s=%.4f Jmc=%.4f Jmf=%.4f P=%.4f" % (phi, best[1], best[0], best[3], best[2]))

    # mean precision needed
    print("phi for mean pool at full alignment to hit 5/12: %.6f" % ((5.0 / 12.0) / N))
    print("A14 max phi 3/32 = %.6f pool at r=1 %.6f vs 5/12 %.6f" % (3 / 32, N * 3 / 32, 5 / 12))


if __name__ == "__main__":
    main()
