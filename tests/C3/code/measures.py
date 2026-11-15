"""Compute σ, B, τ per repo from issues.jsonl (window 2021), per PREREG §3."""
import json, numpy as np, pandas as pd
from lifelines import KaplanMeierFitter
D = '/workspace/gtao/tests/C3/data'
BOTS = {'dependabot','dependabot-preview','renovate','pre-commit-ci','pyup-bot','greenkeeper','codecov',
        'allcontributors','github-actions','stale','mergify','imgbot','snyk-bot'}
NONCORE = {'NONE','CONTRIBUTOR','FIRST_TIMER','FIRST_TIME_CONTRIBUTOR','MANNEQUIN'}
W0, W1, CENS = pd.Timestamp('2021-01-01', tz='UTC'), pd.Timestamp('2022-01-01', tz='UTC'), pd.Timestamp('2022-06-30T23:59:59', tz='UTC')
CAP = 546.0
def isbot(login, typ):
    if login is None: return False
    l = login.lower()
    return typ == 'Bot' or l.endswith('[bot]') or l in BOTS
def km_median(dur, ev):
    if len(dur) == 0: return np.nan, True
    k = KaplanMeierFitter().fit(dur, ev)
    m = k.median_survival_time_
    return (CAP, True) if not np.isfinite(m) else (float(m), False)
rows = []
for line in open(f'{D}/issues.jsonl'):
    r = json.loads(line)
    if r['err'] and not r['items']:
        rows.append({'repo': r['repo'], 'issues_err': r['err']}); continue
    df = pd.DataFrame(r['items'], columns=['num','pr','created','closed','login','utype','assoc','labels','reason'])
    df = df[~df.apply(lambda x: isbot(x.login, x.utype), axis=1)]
    df['created'] = pd.to_datetime(df.created, utc=True); df['closed'] = pd.to_datetime(df.closed, utc=True)
    in21 = (df.created >= W0) & (df.created < W1)
    months = pd.period_range('2021-01', '2021-12', freq='M')
    nc = df[in21 & df.assoc.isin(NONCORE)].created.dt.tz_localize(None).dt.to_period('M').value_counts().reindex(months, fill_value=0)
    cl = df[(df.closed >= W0) & (df.closed < W1)].closed.dt.tz_localize(None).dt.to_period('M').value_counts().reindex(months, fill_value=0)
    iss = df[in21 & ~df.pr].copy()
    end = iss.closed.where(iss.closed.notna() & (iss.closed <= CENS), CENS)
    dur = ((end - iss.created).dt.total_seconds() / 86400).clip(lower=1/1440)
    ev = (iss.closed.notna() & (iss.closed <= CENS)).astype(int)
    tau, capped = km_median(dur, ev)
    # S3: not_planned closes censored
    ev3 = ev & (iss.reason != 'not_planned')
    tau3, _ = km_median(dur, ev3.astype(int))
    # S5: bug-labeled only
    bug = iss.labels.apply(lambda ls: any('bug' in x.lower() for x in ls))
    tau5 = km_median(dur[bug], ev[bug])[0] if bug.sum() >= 5 else np.nan
    rows.append({'repo': r['repo'], 'issues_err': r['err'], 'pages': r['pages'], 'n_issues21': len(iss),
                 'sigma': nc.std(ddof=1), 'noncore_mean': nc.mean(), 'B': cl.mean(), 'tau': tau, 'tau_capped': capped,
                 'tau_np_cens': tau3, 'tau_bug': tau5, 'n_bug': int(bug.sum()), 'n_items21': int(in21.sum())})
pd.DataFrame(rows).to_csv(f'{D}/measures.csv', index=False)
print(pd.DataFrame(rows).describe().T)
