"""Model S+ (theory/STORE_NOISE.md) checks pass; F2 scoring and the diagnostic rerun reproduce (theory/measured/ecoli/f2)."""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F2 = os.path.join(ROOT, "theory", "measured", "ecoli", "f2")


def test_store_noise_checks():
    out = subprocess.run([sys.executable, os.path.join(ROOT, "theory", "store_noise", "checks.py")],
                         capture_output=True, text=True, check=True)
    assert "ALL STORE_NOISE CHECKS PASS" in out.stdout


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
