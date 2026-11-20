"""GRID-2 (GB) as locked (PREREG_GRID2.md) and adjusted by DV-GB1 (50502a0); GRID-S S1 (8b0ef50).
Raw data path: env GB_DATA (not in git)."""
import os, sys, json, glob, gzip
import numpy as np, pandas as pd
from scipy.signal import welch, lfilter
from scipy.optimize import least_squares

DATA = os.environ.get("GB_DATA", "/workspace/gtao-gb-data")
OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20262)
F0 = 50.0
CFG = json.loads(os.environ.get("GRID_CFG", "{}"))  # G3a / GRID-4 reuse this code with other weeks and inputs
WEEKS = CFG.get("weeks", ["2026-01-05", "2026-04-06", "2026-07-06", "2026-10-05"])
EAC_FILES = CFG.get("eac", ["eac_fy2025.csv", "eac_summary.csv"])
MFR_FILES = CFG.get("mfr", ["mfr_360561.bin", "mfr_381851.bin"])
FLAT_Q = CFG.get("flat_Q")  # GRID-4: no DC/DM/DR; one assumed holding Q (MW), linear 0.015-0.5 Hz, tau 10/3 s
OUTNAME = CFG.get("out", "grid2_results.json")

# ---------- inputs
def freq(months):
    fs = []
    for y, m in months:
        d = pd.read_csv(os.path.join(DATA, f"f_{y}_{m:02d}.csv"))
        fs.append(pd.Series(d["f"].to_numpy(float), index=pd.to_datetime(d["dtm"], format="mixed", utc=True).dt.tz_localize(None)))
    return pd.concat(fs)

def inertia():
    d = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(os.path.join(DATA, "inertia_*.csv")))])
    t = pd.to_datetime(d["Settlement Date"]) + pd.to_timedelta((d["Settlement Period"] - 1) * 30, unit="min")
    t = t.dt.tz_localize("Europe/London", ambiguous="NaT", nonexistent="NaT").dt.tz_convert("UTC").dt.tz_localize(None)
    s = pd.Series(d["Outturn Inertia"].to_numpy(float), index=t)
    s = s[s.index.notna()].sort_index()
    return s[~s.index.duplicated(keep="last")]

def eac():
    d = pd.concat([pd.read_csv(os.path.join(DATA, f)) for f in EAC_FILES])
    d = d[d.auctionProduct.isin(["DCL", "DCH", "DML", "DMH", "DRL", "DRH"])]
    d["t"] = pd.to_datetime(d.deliveryStart)
    return {p: g.groupby("t").clearedVolume.sum().sort_index() for p, g in d.groupby("auctionProduct")}

def mfr():
    sheets = {}
    for f in MFR_FILES:
        sheets.update(pd.read_excel(os.path.join(DATA, f), sheet_name=None, header=1))
    d = pd.concat([v.rename(columns=lambda c: str(c).strip().replace(" ", "_").replace("Date", "DATE").replace("BM_UNIT", "BM_UNIT")) for v in sheets.values()])
    d["DATE"] = pd.to_datetime(d["DATE"], errors="coerce")
    d = d.dropna(subset=["DATE"])
    g = d.groupby("DATE")[["Primary_Response_MWHrs", "High_Frequency_Response_MWHrs"]].sum() / 24.0
    return g  # daily mean MW: low (primary), high

def bm(day):
    c = os.path.join(DATA, "bm", f"B_{day}.pkl")
    if os.path.exists(c): return pd.read_pickle(c)
    s = _bm(day); s.to_pickle(c); return s

def _bm(day):
    """Sum over units of (latest BOAL - PN), MW, on a 1-min grid for one UTC day (needs previous day's file)."""
    t0 = pd.Timestamp(day); grid = pd.date_range(t0, t0 + pd.Timedelta("1D"), freq="1min", inclusive="left")
    def load(ds, d):
        p = os.path.join(DATA, "bm", f"{ds}_{d}.json.gz")
        with gzip.open(p, "rt") as fh: return pd.DataFrame(json.load(fh))
    prev = (t0 - pd.Timedelta("1D")).strftime("%Y-%m-%d")
    bo = pd.concat([load("BOALF", prev), load("BOALF", day)])
    pn = load("PN", day)
    def expand(df, extra):
        a = pd.to_datetime(df.timeFrom).dt.tz_localize(None); b = pd.to_datetime(df.timeTo).dt.tz_localize(None)
        rows = []
        for i, (ta, tb, la, lb) in enumerate(zip(a, b, df.levelFrom.astype(float), df.levelTo.astype(float))):
            lo = max(ta, grid[0]); hi = min(tb, grid[-1] + pd.Timedelta("1min"))
            if hi <= lo: continue
            ts = pd.date_range(lo.ceil("1min"), hi, freq="1min", inclusive="left")
            if len(ts) == 0: continue
            frac = (ts - ta) / (tb - ta) if tb > ta else np.zeros(len(ts))
            rows.append(pd.DataFrame({"t": ts, "lvl": la + (lb - la) * np.asarray(frac, float), **{k: v.iloc[i] for k, v in extra.items()}}))
        return pd.concat(rows) if rows else pd.DataFrame(columns=["t", "lvl", *extra])
    bo = bo[bo.nationalGridBmUnit.notna()].reset_index(drop=True)
    e = expand(bo, {"u": bo.nationalGridBmUnit, "n": bo.acceptanceNumber.astype(int)})
    e = e.sort_values("n").groupby(["u", "t"]).last().reset_index()
    pn = pn[pn.nationalGridBmUnit.isin(set(e.u))].reset_index(drop=True)
    p = expand(pn, {"u": pn.nationalGridBmUnit}).groupby(["u", "t"]).lvl.mean().rename("pn").reset_index()
    m = e.merge(p, on=["u", "t"], how="left").fillna({"pn": 0.0})
    s = (m.lvl - m.pn).groupby(m.t).sum()
    return s.reindex(grid, fill_value=0.0)

# ---------- reconstruction
def curve(x, kind):
    a = np.abs(x); out = np.zeros_like(x)
    if kind == "DC": out = np.interp(a, [0, .015, .2, .5], [0, 0, .05, 1], right=1)
    if kind == "DM": out = np.interp(a, [0, .015, .1, .2], [0, 0, .05, 1], right=1)
    if kind == "DR": out = np.interp(a, [0, .015, .2], [0, 0, 1], right=1)
    if kind == "MFR": out = np.interp(a, [0, .015, .5], [0, 0, 1], right=1)
    return out

def lag(x, tau):
    a = np.exp(-1.0 / tau); return lfilter([1 - a], [1, -a], x)

def reconstruct(f, idx, E, vol, M, B, mfr_x=1.0, L_x=1.0, fat=False):
    df = f - F0
    dfdt = np.gradient(f)
    R = np.zeros_like(f)
    if FLAT_Q is not None:
        q = FLAT_Q * mfr_x; tau = 10.0 if fat else 10 / 3
        R = q * lag(curve(np.minimum(df, 0), "MFR") * (df < 0) - curve(np.maximum(df, 0), "MFR") * (df > 0), tau)
        return R + B - 0.02 * 28000 * L_x * df - (2 * E * 1000 / F0) * dfdt
    for k, fatk in [("DC", 1.0), ("DM", 1.0), ("DR", 10.0)]:
        tau = fatk if fat else fatk / 3
        lo = curve(np.minimum(df, 0), k) * vol[k + "L"]; hi = curve(np.maximum(df, 0), k) * vol[k + "H"]
        R += lag(lo * (df < 0) - hi * (df > 0), tau)
    tau = 10.0 if fat else 10 / 3
    R += mfr_x * lag(curve(np.minimum(df, 0), "MFR") * M["lo"] * (df < 0) - curve(np.maximum(df, 0), "MFR") * M["hi"] * (df > 0), tau)
    return R + B - 0.02 * 28000 * L_x * df - (2 * E * 1000 / F0) * dfdt

def align(idx, E, eacv, mf):
    E1 = E.reindex(E.index.union(idx)).ffill().reindex(idx).to_numpy()
    if FLAT_Q is not None: return E1, {}, {}
    vol = {}
    for p in ["DCL", "DCH", "DML", "DMH", "DRL", "DRH"]:
        s = eacv[p]; vol[p] = s.reindex(s.index.union(idx)).ffill(limit=None).reindex(idx).fillna(0).to_numpy()
    day = idx.normalize()
    M = {"lo": mf["Primary_Response_MWHrs"].reindex(day).fillna(0).to_numpy(),
         "hi": mf["High_Frequency_Response_MWHrs"].reindex(day).fillna(0).to_numpy()}
    return E1, vol, M

# ---------- spectrum and fit (GRID-1 rules, DV-GB1 bounds)
def lor(p, f, K):
    S = np.exp(p[0]) * np.ones_like(f)
    for k in range(K): S = S + np.exp(p[1+2*k]) / (1 + (2*np.pi*f*np.exp(p[2+2*k]))**2)
    return S

def fit_all(f, P, lo, hi, trials=40):
    y = np.log(P); n = len(f); res = {}
    for K in range(6):
        best = None
        for _ in range(trials if K else 1):
            th = np.sort(rng.uniform(lo, hi, K))
            p0 = [np.log(P.min())] + sum([[np.log(P.max()), t] for t in th], [])
            r = least_squares(lambda p: np.log(lor(p, f, K)) - y, p0, bounds=([-np.inf] + [-np.inf, lo]*K, [np.inf] + [np.inf, hi]*K))
            if best is None or r.cost < best.cost: best = r
        res[f"L{K}"] = dict(p=best.x.tolist(), bic=float(n*np.log(2*best.cost/n) + (1+2*K)*np.log(n)), K=K)
    best = None
    for g in np.linspace(0.2, 3, 8):
        r = least_squares(lambda p: np.log(np.exp(p[0]) + np.exp(p[1])*f**(-p[2])) - y, [np.log(P.min()), np.log(P.max()*f[0]**g), g],
                          bounds=([-np.inf, -np.inf, -1], [np.inf, np.inf, 5]))
        if best is None or r.cost < best.cost: best = r
    res["PL"] = dict(p=best.x.tolist(), bic=float(n*np.log(2*best.cost/n) + 3*np.log(n)))
    return res, min(res, key=lambda m: res[m]["bic"])

def separated(p, K, f):
    fine = np.logspace(np.log10(f[0]), np.log10(f[-1]), 3000)
    tot = np.trapezoid(lor(p, fine, K), fine); keep = []
    for th, A in sorted((np.exp(p[2+2*k]), np.exp(p[1+2*k])) for k in range(K)):
        sh = np.trapezoid(A / (1 + (2*np.pi*fine*th)**2), fine) / tot
        if sh >= 0.05: keep.append((float(th), float(sh)))
    sep = []
    for th, sh in keep:
        if all(max(th, t)/min(th, t) >= 2.5 for t, _ in sep): sep.append((th, sh))
    return sep

def logbin(f, P, pmin, pmax):
    m = (f >= 1/pmax) & (f <= 1/pmin); f, P = f[m], P[..., m]
    edges = 10**np.arange(np.log10(f[0]), np.log10(f[-1]) + 0.05, 0.05); fb, Pb = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        w = (f >= a) & (f < b)
        if w.any(): fb.append(f[w].mean()); Pb.append(P[..., w].mean(axis=-1))
    return np.array(fb), np.array(Pb).T

def day_periodograms(x, fs, seg, per_day):
    """per-day mean Welch periodograms (segments inside each day; NaN-containing segments skipped)."""
    n_days = len(x) // per_day; out = []
    for d in range(n_days):
        xd = x[d*per_day:(d+1)*per_day]; ps = []
        for a in range(0, per_day - seg + 1, seg // 2):
            s = xd[a:a+seg]
            if np.isnan(s).mean() > 0.0:
                if np.isnan(s).mean() > 0.01: continue
                s = pd.Series(s).interpolate(limit_direction="both").to_numpy()
            f, P = welch(s, fs=fs, window="hann", nperseg=seg, noverlap=0, detrend="constant"); ps.append(P)
        if ps: out.append(np.mean(ps, 0))
    return f, np.array(out)

def score(x, fs, seg, per_day, pmin, pmax, lo, hi, boot=0):
    f, pd_ = day_periodograms(x, fs, seg, per_day)
    fb, Pb = logbin(f, pd_.mean(0), pmin, pmax)
    res, ch = fit_all(fb, Pb, lo, hi)
    out = dict(n_days=len(pd_), choice=ch, bic={k: v["bic"] for k, v in res.items()})
    if ch == "PL": out["gamma"] = res["PL"]["p"][2]; out["sep"] = []
    else: out["sep"] = separated(np.array(res[ch]["p"]), res[ch]["K"], fb)
    if boot and ch != "PL" and out["sep"]:
        K = res[ch]["K"]; B = []
        for _ in range(boot):
            ii = rng.integers(0, len(pd_), len(pd_)); fb2, Pb2 = logbin(f, pd_[ii].mean(0), pmin, pmax)
            best = None
            for _t in range(8):
                p0 = np.array(res[ch]["p"]) + rng.normal(0, .3, 1+2*K); p0[2::2] = np.clip(p0[2::2], lo+1e-6, hi-1e-6)
                r = least_squares(lambda p: np.log(lor(p, fb2, K)) - np.log(Pb2), p0, bounds=([-np.inf]+[-np.inf, lo]*K, [np.inf]+[np.inf, hi]*K))
                if best is None or r.cost < best.cost: best = r
            s = separated(best.x, K, fb2); B.append([t for t, _ in s])
        # match bootstrap corners to the main corners by nearest log distance
        cis = []
        for th, _ in out["sep"]:
            v = [min(b, key=lambda t: abs(np.log(t/th))) for b in B if b]
            cis.append([float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))])
        out["ci"] = cis; out["boot_Ksep"] = np.bincount([len(b) for b in B]).tolist()
    return out

def desched(x, idx):
    x = x.copy(); s = pd.Series(x, index=idx)
    for key in [idx.minute*60 + idx.second, idx.hour*60 + idx.minute]:
        x = x - s.groupby(key).transform("mean").to_numpy(); s = pd.Series(x, index=idx)
    return x

if __name__ == "__main__":
    E = inertia()
    eacv = eac() if FLAT_Q is None else None; mf = mfr() if FLAT_Q is None else None
    mode = sys.argv[1] if len(sys.argv) > 1 else "main"
    results = {}
    if mode == "main":
        xs, idxs, Bs = [], [], []
        for w in WEEKS:
            days = pd.date_range(w, periods=7, freq="1D")
            fw = freq([(w[:4] and int(w[:4]), int(w[5:7]))])
            idx = pd.date_range(days[0], days[-1] + pd.Timedelta("1D"), freq="1s", inclusive="left")
            fv = fw[~fw.index.duplicated()].reindex(idx).to_numpy()
            Bm = pd.concat([bm(d.strftime("%Y-%m-%d")) for d in days])
            Bv = Bm.reindex(Bm.index.union(idx)).interpolate().reindex(idx).to_numpy()
            xs.append(fv); idxs.append(idx); Bs.append(Bv)
        f = np.concatenate(xs); idx = idxs[0].append(idxs[1:]); B = np.concatenate(Bs)
        cov_f = float(np.isfinite(f).mean()); E1, vol, M = align(idx, E, eacv, mf)
        cov_E = float(np.isfinite(E1).mean())
        prem = dict(coverage_freq=cov_f, coverage_inertia=cov_E, mean_E=float(np.nanmean(E1)),
                    mean_DCL=float(vol["DCL"].mean()) if vol else None, mean_DRL=float(vol["DRL"].mean()) if vol else None,
                    mean_MFR_lo=float(M["lo"].mean()) if M else None,
                    sd_B=float(np.nanstd(B)))
        print(json.dumps(prem)); results["premise"] = prem
        if cov_f < 0.9 or cov_E < 0.9:
            print("INVALID coverage"); json.dump(results, open(os.path.join(OUT, OUTNAME), "w"), indent=1); sys.exit()
        fi = pd.Series(f).interpolate(limit=60, limit_area="inside").to_numpy()
        variants = {"main": {}, "mfr_0.5": dict(mfr_x=.5), "mfr_1.5": dict(mfr_x=1.5), "L_0.5": dict(L_x=.5),
                    "L_1.5": dict(L_x=1.5), "lag_FAT": dict(fat=True), "B_dropped": "B0"}
        for x in CFG.get("q_variants", []): variants[f"Q_x{x}"] = dict(mfr_x=x)
        for lab, kw in variants.items():
            Bx = np.zeros_like(B) if kw == "B0" else B
            D = reconstruct(fi, idx, E1, vol, M, Bx, **({} if kw == "B0" else kw))
            D = desched(D, idx)
            r = score(D, 1.0, 4*3600, 86400, 2, 4*3600, np.log(0.5), np.log(30*86400), boot=200 if lab == "main" else 0)
            results[lab] = r; print(lab, json.dumps(r)); sys.stdout.flush()
            if lab == "main":
                D15 = pd.Series(D, index=idx).resample("15min").mean().to_numpy()
                results["S1"] = score(D15, 1/900, 96, 96, 1800, 12*3600, np.log(900), np.log(30*86400), boot=200)
                print("S1", json.dumps(results["S1"])); sys.stdout.flush()
        json.dump(results, open(os.path.join(OUT, OUTNAME), "w"), indent=1)
    else:  # 12-month fast-band robustness, no B
        months = [(2025, 11), (2025, 12)] + [(2026, m) for m in range(1, 11)]
        out = []
        for y, m in months:
            fw = freq([(y, m)]); fw = fw[~fw.index.duplicated()]
            idx = pd.date_range(fw.index[0].normalize(), fw.index[-1].normalize(), freq="1s", inclusive="left")
            fv = pd.Series(fw.reindex(idx).to_numpy()).interpolate(limit=60, limit_area="inside").to_numpy()
            E1, vol, M = align(idx, E, eacv, mf)
            D = reconstruct(fv, idx, E1, vol, M, np.zeros_like(fv))
            f_, P = day_periodograms(D, 1.0, 4*3600, 86400); out.append(P)
        P = np.concatenate(out); fb, Pb = logbin(f_, P.mean(0), 2, 120)
        res, ch = fit_all(fb, Pb, np.log(0.5), np.log(30*86400))
        r = dict(n_days=len(P), choice=ch, sep=[] if ch == "PL" else separated(np.array(res[ch]["p"]), res[ch]["K"], fb),
                 bic={k: v["bic"] for k, v in res.items()})
        print(json.dumps(r)); json.dump(r, open(os.path.join(OUT, "grid2_fast12m.json"), "w"), indent=1)
