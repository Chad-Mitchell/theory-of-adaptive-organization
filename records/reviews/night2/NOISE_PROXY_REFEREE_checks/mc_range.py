#!/usr/bin/env python3
"""R4: does the L0w estimator (within-forecaster robust nowcast dispersion, lower-branch inversion) stay unbiased
BELOW the dry run's validated range K in [0.01, 1]? Own code. Pure-noise panels: deviation from consensus is
a*(v_i - vbar), so x cancels exactly; environment fixed at the recorded fit (fit noise excluded; that part is the
authors' dry run). SPF-like layout: T surveys, geometric spells mean 20, ~nf active."""
import json, numpy as np, ref_model as R
from scipy.optimize import brentq
d = json.load(open('../../../tests/SPF_NOISE_PROXY/results/analysis.json'))['per_var']
rng = np.random.default_rng(20261115 + 22)
def rvar(z):
    q75, q25 = np.percentile(z, [75, 25]); return ((q75 - q25) / 1.349) ** 2
out = {}
for v in ['UNEMP', 'TBILL', 'TBOND', 'HOUSING']:
    r = d[v]; f = r['fit']; W = R.World(f['tauE'], f['alpha'], f['phi']); nf = r['nf']; T = r['T']
    def inv(lev):
        g = lambda lk: R.disp(np.exp(lk), R.weights_single(W, np.exp(lk), 0), nf) - lev
        return float(np.exp(brentq(g, np.log(1e-6), np.log(3.0))))
    for K in (0.001, 0.003, 0.01, 0.03):
        a = R.weights_single(W, K, 0); La = min(len(a), 200); a = a[:La]
        est = []
        for rep in range(30):
            P = int(nf * T / 20) + int(nf)
            starts = rng.integers(-20, T, P); lens = rng.geometric(1 / 20, P)
            act = np.zeros((T, P), bool)
            for i in range(P):
                s, e = max(starts[i], 0), min(starts[i] + lens[i], T)
                if e > s: act[s:e, i] = True
            noise = rng.standard_normal((T + La, P)) * np.sqrt(K)
            F = np.stack([np.convolve(noise[:, i], a)[La:La + T] for i in range(P)], 1)
            F = np.where(act, F, np.nan)
            cons = np.nanmean(F, 1); dev = F - cons[:, None]
            nobs = act.sum(0); fe = np.array([np.nanmean(dev[act[:, i], i]) if nobs[i] else np.nan for i in range(P)])
            D = []
            for t in range(T):
                if act[t].sum() < 10: continue
                b = act[t] & (nobs >= 8)
                if b.sum() >= 10: D.append(rvar(dev[t, b] - fe[b]))
            est.append(np.log(inv(np.mean(D)) / K))
        out[f'{v}_K{K}'] = dict(median_lnratio=float(np.median(est)), iqr=[float(np.percentile(est, 25)), float(np.percentile(est, 75))])
        print(v, K, out[f'{v}_K{K}'], flush=True)
json.dump(out, open('results/mc_range.json', 'w'), indent=1)
