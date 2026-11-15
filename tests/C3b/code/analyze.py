"""C3b preregistered analysis. Input: data/analysis_dataset.csv (one row per repo x shock, Arm P) and
data/analysis_w.csv (Arm W), data/placebo.csv (placebo arm). Output: results.json + printed report.
Written before any post-shock data were pulled. Usage: python3 analyze.py [dataset_dir]"""
import sys, json, numpy as np, pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
from scipy import stats

DD = sys.argv[1] if len(sys.argv) > 1 else '/workspace/gtao/tests/C3b/data'
SEED = 20261114; NBOOT = 1000; SESOI = 0.15
CTRL = 'lcommits + lrel + lage'
res = {}

def prep(df):
    df = df.copy()
    df['ltau'] = np.log(df.tau_days.clip(1, 365))
    df['lB'] = np.log(df.B.clip(lower=1))
    df['lcommits'] = np.log1p(df.commits_pre)
    df['lrel'] = np.log1p(df.nrel730)
    df['lage'] = np.log(df.age_days.clip(lower=30))
    if 'E' in df: df['lE'] = np.log(df.E)
    if 'latency_days' in df: df['llat'] = np.log(df.latency_days.clip(1, 365))
    return df

def logit(f, df, cluster=True):
    m = smf.logit(f, df)
    return m.fit(disp=0, maxiter=200, cov_type='cluster', cov_kwds={'groups': pd.factorize(df.repo)[0]}) if cluster else m.fit(disp=0, maxiter=200)

def ols(f, df):
    return smf.ols(f, df).fit(cov_type='cluster', cov_kwds={'groups': pd.factorize(df.repo)[0]})

def coef(r, k):
    ci = r.conf_int().loc[k]
    return {'b': float(r.params[k]), 'lo': float(ci[0]), 'hi': float(ci[1]), 'p': float(r.pvalues[k])}

def fe(df): return ' + C(shock)' if df.shock.nunique() > 1 else ''

# ---------------- Arm P (primary) ----------------
P = prep(pd.read_csv(f'{DD}/analysis_dataset.csv'))
P = P[P.alive_L == 1].copy()
res['n'] = int(len(P)); res['events'] = int(P.D.sum()); res['n_repos'] = int(P.repo.nunique())
res['by_shock'] = P.groupby('shock').agg(n=('D', 'size'), events=('D', 'sum'), unfixed=('unfixed', 'mean'),
                                         med_tau=('tau_days', 'median')).reset_index().to_dict('records')
P['lEB'] = P.lE - P.lB
for c in ['ltau', 'lEB']: P['c_' + c] = P[c] - P[c].mean()

# H1: relative scale, logit with controls + shock FE, cluster-robust by repo
h1 = logit(f'D ~ ltau + lE + lB + {CTRL}' + fe(P), P)
res['H1'] = {k: coef(h1, k) for k in ['ltau', 'lE', 'lB']}
# H2: absolute scale interaction (LPM)
h2 = ols(f'D ~ c_ltau * c_lEB + {CTRL}' + fe(P), P)
res['H2'] = {k: coef(h2, k) for k in ['c_ltau', 'c_lEB', 'c_ltau:c_lEB']}
# H2 descriptive: RD (tau above vs at/below median) within E/B terciles
P['tert'] = pd.qcut(P.lEB.rank(method='first'), 3, labels=[1, 2, 3])
P['slow'] = (P.tau_days > P.tau_days.median()).astype(int)
rd = []
for t, g in P.groupby('tert', observed=True):
    a, b = g[g.slow == 1].D, g[g.slow == 0].D
    d = a.mean() - b.mean(); se = np.sqrt(a.var(ddof=1) / max(len(a), 1) + b.var(ddof=1) / max(len(b), 1))
    rd.append({'tercile': int(t), 'n': int(len(g)), 'event_rate': float(g.D.mean()), 'rd': float(d), 'lo': float(d - 1.96 * se), 'hi': float(d + 1.96 * se)})
res['H2_terciles'] = rd
# S9 specificity: add latency to first post-shock release of any kind
s9 = logit(f'D ~ ltau + llat + lE + lB + {CTRL}' + fe(P), P)
res['S9'] = {k: coef(s9, k) for k in ['ltau', 'llat']}
res['S9']['ltau']['lo90'] = float(s9.conf_int(alpha=0.10).loc['ltau'][0])

# H3: index form (pure, shock FE only)
free = logit('D ~ lE + lB + ltau' + fe(P), P, cluster=False)
P['z'] = P.lE - P.lB + 0.5 * P.ltau
rest = logit('D ~ z' + fe(P), P, cluster=False)
lr = 2 * (free.llf - rest.llf); lrp = float(stats.chi2.sf(lr, 2))
freec = logit('D ~ lE + lB + ltau' + fe(P), P)
rng = np.random.default_rng(SEED); repos = P.repo.unique(); grp = {r: g for r, g in P.groupby('repo')}
rb, rt = [], []
for i in range(NBOOT):
    s = pd.concat([grp[r] for r in rng.choice(repos, len(repos))], ignore_index=True)
    try:
        f = smf.logit('D ~ lE + lB + ltau' + fe(s), s).fit(disp=0, maxiter=200)
        rb.append(f.params['lB'] / f.params['lE']); rt.append(f.params['ltau'] / f.params['lE'])
    except Exception: pass
rB = float(free.params['lB'] / free.params['lE']); rT = float(free.params['ltau'] / free.params['lE'])
res['H3'] = {**{k: coef(freec, k) for k in ['lE', 'lB', 'ltau']}, 'r_B': rB, 'r_tau': rT,
             'r_B_ci': [float(np.percentile(rb, 2.5)), float(np.percentile(rb, 97.5))],
             'r_tau_ci': [float(np.percentile(rt, 2.5)), float(np.percentile(rt, 97.5))],
             'LR': float(lr), 'LR_p': lrp, 'nboot_ok': len(rb), 'z_coef': coef(rest, 'z')}

# ---------------- Verdicts (PREREG section 6) ----------------
b1, b2 = res['H1']['ltau'], res['H2']['c_ltau:c_lEB']
K1 = b1['hi'] < SESOI; K2 = b2['hi'] < 0
if K1 or K2: mech = 'MISS'
elif b1['lo'] > 0 and b2['lo'] > 0 and res['S9']['ltau']['lo90'] > 0: mech = 'HIT'
else: mech = 'INCONCLUSIVE'
partial = (not K1 and not K2 and b1['lo'] > 0 and res['S9']['ltau']['lo90'] > 0 and b2['lo'] <= 0)
h3 = res['H3']
inb = lambda x, lo, hi: lo <= x <= hi
K3 = (h3['r_tau_ci'][1] < 0.25 or h3['r_tau_ci'][0] > 1.0 or h3['ltau']['hi'] < SESOI
      or h3['r_B_ci'][1] < -2 or h3['r_B_ci'][0] > -0.5
      or (lrp < 0.01 and not (inb(rB, -2, -0.5) and inb(rT, 0.25, 1.0))))
if K3: idx = 'MISS'
elif (h3['lE']['lo'] > 0 and h3['lB']['hi'] < 0 and h3['ltau']['lo'] > 0 and inb(rB, -2, -0.5)
      and inb(rT, 0.25, 1.0) and lrp >= 0.01): idx = 'HIT'
else: idx = 'INCONCLUSIVE'
res['verdict'] = {'mechanism': mech, 'mechanism_partial_H1_only': bool(partial), 'K1': bool(K1), 'K2': bool(K2),
                  'index': idx, 'K3': bool(K3)}

# ---------------- Sensitivity (reported, not decisive) ----------------
sens = {}
def tryfit(name, fn):
    try: sens[name] = fn()
    except Exception as e: sens[name] = {'error': str(e)[:200]}
sens_specs = {
    'S1_no_controls': lambda: coef(logit('D ~ ltau + lE + lB' + fe(P), P), 'ltau'),
    'S2_fixed_only': lambda: coef(logit(f'D ~ ltau + lE + lB + {CTRL}' + fe(P[P.unfixed == 0]), P[P.unfixed == 0]), 'ltau'),
    'S3_unfixed_binary': lambda: coef(logit(f'D ~ unfixed + lE + lB + {CTRL}' + fe(P), P), 'unfixed'),
    'S7_tau_over_cadence': lambda: coef(logit(f'D ~ I(ltau - np.log(cad_days.clip(1))) + lE + lB + {CTRL}' + fe(P), P), 'I(ltau - np.log(cad_days.clip(1)))'),
    'S8_lpm_h1': lambda: coef(ols(f'D ~ ltau + lE + lB + {CTRL}' + fe(P), P), 'ltau'),
}
for k, f in sens_specs.items(): tryfit(k, f)
per = {}
for s, g in P.groupby('shock'):
    try: per[s] = {'n': int(len(g)), 'events': int(g.D.sum()), **coef(logit(f'D ~ ltau + lE + lB + {CTRL}', g), 'ltau')}
    except Exception as e: per[s] = {'n': int(len(g)), 'error': str(e)[:120]}
sens['S5_per_shock'] = per
# S4: no landmark (all shocked-at-baseline rows)
P0 = prep(pd.read_csv(f'{DD}/analysis_dataset.csv'))
tryfit('S4_no_landmark', lambda: {**coef(logit(f'D ~ ltau + lE + lB + {CTRL}' + fe(P0), P0), 'ltau'), 'n': int(len(P0)), 'events': int(P0.D.sum())})
# S6: secondary outcome, star growth log ratio (OLS), repos with stars measured
S = P.dropna(subset=['stars_pre', 'stars_post']).copy()
S['lstar'] = np.log1p(S.stars_post) - np.log1p(S.stars_pre)
tryfit('S6_stars', lambda: {**coef(ols(f'lstar ~ ltau + lE + lB + {CTRL}' + fe(S), S), 'ltau'), 'n': int(len(S)),
                            'interaction': coef(ols(f'lstar ~ c_ltau * c_lEB + {CTRL}' + fe(S), S), 'c_ltau:c_lEB')})
if 'valiev' in P:
    V = P[P.valiev == 1]
    tryfit('S10_valiev_frame_only', lambda: {**coef(logit(f'D ~ ltau + lE + lB + {CTRL}' + fe(V), V), 'ltau'), 'n': int(len(V)), 'events': int(V.D.sum())})
# ---- Addendum A2 secondaries ----
# S12: complementary log-log (interval-censored PH) version of H1 -> hazard ratio per doubling of tau
def s12():
    r = smf.glm(f'D ~ ltau + lE + lB + {CTRL}' + fe(P), P, family=sm.families.Binomial(link=sm.families.links.CLogLog())).fit(
        cov_type='cluster', cov_kwds={'groups': pd.factorize(P.repo)[0]})
    c = coef(r, 'ltau')
    return {**c, 'HR_per_doubling': float(2 ** c['b']), 'HR_ci': [float(2 ** c['lo']), float(2 ** c['hi'])]}
tryfit('S12_cloglog_H1', s12)
# S11: distribution of adapt times (tau) across dependents: KM with censoring at 365, shape diagnostics
def tau_shape(df):
    from lifelines import KaplanMeierFitter
    k = KaplanMeierFitter().fit(df.tau_days, event_observed=1 - df.unfixed)
    fx = df.loc[df.unfixed == 0, 'tau_days'].values
    lt = np.log(fx)
    srt = np.sort(fx)[::-1]; kk = max(10, len(srt) // 10)
    hill = float(1 / np.mean(np.log(srt[:kk] / srt[kk]))) if len(srt) > kk + 1 else None
    lam = (1 - df.unfixed).sum() / df.tau_days.sum()  # exponential MLE with censoring at 365
    km_q = {}
    for x in [0.25, 0.5, 0.75]:
        v = k.percentile(1 - x); km_q[str(x)] = float(v) if np.isfinite(v) else None
    return {'n': int(len(df)), 'share_unfixed': float(df.unfixed.mean()), 'km_quantiles': km_q,
            'exp_fit_quantiles': {str(x): float(-np.log(1 - x) / lam) for x in [0.25, 0.5, 0.75]},
            'cv_fixed': float(fx.std(ddof=1) / fx.mean()) if len(fx) > 2 else None,
            'sd_ln_fixed': float(lt.std(ddof=1)) if len(lt) > 2 else None, 'hill_tail_index_top10pct': hill}
tryfit('S11_tau_distribution', lambda: tau_shape(P))
res['sensitivity'] = sens

# ---------------- Secondary arms ----------------
import os
if os.path.exists(f'{DD}/analysis_w.csv'):
    W = prep(pd.read_csv(f'{DD}/analysis_w.csv')); W = W[W.alive_L == 1]
    try:
        w = logit(f'D ~ ltau + lB + {CTRL}', W)
        res['ArmW'] = {'n': int(len(W)), 'events': int(W.D.sum()), 'ltau': coef(w, 'ltau'), 'lB': coef(w, 'lB'),
                       'S9': coef(logit(f'D ~ ltau + llat + lB + {CTRL}', W), 'ltau')}
    except Exception as e: res['ArmW'] = {'error': str(e)[:200]}
if os.path.exists(f'{DD}/placebo.csv'):
    Q = prep(pd.read_csv(f'{DD}/placebo.csv')); Q = Q[Q.alive_L == 1]
    try:
        q = logit(f'D ~ llat + lE + lB + {CTRL}' + fe(Q), Q)
        res['Placebo'] = {'n': int(len(Q)), 'events': int(Q.D.sum()), 'llat': coef(q, 'llat')}
        # same model in Arm P for direct comparison (latency in place of tau)
        res['Placebo']['ArmP_llat_only'] = coef(logit(f'D ~ llat + lE + lB + {CTRL}' + fe(P), P), 'llat')
    except Exception as e: res['Placebo'] = {'error': str(e)[:200]}

json.dump(res, open(f'{DD}/../results.json', 'w'), indent=1, default=float)
print(json.dumps(res, indent=1, default=float))
