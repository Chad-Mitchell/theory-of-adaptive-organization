"""Runs theory/layerlife_checks/layerlife_checks.py (lifetime identities, stack spacing, D5 sign)."""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_layerlife_checks_all_pass():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "theory", "layerlife_checks", "layerlife_checks.py")],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL PASS" in r.stdout
