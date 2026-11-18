"""Preregistered analysis (PREREG.md §4-6) + clearly labeled exploratory analyses."""
import json, numpy as np, pandas as pd, statsmodels.formula.api as smf
from scipy import stats
from lifelines import CoxPHFitter
from lifelines.statistics import proportional_hazard_test
D = '<local>/gtao/tests/C3/data'
T0, TEND = pd.Timestamp('2023-07-01', tz='UTC'), pd.Timestamp('2025-10-31T23:59:59', tz='UTC')
sc = pd.read_csv(f'{D}/sample_screen.csv'); me = pd.read_csv(f'{D}/measures.csv')
oc = []
for l in open(f'{D}/outcome.jsonl'):
    r = json.loads(l); res = r['res']
    if not res: oc.append({'repo': r['key'], 'oc_missing': True}); continue
    h = (((res.get('defaultBranchRef') or {}).get('target') or {}).get('history') or {}).get('nodes') or []
    oc.append({'repo': r['key'], 'oc_missing': False, 'archivedAt': res['archivedAt'], 'last_commit': h[0]['committedDate'] if h else None})
oc = pd.DataFrame(oc)
d = sc.rename(columns={'nwo': 'repo'}).merge(me, on='repo', how='left').merge(oc, on='repo', how='left')
log = {}
log['sampled'] = len(d)
d = d[d.issues_err.isna()]; log['issues_ok'] = len(d)
d = d[(d.n_issues21 >= 12)]; log['rule4_>=12_issues'] = len(d)
d = d[(d.sigma > 0) & (d.B > 0) & (d.tau > 0)]; log['rule5_sigma_B_pos'] = len(d)
d = d[d.oc_missing == False]; log['outcome_found'] = len(d)
d['arch'] = pd.to_datetime(d.archivedAt, utc=True); d['lc'] = pd.to_datetime(d.last_commit, utc=True)
d = d[~(d.arch < T0)]; log['not_archived_before_t0'] = len(d)
ev_t = []
for a, c in zip(d.arch, d.lc):
    cands = []
    if pd.notna(a) and T0 <= a <= TEND: cands.append(a)
    if pd.notna(c) and T0 <= c <= TEND: cands.append(c)
    if pd.notna(c) and c < T0 and pd.notna(a) is False: cands.append(T0)  # should not occur (gap rule); flagged below
    ev_t.append(min(cands) if cands else pd.NaT)
d['event_time'] = ev_t
d['flag_lc_before_t0'] = d.lc < T0
d['E'] = d.event_time.notna().astype(int)
d['T'] = ((d.event_time.fillna(TEND) - T0).dt.total_seconds() / 86400).clip(lower=0.5)
d['ls'], d['lB'], d['ltau'] = np.log(d.sigma), np.log(d.B), np.log(d.tau)
d['lsb'] = d.ls - d.lB
d['idx'] = d.ls - d.lB + 0.5 * d.ltau
d['age'] = np.log((pd.Timestamp('2021-01-01', tz='UTC') - pd.to_datetime(d.created, utc=True)).dt.days)
d['lc21'] = np.log1p(d.c21); d['org'] = (d.owner_type == 'Organization').astype(int)
d.to_csv(f'{D}/analysis_dataset.csv', index=False)
R = {'flow': log, 'n': len(d), 'events': int(d.E.sum()), 'event_rate': float(d.E.mean()),
     'flag_lastcommit_before_t0': int(d.flag_lc_before_t0.sum()), 'tau_capped': int(d.tau_capped.sum()),
     'corr_ls_lB': float(np.corrcoef(d.ls, d.lB)[0, 1]),
     'medians': d[['sigma', 'B', 'tau', 'noncore_mean', 'n_issues21']].median().to_dict()}
def cox(df, cols, strata=None):
    c = CoxPHFitter(); c.fit(df[cols + ['T', 'E']], 'T', 'E'); return c
# Primary 1
c1 = cox(d, ['ls', 'lB', 'ltau'])
b = c1.params_; ci = c1.confidence_intervals_
R['P1_cox'] = {k: {'beta': float(b[k]), 'lo': float(ci.loc[k].iloc[0]), 'hi': float(ci.loc[k].iloc[1]), 'p': float(c1.summary.loc[k, 'p'])} for k in b.index}
R['P1_ratio_point'] = {'r_B': float(b.lB / b.ls), 'r_tau': float(b.ltau / b.ls)}
cr = cox(d, ['idx']); LR = 2 * (c1.log_likelihood_ - cr.log_likelihood_)
R['P1_LR'] = {'stat': float(LR), 'p': float(stats.chi2.sf(LR, 2)), 'beta_idx': float(cr.params_.idx)}
rng = np.random.RandomState(20261113); bs = []
for i in range(1000):
    s = d.iloc[rng.randint(0, len(d), len(d))]
    try:
        p = cox(s, ['ls', 'lB', 'ltau']).params_; bs.append((p.lB / p.ls, p.ltau / p.ls, p.ls, p.lB, p.ltau))
    except Exception: pass
bs = np.array(bs)
R['P1_boot'] = {'n_ok': len(bs), 'r_B_ci': np.percentile(bs[:, 0], [2.5, 97.5]).tolist(), 'r_tau_ci': np.percentile(bs[:, 1], [2.5, 97.5]).tolist()}
# Primary 2
for v in ['ltau', 'lsb']: d[v + 'c'] = d[v] - d[v].mean()
m2 = smf.ols('E ~ ltauc * lsbc', d).fit(cov_type='HC1')
R['P2_lpm'] = {k: {'b': float(m2.params[k]), 'lo': float(m2.conf_int().loc[k, 0]), 'hi': float(m2.conf_int().loc[k, 1]), 'p': float(m2.pvalues[k])} for k in m2.params.index}
d['terc'] = pd.qcut(d.lsb, 3, labels=['low', 'mid', 'high']); d['slow'] = (d.tau > d.tau.median()).astype(int)
rd = {}
for t, g in d.groupby('terc', observed=True):
    a, z = g[g.slow == 1].E, g[g.slow == 0].E
    diff = a.mean() - z.mean(); se = np.sqrt(a.var() / len(a) + z.var() / len(z))
    rd[t] = {'n': len(g), 'event_rate': float(g.E.mean()), 'rd_slow_minus_fast': float(diff), 'lo': float(diff - 1.96 * se), 'hi': float(diff + 1.96 * se),
             'sigma_over_B_range': [float(np.exp(g.lsb.min())), float(np.exp(g.lsb.max()))], 'near_certain_flag': bool(g.E.mean() > 0.5)}
R['P2_terciles'] = rd
ci_ = cox(d.assign(ix=d.lsbc * d.ltauc), ['lsbc', 'ltauc', 'ix'])
R['shape_cox_interaction'] = {'b': float(ci_.params_.ix), 'lo': float(ci_.confidence_intervals_.loc['ix'].iloc[0]), 'hi': float(ci_.confidence_intervals_.loc['ix'].iloc[1]), 'p': float(ci_.summary.loc['ix', 'p'])}
# Verdict
P, Bt = R['P1_cox'], R['P1_boot']
def outside(ci, lo, hi): return ci[1] < lo or ci[0] > hi
inband = lambda v, lo, hi: lo <= v <= hi
K1 = P['ltau']['beta'] <= 0 or outside(Bt['r_tau_ci'], 0.25, 1.0)
K2 = outside(Bt['r_B_ci'], -2, -0.5) or (R['P1_LR']['p'] < 0.01 and not (inband(R['P1_ratio_point']['r_B'], -2, -.5) and inband(R['P1_ratio_point']['r_tau'], .25, 1)))
K3 = R['P2_lpm']['ltauc:lsbc']['hi'] <= 0
hit = (not (K1 or K2 or K3)) and P['ls']['lo'] > 0 and P['lB']['hi'] < 0 and P['ltau']['lo'] > 0 and inband(R['P1_ratio_point']['r_B'], -2, -.5) \
      and inband(R['P1_ratio_point']['r_tau'], .25, 1) and R['P1_LR']['p'] >= 0.01 and R['P2_lpm']['ltauc:lsbc']['lo'] > 0
R['verdict'] = {'K1': bool(K1), 'K2': bool(K2), 'K3': bool(K3), 'verdict': 'MISS' if (K1 or K2 or K3) else ('HIT' if hit else 'INCONCLUSIVE')}
# Sensitivities
S = {}
def coxsum(c, keys): return {k: [round(float(c.params_[k]), 4), round(float(c.confidence_intervals_.loc[k].iloc[0]), 4), round(float(c.confidence_intervals_.loc[k].iloc[1]), 4)] for k in keys}
S['S1_controls'] = coxsum(cox(d, ['ls', 'lB', 'ltau', 'age', 'lc21', 'org']), ['ls', 'lB', 'ltau', 'age', 'lc21', 'org'])
# S2 discrete-time yearly logit
pp = []
for _, r in d.iterrows():
    for y, (a, z) in enumerate([(0, 365), (365, 731), (731, 854)]):
        if r['T'] <= a: break
        pp.append({'ls': r.ls, 'lB': r.lB, 'ltau': r.ltau, 'y': y, 'ev': int(r.E == 1 and r['T'] <= z)})
pp = pd.DataFrame(pp); lg = smf.logit('ev ~ ls + lB + ltau + C(y)', pp).fit(disp=0, cov_type='cluster', cov_kwds={'groups': np.repeat(np.arange(len(d)), d['T'].apply(lambda t: sum(t > a for a in (0, 365, 731))).values)}) if False else smf.logit('ev ~ ls + lB + ltau + C(y)', pp).fit(disp=0)
S['S2_logit'] = {k: [round(float(lg.params[k]), 4), round(float(lg.conf_int().loc[k, 0]), 4), round(float(lg.conf_int().loc[k, 1]), 4)] for k in ['ls', 'lB', 'ltau']}
S['S2_logit']['ratios'] = [float(lg.params.lB / lg.params.ls), float(lg.params.ltau / lg.params.ls)]
d3 = d[d.tau_np_cens > 0].assign(ltau=lambda x: np.log(x.tau_np_cens)); S['S3_notplanned_censored'] = coxsum(cox(d3, ['ls', 'lB', 'ltau']), ['ls', 'lB', 'ltau']); S['S3_n'] = len(d3)
d4 = d[~d.tau_capped.astype(bool)]; S['S4_drop_capped'] = coxsum(cox(d4, ['ls', 'lB', 'ltau']), ['ls', 'lB', 'ltau']); S['S4_n'] = len(d4)
d5 = d[(d.n_bug >= 5) & (d.tau_bug > 0)].assign(ltau=lambda x: np.log(x.tau_bug)); S['S5_bug_tau'] = coxsum(cox(d5, ['ls', 'lB', 'ltau']), ['ls', 'lB', 'ltau']); S['S5_n'] = len(d5); S['S5_events'] = int(d5.E.sum())
ph = proportional_hazard_test(c1, d[['ls', 'lB', 'ltau', 'T', 'E']], time_transform='rank')
S['S6_schoenfeld_p'] = {k: float(v) for k, v in zip(ph.summary.index, ph.summary.p)}
R['sensitivity'] = S
# EXPLORATORY (not preregistered; added after the parent's steering note, before seeing results of P2)
X = {}
d['quint'] = pd.qcut(d.lsb, 5, labels=False)
X['quintile_rd'] = {}
for q, g in d.groupby('quint'):
    a, z = g[g.slow == 1].E, g[g.slow == 0].E; diff = a.mean() - z.mean(); se = np.sqrt(a.var() / len(a) + z.var() / len(z))
    X['quintile_rd'][int(q)] = {'n': len(g), 'event_rate': round(float(g.E.mean()), 3), 'rd': round(float(diff), 3), 'lo': round(float(diff - 1.96 * se), 3), 'hi': round(float(diff + 1.96 * se), 3)}
mq = smf.ols('E ~ ltauc * (lsbc + I(lsbc**2))', d).fit(cov_type='HC1')
X['lpm_quadratic_interaction'] = {k: [round(float(mq.params[k]), 4), round(float(mq.pvalues[k]), 4)] for k in mq.params.index}
# Univariate tau effect and tau vs size
X['cox_tau_only'] = coxsum(cox(d, ['ltau']), ['ltau'])
X['cox_tau_plus_lsb'] = coxsum(cox(d, ['ltau', 'lsb']), ['ltau', 'lsb'])
X['corr_lt_lB'] = float(np.corrcoef(d.ltau, d.lB)[0, 1]); X['corr_lt_lsb'] = float(np.corrcoef(d.ltau, d.lsb)[0, 1])
R['exploratory'] = X
json.dump(R, open(f'{D}/../results.json', 'w'), indent=1, default=str)
print(json.dumps(R, indent=1, default=str))
