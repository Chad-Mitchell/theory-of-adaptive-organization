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
    S = pg.required_change(b, sigma)
    a = pg.analytic(b * S, sigma, fail_kappa=1.0)
    assert a["P_pass_true"] == pytest.approx(0.8, abs=1e-9)
    assert a["P_fail_null"] == pytest.approx(0.8, abs=1e-9)
    assert a["P_fail_true"] < 0.03 and a["P_pass_null"] < 0.03


def test_kappa_half_doubles_requirement():
    assert pg.required_change(0.5, 0.2, kappa=0.5) == pytest.approx(2 * pg.required_change(0.5, 0.2))


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
    d *= pg.required_change(b, sigma) / math.sqrt((d ** 2).sum())
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
    assert math.exp(pg.required_change(1 / 3, se_tot)) == pytest.approx(17.8, abs=0.05)
    assert 0.05 / (pg.z_two_sided(0.05) + pg.zq(0.8)) == pytest.approx(0.01785, abs=1e-5)
    assert pg.required_contrasts(1 / 3, se_tot, 0.4145515799784859) == 49


def test_wikidata_kg_zero_events():
    assert pg.zero_events_bound(40, 3.0) == pytest.approx(0.0306, abs=1e-4)   # RESULTS: 0.031/yr
    assert pg.zero_events_min_n(0.02, 3.0) == 63                              # RESULTS: n >= 63
    assert pg.zero_events_bound(63, 3.0) <= 0.02 < pg.zero_events_bound(62, 3.0)


def test_cli_exit_codes():
    tool = os.path.join(ROOT, "tools", "power_gate.py")
    bad = subprocess.run([sys.executable, tool, "contrast", "--sigma", "0.342", "--effect", "0.138", "--fail-eps", "0.05",
                          "--sims", "0"], capture_output=True, text=True)
    assert bad.returncode == 1 and json.loads(bad.stdout)["gate_met"] is False
    good = subprocess.run([sys.executable, tool, "contrast", "--sigma", "0.1", "--b", "0.3333", "--dlogx", "0.6", "0.6",
                           "--fail-kappa", "1", "--sims", "0"], capture_output=True, text=True)
    assert good.returncode == 0 and json.loads(good.stdout)["gate_met"] is True
    kg = subprocess.run([sys.executable, tool, "zero-events", "--n", "40", "--years", "3", "--bound", "0.02"],
                        capture_output=True, text=True)
    assert kg.returncode == 1 and json.loads(kg.stdout)["n_min"] == 63
