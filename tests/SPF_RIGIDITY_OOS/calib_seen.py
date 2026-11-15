#!/usr/bin/env python3
"""Calibration check of the planned-sd simulator on SEEN variables (their real NW SEs are already published in
../LFK_SPF/results/outcome.out): planned-n sd of bhat under the model at K_L0w vs the real NW SE. No new outcome."""
import json, os, numpy as np
import prelock as p
NPJ = json.load(open(os.path.join(p.NP, "results", "analysis.json")))["per_var"]
ENV = json.load(open(os.path.join(p.LFK, "results", "env.json")))
OUT = json.load(open(os.path.join(p.LFK, "results", "outcome.json")))["table"]
rng = np.random.default_rng(p.SEED + 50)
for v in ["UNEMP", "HOUSING", "TBILL", "RSLGOV"]:
    fit = {k: ENV[v]["fit"][k] for k in ("tauE", "alpha", "phi")}; r = NPJ[v]
    s = p.sim_cg(fit, r["K"]["L0w"], r["nf"], int(OUT[v]["n"]), 1000, rng)
    print(f"{v:8s} n={OUT[v]['n']} planned sd {s.std(ddof=1):.3f} (mean {s.mean():.3f}, pop beta^G {r['beta_pred']['L0w']:.3f}) | real NW SE {OUT[v]['se']:.3f}", flush=True)
