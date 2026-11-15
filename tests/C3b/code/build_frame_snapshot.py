"""Addendum A1 frame: packages whose latest version in the last pypi-data snapshot (sethmlarson/pypi-data) published
before each shock has an unconditional dependency on the shocked lib; plus (Arm W) packages with a cp311 wheel in the
2023-09-28 snapshot. GitHub URL taken from the snapshot's package_urls (most frequent github.com/owner/repo)."""
import sqlite3, re, collections, pandas as pd
from packaging.utils import canonicalize_name
SNAP = {'sqlalchemy': '2023.01.25', 'pandas': '2023.03.19', 'urllib3': '2023.04.16', 'pydantic': '2023.06.16', 'numpy': '2024.04.24', 'W': '2023.09.28'}
GH = re.compile(r'github\.com/([\w.-]+)/([\w.-]+)', re.I)
rows = []
for k, s in SNAP.items():
    c = sqlite3.connect(f'/workspace/pypidata/{s}.db')
    if k == 'W':
        pk = {r[0] for r in c.execute("select distinct package_name from wheels where python like '%cp311%'")}
    else:
        pk = {r[0] for r in c.execute("select distinct package_name from deps where lower(dep_name)=? and extra is null", (k,))}
    urls = collections.defaultdict(collections.Counter)
    for p, u in c.execute('select package_name, url from package_urls'):
        if p in pk:
            m = GH.search(u or '')
            if m:
                o, r = m.group(1), m.group(2).removesuffix('.git')
                if o.lower() not in ('sponsors', 'orgs') and r.lower() not in ('issues',):
                    urls[p][f'github.com/{o}/{r}'.lower()] += 1
    for p in pk:
        rows.append({'pkg': p, 'frame_shock': k, 'snapshot': s, 'url': urls[p].most_common(1)[0][0] if urls[p] else None})
    print(k, s, len(pk), sum(1 for p in pk if urls[p]), flush=True)
F = pd.DataFrame(rows)
F.to_csv('/workspace/gtao/tests/C3b/data/frame_snapshot.csv', index=False)
