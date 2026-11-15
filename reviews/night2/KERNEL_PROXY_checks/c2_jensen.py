"""In-model (no data): effect on W21 of the tracker reporting ln E[mean level] (VIX-like) instead of E[mean log],
Gaussian fBm + noise at the locked inputs; same bins, n = 9276, Lw = 2000."""
import numpy as np, json
from plib import *
Lw = 2000; n = 9276; burn = 2100
Dq = np.exp(LNQ) * D1(ALPHA); s2 = np.exp(LNS2)
tt = -np.arange(Lw, dtype=float); G = lambda d: -0.5 * Dq * np.abs(d) ** (ALPHA - 1)
C = G(tt[:, None] - tt[None, :]) + s2 * np.eye(Lw)
M = np.zeros((Lw + 1, Lw + 1)); M[:Lw, :Lw] = C; M[:Lw, Lw] = 1; M[Lw, :Lw] = 1
Wj, vj = [], []
for j in range(1, H + 1):
    c = G(tt - j); w = np.linalg.solve(M, np.concatenate([c, [1.0]]))[:Lw]
    Wj.append(w); vj.append(float(w @ C @ w - 2 * w @ c))
rng = np.random.default_rng(20261134); res = []
for k in range(60):
    x, y = driver(n + burn, rng)
    mj = np.stack([np.convolve(y, w)[:len(y)] for w in Wj])[:, burn:]
    yy = y[burn:]; X, t = binmat(yy)
    mlog = mj.mean(0)[t]
    zJ = np.log(np.mean(np.exp(mj + np.array(vj)[:, None] / 2), 0))[t]
    a, b = W21(ols(X, mlog)), W21(ols(X, zJ)); res.append((a, b, b - a, ols(X, zJ)[1:].dot(np.diff(EDGES))))
r = np.array(res)
out = {'v_j_first_last': [vj[0], vj[-1]], 'W_meanlog': float(r[:, 0].mean()), 'W_lnE': float(r[:, 1].mean()),
       'shift_mean': float(r[:, 2].mean()), 'shift_sd': float(r[:, 2].std(ddof=1)), 'sum_beta_lnE': float(r[:, 3].mean()), 'reps': len(r)}
json.dump(out, open('c2_jensen.json', 'w'), indent=1); print(out)
