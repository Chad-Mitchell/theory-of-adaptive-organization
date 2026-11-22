"""Independent recomputation of the boundary-sufficiency numbers.

Does not import theory/boundary_checks. Closed forms are rational arithmetic.
The gasket, the square, and the radius profiles are built from the
preregistration's definitions.
"""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
from numpy.linalg import inv, solve


def path_Q(n: int) -> np.ndarray:
    """Q = I + L on the open path. Endpoints have degree 1."""
    Q = np.zeros((n, n), dtype=float)
    for i in range(n):
        # Endpoints have degree 1, interior vertices degree 2.
        Q[i, i] = 1.0 + (1.0 if i in (0, n - 1) else 2.0)
        if i + 1 < n:
            Q[i, i + 1] = Q[i + 1, i] = -1.0
    if n == 1:
        Q[0, 0] = 1.0
    return Q


def precision_from_edges(n: int, edges) -> np.ndarray:
    Q = np.eye(n)
    deg = np.zeros(n)
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
        Q[a, b] -= 1.0
        Q[b, a] -= 1.0
    for i in range(n):
        Q[i, i] += deg[i]
    return Q


def build_gasket(g: int):
    """Sierpinski gasket graph, corner-gluing as locked in the preregistration."""
    if g == 0:
        return {"n": 3, "edges": [(0, 1), (1, 2), (2, 0)], "corners": (0, 1, 2)}
    sub = build_gasket(g - 1)
    n = sub["n"]
    c0, c1, c2 = sub["corners"]
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
    # copy 0's second with copy 1's first; copy 1's third with copy 2's second;
    # copy 2's first with copy 0's third.
    union((0, c1), (1, c0))
    union((1, c2), (2, c1))
    union((2, c0), (0, c2))
    roots = {}
    for copy in range(3):
        for v in range(n):
            r = find((copy, v))
            if r not in roots:
                roots[r] = len(roots)
    edges = set()
    for copy in range(3):
        for a, b in sub["edges"]:
            ia, ib = roots[find((copy, a))], roots[find((copy, b))]
            if ia != ib:
                edges.add((ia, ib) if ia < ib else (ib, ia))
    corners = (
        roots[find((0, c0))],
        roots[find((1, c1))],
        roots[find((2, c2))],
    )
    copy0 = sorted({roots[find((0, v))] for v in range(n)})
    glue = (roots[find((0, c1))], roots[find((0, c2))])
    return {
        "n": len(roots),
        "edges": sorted(edges),
        "corners": corners,
        "copy0": copy0,
        "glue": glue,
    }


def open_square(n: int):
    def idx(x, y):
        return y * n + x

    edges = []
    for y in range(n):
        for x in range(n):
            if x + 1 < n:
                edges.append((idx(x, y), idx(x + 1, y)))
            if y + 1 < n:
                edges.append((idx(x, y), idx(x, y + 1)))
    return n * n, edges


def schur_trace(Q, region, blanket) -> float:
    I = np.asarray(region, dtype=int)
    B = np.asarray(blanket, dtype=int)
    Qbi = Q[np.ix_(B, I)]
    return float(np.trace(Qbi @ solve(Q[np.ix_(I, I)], Qbi.T)))


def conditional_cov(Sigma, target, given):
    target = list(target)
    given = list(given)
    if not given:
        return Sigma[np.ix_(target, target)].copy()
    Sgg = Sigma[np.ix_(given, given)]
    Stg = Sigma[np.ix_(target, given)]
    Stt = Sigma[np.ix_(target, target)]
    return Stt - Stg @ solve(Sgg, Stg.T)


def uniform_load(Q, sites, eps=1.0 / 18.0, iters=80):
    sites = np.asarray(list(sites), dtype=int)
    lo, hi = 0.0, 1.0 / eps
    for _ in range(30):
        M = Q.copy()
        M[sites, sites] += hi
        smax = float(np.max(np.diag(inv(M))[sites]))
        if smax <= eps:
            break
        hi *= 2.0
    else:
        raise RuntimeError("load did not meet tolerance")
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        M = Q.copy()
        M[sites, sites] += mid
        smax = float(np.max(np.diag(inv(M))[sites]))
        if smax <= eps:
            hi = mid
        else:
            lo = mid
    return len(sites) * hi, hi, smax, hi - lo


def bessel_I(d: int, z: float, terms: int = 120) -> float:
    """I_d(z) by the power series, for integer d >= 0."""
    half = 0.5 * z
    log_term = d * math.log(half) - math.lgamma(d + 1.0)
    term = math.exp(log_term)
    total = term
    for m in range(terms):
        term *= (half * half) / ((m + 1) * (m + 1 + d))
        total += term
        if term < total * 1e-18 and m > d:
            break
    return total


def second_moment(t: float, radius: int = 40):
    weight = math.exp(-2.0 * t)
    arg = 2.0 * t
    mass = weight * bessel_I(0, arg)
    moment = 0.0
    for d in range(1, radius + 1):
        p = weight * bessel_I(d, arg)
        mass += 2.0 * p
        moment += 2.0 * (d * d) * p
    return moment, mass


def expm_sym(A: np.ndarray) -> np.ndarray:
    w, U = np.linalg.eigh(A)
    return (U * np.exp(w)) @ U.T


def delta_profile(n: int, tau: float):
    Q = path_Q(n)
    center = n // 2
    kernel = expm_sym(-tau * Q)
    w = kernel[center]
    out = []
    for r in range(center + 1):
        mask = np.ones(n, dtype=bool)
        mask[np.abs(np.arange(n) - center) <= r] = False
        outside = np.flatnonzero(mask)
        if outside.size == 0:
            out.append(0.0)
            continue
        Qout = Q[np.ix_(outside, outside)]
        wo = w[outside]
        out.append(float(wo @ solve(Qout, wo)))
    return out


def first_radius(ds, eta=0.05):
    base = ds[0]
    for r, val in enumerate(ds):
        if val <= eta * base:
            return r
    return None


def interp_radius(ds, eta=0.05):
    base = ds[0]
    ratios = [v / base for v in ds]
    for r in range(len(ratios) - 1):
        if ratios[r] > eta >= ratios[r + 1]:
            # linear in r
            lin = r + (ratios[r] - eta) / (ratios[r] - ratios[r + 1])
            # log-linear in the ratio
            log = r + math.log(ratios[r] / eta) / math.log(ratios[r] / ratios[r + 1])
            return lin, log, ratios[r], ratios[r + 1]
    return None, None, None, None


def main():
    print("=== P1 path of three, exact ===")
    Q3 = np.array([[2.0, -1.0, 0.0], [-1.0, 3.0, -1.0], [0.0, -1.0, 2.0]])
    Sigma3 = inv(Q3)
    locked = np.array([[5, 2, 1], [2, 4, 2], [1, 2, 5]], dtype=float) / 8.0
    print("Sigma gap", np.max(np.abs(Sigma3 - locked)))
    # conditional variances by the covariance formula
    def svar(Sigma, i, given):
        return float(conditional_cov(Sigma, [i], given)[0, 0])

    print("Var(X2|X1)", svar(Sigma3, 2, [1]), "locked 1/2")
    print("Var(X2|X0,X1)", svar(Sigma3, 2, [0, 1]), "locked 1/2")
    print("Var(X2|X0)", svar(Sigma3, 2, [0]), "locked 3/5", 3 / 5)
    print("Var(X0|X1)", svar(Sigma3, 0, [1]), "locked 1/2")
    rho = Sigma3[0, 2] / math.sqrt(Sigma3[0, 0] * Sigma3[2, 2])
    print("I(X0;X2)", -0.5 * math.log(1 - rho * rho), "locked", 0.5 * math.log(25 / 24))
    # conditional independence given X1: conditional cov of (0,2)
    c = conditional_cov(Sigma3, [0, 2], [1])
    print("cond cov given X1", c, "I", -0.5 * math.log(max(0.0, 1 - (c[0, 1] ** 2) / (c[0, 0] * c[1, 1]))))

    print("=== P3 counterexample, fractions ===")
    # Q+Phi with phi_00=1/10, phi_01=1, phi_11=10
    # posterior block of sites 1,2 is [[13,-1],[-1,2]], det 25
    post_11 = Fraction(2, 25)
    post_22 = Fraction(13, 25)
    print("Var blanket", post_11, float(post_11))
    print("Var exterior", post_22, float(post_22))
    # marginal prior precision of site 1 is 2; phi = 25/2 - 2 = 21/2 = 10.5
    phi = Fraction(25, 2) - 2
    print("blanket-only trace", phi, float(phi))
    print("excess", phi - Fraction(101, 10), "cap", Fraction(1, 2))
    # numerical confirmation of the joint inverse
    P = Q3.copy()
    P[0, 0] += 0.1
    P[0, 1] += 1.0
    P[1, 0] += 1.0
    P[1, 1] += 10.0
    post = inv(P)
    print("numeric Var1", post[1, 1], "Var2", post[2, 2], "tr Phi", np.trace(P - Q3))
    cap = schur_trace(Q3, [0], [1])
    print("tr(K)", cap)

    print("=== P2 gap ===")
    def var_phi_psi(phi, psi):
        M = Q3.copy()
        M[1, 1] += phi
        M[0, 0] += psi
        return inv(M)[2, 2]

    v_b = var_phi_psi(2.0, 0.0)
    v_d = var_phi_psi(1.0, 1.0)
    print("phi2", v_b, 9 / 16, "split", v_d, 11 / 19, "gap", v_d - v_b, 5 / 304)

    print("=== P4 path of five ===")
    Q5 = path_Q(5)
    S5 = inv(Q5)
    d = [1, 2, 5, 13, 34]
    gap = 0.0
    for i in range(5):
        for j in range(5):
            a, b = (i, j) if i <= j else (j, i)
            gap = max(gap, abs(S5[i, j] - d[a] * d[4 - b] / 55.0))
    print("green gap", gap)
    print("Var(X0|X1)", svar(S5, 0, [1]))
    # Var(X0 | X1+X3)
    var_s = S5[1, 1] + S5[3, 3] + 2 * S5[1, 3]
    cov0 = S5[0, 1] + S5[0, 3]
    v0 = S5[0, 0] - cov0 ** 2 / var_s
    cov4 = S5[4, 1] + S5[4, 3]
    v4 = S5[4, 4] - cov4 ** 2 / var_s
    both = svar(S5, 0, [1, 3]) + svar(S5, 4, [1, 3])
    print("Var(X0|sum)", v0, 121 / 220)
    print("sum both", both, "sum pooled", v0 + v4, "gap", both - (v0 + v4))
    print("Var(X2|X1,X3)", svar(S5, 2, [1, 3]), 1 / 3)
    print("trK", schur_trace(Q5, [2], [1, 3]), 2 / 3)
    # Z = X0+X4
    c_both = conditional_cov(S5, [0, 4], [1, 3])
    var_z_both = float(c_both.sum())
    var_z = S5[0, 0] + S5[4, 4] + 2 * S5[0, 4]
    cov_z = cov0 + cov4
    var_z_s = var_z - cov_z ** 2 / var_s
    print("Var Z both", var_z_both, "Var Z sum", var_z_s)

    print("=== leakage ===")
    target = 0.5 * math.log(9 / 8)
    Ql = Q3.copy()
    Ql[0, 0] += 1
    Ql[2, 2] += 1
    Ql[0, 2] -= 1
    Ql[2, 0] -= 1
    Sl = inv(Ql)
    cl = conditional_cov(Sl, [0, 2], [1])
    rho_l = cl[0, 1] / math.sqrt(cl[0, 0] * cl[1, 1])
    print("long-range rho", rho_l, "I", -0.5 * math.log(1 - rho_l ** 2), "target", target)
    # precision partial correlation
    print("precision partial", -Ql[0, 2] / math.sqrt(Ql[0, 0] * Ql[2, 2]))
    Seq = np.full((3, 3), 0.5)
    np.fill_diagonal(Seq, 1.0)
    ce = conditional_cov(Seq, [0, 2], [1])
    rho_e = ce[0, 1] / math.sqrt(ce[0, 0] * ce[1, 1])
    print("equi rho", rho_e, "I", -0.5 * math.log(1 - rho_e ** 2))
    Sma = np.array([[2.0, 1.0, 0.0], [1.0, 2.0, 1.0], [0.0, 1.0, 2.0]])
    cm = conditional_cov(Sma, [0, 2], [1])
    rho_m = cm[0, 1] / math.sqrt(cm[0, 0] * cm[1, 1])
    print("MA rho", rho_m, "I", -0.5 * math.log(1 - rho_m ** 2), "uncond", Sma[0, 2] / 2)

    print("=== finite speed, fractions ===")
    def banded_power_coeff(weights, H, site):
        # weights[d] = coefficient at signed distance d, d>=0, symmetric
        # iterate the row of site 0 as a dict of Fraction
        row = {0: Fraction(1)}
        for _ in range(H):
            nxt = {}
            for pos, coef in row.items():
                for dist, w in weights.items():
                    for sign in ((1, -1) if dist else (1,)):
                        p = pos + sign * dist
                        nxt[p] = nxt.get(p, Fraction(0)) + coef * w
            row = nxt
        return row.get(site, Fraction(0)), max(row)

    w1 = {0: Fraction(1, 2), 1: Fraction(1, 4)}
    for H, excess in ((1, Fraction(1, 16)), (2, Fraction(1, 256)), (3, Fraction(1, 4096))):
        c, far = banded_power_coeff(w1, H, H)
        beyond = banded_power_coeff(w1, H, H + 1)[0]
        print(f"H={H} coeff {c} sq {c*c} locked {excess} beyond {beyond} far {far}")
    w2 = {0: Fraction(1, 2), 1: Fraction(1, 6), 2: Fraction(1, 6)}
    c2, _ = banded_power_coeff(w2, 1, 2)
    b2 = banded_power_coeff(w2, 1, 3)[0]
    c4, _ = banded_power_coeff(w2, 2, 4)
    b4 = banded_power_coeff(w2, 2, 5)[0]
    print("r2 H1", c2, c2 * c2, "beyond", b2)
    print("r2 H2", c4, c4 * c4, "beyond", b4, "locked", Fraction(1, 36), Fraction(1, 1296))

    print("=== bessel ===")
    for t, locked_m in ((0.5, 1.0), (2.0, 4.0)):
        moment, mass = second_moment(t, 40)
        print(f"t={t} moment {moment:.16f} mass {mass:.16f} locked {locked_m}")
    # scipy cross-check if present
    try:
        from scipy.special import iv

        for t in (0.5, 2.0):
            moment = 0.0
            mass = math.exp(-2 * t) * iv(0, 2 * t)
            for d in range(1, 41):
                p = math.exp(-2 * t) * iv(d, 2 * t)
                mass += 2 * p
                moment += 2 * d * d * p
            print(f"scipy t={t} moment {moment:.16f} mass {mass:.16f}")
    except Exception as exc:
        print("scipy skipped", exc)
    for tau in (0.5, 1.0):
        for dist in (1, 5, 15):
            val = math.exp(-3 * tau) * bessel_I(dist, 2 * tau)
            print(f"kernel tau={tau} d={dist} {val:.6e}")

    print("=== radius ===")
    for n in (31, 61):
        for tau in (0.5, 1.0):
            ds = delta_profile(n, tau)
            base = ds[0]
            r = first_radius(ds)
            lin, log, a, b = interp_radius(ds)
            ratios = [ds[k] / base for k in range(min(6, len(ds)))]
            print(
                f"n={n} tau={tau} r={r} ratios "
                + " ".join(f"{x:.8e}" for x in ratios)
                + f" lin {lin} log {log} min_pos {min(ds[:-1]):.6e} end {ds[-1]:.3e}"
            )
        da = delta_profile(n, 0.5)
        db = delta_profile(n, 1.0)
        ra, rb = first_radius(da), first_radius(db)
        print(f"n={n} integer ratio {rb}/{ra} = {rb / ra if ra else None}")

    print("=== pool ===")
    def eps(k):
        return Fraction(1, 2) + Fraction(1, 4 * (2 + k))

    print("eps1", eps(1), "7/12", Fraction(7, 12), "eps3", eps(3), "0.55", Fraction(11, 20))

    def chance(n, kmin=3):
        den = 5 ** n
        total = sum(math.comb(n, k) * (4 ** k) for k in range(kmin, n + 1))
        return Fraction(total, den)

    print("c5", chance(5), Fraction(2944, 3125))
    print("c6", chance(6), Fraction(15360, 15625))
    feasible = [n for n in range(1, 9) if chance(n) >= Fraction(19, 20)]
    print("feasible", feasible)
    expect = sum(
        Fraction(math.comb(6, k) * (4 ** k), 5 ** 6) * eps(k) for k in range(7)
    )
    print("expect", expect, Fraction(470459, 875000), expect == Fraction(470459, 875000))
    cost = 9 + expect
    print("cost", cost, Fraction(8345459, 875000), float(cost))

    print("=== gasket and square ===")
    eps = 1.0 / 18.0
    for g, nR, b_lock, r_lock in (
        (2, 4, 26, 54),
        (3, 13, 26, 171),
        (4, 40, 26, 522),
        (5, 121, 26, 1575),
    ):
        G = build_gasket(g)
        N = 3 * (3 ** g + 1) / 2
        Q = precision_from_edges(G["n"], G["edges"])
        glue = list(G["glue"])
        copy0 = set(G["copy0"])
        region = sorted(copy0 - set(glue))
        exterior = sorted(set(range(G["n"])) - copy0)
        deg = np.zeros(G["n"], dtype=int)
        for a, b in G["edges"]:
            deg[a] += 1
            deg[b] += 1
        hist = {int(k): int(v) for k, v in zip(*np.unique(deg[region], return_counts=True))}
        # screen
        Sigma = inv(Q)
        c_b = conditional_cov(Sigma, exterior, glue)
        c_rb = conditional_cov(Sigma, exterior, region + glue)
        gap = float(np.max(np.abs(c_b - c_rb)))
        qee = inv(Q[np.ix_(exterior, exterior)])
        gap_q = float(np.max(np.abs(c_b - qee)))
        iv = np.diag(conditional_cov(Sigma, region, glue))
        iv_q = np.diag(inv(Q[np.ix_(region, region)]))
        iv_gap = float(np.max(np.abs(iv - iv_q)))
        # Q_RE should be zero
        cross = Q[np.ix_(region, exterior)]
        cross_max = float(np.max(np.abs(cross))) if cross.size else 0.0
        b_bound = sum(1 / eps - Q[i, i] for i in glue)
        r_bound = sum(1 / eps - Q[i, i] for i in region)
        K = schur_trace(Q, region, glue)
        heat_b, phi_b, smax_b, width_b = uniform_load(Q, glue)
        heat_r, phi_r, smax_r, width_r = uniform_load(Q, region)
        print(
            f"g={g} n={G['n']} expect {N:.0f} |R|={len(region)} lock {nR} "
            f"degR {hist} glue deg {deg[glue[0]], deg[glue[1]]}"
        )
        print(
            f"  bounds {b_bound:.6f}/{r_bound:.6f} lock {b_lock}/{r_lock} "
            f"trK {K:.12f} gap {gap:.3e} gapQ {gap_q:.3e} ivgap {iv_gap:.3e} "
            f"ivmin {iv.min():.12f} cross {cross_max:.3e}"
        )
        print(
            f"  loadB {heat_b:.10f} phi {phi_b:.10f} smax {smax_b:.6e} width {width_b:.3e} "
            f"loadR {heat_r:.10f} smax {smax_r:.6e}"
        )

    print("=== square ===")
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
    Sigma = inv(Q)
    c_b = conditional_cov(Sigma, exterior, blanket)
    c_rb = conditional_cov(Sigma, exterior, region + blanket)
    gap = float(np.max(np.abs(c_b - c_rb)))
    iv = np.diag(conditional_cov(Sigma, region, blanket))
    iv_q = np.diag(inv(Q[np.ix_(region, region)]))
    b_bound = sum(1 / eps - Q[i, i] for i in blanket)
    r_bound = sum(1 / eps - Q[i, i] for i in region)
    heat_b, phi_b, smax_b, width_b = uniform_load(Q, blanket)
    K = schur_trace(Q, region, blanket)
    print(
        f"sizes {len(region)} {len(blanket)} {len(exterior)} bounds {b_bound:.6f} {r_bound:.6f} "
        f"gap {gap:.3e} ivmin {iv.min():.12f} ivgap {np.max(np.abs(iv-iv_q)):.3e}"
    )
    print(f"loadB {heat_b:.10f} per {heat_b/8:.10f} phi {phi_b:.8f} smax {smax_b:.6e} trK {K:.8f}")

    print("=== path Schur vs length ===")
    for n in (7, 15, 31, 61):
        # region is the open middle, blanket the two neighbors of the ends of the region
        # sites 2..n-3 region, blanket {1, n-2}, exterior {0, n-1}
        if n < 7:
            continue
        Q = path_Q(n)
        region = list(range(2, n - 2))
        blanket = [1, n - 2]
        print(f"path n={n} |R|={len(region)} trK {schur_trace(Q, region, blanket):.8f}")


if __name__ == "__main__":
    main()
