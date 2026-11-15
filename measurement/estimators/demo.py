"""Locked real-data demo (run only after the PREREG lock commit). Two public FRED daily series, read-only:
DGS10 (10-year Treasury constant-maturity yield, percent) and VIXCLS (CBOE VIX close; analysed as log VIX).
Proxy labels: "daily published value as the drifting target; business days as equal steps; published value =
target + white sensing noise". Outputs results/demo.json. No GTAO prediction is tested."""
import json, hashlib, os, urllib.request, numpy as np
from math import log, pi
import aqn
SERIES = {"DGS10": False, "VIXCLS": True}  # value: take log
START, END = "1990-01-02", "2026-10-30"     # fixed window (VIXCLS starts 1990-01-02)
os.makedirs("data", exist_ok=True)

def fetch(sid):
    path = f"data/{sid}.csv"
    if not os.path.exists(path):
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
        urllib.request.urlretrieve(url, path)
    raw = open(path, "rb").read()
    rows = [l.split(",") for l in raw.decode().strip().splitlines()[1:]]
    vals = [(d, float(v)) for d, v in rows if v not in (".", "") and START <= d <= END]
    return vals, hashlib.sha256(raw).hexdigest()

def analyse(sid, takelog, rng):
    vals, sha = fetch(sid)
    y = np.array([v for _, v in vals]); y = np.log(y) if takelog else y
    n = y.size
    full = aqn.whittle_fit(y)
    lowband = aqn.whittle_fit(y, band=(2 * pi / n, 2 * pi / 20))        # periods > 20 business days
    highband = aqn.whittle_fit(y, band=(2 * pi / 20, pi))
    corner = aqn.whittle_corner_fit(y)
    out = {"series": sid, "log": takelog, "n": n, "first": vals[0][0], "last": vals[-1][0], "sha256": sha,
           "full": {k: full[k] for k in ("alpha", "se_alpha", "logq", "se_logq", "logs2", "se_logs2", "at_bound", "w_cross")},
           "low_band": {k: lowband[k] for k in ("alpha", "se_alpha", "logq", "se_logq", "logs2", "se_logs2", "at_bound")},
           "high_band": {k: highband[k] for k in ("alpha", "se_alpha", "logq", "se_logq", "logs2", "se_logs2", "at_bound")},
           "corner_LR": corner["LR"], "corner_w0": corner["w0"], "corner_alpha": corner["alpha"],
           "dfa_alpha": aqn.dfa_alpha(y), "variogram": dict(zip(("alpha", "q", "s2"), aqn.variogram_nugget(y)))}
    d = np.diff(y)
    out["incr_excess_kurtosis"] = float(np.mean((d - d.mean()) ** 4) / np.var(d) ** 2 - 3)
    lr, p, h, o = aqn.premise_test(y, 39, rng)
    out["premise"] = {"LR_hmm_vs_ou": lr, "p_boot": p, "hmm": {k: h[k] for k in ("mu", "lam", "s2", "q", "kappa", "tA")},
                      "ou": {k: o[k] for k in ("phi", "v", "s2", "q")}}
    # alpha band-consistency (regime check, PREREG §4): |alpha_low - alpha_high| vs combined SE
    out["band_z"] = (lowband["alpha"] - highband["alpha"]) / np.hypot(lowband["se_alpha"], highband["se_alpha"])
    return out

if __name__ == "__main__":
    rng = np.random.default_rng(20261115 + 777)
    res = [analyse(s, t, rng) for s, t in SERIES.items()]
    json.dump(res, open("results/demo.json", "w"), indent=1, default=float)
    print(json.dumps(res, indent=1, default=float))
