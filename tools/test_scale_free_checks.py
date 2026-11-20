"""Runs theory/meq_checks/scale_free_checks.py: THEORY v2.2 CT24 (cost shares, looking : being wrong = alpha - 1, floor multiplier) and CT25 (temperature as the ruin constraint)."""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_cost_shares_and_temperature_corollary():
    r = subprocess.run(["nice", "-n", "19", sys.executable, os.path.join(ROOT, "theory", "meq_checks", "scale_free_checks.py")],
                       capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "RESULT: PASS" in r.stdout
