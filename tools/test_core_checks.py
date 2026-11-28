"""Runs theory/core_checks/core_checks.py, the checks of THEORY v2.0's closed forms (run: python3 -m pytest -q tools/test_core_checks.py)."""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_core_checks_all_ok():
    r = subprocess.run([sys.executable, os.path.join(ROOT, "theory", "core_checks", "core_checks.py")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL OK" in r.stdout
    assert "FAIL" not in r.stdout.replace("SOME FAILED", "")
