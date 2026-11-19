#!/usr/bin/env python3
"""REACH check 2: latency, pooling and station catchments (CONDITIONAL on traversable wormholes existing).
Run: nice -n 19 python3 wormhole_checks.py > wormhole_checks.out
(a) EOQ pooling with a dissemination price d and a latency l (alpha = 2, diffusive drift, hold-last-value reads):
    local:   N targets each read at price c:            cost = N*sqrt(2*c*w*s2)
    central: one read (c) + tell N targets (N*d) per update, staleness l adds N*w*s2*l:
             cost = sqrt(2*(c+N*d)*N*w*s2) + N*w*s2*l
    closed forms checked here by brute-force minimisation over the update interval T.
(b) Station catchments: Poisson stations of density nu, uniform targets; coverage of 'within latency budget' vs formula.
"""
import numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize_scalar
rng = np.random.default_rng(1118)

print("(a) pooling with dissemination price d and latency l   [w*s2 = 1, c = 1]")
print("%5s %6s %9s %9s %9s %9s" % ("N", "d/c", "local", "central*", "closed", "l_crit/T*"))
for N in (4, 16, 100):
    for d in (0.0, 0.05, 0.5, 1.0):
        c = 1.0; ws2 = 1.0
        loc = N * np.sqrt(2 * c * ws2)
        f = lambda T: (c + N * d) / T + N * ws2 * T / 2          # per-unit-time cost of the pooled design
        T = minimize_scalar(f, bounds=(1e-6, 1e3), method='bounded').x
        cen_num = f(T); cen_closed = np.sqrt(2 * (c + N * d) * N * ws2)
        Tloc = np.sqrt(2 * c / ws2)
        lcrit = (loc - cen_closed) / (N * ws2) / Tloc           # latency at which central = local, in units of T*_local
        pred = 1 - np.sqrt((1 + N * d / c) / N)
        assert abs(cen_num - cen_closed) < 1e-3 * cen_closed
        assert abs(lcrit - pred) < 1e-9
        print("%5d %6.2f %9.3f %9.3f %9.3f %9.3f" % (N, d / c, loc, cen_num, cen_closed, lcrit))
print("central wins at zero latency iff d/c < 1 - 1/N; with latency iff l < T*_local * (1 - sqrt((1 + N d/c)/N)).  (negative = never)")

print("\n(b) Poisson stations in the periodic unit cube (c = 1): P[nearest station within r] = 1 - exp(-(4 pi/3) nu r^3)")
print("%7s %7s %9s %9s" % ("nu", "r", "sim", "formula"))
targets = rng.random((4000, 3)); REAL = 60          # average over 60 station realisations (the formula is an expectation)
def dists(nu):
    out = []
    for _ in range(REAL):
        st = rng.random((max(rng.poisson(nu), 1), 3)); out.append(cKDTree(st, boxsize=1.0).query(targets)[0])
    return np.array(out)
for nu in (10, 100, 1000):
    D = dists(nu)
    for r in (0.05, 0.1, 0.2):
        print("%7d %7.2f %9.3f %9.3f" % (nu, r, (D <= r).mean(), 1 - np.exp(-4 * np.pi / 3 * nu * r ** 3)))
print("\n(c) union with the direct light ball around the centre (centre sits at a station; budget l*; hop latency tau):")
print("%7s %6s %6s %9s" % ("nu", "l*", "tau", "covered"))
for nu in (0, 10, 100, 1000):
    for lstar, tau in ((0.2, 0.0), (0.2, 0.1), (0.2, 0.19)):
        direct = np.linalg.norm(targets - 0.5, axis=1) <= lstar
        if nu == 0: cov = direct.mean()
        else:
            D = dists(nu); cov = ((D <= max(lstar - tau, 0.0)) | direct[None, :]).mean()
        print("%7d %6.2f %6.2f %9.3f" % (nu, lstar, tau, cov))
print("nu = 0 is the no-wormhole bound (a light ball); hop latency tau eats the budget l*; coverage -> 1 as station density rises and tau -> 0.")
