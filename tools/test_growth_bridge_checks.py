"""Runs tools/growth_bridge_checks.py (expansion, ruin, coordinates)."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_growth_bridge_checks_all_pass():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "growth_bridge_checks.py")],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL GROWTH-BRIDGE CHECKS PASS" in r.stdout
    assert "FAILS 0" in r.stdout
