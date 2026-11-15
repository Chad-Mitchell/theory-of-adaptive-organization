"""Stage 2 (PRE-SHOCK data only): candidate rows from screen_pypi -> repo resolution, fork, createdAt,
archived-before-R flag, human commits and distinct human authors in [R-365d, R)."""
import json, os, random
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from common import *

rows = []
for l in open(f'{D}/screen_pypi.jsonl'):
    try: r = json.loads(l)
    except Exception: continue  # truncated line from a restart
    if r.get('status') != 'ok': continue
    for lib, e in r.get('shocks', {}).items():
        if dt(e['last_pre_date']) < SHOCKS[lib]['R'] - PRE_RELEASE_WINDOW or not e.get('requires_known'): continue
        if e.get('depends') and e.get('pinned_out'): arm = 'P'
        elif e.get('depends'): arm = 'Q'
        else: continue
        rows.append(dict(pkg=r['pkg'], url=r['url'], arm=arm, shock=lib, R=SHOCKS[lib]['R'].isoformat(), **{k: e[k] for k in ['last_pre_version', 'last_pre_date', 'n_rel_730', 'spec']}))
    w = r.get('w')
    if w and w['cp311'] and not w['abi3'] and dt(w['last_pre_date']) >= PY312_R - PRE_RELEASE_WINDOW:
        rows.append(dict(pkg=r['pkg'], url=r['url'], arm='W', shock='py312', R=PY312_R.isoformat(), last_pre_version=w['last_pre_version'],
                         last_pre_date=w['last_pre_date'], n_rel_730=w['n_rel_730'], spec='', cp312_pre=w['cp312_pre']))
C = pd.DataFrame(rows)
from packaging.utils import canonicalize_name
_v = pd.read_csv(f'{D}/package_urls.csv'); _v.columns = ['pkg', 'url']
VAL = {canonicalize_name(str(p)) for p in _v.pkg.dropna()}
C['valiev'] = C.pkg.map(lambda p: int(canonicalize_name(str(p)) in VAL))
print(C.groupby(['arm', 'shock']).size(), flush=True)
# caps (prereg 2.4): placebo Q <= 2000 rows, Arm W <= 2500 rows, simple random, seed 20261114
parts = []
for arm, cap in [('P', 5000), ('Q', 2000), ('W', 2500)]:  # P cap added by Addendum A1
    s = C[C.arm == arm]
    parts.append(s.sample(n=min(cap, len(s)), random_state=20261114) if len(s) > cap else s)
C = pd.concat(parts, ignore_index=True)
C.to_csv(f'{D}/candidates.csv', index=False)

# resolve repos
urls = sorted(set(C.url.str.lower().str.strip('/').str.removesuffix('.git')))
RES = f'{D}/repos_pre.jsonl'
done = {json.loads(l)['url'] for l in open(RES)} if os.path.exists(RES) else set()
FR = 'r%d: repository(owner:%s, name:%s){ nameWithOwner isFork createdAt archivedAt }'
Rs_by_url = C.assign(u=C.url.str.lower().str.strip('/').str.removesuffix('.git')).groupby('u').R.apply(lambda x: sorted(set(x))).to_dict()
todo = [u for u in urls if u not in done and re.fullmatch(r'github\.com/[\w.-]+/[\w.-]+', u)]
with open(RES, 'a') as f:
    for s in range(0, len(todo), 40):
        b = todo[s:s + 40]
        q = '{' + '\n'.join(FR % (i, json.dumps(u.split('/')[1]), json.dumps(u.split('/')[2])) for i, u in enumerate(b)) + '}'
        d = gql(q) or {}
        data = d.get('data') or {}
        for i, u in enumerate(b):
            x = data.get(f'r{i}')
            # blinding: archivedAt is NOT stored; only per-R flags "archived before R"
            if x:
                a = x.pop('archivedAt', None)
                x['archived_before'] = {R: bool(a) and dt(a) < dt(R) for R in Rs_by_url.get(u, [])}
            f.write(json.dumps({'url': u, 'res': x}) + '\n')
print('repos resolved', flush=True)
rep = {}
for l in open(RES):
    d = json.loads(l); rep[d['url']] = d['res']
C['ukey'] = C.url.str.lower().str.strip('/').str.removesuffix('.git')
C['repo'] = C.ukey.map(lambda u: (rep.get(u) or {}).get('nameWithOwner'))
C['isFork'] = C.ukey.map(lambda u: (rep.get(u) or {}).get('isFork'))
C['createdAt'] = C.ukey.map(lambda u: (rep.get(u) or {}).get('createdAt'))
C['archived_before_R'] = [bool(((rep.get(u) or {}).get('archived_before') or {}).get(R)) for u, R in zip(C.ukey, C.R)]
C = C[C.repo.notna() & (C.isFork == False) & ~C.archived_before_R]
C = C[[dt(c) < dt(R) - timedelta(days=365) for c, R in zip(C.createdAt, C.R)]]
C.drop(columns=['archived_before_R']).to_csv(f'{D}/candidates_resolved.csv', index=False)
pairs = sorted(set(zip(C.repo, C.R)))
print('repo x R pairs', len(pairs), flush=True)
OUT = f'{D}/commits_pre.jsonl'
done = {(json.loads(l)['repo'], json.loads(l)['R']) for l in open(OUT)} if os.path.exists(OUT) else set()
todo = [p for p in pairs if p not in done]
def one(p):
    repo, R = p; R = dt(R)
    return {'repo': repo, 'R': p[1], 'res': commits_window(repo, R - PRE_COMMIT_WINDOW, R, maxpages=10)}
with open(OUT, 'a') as f, ThreadPoolExecutor(6) as ex:
    for k, r in enumerate(ex.map(one, todo)):
        f.write(json.dumps(r) + '\n')
        if k % 200 == 0: print(k, len(todo), time.strftime('%H:%M:%S'), flush=True)
print('done', time.strftime('%Y-%m-%dT%H:%M:%S%z'))
