"""pytest for tools/coadaptation_checks.py (theory/COADAPTATION.md). Run at nice 19."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import coadaptation_checks as C  # noqa: E402


def test_s1_gibbs_in_beta_scaled_potential_and_speed_free():
    r = C.s1_gibbs_two_parties()
    assert r["kolmogorov_matched"] < 1e-10
    assert r["matched_max_rel_err_over_speeds"] < 1e-6
    assert r["matched_speed_dependence_tv"] < 1e-9
    assert r["kolmogorov_mismatch"] > 1.0
    assert r["mismatch_speed_dependence_tv"] > 1e-3


def test_s1c_reversible_iff_beta_scaled_exact_potential():
    r = C.s1c_random_iff()
    assert r["agree"] == r["trials"]
    assert r["potential_reversible"] == r["trials"] // 2
    assert r["random_reversible"] == 0


def test_s2_regret_potential_and_team_split():
    r = C.s2_regret_and_team()
    assert abs(r["E_regret1"] / r["pred1"] - 1) < 0.01
    assert abs(r["E_regret2"] / r["pred2"] - 1) < 0.01
    assert abs(r["E_Psi_excess"] - r["pred_Psi"]) < 0.01
    assert abs(r["E_team_excess"] / r["pred_team"] - 1) < 0.01
    assert r["poa_gap"] > 0


def test_s3_explicit_moran_populations_match_gibbs():
    r = C.s3_moran_population_mc()
    assert r["tv"] < 0.04


def test_s4_matching_pennies_never_settles():
    r = C.s4_matching_pennies()
    for b, v in r.items():
        assert abs(v["E_J1"] - 0.5) < 1e-9 and abs(v["E_J2"] - 0.5) < 1e-9
        assert v["cycle_current"] > 0.01


def test_s5a_potential_lq_speed_free():
    assert C.s5a_potential_speed_free()["max_err_vs_gibbs"] < 1e-10


def test_s5b_opposed_coupling_virial_and_speed_dependence():
    r = C.s5b_opposed_virial()
    for v in r["sigma_by_speed"].values():
        assert all(abs(x - 1) < 1e-9 for x in v["virial"])
    assert r["speed_spread"] > 0.05
    assert all(abs(x - 1) < 0.03 for x in r["mc_virial"])
    assert r["mc_cov_err"] < 0.03 * r["mc_cov_scale"]


def test_s5c_team_mismatch_bound():
    r = C.s5c_team_mismatch()
    assert r["violations"] == 0
    assert r["equal_strength_err"] < 1e-9


def test_s5d_cyclic_chase_hopf_at_c_2():
    r = C.s5d_cyclic_chase()
    assert r[1.5]["stable"] and r[1.9]["stable"]
    assert not r[2.1]["stable"] and not r[3.0]["stable"]


def test_s5e_world_gain_saddle():
    r = C.s5e_world_gain()
    assert all(v["potential"] for v in r.values())
    assert r[0.5]["stable"] and r[0.9]["stable"]
    assert not r[1.1]["stable"] and not r[2.0]["stable"]


def test_s5f_delay_hayes_bound():
    r = C.s5f_delay()
    assert abs(r["k_tau_crit"] - math.acos(-0.5) / math.sqrt(3)) < 1e-12
    assert r[0.8]["late_over_early"] < 1e-2
    assert r[1.2]["late_over_early"] > 10


def test_s5g_nonlinear_virial():
    r = C.s5g_nonlinear_virial()
    assert all(abs(x - 1) < 0.03 for x in r[0.0])
    assert all(abs(x - 1) < 0.05 for x in r[1.0])


def test_s5h_ct34_free_energy_and_factorisation():
    r = C.s5h_ct34_lift()
    assert r["tv_free_energy"] < 1e-9
    assert r["tv_upkeep_only"] > 0.01
    assert abs(r["team_scatter_fixed_theta"] - r["pred_team_scatter"]) < 1e-6


def test_s6a_nonlinear_monotone_hodge_split():
    r = C.s6a_nonlinear_monotone_hodge()
    for v in r.values():
        assert abs(v["virial_sum"] - 2.0) < 0.03
        assert v["E_r2"] <= v["bound_r2"]
        assert v["bound_Psi_lo"] - 0.02 <= v["E_Psi"] <= v["bound_Psi_hi"] + 0.02
        assert v["regret"][0] <= v["regret_bound"][0]
        assert v["regret"][1] <= v["regret_bound"][1]
    assert abs(r["a=2.0,b=0.0,v=(1.0, 0.3)"]["E_Psi"] - 1.0) < 0.02


def test_s6b_nonlinear_monotone_drift():
    r = C.s6b_nonlinear_monotone_drift()
    assert abs(r["virial"] - r["pred_virial"]) < 0.05
    assert r["E_r2"] <= r["bound_r2"]
    assert r["bound_Psi_lo"] <= r["E_Psi"] <= r["bound_Psi_hi"]


def test_s7a_perturbative_tree_bound():
    r = C.s7a_perturbative_tree_bound()
    assert r["trials"] == 100 and r["violations"] == 0


def test_s7b_single_basin_low_temp():
    r = C.s7b_single_basin_low_temp()
    assert r[2] < r[8] < r[32] < r[128]
    assert r[128] > 0.999


def test_s7c_single_basin_bracket_false():
    r = C.s7c_single_basin_bracket_false()
    assert abs(sum(r["local_a"]) - r["local_var"]) < 1e-12
    assert r["local_a"][1] < 0
    assert round(r["local_a2_over_var"], 5) == -0.01130
    assert all(x["excess"] > 0 for x in r["local_eps"])
    assert r["adv"]["E"] > r["adv"]["hi"]
    assert r["adv"]["rel_violation"] > 0.15
    ratios = [row["ratio"] for row in r["entropic"]]
    assert ratios == sorted(ratios) and ratios[-1] > 30.0
    m64 = next(row for row in r["entropic"] if row["m"] == 64)
    assert round(m64["ratio"], 2) == 34.64
    assert round(r["entropic_ratio_m_inf_barrier_held"], 1) == 415.8


def test_s7d_pl_flux_bound():
    r = C.s7d_pl_flux_bound()
    assert r["trials"] == 400 and r["violations"] == 0
    assert r["median_tightness"] < 0.2


def test_s7e_tree_graph_exact():
    r = C.s7e_tree_graph_exact()
    assert r["tv_err"] < 1e-12 and r["detailed_balance_err"] < 1e-12


def test_s8a_lq_drift_coadapt():
    r = C.s8a_lq_drift_coadapt()
    assert r["trials"] == 2000
    assert r["pot_rel_err"] < 1e-11
    assert r["virial_err"] < 1e-11
    assert r["bracket_violations"] == 0


def test_s8b_lq_drift_regret_negative():
    r = C.s8b_lq_drift_regret_negative()
    assert abs(r["static_regret_1"] - r["static_pred_1"]) < 1e-12
    assert abs(r["static_regret_2"] - r["static_pred_2"]) < 1e-12
    assert abs(r["regret_1"] - r["naive_1"]) > 1e-3
    assert abs(r["regret_2"] - r["naive_2"]) > 1e-2


def test_s9_f6_resistance_trees():
    r = C.s9_f6_resistance_trees()
    sp = r["stochastic_potentials"]
    assert abs(sp["(0, 0)"] - 2.1) < 1e-12
    assert abs(sp["(1, 1)"] - 1.0) < 1e-12
    for row in r["slopes"]:
        assert abs(row["slope"] - 1.1) < 1e-9
    scan = {row["c2_over_c1"]: row["pi_B"] for row in r["threshold_scan"]}
    assert scan[1.3] < 0.05 and scan[1.4] < 0.4 and scan[1.46] > 0.6 and scan[1.6] > 0.98
