"""Stage 3 (PRE-SHOCK): exposure E = share of shipped, non-test .py files in the last pre-shock release
that import the shocked module. E = (k + 0.5) / (n + 1). Prefers the sdist, else the first wheel."""
import json, os, io, tarfile, zipfile, re
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from common import *

C = pd.read_csv(f'{D}/candidates_resolved.csv')
C = C[C.arm.isin(['P', 'Q'])]
jobs = sorted(set(zip(C.pkg, C.last_pre_version.astype(str), C.shock)))
OUT = f'{D}/exposure.jsonl'
done = {(json.loads(l)['pkg'], json.loads(l)['ver'], json.loads(l)['shock']) for l in open(OUT)} if os.path.exists(OUT) else set()
EXCL = re.compile(r'(^|/)(tests?|testing|docs?|examples?|benchmarks?|\.github)(/|$)|(^|/)(test_[^/]*|[^/]*_test\.py|conftest\.py|setup\.py)$', re.I)
def members(blob, fname):
    if fname.endswith(('.tar.gz', '.tgz', '.tar.bz2')):
        with tarfile.open(fileobj=io.BytesIO(blob)) as t:
            for m in t.getmembers():
                if m.isfile() and m.name.endswith('.py'):
                    yield m.name, t.extractfile(m).read()
    elif fname.endswith(('.zip', '.whl')):
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            for n in z.namelist():
                if n.endswith('.py'): yield n, z.read(n)
def one(job):
    pkg, ver, shock = job; mod = SHOCKS[shock]['module']
    pat = re.compile(rf'^\s*(?:import\s+(?:[\w.]+\s*(?:as\s+\w+\s*)?,\s*)*{mod}\b|from\s+{mod}\b)', re.M)
    vj = get_json(f'https://pypi.org/pypi/{pkg}/{ver}/json')
    if not isinstance(vj, dict): return {'pkg': pkg, 'ver': ver, 'shock': shock, 'err': 'nojson'}
    urls = [u for u in vj.get('urls', []) if not u.get('yanked')]
    sd = [u for u in urls if u['packagetype'] == 'sdist'] or [u for u in urls if u['packagetype'] == 'bdist_wheel']
    if not sd: return {'pkg': pkg, 'ver': ver, 'shock': shock, 'err': 'nofile'}
    u = sd[0]
    if u.get('size', 0) > 80_000_000: return {'pkg': pkg, 'ver': ver, 'shock': shock, 'err': 'toobig'}
    try:
        with urllib.request.urlopen(u['url'], timeout=120) as r: blob = r.read()
        n = k = lines = 0
        for name, data in members(blob, u['filename']):
            rel = name.split('/', 1)[1] if (u['packagetype'] == 'sdist' and '/' in name) else name
            if EXCL.search(rel): continue
            txt = data.decode('utf-8', 'ignore'); n += 1
            h = len(pat.findall(txt)); k += h > 0; lines += h
        return {'pkg': pkg, 'ver': ver, 'shock': shock, 'file': u['filename'], 'n_py': n, 'k_import': k, 'import_lines': lines}
    except Exception as e:
        return {'pkg': pkg, 'ver': ver, 'shock': shock, 'err': str(e)[:100]}
todo = [j for j in jobs if j not in done]
print('todo', len(todo), flush=True)
with open(OUT, 'a') as f, ThreadPoolExecutor(12) as ex:
    for k, r in enumerate(ex.map(one, todo)):
        f.write(json.dumps(r) + '\n')
        if k % 200 == 0: print(k, len(todo), time.strftime('%H:%M:%S'), flush=True)
print('done', time.strftime('%Y-%m-%dT%H:%M:%S%z'))
