#!/usr/bin/env python3
"""Checks for theory/INFO_PHYSICS_GENERAL.md.

Heat floor for a vector of exogenous equilibrium Ornstein–Uhlenbeck modes,
the sum of those modes, and the comparison with the layer-count rule.

Run from the repo root:
  nice -n 19 python3 theory/info_physics_checks/general_checks.py
"""
from __future__ import annotations

import math

import numpy as np

PASS = 0
FAIL = 0


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


def lyapunov(A, Q):
    """Solve A C + C A.T + Q = 0. Column-major Kronecker form."""
    n = A.shape[0]
    Kmat = np.kron(np.eye(n), A) + np.kron(A, np.eye(n))
    c = np.linalg.solve(Kmat, -np.asarray(Q, float).reshape(-1, order="F"))
    C = c.reshape((n, n), order="F")
    return 0.5 * (C + C.T)


def kalman_rate(a, v, eps):
    return a * (v - eps) / eps


def heat_closed(a, v, beta, gamma, D):
    """Sekimoto heat of one linear memory driven by independent OU modes."""
    s = 0.0
    for ai, vi, gi in zip(a, v, gamma):
        s += ai * vi * gi * gi / (D * (ai + beta))
    return s


def gap_closed(a, v, beta, gamma, D):
    """Algebraic heat minus learning rate. Both terms are nonnegative."""
    q = []
    for ai, vi, gi in zip(a, v, gamma):
        q.append(ai * vi * gi * gi / (ai + beta) ** 2)
    q = np.asarray(q, float)
    N = float(np.sum(q))
    return float(np.sum(np.asarray(a) * q) / D + beta * N * N / (D * (D + N)))


def moments_and_learning(a, v, beta, gamma, D):
    """Joint Lyapunov of (X, M). Returns heat, learning rate, sum-error, marginals."""
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
    Smm = C[K, K]
    Sc = Sxx - np.outer(Sxm, Sxm) / Smm
    Ddiff = np.diag(a * v)
    Sigma = np.diag(v)
    L = float(np.trace(Ddiff @ (np.linalg.inv(Sc) - np.linalg.inv(Sigma))))
    f2 = beta ** 2 * Smm + float(gamma @ Sxx @ gamma) - 2.0 * beta * float(gamma @ Sxm)
    Qh = f2 / D - beta
    ones = np.ones(K)
    eps = float(ones @ Sc @ ones)
    return Qh, L, eps, np.diag(Sc).copy(), Sc


def mu_of_sum_error(a, v, eps):
    """Learning rate mu with sum_k a_k v_k / (a_k + mu) = eps."""
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    V = float(np.sum(v))
    if not (0.0 < eps < V):
        raise ValueError("eps outside (0, V)")
    lo, hi = 0.0, 1.0
    while float(np.sum(a * v / (a + hi))) > eps:
        hi *= 2.0
        if hi > 1e18:
            break
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        e = float(np.sum(a * v / (a + mid)))
        if e > eps:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def separate_heat(a, v, eps):
    """Minimum of sum a(v/s - 1) subject to sum s = eps and 0 < s <= v."""
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    V = float(np.sum(v))
    if eps >= V - 1e-15:
        return 0.0, v.copy()
    lo, hi = 0.0, 1.0

    def total(lam):
        if lam <= 0.0:
            return V
        return float(np.sum(np.minimum(v, np.sqrt(a * v / lam))))

    while total(hi) > eps:
        hi *= 2.0
        if hi > 1e18:
            break
    for _ in range(90):
        mid = 0.5 * (lo + hi)
        if total(mid) > eps:
            lo = mid
        else:
            hi = mid
    lam = 0.5 * (lo + hi)
    s = np.minimum(v, np.sqrt(a * v / lam))
    # Renormalize the free coordinates if a cap made the sum miss eps slightly.
    heat = 0.0
    for ai, vi, si in zip(a, v, s):
        if si < vi - 1e-10:
            heat += ai * (vi / si - 1.0)
    return heat, s


def trace_frontier_mode(a, v, w, kT=1.0):
    """Scalar frontier of one mode. Blind cost w*v below the threshold."""
    if w <= kT * a / v:
        return v, 0.0, w * v
    eps = math.sqrt(kT * a * v / w)
    heat = kT * a * (v - eps) / eps
    return eps, heat, heat + w * eps


def sum_mu_star(a, v, w, kT=1.0):
    """Stationary mu of the sum-loss frontier. Zero when the design is blind."""
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    if w * float(np.sum(v / a)) <= kT:
        return 0.0
    target = kT / w
    lo, hi = 0.0, 1.0
    while float(np.sum(a * v / (a + hi) ** 2)) > target:
        hi *= 2.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        s = float(np.sum(a * v / (a + mid) ** 2))
        if s > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def sum_error_of_mu(a, v, mu):
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    if mu <= 0.0:
        return float(np.sum(v))
    return float(np.sum(a * v / (a + mu)))


def scalar_path_rate(a, v, beta, gamma, D):
    """Duncan rate of one OU observed as dY = gamma X dt + sqrt(2D) dB."""
    # gamma^2 P^2 = 4 a D (v - P), positive root below v.
    disc = (a * D) ** 2 + a * D * v * gamma ** 2
    P = (2.0 * a * D * (-1.0 + math.sqrt(1.0 + (v * gamma ** 2) / (a * D)))) / gamma ** 2
    T = a * (v - P) / P
    T_d = gamma ** 2 * P / (4.0 * D)
    return P, T, T_d


def vector_path_rate(a, v, gamma, D, t_end=40.0, n=20000):
    """Steady Duncan rate for dY = gamma·X dt + sqrt(2D) dB, by integrating the Riccati."""
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    gamma = np.asarray(gamma, float)
    K = a.shape[0]
    F = -np.diag(a)
    Q = np.diag(2.0 * a * v)
    P = np.diag(v.copy())
    dt = t_end / n
    Rinv = 1.0 / (2.0 * D)
    H = gamma.reshape(1, K)
    for _ in range(n):
        HP = H @ P
        innov = (HP.T @ (Rinv * HP))
        dP = F @ P + P @ F.T - innov + Q
        P = P + dt * dP
        P = 0.5 * (P + P.T)
    T = float(np.asarray(H @ P @ H.T).reshape(-1)[0] * Rinv * 0.5)
    return P, T


def main():
    rng = np.random.default_rng(19)

    # --- closed form heat and nonnegative gap ---
    worst_rel = 0.0
    worst_gap = 0.0
    for _ in range(40):
        K = int(rng.integers(1, 5))
        a = rng.uniform(0.2, 8.0, size=K)
        v = rng.uniform(0.2, 3.0, size=K)
        beta = float(rng.uniform(0.3, 20.0))
        gamma = rng.uniform(-4.0, 4.0, size=K)
        D = float(rng.uniform(0.05, 5.0))
        Qh, L, eps, marg, Sc = moments_and_learning(a, v, beta, gamma, D)
        Qc = heat_closed(a, v, beta, gamma, D)
        gap = gap_closed(a, v, beta, gamma, D)
        worst_rel = max(worst_rel, abs(Qh - Qc) / max(1.0, abs(Qc)))
        worst_gap = max(worst_gap, abs((Qh - L) - gap) / max(1.0, abs(gap)))
        if Qh < L - 1e-8:
            check("heat above learning rate", False, "Q=%s L=%s" % (Qh, L))
            break
    else:
        check(
            "closed-form heat matches the Lyapunov expectation on 40 designs",
            worst_rel < 1e-9,
            "max relative residual %.3e" % worst_rel,
        )
        check(
            "algebraic gap matches heat minus learning rate on 40 designs",
            worst_gap < 1e-8,
            "max relative residual %.3e" % worst_gap,
        )

    # One explicit gap, K=2, readable numbers.
    a = np.array([1.0, 4.0])
    v = np.array([1.0, 0.5])
    beta, gamma, D = 3.0, np.array([2.0, -1.0]), 0.4
    Qh, L, eps, _, _ = moments_and_learning(a, v, beta, gamma, D)
    gap = gap_closed(a, v, beta, gamma, D)
    check(
        "explicit two-mode gap",
        near(Qh - L, gap, 1e-10) and gap > 0.0,
        "Q=%.12f L=%.12f gap=%.12f" % (Qh, L, gap),
    )

    # --- fast weighted spring attains mu at the target sum-error ---
    a = np.array([1.0, 100.0])
    v = np.array([1.0, 1.0])
    eps_target = 0.5
    mu = mu_of_sum_error(a, v, eps_target)
    g = 1.0 / (a + mu)
    sig2 = float(np.sum(a * v * g ** 2) / mu)
    check(
        "implicit mu reproduces the target sum-error",
        near(sum_error_of_mu(a, v, mu), 0.5, 1e-12),
        "mu=%.12f" % mu,
    )
    Qh, L, eps, _, _ = moments_and_learning(a, v, 1e6, 1e6 * g, 1e6 * sig2)
    check(
        "fast weighted spring at lambda 1e6, sum-error 0.5",
        near(Qh, mu, 2e-4) and near(L, mu, 5e-4) and near(eps, 0.5, 2e-4) and Qh > L,
        "Q=%.6f L=%.6f eps=%.6f mu=%.6f" % (Qh, L, eps, mu),
    )
    # Separate water-filling at the same sum-error.
    Lsep, ssep = separate_heat(a, v, 0.5)
    check(
        "separate heat at sum-error 0.5 sits above the joint floor",
        Lsep > mu and near(Lsep, 141.0, 1e-9),
        "Lsep=%.6f ratio=%.6f s=%s" % (Lsep, Lsep / mu, np.array2string(ssep, precision=6)),
    )

    # --- identical modes: the sum is one OU, and separate costs exactly K ---
    for K, eps in ((2, 0.8), (3, 1.1), (4, 0.5)):
        a = np.ones(K)
        v = np.ones(K)
        V = float(K)
        Ljoint = kalman_rate(1.0, V, eps)
        # s_k = eps/K <= 1, so the cap does not bind.
        Lsep = K * (1.0 / (eps / K) - 1.0)
        check(
            "identical K=%d sum-error %.3f, separate heat is K times the joint floor" % (K, eps),
            near(Lsep, K * Ljoint) and near(Ljoint, 1.0 * (V - eps) / eps),
            "joint=%.12f sep=%.12f" % (Ljoint, Lsep),
        )

    # Same rate, unequal variances: the sum is still one OU.
    a = np.array([1.0, 1.0])
    v = np.array([1.0, 4.0])
    eps = 2.0
    Ljoint = kalman_rate(1.0, 5.0, eps)
    Lsep, ssep = separate_heat(a, v, eps)
    check(
        "equal rates, variances 1 and 4, sum-error 2",
        near(Ljoint, 1.5) and near(Lsep, 2.5) and Lsep > Ljoint,
        "joint=%.6f sep=%.6f s=%s" % (Ljoint, Lsep, np.array2string(ssep, precision=6)),
    )

    # Product of shrunk springs attains the per-mode floor. Use the scalar limit formula.
    # beta=lambda, gamma=c*lambda, D=lambda*sig2, c=(v-eps)/v, as in the scalar note.
    def shrunk_heat(a, v, eps, lam):
        c = (v - eps) / v
        rho = lam / (a + lam)
        sig2 = (v - eps) * (rho * (v + eps) / v - 1.0)
        return heat_closed([a], [v], lam, [c * lam], lam * sig2), c, sig2

    h1, _, _ = shrunk_heat(1.0, 1.0, 0.2, 1e6)
    h2, _, _ = shrunk_heat(4.0, 0.5, 0.1, 1e6)
    r1 = kalman_rate(1.0, 1.0, 0.2)
    r2 = kalman_rate(4.0, 0.5, 0.1)
    check(
        "two shrunk springs, per-mode errors 0.2 and 0.1, lambda 1e6",
        near(h1, r1, 1e-4) and near(h2, r2, 1e-4) and h1 > r1 and h2 > r2,
        "heats %.6f + %.6f against floor %.6f" % (h1, h2, r1 + r2),
    )

    # Trace loss: an off-diagonal covariance entry raises the trace.
    # Entry 0.1 is correlation coefficient 0.1/sqrt(0.12). Coefficient 0.1 is a smaller entry.
    Ddiff = np.diag([1.0 * 1.0, 4.0 * 0.5])
    Sdiag = np.diag([0.3, 0.4])
    Sentry = np.array([[0.3, 0.1], [0.1, 0.4]])
    c_rho = 0.1 * math.sqrt(0.3 * 0.4)
    Srho = np.array([[0.3, c_rho], [c_rho, 0.4]])
    td = float(np.trace(Ddiff @ np.linalg.inv(Sdiag)))
    tentry = float(np.trace(Ddiff @ np.linalg.inv(Sentry)))
    trho = float(np.trace(Ddiff @ np.linalg.inv(Srho)))
    rho_of_entry = 0.1 / math.sqrt(0.12)
    check(
        "off-diagonal entry 0.1 and correlation coefficient 0.1 both raise the trace",
        near(td, 8.333333333333, 1e-12)
        and near(tentry, 9.090909090909, 1e-12)
        and near(trho, 8.417508417508, 1e-12)
        and near(rho_of_entry, 0.288675134595, 1e-12)
        and near(c_rho, 0.034641016151, 1e-12)
        and tentry > trho > td,
        "diag=%.12f entry=%.12f rho=%.12f coeff=%.12f" % (td, tentry, trho, rho_of_entry),
    )

    # --- frontiers ---
    # Trace, three different modes. kT=1.
    modes = [(1.0, 1.0), (10.0, 1.0), (100.0, 1.0)]
    for w, expect_n, expect_J in (
        (0.5, 0, 0.5 * 3.0),
        (2.0, 1, None),
        (20.0, 2, None),
        (200.0, 3, None),
    ):
        n = 0
        J = 0.0
        for a_i, v_i in modes:
            _, _, Ji = trace_frontier_mode(a_i, v_i, w)
            J += Ji
            if w >= a_i / v_i:
                n += 1
        ok = n == expect_n and (expect_J is None or near(J, expect_J, 1e-12))
        check(
            "trace frontier w=%g tracks %d modes" % (w, expect_n),
            ok,
            "J=%.12f" % J,
        )

    # Sum frontier, identical K=3, a=v=kT=1.
    # J = 2 sqrt(K w) - 1 above w0=1/3, and 3w below.
    for w in (0.2, 0.5, 2.0, 8.0):
        mu = sum_mu_star(np.ones(3), np.ones(3), w)
        eps = sum_error_of_mu(np.ones(3), np.ones(3), mu)
        J = mu + w * eps
        if w <= 1.0 / 3.0:
            Jstar = 3.0 * w
            mstar = 0.0
        else:
            Jstar = 2.0 * math.sqrt(3.0 * w) - 1.0
            mstar = math.sqrt(3.0 * w) - 1.0
        Jsep = 3.0 * trace_frontier_mode(1.0, 1.0, w)[2]
        check(
            "identical sum frontier w=%g" % w,
            near(J, Jstar, 1e-10) and near(mu, mstar, 1e-9) and J <= Jsep + 1e-12,
            "J=%.12f mu=%.12f eps=%.12f sep=%.12f" % (J, mu, eps, Jsep),
        )

    # Stake interval: joint tracks, separate trace-style memories of the sum are still blind.
    # Identical K=3. Separate threshold is 1. At w=0.5, separate cost is 1.5, joint is lower.
    w = 0.5
    mu = sum_mu_star(np.ones(3), np.ones(3), w)
    Jjoint = mu + w * sum_error_of_mu(np.ones(3), np.ones(3), mu)
    Jsep = 3.0 * w  # each mode blind, because w < a/v = 1
    check(
        "at stake 0.5, K=3 identical, the joint sum tracks and separate memories are blind",
        mu > 0.0 and Jjoint < Jsep and near(Jsep, 1.5),
        "joint=%.12f sep=%.12f" % (Jjoint, Jsep),
    )

    # Geometric half-count. a = 1, 10, 100, 1000. v=1.
    a = np.array([1.0, 10.0, 100.0, 1000.0])
    v = np.ones(4)
    rows = []
    for w in (0.5, 2.0, 8.0, 40.0, 200.0, 2000.0):
        mu = sum_mu_star(a, v, w)
        half = int(np.sum(a <= mu + 1e-9)) if mu > 0.0 else 0
        hard = int(np.sum(w >= a / v))
        rows.append((w, mu, half, hard))
    check(
        "geometric half-count is nondecreasing in the stake and ends at 3 of 4",
        [r[2] for r in rows] == [0, 0, 1, 2, 2, 3] and [r[3] for r in rows] == [0, 1, 1, 2, 3, 4],
        " ".join("w=%g mu=%.4f half=%d hard=%d" % r for r in rows),
    )

    # Infinite geometric ladder: multiplying mu by rho multiplies the required stake by rho.
    rho = 10.0
    a0 = 1.0
    vv = 1.0
    ks = np.arange(-30, 31)
    def stake_at(mu):
        ak = a0 * rho ** ks
        s = np.sum(ak * vv / (ak + mu) ** 2)
        return 1.0 / s
    mu0 = 50.0
    ratio = stake_at(rho * mu0) / stake_at(mu0)
    check(
        "infinite geometric ladder, rho=10, stake scales by rho when mu does",
        near(ratio, rho, 1e-8),
        "w(rho mu)/w(mu)=%.12f" % ratio,
    )

    # --- signal bath is zero, diagonal and coupled ---
    a = np.array([1.7, 0.4, 3.0])
    v = np.array([0.4, 1.1, 0.7])
    # Marginal score contraction: tr(D Sigma^{-1}) - tr(D Sigma^{-1}) = 0,
    # evaluated as E[x^T Sigma^{-1} D Sigma^{-1} x] - tr(D Sigma^{-1}).
    Ddiff = np.diag(a * v)
    Sigma = np.diag(v)
    quad = float(np.trace(Sigma @ Sigma @ np.linalg.inv(Sigma) @ Ddiff @ np.linalg.inv(Sigma)))
    # For a centered Gaussian, E[x^T A x] = tr(A Sigma). A = Sigma^{-1} D Sigma^{-1}.
    Aquad = np.linalg.inv(Sigma) @ Ddiff @ np.linalg.inv(Sigma)
    expect = float(np.trace(Aquad @ Sigma))
    tr = float(np.trace(Ddiff @ np.linalg.inv(Sigma)))
    check(
        "signal-bath cancellation on three independent modes",
        near(expect, tr) and near(expect - tr, 0.0),
        "E[x A x]=%.15f tr=%.15f" % (expect, tr),
    )
    Sigma_c = np.array([[1.0, 0.3], [0.3, 1.0]])
    D_c = np.array([[0.8, 0.1], [0.1, 1.2]])
    A_decay = D_c @ np.linalg.inv(Sigma_c)
    lyap_res = A_decay @ Sigma_c + Sigma_c @ A_decay.T - 2.0 * D_c
    Aquad = np.linalg.inv(Sigma_c) @ D_c @ np.linalg.inv(Sigma_c)
    expect = float(np.trace(Aquad @ Sigma_c))
    tr = float(np.trace(D_c @ np.linalg.inv(Sigma_c)))
    check(
        "coupled equilibrium OU obeys the Lyapunov identity and the signal bath cancels",
        np.max(np.abs(lyap_res)) < 1e-12 and near(expect, tr),
        "lyap max %.3e  E-tr=%.3e" % (np.max(np.abs(lyap_res)), expect - tr),
    )

    # Coupled fast spring: heat approaches tr(D Phi) of the instantaneous channel.
    # dM = -lambda (M - X) dt + sqrt(2 lambda sig2) dB, so Phi -> I/sig2.
    sig2 = 0.25
    lam = 1e5
    # State (X1, X2, M1, M2).
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
    L = float(np.trace(D_c @ (np.linalg.inv(Sc) - np.linalg.inv(Sigma_c))))
    # Heat: f = -lam (M - X), D_m = lam sig2 I, Q = E[f·D_m^{-1} f] + div f.
    # E[(M-X)(M-X)^T] from the blocks.
    EXX = Sxx
    EMM = Smm
    EXM = Sxm
    E_dx = EXX + EMM - EXM - EXM.T
    # f = -lam (M-X), E[f·D_m^{-1} f] = lam / sig2 * E[||M-X||^2]
    Qh = (lam / sig2) * float(np.trace(E_dx)) - 2.0 * lam
    L_static = float(np.trace(D_c) / sig2)
    check(
        "coupled fast spring at lambda 1e5 approaches the static learning rate",
        Qh > L and near(L, L_static, 2e-3) and near(Qh, L_static, 2e-3),
        "Q=%.6f L=%.6f static=%.6f" % (Qh, L, L_static),
    )

    # Path rate of two fast shrunk springs is the sum of the scalar Duncan rates,
    # far above the learning-rate floor.
    def one_shrunk_path(a, v, eps, lam):
        c = (v - eps) / v
        rho = lam / (a + lam)
        sig2 = (v - eps) * (rho * (v + eps) / v - 1.0)
        D = lam * sig2
        P, T, Td = scalar_path_rate(a, v, lam, c * lam, D)
        return T, Td

    T1, Td1 = one_shrunk_path(1.0, 1.0, 0.2, 1e6)
    T2, Td2 = one_shrunk_path(1.0, 1.0, 0.2, 1e6)
    floor = 2.0 * kalman_rate(1.0, 1.0, 0.2)
    check(
        "two fast shrunk springs, path rate far above the learning-rate floor",
        near(T1, Td1, 1e-9) and T1 > 900.0 and near(T1 + T2, 2.0 * T1) and (T1 + T2) > 100.0 * floor,
        "path %.6f + %.6f against floor %.6f" % (T1, T2, floor),
    )

    # Weighted joint spring: path rate above the learning rate. Numerical Riccati.
    a = np.array([1.0, 4.0])
    v = np.array([1.0, 1.0])
    mu = 2.0
    g = 1.0 / (a + mu)
    sig2 = float(np.sum(a * v * g ** 2) / mu)
    lam = 500.0  # finite, so the Riccati is the path of this spring, not only the limit
    _, Tpath = vector_path_rate(a, v, lam * g, lam * sig2)
    Qh, L, eps, _, _ = moments_and_learning(a, v, lam, lam * g, lam * sig2)
    check(
        "weighted spring at lambda 500, path rate above the learning rate",
        Tpath > L > 0.0 and Qh > L,
        "path=%.6f L=%.6f Q=%.6f eps=%.6f" % (Tpath, L, Qh, eps),
    )

    # Blind threshold. The four-mode ladder in the note is 1000/1111, not the three-mode 100/111.
    a4 = np.array([1.0, 10.0, 100.0, 1000.0])
    v4 = np.ones(4)
    w0 = 1.0 / float(np.sum(v4 / a4))
    check(
        "four-mode sum-loss blind threshold is 1000/1111",
        near(w0, 1000.0 / 1111.0, 1e-15)
        and ("%.12f" % w0) == "0.900090009001"
        and sum_mu_star(a4, v4, 0.5 * w0) == 0.0
        and sum_mu_star(a4, v4, 2.0 * w0) > 0.0,
        "w0=%.12f" % w0,
    )

    # One mode reproduces the scalar frontier.
    for w in (0.5, 1.0, 2.0, 8.0):
        mu = sum_mu_star(np.array([1.0]), np.array([1.0]), w)
        J = mu + w * sum_error_of_mu(np.array([1.0]), np.array([1.0]), mu)
        _, _, J1 = trace_frontier_mode(1.0, 1.0, w)
        check("one mode, sum frontier equals the scalar frontier at w=%g" % w, near(J, J1, 1e-10), "J=%.12f" % J)

    print()
    print("PASS %d  FAIL %d" % (PASS, FAIL))
    if FAIL:
        print("GENERAL CHECKS FAIL")
        raise SystemExit(1)
    print("FAILS 0")
    print("ALL GENERAL CHECKS PASS")


if __name__ == "__main__":
    main()
