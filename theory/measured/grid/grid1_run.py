"""GRID-1 run as locked (4820d91) and adjusted by DV1 (6636517). Raw data path via env GRID_DATA."""
import os, io, json, zipfile, glob
import numpy as np, pandas as pd
from scipy.signal import welch
from scipy.optimize import least_squares

DATA = os.environ.get("GRID_DATA", "/workspace/gtao-grid-data")
OUT = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20221)

def qa(name):
    f = glob.glob(os.path.join(DATA, f"Aktivierte {name} qualitaetsgesichert*.csv"))[0]
    d = pd.read_csv(f, sep=";", dtype=str, encoding="utf-8-sig")
    num = lambda c: pd.to_numeric(d[c].str.replace(".", "", regex=False).str.replace(",", ".", regex=False), errors="coerce")
    tso = ["50Hertz", "Amprion", "TenneT TSO", "TransnetBW"]  # DV2: sum equals Deutschland where present
    v = sum(num(f"{x} (Positiv)") for x in tso) - sum(num(f"{x} (Negativ)") for x in tso)
    return d["Datum"].astype(str) + " " + d["von"].astype(str), v.to_numpy(float)

def setpoint_15():
    z = zipfile.ZipFile(os.path.join(DATA, "SRL_Soll_20220101_20221231.csv.zip"))
    keys, means, counts = [], [], []
    cur, s, n = None, 0.0, 0
    with z.open(z.namelist()[0]) as fh:
        for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="latin-1"), sep=";", decimal=",", chunksize=2_000_000,
                              names=["d", "t", "v"], header=0, dtype={"d": str, "t": str}):
            hh = ch["t"].str[:2]; mm = (ch["t"].str[3:5].astype(int) // 15 * 15).map("{:02d}".format)
            k = (ch["d"] + " " + hh + ":" + mm).to_numpy()
            v = pd.to_numeric(ch["v"], errors="coerce").to_numpy(float)
            # run-length blocks in file order (keeps the duplicated DST hour as two blocks)
            brk = np.r_[True, k[1:] != k[:-1]]
            idx = np.flatnonzero(brk)
            for a, b in zip(idx, np.r_[idx[1:], len(k)]):
                if k[a] != cur:
                    if cur is not None:
                        keys.append(cur); means.append(s / n if n else np.nan); counts.append(n)
                    cur, s, n = k[a], 0.0, 0
                seg = v[a:b]; ok = np.isfinite(seg); s += seg[ok].sum(); n += int(ok.sum())
    keys.append(cur); means.append(s / n if n else np.nan); counts.append(n)
    return np.array(keys), np.array(means), np.array(counts)

def lor(p, f, K):
    S = np.exp(p[0]) * np.ones_like(f)
    for k in range(K):
        S = S + np.exp(p[1 + 2*k]) / (1 + (2*np.pi*f*np.exp(p[2 + 2*k]))**2)
    return S

def pw(p, f):
    return np.exp(p[0]) + np.exp(p[1]) * f**(-p[2])

def fit_all(f, P):
    y = np.log(P); n = len(f); res = {}
    lo, hi = np.log(900.0), np.log(30*86400.0)
    for K in range(0, 6):
        best = None
        for trial in range(40 if K else 1):
            th = np.sort(rng.uniform(lo, hi, K))
            p0 = [np.log(P.min())] + sum([[np.log(P.max()), t] for t in th], [])
            lb = [-np.inf] + [-np.inf, lo] * K; ub = [np.inf] + [np.inf, hi] * K
            try:
                r = least_squares(lambda p: np.log(lor(p, f, K)) - y, p0, bounds=(lb, ub))
            except Exception:
                continue
            if best is None or r.cost < best.cost: best = r
        rss = 2 * best.cost; k = 1 + 2*K
        res[f"L{K}"] = dict(p=best.x.tolist(), bic=n*np.log(rss/n) + k*np.log(n), K=K)
    best = None
    for g in np.linspace(0.2, 3, 8):
        r = least_squares(lambda p: np.log(pw(p, f)) - y, [np.log(P.min()), np.log(P.max()*f[0]**g), g],
                          bounds=([-np.inf, -np.inf, -1], [np.inf, np.inf, 5]))
        if best is None or r.cost < best.cost: best = r
    res["PL"] = dict(p=best.x.tolist(), bic=n*np.log(2*best.cost/n) + 3*np.log(n))
    choice = min(res, key=lambda m: res[m]["bic"])
    return res, choice

def separated(p, K, f):
    modes = [(np.exp(p[2+2*k]), np.exp(p[1+2*k])) for k in range(K)]
    fine = np.logspace(np.log10(f[0]), np.log10(f[-1]), 2000)
    tot = np.trapezoid(lor(p, fine, K), fine)
    keep = []
    for th, A in sorted(modes):
        share = np.trapezoid(A / (1 + (2*np.pi*fine*th)**2), fine) / tot
        if share >= 0.05: keep.append((th, share))
    sep = []
    for th, sh in keep:
        if all(max(th, t)/min(th, t) >= 2.5 for t, _ in sep): sep.append((th, sh))
    return sep

def spectrum(x):
    seg = 672
    # split at gaps > 1 h (4 quarters); fill shorter
    s = pd.Series(x); isn = s.isna().to_numpy()
    s = s.interpolate(limit=3, limit_area="inside").to_numpy()
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
            f, P = welch(pc[a:a+seg], fs=1/900.0, window="hann", nperseg=seg, noverlap=0, detrend="constant")
            pers.append(P)
    return f, np.array(pers)

def logbin(f, P):
    m = (f >= 1/(3.5*86400)) & (f <= 1/3600)
    f, P = f[m], P[..., m]
    edges = 10**np.arange(np.log10(f[0]), np.log10(f[-1]) + 0.05, 0.05)
    fb, Pb = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        w = (f >= a) & (f < b)
        if w.any(): fb.append(f[w].mean()); Pb.append(P[..., w].mean(axis=-1))
    return np.array(fb), np.array(Pb).T

def score(x, label, boot=True):
    f, pers = spectrum(x)
    fb, Pb = logbin(f, pers.mean(0))
    res, choice = fit_all(fb, Pb)
    out = dict(label=label, n_segments=len(pers), choice=choice, bic={k: v["bic"] for k, v in res.items()})
    if choice == "PL":
        out["gamma"] = res["PL"]["p"][2]; out["sep"] = []
    else:
        K = res[choice]["K"]; out["sep"] = separated(np.array(res[choice]["p"]), K, fb)
    if boot and choice != "PL" and out["sep"]:
        K = res[choice]["K"]; th = []
        for b in range(200):
            ii = rng.integers(0, len(pers), len(pers))
            fb2, Pb2 = logbin(f, pers[ii].mean(0))
            best = None
            for trial in range(15):
                p0 = np.array(res[choice]["p"]) + rng.normal(0, 0.3, 1 + 2*K)
                p0[2::2] = np.clip(p0[2::2], np.log(900)+1e-6, np.log(30*86400)-1e-6)
                r = least_squares(lambda p: np.log(lor(p, fb2, K)) - np.log(Pb2), p0,
                                  bounds=([-np.inf] + [-np.inf, np.log(900)]*K, [np.inf] + [np.inf, np.log(30*86400)]*K))
                if best is None or r.cost < best.cost: best = r
            s = separated(best.x, K, fb2)
            th.append(max(t for t, _ in s) if s else np.nan)
        th = np.array(th); out["boot_slowest"] = dict(n_ok=int(np.isfinite(th).sum()),
            ci=[float(np.nanpercentile(th, 2.5)), float(np.nanpercentile(th, 97.5))])
    return out

if __name__ == "__main__":
    k, A, cnt = setpoint_15()
    kq, aq = qa("aFRR"); km, mq = qa("mFRR")
    # join on (date hh:mm, occurrence) so missing quarters and the duplicated DST hour align
    def occ(keys):
        s = pd.Series(keys); return list(zip(s, s.groupby(s).cumcount()))
    sp = pd.Series(np.where(cnt >= 810, A, np.nan), index=pd.MultiIndex.from_tuples(occ(k)))
    grid = pd.MultiIndex.from_tuples(occ(kq.to_numpy()))
    A = sp.reindex(grid).to_numpy(); n = len(A)
    match = float(np.isfinite(A).mean())
    aq = np.asarray(aq); mq = np.asarray(mq)
    cov_A = float(np.isfinite(A).mean()); cov_M = float(np.isfinite(mq).mean())
    ok = np.isfinite(A) & np.isfinite(aq)
    r_set = float(np.corrcoef(A[ok], aq[ok])[0, 1])
    prem = dict(n_quarters=int(n), key_match=match, coverage_A=cov_A, coverage_M=cov_M, corr_setpoint_vs_QA=r_set,
                var_A=float(np.nanvar(A)), var_M=float(np.nanvar(mq)))
    print(json.dumps(prem, indent=1))
    json.dump(dict(premise=prem), open(os.path.join(OUT, "grid1_premise.json"), "w"), indent=1)
    import sys
    b = "--grid1b" in sys.argv
    if not b and (cov_A < 0.9 or cov_M < 0.9 or r_set < 0.9):
        print("INVALID by premise"); raise SystemExit
    if b:  # GRID-1b data rule
        ratio = float(np.nanvar(mq) / np.nanvar(A)); prem["M_var_share"] = ratio
        if cov_A < 0.9 or r_set < 0.9 or ratio >= 0.05:
            print("GRID-1b INVALID by premise"); raise SystemExit
        mq = np.where(np.isfinite(mq), mq, 0.0)
    slot = np.arange(n) % 96
    def desched(x):
        x = x.copy()
        for s_ in range(96):
            w = slot == s_; x[w] = x[w] - np.nanmean(x[w])
        return x
    runs = {}
    for lab, mult in [("main", 1.0), ("M_dropped", 0.0), ("M_doubled", 2.0)]:
        runs[lab] = score(desched(A + mult*mq), lab, boot=(lab == "main"))
        print(json.dumps(runs[lab], indent=1, default=float))
    if b:
        h2 = np.array([s.startswith(tuple(f".{m:02d}.2022" for m in range(7, 13)), 2) for s in kq.to_numpy()])
        x = desched(A + mq); x[~h2] = np.nan
        runs["H2_only"] = score(x[h2], "H2_only", boot=False)
        print(json.dumps(runs["H2_only"], indent=1, default=float))
    name = "grid1b_results.json" if b else "grid1_results.json"
    json.dump(dict(premise=prem, runs=runs), open(os.path.join(OUT, name), "w"), indent=1, default=float)
