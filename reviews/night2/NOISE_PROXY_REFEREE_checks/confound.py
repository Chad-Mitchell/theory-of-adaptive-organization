#!/usr/bin/env python3
"""R3: public-signal confound. World with private white noise K AND a common public signal z = x + u (var Kc).
For each S-1 variable: grid over (K, Kc); compute the h=0 and h=3 dispersion levels, invert each with the SINGLE-signal
lower branch (what SPF-NOISE-PROXY does), and report the implied G = ln Khat3 - ln Khat0, beta^G(Khat0), and the true
consensus CG beta of the two-signal world. Question: can a public signal (no individual bias, white private noise)
reproduce the observed (Khat_L0, G) and a true beta well above beta^G(Khat0)?"""
import json, sys, numpy as np, ref_model as R
from scipy.optimize import brentq
d = json.load(open('../../../tests/SPF_NOISE_PROXY/results/analysis.json'))['per_var']
LM = 300
CURVES = {}
def inv_lower(W, nf, h, lev):
    key = (id(W), h)
    if key not in CURVES:
        Ks = np.exp(np.linspace(np.log(1e-6), np.log(1e3), 240))
        CURVES[key] = (Ks, np.array([R.disp(K, R.weights_single(W, K, h), nf) for K in Ks]))
    Ks, Dc = CURVES[key]; ip = int(np.argmax(Dc))
    if lev >= Dc[ip]: return np.nan
    if lev <= Dc[0]: return float(Ks[0])
    return float(np.exp(np.interp(np.log(lev), np.log(Dc[:ip + 1]), np.log(Ks[:ip + 1]))))
res = {}
for v in sys.argv[1:]:
    r = d[v]; f = r['fit']; W = R.World(f['tauE'], f['alpha'], f['phi'], Lm=LM); nf = r['nf']
    rows = []
    for K in np.exp(np.linspace(np.log(1e-3), np.log(1.0), 7)):
        for Kc in [None] + list(np.exp(np.linspace(np.log(1e-3), np.log(10.0), 9))):
            a0 = R.weights_two(W, K, Kc, 0)[0] if Kc else R.weights_single(W, K, 0)
            a3 = R.weights_two(W, K, Kc, 3)[0] if Kc else R.weights_single(W, K, 3)
            D0, D3 = R.disp(K, a0, nf), R.disp(K, a3, nf)
            k0, k3 = inv_lower(W, nf, 0, D0), inv_lower(W, nf, 3, D3)
            row = dict(K=float(K), Kc=Kc, D0=D0, D3=D3, Khat0=k0, Khat3=k3, G=float(np.log(k3 / k0)),
                       betaG_khat0=R.cg_beta(W, k0, nf), beta_true=R.cg_beta(W, K, nf, Kc=Kc))
            rows.append(row)
        print(v, f'K={K:.3g} done', flush=True)
    res[v] = dict(obs=dict(K_L0=r['K']['L0'], K_L3=r['K']['L3'], G=r['G'], beta_hat=r['beta_hat_LFK'],
                           betaG_L0w=r['beta_pred']['L0w']), rows=rows)
    json.dump(res, open(f'results/confound_{"_".join(sys.argv[1:])}.json', 'w'), indent=1, default=float)
