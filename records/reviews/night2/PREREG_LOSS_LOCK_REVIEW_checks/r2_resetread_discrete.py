"""Reviewer's own check of the reset-read power-loss elasticities and of the alpha=1.5, p=1/2 discrepancy (Q3).
(1) Own fBm Monte Carlo (Cholesky of the fGn covariance) -> E|X_t - X_0|^p slope in ln t equals p*H.
(2) Sampled-time model: reads every T steps (T real via the Hurwitz zeta, i.e. the exact discrete lag sum interpolated),
    cost rate J(T) = c/T + w q^{p/2} c_p (1/T) sum_{t=0}^{T-1} t^{pH}; elasticities of 1/T* in w and q by central differences,
    at operating points with T* from ~1.5 to ~10^4. If the 0.03 gap is a grid (small-T*) effect it vanishes as T* grows.
"""
import numpy as np, mpmath as mp, json
from scipy.optimize import brentq
rng = np.random.default_rng(20261115)
out = {}
# (1) MC
n, M = 1024, 400
for alpha in (1.5, 2.0, 2.5):
    H = (alpha-1)/2
    k = np.arange(n)
    g = 0.5*(np.abs(k+1)**(2*H) - 2*np.abs(k)**(2*H) + np.abs(k-1)**(2*H))
    C = g[np.abs(k[:, None]-k[None, :])]
    L = np.linalg.cholesky(C + 1e-12*np.eye(n))
    X = np.cumsum(L @ rng.standard_normal((n, M)), axis=0)  # X_t, t=1..n
    lags = np.unique(np.round(np.geomspace(4, 256, 12)).astype(int))
    for p in (0.5, 1.0, 2.0, 4.0):
        m = [np.mean(np.abs(X[l:, :] - X[:-l, :])**p) for l in lags]
        s = np.polyfit(np.log(lags), np.log(m), 1)[0]
        out[f'mc_slope_a{alpha}_p{p}'] = [round(float(s), 4), p*H]
        print(f'MC alpha={alpha} p={p}: slope {s:.4f} vs pH {p*H:.4f}')
# (2) sampled-time elasticities
mp.mp.dps = 30
def lagmean(T, s):  # (1/T) sum_{t=0}^{T-1} t^s for real T>=1 ; sum_{t=1}^{T-1} t^s = zeta(-s) - zeta(-s, T)
    return float((mp.zeta(-s) - mp.zeta(-s, T))/T)
def Tstar(cw, s):  # minimise cw/T + lagmean(T,s) (w q^{p/2} c_p folded into cw ratio)
    f = lambda lt: float(mp.diff(lambda u: cw/mp.e**u + (mp.zeta(-s) - mp.zeta(-s, mp.e**u))/mp.e**u, lt))
    lo, hi = np.log(1.0001), np.log(1e7)
    return np.exp(brentq(f, lo, hi, xtol=1e-12))
res = []
for alpha in (1.5, 2.0, 2.5):
    H = (alpha-1)/2
    for p in (0.5, 1.0, 2.0, 4.0):
        s = p*H; a_th = 2/(2+p*(alpha-1)); b_th = p/(2+p*(alpha-1))
        for cw in (0.2, 1.0, 10.0, 1e2, 1e4):
            try:
                T0 = Tstar(cw, s)
            except ValueError:
                continue
            h = 0.05  # w x e^{+-h} == cw x e^{-+h}; q x e^{+-h} == cw x e^{-+ h p/2}
            ew = -(np.log(Tstar(cw*np.exp(-h), s)) - np.log(Tstar(cw*np.exp(h), s)))/(2*h) * (-1)
            ew = (np.log(Tstar(cw*np.exp(h), s)) - np.log(Tstar(cw*np.exp(-h), s)))/(2*h)  # d ln T*/d ln(c/w) = a
            eq = ew*p/2
            res.append(dict(alpha=alpha, p=p, cw=cw, Tstar=T0, a=ew, a_th=a_th, b=eq, b_th=b_th))
            print(f'alpha={alpha} p={p} c/w={cw:g}: T*={T0:9.2f}  a={ew:.4f} (th {a_th:.4f})  b={eq:.4f} (th {b_th:.4f})')
out['sampled_time'] = res
json.dump(out, open('r2_resetread_discrete.json', 'w'), indent=1)
