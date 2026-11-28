"""Runs theory/area_law_probe_checks/area_law_probe_checks.py."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_area_law_probe_checks_all_pass():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "theory", "area_law_probe_checks", "area_law_probe_checks.py")],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL AREA-LAW-PROBE CHECKS PASS" in r.stdout
    assert "FAILS 0" in r.stdout
    out = os.path.join(ROOT, "theory", "area_law_probe_checks", "area_law_probe_checks.out")
    with open(out, encoding="utf-8") as f:
        expected = f.read()
    assert r.stdout == expected
