#!/usr/bin/env python3
"""Adaptation time on a sampled grid (QUEUE DISCRETE-TA, pick 23, ledger 108-110).

Two worlds with the same second moments, sensed in white noise of density N, sampled every Delta:
  * Gauss-Markov (OU) world, best linear tracker = steady-state Kalman filter.  World rate a = 2*lam, variance mu^2,
    so q = 2 a mu^2 = 4 lam mu^2 (the telegraph world's covariance).  Per-sample model: x_k = phi x_{k-1} + w_k,
    phi = exp(-a Delta), Var w = mu^2 (1 - phi^2); y_k = x_k + e_k, Var e = s2 = N / Delta.
  * Two-state switching (telegraph) world, Bayes filter.  x = +-mu, flips at rate lam each way; per-sample model:
    flip probability p = (1 - exp(-2 lam Delta)) / 2 between samples, y_k = x_k + e_k, Var e = N / Delta.
    This is the discrete-time HMM that the aqn estimators fit (N = s2 * Delta).

Definitions (fixed here; see reviews/night2/DISCRETE_TA/REPORT.md section 1).
  Linear t_A  = the filter's memory (e-folding) time, Delta / (-ln z), z = the steady-state filter pole (1-K) phi.
                Continuous limit 1 / sqrt(a^2 + q/N) (THEORY 2.2 memory time).
  Bayes t_A   = N16's quantity: mean time from a switch until the filtered log-odds L first reaches <= 0, with L at the
                switch drawn from the filter's pre-switch law (two choices below; N16 derived it for 'quiet'), and the
                world held at the new state afterwards.  Continuous time: t = inf{t >= 0: L(t) <= 0}.  Sampled grid: Delta * E[n],
                n = min{n >= 0: L_n <= 0}, L_0 = posterior after the last pre-switch sample, first post-switch sample
                at n = 1.  The N16 plug-in (N/2mu^2)[ln(2mu^2/(lam N)) - gamma - 1] is its kappa -> 0 asymptote.

Results (derived in the report; checked by tests and by the independent Monte Carlo in the report's checks):
  Linear (exact, closed form):  cosh(beta Delta) = cosh(a Delta) + rho sinh(a Delta),  rho = mu^2 Delta / N,
                                t_A = 1/beta;  t_A / t_A_cont = 1 + 1/(24 r^2) + ... at a << beta (r = t_A / Delta).
  Bayes (asymptotic):           t_A_grid = T_cont(kappa) + C1 sqrt(Delta N / mu^2) + c2 Delta + o(Delta),
                                C1 = -zeta(1/2)/sqrt(2 pi) = 0.5826 (expected overshoot of the sampled log-odds walk
                                below 0, per Broadie-Glasserman-Kou 1997 / Siegmund; optional stopping gives the time),
                                c2 ~ 0.25 (numerical fit, 0.21-0.26 over kappa 1e-6..3e-2; not derived),
                                T_cont = exact continuous mean first passage (quadrature below).
                                Exact values on any grid: bayes_ta_grid() (Markov-chain solve on an L lattice).
  Two pre-switch laws (both converge to the N16 plug-in as kappa -> 0; they differ by O(kappa ln 1/kappa)):
    'quiet'  = the filter's resting law after a long period with no switch (N16's derivation, exp(L - kappa cosh L));
    'switch' = the stationary law at a typical switch (what averaging over all switches of a stationary record gives).

Units: any consistent units; functions take mu, lam, N, Delta.  Command line prints JSON:
  discrete_ta.py linear --mu 1 --lam 0.01 --N 1 --Delta 0.5
  discrete_ta.py bayes  --mu 1 --lam 0.002 --N 9 --Delta 1 [--law quiet|switch] [--h 0.02]
  discrete_ta.py table  [--law quiet|switch]   (a compact correction-factor table, theta = 1)
"""
import argparse, json, math, sys
import numpy as np
from scipy.special import k0e, k1e, ndtr, zeta

EULER_GAMMA = 0.5772156649015329
C1 = float(-zeta(0.5) / math.sqrt(2 * math.pi))  # 0.58259...


# ---------------------------------------------------------------- linear tracker (Kalman steady state)
def kalman_steady(mu, lam, N, Delta):
    """Exact steady-state Kalman quantities for the sampled OU world (a = 2 lam, Var x = mu^2, Var e = N/Delta)."""
    a = 2.0 * lam
    phi = math.exp(-a * Delta)
    Q = mu * mu * (1.0 - phi * phi)
    R = N / Delta
    b = R * (1.0 - phi * phi) - Q                      # discrete algebraic Riccati for the prior variance M:
    M = 0.5 * (-b + math.sqrt(b * b + 4.0 * Q * R))    #   M^2 + b M - Q R = 0
    K = M / (M + R)
    z = (1.0 - K) * phi
    return {"phi": phi, "Q": Q, "R": R, "M_prior": M, "P_post": (1 - K) * M, "K": K, "pole": z}


def linear_ta_grid(mu, lam, N, Delta):
    """Memory time on the grid from the closed form cosh(beta Delta) = cosh(a Delta) + rho sinh(a Delta)."""
    a = 2.0 * lam
    rho = mu * mu * Delta / N
    cm1 = 2.0 * math.sinh(0.5 * a * Delta) ** 2 + rho * math.sinh(a * Delta)   # cosh(beta Delta) - 1, no cancellation
    beta = 2.0 * math.asinh(math.sqrt(0.5 * cm1)) / Delta
    return 1.0 / beta


def linear_ta_cont(mu, lam, N):
    a = 2.0 * lam
    return 1.0 / math.sqrt(a * a + 2.0 * a * mu * mu / N)


# ---------------------------------------------------------------- Bayes tracker, continuous time
def bayes_ta_plugin(mu, lam, N):
    """N16 plug-in (kappa -> 0 asymptote)."""
    th = N / (mu * mu)
    return 0.5 * th * (math.log(2.0 / (lam * th)) - EULER_GAMMA - 1.0)


def bayes_ta_cont(mu, lam, N, h=2e-3, law="switch"):
    """Exact continuous-time mean first passage (N16's definition, no small-kappa approximation).

    theta = N/mu^2 units: after the switch dL = (-2 - 2 kappa sinh L) dt + 2 dW, kappa = lam theta.  Mean passage from
    y: T(y) = int_0^y g, g(y) = 1/2 int_y^inf exp(Phi(y) - Phi(z)) dz, Phi = L + kappa cosh L.  Stationary law of L
    given the pre-switch state: p(L|+) = (1 + e^L) exp(-kappa cosh L) / (2 (K0 + K1)).  E T = int_0^inf g(y) S(y) dy,
    S(y) = P(L > y | +).
    law='quiet': the no-switch resting law exp(L - kappa cosh L) / (2 K1) instead (the exact stationary law of a
    filter whose world has stayed at + forever; the law N16's derivation used).  The two differ by O(kappa ln kappa).
    """
    th = N / (mu * mu)
    kap = lam * th
    Lmax = math.acosh(max(1.0, (60.0 + 0.0) / kap)) + 2.0 if kap < 30 else 6.0
    Lmax = max(Lmax, 8.0)
    y = np.arange(0.0, Lmax + h / 2, h)
    Phi = y + kap * np.cosh(y)
    w = np.exp(-(Phi - Phi[0]))                       # e^{-Phi}, scaled
    # reverse cumulative trapezoid: G(y_i) = int_{y_i}^{Lmax} e^{-Phi}
    seg = 0.5 * (w[1:] + w[:-1]) * h
    G = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])
    g = 0.5 * G / w
    # S(y) = int_y^inf p(L|+) dL ; p unnormalised = (1+e^L) e^{-kappa cosh L}; normaliser 2(K0+K1)
    # use exponentially scaled Bessels: K_n(k) = k_n e(k) e^{-k}
    if law == "quiet":
        norm = 2.0 * k1e(kap) * math.exp(-kap)
        pu = np.exp(y - kap * np.cosh(y))
    else:
        norm = 2.0 * (k0e(kap) + k1e(kap)) * math.exp(-kap)
        pu = (1.0 + np.exp(y)) * np.exp(-kap * np.cosh(y))
    segp = 0.5 * (pu[1:] + pu[:-1]) * h
    S = np.concatenate([np.cumsum(segp[::-1])[::-1], [0.0]]) / norm
    f = g * S
    return float(th * np.sum(0.5 * (f[1:] + f[:-1]) * h))


# ---------------------------------------------------------------- Bayes tracker, sampled grid (exact chain solve)
def _predict(L, p):
    """Log-odds prediction through a flip with probability p (stable form)."""
    # f(L) = ln[((1-p) e^L + p) / (p e^L + (1-p))]
    return np.logaddexp(np.log1p(-p) + L, math.log(p)) - np.logaddexp(math.log(p) + L, np.log1p(-p))


def bayes_ta_grid(mu, lam, N, Delta, h=None, Lpad=8.0, return_detail=False, start=None):
    """Exact sampled-grid Bayes t_A (to lattice accuracy) by solving the filter's Markov chain on an L lattice.

    Lattice cells of width h with an edge at 0; transition = deterministic prediction to f(L_j) then the Gaussian
    increment 2 mu y / s2 ~ N(+-2 rho, 4 rho), integrated over each cell (mass at the ends is kept in the end cells).
    Stationary law of (L, x): by symmetry p_-(L) = p_+(-L), so p_+ = T_+ [(1-p) p_+ + p J p_+] (J = reflection);
    solved as a null vector.  Post-switch: E n = 1' (I - Q)^{-1} v0, Q = T_- restricted to L > 0, v0 = p_+ on L > 0.
    start: None = the stationary pre-switch law (a switch at a typical time; default); 'quiet' = the stationary law of
    the filter when the world has stayed at + forever (N16's derivation law; discrete analogue of exp(L - kappa cosh L));
    'resting' = the noiseless fixed point L* = f(L*) + 2 rho
    (a deterministic start, shown in the report to be what inflates AQN_REFEREE V8's larger-sigma values); or a float L0.
    """
    rho = mu * mu * Delta / N
    p = 0.5 * (1.0 - math.exp(-2.0 * lam * Delta))
    sd = 2.0 * math.sqrt(rho)
    if h is None:
        h = min(0.05, sd / 12.0)
    rest = math.log((1 - p) / p) + 2 * rho + 6 * sd   # above the saturation level of the prediction step
    Lmax = max(rest, math.log(2.0 / max(lam * N / mu**2, 1e-300))) + Lpad
    m = int(math.ceil(Lmax / h))
    edges = np.arange(-m, m + 1) * h
    c = 0.5 * (edges[1:] + edges[:-1])
    fL = _predict(c, p)
    z = (edges[:, None] - fL[None, :])                 # (n+1, n)

    def T(mean):
        F = ndtr((z - mean) / sd)
        F[0, :] = 0.0
        F[-1, :] = 1.0
        return np.diff(F, axis=0)                      # T[i, j] = P(next in cell i | now in cell j)

    Tp = T(2.0 * rho)
    n = len(c)
    J = np.eye(n)[::-1]
    A = Tp @ ((1 - p) * np.eye(n) + p * J) - np.eye(n)
    A[-1, :] = 1.0                                     # replace one equation by normalisation
    rhs = np.zeros(n); rhs[-1] = 1.0
    pp = np.linalg.solve(A, rhs)
    pp = np.clip(pp, 0, None); pp /= pp.sum()
    pos = c > 0
    Tm = T(-2.0 * rho)
    Qm = Tm[np.ix_(pos, pos)]
    v0 = pp[pos]
    if start == "quiet":
        Aq = Tp - np.eye(n); Aq[-1, :] = 1.0
        pq = np.clip(np.linalg.solve(Aq, rhs), 0, None); pq /= pq.sum()
        v0 = pq[pos]
    elif start is not None:
        L0 = resting_point(rho, p) if start == "resting" else float(start)
        v0 = np.zeros(pos.sum())
        if L0 > 0:
            cp = c[pos]; i = int(np.argmin(np.abs(cp - L0))); v0[i] = 1.0
    u = np.linalg.solve(np.eye(pos.sum()) - Qm, v0)    # expected occupation of each positive cell
    En = float(u.sum())
    if return_detail:
        return {"t_A": En * Delta, "E_steps": En, "rho": rho, "p_flip": p, "h": h, "cells": n,
                "start": start or "switch", "P_L0_le_0": float(1.0 - v0.sum())}
    return En * Delta


def resting_point(rho, p):
    """Noiseless fixed point of the pre-switch recursion L = f(L) + 2 rho (bisection)."""
    lo, hi = 0.0, 2 * rho + math.log((1 - p) / p) + 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if float(_predict(np.array([mid]), p)[0]) + 2 * rho > mid:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------- convenience: correction factors
C2_FIT = 0.25


def bayes_asymptotic(mu, lam, N, Delta, law="quiet", second_order=True):
    """T_cont + C1 sqrt(Delta N/mu^2) [+ 0.25 Delta]: grid correction without the lattice solve.
    With the Delta/4 term it is within 1.0% (quiet) / 1.5% (switch) of the lattice value for rho = mu^2 Delta/N <= 2
    (r = t_A/Delta >= about ell/4) over kappa 1e-6..3e-2
    (report section 3); it fails for coarse grids (rho > 2, fewer than ~2 samples per adaptation)."""
    t = bayes_ta_cont(mu, lam, N, law=law) + C1 * math.sqrt(Delta * N / (mu * mu))
    return t + (C2_FIT * Delta if second_order else 0.0)


def table(kappas=(1e-2, 1e-3, 1e-4), ratios=(1, 2, 5, 10, 20, 50, 100), law="quiet"):
    """Correction factors t_A_grid / plug-in and t_A_grid / T_cont per kappa and r = plug-in / Delta (theta = 1)."""
    rows = []
    start = "quiet" if law == "quiet" else None
    for kap in kappas:
        tp = bayes_ta_plugin(1.0, kap, 1.0)
        tc = bayes_ta_cont(1.0, kap, 1.0, law=law)
        for r in ratios:
            D = tp / r
            tg = bayes_ta_grid(1.0, kap, 1.0, D, start=start)
            rows.append({"kappa": kap, "law": law, "r_plugin": r, "Delta": D, "plugin": tp, "T_cont": tc, "grid": tg,
                         "grid_over_plugin": tg / tp, "grid_over_cont": tg / tc,
                         "approx_over_cont": bayes_asymptotic(1, kap, 1, D, law=law) / tc,
                         "linear_grid_over_cont": linear_ta_grid(1, kap, 1, D) / linear_ta_cont(1, kap, 1)})
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("linear", "bayes"):
        s = sub.add_parser(name)
        s.add_argument("--mu", type=float, default=1.0); s.add_argument("--lam", type=float, required=True)
        s.add_argument("--N", type=float, required=True); s.add_argument("--Delta", type=float, required=True)
        if name == "bayes":
            s.add_argument("--h", type=float, default=None)
            s.add_argument("--law", choices=["quiet", "switch"], default="quiet")
    t = sub.add_parser("table"); t.add_argument("--law", choices=["quiet", "switch"], default="quiet")
    a = ap.parse_args(argv)
    if a.cmd == "linear":
        tg, tc = linear_ta_grid(a.mu, a.lam, a.N, a.Delta), linear_ta_cont(a.mu, a.lam, a.N)
        out = {"t_A_grid": tg, "t_A_cont": tc, "ratio": tg / tc, "steps": tg / a.Delta,
               **kalman_steady(a.mu, a.lam, a.N, a.Delta)}
    elif a.cmd == "bayes":
        d = bayes_ta_grid(a.mu, a.lam, a.N, a.Delta, h=a.h, return_detail=True,
                          start="quiet" if a.law == "quiet" else None)
        tp, tc = bayes_ta_plugin(a.mu, a.lam, a.N), bayes_ta_cont(a.mu, a.lam, a.N, law=a.law)
        out = {**d, "law": a.law, "plugin": tp, "T_cont": tc,
               "approx": bayes_asymptotic(a.mu, a.lam, a.N, a.Delta, law=a.law),
               "grid_over_plugin": d["t_A"] / tp, "grid_over_cont": d["t_A"] / tc, "plugin_steps": tp / a.Delta}
    else:
        out = table(law=a.law)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
