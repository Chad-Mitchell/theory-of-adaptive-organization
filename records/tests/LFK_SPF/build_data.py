#!/usr/bin/env python3
"""LFK-ALPHA-SPF data assembly (no outcome computed here).

Inputs (raw, kept on the box in RAW, sha256 listed in data/RAW_SHA256.txt):
  SPF consensus means: Philadelphia Fed meanLevel.xlsx (downloaded 15 Nov 2026).
  Actuals and environment series, latest vintage: Philadelphia Fed RTDSM (*QvQd, *MvMd, *QvMd) and
  Federal Reserve H.15 data package (TB 3m secondary, 10y CMT, Moody's Aaa).
Outputs: data/target_<VAR>.csv (quarterly target series, latest vintage) and data/spf_<VAR>.csv
  (survey quarter, F_t of target t+3, F_{t-1} of target t+3, actual of t+3). Targets: growth variables use the
  SPF convention 100*((X_{q}/X_{q-1})^4 - 1) on quarterly levels; rate variables (CPI etc.) use SPF's own
  annualized q/q rates; level variables use the quarterly average level.
"""
import hashlib, os, re, sys
import numpy as np, pandas as pd

RAW = os.environ.get("LFK_RAW", "<local>/lfk_spf")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

# var: (kind, source, file/series, scale applied to actual)
VARS = {
 "NGDP":    ("growth", "rtdsm", "NOUTPUTQvQd.xlsx", 1),
 "PGDP":    ("growth", "rtdsm", "PQvQd.xlsx", 1),
 "CPROF":   ("growth", "rtdsm", "NCPROFATQvQd.xlsx", 1),
 "UNEMP":   ("level",  "rtdsm", "rucQvMd.xlsx", 1),
 "EMP":     ("growth", "rtdsm", "employMvMd.xlsx", 1),
 "INDPROD": ("growth", "rtdsm", "iptMvMd.xlsx", 1),
 "HOUSING": ("level",  "rtdsm", "hstartsMvMd.xlsx", 1e-3),
 "TBILL":   ("level",  "h15",   "RIFSGFSM03_N.M", 1),
 "BOND":    ("level",  "h15",   "RIMLPAAAR_N.M", 1),
 "BAABOND": ("level",  "h15",   "RIMLPBAAR_N.M", 1),
 "TBOND":   ("level",  "h15",   "RIFLGFCY10_N.M", 1),
 "RGDP":    ("growth", "rtdsm", "ROUTPUTQvQd.xlsx", 1),
 "RCONSUM": ("growth", "rtdsm", "RCONQvQd.xlsx", 1),
 "RNRESIN": ("growth", "rtdsm", "rinvbfQvQd.xlsx", 1),
 "RRESINV": ("growth", "rtdsm", "rinvresidQvQd.xlsx", 1),
 "RFEDGOV": ("growth", "rtdsm", "RGFQvQd.xlsx", 1),
 "RSLGOV":  ("growth", "rtdsm", "RGSLQvQd.xlsx", 1),
 "CPI":     ("rate",   "rtdsm", "cpiQvMd.xlsx", 1),
 "CORECPI": ("rate",   "rtdsm", "pcpixMvMd.xlsx", 1),
 "PCE":     ("rate",   "rtdsm", "pconQvQd.xlsx", 1),
 "COREPCE": ("rate",   "rtdsm", "PCONXQvQd.xlsx", 1),
}
# Excluded a priori (declared in PREREG before outcomes): RCBI and REXPORT (levels in chained dollars whose
# base year differs between survey vintage and latest vintage: actual - forecast is not unit-consistent).

def qindex(s):
    s = str(s)
    m = re.match(r"(\d{4}):Q(\d)", s)
    if m: return int(m.group(1)) * 4 + int(m.group(2)) - 1
    m = re.match(r"(\d{4}):(\d{2})", s)
    if m: return ("M", int(m.group(1)), int(m.group(2)))
    raise ValueError(s)

def rtdsm_latest(fname):
    x = pd.ExcelFile(os.path.join(RAW, "rtdsm", fname), engine="calamine")
    d = x.parse(x.sheet_names[0])
    col = d.columns[-1]
    d = d[["DATE", col]].dropna()
    d[col] = pd.to_numeric(d[col], errors="coerce"); d = d.dropna()
    first = qindex(d["DATE"].iloc[0])
    if isinstance(first, tuple):  # monthly obs -> quarterly average (complete quarters only)
        ym = d["DATE"].astype(str).str.split(":", expand=True).astype(int)
        q = ym[0] * 4 + (ym[1] - 1) // 3
        g = d.groupby(q.values)[col].agg(["mean", "count"])
        g = g[g["count"] == 3]["mean"]
        return pd.Series(g.values, index=g.index.astype(int)), col
    return pd.Series(d[col].values, index=[qindex(v) for v in d["DATE"]]), col

def h15_monthly(series):
    x = open(os.path.join(RAW, "h15", "H15_data.xml")).read()
    i = x.index(f'SERIES_NAME="{series}"'); j = x.index("</kf:Series>", i)
    obs = re.findall(r'OBS_STATUS="(\w+)" OBS_VALUE="([-\d.E+]+)" TIME_PERIOD="(\d{4})-(\d{2})', x[i:j])
    if not obs:
        obs = [(a, b, c, d) for (c, d, a, b) in []]
        obs2 = re.findall(r'TIME_PERIOD="(\d{4})-(\d{2})[^"]*" OBS_VALUE="([-\d.E+]+)"', x[i:j])
        rows = [(int(y), int(m), float(v)) for y, m, v in obs2]
    else:
        rows = [(int(y), int(m), float(v)) for st, v, y, m in obs if st == "A"]
    df = pd.DataFrame(rows, columns=["y", "m", "v"])
    q = df.y * 4 + (df.m - 1) // 3
    g = df.groupby(q.values)["v"].agg(["mean", "count"]); g = g[g["count"] == 3]["mean"]
    return pd.Series(g.values, index=g.index.astype(int))

def target_series(var):
    kind, src, f, scale = VARS[var]
    if src == "rtdsm":
        lev, col = rtdsm_latest(f)
    else:
        lev, col = h15_monthly(f), f
    lev = lev.sort_index() * scale
    lev = lev[~lev.index.duplicated()]
    if kind == "level":
        tgt = lev
    else:  # growth and rate: annualized q/q percent change of the quarterly level
        prev = lev.reindex(lev.index - 1).values
        tgt = pd.Series(100 * ((lev.values / prev) ** 4 - 1), index=lev.index).dropna()
    full = pd.RangeIndex(tgt.index.min(), tgt.index.max() + 1)
    tgt = tgt.reindex(full)
    return tgt, col

def spf_pairs(var, tgt):
    kind = VARS[var][0]
    d = pd.read_excel(os.path.join(RAW, "meanLevel.xlsx"), sheet_name=var, engine="calamine")
    d["q"] = (d.YEAR * 4 + d.QUARTER - 1).astype(int)
    d = d.set_index("q")
    c = {k: pd.to_numeric(d[f"{var}{k}"], errors="coerce") for k in range(1, 7)}
    if kind == "level" or kind == "rate":
        f_t = c[5]                       # survey t, quarter t+3
        f_tm1 = c[6].shift(1)            # survey t-1, quarter (t-1)+4 = t+3
    else:
        f_t = 100 * ((c[5] / c[4]) ** 4 - 1)
        f_tm1 = (100 * ((c[6] / c[5]) ** 4 - 1)).shift(1)
    f_tm1 = f_tm1.reindex(d.index)
    # shift(1) above is positional; guard that the previous row is the previous quarter
    prevq = pd.Series(d.index, index=d.index).shift(1)
    f_tm1[prevq != d.index - 1] = np.nan
    act = tgt.reindex(d.index + 3).values
    out = pd.DataFrame({"survey_q": d.index, "target_q": d.index + 3, "F_t": f_t.values,
                        "F_tm1": f_tm1.values, "actual": act})
    return out

def qlabel(q): return f"{q // 4}Q{q % 4 + 1}"

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "RAW_SHA256.txt"), "w") as fh:
        for root, _, files in os.walk(RAW):
            for fn in sorted(files):
                if fn.endswith((".xlsx", ".xml")):
                    p = os.path.join(root, fn)
                    fh.write(f"{hashlib.sha256(open(p,'rb').read()).hexdigest()}  {os.path.relpath(p, RAW)}\n")
    for v in VARS:
        tgt, col = target_series(v)
        t = pd.DataFrame({"q": tgt.index, "label": [qlabel(q) for q in tgt.index], "x": tgt.values})
        t.to_csv(os.path.join(OUT, f"target_{v}.csv"), index=False)
        p = spf_pairs(v, tgt); p["survey"] = [qlabel(q) for q in p.survey_q]
        p.to_csv(os.path.join(OUT, f"spf_{v}.csv"), index=False)
        ok = p.dropna()
        print(f"{v:8s} src={col:16s} target {qlabel(tgt.dropna().index[0])}-{qlabel(tgt.dropna().index[-1])} "
              f"n_target={tgt.notna().sum():4d}  spf pairs complete={len(ok):4d} "
              f"(<=2019Q4 targets: {(ok.target_q <= 2019*4+3).sum()})")
