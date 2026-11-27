"""Runs theory/swarm-2026-11-27/checks/swarm27_checks.py and compares its output with the committed .out."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def test_swarm27_checks_all_pass():
    r = subprocess.run([sys.executable, os.path.join(HERE, "swarm27_checks.py")],
                       capture_output=True, text=True, timeout=900)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL SWARM27 CHECKS PASS" in r.stdout
    assert "FAILS 0" in r.stdout
    with open(os.path.join(HERE, "swarm27_checks.out"), encoding="utf-8") as f:
        expected = f.read()
    assert r.stdout == expected
