#!/usr/bin/env python3
"""Independent recomputation of the boundary-sufficiency load-bearing numbers.

Does not import theory/boundary_checks. Algebra on the paths, the leaks, and
the pool is exact (fractions). The gasket Schur trace and the log-linear
crossing are computed from the preregistered definitions, with a second
algorithm for the crossing.
"""
from __future__ import annotations

import math
from fractions import Fraction

import numpy as np


def show(title, value):
    print("%s\t%s" % (title, value))


# ---------------------------------------------------------------------------
# Exact linear algebra on small rational matrices
# ---------------------------------------------------------------------------

def eye(n):
    return [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]


def matmul(A, B):
    n, p, m = len(A), len(B), len(B[0])
    out = [[Fraction(0) for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for k in range(p):
            if A[i][k] == 0:
                continue
            for j in range(m):
                out[i][j] += A[i][k] * B[k][j]
    return out


def transpose(A):
    return [list(col) for col in zip(*A)]


def solve(A, b):
    """Solve A x = b for a square rational matrix. b is a list of columns."""
    n = len(A)
    M = [[Fraction(v) for v in row] + [Fraction(v) for v in rhs] for row, rhs in zip(A, b)]
    width = n + len(b[0])
    for col in range(n):
        pivot = next(r for r in range(col, n) if M[r][col] != 0)
        M[col], M[pivot] = M[pivot], M[col]
        piv = M[col][col]
        M[col] = [v / piv for v in M[col]]
        for r in range(n):
            if r == col or M[r][col] == 0:
                continue
            factor = M[r][col]
            M[r] = [M[r][c] - factor * M[col][c] for c in range(width)]
    return [row[n:] for row in M]


def inverse(A):
    return solve(A, eye(len(A)))


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def path_precision_exact(n):
    Q = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        deg = (1 if i else 0) + (1 if i + 1 < n else 0)
        Q[i][i] = Fraction(1 + deg)
        if i + 1 < n:
            Q[i][i + 1] = Q[i + 1][i] = Fraction(-1)
    return Q


def conditional_variance(Sigma, i, given):
    """Scalar conditional variance of coordinate i given `given`."""
    if not given:
        return Sigma[i][i]
    idx = list(given)
    Sgg = [[Sigma[a][b] for b in idx] for a in idx]
    s_ig = [[Sigma[i][b] for b in idx]]
    coef = solve(Sgg, transpose(s_ig))  # |given| x 1
    explained = Fraction(0)
    for a, row in enumerate(coef):
        explained += s_ig[0][a] * row[0]
    return Sigma[i][i] - explained


def partial_corr_and_info(Sigma, i, j, given):
    """Conditional correlation and mutual information of two scalars."""
    idx = [i, j]
    # conditional 2x2 via the Schur complement of the covariance
    block = [i, j] + list(given)
    # Build the conditional covariance of (i, j) given `given`.
    if not given:
        C = [[Sigma[a][b] for b in idx] for a in idx]
    else:
        Sgg = [[Sigma[a][b] for b in given] for a in given]
        Sig = [[Sigma[a][b] for b in given] for a in idx]
        coef = solve(Sgg, transpose(Sig))  # |given| x 2
        explained = matmul(Sig, coef)
        full = [[Sigma[a][b] for b in idx] for a in idx]
        C = [[full[a][b] - explained[a][b] for b in range(2)] for a in range(2)]
    rho_sq = (C[0][1] * C[0][1]) / (C[0][0] * C[1][1])
    # signed rho: sign of the covariance, magnitude sqrt(rho_sq)
    sign = 1 if C[0][1] > 0 else (-1 if C[0][1] < 0 else 0)
    rho_f = sign * math.sqrt(float(rho_sq))
    info = -0.5 * math.log(1.0 - float(rho_sq)) if rho_sq < 1 else float("inf")
    return C, rho_sq, rho_f, info


def section_path_three():
    print("\n== path of three, exact ==")
    Q = path_precision_exact(3)
    Sigma = inverse(Q)
    show("Sigma", Sigma)
    v_blanket = conditional_variance(Sigma, 2, [1])
    v_both = conditional_variance(Sigma, 2, [0, 1])
    v_region = conditional_variance(Sigma, 2, [0])
    v_interior = conditional_variance(Sigma, 0, [1])
    show("Var(X2|X1)", v_blanket)
    show("Var(X2|X0,X1)", v_both)
    show("Var(X2|X0)", v_region)
    show("Var(X0|X1)", v_interior)
    # laws: conditional mean of X2. Given X1 only, coefficient is Sigma_21/Sigma_11.
    # Given X0 and X1, the precision formula uses the conditional precision Q_EE=2
    # and the cross row of Q, which has a zero in the region column.
    mean_coef_blanket = Sigma[2][1] / Sigma[1][1]
    # Solve the conditional mean from the joint precision of (X0,X2) is not needed:
    # mean of X2 | X0, X1 equals -Q_2,{0,1} / Q_22 because we condition on both
    # and the conditional precision of the single exterior site is Q_22.
    mean_coef_region = -Q[2][0] / Q[2][2]
    mean_coef_blanket_from_Q = -Q[2][1] / Q[2][2]
    show("mean coef of X2 on X1 (covariance)", mean_coef_blanket)
    show("mean coef of X2 on X0 | X0,X1 (precision)", mean_coef_region)
    show("mean coef of X2 on X1 | X0,X1 (precision)", mean_coef_blanket_from_Q)
    C, rho_sq, rho, info = partial_corr_and_info(Sigma, 0, 2, [])
    show("I(X0;X2) = 1/2 ln(25/24)", info)
    show("target 1/2 ln(25/24)", 0.5 * math.log(25 / 24))
    C0, rho_sq0, rho0, info0 = partial_corr_and_info(Sigma, 0, 2, [1])
    show("I(X0;X2|X1)", info0)
    show("conditional rho^2", rho_sq0)
    return {
        "var_region_alone": v_region,
        "var_blanket": v_blanket,
        "var_region_and_blanket": v_both,
        "screen_equal": v_blanket == v_both,
        "not_region_alone": v_region != v_blanket,
    }


def section_channel():
    print("\n== blanket channel excess, exact ==")
    Q = path_precision_exact(3)
    Phi = [
        [Fraction(1, 10), Fraction(1), Fraction(0)],
        [Fraction(1), Fraction(10), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0)],
    ]
    P = [[Q[i][j] + Phi[i][j] for j in range(3)] for i in range(3)]
    post = inverse(P)
    tr_phi = trace(Phi)
    var_b = post[1][1]
    var_e = post[2][2]
    # Prior marginal precision of the blanket site is 1/Var(X1) = 2.
    Sigma = inverse(Q)
    prior_prec = 1 / Sigma[1][1]
    post_prec = 1 / var_b
    blanket_trace = post_prec - prior_prec
    excess = blanket_trace - tr_phi
    # Schur trace tr(Q_BI Q_II^{-1} Q_IB), I={0}, B={1}.
    # Q_BI is the scalar Q[1][0] = -1, Q_II = 2.
    cap = (Q[1][0] * Q[0][1]) / Q[0][0]
    # Algebraic excess identity: tr(K(0)) - tr(K(Phi)) - tr(Phi_II).
    # K(Phi) = (Q_BI + Phi_BI) (Q_II + Phi_II)^{-1} (Q_IB + Phi_IB)
    k_phi = (Q[1][0] + Phi[1][0]) ** 2 / (Q[0][0] + Phi[0][0])
    k0 = cap
    excess_identity = k0 - k_phi - Phi[0][0]
    # Matching blanket channel: add `blanket_trace` on site 1 only.
    Pb = [row[:] for row in Q]
    Pb[1][1] += blanket_trace
    post_b = inverse(Pb)
    show("trace Phi", tr_phi)
    show("Var blanket posterior", var_b)
    show("Var exterior posterior", var_e)
    show("matching blanket trace", blanket_trace)
    show("matching exterior variance", post_b[2][2])
    show("excess", excess)
    show("cap", cap)
    show("excess from the K identity", excess_identity)
    show("excess <= cap", excess <= cap)
    return {
        "trace_cross": tr_phi,
        "trace_blanket": blanket_trace,
        "excess": excess,
        "cap": cap,
        "exterior": var_e,
        "blanket_var": var_b,
    }


def section_floor():
    print("\n== interior floor ==")
    floor = Fraction(1, 5)
    tol = Fraction(1, 18)
    show("1/5", floor)
    show("1/18", tol)
    show("1/5 - 1/18", floor - tol)
    show("1/5 > 1/18", floor > tol)
    # Path of three: interior given the blanket.
    Sigma = inverse(path_precision_exact(3))
    show("path3 Var(X0|X1)", conditional_variance(Sigma, 0, [1]))
    Q5 = path_precision_exact(5)
    S5 = inverse(Q5)
    show("path5 Var(X2|X1,X3)", conditional_variance(S5, 2, [1, 3]))
    return {"floor": floor, "tol": tol, "gap": floor - tol}


def section_leaks():
    print("\n== leaks ==")
    target = 0.5 * math.log(9 / 8)
    show("1/2 ln(9/8)", "%.15f" % target)

    # Long-range: gamma = 1 on the path of three.
    Q = path_precision_exact(3)
    Q[0][0] += 1
    Q[2][2] += 1
    Q[0][2] -= 1
    Q[2][0] -= 1
    Sigma = inverse(Q)
    C, rho_sq, rho, info = partial_corr_and_info(Sigma, 0, 2, [1])
    show("long-range rho_sq", rho_sq)
    show("long-range rho", "%.15f" % rho)
    show("long-range I", "%.15f" % info)
    # gamma = 0 screens
    C0, rho0, _, info0 = partial_corr_and_info(inverse(path_precision_exact(3)), 0, 2, [1])
    show("gamma0 rho_sq", rho0)
    show("gamma0 I", "%.3e" % info0)

    # Equicorrelated: unit variance, covariance 1/2.
    half = Fraction(1, 2)
    Seq = [[Fraction(1) if i == j else half for j in range(3)] for i in range(3)]
    Ce, rho_sq_e, rho_e, info_e = partial_corr_and_info(Seq, 0, 2, [1])
    show("equi rho_sq", rho_sq_e)
    show("equi rho", "%.15f" % rho_e)
    show("equi I", "%.15f" % info_e)

    # MA(1): X_t = xi_t + xi_{t-1}, Var 2, lag-1 cov 1, lag-2 cov 0.
    Sma = [
        [Fraction(2), Fraction(1), Fraction(0)],
        [Fraction(1), Fraction(2), Fraction(1)],
        [Fraction(0), Fraction(1), Fraction(2)],
    ]
    uncond = Sma[0][2] / Sma[0][0]
    Cm, rho_sq_m, rho_m, info_m = partial_corr_and_info(Sma, 0, 2, [1])
    show("MA uncond corr", uncond)
    show("MA rho_sq", rho_sq_m)
    show("MA rho", "%.15f" % rho_m)
    show("MA I", "%.15f" % info_m)
    return {
        "target": target,
        "long": (rho_sq, rho, info),
        "equi": (rho_sq_e, rho_e, info_e),
        "ma": (rho_sq_m, rho_m, info_m, uncond),
    }


def binom_pmf_numer(n, k):
    """Numerator of Bin(n, 4/5) at k, over 5**n: C(n,k) * 4**k * 1**(n-k)."""
    return math.comb(n, k) * (4 ** k)


def section_pool():
    print("\n== pool ==")
    # Decision variance when k survivors each contribute precision 1.
    def eps(k):
        return Fraction(1, 2) + Fraction(1, 4 * (2 + k))

    tol = Fraction(11, 20)  # 0.55
    show("eps(1)", eps(1))
    show("eps(3)", eps(3))
    show("7/12 > 0.55", eps(1) > tol)
    show("eps(3) <= 0.55", eps(3) <= tol)
    # A copy keeps one survivor, so its best variance is eps(1) at every count.
    den5 = 5 ** 5
    num5 = sum(binom_pmf_numer(5, k) for k in range(3, 6))
    den6 = 5 ** 6
    num6 = sum(binom_pmf_numer(6, k) for k in range(3, 7))
    c5 = Fraction(num5, den5)
    c6 = Fraction(num6, den6)
    show("P(K>=3) n=5", "%s = %s" % (c5, float(c5)))
    show("P(K>=3) n=6", "%s = %s" % (c6, float(c6)))
    # Smallest n in 1..8 with P(K>=3) >= 0.95. For n<3 the event is empty.
    feasible = []
    for n in range(1, 9):
        num = sum(binom_pmf_numer(n, k) for k in range(3, n + 1))
        chance = Fraction(num, 5 ** n)
        ok = chance >= Fraction(95, 100)
        feasible.append((n, chance, ok))
        show("n=%d chance" % n, "%s meet=%s" % (chance, ok))
    smallest = next(n for n, _, ok in feasible if ok)
    # Expected decision variance at 6 units, two reductions.
    expect = sum(Fraction(binom_pmf_numer(6, k), den6) * eps(k) for k in range(7))
    # Second accumulation on one denominator.
    acc_num = 0
    acc_den = 1
    for k in range(7):
        term = Fraction(binom_pmf_numer(6, k), den6) * eps(k)
        acc_num = acc_num * term.denominator + term.numerator * acc_den
        acc_den = acc_den * term.denominator
        g = math.gcd(acc_num, acc_den)
        acc_num //= g
        acc_den //= g
    expect2 = Fraction(acc_num, acc_den)
    heat_upkeep = 6 * (1 + Fraction(1, 2))
    cost = heat_upkeep + expect
    show("smallest n", smallest)
    show("E two ways equal", expect == expect2)
    show("E", expect)
    show("E float", "%.15f" % float(expect))
    show("heat+upkeep", heat_upkeep)
    show("cost", cost)
    show("cost float", "%.15f" % float(cost))
    return {
        "c5": c5,
        "c6": c6,
        "smallest": smallest,
        "expect": expect,
        "cost": cost,
        "heat_upkeep": heat_upkeep,
    }


# ---------------------------------------------------------------------------
# Gasket from the preregistered corner gluing. The three identifications at
# one generation are disjoint pairs, so a direct alias map replaces union-find.
# ---------------------------------------------------------------------------

def sierpinski(generation):
    if generation == 0:
        edges = {frozenset((0, 1)), frozenset((1, 2)), frozenset((2, 0))}
        return {
            "edges": edges,
            "corners": (0, 1, 2),
            "n": 3,
            "copy0": {0, 1, 2},
            "glue": (),
        }
    sub = sierpinski(generation - 1)
    nsub = sub["n"]
    c0, c1, c2 = sub["corners"]
    # Disjoint pair identifications, preregistration section 5.
    alias = {
        (1, c0): (0, c1),
        (2, c1): (1, c2),
        (0, c2): (2, c0),
    }

    def canon(copy, v):
        return alias.get((copy, v), (copy, v))

    ids = {}

    def index(key):
        if key not in ids:
            ids[key] = len(ids)
        return ids[key]

    edges = set()
    for copy in range(3):
        for edge in sub["edges"]:
            a, b = tuple(edge)
            ia = index(canon(copy, a))
            ib = index(canon(copy, b))
            if ia != ib:
                edges.add(frozenset((ia, ib)))
    copy0 = {index(canon(0, v)) for v in range(nsub)}
    glue = (index(canon(0, c1)), index(canon(0, c2)))
    corners = (
        index(canon(0, c0)),
        index(canon(1, c1)),
        index(canon(2, c2)),
    )
    return {
        "edges": edges,
        "corners": corners,
        "n": len(ids),
        "copy0": copy0,
        "glue": glue,
    }


def precision_from_edges(n, edges):
    Q = np.zeros((n, n), dtype=float)
    deg = np.zeros(n, dtype=int)
    for edge in edges:
        i, j = tuple(edge)
        deg[i] += 1
        deg[j] += 1
        Q[i, j] -= 1.0
        Q[j, i] -= 1.0
    for i in range(n):
        Q[i, i] = 1.0 + deg[i]
    return Q, deg


def schur_trace(Q, region, blanket):
    region = np.asarray(region, dtype=int)
    blanket = np.asarray(blanket, dtype=int)
    Qii = Q[np.ix_(region, region)]
    Qib = Q[np.ix_(region, blanket)]
    # Q_BI Q_II^{-1} Q_IB = Q_IB^T Q_II^{-1} Q_IB
    X = np.linalg.solve(Qii, Qib)
    residual = np.max(np.abs(Qii @ X - Qib))
    gram = Qib.T @ X
    return float(np.trace(gram)), float(residual), gram


def section_gasket():
    print("\n== gasket ==")
    rows = []
    for g in range(2, 6):
        G = sierpinski(g)
        N = 3 * (3 ** g + 1) / 2
        edges_expected = 3 ** (g + 1)
        Q, deg = precision_from_edges(G["n"], G["edges"])
        glue = list(G["glue"])
        region = sorted(G["copy0"] - set(glue))
        exterior = sorted(set(range(G["n"])) - G["copy0"])
        # No edge from the region into the exterior: the blanket separates them.
        region_set = set(region)
        exterior_set = set(exterior)
        leak_edges = 0
        for edge in G["edges"]:
            a, b = tuple(edge)
            if (a in region_set and b in exterior_set) or (b in region_set and a in exterior_set):
                leak_edges += 1
        deg_region = sorted(int(deg[i]) for i in region)
        n_deg2 = sum(1 for d in deg_region if d == 2)
        n_deg4 = sum(1 for d in deg_region if d == 4)
        bound_b = sum(18 - int(Q[i, i]) for i in glue)
        bound_r = sum(18 - int(Q[i, i]) for i in region)
        formula_r = 13 * len(region) + 2
        tr, residual, gram = schur_trace(Q, region, glue)
        # Interior conditional variances are the diagonal of Q_RR^{-1}.
        inv_diag = np.diag(np.linalg.inv(Q[np.ix_(region, region)]))
        rows.append(
            {
                "g": g,
                "n": G["n"],
                "N": N,
                "edges": len(G["edges"]),
                "edges_expected": edges_expected,
                "nR": len(region),
                "glue_deg": (int(deg[glue[0]]), int(deg[glue[1]])),
                "leak_edges": leak_edges,
                "n_deg2": n_deg2,
                "n_deg4": n_deg4,
                "bound_b": bound_b,
                "bound_r": bound_r,
                "formula_r": formula_r,
                "tr": tr,
                "residual": residual,
                "iv_min": float(np.min(inv_diag)),
                "corners_deg": tuple(int(deg[c]) for c in G["corners"]),
            }
        )
        show(
            "g=%d" % g,
            "n=%d edges=%d |R|=%d glue_deg=%s leak=%d bounds=%d,%d tr=%.15f resid=%.3e iv_min=%.15f"
            % (
                G["n"],
                len(G["edges"]),
                len(region),
                rows[-1]["glue_deg"],
                leak_edges,
                bound_b,
                bound_r,
                tr,
                residual,
                rows[-1]["iv_min"],
            ),
        )
    return rows


# ---------------------------------------------------------------------------
# Log-linear crossing. Two matrix exponentials, two conditional-variance formulas.
# ---------------------------------------------------------------------------

def path_precision_float(n):
    Q = np.zeros((n, n))
    for i in range(n):
        deg = (1 if i else 0) + (1 if i + 1 < n else 0)
        Q[i, i] = 1.0 + deg
        if i + 1 < n:
            Q[i, i + 1] = Q[i + 1, i] = -1.0
    return Q


def expm_eigh(A):
    evals, U = np.linalg.eigh(A)
    return (U * np.exp(evals)) @ U.T


def expm_taylor(A, order=24):
    nrm = float(np.linalg.norm(A, ord=1))
    s = 0 if nrm == 0 else max(0, int(math.ceil(math.log2(nrm / 0.25))))
    B = A / (2 ** s)
    term = np.eye(A.shape[0])
    acc = np.eye(A.shape[0])
    for k in range(1, order + 1):
        term = term @ B / k
        acc = acc + term
    for _ in range(s):
        acc = acc @ acc
    return acc


def future_weight(Q, tau, center, method):
    kernel = method(-tau * Q)
    return kernel[center].copy()


def deltas_from_precision(Q, w, center):
    n = Q.shape[0]
    out = np.empty(center + 1)
    for r in range(center + 1):
        hidden = [i for i in range(n) if abs(i - center) > r]
        if not hidden:
            out[r] = 0.0
            continue
        Qh = Q[np.ix_(hidden, hidden)]
        wh = w[hidden]
        z = np.linalg.solve(Qh, wh)
        out[r] = float(wh @ z)
    return out


def deltas_from_covariance(Q, w, center):
    Sigma = np.linalg.inv(Q)
    cov = Sigma @ w
    full = float(w @ cov)
    n = Q.shape[0]
    out = np.empty(center + 1)
    for r in range(center + 1):
        seen = [i for i in range(n) if abs(i - center) <= r]
        v = cov[seen]
        gram = Sigma[np.ix_(seen, seen)]
        coef = np.linalg.solve(gram, v)
        out[r] = full - float(v @ coef)
    return out


def log_linear(ds, level=0.05):
    rhos = ds / ds[0]
    for k in range(len(rhos) - 1):
        if rhos[k] >= level > rhos[k + 1] and rhos[k + 1] > 0.0:
            num = math.log(rhos[k]) - math.log(level)
            den = math.log(rhos[k]) - math.log(rhos[k + 1])
            return k + num / den, k, float(rhos[k]), float(rhos[k + 1])
    return None


def integer_radius(ds, level=0.05):
    base = ds[0]
    for r, val in enumerate(ds):
        if val <= level * base:
            return r
    return None


def section_square():
    print("\n== open square ==")
    n = 8
    edges = set()
    def idx(x, y):
        return y * n + x
    for y in range(n):
        for x in range(n):
            if x + 1 < n:
                edges.add(frozenset((idx(x, y), idx(x + 1, y))))
            if y + 1 < n:
                edges.add(frozenset((idx(x, y), idx(x, y + 1))))
    Q, deg = precision_from_edges(n * n, edges)
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
    leak = 0
    region_set, exterior_set = set(region), set(exterior)
    for edge in edges:
        a, b = tuple(edge)
        if (a in region_set and b in exterior_set) or (b in region_set and a in exterior_set):
            leak += 1
    bound_b = sum(18 - int(Q[i, i]) for i in blanket)
    bound_r = sum(18 - int(Q[i, i]) for i in region)
    iv = np.diag(np.linalg.inv(Q[np.ix_(region, region)]))
    show("sizes", (len(region), len(blanket), len(exterior), leak))
    show("bounds", (bound_b, bound_r))
    show("interior min", "%.15f" % float(np.min(iv)))
    return bound_b, bound_r, float(np.min(iv))


def section_crossing():
    print("\n== crossing ==")
    methods = {"eigh": expm_eigh, "taylor": expm_taylor}
    try:
        import scipy.linalg

        methods["scipy"] = scipy.linalg.expm
        show("scipy", "yes")
    except Exception as exc:
        show("scipy", "no (%s)" % exc)
    Q = path_precision_float(61)
    center = 30
    results = {}
    for name, method in methods.items():
        for tau, key in ((0.25, "a"), (1.0, "b")):
            w = future_weight(Q, tau, center, method)
            d_prec = deltas_from_precision(Q, w, center)
            d_cov = deltas_from_covariance(Q, w, center)
            gap = float(np.max(np.abs(d_prec - d_cov)))
            star = log_linear(d_prec)
            show(
                "%s tau=%s" % (name, tau),
                "r*=%.15f k=%s rho=%.15f -> %.15f  formula_gap %.3e"
                % (star[0], star[1], star[2], star[3], gap),
            )
            results[(name, tau)] = {"star": star, "gap": gap, "ds": d_prec}
    ra = results[("eigh", 0.25)]["star"][0]
    rb = results[("eigh", 1.0)]["star"][0]
    ratio = rb / ra
    show("ratio eigh", "%.15f" % ratio)
    show("in band", 1.7 <= ratio <= 2.3)
    show("relative gap to 2", "%.15f" % (abs(ratio - 2.0) / 2.0))
    # Integer 5% radii, the puzzle pair, same definition, not the crossing target.
    print("-- integer radius --")
    for n in (31, 61):
        Qn = path_precision_float(n)
        c = n // 2
        for tau in (0.5, 1.0):
            w = future_weight(Qn, tau, c, expm_eigh)
            ds = deltas_from_precision(Qn, w, c)
            rhos = ds / ds[0]
            r = integer_radius(ds)
            show(
                "n=%d tau=%s" % (n, tau),
                "r=%s rho1=%.8f rho2=%.8f" % (r, rhos[1], rhos[2]),
            )
    return results


def main():
    print("numpy", np.__version__)
    screen = section_path_three()
    channel = section_channel()
    floor = section_floor()
    leaks = section_leaks()
    pool = section_pool()
    gasket = section_gasket()
    section_square()
    crossing = section_crossing()
    print("\n== summary ==")
    show("screen", screen)
    show("channel", {k: str(v) for k, v in channel.items()})
    show("floor", {k: str(v) for k, v in floor.items()})
    show("pool cost", pool["cost"])
    show("gasket tr", [round(row["tr"], 12) for row in gasket])
    eigh_a = crossing[("eigh", 0.25)]["star"][0]
    eigh_b = crossing[("eigh", 1.0)]["star"][0]
    show("crossing", "%.12f %.12f %.12f" % (eigh_a, eigh_b, eigh_b / eigh_a))


if __name__ == "__main__":
    main()
