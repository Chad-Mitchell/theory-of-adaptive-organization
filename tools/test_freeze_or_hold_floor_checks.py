"""Runs theory/freeze_or_hold_floor_checks/freeze_or_hold_floor_checks.py."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_freeze_or_hold_floor_checks_all_pass():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "theory", "freeze_or_hold_floor_checks", "freeze_or_hold_floor_checks.py")],
        capture_output=True, text=True, timeout=180,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL FREEZE-OR-HOLD-FLOOR CHECKS PASS" in r.stdout
    assert "FAILS 0" in r.stdout
    out = os.path.join(ROOT, "theory", "freeze_or_hold_floor_checks", "freeze_or_hold_floor_checks.out")
    with open(out, encoding="utf-8") as f:
        expected = f.read()
    assert r.stdout == expected
