"""C3b shared constants and helpers. Written before any data pull."""
import re, json, time, urllib.request, urllib.error
from datetime import datetime, timezone, timedelta
from packaging.requirements import Requirement
from packaging.version import Version, InvalidVersion
from packaging.utils import canonicalize_name

D = '/workspace/gtao/tests/C3b/data'
UTC = timezone.utc
def dt(s): return datetime.fromisoformat(s.replace('Z', '+00:00')).astimezone(UTC)

# Shock = first final release of the new major (PyPI upload time, verified 2026-11-14).
SHOCKS = {
    'sqlalchemy': dict(R=dt('2023-01-26T22:58:05Z'), major=2, module='sqlalchemy'),
    'pandas':     dict(R=dt('2023-04-03T14:10:47Z'), major=2, module='pandas'),
    'urllib3':    dict(R=dt('2023-04-26T17:21:22Z'), major=2, module='urllib3'),
    'pydantic':   dict(R=dt('2023-06-30T16:27:55Z'), major=2, module='pydantic'),
    'numpy':      dict(R=dt('2024-06-16T13:06:46Z'), major=2, module='numpy'),
}
# Arm W (secondary): CPython 3.12.0 final, 2023-10-02 (python.org).
PY312_R = dt('2023-10-02T00:00:00Z')

FIX_WINDOW = timedelta(days=365)      # tau observed in [R, R+365d]; unfixed -> tau=365, flagged
ALIVE_LOOKBACK = timedelta(days=180)  # alive at landmark L=R+365d: activity in (L-180d, L]
PRE_RELEASE_WINDOW = timedelta(days=730)
PRE_COMMIT_WINDOW = timedelta(days=365)
OUT_START = dt('2026-11-14T00:00:00Z') - timedelta(days=365)  # outcome window start 2025-11-14
OUT_END = dt('2026-11-14T00:00:00Z')  # nominal end; activity up to pull time counts

ENV = {'python_version': '3.11', 'python_full_version': '3.11.6', 'sys_platform': 'linux',
       'platform_system': 'Linux', 'os_name': 'posix', 'implementation_name': 'cpython',
       'platform_python_implementation': 'CPython', 'platform_machine': 'x86_64', 'extra': ''}

BOT_LOGINS = {'dependabot', 'dependabot-preview', 'renovate', 'pre-commit-ci', 'pyup-bot', 'greenkeeper',
              'codecov', 'allcontributors', 'github-actions', 'stale', 'mergify', 'imgbot', 'snyk-bot',
              'web-flow', 'renovate-bot', 'pyup.io bot', 'deepsource-autofix', 'sourcery-ai', 'restyled-io',
              'transifex-integration', 'weblate', 'actions-user', 'semantic-release-bot', 'github-actions[bot]'}

def is_bot(login=None, name=None, email=None):
    for s in (login, name, email):
        if not s: continue
        s = s.lower()
        if '[bot]' in s or s in BOT_LOGINS: return True
        if s.endswith('-bot') or s.endswith('bot@users.noreply.github.com'): return True
    if email and email.lower().startswith(('dependabot', 'renovate', 'pre-commit-ci', 'action@github.com', '41898282+github-actions')):
        return True
    return False

def get_json(url, tries=5):
    for a in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'c3b-research (read-only)'}), timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            time.sleep(2 * (a + 1))
        except Exception:
            time.sleep(2 * (a + 1))
    return 'ERR'

def final_versions(pj):
    """(Version, first upload datetime, filenames) for non-yanked, non-prerelease releases with files."""
    out = []
    for v, files in (pj.get('releases') or {}).items():
        files = [f for f in files if not f.get('yanked')]
        if not files: continue
        try: V = Version(v)
        except InvalidVersion: continue
        if V.is_prerelease or V.is_devrelease: continue
        out.append((V, min(dt(f['upload_time_iso_8601']) for f in files), [f['filename'] for f in files], v))
    return sorted(out, key=lambda x: x[1])

def dep_specs(requires_dist, lib):
    """Unconditional (non-extra) requirements on lib whose markers hold under ENV.
    Returns None if requires_dist is None (unknown metadata), [] if lib not required."""
    if requires_dist is None: return None
    out = []
    for s in requires_dist:
        try: r = Requirement(s)
        except Exception: continue
        if canonicalize_name(r.name) != canonicalize_name(lib): continue
        if r.marker is not None:
            if 'extra' in str(r.marker): continue
            try:
                if not r.marker.evaluate(ENV): continue
            except Exception: continue
        out.append(r.specifier)
    return out

def admits_major(specs, upstream_major_versions):
    """True if every applicable specifier admits at least one released final version of the new major
    (intersection semantics: a version must satisfy all applicable lines)."""
    return any(all(sp.contains(v, prereleases=False) for sp in specs) for v in upstream_major_versions)

# ---------------- GitHub helpers (read-only, gh CLI) ----------------
import subprocess
def gql(q, variables=None, tries=6):
    args = ['gh', 'api', 'graphql', '-f', f'query={q}']
    for k, v in (variables or {}).items(): args += ['-F' if isinstance(v, int) else '-f', f'{k}={v}']
    for a in range(tries):
        p = subprocess.run(args, capture_output=True, text=True)
        try: d = json.loads(p.stdout)
        except Exception: d = None
        if d and d.get('data') is not None: return d
        msg = (p.stdout + p.stderr).lower()
        if d and 'errors' in d and any(e.get('type') == 'NOT_FOUND' for e in d['errors']): return d
        time.sleep(60 if 'rate limit' in msg else 5 * (a + 1))
    return None

def owner_name(repo): o, n = repo.split('/'); return o, n

HIST_Q = '''query($o:String!,$n:String!,$s:GitTimestamp!,$u:GitTimestamp!,$c:String){ repository(owner:$o,name:$n){
 defaultBranchRef{ target{ ... on Commit{ history(since:$s, until:$u, first:100, after:$c){ totalCount
 pageInfo{hasNextPage endCursor} nodes{ committedDate author{ name email user{login} } } } } } } } }'''

def commits_window(repo, since, until, maxpages=10, stop_at_first_human=False):
    """Human (non-bot) commits on the default branch in [since, until).
    Returns dict(total, human_est, authors, capped) or None if repo/branch unreadable."""
    o, n = owner_name(repo); cur = None; seen = human = 0; authors = set(); total = 0
    for page in range(maxpages):
        v = {'o': o, 'n': n, 's': since.strftime('%Y-%m-%dT%H:%M:%SZ'), 'u': until.strftime('%Y-%m-%dT%H:%M:%SZ')}
        if cur: v['c'] = cur
        d = gql(HIST_Q, v)
        try: h = d['data']['repository']['defaultBranchRef']['target']['history']
        except Exception: return None
        total = h['totalCount']
        for nd in h['nodes']:
            a = nd['author'] or {}; u = (a.get('user') or {}).get('login')
            seen += 1
            if not is_bot(u, a.get('name'), a.get('email')):
                human += 1; authors.add((u or a.get('email') or a.get('name') or '?').lower())
                if stop_at_first_human: return {'total': total, 'human_est': human, 'authors': len(authors), 'capped': False}
        if not h['pageInfo']['hasNextPage']: return {'total': total, 'human_est': human, 'authors': len(authors), 'capped': False}
        cur = h['pageInfo']['endCursor']
    est = round(total * human / seen) if seen else 0
    return {'total': total, 'human_est': est, 'authors': len(authors), 'capped': True}
