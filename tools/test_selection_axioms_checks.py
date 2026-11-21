"""Runs tools/selection_axioms_checks.py (equipartition, Dixit occupation, SA2 additivity)."""
import importlib.util
import math
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_checks():
    path = os.path.join(ROOT, "tools", "selection_axioms_checks.py")
    spec = importlib.util.spec_from_file_location("selection_axioms_checks", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_selection_axioms_checks_all_pass():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "selection_axioms_checks.py")],
        capture_output=True, text=True, timeout=120,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL SA CHECKS PASS" in r.stdout
    assert "FAIL" not in r.stdout.replace("SOME SA CHECKS FAILED", "")
    assert "reset-process E[x^2]" in r.stdout
    assert "Green jump" in r.stdout


def test_equipartition_exact_trace():
    d, beta = 6, 3.25
    H = np.diag(np.linspace(0.25, 3.0, d))
    Sigma = np.linalg.inv(beta * H)
    got = 0.5 * float(np.trace(H @ Sigma))
    assert abs(got - d / (2.0 * beta)) < 1e-12


def test_dixit_identities():
    k, sigma2, w = 1.2, 0.5, 0.8
    bstar = (6.0 * k * sigma2 / w) ** 0.25
    op = w * bstar * bstar / 6.0
    lumps = k * sigma2 / (bstar * bstar)
    want = math.sqrt(k * w * sigma2 / 6.0)
    assert abs(op - want) < 1e-12
    assert abs(lumps - op) < 1e-12
    assert abs(op + lumps - 2.0 * want) < 1e-12


def test_moran_fixation_ratio():
    def phi(rho, N):
        if abs(rho - 1.0) < 1e-15:
            return 1.0 / N
        return (1.0 - rho) / (1.0 - rho ** N)

    N, rho = 21, 0.7
    ratio = phi(1.0 / rho, N) / phi(rho, N)
    assert abs(ratio - rho ** (N - 1)) < 1e-12


def test_green_function_occupation_identities():
    sa = _load_checks()
    results = sa.green_function_identities()
    failed = [name for name, ok, _msg in results if not ok]
    assert not failed, failed
    b = 3.0
    assert abs(sa._occupation_moment2(b) - b * b / 6.0) < 1e-12
    assert abs(sa._occupation_moment_abs(b) - b / 3.0) < 1e-12


def test_dixit_occupation_from_reset_process():
    """The (s,S) reset process recovers E[x²]=b²/6, not by sampling the assumed density."""
    sa = _load_checks()
    rng = np.random.default_rng(20261121)
    b, sigma2 = 2.0, 1.0
    ex2, eabs, x = sa.reset_process_moments(b, sigma2, dt=4.0e-4, n_steps=2_000_000, rng=rng)
    assert np.all(np.abs(x) < b + 1e-12)
    assert abs(ex2 - b * b / 6.0) / (b * b / 6.0) < 0.04
    assert abs(eabs - b / 3.0) / (b / 3.0) < 0.04
