#!/usr/bin/env python3
"""STAKES-REFEREE own-code checks on N21 (STAKES-EXOGENOUS) panels. Descriptive referee checks, no locked verdict."""
import os, json, numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(H, "..", "..", "..", "tests", "STAKES_EXOGENOUS", "data")
def load(y):
    p = pd.read_csv(os.path.join(P, f"panel_{y}.csv.gz")); p = p[p.OPR_DT != "2024-06-01"].copy()
    dt = pd.to_datetime(p.OPR_DT); p["month"] = dt.dt.month; p["g"] = p.hr * 100 + p.month
    iso = dt.dt.isocalendar(); p["week"] = iso.year.astype(int) * 100 + iso.week.astype(int)
    p["doy"] = (dt - pd.Timestamp(f"{y}-01-01")).dt.days
    p["e"] = p.load_act - p.load_da; p["s"] = p.p_rt - p.p_da; p["dkey"] = dt
    return p.sort_values(["dkey", "hr"]).reset_index(drop=True)
def dm(x, g):
    u, i = np.unique(g, return_inverse=True); return x - (np.bincount(i, weights=x) / np.bincount(i))[i]
def k(s, e, g):
    ed = dm(e, g); return float(ed @ dm(s, g) / (ed @ ed))
def blocks(lab):
    u, i = np.unique(lab, return_inverse=True); return [np.flatnonzero(i == j) for j in range(u.size)]
def boot(s, e, g, idx, B, seed):
    rng = np.random.default_rng(seed); out = np.empty(B)
    for b in range(B):
        ix = np.concatenate([idx[j] for j in rng.integers(0, len(idx), len(idx))]); out[b] = k(s[ix], e[ix], g[ix])
    return out
R = {}
for y, seed in ((2025, 20261115 + 12), (2024, 20261115 + 13)):
    p = load(y); s, e, g = p.s.values, p.e.values, p.g.values
    r = {"n": len(p), "k_lin": k(s, e, g)}
    # 1. block-length sensitivity (1, 2, 4 weeks) and 1-day blocks
    for name, lab in (("day", p.doy.values), ("week", p.week.values), ("2week", p.doy.values // 14), ("4week", p.doy.values // 28)):
        bs = boot(s, e, g, blocks(lab), 2000, seed)
        lo, hi = np.percentile(bs, [2.5, 97.5]); r[f"ci_{name}"] = [lo, hi, (hi - lo) / (2 * r["k_lin"]), float(bs.std(ddof=1))]
    # 2. week jackknife: influence of single weeks
    wk = p.week.values; jk = np.array([k(s[wk != w], e[wk != w], g[wk != w]) for w in np.unique(wk)])
    nw = jk.size; se_jk = float(np.sqrt((nw - 1) / nw * np.sum((jk - jk.mean()) ** 2)))
    infl = sorted(zip((r["k_lin"] - jk).tolist(), np.unique(wk).tolist()), reverse=True)[:3]
    r["jackknife_se"] = se_jk; r["top3_week_influence(k - k_without)"] = infl
    # 3. spike sensitivity: drop hours with |spread| above 99th / 99.9th pct; Huber-type check via winsor 1/99
    for q in (99.9, 99.0):
        m = np.abs(s) <= np.percentile(np.abs(s), q); r[f"k_drop_abs_spread_gt_p{q}"] = k(s[m], e[m], g[m])
    lo, hi = np.percentile(s, [1, 99]); r["k_winsor_1_99"] = k(np.clip(s, lo, hi), e, g)
    # share of the numerator sum(e~ s~) from the top 1% of hours by |e~ s~|
    c = dm(e, g) * dm(s, g); o = np.sort(np.abs(c))[::-1]; r["numerator_share_top1pct_hours_abs"] = float(o[: len(o) // 100].sum() / np.abs(c).sum())
    r["numerator_share_top1pct_signed"] = float(c[np.argsort(-np.abs(c))[: len(c) // 100]].sum() / c.sum())
    # 4. coverage of the locked percentile week-block CI with REAL residual blocks (week-permuted FE residuals, heavy tails kept)
    ed = dm(e, g); res = dm(s, g) - r["k_lin"] * ed; idx = blocks(wk); rng = np.random.default_rng(7 + y); cov = 0; covd = 0; R_ = 150
    for t in range(R_):
        perm = rng.permutation(len(idx)); res_p = np.concatenate([res[idx[j]] for j in perm])
        L = min(len(res_p), len(ed)); s_sim = (r["k_lin"] * ed[:L] + res_p[:L]); ee, gg = ed[:L], g[:L]
        idx_s = [ix[ix < L] for ix in idx]; idx_s = [ix for ix in idx_s if ix.size]
        bs = boot(s_sim, ee, gg, idx_s, 200, 1000 + t); lo, hi = np.percentile(bs, [2.5, 97.5]); cov += lo <= r["k_lin"] <= hi
        bs2 = boot(s_sim, ee, gg, [ix for ix in blocks(p.doy.values // 28) if ix.max() < L], 200, 5000 + t); lo, hi = np.percentile(bs2, [2.5, 97.5]); covd += lo <= r["k_lin"] <= hi
    r["coverage_week_block_real_resid"] = cov / R_; r["coverage_4week_block_real_resid"] = covd / R_; r["coverage_reps"] = R_
    # 5. exogeneity: D-1 errors (upper bound on information at DA issue: hours of D-1 before ~10 AM are known when DAM closes)
    lag = p[["dkey", "hr", "e"]].copy(); lag1 = lag.copy(); lag1["dkey"] += pd.Timedelta(days=1); lag2 = lag.copy(); lag2["dkey"] += pd.Timedelta(days=2)
    q = p.merge(lag1.rename(columns={"e": "l1"}), on=["dkey", "hr"], how="left").merge(lag2.rename(columns={"e": "l2"}), on=["dkey", "hr"], how="left")
    am = lag[lag.hr <= 9].groupby("dkey").e.mean().rename("l1am").reset_index(); am["dkey"] += pd.Timedelta(days=1)
    q = q.merge(am, on="dkey", how="left"); ok = q[["l1", "l2", "l1am"]].notna().all(axis=1).values
    gg = q.g.values[ok]; yv = dm(q.e.values[ok], gg)
    def r2(cols):
        X = np.column_stack([dm(q[c].values[ok], gg) for c in cols]); b = np.linalg.lstsq(X, yv, rcond=None)[0]; return float(1 - np.var(yv - X @ b) / np.var(yv))
    r["incrR2_l2"] = r2(["l2"]); r["incrR2_l1am_l2"] = r2(["l1am", "l2"]); r["incrR2_l1_l2_upper"] = r2(["l1", "l2"])
    # does the forecastable part carry the same k? split e into fitted (l1am,l2) and residual
    X = np.column_stack([dm(q[c].values[ok], gg) for c in ("l1am", "l2")]); b = np.linalg.lstsq(X, yv, rcond=None)[0]; fit = X @ b; sv = dm(q.s.values[ok], gg)
    r["k_on_unforecastable_part"] = float((yv - fit) @ sv / ((yv - fit) @ (yv - fit)))
    # 6. estimand identity: k_lin = sum_g k_g V_g / sum V_g
    kg, vg = [], []
    for gv in np.unique(g):
        m = g == gv; ee = e[m] - e[m].mean(); ss = s[m] - s[m].mean(); kg.append(ee @ ss / (ee @ ee)); vg.append(ee @ ee)
    kg, vg = np.array(kg), np.array(vg); r["identity_weighted_mean_kg"] = float((kg * vg).sum() / vg.sum())
    r["share_strata_kg_negative"] = float((kg < 0).mean())
    R[y] = r
# 7. year contrast (week blocks, independent years)
b25 = boot(*(lambda p: (p.s.values, p.e.values, p.g.values))(load(2025)), blocks(load(2025).week.values), 2000, 11)
b24 = boot(*(lambda p: (p.s.values, p.e.values, p.g.values))(load(2024)), blocks(load(2024).week.values), 2000, 12)
d = np.log(np.clip(b25, 1e-9, None)) - np.log(np.clip(b24, 1e-9, None))
R["dlog_k_2025_vs_2024"] = {"est": float(np.log(R[2025]["k_lin"] / R[2024]["k_lin"])), "ci": np.percentile(d, [2.5, 97.5]).tolist(), "frac_b25_le0": float((b25 <= 0).mean())}
json.dump(R, open(os.path.join(H, "ref_n21.json"), "w"), indent=1, default=float); print(json.dumps(R, indent=1, default=float))
