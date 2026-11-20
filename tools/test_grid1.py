"""GRID-1b: the recorded result implies the locked verdicts (raw data are not in git)."""
import json, pathlib
R = pathlib.Path(__file__).resolve().parents[1] / "theory/measured/grid/grid1b_results.json"

def test_grid1b_verdicts():
    r = json.loads(R.read_text())
    p = r["premise"]
    assert p["coverage_A"] >= 0.9 and p["corr_setpoint_vs_QA"] >= 0.9 and p["M_var_share"] < 0.05
    assert p["coverage_M"] < 0.9  # GRID-1 as locked + DV1: INVALID
    m = r["runs"]["main"]; lo, hi = m["boot_slowest"]["ci"]
    assert m["choice"] != "L0" and lo > 900          # G2-slow PASS
    assert lo > 1800                                  # rival R1-slow does not pass; discriminating
    th = max(t for t, _ in m["sep"])
    for k in ("M_dropped", "M_doubled", "H2_only"):
        t2 = max(t for t, _ in r["runs"][k]["sep"]); assert 0.5 < t2 / th < 2

def test_grid2_verdicts():
    r = json.loads((R.parent / "grid2_results.json").read_text())
    m = r["main"]; assert m["choice"] == "PL" and 1.7 <= m["gamma"] <= 2.3          # G1 FAIL
    for k in ("mfr_0.5", "mfr_1.5", "L_0.5", "L_1.5", "lag_FAT"):
        assert r[k]["choice"] == "PL" and 1.7 <= r[k]["gamma"] <= 2.3            # not INVALID
    s1 = r["S1"]; assert all(lo > 2900 or hi < 1300 for lo, hi in s1["ci"])      # M-S1 FAIL
