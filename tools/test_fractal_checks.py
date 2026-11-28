"""Runs theory/fractal_checks/fractal_checks.py. Run at nice 19 in the suite."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_fractal_checks_required_pass():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "theory", "fractal_checks", "fractal_checks.py")],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL REQUIRED FRACTAL CHECKS PASS" in r.stdout
    assert "REQUIRED FAILS 0" in r.stdout
    # The lock's own bands that contradict its closed forms stay visible.
    assert "PUZZLE  carpet band |per-13.8|<0.01 at n=4" in r.stdout
    assert "PUZZLE  carpet gap from 13.8*df/2 exceeds 2" in r.stdout
    assert "PUZZLE  gasket gap ratio g=3" in r.stdout
    assert "PUZZLE  gasket gap ratio g=4" in r.stdout
