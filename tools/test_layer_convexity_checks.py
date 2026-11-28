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
                       capture_output=True, text=True)
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


def test_l1_from0_vs_from1_and_nonconvex_counterexamples():
    m = _mod()
    # Convex sequence where leftmost argmin is 0: from-0 matches, from-1 fails
    eps = [1.0, 0.4, 0.0]
    assert m.argmin_J(eps, 1.0) == 0
    assert m.n60_from(eps, 1.0, k0=0) == 0
    assert m.n60_from(eps[1:], 1.0, k0=1) == 1
    # At R = 0, from-0 returns 0 == argmin_J(eps, 0)
    assert m.n60_from(eps, 0.0, k0=0) == 0
    assert m.argmin_J(eps, 0.0) == 0
    # Non-convex d = (-2, -1) still matches from-0 count for every R >= 0
    eps_neg = [-3.0, -1.0, 0.0]
    assert not m.is_convex(eps_neg)
    for R in [0.0, 0.1, 1.0, 10.0, 100.0]:
        assert m.n60_from(eps_neg, R, k0=0) == m.argmin_J(eps_neg, R) == 0


def test_lemma_z_requires_nonnegative_W():
    m = _mod()
    mu = np.array([1.0, 1.0])
    W = np.array([0.0, -1.0])
    C = m.seg_cost_matrix(mu, W)
    z = lambda x: float(np.sum(mu[x:] * W[x:] ** 2))
    # w(AB) - w(B) = 0.5 > 0 = z(0) - z(1)
    assert np.isclose(C[0, 2] - C[1, 2], 0.5)
    assert np.isclose(z(0) - z(1), 0.0)
    assert C[0, 2] - C[1, 2] > z(0) - z(1)
