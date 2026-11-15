#!/usr/bin/env python3
"""SPF-NOISE-PROXY locked analysis on real SPF data (see PREREG.md). Run: nice -n 19 python3 analysis.py
Inputs: data/micro_<VAR>.csv (build_micro.py), ../LFK_SPF/data/target_<VAR>.csv and ../LFK_SPF/results/env.json
(environment fits and parametric draws, committed before LFK outcomes), ../LFK_SPF/results/outcome.json (consensus CG
coefficients, SEEN before this item: used only in the POST HOC secondary S4).
Outputs: results/analysis.json, results/analysis.out.
"""
import json, os, sys, itertools
import numpy as np, pandas as pd
import common, model, gtest
import synth_dryrun as sd

HERE = common.HERE
LFK = os.path.join(HERE, "..", "LFK_SPF")
SEED = 20261115 + 42
VARS7 = ["UNEMP", "HOUSING", "TBILL", "BOND", "TBOND", "RSLGOV", "INDPROD"]
PRICED = ["TBILL", "BOND", "TBOND"]
NONPRICED = ["UNEMP", "HOUSING", "RSLGOV", "INDPROD"]
ENV_START, END_Q = 1960 * 4, 2019 * 4 + 3
B_BOOT, BLOCK, NSIM = 500, 8, 200
MIN_N, MIN_SPELL = 10, 8

def env_series(v):
    t = pd.read_csv(os.path.join(LFK, "data", f"target_{v}.csv"))
    t = t[(t.q >= ENV_START) & (t.q <= END_Q)].dropna()
    assert np.all(np.diff(t.q.values) == 1)
    return t.x.values

def panel(v, h):
    m = pd.read_csv(os.path.join(os.environ.get("SPFNP_DATA", os.path.join(HERE, "data")), f"micro_{v}.csv"))
    m = m[m.h == h]
    F = m.pivot(index="survey_q", columns="id", values="f").sort_index()
    return F.values, ~np.isnan(F.values), F.index.values

def per_survey_D(F, act, within=False, sdmode=False):
    """Per-survey robust dispersion (IQR/1.349)^2 (or SD^2), surveys with >= MIN_N forecasters; within=True removes each
    forecaster's mean deviation from consensus (forecasters with >= MIN_SPELL surveys) first."""
    cons = np.nanmean(np.where(act, F, np.nan), axis=1)
    dev = F - cons[:, None]; nobs = act.sum(0)
    fe = np.array([np.nanmean(dev[act[:, i], i]) if nobs[i] else np.nan for i in range(F.shape[1])])
    D, keep = [], []
    for t in range(len(F)):
        a = act[t] & (nobs >= MIN_SPELL) if within else act[t]
        if a.sum() < MIN_N: continue
        z = (dev[t, a] - fe[a]) if within else F[t, a]
        D.append(np.var(z, ddof=1) if sdmode else common.rvar(z)); keep.append(t)
    return np.array(D), np.array(keep), cons

def block_idx(n, rng):
    nb = int(np.ceil(n / BLOCK)); s = rng.integers(0, n, nb)
    return np.concatenate([(k + np.arange(BLOCK)) % n for k in s])[:n]

def run_var(args):
    v, seed = args
    env = json.load(open(os.path.join(LFK, "results", "env.json")))
    lfk = json.load(open(os.path.join(LFK, "results", "outcome.json")))["table"]
    rng = np.random.default_rng(seed)
    if True:
        fit = {k: env[v]["fit"][k] for k in ("tauE", "alpha", "phi")}
        x = env_series(v)
        pan = {h: panel(v, h)[:2] for h in (0, 3)}
        k, aux = sd.proxies(pan, x, fit_override=fit)
        S, var_x, nf, T = aux["S"], aux["var_x"], aux["nf"], aux["T"]
        Kw = k["L0w"][0]
        bG = {c: common.beta_at(S, k[c][0], nf) for c in ("L0w", "L0", "P0", "P0T")}
        # uncertainty of the chosen proxy: block bootstrap over surveys x paired parametric environment draw
        Dw, keep_w, _ = per_survey_D(*pan[0], within=True)
        draws = env[v]["draws"]; Kb, Bb = [], []
        curves = []
        for e in draws:   # one curve per parametric environment draw (100), used cyclically
            Se = model.env_grid(e["tauE"], e["alpha"], e["phi"])
            curves.append((common.level_curve(Se, 0, nf), Se, common.env_scale(x, e)))
        for b in range(B_BOOT):
            idx = block_idx(len(Dw), rng)
            lc, Se, vx = curves[b % len(curves)]
            kb = common.invert_lower(lc, np.mean(Dw[idx]) / vx)[0]
            Kb.append(kb); Bb.append(common.beta_at(Se, kb, nf))
        # overidentification test of the white-noise premise at h=3 vs h=0
        G = float(np.log(k["L3"][0] / k["L0"][0]))
        null = gtest.null_G(fit, k["L0"][0], T, nf, NSIM, rng)
        p = gtest.pval(G, null)
        # robustness (no verdict): SD-based within dispersion
        Dw_sd, _, _ = per_survey_D(*pan[0], within=True, sdmode=True)
        K_sd = common.invert_lower(aux["l0"], np.mean(Dw_sd) / var_x)[0]
        r = dict(T=T, nf=nf, var_x=var_x, fit=fit,
                 K={c: k[c][0] for c in k}, K_flag={c: k[c][1] for c in k},
                 K_L0w_ci=[float(np.percentile(Kb, 2.5)), float(np.percentile(Kb, 97.5))],
                 beta_pred={c: float(bG[c]) for c in bG},
                 beta_pred_L0w_ci=[float(np.percentile(Bb, 2.5)), float(np.percentile(Bb, 97.5))],
                 G=G, G_null_mean=float(np.mean(null)), G_null_sd=float(np.std(null)), G_p=p,
                 K_L0w_sdmode=K_sd, N_L0w_data_units=Kw * var_x, q_hf_unit=env[v]["q_hf"],
                 memory_scale_Nq_L0w=float((Kw / env[v]["q_hf"]) ** (1 / fit["alpha"])),
                 memory_scale_Nq_LFK=lfk[v].get("memory_scale_Nq"),
                 beta_hat_LFK=lfk[v].get("beta"), beta_se_LFK=lfk[v].get("se"), LFK_excluded=lfk[v].get("excluded"),
                 beta_pred_LFK=lfk[v].get("beta_pred_GTAO"), K_LFK=lfk[v].get("K"),
                 beta_static_LFK=lfk[v].get("beta_pred_static"))
        line = (f"{v:8s} T={T} nf={nf:.0f} K: P0={k['P0'][0]:.3g} P0T={k['P0T'][0]:.3g} L3={k['L3'][0]:.3g}({k['L3'][1]}) "
                     f"L0={k['L0'][0]:.3g}({k['L0'][1]}) L0w={Kw:.3g}({k['L0w'][1]}) CI[{r['K_L0w_ci'][0]:.3g},{r['K_L0w_ci'][1]:.3g}] "
                     f"| G={G:+.2f} null {np.mean(null):+.2f}±{np.std(null):.2f} p={p:.3f}")
        print(line, flush=True)
        return v, r, line

def main():
    from multiprocessing import Pool
    with Pool(4) as pool:
        res = pool.map(run_var, [(v, SEED + i) for i, v in enumerate(VARS7)])
    out = {v: r for v, r, _ in res}; lines = [l for _, _, l in res]
    # T1 Holm
    ps = sorted((out[v]["G_p"], v) for v in VARS7); m = len(ps); holm = {}; run = 0
    for i, (pv, v) in enumerate(ps):
        run = max(run, min(1.0, (m - i) * pv)); holm[v] = run
    for v in VARS7: out[v]["G_p_holm"] = holm[v]
    # T2 known groups on G: difference of means, null-SD z (one-sided) + exact permutation p over all 3-vs-4 splits
    def gdiff(pr, npr): return np.mean([out[v]["G"] - out[v]["G_null_mean"] for v in pr]) - np.mean([out[v]["G"] - out[v]["G_null_mean"] for v in npr])
    d_obs = gdiff(PRICED, NONPRICED)
    se = np.sqrt(sum(out[v]["G_null_sd"] ** 2 for v in PRICED) / 9 + sum(out[v]["G_null_sd"] ** 2 for v in NONPRICED) / 16)
    from math import erf, sqrt
    z = d_obs / se; p_z = 0.5 * (1 - erf(z / sqrt(2)))
    perms = [gdiff(list(c), [u for u in VARS7 if u not in c]) for c in itertools.combinations(VARS7, 3)]
    p_perm = float(np.mean([d >= d_obs - 1e-12 for d in perms]))
    # T3 known groups on the chosen proxy: ln K_L0w lower for priced
    lk = {v: np.log(out[v]["K"]["L0w"]) for v in VARS7}
    kd_obs = np.mean([lk[v] for v in NONPRICED]) - np.mean([lk[v] for v in PRICED])
    kperms = [np.mean([lk[u] for u in VARS7 if u not in c]) - np.mean([lk[u] for u in c]) for c in itertools.combinations(VARS7, 3)]
    p_kperm = float(np.mean([d >= kd_obs - 1e-12 for d in kperms]))
    summ = dict(T2=dict(d_obs=float(d_obs), se=float(se), z=float(z), p_z=float(p_z), p_perm=p_perm, n_perm=len(perms)),
                T3=dict(d_lnK_nonpriced_minus_priced=float(kd_obs), p_perm=p_kperm))
    # S4 POST HOC (beta-hat seen): LFK six (E4 passers)
    six = [v for v in VARS7 if not out[v]["LFK_excluded"]]
    lg = lambda b: np.log(max(b, 0.02))
    mae = lambda key: float(np.mean([abs(lg(out[v]["beta_hat_LFK"]) - lg(key(v))) for v in six]))
    summ["S4_posthoc"] = dict(vars=six, MAE_L0w=mae(lambda v: out[v]["beta_pred"]["L0w"]), MAE_L0=mae(lambda v: out[v]["beta_pred"]["L0"]),
                              MAE_LFK_G=mae(lambda v: out[v]["beta_pred_LFK"]), MAE_static=mae(lambda v: out[v]["beta_static_LFK"]),
                              MAE_P0_repro=mae(lambda v: out[v]["beta_pred"]["P0"]),
                              locked_check_yields_below_0_5={v: out[v]["beta_pred"]["L0w"] < 0.5 for v in ("BOND", "TBOND")})
    res = dict(per_var=out, summary=summ)
    if os.environ.get("SPFNP_DATA"):   # fake-data code test: do not write real results
        print(json.dumps(summ, default=float)); return
    json.dump(res, open(os.path.join(HERE, "results", "analysis.json"), "w"), indent=1, default=float)
    lines.append(json.dumps(summ, indent=1, default=float))
    lines.append("per-variable beta (S4, post hoc): " + "; ".join(
        f"{v}: hat {out[v]['beta_hat_LFK']:.2f} | L0w {out[v]['beta_pred']['L0w']:.2f} [{out[v]['beta_pred_L0w_ci'][0]:.2f},{out[v]['beta_pred_L0w_ci'][1]:.2f}] | LFK {out[v]['beta_pred_LFK']:.2f}"
        for v in six))
    open(os.path.join(HERE, "results", "analysis.out"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines[len(VARS7):]))

if __name__ == "__main__":
    main()
