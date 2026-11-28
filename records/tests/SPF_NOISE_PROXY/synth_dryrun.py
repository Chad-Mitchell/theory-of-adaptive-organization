#!/usr/bin/env python3
"""SPF-NOISE-PROXY pre-lock dry run on synthetic truth. No real SPF dispersion is read here.

Worlds: the 7 LFK-ALPHA-SPF environments that passed gates E1-E3 (point fits, ../LFK_SPF/results/env.json; environment
stage, not an outcome), each with that variable's LFK survey count T (env.json n_pairs) and n_env = 240 quarters of
environment series ending at the panel's last survey. True K ~ logUniform[0.01, 1].
For every panel the environment is RE-FITTED by Whittle from the synthetic environment series (as on real data), and the
variance scale is estimated from it (common.env_scale), so estimation error of the environment is included.
Arms: a pure noise; b fixed individual bias (lam = 1, 3); c heterogeneous dynamics (tauE*exp(0.5z)); d AR(1) bias (lam 1, 3).
Candidates (K-hat from):
  P0  h=3, D / population consensus variance (LFK-ALPHA-SPF proxy, as run)
  P0T h=3, D / expected finite-sample consensus variance over T surveys
  P1T h=0, same finite-sample correction
  L3  h=3, D / env-implied population variance of x (level-normalised; lower branch)
  L0  h=0, level-normalised
  L0w h=0, within-forecaster (fixed effects removed) dispersion, level-normalised
Overidentification: G = ln K-hat_L3 - ln K-hat_L0 (noise model: 0), circular block bootstrap CI over surveys (block 8, 200).
Usage: nice -n 19 python3 synth_dryrun.py REPS
"""
import json, sys, os, collections
import numpy as np
import common, model

SEED = 20261115 + 40
VARS7 = ["UNEMP", "HOUSING", "TBILL", "BOND", "TBOND", "RSLGOV", "INDPROD"]
ARMS = [("a", 0.0), ("b", 1.0), ("b", 3.0), ("c", 0.0), ("d", 1.0), ("d", 3.0)]
CANDS = ["P0", "P0T", "P1T", "L3", "L0", "L0w"]
BLOCK, NB = 8, 200

def per_survey(F, act, min_n=10):
    cons = np.nanmean(np.where(act, F, np.nan), axis=1)
    D = np.array([common.rvar(F[t, act[t]]) if act[t].sum() >= min_n else np.nan for t in range(len(F))])
    ok = ~np.isnan(D)
    return D[ok], cons[ok]

def boot_GL(D0, D3, l0, l3, var_x, rng):
    T = len(D0); nb = int(np.ceil(T / BLOCK)); out = []
    for _ in range(NB):
        s = rng.integers(0, T, nb); idx = np.concatenate([(k + np.arange(BLOCK)) % T for k in s])[:T]
        k0 = common.invert_lower(l0, np.mean(D0[idx]) / var_x)[0]
        k3 = common.invert_lower(l3, np.mean(D3[idx]) / var_x)[0]
        out.append(np.log(k3 / k0))
    return np.array(out)

def proxies(pan, xenv, fit_override=None):
    fit = fit_override or model.whittle_fit(xenv)
    var_x = common.env_scale(xenv, fit)
    S = model.env_grid(fit["tauE"], fit["alpha"], fit["phi"])
    st = {h: common.panel_stats(*pan[h], h) for h in (0, 3)}
    nf, T = st[0]["nf"], st[0]["n"]
    c3p = common.ratio_curve(S, 3, nf)
    c0, c3 = common.ratio_curve(S, 0, nf, T), common.ratio_curve(S, 3, nf, T)
    l0, l3 = common.level_curve(S, 0, nf), common.level_curve(S, 3, nf)
    k = {"P0": common.invert(c3p, st[3]["D_raw"] / st[3]["vf"]),
         "P0T": common.invert(c3, st[3]["D_raw"] / st[3]["vf"]),
         "P1T": common.invert(c0, st[0]["D_raw"] / st[0]["vf"]),
         "L3": common.invert_lower(l3, st[3]["D_raw"] / var_x),
         "L0": common.invert_lower(l0, st[0]["D_raw"] / var_x),
         "L0w": common.invert_lower(l0, st[0]["D_within"] / var_x)}
    return k, dict(fit=fit, var_x=var_x, S=S, nf=nf, T=T, l0=l0, l3=l3, st=st)

def run_var(args):
    v, reps, seed = args
    env = json.load(open(os.path.join(common.HERE, "..", "LFK_SPF", "results", "env.json")))
    rng = np.random.default_rng(seed)
    e = env[v]["fit"]; T = int(env[v]["n_pairs"])
    rows = []
    for arm, lam in ARMS:
        for r in range(reps):
            K = float(np.exp(rng.uniform(np.log(0.01), np.log(1.0))))
            pan, xenv = common.synth_panel(e, K, arm, lam, rng, T=T)
            k, aux = proxies(pan, xenv)
            D0, _ = per_survey(*pan[0]); D3, _ = per_survey(*pan[3])
            bd = boot_GL(D0, D3, aux["l0"], aux["l3"], aux["var_x"], rng)
            lo, hi = np.percentile(bd, [2.5, 97.5])
            row = dict(var=v, arm=arm, lam=lam, K=K, T=aux["T"], fit=aux["fit"], var_x=aux["var_x"],
                       G=float(np.log(k["L3"][0] / k["L0"][0])), G_lo=float(lo), G_hi=float(hi))
            for c in CANDS:
                row[c] = float(np.log(k[c][0] / K)); row[c + "_flag"] = k[c][1]
            rows.append(row)
    return rows

def summarize(rows, path):
    out = []
    g = collections.defaultdict(list)
    for r in rows: g[(r["arm"], r["lam"])].append(r)
    out.append("Median |ln Khat/K| (median signed ln Khat/K) by arm; G = ln Khat_L3 - ln Khat_L0: median, share CI>0, share CI<0")
    out.append("arm lam   n  " + "  ".join(f"{c:>13s}" for c in CANDS) + "   G")
    for k in sorted(g):
        rs = g[k]
        cells = [f"{np.median([abs(r[c]) for r in rs]):5.2f}({np.median([r[c] for r in rs]):+5.2f})" for c in CANDS]
        out.append(f"{k[0]}  {k[1]:3.0f}  {len(rs):3d}  " + "  ".join(f"{x:>13s}" for x in cells) +
                   f"   {np.median([r['G'] for r in rs]):+.2f} {np.mean([r['G_lo'] > 0 for r in rs]):.2f} {np.mean([r['G_hi'] < 0 for r in rs]):.2f}")
    out.append("\nArm a by world: median signed ln Khat/K per candidate; share of above_noise_max flags (L3, L0)")
    for v in VARS7:
        rs = [r for r in rows if r["var"] == v and r["arm"] == "a"]
        if not rs: continue
        out.append(f"{v:8s} " + " ".join(f"{c}={np.median([r[c] for r in rs]):+.2f}" for c in CANDS) +
                   f"  flagsL3={np.mean([r['L3_flag'] != 'ok' for r in rs]):.2f} flagsL0={np.mean([r['L0_flag'] != 'ok' for r in rs]):.2f}"
                   f"  G CI>0 {np.mean([r['G_lo'] > 0 for r in rs]):.2f}")
    # locked selection rule (also written in PREREG): admissible if arm-a median |err| <= 0.35 and |median signed| <= 0.25;
    # choose the admissible candidate with the smallest max over contamination arms of median |err|.
    adm = {}
    for c in CANDS[1:]:
        ra = g[("a", 0.0)]
        e_abs = np.median([abs(r[c]) for r in ra]); e_sig = np.median([r[c] for r in ra])
        worst = max(np.median([abs(r[c]) for r in g[k]]) for k in g if k != ("a", 0.0))
        adm[c] = dict(arm_a_abs=float(e_abs), arm_a_signed=float(e_sig), worst_contaminated=float(worst),
                      admissible=bool(e_abs <= 0.35 and abs(e_sig) <= 0.25))
    ok = [c for c in adm if adm[c]["admissible"]]
    choice = min(ok, key=lambda c: adm[c]["worst_contaminated"]) if ok else None
    out.append("\nSelection (P0 excluded as status quo): " + json.dumps(adm))
    out.append(f"CHOSEN PROXY: {choice}")
    txt = "\n".join(out); print(txt)
    open(path, "w").write(txt + "\n")
    return choice

def main(reps):
    from multiprocessing import Pool
    with Pool(4) as p:
        res = p.map(run_var, [(v, reps, SEED + i) for i, v in enumerate(VARS7)])
    rows = [r for rr in res for r in rr]
    json.dump(rows, open(os.path.join(common.HERE, "results", "synth_dryrun.json"), "w"))
    summarize(rows, os.path.join(common.HERE, "results", "synth_dryrun.out"))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 2)
