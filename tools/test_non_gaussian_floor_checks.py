"""Runs theory/non_gaussian_floor_checks/non_gaussian_floor_checks.py."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_non_gaussian_floor_checks_all_pass():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "theory", "non_gaussian_floor_checks", "non_gaussian_floor_checks.py")],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL NON-GAUSSIAN-FLOOR CHECKS PASS" in r.stdout
    assert "FAILS 0" in r.stdout
    out = os.path.join(ROOT, "theory", "non_gaussian_floor_checks", "non_gaussian_floor_checks.out")
    with open(out, encoding="utf-8") as f:
        expected = f.read()
    assert r.stdout == expected
