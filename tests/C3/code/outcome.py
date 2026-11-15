"""Stage 3 (outcome): archivedAt and last default-branch commit date for analysis-eligible repos."""
import json, subprocess, time
import pandas as pd
D = '/workspace/gtao/tests/C3/data'
repos = [l.strip() for l in open(f'{D}/eligible_repos.txt') if l.strip()]
FRAG = 'r%d: repository(owner:%s, name:%s){ nameWithOwner isArchived archivedAt pushedAt defaultBranchRef{ target{ ... on Commit { history(first:1){ nodes{ committedDate } } } } } }'
out = open(f'{D}/outcome.jsonl', 'w')
for s in range(0, len(repos), 40):
    b = repos[s:s+40]
    q = '{' + '\n'.join(FRAG % (i, json.dumps(r.split('/')[0]), json.dumps(r.split('/')[1])) for i, r in enumerate(b)) + '}'
    for a in range(4):
        p = subprocess.run(['gh', 'api', 'graphql', '-f', f'query={q}'], capture_output=True, text=True)
        try: data = json.loads(p.stdout).get('data') or {}
        except Exception: data = {}
        if data: break
        time.sleep(10)
    for i, r in enumerate(b): out.write(json.dumps({'key': r, 'res': data.get(f'r{i}')}) + '\n')
out.close(); print('done', time.strftime('%Y-%m-%dT%H:%M:%S%z'))
