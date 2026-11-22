"""Runs theory/info_physics_checks/general_checks.py."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_general_checks_all_pass():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "theory", "info_physics_checks", "general_checks.py")],
        capture_output=True, text=True, timeout=120,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL GENERAL CHECKS PASS" in r.stdout
    assert "FAILS 0" in r.stdout
