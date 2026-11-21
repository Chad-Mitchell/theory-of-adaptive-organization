"""Runs theory/cross_field_checks/chow_map.py: the (world exponent, technology exponent) -> design-ratio map of theory/CROSS_FIELD_MAP_2026-11-21.md."""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_cross_field_map():
    r = subprocess.run(["nice", "-n", "19", sys.executable, os.path.join(ROOT, "theory", "cross_field_checks", "chow_map.py")],
                       capture_output=True, text=True, timeout=900)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "RESULT: PASS" in r.stdout
