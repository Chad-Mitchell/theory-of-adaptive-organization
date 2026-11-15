"""Stage 6: merge stages into analysis_dataset.csv (Arm P), placebo.csv (Arm Q), analysis_w.csv (Arm W).
Inclusion (PREREG 2): resolved, non-fork repo created >=365d before R, not archived before R, >=1 human
commit in [R-365d, R) (B>=1), E measurable (Arms P/Q: >=1 counted .py file). Dedupe per (repo, shock):
keep the package with the latest pre-shock release, ties alphabetical. alive_L kept as a column
(primary sample = alive_L==1; S4 uses all)."""
import json, numpy as np, pandas as pd
from common import *
C = pd.read_csv(f'{D}/candidates_resolved.csv')
cp = {(d['repo'], d['R']): d['res'] for d in map(json.loads, open(f'{D}/commits_pre.jsonl'))}
C['B'] = [(cp.get((r, R)) or {}).get('authors', 0) for r, R in zip(C.repo, C.R)]
C['commits_pre'] = [(cp.get((r, R)) or {}).get('human_est', 0) for r, R in zip(C.repo, C.R)]
C['B_capped'] = [(cp.get((r, R)) or {}).get('capped', False) for r, R in zip(C.repo, C.R)]
C['age_days'] = [(dt(R) - dt(c)).days for R, c in zip(C.R, C.createdAt)]
C['nrel730'] = C.n_rel_730
C['cad_days'] = 730 / C.nrel730.clip(lower=1)
flow = {'resolved_candidates': C.groupby('arm').size().to_dict()}
C = C[C.B >= 1]; flow['B>=1'] = C.groupby('arm').size().to_dict()
X = pd.DataFrame([json.loads(l) for l in open(f'{D}/exposure.jsonl')])
X = X[X.get('n_py', pd.Series(dtype=float)).fillna(0) > 0] if 'n_py' in X else X.iloc[0:0]
X['E'] = (X.k_import + 0.5) / (X.n_py + 1)
X['last_pre_version'] = X.ver.astype(str)
C['last_pre_version'] = C.last_pre_version.astype(str)
C = C.merge(X[['pkg', 'last_pre_version', 'shock', 'E', 'k_import', 'n_py']], on=['pkg', 'last_pre_version', 'shock'], how='left')
C = C[(C.arm == 'W') | C.E.notna()]; flow['E_measurable'] = C.groupby('arm').size().to_dict()
C = C.sort_values(['repo', 'shock', 'arm', 'last_pre_date', 'pkg'], ascending=[True, True, True, False, True]).drop_duplicates(['repo', 'shock', 'arm'])
flow['dedup_repo_shock'] = C.groupby('arm').size().to_dict()
T = pd.DataFrame([json.loads(l) for l in open(f'{D}/tau.jsonl')])
C = C.merge(T[['pkg', 'shock', 'tau_days', 'unfixed', 'latency_days', 'alive_L']], on=['pkg', 'shock'], how='inner')
flow['tau_measured'] = C.groupby('arm').size().to_dict()
flow['alive_L'] = C[C.alive_L == 1].groupby('arm').size().to_dict()
try:
    O = pd.DataFrame([json.loads(l) for l in open(f'{D}/outcome.jsonl')])
    C = C.merge(O[['pkg', 'shock', 'D'] + [c for c in ['stars_pre', 'stars_post'] if c in O]], on=['pkg', 'shock'], how='left')
except FileNotFoundError:
    C['D'] = np.nan
for c in ['stars_pre', 'stars_post']:
    if c not in C: C[c] = np.nan
cols = ['repo', 'pkg', 'valiev', 'shock', 'D', 'tau_days', 'unfixed', 'latency_days', 'alive_L', 'E', 'B', 'B_capped', 'commits_pre', 'nrel730', 'cad_days', 'age_days', 'stars_pre', 'stars_post', 'spec', 'k_import', 'n_py']
for arm, fn in [('P', 'analysis_dataset.csv'), ('Q', 'placebo.csv'), ('W', 'analysis_w.csv')]:
    s = C[C.arm == arm]
    s = s[s.D.notna()] if s.D.notna().any() else s
    s[cols].to_csv(f'{D}/{fn}', index=False)
json.dump(flow, open(f'{D}/flow.json', 'w'), indent=1, default=int)
print(json.dumps(flow, indent=1, default=int))
