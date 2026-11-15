#!/usr/bin/env python3
"""SPF-RIGIDITY-OOS pre-lock stage (NO outcome: no actual-minus-forecast error and no CG regression on real data).
Per unseen candidate variable: measured nowcast noise K_L0w (SPF-NOISE-PROXY instrument, validated on synthetic truth),
optimal-noisy-filter CG coefficient beta^G (population and its expectation at the planned n), its uncertainty
(parametric environment draws x block bootstrap of nowcast dispersion), and the planned sampling sd of beta-hat under
the model (consensus simulated from the fitted world). Also an in-model validation: simulated beta-hat at very large n
must match the closed-form beta (model.moments).
Run: nice -n 19 python3 prelock.py  -> results/prelock.json, results/prelock.out"""
import json, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
NP = os.path.join(HERE, "..", "SPF_NOISE_PROXY"); LFK = os.path.join(HERE, "..", "LFK_SPF")
sys.path.insert(0, NP); sys.path.insert(0, LFK)
import model, common
import synth_dryrun as sd

CAND = ["NGDP", "PGDP", "CPROF", "RGDP", "RCONSUM", "RNRESIN", "RRESINV", "RFEDGOV", "CPI"]
SEED = 20261115 + 98
ENV_START, END_Q = 1960 * 4, 2019 * 4 + 3
N_DRAWS, BLOCK, NSIM, NBIG = 200, 8, 2000, 20000
IMP, BURN = 3000, 6000

def env_series(v):
    t = pd.read_csv(os.path.join(LFK, "data", f"target_{v}.csv"))
    t = t[(t.q >= ENV_START) & (t.q <= END_Q)].dropna(); assert np.all(np.diff(t.q.values) == 1)
    return t.x.values

def panel(v, h):
    m = pd.read_csv(os.path.join(HERE, "data", f"micro_{v}.csv")); m = m[m.h == h]
    F = m.pivot(index="survey_q", columns="id", values="f").sort_index()
    return F.values, ~np.isnan(F.values)

def within_D(F, act, min_n=10, min_spell=8):
    cons = np.nanmean(np.where(act, F, np.nan), axis=1); dev = F - cons[:, None]; nobs = act.sum(0)
    fe = np.array([np.nanmean(dev[act[:, i], i]) if nobs[i] else np.nan for i in range(F.shape[1])])
    D = []
    for t in range(len(F)):
        a = act[t] & (nobs >= min_spell)
        if a.sum() >= min_n: D.append(common.rvar(dev[t, a] - fe[a]))
    return np.array(D)

def sim_cg(fit, K, nf, n, nsim, rng):
    """CG beta-hat (OLS with intercept, as LFK nw_ols point estimate) of a simulated consensus: F_t = H3*(x+vbar)(t),
    F_{t-1}(x_{t+3}) = H4*(x+vbar)(t-1); err = x_{t+3}-F_t, rev = F_t - F_{t-1}. Unit-variance x; vbar white, var K/nf."""
    S = model.env_grid(fit["tauE"], fit["alpha"], fit["phi"])
    H3, H4 = model.filters(S, K, 3)
    g3, g4 = common.impulse(H3, IMP), common.impulse(H4, IMP)
    Su = model.spectrum(np.abs(model._Wsym), fit["tauE"], fit["alpha"], fit["phi"]); sc = np.sqrt(np.mean(Su))
    out = []
    L = n + BURN + 8
    for _ in range(nsim):
        x = model.simulate(L, fit["tauE"], fit["alpha"], fit["phi"], rng) / sc
        y = x + rng.standard_normal(L) * np.sqrt(K / nf)
        f3 = common.causal_filter(g3, y); f4 = common.causal_filter(g4, y)
        t = np.arange(BURN, BURN + n)
        err = x[t + 3] - f3[t]; rev = f3[t] - f4[t - 1]
        X = np.column_stack([np.ones(n), rev]); out.append(np.linalg.lstsq(X, err, rcond=None)[0][1])
    return np.array(out)

def run(v):
    rng = np.random.default_rng(SEED + CAND.index(v))
    env = json.load(open(os.path.join(LFK, "results", "env.json")))[v]
    fit = {k: env["fit"][k] for k in ("tauE", "alpha", "phi")}
    x = env_series(v)
    pan = {h: panel(v, h) for h in (0, 3)}
    k, aux = sd.proxies(pan, x, fit_override=fit)
    S, nf, var_x = aux["S"], aux["nf"], aux["var_x"]
    K, flag = k["L0w"]
    bpop = model.moments(S, K, h=3, nf=nf)[0]
    G = float(np.log(k["L3"][0] / k["L0"][0]))           # horizon diagnostic (no test here)
    n = int(env["n_pairs"])
    # in-model validation and planned-n distribution
    big = sim_cg(fit, K, nf, NBIG, 20, rng)
    sims = sim_cg(fit, K, nf, n, NSIM, rng)
    # beta^G uncertainty: parametric environment draw x block bootstrap of within nowcast dispersion
    Dw = within_D(*pan[0]); bb, kb = [], []
    for b in range(N_DRAWS):
        xs = model.simulate(len(x), fit["tauE"], fit["alpha"], fit["phi"], rng)
        e = model.whittle_fit(xs, starts=[(np.log(fit["tauE"]), fit["alpha"], fit["phi"]), (np.log(2), 2.0, 0.3)])
        Se = model.env_grid(e["tauE"], e["alpha"], e["phi"])
        nb = int(np.ceil(len(Dw) / BLOCK)); s = rng.integers(0, len(Dw), nb)
        idx = np.concatenate([(j + np.arange(BLOCK)) % len(Dw) for j in s])[:len(Dw)]
        Kb = common.invert_lower(common.level_curve(Se, 0, nf), np.mean(Dw[idx]) / common.env_scale(x, e))[0]
        kb.append(Kb); bb.append(model.moments(Se, Kb, h=3, nf=nf)[0])
    bb = np.array(bb)
    r = dict(var=v, n_pairs=n, nf=nf, T_nowcast=aux["T"], fit=fit, var_x=var_x, K_L0w=K, K_flag=flag,
             K_ci=[float(np.percentile(kb, 2.5)), float(np.percentile(kb, 97.5))],
             K_other={c: k[c][0] for c in k}, G_L3_L0=G,
             beta_pop=bpop, beta_sim_big_mean=float(big.mean()),
             beta_planned_mean=float(sims.mean()), beta_planned_sd=float(sims.std(ddof=1)),
             beta_G_draws=bb.tolist(),
             beta_G_ci=[float(np.percentile(bb, 2.5)), float(np.percentile(bb, 97.5))])
    line = (f"{v:8s} n={n} nf={nf:.0f} K_L0w={K:.3g}({flag}) [{r['K_ci'][0]:.3g},{r['K_ci'][1]:.3g}] G={G:+.2f} | "
            f"beta^G pop {bpop:.3f} bigN-sim {big.mean():.3f} planned-n mean {sims.mean():.3f} sd {sims.std(ddof=1):.3f} | "
            f"beta^G CI [{r['beta_G_ci'][0]:.3f},{r['beta_G_ci'][1]:.3f}]")
    print(line, flush=True)
    return r, line

if __name__ == "__main__":
    from multiprocessing import Pool
    vs = sys.argv[1:] or CAND
    with Pool(min(4, len(vs))) as p:
        res = p.map(run, vs)
    if len(vs) == len(CAND):
        json.dump({r["var"]: r for r, _ in res}, open(os.path.join(HERE, "results", "prelock.json"), "w"), indent=1)
        open(os.path.join(HERE, "results", "prelock.out"), "w").write("\n".join(l for _, l in res) + "\n")
