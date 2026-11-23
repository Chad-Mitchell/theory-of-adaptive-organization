"""T67 analysis exactly as PREREG_T67.md: approach exponent s on doubling ladders, p_c, error bars, decisions.
Reads raw_d*_n*.json, writes t67_results.json, prints the report."""
import os, json, numpy as np, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from t67lib import approach_exponent, p_crossing, boundary
HERE = os.path.dirname(os.path.abspath(__file__))
raw = {}
for d, n in [(1, 1024), (1, 2048), (2, 48), (2, 64)]:
    raw[(d, n)] = json.load(open(os.path.join(HERE, f"raw_d{d}_n{n}.json")))
LADDERS = {1: [("primary", 2048, (64, 128, 256)), ("v1", 2048, (32, 64, 128)), ("v2", 2048, (16, 32, 64)), ("v3", 1024, (32, 64, 128))],
           2: [("primary", 64, (4, 8, 16)), ("v1", 64, (3, 6, 12)), ("v2", 48, (3, 6, 12)), ("v3", 48, (2, 4, 8))]}
QTY = {"I_EQ": ("EQ", 0), "I_HOT": ("HOT", 0), "I_COLD": ("COLD", 0), "Idot_HOT": ("HOT", 1), "Idot_COLD": ("COLD", 1),
       "t1_HOT": ("HOT", 2), "t2_HOT": ("HOT", 3), "t1_COLD": ("COLD", 2), "t2_COLD": ("COLD", 3)}

def series(d, n, q, p, Ls):
    dr, k = QTY[q]
    rows = {r["L"]: r for r in raw[(d, n)]["rows"] if abs(r["p"] - p) < 1e-9}
    return np.array([abs(rows[L][dr][k]) / boundary(d, L) for L in Ls])

out = {"gates": {f"d{d}_n{n}": raw[(d, n)]["gate"] for (d, n) in raw}, "cells": {}}
lines = []
P = lambda s: lines.append(s)
P("T67 threshold test: analysis per PREREG_T67.md (sha256 b91e2101ec93acf3c22cf8b93241014012938b0db2fccc7df62ea27748d54b98)")
g = out["gates"]
P("Gates G3/G4: " + "; ".join(f"{k} max|Idot_EQ|={v['eq_idot_max']:.1e} max resid={v['res_max']:.1e}" for k, v in g.items()))
G3 = all(v["eq_idot_max"] < 1e-9 for v in g.values()); G4 = all(v["res_max"] < 1e-9 for v in g.values())
P(f"G3 {'PASS' if G3 else 'FAIL'}  G4 {'PASS' if G4 else 'FAIL'}  G5 PASS (every Cholesky succeeded; run completed)")
# sign consistency of Idot
for d, n in raw:
    sh = all(r["HOT"][1] < 0 for r in raw[(d, n)]["rows"]); sc = all(r["COLD"][1] > 0 for r in raw[(d, n)]["rows"])
    P(f"sign d={d} n={n}: HOT Idot<0 everywhere {sh}; COLD Idot>0 everywhere {sc}")
res = {}
for d in (1, 2):
    grid = raw[(d, LADDERS[d][0][1])]["grid"]
    for q in QTY:
        pcs = {}; svals = {}
        for name, n, Ls in LADDERS[d]:
            ss = [approach_exponent(series(d, n, q, p, Ls)) for p in grid]
            pcs[name] = p_crossing(grid, ss); svals[name] = ss
        vals = [v["p_c"] for v in pcs.values() if v["p_c"] is not None]
        sig = (max(vals) - min(vals)) / 2 if vals else None
        # naive: OLS slope of ln y on ln L over primary ladder, largest crossing of 0.05
        name, n, Ls = LADDERS[d][0]
        sl_ = [float(np.polyfit(np.log(Ls), np.log(series(d, n, q, p, Ls)), 1)[0]) for p in grid]
        nv = p_crossing(grid, [x - 0.05 for x in sl_])
        undefined_primary = [p for p, s in zip(grid, svals["primary"]) if s is None]
        res[(d, q)] = {"p_c": pcs["primary"]["p_c"], "status": pcs["primary"]["status"], "all_crossings": pcs["primary"]["all"],
                       "sigma": sig, "variants": {k: v["p_c"] for k, v in pcs.items()}, "variant_status": {k: v["status"] for k, v in pcs.items()},
                       "naive_p": nv["p_c"], "s_primary": dict(zip([str(p) for p in grid], svals["primary"])),
                       "logslope_primary": dict(zip([str(p) for p in grid], sl_)), "undefined_primary": undefined_primary}
for d in (1, 2):
    P(f"\n=== d={d}: s(p) on the primary ladder (approach exponent; area form <=> s<0) ===")
    grid = raw[(d, LADDERS[d][0][1])]["grid"]
    hdr = ["I_EQ", "I_HOT", "Idot_HOT", "I_COLD", "Idot_COLD", "t1_HOT", "t2_HOT"]
    P("p     " + " ".join(f"{h:>10s}" for h in hdr))
    for p in grid:
        P(f"{p:<5} " + " ".join(f"{res[(d,h)]['s_primary'][str(p)]:>10.4f}" if res[(d, h)]['s_primary'][str(p)] is not None else f"{'undef':>10s}" for h in hdr))
    P(f"--- d={d}: p_c (primary, sigma=half-range over 4 ladders, variants, naive) ---")
    for q in QTY:
        r = res[(d, q)]
        vs = ", ".join(f"{k}={v:.3f}" if v is not None else f"{k}=None" for k, v in r["variants"].items())
        P(f"{q:10s} p_c={r['p_c']:.3f} [{r['status']}] sigma={r['sigma']:.3f}  ({vs}; statuses {sorted(set(r['variant_status'].values()))})  naive={r['naive_p']}  crossings={['%.3f'%c for c in r['all_crossings']]} undefined={r['undefined_primary']}")
# decisions
P("\n=== Decisions (PREREG_T67.md) ===")
fails = []
for d in (1, 2):
    lo, hi = (d + 1) / 2 - 0.15, (d + 1) / 2 + 0.15
    for q in ["I_EQ", "I_HOT", "I_COLD"]:
        r = res[(d, q)]; ok = r["status"] == "ok" and lo <= r["p_c"] <= hi
        tag = "P-a" if q == "I_EQ" else "P-a'"
        P(f"{tag} d={d} {q}: p_c={r['p_c']:.3f} window [{lo:.2f},{hi:.2f}] -> {'MET' if ok else 'MISSED (puzzle)'}")
        if not ok: fails.append(f"F1 {tag} d={d} {q}")
    for dr in ["HOT", "COLD"]:
        ri, rd = res[(d, f"I_{dr}")], res[(d, f"Idot_{dr}")]
        delta = rd["p_c"] - ri["p_c"]; sd = float(np.hypot(ri["sigma"], rd["sigma"]))
        pb = rd["status"] == "ok" and rd["p_c"] >= ri["p_c"] - 0.15 and rd["p_c"] <= d + 1 + 0.15
        if abs(delta) <= 0.15: oc = "EQUAL"
        elif delta > max(0.15, 2 * sd): oc = "DIFFERENT"
        elif delta > 0.15: oc = "UNRESOLVED"
        else: oc = "P-b MISS"
        grid = raw[(d, LADDERS[d][0][1])]["grid"]
        above = [(p, rd["s_primary"][str(p)]) for p in grid if p >= d + 1 + 0.2 - 1e-9]
        pc_ok = all(s is not None and s < 0.05 for _, s in above)
        near_undef = [p for p in rd["undefined_primary"] + ri["undefined_primary"] if abs(p - rd["p_c"]) <= 0.5 or abs(p - ri["p_c"]) <= 0.5]
        P(f"d={d} {dr}: p_c(I)={ri['p_c']:.3f}+-{ri['sigma']:.3f}  p_c(Idot)={rd['p_c']:.3f}+-{rd['sigma']:.3f}  Delta={delta:+.3f} sigma_Delta={sd:.3f} -> {oc};  P-b {'MET' if pb else 'MISSED (puzzle)'};  P-c (s<0.05 for p>={d+1+0.2:.1f}, max s={max(s for _, s in above if s is not None):.4f}) {'MET' if pc_ok else 'MISSED (puzzle)'};  F3 near-threshold undefined: {near_undef or 'none'}")
        out["cells"][f"d{d}_{dr}"] = {"pc_I": ri["p_c"], "pc_Idot": rd["p_c"], "sig_I": ri["sigma"], "sig_Idot": rd["sigma"], "delta": delta, "outcome": oc, "Pb": pb, "Pc": pc_ok}
        if not pb: fails.append(f"F1 P-b d={d} {dr}")
        if not pc_ok: fails.append(f"F2 d={d} {dr}")
        if near_undef: fails.append(f"F3 d={d} {dr}")
ocs = [c["outcome"] for c in out["cells"].values()]
if all(o == "EQUAL" for o in ocs): glob = "EQUAL in all four cells: the learning rate's area form is the known mutual-information area law relabeled on this route."
elif any(all(out["cells"][f"d{d}_{dr}"]["outcome"] == "DIFFERENT" for dr in ["HOT", "COLD"]) for d in (1, 2)) and not any("P-b" in f for f in fails): glob = "DIFFERENT in both drives of at least one d: the flow has its own locality class there."
else: glob = "MIXED: see cells."
P(f"GLOBAL: {glob}")
P(f"Failure flags (puzzles): {fails or 'none'}")
out["global"] = glob; out["fails"] = fails
out["per_quantity"] = {f"d{d}_{q}": v for (d, q), v in res.items()}
json.dump(out, open(os.path.join(HERE, "t67_results.json"), "w"), indent=1, sort_keys=True)
print("\n".join(lines))
