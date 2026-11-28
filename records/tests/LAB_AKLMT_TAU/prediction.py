"""Pre-lock: locked prediction from x paths only (no participant forecast is read). Prints the feasible-learner
implied persistence per condition and its slope on rho (b_opt) for Experiment 1 (primary) and 3 (replication)."""
import json, sys
from common import load, ols_forecasts, implied_persistence, slope_on_rho
out = {}
for exp in (1, 3):
    d = load(exp)
    d["f_ols"] = ols_forecasts(d)
    d["f_fire"] = d["rho"] * d["x_prev"]          # known-rho rational forecast (mu = 0)
    ip = implied_persistence(d, "f_ols"); ipf = implied_persistence(d, "f_fire")
    out[f"exp{exp}"] = {"ip_ols": {str(k): round(v, 4) for k, v in ip.items()},
                        "b_opt_ols": round(slope_on_rho(ip), 4),
                        "ip_fire": {str(k): round(v, 4) for k, v in ipf.items()},
                        "b_fire": round(slope_on_rho(ipf), 4),
                        "n_participants": {str(k): int(v) for k, v in d.groupby("rho")["assignmentid"].nunique().items()}}
json.dump(out, open("prediction.json", "w"), indent=1); print(json.dumps(out, indent=1))
