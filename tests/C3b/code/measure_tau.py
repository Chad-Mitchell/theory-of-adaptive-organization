"""Stage 4 (POST-SHOCK, fix window only: [R, L], L = R + 365d). Writes only window fields:
tau (days to first final release that admits the new major or drops the dependency; Arm W: first cp312
file upload), unfixed flag, latency to first final release of any kind, alive at L (final release or
human commit in (L-180d, L]). Data after L are fetched by the PyPI API but not stored."""
import json, os, re
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from common import *

up = {k: [Version(v) for v in vs] for k, vs in json.load(open(f'{D}/upstream_major_versions.json')).items()}
C = pd.read_csv(f'{D}/candidates_resolved.csv')
OUT = f'{D}/tau.jsonl'
done = {(json.loads(l)['pkg'], json.loads(l)['shock']) for l in open(OUT)} if os.path.exists(OUT) else set()
def days(a, b): return (a - b).total_seconds() / 86400
def one(row):
    pkg, shock, repo = row.pkg, row.shock, row.repo
    R = dt(row.R); L = R + FIX_WINDOW
    pj = get_json(f'https://pypi.org/pypi/{pkg}/json')
    if not isinstance(pj, dict): return {'pkg': pkg, 'shock': shock, 'err': 'pypi'}
    fv = final_versions(pj)
    win = [x for x in fv if R <= x[1] <= L]
    rec = {'pkg': pkg, 'shock': shock, 'repo': repo, 'arm': row.arm}
    rec['latency_days'] = max(1.0, days(win[0][1], R)) if win else 365.0
    rec['n_rel_window'] = len(win)
    tau = None
    if row.arm in ('P', 'Q'):
        unknown = 0
        for V, t, files, vs in win:
            vj = get_json(f'https://pypi.org/pypi/{pkg}/{vs}/json')
            rd = vj['info'].get('requires_dist') if isinstance(vj, dict) else None
            specs = dep_specs(rd, shock)
            if specs is None: unknown += 1; continue
            if specs == [] or admits_major(specs, up[shock]):
                tau = max(1.0, days(t, R)); rec['fix_version'] = vs; rec['fix_kind'] = 'dropped' if specs == [] else 'admits'; break
        rec['n_unknown_meta'] = unknown
    else:  # Arm W: first cp312 file upload, any final version, upload time <= L
        ups = [dt(f['upload_time_iso_8601']) for v, files in (pj.get('releases') or {}).items() for f in files
               if re.search(r'-cp312-', f['filename']) and not f.get('yanked')]
        ups = [u for u in ups if u <= L]
        if ups: tau = max(1.0, days(min(ups), R)); rec['fix_kind'] = 'cp312'
    rec['tau_days'] = tau if tau is not None else 365.0
    rec['unfixed'] = int(tau is None)
    rel_alive = any(L - ALIVE_LOOKBACK < x[1] <= L for x in fv)
    rec['alive_rel'] = int(rel_alive)
    if rel_alive: rec['alive_L'] = 1
    else:
        c = commits_window(repo, L - ALIVE_LOOKBACK, L, maxpages=3, stop_at_first_human=True)
        rec['alive_commit'] = None if c is None else int(c['human_est'] > 0)
        rec['alive_L'] = int(bool(c and c['human_est'] > 0))
    return rec
todo = [r for r in C.itertuples() if (r.pkg, r.shock) not in done]
print('todo', len(todo), flush=True)
with open(OUT, 'a') as f, ThreadPoolExecutor(8) as ex:
    for k, r in enumerate(ex.map(one, todo)):
        f.write(json.dumps(r) + '\n')
        if k % 200 == 0: print(k, len(todo), time.strftime('%H:%M:%S'), flush=True)
print('done', time.strftime('%Y-%m-%dT%H:%M:%S%z'))
