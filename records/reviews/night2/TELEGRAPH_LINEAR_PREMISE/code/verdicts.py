"""Apply the locked decision rules of PREREG.md §5 (and amendment 1) to the out_*.json files. No new simulation."""
import json, numpy as np
d = lambda f: json.load(open("../" + f))
A, A2, FP, MC, RS, SY, LP = d("out_adapt.json"), d("out_adapt_dt0025.json"), d("out_fp.json")["rows"], d("out_mse_mc.json"), d("out_reset.json"), d("out_symbolic.json"), d("out_linproj.json")
V = {}
def p1(a):
    f1, f2, f4 = a["fits"]["F1"], a["fits"]["F2"], a["fits"]["F4"]
    agree = max(abs(a["runs"][t]["F2"]["mean_fpt"] / a["runs"][t]["F1"]["mean_fpt"] - 1) for t in a["runs"])
    return {"P1a_slope": f1["slope_vs_lntau_tau>=300"], "P1a": 0.40 <= f1["slope_vs_lntau_tau>=300"] <= 0.60,
            "P1b_ln2coef": f1["quad_coef_ln2"], "P1b": abs(f1["quad_coef_ln2"]) < 0.05,
            "P1c_maxrel_F2_vs_F1": agree, "P1c": agree <= 0.05,
            "P1e_loglog": f1["loglog_slope_tau>=1000"], "P1e": f1["loglog_slope_tau>=1000"] < 0.25,
            "P1d_F4_ln2coef": f4["quad_coef_ln2"], "P1d_F4_slope": f4["slope_vs_lntau_tau>=300"],
            "P1d": 0.15 <= f4["quad_coef_ln2"] <= 0.35 and f4["slope_vs_lntau_tau>=300"] > 1.5,
            "F3_ln2coef": a["fits"]["F3"]["quad_coef_ln2"]}
V["P1_primary_dt0.005"] = p1(A); V["P1_robust_dt0.0025"] = p1(A2)
K = np.array([r["kappa"] for r in FP])
pts = []
for tgt in (1e-3, 3e-4, 1e-4):
    r = FP[int(np.argmin(abs(np.log(K) - np.log(tgt))))]; pts.append(r)
eb = [r["eta_bayes"] for r in pts]; ek = [r["eta_kalman"] for r in pts]
V["P2a"] = {"kappa": [r["kappa"] for r in pts], "eta_B": eb, "eta_K": ek,
            "pass": all(0.75 <= e < 1.0 for e in eb) and eb == sorted(eb) and all(0.45 <= e <= 0.55 for e in ek),
            "kill": any(e <= 0.6 or e >= 1.05 for e in eb)}
T = np.array([r["tau"] for r in FP]); MB = np.array([r["mse_bayes_2xgrid"] for r in FP])
mc = {t: (v["mse"], v["se"], float(np.exp(np.interp(np.log(float(t)), np.log(T), np.log(MB))))) for t, v in MC.items()}
grid = max(abs(r["mse_bayes"] / r["mse_bayes_2xgrid"] - 1) for r in FP)
V["P2b"] = {"mc_vs_fp": {t: {"mc": m, "se": s, "fp": f, "rel": m / f - 1} for t, (m, s, f) in mc.items()}, "grid_maxrel": grid,
            "pass": all(abs(m / f - 1) <= 0.10 or abs(m - f) <= 3 * s for m, s, f in mc.values()) and grid <= 0.02}
lr = [r["mse_bayes_2xgrid"] / r["lead_2k_ln(2/k)"] for r in FP if r["kappa"] <= 1e-3]
V["P2c"] = {"ratio_range": [min(lr), max(lr)], "pass": all(0.7 <= x <= 1.3 for x in lr)}
e = pts[0]["eta_bayes"]; w, lam, mu = 1 / (1 + e), e / (1 + e), 2 * (1 - e) / (1 + e)
V["P3"] = {"eta": e, "w": w, "lambda": lam, "mu": mu,
           "pass": 0.5 <= w <= 0.6 and 0.4 <= lam <= 0.5 and 0 <= mu <= 0.3 and abs(w - 2 / 3) >= 0.07 and abs(lam - 1 / 3) >= 0.07}
ok4 = True; det = {}
for Tk, r in RS.items():
    for m, th in (("hold", "theory_hold"), ("cond", "theory_cond")):
        a_, b_ = r["telegraph"], r["ou"]
        z_to = (a_[m + "_mse"] - b_[m + "_mse"]) / np.hypot(a_[m + "_se"], b_[m + "_se"])
        z_tt = (a_[m + "_mse"] - r[th]) / a_[m + "_se"]; z_ot = (b_[m + "_mse"] - r[th]) / b_[m + "_se"]
        det[f"T{Tk}_{m}"] = [round(z_to, 2), round(z_tt, 2), round(z_ot, 2)]
        ok4 &= max(abs(z_to), abs(z_tt), abs(z_ot)) <= 3
V["P4"] = {"z(tel-ou, tel-theory, ou-theory)": det, "S5": SY["S5_equals_exp(-t/tau)"], "pass": bool(ok4 and SY["S5_equals_exp(-t/tau)"])}
V["S"] = {"S1": SY["S1_ds_coef_is_(1-x^2)/theta"] and SY["S1_dt_coef_is_-x/tau-x(1-x^2)/theta"], "S2": SY["S2_second_order_is_-x(1-x^2)"], "S5": SY["S5_equals_exp(-t/tau)"]}
V["P5"] = {**{k: LP[k] for k in ("rel_L2_bayes_vs_y", "rel_L2_bayes_vs_kalman")},
           "pass": LP["rel_L2_bayes_vs_y"] <= 0.10 and LP["rel_L2_bayes_vs_kalman"] <= 0.10}
p = V["P1_primary_dt0.005"]
V["VERDICT_P1"] = ("single-log adaptation CONFIRMED in-model" if all(p[k] for k in ("P1a", "P1b", "P1c", "P1e")) else "see rule")
V["VERDICT_P1d"] = "C&M ln^2 reproduced by printed eq.(20) read as Ito, not by the exact filter" if p["P1d"] else "not reproduced"
print(json.dumps(V, indent=1, default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o)))
json.dump(V, open("../VERDICTS.json", "w"), indent=1, default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o))
