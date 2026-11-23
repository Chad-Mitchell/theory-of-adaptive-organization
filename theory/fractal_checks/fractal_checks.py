#!/usr/bin/env python3
"""Checks for the fractal-world preregistration.

The lock is theory/fractal_checks/PREREG.md, commit 5da0f73, written before
this script. Required identities that miss exit nonzero. A locked tolerance
that misses is printed as a puzzle and does not by itself fail the run.

Run from the repo root:
  nice -n 19 python3 theory/fractal_checks/fractal_checks.py
"""
from __future__ import annotations

import math
import sys

import numpy as np

PASS = 0
FAIL = 0
PUZZLES = 0
EPS = 1.0 / 18.0
LOG5 = math.log(5.0)
LOG25 = math.log(25.0)


def check(name, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print("PASS  %s  %s" % (name, detail))
    else:
        FAIL += 1
        print("FAIL  %s  %s" % (name, detail))


def puzzle(name, ok, detail=""):
    """A locked tolerance. A miss is recorded and is not a required failure."""
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


def ols(x, y):
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = int(x.shape[0])
    xb = float(x.mean())
    yb = float(y.mean())
    sxx = float(np.sum((x - xb) ** 2))
    if sxx <= 0.0:
        return float("nan"), float("nan"), float("nan"), n
    slope = float(np.sum((x - xb) * (y - yb)) / sxx)
    intercept = yb - slope * xb
    resid = y - (intercept + slope * x)
    dof = n - 2
    sigma2 = float(np.sum(resid ** 2) / dof) if dof > 0 else float("nan")
    stderr = math.sqrt(max(sigma2, 0.0) / sxx) if dof > 0 else float("nan")
    return slope, intercept, stderr, n


def k_u(r):
    return int(math.floor(math.log(r) / LOG5) + 1)


def k_e(r):
    return int(math.floor(math.log(r) / LOG25) + 1)


def bin_index(lam):
    """j with 5^{-j} <= lam < 5^{-j+1}."""
    x = -math.log(float(lam)) / LOG5
    return int(math.ceil(x - 1e-12))


# ---------------------------------------------------------------------------
# Graphs
# ---------------------------------------------------------------------------

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
    return {"n": len(idx), "edges": sorted(edges), "corners": corners}


def carpet_cells(n):
    cells = []

    def rec(level, x0, y0):
        if level == 0:
            cells.append((x0, y0))
            return
        s = 3 ** (level - 1)
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    continue
                rec(level - 1, x0 + i * s, y0 + j * s)

    rec(n, 0, 0)
    return cells


def build_carpet(n):
    cells = carpet_cells(n)
    side = 3 ** n
    index = {xy: i for i, xy in enumerate(cells)}
    edges = []
    boundary = []
    for i, (x, y) in enumerate(cells):
        for dx, dy in ((1, 0), (0, 1)):
            j = index.get((x + dx, y + dy))
            if j is not None:
                edges.append((i, j))
        if x == 0 or y == 0 or x == side - 1 or y == side - 1:
            boundary.append(i)
    return {
        "n": len(cells),
        "edges": edges,
        "boundary": np.asarray(boundary, dtype=int),
        "side": side,
        "coords": cells,
    }


def grid_edges(n, periodic):
    edges = []

    def idx(x, y):
        return y * n + x

    for y in range(n):
        for x in range(n):
            for dx, dy in ((1, 0), (0, 1)):
                xx, yy = x + dx, y + dy
                if periodic:
                    edges.append((idx(x, y), idx(xx % n, yy % n)))
                elif 0 <= xx < n and 0 <= yy < n:
                    edges.append((idx(x, y), idx(xx, yy)))
    boundary = []
    if not periodic:
        for y in range(n):
            for x in range(n):
                if x == 0 or y == 0 or x == n - 1 or y == n - 1:
                    boundary.append(idx(x, y))
    return n * n, edges, np.asarray(boundary, dtype=int)


def path_edges(n):
    return [(i, i + 1) for i in range(n - 1)], [(0, n - 1)]


def adjacency(n, edges):
    deg = np.zeros(n, dtype=float)
    rows = []
    cols = []
    for i, j in edges:
        deg[i] += 1.0
        deg[j] += 1.0
        rows.append(i)
        cols.append(j)
    return deg


def precision(n, edges, alpha=1.0, beta=1.0):
    deg = adjacency(n, edges)
    Q = np.zeros((n, n), dtype=float)
    for i, j in edges:
        Q[i, j] -= beta
        Q[j, i] -= beta
    for i in range(n):
        Q[i, i] = alpha + beta * deg[i]
    return Q, deg


def laplacian_eigs_from_edges(n, edges):
    L = np.zeros((n, n), dtype=float)
    deg = adjacency(n, edges)
    for i, j in edges:
        L[i, j] -= 1.0
        L[j, i] -= 1.0
    for i in range(n):
        L[i, i] = deg[i]
    return np.linalg.eigvalsh(L), deg


def graph_distance(n, edges, src, dst):
    adj = [[] for _ in range(n)]
    for i, j in edges:
        adj[i].append(j)
        adj[j].append(i)
    seen = [False] * n
    q = [(src, 0)]
    seen[src] = True
    for i, dist in q:
        if i == dst:
            return dist
        for j in adj[i]:
            if not seen[j]:
                seen[j] = True
                q.append((j, dist + 1))
    return None


def block_covariance(Q, sites):
    sites = np.asarray(sites, dtype=int)
    eye = np.zeros((Q.shape[0], sites.shape[0]))
    for col, site in enumerate(sites):
        eye[site, col] = 1.0
    solved = np.linalg.solve(Q, eye)
    return solved[sites, :]


def uniform_phi(Sbb, eps):
    """Smallest uniform diagonal load whose conditional variances are <= eps."""
    m = Sbb.shape[0]

    def smax(phi):
        a = Sbb + np.eye(m) / phi
        correction = np.linalg.solve(a, Sbb)
        cond = Sbb - Sbb @ correction
        # Symmetrize roundoff before reading the diagonal.
        cond = 0.5 * (cond + cond.T)
        return float(np.max(np.diag(cond)))

    lo, hi = 0.0, 1.0 / eps
    for _ in range(30):
        if smax(hi) <= eps:
            break
        hi *= 2.0
    else:
        raise RuntimeError("uniform load did not meet the tolerance")
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if smax(mid) <= eps:
            hi = mid
        else:
            lo = mid
    return float(hi), smax(hi), m * float(hi)


def heat_from_degrees(n, deg_sum, eps=EPS, alpha=1.0, beta=1.0):
    return n / eps - alpha * n - beta * deg_sum


def nonempty_bins(eigs, lo, hi):
    """Bins [5^{-j}, 5^{-j+1}) that contain a positive eigenvalue in [lo, hi]."""
    chosen = []
    pad = 1e-12
    for lam in np.asarray(eigs, float):
        if lam > pad and (lo - pad) <= lam <= (hi + pad):
            chosen.append(float(lam))
    return {bin_index(lam) for lam in chosen}, chosen


# ---------------------------------------------------------------------------
# Locked arithmetic that does not touch a fractal graph
# ---------------------------------------------------------------------------

def check_ladder_table():
    locked = {
        5: (2, 1),
        25: (3, 2),
        125: (4, 2),
        625: (5, 3),
        3125: (6, 3),
        15625: (7, 4),
    }
    for r, (ku, ke) in locked.items():
        check(
            "layer table R=%d" % r,
            k_u(r) == ku and k_e(r) == ke,
            "K_U %d K_E %d" % (k_u(r), k_e(r)),
        )
    check("K_U(1.44)=1", k_u(1.44) == 1, "got %d" % k_u(1.44))
    check("K_E(1.44)=1", k_e(1.44) == 1, "got %d" % k_e(1.44))
    check("bin of 5^{-3} is 3", bin_index(5.0 ** -3) == 3, "j %d" % bin_index(5.0 ** -3))
    check("bin of 0.04 is 2", bin_index(0.04) == 2, "j %d" % bin_index(0.04))
    check("bin just below 0.04 is 3", bin_index(0.039) == 3, "j %d" % bin_index(0.039))


def check_lattice_closed_form():
    def gap(n):
        return 2.0 - 2.0 * math.cos(2.0 * math.pi / n)

    ns = [16, 32, 64, 128]
    gaps = [gap(n) for n in ns]
    locked = [
        0.152240934977,
        0.038429439194,
        0.009630546656,
        0.002409087590,
    ]
    for n, g, lock in zip(ns, gaps, locked):
        check(
            "periodic gap n=%d" % n,
            absnear(g, lock, 5e-13),
            "gap %.12f" % g,
        )
    slope, _intercept, stderr, nfit = ols([math.log(n) for n in ns], [math.log(g) for g in gaps])
    check(
        "lattice gap slope",
        absnear(slope, -1.994169933238, 1e-12),
        "slope %.12f stderr %.12f N %d" % (slope, stderr, nfit),
    )
    check(
        "lattice gap slope is not -log 5",
        abs(slope - (-LOG5)) > 0.3,
        "slope %.6f  -log5 %.6f" % (slope, -LOG5),
    )
    # Doubling ratios approach 4, not 5.
    for n in (16, 32, 64):
        ratio = gap(n) / gap(2 * n)
        check(
            "lattice doubling ratio n=%d" % n,
            abs(ratio - 4.0) < 0.2 and abs(ratio - 5.0) > 0.5,
            "ratio %.12f" % ratio,
        )


def cumulative_slope(counts_at, lams):
    xs, ys = [], []
    for lam, count in zip(lams, counts_at):
        if count >= 2:
            xs.append(math.log(lam))
            ys.append(math.log(count))
    if len(xs) < 3:
        return None, len(xs)
    slope, _b, stderr, nfit = ols(xs, ys)
    return (slope, stderr, nfit), len(xs)


def lattice_cumulative_slopes():
    print("\n-- lattice counting function, exact eigenvalues")
    for n in (32, 64, 128):
        ks = 2.0 - 2.0 * np.cos(2.0 * math.pi * np.arange(n) / n)
        lam = ks[:, None] + ks[None, :]
        lams = [0.05, 0.1, 0.2, 0.4]
        counts = [int(np.sum((lam > 0.0) & (lam <= L))) for L in lams]
        fit, nused = cumulative_slope(counts, lams)
        print("  n=%d counts %s" % (n, counts))
        if fit is None:
            puzzle("lattice DOS slope n=%d" % n, False, "fewer than 3 usable points (%d)" % nused)
        else:
            slope, stderr, nfit = fit
            print("  n=%d slope %.6f stderr %.3e" % (n, slope, stderr))
            puzzle(
                "lattice DOS slope n=%d" % n,
                abs(slope - 1.0) <= 0.15,
                "slope %.6f target 1 tolerance 0.15" % slope,
            )


# ---------------------------------------------------------------------------
# Gasket and carpet
# ---------------------------------------------------------------------------

def g0_reference_phi():
    phi = (13.0 + 3.0 * math.sqrt(33.0)) / 2.0
    total = 3.0 * phi
    return phi, total


def run_graphs():
    print("\n-- gasket combinatorics and all-site heat")
    gaskets = []
    spectra = {}
    for g in range(7):
        graph = build_gasket(g)
        n = graph["n"]
        n_lock = (3 ** g + 1) * 3 // 2
        deg = adjacency(n, graph["edges"])
        deg_sum = float(np.sum(deg))
        corners = graph["corners"]
        corner_deg = [float(deg[c]) for c in corners]
        others = [float(deg[i]) for i in range(n) if i not in corners]
        dist = graph_distance(n, graph["edges"], corners[0], corners[1])
        check("gasket N g=%d" % g, n == n_lock, "N %d" % n)
        check(
            "gasket degrees g=%d" % g,
            all(d == 2.0 for d in corner_deg) and (g == 0 or all(d == 4.0 for d in others)),
            "corners %s degree sum %.0f" % (corner_deg, deg_sum),
        )
        check(
            "gasket degree sum g=%d" % g,
            deg_sum == 4 * n - 6,
            "sum %.0f" % deg_sum,
        )
        check(
            "gasket corner distance g=%d" % g,
            dist == 2 ** g,
            "distance %s" % dist,
        )
        heat = heat_from_degrees(n, deg_sum)
        heat_lock = 13 * n + 6
        check(
            "gasket heat g=%d" % g,
            absnear(heat, heat_lock, 1e-9),
            "heat %.12f per site %.12f" % (heat, heat / n),
        )
        gaskets.append((g, graph, deg, heat))
        print("  g=%d N=%d heat %.12f per %.12f" % (g, n, heat, heat / n))

    # Dimension alternatives at g=6.
    _g, graph, _deg, heat = gaskets[-1]
    n = graph["n"]
    per = heat / n
    ds = 2.0 * math.log(3.0) / LOG5
    df = math.log(3.0) / math.log(2.0)
    check(
        "gasket per site near 13 at g=6",
        abs(per - 13.0) < 0.01,
        "per %.12f" % per,
    )
    check(
        "gasket per site is not 13*ds/2",
        abs(per - 13.0 * ds / 2.0) > 2.0,
        "alternative %.6f" % (13.0 * ds / 2.0),
    )
    check(
        "gasket per site is not 13*df/2",
        abs(per - 13.0 * df / 2.0) > 2.0,
        "alternative %.6f" % (13.0 * df / 2.0),
    )
    heats = [h for _g, _gr, _d, h in gaskets if _g >= 3]
    ns = [gr["n"] for g, gr, _d, _h in gaskets if g >= 3]
    slope, _b, stderr, nfit = ols([math.log(v) for v in ns], [math.log(h) for h in heats])
    check(
        "gasket log-log slope g=3..6",
        absnear(slope, 0.996878303620, 1e-9),
        "slope %.12f stderr %.3e N %d" % (slope, stderr, nfit),
    )

    print("\n-- gasket spectrum, boundary load, aggregate")
    phi0, total0 = g0_reference_phi()
    corner_costs = []
    gap = {}
    for g, graph, deg, heat in gaskets:
        n = graph["n"]
        evals, _deg_e = laplacian_eigs_from_edges(n, graph["edges"])
        spectra[g] = evals
        check(
            "gasket eigenvalue sum g=%d" % g,
            absnear(float(np.sum(evals)), float(np.sum(deg)), 1e-6 * n),
            "sum %.6f degree sum %.6f" % (float(np.sum(evals)), float(np.sum(deg))),
        )
        lam_max = float(evals[-1])
        qmax = 1.0 + lam_max
        check("gasket feasible g=%d" % g, qmax <= 18.0, "lambda_max(Q) %.6f" % qmax)
        positive = evals[evals > 1e-8]
        gap[g] = float(positive[0])
        Q, _ = precision(n, graph["edges"])
        ones = np.ones(n)
        image = Q @ ones
        check(
            "gasket constant mode g=%d" % g,
            np.max(np.abs(image - ones)) < 1e-8,
            "max residual %.3e" % float(np.max(np.abs(image - ones))),
        )
        if g in (0, 6):
            var_sum = float(ones @ np.linalg.solve(Q, ones))
            v_mean = var_sum / float(n * n)
            # Scalar floor at half the prior variance: a(v - v/2)/(v/2) = a.
            heat_agg = (v_mean - 0.5 * v_mean) / (0.5 * v_mean)
            check(
                "gasket mean variance g=%d" % g,
                absnear(var_sum, n, 1e-6 * n),
                "1^T Q^{-1} 1 = %.6f N %d" % (var_sum, n),
            )
            check(
                "gasket aggregate heat g=%d" % g,
                absnear(heat_agg, 1.0, 1e-9) and absnear(v_mean, 1.0 / n, 1e-8),
                "heat %.12f var(mean) %.6e" % (heat_agg, v_mean),
            )
        corners = np.asarray(graph["corners"], dtype=int)
        qdiag = np.array([Q[c, c] for c in corners])
        bound = float(np.sum(1.0 / EPS - qdiag))
        check(
            "gasket corner bound g=%d" % g,
            absnear(bound, 45.0, 1e-9),
            "bound %.6f Qdiag %s" % (bound, qdiag),
        )
        Sbb = block_covariance(Q, corners)
        phi, smax, total = uniform_phi(Sbb, EPS)
        corner_costs.append(total)
        check(
            "gasket corner load meets tolerance g=%d" % g,
            smax <= EPS * (1.0 + 1e-8) and total + 1e-8 >= bound,
            "phi %.12f total %.12f smax %.6e" % (phi, total, smax),
        )
        if g == 0:
            direct = np.linalg.inv(Q + phi * np.eye(n))
            direct_max = float(np.max(np.diag(direct)))
            check(
                "gasket g=0 load matches the closed form",
                absnear(phi, phi0, 1e-9) and absnear(total, total0, 1e-9),
                "phi %.12f total %.12f direct smax %.6e" % (phi, total, direct_max),
            )
        print(
            "  g=%d lambda1 %.8e lambda_max %.6f bound %.3f achieved %.6f ratio %.6f"
            % (g, gap[g], lam_max, bound, total, total / bound)
        )
        puzzle(
            "gasket load ratio g=%d" % g,
            total / bound < 1.15,
            "ratio %.6f" % (total / bound),
        )

    print("\n-- gasket decimation")
    for g in range(3, 6):
        ratio = gap[g] / gap[g + 1]
        print("  ratio g=%d  %.8f" % (g, ratio))
        puzzle(
            "gasket gap ratio g=%d" % g,
            abs(ratio - 5.0) <= 0.05,
            "ratio %.8f" % ratio,
        )
    slope, _b, stderr, nfit = ols(
        [3, 4, 5, 6],
        [math.log(gap[g]) for g in (3, 4, 5, 6)],
    )
    print("  log lambda1 slope %.8f stderr %.3e" % (slope, stderr))
    puzzle(
        "gasket gap slope",
        abs(slope - (-LOG5)) <= 0.05,
        "slope %.8f target %.8f" % (slope, -LOG5),
    )

    if all(corner_costs[g] > 0 for g in range(2, 7)):
        slope, _b, stderr, nfit = ols(
            [math.log(gaskets[g][1]["n"]) for g in range(2, 7)],
            [math.log(corner_costs[g]) for g in range(2, 7)],
        )
        print("  corner-cost log slope g=2..6  %.6f stderr %.3e" % (slope, stderr))
        ratios_ok = all(corner_costs[g] / 45.0 < 1.15 for g in range(2, 7))
        if ratios_ok:
            puzzle(
                "gasket corner-cost slope",
                abs(slope) < 0.20,
                "slope %.6f" % slope,
            )
        else:
            print("  corner-cost slope not scored: a load ratio missed 1.15")

    # (c1) partial sum on G_6, modes with lambda in (0, 0.2].
    evals = spectra[6]
    mask = (evals > 1e-8) & (evals <= 0.2)
    rates = 1.0 + evals[mask]
    partial = float(np.sum(1.0 / EPS - rates))
    Q6, _ = precision(gaskets[6][1]["n"], gaskets[6][1]["edges"])
    q_eigs = np.linalg.eigvalsh(Q6)
    q_mask = (q_eigs > 1.0 + 1e-8) & (q_eigs <= 1.2)
    partial_q = float(np.sum(1.0 / EPS - q_eigs[q_mask]))
    ds_scaled = partial * (math.log(3.0) / LOG5)
    check(
        "gasket partial sum matches Q eigenvalues g=6",
        near(partial, partial_q, 1e-8) and int(mask.sum()) == int(q_mask.sum()) and partial > 0.0,
        "modes %d heat %.12f Q-heat %.12f" % (int(mask.sum()), partial, partial_q),
    )
    check(
        "gasket partial sum is not multiplied by ds/2",
        abs(partial - ds_scaled) / partial > 0.2,
        "heat %.6f ds-scaled %.6f" % (partial, ds_scaled),
    )

    lams = [5.0 ** (-k) for k in (4, 3, 2, 1)]
    counts = [int(np.sum((evals > 0.0) & (evals <= L))) for L in lams]
    print("  G6 cumulative %s at %s" % (counts, [round(L, 6) for L in lams]))
    for i in range(1, len(counts)):
        if counts[i - 1] > 0 and lams[i] != lams[i - 1]:
            step = math.log(counts[i] / counts[i - 1]) / math.log(lams[i] / lams[i - 1])
            print("  cumulative step %d exponent %.6f" % (i, step))
    fit, nused = cumulative_slope(counts, lams)
    if fit is None:
        puzzle("gasket DOS slope", False, "fewer than 3 usable points (%d) counts %s" % (nused, counts))
    else:
        slope, stderr, nfit = fit
        print("  G6 DOS slope %.6f stderr %.3e points %d" % (slope, stderr, nfit))
        puzzle(
            "gasket DOS slope",
            abs(slope - (math.log(3.0) / LOG5)) <= 0.15,
            "slope %.6f target %.6f" % (slope, math.log(3.0) / LOG5),
        )

    # (c2) massive field, alpha=1, generation 6.
    a = 1.0 + evals
    m_tracked = int(np.sum(a <= 1.2))
    bins, _chosen = nonempty_bins(evals, 1e-15, 0.2)
    n_bins = len(bins)
    tracked = a[a <= 1.2]
    heat_m = float(np.sum(1.0 / EPS - tracked))
    heat_q = float(np.sum(1.0 / EPS - q_eigs[q_eigs <= 1.2]))
    print(
        "  alpha=1 g=6 M=%d n_bins=%d heat %.6f K_U %d K_E %d"
        % (m_tracked, n_bins, heat_m, k_u(1.44), k_e(1.44))
    )
    check(
        "massive tracked heat is the partial sum",
        near(heat_m, heat_q, 1e-8) and m_tracked == int(np.sum(q_eigs <= 1.2)),
        "heat %.12f Q-heat %.12f" % (heat_m, heat_q),
    )
    puzzle("massive M >= 20", m_tracked >= 20, "M %d" % m_tracked)
    puzzle("massive n_bins >= 3", n_bins >= 3, "bins %d" % n_bins)

    # Small-mass arm.
    alpha = 1e-8
    lam_lo = gap[6]
    lam_hi = 0.2
    r_stake = ((alpha + lam_hi) / (alpha + lam_lo)) ** 2
    bins_s, _ = nonempty_bins(evals, lam_lo, lam_hi)
    n_bins_s = len(bins_s)
    ku, ke = k_u(r_stake), k_e(r_stake)
    print(
        "  alpha=1e-8 g=6 lambda1 %.8e R %.6e n_bins %d K_U %d K_E %d"
        % (lam_lo, r_stake, n_bins_s, ku, ke)
    )
    puzzle(
        "small-mass bins match K_E",
        abs(n_bins_s - ke) <= 2,
        "|%d - %d| <= 2" % (n_bins_s, ke),
    )
    puzzle(
        "small-mass K_U overshoots the bins",
        ku - n_bins_s >= 2,
        "K_U - bins = %d" % (ku - n_bins_s),
    )
    return gaskets, spectra, corner_costs, gap


def run_carpet():
    print("\n-- carpet combinatorics, heat, boundary")
    achieved = []
    bounds = []
    bs = []
    ns = []
    for ngen in range(1, 5):
        graph = build_carpet(ngen)
        n = graph["n"]
        n_lock = 8 ** ngen
        edges = graph["edges"]
        e_lock = (8 * (n_lock - 3 ** ngen)) // 5
        deg = adjacency(n, edges)
        deg_sum = int(round(float(np.sum(deg))))
        b_idx = graph["boundary"]
        b_lock = 4 * (3 ** ngen - 1)
        bound_lock = 172 * 3 ** (ngen - 1) - 52
        heat = heat_from_degrees(n, deg_sum)
        heat_lock = (69 * n_lock) / 5.0 + (16 * 3 ** ngen) / 5.0
        check("carpet N n=%d" % ngen, n == n_lock, "N %d" % n)
        check("carpet edges n=%d" % ngen, len(edges) == e_lock, "E %d lock %d" % (len(edges), e_lock))
        check(
            "carpet degree sum n=%d" % ngen,
            deg_sum == 2 * e_lock,
            "sum %d" % deg_sum,
        )
        check("carpet boundary count n=%d" % ngen, int(b_idx.shape[0]) == b_lock, "B %d" % int(b_idx.shape[0]))
        check(
            "carpet heat n=%d" % ngen,
            absnear(heat, heat_lock, 1e-6),
            "heat %.6f lock %.6f per %.8f" % (heat, heat_lock, heat / n),
        )
        Q, _ = precision(n, edges)
        q_b = np.array([Q[i, i] for i in b_idx])
        bound = float(np.sum(1.0 / EPS - q_b))
        check(
            "carpet bound n=%d" % ngen,
            absnear(bound, bound_lock, 1e-6),
            "bound %.6f lock %d" % (bound, bound_lock),
        )
        # Feasibility from the degree bound, plus the computed edge of Q.
        # Full spectrum at every locked carpet generation.
        evals, _ = laplacian_eigs_from_edges(n, edges)
        qmax = 1.0 + float(evals[-1])
        check("carpet feasible n=%d" % ngen, qmax <= 18.0, "lambda_max(Q) %.6f" % qmax)
        if ngen in (1, 4):
            ones = np.ones(n)
            check(
                "carpet constant mode n=%d" % ngen,
                np.max(np.abs(Q @ ones - ones)) < 1e-6,
                "residual %.3e" % float(np.max(np.abs(Q @ ones - ones))),
            )
            var_sum = float(ones @ np.linalg.solve(Q, ones))
            check(
                "carpet mean variance n=%d" % ngen,
                absnear(var_sum, n, 1e-6 * max(n, 1)),
                "1^T Q^{-1} 1 = %.6f" % var_sum,
            )
        Sbb = block_covariance(Q, b_idx)
        phi, smax, total = uniform_phi(Sbb, EPS)
        check(
            "carpet load meets tolerance n=%d" % ngen,
            smax <= EPS * (1.0 + 1e-7) and total + 1e-6 >= bound,
            "phi %.8f total %.6f smax %.6e" % (phi, total, smax),
        )
        puzzle(
            "carpet load ratio n=%d" % ngen,
            total / bound < 1.15,
            "ratio %.6f" % (total / bound),
        )
        print(
            "  n=%d N=%d B=%d heat %.6f bound %.6f achieved %.6f ratio %.6f lambda_max %.6f"
            % (ngen, n, b_lock, heat, bound, total, total / bound, float(evals[-1]))
        )
        achieved.append(total)
        bounds.append(bound)
        bs.append(b_lock)
        ns.append(n)
        if ngen == 4:
            per = heat / n
            ds = 2.0 * math.log(3.0) / LOG5
            df = math.log(8.0) / math.log(3.0)
            # The lock also states the exact per-site value 13.86328125 and the
            # excess 3.2*(3/8)^n. That excess at n=4 is 0.06328125, so the band
            # |per-13.8|<0.01 cannot hold at the same time. Recorded as a puzzle,
            # not as an identity failure. Same for the gap of 2 against
            # 13.8*d_f/2: |13.8 - 13.8*d_f/2| = 0.73975, which is below 2 at the
            # limit, so no generation can meet it.
            excess = per - 13.8
            puzzle(
                "carpet band |per-13.8|<0.01 at n=4",
                abs(excess) < 0.01,
                "per %.12f excess %.12f locked excess 0.06328125" % (per, excess),
            )
            puzzle(
                "carpet gap from 13.8*ds/2 exceeds 2",
                abs(per - 13.8 * ds / 2.0) > 2.0,
                "gap %.6f alternative %.6f" % (abs(per - 13.8 * ds / 2.0), 13.8 * ds / 2.0),
            )
            limit_gap_df = abs(13.8 - 13.8 * df / 2.0)
            puzzle(
                "carpet gap from 13.8*df/2 exceeds 2",
                abs(per - 13.8 * df / 2.0) > 2.0,
                "gap %.6f alternative %.6f limit-gap %.6f" % (
                    abs(per - 13.8 * df / 2.0),
                    13.8 * df / 2.0,
                    limit_gap_df,
                ),
            )

    slope, _b, stderr, nfit = ols([math.log(b) for b in bs], [math.log(h) for h in bounds])
    check(
        "carpet bound-vs-B slope",
        absnear(slope, 0.988226953947, 1e-9),
        "slope %.12f stderr %.3e" % (slope, stderr),
    )
    slope_n, _b, stderr, nfit = ols(
        [math.log(n) for n in ns[1:]],
        [math.log(b / n) for b, n in zip(bounds[1:], ns[1:])],
    )
    print("  bound/N slope n=2..4 %.8f" % slope_n)
    if all(a / b < 1.15 for a, b in zip(achieved, bounds)):
        slope_c, _b, stderr, nfit = ols(
            [math.log(n) for n in ns[1:]],
            [math.log(a / n) for a, n in zip(achieved[1:], ns[1:])],
        )
        print("  achieved/N slope n=2..4 %.8f stderr %.3e" % (slope_c, stderr))
        puzzle(
            "carpet achieved/N slope",
            abs(slope_c - (-0.471679166426)) <= 0.05,
            "slope %.8f" % slope_c,
        )
    else:
        print("  achieved/N slope not scored: a load ratio missed 1.15")
    return achieved, bounds


def run_controls():
    print("\n-- lattice heat controls")
    for n in (4, 8, 16):
        n_sites, edges, _b = grid_edges(n, periodic=True)
        deg = adjacency(n_sites, edges)
        heat = heat_from_degrees(n_sites, float(np.sum(deg)))
        check(
            "periodic square heat n=%d" % n,
            absnear(heat, 13 * n_sites, 1e-9) and abs(float(np.sum(deg)) - 4 * n_sites) < 1e-9,
            "heat %.6f" % heat,
        )
        # Path, periodic: degree 2, heat 15 N. Build the cycle.
        cycle = [(i, (i + 1) % n) for i in range(n)]
        deg_p = adjacency(n, cycle)
        heat_p = heat_from_degrees(n, float(np.sum(deg_p)))
        check(
            "periodic path heat n=%d" % n,
            absnear(heat_p, 15 * n, 1e-9),
            "heat %.6f" % heat_p,
        )
    print("\n-- open square boundary")
    bounds = []
    ns = []
    for n in (4, 8, 12, 16):
        n_sites, edges, boundary = grid_edges(n, periodic=False)
        deg = adjacency(n_sites, edges)
        heat = heat_from_degrees(n_sites, float(np.sum(deg)))
        heat_lock = 13 * n * n + 4 * n
        check(
            "open square heat n=%d" % n,
            absnear(heat, heat_lock, 1e-8),
            "heat %.6f" % heat,
        )
        Q, _ = precision(n_sites, edges)
        q_b = np.array([Q[i, i] for i in boundary])
        bound = float(np.sum(1.0 / EPS - q_b))
        bound_lock = 56 * n - 52
        check(
            "open square bound n=%d" % n,
            absnear(bound, bound_lock, 1e-8),
            "bound %.6f B %d" % (bound, boundary.shape[0]),
        )
        if n == 16:
            ones = np.ones(n_sites)
            var_sum = float(ones @ np.linalg.solve(Q, ones))
            check(
                "open square mean variance n=16",
                absnear(var_sum, n_sites, 1e-6 * n_sites),
                "var sum %.6f" % var_sum,
            )
        Sbb = block_covariance(Q, boundary)
        phi, smax, total = uniform_phi(Sbb, EPS)
        check(
            "open square load n=%d" % n,
            smax <= EPS * (1.0 + 1e-7) and total + 1e-6 >= bound,
            "total %.6f smax %.3e" % (total, smax),
        )
        puzzle(
            "open square load ratio n=%d" % n,
            total / bound < 1.15,
            "ratio %.6f" % (total / bound),
        )
        print("  n=%d heat %.3f bound %.3f achieved %.6f ratio %.6f" % (n, heat, bound, total, total / bound))
        bounds.append(bound)
        ns.append(n * n)
    slope, _b, stderr, nfit = ols(
        [math.log(n) for n in ns],
        [math.log(b / n) for b, n in zip(bounds, ns)],
    )
    check(
        "open-square bound/N slope",
        absnear(slope, -0.425058011513, 1e-9),
        "slope %.12f stderr %.3e" % (slope, stderr),
    )


def next_tests():
    """Computations named after the locked run. Not gates of the prereg."""
    print("\n-- next tests, outside the lock")
    # Carpet degree sum at n=5 and n=6. No spectrum, no load.
    for ngen in (5, 6):
        graph = build_carpet(ngen)
        n = graph["n"]
        e_lock = (8 * (8 ** ngen - 3 ** ngen)) // 5
        deg_sum = int(round(float(np.sum(adjacency(n, graph["edges"])))))
        heat = heat_from_degrees(n, deg_sum)
        per = heat / n
        print(
            "  carpet n=%d N=%d edges %d lock %d heat %.6f per %.12f excess %.12f"
            % (ngen, n, len(graph["edges"]), e_lock, heat, per, per - 13.8)
        )
        check(
            "next-test carpet edges n=%d" % ngen,
            len(graph["edges"]) == e_lock and deg_sum == 2 * e_lock,
            "E %d" % len(graph["edges"]),
        )
    # One further gasket generation, gap ratio only.
    g6 = build_gasket(6)
    g7 = build_gasket(7)
    e6, _ = laplacian_eigs_from_edges(g6["n"], g6["edges"])
    e7, _ = laplacian_eigs_from_edges(g7["n"], g7["edges"])
    lam6 = float(e6[e6 > 1e-8][0])
    lam7 = float(e7[e7 > 1e-8][0])
    ratio = lam6 / lam7
    print("  gasket g=7 N=%d lambda1 %.8e ratio g=6/g=7 %.8f" % (g7["n"], lam7, ratio))
    print("  |ratio-5| = %.8f" % abs(ratio - 5.0))


def main():
    print("fractal-world checks")
    print("prereg theory/fractal_checks/PREREG.md")
    print("epsilon 1/18 = %.12f" % EPS)
    check_ladder_table()
    check_lattice_closed_form()
    lattice_cumulative_slopes()
    run_controls()
    run_graphs()
    run_carpet()
    next_tests()
    print("\nREQUIRED PASS %d  REQUIRED FAILS %d  PUZZLES %d" % (PASS, FAIL, PUZZLES))
    if FAIL == 0:
        print("ALL REQUIRED FRACTAL CHECKS PASS")
        return 0
    print("REQUIRED FRACTAL CHECKS FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
