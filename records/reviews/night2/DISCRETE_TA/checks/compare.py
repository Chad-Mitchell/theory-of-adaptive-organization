#!/usr/bin/env python3
"""Cross-checks: lattice (tools/discrete_ta.py) vs independent Monte Carlo (mc_discrete.json); closed-form linear
memory time vs Riccati iteration (in the MC script); small-Delta asymptote; universality of the excess
g = (T_grid - T_cont)/sqrt(Delta theta) in rho; 5% / 10% thresholds.  Output: compare.out."""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "tools"))
import discrete_ta as d

mc = json.load(open(os.path.join(HERE, "mc_discrete.json")))
print("== lattice vs independent MC (Bayes, world held after the switch)")
zs = []
for e in mc["bayes"]:
    if not e["hold"]:
        continue
    start = None if e["law"] == "switch" else "quiet"
    g = d.bayes_ta_grid(e["mu"], e["lam"], e["N"], e["Delta"], start=start)
    z = (e["t_A"] - g) / e["se_t"]; zs.append(z)
    print(f"{e['law']:6s} lam={e['lam']:<7g} N={e['N']:<5g} Delta={e['Delta']:<5g} MC {e['t_A']:.4f} +- {e['se_t']:.4f}"
          f"  lattice {g:.4f}  rel {e['t_A']/g-1:+.4f}  z {z:+.2f}")
zs = np.array(zs)
print(f"n={zs.size}  max|z|={np.abs(zs).max():.2f}  chi2={np.sum(zs**2):.1f} (df {zs.size})")
print("== definition sensitivity (MC): world NOT held after the switch")
for e in mc["bayes"]:
    if not e["hold"]:
        g = d.bayes_ta_grid(e["mu"], e["lam"], e["N"], e["Delta"])
        print(f"lam={e['lam']} N={e['N']} Delta={e['Delta']}: free {e['t_A']:.3f} +- {e['se_t']:.3f} vs held {g:.3f}")
print("== linear: closed form cosh(beta D) = cosh(aD) + rho sinh(aD) vs Riccati iteration (MC script)")
for e in mc["linear"]:
    cf = d.linear_ta_grid(e["mu"], e["lam"], e["N"], e["Delta"])
    ks = d.kalman_steady(e["mu"], e["lam"], e["N"], e["Delta"])
    print(f"lam={e['lam']} N={e['N']} D={e['Delta']}: closed {cf:.10f} iter {e['t_A_from_riccati_iteration']:.10f}"
          f"  pole closed {ks['pole']:.10f} iter {e['pole']:.10f}  P_post {ks['P_post']:.5f} emp MSE {e['mse_emp']:.5f}")
print("== linear ratio vs 1 + (1 - a^2 tau^2)^2/(24 r^2)")
for lam, D in [(1e-3, 3.0), (1e-3, 1.0), (1e-2, 0.5), (0.1, 1.0), (0.2, 2.0)]:
    tc = d.linear_ta_cont(1, lam, 1); tg = d.linear_ta_grid(1, lam, 1, D); r = tc / D; a = 2 * lam
    print(f"lam={lam} D={D} r={r:.3f} exact {tg/tc:.5f} series {1 + (1 - (a*tc)**2)**2/(24*r*r):.5f}")
print("== small-Delta asymptote: (T_grid - T_cont)/sqrt(Delta) -> C1 = %.4f (theta = 1)" % d.C1)
for kap in (1e-2, 1e-4):
    tc = d.bayes_ta_cont(1, kap, 1, h=5e-4)
    for D in (0.04, 0.01, 0.0025):
        sd = 2 * math.sqrt(D)
        vals = [(d.bayes_ta_grid(1, kap, 1, D, h=sd / f) - tc) / math.sqrt(D) for f in (8, 16)]
        rich = vals[1] + (vals[1] - vals[0]) / 3      # Richardson in h (O(h^2))
        print(f"kappa={kap} D={D}: g(h=sd/8) {vals[0]:.4f}  g(h=sd/16) {vals[1]:.4f}  Richardson {rich:.4f}"
              f"  C1 + 0.314 sqrt(D) = {d.C1 + 0.314*math.sqrt(D):.4f}")
print("== universality: g = (T_grid - T_cont)/sqrt(Delta theta) as a function of rho = mu^2 Delta/N, across kappa")
tab = json.load(open(os.path.join(HERE, "table.json")))
rhos = sorted({round(r["rho"], 6) for r in tab})
for kap in sorted({r["kappa"] for r in tab}, reverse=True):
    rr = [r for r in tab if r["kappa"] == kap]
    print(f"kappa={kap:g}: " + "  ".join(f"rho={r['rho']:.3g}:g={(r['grid_quiet']-r['cont_quiet'])/math.sqrt(r['rho']):.3f}" for r in rr))
print("== thresholds (from table.json, log-linear interpolation in r): smallest r_plugin beyond which the factor stays within")
for key in ("quiet_over_plugin", "switch_over_plugin", "quiet_over_cont"):
    for kap in sorted({r["kappa"] for r in tab}, reverse=True):
        rr = sorted([r for r in tab if r["kappa"] == kap], key=lambda r: r["r_plugin"])
        out = []
        for tol in (0.05, 0.10):
            ok = [abs(r[key] - 1) <= tol for r in rr]
            if not ok[-1]:
                out.append(f"{int(tol*100)}%: >500"); continue
            i = len(ok) - 1
            while i > 0 and ok[i - 1]:
                i -= 1
            if i == 0:
                out.append(f"{int(tol*100)}%: <=0.5"); continue
            a, b = rr[i - 1], rr[i]
            fa, fb = abs(a[key] - 1) - tol, abs(b[key] - 1) - tol
            x = math.exp(math.log(a["r_plugin"]) + (math.log(b["r_plugin"]) - math.log(a["r_plugin"])) * fa / (fa - fb))
            out.append(f"{int(tol*100)}%: r >= {x:.0f}")
        print(f"{key:18s} kappa={kap:g}: " + ", ".join(out))
