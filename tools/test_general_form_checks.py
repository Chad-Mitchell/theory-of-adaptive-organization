"""Runs tools/general_form_checks.py (frontier form, dent, Kelly, Lundberg)."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_general_form_checks_all_pass():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "general_form_checks.py")],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL GF CHECKS PASS" in r.stdout
    assert "FAILS 0" in r.stdout
