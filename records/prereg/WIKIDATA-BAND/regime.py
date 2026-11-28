"""Regime-first gate (THEORY.md v1.2 §2.5): per property, (i) split-half stationarity of change rates and (ii) the error-growth
exponent 2H, both from the dated history recorded in current Wikidata statements (qualifiers P580 start time, P585 point in
time, P577 publication date). Loss of a held last value after lag tau: quantity -> squared log change; other -> indicator of
any change. E[loss(tau)] ~ tau^(2H); regime A (single pace, sqrt case) iff H ~ 1/2. Predicted reset-read elasticity a = b = 1/(1+2H)."""
import math, re
import numpy as np
LAGS_Q = [1, 2, 4, 8]; LAGS_C = [0.5, 1, 2, 4, 8]

def tyear(tv):
    m = re.match(r"([+-])(\d+)-(\d\d)-(\d\d)", tv.get("time", ""))
    if not m or tv.get("precision", 0) < 9: return None
    y = int(m.group(2)); mo = int(m.group(3)) or 7; d = int(m.group(4)) or 1
    if tv.get("precision") == 9: mo, d = 7, 1
    return y + (mo - 1) / 12 + (d - 1) / 365.25

def history(item):
    ev = []; series = []
    for c in item["claims_now"]:
        if c.get("rank") == "deprecated": continue
        for q in ("P580", "P585", "P577"):
            for s in c.get("qualifiers", {}).get(q, []):
                tv = s.get("datavalue", {}).get("value")
                if isinstance(tv, dict):
                    t = tyear(tv)
                    if t is not None and 1990 <= t:
                        ev.append(t)
                        dv = c.get("mainsnak", {}).get("datavalue", {})
                        if q == "P585" and dv.get("type") == "quantity":
                            a = float(dv["value"]["amount"])
                            if a > 0: series.append((t, a))
    return sorted(set(round(e, 4) for e in ev)), sorted(set(series))

def _h_quantity(hists):
    D = {}
    for tau in LAGS_Q:
        per_item = []
        for _, s in hists:
            v = [(math.log(b[1]) - math.log(a[1])) ** 2 for i, a in enumerate(s) for b in s[i + 1:] if tau / math.sqrt(2) <= b[0] - a[0] < tau * math.sqrt(2)]
            if v: per_item.append(np.mean(v))
        D[tau] = per_item
    return D

def _h_events(hists, t1):
    P = {}
    for tau in LAGS_C:
        per_item = []
        for ev, _ in hists:
            if not ev: continue
            start = ev[0]; grid = np.arange(start, t1 - tau, 0.25)
            if len(grid) < 4: continue
            e = np.array(ev)
            per_item.append(np.mean([np.any((e > g) & (e <= g + tau)) for g in grid]))
        P[tau] = per_item
    return P

def slope(xs, ys):
    xs = np.log(xs); ys = np.log(ys); return float(np.polyfit(xs, ys, 1)[0])

def estimate(items, t1, datatype, rng, B=500):
    hists = [history(x) for x in items]
    n_ev = sum(1 for e, _ in hists if e)
    out = {"n_items": len(items), "n_with_history": n_ev}
    # split-half stationarity: event rate 2016-2020 vs 2021-2025 among items with any event before 2016
    old = [e for e, _ in hists if e and e[0] < 2016]
    def ratio(sub):
        a = sum(sum(1 for t in e if 2016 <= t < 2021) for e in sub); b = sum(sum(1 for t in e if 2021 <= t < 2026) for e in sub)
        return (b + 0.5) / (a + 0.5), a, b
    if len(old) >= 10:
        r, a, b = ratio(old); bs = [ratio([old[i] for i in rng.integers(0, len(old), len(old))])[0] for _ in range(B)]
        lo, hi = np.percentile(bs, [2.5, 97.5])
        out["split_half"] = {"n": len(old), "events_2016_20": a, "events_2021_25": b, "ratio": r, "lo": float(lo), "hi": float(hi),
                             "stable": bool(lo <= 1 <= hi and 0.5 <= r <= 2)}
    else: out["split_half"] = {"n": len(old), "stable": None}
    # error-growth exponent
    def est(hs):
        if datatype == "quantity":
            D = _h_quantity(hs); taus = [t for t in LAGS_Q if len(D[t]) >= 5 and np.mean(D[t]) > 0]
            if len(taus) < 3: return None
            return slope(taus, [np.mean(D[t]) for t in taus]) / 2
        P = _h_events(hs, t1); taus = [t for t in LAGS_C if len(P[t]) >= 10 and 0 < np.mean(P[t]) < 0.95]
        if len(taus) < 3: return None
        return slope(taus, [-math.log(1 - np.mean(P[t])) for t in taus]) / 2
    H = est(hists)
    if H is None:
        out["H"] = None; out["regime"] = "NOT ESTABLISHED (too little dated history)"; return out
    bs = []
    for _ in range(B):
        h = est([hists[i] for i in rng.integers(0, len(hists), len(hists))])
        if h is not None: bs.append(h)
    lo, hi = np.percentile(bs, [2.5, 97.5])
    out.update(H=H, H_lo=float(lo), H_hi=float(hi), b_pred=1 / (1 + 2 * H))
    if lo <= 0.5 <= hi and hi - lo <= 0.4: out["regime"] = "A (H~1/2)"
    elif hi < 0.5 or lo > 0.5: out["regime"] = "not A (H != 1/2)"
    else: out["regime"] = "NOT ESTABLISHED (CI too wide)"
    return out
