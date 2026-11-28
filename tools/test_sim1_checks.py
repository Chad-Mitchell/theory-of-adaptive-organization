"""Runs core/sim1_2026-11-21/math_checks.py (T28 identities and lock hashes)."""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_sim1_math_checks_all_ok():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "theory", "sim1_2026-11-21", "math_checks.py")],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL OK" in r.stdout
    assert "FAIL" not in r.stdout.replace("SOME FAILED", "")
