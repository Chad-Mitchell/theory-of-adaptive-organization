"""Runs theory/drift_heat_lift_checks/drift_heat_lift_checks.py and locks the closed forms."""
import importlib.util
import math
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "theory", "drift_heat_lift_checks", "drift_heat_lift_checks.py")


def _load():
    spec = importlib.util.spec_from_file_location("drift_heat_lift_checks", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_drift_heat_lift_checks_pass():
    r = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL DRIFT-HEAT-LIFT CHECKS PASS" in r.stdout


def test_kb_matched_random_walk_factor_two():
    m = _load()
    K, Dm = m.rw_kb_params(1.0, 0.2)
    asy = m.rw_centered_asymptotics(1.0, K, Dm, kT=1.0)
    assert abs(K - 5.0) < 1e-15
    assert abs(Dm - 0.5) < 1e-15
    assert abs(asy["I_dot"] - 2.5) < 1e-15
    assert abs(asy["Q"] - 5.0) < 1e-15
    assert abs(asy["Q_over_Idot"] - 2.0) < 1e-15
    assert abs(asy["capacity"] - 1.0) < 1e-15
    assert abs(asy["err"] - 0.2) < 1e-15


def test_fast_spring_heat_approaches_factor_one():
    m = _load()
    lam, Dm = m.rw_fast_params(1.0, 0.2, 1e6)
    asy = m.rw_centered_asymptotics(1.0, lam, Dm, kT=1.0)
    assert abs(asy["I_dot"] - 2.5) < 1e-12
    assert abs(asy["Q"] - 2.5) < 1e-5
    assert asy["Q"] > 2.5
    assert asy["capacity"] < 0.01
    # The short-time PD1-style inflow is not I_dot on this design.
    st = m.short_time_inflow(lam, asy["err"], Dm)
    assert st > 100 * asy["I_dot"]


def test_ratio_closed_form():
    m = _load()
    for Dm in (0.5, 2.0, 10.0, 100.0):
        lam, _ = m.rw_fast_params(1.0, 0.2, Dm)
        asy = m.rw_centered_asymptotics(1.0, lam, Dm, kT=1.0)
        assert abs(asy["Q_over_Idot"] - (1.0 + 1.0 / (2.0 * Dm))) < 1e-12
