#!/usr/bin/env python3
"""Checks for theory/INFO_PHYSICS_ATTAINABILITY.md.

The question is the infimum of the memory-bath heat at fixed mean squared
error for an exogenous equilibrium Ornstein–Uhlenbeck signal, over couplings
wider than the centered linear spring.

Run from the repo root:
  nice -n 19 python3 theory/info_physics_checks/attainability_checks.py
"""
from __future__ import annotations

import math
import sys

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


def kalman_rate(a, v, eps):
    """Duncan / Kalman–Bucy information rate at causal error eps. kT = 1."""
    return a * (v - eps) / eps


def linear_memory(a, beta, gamma, D, v):
    """One OU signal and one linear memory.

    dX = -a X dt + sqrt(2 a v) dW
    dM = (-beta M + gamma X) dt + sqrt(2 D) dB
    Sekimoto heat uses kT = 1 and the note's sign: E[f^2]/D + d_M f.
    Learning rate is a(v/s - 1) with s = Var(X|M).
    Path error P solves the scalar Kalman–Bucy Riccati for X given the path of M.
    Transfer-entropy rate T = a(v - P)/P, which equals gamma^2 P / (4 D).
    """
    Cxm = gamma * v / (a + beta)
    Cmm = D / beta + (gamma ** 2) * v / (beta * (a + beta))
    det = v * Cmm - Cxm ** 2
    s = det / Cmm
    err = Cmm + v - 2.0 * Cxm
    L = a * (v / s - 1.0)
    Q = a * v * gamma ** 2 / (D * (a + beta))
    # gamma^2 P^2 = 4 a D (v - P)
    disc = (a * D) ** 2 + a * D * v * gamma ** 2
    P = (2.0 * a * D * (-1.0 + math.sqrt(1.0 + (v * gamma ** 2) / (a * D)))) / gamma ** 2
    T = a * (v - P) / P
    T_duncan = gamma ** 2 * P / (4.0 * D)
    return {
        "Cxm": Cxm,
        "Cmm": Cmm,
        "det": det,
        "s": s,
        "err": err,
        "L": L,
        "Q": Q,
        "P": P,
        "T": T,
        "T_duncan": T_duncan,
        "disc": disc,
    }


def excess_closed(a, beta, gamma, D, v):
    """Factored Sekimoto heat minus learning rate. Nonnegative for D, beta, a > 0."""
    num = (a ** 2) * (gamma ** 2) * v * (D * (a + beta) + gamma ** 2 * v)
    den = D * (a + beta) * (D * (a + beta) ** 2 + a * gamma ** 2 * v)
    return num / den


def shrunk_at_rate(a, v, eps, lam):
    """Linear memory aimed at c X, noise retuned so E[(M-X)^2] = eps exactly.

    Valid for lam > a v / eps. Heat falls to the Kalman rate as lam -> infinity.
    """
    c = (v - eps) / v
    rho = lam / (a + lam)
    sig2 = (v - eps) * (rho * (v + eps) / v - 1.0)
    beta = lam
    gamma = c * lam
    D = lam * sig2
    row = linear_memory(a, beta, gamma, D, v)
    row.update({"c": c, "sig2": sig2, "rho": rho, "lam": lam})
    return row


def trap(y, dx):
    y = np.asarray(y, dtype=float)
    return float(np.sum((y[1:] + y[:-1]) * 0.5 * dx))


def standard_normal_cdf(z):
    z = np.asarray(z, dtype=float)
    return 0.5 * (1.0 + np.vectorize(math.erf)(z / math.sqrt(2.0)))


def phi(z):
    return np.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)


def quantizer_channel(v, sigma, edges, n_grid=4001):
    """K-bin quantization of Y = X + sigma * noise, X ~ N(0, v).

    Returns the fast-equilibrium learning rate (heat floor of that conditional)
    and the MMSE of the bin index.
    """
    xmax = 8.0 * math.sqrt(v)
    x = np.linspace(-xmax, xmax, n_grid)
    dx = float(x[1] - x[0])
    px = np.exp(-0.5 * x * x / v) / math.sqrt(2.0 * math.pi * v)
    K = len(edges) - 1
    # p(bin|x)
    z_hi = (edges[1:, None] - x[None, :]) / sigma
    z_lo = (edges[:-1, None] - x[None, :]) / sigma
    p_bin = standard_normal_cdf(z_hi) - standard_normal_cdf(z_lo)
    p_bin = np.clip(p_bin, 0.0, None)
    mass = np.array([trap(p_bin[k] * px, dx) for k in range(K)])
    L = 0.0
    mmse = 0.0
    used = 0
    for k in range(K):
        if mass[k] < 1e-14:
            continue
        used += 1
        lik = p_bin[k]
        good = lik > 1e-12
        post = np.where(good, lik * px, 0.0)
        z = trap(post, dx)
        if z <= 0.0:
            continue
        post = post / z
        mean = trap(x * post, dx)
        var = trap((x - mean) ** 2 * post, dx)
        mmse += mass[k] * var
        # score of the posterior: -x/v + d/dx ln p(bin|x), only where the bin has mass
        dpx = (phi(z_lo[k]) - phi(z_hi[k])) / sigma
        score = np.zeros_like(x)
        score[good] = -x[good] / v + dpx[good] / lik[good]
        F = trap(score ** 2 * post, dx)
        L += mass[k] * (v * F - 1.0)
    return {"L_over_a": L, "mmse": mmse, "used": used, "mass": mass}


def quartic_conditional(v, width, n_m=801, n_x=1201):
    """Fast equilibrium in V = (m - x)^4 / (4 width^4). Non-Gaussian conditional.

    width sets the scale of m - x. Returns E[F], MMSE, and 1/MMSE.
    """
    xmax = 6.0 * math.sqrt(v)
    mmax = xmax + 4.0 * width
    x = np.linspace(-xmax, xmax, n_x)
    m = np.linspace(-mmax, mmax, n_m)
    dx = float(x[1] - x[0])
    dm = float(m[1] - m[0])
    px = np.exp(-0.5 * x * x / v) / math.sqrt(2.0 * math.pi * v)
    # log p(m|x) = -(m-x)^4 / (4 width^4) - log Z(x)
    mm, xx = np.meshgrid(m, x, indexing="ij")
    log_lik = -((mm - xx) ** 4) / (4.0 * width ** 4)
    log_lik -= log_lik.max(axis=0, keepdims=True)
    lik = np.exp(log_lik)
    Z = np.sum(lik, axis=0) * dm
    pm_x = lik / Z
    # joint proportional to pm_x * px; posterior p(x|m)
    joint = pm_x * px[None, :]
    marg_m = np.sum(joint, axis=1) * dx
    L_acc = 0.0
    mmse = 0.0
    weight = 0.0
    # score on the x grid for each m, by log-posterior differences where mass is real
    for i in range(n_m):
        if marg_m[i] < 1e-12 * marg_m.max():
            continue
        post = joint[i] / (marg_m[i])
        # renormalize numerically
        z = trap(post, dx)
        post = post / z
        mean = trap(x * post, dx)
        var = max(trap((x - mean) ** 2 * post, dx), 1e-18)
        mmse += marg_m[i] * var
        weight += marg_m[i]
        logp = np.log(np.clip(post, 1e-300, None))
        score = np.gradient(logp, dx)
        F = trap(score ** 2 * post, dx)
        L_acc += marg_m[i] * F
    mmse /= weight
    Fbar = L_acc / weight
    return {"F": Fbar, "mmse": mmse, "inv": 1.0 / mmse}


def lyapunov(A, Q):
    n = A.shape[0]
    M = np.kron(np.eye(n), A) + np.kron(A, np.eye(n))
    c = np.linalg.solve(M, -Q.reshape(-1))
    C = c.reshape(n, n)
    return 0.5 * (C + C.T)


def two_memory_heat(a, v, beta1, beta2, gamma1, gamma2, k12, k21, D1, D2):
    """Two linear memories on one OU signal. Sum of Sekimoto heats versus learning rate."""
    A = np.array(
        [
            [-a, 0.0, 0.0],
            [gamma1, -beta1, k12],
            [gamma2, k21, -beta2],
        ],
        dtype=float,
    )
    if np.any(np.real(np.linalg.eigvals(A)) >= -1e-8):
        return None
    BB = np.diag([2.0 * a * v, 2.0 * D1, 2.0 * D2])
    C = lyapunov(A, BB)
    if np.any(np.linalg.eigvalsh(C) <= 0.0):
        return None
    # Var(X | M1, M2) via the Schur complement
    Cmm = C[1:, 1:]
    Cmx = C[1:, 0]
    s = float(C[0, 0] - Cmx @ np.linalg.solve(Cmm, Cmx))
    if s <= 0.0 or s >= v:
        return None
    L = a * (v / s - 1.0)

    def heat(i, coef):
        # f = coef · z, self derivative coef[i]
        Ef2 = float(coef @ C @ coef)
        return Ef2 / (D1 if i == 1 else D2) + coef[i]

    # state order (X, M1, M2)
    f1 = np.array([gamma1, -beta1, k12])
    f2 = np.array([gamma2, k21, -beta2])
    Q = heat(1, f1) + heat(2, f2)
    return {"s": s, "L": L, "Q": Q, "R": kalman_rate(a, v, s)}


def test_identity_and_signal_bath():
    rng = np.random.default_rng(11)
    worst = 0.0
    for _ in range(40):
        a = float(rng.uniform(0.2, 3.0))
        beta = float(rng.uniform(0.2, 8.0))
        gamma = float(rng.uniform(0.1, 6.0))
        D = float(rng.uniform(0.05, 2.0))
        v = float(rng.uniform(0.3, 2.5))
        row = linear_memory(a, beta, gamma, D, v)
        gap = row["Q"] - row["L"]
        closed = excess_closed(a, beta, gamma, D, v)
        worst = max(worst, abs(gap - closed) / max(1.0, abs(closed)))
        if gap < -1e-9 or row["T"] + 1e-9 < row["L"]:
            check("heat is at least the learning rate on a random linear memory", False,
                  "Q-L=%.3e T-L=%.3e" % (gap, row["T"] - row["L"]))
            return
        if abs(row["T"] - row["T_duncan"]) > 1e-9 * max(1.0, row["T"]):
            check("path information rate matches the two Duncan normalizations", False,
                  "T=%.6e duncan=%.6e" % (row["T"], row["T_duncan"]))
            return
    check("Sekimoto heat minus learning rate matches the factored square on 40 designs",
          worst < 1e-9, "rel=%.3e" % worst)
    check("on those designs the path transfer entropy is at least the learning rate", True)
    # signal bath: equilibrium OU force F = -X/v, diffusion a*v, Stratonovich power
    # D_x * E[X^2] / v^2 + D_x * (-1/v), with E[X^2] = v
    a_s, v_s = 1.7, 0.4
    diffusion = a_s * v_s
    power = diffusion * v_s / (v_s ** 2) + diffusion * (-1.0 / v_s)
    check("the equilibrium signal bath has medium heat 0",
          near(power, 0.0, 1e-15),
          "a=1.7 v=0.4 power=%.3e" % power)


def test_shrunk_attains():
    a, v, eps = 1.0, 1.0, 0.2
    R = kalman_rate(a, v, eps)
    ratios = []
    for lam in (6.0, 20.0, 100.0, 1.0e3, 1.0e4, 1.0e6):
        row = shrunk_at_rate(a, v, eps, lam)
        ratios.append(row["Q"] / R)
        ok_err = near(row["err"], eps, 1e-9)
        ok_above = row["Q"] > R - 1e-9 and row["Q"] + 1e-12 >= row["L"]
        if not (ok_err and ok_above):
            check("shrunk spring holds the error and stays above the Kalman rate", False,
                  "lam=%.1f err=%.6e Q=%.6e L=%.6e" % (lam, row["err"], row["Q"], row["L"]))
            return
    early = shrunk_at_rate(a, v, eps, 6.0)
    check("at lambda=6 the shrunk coordinate is not yet the conditional mean",
          near(early["Q"], 24.0, 1e-9)
          and near(early["Cxm"] / early["Cmm"], 1.2, 1e-12)
          and abs(early["s"] - 0.177142857143) < 1e-12,
          "Q=%.6f s=%.12f gain=%.6f" % (early["Q"], early["s"], early["Cxm"] / early["Cmm"]))
    check("shrunk spring at eps=0.2 holds E[(M-X)^2] and Q >= Kalman rate",
          True, "ratios " + " ".join("%.6f" % r for r in ratios))
    check("at lambda=1e6 the heat is within 2e-5 of the Kalman rate 4",
          abs(ratios[-1] - 1.0) < 2e-5 and near(R, 4.0),
          "Q/R=%.12f" % ratios[-1])
    # conditional error meets the raw error in that limit
    row = shrunk_at_rate(a, v, eps, 1.0e6)
    check("the attaining design is calibrated: conditional variance meets the raw error",
          abs(row["s"] - eps) < 1e-5, "s=%.12f" % row["s"])
    # centered spring, same raw error: heat -> a v/eps, gap -> a, and heat -> R(s)
    lam = 1.0e6
    # D = lam * eps_thermal with eps_raw -> eps, so thermal variance eps - a v/(a+lam)
    D = lam * (eps - a * v / (a + lam))
    cen = linear_memory(a, lam, lam, D, v)
    check("centered spring heat approaches a v/eps = 5 at raw error 0.2",
          near(cen["err"], eps, 1e-8) and abs(cen["Q"] - a * v / eps) < 1e-4,
          "err=%.8f Q=%.8f" % (cen["err"], cen["Q"]))
    check("that heat meets the Kalman rate of the conditional error, and exceeds the raw-error rate by a",
          abs(cen["Q"] - kalman_rate(a, v, cen["s"])) < 1e-4
          and abs((cen["Q"] - kalman_rate(a, v, eps)) - a) < 1e-3,
          "s=%.8f Q-R(raw)=%.8f" % (cen["s"], cen["Q"] - R))
    # Same centered family, raw coordinate error held at 0.25 so the conditional mean has decision error 0.2.
    raw = v * eps / (v - eps)
    D_dec = lam * (raw - a * v / (a + lam))
    dec = linear_memory(a, lam, lam, D_dec, v)
    gain = dec["Cxm"] / dec["Cmm"]
    check("centered spring at raw error 0.25 has decision error 0.2 and heat 4.000012",
          near(dec["err"], 0.25, 1e-9)
          and abs(dec["s"] - 0.20000032) < 5e-8
          and abs(dec["Q"] - 4.00001200) < 5e-8
          and abs(gain - 0.80000048) < 5e-8,
          "raw=%.8f s=%.8f Q=%.8f gain=%.8f" % (dec["err"], dec["s"], dec["Q"], gain))
    caps = []
    for lam_c in (6.0, 20.0, 100.0, 1.0e3, 1.0e4, 1.0e6):
        row_c = shrunk_at_rate(a, v, eps, lam_c)
        caps.append(row_c["L"] / row_c["T"])
    fast = shrunk_at_rate(a, v, eps, 1.0e6)
    check("the floor limit sends sensory capacity to 0",
          abs(fast["T"] - 999.503125) < 1e-3
          and abs(fast["L"] / fast["T"] - 0.004002) < 1e-5
          and abs(caps[0] - 0.774) < 0.002
          and abs(caps[1] - 0.841) < 0.002
          and abs(caps[-1] - 0.004) < 0.0005,
          "T=%.6f C=%s" % (fast["T"], " ".join("%.4f" % c for c in caps)))


def test_capacity_one():
    """Hartich, Barato, Seifert bare-sensor point: B = nu^2/(nu^2-1), efficiency 1/2."""
    a, v = 1.0, 1.0
    for nu in (2.0, 4.0, 10.0):
        B = nu ** 2 / (nu ** 2 - 1.0)
        D = B * a * v
        lam = nu * a
        row = linear_memory(a, lam, lam, D, v)
        # their closed forms
        L_paper = a * (nu ** 3) / (nu ** 2 + B * (1.0 + nu) ** 2)
        Q_paper = a * (nu ** 2) / (B * (1.0 + nu))
        T_paper = (a / 2.0) * (math.sqrt(1.0 + nu ** 2 / B) - 1.0)
        ok = (
            near(row["L"], L_paper, 1e-9)
            and near(row["Q"], Q_paper, 1e-9)
            and near(row["T"], T_paper, 1e-9)
            and near(row["Q"], 2.0 * row["L"], 1e-9)
            and abs(row["P"] - row["s"]) / row["s"] < 1e-9
        )
        if not ok:
            check("capacity-1 spring matches Hartich and pays twice the learning rate", False,
                  "nu=%.1f L=%.6e paper=%.6e Q/L=%.6f P-s=%.3e" % (
                      nu, row["L"], L_paper, row["Q"] / row["L"], row["P"] - row["s"]))
            return
    check("at sensory capacity 1 the centered spring pays twice the Kalman rate of its error", True)
    for nu, B in ((10.0, 0.3), (3.0, 1.5), (20.0, 2.0), (1.5, 0.4)):
        row = linear_memory(a, nu * a, nu * a, B * a * v, v)
        L_paper = a * (nu ** 3) / (nu ** 2 + B * (1.0 + nu) ** 2)
        Q_paper = a * (nu ** 2) / (B * (1.0 + nu))
        T_paper = (a / 2.0) * (math.sqrt(1.0 + nu ** 2 / B) - 1.0)
        if not (near(row["L"], L_paper, 1e-9) and near(row["Q"], Q_paper, 1e-9) and near(row["T"], T_paper, 1e-9)):
            check("centered spring matches the Hartich bare-sensor formulas off the capacity-1 locus", False,
                  "nu=%.1f B=%.2f" % (nu, B))
            return
    check("centered spring matches the Hartich bare-sensor formulas off the capacity-1 locus", True)
    # same conditional error, shrunk spring is cheaper
    # pick nu=9: s = 2v/(nu+1) = 0.2, heat = a(nu-1) = 8, shrunk floor = 4
    nu = 9.0
    B = nu ** 2 / (nu ** 2 - 1.0)
    row = linear_memory(a, nu * a, nu * a, B * a * v, v)
    R = kalman_rate(a, v, row["s"])
    check("capacity 1 at conditional error 0.2 costs 8, twice the attainable floor 4",
          near(row["s"], 0.2, 1e-9) and near(row["Q"], 8.0, 1e-9) and near(R, 4.0),
          "s=%.6f Q=%.6f" % (row["s"], row["Q"]))


def test_quantizer():
    v = 1.0
    sigma = 0.5  # unquantized MMSE = v sigma^2 / (sigma^2 + v) = 0.2
    s_parent = v * sigma ** 2 / (sigma ** 2 + v)
    check("parent Gaussian channel has MMSE 0.2", near(s_parent, 0.2, 1e-12))
    print("  K-bin quantization of that channel (learning rate a(v E[F]-1); bath heat not computed):")
    print("  %4s %12s %12s %12s %12s" % ("K", "MMSE", "L", "R(MMSE)", "L/R"))
    ratios = []
    for K in (2, 4, 8, 16, 32, 64):
        # equal-probability bins of the marginal of Y under the Gaussian approximation
        # Var(Y) = v + sigma^2
        vy = v + sigma ** 2
        # quantile edges of N(0, vy)
        ps = np.linspace(0.0, 1.0, K + 1)
        # inverse CDF via a rational approximation on a grid of the cdf, endpoints +/- infinity clipped
        grid = np.linspace(-12.0, 12.0, 200001)
        cdf = standard_normal_cdf(grid)
        edges = []
        for p in ps:
            if p <= 0.0:
                edges.append(-1e3)
            elif p >= 1.0:
                edges.append(1e3)
            else:
                edges.append(float(grid[np.searchsorted(cdf, p)]) * math.sqrt(vy))
        edges = np.array(edges)
        out = quantizer_channel(v, sigma, edges)
        L = out["L_over_a"]  # a = 1
        R = kalman_rate(1.0, v, out["mmse"])
        ratio = L / R
        ratios.append(ratio)
        print("  %4d %12.6f %12.6f %12.6f %12.6f" % (K, out["mmse"], L, R, ratio))
        if L + 1e-6 < R:
            check("quantizer learning rate stays above the Kalman rate", False, "K=%d" % K)
            return
    check("64-bin quantization sits within 2% of the Kalman rate",
          ratios[-1] < 1.02, "L/R=%.6f" % ratios[-1])
    check("the ratio falls as K grows from 2 to 64",
          ratios[-1] < ratios[0] and ratios[-1] < ratios[2],
          "K2=%.4f K64=%.4f" % (ratios[0], ratios[-1]))
    # Retune the parent noise so the bin index has MMSE 0.2, where that is reachable.
    print("  same bins, parent noise retuned to MMSE 0.2:")
    print("  %4s %12s %12s %12s" % ("K", "sigma", "L", "L/R"))
    tuned = []
    for K in (8, 16, 32, 64):
        lo, hi = 0.05, 1.2
        best = None
        for _ in range(28):
            mid = 0.5 * (lo + hi)
            vy = v + mid ** 2
            ps = np.linspace(0.0, 1.0, K + 1)
            grid = np.linspace(-12.0, 12.0, 100001)
            cdf = standard_normal_cdf(grid)
            edges = []
            for p in ps:
                if p <= 0.0:
                    edges.append(-1e3)
                elif p >= 1.0:
                    edges.append(1e3)
                else:
                    edges.append(float(grid[np.searchsorted(cdf, p)]) * math.sqrt(vy))
            out = quantizer_channel(v, mid, np.array(edges), n_grid=2501)
            if out["mmse"] > 0.2:
                hi = mid
            else:
                lo = mid
            best = (mid, out)
        sigma_hat, out = best
        L = out["L_over_a"]
        R = kalman_rate(1.0, v, out["mmse"])
        tuned.append((K, sigma_hat, out["mmse"], L, L / R))
        print("  %4d %12.6f %12.6f %12.6f" % (K, sigma_hat, L, L / R))
        if L + 1e-4 < R:
            check("retuned quantizer stays above the Kalman rate", False, "K=%d" % K)
            return
    check("at MMSE 0.2 the 64-bin learning rate is within 1% of the Kalman rate 4",
          abs(tuned[-1][3] - 4.0) < 0.04 and abs(tuned[-1][2] - 0.2) < 2e-3,
          "L=%.6f mmse=%.6f" % (tuned[-1][3], tuned[-1][2]))


def test_quartic():
    v = 1.0
    out = quartic_conditional(v, width=0.45)
    excess = out["F"] - out["inv"]
    print("  quartic fast equilibrium: MMSE=%.6f Fisher=%.6f 1/MMSE=%.6f excess=%.6f" % (
        out["mmse"], out["F"], out["inv"], excess))
    check("a quartic conditional has Fisher above 1/variance",
          excess > 0.01 and out["mmse"] < v,
          "excess=%.4f mmse=%.4f" % (excess, out["mmse"]))


def test_two_memories():
    rng = np.random.default_rng(19)
    a, v = 1.0, 1.0
    n_ok = 0
    worst_ratio = 1e9
    for _ in range(30):
        beta1 = float(rng.uniform(0.5, 6.0))
        beta2 = float(rng.uniform(0.5, 6.0))
        gamma1 = float(rng.uniform(0.2, 5.0))
        gamma2 = float(rng.uniform(0.2, 5.0))
        k12 = float(rng.uniform(-1.0, 1.0))
        k21 = float(rng.uniform(-1.0, 1.0))
        D1 = float(rng.uniform(0.05, 1.5))
        D2 = float(rng.uniform(0.05, 1.5))
        row = two_memory_heat(a, v, beta1, beta2, gamma1, gamma2, k12, k21, D1, D2)
        if row is None:
            continue
        n_ok += 1
        if row["Q"] + 1e-7 < row["L"]:
            check("two memories dissipate at least the learning rate", False,
                  "Q=%.6e L=%.6e" % (row["Q"], row["L"]))
            return
        worst_ratio = min(worst_ratio, row["Q"] / row["R"])
    check("30 stable two-memory designs stay above the learning-rate floor",
          n_ok >= 20 and worst_ratio >= 1.0 - 1e-6,
          "stable=%d closest Q/R=%.6f" % (n_ok, worst_ratio))
    # Embed the shrunk spring as the first memory and leave the second at equilibrium.
    lam = 1.0e4
    eps = 0.2
    one = shrunk_at_rate(a, v, eps, lam)
    emb = two_memory_heat(
        a, v, lam, 1.7, one["c"] * lam, 0.0, 0.0, 0.0, lam * one["sig2"], 0.4
    )
    check("an equilibrium second memory adds no heat to the shrunk spring",
          emb is not None and near(emb["Q"], one["Q"], 1e-8) and near(emb["s"], one["s"], 1e-8),
          "Q=%.8f one=%.8f" % (emb["Q"], one["Q"]))


def test_frontier():
    a = v = 1.0
    # blind threshold kT a / v = 1; centered-spring threshold 4
    rows = []
    for w in (2.0, 8.0, 20.0, 50.0):
        eps = math.sqrt(a * v / w)
        heat = a * (v / eps - 1.0)
        cost = heat + w * eps
        centered_heat = a * v / eps
        rows.append((w, eps, heat, cost, centered_heat))
    # stake 2 tracks; centered heat objective is blind because 2*sqrt(w)=2.828 > 2
    w, eps, heat, cost, ch = rows[0]
    check("at stake 2 the attainable frontier tracks at error 1/sqrt(2), cost 2 sqrt(2)-1",
          near(eps, 1.0 / math.sqrt(2.0), 1e-12)
          and near(cost, 2.0 * math.sqrt(2.0) - 1.0, 1e-12)
          and cost < w * v,
          "eps=%.12f heat=%.12f cost=%.12f" % (eps, heat, cost))
    expect_eps = {
        8.0: 1.0 / math.sqrt(8.0),
        20.0: 1.0 / math.sqrt(20.0),
        50.0: 1.0 / math.sqrt(50.0),
    }
    for w, eps, heat, cost, ch in rows[1:]:
        check("stake %g error matches 1/sqrt(w) and heat is one below the centered floor" % w,
              near(eps, expect_eps[w], 1e-12) and near(ch - heat, 1.0, 1e-12),
              "eps=%.12f heat=%.12f centered=%.12f" % (eps, heat, ch))
    # derivative test: interior minimum of R(eps)+w eps
    def f(eps, w):
        return a * (v - eps) / eps + w * eps
    for w, eps, heat, cost, ch in rows:
        step = 1e-4
        check("stake %g critical point is a local minimum" % w,
              f(eps, w) <= f(eps * (1.0 - step), w) and f(eps, w) <= f(min(v * 0.999, eps * (1.0 + step)), w))
    print("  frontier (a=v=kT=1):")
    print("  %6s %14s %14s %14s %14s" % ("w", "eps", "heat", "cost", "centered heat"))
    for w, eps, heat, cost, ch in rows:
        print("  %6g %14.12f %14.12f %14.12f %14.12f" % (w, eps, heat, cost, ch))


def test_reference_spring_numbers():
    """The centered reference point of INFO_PHYSICS stays where that note put it."""
    row = linear_memory(1.0, 2.0, 2.0, 0.3, 1.0)
    check("reference spring error is 0.483333333333",
          near(row["err"], 0.483333333333, 1e-12), "err=%.12f" % row["err"])
    Q_note = (2.0 ** 2 / 0.3) * row["err"] - 2.0
    check("reference Sekimoto heat is 4.444444444444",
          near(Q_note, 4.444444444444, 1e-12) and near(row["Q"], Q_note, 1e-12),
          "Q=%.12f" % row["Q"])


def main():
    test_identity_and_signal_bath()
    test_reference_spring_numbers()
    test_shrunk_attains()
    test_capacity_one()
    test_quantizer()
    test_quartic()
    test_two_memories()
    test_frontier()
    print("PASS %d  FAIL %d" % (PASS, FAIL))
    if FAIL:
        print("ATTAINABILITY CHECKS FAILED")
        return 1
    print("ALL ATTAINABILITY CHECKS PASS")
    print("FAILS 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
