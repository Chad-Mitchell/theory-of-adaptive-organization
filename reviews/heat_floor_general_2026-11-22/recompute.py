#!/usr/bin/env python3
"""Independent recomputation for the review of draft PR #180.

Derives the Lyapunov covariance, the Sekimoto expectation, the Riccati
path rate, and the two error allocations from the SDEs. Imports nothing
from theory/info_physics_checks/.
"""
from __future__ import annotations

import math

import numpy as np


def lyapunov(A, Q):
    """Solve A C + C A.T + Q = 0."""
    A = np.asarray(A, float)
    Q = np.asarray(Q, float)
    n = A.shape[0]
    K = np.kron(np.eye(n), A) + np.kron(A, np.eye(n))
    c = np.linalg.solve(K, -Q.reshape(-1, order="F"))
    C = c.reshape((n, n), order="F")
    return 0.5 * (C + C.T)


def linear_memory(a, v, beta, gamma, D):
    """One memory dM = (-beta M + gamma·X) dt + sqrt(2D) dB.

    Returns Sekimoto heat, Gaussian learning rate, sum-error, marginal
    conditional variances, and the conditional covariance.
    """
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    gamma = np.asarray(gamma, float)
    K = a.shape[0]
    n = K + 1
    A = np.zeros((n, n))
    Q = np.zeros((n, n))
    for i in range(K):
        A[i, i] = -a[i]
        Q[i, i] = 2.0 * a[i] * v[i]
        A[K, i] = gamma[i]
    A[K, K] = -beta
    Q[K, K] = 2.0 * D
    C = lyapunov(A, Q)
    Sxx = C[:K, :K]
    Sxm = C[:K, K]
    Smm = float(C[K, K])
    # Prior covariance must stay diagonal with the named variances.
    prior_err = np.max(np.abs(Sxx - np.diag(v)))
    Sc = Sxx - np.outer(Sxm, Sxm) / Smm
    Ddiff = np.diag(a * v)
    Sigma = np.diag(v)
    L = float(np.trace(Ddiff @ (np.linalg.inv(Sc) - np.linalg.inv(Sigma))))
    f2 = (
        beta ** 2 * Smm
        + float(gamma @ Sxx @ gamma)
        - 2.0 * beta * float(gamma @ Sxm)
    )
    heat = f2 / D - beta
    ones = np.ones(K)
    eps = float(ones @ Sc @ ones)
    raw = float(np.sum(np.diag(Sxx)) + K * 0.0)  # placeholder, unused
    return {
        "heat": heat,
        "L": L,
        "sum_error": eps,
        "marginals": np.diag(Sc).copy(),
        "Sc": Sc,
        "Sxx": Sxx,
        "Sxm": Sxm,
        "Smm": Smm,
        "prior_err": prior_err,
        "raw_vs_signal": None,
    }


def shrunk_spring(a, v, eps, lam):
    """Rest point c X with c = (v-eps)/v. Noise chosen so E[(M-X)^2] = eps.

    The noise follows from the stationary moments, not from a copied formula.
    """
    c = (v - eps) / v
    beta = lam
    gamma = c * lam
    # C_XM = gamma v / (a+beta), C_MM = gamma^2 v / (beta (a+beta)) + D/beta.
    cx = gamma * v / (a + beta)
    # E[(M-X)^2] = C_MM + v - 2 cx = eps
    # C_MM = gamma**2 * v / (beta * (a+beta)) + D/beta
    # so D/beta = eps - v + 2 cx - gamma**2 * v / (beta * (a+beta))
    sig2 = eps - v + 2.0 * cx - (gamma ** 2) * v / (beta * (a + beta))
    D = beta * sig2
    out = linear_memory([a], [v], beta, [gamma], D)
    Cxx = float(out["Sxx"][0, 0])
    Cxm = float(out["Sxm"][0])
    Cmm = out["Smm"]
    raw = Cmm + Cxx - 2.0 * Cxm
    cond = Cxx - Cxm ** 2 / Cmm
    out["raw"] = raw
    out["cond"] = cond
    out["sig2"] = sig2
    out["c"] = c
    return out


def solve_mu(a, v, eps):
    """Unique mu >= 0 with sum a v / (a+mu) = eps. Bisection."""
    a = np.asarray(a, float)
    v = np.asarray(v, float)

    def err(mu):
        return float(np.sum(a * v / (a + mu)))

    lo, hi = 0.0, 1.0
    while err(hi) > eps:
        hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if err(mid) > eps:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def separate_allocation(a, v, eps):
    """Minimize sum a(v/s - 1) on sum s = eps, 0 < s <= v.

    Stationarity: a v / s^2 equal on every free coordinate.
    """
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    V = float(np.sum(v))

    def total(lam):
        return float(np.sum(np.minimum(v, np.sqrt(a * v / lam))))

    lo, hi = 0.0, 1.0
    while total(hi) > eps:
        hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if total(mid) > eps:
            lo = mid
        else:
            hi = mid
    lam = 0.5 * (lo + hi)
    s = np.minimum(v, np.sqrt(a * v / max(lam, 1e-300)))
    heat = 0.0
    for ai, vi, si in zip(a, v, s):
        heat += ai * (vi / si - 1.0)
    return heat, s, lam


def trace_cost(a, v, w):
    if w <= a / v:
        return v, 0.0, w * v
    s = math.sqrt(a * v / w)
    heat = a * (v - s) / s
    return s, heat, heat + w * s


def sum_frontier(a, v, w):
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    w0 = 1.0 / float(np.sum(v / a))
    if w <= w0:
        return 0.0, float(np.sum(v)), w * float(np.sum(v))
    target = 1.0 / w
    lo, hi = 0.0, 1.0
    while float(np.sum(a * v / (a + hi) ** 2)) > target:
        hi *= 2.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        s = float(np.sum(a * v / (a + mid) ** 2))
        if s > target:
            lo = mid
        else:
            hi = mid
    mu = 0.5 * (lo + hi)
    eps = float(np.sum(a * v / (a + mu)))
    return mu, eps, mu + w * eps


def duncan_rate(a, v, gamma, D, t_end=80.0, n=80000):
    """Steady Duncan rate of dY = gamma·X dt + sqrt(2D) dB, by the Riccati."""
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    gamma = np.asarray(gamma, float)
    F = -np.diag(a)
    Q = np.diag(2.0 * a * v)
    P = np.diag(v.copy())
    dt = t_end / n
    H = gamma.reshape(1, -1)
    Rinv = 1.0 / (2.0 * D)
    for _ in range(n):
        HP = H @ P
        innov = HP.T @ (Rinv * HP)
        dP = F @ P + P @ F.T - innov + Q
        P = P + dt * dP
        P = 0.5 * (P + P.T)
    T = float(np.asarray(H @ P @ H.T).reshape(-1)[0] / (4.0 * D))
    return P, T


def main():
    print("numpy", np.__version__)
    print()

    # --- (1) product of shrunk springs ---
    print("== product springs, lambda = 1e6 ==")
    floors = []
    heats = []
    for a, v, eps in ((1.0, 1.0, 0.2), (4.0, 0.5, 0.1)):
        out = shrunk_spring(a, v, eps, 1e6)
        R = a * (v - eps) / eps
        floors.append(R)
        heats.append(out["heat"])
        print(
            "a=%.1f v=%.1f eps=%.1f  heat=%.12f  raw=%.12f  cond=%.12f  "
            "L=%.12f  floor=%.12f  sig2=%.12e  prior_err=%.3e"
            % (
                a,
                v,
                eps,
                out["heat"],
                out["raw"],
                out["cond"],
                out["L"],
                R,
                out["sig2"],
                out["prior_err"],
            )
        )
    print("sum heat %.12f  sum floor %.12f" % (sum(heats), sum(floors)))

    # Exact rational values of the moment formula, printed for the record.
    # rho = lam/(a+lam), heat = a(v-eps) * rho / (rho(v+eps)-v),
    # which is what the moment solution gives. Checked against the Lyapunov heat above.
    def moment_heat(a, v, eps, lam):
        rho = lam / (a + lam)
        return a * (v - eps) * rho / (rho * (v + eps) - v)

    print(
        "moment formula %.12f  %.12f"
        % (moment_heat(1, 1, 0.2, 1e6), moment_heat(4, 0.5, 0.1, 1e6))
    )
    print(
        "fractions 800000/199999 = %.15f   1600000/99998 = %.15f"
        % (800000 / 199999, 1600000 / 99998)
    )

    # Correlated error covariance at the same marginals.
    Ddiff = np.diag([1.0, 2.0])
    S0 = np.diag([0.3, 0.4])
    S1 = np.array([[0.3, 0.1], [0.1, 0.4]])
    rho = 0.1
    c_rho = rho * math.sqrt(0.3 * 0.4)
    Srho = np.array([[0.3, c_rho], [c_rho, 0.4]])
    t0 = float(np.trace(Ddiff @ np.linalg.inv(S0)))
    t1 = float(np.trace(Ddiff @ np.linalg.inv(S1)))
    tr = float(np.trace(Ddiff @ np.linalg.inv(Srho)))
    print(
        "tr(D S^{-1}) diagonal %.12f  off-diagonal entry 0.1 -> %.12f  "
        "correlation coefficient 0.1 (entry %.6f) -> %.12f"
        % (t0, t1, c_rho, tr)
    )
    # Schur: inverse diagonal dominates 1/marginal.
    inv = np.linalg.inv(S1)
    print(
        "Schur (S^{-1})_11=%.6f > 1/0.3=%.6f   (S^{-1})_22=%.6f > 1/0.4=%.6f"
        % (inv[0, 0], 1 / 0.3, inv[1, 1], 1 / 0.4)
    )

    # A joint one-memory channel cannot undercut the sum of the marginal floors
    # at these two decision errors. Rank-one precision updates are the extreme.
    print()
    print("== joint vs product at marginal targets 0.2 and 0.1 ==")
    # Not a minimization over all channels: a grid of rank-one gains, scored by
    # whether both marginal conditional variances meet the targets, and the heat.
    # The product floor is 20. Any feasible joint design must sit at or above it;
    # this grid is a search, not a proof.
    best = None
    for g1 in np.linspace(0.05, 4.0, 40):
        for g2 in np.linspace(-4.0, 4.0, 80):
            for sig2 in (0.05, 0.2, 0.5, 1.0, 2.0):
                # static channel Y = g·X + noise, precision gg^T/sig2
                g = np.array([g1, g2])
                Sigma = np.diag([1.0, 0.5])
                Ddiff = np.diag([1.0 * 1.0, 4.0 * 0.5])
                Phi = np.outer(g, g) / sig2
                S = np.linalg.inv(np.linalg.inv(Sigma) + Phi)
                if S[0, 0] <= 0.2 + 1e-9 and S[1, 1] <= 0.1 + 1e-9:
                    rate = float(np.trace(Ddiff @ Phi))
                    if best is None or rate < best[0]:
                        best = (rate, g1, g2, sig2, S[0, 0], S[1, 1])
    print("best rank-one static channel on the grid meeting both marginals:", best)
    print("product floor 20")

    # --- (2) per-mode frontier ---
    print()
    print("== per-mode frontier, a=(1,10,100), v=1 ==")
    modes = [(1.0, 1.0), (10.0, 1.0), (100.0, 1.0)]
    for w in (0.5, 2.0, 20.0, 200.0):
        n = 0
        J = 0.0
        parts = []
        for a, v in modes:
            s, heat, cost = trace_cost(a, v, w)
            J += cost
            if w + 0.0 >= a / v:
                n += 1
            parts.append((s, heat, cost))
        print("w=%g tracked=%d J=%.12f parts=%s" % (w, n, J, parts))
    # geometric count
    print("geometric count, rho=10, a0=1, v=1, by comparing a*rho^(k-1) to w")
    for w in (0.5, 1.0, 2.0, 10.0, 100.0, 1000.0):
        rates = [10.0 ** (k - 1) for k in range(1, 8)]
        Kh = sum(1 for r in rates if r <= w)
        print("  w=%g K_hard=%d" % (w, Kh))

    # --- (3) sum loss ---
    print()
    print("== sum loss, rates 1 and 100, sum-error 0.5 ==")
    a = np.array([1.0, 100.0])
    v = np.array([1.0, 1.0])
    # exact root of mu^2 - 101 mu - 300 = 0
    disc = 101.0 ** 2 + 1200.0
    mu_exact = (101.0 + math.sqrt(disc)) / 2.0
    mu = solve_mu(a, v, 0.5)
    print("mu exact %.15f  bisection %.15f  disc %.1f" % (mu_exact, mu, disc))
    print(
        "back-substitution sum a v/(a+mu) = %.15f"
        % float(np.sum(a * v / (a + mu_exact)))
    )
    g = 1.0 / (a + mu_exact)
    sig2 = float(np.sum(a * v * g ** 2) / mu_exact)
    print("gains %.12f %.12f  sig2 %.12e" % (g[0], g[1], sig2))
    fast = linear_memory(a, v, 1e6, 1e6 * g, 1e6 * sig2)
    print(
        "lambda 1e6  heat %.12f  L %.12f  sum-error %.12f  mu %.12f"
        % (fast["heat"], fast["L"], fast["sum_error"], mu_exact)
    )
    # floor at the error the spring actually reaches
    mu_at = solve_mu(a, v, fast["sum_error"])
    print(
        "floor at the realized sum-error %.12f  heat minus that floor %.6e"
        % (mu_at, fast["heat"] - mu_at)
    )
    heat_sep, s_sep, lam_sep = separate_allocation(a, v, 0.5)
    print(
        "separate heat %.12f  errors %.12f %.12f  ratio %.12f"
        % (heat_sep, s_sep[0], s_sep[1], heat_sep / mu_exact)
    )
    # exact separate allocation s2 = 10 s1, s1+s2=1/2
    s1 = 0.5 / 11.0
    s2 = 5.0 / 11.0
    hexact = 1.0 * (1.0 / s1 - 1.0) + 100.0 * (1.0 / s2 - 1.0)
    print("exact separate errors %.15f %.15f heat %.15f" % (s1, s2, hexact))

    # Unweighted sum: one gain on Z = X1+X2. Learning rate at sum-error 0.5.
    # g_k = g, v_k = 1. Solved in closed form in the review text; checked here.
    # eps = 2 - 4 g^2 / (sig2 + 2 g^2) = 0.5 => sig2 = (2/3) g^2
    # rate = (1+100) g^2 / sig2 = 151.5
    print("unweighted-sum channel learning rate at sum-error 0.5: %.6f" % (101.0 * 1.5))
    # Confirm with the static formula over a scalar g.
    g_u = 1.0
    sig2_u = (2.0 / 3.0) * g_u ** 2
    V = 2.0
    eps_u = V - (2.0 * g_u) ** 2 / (sig2_u + 2.0 * g_u ** 2)
    rate_u = (1.0 + 100.0) * g_u ** 2 / sig2_u
    print("unweighted check eps %.12f rate %.12f" % (eps_u, rate_u))

    # Equal rates: mu equals the scalar Kalman rate of the sum, and the
    # unweighted gain is the optimal gain.
    print()
    print("== identical modes ==")
    for K, eps in ((2, 0.8), (3, 1.1), (4, 0.5)):
        joint = 1.0 * (K - eps) / eps
        sep = K * (1.0 / (eps / K) - 1.0)
        muK = solve_mu(np.ones(K), np.ones(K), eps)
        print(
            "K=%d eps=%.3f scalar=%.12f mu=%.12f separate=%.12f ratio=%.1f"
            % (K, eps, joint, muK, sep, sep / joint)
        )
    # unequal variances, equal rates
    mu_uv = solve_mu(np.array([1.0, 1.0]), np.array([1.0, 4.0]), 2.0)
    h_uv, s_uv, _ = separate_allocation(np.array([1.0, 1.0]), np.array([1.0, 4.0]), 2.0)
    print(
        "rates (1,1) variances (1,4) eps 2: mu %.12f (scalar of variance 5 is %.12f) separate %.12f s=%s"
        % (mu_uv, (5.0 - 2.0) / 2.0, h_uv, s_uv)
    )

    # Random conditional covariances cannot undercut mu.
    print()
    print("== random covariances against the sum-loss floor ==")
    rng = np.random.default_rng(19)
    a = np.array([1.0, 100.0])
    v = np.array([1.0, 1.0])
    Sigma = np.diag(v)
    Ddiff = np.diag(a * v)
    worst_slack = 1e9
    n_under = 0
    for _ in range(400):
        G = rng.normal(size=(2, 2))
        Phi = G @ G.T
        S = np.linalg.inv(np.linalg.inv(Sigma) + Phi)
        # enforce S ≼ Sigma by construction of Phi ≽ 0
        eps = float(np.ones(2) @ S @ np.ones(2))
        if not (0.05 < eps < 1.9):
            continue
        rate = float(np.trace(Ddiff @ Phi))
        bound = solve_mu(a, v, eps)
        slack = rate - bound
        if slack < -1e-8:
            n_under += 1
        worst_slack = min(worst_slack, slack)
    print("undercuts %d  smallest rate-minus-mu %.6e" % (n_under, worst_slack))

    # --- frontiers, identical K=3 ---
    print()
    print("== sum frontier, K=3 identical ==")
    for w in (0.2, 0.5, 2.0, 8.0):
        mu, eps, J = sum_frontier(np.ones(3), np.ones(3), w)
        Jsep = 3.0 * trace_cost(1.0, 1.0, w)[2]
        if w <= 1.0 / 3.0:
            Jstar = 3.0 * w
            mstar = 0.0
        else:
            Jstar = 2.0 * math.sqrt(3.0 * w) - 1.0
            mstar = math.sqrt(3.0 * w) - 1.0
        print(
            "w=%g mu=%.12f (formula %.12f) eps=%.12f J=%.12f (formula %.12f) sep=%.12f"
            % (w, mu, mstar, eps, J, Jstar, Jsep)
        )
    # ratio of optimized costs at large stake
    w = 1e6
    _, _, Jb = sum_frontier(np.ones(3), np.ones(3), w)
    Js = 3.0 * trace_cost(1.0, 1.0, w)[2]
    print("at w=1e6 separate/joint %.6f  sqrt(3)=%.6f" % (Js / Jb, math.sqrt(3.0)))

    # finite ladder
    print()
    print("== four-mode ladder ==")
    a = np.array([1.0, 10.0, 100.0, 1000.0])
    v = np.ones(4)
    w0 = 1.0 / float(np.sum(v / a))
    print(
        "w0 from sum(v/a)=%.15f  exact 1000/1111=%.15f  three-mode 100/111=%.15f"
        % (w0, 1000 / 1111, 100 / 111)
    )
    for w in (0.5, 2.0, 8.0, 40.0, 200.0, 2000.0):
        mu, eps, J = sum_frontier(a, v, w)
        half = int(np.sum(a <= mu + 1e-9)) if mu > 0 else 0
        hard = int(np.sum(w >= a))
        print("w=%g mu=%.6f half=%d hard=%d eps=%.6f" % (w, mu, half, hard, eps))

    # infinite ladder
    print()
    rho = 10.0
    ks = np.arange(-30, 31)
    def stake(mu):
        ak = rho ** ks
        return 1.0 / np.sum(ak / (ak + mu) ** 2)
    print(
        "infinite ladder w(500)/w(50) = %.15f   w(10*mu)/w(mu) at mu=50: %.15f"
        % (stake(500.0) / stake(50.0), stake(rho * 50.0) / stake(50.0))
    )
    # set difference has one new index
    def edge(mu):
        return int(np.sum(ks <= math.log(mu) / math.log(rho) + 1e-12))
    # a_k = rho^k <= mu iff k <= log(mu)/log(rho)
    print("count of k in [-30,30] with rho^k <= 50, and <= 500:", end=" ")
    print(int(np.sum(rho ** ks <= 50)), int(np.sum(rho ** ks <= 500)))

    # --- coupled spring ---
    print()
    print("== coupled spring ==")
    Sigma = np.array([[1.0, 0.3], [0.3, 1.0]])
    D_c = np.array([[0.8, 0.1], [0.1, 1.2]])
    A_decay = D_c @ np.linalg.inv(Sigma)
    lyap_res = A_decay @ Sigma + Sigma @ A_decay.T - 2.0 * D_c
    print("signal Lyapunov residual max %.3e" % np.max(np.abs(lyap_res)))
    # signal bath cancellation
    score = np.linalg.inv(Sigma) @ D_c @ np.linalg.inv(Sigma)
    print(
        "signal bath E[x A x] - tr = %.3e"
        % (float(np.trace(score @ Sigma)) - float(np.trace(D_c @ np.linalg.inv(Sigma))))
    )
    sig2 = 0.25
    lam = 1e5
    n = 4
    A = np.zeros((n, n))
    Q = np.zeros((n, n))
    A[:2, :2] = -A_decay
    Q[:2, :2] = 2.0 * D_c
    A[2:, :2] = lam * np.eye(2)
    A[2:, 2:] = -lam * np.eye(2)
    Q[2:, 2:] = 2.0 * lam * sig2 * np.eye(2)
    C = lyapunov(A, Q)
    Sxx = C[:2, :2]
    Sxm = C[:2, 2:]
    Smm = C[2:, 2:]
    Sc = Sxx - Sxm @ np.linalg.inv(Smm) @ Sxm.T
    L = float(np.trace(D_c @ (np.linalg.inv(Sc) - np.linalg.inv(Sigma))))
    E_dx = Sxx + Smm - Sxm - Sxm.T
    heat = (lam / sig2) * float(np.trace(E_dx)) - 2.0 * lam
    static = float(np.trace(D_c) / sig2)
    print(
        "heat %.12f  L %.12f  static %.12f  heat-L %.6e" % (heat, L, static, heat - L)
    )

    # reference gap
    print()
    print("== reference two-mode gap ==")
    ref = linear_memory(
        np.array([1.0, 4.0]),
        np.array([1.0, 0.5]),
        3.0,
        np.array([2.0, -1.0]),
        0.4,
    )
    print(
        "heat %.12f  L %.12f  gap %.12f" % (ref["heat"], ref["L"], ref["heat"] - ref["L"])
    )

    # path rate of the weighted spring at lambda 500
    print()
    print("== path rate, weighted spring, lambda 500 ==")
    a = np.array([1.0, 4.0])
    v = np.array([1.0, 1.0])
    mu = 2.0
    g = 1.0 / (a + mu)
    sig2 = float(np.sum(a * v * g ** 2) / mu)
    P, T = duncan_rate(a, v, 500.0 * g, 500.0 * sig2)
    mem = linear_memory(a, v, 500.0, 500.0 * g, 500.0 * sig2)
    print(
        "path %.12f  L %.12f  heat %.12f  sum-error %.12f" % (T, mem["L"], mem["heat"], mem["sum_error"])
    )
    # scalar Duncan identity, algebraic Riccati (the Euler step overflows at lambda 1e6)
    print("scalar Duncan identity on one shrunk spring")

    def scalar_duncan(a, v, eps, lam):
        c = (v - eps) / v
        gamma = c * lam
        cx = gamma * v / (a + lam)
        sig2 = eps - v + 2.0 * cx - (gamma ** 2) * v / (lam * (a + lam))
        D = lam * sig2
        inner = 1.0 + (v * gamma ** 2) / (a * D)
        P = (2.0 * a * D * (-1.0 + math.sqrt(inner))) / gamma ** 2
        T = a * (v - P) / P
        Td = gamma ** 2 * P / (4.0 * D)
        return P, T, Td

    P1, T1, Td1 = scalar_duncan(1.0, 1.0, 0.2, 1e6)
    print("P %.12f  a(v-P)/P %.12f  gamma^2 P/(4D) %.12f" % (P1, T1, Td1))
    print(
        "two copies at eps 0.2: path %.12f  floor 8  ratio floor/path %.12f"
        % (2 * T1, 8.0 / (2 * T1))
    )

    # Confirm block for the repair at 661abc8. Own arithmetic only.
    print()
    print("== confirm 661abc8 ==")
    from fractions import Fraction

    w0_frac = Fraction(1000, 1111)
    # Round half away from zero at the 13th decimal, which is the digit after 12 places.
    # 1000/1111 = 0.9000900090009... with digit 13 equal to 9, so the 12-place value rounds up.
    scaled = (w0_frac * 10**13 + Fraction(1, 2)) // 1  # not used; print the expansion
    digits = []
    rem = 1000
    for _ in range(16):
        rem *= 10
        digits.append(rem // 1111)
        rem %= 1111
    twelve = "".join(str(d) for d in digits[:12])
    # round using digit 13
    if digits[12] >= 5:
        twelve = str(int(twelve) + 1).zfill(12)
    w0_12 = "0." + twelve
    a4 = np.array([1.0, 10.0, 100.0, 1000.0])
    v4 = np.ones(4)
    w0_float = 1.0 / float(np.sum(v4 / a4))
    print("digits", "".join(str(d) for d in digits))
    print("w0 fraction 1000/1111 rounded to 12 decimals:", w0_12)
    print("w0 float %.16f  formatted %.12f" % (w0_float, w0_float))
    print("float matches 1000/1111 within 1e-15:", abs(w0_float - 1000.0 / 1111.0) < 1e-15)
    print("three-mode 100/111 formatted %.12f" % (100.0 / 111.0))

    Ddiff = np.diag([1.0, 2.0])
    Sdiag = np.diag([0.3, 0.4])
    Sentry = np.array([[0.3, 0.1], [0.1, 0.4]])
    coeff = 0.1
    entry_at_coeff = coeff * math.sqrt(0.3 * 0.4)
    Srho = np.array([[0.3, entry_at_coeff], [entry_at_coeff, 0.4]])
    td = float(np.trace(Ddiff @ np.linalg.inv(Sdiag)))
    tentry = float(np.trace(Ddiff @ np.linalg.inv(Sentry)))
    trho = float(np.trace(Ddiff @ np.linalg.inv(Srho)))
    rho_of_entry = 0.1 / math.sqrt(0.12)
    print("diag %.15f" % td)
    print("entry 0.1 %.15f" % tentry)
    print("coeff of entry 0.1 %.15f" % rho_of_entry)
    print("entry at coeff 0.1 %.15f" % entry_at_coeff)
    print("trace at coeff 0.1 %.15f" % trho)

    print("geometric floor count, rho=10, a=v=kT=1")
    for w in (0.5, 1.0, 2.0, 10.0, 100.0, 1000.0):
        if w < 1.0:
            Kh = 0
            formula = None
        else:
            raw = math.log(w / 1.0) / math.log(10.0)
            formula = math.floor(raw) + 1
            rates = [10 ** (k - 1) for k in range(1, 8)]
            Kh = sum(1 for r in rates if r <= w)
        print("  w=%g count_by_rate=%d floor(log)=%s raw_log=%.16f" % (w, Kh, formula, raw if w >= 1 else float("nan")))


if __name__ == "__main__":
    main()
