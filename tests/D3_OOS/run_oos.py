"""D3-TWO-EXPONENT-OOS runner (locked with PREREG.md). Usage: run_oos.py GITDIR WIKIFILE
Git pipeline = D3S (reviews/night2/SPECTRUM_MAP/checks/d3s_shuffle.py): no merges, commits touching <= 100 files,
files with >= 50 edit days, alive/dead split for a_need. Repo k (0-based in repos.txt order, reserves after) uses seed 20261115+k.
Wikipedia: one 'repo' per category; edits by users whose name ends in 'bot' (case-insensitive) dropped; day = UTC date."""
import sys, os, json, subprocess, collections, datetime, numpy as np
from scipy.stats import spearmanr, wilcoxon
from d3lib import repo_stats, need_exponent
GITDIR, WIKI = sys.argv[1], sys.argv[2]; HERE = os.path.dirname(os.path.abspath(__file__))
repos = [l.strip() for l in open(os.path.join(HERE, "repos.txt")) if l.strip()]
reserve = [l.strip() for l in open(os.path.join(HERE, "reserve.txt")) if l.strip()]
def git_repo(path, seed):
    txt = subprocess.run(["git", "-C", path, "log", "--no-merges", "--format=@%ct", "--name-status", "--no-renames", "HEAD"], capture_output=True, text=True, errors="replace").stdout
    commits = []; cur = None
    for line in txt.splitlines():
        if line.startswith("@"): cur = [int(line[1:])//86400, []]; commits.append(cur)
        elif line.strip() and cur is not None:
            st, _, f = line.partition("\t"); cur[1].append((st, f))
    ed = collections.defaultdict(set); dele = {}
    for day, fs in commits:
        if len(fs) > 100: continue
        for st, f in fs:
            ed[f].add(day)
            if st.startswith("D"): dele[f] = max(dele.get(f, 0), day)
    if not ed: return None
    end = max(max(s) for s in ed.values()); start = min(min(s) for s in ed.values()); n = end - start + 1
    alive = [sorted(s) for f, s in ed.items() if not (f in dele and dele[f] >= max(s))]
    dead = [sorted(s) for f, s in ed.items() if (f in dele and dele[f] >= max(s))]
    a = need_exponent(alive, dead, end)
    big = [np.array(sorted(s)) - start for s in ed.values() if len(s) >= 50]
    return repo_stats(big, n, np.random.default_rng(seed), a_need=a)
def summarize(rows, label):
    D = [r for r in rows if r]
    dl = [r["delta"] for r in D]; ex = float(np.mean([r["M_w_exceed"] for r in D])); md = float(np.median(dl))
    p4 = float(wilcoxon(dl, alternative="greater").pvalue) if len(D) >= 6 else None
    s = dict(arm=label, n=len(D),
             P1_spearman_orig_shuf=round(float(spearmanr([r["beta_orig"] for r in D], [r["beta_shuf"] for r in D])[0]), 3),
             median_delta=round(md, 4),
             P3_exceed_frac=round(ex, 3), P4_wilcoxon_p=None if p4 is None else float(f"{p4:.3g}"),
             median_M_w=round(float(np.median([r["M_w"] for r in D])), 3), median_M_raw=round(float(np.median([r["M_raw"] for r in D])), 3),
             median_beta_orig=round(float(np.median([r["beta_orig"] for r in D])), 3))
    if all(r["a_need"] is not None for r in D):
        s["D3_spearman_beta_orig_vs_a"] = round(float(spearmanr([r["beta_orig"] for r in D], [r["a_need"] for r in D])[0]), 3)
        s["S2_spearman_beta_shuf_vs_a"] = round(float(spearmanr([r["beta_shuf"] for r in D], [r["a_need"] for r in D])[0]), 3)
    s["P1"] = "PASS (non-discriminating)" if s["P1_spearman_orig_shuf"] > 0.3 else "FAIL"
    s["P2"] = "PASS (non-discriminating)" if -0.03 <= md <= 0.05 else ("ABOVE BAND" if md > 0.05 else "BELOW BAND")
    s["P3"] = "RENEWAL REJECTED" if ex >= 0.5 else ("RENEWAL RETAINED" if ex <= 0.15 else "PARTIAL")
    s["P4"] = None if p4 is None else ("DELTA>0 DETECTED" if (p4 < 0.01 and md > 0.01) else "not detected")
    return s
out = {"git": [], "wiki": []}
valid = 0
for k, r in enumerate(repos + reserve):
    if k >= len(repos) and valid >= 20: break
    path = os.path.join(GITDIR, r.replace("/", "_"))
    row = git_repo(path, 20261115 + k) if os.path.isdir(path) else None
    out["git"].append({"repo": r, "k": k, **(row or {"excluded": "clone failed or < 5 files with >= 50 edit days"})})
    if row: valid += 1
    print(json.dumps(out["git"][-1]), flush=True)
groups = collections.defaultdict(list); cutoff = None
for l in open(WIKI):
    p = json.loads(l)
    days = sorted({datetime.date.fromisoformat(t[:10]).toordinal() for t, u in p["revs"] if not u.lower().endswith("bot")})
    groups[p["category"]].append(days)
for gi, (cat, lists) in enumerate(groups.items()):
    lists = [d for d in lists if len(d) >= 50]
    if len(lists) < 5:
        out["wiki"].append({"category": cat, "excluded": "< 5 pages with >= 50 edit days"}); print(json.dumps(out["wiki"][-1])); continue
    start = min(d[0] for d in lists); end = max(d[-1] for d in lists)
    row = repo_stats([np.array(d) - start for d in lists], end - start + 1, np.random.default_rng(20261115 + 1000 + gi))
    out["wiki"].append({"category": cat, **row}); print(json.dumps(out["wiki"][-1]), flush=True)
out["summary_git"] = summarize([r if "excluded" not in r else None for r in out["git"]], "github")
out["summary_wiki"] = summarize([r if "excluded" not in r else None for r in out["wiki"]], "wikipedia")
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(out["summary_git"], indent=1)); print(json.dumps(out["summary_wiki"], indent=1))
