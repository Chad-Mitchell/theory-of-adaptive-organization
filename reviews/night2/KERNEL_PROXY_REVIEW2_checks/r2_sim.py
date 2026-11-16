"""In-model like-with-like references with own fGn/kriging (rlib), locked pick-28 inputs (numbers only).
Planned rows: n = 9276, rows t = 503..n-22 (8752; also the 69x126 = 8694 truncation used by the locked run).
Statistics per rep: W(m) noiseless BLP tracker; W(ybar) realized mean-log response; W(L) realized ln-mean-level;
W(z_r) tracker + AR(1) noise; W(lnE) Jensen tracker; paired z - ybar; sum of weights. Also dW(ybar)/dalpha (CRN)."""
import numpy as np, json, sys, math
from scipy.signal import fftconvolve
from rlib import *
A0, Q0, S0 = 1.2587, -1.8116, -0.9005
NREP = int(sys.argv[1]) if len(sys.argv) > 1 else 300
n = 9276; burn = 2100; Lw = 2000

def weights_all(alpha, lnq, lns2):
    c = vario_coef(alpha, lnq); s2 = math.exp(lns2)
    pos = -np.arange(Lw, dtype=float); K = lambda d: -0.5 * c * np.abs(d) ** (alpha - 1)
    A = np.empty((Lw + 1, Lw + 1)); A[:Lw, :Lw] = K(pos[:, None] - pos[None, :]); A[np.diag_indices(Lw)] += s2
    A[Lw, :Lw] = A[:Lw, Lw] = 1.0; A[Lw, Lw] = 0.0
    Ws, Vs = [], []
    for j in range(1, H + 1):
        k = K(pos - j); w = np.linalg.solve(A, np.r_[k, 1.0])[:Lw]
        V = -2 * w @ k + w @ (A[:Lw, :Lw] @ w)     # Var(x_{t+j} - sum w y), K(0)=0, allowable combination
        Ws.append(w); Vs.append(V)
    return np.array(Ws), np.array(Vs)

def ar1(m, phi, sd, rng):
    e = rng.standard_normal(m); u = np.empty(m); u[0] = e[0] * sd
    a = sd * math.sqrt(1 - phi * phi)
    for i in range(1, m): u[i] = phi * u[i - 1] + a * e[i]
    return u

def one(rng, alpha, lnq, lns2, Wj, Vj, full=True):
    x, y = sim_driver(n + burn, rng, alpha, lnq, lns2)
    yy = y[burn:]; X, t = design(yy)
    ybar = future_mean(yy)[t]; rows = np.isfinite(ybar)
    o = {'W_ybar': W(ols(X[rows], ybar[rows])), 'W_ybar_8694': W(ols(X[rows][:8694], ybar[rows][:8694])),
         'sum_ybar': kernel_stats(ols(X[rows], ybar[rows]))[1]}
    if not full: return o
    mj = np.stack([fftconvolve(y, w)[:len(y)] for w in Wj])[:, burn:]   # m_j(t) = sum_i w_i y_{t-i}
    m = mj.mean(0)[t]
    L = np.log(future_mean(np.exp(yy)))[t]
    bm = ols(X, m); o['W_m'] = W(bm); o['sum_m'] = kernel_stats(bm)[1]
    o['W_L'] = W(ols(X[rows], L[rows]))
    zJ = np.log(np.mean(np.exp(mj + Vj[:, None] / 2), 0))[t]
    o['W_lnE'] = W(ols(X, zJ)); o['jensen_shift'] = o['W_lnE'] - o['W_m']
    sdm = m.std()
    for r in (0.25, 0.45):
        z = m + ar1(len(m), 0.95, r * sdm, rng)
        o[f'W_z{r}'] = W(ols(X[rows], z[rows]))
        o[f'D_z{r}_ybar'] = o[f'W_z{r}'] - o['W_ybar']; o[f'D_z{r}_L'] = o[f'W_z{r}'] - o['W_L']
    o['D_m_ybar'] = W(ols(X[rows], m[rows])) - o['W_ybar']
    return o

Wj, Vj = weights_all(A0, Q0, S0)
rng = np.random.default_rng(66001); res = []
for k in range(NREP):
    res.append(one(rng, A0, Q0, S0, Wj, Vj))
    if k % 50 == 0: print(k, {kk: round(v, 4) for kk, v in res[-1].items()}, flush=True)
summ = {kk: {'mean': float(np.mean([r[kk] for r in res])), 'sd': float(np.std([r[kk] for r in res], ddof=1)),
             'se_mean': float(np.std([r[kk] for r in res], ddof=1) / math.sqrt(len(res)))} for kk in res[0]}
# derivative wrt alpha with common random numbers (realized response depends only on driver params)
der = {}
for da in (-0.1, 0.1):
    rr = np.random.default_rng(66002); der[da] = [one(rr, A0 + da, Q0, S0, None, None, full=False)['W_ybar'] for _ in range(150)]
rr = np.random.default_rng(66002); base = [one(rr, A0, Q0, S0, None, None, full=False)['W_ybar'] for _ in range(150)]
dd = (np.array(der[0.1]) - np.array(der[-0.1])) / 0.2
out = {'nrep': NREP, 'Lw': Lw, 'summary': summ, 'dWybar_dalpha': float(dd.mean()), 'dWybar_dalpha_se': float(dd.std(ddof=1) / math.sqrt(len(dd))),
       'W_ybar_at_alpha_pm0.1': [float(np.mean(der[-0.1])), float(np.mean(base)), float(np.mean(der[0.1]))],
       'sigma_pred_alpha_only(0.0429)': float(abs(dd.mean()) * 0.0429)}
json.dump(out, open('r2_sim.json', 'w'), indent=1); print(json.dumps(out, indent=1))
