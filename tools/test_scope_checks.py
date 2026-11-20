"""Runs theory/meq_checks/scope_checks.py: THEORY v2.4 scope fixes (CT33 spend monotone, CT34 exact upkeep embedding and its error bound, CT24 binding ruin, rhythms, alpha-1 scope, per-window CT25, CT29 2/N, interlacing)."""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_scope_checks():
    r = subprocess.run(["nice", "-n", "19", sys.executable, os.path.join(ROOT, "theory", "meq_checks", "scope_checks.py")],
                       capture_output=True, text=True, timeout=900)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "RESULT: PASS" in r.stdout
