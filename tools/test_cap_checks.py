"""Runs theory/antifragility_checks/cap_checks.py."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_cap_checks_all_pass():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "theory", "antifragility_checks", "cap_checks.py")],
        capture_output=True, text=True, timeout=180,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL CAP CHECKS PASS" in r.stdout
    assert "FAILS 0" in r.stdout
    assert "Q1 official YES" in r.stdout
