#!/usr/bin/env python3
"""Numerical checks for theory/SELECTION_AXIOMS.md (SA1b equipartition, CL19
occupation and excess rates, SA2 addition of means).

These checks are NUMERICAL. They are not a substitute for the proofs in the
note, they do not re-run T27, and they do not touch locked hashes.

The occupation of driftless Brownian motion reset at ±b is the normalized
Green function ρ(x)=(b-|x|)/b². That identity is recorded algebraically
below. A path simulation of the reset ((s,S)) process recovers E[x²]=b²/6
and the first absolute moment. Inverse-CDF sampling of the assumed density,
if used, is labeled as such and is not a derivation and not a path
simulation.

Run from the repo root:

    nice -n 19 python3 tools/selection_axioms_checks.py

Exit 0 and the line ALL SA CHECKS PASS means every identity below held.
"""
from __future__ import annotations

import math
import sys

import numpy as np


def check(ok, detail, name, cond, msg=""):
    ok.append((name, bool(cond)))
    detail.append("%s: %s%s" % (name, "OK" if cond else "FAIL", ("  " + msg) if msg else ""))


# ---------------------------------------------------------------------------
# Green function of driftless BM of variance rate sigma2, killed at ±b.
# (σ²/2) g'' = -δ_0 on (-b,b), g(±b)=0. Then ρ = g / ∫g.
# ---------------------------------------------------------------------------
def green_function(x, b, sigma2):
    return (b - abs(x)) / sigma2 if abs(x) <= b else 0.0


def occupation_density(x, b):
    return (b - abs(x)) / (b * b) if abs(x) <= b else 0.0


def green_function_identities(b=2.0, sigma2=1.0, tol=1e-12):
    """Algebraic identities for the Green function and the occupation. Not a Monte Carlo."""
    results = []

    def rec(name, cond, msg=""):
        results.append((name, bool(cond), msg))

    rec("Green g(±b)=0", abs(green_function(b, b, sigma2)) < tol and abs(green_function(-b, b, sigma2)) < tol)
    # one-sided derivatives of g(x)=(b-|x|)/σ²: g'(0+)=-1/σ², g'(0-)=+1/σ²
    gp_plus = -1.0 / sigma2
    gp_minus = 1.0 / sigma2
    rec(
        "Green jump (σ²/2)(g'(0+)-g'(0-))=-1",
        abs((sigma2 / 2.0) * (gp_plus - gp_minus) + 1.0) < tol,
        "jump=%.12f" % ((sigma2 / 2.0) * (gp_plus - gp_minus)),
    )
    # ∫_{-b}^b g dx = b²/σ², the mean exit time (trapezoid on a fine grid)
    mean_exit = b * b / sigma2
    grid = np.linspace(-b, b, 20001)
    # numpy 2 names this trapezoid; numpy 1.26 has trapz.
    trap = getattr(np, "trapezoid", None)
    if trap is None:
        trap = np.trapz
    integ = float(trap((b - np.abs(grid)) / sigma2, grid))
    rec("Green integral is mean exit b²/σ²", abs(integ - mean_exit) < 1e-8, "integ=%.12f want=%.12f" % (integ, mean_exit))
    # ρ = g / ∫g
    xs = np.linspace(-b, b, 9)
    ok_ratio = all(
        abs(occupation_density(x, b) - green_function(x, b, sigma2) / mean_exit) < tol for x in xs
    )
    rec("occupation is normalized Green function", ok_ratio)
    rec("occupation E[x²]=b²/6", abs(_occupation_moment2(b) - (b * b / 6.0)) < tol)
    rec("occupation E[|x|]=b/3", abs(_occupation_moment_abs(b) - (b / 3.0)) < tol)
    return results


def _occupation_moment2(b):
    # 2 ∫_0^b x² (b-x)/b² dx = 2/b² (b·b³/3 - b⁴/4) = b²/6
    return (2.0 / (b * b)) * (b * (b ** 3) / 3.0 - (b ** 4) / 4.0)


def _occupation_moment_abs(b):
    # 2 ∫_0^b x (b-x)/b² dx = 2/b² (b·b²/2 - b³/3) = b/3
    return (2.0 / (b * b)) * (b * (b * b) / 2.0 - (b ** 3) / 3.0)


# ---------------------------------------------------------------------------
# Path simulation of the reset ((s,S)) process: driftless BM, reset to 0
# when |x| hits b. Brownian-bridge first-exit correction between steps.
# ---------------------------------------------------------------------------
def simulate_reset_process(b, sigma2, dt, n_steps, rng, burn_frac=0.1):
    """Simulate X_{t+dt}=X_t+σ√dt Z, reset to 0 on exit of [-b,b].

    Between steps, exit is declared with the Brownian-bridge hitting
    probability, so the discrete scheme does not wait for a sample to
    land outside the interval.
    """
    scale = math.sqrt(sigma2 * dt)
    inc = scale * rng.standard_normal(n_steps)
    u = rng.random(n_steps)
    x = np.empty(n_steps)
    cur = 0.0
    s = sigma2 * dt
    thresh = 8.0 * scale
    for i in range(n_steps):
        prev = cur
        cur = prev + inc[i]
        if cur >= b or cur <= -b:
            cur = 0.0
        elif b - prev < thresh or b - cur < thresh or prev + b < thresh or cur + b < thresh:
            p_up = math.exp(-2.0 * (b - prev) * (b - cur) / s)
            p_dn = math.exp(-2.0 * (prev + b) * (cur + b) / s)
            if u[i] < p_up + p_dn - p_up * p_dn:
                cur = 0.0
        x[i] = cur
    burn = int(burn_frac * n_steps)
    return x[burn:]


def reset_process_moments(b, sigma2, dt, n_steps, rng):
    x = simulate_reset_process(b, sigma2, dt, n_steps, rng)
    return float(np.mean(x * x)), float(np.mean(np.abs(x))), x


def triangular_occupation_sample(b, n, rng):
    """Inverse-CDF sample of the assumed density. Not a derivation and not a path simulation."""
    # density rho(x) = (b - |x|) / b^2 on [-b, b].
    # CDF on [0, b] of |X|: P(|X| <= t) = 1 - (b-t)^2 / b^2, so |X| = b (1 - sqrt(U)).
    u = rng.random(n)
    mag = b * (1.0 - np.sqrt(u))
    sign = rng.choice(np.array([-1.0, 1.0]), size=n)
    return sign * mag


def run_checks(rng=None):
    if rng is None:
        rng = np.random.default_rng(20261121)
    ok, detail = [], []

    # SA1b: equipartition
    def equipartition_mc(d, beta, n=200_000):
        x = rng.normal(0.0, 1.0 / math.sqrt(beta), size=(n, d))
        j = 0.5 * np.sum(x * x, axis=1)
        return float(j.mean()), d / (2.0 * beta)

    for d, beta in ((1, 2.0), (1, 8.0), (2, 4.0), (3, 10.0), (5, 3.0)):
        got, want = equipartition_mc(d, beta)
        rel = abs(got - want) / want
        check(
            ok, detail, "SA1b d=%d beta=%g" % (d, beta),
            rel < 0.03,
            "mc=%.6f exact=%.6f rel=%.4f" % (got, want, rel),
        )

    for d, beta in ((1, 1.0), (4, 7.5), (8, 0.5)):
        H = np.diag(np.linspace(0.5, 2.0, d))
        Sigma = np.linalg.inv(beta * H)
        got = 0.5 * float(np.trace(H @ Sigma))
        want = d / (2.0 * beta)
        check(
            ok, detail, "SA1b-trace d=%d beta=%g" % (d, beta),
            abs(got - want) < 1e-12,
            "got=%.12f want=%.12f" % (got, want),
        )

    # Green function / occupation algebra
    for name, cond, msg in green_function_identities():
        check(ok, detail, name, cond, msg)

    # Path simulation of the reset process
    b_sim, sigma2_sim = 2.0, 1.0
    dt, n_steps = 4.0e-4, 3_000_000
    ex2, eabs, _xs = reset_process_moments(b_sim, sigma2_sim, dt, n_steps, rng)
    want2, want1 = b_sim * b_sim / 6.0, b_sim / 3.0
    check(
        ok, detail, "reset-process E[x^2]",
        abs(ex2 - want2) / want2 < 0.03,
        "mc=%.6f exact=%.6f rel=%.4f" % (ex2, want2, abs(ex2 - want2) / want2),
    )
    check(
        ok, detail, "reset-process E[|x|]",
        abs(eabs - want1) / want1 < 0.03,
        "mc=%.6f exact=%.6f rel=%.4f" % (eabs, want1, abs(eabs - want1) / want1),
    )

    # Inverse-CDF of the assumed density: labeled, not a derivation
    w = 3.0
    xs = triangular_occupation_sample(b_sim, 300_000, rng)
    got_ex = w * float(np.mean(xs ** 2))
    want_ex = w * b_sim * b_sim / 6.0
    check(
        ok, detail, "inverse-CDF assumed density E[w x^2]",
        abs(got_ex - want_ex) / want_ex < 0.02,
        "mc=%.6f exact=%.6f" % (got_ex, want_ex),
    )

    # CL19 algebraic identities at b*
    k, sigma2, w = 0.4, 0.9, 2.0
    bstar = (6.0 * k * sigma2 / w) ** 0.25
    op = w * bstar * bstar / 6.0
    lumps = k * sigma2 / (bstar * bstar)
    total = op + lumps
    want_op = math.sqrt(k * w * sigma2 / 6.0)
    want_total = 2.0 * want_op
    check(ok, detail, "CL19 b* operational identity", abs(op - want_op) < 1e-12, "op=%.12f want=%.12f" % (op, want_op))
    check(ok, detail, "CL19 b* lumps equal operational", abs(lumps - op) < 1e-12, "lumps=%.12f op=%.12f" % (lumps, op))
    check(ok, detail, "CL19 b* total identity", abs(total - want_total) < 1e-12, "total=%.12f want=%.12f" % (total, want_total))

    def rate(bb):
        return k * sigma2 / (bb * bb) + w * bb * bb / 6.0

    eps = 1e-6
    dleft = (rate(bstar) - rate(bstar - eps)) / eps
    dright = (rate(bstar + eps) - rate(bstar)) / eps
    check(
        ok, detail, "CL19 first-order condition at b*",
        abs(dleft) < 1e-5 and abs(dright) < 1e-5,
        "dleft=%.3e dright=%.3e" % (dleft, dright),
    )

    # SA2 addition of means. Inverse-CDF here is a convenience sampler of the
    # assumed occupation, not a derivation of it.
    d, beta = 3, 5.0
    n = 200_000
    x = triangular_occupation_sample(bstar, n, rng)
    y = rng.normal(0.0, 1.0 / math.sqrt(beta), size=(n, d))
    excess = w * x * x + 0.5 * np.sum(y * y, axis=1)
    got = float(excess.mean())
    want = w * bstar * bstar / 6.0 + d / (2.0 * beta)
    check(
        ok, detail, "SA2 addition of means",
        abs(got - want) / want < 0.02,
        "mc=%.6f exact=%.6f" % (got, want),
    )

    # SA3 curvature cancellation
    alpha, w3, VG, sig_th2 = 0.8, 1.7, 0.25, 0.5
    lam = 2.0 * alpha * w3 * VG
    var_L = sig_th2 / (2.0 * lam)
    got = w3 * var_L
    want = sig_th2 / (4.0 * alpha * VG)
    check(ok, detail, "SA3 curvature cancellation", abs(got - want) < 1e-12, "got=%.12f want=%.12f" % (got, want))

    def phi(rho, N):
        if abs(rho - 1.0) < 1e-15:
            return 1.0 / N
        return (1.0 - rho) / (1.0 - rho ** N)

    N = 11
    for rho in (0.4, 0.9, 1.0, 1.2, 2.5):
        ratio = phi(1.0 / rho, N) / phi(rho, N) if rho != 1.0 else 1.0
        want = rho ** (N - 1) if rho != 1.0 else 1.0
        check(
            ok, detail, "SA1 fixation ratio rho=%g" % rho,
            abs(ratio - want) / max(want, 1e-12) < 1e-10,
            "got=%.12g want=%.12g" % (ratio, want),
        )

    return ok, detail


def main(argv=None):
    ok, detail = run_checks()
    nfail = sum(1 for _, c in ok if not c)
    for line in detail:
        print(line)
    if nfail:
        print("SOME SA CHECKS FAILED (%d)" % nfail)
        return 1
    print("ALL SA CHECKS PASS (%d)" % len(ok))
    return 0


if __name__ == "__main__":
    sys.exit(main())
