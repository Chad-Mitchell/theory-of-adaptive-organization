#!/usr/bin/env python3
"""Synthetic validation of stakes_lib (run before any CAISO 2024/2025 analysis data was fetched).
World: 52 weeks x 7 days x 24 h; stratum FE (hour x month) in the spread; e = AR(1) within day (phi 0.9), sd by stratum;
spread = FE + k e + u, u Student-t(3) scaled, with day-level common shocks (weekly-correlated). True w = k.
Arms: (A) homoskedastic; (B) self-selection across strata: k_s log-normal, error sd_s ∝ k_s^{-1/2} (the AQN S-block failure
case for cross-sections) -> FE estimand is the e^2-variance-weighted mean of k_s; (C) price spikes: 1% of hours get
|u| x 20; (D) convex price response spread = k e (1 + |e|/sd_e) (super-quadratic loss; w defined as k). Reports bias and 95% coverage of the week-block bootstrap for w_quad and k_lin (R = 200 replicates, B = 200)."""
import json, sys, numpy as np
from stakes_lib import block_boot

def world(rng, arm, k=0.02, sd_e=600.0, sd_u=15.0):
    H, D = 24, 364
    day = np.repeat(np.arange(D), H); hour = np.tile(np.arange(H), D); month = np.minimum(day // 31, 11)
    g = hour * 12 + month; week = day // 7
    S = 24 * 12
    if arm == "B":
        ks = k * np.exp(rng.normal(0, 0.5, S)); sds = sd_e * (ks / k) ** -0.5
    else:
        ks = np.full(S, k); sds = np.full(S, sd_e)
    z = rng.normal(size=H * D); e = np.empty(H * D)
    for t in range(H * D):
        e[t] = z[t] if hour[t] == 0 else 0.9 * e[t - 1] + np.sqrt(1 - 0.81) * z[t]
    e = e * sds[g]
    fe = rng.normal(0, 10, S)[g]
    dshock = np.repeat(np.convolve(rng.normal(0, 5, D + 6), np.ones(7) / np.sqrt(7), "valid"), H)
    u = sd_u * rng.standard_t(3, H * D) / np.sqrt(3) + dshock
    if arm == "C":
        m = rng.random(H * D) < 0.01; u[m] *= 20
    spread = fe + ks[g] * e + u
    if arm == "D":   # convex price response: spread = k e (1 + |e|/sd_e); super-quadratic loss
        spread = fe + ks[g] * e * (1 + np.abs(e) / sd_e) + u
    wtrue = float(np.sum(ks[g] * (e - 0) ** 2) / np.sum(e ** 2)) if arm == "B" else k
    return e, spread, g, week, wtrue

def main(R=200, B=200):
    out = {}
    for arm in "ABCD":
        rng = np.random.default_rng(20261115 + ord(arm))
        rec = {"w_quad": [], "k_lin": []}; s2 = []
        for r in range(R):
            e, s, g, wk, wt = world(rng, arm)
            bb = block_boot(e, s, g, wk, B, seed=r)
            for key in rec:
                x = bb[key]; rec[key].append((x["est"] / wt, x["lo"] <= wt <= x["hi"], (x["hi"] - x["lo"]) / (2 * wt)))
            r2 = bb["log_large_over_small"]; s2.append(r2["lo"] <= 0 <= r2["hi"])
        out[arm] = {key: {"mean_ratio": float(np.mean([a for a, _, _ in v])), "coverage": float(np.mean([c for _, c, _ in v])),
                          "median_rel_halfwidth": float(np.median([h for _, _, h in v]))} for key, v in rec.items()}
        out[arm]["S2_pass_rate (CI of log(k_large/k_small) contains 0)"] = float(np.mean(s2))
        print(arm, json.dumps(out[arm]), flush=True)
    json.dump(out, open("validate_synth.json", "w"), indent=1)

if __name__ == "__main__":
    main(*[int(a) for a in sys.argv[1:]])
