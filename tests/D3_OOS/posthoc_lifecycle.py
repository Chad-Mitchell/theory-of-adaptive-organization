"""POST HOC (written after run_oos.out was seen; exploratory, not a locked test). Does M_w > 0 survive removing each file's
first 365 days of life (early-life burst) and its last 365 days before the repo's last commit? Same files, same null (200 shuffles)."""
import sys, os, json, collections, subprocess, numpy as np
from d3lib import mw, shuffle_gaps
G = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__))
repos = [l.strip() for l in open(os.path.join(HERE, "repos.txt")) if l.strip()]; out = []
for k, r in enumerate(repos):
    txt = subprocess.run(["git", "-C", os.path.join(G, r.replace("/", "_")), "log", "--no-merges", "--format=@%ct", "--name-only", "HEAD"], capture_output=True, text=True, errors="replace").stdout
    ed = collections.defaultdict(set); cur = None; fs = []
    def flush():
        if cur is not None and len(fs) <= 100:
            for f in fs: ed[f].add(cur)
    for line in txt.splitlines():
        if line.startswith("@"): flush(); cur = int(line[1:])//86400; fs = []
        elif line.strip(): fs.append(line)
    flush()
    end = max(max(s) for s in ed.values())
    files = []
    for s in ed.values():
        if len(s) < 50: continue
        d = np.array(sorted(s)); d = d[(d >= d[0] + 365) & (d <= end - 365)]
        if len(d) >= 20: files.append(d)
    if len(files) < 5: out.append(dict(repo=r, excluded=True)); continue
    rng = np.random.default_rng(20261115 + k); m = mw(files); null = np.array([mw([shuffle_gaps(d, rng) for d in files]) for _ in range(200)])
    out.append(dict(repo=r, n_files=len(files), M_w_trim=round(m, 4), null_q975=round(float(np.quantile(null, 0.975)), 4), exceed=bool(m > np.quantile(null, 0.975))))
    print(json.dumps(out[-1]), flush=True)
v = [o for o in out if not o.get("excluded")]
print(json.dumps(dict(n=len(v), exceed_frac=round(float(np.mean([o["exceed"] for o in v])), 3), median_M_w_trim=round(float(np.median([o["M_w_trim"] for o in v])), 3))))
