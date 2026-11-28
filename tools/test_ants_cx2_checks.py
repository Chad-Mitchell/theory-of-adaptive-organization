"""Runs theory/meq_checks/ants_cx2_checks.py: THEORY v2.4 CT30 (ant-trail update rule), CT31 (potential games, price of anarchy, cost shares), CT32 (no general convergence theorem; time-scale separation)."""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_ants_and_cx2_checks():
    r = subprocess.run(["nice", "-n", "19", sys.executable, os.path.join(ROOT, "theory", "meq_checks", "ants_cx2_checks.py")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "RESULT: PASS" in r.stdout
