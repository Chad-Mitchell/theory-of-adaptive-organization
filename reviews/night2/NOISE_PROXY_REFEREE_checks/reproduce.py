#!/usr/bin/env python3
"""R1: re-derive K_L0w from the micro csv with own code (pandas + ref_model), and R2: branch identification from the
consensus nowcast variance. Inputs: ../../../tests/SPF_NOISE_PROXY/data/micro_*.csv (data), and the environment fit + var_x
recorded in ../../../tests/SPF_NOISE_PROXY/results/analysis.json (inputs, not re-fitted here)."""
import json, numpy as np, pandas as pd, ref_model as R
from scipy.optimize import brentq
d = json.load(open('../../../tests/SPF_NOISE_PROXY/results/analysis.json'))['per_var']
def rvar(z):
    q75, q25 = np.percentile(z, [75, 25]); return ((q75 - q25) / 1.349) ** 2
out = {}
for v, r in d.items():
    m = pd.read_csv(f'../../../tests/SPF_NOISE_PROXY/data/micro_{v}.csv'); m = m[m.h == 0]
    m['cons'] = m.groupby('survey_q').f.transform('mean'); m['dev'] = m.f - m.cons
    m['fe'] = m.groupby('id').dev.transform('mean'); m['nobs'] = m.groupby('id').dev.transform('size')
    cnt = m.groupby('survey_q').size()
    keep = cnt[cnt >= 10].index
    Dw = []
    for q in keep:
        g = m[(m.survey_q == q) & (m.nobs >= 8)]
        if len(g) >= 10: Dw.append(rvar((g.dev - g.fe).values))
    cons = m[m.survey_q.isin(keep)].groupby('survey_q').cons.first().values
    T = len(keep); nf = float(m[m.survey_q.isin(keep)].groupby('survey_q').size().median())
    f = r['fit']; W = R.World(f['tauE'], f['alpha'], f['phi']); vx = r['var_x']
    lev = np.mean(Dw) / vx
    Ks = np.exp(np.linspace(np.log(1e-5), np.log(1e7), 360))
    Dc = np.array([R.disp(K, R.weights_single(W, K, 0), nf) for K in Ks])
    ip = int(np.argmax(Dc))
    f1 = lambda lk: R.disp(np.exp(lk), R.weights_single(W, np.exp(lk), 0), nf) - lev
    Klo = np.exp(brentq(f1, np.log(Ks[0]), np.log(Ks[ip]))) if lev < Dc[ip] else None
    Khi = np.exp(brentq(f1, np.log(Ks[ip]), np.log(Ks[-1]))) if (lev < Dc[ip] and Dc[-1] < lev) else None
    vc_obs = float(np.var(cons)) / vx
    vc = lambda K: R.nowcast_cons_var(W, K, nf, T=T)
    rec = dict(T=T, nf=nf, level=lev, peak_level=float(Dc[ip]), K_peak=float(Ks[ip]), level_over_peak=lev / Dc[ip],
               K_lower=Klo, K_upper=Khi, K_L0w_pipeline=r['K']['L0w'],
               cons_var_obs=vc_obs, cons_var_pred_lower=vc(Klo) if Klo else None, cons_var_pred_upper=vc(Khi) if Khi else None,
               beta_lower=R.cg_beta(W, Klo, nf) if Klo else None, beta_upper=R.cg_beta(W, Khi, nf) if Khi else None,
               beta_hat=r['beta_hat_LFK'], in_validated_K_range=bool(Klo and 0.01 <= Klo <= 1.0))
    out[v] = rec
    print(v, {k: (round(x, 4) if isinstance(x, float) else x) for k, x in rec.items()}, flush=True)
json.dump(out, open('results/reproduce.json', 'w'), indent=1)
