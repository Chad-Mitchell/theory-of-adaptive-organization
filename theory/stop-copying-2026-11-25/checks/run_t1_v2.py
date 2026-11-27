#!/usr/bin/env python3
"""T1 search v2 for theory/stop-copying-2026-11-25/PREREG_3.md. Not a paper check.

Supersedes checks/run_t1.py (untouched). Invoke only after an independent
reader passes the PREREG_3 Gate, and only with --execute, under the locked
shell command in PREREG_3 (thread-limit env vars set before the process starts).
Does nothing on import or when run without --execute.
"""
from __future__ import annotations

# Thread limits before numpy/scipy load, in case the process was not started
# under the locked shell command. The shell command is the binding rule.
import os
import sys

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"

import argparse
import json
import time

import numpy as np
from scipy.linalg import solve_continuous_lyapunov as lyap
from scipy.optimize import minimize

import aggregate as agg

D = 1.0
SETTINGS = [(10, 0.5), (10, 1), (10, 2), (3, 1), (30, 1)]
BOUNDS = [(-3, 5), (0, 0.999), (-3, 5), (0, 0.999)]
SEED = 20261125
N_UNIFORM = 256
STRUCTURED = [
    (5.0, 0.0, 5.0, 0.7),
    (5.0, 0.0, 3.0, 0.9),
    (5.0, 0.0, 1.0, 0.9),
    (5.0, 0.0, 0.0, 0.5),
]
FTOL, GTOL, MAXITER = 1e-12, 1e-8, 5000
# 4 design coordinates: a finite-difference gradient is 5 evaluations, so
# maxfun=25000 is consistent with maxiter 5000. Worst case at the probe timing
# (~0.065 ms/eval, 260 starts) is about 7 CPU-min, under the 12-min cap.
MAXFUN = 25000
UNSTABLE = 1e9
CPU_CAP_SEC = 12 * 60
TOTAL_CAP_SEC = 2 * 3600
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
        return None, kA, kB, ev
    return abs(kA - kB) / s, kA, kB, ev


def classify_A(A):
    if A is None:
        return "clean miss (no copying)"
    if abs(A - BAR) <= RES:
        return "inside-resolution"
    if A > BAR + RES:
        return "hit"
    return "clean miss"


def a_value(A):
    return 0.0 if A is None else A


def close_to_best(j, best):
    """PREREG_3 B3: relative window 1e-6 * abs(best)."""
    return abs(j - best) <= REL_BEST * abs(best)


def pairwise_A_agree(As):
    """Every pair of scalar A values agrees within A_AGREE."""
    vals = [a_value(a) for a in As]
    return all(abs(a - b) <= A_AGREE for i, a in enumerate(vals) for b in vals[i + 1 :])


def stopped_on_limit(r):
    return (
        int(getattr(r, "status", 0)) == 1
        or int(getattr(r, "nfev", 0)) >= MAXFUN
        or int(getattr(r, "nit", 0)) >= MAXITER
    )


def draw_stable(rng):
    for _ in range(10000):
        v = np.array(
            [
                rng.uniform(-3, 5),
                rng.uniform(0, 0.999),
                rng.uniform(-3, 5),
                rng.uniform(0, 0.999),
            ]
        )
        if _stable(*v)[0]:
            return v
    raise RuntimeError("could not draw a stable start")


def run_setting(w, wx, setting_cap, remaining_total):
    cap = min(setting_cap, remaining_total)
    t0 = time.process_time()

    def used():
        return time.process_time() - t0

    started = False
    results = []
    over = False
    if cap <= 0:
        flags = {"not_run_budget": True, "classification": None}
        return {
            "label": agg.setting_label(flags),
            "flags": flags,
            "cpu": 0.0,
            "n_done": 0,
            "started": False,
            "note": "not run (budget): no remaining CPU",
        }

    # Re-seeded per setting, so all five settings draw the same uniform starts
    # (PREREG_3 N1). This is the PREREG §3 seed, applied once per setting.
    rng = np.random.default_rng(SEED)
    starts = [draw_stable(rng) for _ in range(N_UNIFORM)]
    starts.extend(np.array(s, dtype=float) for s in STRUCTURED)

    opts = {"ftol": FTOL, "gtol": GTOL, "maxiter": MAXITER, "maxfun": MAXFUN}
    for i, x0 in enumerate(starts):
        if used() >= cap:
            over = True
            break
        started = True
        r = minimize(lambda v: Jtot(v, w, wx), x0, method="L-BFGS-B", bounds=BOUNDS, options=opts)
        results.append(
            {
                "i": i,
                "J": float(r.fun),
                "x": np.array(r.x, dtype=float),
                "status": int(r.status),
                "nit": int(r.nit),
                "nfev": int(getattr(r, "nfev", 0)),
                "message": str(r.message),
                "stopped_on_maxfun_or_maxiter": stopped_on_limit(r),
            }
        )

    usable = [s for s in results if not s["stopped_on_maxfun_or_maxiter"]]
    not_settled = False
    note = None
    close = []
    best_J = None
    if over or used() >= cap:
        not_settled = True
        note = "over CPU cap"
    if not usable:
        not_settled = True
        note = (note + "; " if note else "") + "no converged starts"
    else:
        best_J = min(s["J"] for s in usable)
        close = [s for s in usable if close_to_best(s["J"], best_J)]
        if len(close) < 3:
            not_settled = True
            note = (note + "; " if note else "") + "fewer than 3 converged starts at the best value"
        else:
            As = [copy_index(s["x"])[0] for s in close]
            if not pairwise_A_agree(As):
                not_settled = True
                note = (note + "; " if note else "") + "starts at the best value disagree on A by more than 0.01"

    # Flags on the lowest-J start among finished starts (any status), for
    # guard and half-tolerance; representative design from close converged
    # starts when available.
    all_finished = results
    lowest = min(all_finished, key=lambda s: (s["J"], s["i"])) if all_finished else None
    rep = min(close, key=lambda s: (s["J"], s["i"])) if close else lowest

    measurement_code = False
    A_half = None
    if rep is not None and used() < cap:
        x0_best = starts[rep["i"]]
        r2 = minimize(
            lambda v: Jtot(v, w, wx),
            x0_best,
            method="L-BFGS-B",
            bounds=BOUNDS,
            options={"ftol": FTOL / 2, "gtol": GTOL / 2, "maxiter": MAXITER, "maxfun": MAXFUN},
        )
        A2, *_ = copy_index(r2.x)
        A_half = A2
        A_rep = copy_index(rep["x"])[0]
        if abs(a_value(A_rep) - a_value(A2)) > TOL_A_MOVE:
            measurement_code = True
    elif rep is not None and used() >= cap:
        not_settled = True
        note = (note + "; " if note else "") + "no CPU left for the half-tolerance rerun"

    guard_hit = False
    A = kA = kB = leader_c = min_re = None
    classification = "clean miss"
    if rep is not None:
        A, kA, kB, ev = copy_index(rep["x"])
        min_re = float(np.min(ev.real)) if ev is not None else 0.0
        x = rep["x"]
        if any(abs(c - 0.999) <= GUARD_C for c in (x[1], x[3])) or min_re < GUARD_EIG:
            guard_hit = True
        classification = classify_A(A)
        if kA is not None and kB is not None:
            leader_c = float(x[1] if kA <= kB else x[3])

    flags = {
        "measurement_code": measurement_code,
        "guard_hit": guard_hit,
        "not_settled": not_settled,
        "not_run_budget": (not started),
        "classification": classification,
    }
    label = agg.setting_label(flags)
    cpu = used()
    return {
        "label": label,
        "flags": flags,
        "cpu": cpu,
        "n_done": len(results),
        "n_usable": len(usable),
        "n_close": len(close),
        "started": started,
        "best_J": best_J,
        "x": None if rep is None else rep["x"].tolist(),
        "A": A,
        "kA": None if kA is None else float(kA),
        "kB": None if kB is None else float(kB),
        "leader_c": leader_c,
        "min_re": min_re,
        "A_half_tol": A_half,
        "note": note,
        "starts_status": [
            {k: s[k] for k in ("i", "J", "status", "nit", "nfev", "stopped_on_maxfun_or_maxiter", "message")}
            for s in results
        ],
    }


def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument(
        "--execute",
        action="store_true",
        help="required; refuse to run the search without this flag",
    )
    args = p.parse_args(argv)
    if not args.execute:
        print(
            "run_t1_v2.py: refusing to run (pass --execute after the PREREG_3 Gate passes).",
            file=sys.stderr,
        )
        return 2
    print("# T1 v2 run under PREREG_3; OMP/OPENBLAS/MKL_NUM_THREADS=1; CPU via time.process_time()")
    print(f"# maxiter={MAXITER} maxfun={MAXFUN} relative-best={REL_BEST}*abs(best)")
    total = 0.0
    remaining = TOTAL_CAP_SEC
    for w, wx in SETTINGS:
        row = run_setting(w, wx, CPU_CAP_SEC, remaining)
        row["w"] = w
        row["wx"] = wx
        total += row["cpu"]
        remaining = TOTAL_CAP_SEC - total
        # compact print: drop the bulky per-start list from the log line
        public = {k: v for k, v in row.items() if k != "starts_status"}
        public["n_status_rows"] = len(row.get("starts_status") or [])
        print("SETTING_JSON: " + json.dumps(public, default=str))
        # keep the statuses, one compact line, so the record is complete
        print("STARTS_STATUS_JSON: " + json.dumps({"w": w, "wx": wx, "starts": row.get("starts_status") or []}, default=str))
        sys.stdout.flush()
    print("TOTAL_JSON: " + json.dumps({"total_cpu": total, "settings": 5, "total_cap": TOTAL_CAP_SEC}))
    print("# end T1 v2")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
