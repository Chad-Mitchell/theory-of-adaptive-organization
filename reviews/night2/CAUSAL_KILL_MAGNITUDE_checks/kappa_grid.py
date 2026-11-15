#!/usr/bin/env python3
"""CAUSAL-KILL-MAGNITUDE (pick 24): false-kill and power of the one-sided share rule
   FAIL iff bhat + 1.645 se < kappa * bstar_eff
for kappa in {0, 0.25, 0.5, 1}, with bstar_eff = bstar (naive) or bstar * s * lam (adjusted for a KNOWN adjustment
share s and input reliability lam; best case, their estimation error is not modelled). Own code; seed fixed.
Analytic check: with no nuisance, P(FAIL | b_true) = Phi((kappa*b* - b_true) * SNR_unit - 1.645) approximately,
SNR_unit = sqrt(K) * sd_d / sig_y; compared below for the clean rows."""
import json, math
import numpy as np
from statistics import NormalDist
Phi = NormalDist().cdf
rng = np.random.default_rng(20261125)
NS, K, sd_d, sig_y = 4000, 30, 0.5, 0.15

def run(b_true, bstar=0.5, s=1.0, sig_x=0.0, kappas=(0, 0.25, 0.5, 1.0)):
    lam = sd_d**2 / (sd_d**2 + sig_x**2)
    out = {f"k{k}": 0 for k in kappas} | {f"k{k}adj": 0 for k in kappas}
    for _ in range(NS):
        d = sd_d * rng.standard_normal(K)
        dx = d + sig_x * rng.standard_normal(K)
        dy = b_true * s * d + sig_y * rng.standard_normal(K)
        bh = (dx @ dy) / (dx @ dx); r = dy - bh * dx
        se = math.sqrt((r @ r) / (K - 1) / (dx @ dx))
        for k in kappas:
            out[f"k{k}"] += bh + 1.645 * se < k * bstar
            out[f"k{k}adj"] += bh + 1.645 * se < k * bstar * s * lam
    return {k: round(v / NS, 3) for k, v in out.items()}

snr = math.sqrt(K) * sd_d / sig_y
rows = {}
g = 0.5772156649; l3 = math.log(2e3) - g - 1
for name, kw in [("true clean", dict(b_true=0.5)),
                 ("true s=0.39", dict(b_true=0.5, s=1 - math.exp(-0.5))),
                 ("true lam=0.5", dict(b_true=0.5, sig_x=0.5)),
                 ("true s=0.63 & lam=0.5", dict(b_true=0.5, s=1 - math.exp(-1), sig_x=0.5)),
                 ("Bayes switching vs linear lock (b_true=1/l=%.3f)" % (1 / l3), dict(b_true=1 / l3)),
                 ("false b=0 (fixed share), clean", dict(b_true=0.0)),
                 ("false b=0.25b*, clean", dict(b_true=0.125)),
                 ("false b=0 with s=0.63 & lam=0.5", dict(b_true=0.0, s=1 - math.exp(-1), sig_x=0.5))]:
    rows[name] = run(**kw)
    print(f"{name:52s} {rows[name]}")
print("analytic (clean, approx, se treated as known):")
for bt in (0.5, 0.125, 0.0):
    print(" b_true", bt, {f"k{k}": round(Phi((k * 0.5 - bt) * snr - 1.645), 3) for k in (0, 0.25, 0.5, 1.0)})
json.dump(rows, open(__file__.replace(".py", ".json"), "w"), indent=1)
