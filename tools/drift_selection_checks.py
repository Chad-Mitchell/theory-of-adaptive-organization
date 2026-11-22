#!/usr/bin/env python3
"""Numerical checks for theory/DRIFT_SELECTION.md (DS1-DS3).

NUMERICAL: these checks are not the proofs. They (1) check the closed-form
trace formula of DS1 against a direct Lyapunov solve, and (2) simulate the
weak-mutation (origination-fixation) chain of a haploid Moran population
on a uniform integer lattice, with exact Moran fixation probabilities and
exact quadratic Delta J under the log-linear map r = exp(-alpha J), against
an optimum that moves (Brownian, Ornstein-Uhlenbeck, or constant speed),
and compare the measured time-averaged excess with the DS1 formula. The
time step is tau-leaping: at most one substitution per dt, with probability
1 - exp(-R dt). They also check the DS2 speed limit (an optimum faster
than v_max = N mu delta/(2d) outruns the chain) and record where the DS1
formula stops matching (DS3).

Units: lattice spacing delta = 1, mutation probability per birth mu = 1 per
unit time (time is measured in units of 1/mu generations), so the neutral
substitution rate is 1 and the per-coordinate mutational diffusion
coefficient is D_m = mu delta^2 / (2 d) = 1 / (2 d). J* = 0, so J is the
absolute excess.

Run from the repo root:

    nice -n 19 python3 tools/drift_selection_checks.py          # quick (pytest)
    nice -n 19 python3 tools/drift_selection_checks.py --full   # documented run

Exit 0 and the line ALL DS CHECKS PASS means every check held.
--full also writes theory/drift_selection_checks/results_full.json.
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
from scipy.linalg import solve_continuous_lyapunov

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------- formulas
def ds1_excess(beta, Dm, H, Q, gamma=0.0):
    """DS1: d/(2 beta) + 1/2 Tr[H (Dm beta H + gamma I)^{-1} Q]."""
    H = np.atleast_2d(np.asarray(H, float))
    Q = np.atleast_2d(np.asarray(Q, float))
    d = H.shape[0]
    A = Dm * beta * H + gamma * np.eye(d)
    return d / (2.0 * beta) + 0.5 * float(np.trace(H @ np.linalg.solve(A, Q)))


def ds1_velocity_excess(beta, Dm, H, v):
    """DS1(c): d/(2 beta) + v^T H^{-1} v / (2 beta^2 Dm^2)."""
    H = np.atleast_2d(np.asarray(H, float))
    v = np.atleast_1d(np.asarray(v, float))
    d = H.shape[0]
    return d / (2.0 * beta) + float(v @ np.linalg.solve(H, v)) / (2.0 * beta**2 * Dm**2)


def lyapunov_excess(beta, M, H, Q, gamma):
    """Direct solve of the joint stationary covariance of (L, theta*) for
    dtheta = -beta M H (theta - theta*) dt + sqrt(2M) dW,
    dtheta* = -gamma theta* dt + sqrt(2Q) dB. Returns E[1/2 L^T H L]."""
    H = np.asarray(H, float); Q = np.asarray(Q, float); M = np.asarray(M, float)
    d = H.shape[0]
    # state z = (theta, theta*)
    F = np.zeros((2 * d, 2 * d))
    F[:d, :d] = -beta * M @ H
    F[:d, d:] = beta * M @ H
    F[d:, d:] = -gamma * np.eye(d)
    G = np.zeros((2 * d, 2 * d))
    G[:d, :d] = 2 * M
    G[d:, d:] = 2 * Q
    if gamma == 0.0:
        # theta* is not stationary; work with L = theta - theta* directly
        A = beta * M @ H
        P = solve_continuous_lyapunov(-A, -(2 * M + 2 * Q))
        return 0.5 * float(np.trace(H @ P))
    S = solve_continuous_lyapunov(F, -G)
    T = np.hstack([np.eye(d), -np.eye(d)])
    P = T @ S @ T.T
    return 0.5 * float(np.trace(H @ P))


# ---------------------------------------------------------------- Moran
def moran_phi(x, N):
    """Haploid Moran fixation probability of a single mutant whose cost is
    higher by Delta J, with x = alpha Delta J: (1 - e^x)/(1 - e^{N x})."""
    x = np.asarray(x, float)
    out = np.empty_like(x)
    small = np.abs(x) < 1e-12
    pos = (x > 0) & ~small
    neg = (x < 0) & ~small
    out[small] = 1.0 / N
    xp = x[pos]
    out[pos] = np.exp(-(N - 1) * xp) * (-np.expm1(-xp)) / (-np.expm1(-N * xp))
    xn = x[neg]
    out[neg] = np.expm1(xn) / np.expm1(N * xn)
    return out


def simulate(N, alpha, H, mode, D=0.0, gamma=0.0, v=None, reps=400, T=2000.0,
             burn=400.0, dt=0.05, seed=0, record_lag=False):
    """Weak-mutation origination-fixation chain on Z^d (delta = 1, mu = 1)
    with a moving optimum. The fixation probability and the quadratic Delta J
    are exact Moran; the time step is tau-leaping (at most one substitution
    per dt, with probability 1 - exp(-R dt)). Returns time- and
    replicate-averaged J after burn (J* = 0), its standard error over
    replicates, and optionally the mean lag path."""
    rng = np.random.default_rng(seed)
    H = np.atleast_2d(np.asarray(H, float))
    d = H.shape[0]
    beta = alpha * (N - 1)
    # start in the stationary static law around 0, rounded to the lattice
    tstar = np.zeros((reps, d))
    x = np.round(rng.normal(size=(reps, d)) / np.sqrt(beta * np.diag(H)))
    steps = int(round(T / dt))
    nburn = int(round(burn / dt))
    acc = np.zeros(reps)
    nacc = 0
    E = np.vstack([np.eye(d), -np.eye(d)])           # 2d neighbour moves
    lag_path = []
    if mode == "ou":
        ou_a = math.exp(-gamma * dt)
        ou_s = math.sqrt(D / gamma * (1 - ou_a**2)) if gamma > 0 else 0.0
    for s in range(steps):
        L = x - tstar                                   # reps x d
        HL = L @ H                                      # reps x d (H symmetric)
        J0 = 0.5 * np.einsum("ij,ij->i", L, HL)
        # Delta J for each move e: e^T H L + 1/2 e^T H e
        dJ = HL @ E.T + 0.5 * np.einsum("kj,jl,kl->k", E, H, E)[None, :]
        rates = (N / (2.0 * d)) * moran_phi(alpha * dJ, N)   # reps x 2d
        R = rates.sum(axis=1)
        jump = rng.random(reps) < -np.expm1(-R * dt)
        if jump.any():
            cum = np.cumsum(rates[jump], axis=1)
            u = rng.random(jump.sum()) * cum[:, -1]
            k = (cum < u[:, None]).sum(axis=1)
            x[jump] += E[k]
        if s >= nburn:
            acc += J0
            nacc += 1
        if record_lag and s % 100 == 0:
            lag_path.append((s * dt, float(np.mean(tstar[:, 0] - x[:, 0]))))
        # move the optimum
        if mode == "bm":
            tstar += math.sqrt(2 * D * dt) * rng.normal(size=(reps, d))
        elif mode == "ou":
            tstar = tstar * ou_a + ou_s * rng.normal(size=(reps, d))
        elif mode == "vel":
            tstar += np.asarray(v, float)[None, :] * dt
    per_rep = acc / max(nacc, 1)
    out = {"mean": float(per_rep.mean()), "se": float(per_rep.std(ddof=1) / math.sqrt(reps))}
    if record_lag:
        out["lag_path"] = lag_path
    return out


# ---------------------------------------------------------------- checks
def check(ok, lines, name, cond, msg=""):
    ok.append((name, bool(cond)))
    lines.append("%s: %s%s" % (name, "OK" if cond else "FAIL", ("  " + msg) if msg else ""))


def analytic_checks(ok, lines):
    rng = np.random.default_rng(1)
    for trial in range(5):
        d = 3
        A = rng.normal(size=(d, d)); H = A @ A.T + 0.5 * np.eye(d)
        B = rng.normal(size=(d, d)); Q = B @ B.T * 0.3
        beta, Dm = 2.5, 0.7
        for gamma in (0.0, 0.3, 4.0):
            f = ds1_excess(beta, Dm, H, Q, gamma)
            g = lyapunov_excess(beta, Dm * np.eye(d), H, Q, gamma)
            check(ok, lines, "DS1 trace formula = Lyapunov (trial %d, gamma %.1f)" % (trial, gamma),
                  abs(f - g) < 1e-9 * max(1, abs(g)), "formula %.10f lyapunov %.10f" % (f, g))
        # anisotropic mutation matrix M, Brownian optimum: d/(2b) + Tr(M^-1 Q)/(2b)
        C = rng.normal(size=(d, d)); M = C @ C.T + 0.2 * np.eye(d)
        f = d / (2 * beta) + float(np.trace(np.linalg.solve(M, Q))) / (2 * beta)
        g = lyapunov_excess(beta, M, H, Q, 0.0)
        check(ok, lines, "DS1 anisotropic M (trial %d)" % trial, abs(f - g) < 1e-9 * max(1, abs(g)),
              "formula %.10f lyapunov %.10f" % (f, g))
    # limits
    H = np.diag([1.0, 3.0]); Q = 0.4 * np.eye(2); beta, Dm = 2.0, 0.5
    fast = ds1_excess(beta, Dm, H, Q, 1e7) - 2 / (2 * beta)
    check(ok, lines, "DS1 fast-world limit -> 1/2 Tr(H Q/gamma)", abs(fast - 0.5 * np.trace(H @ Q) / 1e7) < 1e-12)
    check(ok, lines, "DS1 Brownian: curvature cancels",
          abs(ds1_excess(beta, Dm, H, Q) - ds1_excess(beta, Dm, 7 * np.eye(2), Q)) < 1e-12)
    # Moran phi sanity: phi(-x) = e^{(N-1)x} phi(x); phi(0)=1/N
    N = 50; xs = np.array([1e-4, 0.01, 0.1, 0.5])
    lhs = moran_phi(-xs, N); rhs = np.exp((N - 1) * xs) * moran_phi(xs, N)
    check(ok, lines, "Moran phi(-x) = e^{(N-1)x} phi(x)", np.allclose(lhs, rhs, rtol=1e-9))
    check(ok, lines, "Moran phi(0) = 1/N", abs(moran_phi(np.array([0.0]), N)[0] - 1 / N) < 1e-15)


def sim_case(ok, lines, results, name, N, alpha, H, mode, pred, tol, **kw):
    r = simulate(N, alpha, H, mode, **kw)
    rel = (r["mean"] - pred) / pred
    cond = abs(rel) <= tol if tol is not None else True
    tag = "within %.0f%%" % (100 * tol) if tol is not None else "REPORTED ONLY (outside DS1 conditions)"
    check(ok, lines, name, cond, "sim %.2f +/- %.2f  formula %.2f  rel %+.3f  [%s]" % (r["mean"], r["se"], pred, rel, tag))
    results.append({"case": name, "sim_mean": r["mean"], "sim_se": r["se"], "formula": pred,
                    "rel_err": rel, "tol": tol, **{k: (v if not isinstance(v, np.ndarray) else v.tolist())
                                                   for k, v in kw.items() if k in ("D", "gamma", "v", "reps", "T", "burn", "dt")}})
    return r


def sim_checks(ok, lines, full):
    results = []
    reps = 1500 if full else 300
    T, burn = (4000.0, 600.0) if full else (1500.0, 400.0)
    tol = 0.08 if full else 0.15
    # 1-D, N = 100, beta h = 0.02 (stationary width ~7 lattice units)
    N, h = 100, 1.0
    beta = 0.02; alpha = beta / (N - 1); Dm = 0.5
    H1 = np.array([[h]])
    for ratio in ([0.0, 0.5, 1.0, 2.0, 5.0] if full else [0.0, 2.0]):
        D = ratio * Dm
        eps = beta * h * (1 + ratio)
        pred = ds1_excess(beta, Dm, H1, np.array([[D]]))
        sim_case(ok, lines, results, "BM d=1 D/Dm=%.1f (eps_lat=%.2f)" % (ratio, eps), N, alpha, H1, "bm",
                 pred, tol, D=D, reps=reps, T=T, burn=burn, seed=int(10 + 10 * ratio))
    # time-step check: the dt = 0.05 runs above carry a small positive bias
    # (a few standard errors at D/Dm = 5); dt = 0.01 removes it
    if full:
        pred = ds1_excess(beta, Dm, H1, np.array([[5.0 * Dm]]))
        sim_case(ok, lines, results, "BM d=1 D/Dm=5.0 dt=0.01 (time-step check)", N, alpha, H1, "bm",
                 pred, 0.03, D=5.0 * Dm, reps=reps, T=T, burn=burn, dt=0.01, seed=77)
    # 2-D, anisotropic H; Dm = 1/4; curvature should cancel
    H2 = np.diag([1.0, 3.0]); Dm2 = 0.25
    for ratio in ([0.0, 2.0] if full else [2.0]):
        D = ratio * Dm2
        pred = ds1_excess(beta, Dm2, H2, D * np.eye(2))
        sim_case(ok, lines, results, "BM d=2 H=diag(1,3) D/Dm=%.1f" % ratio, N, alpha, H2, "bm",
                 pred, tol, D=D, reps=reps, T=T * 1.5, burn=burn * 2, seed=int(200 + ratio))
    # OU optimum, 1-D, D = Dm
    if full:
        for gamma in (0.001, 0.01, 0.1):
            pred = ds1_excess(beta, Dm, H1, np.array([[Dm]]), gamma)
            sim_case(ok, lines, results, "OU d=1 D=Dm gamma=%.3f (chain rate a=%.3f)" % (gamma, Dm * beta * h),
                     N, alpha, H1, "ou", pred, tol, D=Dm, gamma=gamma, reps=reps, T=T, burn=burn, seed=int(300 + 1000 * gamma))
    # constant speed, linear regime v << mu delta/(2d) = 0.5
    for v in ([0.05, 0.1, 0.2] if full else [0.05]):
        pred = ds1_velocity_excess(beta, Dm, H1, [v])
        Nx = beta * v / (Dm * beta * h)  # N alpha h |L| with L = v/(Dm beta h)
        # the DS1 velocity formula is claimed only for N x << 1; report 0.2 only
        t = tol if Nx <= 0.11 else None
        sim_case(ok, lines, results, "velocity d=1 v=%.2f (N x=%.2f)" % (v, Nx), N, alpha, H1, "vel",
                 pred, t, v=np.array([v]), reps=reps, T=T, burn=burn, seed=int(400 + 100 * v))
    # outside the fine-lattice condition: reported, not claimed
    if full:
        for ratio in (20.0, 50.0):
            D = ratio * Dm
            pred = ds1_excess(beta, Dm, H1, np.array([[D]]))
            sim_case(ok, lines, results, "BM d=1 D/Dm=%.0f (eps_lat=%.2f)" % (ratio, beta * h * (1 + ratio)),
                     N, alpha, H1, "bm", pred, None, D=D, reps=reps // 2, T=T, burn=burn, dt=0.02, seed=int(500 + ratio))
    return results


def speed_limit_checks(ok, lines, full):
    """DS2: per-coordinate chain speed < v_max = N mu delta/(2d). Coarse lattice, N=20, alpha h=0.05."""
    N, d = 20, 1
    alpha, h = 0.05, 1.0
    vmax = N / (2.0 * d)
    reps = 400 if full else 120
    T = 300.0 if full else 120.0
    out = {}
    for v in (5.0, 12.0):
        r = simulate(N, alpha, np.array([[h]]), "vel", v=np.array([v]), reps=reps, T=T, burn=T / 2,
                     dt=0.004, seed=int(600 + v), record_lag=True)
        path = np.array(r["lag_path"])
        half = path[path[:, 0] >= T / 2]
        slope = float(np.polyfit(half[:, 0], half[:, 1], 1)[0])
        lag_end = float(path[-1, 1])
        out[v] = {"lag_slope_second_half": slope, "mean_lag_at_end": lag_end, "T": T}
        if v > vmax:
            lb = (v - vmax)
            check(ok, lines, "DS2 v=%.0f > v_max=%.0f: lag grows at >= v - v_max" % (v, vmax), slope >= 0.95 * lb,
                  "measured lag slope %.3f, bound %.3f, mean lag at T %.1f >= %.1f" % (slope, lb, lag_end, lb * T))
        else:
            # stationary lag: slope near zero compared with v
            check(ok, lines, "DS2 v=%.0f < v_max=%.0f: lag stationary" % (v, vmax), abs(slope) < 0.05 * v,
                  "lag slope %.4f, mean lag %.1f" % (slope, lag_end))
    return out


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    full = "--full" in argv
    ok, lines = [], []
    analytic_checks(ok, lines)
    results = sim_checks(ok, lines, full)
    sl = speed_limit_checks(ok, lines, full)
    print("\n".join(lines))
    if full:
        os.makedirs(os.path.join(ROOT, "theory", "drift_selection_checks"), exist_ok=True)
        with open(os.path.join(ROOT, "theory", "drift_selection_checks", "results_full.json"), "w") as fh:
            json.dump({"sim": results, "speed_limit": {str(k): v for k, v in sl.items()}}, fh, indent=1)
    if all(c for _, c in ok):
        print("ALL DS CHECKS PASS")
        return 0
    print("SOME DS CHECKS FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
