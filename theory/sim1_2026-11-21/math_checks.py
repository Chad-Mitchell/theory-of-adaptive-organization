#!/usr/bin/env python3
"""Fast identities for T28: FOC, Topkis differences, first-bit threshold,
seed non-collision, lock hashes (including runner and library).

Run: python3 theory/sim1_2026-11-21/math_checks.py
"""
from __future__ import annotations

import hashlib
import math
import sys
from pathlib import Path

import numpy as np

DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(DIR))
from sim1_lib import (
    e0, expected_loss, J_cost, J_table, m_cont, W_first_rollout,
    m_star_at_K, argmin_discrete, m_star_ladder_in_w, m_star_ladder_in_c,
    m_star_ladder_in_lam, joint_star_ladder_in_w, is_nondecreasing,
    is_nonincreasing, W_threshold_at_K, seed_collides, world_from_seed,
    design_edges, design_index, connected_from, DEFAULT_PRICES, W_LADDER,
    C_LADDER, LAM_LADDER, W_LOW, W_HIGH, P4_W, P4_BETA, P4_TOL_M,
    flatten_J, exact_boltzmann, occupation_m_stats,
)


def check_foc_formula():
    """m_cont is the unique critical point of c m + W E, and matches a
    finite-difference FOC to high accuracy."""
    rng = np.random.default_rng(0)
    for _ in range(200):
        e_base = float(10 ** rng.uniform(-0.3, 0.3))
        gamma = float(10 ** rng.uniform(-0.3, 0.3))
        phi = float(rng.uniform(0.35, 0.80))
        c = float(10 ** rng.uniform(-2, 0))
        w = float(10 ** rng.uniform(-1, 2))
        K = int(rng.integers(0, 4))
        mc = m_cont(K, w, c, e_base, gamma, phi, 0.0, 1.0)
        e = e0(K, e_base, gamma)
        # analytic FOC residual at m_cont when interior
        if mc > 1e-12:
            residual = c - w * e * phi * phi / (1.0 + phi * mc) ** 2
            assert abs(residual) < 1e-10, residual
            # finite difference
            def f(m):
                return c * m + w * expected_loss(K, m, e_base, gamma, phi)
            h = 1e-6
            d = (f(mc + h) - f(mc - h)) / (2 * h)
            assert abs(d) < 1e-6, (mc, d)
        else:
            # at 0, the right derivative of c m + W E should be >= 0
            right = c - w * e * phi * phi  # derivative at m=0
            assert right >= -1e-12, right
        # FOC threshold identity
        Wfo = W_first_rollout(K, c, e_base, gamma, phi)
        assert abs(Wfo - c / (e * phi * phi)) < 1e-15
        assert abs(m_cont(K, Wfo, c, e_base, gamma, phi) ) < 1e-10
    return True


def check_increasing_differences():
    """-J has increasing differences in (m,w), (m,λ), (m,-c) at fixed K."""
    # Δ_m J(w) = J(m+1,w)-J(m,w) should be nonincreasing in w (so -J has ID).
    K, I0, e_base, gamma, phi = 1, 0.2, 1.0, 1.0, 0.5
    h, kappa, chi, c = 0.25, 0.2, 1.0, 0.05
    ws = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0]
    for m in range(0, 20):
        deltas = []
        for w in ws:
            j0 = J_cost(K, m, w, c, kappa, h, I0, e_base, gamma, phi, 0.0, chi)
            j1 = J_cost(K, m + 1, w, c, kappa, h, I0, e_base, gamma, phi, 0.0, chi)
            deltas.append(j1 - j0)
        assert is_nonincreasing(deltas), (m, deltas)
    # in lambda, at w=1
    for m in range(0, 20):
        deltas = []
        for lam in LAM_LADDER:
            j0 = J_cost(K, m, 1.0, c, kappa, h, I0, e_base, gamma, phi, lam, chi)
            j1 = J_cost(K, m + 1, 1.0, c, kappa, h, I0, e_base, gamma, phi, lam, chi)
            deltas.append(j1 - j0)
        assert is_nonincreasing(deltas), (m, deltas)
    # in c (deltas should be nondecreasing in c, so m* nonincreasing)
    for m in range(0, 20):
        deltas = []
        for c in C_LADDER:
            j0 = J_cost(K, m, 5.0, c, kappa, h, I0, e_base, gamma, phi, 0.0, chi)
            j1 = J_cost(K, m + 1, 5.0, c, kappa, h, I0, e_base, gamma, phi, 0.0, chi)
            deltas.append(j1 - j0)
        assert is_nondecreasing(deltas), (m, deltas)
    return True


def check_topkis_on_pilots():
    """Exact discrete monotone gates on the published tightened-box pilots."""
    P = dict(DEFAULT_PRICES)
    for seed in range(20261122800, 20261122820):
        world = world_from_seed(seed)
        for K in range(P["K_max"] + 1):
            mw = m_star_ladder_in_w(world, P, W_LADDER, K)
            mc = m_star_ladder_in_c(world, P, C_LADDER, K)
            ml = m_star_ladder_in_lam(world, P, LAM_LADDER, K, w=1.0)
            th = W_threshold_at_K(
                K, P["c"], P["kappa"], P["h"], world["I0"], world["e_base"],
                world["gamma"], world["phi"], P["lam"], P["chi"], P["m_max"],
            )
            assert is_nondecreasing(mw), (seed, K, mw)
            assert is_nonincreasing(mc), (seed, K, mc)
            assert is_nondecreasing(ml), (seed, K, ml)
            assert mw[0] == 0 and mw[-1] >= 1, (seed, K, mw)
            assert W_LOW < th < W_HIGH, (seed, K, th)
        J = J_table(
            P["K_max"], P["m_max"], P4_W, P["c"], P["kappa"], P["h"],
            world["I0"], world["e_base"], world["gamma"], world["phi"],
            0.0, P["chi"],
        )
        star = argmin_discrete(J)
        assert star["n_ties"] == 1 and 2 <= star["m"] < P["m_max"]
        pi = exact_boltzmann(flatten_J(J), P4_BETA)
        st = occupation_m_stats(pi, P["m_max"], star["m"])
        assert st["marg_mode_m"] == star["m"]
        assert st["abs_err"] <= P4_TOL_M
    return True


def check_ct33_diagnostic():
    """With the cap slack, joint spend is nondecreasing and E nonincreasing
    in w (CT33), on the published pilots. Not an official gate for m*."""
    P = dict(DEFAULT_PRICES)
    for seed in range(20261122800, 20261122820):
        world = world_from_seed(seed)
        joint = joint_star_ladder_in_w(world, P, W_LADDER)
        assert is_nondecreasing(r["spend"] for r in joint)
        assert is_nonincreasing(r["E"] for r in joint)
    return True


def check_graph_connected():
    K_max, m_max = 3, 40
    edges = design_edges(K_max, m_max)
    n = (K_max + 1) * (m_max + 1)
    reach = connected_from(0, edges, n)
    assert len(reach) == n
    # every (K,0) is linked to every (K,m)
    for K in range(K_max + 1):
        i0 = design_index(K, 0, m_max)
        for m in range(1, m_max + 1):
            a, b = (i0, design_index(K, m, m_max))
            if a > b:
                a, b = b, a
            assert (a, b) in {(e[0], e[1]) if e[0] < e[1] else (e[1], e[0])
                              for e in edges} or True
    # cheaper: adjacency check
    pairs = {tuple(sorted(e)) for e in edges}
    for K in range(K_max + 1):
        for m in range(1, m_max + 1):
            assert tuple(sorted((design_index(K, 0, m_max),
                                 design_index(K, m, m_max)))) in pairs
    return True


def check_official_seeds_clean():
    seeds = list(range(20261122000, 20261122016))
    assert not any(seed_collides(s) for s in seeds)
    chains = [20261122400 + 1000 * i + 10 * 40 + c
              for i in range(16) for c in range(8)]
    assert not any(seed_collides(s) for s in chains)
    pilots = list(range(20261122800, 20261122820))
    assert not any(seed_collides(s) for s in pilots)
    # prior sets do collide
    assert seed_collides(1000)
    assert seed_collides(0)
    assert seed_collides(20261120)
    assert seed_collides(2026112100)
    assert seed_collides(20261121500)
    # official and pilot blocks must be disjoint
    assert set(seeds).isdisjoint(pilots)
    return True


def check_lock_hashes():
    lock_path = DIR / "LOCK.txt"
    assert lock_path.exists(), "LOCK.txt missing"
    lock = lock_path.read_text()
    for name in ("PREREG.md", "predictions.json", "run_sim1.py", "sim1_lib.py"):
        digest = hashlib.sha256((DIR / name).read_bytes()).hexdigest()
        assert digest in lock, (name, digest)
        sha_file = DIR / (name.split(".")[0].upper() + ".sha256")
        # optional sidecar; PREREG.sha256 etc. if present must match
    # sidecars if present
    mapping = {
        "PREREG.md": "PREREG.sha256",
        "predictions.json": "PREDICTIONS.sha256",
        "run_sim1.py": "RUN_SIM1.sha256",
        "sim1_lib.py": "SIM1_LIB.sha256",
    }
    for name, side in mapping.items():
        p = DIR / side
        if p.exists():
            digest = hashlib.sha256((DIR / name).read_bytes()).hexdigest()
            assert p.read_text().strip() == digest, side
    return True


def main():
    checks = [
        ("foc_formula", check_foc_formula),
        ("increasing_differences", check_increasing_differences),
        ("topkis_on_pilots", check_topkis_on_pilots),
        ("ct33_diagnostic", check_ct33_diagnostic),
        ("graph_connected", check_graph_connected),
        ("official_seeds_clean", check_official_seeds_clean),
        ("lock_hashes", check_lock_hashes),
    ]
    fails = []
    for name, fn in checks:
        try:
            fn()
            print(f"OK  {name}")
        except Exception as exc:
            print(f"FAIL  {name}: {exc}")
            fails.append(name)
    if fails:
        print("SOME FAILED")
        return 1
    print("ALL OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
