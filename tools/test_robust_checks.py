"""Robustness extension (theory/ROBUSTNESS.md): R1 copies under component failure, R2 model
uncertainty, R3 lean versus robust, R4 antifragility. Checks live in theory/robust_checks/."""
import math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "theory", "robust_checks"))

import r1_redundancy as r1  # noqa: E402
import r2_ambiguity as r2  # noqa: E402
import r3_lean as r3  # noqa: E402
import r4_antifragile as r4  # noqa: E402


def test_r1_copies():
    r = r1.run()
    assert r["a_mismatches"] == 0 and r["a_monotone_w"] and r["a_monotone_h"]
    assert abs(r["a_slope_per_ln_w"] - r["a_slope_theory"]) < 0.05
    assert r["a_p_profile_ends"][0] == 1 and r["a_p_profile_ends"][2] == 1 and r["a_p_profile_ends"][1] > 1
    assert r["b_mismatches"] == 0 and r["b_nstar_mismatches"] == 0
    assert r["b_nR_vs_N"] == sorted(r["b_nR_vs_N"]) and r["b_nR_vs_N"][-1] > r["b_nR_vs_N"][0]
    assert r["c_feasible_any_n"] is False
    assert r["d_A_nE"] == 3 and r["d_A_n_by_B"][1.5] > r["d_A_nE"] and r["d_A_n_by_B"][50] == r["d_A_nE"]
    assert r["d_grid_tested"] >= 100
    assert r["d_viol_theta_below_nE"] == 0 and r["d_viol_nstar_formula"] == 0 and r["d_viol_monotone_in_B"] == 0
    for n, (mc, bound) in r["d_mc_ruin_vs_bound"].items():
        assert mc <= bound


def test_r2_ambiguity():
    r = r2.run()
    assert r["a_elasticity_on_foc"] == "-a/(8*A*x + 3*a)"
    for tag in ("nom", "wc"):
        assert r[f"a_{tag}_tau_decreasing"] and r[f"a_{tag}_B_increasing"] and r[f"a_{tag}_J_increasing"]
    assert r["a_nom_ratio_in_[(1+u)^(2/3),(1+u)]"]
    assert r["b_factor_decreasing_in_n"] and r["b_factor_vs_n"][5] > r["b_factor_vs_n"][1000] > 1
    assert abs(r["b_plugin_mc_n20"] - r["b_plugin_true_exceedance_n20"]) < 0.0006
    assert r["b_plugin_true_exceedance_n20"] > 3 * 1e-3
    assert r["c_viol_predictive_below_postmean_plugin"] == 0
    q = list(r["d_t_unitvar_quantiles_eps1e-3"].values())
    assert all(b < a for a, b in zip(q, q[1:])) and q[-1] > r["d_gauss_quantile"]
    assert r["d_cantelli_factor_eps1e-3"] > 10 * r["d_gauss_quantile"]


def test_r3_lean():
    r = r3.run()
    m = r["a_sigma_margin_by_B"]
    assert m[0.49] < 1e-6 and m[0.5] < 1e-6 and m[0.505] < 1e-6
    assert 0 < m[0.52] < m[0.6] < m[1.0] < m[5.0]
    assert r["a_bound_at_binding_sigma+1%"] > 1
    assert r["e_theta_decreasing_in_sigma_violations"] == 0
    assert r["e_tau_nonincreasing_in_u"] and r["e_cost_nondecreasing_in_u"]
    bm = [v["Bmin"] for v in r["e_robust_by_u"].values()]
    assert all(b > a for a, b in zip(bm, bm[1:]))


def test_r4_antifragility():
    r = r4.run()
    assert r["affine_in_a_at_fixed_design"] and r["Jstar_nondecreasing"]
    assert r["Jstar_concave_max_second_diff"] < 1e-9
    assert r["gap_vs_blind_nonneg"] and r["gap_nondecreasing"] and r["gap_convex_min_second_diff"] > -1e-9
    assert abs(r["regimes_fixed_design_cost"] - r["regimes_Jstar(abar)"]) < 1e-9
    assert r["regimes_redesign_cost"] < r["regimes_fixed_design_cost"]
