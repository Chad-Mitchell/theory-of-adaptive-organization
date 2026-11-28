"""Check the Cholesky fBm generator: empirical variogram Var(B_{t+tau}-B_t)/tau^(alpha-1) ~ 1."""
import numpy as np, sys
sys.argv = ['x']; import sim
rng = np.random.default_rng(1)
for a in (1.5, 2.5):
    X = sim.fbm(rng, a, 1.0, 400)
    r = [np.mean((X[:, 1000 + tau] - X[:, 1000]) ** 2) / tau ** (a - 1) for tau in (1, 10, 100, 1000, 3000)]
    print(a, np.round(r, 3))
