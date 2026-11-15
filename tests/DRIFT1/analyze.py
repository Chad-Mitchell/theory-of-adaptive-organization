"""DRIFT1 analysis: per-domain rate distributions + aggregate spectra, using drift_stats (prereg'd)."""
import json, collections, numpy as np, pandas as pd, sys
from datetime import datetime, timezone
from drift_stats import rate_tests, spectrum_tests
C3 = "../C3/data/"
OUT = {}
def ts(s):
    s = s.replace("Z", "+00:00")
    d = datetime.fromisoformat(s)
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.timestamp()
DAY = 86400.0

def rates_from_counts(n, window_days, minc):
    n = np.asarray(n, float); w = np.asarray(window_days, float)
    ok = (n >= minc) & (w > 0)
    return np.log10(n[ok] / w[ok]), ok

def domain(name, n, window_days, extra=None):
    res = {}
    for minc in (5, 2, 20):
        u, ok = rates_from_counts(n, window_days, minc)
        r = rate_tests(u) if len(u) >= 30 else {"n": int(len(u)), "verdict": "TOO_FEW"}
        r["items_total"] = int(len(n)); r["excluded_frac"] = float(1 - ok.mean())
        res[f"min{minc}"] = r
    if extra: res.update(extra)
    OUT[name] = res
    v = res["min5"]
    print(f"{name}: n={v.get('n')} excl={res['min5']['excluded_frac']:.2f} span={v.get('span_decades', float('nan')):.2f} "
          f"q05/50/95={v.get('q05',0):.2f}/{v.get('q50',0):.2f}/{v.get('q95',0):.2f} dip_p={v.get('dip_p',float('nan')):.3g} "
          f"gmm_k={v.get('gmm_k')} verdict={v['verdict']} | min2={res['min2']['verdict']} min20={res['min20']['verdict']}", flush=True)

def hourly_counts(times, t0, t1, dt=3600.0):
    times = np.asarray(times); times = times[(times >= t0) & (times < t1)]
    return np.bincount(((times - t0) // dt).astype(int), minlength=int((t1 - t0) // dt))

CAL = [24, 168, 8766]
SPEC = {}

# ---------- PERSON scale (withheld) ----------
# The original analysis read a private personal journal that is not in this
# repository. That arm is withheld; see REDACTION.md. Public-domain arms below
# are unchanged.
print("PERSON_scale_arm: REDACTED (private journal withheld; see REDACTION.md)")


# ---------- PROJECT: GitHub issues created in 2021 ----------
t0, t1 = ts("2021-01-01T00:00:00Z"), ts("2022-01-01T00:00:00Z")
cnt = []; alltimes = []
for l in open(C3 + "issues.jsonl"):
    j = json.loads(l)
    if j["err"] or j["repo"].split("/")[-1] in ("pandas", "sentry", "superset"):
        continue
    tt = [ts(it[2]) for it in j["items"]]
    tt = [x for x in tt if t0 <= x < t1]
    cnt.append(len(tt)); alltimes += tt
domain("PROJECT_github_issues2021", np.array(cnt), np.full(len(cnt), 365.0),
       {"note": "C3 sample: repos with >=12 commits in 2021 (selection truncates the slow end); issues+PRs opened in 2021"})
SPEC["PROJECT_github_issues2021_hourly"] = spectrum_tests(hourly_counts(alltimes, t0, t1), 1.0, [24, 168])
# commits 2021 across the full screened frame
c21 = []
for l in open(C3 + "screen.jsonl"):
    j = json.loads(l); r = j.get("res")
    try:
        c21.append(r["defaultBranchRef"]["target"]["c21"]["totalCount"])
    except Exception:
        pass
domain("PROJECT_github_commits2021", np.array(c21), np.full(len(c21), 365.0),
       {"note": "Valiev frame (PyPI/npm etc. packages' repos); commits on default branch in 2021"})

# ---------- KNOWLEDGE: Wikipedia ----------
try:
    n = []; w = []; allrev = []
    for l in open("data/wiki_revs.jsonl"):
        j = json.loads(l)
        tt = sorted(ts(x) for x in j["ts"])
        if not tt:
            continue
        pulled = ts(j["pulled"])
        n.append(len(tt)); w.append((pulled - tt[0]) / DAY)
        allrev += tt
    domain("KNOWLEDGE_wikipedia", np.array(n), np.array(w), {"note": "random en articles; rate = revisions / age (capped at 5000 most recent)"})
    a0, a1 = ts("2016-01-01T00:00:00Z"), ts("2026-01-01T00:00:00Z")
    SPEC["KNOWLEDGE_wikipedia_hourly_2016_2025"] = spectrum_tests(hourly_counts(allrev, a0, a1), 1.0, CAL)
except FileNotFoundError:
    pass

# ---------- FIRM: EDGAR ----------
try:
    n = []; w = []; alld = []
    for l in open("data/edgar_filings.jsonl"):
        j = json.loads(l)
        dd = sorted(ts(x + "T00:00:00Z") for x in j["dates"])
        if len(dd) < 1:
            continue
        pulled = ts("2026-11-14T00:00:00Z")
        n.append(len(dd)); w.append((pulled - dd[0]) / DAY)
        alld += dd
    domain("FIRM_edgar_filings", np.array(n), np.array(w), {"note": "currently-listed companies (company_tickers.json); recent block of filings"})
    a0, a1 = ts("2016-01-01T00:00:00Z"), ts("2026-01-01T00:00:00Z")
    SPEC["FIRM_edgar_daily_2016_2025"] = spectrum_tests(hourly_counts(alld, a0, a1, 86400.0), 24.0, [168, 2191.5, 8766])
except FileNotFoundError:
    pass

# ---------- CITY: NYC 311 ----------
try:
    items = json.load(open("data/nyc311_items_2025.json"))
    n = np.array([int(x["n"]) for x in items])
    domain("CITY_nyc311_type_x_board_2025", n, np.full(len(n), 365.0), {"note": "items = complaint_type x community_board, calendar 2025"})
    hrs = json.load(open("data/nyc311_hourly_2020_2025.json"))
    t = np.array([ts(x["d"]) + 3600 * int(x["hh"]) for x in hrs]); c = np.array([int(x["n"]) for x in hrs])
    a0, a1 = ts("2020-01-01T00:00:00Z"), ts("2026-01-01T00:00:00Z")
    series = np.zeros(int((a1 - a0) // 3600)); idx = ((t - a0) // 3600).astype(int); ok = (idx >= 0) & (idx < len(series))
    series[idx[ok]] = c[ok]
    SPEC["CITY_nyc311_hourly_2020_2025"] = spectrum_tests(series, 1.0, CAL)
except FileNotFoundError:
    pass

for k, v in SPEC.items():
    print(k, {kk: v.get(kk) for kk in ["verdict", "slope_single", "slope_low", "slope_high", "break_log10_f", "dBIC_broken", "n_noncal_peaks", "peak_periods_h", "fit_freq_decades"]})
json.dump({"rates": OUT, "spectra": SPEC}, open("results.json", "w"), indent=1, default=float)
