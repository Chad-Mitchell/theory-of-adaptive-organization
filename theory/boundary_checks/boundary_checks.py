#!/usr/bin/env python3
"""Checks for the boundary-sufficiency preregistration.

The lock is theory/boundary_checks/PREREG.md, commit 93084b0, sha256
58ba0ebaa19d126d8c47293bc82d598f4416832b1bf767c64c73e9d175de943c,
written before this script. Required identities that miss exit nonzero.
The radius-ratio tolerance is printed as a puzzle and does not by itself
fail the run.

Run from the repo root:
  nice -n 19 python3 theory/boundary_checks/boundary_checks.py
"""
from __future__ import annotations

import math

import numpy as np
from numpy.linalg import inv, solve

PASS = 0
FAIL = 0
PUZZLES = 0
EPS = 1.0 / 18.0


def check(name, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print("PASS  %s  %s" % (name, detail))
    else:
        FAIL += 1
        print("FAIL  %s  %s" % (name, detail))


def puzzle(name, ok, detail=""):
    global PUZZLES
    if ok:
        print("PASS  %s  %s" % (name, detail))
    else:
        PUZZLES += 1
        print("PUZZLE  %s  %s" % (name, detail))


def near(a, b, tol=1e-9):
    a = float(a)
    b = float(b)
    scale = max(1.0, abs(a), abs(b))
    return abs(a - b) <= tol * scale


def absnear(a, b, tol=1e-9):
    return abs(float(a) - float(b)) <= tol


def path_precision(n, alpha=1.0, beta=1.0):
    Q = np.zeros((n, n))
    for i in range(n):
        deg = (1 if i > 0 else 0) + (1 if i + 1 < n else 0)
        Q[i, i] = alpha + beta * deg
        if i + 1 < n:
            Q[i, i + 1] = Q[i + 1, i] = -beta
    return Q


def precision_from_edges(n, edges, alpha=1.0, beta=1.0):
    Q = np.eye(n) * alpha
    deg = np.zeros(n)
    for i, j in edges:
        deg[i] += 1
        deg[j] += 1
        Q[i, j] -= beta
        Q[j, i] -= beta
    for i in range(n):
        Q[i, i] += beta * deg[i]
    return Q


def conditional_cov(Sigma, target, given):
    target = np.asarray(target, dtype=int)
    given = np.asarray(given, dtype=int)
    tt = Sigma[np.ix_(target, target)]
    if given.size == 0:
        return tt.copy()
    tg = Sigma[np.ix_(target, given)]
    gg = Sigma[np.ix_(given, given)]
    return tt - tg @ solve(gg, tg.T)


def scalar_var(Sigma, i, given):
    return float(conditional_cov(Sigma, [i], given)[0, 0])


def pair_mi(Sigma, i, j, given):
    c = conditional_cov(Sigma, [i, j], given)
    rho2 = (c[0, 1] ** 2) / (c[0, 0] * c[1, 1])
    rho2 = min(max(float(rho2), 0.0), 1.0 - 1e-16)
    return -0.5 * math.log(1.0 - rho2), float(c[0, 1] / math.sqrt(c[0, 0] * c[1, 1]))


def holding_bound(Q, sites):
    sites = list(sites)
    return float(sum(1.0 / EPS - Q[i, i] for i in sites))


def uniform_diagonal_load(Q, sites):
    sites = np.asarray(list(sites), dtype=int)
    lo, hi = 0.0, 1.0 / EPS
    for _ in range(20):
        M = Q.copy()
        M[sites, sites] += hi
        smax = float(np.max(np.diag(inv(M))[sites]))
        if smax <= EPS:
            break
        hi *= 2.0
    else:
        raise RuntimeError("diagonal load did not meet the tolerance")
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        M = Q.copy()
        M[sites, sites] += mid
        smax = float(np.max(np.diag(inv(M))[sites]))
        if smax <= EPS:
            hi = mid
        else:
            lo = mid
    M = Q.copy()
    M[sites, sites] += hi
    smax = float(np.max(np.diag(inv(M))[sites]))
    return float(len(sites) * hi), float(hi), smax


def build_gasket(g):
    if g == 0:
        return {"n": 3, "edges": [(0, 1), (1, 2), (2, 0)], "corners": (0, 1, 2)}
    sub = build_gasket(g - 1)
    n = sub["n"]
    c = sub["corners"]
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for copy in range(3):
        for v in range(n):
            find((copy, v))
    union((0, c[1]), (1, c[0]))
    union((1, c[2]), (2, c[1]))
    union((2, c[0]), (0, c[2]))
    idx = {}
    for copy in range(3):
        for v in range(n):
            r = find((copy, v))
            if r not in idx:
                idx[r] = len(idx)
    edges = set()
    for copy in range(3):
        for a, b in sub["edges"]:
            ia = idx[find((copy, a))]
            ib = idx[find((copy, b))]
            if ia != ib:
                edges.add((ia, ib) if ia < ib else (ib, ia))
    corners = (
        idx[find((0, c[0]))],
        idx[find((1, c[1]))],
        idx[find((2, c[2]))],
    )
    copy0 = sorted({idx[find((0, v))] for v in range(n)})
    glue = (idx[find((0, c[1]))], idx[find((0, c[2]))])
    return {
        "n": len(idx),
        "edges": sorted(edges),
        "corners": corners,
        "copy0": copy0,
        "glue": glue,
    }


def open_square(n):
    edges = []

    def idx(x, y):
        return y * n + x

    for y in range(n):
        for x in range(n):
            if x + 1 < n:
                edges.append((idx(x, y), idx(x + 1, y)))
            if y + 1 < n:
                edges.append((idx(x, y), idx(x, y + 1)))
    return n * n, edges


def mod_bessel(d, z, terms=80):
    """I_d(z) for integer d >= 0, series."""
    half = 0.5 * z
    # (z/2)^d / d!
    log_term = d * math.log(half) - math.lgamma(d + 1)
    term = math.exp(log_term)
    total = term
    for m in range(terms):
        # multiply by (z/2)^2 / ((m+1)(m+1+d))
        term *= half * half / ((m + 1) * (m + 1 + d))
        total += term
        if term < total * 1e-18:
            break
    return total


def bessel_second_moment(t, radius=40):
    # p_d = exp(-2t) I_|d|(2t), second moment 2t
    weight = math.exp(-2.0 * t)
    arg = 2.0 * t
    m0 = weight * mod_bessel(0, arg)
    moment = 0.0
    mass = m0
    for d in range(1, radius + 1):
        p = weight * mod_bessel(d, arg)
        mass += 2.0 * p
        moment += 2.0 * (d * d) * p
    return moment, mass


def kernel_entry_positive(dist, tau):
    # e^{-3 tau} I_dist(2 tau) > 0 for tau > 0
    val = math.exp(-3.0 * tau) * mod_bessel(dist, 2.0 * tau)
    return val > 0.0, val


def expm_symmetric(A):
    """Exponential of a real symmetric matrix, via its eigenvalues."""
    w, U = np.linalg.eigh(A)
    return (U * np.exp(w)) @ U.T


def radius_ratio(n, tau_a, tau_b, eta=0.05):
    Q = path_precision(n)
    Sigma = inv(Q)
    center = n // 2

    def delta(tau):
        kernel = expm_symmetric(-tau * Q)
        w = kernel[center]
        out = []
        for r in range(center + 1):
            ball = [i for i in range(n) if abs(i - center) <= r]
            given = ball
            # variance of w·X given the ball = quadratic form on the complement
            mask = np.ones(n, dtype=bool)
            mask[given] = False
            outside = np.flatnonzero(mask)
            if outside.size == 0:
                out.append(0.0)
                continue
            cov = conditional_cov(Sigma, outside, given)
            wo = w[outside]
            out.append(float(wo @ cov @ wo))
        return out

    da = delta(tau_a)
    db = delta(tau_b)

    def first(ds):
        base = ds[0]
        for r, val in enumerate(ds):
            if val <= eta * base:
                return r, val, base
        return None, ds[-1], base

    ra, _, _ = first(da)
    rb, _, _ = first(db)
    return da, db, ra, rb


def log_linear_crossing(ds, level=0.05):
    """First log-linear crossing of Delta(r)/Delta(0) through `level`.

    Returns (r_star, k, rho_k, rho_next) or None.
    """
    if not ds or ds[0] <= 0.0:
        return None
    rhos = [float(v) / float(ds[0]) for v in ds]
    for k in range(len(rhos) - 1):
        if rhos[k] >= level > rhos[k + 1] and rhos[k + 1] > 0.0:
            num = math.log(rhos[k]) - math.log(level)
            den = math.log(rhos[k]) - math.log(rhos[k + 1])
            if den == 0.0:
                return None
            return (k + num / den, k, rhos[k], rhos[k + 1])
    return None


def check_crossing():
    """PREREG_CROSSING.md, commit 8afc11f. Times 1/4 and 1, path 61."""
    da, db, _, _ = radius_ratio(61, 0.25, 1.0, eta=0.05)
    ca = log_linear_crossing(da)
    cb = log_linear_crossing(db)
    if ca is None or cb is None or ca[0] <= 0.0:
        puzzle("C1 log-linear crossing", False, "missing %s %s" % (ca, cb))
        print("INFO  C1 missing")
        return
    ra, ka, rho_a0, rho_a1 = ca
    rb, kb, rho_b0, rho_b1 = cb
    ratio = rb / ra
    in_band = 1.7 <= ratio <= 2.3 and ka <= 28 and kb <= 28
    puzzle(
        "C1 log-linear crossing ratio",
        in_band,
        "r(1/4)=%.12f r(1)=%.12f ratio %.12f" % (ra, rb, ratio),
    )
    print(
        "INFO  C1 k=%d rho %.12e -> %.12e | k=%d rho %.12e -> %.12e"
        % (ka, rho_a0, rho_a1, kb, rho_b0, rho_b1)
    )


def random_excess(Q, region, blanket, draws, rng):
    """Excess of the matching blanket channel over a random channel on R∪B."""
    region = list(region)
    blanket = list(blanket)
    support = region + blanket
    k = len(support)
    Sigma = inv(Q)
    B = np.asarray(blanket, dtype=int)
    pi0 = inv(Sigma[np.ix_(B, B)])
    K = None
    if region:
        I = np.asarray(region, dtype=int)
        Qbi = Q[np.ix_(B, I)]
        Ktr = float(np.trace(Qbi @ solve(Q[np.ix_(I, I)], Qbi.T)))
    else:
        Ktr = 0.0
    worst = -1e300
    worst_detail = ""
    for draw in range(draws):
        A = rng.normal(scale=0.4, size=(k, k))
        phi_s = A.T @ A
        Phi = np.zeros_like(Q)
        for a, i in enumerate(support):
            for b, j in enumerate(support):
                Phi[i, j] = phi_s[a, b]
        P = Q + Phi
        VB = inv(P)[np.ix_(B, B)]
        # jitter if a draw is singular
        try:
            pi = inv(VB)
        except np.linalg.LinAlgError:
            continue
        Delta = pi - pi0
        excess = float(np.trace(Delta) - np.trace(Phi))
        if excess > worst:
            worst = excess
            worst_detail = "draw %d excess %.12f cap %.12f" % (draw, excess, Ktr)
    return worst, Ktr, worst_detail


def check_path3():
    Q = path_precision(3)
    Sigma = inv(Q)
    locked_sigma = np.array([[5, 2, 1], [2, 4, 2], [1, 2, 5]], dtype=float) / 8.0
    check("P1 covariance", np.max(np.abs(Sigma - locked_sigma)) < 1e-12,
          "max abs %.3e" % np.max(np.abs(Sigma - locked_sigma)))
    v_b = scalar_var(Sigma, 2, [1])
    v_rb = scalar_var(Sigma, 2, [0, 1])
    v_r = scalar_var(Sigma, 2, [0])
    v_int = scalar_var(Sigma, 0, [1])
    check("P1 Var(X2|X1)=1/2", absnear(v_b, 0.5), "got %.12f" % v_b)
    check("P1 Var(X2|X0,X1)=1/2", absnear(v_rb, 0.5), "got %.12f" % v_rb)
    check("P1 Var(X2|X0)=3/5", absnear(v_r, 0.6), "got %.12f" % v_r)
    check("P1 Var(X0|X1)=1/2", absnear(v_int, 0.5), "got %.12f" % v_int)
    mi, _ = pair_mi(Sigma, 0, 2, [])
    mi_c, rho_c = pair_mi(Sigma, 0, 2, [1])
    target = 0.5 * math.log(25.0 / 24.0)
    check("P1 I(X0;X2)", absnear(mi, target, 1e-12), "got %.12f target %.12f" % (mi, target))
    check("P1 I(X0;X2|X1)=0", absnear(mi_c, 0.0, 1e-12) and abs(rho_c) < 1e-12,
          "I %.3e rho %.3e" % (mi_c, rho_c))

    def var_phi_psi(phi, psi):
        P = Q.copy()
        P[1, 1] += phi
        P[0, 0] += psi
        return float(inv(P)[2, 2])

    v_phi = var_phi_psi(2.0, 0.0)
    v_both = var_phi_psi(1.0, 1.0)
    check("P2 phi=2 is 9/16", absnear(v_phi, 9.0 / 16.0), "got %.12f" % v_phi)
    check("P2 phi=1,psi=1 is 11/19", absnear(v_both, 11.0 / 19.0), "got %.12f" % v_both)
    check("P2 gap 5/304 and boundary spend wins",
          absnear(v_both - v_phi, 5.0 / 304.0) and v_phi < v_both,
          "gap %.12e" % (v_both - v_phi))

    P = Q.copy()
    P[0, 0] += 0.1
    P[0, 1] += 1.0
    P[1, 0] += 1.0
    P[1, 1] += 10.0
    post = inv(P)
    check("P3 trace 10.1", absnear(np.trace(P - Q), 10.1), "tr %.12f" % np.trace(P - Q))
    check("P3 Var(X2)=13/25", absnear(post[2, 2], 13.0 / 25.0), "got %.12f" % post[2, 2])
    check("P3 Var(X1)=2/25", absnear(post[1, 1], 2.0 / 25.0), "got %.12f" % post[1, 1])
    # blanket-only match of Var(X1)=2/25: phi = 1/v - 2 = 10.5
    Pb = Q.copy()
    Pb[1, 1] += 10.5
    post_b = inv(Pb)
    check("P3 blanket-only trace 10.5 matches blanket variance",
          absnear(post_b[1, 1], 2.0 / 25.0) and absnear(post_b[2, 2], 13.0 / 25.0),
          "vB %.12f vE %.12f" % (post_b[1, 1], post_b[2, 2]))
    excess = 10.5 - 10.1
    check("P3 exhibited excess 0.4 inside the cap 1/2",
          absnear(excess, 0.4) and excess <= 0.5 + 1e-8,
          "excess %.12f" % excess)

    rng = np.random.default_rng(7)
    worst, cap, detail = random_excess(Q, [0], [1], 40, rng)
    check("P3 random excess <= 1/2", worst <= 0.5 + 1e-8, "%s" % detail)


def check_path5():
    Q = path_precision(5)
    Sigma = inv(Q)
    d = [1, 2, 5, 13, 34]
    formula = np.zeros((5, 5))
    for i in range(5):
        for j in range(5):
            a, b = (i, j) if i <= j else (j, i)
            formula[i, j] = d[a] * d[4 - b] / 55.0
    check("P4 covariance formula", np.max(np.abs(Sigma - formula)) < 1e-12,
          "max abs %.3e" % np.max(np.abs(Sigma - formula)))
    v_sep = scalar_var(Sigma, 0, [1])
    check("P4 Var(X0|X1)=1/2", absnear(v_sep, 0.5), "got %.12f" % v_sep)
    # pooled sum S = X1+X3
    var_s = Sigma[1, 1] + Sigma[3, 3] + 2 * Sigma[1, 3]
    cov0 = Sigma[0, 1] + Sigma[0, 3]
    cov4 = Sigma[4, 1] + Sigma[4, 3]
    v0 = Sigma[0, 0] - cov0 ** 2 / var_s
    v4 = Sigma[4, 4] - cov4 ** 2 / var_s
    check("P4 Var(X0|X1+X3)=121/220", absnear(v0, 121.0 / 220.0), "got %.12f" % v0)
    both = scalar_var(Sigma, 0, [1, 3]) + scalar_var(Sigma, 4, [1, 3])
    pooled = v0 + v4
    check("P4 per-site gap -1/10", absnear(both - pooled, -0.1),
          "both %.12f pooled %.12f gap %.12f" % (both, pooled, both - pooled))
    v_int = scalar_var(Sigma, 2, [1, 3])
    check("P4 Var(X2|X1,X3)=1/3", absnear(v_int, 1.0 / 3.0), "got %.12f" % v_int)
    # sum Z is screened by S
    c_both = conditional_cov(Sigma, [0, 4], [1, 3])
    var_z_both = float(c_both.sum())
    var_z = Sigma[0, 0] + Sigma[4, 4] + 2 * Sigma[0, 4]
    cov_z = cov0 + cov4
    var_z_s = var_z - cov_z ** 2 / var_s
    check("P4 sum of the ends matches the pooled blanket",
          absnear(var_z_both, var_z_s, 1e-12),
          "both %.12f sum %.12f" % (var_z_both, var_z_s))
    Ktr = float(Q[1, 2] ** 2 / Q[2, 2] + Q[3, 2] ** 2 / Q[2, 2])
    # tr(Q_BI Q_II^{-1} Q_IB) = (1/3) * tr([[1,1],[1,1]]) = 2/3
    check("P4 tr(K)=2/3", absnear(Ktr, 2.0 / 3.0), "got %.12f" % Ktr)
    b_bound = holding_bound(Q, [1, 3])
    r_bound = holding_bound(Q, [2])
    check("P4 holding bounds 30 and 15", absnear(b_bound, 30.0) and absnear(r_bound, 15.0),
          "B %.6f R %.6f" % (b_bound, r_bound))
    rng = np.random.default_rng(11)
    worst, cap, detail = random_excess(Q, [2], [1, 3], 30, rng)
    check("P4 random excess <= 2/3", worst <= cap + 1e-7, "%s" % detail)


def check_breaks():
    Q = path_precision(3)
    Q[0, 0] += 1.0
    Q[2, 2] += 1.0
    Q[0, 2] -= 1.0
    Q[2, 0] -= 1.0
    Sigma = inv(Q)
    mi, rho = pair_mi(Sigma, 0, 2, [1])
    target = 0.5 * math.log(9.0 / 8.0)
    check("P5 long-range I=(1/2)ln(9/8)", absnear(mi, target, 1e-12),
          "I %.12f" % mi)
    check("P5 partial correlation 1/3", absnear(rho, 1.0 / 3.0), "rho %.12f" % rho)
    Q0 = path_precision(3)
    mi0, _ = pair_mi(inv(Q0), 0, 2, [1])
    check("P5 gamma=0 screens", absnear(mi0, 0.0, 1e-12), "I %.3e" % mi0)

    Sigma_eq = np.full((3, 3), 0.5)
    np.fill_diagonal(Sigma_eq, 1.0)
    mi_eq, rho_eq = pair_mi(Sigma_eq, 0, 2, [1])
    check("P6 equicorrelated I", absnear(mi_eq, target, 1e-12), "I %.12f" % mi_eq)
    check("P6 partial correlation 1/3", absnear(rho_eq, 1.0 / 3.0), "rho %.12f" % rho_eq)

    # MA(1): Var 2, adjacent cov 1, lag-2 cov 0
    Sigma_ma = np.array([[2.0, 1.0, 0.0], [1.0, 2.0, 1.0], [0.0, 1.0, 2.0]])
    mi_ma, rho_ma = pair_mi(Sigma_ma, 0, 2, [1])
    corr_uncond = Sigma_ma[0, 2] / 2.0
    check("P7 MA(1) unconditional correlation 0", absnear(corr_uncond, 0.0), "")
    check("P7 MA(1) conditional I", absnear(mi_ma, target, 1e-12), "I %.12f" % mi_ma)
    check("P7 MA(1) conditional correlation -1/3", absnear(rho_ma, -1.0 / 3.0),
          "rho %.12f" % rho_ma)


def transition_range1(n):
    S = np.zeros((n, n))
    for i in range(n):
        S[i, i] = 0.5
        if i - 1 >= 0:
            S[i, i - 1] = 0.25
        if i + 1 < n:
            S[i, i + 1] = 0.25
    return S


def transition_range2(n):
    S = np.zeros((n, n))
    for i in range(n):
        S[i, i] = 0.5
        for dist, w in ((1, 1.0 / 6.0), (2, 1.0 / 6.0)):
            if i - dist >= 0:
                S[i, i - dist] = w
            if i + dist < n:
                S[i, i + dist] = w
    return S


def check_finite_speed():
    # Horizon H on a path long enough that the far coefficient is interior.
    cases = [(1, 1.0 / 16.0), (2, 1.0 / 256.0), (3, 1.0 / 4096.0)]
    for H, excess in cases:
        n = H + 3
        S = transition_range1(n)
        SH = np.linalg.matrix_power(S, H)
        coeff = float(SH[0, H])
        # sites beyond H
        beyond = float(np.max(np.abs(SH[0, H + 1 :]))) if H + 1 < n else 0.0
        check("P8 H=%d excess" % H, absnear(coeff ** 2, excess, 1e-15),
              "coeff %.12e excess %.12e" % (coeff, coeff ** 2))
        check("P8 H=%d no mass beyond" % H, beyond == 0.0 or beyond < 1e-15,
              "max beyond %.3e" % beyond)
    S2 = transition_range2(8)
    c1 = float(S2[0, 2])
    beyond1 = float(np.max(np.abs(S2[0, 3:])))
    check("P8 range2 H=1 coeff 1/6", absnear(c1, 1.0 / 6.0), "got %.12f" % c1)
    check("P8 range2 H=1 excess 1/36", absnear(c1 ** 2, 1.0 / 36.0), "")
    check("P8 range2 H=1 cutoff", beyond1 < 1e-15, "beyond %.3e" % beyond1)
    S2H = S2 @ S2
    c2 = float(S2H[0, 4])
    beyond2 = float(np.max(np.abs(S2H[0, 5:])))
    check("P8 range2 H=2 coeff 1/36", absnear(c2, 1.0 / 36.0), "got %.12e" % c2)
    check("P8 range2 H=2 excess 1/1296", absnear(c2 ** 2, 1.0 / 1296.0, 1e-12),
          "got %.12e" % (c2 ** 2))
    check("P8 range2 H=2 thickness 4", beyond2 < 1e-12, "beyond %.3e" % beyond2)


def check_continuous():
    m_half, mass_half = bessel_second_moment(0.5)
    m_two, mass_two = bessel_second_moment(2.0)
    check("P9 second moment at t=1/2", absnear(m_half, 1.0, 1e-10),
          "moment %.12f mass %.12f" % (m_half, mass_half))
    check("P9 second moment at t=2", absnear(m_two, 4.0, 1e-10),
          "moment %.12f mass %.12f" % (m_two, mass_two))
    check("P9 kernel mass", absnear(mass_half, 1.0, 1e-10) and absnear(mass_two, 1.0, 1e-10),
          "")
    # nonzero at large distance
    ok_pos = True
    smallest = 1e300
    for tau in (0.5, 1.0):
        for dist in (1, 5, 15):
            pos, val = kernel_entry_positive(dist, tau)
            ok_pos = ok_pos and pos
            smallest = min(smallest, val)
    check("P9 infinite-path kernel positive", ok_pos, "smallest printed %.3e" % smallest)

    da, db, ra, rb = radius_ratio(31, 0.5, 1.0)
    # strict positivity of Delta(r) for r < 15, and Delta(15)=0
    def positive_prefix(ds):
        if abs(ds[-1]) > 1e-18:
            return False, ds[-1]
        return all(v > 0.0 for v in ds[:-1]), min(ds[:-1])

    ok_a, min_a = positive_prefix(da)
    ok_b, min_b = positive_prefix(db)
    check("P9 Delta(r)>0 for r<15 at tau=1/2", ok_a, "min %.6e end %.3e" % (min_a, da[-1]))
    check("P9 Delta(r)>0 for r<15 at tau=1", ok_b, "min %.6e end %.3e" % (min_b, db[-1]))
    if ra is None or rb is None or ra == 0:
        puzzle("P9 radius ratio", False, "radii %s %s (path too short or undefined)" % (ra, rb))
        ratio = float("nan")
    else:
        ratio = rb / ra
        # tolerance: puzzle if >= 1.7 or <= 1.05; also puzzle if a radius hits the end
        hit_end = ra >= 15 or rb >= 15
        in_band = (1.05 < ratio < 1.7) and not hit_end
        puzzle("P9 radius ratio", in_band,
               "r(1/2)=%s r(1)=%s ratio %.6f" % (ra, rb, ratio))
    print("INFO  P9 Delta(tau=1/2) " + " ".join("%.4e" % v for v in da))
    print("INFO  P9 Delta(tau=1) " + " ".join("%.4e" % v for v in db))
    # Named next test in the preregistration. It does not replace the locked gate.
    d61a, d61b, r61a, r61b = radius_ratio(61, 0.5, 1.0)
    if r61a and r61b and r61a > 0:
        print("INFO  P9 next-test n=61 r(1/2)=%d r(1)=%d ratio %.6f" % (r61a, r61b, r61b / r61a))
    else:
        print("INFO  P9 next-test n=61 radii %s %s" % (r61a, r61b))
    return ratio if ra and rb else float("nan"), ra, rb


def screen_identity(Q, region, blanket, exterior):
    Sigma = inv(Q)
    c_b = conditional_cov(Sigma, exterior, blanket)
    c_rb = conditional_cov(Sigma, exterior, list(region) + list(blanket))
    gap = float(np.max(np.abs(c_b - c_rb)))
    Qrr = Q[np.ix_(region, region)]
    pred = np.diag(inv(Qrr))
    got = np.diag(conditional_cov(Sigma, region, blanket))
    iv_gap = float(np.max(np.abs(pred - got)))
    iv_min = float(np.min(got))
    return gap, iv_gap, iv_min


def check_gasket_and_square():
    expected = {2: (4, 26.0, 54.0), 3: (13, 26.0, 171.0), 4: (40, 26.0, 522.0), 5: (121, 26.0, 1575.0)}
    loads = []
    for g, (nR, b_lock, r_lock) in expected.items():
        G = build_gasket(g)
        N = 3 * (3 ** g + 1) / 2
        check("P10 g=%d count" % g, G["n"] == int(N), "n=%d" % G["n"])
        Q = precision_from_edges(G["n"], G["edges"])
        glue = list(G["glue"])
        copy0 = set(G["copy0"])
        region = sorted(copy0 - set(glue))
        blanket = glue
        exterior = sorted(set(range(G["n"])) - copy0)
        check("P10 g=%d |R|" % g, len(region) == nR, "|R|=%d" % len(region))
        check("P10 g=%d |B|=2" % g, len(set(blanket)) == 2, "%s" % (blanket,))
        degrees = np.zeros(G["n"])
        for a, b in G["edges"]:
            degrees[a] += 1
            degrees[b] += 1
        check("P10 g=%d glue degree 4" % g,
              degrees[blanket[0]] == 4 and degrees[blanket[1]] == 4,
              "deg %s %s" % (degrees[blanket[0]], degrees[blanket[1]]))
        b_bound = holding_bound(Q, blanket)
        r_bound = holding_bound(Q, region)
        check("P10 g=%d bounds" % g,
              absnear(b_bound, b_lock) and absnear(r_bound, r_lock),
              "B %.6f R %.6f" % (b_bound, r_bound))
        gap, iv_gap, iv_min = screen_identity(Q, region, blanket, exterior)
        check("P10 g=%d exterior law" % g, gap < 1e-8, "entry gap %.3e" % gap)
        check("P10 g=%d interior is Q_RR^{-1}" % g, iv_gap < 1e-8, "gap %.3e" % iv_gap)
        check("P10 g=%d interior floor >= 1/5" % g, iv_min >= 0.2 - 1e-12,
              "min %.12f" % iv_min)
        heat_b, phi_b, smax_b = uniform_diagonal_load(Q, blanket)
        heat_r, phi_r, smax_r = uniform_diagonal_load(Q, region)
        I = np.asarray(region, dtype=int)
        Bix = np.asarray(blanket, dtype=int)
        Qbi = Q[np.ix_(Bix, I)]
        Ktr = float(np.trace(Qbi @ solve(Q[np.ix_(I, I)], Qbi.T)))
        check("P10 g=%d load meets tolerance" % g,
              smax_b <= EPS + 1e-9 and smax_r <= EPS + 1e-9 and heat_b + 1e-8 >= b_bound,
              "blanket %.6f (bound %.1f) region %.6f" % (heat_b, b_bound, heat_r))
        # The Schur cap is not a locked digit. It is printed, and it is required
        # only to stay below 2 while the region bound is the locked volume figure.
        check("P10 g=%d Schur cap below 2" % g, Ktr < 2.0,
              "tr(K)=%.12f" % Ktr)
        loads.append((g, heat_b, phi_b, heat_r, iv_min, len(exterior), Ktr))
        # excess cap on a modest generation
        if g == 2:
            rng = np.random.default_rng(19)
            worst, cap, detail = random_excess(Q, region, blanket, 15, rng)
            check("P10 g=2 excess <= tr(K)", worst <= cap + 1e-6, "%s" % detail)
    return loads


def check_square():
    n = 8
    N, edges = open_square(n)
    Q = precision_from_edges(N, edges)

    def idx(x, y):
        return y * n + x

    region, blanket, exterior = [], [], []
    for y in range(n):
        for x in range(n):
            i = idx(x, y)
            if x <= 2:
                region.append(i)
            elif x == 3:
                blanket.append(i)
            else:
                exterior.append(i)
    check("P11 sizes", len(region) == 24 and len(blanket) == 8 and len(exterior) == 32,
          "|R| %d |B| %d |E| %d" % (len(region), len(blanket), len(exterior)))
    b_bound = holding_bound(Q, blanket)
    r_bound = holding_bound(Q, region)
    check("P11 bounds 106 and 326", absnear(b_bound, 106.0) and absnear(r_bound, 326.0),
          "B %.6f R %.6f" % (b_bound, r_bound))
    gap, iv_gap, iv_min = screen_identity(Q, region, blanket, exterior)
    check("P11 exterior law", gap < 1e-8, "entry gap %.3e" % gap)
    check("P11 interior is Q_RR^{-1}", iv_gap < 1e-8, "gap %.3e" % iv_gap)
    check("P11 interior floor >= 1/5", iv_min >= 0.2 - 1e-12, "min %.12f" % iv_min)
    heat_b, phi_b, smax = uniform_diagonal_load(Q, blanket)
    check("P11 blanket load above the bound",
          smax <= EPS + 1e-9 and heat_b + 1e-6 >= 106.0,
          "heat %.6f phi %.6f smax %.6e" % (heat_b, phi_b, smax))
    return heat_b, phi_b, iv_min


def check_pool():
    from fractions import Fraction
    # decision variance at survivor count k
    def eps(k):
        return Fraction(1, 2) + Fraction(1, 4 * (2 + k))

    check("P12 one unit is 7/12", eps(1) == Fraction(7, 12), "%s" % eps(1))
    check("P12 three units meet 0.55", eps(3) == Fraction(11, 20) and eps(3) <= Fraction(55, 100),
          "%s" % eps(3))
    # 0.55 = 11/20
    check("P12 copy never meets", all(eps(k) > Fraction(11, 20) for k in range(0, 3)),
          "eps0 %s eps1 %s eps2 %s" % (eps(0), eps(1), eps(2)))

    def chance(n):
        # P(K>=3), K~Bin(n, 4/5)
        total = 0
        den = 5 ** n
        for k in range(3, n + 1):
            ways = math.comb(n, k) * (4 ** k)
            total += ways
        return Fraction(total, den)

    c5 = chance(5)
    c6 = chance(6)
    check("P12 n=5 chance 2944/3125", c5 == Fraction(2944, 3125), "%s" % c5)
    check("P12 n=6 chance 15360/15625", c6 == Fraction(15360, 15625), "%s" % c6)
    check("P12 five misses and six meets",
          c5 < Fraction(95, 100) and c6 >= Fraction(95, 100),
          "c5 %.6f c6 %.6f" % (float(c5), float(c6)))
    # smallest in 1..8
    feasible = [n for n in range(1, 9) if chance(n) >= Fraction(95, 100)]
    check("P12 smallest count is 6", feasible and feasible[0] == 6, "%s" % feasible)
    expect = sum(chance_term(6, k) * eps(k) for k in range(0, 7))
    # rebuild with the same denominator convention
    check("P12 expected error", expect == Fraction(470459, 875000),
          "%s vs %s" % (expect, Fraction(470459, 875000)))
    cost = 9 + expect
    check("P12 cost", cost == Fraction(8345459, 875000), "%s" % cost)


def chance_term(n, k):
    from fractions import Fraction
    return Fraction(math.comb(n, k) * (4 ** k), 5 ** n)


def main():
    check_path3()
    check_path5()
    check_breaks()
    check_finite_speed()
    ratio, ra, rb = check_continuous()
    check_crossing()
    loads = check_gasket_and_square()
    heat_b, phi_b, iv_min = check_square()
    check_pool()
    print("---")
    for row in loads:
        print("LOAD gasket g=%d blanket %.8f phi %.8f region %.8f interior_min %.8f exterior %d trK %.12f" % row)
    print("LOAD square blanket %.8f phi %.8f interior_min %.8f" % (heat_b, phi_b, iv_min))
    print("RATIO r05 %s %s" % (ra, rb))
    print("PASS %d  FAIL %d  PUZZLES %d" % (PASS, FAIL, PUZZLES))
    if FAIL == 0:
        print("FAILS 0")
        print("ALL BOUNDARY SUFFICIENCY CHECKS PASS")
        return 0
    print("FAILS %d" % FAIL)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
