"""Runs tools/theorem_p_drift_checks.py (quick mode) and checks the PD1/PD5 formulas directly."""
import importlib.util
import math
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load():
    path = os.path.join(ROOT, "tools", "theorem_p_drift_checks.py")
    spec = importlib.util.spec_from_file_location("theorem_p_drift_checks", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_theorem_p_drift_checks_quick_pass():
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "theorem_p_drift_checks.py")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL PD CHECKS PASS" in r.stdout


def test_sharp_floor_equals_kalman_and_rate_form():
    m = _load()
    for a in (0.8, 1.0, 1.5):
        P, Pp, r = m.kalman_steady(a, 2.0, 0.3)
        assert abs(P - m.floor_sharp(r, a, 2.0)) < 1e-9 * P
        assert abs(r - 0.5 * math.log(a * a + 2.0 / P)) < 1e-12


def test_data_rate_threshold_and_random_walk_form():
    m = _load()
    assert m.floor_sharp(math.log(2.0), 2.0, 1.0) == math.inf
    r = 0.3
    assert abs(m.floor_sharp(r, 1.0, 1.0) - 1.0 / math.expm1(2 * r)) < 1e-12


def test_price_optimum_first_order_condition():
    m = _load()
    q, w, c = 1.3, 0.7, 0.2
    r, J = m.price_optimum_rw(q, w, c)
    z = math.exp(2 * r)
    assert abs(2 * w * q * z - c * (z - 1) ** 2) < 1e-9


def test_ce7_sparse_look_counterexample():
    import numpy as np
    m = _load()
    ce7 = m.sparse_look_counterexample(16)
    T = 2 ** 16
    assert ce7["T"] == T
    assert ce7["n_looks"] == 17
    assert ce7["max_mse"] <= 7.00 + 1e-9
    assert abs(ce7["total_r"] - 16.8) < 0.05
    assert abs(ce7["mean_r"] - 2.56e-4) < 5e-7
    assert abs(ce7["blind_mse"] - 4.29e9) / 4.29e9 < 0.005
    assert abs(ce7["stock_I"] - 0.5 * math.log(T * T + 1.0)) < 1e-9
    assert abs(ce7["stock_I"] - 11.090354889) < 1e-6
    assert abs(ce7["stock_I_record"] - 11.157120585) < 1e-6

    # Direct full-covariance Schur-complement verification
    ts = np.array([float(2 ** k) for k in range(17)])
    Sig_Y = np.outer(ts, ts) + 2.0 * np.eye(17)
    cov_XY = float(T) * ts
    cov_XY[-1] += 1.0
    var_X_Y = (T * T + 1.0) - cov_XY @ np.linalg.solve(Sig_Y, cov_XY)
    w_mu = np.linalg.solve(Sig_Y, ts)
    var_X_mu = (T * T + 1.0) - (cov_XY @ w_mu) ** 2 / (w_mu @ Sig_Y @ w_mu)
    assert abs(ce7["var_X_given_mu"] - var_X_mu) < 1e-9
    assert abs(ce7["var_X_given_Y"] - var_X_Y) < 1e-9
    assert abs(ce7["stock_I"] - 0.5 * math.log((T * T + 1.0) / var_X_mu)) < 1e-9
    assert abs(ce7["stock_I_record"] - 0.5 * math.log((T * T + 1.0) / var_X_Y)) < 1e-9

