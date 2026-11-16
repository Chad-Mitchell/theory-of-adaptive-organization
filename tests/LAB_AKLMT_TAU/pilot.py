"""Pre-lock noise pilot OUTSIDE the contrast: Experiment 2 (different participants, same h = 1 task, rho 0.2-0.8).
Prints ONLY the participant-bootstrap sd of each condition's implied persistence (no point values, no slope), then
projects the sd of the Experiment 1 slope D = slope of implied persistence on rho, scaling each condition's variance by
n_exp2 / n_exp1 and using the largest Exp-2 sd for rho = 0 and 1 (absent in Exp 2), times an inflation 1.5."""
import json, numpy as np
from common import load, boot_conditions
d2 = load(2); d1 = load(1)
bs = boot_conditions(d2, "predictiona_value", 2000, 20261284)
sd2 = {r: float(np.std([b[r] for b in bs], ddof=1)) for r in bs[0]}
n2 = d2.groupby("rho")["assignmentid"].nunique().to_dict(); n1 = d1.groupby("rho")["assignmentid"].nunique().to_dict()
smax = max(sd2.values()); nmean2 = float(np.mean(list(n2.values())))
rhos = np.array(sorted(n1)); w = (rhos - rhos.mean()) / ((rhos - rhos.mean()) ** 2).sum()
var = 0.0
for wi, r in zip(w, rhos):
    s = sd2.get(r, smax); n_ref = n2.get(r, nmean2)
    var += wi ** 2 * s ** 2 * n_ref / n1[r]
sigma_D = float(np.sqrt(var)); infl = 1.5
out = {"exp2_boot_sd_by_rho": {str(k): round(v, 4) for k, v in sd2.items()}, "n_exp2": {str(k): int(v) for k, v in n2.items()},
       "n_exp1": {str(k): int(v) for k, v in n1.items()}, "sigma_D_projected": round(sigma_D, 4), "inflation": infl,
       "sigma_D_gate": round(sigma_D * infl, 4)}
json.dump(out, open("pilot.json", "w"), indent=1); print(json.dumps(out, indent=1))
