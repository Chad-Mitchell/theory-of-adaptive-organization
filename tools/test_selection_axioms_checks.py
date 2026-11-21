"""Runs tools/selection_axioms_checks.py (equipartition, Dixit occupation, SA2 additivity)."""
import math
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_selection_axioms_checks_all_pass():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "selection_axioms_checks.py")],
        capture_output=True, text=True, timeout=120,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL SA CHECKS PASS" in r.stdout
    assert "FAIL" not in r.stdout.replace("SOME SA CHECKS FAILED", "")


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
