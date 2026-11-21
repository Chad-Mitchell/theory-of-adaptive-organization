#!/usr/bin/env python3
"""S5: rerun the 120-world Model S convexity search with the merged #116 solver.

Worlds: the same generator as convexity_targeted.py (seeds 0..119, rng 1000+seed,
J in {3,4}, scale separations x3 to x100).

Solver: theory/layers_checks/stores.py (Jacobi-scaled pseudo-inverse; MSE
re-evaluated at the returned rates) plus a Model-S adaptation of the reviewer
multi-start in rhythm_rule.py (informed grids at the mode rates, 2% store-rate
separation, Nelder-Mead, L-BFGS-B polish, differential evolution). No
minimum.accumulate.

For each world, compute E_0 = sum(v) (act blind) and E_K for K = 1..J, and
E_inf by the Yovits-Jackson integral in the merged solver. Report:

  - how many worlds have convex eps_K on K=1..J (the N60 premise) and on K=0..J;
  - how many N60 increment predictions match argmin_K [K + R(1+eps_K)],
    with the known K*=0 hole (formula starts at 1) counted separately;
  - any counterexample, with full parameters.

Run: nice -n 19 python3 s5_rerun.py
Budget: cap about 60 minutes, 6 workers.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution, minimize

DIR = Path(__file__).resolve().parent
REPO = DIR.parents[1]
MERGED_STORES = REPO / "theory" / "layers_checks" / "stores.py"
DEADLINE_S = 55 * 60
N_WORKERS = 6
N_WORLDS = 120
TOL = 1e-4  # same absolute decrement tolerance as convexity_targeted.py
R_GRID = np.logspace(-1, 7, 161)  # includes R < 1, so the K*=0 hole is visible

# Load the merged solver under a unique name so the pre-#116 copy of stores.py
# sitting in this folder cannot win the import.
spec = importlib.util.spec_from_file_location("stores_merged_s5", MERGED_STORES)
stores = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stores)


# ---- world generator: bit-identical to convexity_targeted.py ----
def world(seed):
    rng = np.random.default_rng(1000 + seed)
    J = int(rng.integers(3, 5))
    sep = 10 ** rng.uniform(0.5, 2.0, J - 1)  # factor 3 to 100 between scales
    taus = np.cumprod(np.r_[10 ** rng.uniform(0, 1), sep])
    v = 10 ** rng.uniform(-1.5, 1.5, J)
    N = 10 ** rng.uniform(-2, 1)
    return np.asarray(1 / taus, float), np.asarray(v, float), float(N)


# ---- reviewer-style multi-start, calling the merged mse_given_b ----
def safe_log_rates(x, sep=1.02):
    x = np.sort(np.clip(np.asarray(x, float), -40, 40))
    for i in range(1, len(x)):
        x[i] = max(x[i], x[i - 1] + np.log(sep))
    return x


def informed_inits(K, a, lo, hi, rng, n_rand=12):
    freqs = np.sort(np.unique(np.abs(np.asarray(a, float))))
    inits = [np.linspace(lo + 1, hi - 1, K), np.linspace(lo, hi, K)]
    for scale in (0.3, 0.7, 1.0, 1.5, 3.0, 8.0):
        pts = [np.log(max(f * scale, 1e-18)) for f in freqs]
        if K > len(pts):
            pts = pts + [
                pts[i % len(pts)] + 0.2 * ((i // len(pts)) + 1)
                for i in range(K - len(pts))
            ]
        inits.append(np.sort(np.asarray(pts[:K], float)))
    logs = np.log(np.clip(freqs, 1e-18, None))
    if K <= len(logs):
        inits.append(np.sort(logs[:K] if K < len(logs) else logs.copy()))
        if K >= 2:
            mids = 0.5 * (logs[:-1] + logs[1:])
            take = np.r_[logs, mids][:K]
            inits.append(np.sort(take))
    else:
        extra = np.linspace(lo, hi, K - len(logs))
        inits.append(np.sort(np.r_[logs, extra]))
    for _ in range(n_rand):
        inits.append(np.sort(rng.uniform(lo, hi, K)))
    out, seen = [], set()
    for x in inits:
        key = tuple(np.round(np.asarray(x, float), 5))
        if key not in seen:
            seen.add(key)
            out.append(np.asarray(x, float))
    return out


def optimize_K(a, v, N, K, seed=0, n_rand=12, use_de=True, de_maxiter=25):
    """Reviewer methods (informed starts, NM, L-BFGS-B, DE) on merged mse_given_b."""
    rng = np.random.default_rng(seed)
    la = np.log(np.abs(np.asarray(a, float)))
    lo, hi = float(la.min() - 3), float(la.max() + 6)

    def obj(x):
        e, _g = stores.mse_given_b(a, v, np.exp(safe_log_rates(x)), N)
        return float(e)

    inits = informed_inits(K, a, lo, hi, rng, n_rand=n_rand)
    t0 = time.time()
    ranked = []
    for x0 in inits:
        try:
            r = minimize(
                obj,
                x0,
                method="Nelder-Mead",
                options=dict(xatol=1e-7, fatol=1e-13, maxiter=4000 * K),
            )
            ranked.append((obj(r.x), safe_log_rates(r.x), "Nelder-Mead"))
        except Exception:
            pass
    if ranked:
        ranked.sort(key=lambda t: t[0])
        polish = [t[1] for t in ranked[:4]] + list(inits[:2])
        for x0 in polish:
            try:
                r = minimize(
                    obj,
                    x0,
                    method="L-BFGS-B",
                    bounds=[(lo - 2, hi + 2)] * K,
                    options=dict(ftol=1e-14, maxiter=2000 * K),
                )
                ranked.append((obj(r.x), safe_log_rates(r.x), "L-BFGS-B"))
            except Exception:
                pass
    if use_de:
        try:
            r = differential_evolution(
                obj,
                bounds=[(lo - 2, hi + 2)] * K,
                popsize=8,
                mutation=0.5,
                recombination=0.7,
                seed=int(seed) % (2**31 - 1),
                polish=True,
                workers=1,
                atol=1e-12,
                maxiter=de_maxiter,
            )
            ranked.append((obj(r.x), safe_log_rates(r.x), "DE"))
        except Exception:
            pass
    if not ranked:
        return dict(
            E=float("inf"),
            stores=None,
            method="none",
            n_inits=len(inits),
            elapsed=time.time() - t0,
        )
    ranked.sort(key=lambda t: t[0])
    best = ranked[0]
    b = np.exp(best[1])
    # Re-evaluate with the merged solver at the returned rates (already obj, but
    # record the realizable MSE explicitly).
    E, _g = stores.mse_given_b(a, v, b, N)
    return dict(
        E=float(E),
        stores=b.tolist(),
        method=best[2],
        n_inits=len(inits),
        elapsed=time.time() - t0,
    )


def n60_raw(eps_from1, R):
    """N60 as written: starts at K=1, counts adjacent decrements > 1/R."""
    return 1 + sum(
        1
        for k in range(1, len(eps_from1))
        if R * (eps_from1[k - 1] - eps_from1[k]) > 1
    )


def argmin_J(eps, R, k0=0):
    """Leftmost minimizer of J(K) = K + R(1+eps_K). eps[0] is K=k0."""
    J = [k0 + k + R * (1.0 + e) for k, e in enumerate(eps)]
    return int(np.argmin(J) + k0), J


def convexity_flags(eps, tol=TOL):
    """eps is a sequence in K (already ordered). Decrements dec[i] = eps[i]-eps[i+1]."""
    if any(not np.isfinite(e) for e in eps):
        return dict(
            decreasing=False,
            convex=False,
            viol=[],
            increasing_at=[],
            dec=[],
            finite=False,
        )
    dec = [eps[k] - eps[k + 1] for k in range(len(eps) - 1)]
    increasing_at = [k + 1 for k, d in enumerate(dec) if d < -tol]
    # same test as convexity_targeted.py: a violation if a later decrement exceeds
    # an earlier one by more than TOL.
    viol = [k for k in range(len(dec) - 1) if dec[k + 1] - dec[k] > tol]
    decreasing = len(increasing_at) == 0
    convex = decreasing and len(viol) == 0 and all(np.isfinite(dec))
    return dict(
        decreasing=decreasing,
        convex=convex,
        viol=viol,
        increasing_at=increasing_at,
        dec=dec,
        finite=True,
    )


def run_world(seed, use_de=True):
    t0 = time.time()
    a, v, N = world(seed)
    J = len(a)
    E0 = float(np.sum(v))
    Einf_YJ = float(stores.E_inf(a, v, N))
    fits = []
    for K in range(1, J + 1):
        fits.append(
            optimize_K(
                a, v, N, K, seed=10_000 + 17 * seed + K, n_rand=12, use_de=use_de
            )
        )
    E = [E0] + [f["E"] for f in fits]  # index 0 is K=0
    methods = [f["method"] for f in fits]
    stores_k = [f["stores"] for f in fits]
    elapsed_k = [f["elapsed"] for f in fits]

    below_causal = [
        k for k, e in enumerate(E) if k >= 1 and np.isfinite(e) and e < Einf_YJ - 1e-10
        and (Einf_YJ - e) / max(Einf_YJ, 1e-18) > 1e-8
    ]
    # Reference floor: Yovits-Jackson. In Model S, E_J = E_inf exactly; use YJ
    # for eps (do not take min(E_J, YJ), which would force eps_J = 0 and can
    # hide an optimizer that undershoots). Also record the gap.
    Einf = Einf_YJ
    eps = [float(e / Einf - 1.0) if (Einf > 0 and np.isfinite(e)) else float("nan") for e in E]
    # K=1..J view used by N60 as written (drops the K=0 entry).
    eps_from1 = eps[1:]
    flags_1J = convexity_flags(eps_from1, TOL)
    flags_0J = convexity_flags(eps, TOL)
    # tighter diagnostic, not the official test
    flags_1J_tight = convexity_flags(eps_from1, 1e-6)

    ratio = None
    if (
        len(eps_from1) == 3
        and np.isfinite(eps_from1[0])
        and eps_from1[0] > 1e-3
        and np.isfinite(eps_from1[1])
    ):
        ratio = float(eps_from1[1] / eps_from1[0])

    hole = []          # (R, argmin, n60) where argmin == 0
    mismatch = []      # genuine: argmin >= 1 and n60 != argmin
    near_tie = []      # |J differences| tiny at a disagreement, or increment ~ 1
    for R in R_GRID:
        ks, Js = argmin_J(eps, float(R), k0=0)
        cnt = n60_raw(eps_from1, float(R))
        rec = (float(R), int(ks), int(cnt))
        if ks == 0 and cnt != 0:
            hole.append(rec)
        elif ks >= 1 and cnt != ks:
            # is it a numerical knife-edge?
            J_at = {k0 + k: val for k, val in enumerate(Js) for k0 in [0]}
            gap = abs(J_at.get(cnt, np.inf) - J_at.get(ks, np.inf)) if cnt in J_at else np.inf
            # increment test knife-edge
            edge = False
            for k in range(1, len(eps_from1)):
                inc = float(R) * (eps_from1[k - 1] - eps_from1[k])
                if abs(inc - 1.0) < 1e-6:
                    edge = True
            if edge or gap < 1e-8:
                near_tie.append(rec + (float(gap),))
            else:
                mismatch.append(rec)

    return dict(
        seed=int(seed),
        J=int(J),
        taus=[float(x) for x in (1.0 / a)],
        a=[float(x) for x in a],
        v=[float(x) for x in v],
        N=float(N),
        E0=E0,
        E=[float(e) for e in E],
        Einf_YJ=Einf_YJ,
        EJ_minus_Einf=float(E[-1] - Einf_YJ) if np.isfinite(E[-1]) else None,
        below_causal=below_causal,
        eps=eps,  # K=0..J
        eps_from1=eps_from1,
        flags_1J=dict(
            decreasing=flags_1J["decreasing"],
            convex=flags_1J["convex"],
            viol=flags_1J["viol"],
            increasing_at=flags_1J["increasing_at"],
            dec=flags_1J["dec"],
            finite=flags_1J["finite"],
        ),
        flags_0J=dict(
            decreasing=flags_0J["decreasing"],
            convex=flags_0J["convex"],
            viol=flags_0J["viol"],
            increasing_at=flags_0J["increasing_at"],
            dec=flags_0J["dec"],
            finite=flags_0J["finite"],
        ),
        convex_1J_tol1e4=bool(flags_1J["convex"]),
        convex_1J_tol1e6=bool(flags_1J_tight["convex"]),
        convex_0J_tol1e4=bool(flags_0J["convex"]),
        ratio_eps2_eps1=ratio,
        n_R=len(R_GRID),
        n_hole=len(hole),
        n_mismatch=len(mismatch),
        n_near_tie=len(near_tie),
        hole_R_range=[hole[0][0], hole[-1][0]] if hole else None,
        mismatch_examples=mismatch[:8],
        near_tie_examples=near_tie[:4],
        methods=methods,
        stores=stores_k,
        elapsed=time.time() - t0,
        elapsed_K=elapsed_k,
    )


def summarize(rows):
    n = len(rows)
    conv_1J = sum(1 for r in rows if r["convex_1J_tol1e4"])
    conv_1J_tight = sum(1 for r in rows if r["convex_1J_tol1e6"])
    conv_0J = sum(1 for r in rows if r["convex_0J_tol1e4"])
    finite = sum(1 for r in rows if r["flags_1J"]["finite"])
    below = [r for r in rows if r["below_causal"]]
    incr = [r for r in rows if r["flags_1J"]["increasing_at"]]
    nonconv = [r for r in rows if not r["convex_1J_tol1e4"]]
    nonconv0 = [r for r in rows if not r["convex_0J_tol1e4"]]
    # N60 vs argmin, pooled over worlds x R
    n_comp = sum(r["n_R"] for r in rows)
    n_hole = sum(r["n_hole"] for r in rows)
    n_mis = sum(r["n_mismatch"] for r in rows)
    n_tie = sum(r["n_near_tie"] for r in rows)
    n_match_ex_hole = n_comp - n_hole - n_mis - n_tie
    worlds_with_hole = sum(1 for r in rows if r["n_hole"])
    worlds_with_mis = sum(1 for r in rows if r["n_mismatch"])
    # On convex K>=1 worlds, excluding comparisons where argmin=0:
    conv_rows = [r for r in rows if r["convex_1J_tol1e4"]]
    # per-world match rate among R with argmin>=1 is n_R - n_hole - mismatches
    ratios = [r["ratio_eps2_eps1"] for r in rows if r["ratio_eps2_eps1"] is not None]
    j3 = sum(1 for r in rows if r["J"] == 3)
    j4 = sum(1 for r in rows if r["J"] == 4)
    return dict(
        n=n,
        J3=j3,
        J4=j4,
        finite=finite,
        convex_1J_tol1e4=conv_1J,
        convex_1J_tol1e6=conv_1J_tight,
        convex_0J_tol1e4=conv_0J,
        n_nonconvex_1J=len(nonconv),
        n_nonconvex_0J=len(nonconv0),
        n_below_causal=len(below),
        n_increasing_1J=len(incr),
        below_seeds=[r["seed"] for r in below],
        nonconvex_1J_seeds=[r["seed"] for r in nonconv],
        nonconvex_0J_seeds=[r["seed"] for r in nonconv0],
        increasing_seeds=[r["seed"] for r in incr],
        n_comparisons=n_comp,
        n_hole=n_hole,
        n_mismatch=n_mis,
        n_near_tie=n_tie,
        n_match_excluding_hole=n_match_ex_hole,
        worlds_with_hole=worlds_with_hole,
        worlds_with_mismatch=worlds_with_mis,
        n_convex_worlds=len(conv_rows),
        # among convex worlds, comparisons with argmin>=1 should all match if
        # the theorem applies and numerics are clean
        convex_comparisons=sum(r["n_R"] for r in conv_rows),
        convex_hole=sum(r["n_hole"] for r in conv_rows),
        convex_mismatch=sum(r["n_mismatch"] for r in conv_rows),
        convex_near_tie=sum(r["n_near_tie"] for r in conv_rows),
        eps2_over_eps1_n=len(ratios),
        eps2_over_eps1_min=float(min(ratios)) if ratios else None,
        eps2_over_eps1_max=float(max(ratios)) if ratios else None,
        eps1_quantiles=list(
            map(
                float,
                np.quantile([r["eps_from1"][0] for r in rows if np.isfinite(r["eps_from1"][0])],
                            [0.0, 0.1, 0.5, 0.9, 1.0]),
            )
        ),
        max_elapsed=max(r["elapsed"] for r in rows) if rows else None,
        sum_elapsed=sum(r["elapsed"] for r in rows) if rows else None,
    )


def main():
    t_start = time.time()
    seeds = list(range(N_WORLDS))
    print(
        f"S5 rerun: {N_WORLDS} Model-S worlds, merged solver {MERGED_STORES}, "
        f"reviewer multi-start, {N_WORKERS} workers, TOL={TOL}, "
        f"R in logspace(-1,7,{len(R_GRID)})",
        flush=True,
    )
    rows = [None] * N_WORLDS
    with ProcessPoolExecutor(max_workers=N_WORKERS) as ex:
        futs = {ex.submit(run_world, s, True): s for s in seeds}
        done = 0
        for fut in as_completed(futs):
            s = futs[fut]
            try:
                rows[s] = fut.result()
            except Exception as e:
                rows[s] = dict(seed=s, error=str(e), convex_1J_tol1e4=False,
                               convex_0J_tol1e4=False, flags_1J=dict(finite=False,
                               decreasing=False, convex=False, viol=[], increasing_at=[], dec=[]),
                               below_causal=[0], n_R=len(R_GRID), n_hole=0,
                               n_mismatch=0, n_near_tie=0, eps_from1=[float("nan")],
                               ratio_eps2_eps1=None, elapsed=0.0, J=-1)
                print(f"ERROR seed {s}: {e}", flush=True)
            done += 1
            elapsed = time.time() - t_start
            if done % 10 == 0 or done == N_WORLDS:
                ok = sum(1 for r in rows if r and r.get("convex_1J_tol1e4"))
                print(
                    f"  {done}/{N_WORLDS} in {elapsed:.1f}s; convex so far {ok}/{done}",
                    flush=True,
                )
            if elapsed > DEADLINE_S:
                print(f"DEADLINE {DEADLINE_S}s reached after {done} worlds; cancelling.", flush=True)
                break
    rows = [r for r in rows if r is not None]
    wall = time.time() - t_start
    summary = summarize(rows)
    summary["wall_s"] = wall
    summary["solver"] = str(MERGED_STORES)
    summary["tol"] = TOL
    summary["n_R"] = len(R_GRID)
    summary["n_workers"] = N_WORKERS
    summary["deadline_s"] = DEADLINE_S
    summary["completed"] = len(rows)

    out = dict(summary=summary, worlds=rows)
    json_path = DIR / "s5_rerun.json"
    with open(json_path, "w") as f:
        json.dump(out, f, indent=1)
    # short stdout
    print(json.dumps(summary, indent=2), flush=True)
    print(
        f"wrote {json_path}  wall={wall:.1f}s  "
        f"convex 1..J @ 1e-4: {summary['convex_1J_tol1e4']}/{summary['n']}  "
        f"mismatches (excl hole): {summary['n_mismatch']}  holes: {summary['n_hole']}",
        flush=True,
    )
    # print any counterexamples in full
    for r in rows:
        if (not r.get("convex_1J_tol1e4")) or r.get("n_mismatch") or r.get("below_causal") or r.get("error"):
            print(
                "FLAG seed={seed} J={J} taus={taus} v={v} N={N} "
                "eps={eps} conv1J={convex_1J_tol1e4} conv0J={convex_0J_tol1e4} "
                "below={below_causal} n_mis={n_mismatch} n_hole={n_hole} "
                "err={err}".format(err=r.get("error"), **{k: r.get(k) for k in
                    ["seed","J","taus","v","N","eps","convex_1J_tol1e4",
                     "convex_0J_tol1e4","below_causal","n_mismatch","n_hole"]}),
                flush=True,
            )


if __name__ == "__main__":
    main()
