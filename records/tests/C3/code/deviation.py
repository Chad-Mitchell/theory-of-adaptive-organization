"""NOTE (corrected after inspection): analyze.py, written before outcome data were pulled but not hashed, codes non-archived repos whose last commit is before t0 as events at t0+0.5d (30 repos). The PREREG.md text would censor them at tend. L_literal reproduces the PREREG text exactly. D2 drops all 37 flagged repos.
DEVIATION analysis (not preregistered): 37 repos whose last default-branch commit fell in the gap
(before t0) were coded 'censored at tend' by the literal prereg rule, although they made no commits
during the risk period. D1 codes them as events at t0+0.5d; D2 drops them. Also re-pulls nothing."""
import json, numpy as np, pandas as pd, statsmodels.formula.api as smf
from scipy import stats
from lifelines import CoxPHFitter
d0 = pd.read_csv('<local>/gtao/tests/C3/data/analysis_dataset.csv')
def fit(df, cols):
    c = CoxPHFitter(); c.fit(df[cols + ['T', 'E']], 'T', 'E'); return c
out = {}
T0=pd.Timestamp('2023-07-01',tz='UTC'); TEND=pd.Timestamp('2025-10-31T23:59:59',tz='UTC')
arch=pd.to_datetime(d0.archivedAt,utc=True); inwin=arch.notna()&(arch>=T0)&(arch<=TEND)
lit=d0.flag_lc_before_t0 & ~inwin
L=d0.assign(E=np.where(lit,0,d0.E), T=np.where(lit,(TEND-T0).total_seconds()/86400,d0['T']))
for name, d in [('L_literal_prereg', L), ('D1_events_at_t0', d0.assign(E=np.where(d0.flag_lc_before_t0, 1, d0.E), T=np.where(d0.flag_lc_before_t0, 0.5, d0['T']))),
                ('D2_dropped', d0[~d0.flag_lc_before_t0].copy())]:
    c = fit(d, ['ls', 'lB', 'ltau']); cr = fit(d, ['idx']); LR = 2 * (c.log_likelihood_ - cr.log_likelihood_)
    r = {'n': len(d), 'events': int(d.E.sum())}
    for k in ['ls', 'lB', 'ltau']:
        r[k] = [round(float(c.params_[k]), 3), round(float(c.confidence_intervals_.loc[k].iloc[0]), 3), round(float(c.confidence_intervals_.loc[k].iloc[1]), 3)]
    r['r_B'], r['r_tau'] = float(c.params_.lB / c.params_.ls), float(c.params_.ltau / c.params_.ls)
    r['LR_p'] = float(stats.chi2.sf(LR, 2))
    for v in ['ltau', 'lsb']: d[v + 'c'] = d[v] - d[v].mean()
    m = smf.ols('E ~ ltauc * lsbc', d).fit(cov_type='HC1')
    r['P2_interaction'] = [round(float(m.params['ltauc:lsbc']), 4), round(float(m.conf_int().loc['ltauc:lsbc', 0]), 4), round(float(m.conf_int().loc['ltauc:lsbc', 1]), 4)]
    out[name] = r
json.dump(out, open('<local>/gtao/tests/C3/deviation_results.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
