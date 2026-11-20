#!/usr/bin/env python3
"""ECOLI-MEM F2 scoring (rule locked in PREREG_F2.md at f18fdfd): s = d ln sigma_n / d ln tau.
Arm C iff s in [-0.2, 0.25]; arm B iff s in [0.35, 0.65]; otherwise neither.
Sources: Park et al. 2010 Fig. 4c (digitized, park2010_fig4c_digitized.csv) and Keegstra et al. 2017 Fig. 4 source data
(eLife 6:e27455, CC BY; per-cell OU noise amplitude and timescale; fetched by fetch_keegstra.py, not committed)."""
import csv, json, os, sys
import numpy as np
from scipy.stats import theilslopes, spearmanr
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20261120)

def band(s):
    if -0.2 <= s <= 0.25: return "arm C"
    if 0.35 <= s <= 0.65: return "arm B"
    return "neither"

out = {}
# Park 2010: Var vs tau across 9 strains/conditions. s = (1/2) d lnVar / d lnTau. Errors in both -> report both
# regressions and their geometric mean (reduced major axis), bootstrap over points and digitization jitter.
rows = [r for r in csv.reader(l for l in open(os.path.join(HERE, "park2010_fig4c_digitized.csv")) if not l.startswith("#"))][1:]
V = np.array([float(r[1]) for r in rows]); T = np.array([float(r[2]) for r in rows])
x, y = np.log(T), np.log(V)
b_yx = np.polyfit(x, y, 1)[0]; b_xy = 1 / np.polyfit(y, x, 1)[0]; rma = np.sqrt(b_yx * b_xy)
boot = []
for _ in range(20000):
    i = rng.integers(0, len(x), len(x))
    if len(set(i)) < 3: continue
    p = np.polyfit(x[i], y[i], 1)[0]; q = np.polyfit(y[i], x[i], 1)[0]
    if p * q > 0: boot.append(np.sign(p) * np.sqrt(p / q) / 2)
jit = []
for _ in range(5000):
    Vp = V + rng.normal(0, 0.001, V.size); Tp = T + rng.normal(0, 0.3, T.size)
    if (Vp <= 0).any() or (Tp <= 0).any(): continue
    p = np.polyfit(np.log(Tp), np.log(Vp), 1)[0]; q = np.polyfit(np.log(Vp), np.log(Tp), 1)[0]; jit.append(np.sqrt(p / q) / 2)
out["park2010"] = dict(n=int(V.size), tau_range_s=[float(T.min()), float(T.max())],
    s_ols_var_on_tau=b_yx / 2, s_ols_tau_on_var=b_xy / 2, s_rma=rma / 2,
    s_rma_boot95=list(np.percentile(boot, [2.5, 97.5])), s_rma_digitization95=list(np.percentile(jit, [2.5, 97.5])),
    band_point=band(rma / 2))
# Keegstra 2017: natural cell-to-cell variation in wild type (CheRB+), per-cell OU fits.
kp = os.path.join(HERE, "keegstra2017_fig4_percell.csv")
if os.path.exists(kp):
    d = np.genfromtxt(kp, delimiter=",", names=True)
    ok = np.isfinite(d["eta_OU"]) & np.isfinite(d["tau_m_s"]) & (d["eta_OU"] > 0)
    tx = np.log(d["tau_m_s"][ok])
    for col in ("eta_OU", "eta_TS"):
        ty = np.log(d[col][ok]); s = np.polyfit(tx, ty, 1)[0]
        bs = [np.polyfit(tx[i], ty[i], 1)[0] for i in (rng.integers(0, tx.size, tx.size) for _ in range(20000))]
        ts = theilslopes(ty, tx); r = spearmanr(tx, ty)
        out["keegstra2017_" + col] = dict(n=int(ok.sum()), tau_range_s=[float(np.exp(tx).min()), float(np.exp(tx).max())],
            s_ols=s, s_boot95=list(np.percentile(bs, [2.5, 97.5])), s_theilsen=ts[0], s_theilsen95=[ts[2], ts[3]],
            spearman_rho=r[0], spearman_p=r[1], band_point=band(s))
else:
    print("keegstra per-cell table missing; run fetch_keegstra.py", file=sys.stderr)
json.dump(out, open(os.path.join(HERE, "f2_results.json"), "w"), indent=1, default=float)
for k, v in out.items():
    print(k, {a: (round(b, 3) if isinstance(b, float) else ([round(c, 3) for c in b] if isinstance(b, list) else b)) for a, b in v.items()})
