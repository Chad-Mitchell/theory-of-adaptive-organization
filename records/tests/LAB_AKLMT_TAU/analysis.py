"""LOCKED outcome analysis for LAB-AKLMT-TAU (pick 36). Run only after PREREG.md + this file are pushed.
Primary: D = OLS slope on rho of the participants' implied persistence (AKLMT Exp 1, h = 1, rounds 1..40, no trimming);
sigma = participant-bootstrap sd of D (within-condition resampling, B = 2000, seed 20261284). Prediction b_opt from
prediction.json (feasible OLS AR(1) learner on the same x paths), scale s*lam = 1, kappa_F = 1/2, z = 1.96.
  FAIL (failed on proxy)  iff D + z*sigma < kappa_F * b_opt    (takes precedence)
  PASS (passed on proxy)  iff D - z*sigma > 0 and not FAIL
  else INCONCLUSIVE.
Report-only rows (no verdict): R1 FIRE prediction b = 1; R2 trimmed (|F - x_{t-1}| > 200 dropped); R3 Exp 3 (MIT,
rho 0.2/0.6) same rule; R4 ratio D/b_opt with percentile CI; R5 lag-2 weight given x_{t-1} per condition, participants
vs learner; R6 per-condition implied persistence, participants vs learner."""
import json, numpy as np
from common import load, ols_forecasts, implied_persistence, slope_on_rho, boot_conditions
Z, KAPPA, B, SEED = 1.959964, 0.5, 2000, 20261284
pred = json.load(open("prediction.json"))

from analysis_rule import verdict as _v
def verdict(D, s, b):
    return _v(D, s, b)
def _unused(D, s, b):
    if D + Z * s < KAPPA * b: return "FAIL"
    if D - Z * s > 0: return "PASS"
    return "INCONCLUSIVE"

def run(exp, col, d):
    ip = implied_persistence(d, col); D = slope_on_rho(ip)
    bs = boot_conditions(d, col, B, SEED); Ds = np.array([slope_on_rho(b) for b in bs])
    return ip, D, float(Ds.std(ddof=1)), Ds

out = {}
d1 = load(1); d1["f_ols"] = ols_forecasts(d1)
b_opt = pred["exp1"]["b_opt_ols"]
ip, D, s, Ds = run(1, "predictiona_value", d1)
out["primary"] = {"D": round(D, 4), "sigma_boot": round(s, 4), "b_opt": b_opt, "fail_threshold": round(KAPPA * b_opt, 4),
                  "D_ci95_normal": [round(D - Z * s, 4), round(D + Z * s, 4)], "verdict": verdict(D, s, b_opt)}
out["R1_fire"] = {"b": 1.0, "verdict": verdict(D, s, 1.0)}
d1t = d1.copy(); bad = (d1t["predictiona_value"] - d1t["x_prev"]).abs() > 200
d1t.loc[bad, "predictiona_value"] = np.nan
ipt, Dt, st, _ = run(1, "predictiona_value", d1t)
out["R2_trimmed"] = {"n_dropped": int(bad.sum()), "D": round(Dt, 4), "sigma": round(st, 4), "verdict": verdict(Dt, st, b_opt)}
d3 = load(3); ip3, D3, s3, _ = run(3, "predictiona_value", d3)
out["R3_exp3"] = {"ip": {str(k): round(v, 4) for k, v in ip3.items()}, "D": round(D3, 4), "sigma": round(s3, 4),
                  "b_opt": pred["exp3"]["b_opt_ols"], "verdict": verdict(D3, s3, pred["exp3"]["b_opt_ols"])}
r = Ds / b_opt
out["R4_ratio"] = {"D_over_b_opt": round(D / b_opt, 4), "ci95_pct": [round(float(np.quantile(r, .025)), 4), round(float(np.quantile(r, .975)), 4)]}
d1["x_prev2"] = d1.groupby("assignmentid")["actual"].shift(2)
lag = {}
for rho, g in d1[d1["round"] >= 1].dropna(subset=["predictiona_value", "x_prev", "x_prev2"]).groupby("rho"):
    X = np.column_stack([np.ones(len(g)), g["x_prev"], g["x_prev2"]])
    bh = np.linalg.lstsq(X, g["predictiona_value"].to_numpy(), rcond=None)[0]
    bl = np.linalg.lstsq(X, g["f_ols"].to_numpy(), rcond=None)[0]
    lag[str(rho)] = {"participants": [round(bh[1], 4), round(bh[2], 4)], "learner": [round(bl[1], 4), round(bl[2], 4)]}
out["R5_lag_weights_[x_t-1, x_t-2]"] = lag
out["R6_ip"] = {str(k): {"participants": round(ip[k], 4), "learner": pred["exp1"]["ip_ols"][str(k)]} for k in ip}
json.dump(out, open("results.json", "w"), indent=1); print(json.dumps(out, indent=1))
