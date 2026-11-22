"""Runs tools/drift_selection_checks.py (DS1 trace formula, exact Moran chain vs
moving optimum, DS2 speed limit). Quick mode; the documented run is --full."""
import importlib.util
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load():
    path = os.path.join(ROOT, "tools", "drift_selection_checks.py")
    spec = importlib.util.spec_from_file_location("drift_selection_checks", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_drift_selection_checks_quick_pass():
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "drift_selection_checks.py")],
                       capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL DS CHECKS PASS" in r.stdout
    assert "DS2 v=12 > v_max=10" in r.stdout


def test_ds1_reduces_to_static_and_brownian_form():
    m = _load()
    beta, Dm = 3.0, 0.25
    H = np.diag([0.5, 2.0, 5.0])
    assert abs(m.ds1_excess(beta, Dm, H, np.zeros((3, 3))) - 3 / (2 * beta)) < 1e-12
    D = 0.7
    got = m.ds1_excess(beta, Dm, H, D * np.eye(3))
    assert abs(got - (3 / (2 * beta)) * (1 + D / Dm)) < 1e-12


def test_ds1_matches_lyapunov_ou():
    m = _load()
    rng = np.random.default_rng(5)
    A = rng.normal(size=(2, 2)); H = A @ A.T + np.eye(2)
    Q = np.diag([0.3, 0.8])
    for gamma in (0.0, 0.05, 2.0):
        assert abs(m.ds1_excess(1.7, 0.4, H, Q, gamma) - m.lyapunov_excess(1.7, 0.4 * np.eye(2), H, Q, gamma)) < 1e-9


def test_moran_phi_bounded_by_one():
    m = _load()
    xs = -np.logspace(-4, 1, 50)  # |x| <= 10 keeps 1 - phi above float rounding
    phi = m.moran_phi(xs, 20)
    assert np.all(phi < 1.0) and np.all(phi > 0.0)
