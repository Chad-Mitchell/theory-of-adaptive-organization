#!/usr/bin/env python3
"""Independent recomputation for the review of draft PR #178.

Written from the Langevin equations and the definitions of the learning rate,
Sekimoto heat, and Duncan's path mutual-information rate. Imports nothing from
theory/info_physics_checks or from the draft.
"""
from __future__ import annotations

import json
import math
import time
import urllib.request

import numpy as np
import sympy as sp

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
    scale = max(1.0, abs(float(a)), abs(float(b)))
    return abs(float(a) - float(b)) <= tol * scale


def moments(a, beta, gamma, D, v):
    """Stationary covariances of the exogenous OU signal and one linear memory.

    dX = -a X dt + sqrt(2 a v) dW
    dM = (-beta M + gamma X) dt + sqrt(2 D) dB
    The Lyapunov equation A C + C A^T + diag(2 a v, 2 D) = 0 gives the moments.
    """
    cxm = gamma * v / (a + beta)
    cmm = D / beta + (gamma ** 2) * v / (beta * (a + beta))
    det = v * cmm - cxm ** 2
    s = det / cmm
    raw = cmm + v - 2.0 * cxm
    # Sekimoto, kT = 1, sign used by the draft: E[f^2]/D + d_M f, f = -beta M + gamma X.
    # Algebra: this equals a v gamma^2 / (D (a+beta)).
    heat = a * v * gamma ** 2 / (D * (a + beta))
    # Gaussian learning rate a(v/s - 1) = a cxm^2 / det.
    learn = a * cxm ** 2 / det
    # Path error of X given the path of M. Observation dY = gamma X dt + sqrt(2 D) dB
    # after removing the known -beta M dt. Duncan rate (1/2) E[(H/sqrt(R)) (X-hat)^2]
    # with H=gamma and R=2D is gamma^2 P / (4 D). The OU Riccati is gamma^2 P^2 = 4 a D (v-P).
    disc = 1.0 + (v * gamma ** 2) / (a * D)
    P = (2.0 * a * D * (-1.0 + math.sqrt(disc))) / gamma ** 2
    transfer = a * (v - P) / P
    duncan = gamma ** 2 * P / (4.0 * D)
    gain = cxm / cmm  # E[X|M] = gain * M
    return {
        "cxm": cxm,
        "cmm": cmm,
        "det": det,
        "s": s,
        "raw": raw,
        "heat": heat,
        "learn": learn,
        "P": P,
        "transfer": transfer,
        "duncan": duncan,
        "gain": gain,
    }


def symbolic_identities():
    a, beta, gamma, D, v = sp.symbols("a beta gamma D v", positive=True)
    cxm = gamma * v / (a + beta)
    cmm = D / beta + (gamma ** 2) * v / (beta * (a + beta))
    det = sp.simplify(v * cmm - cxm ** 2)
    heat = sp.simplify(a * v * gamma ** 2 / (D * (a + beta)))
    learn = sp.simplify(a * cxm ** 2 / det)
    num = (a ** 2) * (gamma ** 2) * v * (D * (a + beta) + gamma ** 2 * v)
    den = D * (a + beta) * (D * (a + beta) ** 2 + a * gamma ** 2 * v)
    gap = sp.simplify(heat - learn - num / den)
    check("symbolic heat minus learning rate equals the factored expression", gap == 0, str(gap))

    # Sekimoto from the quadratic expectation, not from the closed heat.
    # E[f^2] = beta^2 cmm - 2 beta gamma cxm + gamma^2 v, f_M derivative = -beta.
    ef2 = sp.expand(beta ** 2 * cmm - 2 * beta * gamma * cxm + gamma ** 2 * v)
    sek = sp.simplify(ef2 / D - beta)
    check("Sekimoto expectation E[f^2]/D - beta equals a v gamma^2 / (D(a+beta))",
          sp.simplify(sek - heat) == 0)

    eps, lam = sp.symbols("eps lam", positive=True)
    c = (v - eps) / v
    rho = lam / (a + lam)
    sig2 = (v - eps) * (rho * (v + eps) / v - 1)
    b = lam
    g = c * lam
    Dd = lam * sig2
    cx = g * v / (a + b)
    cm = Dd / b + (g ** 2) * v / (b * (a + b))
    raw = sp.simplify(cm + v - 2 * cx)
    heat_s = sp.simplify(a * v * g ** 2 / (Dd * (a + b)))
    target = sp.simplify(a * (v - eps) * rho / (rho * (v + eps) - v))
    check("shrunk spring raw error is exactly eps", sp.simplify(raw - eps) == 0)
    check("shrunk spring heat is a(v-eps) rho / (rho(v+eps)-v)",
          sp.simplify(heat_s - target) == 0)
    ratio = sp.simplify(heat_s / (a * (v - eps) / eps))
    ratio_target = sp.simplify(rho * eps / (rho * (v + eps) - v))
    check("heat over the Kalman rate is rho eps / (rho(v+eps)-v)",
          sp.simplify(ratio - ratio_target) == 0)

    # Signal bath. Force F=-X/v, diffusion coefficient a v, Stratonovich power
    # D E[F^2] + D dF/dX. For the equilibrium Gaussian this is a - a.
    Fx, dFx = -1 / v, -1 / v  # F = Fx * X, constant slope
    # E[F^2] = Fx^2 * v, so D E[F^2] = (a v) * (1/v^2) * v = a
    power = sp.simplify((a * v) * (Fx ** 2) * v + (a * v) * dFx)
    check("equilibrium signal bath Stratonovich power is identically 0", power == 0)


def gaussian_flow_sign():
    """Both information-flow contractions on one Gaussian joint, from the moments."""
    rng = np.random.default_rng(3)
    worst = 0.0
    for _ in range(20):
        a = float(rng.uniform(0.3, 2.5))
        beta = float(rng.uniform(0.3, 5.0))
        gamma = float(rng.uniform(0.2, 4.0))
        D = float(rng.uniform(0.05, 1.5))
        v = float(rng.uniform(0.4, 2.0))
        row = moments(a, beta, gamma, D, v)
        c, mm = row["cxm"], row["cmm"]
        sigma = np.array([[v, c], [c, mm]])
        H = np.linalg.inv(sigma)
        h = H[0].copy()
        k = H[1].copy()
        # j_X / p = -a X - a v d_X ln p, and d_X ln p = -h·z
        b = a * v * h
        b[0] -= a
        # Horowitz-Esposito factor d_X ln(p/(p_X p_M)) = d_X ln p(x|m) + X/v
        s_he = -h.copy()
        s_he[0] += 1.0 / v
        i_x = float(b @ sigma @ s_he)
        # Hartich learning rate from the signal current: -E[(j_X/p) d_X ln p(x|m)]
        # d_X ln p(x|m) = -h·z
        l_hartich = float(b @ sigma @ h)
        # extra term that separates the two contractions
        extra = float(b @ sigma @ np.array([1.0 / v, 0.0]))
        # memory current: drift g·z, g=(gamma, -beta); diffusion correction D * score
        gvec = np.array([gamma, -beta])
        b_m = gvec + D * k
        # d_M ln p(x|m) = d_M ln p(m|x) - d_M ln p_M = -k·z + M/cmm
        s_m = -k.copy()
        s_m[1] += 1.0 / mm
        l_from_memory = float(b_m @ sigma @ s_m)
        worst = max(
            worst,
            abs(l_hartich - row["learn"]),
            abs((-i_x) - row["learn"]),
            abs(extra),
            abs(l_from_memory - row["learn"]),
            abs(row["transfer"] - row["duncan"]),
        )
    check("learning rate equals -I_X, Hartich's signal contraction, and the memory contraction",
          worst < 1e-9, "worst abs %.3e" % worst)


def reference_and_shrunk():
    row = moments(1.0, 2.0, 2.0, 0.3, 1.0)
    check("reference raw error 29/60", near(row["raw"], 29.0 / 60.0, 1e-12),
          "raw=%.12f" % row["raw"])
    check("reference Sekimoto heat 40/9", near(row["heat"], 40.0 / 9.0, 1e-12),
          "heat=%.12f learn=%.12f" % (row["heat"], row["learn"]))

    a = v = 1.0
    eps = 0.2
    R = a * (v - eps) / eps
    print("  shrunk spring, raw error held at 0.2, R=4")
    print("  %10s %16s %16s %16s %16s %12s" % ("lambda", "heat", "learn", "s", "gain", "C=L/T"))
    for lam in (6.0, 20.0, 100.0, 1e3, 1e4, 1e6):
        c = (v - eps) / v
        rho = lam / (a + lam)
        sig2 = (eps) * 0 + (v - eps) * (rho * (v + eps) / v - 1.0)
        row = moments(a, lam, c * lam, lam * sig2, v)
        cap = row["learn"] / row["transfer"]
        print("  %10.3g %16.12f %16.12f %16.12f %16.12f %12.6f" % (
            lam, row["heat"], row["learn"], row["s"], row["gain"], cap))
        if abs(row["raw"] - eps) > 1e-9 or row["heat"] + 1e-9 < row["learn"]:
            check("shrunk row stays at raw error eps and above its learning rate", False, str(lam))
            return
    heat_exact = 800000 / 199999
    rho = 1e6 / (1.0 + 1e6)
    sig2 = (v - eps) * (rho * (v + eps) / v - 1.0)
    row = moments(a, 1e6, 0.8e6, 1e6 * sig2, v)
    check("at lambda=1e6 the heat is 800000/199999 = 4.000020000100",
          near(row["heat"], heat_exact, 1e-12) and near(heat_exact, 4.000020000100, 1e-12),
          "heat=%.15f exact=%.15f" % (row["heat"], heat_exact))
    check("conditional variance at lambda=1e6 is within 1e-11 of 0.2",
          abs(row["s"] - 0.2) < 1e-11, "s=%.15f gain=%.15f" % (row["s"], row["gain"]))
    check("at lambda=1e6 sensory capacity stays strictly below 1",
          row["learn"] / row["transfer"] < 0.999,
          "C=%.6f T=%.6f L=%.6f" % (row["learn"] / row["transfer"], row["transfer"], row["learn"]))

    # Centered spring, same raw error 0.2, fast.
    lam = 1e6
    D = lam * (eps - a * v / (a + lam))
    cen = moments(a, lam, lam, D, v)
    check("centered fast raw error 0.2 has heat near 5 and conditional error near 1/6",
          abs(cen["raw"] - 0.2) < 1e-9 and abs(cen["heat"] - 5.0) < 1e-4
          and abs(cen["s"] - (v * eps) / (v + eps)) < 1e-5,
          "raw=%.8f heat=%.8f s=%.8f learn=%.8f" % (cen["raw"], cen["heat"], cen["s"], cen["learn"]))

    # Same decision error 0.2 by a free linear readout of a centered spring.
    # Fast conditional error s = v e /(v+e) = 0.2 implies raw e = 0.25, heat -> 4.
    e_raw = v * eps / (v - eps)
    D2 = lam * (e_raw - a * v / (a + lam))
    cen2 = moments(a, lam, lam, D2, v)
    check("centered spring plus the conditional-mean readout meets decision error 0.2 at heat near 4",
          abs(e_raw - 0.25) < 1e-15 and abs(cen2["s"] - eps) < 1e-5 and abs(cen2["heat"] - 4.0) < 1e-4,
          "raw=%.8f s=%.8f heat=%.8f gain=%.8f" % (cen2["raw"], cen2["s"], cen2["heat"], cen2["gain"]))


def capacity_and_hartich():
    a = v = 1.0
    for nu in (2.0, 4.0, 9.0, 10.0):
        B = nu ** 2 / (nu ** 2 - 1.0)
        row = moments(a, nu * a, nu * a, B * a * v, v)
        L = a * (nu ** 3) / (nu ** 2 + B * (1.0 + nu) ** 2)
        Q = a * (nu ** 2) / (B * (1.0 + nu))
        T = (a / 2.0) * (math.sqrt(1.0 + nu ** 2 / B) - 1.0)
        ok = (near(row["learn"], L, 1e-12) and near(row["heat"], Q, 1e-12)
              and near(row["transfer"], T, 1e-12) and near(row["heat"], 2.0 * row["learn"], 1e-12)
              and abs(row["P"] - row["s"]) / row["s"] < 1e-12)
        if not ok:
            check("capacity-1 centered spring matches Hartich (52)-(54) and pays twice", False,
                  "nu=%g" % nu)
            return
    check("capacity-1 centered spring matches Hartich (52)-(54) and heat is twice the learning rate", True)
    row = moments(a, 9.0, 9.0, (81.0 / 80.0), v)
    check("nu=9 capacity-1 conditional error is 0.2 and heat is 8",
          near(row["s"], 0.2, 1e-12) and near(row["heat"], 8.0, 1e-12),
          "s=%.6f heat=%.6f" % (row["s"], row["heat"]))
    # Off the locus, efficiency of the centered family stays below 1.
    # As B -> infinity at fixed nu, eta -> nu/(1+nu).
    for nu, B in ((10.0, 0.3), (3.0, 1.5), (20.0, 2.0), (1.5, 0.4), (10.0, 1e6)):
        row = moments(a, nu, nu, B * a * v, v)
        L = a * (nu ** 3) / (nu ** 2 + B * (1.0 + nu) ** 2)
        Q = a * (nu ** 2) / (B * (1.0 + nu))
        T = (a / 2.0) * (math.sqrt(1.0 + (nu ** 2) / B) - 1.0)
        if not (near(row["learn"], L, 1e-9) and near(row["heat"], Q, 1e-9) and near(row["transfer"], T, 1e-9)):
            check("centered spring matches Hartich off the capacity-1 noise", False, "nu=%g B=%g" % (nu, B))
            return
        eta = row["learn"] / row["heat"]
        if eta > nu / (1.0 + nu) + 1e-9:
            check("centered-family efficiency stays at or below nu/(1+nu)", False, "eta=%.6f" % eta)
            return
    check("centered spring matches Hartich off capacity 1, and eta stays at most nu/(1+nu)", True)


def frontier():
    a = v = kT = 1.0

    def cost(eps, w):
        return kT * a * (v - eps) / eps + w * eps

    rows = []
    for w in (0.5, 1.0, 2.0, 3.0, 8.0, 20.0, 50.0):
        if w + 1e-15 < kT * a / v:
            eps = v
            heat = 0.0
        else:
            eps = math.sqrt(kT * a * v / w)
            heat = kT * a * (v / eps - 1.0)
        rows.append((w, eps, heat, heat + w * eps))
    print("  frontier a=v=kT=1")
    print("  %6s %16s %16s %16s" % ("w", "eps", "heat", "cost"))
    for w, eps, heat, c in rows:
        print("  %6g %16.12f %16.12f %16.12f" % (w, eps, heat, c))
    # closed forms
    expect = {
        2.0: (1.0 / math.sqrt(2.0), math.sqrt(2.0) - 1.0, 2.0 * math.sqrt(2.0) - 1.0),
        8.0: (1.0 / math.sqrt(8.0), math.sqrt(8.0) - 1.0, 2.0 * math.sqrt(8.0) - 1.0),
        20.0: (1.0 / math.sqrt(20.0), math.sqrt(20.0) - 1.0, 2.0 * math.sqrt(20.0) - 1.0),
        50.0: (1.0 / math.sqrt(50.0), math.sqrt(50.0) - 1.0, 2.0 * math.sqrt(50.0) - 1.0),
    }
    ok = True
    for w, eps, heat, c in rows:
        if w in expect:
            e, h, cc = expect[w]
            ok = ok and near(eps, e, 1e-12) and near(heat, h, 1e-12) and near(c, cc, 1e-12)
        step = 1e-4
        ok = ok and cost(eps, w) <= cost(max(1e-6, eps * (1 - step)), w) + 1e-12
        ok = ok and cost(eps, w) <= cost(min(v, eps * (1 + step) if eps < v else v), w) + 1e-12
    check("frontier values and local minima match 2 sqrt(kT a v w) - kT a above the threshold",
          ok and near(rows[0][3], 0.5, 1e-12) and near(rows[1][3], 1.0, 1e-12)
          and rows[2][3] < 2.0 and rows[3][3] < 3.0)
    # centered raw-error objective at stake 2 and 3 is above the blind cost
    for w, blind in ((2.0, 2.0), (3.0, 3.0)):
        eps = math.sqrt(a * v / w)
        centered = 2.0 * math.sqrt(a * v * w)  # min of av/eps + w eps
        if centered <= blind:
            check("centered raw-error cost is above the blind cost below w=4", False, "w=%g" % w)
            return
    check("centered raw-error objective is above the blind cost at stakes 2 and 3", True,
          "costs %.6f and %.6f against blind 2 and 3" % (2 * math.sqrt(2), 2 * math.sqrt(3)))


def trap(y, dx):
    y = np.asarray(y, dtype=float)
    return float(np.sum((y[1:] + y[:-1]) * 0.5) * dx)


def norm_cdf(z):
    z = np.asarray(z, dtype=float)
    return 0.5 * (1.0 + np.vectorize(math.erf)(z / math.sqrt(2.0)))


def norm_ppf(p):
    # Inverse standard normal via Newton on erf, accurate past 1e-14 on (1e-16, 1-1e-16).
    p = float(p)
    if p <= 0.0:
        return -1e6
    if p >= 1.0:
        return 1e6
    # rational start from a Beasley-Springer/Moro-style seed is unnecessary; erf Newton is stable
    x = 0.0 if abs(p - 0.5) < 1e-8 else math.sqrt(2.0) * _erfinv_seed(2 * p - 1)
    for _ in range(8):
        f = 0.5 * (1.0 + math.erf(x / math.sqrt(2.0))) - p
        dens = math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)
        x -= f / dens
    return x


def _erfinv_seed(y):
    # y in (-1,1). A short asymptotic seed; Newton above finishes it.
    a = 0.147
    sign = 1.0 if y >= 0 else -1.0
    ln = math.log(1.0 - y * y)
    first = 2 / (math.pi * a) + ln / 2
    return sign * math.sqrt(math.sqrt(first * first - ln / a) - first)


def quantizer(v, sigma, edges, n_grid, xmax):
    x = np.linspace(-xmax, xmax, n_grid)
    dx = float(x[1] - x[0])
    px = np.exp(-0.5 * x * x / v) / math.sqrt(2.0 * math.pi * v)
    z_hi = (edges[1:, None] - x[None, :]) / sigma
    z_lo = (edges[:-1, None] - x[None, :]) / sigma
    p_bin = np.clip(norm_cdf(z_hi) - norm_cdf(z_lo), 0.0, None)
    K = len(edges) - 1
    mass = np.array([trap(p_bin[k] * px, dx) for k in range(K)])
    learn = 0.0
    mmse = 0.0
    phi = np.exp(-0.5 * z_hi * z_hi) / math.sqrt(2.0 * math.pi)
    phi_lo = np.exp(-0.5 * z_lo * z_lo) / math.sqrt(2.0 * math.pi)
    for k in range(K):
        if mass[k] < 1e-16:
            continue
        lik = p_bin[k]
        good = lik > 1e-14
        post = np.where(good, lik * px, 0.0)
        z = trap(post, dx)
        if z <= 0.0:
            continue
        post /= z
        mean = trap(x * post, dx)
        var = trap((x - mean) ** 2 * post, dx)
        mmse += mass[k] * var
        dpx = (phi_lo[k] - phi[k]) / sigma
        score = np.zeros_like(x)
        score[good] = -x[good] / v + dpx[good] / lik[good]
        fisher = trap(score ** 2 * post, dx)
        learn += mass[k] * (v * fisher - 1.0)
    return {"learn": learn, "mmse": mmse, "mass_sum": float(mass.sum())}


def equal_edges(v, sigma, K):
    scale = math.sqrt(v + sigma ** 2)
    edges = [norm_ppf(k / K) * scale for k in range(K + 1)]
    edges[0] = -1e6
    edges[-1] = 1e6
    return np.array(edges, dtype=float)


def kbin():
    v = 1.0
    sigma = 0.5
    parent = v * sigma ** 2 / (sigma ** 2 + v)
    check("parent channel MMSE is 0.2", near(parent, 0.2, 1e-15))
    print("  K-bin, fine grid (xmax=12, n=12001), equal-probability edges by Newton ppf")
    print("  %4s %12s %12s %12s %12s" % ("K", "MMSE", "L", "R", "L/R"))
    fine = {}
    for K in (2, 4, 8, 16, 32, 64):
        out = quantizer(v, sigma, equal_edges(v, sigma, K), 12001, 12.0)
        R = (v - out["mmse"]) / out["mmse"]
        fine[K] = out
        print("  %4d %12.6f %12.6f %12.6f %12.6f" % (K, out["mmse"], out["learn"], R, out["learn"] / R))
        if out["learn"] + 1e-6 < R or abs(out["mass_sum"] - 1.0) > 1e-3:
            check("fine quantizer learning rate stays above R(MMSE)", False, "K=%d" % K)
            return
    check("fine 64-bin learning rate is within 1% of R(MMSE) and the ratio falls with K",
          fine[64]["learn"] / ((v - fine[64]["mmse"]) / fine[64]["mmse"]) < 1.01
          and fine[64]["learn"] / ((1 - fine[64]["mmse"]) / fine[64]["mmse"])
          < fine[2]["learn"] / ((1 - fine[2]["mmse"]) / fine[2]["mmse"]))
    print("  retuned so the bin MMSE is 0.2, same fine grid")
    tuned = {}
    for K in (8, 16, 32, 64):
        lo, hi = 0.02, 2.0
        best = None
        for _ in range(50):
            mid = 0.5 * (lo + hi)
            out = quantizer(v, mid, equal_edges(v, mid, K), 8001, 12.0)
            best = (mid, out)
            if out["mmse"] > 0.2:
                hi = mid
            else:
                lo = mid
        sigma_hat, out = best
        # one confirmation pass on the finer grid at the tuned sigma
        out = quantizer(v, sigma_hat, equal_edges(v, sigma_hat, K), 12001, 12.0)
        tuned[K] = (sigma_hat, out)
        print("  K=%d sigma=%.6f mmse=%.6f L=%.6f" % (K, sigma_hat, out["mmse"], out["learn"]))
    # The draft prints 4.471064, 4.157870, 4.058746, 4.022937.
    draft = {8: 4.471064, 16: 4.157870, 32: 4.058746, 64: 4.022937}
    gaps = []
    for K, target in draft.items():
        gaps.append(abs(tuned[K][1]["learn"] - target))
    print("  absolute gaps versus the draft's four heats: " + " ".join("%.6f" % g for g in gaps))
    check("retuned fine-grid learning rates agree with the draft heats to 0.002",
          max(gaps) < 0.002 and all(abs(tuned[K][1]["mmse"] - 0.2) < 2e-3 for K in draft),
          "max gap %.6f" % max(gaps))


def quartic():
    def run(v, width, n_m, n_x, xmax_scale):
        xmax = xmax_scale * math.sqrt(v)
        mmax = xmax + 5.0 * width
        x = np.linspace(-xmax, xmax, n_x)
        m = np.linspace(-mmax, mmax, n_m)
        dx = float(x[1] - x[0])
        dm = float(m[1] - m[0])
        px = np.exp(-0.5 * x * x / v) / math.sqrt(2.0 * math.pi * v)
        mm, xx = np.meshgrid(m, x, indexing="ij")
        log_lik = -((mm - xx) ** 4) / (4.0 * width ** 4)
        log_lik -= log_lik.max(axis=0, keepdims=True)
        lik = np.exp(log_lik)
        Z = np.sum(lik, axis=0) * dm
        pm_x = lik / Z
        joint = pm_x * px[None, :]
        marg = np.sum(joint, axis=1) * dx
        # posterior along x for every m
        post = joint / np.maximum(marg[:, None], 1e-300)
        z = np.sum((post[:, 1:] + post[:, :-1]) * 0.5, axis=1) * dx
        post = post / np.maximum(z[:, None], 1e-300)
        mean = np.sum((x[None, 1:] * post[:, 1:] + x[None, :-1] * post[:, :-1]) * 0.5, axis=1) * dx
        var = np.sum((((x - mean[:, None]) ** 2 * post)[:, 1:] + ((x - mean[:, None]) ** 2 * post)[:, :-1]) * 0.5, axis=1) * dx
        logp = np.log(np.clip(post, 1e-300, None))
        score = np.gradient(logp, dx, axis=1)
        # kill the gradient where the posterior was clipped
        score = np.where(post > 1e-18, score, 0.0)
        fisher = np.sum((score[:, 1:] ** 2 * post[:, 1:] + score[:, :-1] ** 2 * post[:, :-1]) * 0.5, axis=1) * dx
        weight = np.sum((marg[1:] + marg[:-1]) * 0.5) * dm
        mmse = float(np.sum((marg[1:] * var[1:] + marg[:-1] * var[:-1]) * 0.5) * dm / weight)
        fbar = float(np.sum((marg[1:] * fisher[1:] + marg[:-1] * fisher[:-1]) * 0.5) * dm / weight)
        return {"mmse": mmse, "F": fbar, "weight": weight}

    coarse = run(1.0, 0.45, 801, 1201, 6.0)
    fine = run(1.0, 0.45, 1601, 2401, 8.0)
    for label, out in (("coarse", coarse), ("fine", fine)):
        excess = out["F"] - 1.0 / out["mmse"]
        learn = out["F"] - 1.0  # a=v=1, L=a(v F - 1)= F-1
        kalman = 1.0 / out["mmse"] - 1.0
        print("  quartic %s: MMSE=%.6f Fisher=%.6f 1/MMSE=%.6f L=%.6f R=%.6f excess=%.6f weight=%.4f" % (
            label, out["mmse"], out["F"], 1.0 / out["mmse"], learn, kalman, excess, out["weight"]))
    check("quartic conditional Fisher exceeds 1/MMSE on both grids",
          coarse["F"] > 1.0 / coarse["mmse"] + 0.5 and fine["F"] > 1.0 / fine["mmse"] + 0.5,
          "coarse excess %.4f fine excess %.4f" % (
              coarse["F"] - 1.0 / coarse["mmse"], fine["F"] - 1.0 / fine["mmse"]))


def lyapunov(A, diffusion):
    n = A.shape[0]
    M = np.kron(np.eye(n), A) + np.kron(A, np.eye(n))
    c = np.linalg.solve(M, -diffusion.reshape(-1))
    C = c.reshape(n, n)
    return 0.5 * (C + C.T)


def two_memory(a, v, beta1, beta2, gamma1, gamma2, k12, k21, D1, D2):
    A = np.array([
        [-a, 0.0, 0.0],
        [gamma1, -beta1, k12],
        [gamma2, k21, -beta2],
    ], dtype=float)
    if np.any(np.real(np.linalg.eigvals(A)) >= -1e-8):
        return None
    C = lyapunov(A, np.diag([2 * a * v, 2 * D1, 2 * D2]))
    if np.any(np.linalg.eigvalsh(C) <= 1e-12):
        return None
    Cmm = C[1:, 1:]
    Cmx = C[1:, 0]
    s = float(C[0, 0] - Cmx @ np.linalg.solve(Cmm, Cmx))
    if not (0.0 < s < v):
        return None
    learn = a * (v / s - 1.0)
    # f1 = gamma1 X - beta1 M1 + k12 M2, derivative in M1 is -beta1
    f1 = np.array([gamma1, -beta1, k12])
    f2 = np.array([gamma2, k21, -beta2])
    Q = float(f1 @ C @ f1) / D1 - beta1 + float(f2 @ C @ f2) / D2 - beta2
    return {"s": s, "learn": learn, "heat": Q, "R": a * (v - s) / s}


def two_memories():
    rng = np.random.default_rng(19)
    a = v = 1.0
    n_ok = 0
    closest = 1e9
    worst_gap = 0.0
    for _ in range(30):
        row = two_memory(
            a, v,
            float(rng.uniform(0.5, 6.0)),
            float(rng.uniform(0.5, 6.0)),
            float(rng.uniform(0.2, 5.0)),
            float(rng.uniform(0.2, 5.0)),
            float(rng.uniform(-1.0, 1.0)),
            float(rng.uniform(-1.0, 1.0)),
            float(rng.uniform(0.05, 1.5)),
            float(rng.uniform(0.05, 1.5)),
        )
        if row is None:
            continue
        n_ok += 1
        if row["heat"] + 1e-8 < row["learn"]:
            check("two-memory heat stays above the learning rate", False,
                  "Q=%.6e L=%.6e" % (row["heat"], row["learn"]))
            return
        closest = min(closest, row["heat"] / row["R"])
        worst_gap = max(worst_gap, row["heat"] - row["learn"])
    check("30-draw seed 19: stable systems stay above the learning rate",
          n_ok >= 20 and closest >= 1.0 - 1e-8,
          "stable=%d closest heat/R(s)=%.6f" % (n_ok, closest))
    # equilibrium embedding of the shrunk spring
    lam = 1e4
    eps = 0.2
    c = (v - eps) / v
    rho = lam / (a + lam)
    sig2 = (v - eps) * (rho * (v + eps) / v - 1.0)
    one = moments(a, lam, c * lam, lam * sig2, v)
    emb = two_memory(a, v, lam, 1.7, c * lam, 0.0, 0.0, 0.0, lam * sig2, 0.4)
    check("equilibrium second coordinate adds no heat",
          emb is not None and near(emb["heat"], one["heat"], 1e-9) and near(emb["s"], one["s"], 1e-9),
          "heat=%.10f one=%.10f" % (emb["heat"], one["heat"]))


def crossref():
    dois = [
        ("10.1103/PhysRevX.4.031015", "Horowitz", "Esposito", 2014),
        ("10.1088/1367-2630/16/10/103024", "Barato", "Seifert", 2014),
        ("10.1103/PhysRevE.93.022116", "Hartich", "Seifert", 2016),
        ("10.1088/1367-2630/16/12/125007", "Horowitz", "Sandberg", 2014),
        ("10.1137/0119020", "Duncan", None, 1970),
        ("10.1088/1742-5468/2015/01/P01014", "Bo", "Celani", 2015),
        ("10.1007/s10955-004-8781-9", "Mitter", "Newton", 2005),
        ("10.1103/PhysRevE.90.042119", "Sandberg", "Mitter", 2014),
        ("10.1109/ALLERTON.2014.7028503", "Sandberg", "Mitter", 2014),
    ]
    print("  Crossref")
    for doi, family_a, family_b, year in dois:
        url = "https://api.crossref.org/works/" + doi
        req = urllib.request.Request(url, headers={"User-Agent": "gtao-review/pr178 (mailto:review@example.com)"})
        status = None
        body = None
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    status = resp.status
                    body = resp.read().decode("utf-8")
                break
            except Exception as exc:
                status = getattr(exc, "code", None)
                print("  retry %s status=%s %s" % (doi, status, exc.__class__.__name__))
                time.sleep(2.0 * (attempt + 1))
        if status != 200 or not body:
            check("Crossref %s" % doi, False, "status %s" % status)
            continue
        msg = json.loads(body)["message"]
        title = (msg.get("title") or [""])[0]
        got_year = None
        issued = (msg.get("issued") or {}).get("date-parts") or [[None]]
        if issued and issued[0]:
            got_year = issued[0][0]
        authors = []
        for person in msg.get("author") or []:
            authors.append(person.get("family") or "")
        ok = (got_year == year) and any(family_a.lower() in a.lower() for a in authors)
        if family_b:
            ok = ok and any(family_b.lower() in a.lower() for a in authors)
        container = (msg.get("container-title") or [""])[0]
        print("  HTTP %s | %s | %s | %s | %s | %s" % (status, doi, got_year, container, title, "; ".join(authors)))
        check("Crossref %s matches %s %s" % (doi, family_a, year), ok,
              "year=%s authors=%s" % (got_year, ", ".join(authors)))
        time.sleep(0.4)


def main():
    symbolic_identities()
    gaussian_flow_sign()
    reference_and_shrunk()
    capacity_and_hartich()
    frontier()
    kbin()
    quartic()
    two_memories()
    crossref()
    print("PASS %d  FAIL %d" % (PASS, FAIL))
    if FAIL:
        print("RECOMPUTE FAILED")
        return 1
    print("ALL INDEPENDENT CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
