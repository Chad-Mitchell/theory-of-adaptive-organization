"""Runs theory/info_physics_checks/info_physics_checks.py."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_info_physics_checks_all_pass():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "theory", "info_physics_checks", "info_physics_checks.py")],
        capture_output=True, text=True, timeout=120,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL INFO-PHYSICS CHECKS PASS" in r.stdout
    assert "FAILS 0" in r.stdout
