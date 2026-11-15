"""Stage 5 (OUTCOMES). Run only after PREREG.md is hashed and committed.
D = 1 iff [no PyPI file upload in [2025-11-14, pull] AND no human default-branch commit in that window]
        OR [repo archived (or gone) AND no PyPI upload after archivedAt (gone: in window)].
Secondary: GitHub stars gained in [R-365d, R) and [L, L+365d) for repos with <= 10,000 stars."""
import json, os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from common import *

C = pd.read_csv(f'{D}/candidates_resolved.csv')
T = pd.DataFrame([json.loads(l) for l in open(f'{D}/tau.jsonl')])
# all tau-measured rows (alive_L==0 rows are needed for sensitivity S4)
keep = set(zip(T.pkg, T.shock))
C = C[[(p, s) in keep for p, s in zip(C.pkg, C.shock)]]
OUT = f'{D}/outcome.jsonl'
done = {(json.loads(l)['pkg'], json.loads(l)['shock']) for l in open(OUT)} if os.path.exists(OUT) else set()
RQ = '''query($o:String!,$n:String!){ repository(owner:$o,name:$n){ isArchived archivedAt stargazerCount } }'''
SQ = '''query($o:String!,$n:String!,$c:String){ repository(owner:$o,name:$n){ stargazers(first:100, after:$c, orderBy:{field:STARRED_AT, direction:ASC}){
 pageInfo{hasNextPage endCursor} edges{ starredAt } } } }'''
repo_cache = {}
def repo_info(repo):
    if repo in repo_cache: return repo_cache[repo]
    o, n = owner_name(repo)
    d = gql(RQ, {'o': o, 'n': n})
    x = (d or {}).get('data', {}) or {}
    info = x.get('repository')
    if info is not None:
        c = commits_window(repo, OUT_START, datetime.now(UTC), maxpages=3, stop_at_first_human=True)
        info['human_commit_window'] = None if c is None else int(c['human_est'] > 0)
    repo_cache[repo] = info
    return info
def stars(repo, windows):
    o, n = owner_name(repo); cur = None; cnt = [0] * len(windows); last = max(w[1] for w in windows)
    for page in range(100):
        v = {'o': o, 'n': n}
        if cur: v['c'] = cur
        d = gql(SQ, v)
        try: s = d['data']['repository']['stargazers']
        except Exception: return None
        for e in s['edges']:
            t = dt(e['starredAt'])
            for i, (a, b) in enumerate(windows):
                if a <= t < b: cnt[i] += 1
            if t >= last: return cnt
        if not s['pageInfo']['hasNextPage']: return cnt
        cur = s['pageInfo']['endCursor']
    return None
def one(row):
    R = dt(row.R); L = R + FIX_WINDOW
    pj = get_json(f'https://pypi.org/pypi/{row.pkg}/json')
    ups = [dt(f['upload_time_iso_8601']) for v, fs in ((pj or {}).get('releases') or {}).items() for f in fs] if isinstance(pj, dict) else []
    info = repo_info(row.repo)
    rec = {'pkg': row.pkg, 'shock': row.shock, 'repo': row.repo, 'pypi_ok': isinstance(pj, dict)}
    rec['pypi_upload_window'] = int(any(u >= OUT_START for u in ups))
    if info is None:
        rec['repo_gone'] = 1; arch = True; arch_at = OUT_START; commit = 0
    else:
        rec['repo_gone'] = 0; arch = info['isArchived']; arch_at = dt(info['archivedAt']) if info.get('archivedAt') else OUT_START
        commit = info.get('human_commit_window') or 0
        rec.update(isArchived=arch, archivedAt=info.get('archivedAt'), stargazerCount=info['stargazerCount'], human_commit_window=info.get('human_commit_window'))
    dormant = (not rec['pypi_upload_window']) and (not commit)
    archived_dead = arch and not any(u >= arch_at for u in ups)
    rec['D'] = int(dormant or archived_dead)
    if info is not None and info['stargazerCount'] <= 10000:
        s = stars(row.repo, [(R - timedelta(days=365), R), (L, L + timedelta(days=365))])
        if s: rec['stars_pre'], rec['stars_post'] = s
    return rec
todo = [r for r in C.itertuples() if (r.pkg, r.shock) not in done]
print('todo', len(todo), flush=True)
with open(OUT, 'a') as f, ThreadPoolExecutor(6) as ex:
    for k, r in enumerate(ex.map(one, todo)):
        f.write(json.dumps(r) + '\n')
        if k % 200 == 0: print(k, len(todo), time.strftime('%H:%M:%S'), flush=True)
print('done', time.strftime('%Y-%m-%dT%H:%M:%S%z'))
