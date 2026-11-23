"""Math behind figures/master_curve.png. Every plotted number comes from here.

Worked class only (theory/GENERAL_FORM_PHYSICS_2026-11-22.md sections 3-5):
exogenous equilibrium Ornstein-Uhlenbeck signal dX = -aX dt + sqrt(2av) dW,
mean-square decision loss, memory does not move the signal, memory-bath heat
at its floor kT*a*(v-eps)/eps (approached in a limit, IP11).

Dimensionless stake x = w*v/(kT*a).
  J*/(kT a) = x            for x <= 1   (blind: no memory, error v)
            = 2 sqrt(x) - 1 for x > 1   (tracked: error v/sqrt(x))
This is the scalar frontier 2 sqrt(kT a v w) - kT a of section 5 divided by kT a.
"""
import math

import numpy as np


def F(x):
    """Minimum cost of judgment in units of kT*a, as a function of x = w v /(kT a)."""
    x = np.asarray(x, float)
    return np.where(x <= 1.0, x, 2.0 * np.sqrt(np.maximum(x, 1.0)) - 1.0)


def err_frac(x):
    """Minimizing error as a fraction of the signal variance v."""
    x = np.asarray(x, float)
    return np.where(x <= 1.0, 1.0, 1.0 / np.sqrt(np.maximum(x, 1.0)))


def heat_floor(a, v, eps, kT=1.0):
    """IP11 floor on the memory-bath heat at decision error eps (0 < eps <= v)."""
    return kT * a * (v - eps) / eps


def brute_min(a, v, w, kT=1.0, n=200001):
    """Numerical minimum over eps in (0, v] of heat floor + w*eps; no closed form used."""
    # log grid on eps/v from 1e-6 to 1, refined once around the best point
    t = np.exp(np.linspace(math.log(1e-6), 0.0, n))
    J = heat_floor(a, v, t * v, kT) + w * t * v
    i = int(np.argmin(J))
    lo, hi = t[max(i - 1, 0)], t[min(i + 1, n - 1)]
    t2 = np.linspace(lo, hi, 20001)
    J2 = heat_floor(a, v, t2 * v, kT) + w * t2 * v
    j = int(np.argmin(J2))
    return float(J2[j]), float(t2[j] * v)


def ladder_count(x, rho):
    """Closed-form tracked count on a per-mode geometric ladder (infinite ladder), x at the slowest mode."""
    if x <= 1.0:
        return 0
    return int(math.floor(math.log(x) / math.log(rho))) + 1


def ladder_xs(x_slowest, rho, n):
    """x of each rung: the k-th mode is faster by rho**k, so its x is x_slowest / rho**k."""
    return [x_slowest / rho ** k for k in range(n)]


def separate_copies(x, K):
    """K separate memories of K identical modes, decision = their sum.
    x = w*(K v)/(kT a) is the stake of the sum. Cost in units of kT a.
    Each copy is the scalar frontier at variance v: K * F(x/K)  (general_checks.py: Jsep = K * trace_frontier_mode)."""
    x = np.asarray(x, float)
    return K * F(x / K)


def random_worlds(n=240, seed=20261122):
    """Random parameter draws in the worked class (computed, not measured)."""
    rng = np.random.default_rng(seed)
    kT = 10 ** rng.uniform(-3, 3, n)
    a = 10 ** rng.uniform(-3, 3, n)
    v = 10 ** rng.uniform(-3, 3, n)
    # choose w so that x spans 1e-2..1e4 while raw w spans many decades
    x = 10 ** rng.uniform(-2, 4, n)
    w = x * kT * a / v
    return kT, a, v, w


def cut_vs_bulk(ns=(6, 8, 10, 12, 16)):
    """T41 (theory/HOLOGRAPHIC_2026-11-22.md section 3, line 130): periodic d=2 lattice, alpha=beta=1,
    per-site error 1/18. Bulk floor = 13 per site (x n^2). Cut lower bound = 13 per cut site (x n).
    Achieved cut cost = uniform diagonal load on one column, computed by the repo's own checker functions."""
    import importlib.util
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    spec = importlib.util.spec_from_file_location("hc", os.path.join(root, "theory/holographic_checks/holographic_checks.py"))
    hc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hc)
    eps = 0.5 / 9.0
    per = 1.0 / eps - 5.0
    rows = []
    for n in ns:
        Q = hc.periodic_precision(2, n, 1.0, 1.0)
        sites = np.arange(0, n * n, n)
        total, _phi, smax = hc.uniform_diagonal_load(Q, sites, eps)
        rows.append((n, n * n * per, n * per, total, smax <= eps * (1 + 1e-6)))
    return rows
