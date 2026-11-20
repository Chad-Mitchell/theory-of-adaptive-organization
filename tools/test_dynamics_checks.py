"""DYNAMICS (theory/DYNAMICS.md) checks: redesign band (CL19, CT41, CX9), lineage objective (CL20, CT42), discrete Bode (d5),
time average (CL21, CT43), and the two re-checked OVERREACH verdicts (Bode, barbell)."""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "theory", "dynamics_checks")


def run(name, marker):
    out = subprocess.run([sys.executable, os.path.join(D, name)], capture_output=True, text=True, check=True)
    assert marker in out.stdout, out.stdout[-2000:]


def test_d1_redesign_band():
    run("d1_redesign_band.py", "ALL D1 CHECKS PASS")
    r = json.load(open(os.path.join(D, "d1_results.json")))
    b, bg = r["D1a_bstar_closed_vs_grid"]; assert abs(bg / b - 1) < 1e-3 and abs(b - 0.495) < 1e-3
    up, down = r["D1c_with_switch_cost_up_down"]; assert up > 1.05 and down < 1 / 1.05      # hysteresis around w_c = 1
    t, tc = r["D1e_Tred_numeric_vs_sqrt_kappa_over_w"]; assert abs(t / tc - 1) < 0.02


def test_d2_lineage():
    run("d2_lineage.py", "ALL D2 CHECKS PASS")
    r = json.load(open(os.path.join(D, "d2_results.json")))
    assert abs(r["D2a_q_star_numeric_vs_closed"][1] - 0.26) < 1e-12
    assert r["D2b_indep_argmax"] == 0.0                         # independent shocks: per-unit and lineage agree
    assert [q for _, q in r["D2c_qstar_vs_shared_fraction"]][0] < 1e-3


def test_d3_time_average():
    run("d3_time_average.py", "ALL D3 CHECKS PASS")
    r = json.load(open(os.path.join(D, "d3_results.json")))
    assert r["D3c_scan_toy_nE_nG"] == [3, 4] and r["D3c_grid_counts"]["G_fewer"] == 0
    assert r["D3c_grid_max_extra_copies"] == 1


def test_d4_overreach():
    run("d4_overreach.py", "ALL D4 CHECKS PASS")
    r = json.load(open(os.path.join(D, "d4_results.json")))
    assert r["D4a_max_abs_S_over_40_random_worlds"] <= 1 + 1e-9
    assert all(g[3] < 1e-6 for g in r["D4b_mix_gain_continuous"])


def test_d3_share_by_X():
    r = json.load(open(os.path.join(D, "d3_results.json")))
    sh = {float(k): v[2] for k, v in r["D3c_grid_share_differ_by_X"].items()}
    assert sh[0.05] == 0.08 and sh[0.8] == 0.32                 # review should-fix 2: not confined to lumpy X


def test_d5_bode_discrete():
    run("d5_bode_discrete.py", "ALL D5 CHECKS PASS")
    r = json.load(open(os.path.join(D, "d5_results.json")))
    mx = [row[3] for row in r["D5a_scalar_AR1_a_q_r_maxS_at_meanlnS_identityerr"]]
    assert abs(min(mx) - 1.045) < 1e-3 and abs(max(mx) - 1.436) < 1e-3   # sampled reads: |S| > 1 (waterbed)
    assert r["D5b_random_worlds_maxS_min_max"][0] > 1 and r["D5b_random_worlds_max_abs_mean_lnS"] < 1e-6
