#!/usr/bin/env python3
"""T27 official run: weak-mutation Moran on Model S design grids.

Prereg and predictions must be locked (LOCK.txt) before this script evaluates
J on an official world or starts a chain. Run:

    nice -n 19 python3 theory/bridge_2026-11-21/run_t27.py

Does not edit PREREG.md or predictions.json.
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
from bridge_lib import (
    s5_world_from_rng_seed, seed_collides, log_grid, enumerate_designs,
    compute_J_table, neighbor_edges, exact_boltzmann, hessian_K2,
    argmin_unique, interior_K2, polish_K2, whitened_lattice, J_on_thetas,
    lattice_4_edges, run_moran_ct, tv_distance, coarse_mass_on_K,
    connected_from, stores,
)

PRED = json.loads((DIR / "predictions.json").read_text())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assert_lock():
    lock = (DIR / "LOCK.txt").read_text()
    for name in ("PREREG.md", "predictions.json"):
        digest = sha256(DIR / name)
        if digest not in lock:
            raise SystemExit(f"LOCK mismatch or missing hash for {name}: {digest}")
    print("LOCK ok: PREREG.md and predictions.json hashes match LOCK.txt")


def build_coarse(a, v, N, P):
    g = log_grid(a, P["N_GRID"], P["LO_PAD"], P["HI_PAD"])
    designs = enumerate_designs(g, P["K_MAX"])
    tab = compute_J_table(a, v, N, P["R"], designs, g)
    edges = neighbor_edges(designs)
    return g, designs, tab, edges


def validity(a, v, N, g, designs, tab, edges, P):
    J = tab["J"]
    star, ties = argmin_unique(J)
    reasons = []
    Ks, idx = designs[star]
    if len(ties) != 1:
        reasons.append(f"nonunique_argmin ties={len(ties)}")
    if Ks != 2:
        reasons.append(f"K*={Ks} not 2")
    if not interior_K2(designs[star], P["N_GRID"]):
        reasons.append("argmin_not_interior")
    n = len(designs)
    reach = connected_from(star, edges, n)
    if len(reach) != n:
        reasons.append(f"disconnected {len(reach)}/{n}")
    polished = None
    hess = None
    if Ks == 2:
        theta0 = g[list(idx)]
        theta_p, Jp, ok_p = polish_K2(a, v, N, P["R"], tab["E_inf"], theta0)
        polished = dict(theta=theta_p.tolist(), J=Jp, success=ok_p)
        H, ev, ok_h = hessian_K2(a, v, N, P["R"], tab["E_inf"], theta_p)
        hess = dict(H=H.tolist(), ev=ev.tolist(), ok=ok_h)
        if not ok_h or ev[0] <= P["HESS_EV_MIN"]:
            reasons.append(f"hessian_not_spd ev={ev.tolist()}")
    masses = {}
    for b in P["BETA_HIGH"]:
        m = coarse_mass_on_K(J, designs, b, 2)
        masses[str(b)] = m
        if m < P["MASS_K2_MIN"]:
            reasons.append(f"mass_K2_beta{b}={m:.4f}<{P['MASS_K2_MIN']}")
    valid = len(reasons) == 0
    return dict(
        valid=valid,
        reasons=reasons,
        star=int(star),
        Kstar=int(Ks),
        idx=list(idx),
        Jstar_coarse=float(J[star]),
        n_ties=int(len(ties)),
        polished=polished,
        hessian=hess,
        mass_K2_high=masses,
        n_designs=n,
        n_edges=len(edges),
        reachable=len(reach),
    )


def pool_occupation(occs):
    total = np.sum(occs, axis=0)
    s = total.sum()
    if s <= 0:
        return total, total
    return total, total / s


def score_p1(emp, star):
    mode = int(np.argmax(emp))
    return dict(mode=mode, star=int(star), pass_flag=(mode == int(star)))


def score_p2(emp, J, d, beta, rel_tol):
    star = int(np.argmin(J))
    mean = float(np.dot(emp, J))
    excess = mean - float(J[star])
    target = d / 2.0
    bex = beta * excess
    rel = abs(bex - target) / target if target else float("inf")
    return dict(
        Jstar=float(J[star]),
        mean_J=mean,
        excess=excess,
        beta_excess=bex,
        target=target,
        rel_err=rel,
        pass_flag=bool(rel <= rel_tol),
        mode=int(np.argmax(emp)),
        mass_at_min=float(emp[star]),
        min_interior=None,
    )


def score_p3(emp, J, designs, Jstar, excess_high_mean, P):
    mean = float(np.dot(emp, J))
    excess = mean - float(Jstar)
    masses = {}
    for K in range(0, P["K_MAX"] + 1):
        masses[str(K)] = float(sum(emp[i] for i, d in enumerate(designs) if d[0] == K))
    n_k = sum(1 for m in masses.values() if m >= P["P3_MIN_K_MASS"])
    spread = n_k >= 2
    above = mean > float(Jstar)
    ratio_ok = excess >= P["P3_EXCESS_RATIO"] * float(excess_high_mean)
    return dict(
        mean_J=mean,
        excess=excess,
        masses_K=masses,
        n_K_above_floor=n_k,
        spread=spread,
        mean_above_Jstar=above,
        excess_ratio=excess / float(excess_high_mean) if excess_high_mean else None,
        pass_flag=bool(above and spread and ratio_ok),
    )


def run_world(world_index, rng_seed, P, t0):
    row = dict(world_index=world_index, rng_seed=int(rng_seed), collided=seed_collides(rng_seed))
    if row["collided"]:
        row["valid"] = False
        row["reasons"] = ["seed_collision"]
        return row
    a, v, N = s5_world_from_rng_seed(rng_seed)
    row["world"] = dict(a=a.tolist(), v=v.tolist(), N=N, taus=(1 / a).tolist(), n_modes=int(len(a)))
    g, designs, tab, edges = build_coarse(a, v, N, P)
    val = validity(a, v, N, g, designs, tab, edges, P)
    row.update(val)
    row["E_inf"] = tab["E_inf"]
    row["E0"] = tab["E0"]
    if not val["valid"]:
        return row

    J = tab["J"]
    star = val["star"]
    N_pop = P["N_POP"]
    n_jumps_high = P["N_JUMPS"]
    n_jumps_low = P["N_JUMPS_LOW"]
    burn = P["BURN_JUMPS"]
    n_chains = P["N_CHAINS"]
    mix_tv = P["MIX_TV_MAX"]

    # ---- P1 / P3 on the coarse graph ----
    coarse = {"P1": {}, "P3": None, "sanity": {}, "exact": {}}
    high_excess_exact = []
    high_excess_emp = []
    p1_ok = True
    for beta in P["BETA_HIGH"] + [P["BETA_LOW"]]:
        pi = exact_boltzmann(J, beta)
        exact_stats = dict(
            mean_J=float(np.dot(pi, J)),
            excess=float(np.dot(pi, J) - J[star]),
            mode=int(np.argmax(pi)),
            mass_star=float(pi[star]),
            mass_K2=float(sum(pi[i] for i, d in enumerate(designs) if d[0] == 2)),
        )
        exact_stats["beta_excess"] = beta * exact_stats["excess"]
        coarse["exact"][str(beta)] = exact_stats
        n_jumps = n_jumps_low if beta == P["BETA_LOW"] else n_jumps_high
        occs = []
        for c in range(n_chains):
            seed = P["CHAIN_SEED_BASE"] + 1000 * world_index + 10 * int(round(10 * beta)) + c
            rng = np.random.default_rng(seed)
            start = 0 if c < n_chains // 2 else star  # K=0 is designs[0]
            occ, _ = run_moran_ct(J, edges, beta, N_pop, n_jumps, burn, rng, start)
            occs.append(occ)
        total, emp = pool_occupation(np.array(occs))
        tv = tv_distance(emp, pi)
        mixed = tv <= mix_tv
        cell = dict(
            visits=float(total.sum()),
            tv=tv,
            mixed=mixed,
            emp_mean_J=float(np.dot(emp, J)),
            emp_excess=float(np.dot(emp, J) - J[star]),
            emp_mode=int(np.argmax(emp)),
            emp_mass_star=float(emp[star]),
        )
        coarse["sanity"][str(beta)] = cell
        if beta in P["BETA_HIGH"]:
            p1 = score_p1(emp, star)
            p1["tv"] = tv
            p1["mixed"] = mixed
            p1["valid_cell"] = mixed
            if not mixed:
                p1["pass_flag"] = None
            coarse["P1"][str(beta)] = p1
            if mixed:
                high_excess_emp.append(cell["emp_excess"])
                high_excess_exact.append(exact_stats["excess"])
                p1_ok = p1_ok and p1["pass_flag"]
            else:
                p1_ok = False  # world may be marked invalid later
        else:
            excess_high = float(np.mean(high_excess_emp)) if high_excess_emp else float(np.mean(high_excess_exact))
            p3 = score_p3(emp, J, designs, J[star], excess_high, P)
            p3["tv"] = tv
            p3["mixed"] = mixed
            p3["valid_cell"] = mixed
            if not mixed:
                p3["pass_flag"] = None
            coarse["P3"] = p3
    row["coarse"] = coarse

    # ---- P2 on the whitened K=2 lattice ----
    theta_p = np.array(val["polished"]["theta"], float)
    H = np.array(val["hessian"]["H"], float)
    Y, Theta, L, ys = whitened_lattice(H, theta_p, P["P2_HALF"], P["P2_N_AXIS"])
    Jf = J_on_thetas(a, v, N, P["R"], tab["E_inf"], Theta, K=2)
    edges_f = lattice_4_edges(P["P2_N_AXIS"])
    imin = int(np.argmin(Jf))
    nax = P["P2_N_AXIS"]
    i1, i2 = divmod(imin, nax)
    interior = 0 < i1 < nax - 1 and 0 < i2 < nax - 1
    p2 = {"interior_min": interior, "Jmin_fine": float(Jf[imin]), "ymin": Y[imin].tolist(), "cells": {}}
    p2_ok = interior
    if not interior:
        p2_ok = False
        p2["reasons"] = ["fine_min_on_boundary"]
    for beta in P["BETA_HIGH"]:
        pi = exact_boltzmann(Jf, beta)
        exact = dict(
            mean_J=float(np.dot(pi, Jf)),
            excess=float(np.dot(pi, Jf) - Jf[imin]),
        )
        exact["beta_excess"] = beta * exact["excess"]
        exact["rel_err"] = abs(exact["beta_excess"] - 1.0)
        occs = []
        center = (P["P2_N_AXIS"] // 2) * P["P2_N_AXIS"] + (P["P2_N_AXIS"] // 2)
        for c in range(n_chains):
            seed = P["CHAIN_SEED_BASE"] + 1000 * world_index + 70000 + 10 * int(beta) + c
            rng = np.random.default_rng(seed)
            start = center if c < 2 else imin
            occ, _ = run_moran_ct(Jf, edges_f, beta, N_pop, n_jumps_high, burn, rng, start)
            occs.append(occ)
        total, emp = pool_occupation(np.array(occs))
        tv = tv_distance(emp, pi)
        mixed = tv <= mix_tv
        sc = score_p2(emp, Jf, P["D"], beta, P["P2_REL_TOL"])
        sc.update(dict(tv=tv, mixed=mixed, valid_cell=mixed and interior,
                        exact_beta_excess=exact["beta_excess"], visits=float(total.sum())))
        if not sc["valid_cell"]:
            sc["pass_flag"] = None
        p2["cells"][str(beta)] = sc
        p2[f"exact_{beta}"] = exact
        if sc["valid_cell"]:
            p2_ok = p2_ok and sc["pass_flag"]
        else:
            p2_ok = False
    row["P2"] = p2

    # world-level official flags (None if invalid mixing)
    p1_cells = [coarse["P1"][str(b)] for b in P["BETA_HIGH"]]
    p2_cells = [p2["cells"][str(b)] for b in P["BETA_HIGH"]]
    mixed_ok = all(c.get("mixed") for c in p1_cells + p2_cells + [coarse["P3"]])
    row["mixed_ok"] = mixed_ok
    row["official_valid"] = bool(val["valid"] and mixed_ok and interior)
    if row["official_valid"]:
        row["P1_pass"] = all(c["pass_flag"] for c in p1_cells)
        row["P2_pass"] = all(c["pass_flag"] for c in p2_cells)
        row["P3_pass"] = bool(coarse["P3"]["pass_flag"])
    else:
        row["P1_pass"] = row["P2_pass"] = row["P3_pass"] = None
    row["seconds"] = time.time() - t0
    return row


def main():
    assert_lock()
    P = PRED["parameters"]
    t_all = time.time()
    # choose official worlds
    candidates = [P["BASE_WORLD_SEED"] + i for i in range(P["N_CANDIDATES"])]
    collisions = [s for s in candidates if seed_collides(s)]
    if collisions:
        raise SystemExit(f"locked candidate seeds collide: {collisions}")
    official = []
    rejected = []
    rows = []
    for i, seed in enumerate(candidates):
        if len(official) >= P["N_OFFICIAL"]:
            break
        print(f"\n==== candidate {i} rng_seed={seed} ====", flush=True)
        t0 = time.time()
        row = run_world(i, seed, P, t0)
        rows.append(row)
        if row.get("official_valid"):
            official.append(row)
            print(f"  VALID official #{len(official)}  P1={row['P1_pass']} P2={row['P2_pass']} P3={row['P3_pass']}  {row['seconds']:.1f}s", flush=True)
        else:
            rejected.append(dict(rng_seed=seed, reasons=row.get("reasons"), mixed_ok=row.get("mixed_ok"), official_valid=row.get("official_valid")))
            print(f"  INVALID/reject  reasons={row.get('reasons')} mixed={row.get('mixed_ok')}", flush=True)

    n_ok = len(official)
    inconclusive = n_ok < P["N_OFFICIAL"]
    summary = dict(
        n_official=n_ok,
        inconclusive=inconclusive,
        official_seeds=[r["rng_seed"] for r in official],
        rejected=rejected,
    )
    if not inconclusive:
        summary["P1"] = all(r["P1_pass"] for r in official)
        summary["P2"] = all(r["P2_pass"] for r in official)
        summary["P3"] = all(r["P3_pass"] for r in official)
        summary["OVERALL"] = summary["P1"] and summary["P2"] and summary["P3"]
    else:
        summary["P1"] = summary["P2"] = summary["P3"] = summary["OVERALL"] = "INCONCLUSIVE"

    out = dict(
        parameters=P,
        prereg_sha256=sha256(DIR / "PREREG.md"),
        predictions_sha256=sha256(DIR / "predictions.json"),
        summary=summary,
        rows=rows,
        seconds=time.time() - t_all,
    )
    path = DIR / "run_t27.json"
    path.write_text(json.dumps(out, indent=2, default=float))
    print("\n==== SUMMARY ====")
    print(json.dumps(summary, indent=2))
    print(f"wrote {path} in {out['seconds']:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
