"""Runs tools/chain_diffusion_checks.py (static Poisson bound, exact lag vs DS1)."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_chain_diffusion_checks_quick_pass():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "chain_diffusion_checks.py")],
        capture_output=True, text=True, timeout=180,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL CHAIN DIFFUSION CHECKS PASS" in r.stdout
    assert "CD1 static" in r.stdout
    assert "identity gap" in r.stdout
