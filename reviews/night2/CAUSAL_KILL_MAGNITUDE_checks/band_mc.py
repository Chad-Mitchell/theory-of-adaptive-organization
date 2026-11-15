#!/usr/bin/env python3
"""CAUSAL-KILL-MAGNITUDE (pick 24): Monte Carlo of causal kill rules under first-principles failure modes.
Own code; imports nothing from the repo. Seed fixed.

Model. A system's log design quantity y (e.g. log read rate) responds to a log input x (e.g. log stakes) with true
elasticity b_true and first-order partial adjustment: after lag L the realized share of the long-run move is
s = 1 - exp(-L/tau). K units (contrasts) with input changes d_k ~ N(0, sd_d) (|d_k| as given). Observed:
  dy_k = b_true * s * d_k + e_y,  e_y ~ N(0, sig_y)
  dx_k = d_k + e_x,               e_x ~ N(0, sig_x)      (input measured with error)
The locked prediction is b* = 1/alpha_hat with alpha_hat ~ N(alpha, se_alpha) (locked from pre-period data).
Slope bhat = OLS through origin of dy on dx; se from residuals.
Rules (one-sided z = 1.645 tails, two-sided 1.96):
  SIGN : kill iff bhat + 1.645 se < 0 and sign(b*) > 0       (current N6: move not in predicted direction)
  BAND2: kill iff |bhat - b*| > 1.96 * sqrt(se^2 + se_bstar^2)  (symmetric elasticity band)
  LOWk : kill iff bhat + 1.645 se < kappa * b*               (one-sided 'too small', kappa = 0.5; = power_gate --fail-kappa)
Scenarios give the false-kill rate when the theory is TRUE (b_true = b* in the locked optimum's sense) under each
nuisance, and the kill rate when it is FALSE (under-responder, fixed-share rival b = 0, wrong sign).
"""
import json, math
import numpy as np

rng = np.random.default_rng(20261124)
NS = 4000

def run(b_true, alpha=2.0, se_alpha=0.1, K=30, sd_d=0.5, sig_y=0.15, sig_x=0.0, s=1.0, kappa=0.5, b_lock=None):
    kills = {"SIGN": 0, "BAND2": 0, "LOWk": 0}
    for _ in range(NS):
        ah = alpha + se_alpha * rng.standard_normal()
        bstar = 1.0 / ah if b_lock is None else b_lock
        se_bstar = se_alpha / ah**2 if b_lock is None else 0.0
        d = sd_d * rng.standard_normal(K)
        dx = d + sig_x * rng.standard_normal(K)
        dy = b_true * s * d + sig_y * rng.standard_normal(K)
        bh = (dx @ dy) / (dx @ dx)
        r = dy - bh * dx
        se = math.sqrt((r @ r) / (K - 1) / (dx @ dx))
        kills["SIGN"] += (bh + 1.645 * se < 0)
        kills["BAND2"] += (abs(bh - bstar) > 1.96 * math.sqrt(se**2 + se_bstar**2))
        kills["LOWk"] += (bh + 1.645 * se < kappa * bstar)
    return {k: round(v / NS, 3) for k, v in kills.items()}

out = {}
b = 0.5  # 1/alpha at alpha = 2 (reset-read read-rate elasticity in stakes)
# --- theory TRUE (false-kill rates) ---
out["T0 true, clean"] = run(b)
out["T1 true, partial adjustment s=0.63 (L = tau)"] = run(b, s=1 - math.exp(-1))
out["T2 true, partial adjustment s=0.39 (L = tau/2)"] = run(b, s=1 - math.exp(-0.5))
out["T3 true, input noise reliability 0.5 (sig_x = sd_d)"] = run(b, sig_x=0.5)
out["T4 true, alpha SE 0.3"] = run(b, se_alpha=0.3)
out["T5 true, all of T1+T3"] = run(b, s=1 - math.exp(-1), sig_x=0.5)
# Bayes-optimal switching system scored against the DEFAULT linear lock (N6: prereg names none -> linear).
# t_A elasticity in switching time: Bayes 1/l ~ 0.17 (kappa_N16 = 1e-3), linear 0.5.
g = 0.5772156649
for kap in (1e-2, 1e-3, 1e-4):
    l = math.log(2 / kap) - g - 1
    out[f"T6 Bayes-optimal switching (kappa={kap:g}, b_true=1/l={1/l:.3f}) scored vs linear lock b*=0.5"] = run(1 / l, b_lock=0.5)
# --- theory FALSE (kill power) ---
out["F1 under-responder b=0.25 b*"] = run(0.25 * b)
out["F2 fixed-share rival b=0"] = run(0.0)
out["F3 wrong sign b=-0.5 b*"] = run(-0.5 * b)
out["F4 over-responder b=2 b*"] = run(2 * b)
out["F1' under-responder, with T1+T3 nuisances"] = run(0.25 * b, s=1 - math.exp(-1), sig_x=0.5)
for k, v in out.items():
    print(f"{k:95s} {v}")
json.dump(out, open(__file__.replace(".py", ".json"), "w"), indent=1)
