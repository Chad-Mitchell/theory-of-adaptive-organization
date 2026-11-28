"""Runs theory/meq_checks/rules_scaling_checks.py: THEORY v2.3 CT18/CT25 general form (tau^H), CT24 general (shares = elasticities), CT26 (keep the superseded version), CT27 (outcome records as information acquisition), CT28 (closure and nesting)."""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_rules_and_scaling_checks():
    r = subprocess.run(["nice", "-n", "19", sys.executable, os.path.join(ROOT, "theory", "meq_checks", "rules_scaling_checks.py")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "RESULT: PASS" in r.stdout
