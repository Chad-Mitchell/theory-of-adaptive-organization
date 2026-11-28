"""Runs theory/meq_checks/meq_derive.py: each special case listed in THEORY v2.1 §5 derives from the master equation (run: python3 -m pytest -q tools/test_meq_derive.py)."""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_special_cases_derive_from_master_equation():
    r = subprocess.run([sys.executable, os.path.join(ROOT, "theory", "meq_checks", "meq_derive.py")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "RESULT: PASS" in r.stdout
    assert "FAIL " not in r.stdout
