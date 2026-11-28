"""Shared loaders for LAB-AKLMT-TAU (pick 36). Data: Afrouzi, Kwon, Landier, Ma, Thesmar (2023 QJE) replication
package, Harvard Dataverse doi:10.7910/DVN/3Q6BHC (CC0 1.0), Replication.zip sha256
efa8fd126bf18836b203f5ac8a5d9e1d6df37683ca9c92b9e88dff75bcb4d6c9, files data/ExperimentK/{detail,overview}.csv copied
unchanged (data/SHA256SUMS).
Row convention (AKLMT code/FigureII.do): in the row of round t, predictiona_value is the forecast of x_t made after
seeing x_{t-1} (the previous row's `actual`). Rounds -39..0 are the shown history, 1..40 the forecast rounds."""
import os
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))

def load(exp):
    d = pd.read_csv(os.path.join(HERE, "data", f"exp{exp}_detail.csv"))
    d["rho"] = d["rho"].round(1)
    d = d.sort_values(["assignmentid", "round"]).reset_index(drop=True)
    d["x_prev"] = d.groupby("assignmentid")["actual"].shift(1)
    return d

def ols_forecasts(d):
    """Feasible-information learner: in round t (>= 1), fit x_s = a + b x_{s-1} by OLS on every pair available before
    the forecast (s <= t-1, history included) and forecast a + b x_{t-1}. Same information as the participant."""
    out = []
    for aid, g in d.groupby("assignmentid", sort=False):
        x = g["actual"].to_numpy(float); r = g["round"].to_numpy()
        f = np.full(len(x), np.nan)
        for i in range(len(x)):
            if r[i] < 1:
                continue
            y, z = x[1:i], x[0:i - 1]          # pairs (x_{s-1}, x_s) with s <= t-1
            Z = np.column_stack([np.ones_like(z), z])
            a, b = np.linalg.lstsq(Z, y, rcond=None)[0]
            f[i] = a + b * x[i - 1]
        out.append(pd.Series(f, index=g.index))
    return pd.concat(out).reindex(d.index)

def implied_persistence(d, col):
    """AKLMT Figure II panel B statistic per condition: pooled OLS slope of the forecast on x_{t-1}, rounds 1..40."""
    s = d[(d["round"] >= 1)].dropna(subset=[col, "x_prev"])
    res = {}
    for rho, g in s.groupby("rho"):
        x = g["x_prev"].to_numpy(); y = g[col].to_numpy()
        res[rho] = np.cov(x, y, ddof=0)[0, 1] / np.var(x)
    return res

def slope_on_rho(ip):
    r = np.array(sorted(ip)); v = np.array([ip[k] for k in r])
    return float(np.polyfit(r, v, 1)[0])

def boot_conditions(d, col, B, seed):
    """Resample participants with replacement within condition; returns list of implied-persistence dicts."""
    rng = np.random.default_rng(seed)
    s = d[(d["round"] >= 1)].dropna(subset=[col, "x_prev"])
    groups = {rho: [g for _, g in gg.groupby("assignmentid")] for rho, gg in s.groupby("rho")}
    stats = {rho: [(g["x_prev"].to_numpy(), g[col].to_numpy()) for g in gs] for rho, gs in groups.items()}
    out = []
    for _ in range(B):
        ip = {}
        for rho, lst in stats.items():
            idx = rng.integers(0, len(lst), len(lst))
            x = np.concatenate([lst[i][0] for i in idx]); y = np.concatenate([lst[i][1] for i in idx])
            ip[rho] = np.cov(x, y, ddof=0)[0, 1] / np.var(x)
        out.append(ip)
    return out
