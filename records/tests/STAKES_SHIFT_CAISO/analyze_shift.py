#!/usr/bin/env python3
"""STAKES-SHIFT-CAISO locked analysis (PREREG.md). python3 analyze_shift.py -> results.json + printed verdict."""
import json, os, sys, numpy as np, pandas as pd
from shift_lib import hourly, mse_fe, k_lin, week_index, resample, D_stat, D_boot, fe_demean, K, HERE
sys.path.insert(0, os.path.join(HERE, "..", "..", "measurement", "estimators"))
B = 2000; SEED = 20261115 + 15
ALPHA0 = 2.0; BQ = 1 / (2 * ALPHA0 - 1); BW = (ALPHA0 - 1) / (2 * ALPHA0 - 1)   # 1/3, 1/3 (best linear tracker, linear precision price)
BW_MAX = 0.4                                     # sup of (a-1)/(2a-1) over 1 < a <= 3
YEARS = list(range(2019, 2027)); PRIMARY = (2025, 2026); FAIL_EPS = 0.05; COVER = 0.90
EXCLUDE = {"2024-06-01"}
COLS = ["e_rt", "e_naive"]

def window(d, months=range(1, 11)):
    x = d[d.month.isin(list(months)) & ~d.OPR_DT.astype(str).isin(EXCLUDE)]
    return x[np.isfinite(x[COLS]).all(axis=1)].copy()

def coverage(d, y):
    days = pd.date_range(f"{y}-01-01", f"{y}-10-31").size
    return len(window(d)) / (24 * days)

def main():
    R = {"seed": SEED, "B": B, "alpha0": ALPHA0, "bq": BQ, "bw": BW}
    P = {y: hourly(y) for y in YEARS}
    R["coverage"] = {y: (coverage(P[y], y) if len(P[y]) else 0.0) for y in YEARS}
    # --- G0: stakes on the clean proxy (e_rt), full years 2024 and 2025, prices from the STAKES-EXOGENOUS panels
    st = {}
    for j, y in enumerate((2025, 2024)):
        pr = pd.read_csv(os.path.join(HERE, "..", "STAKES_EXOGENOUS", "data", f"panel_{y}.csv.gz"))[[K, "p_da", "p_rt"]]
        d = P[y].merge(pr, on=K)
        d = d[np.isfinite(d.e_rt) & ~d.OPR_DT.astype(str).isin(EXCLUDE)].copy(); d["spread"] = d.p_rt - d.p_da
        rng = np.random.default_rng(SEED + 1 + j); idx = week_index(d.week.values)
        bs = []
        for _ in range(B):
            ix = resample(idx, rng); bs.append(k_lin(d.spread.values[ix], d.e_rt.values[ix], d.g.values[ix]))
        st[y] = {"k": k_lin(d.spread.values, d.e_rt.values, d.g.values), "boot": np.array(bs), "n": int(len(d)),
                 "sd_ert_fe": float(np.sqrt(mse_fe(d.e_rt.values, d.g.values)))}
    with np.errstate(invalid="ignore", divide="ignore"):
        lr_b = np.log(st[2025]["boot"] / st[2024]["boot"])
    lr = float(np.log(st[2025]["k"] / st[2024]["k"])) if st[2025]["k"] > 0 and st[2024]["k"] > 0 else float("nan")
    lr_lo, lr_hi = np.nanpercentile(lr_b, [2.5, 97.5])
    R["stakes_clean"] = {str(y): {"k_lin": st[y]["k"], "lo": float(np.percentile(st[y]["boot"], 2.5)), "hi": float(np.percentile(st[y]["boot"], 97.5)),
                                  "n": st[y]["n"], "sd_ert_fe_MW": st[y]["sd_ert_fe"]} for y in st}
    R["stakes_clean"]["dlogw_2025_vs_2024"] = {"est": lr, "lo": float(lr_lo), "hi": float(lr_hi), "nan_frac": float(np.mean(~np.isfinite(lr_b)))}
    G0 = bool(np.isfinite(lr) and st[2025]["k"] > 0 and st[2024]["k"] > 0 and lr_hi < 0)
    # --- prediction (best linear tracker, alpha = 2, linear precision price; lag 12 months)
    D_pred = -BW * lr if np.isfinite(lr) else float("nan")
    D_upper = BW_MAX * (-lr_lo) if np.isfinite(lr_lo) else float("nan")
    R["prediction"] = {"D_pred": D_pred, "band": [0.0, D_upper], "fail_eps": FAIL_EPS}
    # N21 proxy prediction (report only): k_lin 7.8e-4 vs 32.1e-4 on e_act
    R["prediction"]["D_pred_N21_report"] = -BW * float(np.log(7.8 / 32.1))
    # --- primary D, 2026 vs 2025 (Jan-Oct)
    a, b = window(P[PRIMARY[0]]), window(P[PRIMARY[1]])
    D = float(D_stat(a, b, "e_rt", BQ)); Db = D_boot(a, b, "e_rt", BQ, B, SEED)
    se_b = float(np.std(Db, ddof=1))
    R["primary"] = {"D": D, "boot_lo": float(np.percentile(Db, 2.5)), "boot_hi": float(np.percentile(Db, 97.5)), "se_boot": se_b,
                    "dlog_mse_ert": float(np.log(mse_fe(b.e_rt.values, b.g.values)) - np.log(mse_fe(a.e_rt.values, a.g.values))),
                    "dlog_mse_naive": float(np.log(mse_fe(b.e_naive.values, b.g.values)) - np.log(mse_fe(a.e_naive.values, a.g.values))),
                    "sd_ert_fe_MW": {str(PRIMARY[0]): float(np.sqrt(mse_fe(a.e_rt.values, a.g.values))), str(PRIMARY[1]): float(np.sqrt(mse_fe(b.e_rt.values, b.g.values)))},
                    "n_hours": [int(len(a)), int(len(b))]}
    # --- year-to-year noise from earlier consecutive pairs (Jan-Oct), years with coverage >= 0.9
    pairs = {}
    for y in range(2020, 2026):
        if R["coverage"][y - 1] >= COVER and R["coverage"][y] >= COVER:
            pairs[f"{y-1}-{y}"] = float(D_stat(window(P[y - 1]), window(P[y]), "e_rt", BQ))
    R["year_pairs"] = pairs
    s_yr = float(np.std(list(pairs.values()), ddof=1)) if len(pairs) >= 3 else float("nan")
    m_yr = float(np.mean(list(pairs.values()))) if pairs else float("nan")
    se_tot = float(np.sqrt(se_b ** 2 + s_yr ** 2)) if np.isfinite(s_yr) else float("nan")
    R["noise"] = {"s_yr": s_yr, "m_yr": m_yr, "n_pairs": len(pairs), "se_tot": se_tot,
                  "lo_tot": D - 1.96 * se_tot, "hi_tot": D + 1.96 * se_tot}
    # --- gates
    G1 = R["coverage"][2025] >= COVER and R["coverage"][2026] >= COVER
    G2 = abs(R["primary"]["dlog_mse_naive"]) <= np.log(2)
    try:
        from aqn import whittle_fit
        dd = pd.concat([P[2024], P[2025]]); dd = dd[np.isfinite(dd.rtd)]
        day = dd.groupby("dkey").agg(y=("rtd", "mean"), dow=("dow", "first"), month=("month", "first")).reset_index()
        day["yr"] = day.dkey.dt.year
        full = pd.date_range("2024-01-01", "2025-12-31")
        day = day.set_index("dkey").reindex(full)
        miss = int(day.y.isna().sum()); day["y"] = day.y.interpolate(limit_direction="both")
        day["dow"] = day.index.dayofweek; day["month"] = day.index.month; day["yr"] = day.index.year
        resid = fe_demean(day.y.values, (day.yr * 1000 + day.month * 10 + day.dow).values)
        wf = whittle_fit(resid)
        R["alpha"] = {"alpha": wf["alpha"], "se": wf["se_alpha"], "at_bound": wf["at_bound"], "logq": wf["logq"], "logs2": wf["logs2"], "days_interpolated": miss}
        G4cap = bool(wf["alpha"] + 2 * wf["se_alpha"] < 1.1)
    except Exception as ex:
        R["alpha"] = {"error": repr(ex)}; G4cap = False
    R["gates"] = {"G0_stakes_fell_clean": G0, "G1_coverage": bool(G1), "G2_naive_within_2x": bool(G2),
                  "G4_alpha_clearly_le_1_cap": G4cap, "year_noise_available": bool(np.isfinite(s_yr))}
    # --- verdict (locked)
    if not (G0 and G1 and G2) or G4cap or not np.isfinite(se_tot):
        v = "INCONCLUSIVE"; why = "gate"
    elif D - 1.96 * se_tot > 0 and D <= D_upper:
        v = "PASSED"; why = "D > 0 beyond boot+year noise, within predicted band"
    elif D + 1.96 * se_tot < FAIL_EPS:
        v = "FAILED"; why = "data exclude even a 5% rise in q-adjusted MSE"
    else:
        v = "INCONCLUSIVE"; why = "neither rule met" + (" (size above band)" if D - 1.96 * se_tot > 0 else "")
    R["verdict"] = v; R["verdict_reason"] = why
    # --- report only
    rep = {}
    for col in ("e_2da", "e_act"):
        aa, bb = a[np.isfinite(a[col])], b[np.isfinite(b[col])]
        rep[f"D_{col}"] = float(D_stat(aa, bb, col, BQ))
    night = [1, 2, 3, 4, 5, 20, 21, 22, 23, 24]
    aa, bb = a[a.hr.isin(night) & np.isfinite(a.e_act)], b[b.hr.isin(night) & np.isfinite(b.e_act)]
    rep["D_e_act_night"] = float(D_stat(aa, bb, "e_act", BQ))
    rep["D_detrended"] = D - m_yr if np.isfinite(m_yr) else float("nan")
    for lab, mo in (("JanApr", range(1, 5)), ("MayOct", range(5, 11))):
        rep[f"D_{lab}"] = float(D_stat(window(P[2025], mo), window(P[2026], mo), "e_rt", BQ))
    al = R["alpha"].get("alpha", float("nan"))
    if np.isfinite(al) and 1 < al < 3:
        bq_a, bw_a = 1 / (2 * al - 1), (al - 1) / (2 * al - 1)
        rep["alpha_hat_D"] = float(D_stat(a, b, "e_rt", bq_a)); rep["alpha_hat_D_pred"] = -bw_a * lr
    rep["D_unadjusted"] = R["primary"]["dlog_mse_ert"]
    R["report_only"] = rep
    json.dump(R, open(os.path.join(HERE, "results.json"), "w"), indent=1, default=float)
    print(json.dumps({k: R[k] for k in ("coverage", "stakes_clean", "prediction", "primary", "year_pairs", "noise", "gates", "verdict", "verdict_reason", "alpha", "report_only")}, indent=1, default=float))

if __name__ == "__main__":
    main()
