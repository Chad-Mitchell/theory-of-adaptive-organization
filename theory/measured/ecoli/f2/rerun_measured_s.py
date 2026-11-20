#!/usr/bin/env python3
"""DIAGNOSTIC RERUN (not a new verdict on P1): the ECOLI-MEM single-store optimum with the store-noise scaling the F2 data
measured, Var_a(tau) = sigma_n^2 (tau/tau2)^(2s), i.e. input-referred noise V0 (tau2/tau)^(2-2s) on the low-passed signal.
s = 0 is locked arm C, s = 1/2 is locked arm B (up to the factor tau_n/tau2 = 1.19). Inputs exactly as ecoli_calc.py.
The locked PASS/FAIL thresholds of PREREG.md are applied for reference only; s was measured after the prereg, so this
cannot change the locked verdict. Closed form at low SNR (theory/STORE_NOISE.md, E1): lambda*tau* = (1-s)/s."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
lam, av, G, t1, t2, sn = 0.862, 157.1, 1.73, 0.22, 9.9, 0.092
K0 = G * t2 * t2 / (t1 + t2); V0 = sn ** 2 / K0 ** 2
taus = np.logspace(-2, 4, 60001); jm = np.argmin(abs(taus - t2))
f2 = json.load(open(os.path.join(HERE, "f2_results.json")))
s_pt = f2["park2010"]["s_rma"]; s_lo, s_hi = f2["park2010"]["s_rma_boot95"]

def opt(s, g):
    s2 = (g * 1e-3) ** 2 * av; A = 1 / (1 + lam * taus)
    ev = (s2 * A) ** 2 / (s2 * A + V0 * (t2 / taus) ** (2 - 2 * s)); i = np.argmax(ev)
    return taus[i], ev[jm] / ev[i]

res = {}
for name, s in (("s_lo", s_lo), ("s_point", s_pt), ("s_hi", s_hi)):
    r = [opt(s, g) for g in (0.1, 0.2, 0.3, 0.4)]
    res[name] = dict(s=s, tau_star_s=[a for a, _ in r], captured_fraction_at_9p9s=[b for _, b in r],
                     closed_form_low_snr_s=(1 - s) / s / lam)
allt = [t for v in res.values() for t in v["tau_star_s"]]; L, U = min(allt), max(allt)
pt = res["s_point"]["tau_star_s"]; Lp, Up = min(pt), max(pt)
M = (9.3, 10.5)
def verdict(L, U):
    if L / 2 <= M[0] and M[1] <= 2 * U: return "PASS"
    if M[0] > 3 * U or M[1] < L / 3: return "FAIL"
    return "NEITHER (between the locked pass and fail bands)"
res["reference_verdict_over_s_CI"] = dict(L=L, U=U, verdict=verdict(L, U))
res["reference_verdict_at_point_s"] = dict(L=Lp, U=Up, verdict=verdict(Lp, Up))
res["implied_s_if_9p9s_were_the_low_snr_optimum"] = 1 / (1 + lam * t2)
res["log_gap_closed_fraction_at_point_s"] = float(np.log(np.mean(pt) / 1.13) / np.log(t2 / 1.13))
json.dump(res, open(os.path.join(HERE, "rerun_results.json"), "w"), indent=1)
for k, v in res.items(): print(k, v)
