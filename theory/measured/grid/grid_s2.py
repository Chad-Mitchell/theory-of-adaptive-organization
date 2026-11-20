"""GRID-S S2 (locked 8b0ef50, DV-S2 d5ccf03): German aFRR setpoint Jan-Jun 2026."""
import os, io, glob, json, zipfile
import numpy as np, pandas as pd
from scipy.signal import welch
import grid2_run as g

DATA = os.environ.get("DE_DATA", "/workspace/gtao-grid-data/de2026")
OUT = os.path.dirname(os.path.abspath(__file__))
g.rng = np.random.default_rng(20263)

def setpoint():
    parts = []
    for z in sorted(glob.glob(os.path.join(DATA, "SRL_Soll_2026*.zip"))):
        zf = zipfile.ZipFile(z)
        d = pd.read_csv(zf.open(zf.namelist()[0]), sep=";", decimal=",", dtype={"DATE": str, "TIME": str})
        d.columns = ["d", "t", "v"]
        ts = pd.to_datetime(d.d + " " + d.t, format="%d.%m.%Y %H:%M:%S")
        # local time: the DST hour repeats in autumn only (not in Jan-Jun); spring gap stays a gap
        parts.append(pd.Series(pd.to_numeric(d.v, errors="coerce").to_numpy(float), index=ts))
    s = pd.concat(parts); s = s[~s.index.duplicated()]
    return s

def qa(pattern, cols):
    f = glob.glob(os.path.join(DATA, pattern))[0]
    d = pd.read_csv(f, sep=";", dtype=str, encoding="utf-8-sig")
    num = lambda c: pd.to_numeric(d[c].str.replace(".", "", regex=False).str.replace(",", ".", regex=False), errors="coerce")
    v = num("Deutschland (Positiv)") - num("Deutschland (Negativ)")
    ts = pd.to_datetime(d.Datum + " " + d.von, format="%d.%m.%Y %H:%M")
    s = pd.Series(v.to_numpy(float), index=ts); return s[~s.index.duplicated()]

def segments(x, seg):
    s = pd.Series(x).interpolate(limit=10 if seg > 1000 else 3, limit_area="inside").to_numpy()
    pieces, cur = [], []
    for v in s:
        if np.isnan(v):
            if len(cur) >= seg: pieces.append(np.array(cur))
            cur = []
        else: cur.append(v)
    if len(cur) >= seg: pieces.append(np.array(cur))
    pers = []
    for pc in pieces:
        for a in range(0, len(pc) - seg + 1, seg // 2):
            f, P = welch(pc[a:a+seg], fs=fs_, window="hann", nperseg=seg, noverlap=0, detrend="constant"); pers.append(P)
    return f, np.array(pers)

def run(x, fs, seg, pmin, pmax, lo, boot=200):
    global fs_; fs_ = fs
    f, pers = segments(x, seg); fb, Pb = g.logbin(f, pers.mean(0), pmin, pmax)
    res, ch = g.fit_all(fb, Pb, np.log(lo), np.log(30*86400))
    out = dict(n_segments=len(pers), choice=ch, bic={k: v["bic"] for k, v in res.items()})
    if ch == "PL": out.update(gamma=res["PL"]["p"][2], sep=[]); return out
    K = res[ch]["K"]; out["sep"] = g.separated(np.array(res[ch]["p"]), K, fb)
    B = []
    if not boot: return out
    for _ in range(boot):
        ii = g.rng.integers(0, len(pers), len(pers)); fb2, Pb2 = g.logbin(f, pers[ii].mean(0), pmin, pmax)
        best = None
        for _t in range(8):
            p0 = np.array(res[ch]["p"]) + g.rng.normal(0, .3, 1+2*K); p0[2::2] = np.clip(p0[2::2], np.log(lo)+1e-6, np.log(30*86400)-1e-6)
            r = g.least_squares(lambda p: np.log(g.lor(p, fb2, K)) - np.log(Pb2), p0, bounds=([-np.inf]+[-np.inf, np.log(lo)]*K, [np.inf]+[np.inf, np.log(30*86400)]*K))
            if best is None or r.cost < best.cost: best = r
        B.append([t for t, _ in g.separated(best.x, K, fb2)])
    out["ci"] = [[float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] for v in
                 ([min(b, key=lambda t: abs(np.log(t/th))) for b in B if b] for th, _ in out["sep"])]
    return out

def desched(s, key):
    return s - s.groupby(key).transform("mean")

if __name__ == "__main__":
    sp = setpoint()
    idx1 = pd.date_range("2026-01-01", "2026-07-01", freq="1min", inclusive="left")
    cnt = sp.resample("1min").count().reindex(idx1, fill_value=0); m1 = sp.resample("1min").mean().reindex(idx1)
    A1 = m1.where(cnt >= 54)
    idx15 = pd.date_range("2026-01-01", "2026-07-01", freq="15min", inclusive="left")
    c15 = sp.resample("15min").count().reindex(idx15, fill_value=0); A15 = sp.resample("15min").mean().reindex(idx15).where(c15 >= 810)
    aq = qa("Aktivierte aFRR betrieblich*.csv", None).reindex(idx15); mq = qa("Aktivierte mFRR*.csv", None).reindex(idx15)
    ok = A15.notna() & aq.notna()
    prem = dict(coverage_A1=float(A1.notna().mean()), coverage_A15=float(A15.notna().mean()),
                corr_setpoint_vs_aFRR_operational=float(np.corrcoef(A15[ok], aq[ok])[0, 1]),
                coverage_M=float(mq.notna().mean()), M_var_share=float(np.nanvar(mq) / np.nanvar(A15)))
    print(json.dumps(prem)); res = dict(premise=prem)
    if prem["coverage_A1"] < 0.9 or prem["corr_setpoint_vs_aFRR_operational"] < 0.9:
        res["verdict"] = "INVALID"; json.dump(res, open(os.path.join(OUT, "grid_s2_results.json"), "w"), indent=1); raise SystemExit
    x1 = desched(A1, idx1.hour*60 + idx1.minute).to_numpy()
    res["main_1min"] = run(x1, 1/60, 7*1440, 300, 3.5*86400, 60); print("main", json.dumps(res["main_1min"]))
    x15 = desched(A15, idx15.hour*4 + idx15.minute//15).to_numpy()
    res["gridb_15min"] = run(x15, 1/900, 672, 3600, 3.5*86400, 900); print("15min", json.dumps(res["gridb_15min"]))
    if prem["M_var_share"] < 0.05:
        m1f = mq.reindex(idx1, method="ffill").fillna(0)
        res["robust_M_1min"] = run(desched(A1 + m1f, idx1.hour*60 + idx1.minute).to_numpy(), 1/60, 7*1440, 300, 3.5*86400, 60, boot=0)
        print("robM", json.dumps(res["robust_M_1min"]))
    json.dump(res, open(os.path.join(OUT, "grid_s2_results.json"), "w"), indent=1)
