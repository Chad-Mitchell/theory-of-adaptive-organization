"""Apply PREREG §2 rules 1-3 to screen.jsonl; dedupe by resolved nameWithOwner; sample 2,500 (seed 20261113)."""
import json, numpy as np, pandas as pd
D = '<local>/gtao/tests/C3/data'
rows = []
for l in open(f'{D}/screen.jsonl'):
    r = json.loads(l); res = r['res']
    if r.get('err'): rows.append({'key': r['key'], 'status': 'query_error'}); continue
    if not res: rows.append({'key': r['key'], 'status': 'not_found'}); continue
    t = ((res.get('defaultBranchRef') or {}).get('target') or {})
    rows.append({'key': r['key'], 'status': 'ok', 'nwo': res['nameWithOwner'].lower(), 'fork': res['isFork'],
                 'created': res['createdAt'], 'owner_type': res['owner']['__typename'],
                 'c21': (t.get('c21') or {}).get('totalCount', 0), 'cgap': (t.get('cgap') or {}).get('totalCount', 0)})
s = pd.DataFrame(rows)
print(s.status.value_counts())
ok = s[s.status == 'ok'].drop_duplicates('nwo')
print('unique resolved repos', len(ok))
f1 = ok[(~ok.fork) & (ok.created < '2020-01-01')]; print('rule1', len(f1))
f2 = f1[f1.c21 >= 12]; print('rule2', len(f2))
f3 = f2[f2.cgap >= 1]; print('rule3 (commit part)', len(f3))
f3.to_csv(f'{D}/screen_passed.csv', index=False)
samp = f3.sample(n=min(2500, len(f3)), random_state=np.random.RandomState(20261113)) if len(f3) > 2500 else f3
open(f'{D}/sample_repos.txt', 'w').write('\n'.join(samp.nwo) + '\n')
samp.to_csv(f'{D}/sample_screen.csv', index=False); print('sampled', len(samp))
