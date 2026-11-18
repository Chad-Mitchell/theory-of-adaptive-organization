"""Real pre-shock n for C3b Arm P (pick 31). Reads ONLY stage-1/2 pre-shock outputs in <local>/gtao/tests/C3b/data
(candidates_resolved.csv = rules 1-3 applied by screen_github.py; commits_pre.jsonl = human commits in [R-365d, R)).
Applies rule 4 (>= 1 human commit) and the dedupe (one row per repo x shock: latest pre-shock release, ties alphabetical).
Rules 5 (exposure, stage 3 not run) and 6 (landmark at L, post-shock) are NOT applied, so this is an upper bound."""
import pandas as pd, json
D = '<local>/gtao/tests/C3b/data'
C = pd.read_csv(f'{D}/candidates_resolved.csv')
cm = {(d['repo'], d['R']): d['res'] for d in map(json.loads, open(f'{D}/commits_pre.jsonl'))}
C['human'] = [(cm.get((r, R)) or {}).get('human_est') for r, R in zip(C.repo, C.R)]
P = C[(C.arm == 'P') & (C.human.fillna(0) >= 1)]
P = P.sort_values(['last_pre_date', 'pkg'], ascending=[False, True]).drop_duplicates(['repo', 'shock'])
out = {'stage2_rows_by_arm': C.groupby('arm').size().to_dict(), 'armP_rules1to4_dedup': len(P),
       'by_shock': P.groupby('shock').size().to_dict(), 'unique_repos': int(P.repo.nunique()), 'valiev_subset': int(P.valiev.sum())}
print(json.dumps(out))
