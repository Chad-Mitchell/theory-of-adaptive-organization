"""Model S+ (theory/STORE_NOISE.md) checks pass; F2 scoring and the diagnostic rerun reproduce (theory/measured/ecoli/f2)."""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F2 = os.path.join(ROOT, "theory", "measured", "ecoli", "f2")


def test_store_noise_checks():
    out = subprocess.run([sys.executable, os.path.join(ROOT, "theory", "store_noise", "checks.py")],
                         capture_output=True, text=True, check=True)
    assert "ALL STORE_NOISE CHECKS PASS" in out.stdout


def test_interlacing_threshold_check():
    """THEORY v2.5.4 premise: lam*tau* = (1-s)/s at low SNR, shorter at any positive SNR (theory/store_noise/threshold_check.py)."""
    out = subprocess.run([sys.executable, os.path.join(ROOT, "theory", "store_noise", "threshold_check.py")],
                         capture_output=True, text=True, check=True)
    assert "ALL PASS" in out.stdout
    r = json.load(open(os.path.join(ROOT, "theory", "store_noise", "threshold_check.json")))
    assert r["faster_than_mode_iff"] == "s > 1/2" and r["ecoli_s"]["0.31"] == 2.226
    assert r["grid_37x13_max_ratio_to_closed_form"] < 1


def test_f2_park_score_and_rerun():
    subprocess.run([sys.executable, os.path.join(F2, "f2_score.py")], capture_output=True, text=True, check=True)
    r = json.load(open(os.path.join(F2, "f2_results.json")))
    p = r["park2010"]
    assert p["band_point"] == "neither" and 0.28 < p["s_rma"] < 0.34
    lo, hi = p["s_rma_boot95"]; assert 0.2 < lo < 0.26 and 0.35 < hi < 0.42
    subprocess.run([sys.executable, os.path.join(F2, "rerun_measured_s.py")], capture_output=True, text=True, check=True)
    q = json.load(open(os.path.join(F2, "rerun_results.json")))
    assert q["reference_verdict_at_point_s"]["verdict"] == "FAIL"
    assert q["reference_verdict_over_s_CI"]["verdict"].startswith("NEITHER")
    for k in ("s_lo", "s_point", "s_hi"):
        cf = q[k]["closed_form_low_snr_s"]; t = q[k]["tau_star_s"]
        assert all(abs(x / cf - 1) < 0.1 for x in t)


def test_followup_d_reproduces():
    D = os.path.join(ROOT, "theory", "measured", "ecoli", "d")
    subprocess.run([sys.executable, os.path.join(D, "d_calc.py")], capture_output=True, text=True, check=True)
    r = json.load(open(os.path.join(D, "d_results.json")))
    assert r["D1_celani_vergassola"]["verdict"] == "DOES NOT EXPLAIN" and r["D1_celani_vergassola"]["U"] < 0.6
    assert r["D2_gain_bounded_drift"]["verdict"] == "NEITHER"
    assert r["E2_speed_price"]["verdict_k1"] == "CONSISTENT" and r["E2_speed_price"]["verdict_k2"] == "MARGINAL"
