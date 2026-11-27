#!/usr/bin/env python3
"""T1 search for theory/stop-copying-2026-11-25/PREREG_2.md. Not a paper check.

Invoke only after an independent reader passes the PREREG_2 Gate, and only with
--execute. This file is hash-locked in PREREG_2.md; do not edit it after that lock.
Does nothing on import or when run without --execute.
"""
from __future__ import annotations

import argparse
import os
import sys
import time

import numpy as np
from scipy.linalg import solve_continuous_lyapunov as lyap
from scipy.optimize import minimize

D = 1.0
SETTINGS = [(10, 0.5), (10, 1), (10, 2), (3, 1), (30, 1)]
BOUNDS = [(-3, 5), (0, 0.999), (-3, 5), (0, 0.999)]
SEED = 20261125
N_UNIFORM = 256
STRUCTURED = [(5.0, 0.0, 5.0, 0.7), (5.0, 0.0, 3.0, 0.9), (5.0, 0.0, 1.0, 0.9), (5.0, 0.0, 0.0, 0.5)]
FTOL, GTOL, MAXITER = 1e-12, 1e-8, 5000
UNSTABLE = 1e9
CPU_CAP_SEC = 12 * 60
REL_BEST = 1e-6
A_AGREE = 0.01
TOL_A_MOVE = 0.005
GUARD_C = 1e-3
GUARD_EIG = 1e-3
K_SUM_MIN = 1e-6
BAR = 0.10
RES = 0.02


def _stable(lgA, cA, lgB, cB):
    gA, gB = np.exp(lgA), np.exp(lgB)
    A = np.array([[gA, -gA * cA], [-gB * cB, gB]])
    ev = np.linalg.eigvals(A)
    return bool(np.all(ev.real > 0)), ev, A, gA, gB


def Jtot(v, w, wx):
    ok, ev, A, gA, gB = _stable(*v)
    if not ok:
        return UNSTABLE
    S = lyap(-A, -np.diag([2 * D, 2 * D]))
    cA, cB = v[1], v[3]
    L = S[0, 0] - 2 * S[0, 1] + S[1, 1]
    QA = gA ** 2 * (S[0, 0] - 2 * cA * S[0, 1] + cA ** 2 * S[1, 1]) - D * gA
    QB = gB ** 2 * (S[1, 1] - 2 * cB * S[0, 1] + cB ** 2 * S[0, 0]) - D * gB
    return float(QA + QB + 2 * w * L + wx * (S[0, 0] + S[1, 1]))


def copy_index(v):
    ok, ev, A, gA, gB = _stable(*v)
    if not ok:
        return None, None, None, ev
    kA, kB = gA * v[1], gB * v[3]
    s = kA + kB
    if s < K_SUM_MIN:
        return None, kA, kB, ev  # no copying
    return abs(kA - kB) / s, kA, kB, ev


def classify_A(A):
    if A is None:
        return "clean miss (no copying)"
    if abs(A - BAR) <= RES:
        return "inside-resolution"
    if A > BAR:
        return "hit"
    return "clean miss"


def draw_stable(rng):
    for _ in range(10000):
        v = np.array([
            rng.uniform(-3, 5), rng.uniform(0, 0.999),
            rng.uniform(-3, 5), rng.uniform(0, 0.999),
        ])
        if _stable(*v)[0]:
            return v
    raise RuntimeError("could not draw a stable start")


def run_setting(w, wx, cpu_budget):
    os.environ["OMP_NUM_THREADS"] = "1"
    t0 = time.process_time()
    rng = np.random.default_rng(SEED)
    starts = [draw_stable(rng) for _ in range(N_UNIFORM)]
    starts.extend(np.array(s, dtype=float) for s in STRUCTURED)
    results = []
    over = False
    for i, x0 in enumerate(starts):
        if time.process_time() - t0 >= cpu_budget:
            over = True
            break
        r = minimize(lambda v: Jtot(v, w, wx), x0, method="L-BFGS-B",
                      bounds=BOUNDS, options={"ftol": FTOL, "gtol": GTOL, "maxiter": MAXITER})
        results.append((float(r.fun), np.array(r.x, dtype=float), i))
    used = time.process_time() - t0
    if over or used >= cpu_budget:
        return {"label": "not settled", "cpu": used, "n_done": len(results), "note": "over CPU cap"}
    if not results:
        return {"label": "not settled", "cpu": used, "n_done": 0, "note": "no starts finished"}
    best_J = min(j for j, _, _ in results)
    close = [(j, x, i) for j, x, i in results if abs(j - best_J) <= REL_BEST * max(1.0, abs(best_J))]
    if len(close) < 3:
        return {"label": "not settled", "cpu": used, "n_done": len(results),
                "best_J": best_J, "n_close": len(close), "note": "fewer than 3 starts at the best value"}
    As = []
    for j, x, i in close:
        A, kA, kB, ev = copy_index(x)
        As.append((A, kA, kB, ev, x, j, i))
    # A is exchange-invariant; compare the defined values (None counts as 0 for agreement)
    aval = [0.0 if a is None else a for a, *_ in As]
    if max(aval) - min(aval) > A_AGREE:
        return {"label": "not settled", "cpu": used, "n_done": len(results),
                "best_J": best_J, "n_close": len(close), "A_range": (min(aval), max(aval)),
                "note": "starts at the best value disagree on A by more than 0.01"}
    # representative: lowest J, then lowest start index
    A, kA, kB, ev, x, j, i = min(As, key=lambda t: (t[5], t[6]))
    # tolerance check on the best start (the one that produced this x)
    x0_best = starts[i]
    r2 = minimize(lambda v: Jtot(v, w, wx), x0_best, method="L-BFGS-B",
                   bounds=BOUNDS, options={"ftol": FTOL / 2, "gtol": GTOL / 2, "maxiter": MAXITER})
    A2, *_ = copy_index(r2.x)
    a1 = 0.0 if A is None else A
    a2 = 0.0 if A2 is None else A2
    if abs(a1 - a2) > TOL_A_MOVE:
        return {"label": "measurement/code", "cpu": used, "n_done": len(results),
                "best_J": best_J, "x": x.tolist(), "A": A, "A_half_tol": A2,
                "note": "A moved by more than 0.005 at half tolerances"}
    min_re = float(np.min(ev.real)) if ev is not None else 0.0
    if any(abs(c - 0.999) <= GUARD_C for c in (x[1], x[3])) or min_re < GUARD_EIG:
        return {"label": "guard-hit", "cpu": used, "n_done": len(results),
                "best_J": best_J, "x": x.tolist(), "A": A, "min_re": min_re}
    lab = classify_A(A)
    leader_c = float(x[1] if kA <= kB else x[3]) if (kA is not None and kB is not None) else None
    return {"label": lab, "cpu": used, "n_done": len(results), "n_close": len(close),
            "best_J": best_J, "x": x.tolist(), "A": A, "kA": kA, "kB": kB,
            "leader_c": leader_c, "min_re": min_re, "A_half_tol": A2}


def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument("--execute", action="store_true",
                   help="required; refuse to run the search without this flag")
    args = p.parse_args(argv)
    if not args.execute:
        print("run_t1.py: refusing to run (pass --execute after the PREREG_2 Gate passes).", file=sys.stderr)
        return 2
    os.environ["OMP_NUM_THREADS"] = "1"
    print("# T1 run under PREREG_2; OMP_NUM_THREADS=1; CPU via time.process_time()")
    rows = []
    for w, wx in SETTINGS:
        row = run_setting(w, wx, CPU_CAP_SEC)
        row["w"] = w
        row["wx"] = wx
        rows.append(row)
        print(f"setting w={w} wx={wx}: {row}")
        sys.stdout.flush()
    print("# end T1")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
