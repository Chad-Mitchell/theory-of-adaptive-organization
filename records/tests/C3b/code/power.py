"""Power by simulation (assumed covariate distributions; no real data). Also writes a synthetic
dataset to /tmp/c3bsyn/data for testing analyze.py end-to-end."""
import numpy as np, pandas as pd, statsmodels.formula.api as smf, os, sys
rng = np.random.default_rng(20261114)
def sim(n, b_tau=0.25, b_int=0.03, p0=0.30):
    shock = rng.choice(['numpy', 'pydantic', 'sqlalchemy', 'pandas', 'urllib3'], n)
    lB = np.log(rng.integers(1, 15, n)); lE = np.log(rng.beta(1, 4, n).clip(0.005))
    act = rng.normal(0, 1, n)                              # latent activity
    ltau = np.clip(4.0 - 0.6 * act + rng.normal(0, 1.1, n), 0, np.log(365))
    lcommits = np.clip(3 + 0.9 * act + rng.normal(0, 0.8, n), 0, None); lrel = np.clip(1.5 + 0.5 * act + rng.normal(0, .5, n), 0, None)
    lage = rng.normal(8, 0.5, n)
    lin = np.log(p0 / (1 - p0)) + b_tau * (ltau - 4) - 0.4 * (lB - 1.5) + 0.1 * (lE + 2) - 0.3 * act
    lEB = lE - lB
    pr = 1 / (1 + np.exp(-lin)) + b_int * (ltau - ltau.mean()) * (lEB - lEB.mean())
    D = rng.random(n) < pr.clip(0.01, 0.99)
    return pd.DataFrame(dict(shock=shock, repo=[f'r{i}' for i in range(n)], D=D.astype(int), tau_days=np.exp(ltau),
        unfixed=(ltau >= np.log(365) - 1e-9).astype(int), E=np.exp(lE), B=np.exp(lB).round(), commits_pre=np.expm1(lcommits).round(),
        nrel730=np.expm1(lrel).round(), age_days=np.exp(lage), latency_days=np.exp(np.clip(ltau - rng.exponential(.5, n), 0, None)),
        cad_days=730 / np.expm1(lrel).round().clip(1), alive_L=1, stars_pre=rng.poisson(20, n), stars_post=rng.poisson(15, n)))
def power(n, b_tau, b_int, reps=300):
    h1 = h2 = k1 = 0
    for _ in range(reps):
        df = sim(n, b_tau, b_int)
        df['ltau'] = np.log(df.tau_days.clip(1, 365)); df['lB'] = np.log(df.B.clip(lower=1)); df['lE'] = np.log(df.E)
        df['lcommits'] = np.log1p(df.commits_pre); df['lrel'] = np.log1p(df.nrel730); df['lage'] = np.log(df.age_days)
        df['lEB'] = df.lE - df.lB
        for c in ['ltau', 'lEB']: df['c_' + c] = df[c] - df[c].mean()
        try:
            r = smf.logit('D ~ ltau + lE + lB + lcommits + lrel + lage + C(shock)', df).fit(disp=0)
            lo, hi = r.conf_int().loc['ltau']; h1 += lo > 0; k1 += hi < 0.15
            o = smf.ols('D ~ c_ltau * c_lEB + lcommits + lrel + lage + C(shock)', df).fit(cov_type='HC1')
            h2 += o.conf_int().loc['c_ltau:c_lEB'][0] > 0
        except Exception: pass
    return h1 / reps, h2 / reps, k1 / reps
if __name__ == '__main__':
    if 'syn' in sys.argv:
        os.makedirs('/tmp/c3bsyn/data', exist_ok=True)
        sim(800).to_csv('/tmp/c3bsyn/data/analysis_dataset.csv', index=False)
        w = sim(600).drop(columns=['E']); w['shock'] = 'py312'; w.to_csv('/tmp/c3bsyn/data/analysis_w.csv', index=False)
        sim(900, b_tau=0).to_csv('/tmp/c3bsyn/data/placebo.csv', index=False); print('syn written'); sys.exit()
    print('n, b_tau, b_int -> P(H1 CI>0), P(H2 CI>0), P(K1 fires)')
    for n in [150, 300, 600, 1200]:
        for bt, bi in [(0.25, 0.03), (0.15, 0.015), (0.0, 0.0)]:
            print(n, bt, bi, power(n, bt, bi), flush=True)
