#!/usr/bin/env python3
"""Report-only extras (post-lock, descriptive): k_rt by hour band; linear (bias x premium) cost term vs quadratic term."""
import json, numpy as np
from eiv import panel, dm, k
p = panel(); out = {}
bands = {"night_1-5_21-24": list(range(1, 6)) + list(range(21, 25)), "morning_6-9": list(range(6, 10)), "midday_10-16": list(range(10, 17)), "evening_ramp_17-20": list(range(17, 21))}
for y in (2024, 2025):
    q = p[p.year == y]
    out[y] = {b: {"k_rt": k(q[q.hr.isin(h)].s.values, q[q.hr.isin(h)].e_rt.values, q[q.hr.isin(h)].g.values),
                  "k_act": k(q[q.hr.isin(h)].s.values, q[q.hr.isin(h)].e_act.values, q[q.hr.isin(h)].g.values)} for b, h in bands.items()}
    for col in ("e_rt", "e_act"):
        g = q.g.values; e = q[col].values; s = q.s.values
        u, i = np.unique(g, return_inverse=True); n = np.bincount(i)
        eb = np.bincount(i, weights=e) / n; sb = np.bincount(i, weights=s) / n
        lin = float((n * eb * sb).sum() / len(q))                         # mean of ebar_g * sbar_g  ($/h)
        quad = float((dm(e, g) * dm(s, g)).mean())                        # mean within-stratum e~ s~ = k * Var_within(e)  ($/h)
        out[y][f"mean_cost_{col}"] = {"total_mean_e_x_spread": float((e * s).mean()), "between_strata_bias_x_premium": lin, "within_strata_k_var": quad,
                                      "mean_e_MW": float(e.mean())}
print(json.dumps(out, indent=1)); json.dump(out, open("extra.json", "w"), indent=1)
