#!/usr/bin/env python3
"""CAUSAL-KAPPA-LENIENCY (pick 38) own Monte Carlo. Independent of tools/power_gate.py (no imports from repo).
Model: K contrasts, measured input change dx_k (true dxt_k, reliability lam), design move dy_k = r*b*s*dxt_k + e_k.
Locked scaled prediction P = b*s_hat*lam_hat (s, lam estimated before data with log-sd sd_sl). Share estimate
D/P where D = OLS slope through the origin of dy on dx. Rules at z = 1.96, kappa_F = 1/2:
  R0 (current N6/MV10): FAIL iff D+z*se < kF*P; PASS iff D-z*se > 0 and not FAIL; else INC.
  R1 (mirror):          FAIL iff D+z*se < kF*P; PASS iff D-z*se > kF*P; else INC.
  R2 (kappa_F=1 'tied to measured s*lam', error propagated): FAIL iff D+z*se' < P, se'^2 = se^2+(P*sd_sl)^2.
  L  (level pairing, AND): R1 PASS and level gap |g_hat| < z*se_g, where level read on a proxy with additive bias.
"""
import numpy as np, json, sys
from statistics import NormalDist
Phi = NormalDist().cdf
rng = np.random.default_rng(20261115 + 179)
z, kF, b, s_true = 1.96, 0.5, 0.5, 0.63
lam_true = 1.0  # reliability scaling itself was checked in CAUSAL_KILL_MAGNITUDE(_REVIEW); one lam<1 row below
def run(r, snr, sd_sl=0.0, reps=20000, K=30, level_bias=0.0, lam=None):
    global lam_true
    lam_true = 1.0 if lam is None else lam
    sdx = 0.5
    # choose sigma_y so that expected SNR of scaled prediction = snr
    Ptrue = b * s_true * lam_true
    S = sdx * np.sqrt(K)
    sig = Ptrue * S / snr
    if lam_true < 1:  # keep the realized se near P/snr: remove the EIV residual from sigma
        sig = float(np.sqrt(max(sig**2 - (r*b*s_true)**2 * sdx**2 * lam_true*(1-lam_true), 1e-12)))
    out = {"R0": [0, 0, 0], "R1": [0, 0, 0], "R2": [0, 0, 0], "L_pass": 0}
    dxt = rng.normal(0, sdx * np.sqrt(lam_true), (reps, K))          # true changes
    dx = dxt + rng.normal(0, sdx * np.sqrt(1 - lam_true), (reps, K))  # measured, reliability lam
    dy = r * b * s_true * dxt + rng.normal(0, sig, (reps, K))
    sxx = (dx * dx).sum(1); D = (dx * dy).sum(1) / sxx
    res = dy - D[:, None] * dx; se = np.sqrt((res * res).sum(1) / (K - 1) / sxx)
    P = b * s_true * lam_true * np.exp(rng.normal(0, sd_sl, reps))  # plug-in estimated s*lam
    hi, lo = D + z * se, D - z * se
    f0 = hi < kF * P
    for name, pas, fail in (("R0", (lo > 0) & ~f0, f0), ("R1", (lo > kF * P) & ~f0, f0)):
        out[name] = [float(fail.mean()), float(pas.mean()), float((~fail & ~pas).mean())]
    se2 = np.sqrt(se ** 2 + (P * sd_sl) ** 2); f2 = D + z * se2 < P; p2 = (D - z * se2 > 0) & ~f2
    out["R2"] = [float(f2.mean()), float(p2.mean()), float((~f2 & ~p2).mean())]
    # level: optimum's level gap read on a proxy; true design at optimum level => true gap 0 (+ proxy bias)
    se_g = 0.05; g = level_bias + (0 if r == 1 else 0) + rng.normal(0, se_g, reps)
    out["L_pass"] = float(((lo > kF * P) & ~f0 & (np.abs(g) < z * se_g)).mean())
    out["analytic_R1"] = {"fail": Phi((kF - r) * snr - z), "pass": Phi((r - kF) * snr - z)}
    out["analytic_R0_pass"] = Phi(r * snr - z)
    out["realized_snr"] = float(Ptrue / se.mean())
    return out
rows = []
for label, r, sd_sl, lb in [("true optimum, s*lam known", 1.0, 0.0, 0.0),
                            ("true optimum, s*lam plug-in (log-sd 0.3)", 1.0, 0.3, 0.0),
                            ("true optimum, level proxy offset 0.15", 1.0, 0.0, 0.15),
                            ("prediction overstated 1.6x (r 0.63)", 0.63, 0.0, 0.0),
                            ("AKLMT-like partial responder (r 0.53)", 0.53, 0.0, 0.0),
                            ("half responder (r 0.40)", 0.40, 0.0, 0.0),
                            ("quarter responder (r 0.25)", 0.25, 0.0, 0.0),
                            ("named rival: no move (r 0)", 0.0, 0.0, 0.0),
                            ("true optimum, lam 0.8 measured", 1.0, 0.0, 0.0)]:
    for snr in (5.6, 9.7, 20.0):
        o = run(r, snr, sd_sl, level_bias=lb, lam=(0.8 if 'lam 0.8' in label else None)); o.update(scenario=label, r=r, snr=snr); rows.append(o)
        print(f"{label:45s} SNR {snr:4.1f} (real {o['realized_snr']:4.1f})  R0 F/P/I {o['R0'][0]:.3f}/{o['R0'][1]:.3f}/{o['R0'][2]:.3f}  "
              f"R1 {o['R1'][0]:.3f}/{o['R1'][1]:.3f}/{o['R1'][2]:.3f}  R2 {o['R2'][0]:.3f}/{o['R2'][1]:.3f}  "
              f"L {o['L_pass']:.3f}  anR1 F {o['analytic_R1']['fail']:.3f} P {o['analytic_R1']['pass']:.3f}")
json.dump(rows, open(sys.argv[0].replace(".py", ".json"), "w"), indent=1)
