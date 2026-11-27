#!/usr/bin/env python3
"""T2 search v2 for theory/stop-copying-2026-11-25/PREREG_3.md. Not a paper check.

Supersedes checks/run_t2.py (untouched). Invoke only after an independent
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

N = 8
D = 1.0
SETTINGS = [(10, 0.5), (10, 1), (10, 2), (3, 1), (30, 1)]
C_SYM = {
    (10, 0.5): 0.3351,
    (10, 1): 0.3161,
    (10, 2): 0.2879,
    (3, 1): 0.2603,
    (30, 1): 0.3426,
}
SEED_UNIF = 20261126
SEED_STR = 20261127
N_UNIFORM = 512
N_STRUCT_EACH = 16
FTOL, GTOL, MAXITER = 1e-12, 1e-8, 5000
# 24 design coordinates: a finite-difference gradient is 25 evaluations.
# maxfun consistent with maxiter 5000 would be 125000, which at the v2 probe
# timing (~0.122 ms/eval, 576 starts) would exceed the 12 CPU-minute cap.
# maxfun=8000 caps a start at about 1.0 CPU-s and a setting, if every start
# hits the cap, at about 9.4 CPU-min, leaving room for the half-tolerance
# rerun inside the 12-min cap.
MAXFUN = 8000
UNSTABLE = 1e9
CPU_CAP_SEC = 12 * 60
TOTAL_CAP_SEC = 2 * 3600
REL_BEST = 1e-6
A_AGREE = 0.01
ORIENT_AE = 0.02  # compare orientations only on edges with both A_e > this
TOL_A_MOVE = 0.005
GUARD_C = 1e-3
GUARD_EIG = 1e-3
K_SUM_MIN = 1e-6
BAR = 0.10
RES = 0.02
BROKEN = agg.BROKEN  # 0.12; single threshold everywhere (PREREG_3 B5)
BOUNDS = [(-3, 5)] * 8 + [(0, 0.999)] * 16
T1_TOTAL_PATHS = (
    os.path.join(os.path.dirname(__file__), "run_t1_v2.out"),
)


def unpack(v):
    v = np.asarray(v, dtype=float)
    return v[:8], v[8:16], v[16:24]


def pack(lg, cp, cm):
    return np.concatenate([lg, cp, cm])


def build(lg, cp, cm):
    g = np.exp(lg)
    A = np.zeros((N, N))
    for i in range(N):
        A[i, i] = g[i]
        A[i, (i + 1) % N] -= g[i] * cp[i]
        A[i, (i - 1) % N] -= g[i] * cm[i]
    ev = np.linalg.eigvals(A)
    return A, g, ev


def _stable(v):
    A, g, ev = build(*unpack(v))
    return bool(np.all(ev.real > 0)), ev, A, g


def Jtot(v, w, wx):
    ok, ev, A, g = _stable(v)
    if not ok:
        return UNSTABLE
    lg, cp, cm = unpack(v)
    S = lyap(-A, -2 * D * np.eye(N))
    J = 0.0
    for i in range(N):
        u = np.zeros(N)
        u[i] = 1
        u[(i + 1) % N] -= cp[i]
        u[(i - 1) % N] -= cm[i]
        Q = g[i] ** 2 * (u @ S @ u) - D * g[i]
        e1 = S[i, i] - 2 * S[i, (i + 1) % N] + S[(i + 1) % N, (i + 1) % N]
        e2 = S[i, i] - 2 * S[i, (i - 1) % N] + S[(i - 1) % N, (i - 1) % N]
        J += Q + w * 0.5 * (e1 + e2) + wx * S[i, i]
    return float(J)


def edge_A(v):
    ok, ev, A, g = _stable(v)
    lg, cp, cm = unpack(v)
    Aes, orients = [], []
    for i in range(N):
        k_to = g[i] * cp[i]
        k_from = g[(i + 1) % N] * cm[(i + 1) % N]
        s = k_to + k_from
        if s < K_SUM_MIN:
            Aes.append(None)
            orients.append(0)
        else:
            Aes.append(abs(k_to - k_from) / s)
            orients.append(int(np.sign(k_to - k_from)))
    return Aes, orients, ev


def a_num(A):
    return np.array([0.0 if a is None else a for a in A], dtype=float)


def a5(Aes):
    """Fifth-largest edge A_e, treating undefined (no copying) as 0."""
    vals = sorted((0.0 if a is None else a for a in Aes), reverse=True)
    return vals[4]


def classify_A5(val):
    if abs(val - BAR) <= RES:
        return "inside-resolution"
    if val > BAR + RES:
        return "hit"
    return "clean miss"


def apply_dihedral(Aes, orients, k, reflect):
    """Rotation by k edges, then optional reflection.

    A reflection reverses the edge cycle and flips orientation signs
    (edge i maps to edge -i-1 mod 8; k→ swaps with k←).
    """
    A = a_num(Aes)
    o = np.array(orients, dtype=int)
    if reflect:
        A = A[::-1]
        o = -o[::-1]
    return np.roll(A, k), np.roll(o, k)


def dihedral_match(Aes_a, orients_a, Aes_b, orients_b, orient_thresh=ORIENT_AE, a_tol=A_AGREE):
    """True if some 16-element dihedral maps b onto a.

    After the map: every A_e agrees within a_tol, and orientations agree
    only on edges where both A_e > orient_thresh (PREREG_3 B1).
    """
    Aa = a_num(Aes_a)
    oa = np.array(orients_a, dtype=int)
    for reflect in (False, True):
        for k in range(N):
            Ab, ob = apply_dihedral(Aes_b, orients_b, k, reflect)
            if np.any(np.abs(Aa - Ab) > a_tol):
                continue
            ok = True
            for i in range(N):
                if Aa[i] > orient_thresh and Ab[i] > orient_thresh and oa[i] != ob[i]:
                    ok = False
                    break
            if ok:
                return True
    return False


def pairwise_settled(records):
    """Every pair of (Aes, orients) among the starts at the best value matches."""
    for i, (Aa, oa) in enumerate(records):
        for Ab, ob in records[i + 1 :]:
            if not dihedral_match(Aa, oa, Ab, ob):
                return False
    return True


def close_to_best(j, best):
    return abs(j - best) <= REL_BEST * abs(best)


def stopped_on_limit(r):
    return (
        int(getattr(r, "status", 0)) == 1
        or int(getattr(r, "nfev", 0)) >= MAXFUN
        or int(getattr(r, "nit", 0)) >= MAXITER
    )


def draw_stable(rng):
    for _ in range(10000):
        v = pack(rng.uniform(-3, 5, N), rng.uniform(0, 0.999, N), rng.uniform(0, 0.999, N))
        if _stable(v)[0]:
            return v
    raise RuntimeError("could not draw a stable start")


def clip_box(v):
    lg, cp, cm = unpack(v)
    return pack(np.clip(lg, -3, 5), np.clip(cp, 0, 0.999), np.clip(cm, 0, 0.999))


def structured_starts(wx_key, rng):
    """16 starts near each of four patterns, perturbation U(-0.05, 0.05) per coordinate."""
    c = C_SYM[wx_key]
    lg = np.full(N, 5.0)
    patterns = []
    # uniform (reciprocal)
    patterns.append(pack(lg, np.full(N, c), np.full(N, c)))
    # circulation (all clockwise): c+_i = c, c-_i = 0
    patterns.append(pack(lg, np.full(N, c), np.zeros(N)))
    # acyclic chain with judge 0 a leader: judges 1..7 copy the previous only
    cp, cm = np.zeros(N), np.zeros(N)
    cm[1:] = c
    patterns.append(pack(lg, cp, cm))
    # alternating sources and sinks: even judges leaders (c=0), odd copy both neighbours
    cp, cm = np.zeros(N), np.zeros(N)
    for i in range(1, N, 2):
        cp[i] = c
        cm[i] = c
    patterns.append(pack(lg, cp, cm))
    out = []
    for base in patterns:
        for _ in range(N_STRUCT_EACH):
            pert = rng.uniform(-0.05, 0.05, 24)
            out.append(clip_box(base + pert))
    return out


def read_t1_cpu():
    for path in T1_TOTAL_PATHS:
        if not os.path.isfile(path):
            continue
        with open(path) as f:
            for line in f:
                if line.startswith("TOTAL_JSON:"):
                    return float(json.loads(line[len("TOTAL_JSON:"):].strip())["total_cpu"])
    return 0.0


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
            "circulation": False,
        }

    # Re-seeded per setting, so all five settings draw the same uniform starts
    # and the same structured-start perturbations (PREREG_3 N1).
    rng_u = np.random.default_rng(SEED_UNIF)
    rng_s = np.random.default_rng(SEED_STR)
    starts = [draw_stable(rng_u) for _ in range(N_UNIFORM)]
    starts.extend(structured_starts((w, wx), rng_s))

    opts = {"ftol": FTOL, "gtol": GTOL, "maxiter": MAXITER, "maxfun": MAXFUN}
    for i, x0 in enumerate(starts):
        if used() >= cap:
            over = True
            break
        started = True
        r = minimize(lambda v, w=w, wx=wx: Jtot(v, w, wx), x0, method="L-BFGS-B", bounds=BOUNDS, options=opts)
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
            recs = [edge_A(s["x"])[:2] for s in close]
            if not pairwise_settled(recs):
                not_settled = True
                note = (note + "; " if note else "") + (
                    "starts at the best value disagree on A_e "
                    "(no pairwise 16-element dihedral match within 0.01, "
                    "orientations compared only on edges with both A_e > 0.02)"
                )

    lowest = min(results, key=lambda s: (s["J"], s["i"])) if results else None
    rep = min(close, key=lambda s: (s["J"], s["i"])) if close else lowest

    measurement_code = False
    A5_half = None
    if rep is not None and used() < cap:
        x0_best = starts[rep["i"]]
        r2 = minimize(
            lambda v, w=w, wx=wx: Jtot(v, w, wx),
            x0_best,
            method="L-BFGS-B",
            bounds=BOUNDS,
            options={"ftol": FTOL / 2, "gtol": GTOL / 2, "maxiter": MAXITER, "maxfun": MAXFUN},
        )
        Aes2, _, _ = edge_A(r2.x)
        A5_half = a5(Aes2)
        if abs(a5(edge_A(rep["x"])[0]) - A5_half) > TOL_A_MOVE:
            measurement_code = True
    elif rep is not None and used() >= cap:
        not_settled = True
        note = (note + "; " if note else "") + "no CPU left for the half-tolerance rerun"

    guard_hit = False
    Aes = orients = None
    val = min_re = None
    classification = "clean miss"
    circulation = False
    if rep is not None:
        Aes, orients, ev = edge_A(rep["x"])
        min_re = float(np.min(ev.real))
        cs = list(unpack(rep["x"])[1]) + list(unpack(rep["x"])[2])
        if any(abs(c - 0.999) <= GUARD_C for c in cs) or min_re < GUARD_EIG:
            guard_hit = True
        val = a5(Aes)
        classification = classify_A5(val)
        circulation = agg.is_circulation(Aes, orients, broken=BROKEN)

    flags = {
        "measurement_code": measurement_code,
        "guard_hit": guard_hit,
        "not_settled": not_settled,
        "not_run_budget": (not started),
        "classification": classification,
    }
    label = agg.setting_label(flags)
    return {
        "label": label,
        "flags": flags,
        "cpu": used(),
        "n_done": len(results),
        "n_usable": len(usable),
        "n_close": len(close),
        "started": started,
        "best_J": best_J,
        "x": None if rep is None else rep["x"].tolist(),
        "A5": val,
        "Aes": Aes,
        "orients": None if orients is None else [int(o) for o in orients],
        "n_broken": None if Aes is None else sum(1 for a in Aes if a is not None and a > BROKEN),
        "circulation": circulation,
        "acyclic": (not circulation),
        "min_re": min_re,
        "A5_half_tol": A5_half,
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
            "run_t2_v2.py: refusing to run (pass --execute after the PREREG_3 Gate passes).",
            file=sys.stderr,
        )
        return 2
    t1_cpu = read_t1_cpu()
    print("# T2 v2 run under PREREG_3; OMP/OPENBLAS/MKL_NUM_THREADS=1; CPU via time.process_time()")
    print(f"# maxiter={MAXITER} maxfun={MAXFUN} relative-best={REL_BEST}*abs(best) broken={BROKEN}")
    print(f"# T1 cpu already used: {t1_cpu}")
    total = 0.0
    remaining = TOTAL_CAP_SEC - t1_cpu
    for w, wx in SETTINGS:
        row = run_setting(w, wx, CPU_CAP_SEC, remaining)
        row["w"] = w
        row["wx"] = wx
        total += row["cpu"]
        remaining = TOTAL_CAP_SEC - t1_cpu - total
        public = {k: v for k, v in row.items() if k != "starts_status"}
        public["n_status_rows"] = len(row.get("starts_status") or [])
        print("SETTING_JSON: " + json.dumps(public, default=str))
        print("STARTS_STATUS_JSON: " + json.dumps({"w": w, "wx": wx, "starts": row.get("starts_status") or []}, default=str))
        sys.stdout.flush()
    print(
        "TOTAL_JSON: "
        + json.dumps({"total_cpu": total, "t1_cpu": t1_cpu, "grand_total_cpu": t1_cpu + total, "settings": 5, "total_cap": TOTAL_CAP_SEC})
    )
    print("# end T2 v2")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
