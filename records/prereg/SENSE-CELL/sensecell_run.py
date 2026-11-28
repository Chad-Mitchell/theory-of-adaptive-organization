"""SENSE-CELL runner (written after lock; implements PREREG.md section 4 with sensecell_calc.py). nice 19."""
import json, math, sys
import numpy as np, scipy.io as sio
import sensecell_calc as C
rng = np.random.default_rng(20261118); B = 2000
d = sio.loadmat('data/FIG1_keegstra2017.mat', squeeze_me=True, struct_as_record=False)['FIG1'].analysis
a0 = np.asarray(d.a0, float); Pi = np.asarray(d.precision, float); n = len(a0)
ok = np.isfinite(a0) & np.isfinite(Pi); a0, Pi = a0[ok], Pi[ok]; n = len(a0)
FIGREAD = None
if len(sys.argv) > 1: FIGREAD = json.loads(sys.argv[1])   # method F: {"eps0_by_alpha": ...} not used unless supplied
def stats(a0m, Pim, method='A', eps0_fixed=None):
    alpha = C.alpha_from_a0(a0m); eps = abs(1 - Pim)
    eps0 = C.eps0_anchor(alpha) if method == 'A' else eps0_fixed
    out = {"alpha": alpha, "eps_obs": eps, "eps0": eps0,
           "dW_bp": C.dW_bp(eps, eps0, alpha), "beta": C.beta_phys(eps, eps0, alpha)}
    # theta over eps in [0.01, 0.05]: extremes at the ends (monotone in eps)
    th = [C.theta_eff(e, eps0, 'amplitude') for e in (0.01, 0.05)]
    out["theta_amp_lo"], out["theta_amp_hi"] = min(th), max(th)
    out["theta_var_hi"] = max(C.theta_eff(e, eps0, 'variance') for e in (0.01, 0.05))
    return out
def boot(method='A', eps0_fixed=None):
    rows = []
    for _ in range(B):
        i = rng.integers(0, n, n)
        rows.append(stats(a0[i].mean(), Pi[i].mean(), method, eps0_fixed))
    return rows
def pct(rows, k):
    v = np.array([r[k] for r in rows], float); v = v[np.isfinite(v)]
    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))], int(len(v))
res = {"n_cells": int(n), "a0_mean": float(a0.mean()), "a0_median": float(np.median(a0)), "Pi_mean": float(Pi.mean()), "Pi_median": float(np.median(Pi)),
       "Pi_sd": float(Pi.std(ddof=1)), "Pi_frac_gt1": float((Pi > 1).mean()), "Pi_frac_lt0.5": float((Pi < .5).mean())}
res["point_A"] = stats(a0.mean(), Pi.mean())
rows = boot('A')
res["boot_A"] = {k: pct(rows, k)[0] for k in ("alpha", "eps_obs", "eps0", "dW_bp", "beta", "theta_amp_lo", "theta_amp_hi", "theta_var_hi")}
bl = [r["beta"] for r in rows]; res["boot_A"]["beta_inf_fraction"] = float(np.mean([not math.isfinite(b) for b in bl]))
# verdicts, primary method A (infinite beta replicates make hi = inf)
bb = np.array([r["beta"] for r in rows]); blo = float(np.percentile(bb, 2.5)); bhi = float(np.percentile(bb, 97.5))
tlo = float(np.percentile([r["theta_amp_lo"] for r in rows], 2.5)); thi = float(np.percentile([r["theta_amp_hi"] for r in rows], 97.5))
res["verdict_A"] = {"H1": C.verdict_band_upper(tlo, thi, 0.5), "H1_interval": [tlo, thi],
                    "H2": C.verdict_band_upper(blo, bhi, 10), "H2_interval": [blo, bhi],
                    "H3": C.verdict_band_upper(blo, bhi, 1000), "H4": "INCONCLUSIVE (data gap, fixed at lock)"}
json.dump(res, open('results_A.json', 'w'), indent=1, default=str)
print(json.dumps(res, indent=1, default=str))
