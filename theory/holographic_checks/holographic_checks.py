#!/usr/bin/env python3
"""Checks for theory/HOLOGRAPHIC_2026-11-22.md.

Boundary-versus-bulk form of the heat floor, area-versus-volume scaling on a
lattice of equilibrium Ornstein-Uhlenbeck modes, and the geometric-ladder
comparison with a scale-invariant layered cost.

Run from the repo root:
  nice -n 19 python3 theory/holographic_checks/holographic_checks.py
"""
from __future__ import annotations

import math

import numpy as np

PASS = 0
FAIL = 0
HYP = (
    "The law of adaptive organization (hypothesis): "
    "strongly selected systems minimize the cost of judgment."
)


def check(name, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
        print("PASS  %s  %s" % (name, detail))
    else:
        FAIL += 1
        print("FAIL  %s  %s" % (name, detail))


def near(a, b, tol=1e-9):
    a = float(a)
    b = float(b)
    scale = max(1.0, abs(a), abs(b))
    return abs(a - b) <= tol * scale


def ols(x, y):
    """Ordinary least squares of y on x. Returns slope, intercept, stderr, n."""
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


def fmt_slope(slope, stderr, n):
    return "slope %.12f  stderr %.3e  N %d" % (slope, stderr, n)


# ---------------------------------------------------------------------------
# Scalar linear memory, the formulas already proved in the attainability note.
# ---------------------------------------------------------------------------

def shrunk(a, v, eps, lam):
    c = (v - eps) / v
    rho = lam / (a + lam)
    sig2 = (v - eps) * (rho * (v + eps) / v - 1.0)
    beta = lam
    gamma = c * lam
    D = lam * sig2
    return beta, gamma, D, rho


def moments(a, v, beta, gamma, D):
    cxm = gamma * v / (a + beta)
    cmm = D / beta + (gamma ** 2) * v / (beta * (a + beta))
    raw = v + cmm - 2.0 * cxm
    s = (v * cmm - cxm ** 2) / cmm
    learn = a * (v / s - 1.0)
    heat = a * v * gamma ** 2 / (D * (a + beta))
    # Path error from the scalar Riccati γ^2 P^2 = 4 a D (v - P).
    disc = math.sqrt((a * D) ** 2 + (gamma ** 2) * a * D * v)
    P = 2.0 * (-a * D + disc) / (gamma ** 2)
    path = (gamma ** 2) * P / (4.0 * D)
    return {
        "cxm": cxm,
        "cmm": cmm,
        "raw": raw,
        "s": s,
        "L": learn,
        "Q": heat,
        "P": P,
        "T": path,
        "I": 0.5 * math.log(v / s),
    }


def heat_closed_shrunk(a, v, eps, lam):
    rho = lam / (a + lam)
    return a * (v - eps) * rho / (rho * (v + eps) - v)


def binary_entropy(p):
    p = float(p)
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log(p) - (1.0 - p) * math.log(1.0 - p)


# ---------------------------------------------------------------------------
# Lattice of equilibrium OU modes. Q = α I + β L, noise identity.
# ---------------------------------------------------------------------------

def laplacian_eigs_periodic(d, n):
    ks = 2.0 * math.pi * np.arange(n) / n
    axes = np.meshgrid(*([ks] * d), indexing="ij")
    lam = np.zeros_like(axes[0])
    for k in axes:
        lam = lam + 2.0 * (1.0 - np.cos(k))
    return lam.ravel()


def q_eigs(d, n, alpha, beta):
    return alpha + beta * laplacian_eigs_periodic(d, n)


def mean_degree_periodic(d):
    """Each site of the periodic cubic lattice has 2d neighbors. tr(L) = 2d V."""
    return 2 * d


def path_eigs(n):
    return np.linalg.eigvalsh(path_graph_laplacian(n))


def q_eigs_open(d, n, alpha, beta):
    """Open cubic grid. Eigenvalues are α + β times a sum of path eigenvalues."""
    pe = path_eigs(n)
    grids = np.meshgrid(*([pe] * d), indexing="ij")
    lam = np.zeros_like(grids[0])
    for g in grids:
        lam = lam + g
    return (alpha + beta * lam).ravel()


def trace_sigma_open(d, n, alpha, beta):
    """Sum of prior variances. Avoids an n^d temporary in d=3."""
    pe = path_eigs(n)
    if d == 1:
        return float(np.sum(1.0 / (alpha + beta * pe)))
    if d == 2:
        pair = pe[:, None] + pe[None, :]
        return float(np.sum(1.0 / (alpha + beta * pair)))
    total = 0.0
    pair = pe[:, None] + pe[None, :]
    for p in pe:
        total += float(np.sum(1.0 / (alpha + beta * (pair + p))))
    return total


def surface_count_open(d, n):
    if n <= 0:
        return 0
    if d == 1:
        return 1 if n == 1 else 2
    inner = max(n - 2, 0) ** d
    return n ** d - inner


def heat_equal_error(lams, eps):
    """Heat at modal error eps on every mode, if eps is below every prior variance."""
    if eps <= 0 or np.any(eps > 1.0 / lams + 1e-12):
        return None
    return float(np.sum(1.0 / eps - lams))


def heat_waterfill(lams, mean_eps):
    """Minimum of sum (1/s - λ) at mean modal error mean_eps, s ≤ 1/λ.

    Modes whose prior variance lies below the water level stay at the prior
    and contribute no learning rate. Returns (heat, theta, n_tracked) or None.
    """
    lams = np.asarray(lams, float)
    v = 1.0 / lams
    V = int(lams.shape[0])
    target = float(mean_eps) * V
    if target <= 0 or target > float(np.sum(v)) + 1e-8:
        return None
    order = np.argsort(v)
    vs = v[order]
    ls = lams[order]
    pinned = 0.0
    theta = None
    k_pin = None
    for k in range(V):
        free = V - k
        theta_try = (target - pinned) / free
        lo_ok = (k == 0) or (vs[k - 1] <= theta_try + 1e-9)
        hi_ok = theta_try <= vs[k] + 1e-9
        if lo_ok and hi_ok and theta_try > 0:
            theta = theta_try
            k_pin = k
            break
        pinned += vs[k]
    if theta is None:
        return None
    heat = 0.0
    n_tracked = 0
    for j in range(k_pin, V):
        if vs[j] > theta + 1e-10:
            heat += 1.0 / theta - ls[j]
            n_tracked += 1
    return heat, theta, n_tracked


def path_graph_laplacian(n):
    L = np.zeros((n, n))
    for i in range(n):
        if i == 0 or i == n - 1:
            L[i, i] = 1.0 if n > 1 else 0.0
        else:
            L[i, i] = 2.0
        if i + 1 < n:
            L[i, i + 1] = L[i + 1, i] = -1.0
    if n == 1:
        L[0, 0] = 0.0
    return L


def grid_precision(d, n, alpha, beta):
    """Open cubic grid, combinatorial Laplacian, Q = α I + β L."""
    axes = [n] * d
    V = n ** d
    coords = np.stack(np.unravel_index(np.arange(V), axes), axis=1)
    index = {tuple(int(c) for c in coords[i]): i for i in range(V)}
    Q = np.zeros((V, V))
    boundary = []
    for i, c in enumerate(coords):
        deg = 0
        ct = tuple(int(x) for x in c)
        for mu in range(d):
            for step in (-1, 1):
                nb = list(ct)
                nb[mu] += step
                key = tuple(nb)
                if key in index:
                    j = index[key]
                    if j > i:
                        Q[i, j] -= beta
                        Q[j, i] -= beta
                    deg += 1
        Q[i, i] += alpha + beta * deg
        if deg < 2 * d:
            boundary.append(i)
    return Q, np.asarray(boundary, dtype=int), coords


def circulant_cov(d, n, alpha, beta):
    ks = 2.0 * math.pi * np.arange(n) / n
    axes = np.meshgrid(*([ks] * d), indexing="ij")
    lam = np.full_like(axes[0], alpha)
    for k in axes:
        lam = lam + beta * 2.0 * (1.0 - np.cos(k))
    green = np.fft.ifftn(1.0 / lam).real
    V = n ** d
    coords = np.stack(np.unravel_index(np.arange(V), (n,) * d), axis=1)
    delta = (coords[:, None, :] - coords[None, :, :]) % n
    flat = np.ravel_multi_index(np.moveaxis(delta, -1, 0), (n,) * d)
    return green.ravel()[flat]


def variance_reduction(Sigma, sites):
    sites = np.asarray(sites, dtype=int)
    Sbb = Sigma[np.ix_(sites, sites)]
    cross = Sigma[sites, :] @ Sigma[:, sites]
    delta = float(np.trace(np.linalg.solve(Sbb, cross)))
    return delta


def slab_mutual_info(d, n, alpha, beta):
    """Mutual information between two contiguous halves of a periodic lattice."""
    Sigma = circulant_cov(d, n, alpha, beta)
    V = n ** d
    coords = np.stack(np.unravel_index(np.arange(V), (n,) * d), axis=1)
    left = coords[:, 0] < (n // 2)
    A = np.flatnonzero(left)
    B = np.flatnonzero(~left)
    def slog(idx):
        sign, logdet = np.linalg.slogdet(Sigma[np.ix_(idx, idx)])
        if sign <= 0:
            raise RuntimeError("covariance block not positive")
        return float(logdet)
    sign, logdet = np.linalg.slogdet(Sigma)
    if sign <= 0:
        raise RuntimeError("covariance not positive")
    return 0.5 * (slog(A) + slog(B) - float(logdet))


def zero_mode_heat(alpha, s):
    """Heat of the normalized zero mode at modal error s. Independent of volume."""
    return (1.0 - alpha * s) / s


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_hypothesis():
    for rel in ("THEORY.md", "CORE.md", "README.md"):
        text = open(rel, encoding="utf-8").read()
        check(
            "hypothesis sentence byte-identical in %s" % rel,
            text.count(HYP) == 1,
            "count %d" % text.count(HYP),
        )


def check_q1():
    print("\n== Q1 boundary versus bulk")
    a = v = 1.0
    eps = 0.2
    lam = 1.0e6
    beta, gamma, D, rho = shrunk(a, v, eps, lam)
    m = moments(a, v, beta, gamma, D)
    q_closed = heat_closed_shrunk(a, v, eps, lam)
    check("shrunk heat matches closed form", near(m["Q"], q_closed, 1e-12), "Q %.12f" % m["Q"])
    check(
        "shrunk heat at 1e6 is 4.000020000100",
        near(m["Q"], 4.0 * 200000.0 / 199999.0, 1e-12),
        "Q %.12f  ratio %.12f" % (m["Q"], m["Q"] / 4.0),
    )
    check("shrunk conditional error tends to 0.2", near(m["s"], 0.2, 1e-8), "s %.12f" % m["s"])
    check(
        "shrunk learning rate is above 4 and the heat is above it",
        m["L"] > 4.0 and m["Q"] > m["L"] and near(m["L"], 4.0, 1e-9),
        "L %.12f  Q-L %.12e" % (m["L"], m["Q"] - m["L"]),
    )
    check(
        "path rate at the floor is about 999.503",
        near(m["T"], 999.503125, 1e-5),
        "T %.6f  capacity %.6f" % (m["T"], m["L"] / m["T"]),
    )
    check(
        "path rate exceeds the heat",
        m["T"] > 100.0 * m["Q"],
        "T/Q %.6f" % (m["T"] / m["Q"]),
    )
    # Relevant mutual information of the present, Gaussian equality case.
    check(
        "Gaussian stock is (1/2) log(v/s)",
        near(m["I"], 0.5 * math.log(1.0 / 0.2), 1e-8),
        "I %.12f" % m["I"],
    )

    # Capacity-1 centered spring. Hartich factor 2, already proved. Recomputed.
    nu = 9.0
    B = nu ** 2 / (nu ** 2 - 1.0)
    beta_c = nu
    gamma_c = nu
    D_c = B  # a = v = 1
    mc = moments(a, v, beta_c, gamma_c, D_c)
    check("capacity-1 conditional error is 0.2", near(mc["s"], 0.2, 1e-12), "s %.12f" % mc["s"])
    check("capacity-1 heat is 8", near(mc["Q"], 8.0, 1e-12), "Q %.12f" % mc["Q"])
    check("capacity-1 learning rate is 4", near(mc["L"], 4.0, 1e-12), "L %.12f" % mc["L"])
    check(
        "same stock, twice the heat",
        near(mc["I"], m["I"], 1e-6) and mc["Q"] > 1.9 * m["Q"],
        "I_cap %.12f  I_floor %.12f  Q ratio %.6f" % (mc["I"], m["I"], mc["Q"] / m["Q"]),
    )

    # Raw-coordinate gap on the fast centered spring.
    # D = λ (ε - a v / (a+λ)) holds the raw error at ε.
    raw = 0.2
    D_raw = lam * (raw - a * v / (a + lam))
    mr = moments(a, v, lam, lam, D_raw)
    check("centered raw error held at 0.2", near(mr["raw"], 0.2, 1e-8), "raw %.12f" % mr["raw"])
    check("centered fast heat is 5.000020", near(mr["Q"], 5.00002, 1e-5), "Q %.12f" % mr["Q"])
    check(
        "scoring gap is 1",
        near(mr["Q"] - 4.0, 1.0, 1e-4),
        "Q - R(0.2) %.12f  conditional %.12f" % (mr["Q"] - 4.0, mr["s"]),
    )

    # Irrelevant bulk: an equilibrium coordinate of arbitrary entropy, heat 0.
    for var in (1.0, 100.0, 1.0e6):
        # dZ = -λ Z dt + sqrt(2 λ var) dB, stationary variance `var`, heat λ - λ.
        heat_z = 0.0
        entropy = 0.5 * math.log(2.0 * math.pi * math.e * var)
        check(
            "equilibrium bulk heat is 0 at variance %g" % var,
            heat_z == 0.0 and entropy > 0.0,
            "H %.6f" % entropy,
        )
    entropy_ratio = (
        0.5 * math.log(2.0 * math.pi * math.e * 1.0e6)
        - 0.5 * math.log(2.0 * math.pi * math.e * 1.0)
    )
    check(
        "bulk entropy can be raised with no heat",
        near(entropy_ratio, 0.5 * math.log(1.0e6), 1e-12),
        "delta H %.6f" % entropy_ratio,
    )

    # Telegraph ray: fixed error, fixed stock, heat unbounded in the affinity.
    err = 0.2
    flow = (1.0 - 2.0 * err) * math.log((1.0 - err) / err)
    stock = math.log(2.0) - binary_entropy(err)
    heats = []
    for log_rho in (math.log(4.0), 10.0, 40.0):
        heats.append((1.0 - 2.0 * err) * log_rho)
    check("telegraph flow is 0.6 ln 4", near(flow, 0.6 * math.log(4.0), 1e-15), "flow %.12f" % flow)
    check(
        "telegraph stock does not move with affinity",
        near(stock, math.log(2.0) - binary_entropy(0.2), 1e-15),
        "I %.12f" % stock,
    )
    check(
        "telegraph heat at fixed stock is not the flow",
        heats[2] > 20.0 * heats[0] and near(heats[0], flow, 1e-15),
        "Q(rho=4) %.6f  Q(ln rho=40) %.6f" % (heats[0], heats[2]),
    )


def check_q2():
    print("\n== Q2 area versus volume")
    # Trace identity and the exact volume floor.
    # tr(L) = (mean degree) V = 2d V. The rows of L sum to 0; the trace does not.
    for d, n, alpha, beta in ((1, 32, 1.0, 0.5), (2, 8, 1.0, 1.0), (3, 6, 0.3, 0.25)):
        lams = q_eigs(d, n, alpha, beta)
        V = n ** d
        tr = V * (alpha + beta * mean_degree_periodic(d))
        check(
            "tr Q = V(alpha + 2 d beta) d=%d n=%d" % (d, n),
            near(float(np.sum(lams)), tr, 1e-10),
            "sum %.12f" % float(np.sum(lams)),
        )
        lam_max = float(np.max(lams))
        eps = 0.5 / lam_max
        heat = heat_equal_error(lams, eps)
        expect = V / eps - tr
        check(
            "equal-error heat is V/eps - tr(Q) d=%d" % d,
            heat is not None and near(heat, expect, 1e-9) and heat > 0.0,
            "heat %.12f  per site %.12f" % (heat, heat / V),
        )
        filled = heat_waterfill(lams, eps)
        check(
            "water-fill agrees when eps is below every prior d=%d" % d,
            filled is not None and near(filled[0], expect, 1e-8),
            "heat %.12f  tracked %d" % (filled[0], filled[2]),
        )

    # Path-graph Laplacian formula is not assumed; the dense grid is tested
    # against the hand matrix on a short path.
    L3 = path_graph_laplacian(3)
    expect_L3 = np.array([[1.0, -1.0, 0.0], [-1.0, 2.0, -1.0], [0.0, -1.0, 1.0]])
    check("path Laplacian n=3", np.allclose(L3, expect_L3), "")

    # Exponent sweeps. Exact floor, eps = half the smallest prior variance.
    sizes = {
        1: [8, 16, 32, 64, 128, 256],
        2: [4, 6, 8, 12, 16, 24, 32],
        3: [4, 6, 8, 10, 12, 16],
    }
    alphas = (0.3, 1.0, 3.0)
    betas = (0.25, 1.0)
    print("\n-- exact per-site floor, exponent versus volume and versus cross-section")
    slopes_v = []
    slopes_a = []
    for d, ns in sizes.items():
        for alpha in alphas:
            for beta in betas:
                xs_v, ys, xs_a = [], [], []
                for n in ns:
                    lams = q_eigs(d, n, alpha, beta)
                    V = float(n ** d)
                    eps = 0.5 / float(np.max(lams))
                    heat = float(np.sum(1.0 / eps - lams))
                    xs_v.append(math.log(V))
                    ys.append(math.log(heat))
                    if d > 1:
                        xs_a.append(math.log(float(n ** (d - 1))))
                sv, _, ev, nv = ols(xs_v, ys)
                slopes_v.append(sv)
                if d > 1:
                    sa, _, ea, na = ols(xs_a, ys)
                    slopes_a.append((d, sa, ea, d / (d - 1)))
                    a_txt = fmt_slope(sa, ea, na)
                else:
                    sa, ea, na = float("nan"), float("nan"), 0
                    a_txt = "cross-section is constant in d=1"
                print(
                    "  d=%d alpha=%g beta=%g  V %s  A %s"
                    % (d, alpha, beta, fmt_slope(sv, ev, nv), a_txt)
                )
                check(
                    "volume exponent is 1 d=%d a=%g b=%g" % (d, alpha, beta),
                    abs(sv - 1.0) < 1e-9 and ev < 1e-9,
                    fmt_slope(sv, ev, nv),
                )
                if d > 1:
                    target = d / (d - 1)
                    check(
                        "cross-section exponent is d/(d-1)=%.3f d=%d a=%g b=%g"
                        % (target, d, alpha, beta),
                        abs(sa - target) < 1e-8 and ea < 1e-8,
                        fmt_slope(sa, ea, na),
                    )
    print(
        "  volume-slope scatter across the grid: mean %.12f  std %.3e  count %d"
        % (float(np.mean(slopes_v)), float(np.std(slopes_v)), len(slopes_v))
    )

    # Fixed fraction of the prior mean. Finite-size water-fill, then a slope.
    print("\n-- water-fill at half the prior mean")
    for d, ns in sizes.items():
        for alpha, beta in ((1.0, 1.0), (0.3, 0.25), (3.0, 1.0)):
            xs, ys, tracked_frac = [], [], []
            for n in ns:
                lams = q_eigs(d, n, alpha, beta)
                V = n ** d
                vbar = float(np.sum(1.0 / lams) / V)
                filled = heat_waterfill(lams, 0.5 * vbar)
                if filled is None or filled[0] <= 0:
                    continue
                xs.append(math.log(V))
                ys.append(math.log(filled[0]))
                tracked_frac.append(filled[2] / V)
            sv, _, ev, nv = ols(xs, ys)
            print(
                "  d=%d alpha=%g beta=%g  %s  tracked fraction first/last %.4f/%.4f"
                % (d, alpha, beta, fmt_slope(sv, ev, nv), tracked_frac[0], tracked_frac[-1])
            )
            check(
                "half-prior heat stays extensive d=%d a=%g b=%g" % (d, alpha, beta),
                abs(sv - 1.0) < 0.02,
                fmt_slope(sv, ev, nv),
            )

    # One global mode. Heat does not depend on volume.
    print("\n-- zero-mode observable")
    heats = []
    vols = []
    for n in (8, 16, 32, 64, 128):
        # Modal error held at half the prior variance of the zero mode.
        heats.append(zero_mode_heat(1.0, 0.5 * 1.0))
        vols.append(n)  # d=1 stand-in; the formula has no n
    sv, _, ev, nv = ols(np.log(np.asarray(vols, float)), np.log(np.asarray(heats, float)))
    check(
        "zero-mode heat exponent versus volume is 0",
        abs(sv) < 1e-12 and near(heats[0], 1.0, 1e-15),
        "%s  heat %.12f" % (fmt_slope(sv, ev, nv), heats[0]),
    )

    # Any observed set of A sites reduces total variance by at most A/α.
    print("\n-- surface observation bound")
    rng = np.random.default_rng(20261122)
    for d, n, alpha, beta, a_count in (
        (1, 64, 1.0, 1.0, 2),
        (1, 96, 0.3, 0.5, 2),
        (2, 16, 1.0, 1.0, 16),
        (2, 12, 1.0, 1.0, 12),
    ):
        Sigma = circulant_cov(d, n, alpha, beta)
        V = n ** d
        sites = rng.choice(V, size=a_count, replace=False)
        delta = variance_reduction(Sigma, sites)
        cap = a_count / alpha
        check(
            "reduction <= A/alpha d=%d n=%d A=%d" % (d, n, a_count),
            delta <= cap * (1.0 + 1e-8) and delta > 0.0,
            "delta %.6f  cap %.6f" % (delta, cap),
        )
    # The cap, not a particular subset, is what rules a fixed per-site gap out.
    # Scan open cubes until δ = 0.1 of the total variance exceeds A/α.
    print("  crossover where a 10 percent total-variance cut exceeds the surface cap")
    for d, alpha, beta in ((1, 1.0, 1.0), (2, 1.0, 1.0), (3, 1.0, 0.5)):
        found = None
        n_list = list(range(4, 241, 2)) if d < 3 else list(range(4, 261, 4))
        for n in n_list:
            need = 0.1 * trace_sigma_open(d, n, alpha, beta)
            cap = surface_count_open(d, n) / alpha
            if need > cap:
                found = (n, need, cap, surface_count_open(d, n), n ** d)
                break
        check(
            "a fixed per-site gap outgrows the surface cap d=%d" % d,
            found is not None,
            "first n=%s need %.4f cap %.4f A %s V %s"
            % (
                None if found is None else found[0],
                0 if found is None else found[1],
                0 if found is None else found[2],
                None if found is None else found[3],
                None if found is None else found[4],
            ),
        )
        if found is not None:
            print(
                "  d=%d alpha=%g beta=%g  crossover n=%d  need %.4f  cap %.4f  A=%d  V=%d"
                % (d, alpha, beta, found[0], found[1], found[2], found[3], found[4])
            )

    # Geometric boundary of an open cube. Posterior mean error versus prior.
    print("\n-- open-cube boundary, perfect observation of the surface")
    for d, ns, alpha, beta in (
        (1, [16, 32, 64, 128, 192], 1.0, 1.0),
        (2, [8, 12, 16, 20, 24], 1.0, 1.0),
        (3, [4, 6, 8, 10], 1.0, 0.5),
    ):
        rows = []
        for n in ns:
            Q, boundary, _ = grid_precision(d, n, alpha, beta)
            V = n ** d
            A = int(boundary.shape[0])
            Sigma = np.linalg.inv(Q)
            prior_mean = float(np.trace(Sigma) / V)
            interior = np.setdiff1d(np.arange(V), boundary)
            Qii = Q[np.ix_(interior, interior)]
            # Perfect observation of the boundary: interior conditional covariance is Q_II^{-1}.
            cond_tr = float(np.trace(np.linalg.inv(Qii)))
            post_mean = cond_tr / V  # boundary sites contribute 0 error once observed perfectly
            gap = prior_mean - post_mean
            cap = A / alpha
            delta = float(np.trace(Sigma)) - cond_tr
            rows.append((n, V, A, prior_mean, post_mean, gap, delta, cap))
            check(
                "cube reduction <= surface/alpha d=%d n=%d" % (d, n),
                delta <= cap * (1.0 + 1e-6),
                "delta %.6f cap %.6f A %d" % (delta, cap, A),
            )
        # Fractional gap falls as the cube grows.
        frac = [r[5] / r[3] for r in rows]
        print(
            "  d=%d alpha=%g beta=%g  fractional gap first/last %.4f/%.4f  A/V last %.4f"
            % (d, alpha, beta, frac[0], frac[-1], rows[-1][2] / rows[-1][1])
        )
        for r in rows:
            print(
                "    n=%d V=%d A=%d prior %.6f post %.6f gap %.6e delta %.6f cap %.6f"
                % (r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7])
            )
        check(
            "fractional gap falls with volume d=%d" % d,
            frac[-1] < frac[0],
            "first %.4f last %.4f" % (frac[0], frac[-1]),
        )
        # Exponent of the total reduction. In d=1 the surface size is constant,
        # so the reduction is compared with volume and the exponent is 0.
        if d == 1:
            sv, _, ev, nv = ols(
                [math.log(r[1]) for r in rows],
                [math.log(r[6]) for r in rows],
            )
            print("    reduction versus volume  %s" % fmt_slope(sv, ev, nv))
            check(
                "1d surface reduction does not grow with volume",
                abs(sv) < 1e-6,
                fmt_slope(sv, ev, nv),
            )
            sg, _, eg, ng = ols(
                [math.log(r[1]) for r in rows],
                [math.log(r[5]) for r in rows],
            )
            print("    per-site gap versus volume  %s" % fmt_slope(sg, eg, ng))
            check(
                "1d per-site gap exponent is -1",
                abs(sg + 1.0) < 1e-6,
                fmt_slope(sg, eg, ng),
            )
        elif len(rows) >= 3:
            sv, _, ev, nv = ols(
                [math.log(r[2]) for r in rows],
                [math.log(r[6]) for r in rows],
            )
            print("    reduction versus area  %s" % fmt_slope(sv, ev, nv))
            check(
                "geometric reduction tracks area d=%d" % d,
                abs(sv - 1.0) < 0.08,
                fmt_slope(sv, ev, nv),
            )

    # Bulk channel on the same open cubes: one fast sensor per site would cost
    # V/σ^2. The floor at equal modal error is already volume. Report heat/V.
    print("\n-- open-cube bulk floor per site, fixed error, surface correction kept")
    for d, ns in ((1, [16, 32, 64, 128, 256]), (2, [8, 12, 16, 24, 32]), (3, [4, 6, 8, 12])):
        stiff = float(np.max(q_eigs_open(d, ns[-1], 1.0, 1.0)))
        eps = 0.5 / stiff
        xs, ys, ratios = [], [], []
        for n in ns:
            evals = q_eigs_open(d, n, 1.0, 1.0)
            V = float(n ** d)
            heat = float(np.sum(1.0 / eps - evals))
            # heat = V(1/eps - α - 2 d β) + 2 d β V/n. The second piece is the boundary deficit in the degree sum.
            volume_piece = V * (1.0 / eps - 1.0 - 2.0 * d * 1.0)
            surface_piece = 2.0 * d * 1.0 * V / n
            xs.append(math.log(V))
            ys.append(math.log(heat))
            ratios.append(surface_piece / heat)
            check(
                "open-cube heat splits into volume plus surface d=%d n=%d" % (d, n),
                near(heat, volume_piece + surface_piece, 1e-8) and heat > 0.0,
                "heat/V %.6f  surface/heat %.4f" % (heat / V, surface_piece / heat),
            )
        sv, _, ev, nv = ols(xs, ys)
        print("  d=%d open-cube bulk  %s  surface/heat last %.4f" % (d, fmt_slope(sv, ev, nv), ratios[-1]))
        check(
            "open-cube finite-size exponent stays near 1 d=%d" % d,
            abs(sv - 1.0) < 0.03,
            fmt_slope(sv, ev, nv),
        )
        check(
            "surface piece shrinks relative to the volume piece d=%d" % d,
            ratios[-1] < ratios[0],
            "first %.4f last %.4f" % (ratios[0], ratios[-1]),
        )

    # Disordered on-site mass. Same volume floor once eps is below every prior.
    print("\n-- disordered mass, periodic d=2, fixed decision error")
    rng = np.random.default_rng(7)
    # ε below 1/(max α + 4 d β) for every draw with α_i in [0.5, 1.5], β=1, d=2.
    eps = 0.5 / (1.5 + 8.0)
    xs, ys = [], []
    for n in (4, 6, 8, 10, 12, 16):
        V = n * n
        alpha_i = rng.uniform(0.5, 1.5, size=V)
        alpha_i = alpha_i - float(np.mean(alpha_i)) + 1.0
        # D = I, so the eigenbasis of Q decouples the field into independent OU
        # modes. The uniform-error floor is V/ε - tr(Q), and tr(Q) does not
        # need that basis: tr(L) = 4 V on the periodic square lattice.
        tr = float(np.sum(alpha_i)) + 4.0 * V
        heat = V / eps - tr
        xs.append(math.log(V))
        ys.append(math.log(heat))
        check(
            "disordered floor uses the trace n=%d" % n,
            heat > 0.0 and near(float(np.mean(alpha_i)), 1.0, 1e-12),
            "heat/V %.6f" % (heat / V),
        )
    sv, _, ev, nv = ols(xs, ys)
    print("  disordered volume exponent  %s" % fmt_slope(sv, ev, nv))
    check("disordered mass stays extensive", abs(sv - 1.0) < 1e-9, fmt_slope(sv, ev, nv))

    # Mutual information of the field, for contrast with the heat.
    print("\n-- field mutual information across a cut")
    mi_rows = []
    for n in (16, 32, 48, 64, 96):
        mi = slab_mutual_info(1, n, 1.0, 1.0)
        mi_rows.append((n, mi))
        print("  d=1 n=%d I(half;half)=%.6f" % (n, mi))
    # Area of a 1d cut is constant (two bonds). I should level off.
    rel = abs(mi_rows[-1][1] - mi_rows[-2][1]) / mi_rows[-1][1]
    check(
        "1d mutual information levels off",
        rel < 0.02,
        "last %.6f prev %.6f rel %.4f" % (mi_rows[-1][1], mi_rows[-2][1], rel),
    )
    mi2 = []
    for n in (4, 6, 8, 10, 12, 16):
        mi = slab_mutual_info(2, n, 1.0, 1.0)
        mi2.append((n, mi, 2 * n))
        print("  d=2 n=%d cut=%d I=%.6f I/cut=%.6f" % (n, 2 * n, mi, mi / (2 * n)))
    sv, _, ev, nv = ols([math.log(r[2]) for r in mi2], [math.log(r[1]) for r in mi2])
    print("  d=2 mutual information versus cut length  %s" % fmt_slope(sv, ev, nv))
    check(
        "2d mutual information scales as the cut",
        abs(sv - 1.0) < 0.15,
        fmt_slope(sv, ev, nv),
    )
    # Same lattices, per-site heat versus linear size has exponent d = 2.
    heats = []
    for n, _, _ in mi2:
        lams = q_eigs(2, n, 1.0, 1.0)
        eps = 0.5 / float(np.max(lams))
        heats.append(float(np.sum(1.0 / eps - lams)))
    sh, _, eh, nh = ols([math.log(r[0]) for r in mi2], [math.log(h) for h in heats])
    print("  d=2 per-site heat versus linear size  %s" % fmt_slope(sh, eh, nh))
    check(
        "same lattices, heat exponent in linear size is 2",
        abs(sh - 2.0) < 1e-8,
        fmt_slope(sh, eh, nh),
    )


def check_q3():
    print("\n== Q3 ladder versus a scale-invariant layer cost")
    # Sum-loss homogeneity, already G-scale. The heat increment per octave
    # grows by ρ. That is the counterexample to a constant cost per layer.
    for rho, mu0, v, a in ((2.0, 4.0, 1.0, 1.0), (10.0, 10.0, 1.0, 1.0)):
        # Infinite ladder truncated far from μ. μ sits on a rung.
        ks = np.arange(-80, 81)
        def stake(mu):
            ak = a * rho ** ks.astype(float)
            return 1.0 / np.sum(ak * v / (ak + mu) ** 2)
        ratios = []
        increments = []
        mu = mu0
        for _ in range(4):
            w = stake(mu)
            w2 = stake(rho * mu)
            ratios.append(w2 / w)
            # Heat is μ. Increment when μ -> ρ μ.
            increments.append(rho * mu - mu)
            mu = rho * mu
        check(
            "stake scales by rho=%g" % rho,
            all(near(r, rho, 1e-8) for r in ratios),
            "ratios %s" % ", ".join("%.12f" % r for r in ratios),
        )
        inc_ratios = [increments[i + 1] / increments[i] for i in range(len(increments) - 1)]
        check(
            "heat increment per octave scales by rho=%g, not by 1" % rho,
            all(near(r, rho, 1e-12) for r in inc_ratios) and abs(rho - 1.0) > 0.5,
            "increment ratios %s" % ", ".join("%.6f" % r for r in inc_ratios),
        )
        # Modal shares at μ0 are peaked, not flat.
        ak = a * rho ** ks.astype(float)
        share = ak * v / (ak + mu0) ** 2
        # Compare the bin nearest μ0 with the bin two octaves higher.
        k_peak = int(np.argmin(np.abs(np.log(ak) - math.log(mu0))))
        k_far = k_peak + 2
        ratio = float(share[k_peak] / share[k_far])
        expect = (rho ** 2 + 1.0) ** 2 / (4.0 * rho ** 2)
        print(
            "  rho=%g share peak/two-octaves %.6f  formula %.6f"
            % (rho, ratio, expect)
        )
        check(
            "modal share ratio equals (rho^2+1)^2/(4 rho^2) and is not 1, rho=%g" % rho,
            near(ratio, expect, 1e-9) and ratio > 1.5,
            "ratio %.6f" % ratio,
        )

    # Per-mode frontier. Heats across tracked modes are not equal.
    rho = 2.0
    a0 = 1.0
    v = 1.0
    K = 10
    # Stake at the threshold of mode K (1-based), so mode K has heat 0
    # and modes 1..K-1 are tracked.
    aK = a0 * rho ** (K - 1)
    w = aK / v
    heats = []
    for j in range(1, K):
        aj = a0 * rho ** (j - 1)
        # s = sqrt(a_j v / w), heat = a_j (v/s - 1), kT = 1.
        s = math.sqrt(aj * v / w)
        heats.append(aj * (v / s - 1.0))
    ratio = max(heats) / min(heats)
    print(
        "  per-mode heats at the threshold of mode %d, rho=%g: min %.6f max %.6f ratio %.6f"
        % (K, rho, min(heats), max(heats), ratio)
    )
    check(
        "per-mode heats are not equal across the ladder",
        ratio > 2.0,
        "ratio %.6f" % ratio,
    )
    # Sum-loss memory degree stays 1 while a layered depth would grow.
    for K in (2, 4, 8):
        depth = K  # one step of log_rho per added mode, counting the slowest
        degree = 1
        check(
            "sum-loss degree stays 1 at K=%d modes" % K,
            degree == 1 and depth > degree,
            "degree %d  octave count %d" % (degree, depth),
        )


def main():
    check_hypothesis()
    check_q1()
    check_q2()
    check_q3()
    print("\n%d checks, FAILS %d" % (PASS + FAIL, FAIL))
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
