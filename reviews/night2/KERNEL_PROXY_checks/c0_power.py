"""Pre-outcome simulation (no outcome data read): sampling sd and like-with-like means of the three proxy-check
statistics on planned data (n=9276, rows with 504 past and 21 future days), for the MV10 gate."""
import numpy as np, json, sys
from plib import *
NREP = int(sys.argv[1]) if len(sys.argv) > 1 else 200
n = 9276; burn = 1000; Lw = 2000
w = blp_weights(Lw)
rng = np.random.default_rng(20261133)
res = []
for k in range(NREP):
    x, y = driver(n + burn, rng)
    m = np.convolve(y, w)[:len(y)]                       # m_t = sum_i w_i y_{t-i}
    y, m = y[burn:], m[burn:]
    X, t = binmat(y)
    ybar = fut_mean(y)[t]; Lv = np.log(fut_mean(np.exp(y)))[t]
    rows = t <= n - H - 1
    sdm = np.std(m[t]); out = {}
    out['W_bar'] = W21(ols(X[rows], ybar[rows]))
    out['W_L'] = W21(ols(X[rows], Lv[rows]))
    out['W_m'] = W21(ols(X, m[t]))
    for r in (0.25, 0.45):
        z = m[t] + ar1(len(t), 0.95, r * sdm, rng)
        out['W_z%.2f' % r] = W21(ols(X, z))
        out['D_zL%.2f' % r] = W21(ols(X[rows], z[rows])) - out['W_L']
    res.append(out)
    if k % 20 == 0: print(k, out, flush=True)
keys = res[0].keys()
summ = {kk: {'mean': float(np.mean([r[kk] for r in res])), 'sd': float(np.std([r[kk] for r in res], ddof=1))} for kk in keys}
json.dump({'nrep': NREP, 'Lw': Lw, 'summary': summ}, open('c0_power.json', 'w'), indent=1)
print(json.dumps(summ, indent=1))
