#!/usr/bin/env python3
"""Pre-lock pilot for T28 / SIM-1. Uses ONLY pilot seeds, never official
candidate seeds. Computes exact discrete m* and exact Boltzmann masses so
that every official gate can be given a bar the exact values already meet
(T27 lesson). Not an official result.
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(DIR))
from sim1_lib import (
    DEFAULT_PRICES, W_LADDER, C_LADDER, LAM_LADDER, W_LOW, W_HIGH,
    P4_W, P4_C, P4_LAM, P3_W,
    seed_collides, world_from_seed, J_table, m_star_at_K, argmin_discrete,
    m_star_ladder_in_w, m_star_ladder_in_c, m_star_ladder_in_lam,
    joint_star_ladder_in_w, is_nondecreasing, is_nonincreasing,
    W_threshold_at_K, W_first_rollout, m_cont, design_edges, design_index,
    exact_boltzmann, flatten_J, connected_from, tv_distance, run_moran_ct,
    expected_loss, I_mem, e0,
)

# Pilot seeds: clearly separated from official 20261122000+ and T27.
PILOT_SEEDS = list(range(20261122800, 20261122820))  # 20 worlds
# A short mixing probe uses a subset and a modest jump count.
MIX_SEEDS = PILOT_SEEDS[:5]
N_POP = 201
BETAS = (8.0, 10.0, 12.0)
N_CHAINS = 4
N_JUMPS = 40000
BURN = 4000


def prices():
    return dict(DEFAULT_PRICES)


def check_seeds():
    for s in PILOT_SEEDS:
        if seed_collides(s):
            raise SystemExit(f"PILOT seed {s} collides")
        # Official block reserved in predictions (not imported here):
        # 20261122000..20261122015 and chains 20261122400+
        if 20261122000 <= s <= 20261122031:
            raise SystemExit(f"PILOT seed {s} sits in the reserved official block")
        if 20261122400 <= s <= 20261122600:
            raise SystemExit(f"PILOT seed {s} sits in the reserved chain block")
    print(f"pilot seeds clean: {PILOT_SEEDS[0]}..{PILOT_SEEDS[-1]}")


def analyze_world(seed, P):
    world = world_from_seed(seed)
    K_max, m_max = P["K_max"], P["m_max"]
    rec = dict(seed=seed, world=world, K_rows={}, joint=None, p4=None)
    # P1 / P2 / P3 exact ladders at each K
    for K in range(K_max + 1):
        mw = m_star_ladder_in_w(world, P, W_LADDER, K)
        mc = m_star_ladder_in_c(world, P, C_LADDER, K)
        ml = m_star_ladder_in_lam(world, P, LAM_LADDER, K, w=1.0)
        wth = W_threshold_at_K(
            K, P["c"], P["kappa"], P["h"], world["I0"], world["e_base"],
            world["gamma"], world["phi"], P["lam"], P["chi"], m_max,
        )
        w_fo = W_first_rollout(K, P["c"], world["e_base"], world["gamma"], world["phi"])
        rec["K_rows"][str(K)] = dict(
            m_of_w=mw,
            mono_w=is_nondecreasing(mw),
            m_of_c=mc,
            mono_c=is_nonincreasing(mc),
            m_of_lam=ml,
            mono_lam=is_nondecreasing(ml),
            W_threshold=wth,
            W_FOC=w_fo,
            m_at_W_LOW=mw[0],
            m_at_W_HIGH=mw[-1],
            below=mw[0] == 0 and (wth > W_LOW or wth == 0),
            above=mw[-1] >= 1 and wth < W_HIGH,
        )
    rec["joint"] = joint_star_ladder_in_w(world, P, W_LADDER)
    rec["joint_spend_mono"] = is_nondecreasing(r["spend"] for r in rec["joint"])
    rec["joint_E_mono"] = is_nonincreasing(r["E"] for r in rec["joint"])
    rec["joint_m_mono"] = is_nondecreasing(r["m"] for r in rec["joint"])
    rec["joint_K_mono"] = is_nondecreasing(r["K"] for r in rec["joint"])

    # P4 cell: exact argmin and exact Boltzmann at locked prices
    J = J_table(
        K_max, m_max, P4_W, P4_C, P["kappa"], P["h"], world["I0"],
        world["e_base"], world["gamma"], world["phi"], P4_LAM, P["chi"],
    )
    star = argmin_discrete(J)
    flat = flatten_J(J)
    edges = design_edges(K_max, m_max)
    n = flat.size
    reach = connected_from(star["index"], edges, n)
    p4 = dict(
        star=star,
        connected=len(reach) == n,
        m_cont=m_cont(
            star["K"], P4_W, P4_C, world["e_base"], world["gamma"],
            world["phi"], P4_LAM, P["chi"],
        ),
        m_on_cap=star["m"] >= m_max,
        boltzmann={},
    )
    for beta in BETAS:
        pi = exact_boltzmann(flat, beta)
        mass = float(pi[star["index"]])
        # mass on the correct m, allowing any K (shouldn't matter)
        mass_m = float(sum(pi[i] for i in range(n)
                           if (i % (m_max + 1)) == star["m"]))
        mode = int(np.argmax(pi))
        p4["boltzmann"][str(beta)] = dict(
            mass_at_star=mass,
            mass_at_mstar=mass_m,
            mode=int(mode),
            mode_is_star=mode == star["index"],
        )
    rec["p4"] = p4
    return rec, J, edges, flat, star


def mixing_probe(flat, edges, star, betas, seed, n_chains=N_CHAINS,
                 n_jumps=N_JUMPS, burn=BURN, n_pop=N_POP):
    out = {}
    for beta in betas:
        occ = np.zeros_like(flat, dtype=float)
        for c in range(n_chains):
            rng = np.random.default_rng(9000 + 1000 * seed + 10 * int(beta) + c)
            # half start at (0,0), half at the star
            start = 0 if c < n_chains // 2 else star["index"]
            visits, _ = run_moran_ct(
                flat, edges, beta, n_pop, n_jumps, burn, rng, start
            )
            occ += visits
        if occ.sum() <= 0:
            tv = 1.0
            mode = -1
            mass = 0.0
        else:
            pi_hat = occ / occ.sum()
            pi = exact_boltzmann(flat, beta)
            tv = tv_distance(pi_hat, pi)
            mode = int(np.argmax(pi_hat))
            mass = float(pi_hat[star["index"]])
        out[str(beta)] = dict(
            tv=tv, mode=mode, mode_is_star=(mode == star["index"]),
            emp_mass_at_star=mass,
        )
    return out


def main():
    t0 = time.time()
    check_seeds()
    P = prices()
    records = []
    mixing = []
    for seed in PILOT_SEEDS:
        rec, J, edges, flat, star = analyze_world(seed, P)
        records.append(rec)
        print(
            f"seed {seed}: e_base={rec['world']['e_base']:.3f} "
            f"γ={rec['world']['gamma']:.3f} φ={rec['world']['phi']:.3f} "
            f"I0={rec['world']['I0']:.3f}  "
            f"P4 (K*,m*)=({star['K']},{star['m']}) J*={star['J']:.4f} "
            f"ties={star['n_ties']} cap={rec['p4']['m_on_cap']}"
        )
        for K in range(P["K_max"] + 1):
            row = rec["K_rows"][str(K)]
            print(
                f"  K={K} m(w)={row['m_of_w']} mono_w={row['mono_w']} "
                f"W_th={row['W_threshold']:.4f} FOC={row['W_FOC']:.4f} "
                f"low/high m={row['m_at_W_LOW']}/{row['m_at_W_HIGH']} "
                f"below={row['below']} above={row['above']} "
                f"mono_c={row['mono_c']} m(c)={row['m_of_c']} "
                f"mono_λ={row['mono_lam']}"
            )
        joint_m = [r["m"] for r in rec["joint"]]
        joint_K = [r["K"] for r in rec["joint"]]
        print(
            f"  joint K={joint_K} m={joint_m} "
            f"spend_mono={rec['joint_spend_mono']} "
            f"E_mono={rec['joint_E_mono']} m_mono={rec['joint_m_mono']}"
        )
        for beta, d in rec["p4"]["boltzmann"].items():
            print(
                f"  exact β={beta} mass*={d['mass_at_star']:.4f} "
                f"mode_is_star={d['mode_is_star']}"
            )
        if seed in MIX_SEEDS:
            mix = mixing_probe(flat, edges, star, BETAS, seed)
            mixing.append(dict(seed=seed, mix=mix))
            for beta, d in mix.items():
                print(
                    f"  MIX β={beta} TV={d['tv']:.4f} "
                    f"mode_is_star={d['mode_is_star']} "
                    f"emp_mass={d['emp_mass_at_star']:.4f}"
                )

    # Summaries
    def all_rows(pred):
        return [pred(rec, K) for rec in records for K in range(P["K_max"] + 1)]

    n_rows = 20 * 4
    n_mono_w = sum(all_rows(lambda r, K: r["K_rows"][str(K)]["mono_w"]))
    n_mono_c = sum(all_rows(lambda r, K: r["K_rows"][str(K)]["mono_c"]))
    n_mono_l = sum(all_rows(lambda r, K: r["K_rows"][str(K)]["mono_lam"]))
    n_below = sum(all_rows(lambda r, K: r["K_rows"][str(K)]["m_at_W_LOW"] == 0))
    n_above = sum(all_rows(lambda r, K: r["K_rows"][str(K)]["m_at_W_HIGH"] >= 1))
    n_th_in = sum(all_rows(
        lambda r, K: W_LOW < r["K_rows"][str(K)]["W_threshold"] < W_HIGH
    ))
    n_cap = sum(1 for r in records if r["p4"]["m_on_cap"])
    n_ties = sum(1 for r in records if r["p4"]["star"]["n_ties"] != 1)
    n_joint_m = sum(1 for r in records if r["joint_m_mono"])
    n_joint_spend = sum(1 for r in records if r["joint_spend_mono"])
    n_joint_E = sum(1 for r in records if r["joint_E_mono"])
    p4_ms = [r["p4"]["star"]["m"] for r in records]
    masses = [
        r["p4"]["boltzmann"][str(b)]["mass_at_star"]
        for r in records for b in BETAS
    ]
    print("----- SUMMARY -----")
    print(f"rows {n_rows}: mono_w {n_mono_w}/{n_rows}, mono_c {n_mono_c}/{n_rows}, "
          f"mono_λ {n_mono_l}/{n_rows}")
    print(f"m*(W_LOW)=0: {n_below}/{n_rows}; m*(W_HIGH)>=1: {n_above}/{n_rows}; "
          f"W_th in (W_LOW,W_HIGH): {n_th_in}/{n_rows}")
    print(f"P4 m* range {min(p4_ms)}..{max(p4_ms)}; on cap {n_cap}/20; "
          f"nonunique {n_ties}/20")
    print(f"exact Boltzmann mass at star: min {min(masses):.6f} max {max(masses):.6f}")
    print(f"joint m mono {n_joint_m}/20; spend mono {n_joint_spend}/20; "
          f"E mono {n_joint_E}/20")
    if mixing:
        tvs = [d["tv"] for m in mixing for d in m["mix"].values()]
        print(f"mixing TVs (n={len(tvs)}): min {min(tvs):.4f} max {max(tvs):.4f}")

    out = dict(
        pilot_seeds=PILOT_SEEDS,
        seconds=time.time() - t0,
        records=records,
        mixing=mixing,
        summary=dict(
            n_mono_w=n_mono_w, n_mono_c=n_mono_c, n_mono_lam=n_mono_l,
            n_below=n_below, n_above=n_above, n_th_in=n_th_in,
            n_cap=n_cap, n_ties=n_ties, p4_m_min=int(min(p4_ms)),
            p4_m_max=int(max(p4_ms)), mass_min=float(min(masses)),
            mass_max=float(max(masses)),
            n_joint_m=n_joint_m, n_joint_spend=n_joint_spend, n_joint_E=n_joint_E,
        ),
    )
    path = DIR / "pilot_explore.json"
    path.write_text(json.dumps(out, indent=2, default=float))
    print(f"wrote {path} in {out['seconds']:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
