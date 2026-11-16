#!/usr/bin/env python3
"""R-EIV locked check (PREREG_EIV.md). Own code. Prints sigma_n, r_all and the gate BEFORE r_night."""
import glob, os, json, subprocess, numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); K = "INTERVALSTARTTIME_GMT"
P = os.path.join(H, "..", "..", "..", "tests", "STAKES_EXOGENOUS", "data")
def rtd():
    d = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(os.path.join(H, "raw", "rtd_*.csv")))], ignore_index=True)
    d = d[(d.TAC_AREA_NAME == "CA ISO-TAC") & (d.EXECUTION_TYPE == "RTD")].drop_duplicates(K)
    d["h"] = pd.to_datetime(d[K], utc=True).dt.floor("h").dt.strftime("%Y-%m-%dT%H:%M:%S-00:00")
    r = d.groupby("h").agg(rtd=("MW", "mean"), n=("MW", "size")).reset_index().rename(columns={"h": K})
    return r[r.n >= 10][[K, "rtd"]]
def panel():
    p = pd.concat([pd.read_csv(os.path.join(P, f"panel_{y}.csv.gz")) for y in (2024, 2025)], ignore_index=True)
    p = p[p.OPR_DT != "2024-06-01"].merge(rtd(), on=K, how="inner")
    dt = pd.to_datetime(p.OPR_DT); p["year"] = dt.dt.year; p["month"] = dt.dt.month
    p["g"] = p.year * 10000 + p.hr * 100 + p.month
    iso = dt.dt.isocalendar(); p["week"] = iso.year.astype(int) * 100 + iso.week.astype(int)
    p["e_act"] = p.load_act - p.load_da; p["e_rt"] = p.rtd - p.load_da; p["s"] = p.p_rt - p.p_da
    return p.reset_index(drop=True)
def dm(x, g):
    u, i = np.unique(g, return_inverse=True); return x - (np.bincount(i, weights=x) / np.bincount(i))[i]
def k(s, x, g):
    xd = dm(x, g); return float(xd @ dm(s, g) / (xd @ xd))
def r_of(d):
    s, g = d.s.values, d.g.values; ka, kr = k(s, d.e_act.values, g), k(s, d.e_rt.values, g)
    return np.log(ka / kr) if ka > 0 and kr > 0 else np.nan
NIGHT = set(range(1, 6)) | set(range(21, 25)); DAY = set(range(10, 17))
if __name__ == "__main__":
    p = panel(); night = p[p.hr.isin(NIGHT)].reset_index(drop=True)
    print("rows", len(p), "night rows", len(night), "years", sorted(p.year.unique()))
    wk = night.week.values; ub, inv = np.unique(wk, return_inverse=True); idx = [np.flatnonzero(inv == j) for j in range(ub.size)]
    rng = np.random.default_rng(20261115 + 34); bs = []
    for _ in range(2000):
        ix = np.concatenate([idx[j] for j in rng.integers(0, ub.size, ub.size)]); bs.append(r_of(night.iloc[ix]))
    bs = np.array(bs); sig = float(np.nanstd(bs, ddof=1)); nnan = int(np.isnan(bs).sum())
    r_all = r_of(p); m = r_all / 2
    print(json.dumps({"sigma_n": sig, "boot_nan": nnan, "r_all": r_all, "m": m}))
    gate = subprocess.run(["python3", os.path.join(H, "..", "..", "..", "tools", "power_gate.py"), "contrast", "--form", "optimality",
                           "--effect", str(abs(m)), "--sigma", str(sig)], capture_output=True, text=True)
    print("GATE exit", gate.returncode, gate.stdout.strip())
    if r_all >= -0.2: print("VOID: r_all >= -0.2"); raise SystemExit
    rn = r_of(night)
    v = "PASS" if rn - 1.96 * sig > m else ("FAIL" if rn + 1.96 * sig < m else "INCONCLUSIVE")
    out = {"r_night": rn, "ci": [rn - 1.96 * sig, rn + 1.96 * sig], "verdict": v, "gate_met": gate.returncode == 0}
    print("LOCKED", json.dumps(out))
    # report only
    rep = {}
    for name, d in (("all", p), ("night", night), ("day", p[p.hr.isin(DAY)])):
        g = d.g.values; ea, er = dm(d.e_act.values, g), dm(d.e_rt.values, g)
        rep[name] = {"k_act": k(d.s.values, d.e_act.values, g), "k_rt": k(d.s.values, d.e_rt.values, g), "lambda": float(ea @ er / (ea @ ea)),
                     "sd_u": float(np.std(ea - er)), "sd_e_rt": float(np.std(er)), "corr": float(np.corrcoef(ea, er)[0, 1])}
        rep[name]["ratio"] = rep[name]["k_act"] / rep[name]["k_rt"]
    for y in (2024, 2025):
        rep[f"r_night_{y}"] = r_of(night[night.year == y]); rep[f"r_all_{y}"] = r_of(p[p.year == y])
        rep[f"k_rt_{y}"] = k(p[p.year == y].s.values, p[p.year == y].e_rt.values, p[p.year == y].g.values)
    print("REPORT", json.dumps(rep, indent=1))
    json.dump({"locked": out, "sigma_n": sig, "r_all": r_all, "report": rep}, open(os.path.join(H, "eiv_results.json"), "w"), indent=1)
