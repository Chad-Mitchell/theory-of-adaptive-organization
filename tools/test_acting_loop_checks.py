"""Runs theory/acting_loop_checks/acting_loop_checks.py."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_acting_loop_checks():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "theory", "acting_loop_checks", "acting_loop_checks.py")],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL ACTING LOOP CHECKS PASS" in r.stdout
    assert "FAILS 0" in r.stdout
    assert "PREDICTION-MISSES 0" in r.stdout
    assert not any(line.startswith("PREDICTION-MISS ") for line in r.stdout.splitlines())
