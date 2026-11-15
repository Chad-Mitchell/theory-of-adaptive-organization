#!/usr/bin/env python3
"""CAUSAL-KILL-MAGNITUDE-REVIEW: reviewer's own Monte Carlo (written independently of the author's band_mc.py /
kappa_grid.py; only the scenario parameters are taken from the author note so the table can be compared).
Model: K contrasts per study; true input change d ~ N(0, sd_d^2); measured dx = d + N(0, sig_x^2);
design move dy = b_true * s * d + N(0, sig_y^2). Slope bhat by least squares through the origin on dx.
Rule: FAIL iff bhat + z*se < kappa * bstar * scale, scale = 1 (naive), s*lam (known) or s_hat*lam_hat (estimated).
Vectorised over studies; seeds fixed."""
import json, math, sys
import numpy as np
from statistics import NormalDist
N = NormalDist(); Phi = N.cdf
G = 0.5772156649015329
K, SD, SY, BSTAR = 30, 0.5, 0.15, 0.5
R = int(sys.argv[1]) if len(sys.argv) > 1 else 20000

def ell(kap): return math.log(2 / kap) - G - 1

def study(rng, b_true, s=1.0, sig_x=0.0, a_se=0.0):
    d = SD * rng.standard_normal((R, K))
    dx = d + sig_x * rng.standard_normal((R, K))
    dy = b_true * s * d + SY * rng.standard_normal((R, K))
    sxx = (dx * dx).sum(1); bh = (dx * dy).sum(1) / sxx
    res = dy - bh[:, None] * dx
    se = np.sqrt((res * res).sum(1) / (K - 1) / sxx)
    # locked elasticity 1/alpha with alpha measured (alpha=2, se a_se)
    bstar = 1 / (2 + a_se * rng.standard_normal(R)) if a_se else np.full(R, BSTAR)
    return dict(bh=bh, se=se, bstar=bstar, dx=dx, sxx=sxx)

def kill(st, kappa, z, scale=1.0, extra_var=0.0):
    thr = kappa * st["bstar"] * scale
    return float(np.mean(st["bh"] + z * np.sqrt(st["se"] ** 2 + extra_var) < thr))

S63, S39 = 1 - math.exp(-1), 1 - math.exp(-0.5)
SCEN = [("theory true, clean", dict(b_true=.5)),
        ("true, s=0.63 (L=tau)", dict(b_true=.5, s=S63)),
        ("true, s=0.39 (L=tau/2)", dict(b_true=.5, s=S39)),
        ("true, lam=0.5", dict(b_true=.5, sig_x=SD)),
        ("true, s=0.63 and lam=0.5", dict(b_true=.5, s=S63, sig_x=SD)),
        ("true, alpha se 0.3", dict(b_true=.5, a_se=.3)),
        ("Bayes switching (kN16=1e-3, b=1/l) vs linear lock", dict(b_true=1 / ell(1e-3))),
        ("false: b=0", dict(b_true=0.)),
        ("false: b=b*/4", dict(b_true=.125)),
        ("false: b=-b*/2", dict(b_true=-.25)),
        ("false: b=0 with s=0.63, lam=0.5", dict(b_true=0., s=S63, sig_x=SD))]

def table(z, seed):
    rng = np.random.default_rng(seed); out = {}
    for name, kw in SCEN:
        st = study(rng, **kw)
        lam = SD**2 / (SD**2 + kw.get("sig_x", 0) ** 2); sl = kw.get("s", 1.0) * lam
        bh, se = st["bh"], st["se"]
        row = {"sign": float(np.mean(bh + z * se < 0)),
               "band": float(np.mean(np.abs(bh - st["bstar"]) > 1.96 * se))}
        for k in (.25, .5, 1.):
            row[f"k{k}"] = kill(st, k, z); row[f"k{k}_adj"] = kill(st, k, z, sl)
        out[name] = {k: round(v, 3) for k, v in row.items()}
    return out

def q2(z, seed):
    """Estimated s and lam. tau measured with lognormal error sd_lt (log tau), lam from m duplicate pairs of the
    input measurement plus the K contrasts' own variance. 'plug' = plug-in; 'prop' = se of kappa*b*s_hat*lam_hat
    added in quadrature (delta method from reported se's)."""
    rng = np.random.default_rng(seed); out = {}
    for b_true, lab in ((.5, "true"), (0., "b=0")):
        for Lt in (1.0, 0.5):                        # lag / tau
            s = 1 - math.exp(-Lt)
            for sig_x in (0.0, SD):
                st = study(rng, b_true, s=s, sig_x=sig_x)
                for sd_lt in (0.1, 0.25, 0.5):
                    for m in (20, 50, 200):
                        if sig_x == 0 and m != 50: continue
                        lt_hat = Lt * np.exp(-sd_lt * rng.standard_normal(R))   # L / tau_hat
                        s_hat = 1 - np.exp(-lt_hat)
                        se_s = lt_hat * np.exp(-lt_hat) * sd_lt
                        if sig_x > 0:
                            dup = sig_x * math.sqrt(2) * rng.standard_normal((R, m))   # difference of 2 repeats
                            sx2 = (dup ** 2).mean(1) / 2
                            V = st["sxx"] / K
                            lam_hat = np.clip(1 - sx2 / V, 0.05, 1)
                            se_l = np.sqrt(2 * (sx2 / V) ** 2 * (1 / m + 1 / K))
                        else:
                            lam_hat = np.ones(R); se_l = np.zeros(R)
                        sc = s_hat * lam_hat
                        var_sc = (lam_hat * se_s) ** 2 + (s_hat * se_l) ** 2
                        for k in (.25, .5, 1.):
                            key = f"{lab} L/tau={Lt} lam={'0.5' if sig_x else '1'} sd_logtau={sd_lt} m={m} k={k}"
                            out[key] = {"plug": round(kill(st, k, z, sc), 3),
                                        "prop": round(kill(st, k, z, sc, (k * BSTAR) ** 2 * var_sc), 3),
                                        "known": round(kill(st, k, z, s * (SD**2 / (SD**2 + sig_x**2))), 3)}
    return out

def q1(z, seed):
    """Kill rate of a Bayes-optimal switching design (b = 1/l) under the linear lock (b* = 1/2), versus kN16,
    at the table's data size and at 4x more contrasts; and power against b = 0 at the same kappas."""
    out = {}
    for mult in (1, 4):
        snr = math.sqrt(K * mult) * SD / SY
        for kap in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
            b = 1 / ell(kap)
            out[f"K={K*mult} kN16={kap:g} ratio 2/l={2*b:.3f}"] = {f"k{k}": round(Phi((k * BSTAR - b) * snr - z), 3)
                                                                 for k in (.125, .25, .5)}
        out[f"K={K*mult} power vs b=0"] = {f"k{k}": round(Phi(k * BSTAR * snr - z), 3) for k in (.125, .25, .5)}
    return out

if __name__ == "__main__":
    res = {"R": R, "z1.645": table(1.645, 101), "z1.96": table(1.96, 202), "q2_z1.645": q2(1.645, 303),
           "q2_z1.96": q2(1.96, 404), "q1_analytic_z1.645": q1(1.645, 0)}
    json.dump(res, open(__file__.replace(".py", ".json"), "w"), indent=1)
    for sec in ("z1.645", "z1.96"):
        print("==", sec)
        for k, v in res[sec].items(): print(f"{k:55s} {v}")
    for sec in ("q2_z1.645", "q2_z1.96", "q1_analytic_z1.645"):
        print("==", sec)
        for k, v in res[sec].items(): print(f"{k:60s} {v}")
