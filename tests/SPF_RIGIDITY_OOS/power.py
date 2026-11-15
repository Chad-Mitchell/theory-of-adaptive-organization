#!/usr/bin/env python3
"""SPF-RIGIDITY-OOS MV10 power gate on the planned data (uses results/prelock.json only; no outcome).
Planned statistic (would-be locked): pooled multiple of the optimal-filter CG coefficient,
    c = sum_v w_v (bhat_v - bias_v) bG_v / sum_v w_v bG_v^2,   w_v = 1/sd_v^2,
bG_v = population optimal-filter beta at K_L0w, bias_v = (planned-n mean - population) finite-sample bias of the CG
regression under the model, sd_v = planned-n sampling sd of bhat under the model. CI: percentile cluster bootstrap over
variables (B = 1000). Hypotheses: H_R (item; post hoc S-1): c = 2.5 (lower end of 2.5-6x); H_0 (theory, measured-input
optimum of the Gaussian noisy filter): c = 1. PASS iff c_lo > 1; FAIL iff c_hi < 2.5 (MV10 form, kappa = 1).
Truth in the simulation: bhat_v = m * exp(tau z_v) * b_v + bias_v + sd_v e_v, with b_v drawn from the variable's beta^G
uncertainty draws (rescaled so their median is the point bG_v) and tau = between-variable heterogeneity of ln m.
Run: nice -n 19 python3 power.py -> results/power.json, results/power.out"""
import json, os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import power_gate
P = json.load(open(os.path.join(HERE, "results", "prelock.json")))
REPS, B, SEED = 2000, 1000, 20261115 + 98 + 1
M_R, M_0 = 2.5, 1.0

def setup(vs):
    bG = np.array([P[v]["beta_pop"] for v in vs]); bias = np.array([P[v]["beta_planned_mean"] - P[v]["beta_pop"] for v in vs])
    sd = np.array([P[v]["beta_planned_sd"] for v in vs])
    dr = [np.array(P[v]["beta_G_draws"]) / np.median(P[v]["beta_G_draws"]) for v in vs]
    return bG, bias, sd, dr

def c_stat(bh, bG, bias, w):
    return np.sum(w * (bh - bias) * bG, -1) / np.sum(w * bG ** 2, -1)

def decide(bh, bG, bias, sd, rng):
    w = 1 / sd ** 2; k = len(bG)
    idx = rng.integers(0, k, (B, k))
    cb = c_stat(bh[idx], bG[idx], bias[idx], w[idx])
    lo, hi = np.percentile(cb, [2.5, 97.5])
    return c_stat(bh, bG, bias, w), lo, hi

def power(vs, tau, rng):
    bG, bias, sd, dr = setup(vs); out = {}
    for name, m in (("R", M_R), ("0", M_0)):
        cs, P_, F_ = [], 0, 0
        for _ in range(REPS):
            b = np.array([bG[i] * rng.choice(dr[i]) for i in range(len(vs))])
            bh = m * np.exp(tau * rng.standard_normal(len(vs))) * b + bias + sd * rng.standard_normal(len(vs))
            c, lo, hi = decide(bh, bG, bias, sd, rng); cs.append(c)
            P_ += lo > 1; F_ += hi < M_R
        out[name] = dict(P_pass=P_ / REPS, P_fail=F_ / REPS, c_sd=float(np.std(cs)), c_median=float(np.median(cs)))
    se_c = float(1 / math.sqrt(np.sum(bG ** 2 / sd ** 2)))   # sampling-only analytic se of c
    gate = power_gate.gate(M_R - M_0, se_c)                     # optimality form: gap 1.5 vs sampling-only se (best case)
    return dict(vars=vs, tau=tau, se_c_sampling_only=se_c, info_share={v: float((bG[i] / sd[i]) ** 2 / np.sum(bG ** 2 / sd ** 2)) for i, v in enumerate(vs)},
                sim=out, gate_met=bool(out["R"]["P_pass"] >= 0.8 and out["0"]["P_fail"] >= 0.8),
                power_gate_tool_best_case=dict(P_pass_true=gate["analytic"]["P_pass_true"], P_fail_null=gate["analytic"]["P_fail_null"],
                                               gate_met=gate["gate_met"], sigma_max_needed=(M_R - M_0) / 2.8016))

if __name__ == "__main__":
    rng = np.random.default_rng(SEED)
    ok = [v for v in P if P[v]["K_flag"] == "ok"]
    narrow = [v for v in ok if P[v]["beta_G_ci"][1] / max(P[v]["beta_G_ci"][0], 1e-9) <= 10]
    res, lines = [], []
    for label, vs in (("A all K-ok", ok), ("B K-ok and beta^G CI within x10", narrow)):
        for tau in (0.0, 0.4):
            r = power(vs, tau, rng); r["set"] = label; res.append(r)
            l = (f"{label:34s} tau={tau}: k={len(vs)} se_c(sampling only)={r['se_c_sampling_only']:.2f} | "
                 f"P(PASS|c=2.5)={r['sim']['R']['P_pass']:.3f} P(FAIL|c=1)={r['sim']['0']['P_fail']:.3f} "
                 f"sd(c)|R={r['sim']['R']['c_sd']:.2f} |0={r['sim']['0']['c_sd']:.2f} | gate {'MET' if r['gate_met'] else 'NOT MET'} | "
                 f"info shares " + ", ".join(f"{v} {s:.2f}" for v, s in r["info_share"].items()))
            print(l, flush=True); lines.append(l)
    json.dump(res, open(os.path.join(HERE, "results", "power.json"), "w"), indent=1)
    open(os.path.join(HERE, "results", "power.out"), "w").write("\n".join(lines) + "\n")
