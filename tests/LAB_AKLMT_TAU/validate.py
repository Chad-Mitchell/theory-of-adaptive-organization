"""Pre-lock synthetic validation of the locked rule (participant forecasts NOT read: the forecast column is replaced).
T1 optimal forecaster (learner + noise sd 15) -> expect PASS. T2 'sluggish' forecaster F = 0.25 rho x + 0.6 x (slope
0.25) -> expect FAIL. T3 no response to rho, F = 0.6 x -> expect FAIL."""
import json, numpy as np
from common import load, ols_forecasts, implied_persistence, slope_on_rho, boot_conditions
import analysis_rule as ar
rng = np.random.default_rng(7)
d = load(1); d["f_ols"] = ols_forecasts(d); b_opt = json.load(open("prediction.json"))["exp1"]["b_opt_ols"]
out = {}
for name, f in {"T1_opt": d["f_ols"] + rng.normal(0, 15, len(d)),
                "T2_slope025": (0.25 * d["rho"] + 0.6) * d["x_prev"] + rng.normal(0, 15, len(d)),
                "T3_flat": 0.6 * d["x_prev"] + rng.normal(0, 15, len(d))}.items():
    d["fake"] = f
    D = slope_on_rho(implied_persistence(d, "fake"))
    s = float(np.std([slope_on_rho(b) for b in boot_conditions(d, "fake", 300, 1)], ddof=1))
    out[name] = {"D": round(D, 3), "sigma": round(s, 3), "verdict": ar.verdict(D, s, b_opt)}
print(json.dumps(out, indent=1)); json.dump(out, open("validate.json", "w"), indent=1)
