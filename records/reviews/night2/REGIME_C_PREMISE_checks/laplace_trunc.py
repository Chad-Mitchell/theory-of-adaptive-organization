# Optimal sub-Gaussian proxy v* (and zero-rate slope u* = 1/(2 v*)) of a unit-variance Laplace truncated at |x| <= L.
import numpy as np
from scipy.special import logsumexp
for L in (10, 20, 40, 80, 160):
    x = np.arange(-L, L+1e-9, 0.05); p = np.exp(-abs(x)*2**.5); p /= p.sum(); x = x/np.sqrt(p @ x**2)
    best = 0
    for t in np.geomspace(1e-3, 200, 4000):
        for tt in (t, -t):
            best = max(best, 2*logsumexp(np.log(p) + tt*x)/tt**2)
    print("L", L, "v*", round(best, 3), "u*", round(1/(2*best), 5), flush=True)
