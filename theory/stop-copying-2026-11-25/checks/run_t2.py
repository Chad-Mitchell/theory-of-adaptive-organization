#!/usr/bin/env python3
"""T2 search for theory/stop-copying-2026-11-25/PREREG_2.md. Not a paper check.

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

N = 8
D = 1.0
SETTINGS = [(10, 0.5), (10, 1), (10, 2), (3, 1), (30, 1)]
# paper_ring.out uniform c* at lnγ=5, in setting order
C_SYM = { (10, 0.5): 0.3351, (10, 1): 0.3161, (10, 2): 0.2879, (3, 1): 0.2603, (30, 1): 0.3426 }
SEED_UNIF = 20261126
SEED_STR = 20261127
N_UNIFORM = 512
N_STRUCT_EACH = 16
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
# packed v: lnγ[0:8], c+[8:16], c-[16:24]
BOUNDS = [(-3, 5)] * 8 + [(0, 0.999)] * 16


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


def a5(Aes):
    """Fifth-largest edge A_e, treating undefined (no copying) as 0."""
    vals = sorted((0.0 if a is None else a for a in Aes), reverse=True)
    return vals[4]


def classify_A5(val):
    if abs(val - BAR) <= RES:
        return "inside-resolution"
    if val > BAR:
        return "hit"
    return "clean miss"


def dihedral_match(Aes_a, orients_a, Aes_b, orients_b):
    """True if some rotation or reflection maps b's (A_e, orientation) to a's within A_AGREE.

    Reflection reverses the edge cycle and flips orientation signs.
    """
    def num(A):
        return np.array([0.0 if a is None else a for a in A])

    Aa, oa = num(Aes_a), np.array(orients_a)
    Ab, ob = num(Aes_b), np.array(orients_b)
    for k in range(N):
        if np.all(np.abs(Aa - np.roll(Ab, k)) <= A_AGREE) and np.all(oa == np.roll(ob, k)):
            return True
        # reflection: edge i maps to edge (-i-1) mod 8, orientation flips
        Ar = np.roll(Ab[::-1], k)
        orr = -np.roll(ob[::-1], k)
        if np.all(np.abs(Aa - Ar) <= A_AGREE) and np.all(oa == orr):
            return True
    return False


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
    # one-way chain (acyclic): judge 0 is a leader (c=0); 1..7 copy the previous only
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


def run_setting(w, wx, cpu_budget):
    os.environ["OMP_NUM_THREADS"] = "1"
    t0 = time.process_time()
    rng_u = np.random.default_rng(SEED_UNIF)
    rng_s = np.random.default_rng(SEED_STR)
    starts = [draw_stable(rng_u) for _ in range(N_UNIFORM)]
    starts.extend(structured_starts((w, wx), rng_s))
    results = []
    over = False
    bounds = BOUNDS
    for i, x0 in enumerate(starts):
        if time.process_time() - t0 >= cpu_budget:
            over = True
            break
        r = minimize(lambda v: Jtot(v, w, wx), x0, method="L-BFGS-B",
                      bounds=bounds, options={"ftol": FTOL, "gtol": GTOL, "maxiter": MAXITER})
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
    packed = []
    for j, x, i in close:
        Aes, orients, ev = edge_A(x)
        packed.append((Aes, orients, ev, x, j, i))
    ref = packed[0]
    for Aes, orients, ev, x, j, i in packed[1:]:
        if not dihedral_match(ref[0], ref[1], Aes, orients):
            return {"label": "not settled", "cpu": used, "n_done": len(results),
                    "best_J": best_J, "n_close": len(close),
                    "note": "starts at the best value disagree on A_e (no 16-element dihedral match within 0.01)"}
    Aes, orients, ev, x, j, i = min(packed, key=lambda t: (t[4], t[5]))
    x0_best = starts[i]
    r2 = minimize(lambda v: Jtot(v, w, wx), x0_best, method="L-BFGS-B",
                   bounds=bounds, options={"ftol": FTOL / 2, "gtol": GTOL / 2, "maxiter": MAXITER})
    Aes2, _, ev2 = edge_A(r2.x)
    if abs(a5(Aes) - a5(Aes2)) > TOL_A_MOVE:
        return {"label": "measurement/code", "cpu": used, "n_done": len(results),
                "best_J": best_J, "x": x.tolist(), "A5": a5(Aes), "A5_half_tol": a5(Aes2),
                "note": "fifth-largest A_e moved by more than 0.005 at half tolerances"}
    min_re = float(np.min(ev.real))
    cs = list(unpack(x)[1]) + list(unpack(x)[2])
    if any(abs(c - 0.999) <= GUARD_C for c in cs) or min_re < GUARD_EIG:
        return {"label": "guard-hit", "cpu": used, "n_done": len(results),
                "best_J": best_J, "x": x.tolist(), "A5": a5(Aes), "min_re": min_re}
    val = a5(Aes)
    lab = classify_A5(val)
    n_broken = sum(1 for a in Aes if a is not None and a >= BAR)
    n_broken_res = sum(1 for a in Aes if a is not None and a > BAR + RES)
    circulation = all(o == orients[0] and o != 0 for o in orients) and all(a is not None and a >= BAR for a in Aes)
    return {"label": lab, "cpu": used, "n_done": len(results), "n_close": len(close),
            "best_J": best_J, "x": x.tolist(), "A5": val, "Aes": Aes, "orients": orients,
            "n_broken": n_broken, "n_broken_resolved": n_broken_res,
            "circulation": circulation, "acyclic": (not circulation), "min_re": min_re,
            "A5_half_tol": a5(Aes2)}


def main(argv):
    p = argparse.ArgumentParser()
    p.add_argument("--execute", action="store_true",
                   help="required; refuse to run the search without this flag")
    args = p.parse_args(argv)
    if not args.execute:
        print("run_t2.py: refusing to run (pass --execute after the PREREG_2 Gate passes).", file=sys.stderr)
        return 2
    os.environ["OMP_NUM_THREADS"] = "1"
    print("# T2 run under PREREG_2; OMP_NUM_THREADS=1; CPU via time.process_time()")
    for w, wx in SETTINGS:
        row = run_setting(w, wx, CPU_CAP_SEC)
        row["w"] = w
        row["wx"] = wx
        print(f"setting w={w} wx={wx}: {row}")
        sys.stdout.flush()
    print("# end T2")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
