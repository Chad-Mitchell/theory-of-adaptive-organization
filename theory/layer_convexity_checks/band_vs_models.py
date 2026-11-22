#!/usr/bin/env python3
"""Shape comparison, band model B vs Model S, on the 120 S5 worlds (read-only S5 eps).
Reports the rank correlation of log eps_K (K=1..J-1) and of the decrement ratios.
NUMERICAL, descriptive; B is a different model (zero-phase bands), so only shape is compared.
Run: nice -n 19 python3 theory/layer_convexity_checks/band_vs_models.py
"""
import importlib.util, json
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
HERE = Path(__file__).resolve().parent; REPO = HERE.parents[1]
spec = importlib.util.spec_from_file_location("lc", REPO / "tools" / "layer_convexity_checks.py"); lc = importlib.util.module_from_spec(spec); spec.loader.exec_module(lc)
ws = json.load(open(REPO / "core" / "keystone_checks" / "s5_rerun.json"))["worlds"]
xs, ys, rs, rb, rows = [], [], [], [], []
for w in ws:
    a = np.array(w["a"]); v = np.array(w["v"]); N = w["N"]; J = w["J"]
    _, mu, W, Ebi = lc.spectrum_grid(lc.ou_S(a, v), lambda x: N + 0 * x, a.min() * 1e-3, a.max() * 1e3 + 100, 320)
    eB = lc.band_curve(mu, W, J) / Ebi
    eS = np.array(w["eps"])
    rows.append(dict(seed=w["seed"], epsS=eS.tolist(), epsB=eB.tolist(), convexB=lc.is_convex(eB, 1e-12)))
    for K in range(1, J):
        if eS[K] > 1e-6:
            xs.append(np.log10(eS[K])); ys.append(np.log10(eB[K]))
    if eS[1] > 1e-4:
        rs.append(eS[2] / eS[1]); rb.append(eB[2] / eB[1])
summ = dict(worlds=len(ws), band_convex=sum(r["convexB"] for r in rows),
            spearman_log_eps=float(spearmanr(xs, ys).correlation), n_pairs=len(xs),
            spearman_ratio21=float(spearmanr(rs, rb).correlation), n_ratio=len(rs),
            band_max_ratio21=float(max(rb)), models_max_ratio21=float(max(rs)))
print(json.dumps(summ, indent=1))
json.dump(dict(summary=summ, worlds=rows), open(HERE / "band_vs_models.json", "w"), indent=1)
