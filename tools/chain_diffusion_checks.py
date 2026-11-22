#!/usr/bin/env python3
"""Numerical checks for theory/CHAIN_DIFFUSION.md (N66).

NUMERICAL, not the proofs. They check:
  (1) the static discrete-Gaussian excess against the Poisson bound of CD1;
  (2) the stationary excess of the exact one-dimensional lag jump-diffusion
      (Brownian centre) against DS1's (1/(2 beta))(1+D/D_m), at several
      lattice spacings, population sizes, and drift ratios;
  (3) the exact identity excess error = E[R] / (4 D_m beta), where R is the
      generator defect on L^2.

The stationary density is the null vector of the forward operator on a grid
aligned with the jump. Quick mode is what pytest runs. --full writes
theory/chain_diffusion_checks/results_full.json.

    nice -n 19 python3 tools/chain_diffusion_checks.py
    nice -n 19 python3 tools/chain_diffusion_checks.py --full
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def moran_phi(x, N):
    x = np.asarray(x, float)
    out = np.empty(x.shape, float)
    small = np.abs(x) < 1e-12
    out[small] = 1.0 / N
    pos = (x > 0) & ~small
    neg = (x < 0) & ~small
    xp = np.asarray(x[pos], float)
    out[pos] = np.exp(-(N - 1) * xp) * (-np.expm1(-xp)) / (-np.expm1(-N * xp))
    xn = np.asarray(x[neg], float)
    out[neg] = np.expm1(xn) / np.expm1(N * xn)
    return out


def static_excess(beta, h, delta, n_sigma=14):
    """Exact stationary excess of the static chain: Gibbs weight exp(-beta J)
    on delta Z, J = (h/2) (n delta)^2. Returns (excess, formula, a)."""
    a = beta * h * delta ** 2
    sigma = 1.0 / math.sqrt(beta * h)
    nmax = int(math.ceil(n_sigma * sigma / delta)) + 5
    ns = np.arange(-nmax, nmax + 1)
    logw = -0.5 * a * ns ** 2
    logw -= logw.max()
    w = np.exp(logw)
    w /= w.sum()
    excess = float(np.sum(0.5 * h * (ns * delta) ** 2 * w))
    return excess, 1.0 / (2.0 * beta), a


def poisson_gap_bound(beta, a):
    """CD1 upper bound on 1/(2 beta) - E[J], for a = beta h delta^2 <= 1."""
    q = math.exp(-2.0 * math.pi ** 2 / a)
    return (8.0 * math.pi ** 2 / (beta * a)) * q


def solve_brownian(N, beta, h, Dm, D, delta, n_sigma=8, m=2):
    """Stationary excess of the exact lag jump-diffusion, Brownian centre.

    Jumps ±delta at Moran rates, plus diffusion of variance rate 2D from the
    centre. Returns a dict with the excess, the DS1 formula, the generator
    defect, and grid diagnostics.
    """
    sigma2 = (Dm + D) / (Dm * beta * h)
    sigma = math.sqrt(sigma2)
    dx = delta / m
    Lmax = n_sigma * sigma + 6.0 * delta
    n_half = int(math.ceil(Lmax / dx))
    xs = np.arange(-n_half, n_half + 1) * dx
    n = len(xs)
    alpha = beta / (N - 1.0)
    mu = 2.0 * Dm / delta ** 2
    rho = N * mu / 2.0
    x_plus = alpha * h * (delta * xs + 0.5 * delta ** 2)
    x_minus = alpha * h * (-delta * xs + 0.5 * delta ** 2)
    rp = rho * moran_phi(x_plus, N)
    rm = rho * moran_phi(x_minus, N)
    # interior indices 1..n-2; Dirichlet at the ends
    Nint = n - 2
    rows, cols, vals = [], [], []

    def add(r, c, val):
        rows.append(r)
        cols.append(c)
        vals.append(val)

    for i in range(1, n - 1):
        r = i - 1
        add(r, r, -2.0 * D / dx ** 2 - (rp[i] + rm[i]))
        if i + 1 < n - 1:
            add(r, i, D / dx ** 2)          # interior index of i+1 is i
        if i - 1 > 0:
            add(r, i - 2, D / dx ** 2)      # interior index of i-1 is i-2
        j = i - m
        if 0 < j < n - 1:
            add(r, j - 1, rp[j])
        j = i + m
        if 0 < j < n - 1:
            add(r, j - 1, rm[j])
    A = csr_matrix((vals, (rows, cols)), shape=(Nint, Nint)).tolil()
    A[-1, :] = dx
    b = np.zeros(Nint)
    b[-1] = 1.0
    p_int = spsolve(A.tocsr(), b)
    p = np.zeros(n)
    p[1:-1] = np.real(p_int)
    mass = float(p.sum() * dx)
    excess = float(np.sum(0.5 * h * xs ** 2 * p) * dx)
    formula = (1.0 / (2.0 * beta)) * (1.0 + D / Dm)
    # generator defect on L^2: G(L^2) - Langevin(L^2)
    # Langevin: -2 a L^2 + 2 Dm + 2 D, a = Dm beta h
    a_drift = Dm * beta * h
    GL2 = rp * (2.0 * delta * xs + delta ** 2) + rm * (-2.0 * delta * xs + delta ** 2) + 2.0 * D
    LL2 = -2.0 * a_drift * xs ** 2 + 2.0 * Dm + 2.0 * D
    R = GL2 - LL2
    ER = float(np.sum(R * p) * dx)
    # At stationarity E[G(L^2)] = 0, so E[Langevin(L^2)] = -E[R].
    # Langevin(L^2) = -2 a L^2 + 2(Dm+D), hence
    # E[L^2] = (Dm+D)/a + E[R]/(2a) and E[J] - formula = E[R]/(4 Dm beta).
    predicted_gap = ER / (4.0 * Dm * beta)
    return {
        "excess": excess,
        "formula": formula,
        "rel": (excess - formula) / formula,
        "eps": delta ** 2 * beta * h * (1.0 + D / Dm),
        "mass": mass,
        "minp": float(p.min()),
        "n": n,
        "ER": ER,
        "gap": excess - formula,
        "predicted_gap": predicted_gap,
        "sigma": sigma,
    }


def check(ok, lines, name, cond, msg=""):
    ok.append((name, bool(cond)))
    lines.append("%s: %s%s" % (name, "OK" if cond else "FAIL", ("  " + msg) if msg else ""))


def static_checks(ok, lines, full):
    betas = (1.0, 2.5) if full else (1.0,)
    deltas = (0.9, 0.6, 0.4, 0.25) if full else (0.8, 0.5)
    for beta in betas:
        for delta in deltas:
            excess, formula, a = static_excess(beta, 1.0, delta)
            gap = formula - excess  # positive: lattice sits slightly below
            bound = poisson_gap_bound(beta, a)
            # Below ~1e-15 the excess is an order-1 float and the gap is roundoff.
            tol = 1e-14
            check(ok, lines, "CD1 static a=%.3f beta=%.1f gap>=0" % (a, beta), gap >= -tol,
                  "gap %.3e" % gap)
            check(ok, lines, "CD1 static a=%.3f beta=%.1f gap<=bound" % (a, beta),
                  gap <= bound * (1 + 1e-9) + tol,
                  "gap %.3e bound %.3e" % (gap, bound))
            q = math.exp(-2.0 * math.pi ** 2 / a)
            lead = (4.0 * math.pi ** 2 / (beta * a)) * q
            if lead >= tol:
                check(ok, lines, "CD1 static a=%.3f lead within 1e-3 rel" % a,
                      abs(gap - lead) <= 1e-3 * lead + tol,
                      "gap %.6e lead %.6e" % (gap, lead))
            else:
                check(ok, lines, "CD1 static a=%.3f gap at roundoff" % a, abs(gap) <= tol,
                      "gap %.3e lead %.3e" % (gap, lead))


def moving_checks(ok, lines, results, full):
    # several sizes: lattice spacing at fixed beta, h, Dm, and a few N and D/Dm
    specs = [
        (20, 1.0, 1.0, 1.0, 1.0, 0.50),
        (20, 1.0, 1.0, 1.0, 1.0, 0.25),
        (20, 1.0, 1.0, 1.0, 0.25, 0.25),
        (5, 1.0, 1.0, 1.0, 1.0, 0.25),
        (50, 1.0, 1.0, 1.0, 1.0, 0.25),
    ]
    if full:
        specs += [
            (20, 1.0, 1.0, 1.0, 1.0, 0.35),
            (20, 1.0, 1.0, 1.0, 1.0, 0.18),
            (20, 1.0, 1.0, 1.0, 4.0, 0.25),
            (100, 1.0, 1.0, 1.0, 1.0, 0.25),
            (10, 2.0, 1.0, 0.5, 0.5, 0.20),
        ]
    else:
        specs = specs[:3]
    for N, beta, h, Dm, D, delta in specs:
        r = solve_brownian(N, beta, h, Dm, D, delta)
        rel_over = abs(r["rel"]) / max(r["eps"], 1e-12)
        tag = "N=%d D/Dm=%.2f delta=%.2f eps=%.4f rel=%+.4e rel/eps=%.3f" % (
            N, D / Dm, delta, r["eps"], r["rel"], rel_over)
        check(ok, lines, "mass " + tag, abs(r["mass"] - 1.0) < 1e-6, "mass %.6f" % r["mass"])
        check(ok, lines, "density >= -1e-8 " + tag, r["minp"] >= -1e-8, "minp %.2e" % r["minp"])
        # observed envelope on this grid; the proof is O(eps), this is the check
        check(ok, lines, "rel error <= 0.15*eps " + tag, abs(r["rel"]) <= 0.15 * r["eps"] + 1e-6,
              tag)
        check(ok, lines, "identity gap= E[R]/(4 Dm beta) " + tag,
              abs(r["gap"] - r["predicted_gap"]) <= 1e-4 * max(1.0, abs(r["formula"])),
              "gap %.6e pred %.6e" % (r["gap"], r["predicted_gap"]))
        results.append({
            "N": N, "beta": beta, "h": h, "Dm": Dm, "D": D, "delta": delta,
            "eps": r["eps"], "excess": r["excess"], "formula": r["formula"],
            "rel": r["rel"], "rel_over_eps": rel_over, "mass": r["mass"],
            "gap": r["gap"], "predicted_gap": r["predicted_gap"],
        })


def main(argv=None):
    argv = sys.argv if argv is None else argv
    full = "--full" in argv
    ok, lines, results = [], [], []
    static_checks(ok, lines, full)
    moving_checks(ok, lines, results, full)
    nfail = sum(1 for _, c in ok if not c)
    lines.append("%d checks, %d failed" % (len(ok), nfail))
    if nfail == 0:
        lines.append("ALL CHAIN DIFFUSION CHECKS PASS")
    text = "\n".join(lines)
    print(text)
    if full:
        out_dir = os.path.join(ROOT, "theory", "chain_diffusion_checks")
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "results_full.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"checks_failed": nfail, "rows": results, "log": text}, fh, indent=1)
        print("wrote", path)
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
