"""Stage 1 (PRE-SHOCK data only). For each frame package: per shock, last final release before R,
release count in [R-730d, R), its requires_dist on the shocked lib, pinned-out flag; Arm W: whether
the last release before 2023-10-02 shipped cp311 wheels (and no abi3/py3-none wheel).
The full PyPI JSON contains post-shock releases; this script discards them and writes pre-shock fields only."""
import json, os, sys, re
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from packaging.version import Version
from packaging.utils import canonicalize_name
from common import *

UPF = f'{D}/upstream_major_versions.json'
if os.path.exists(UPF):
    up = {k: [Version(v) for v in vs] for k, vs in json.load(open(UPF)).items()}
else:
    up = {}
    for lib, s in SHOCKS.items():
        pj = get_json(f'https://pypi.org/pypi/{lib}/json')
        up[lib] = [V for V, t, f, v in final_versions(pj) if V.major == s['major']]
        print(lib, 'major-2 finals:', len(up[lib]), flush=True)
    json.dump({k: [str(v) for v in vs] for k, vs in up.items()}, open(UPF, 'w'))

frame = pd.read_csv(f'{D}/package_urls.csv').rename(columns={'Unnamed: 0': 'pkg'})
frame.columns = ['pkg', 'url']
frame = frame.dropna()
frame['cn'] = frame.pkg.map(lambda x: canonicalize_name(str(x)))
frame = frame.drop_duplicates('cn')
if 'a1' in sys.argv:  # Addendum A1: snapshot frame (packages with a GitHub URL in the snapshot)
    fs = pd.read_csv(f'{D}/frame_snapshot.csv').dropna(subset=['url'])
    fs['cn'] = fs.pkg.map(lambda x: canonicalize_name(str(x)))
    frame = pd.concat([frame, fs[['pkg', 'url', 'cn']]]).drop_duplicates('cn')
frame = frame[~frame.cn.isin([canonicalize_name(x) for x in SHOCKS])]
OUT = f'{D}/screen_pypi.jsonl'
done = set()
if os.path.exists(OUT):
    for l in open(OUT): done.add(canonicalize_name(str(json.loads(l)['pkg'])))
todo = [(p, u) for p, u, c in zip(frame.pkg, frame.url, frame.cn) if c not in done]
print('todo', len(todo), flush=True)

def one(pu):
    pkg, url = pu
    pj = get_json(f'https://pypi.org/pypi/{pkg}/json')
    if pj is None: return {'pkg': pkg, 'url': url, 'status': 'gone'}
    if pj == 'ERR': return {'pkg': pkg, 'url': url, 'status': 'err'}
    fv = final_versions(pj)
    rec = {'pkg': pkg, 'url': url, 'status': 'ok', 'name': pj['info']['name'], 'shocks': {}}
    vjson_cache = {}
    for lib, s in SHOCKS.items():
        R = s['R']
        pre = [x for x in fv if x[1] < R]
        if not pre: continue
        V, t, files, vs = pre[-1]
        n730 = sum(1 for x in pre if x[1] >= R - PRE_RELEASE_WINDOW)
        e = {'last_pre_version': vs, 'last_pre_date': t.isoformat(), 'n_rel_730': n730,
             'pre_release_dates': [x[1].isoformat() for x in pre if x[1] >= R - PRE_RELEASE_WINDOW]}
        if t >= R - PRE_RELEASE_WINDOW:
            if vs not in vjson_cache:
                vj = get_json(f'https://pypi.org/pypi/{pkg}/{vs}/json')
                vjson_cache[vs] = vj
            vj = vjson_cache[vs]
            rd = vj['info'].get('requires_dist') if isinstance(vj, dict) else None
            specs = dep_specs(rd, lib)
            e['requires_known'] = specs is not None
            if specs:
                e['spec'] = ','.join(str(x) for x in specs) or '(any)'
                e['pinned_out'] = not admits_major(specs, up[lib])
            else:
                e['depends'] = False if specs is not None else None
            if specs: e['depends'] = True
            # sdist / wheel filenames of the pre-shock release (for exposure stage)
            e['files'] = files
        rec['shocks'][lib] = e
    pre = [x for x in fv if x[1] < PY312_R]
    if pre:
        V, t, files, vs = pre[-1]
        tags = ' '.join(files)
        rec['w'] = {'last_pre_version': vs, 'last_pre_date': t.isoformat(),
                    'n_rel_730': sum(1 for x in pre if x[1] >= PY312_R - PRE_RELEASE_WINDOW),
                    'pre_release_dates': [x[1].isoformat() for x in pre if x[1] >= PY312_R - PRE_RELEASE_WINDOW],
                    'cp311': bool(re.search(r'-cp311-', tags)), 'abi3': 'abi3' in tags,
                    'pure': bool(re.search(r'-(py3|py2\.py3)-none-any', tags)),
                    'cp312_pre': bool(re.search(r'-cp312-', tags))}
    return rec

with open(OUT, 'a') as f, ThreadPoolExecutor(24) as ex:
    for k, r in enumerate(ex.map(one, todo)):
        f.write(json.dumps(r) + '\n')
        if k % 2000 == 0: print(k, len(todo), time.strftime('%H:%M:%S'), flush=True)
print('done', time.strftime('%Y-%m-%dT%H:%M:%S%z'))
