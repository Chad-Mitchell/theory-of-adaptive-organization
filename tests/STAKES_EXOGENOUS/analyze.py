#!/usr/bin/env python3
"""STAKES-EXOGENOUS locked analysis (see PREREG.md). Usage: python3 analyze.py  -> results.json, prints verdict."""
import glob, json, os, numpy as np, pandas as pd
from stakes_lib import block_boot, exog_r2, winsor, relprec, estimates
HERE = os.path.dirname(os.path.abspath(__file__))
B = 2000
EXCLUDE_DAYS = {"2024-06-01"}   # plumbing day seen before the lock

def read(year, key):
    fs = sorted(glob.glob(os.path.join(HERE, "data", "raw", str(year), f"{key}_*.csv")))
    return pd.concat([pd.read_csv(f) for f in fs], ignore_index=True) if fs else pd.DataFrame()

def panel(year):
    da, act = read(year, "load_da"), read(year, "load_act")
    da = da[da.TAC_AREA_NAME == "CA ISO-TAC"]; act = act[act.TAC_AREA_NAME == "CA ISO-TAC"]
    k = ["INTERVALSTARTTIME_GMT"]
    da = da.drop_duplicates(k)[k + ["OPR_DT", "OPR_HR", "MW"]].rename(columns={"MW": "load_da"})
    act = act.drop_duplicates(k)[k + ["MW"]].rename(columns={"MW": "load_act"})
    pda = read(year, "lmp_da"); pda = pda[pda.XML_DATA_ITEM == "LMP_PRC"].drop_duplicates(k + ["NODE"])
    pda = pda.groupby(k).agg(p_da=("MW", "mean"), n_da=("MW", "size")).reset_index()
    pf = read(year, "lmp_fmm"); pf = pf[pf.XML_DATA_ITEM == "LMP_PRC"].drop_duplicates(k + ["NODE"])
    pf["hour"] = pd.to_datetime(pf.INTERVALSTARTTIME_GMT, utc=True).dt.floor("h").dt.strftime("%Y-%m-%dT%H:%M:%S-00:00")
    pf = pf.groupby("hour").agg(p_rt=("PRC", "mean"), n_rt=("PRC", "size")).reset_index().rename(columns={"hour": k[0]})
    d = da.merge(act, on=k).merge(pda, on=k).merge(pf, on=k)
    d = d[(d.n_da == 2) & (d.n_rt >= 6)]
    d = d[d.OPR_DT.str.startswith(str(year)) & ~d.OPR_DT.isin(EXCLUDE_DAYS)].copy()
    d["e"] = d.load_act - d.load_da
    d["spread"] = d.p_rt - d.p_da
    dt = pd.to_datetime(d.OPR_DT)
    d["hr"] = d.OPR_HR.clip(1, 24).astype(int); d["month"] = dt.dt.month
    d["g"] = d.hr * 100 + d.month
    iso = dt.dt.isocalendar(); d["week"] = iso.year.astype(int) * 100 + iso.week.astype(int)
    # information at DA issue time: errors of day D-2 (same hour; daily mean)
    d["dkey"] = dt
    lag = d[["dkey", "hr", "e"]].copy(); lag["dkey"] = lag.dkey + pd.Timedelta(days=2)
    d = d.merge(lag.rename(columns={"e": "e_lag2"}), on=["dkey", "hr"], how="left")
    dm = d.groupby("dkey").e.mean().rename("e_lag2_day").reset_index(); dm["dkey"] = dm.dkey + pd.Timedelta(days=2)
    d = d.merge(dm, on="dkey", how="left")
    return d.sort_values(k[0]).reset_index(drop=True)

def run(year, seed):
    d = panel(year)
    e, s, g, wk = d.e.values, d.spread.values, d.g.values, d.week.values
    r = {"year": year, "n_hours": int(len(d)), "n_weeks": int(np.unique(wk).size),
         "sd_e_MW": float(e.std()), "sd_spread": float(s.std()), "mean_load_MW": float(d.load_act.mean())}
    r["primary"] = block_boot(e, s, g, wk, B, seed)
    r["winsor_0.5"] = block_boot(e, winsor(s), g, wk, B, seed + 100)
    r["exog_incr_r2"], r["exog_n"] = exog_r2(e, g, d.e_lag2.values, d.e_lag2_day.values)
    terc = pd.qcut(d.load_act, 3, labels=False).values
    r["by_load_tercile"] = {int(t): block_boot(e[terc == t], s[terc == t], g[terc == t], wk[terc == t], 500, seed + 200 + t)["w_quad"] for t in range(3)}
    q = (d.month.values - 1) // 3
    r["by_quarter"] = {int(t): block_boot(e[q == t], s[q == t], g[q == t], wk[q == t], 500, seed + 300 + t)["w_quad"] for t in range(4)}
    # report only (exploratory, no verdict): stratum error variance vs stratum k
    st = []
    for gg in np.unique(g):
        m = g == gg
        if m.sum() >= 20:
            em, sm = e[m] - e[m].mean(), s[m] - s[m].mean()
            st.append((np.var(e[m]), float(np.dot(em, sm) / np.dot(em, em))))
    st = np.array(st)
    r["exploratory_spearman_var_e_vs_k_strata"] = float(pd.Series(st[:, 0]).corr(pd.Series(st[:, 1]), method="spearman"))
    return r

def verdict(p, rep):
    w = p["primary"]["k_lin"]; wr = rep["primary"]["k_lin"]; sh = p["primary"]["log_large_over_small"]
    S1 = w["est"] > 0 and w["lo"] > 0 and relprec(w) <= 0.5
    S2 = sh["lo"] <= 0 <= sh["hi"]
    S3 = p["exog_incr_r2"] <= 0.10
    S4 = wr["est"] > 0 and wr["lo"] > 0
    fail = (w["est"] <= 0) or (w["lo"] <= 0 <= w["hi"]) or (p["exog_incr_r2"] > 0.25)
    if S1 and S3 and S4 and S2: v = "PASS: stakes identified on proxy"
    elif S1 and S3 and S4: v = "PARTIAL: identified, but quadratic-loss consistency (S2) failed"
    elif fail: v = "FAIL: stakes not identified on proxy"
    else: v = "INCONCLUSIVE"
    return {"S1": S1, "S2": S2, "S3": S3, "S4": S4, "verdict": v}

if __name__ == "__main__":
    p = run(2025, 20261115 + 12); rep = run(2024, 20261115 + 13)
    out = {"primary_2025": p, "replication_2024": rep, "rules": verdict(p, rep)}
    json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1, default=float)
    print(json.dumps(out["rules"]), json.dumps(p["primary"]), json.dumps(rep["primary"]), p["exog_incr_r2"])
