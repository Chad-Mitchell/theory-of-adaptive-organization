"""Tests for tools/power_gate.py (run: python3 -m pytest -q tools/test_power_gate.py)."""
import json, math, os, subprocess, sys
import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import power_gate as pg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAISO = json.load(open(os.path.join(ROOT, "tests", "STAKES_SHIFT_CAISO", "results.json")))


def test_minimal_formula_hits_power_exactly():
    b, sigma = 1 / 3, 0.3
    S = pg.required_change(b, sigma, kappa=1.0)   # both rules bind exactly only at kappa = 1 (formula check)
    a = pg.analytic(b * S, sigma, fail_kappa=1.0)
    assert a["P_pass_true"] == pytest.approx(0.8, abs=1e-9)
    assert a["P_fail_null"] == pytest.approx(0.8, abs=1e-9)
    assert a["P_fail_true"] < 0.03 and a["P_pass_null"] < 0.03


def test_kappa_half_doubles_requirement():
    assert pg.required_change(0.5, 0.2, kappa=0.5) == pytest.approx(2 * pg.required_change(0.5, 0.2, kappa=1.0))


@pytest.mark.parametrize("eff,sig,kw", [(0.5, 0.2, {"fail_kappa": 1.0}), (0.14, 0.34, {"fail_eps": 0.05}),
                                        (0.9, 0.3, {"fail_kappa": 0.5, "band_top": 1.4})])
def test_simulation_matches_analytic(eff, sig, kw):
    a = pg.analytic(eff, sig, **kw)
    s = pg.simulate(eff, sig, sims=400_000, seed=7, **kw)
    for k in ("P_pass_true", "P_fail_null", "P_fail_true", "P_pass_null"):
        assert s[k] == pytest.approx(a[k], abs=0.004), k


def test_panel_slope_power_matches_formula():
    # K independent contrasts, through-origin LS slope; at S = S_req both rules reach 0.8.
    rng = np.random.default_rng(3)
    b, sigma = 1 / 3, 0.32
    d = rng.uniform(-0.6, 0.6, 30)
    d *= pg.required_change(b, sigma, kappa=1.0) / math.sqrt((d ** 2).sum())   # FAIL rule below is kappa = 1
    S = math.sqrt((d ** 2).sum()); se = sigma / S; z = pg.z_two_sided(0.05)
    sims = 40_000
    for btrue, rule, want in ((b, "pass", 0.8), (0.0, "fail", 0.8)):
        D = btrue * d + rng.normal(0, sigma, (sims, d.size))
        bh = (D * d).sum(1) / S ** 2
        hit = (bh - z * se > 0) if rule == "pass" else (bh + z * se < b)
        assert hit.mean() == pytest.approx(want, abs=0.01)


def test_caiso_pick15_numbers():
    se_tot, s_yr = CAISO["noise"]["se_tot"], CAISO["noise"]["s_yr"]
    pairs = list(CAISO["year_pairs"].values())
    assert np.std(pairs, ddof=1) == pytest.approx(s_yr, rel=1e-9)
    assert math.hypot(s_yr, CAISO["primary"]["se_boot"]) == pytest.approx(se_tot, rel=1e-9)
    Dp = CAISO["prediction"]["D_pred"]
    assert Dp == pytest.approx(-CAISO["stakes_clean"]["dlogw_2025_vs_2024"]["est"] / 3, rel=1e-9)
    a = pg.analytic(Dp, se_tot, fail_eps=0.05, band_top=CAISO["prediction"]["band"][1])
    assert a["pass_region_empty"]                     # band top 0.352 < 1.96 * 0.342 = 0.671
    assert a["P_pass_true"] == 0.0
    assert a["P_fail_null"] == pytest.approx(0.0348, abs=5e-4)
    assert not a["best_case_fail_fires"]
    # the item's "~7x": the stakes change at which PASS fires half the time (no band)
    assert math.exp(1.96 * se_tot * 3) == pytest.approx(7.5, abs=0.05)
    assert math.exp(pg.required_change(1 / 3, se_tot, kappa=1.0)) == pytest.approx(17.8, abs=0.05)   # pre-v1.4.7 kappa = 1
    assert 0.05 / (pg.z_two_sided(0.05) + pg.zq(0.8)) == pytest.approx(0.01785, abs=1e-5)
    assert pg.required_contrasts(1 / 3, se_tot, 0.4145515799784859, kappa=1.0) == 49


def test_wikidata_kg_zero_events():
    assert pg.zero_events_bound(40, 3.0) == pytest.approx(0.0306, abs=1e-4)   # RESULTS: 0.031/yr
    assert pg.zero_events_min_n(0.02, 3.0) == 63                              # RESULTS: n >= 63
    assert pg.zero_events_bound(63, 3.0) <= 0.02 < pg.zero_events_bound(62, 3.0)


def test_cli_exit_codes():
    tool = os.path.join(ROOT, "tools", "power_gate.py")
    bad = subprocess.run([sys.executable, tool, "contrast", "--sigma", "0.342", "--effect", "0.138", "--fail-eps", "0.05",
                          "--sims", "0"], capture_output=True, text=True)
    assert bad.returncode == 1 and json.loads(bad.stdout)["gate_met"] is False
    good = subprocess.run([sys.executable, tool, "contrast", "--sigma", "0.1", "--b", "0.3333", "--dlogx", "1.3", "1.3",
                           "--fail-kappa", "0.5", "--sims", "0"], capture_output=True, text=True)
    assert good.returncode == 0 and json.loads(good.stdout)["gate_met"] is True
    k1 = subprocess.run([sys.executable, tool, "contrast", "--sigma", "0.1", "--b", "0.3333", "--dlogx", "1.3", "1.3",
                         "--fail-kappa", "1", "--sims", "0"], capture_output=True, text=True)
    assert k1.returncode == 1 and json.loads(k1.stdout)["kappa_in_N6_range"] is False   # v1.4.7: kappa <= 1/2
    kg = subprocess.run([sys.executable, tool, "zero-events", "--n", "40", "--years", "3", "--bound", "0.02"],
                        capture_output=True, text=True)
    assert kg.returncode == 1 and json.loads(kg.stdout)["n_min"] == 63


# ---- v1.4.7 (CAUSAL-KILL-MAGNITUDE-REVIEW): default kappa = 1/2, N6 range, s*lam scaling ----
def test_default_kappa_is_half():
    assert pg.DEFAULT_KAPPA == 0.5
    assert pg.required_change(0.5, 0.2) == pytest.approx(pg.required_change(0.5, 0.2, kappa=0.5))
    a = pg.analytic(1.0, 0.2)
    assert a["fail_threshold"] == pytest.approx(0.5)
    r = pg.gate(1.0, 0.1)
    assert r["kappa_used"] == 0.5 and r["kappa_in_N6_range"] is True


@pytest.mark.parametrize("k,ok", [(0.0, False), (0.25, True), (0.5, True), (0.51, False), (1.0, False)])
def test_kappa_range(k, ok):
    assert pg.kappa_in_n6_range(k) is ok
    r = pg.gate(5.0, 0.1, fail_kappa=k)          # huge SNR: only the range can fail it (k = 0 makes FAIL|null ~ size)
    if k > 0:
        assert r["gate_met"] is ok


def test_absolute_margin_not_flagged_as_n6():
    r = pg.gate(0.138, 0.342, fail_eps=0.05)
    assert r["kappa_in_N6_range"] is None and r["gate_met"] is False


def test_kappa_one_kills_true_design_under_partial_adjustment_half_does_not():
    # first principles: true move b*s, unscaled threshold kappa*b; lag tau/2 => s = 0.39
    s = 1 - math.exp(-0.5); b, sig = 1.0, 0.1
    a1 = pg.analytic(b * s, sig, fail_eps=1.0 * b)        # kappa = 1, prediction not scaled by s
    ah = pg.analytic(b * s, sig, fail_eps=0.5 * b * s)    # kappa = 1/2, prediction scaled by s
    assert a1["P_fail_null"] > 0.99 and pg.Phi((1.0 * b - z_(0.05) * sig - b * s) / sig) > 0.99
    assert pg.Phi((0.5 * b * s - z_(0.05) * sig - b * s) / sig) < 0.01 and ah["P_fail_true"] < 0.01


def z_(alpha):
    return pg.z_two_sided(alpha)


def test_cli_scale_and_required_default():
    tool = os.path.join(ROOT, "tools", "power_gate.py")
    r = subprocess.run([sys.executable, tool, "required", "--sigma", "0.3", "--b", "0.5", "--scale", "0.5"],
                       capture_output=True, text=True)
    out = json.loads(r.stdout)
    assert out["kappa_used"] == 0.5 and out["kappa_in_N6_range"] is True
    assert out["S_req_log"] == pytest.approx(pg.required_change(0.25, 0.3, kappa=0.5))


def test_optimality_form_keeps_kappa_one_and_spf_rigidity_record():
    # optimality form (MV10 "Delta >= 2.80 sigma") keeps kappa = 1 and no N6 range check
    r = pg.gate(1.0, 0.3, form="optimality")
    assert r["kappa_used"] == 1.0 and r["kappa_in_N6_range"] is None
    assert r["analytic"]["fail_threshold"] == pytest.approx(1.0)
    with pytest.raises(ValueError):
        pg.gate(1.0, 0.3, form="other")
    # SPF-RIGIDITY-OOS power.py (optimality form) reproduces its recorded best-case gate numbers
    rec = json.load(open(os.path.join(ROOT, "tests", "SPF_RIGIDITY_OOS", "results", "power.json")))
    found = []
    def walk(o):
        if isinstance(o, dict):
            if "power_gate_tool_best_case" in o and "se_c_sampling_only" in o:
                found.append(o)
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(rec)
    assert found
    for o in found:
        g = pg.gate(1.5, o["se_c_sampling_only"], form="optimality")["analytic"]
        assert g["P_fail_null"] == pytest.approx(o["power_gate_tool_best_case"]["P_fail_null"], abs=1e-9)
        assert g["P_pass_true"] == pytest.approx(o["power_gate_tool_best_case"]["P_pass_true"], abs=1e-9)


def test_rival_line_pick35_numbers_unreachable_and_kalman_reachable():
    # pick 35 (CAUSAL-NULL-INVARIANCE): Bayes move 0.350, sigma 0.028, kappa_F 1/2 -> kill line 0.175.
    # 0-1-best linear rival moves +0.244..+0.284 -> FAIL cannot reach it at any n; MSE-best (Kalman) rival -0.071 -> reached.
    for r in (0.244, 0.284):
        g = pg.gate(0.350, 0.028, rival_effect=r)
        assert g["gate_met"] and g["rival"]["rival_unreachable_any_n"] and not g["rival"]["discriminates_rival"]
        assert g["rival"]["P_fail_rival"] < 1e-3
    g = pg.gate(0.350, 0.028, rival_effect=-0.071)
    assert g["rival"]["discriminates_rival"] and g["rival"]["P_fail_rival"] > 0.999


def test_rival_line_absent_by_default_and_cli():
    assert "rival" not in pg.gate(0.35, 0.028)
    assert pg.main(["contrast", "--sigma", "0.028", "--effect", "0.35", "--rival-effect", "0.26", "--sims", "0"]) == 0

def test_mirror_pass_same_gate_at_kappa_le_half():
    # CAUSAL-KAPPA-LENIENCY (pick 38): mirror PASS (D - z sigma > kappa*effect) needs (1-kappa)SNR >= z+z_pi; for
    # kappa <= 1/2 the FAIL leg (kappa*SNR >= z+z_pi) binds, so the minimal gate is unchanged.
    zp = pg.z_two_sided(0.05) + pg.zq(0.8)
    for k in (0.1, 0.25, 0.5):
        eff = zp / k * 1.0001
        g = pg.gate(eff, 1.0, fail_kappa=k)
        assert g["gate_met"] and g["mirror_pass"]["pass_reachable_mirror"]
        g = pg.gate(eff * 0.98, 1.0, fail_kappa=k)
        assert not g["gate_met"]
    m = pg.mirror_pass(5.6, 1.0, fail_kappa=0.5)
    assert abs(m["P_pass_true_mirror"] - pg.Phi(0.5 * 5.6 - 1.959964)) < 1e-6


def test_mirror_pass_rereads_aklmt_as_inconclusive():
    # LAB-AKLMT-TAU primary: D 0.5182, sigma 0.0479, b_opt 0.9835 -> current PASS, mirror INCONCLUSIVE (lo 0.424 < 0.492).
    D, s, b = 0.5182, 0.0479, 0.9835
    assert D - 1.96 * s > 0 and D + 1.96 * s > 0.5 * b and not (D - 1.96 * s > 0.5 * b)
    assert "mirror_pass" not in pg.gate(0.35, 0.028, fail_eps=0.05)
