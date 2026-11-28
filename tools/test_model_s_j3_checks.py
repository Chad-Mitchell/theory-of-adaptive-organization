"""Runs tools/model_s_j3_checks.py (weak third mode, screen, no counterexample)."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_model_s_j3_checks_quick_pass():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "model_s_j3_checks.py")],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL J3 CHECKS PASS" in r.stdout
    assert "no certified counterexample" in r.stdout
    assert "weak third mode convex" in r.stdout
