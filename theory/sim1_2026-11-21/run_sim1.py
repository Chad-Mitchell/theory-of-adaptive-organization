#!/usr/bin/env python3
"""T28 official run: simulation already inside J.

Prereg, predictions, this runner, and sim1_lib.py must be locked
(LOCK.txt) before this script evaluates J on an official world or
starts a Moran chain. Run:

    nice -n 19 python3 theory/sim1_2026-11-21/run_sim1.py

Does not edit PREREG.md, predictions.json, this file, or sim1_lib.py.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(DIR))
from sim1_lib import (
    DEFAULT_PRICES, W_LADDER, C_LADDER, LAM_LADDER, W_LOW, W_HIGH,
    P4_W, P4_C, P4_LAM, P4_BETA, P4_TOL_M,
    seed_collides, world_from_seed, J_table, m_star_at_K, argmin_discrete,
    m_star_ladder_in_w, m_star_ladder_in_c, m_star_ladder_in_lam,
    joint_star_ladder_in_w, is_nondecreasing, is_nonincreasing,
    W_threshold_at_K, design_edges, flatten_J, exact_boltzmann,
    connected_from, tv_distance, run_moran_ct, occupation_m_stats,
    km_of_index,
)

PRED = json.loads((DIR / "predictions.json").read_text())
LOCKED_FILES = ("PREREG.md", "predictions.json", "run_sim1.py", "sim1_lib.py")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assert_lock():
    lock = (DIR / "LOCK.txt").read_text()
    for name in LOCKED_FILES:
        digest = sha256(DIR / name)
        if digest not in lock:
            raise SystemExit(f"LOCK mismatch or missing hash for {name}: {digest}")
    print("LOCK ok: PREREG.md, predictions.json, run_sim1.py, and "
          "sim1_lib.py hashes match LOCK.txt")


def prices(P):
    out = dict(DEFAULT_PRICES)
    # predictions.json is the locked source of prices and ladders
    for k in ("h", "c", "kappa", "lam", "chi", "K_max", "m_max"):
        if k in P:
            out[k] = P[k]
    return out


def exact_p1_p2_p3(world, Pr):
    """Exact discrete gates at every locked K. No sampling."""
    K_max = Pr["K_max"]
    rows = {}
    p1_ok = p2_ok = p3_ok = True
    for K in range(K_max + 1):
        mw = m_star_ladder_in_w(world, Pr, tuple(PRED["parameters"]["W_LADDER"]), K)
        mc = m_star_ladder_in_c(
            world, Pr, tuple(PRED["parameters"]["C_LADDER"]), K,
            w=PRED["parameters"]["P3_W"], lam=PRED["parameters"]["P3_LAM"],
        )
        ml = m_star_ladder_in_lam(
            world, Pr, tuple(PRED["parameters"]["LAM_LADDER"]), K,
            w=PRED["parameters"]["W_FOR_LAM"],
        )
        th = W_threshold_at_K(
            K, Pr["c"], Pr["kappa"], Pr["h"], world["I0"], world["e_base"],
            world["gamma"], world["phi"], Pr["lam"], Pr["chi"], Pr["m_max"],
        )
        mono_w = is_nondecreasing(mw)
        mono_c = is_nonincreasing(mc)
        mono_l = is_nondecreasing(ml)
        below = (mw[0] == 0)
        above = (mw[-1] >= 1)
        th_in = (W_LOW < th < W_HIGH)
        # P2 also requires the threshold itself sits in the locked interval,
        # so the low and high rungs really are on opposite sides.
        row_p1 = mono_w and mono_l
        row_p2 = below and above and th_in
        row_p3 = mono_c
        if not row_p1:
            p1_ok = False
        if not row_p2:
            p2_ok = False
        if not row_p3:
            p3_ok = False
        rows[str(K)] = dict(
            m_of_w=list(mw), mono_w=mono_w,
            m_of_c=list(mc), mono_c=mono_c,
            m_of_lam=list(ml), mono_lam=mono_l,
            W_threshold=float(th),
            m_at_W_LOW=int(mw[0]), m_at_W_HIGH=int(mw[-1]),
            below=below, above=above, th_in=th_in,
            p1=row_p1, p2=row_p2, p3=row_p3,
        )
    joint = joint_star_ladder_in_w(
        world, Pr, tuple(PRED["parameters"]["W_LADDER"])
    )
    # Diagnostic only: not an official gate (K and m are substitutes).
    diag = dict(
        joint=[{k: (float(v) if k in ("w", "spend", "E", "J") else int(v))
                for k, v in r.items()} for r in joint],
        joint_m_nondecreasing=is_nondecreasing(r["m"] for r in joint),
        joint_spend_nondecreasing=is_nondecreasing(r["spend"] for r in joint),
        joint_E_nonincreasing=is_nonincreasing(r["E"] for r in joint),
    )
    return dict(P1=p1_ok, P2=p2_ok, P3=p3_ok, rows=rows, diagnostic=diag)


def p4_exact_and_validity(world, Pr):
    J = J_table(
        Pr["K_max"], Pr["m_max"], P4_W, P4_C, Pr["kappa"], Pr["h"],
        world["I0"], world["e_base"], world["gamma"], world["phi"],
        P4_LAM, Pr["chi"],
    )
    star = argmin_discrete(J)
    flat = flatten_J(J)
    edges = design_edges(Pr["K_max"], Pr["m_max"])
    n = flat.size
    reach = connected_from(star["index"], edges, n)
    pi = exact_boltzmann(flat, P4_BETA)
    exact_stats = occupation_m_stats(pi, Pr["m_max"], star["m"])
    reasons = []
    if star["n_ties"] != 1:
        reasons.append(f"nonunique_argmin ties={star['n_ties']}")
    if star["m"] < 2:
        reasons.append(f"m*={star['m']} < 2")
    if star["m"] >= Pr["m_max"]:
        reasons.append(f"m* on cap {star['m']}")
    if len(reach) != n:
        reasons.append(f"disconnected {len(reach)}/{n}")
    if exact_stats["marg_mode_m"] != star["m"]:
        reasons.append(f"exact marg mode {exact_stats['marg_mode_m']} != m*")
    if exact_stats["abs_err"] > P4_TOL_M:
        reasons.append(f"exact |E[m]-m*|={exact_stats['abs_err']:.4f} > {P4_TOL_M}")
    return dict(
        star=dict(K=star["K"], m=star["m"], J=star["J"],
                  index=star["index"], n_ties=star["n_ties"]),
        exact=exact_stats,
        reasons=reasons,
        J=J, flat=flat, edges=edges,
    )


def run_p4_moran(flat, edges, star, world_index, P):
    n_chains = P["N_CHAINS"]
    n_jumps = P["N_JUMPS"]
    burn = P["BURN_JUMPS"]
    n_pop = P["N_POP"]
    base = P["CHAIN_SEED_BASE"]
    occ = np.zeros_like(flat, dtype=float)
    chain_seeds = []
    t0 = time.time()
    for c in range(n_chains):
        seed = int(base + 1000 * world_index + 10 * int(P4_BETA) + c)
        if seed_collides(seed):
            raise SystemExit(f"chain seed {seed} collides")
        chain_seeds.append(seed)
        rng = np.random.default_rng(seed)
        start = 0 if c < n_chains // 2 else star["index"]
        visits, _ = run_moran_ct(
            flat, edges, P4_BETA, n_pop, n_jumps, burn, rng, start
        )
        occ += visits
    seconds = time.time() - t0
    if occ.sum() <= 0:
        emp = occupation_m_stats(occ, P["m_max"], star["m"])
        tv = 1.0
    else:
        emp = occupation_m_stats(occ, P["m_max"], star["m"])
        pi = exact_boltzmann(flat, P4_BETA)
        tv = tv_distance(occ / occ.sum(), pi)
    mode_joint = int(np.argmax(occ)) if occ.sum() > 0 else -1
    return dict(
        tv=float(tv),
        emp=emp,
        mode_joint=mode_joint,
        mode_joint_km=list(km_of_index(mode_joint, P["m_max"])) if mode_joint >= 0 else None,
        chain_seeds=chain_seeds,
        seconds=seconds,
        occupation=occ.tolist(),
    )


def main():
    t_all = time.time()
    assert_lock()
    Pparam = PRED["parameters"]
    Pr = prices(Pparam)
    candidates = list(PRED["candidate_rng_seeds"])
    n_official_target = int(Pparam["N_OFFICIAL"])
    for s in candidates:
        if seed_collides(s):
            raise SystemExit(f"official candidate seed {s} collides with a prior set")
    print(f"candidate seeds clean: {candidates[0]}..{candidates[-1]}")

    official = []
    rejected = []
    for i, seed in enumerate(candidates):
        if len(official) >= n_official_target:
            break
        t0 = time.time()
        world = world_from_seed(seed)
        print(f"candidate {i} seed {seed} e_base={world['e_base']:.4f} "
              f"gamma={world['gamma']:.4f} phi={world['phi']:.4f} I0={world['I0']:.4f}")
        gates = exact_p1_p2_p3(world, Pr)
        p4v = p4_exact_and_validity(world, Pr)
        rec = dict(
            candidate_index=i,
            seed=seed,
            world={k: (int(v) if k == "rng_seed" else float(v)) for k, v in world.items()},
            P1=gates["P1"], P2=gates["P2"], P3=gates["P3"],
            rows=gates["rows"], diagnostic=gates["diagnostic"],
            p4_star=p4v["star"], p4_exact= {k: v for k, v in p4v["exact"].items() if k != "marg"},
            p4_exact_marg=p4v["exact"]["marg"],
            validity_reasons=list(p4v["reasons"]),
        )
        # Mixing is part of validity; only run Moran if the exact screen passed.
        if p4v["reasons"]:
            rec["official_valid"] = False
            rec["seconds"] = time.time() - t0
            rejected.append(rec)
            print(f"  NOT official-valid: {p4v['reasons']}")
            continue
        moran = run_p4_moran(p4v["flat"], p4v["edges"], p4v["star"], i, Pparam)
        rec["p4_moran"] = {k: v for k, v in moran.items() if k != "occupation"}
        rec["p4_occupation"] = moran["occupation"]
        mix_ok = moran["tv"] <= Pparam["MIX_TV_MAX"]
        if not mix_ok:
            rec["official_valid"] = False
            rec["validity_reasons"] = [f"mixing TV={moran['tv']:.4f} > {Pparam['MIX_TV_MAX']}"]
            rec["seconds"] = time.time() - t0
            rejected.append(rec)
            print(f"  NOT official-valid: mixing TV={moran['tv']:.4f}")
            continue
        # Official P4 clauses (empirical).
        p4_mode = moran["emp"]["marg_mode_m"] == p4v["star"]["m"]
        p4_mean = moran["emp"]["abs_err"] <= P4_TOL_M
        rec["P4"] = bool(p4_mode and p4_mean)
        rec["P4_marg_mode_ok"] = bool(p4_mode)
        rec["P4_mean_ok"] = bool(p4_mean)
        rec["official_valid"] = True
        rec["seconds"] = time.time() - t0
        official.append(rec)
        print(
            f"  official-valid #{len(official)}  (K*,m*)=({p4v['star']['K']},{p4v['star']['m']})  "
            f"P1={rec['P1']} P2={rec['P2']} P3={rec['P3']} P4={rec['P4']}  "
            f"TV={moran['tv']:.4f} emp |E[m]-m*|={moran['emp']['abs_err']:.3f}  "
            f"marg_mode={moran['emp']['marg_mode_m']}  {rec['seconds']:.1f}s"
        )

    n_off = len(official)
    if n_off < n_official_target:
        overall = "INCONCLUSIVE"
        p1s = p2s = p3s = p4s = None
    else:
        p1s = all(r["P1"] for r in official)
        p2s = all(r["P2"] for r in official)
        p3s = all(r["P3"] for r in official)
        p4s = all(r["P4"] for r in official)
        overall = "PASS" if (p1s and p2s and p3s and p4s) else "FAIL"

    # Strip occupation from the JSON? Keep it for review; it's 164 numbers.
    out = dict(
        test="T28",
        overall=overall,
        n_official=n_off,
        n_target=n_official_target,
        P1=p1s, P2=p2s, P3=p3s, P4=p4s,
        official_seeds=[r["seed"] for r in official],
        official=official,
        rejected=rejected,
        lock_hashes={name: sha256(DIR / name) for name in LOCKED_FILES},
        seconds=time.time() - t_all,
        parameters_echo={
            "P4_W": P4_W, "P4_C": P4_C, "P4_LAM": P4_LAM,
            "P4_BETA": P4_BETA, "P4_TOL_M": P4_TOL_M,
        },
    )
    (DIR / "run_sim1.json").write_text(json.dumps(out, indent=2))
    log = []
    log.append(f"T28 official run overall={overall}")
    log.append(f"official_seeds={out['official_seeds']}")
    log.append(f"P1={p1s} P2={p2s} P3={p3s} P4={p4s} n_official={n_off}/{n_official_target}")
    log.append(f"seconds={out['seconds']:.3f}")
    log.append(f"lock={out['lock_hashes']}")
    (DIR / "run_sim1.log").write_text("\n".join(log) + "\n")
    print(f"OVERALL {overall}  P1={p1s} P2={p2s} P3={p3s} P4={p4s}  "
          f"{out['seconds']:.1f}s  wrote run_sim1.json")
    return 0 if overall != "ERROR" else 1


if __name__ == "__main__":
    raise SystemExit(main())
