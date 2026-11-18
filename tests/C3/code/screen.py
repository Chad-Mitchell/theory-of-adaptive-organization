"""Stage 1 screen (pre-risk data only): repo existence, fork, createdAt, owner type,
default-branch commit counts in 2021 and in the gap (2022-07-01..2023-06-30)."""
import json, subprocess, sys, time, re, os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
D = '<local>/gtao/tests/C3/data'
urls = pd.read_csv(f'{D}/package_urls.csv')['url'].dropna().astype(str)
repos = sorted({u.lower().strip('/').removesuffix('.git') for u in urls if re.fullmatch(r'github\.com/[\w.-]+/[\w.-]+', u.strip('/'))})
print('unique repos', len(repos), flush=True)
OUT = f'{D}/screen.jsonl'
done = set()
if os.path.exists(OUT):
    for l in open(OUT): done.add(json.loads(l)['key'])
todo = [r for r in repos if r not in done]
FRAG = '''r%d: repository(owner:%s, name:%s){ nameWithOwner isFork createdAt owner{__typename}
 defaultBranchRef{ target{ ... on Commit { c21: history(since:"2021-01-01T00:00:00Z", until:"2022-01-01T00:00:00Z"){totalCount}
 cgap: history(since:"2022-07-01T00:00:00Z", until:"2023-07-01T00:00:00Z"){totalCount} } } } }'''
def run(batch):
    q = '{' + '\n'.join(FRAG % (i, json.dumps(r.split('/')[1]), json.dumps(r.split('/')[2])) for i, r in enumerate(batch)) + '}'
    for attempt in range(4):
        p = subprocess.run(['gh', 'api', 'graphql', '-f', f'query={q}'], capture_output=True, text=True)
        try:
            d = json.loads(p.stdout)
        except Exception:
            time.sleep(10 * (attempt + 1)); continue
        data = d.get('data') or {}
        if not data and attempt < 3:
            time.sleep(10 * (attempt + 1)); continue
        return [{'key': r, 'res': data.get(f'r{i}')} for i, r in enumerate(batch)]
    return [{'key': r, 'res': None, 'err': True} for r in batch]
B = 25
batches = [todo[i:i+B] for i in range(0, len(todo), B)]
with open(OUT, 'a') as f, ThreadPoolExecutor(8) as ex:
    for k, res in enumerate(ex.map(run, batches)):
        for row in res: f.write(json.dumps(row) + '\n')
        if k % 100 == 0: print(k, len(batches), time.strftime('%H:%M:%S'), flush=True)
print('done')
