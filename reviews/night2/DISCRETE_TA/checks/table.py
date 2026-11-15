#!/usr/bin/env python3
"""Correction-factor map from tools/discrete_ta.py (lattice-exact sampled-grid Bayes t_A) and the closed-form linear
memory time.  theta = N/mu^2 = 1 units; r = plug-in t_A / Delta (what a user computes from the N16 formula).
Writes table.json; prints a compact text table."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "tools"))
import discrete_ta as d

KAPPAS = [3e-2, 1e-2, 1e-3, 1e-4, 1e-6]
RS = [0.5, 1, 2, 3, 5, 10, 20, 30, 50, 100, 200, 500]
rows = []
for kap in KAPPAS:
    tp = d.bayes_ta_plugin(1, kap, 1)
    tcs, tcq = d.bayes_ta_cont(1, kap, 1, h=1e-3), d.bayes_ta_cont(1, kap, 1, h=1e-3, law="quiet")
    for r in RS:
        D = tp / r
        gs = d.bayes_ta_grid(1, kap, 1, D)
        gq = d.bayes_ta_grid(1, kap, 1, D, start="quiet")
        row = {"kappa": kap, "r_plugin": r, "Delta": D, "rho": D, "plugin": tp, "cont_switch": tcs, "cont_quiet": tcq,
               "grid_switch": gs, "grid_quiet": gq,
               "quiet_over_plugin": gq / tp, "switch_over_plugin": gs / tp,
               "quiet_over_cont": gq / tcq, "switch_over_cont": gs / tcs,
               "asym1_quiet": (tcq + d.C1 * math.sqrt(D)) / tcq,
               "linear_grid_over_cont": d.linear_ta_grid(1, kap, 1, D) / d.linear_ta_cont(1, kap, 1)}
        rows.append(row)
        print(f"k={kap:g} r={r:5g} D={D:.4g} quiet/plug={gq/tp:.3f} switch/plug={gs/tp:.3f} "
              f"quiet/cont={gq/tcq:.3f} switch/cont={gs/tcs:.3f} asym={row['asym1_quiet']:.3f}", flush=True)
json.dump(rows, open(os.path.join(HERE, "table.json"), "w"), indent=1)
