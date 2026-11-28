"""POST HOC, descriptive (after the locked run): per-bin weights and survival of the measured VIX kernel vs the
theory kernel's simulated expectation (H0, r = 0). Not part of the decision."""
import json, numpy as np, klib, decide
y, z = decide.load()
X = klib.lagmat(y); zz = z[klib.L - 1:]; ok = np.isfinite(zz); X, zz = X[ok], zz[ok]
E = klib.EDGES
B = np.column_stack([np.ones(len(zz))] + [X[:, E[j]:E[j + 1]].sum(1) for j in range(len(E) - 1)])
b = np.linalg.lstsq(B, zz, rcond=None)[0][1:]
mass = b * np.diff(E); share = mass / mass.sum()
# theory expectation via the same estimator on a long noiseless simulation
rng = np.random.default_rng(5)
A, Q, S2 = 1.2587, np.exp(-1.8116), np.exp(-0.9005)
w = klib.ok_kernel(A, Q, S2, Lw=2000)
from numpy.lib.stride_tricks import sliding_window_view
x, ys = klib.sim_driver(200000, A, Q, S2, rng)
f = np.full(len(ys), np.nan); f[1999:] = sliding_window_view(ys, 2000)[:, ::-1] @ w
Xs = klib.lagmat(ys[1496:]); fs = f[1496:][klib.L - 1:]
Bs = np.column_stack([np.ones(len(fs))] + [Xs[:, E[j]:E[j + 1]].sum(1) for j in range(len(E) - 1)])
bs = np.linalg.lstsq(Bs, fs, rcond=None)[0][1:]; ms = bs * np.diff(E); sh = ms / ms.sum()
out = {'bins': [f'{E[j]}-{E[j+1]-1}' for j in range(len(E) - 1)], 'vix_mass_share': share.round(4).tolist(),
       'theory_mass_share': sh.round(4).tolist(), 'vix_slope_b_sum': float(mass.sum()),
       'vix_survival_at': {str(t): float(share[E.index(t):].sum()) for t in (1, 5, 10, 21, 42, 84, 168, 336)},
       'theory_survival_at': {str(t): float(sh[E.index(t):].sum()) for t in (1, 5, 10, 21, 42, 84, 168, 336)}}
print(json.dumps(out, indent=1)); json.dump(out, open('posthoc_bins.json', 'w'), indent=1)
