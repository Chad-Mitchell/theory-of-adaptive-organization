#!/usr/bin/env python3
"""Build locked predictions.json from HOLO PREREG.md world tables.

No optimize_K, no E_K. Band centres and world poles only.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np

DIR = Path(__file__).resolve().parent
REPO = DIR.parents[2]
MERGED = REPO / "theory" / "layers_checks" / "stores.py"

spec = importlib.util.spec_from_file_location("stores_merged_t20", MERGED)
stores = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stores)

BASE_SEED = 2026112020
R_GRID = [float(10 ** (i / 2)) for i in range(17)]
TAU_MIN = 1.0


def n_dec_of(Gamma):
    return float(np.log10(Gamma))


def k_cap(J, n_dec):
    return int(min(J, max(8, int(n_dec) + 6)))


def band_centres(Gamma, n_bands, tau_min=TAU_MIN):
    n_dec = n_dec_of(Gamma)
    mid = [float(tau_min * 10 ** (d + 0.5)) for d in range(n_bands)]
    span = [
        float(tau_min * 10 ** (n_dec * (k) / (n_bands - 1)))
        for k in range(n_bands)
    ]
    return mid, span


def family_s(wid, alpha, N, Gamma=1e4, per_decade=4, role="primary"):
    a, v = stores.scalefree_world(alpha, Gamma, per_decade=per_decade, tau_min=TAU_MIN)
    a = np.asarray(a, float)
    v = np.asarray(v, float)
    J = int(len(a))
    n_dec = n_dec_of(Gamma)
    n_bands = int(round(n_dec))
    mid, span = band_centres(Gamma, n_bands)
    b_strict = abs(alpha - 1.0) < 1e-12 and "primary" in role
    return dict(
        id=wid,
        family="S",
        role=role,
        alpha=float(alpha),
        N=float(N),
        Gamma=float(Gamma),
        per_decade=int(per_decade),
        tau_min=TAU_MIN,
        M=None,
        a=a.tolist(),
        v=v.tolist(),
        tau=(1.0 / a).tolist(),
        J=J,
        n_dec=float(n_dec),
        n_bands=n_bands,
        K_cap=k_cap(J, n_dec),
        band_centres_mid=mid,
        band_centres_span=span,
        B_strict=bool(b_strict),
        predicted_K_set=None,
        A_must_not_pass=False,
        B_is_not_a_test=False,
    )


def family_m(wid, alpha, N, Gamma=1e4, M=16, role="primary"):
    n_dec = n_dec_of(Gamma)
    tau = TAU_MIN * np.logspace(0, np.log10(Gamma), M)
    a = 1.0 / tau
    v = tau ** (alpha - 1.0)
    v = v / v.sum()
    J = int(M)
    n_bands = int(round(n_dec))
    mid, span = band_centres(Gamma, n_bands)
    b_strict = abs(alpha - 1.0) < 1e-12 and "primary" in role
    return dict(
        id=wid,
        family="M",
        role=role,
        alpha=float(alpha),
        N=float(N),
        Gamma=float(Gamma),
        per_decade=None,
        tau_min=TAU_MIN,
        M=int(M),
        a=a.tolist(),
        v=v.tolist(),
        tau=tau.tolist(),
        J=J,
        n_dec=float(n_dec),
        n_bands=n_bands,
        K_cap=k_cap(J, n_dec),
        band_centres_mid=mid,
        band_centres_span=span,
        B_strict=bool(b_strict),
        predicted_K_set=None,
        A_must_not_pass=False,
        B_is_not_a_test=False,
    )


def nc_single(wid, N):
    a = np.array([1.0])
    v = np.array([1.0])
    return dict(
        id=wid,
        family="NC",
        role="validity",
        alpha=None,
        N=float(N),
        Gamma=1.0,
        per_decade=None,
        tau_min=TAU_MIN,
        M=None,
        a=a.tolist(),
        v=v.tolist(),
        tau=[1.0],
        J=1,
        n_dec=0.0,
        n_bands=1,
        K_cap=1,  # min(1, max(8, 6)) = 1
        band_centres_mid=[],
        band_centres_span=[],
        B_strict=False,
        predicted_K_set=[0, 1],
        A_must_not_pass=True,
        B_is_not_a_test=True,
    )


def nc_narrow(wid, N):
    tau = np.array([1.0, 10 ** 0.1])
    a = 1.0 / tau
    v = np.array([0.5, 0.5])
    return dict(
        id=wid,
        family="NC",
        role="validity",
        alpha=None,
        N=float(N),
        Gamma=float(10 ** 0.1),
        per_decade=None,
        tau_min=TAU_MIN,
        M=None,
        a=a.tolist(),
        v=v.tolist(),
        tau=tau.tolist(),
        J=2,
        n_dec=0.1,
        n_bands=0,
        K_cap=2,  # min(2, max(8, 6)) would be 2 if we special-case n_dec; locked here as 2
        band_centres_mid=[],
        band_centres_span=[],
        B_strict=False,
        predicted_K_set=[0, 1, 2],
        A_must_not_pass=True,
        B_is_not_a_test=True,
    )


def main():
    worlds = []
    # Family S primary, table order in PREREG §3.1
    for alpha, N, tag in [
        (0.5, 1e-4, "S_a05_N1e-4"),
        (0.5, 1e-6, "S_a05_N1e-6"),
        (1.0, 1e-4, "S_a10_N1e-4"),
        (1.0, 1e-6, "S_a10_N1e-6"),
        (1.5, 1e-4, "S_a15_N1e-4"),
        (1.5, 1e-6, "S_a15_N1e-6"),
    ]:
        worlds.append(family_s(tag, alpha, N))
    # Family M primary, §3.2
    for alpha, N, tag in [
        (0.5, 1e-4, "M_a05_N1e-4"),
        (0.5, 1e-6, "M_a05_N1e-6"),
        (1.0, 1e-4, "M_a10_N1e-4"),
        (1.0, 1e-6, "M_a10_N1e-6"),
        (1.5, 1e-4, "M_a15_N1e-4"),
        (1.5, 1e-6, "M_a15_N1e-6"),
    ]:
        worlds.append(family_m(tag, alpha, N))
    # NC §3.3
    worlds.append(nc_single("NC_single_N1e-4", 1e-4))
    worlds.append(nc_single("NC_single_N1e-6", 1e-6))
    worlds.append(nc_narrow("NC_narrow_N1e-4", 1e-4))
    # Secondary §3.4
    worlds.append(family_s("S_a10_N1e-3", 1.0, 1e-3, role="secondary"))
    worlds.append(
        family_s(
            "S_a10_N1e-4_G5",
            1.0,
            1e-4,
            Gamma=1e5,
            per_decade=4,
            role="secondary",
        )
    )
    worlds.append(
        family_s(
            "S_a10_N1e-4_pd8",
            1.0,
            1e-4,
            Gamma=1e4,
            per_decade=8,
            role="secondary",
        )
    )

    for i, w in enumerate(worlds):
        w["index"] = i
        w["optimizer_seed_K"] = "BASE_SEED + 1000*index + 17*K"

    # Sanity on K_cap and J against the prereg text
    checks = {}
    for w in worlds:
        if w["id"].startswith("S_a") and w["role"] == "primary":
            assert w["J"] == 17, (w["id"], w["J"])
            assert w["K_cap"] == 10, (w["id"], w["K_cap"])
            assert w["n_bands"] == 4
        if w["id"].startswith("M_a") and w["role"] == "primary":
            assert w["J"] == 16, (w["id"], w["J"])
            assert w["K_cap"] == 10
            assert w["n_bands"] == 4
        if w["id"] == "S_a10_N1e-4_G5":
            assert w["J"] == 21, w["J"]
            assert w["K_cap"] == 11, w["K_cap"]
            assert w["n_bands"] == 5
        if w["id"] == "S_a10_N1e-4_pd8":
            assert w["J"] == 33, w["J"]
            assert w["K_cap"] == 10
            assert w["n_bands"] == 4
        if w["id"].startswith("NC_single"):
            assert w["K_cap"] == 1 and w["J"] == 1
        if w["id"].startswith("NC_narrow"):
            assert w["K_cap"] == 2 and w["J"] == 2

    pred = dict(
        locked_note=(
            "T20 holographic/fractal predictions from world parameters only. "
            "No E_K, no store-rate optimization, no look at ε curves. "
            "Gates are those in PREREG.md §§5.1–5.6. Band centres from τ_min, Γ, n_bands."
        ),
        BASE_SEED=BASE_SEED,
        R_grid=R_GRID,
        R_grid_rule="R_i = 10**(i/2) for i=0..16",
        tau_min=TAU_MIN,
        TOL_convexity=1e-4,
        solver="theory/layers_checks/stores.py + s5_rerun.py optimize_K style",
        de_maxiter_K_le_6=25,
        de_for_K_gt_6=False,
        store_sep=1.02,
        gates=dict(
            A=dict(
                monotone=True,
                growth_min=3,
                distinct_min=4,
                max_jump=2,
                slope_lo=0.25,
                slope_hi=2.0,
                mae_max=1.0,
                family_pass_min=5,
                family_pass_of=6,
            ),
            B_strict=dict(
                cv_max=0.5,
                mean_spacing_factor_lo=0.5,
                mean_spacing_factor_hi=2.0,
                coverage_slack=1.5,
                hausdorff_mid_max=0.75,
                hausdorff_span_max=0.50,
                evaluate_at="K=n_bands",
                family_pass="both alpha=1 primary B-strict AND at least 4/6 primary B-strict",
            ),
            B_tilted=dict(
                cv_max=0.75,
                hausdorff_mid_max=1.00,
                hausdorff_span_max=0.75,
                descriptive_only=True,
            ),
            C=dict(
                rule="N60-from-0 equals leftmost argmin or a co-minimizer, when convex at 1e-4",
                family_pass="every convex primary world passes C, and at least 5/6 primary worlds convex",
                not_evidence_for_holography=True,
            ),
        ),
        worlds=worlds,
        n_worlds=len(worlds),
        order="Family S primary, Family M primary, NC, Family S secondary, as PREREG §3",
    )

    out = DIR / "predictions.json"
    with open(out, "w") as f:
        json.dump(pred, f, indent=1)
        f.write("\n")
    print(f"wrote {out} n_worlds={len(worlds)}")
    for w in worlds:
        print(
            f"  {w['index']:2d} {w['id']:20s} fam={w['family']} J={w['J']:2d} "
            f"K_cap={w['K_cap']:2d} n_bands={w['n_bands']} N={w['N']} role={w['role']}"
        )


if __name__ == "__main__":
    main()
