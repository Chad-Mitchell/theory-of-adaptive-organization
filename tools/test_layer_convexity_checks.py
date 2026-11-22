"""Runs tools/layer_convexity_checks.py --quick and spot-checks the proofs' key identities."""
import importlib.util
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _mod():
    path = os.path.join(ROOT, "tools", "layer_convexity_checks.py")
    spec = importlib.util.spec_from_file_location("layer_convexity_checks", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_layer_convexity_checks_quick_all_pass():
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "layer_convexity_checks.py"), "--quick"],
                       capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL LAYER CONVEXITY CHECKS PASS" in r.stdout


def test_minimal_bump_is_nonconvex():
    m = _mod()
    e = m.band_curve([2.0, 1.0, 1.0], [0.0, 1.0, 0.0], 2)
    assert np.allclose(e, [1.0, 2.0 / 3.0, 0.0])
    assert not m.is_convex(e)


def test_monotone_band_model_convex():
    m = _mod()
    rng = np.random.default_rng(7)
    for _ in range(30):
        n = int(rng.integers(5, 40))
        mu = rng.exponential(1.0, n)
        W = np.sort(rng.uniform(0, 1, n))[::-1]
        e = m.band_curve(mu, W, min(n, 8))
        assert m.is_convex(e, 1e-10 * max(1.0, e[0]))


def test_n60_equals_argmin_on_convex_sequence():
    m = _mod()
    eps = [1.0, 0.4, 0.15, 0.05, 0.0]
    for R in np.logspace(-2, 3, 200):
        assert m.n60_from(eps, R) == m.argmin_J(eps, R)


def test_models_residues_positive_two_modes():
    m = _mod()
    a = np.array([0.01, 1.0]); v = np.array([2.0, 0.5]); N = 0.1
    c = m.models_poles(a, v, N)
    assert a[0] < c[0] < a[1] < c[1]
    assert np.all(m.models_residues(a, c) > 0)
