"""Stage 2: pull issues+PRs (REST) for the sampled repos. Keeps items created <= 2021-12-31
that were updated since 2021-01-01 (covers all items opened in 2021 and all closed in 2021)."""
import json, subprocess, sys, time, os
from concurrent.futures import ThreadPoolExecutor, as_completed
D = '/workspace/gtao/tests/C3/data'
sample = [l.strip() for l in open(f'{D}/sample_repos.txt') if l.strip()]
OUT = f'{D}/issues.jsonl'
done = set()
if os.path.exists(OUT):
    for l in open(OUT): done.add(json.loads(l)['repo'])
todo = [r for r in sample if r not in done]
END = '2021-12-31T23:59:59Z'
def get(path):
    for attempt in range(8):
        p = subprocess.run(['gh', 'api', '-H', 'Accept: application/vnd.github+json', path], capture_output=True, text=True)
        if p.returncode == 0:
            return json.loads(p.stdout), None
        err = (p.stderr or '') + (p.stdout or '')
        if 'rate limit' in err.lower():
            try:
                rs = json.loads(subprocess.run(['gh','api','rate_limit'],capture_output=True,text=True).stdout)['resources']['core']['reset']
                time.sleep(max(30, rs - time.time() + 15))
            except Exception:
                time.sleep(300)
            continue
        if any(s in err for s in ('404', '410', 'Not Found', 'disabled')):
            return None, err.strip()[:200]
        time.sleep(20 * (attempt + 1))
    return None, 'retry-exhausted'
def pull(repo):
    items, page, err = [], 1, None
    while True:
        d, err = get(f'repos/{repo}/issues?state=all&since=2021-01-01T00:00:00Z&sort=created&direction=asc&per_page=100&page={page}')
        if d is None: break
        for it in d:
            if it['created_at'] > END: break
            u = it.get('user') or {}
            items.append([it['number'], 'pull_request' in it, it['created_at'], it.get('closed_at'),
                          u.get('login'), u.get('type'), it.get('author_association'),
                          [l['name'] for l in it.get('labels', [])], it.get('state_reason')])
        if len(d) < 100 or d[-1]['created_at'] > END: break
        page += 1
        if page > 300: err = 'page-cap'; break
    return {'repo': repo, 'err': err, 'pages': page, 'items': items}
with open(OUT, 'a') as f, ThreadPoolExecutor(6) as ex:
    for k, fut in enumerate(as_completed([ex.submit(pull, r) for r in todo])):
        res = fut.result()
        f.write(json.dumps(res) + '\n'); f.flush()
        if k % 50 == 0: print(k, len(todo), time.strftime('%H:%M:%S'), flush=True)
print('done')
