#!/usr/bin/env python3
"""Check every included DOI in data/coded.csv on Crossref (title match). Writes data/crossref_check.json.
Written after the lock (not part of the locked set); it only reads DOIs and titles."""
import csv, difflib, json, re, time, urllib.parse, urllib.request
from pathlib import Path
HERE = Path(__file__).resolve().parent
POOL = json.load(open('/workspace/gtao-dir-data/DIR1/pool.json'))
T = {(p['cell'], p['rank']): p['title'] for p in POOL}

def norm(s): return re.sub(r'[^a-z0-9 ]', '', re.sub(r'<[^>]+>', '', (s or '').lower()))

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'GTAO-DIR1 (mailto:chad39@gmail.com)'})
    with urllib.request.urlopen(req, timeout=40) as r: return json.loads(r.read())

out = []
for r in csv.DictReader(open(HERE / 'data' / 'coded.csv')):
    if r['included'] != '1': continue
    t = T[(r['cell'], int(r['rank']))]
    rec = {'cell': r['cell'], 'rank': int(r['rank']), 'doi': r['doi'], 'openalex_title': t}
    try:
        if r['doi']:
            m = get('https://api.crossref.org/works/' + urllib.parse.quote(r['doi']))['message']
        else:
            items = get('https://api.crossref.org/works?rows=1&query.bibliographic=' + urllib.parse.quote(t))['message']['items']
            m = items[0] if items else {}
            rec['doi_found_by_search'] = m.get('DOI')
        ct = (m.get('title') or [''])[0]
        rec.update(crossref_title=ct, issued=m.get('issued', {}).get('date-parts', [[None]])[0],
                   container=(m.get('container-title') or [''])[0],
                   similarity=round(difflib.SequenceMatcher(None, norm(t), norm(ct)).ratio(), 3))
    except Exception as e:  # noqa: BLE001
        rec['error'] = repr(e)
    rec['match'] = rec.get('similarity', 0) >= 0.85
    out.append(rec); time.sleep(0.3)
(HERE / 'data' / 'crossref_check.json').write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(sum(o['match'] for o in out), 'of', len(out), 'match')
for o in out:
    if not o['match']: print(o)
