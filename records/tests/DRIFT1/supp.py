"""DRIFT1 supplementary analysis (POST HOC, labelled in RESULTS):
(1) dequantize integer counts over a common window (n -> n + U(-0.5,0.5)): counts/365 sit on a discrete grid in
    log-rate, which the dip test and GMM read as multimodality (artifact found after the prereg'd run);
(2) text histograms of log10 rate per domain; q01-q99 spans; (3) Wikipedia rate over the last 5 years only."""
import json, collections, numpy as np
from datetime import datetime, timezone
from drift_stats import rate_tests
DAY = 86400.0
def ts(s):
    d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    return (d if d.tzinfo else d.replace(tzinfo=timezone.utc)).timestamp()
rng = np.random.default_rng(7)
out = {}
def hist(u, lab):
    h, e = np.histogram(u, bins=np.arange(np.floor(u.min() * 5) / 5, u.max() + 0.2, 0.2))
    s = [f"  {a:5.1f} {'#' * int(60 * c / h.max())} {c}" for c, a in zip(h, e)]
    return f"{lab}\n" + "\n".join(s)
lines = []
def report(name, u, deq_note):
    t = rate_tests(u)
    q01, q99 = np.quantile(u, [0.01, 0.99])
    out[name] = dict(t, q01=float(q01), q99=float(q99), note=deq_note)
    lines.append(f"{name}: n={t['n']} verdict={t['verdict']} span(q05-q95)={t['span_decades']:.2f} span(q01-q99)={q99-q01:.2f} "
                 f"dip_p={t['dip_p']:.3g} gmm_k={t['gmm_k']} quad-vs-lin dBIC={t['dBIC_quad_vs_lin']:.1f} vertex={t['vertex']:.2f} "
                 f"peak/edge={t['peak_to_edge'][0]:.2f},{t['peak_to_edge'][1]:.2f} central slope={t['central_loglog_slope']:.2f} [{deq_note}]")
    lines.append(hist(u, "  histogram of log10(rate per day), 0.2-decade bins:"))
def deq(n, w):
    return np.log10((n + rng.uniform(-0.5, 0.5, len(n))) / w)
C3 = "../C3/data/"
t0, t1 = ts("2021-01-01T00:00:00Z"), ts("2022-01-01T00:00:00Z")
cnt = []
for l in open(C3 + "issues.jsonl"):
    j = json.loads(l)
    if j["err"] or j["repo"].split("/")[-1] in ("pandas", "sentry", "superset"):
        continue
    cnt.append(sum(t0 <= ts(it[2]) < t1 for it in j["items"]))
cnt = np.array(cnt); c = cnt[cnt >= 5]
report("PROJECT_github_issues2021", deq(c, 365.0), "dequantized")
c21 = []
for l in open(C3 + "screen.jsonl"):
    r = json.loads(l).get("res")
    try: c21.append(r["defaultBranchRef"]["target"]["c21"]["totalCount"])
    except Exception: pass
c21 = np.array(c21); c = c21[c21 >= 5]
report("PROJECT_github_commits2021", deq(c, 365.0), "dequantized")
items = json.load(open("data/nyc311_items_2025.json"))
n = np.array([int(x["n"]) for x in items]); n = n[n >= 5]
report("CITY_nyc311_type_x_board_2025", deq(n, 365.0), "dequantized")
n2 = collections.Counter()
for x in items: n2[x["complaint_type"]] += int(x["n"])
v = np.array(list(n2.values())); v = v[v >= 5]
report("CITY_nyc311_type_only_2025", deq(v, 365.0), "dequantized; item = complaint type (citywide)")
# Wikipedia: full age and last-5-years
n = []; w = []; n5 = []
P = ts("2026-11-14T00:00:00Z"); F5 = P - 5 * 365.25 * DAY
for l in open("data/wiki_revs.jsonl"):
    j = json.loads(l); tt = sorted(ts(x) for x in j["ts"])
    if len(tt) >= 5:
        n.append(len(tt)); w.append((ts(j["pulled"]) - tt[0]) / DAY)
    k = sum(x >= F5 for x in tt)
    if tt and tt[0] < F5 and k >= 5:
        n5.append(k)
report("KNOWLEDGE_wikipedia_age", np.log10(np.array(n) / np.array(w)), "variable window, no dequantization needed")
report("KNOWLEDGE_wikipedia_last5y", deq(np.array(n5, float), 5 * 365.25), "articles older than 5y, revisions in last 5y, dequantized")
n = []; w = []
for l in open("data/edgar_filings.jsonl"):
    j = json.loads(l); dd = sorted(ts(x + "T00:00:00Z") for x in j["dates"])
    if len(dd) >= 5:
        n.append(len(dd)); w.append((ts("2026-11-14T00:00:00Z") - dd[0]) / DAY)
report("FIRM_edgar_filings", np.log10(np.array(n) / np.array(w)), "variable window")
# Person-scale arm withheld (private journal). See REDACTION.md.
print("PERSON_scale_arm: REDACTED (private journal withheld; see REDACTION.md)")
open("supp_output.txt", "w").write("\n".join(lines) + "\n")
json.dump(out, open("supp_results.json", "w"), indent=1, default=float)
print("\n".join(lines))
