#!/usr/bin/env python3
"""LFK-ALPHA-SPF analysis (locked with PREREG.md). Stages:
  python3 analysis.py env      -> results/env.json      (environment only: Whittle fits, gates E2/E3, parametric draws)
  python3 analysis.py outcome  -> results/outcome.json  (SPF moments, predictions, bootstrap, verdict)
Seeds: numpy default_rng(20261115 + stage offset). nice -n 19.
"""
import json, os, sys
import numpy as np, pandas as pd
import model
from build_data import VARS, RAW

HERE = os.path.dirname(os.path.abspath(__file__))
DATA, RES = os.path.join(HERE, "data"), os.path.join(HERE, "results")
SEED = 20261115
CANDIDATES = [v for v in VARS]                    # RCBI, REXPORT excluded a priori (build_data.py)
ENV_START, END_Q = 1960 * 4, 2019 * 4 + 3         # environment sample 1960Q1-2019Q4; targets <= 2019Q4
N_ENV_DRAWS, N_SPF_DRAWS, B = 100, 100, 2000
BLOCK = 8
FLOOR = 0.02
MIN_PAIRS = 80
MIN_FORECASTERS = 10
MAX_SE = 0.5                                      # gate E4: CG coefficient must be estimable

def env_series(v, start=ENV_START, end=END_Q):
    t = pd.read_csv(os.path.join(DATA, f"target_{v}.csv"))
    t = t[(t.q >= start) & (t.q <= end)].dropna()
    q = t.q.values
    assert np.all(np.diff(q) == 1), f"gap in {v}"
    return t.x.values

def spf_frame(v, end=END_Q, start=None):
    p = pd.read_csv(os.path.join(DATA, f"spf_{v}.csv")).dropna(subset=["F_t", "F_tm1", "actual"])
    p = p[p.target_q <= end]
    if start is not None: p = p[p.survey_q >= start]
    return p

def micro_dispersion(v):
    """Per survey quarter: robust cross-sectional variance (IQR/1.349)^2 of individual forecasts of target t+3."""
    cache = os.path.join(DATA, f"disp_{v}.csv")
    if os.path.exists(cache): return pd.read_csv(cache)
    d = pd.read_excel(os.path.join(RAW, "SPFmicrodata.xlsx"), sheet_name=v, engine="calamine")
    kind = VARS[v][0]
    x5 = pd.to_numeric(d[f"{v}5"], errors="coerce"); x4 = pd.to_numeric(d[f"{v}4"], errors="coerce")
    f = x5 if kind in ("level", "rate") else 100 * ((x5 / x4) ** 4 - 1)
    df = pd.DataFrame({"survey_q": (d.YEAR * 4 + d.QUARTER - 1).astype(int), "f": f}).dropna()
    g = df.groupby("survey_q")["f"]
    out = pd.DataFrame({"n": g.count(), "iqr": g.quantile(0.75) - g.quantile(0.25), "sd": g.std()}).reset_index()
    out["rvar"] = (out.iqr / 1.349) ** 2
    out.to_csv(cache, index=False)
    return out

def nw_ols(y, x, lags=4):
    X = np.column_stack([np.ones_like(x), x]); n = len(y)
    b = np.linalg.lstsq(X, y, rcond=None)[0]; u = y - X @ b
    Xu = X * u[:, None]; S = Xu.T @ Xu
    for l in range(1, lags + 1):
        w = 1 - l / (lags + 1); G = Xu[l:].T @ Xu[:-l]; S += w * (G + G.T)
    XtXi = np.linalg.inv(X.T @ X); V = XtXi @ S @ XtXi
    return b[1], float(np.sqrt(V[1, 1]))

def spf_moments(p, disp, dmode="rvar"):
    m = p.merge(disp, on="survey_q", how="inner")
    m = m[m.n >= MIN_FORECASTERS]
    err = (m.actual - m.F_t).values; rev = (m.F_t - m.F_tm1).values
    beta, se = nw_ols(err, rev)
    D = float(np.mean(m[dmode] if dmode == "rvar" else m.sd ** 2)); vf = float(np.var(m.F_t.values))
    return dict(beta=float(beta), se=se, D=D, vf=vf, ratio=D / vf, n=int(len(m)), nf=float(np.median(m.n))), m

def block_boot(m, rng, reps, dmode="rvar"):
    n = len(m); out = []
    err = (m.actual - m.F_t).values; rev = (m.F_t - m.F_tm1).values
    Dv = (m[dmode] if dmode == "rvar" else m.sd ** 2).values; F = m.F_t.values
    nb = int(np.ceil(n / BLOCK))
    for _ in range(reps):
        st = rng.integers(0, n, nb); idx = np.concatenate([(s + np.arange(BLOCK)) % n for s in st])[:n]
        X = np.column_stack([np.ones(n), rev[idx]]); b = np.linalg.lstsq(X, err[idx], rcond=None)[0][1]
        out.append((float(b), float(np.mean(Dv[idx]) / np.var(F[idx]))))
    return out

def q_hf(th):
    """High-frequency level q of the unit-variance world: (1-phi) c_a tauE^(1-alpha) (S ~ q |w|^-alpha)."""
    from scipy.special import beta as Bf
    ca = 2 * np.pi / Bf(0.5, (th["alpha"] - 1) / 2)
    return (1 - th["phi"]) * ca * th["tauE"] ** (1 - th["alpha"])

def whittle_fixed_alpha(x, alpha=2.0):
    w, I = model.periodogram(x)
    from scipy.optimize import minimize
    def nll(p):
        tau = np.exp(np.clip(p[0], *model.BOUNDS["logtau"])); ph = np.clip(p[1], 0, 0.98)
        S = model.spectrum(w, tau, alpha, ph); s2 = np.mean(I / S)
        return np.sum(np.log(s2 * S)) + 1e3 * ((p[1] - ph) ** 2)
    best = min((minimize(nll, np.array([lt, ph]), method="Nelder-Mead") for lt in np.log([0.7, 4, 25, 150]) for ph in (0.1, 0.5)),
               key=lambda r: r.fun)
    return dict(tauE=float(np.exp(np.clip(best.x[0], *model.BOUNDS["logtau"]))), alpha=alpha, phi=float(np.clip(best.x[1], 0, 0.98)))

# ---------------- stage 1: environment ----------------
def stage_env():
    rng = np.random.default_rng(SEED + 1)
    out = {}
    for v in CANDIDATES:
        p = spf_frame(v); disp = micro_dispersion(v)
        npairs = int(len(p.merge(disp[disp.n >= MIN_FORECASTERS], on="survey_q")))
        x = env_series(v)
        th = model.whittle_fit(x); thM = whittle_fixed_alpha(x)
        r = dict(n_env=len(x), n_pairs=npairs, fit=th, fit_alpha2=thM, q_hf=q_hf(th))
        r["E1"] = npairs >= MIN_PAIRS
        r["E2"] = 1.05 < th["alpha"] < 5.9
        r["E3"] = th["tauE"] < len(x) / 4
        r["included"] = bool(r["E1"] and r["E2"] and r["E3"])
        if r["included"]:
            draws, drawsM = [], []
            for _ in range(N_ENV_DRAWS):
                xs = model.simulate(len(x), th["tauE"], th["alpha"], th["phi"], rng)
                draws.append(model.whittle_fit(xs, starts=[(np.log(th["tauE"]), th["alpha"], th["phi"]), (np.log(2), 2.0, 0.3)]))
                xsM = model.simulate(len(x), thM["tauE"], 2.0, thM["phi"], rng)
                drawsM.append(whittle_fixed_alpha(xsM))
            r["draws"], r["draws_alpha2"] = draws, drawsM
            # robustness: environment from pre-1990 data only (look-ahead check)
            r["fit_pre1990"] = model.whittle_fit(env_series(v, end=1989 * 4 + 3)) if len(env_series(v, end=1989 * 4 + 3)) > 60 else None
        out[v] = r
        print(f"{v:8s} n_env={len(x)} pairs={npairs} tauE={th['tauE']:.2f} alpha={th['alpha']:.2f} phi={th['phi']:.2f} "
              f"E1={r['E1']} E2={r['E2']} E3={r['E3']} included={r['included']}", flush=True)
    os.makedirs(RES, exist_ok=True)
    json.dump(out, open(os.path.join(RES, "env.json"), "w"), indent=1)

# ---------------- stage 2: outcome ----------------
def predict(th, ratio, nf):
    S = model.env_grid(th["tauE"], th["alpha"], th["phi"])
    K, flag = model.invert_ratio(S, ratio, nf=nf)
    return model.moments(S, K, nf=nf)[0], K, flag

def lg(b): return np.log(np.maximum(b, FLOOR))

def evaluate(per, rng):
    """per: dict v -> dict(beta, draws list of (beta*, G*, S*, M*)), point preds. Returns metrics with bootstrap CIs."""
    vs = sorted(per); n = len(vs)
    def metrics(bh, G, St, Mk):
        bh, G, St, Mk = map(np.asarray, (bh, G, St, Mk))
        # leave-one-out null: median of the other variables' betas
        Nl = np.array([np.median(np.delete(bh, i)) for i in range(len(bh))])
        e = lambda P: np.mean(np.abs(lg(bh) - lg(P)))
        X = lg(G); slope = np.polyfit(X, lg(bh), 1)[0] if np.ptp(X) > 0 else np.nan
        return dict(MAE_G=e(G), MAE_S=e(St), MAE_M=e(Mk), MAE_N=e(Nl), slope=slope)
    pt = metrics([per[v]["beta"] for v in vs], [per[v]["G"] for v in vs], [per[v]["S"] for v in vs], [per[v]["M"] for v in vs])
    bs = []
    for _ in range(B):
        idx = rng.integers(0, n, n); rows = []
        for i in idx:
            d = per[vs[i]]["draws"][rng.integers(0, len(per[vs[i]]["draws"]))]; rows.append(d)
        r = np.array(rows)
        if np.ptp(r[:, 1]) == 0: continue
        m = metrics(r[:, 0], r[:, 1], r[:, 2], r[:, 3])
        bs.append([m["MAE_G"] - m["MAE_S"], m["MAE_G"] - m["MAE_N"], m["MAE_G"] - m["MAE_M"], m["slope"]])
    bs = np.array(bs)
    ci = lambda c: [float(np.percentile(bs[:, c], 2.5)), float(np.percentile(bs[:, c], 97.5))]
    res = dict(point={k: float(v) for k, v in pt.items()}, n_vars=n,
               dGS=ci(0), dGN=ci(1), dGM=ci(2), slope_ci=ci(3), n_boot=int(len(bs)))
    return res

def verdict(res, n_nonpos, n):
    if n < 8: return "INCONCLUSIVE (fewer than 8 variables)"
    if n_nonpos > n / 3: return "INCONCLUSIVE (premise unmet: more than 1/3 of consensus CG coefficients <= 0)"
    s, gS, gN = res["slope_ci"], res["dGS"], res["dGN"]
    if s[0] > 1 or s[1] < 1 or gS[0] > 0 or gN[0] > 0: return "FAILED"
    if gS[1] < 0 and gN[1] < 0 and s[0] <= 1 <= s[1] and s[0] > 0: return "PASSED"
    return "INCONCLUSIVE"

def stage_outcome(env_path=None, tag="", end=END_Q, dmode="rvar", envkey="fit"):
    env = json.load(open(env_path or os.path.join(RES, "env.json")))
    rng = np.random.default_rng(SEED + 2)
    per, table = {}, {}
    for v, r in env.items():
        if not r["included"]: continue
        th = r[envkey] if r.get(envkey) else r["fit"]
        mom, m = spf_moments(spf_frame(v, end=end), micro_dispersion(v), dmode)
        if mom["se"] > MAX_SE:
            table[v] = dict(**mom, excluded="E4: NW SE of beta > %.2f" % MAX_SE); print(f"{v:8s} excluded by E4 (se {mom['se']:.3f})"); continue
        nf = mom["nf"]
        G, K, flag = predict(th, mom["ratio"], nf); Mk, KM, flagM = predict(r["fit_alpha2"], mom["ratio"], nf)
        spf_draws = block_boot(m, rng, N_SPF_DRAWS, dmode)
        draws = []
        for d in range(N_SPF_DRAWS):
            bh, ratio = spf_draws[d]; e, eM = r["draws"][d % len(r["draws"])], r["draws_alpha2"][d % len(r["draws_alpha2"])]
            draws.append((bh, predict(e, ratio, nf)[0], ratio, predict(eM, ratio, nf)[0]))
        per[v] = dict(beta=mom["beta"], G=G, S=mom["ratio"], M=Mk, draws=draws)
        qh = q_hf(th)
        table[v] = dict(**mom, beta_pred_GTAO=G, K=K, K_flag=flag, beta_pred_static=mom["ratio"], beta_pred_alpha2=Mk,
                        tauE=th["tauE"], alpha=th["alpha"], phi=th["phi"], q_hf=qh,
                        memory_scale_Nq=(K / qh) ** (1 / th["alpha"]))
        print(f"{v:8s} n={mom['n']} beta={mom['beta']:.3f} (NW se {mom['se']:.3f}) D/vf={mom['ratio']:.3f} "
              f"pred GTAO={G:.3f} alpha2={Mk:.3f} K={K:.3g}{'' if flag=='ok' else ' '+flag}", flush=True)
    vs = sorted(per)
    res = evaluate(per, rng)
    nonpos = sum(per[v]["beta"] <= 0 for v in vs)
    res["n_beta_nonpos"] = int(nonpos)
    res["verdict_primary"] = verdict(res, nonpos, len(vs))
    a = res["dGM"]
    res["verdict_alpha"] = ("alpha-dependence helps" if a[1] < 0 else "alpha-dependence hurts" if a[0] > 0 else "inconclusive")
    # secondary S1: as-scoped tauE-only slope (tests the fixed-variance assumption A1, per SPECTRUM_MAP_REFEREE)
    lb = lg(np.array([per[v]["beta"] for v in vs]))  # floored at FLOOR; lt = np.log([table[v]["tauE"] for v in vs])
    al = np.array([table[v]["alpha"] for v in vs]); lK = np.log([table[v]["K"] for v in vs]); lq = np.log([table[v]["q_hf"] for v in vs])
    boot = []
    for _ in range(B):
        i = rng.integers(0, len(vs), len(vs))
        if np.ptp(lt[i]) == 0 or np.ptp(lq[i]) == 0: continue
        boot.append([np.polyfit(lt[i], lb[i], 1)[0], np.mean(1 - 1 / al[i]), np.polyfit(lq[i], lK[i], 1)[0]])
    boot = np.array(boot)
    pc = lambda c: [float(np.percentile(boot[:, c], 2.5)), float(np.percentile(boot[:, c], 97.5))]
    res["S1_tauE_slope"] = dict(point=float(np.polyfit(lt, lb, 1)[0]), ci=pc(0), pred_1_minus_1_over_alpha=float(np.mean(1 - 1 / al)),
                                pred_ci=pc(1), rivals={"LFK": 0.5, "S2.2_B": 1.0, "fixed_q": 0.0})
    res["S2_noise_scaling"] = dict(slope_logK_on_logq=float(np.polyfit(lq, lK, 1)[0]), ci=pc(2),
                                   note="A1 (noise proportional to variance) predicts 0; noise proportional to short-timescale volatility predicts about 1")
    res["table"] = table
    os.makedirs(RES, exist_ok=True)
    json.dump(res, open(os.path.join(RES, f"outcome{tag}.json"), "w"), indent=1)
    print(json.dumps({k: res[k] for k in res if k != "table"}, indent=1))
    return res

if __name__ == "__main__":
    st = sys.argv[1]
    if st == "env": stage_env()
    elif st == "outcome": stage_outcome()
    elif st == "robust":
        stage_outcome(tag="_R1_full_sample", end=2026 * 4 + 3)
        stage_outcome(tag="_R2_sd_dispersion", dmode="sd")
        stage_outcome(tag="_R3_env_pre1990", envkey="fit_pre1990")
