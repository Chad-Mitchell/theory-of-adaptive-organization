"""STAKES-EXOGENOUS analysis library (locked with PREREG.md). numpy/pandas only.

Proxy (declared): world X = CA ISO-TAC hourly integrated actual load; the system's state M = CAISO's day-ahead
load forecast for that hour; tracking error e = actual - DA forecast (MW). Cost of the error to load that bought at the
DA forecast and settles the difference in real time: C = e * (P_RT - P_DA), with P = mean of the NP15 and SP15 trading-hub
LMPs, P_RT = hourly mean of the 15-min FMM (RTPD) LMP. Under quadratic loss (THEORY 2.1) E[C | e] = w e^2.
"""
import numpy as np

def fe_demean(y, g):
    """Subtract group means (one-way fixed effects)."""
    y = np.asarray(y, float); out = y.copy()
    u, inv = np.unique(g, return_inverse=True)
    s = np.bincount(inv, weights=y); n = np.bincount(inv)
    return y - (s / n)[inv]

def slope_fe(y, x, g):
    yd, xd = fe_demean(y, g), fe_demean(x, g)
    return float(np.dot(xd, yd) / np.dot(xd, xd))

def zscore_fe(e, g):
    """Within-stratum standardized error."""
    ed = fe_demean(e, g)
    u, inv = np.unique(g, return_inverse=True)
    sd = np.sqrt(np.bincount(inv, weights=ed ** 2) / np.bincount(inv))
    sd = np.where(sd > 0, sd, np.inf)   # degenerate bootstrap strata (all rows identical): ed = 0, contributes nothing
    return ed / sd[inv]

def estimates(e, spread, g):
    """w (primary) = k_lin: FE slope of spread on e = sum(e~ s~)/sum(e~^2) = stratum-demeaned cost per unit squared error,
    i.e. the e^2-weighted mean of stratum stakes. w_quad: FE slope of C = e*spread on e^2 (N18 form; weights strata by
    var(e^2), so it differs from w when stakes vary across strata). k_small / k_large: k_lin on |z| below / above 0.6745
    (the median of |N(0,1)|), z = within-stratum standardized error; quadratic loss implies k_small = k_large."""
    C = e * spread
    z = np.abs(zscore_fe(e, g)); sm = z <= 0.6745
    ed, sd_ = fe_demean(e, g), fe_demean(spread, g)
    ks = float(np.dot(ed[sm], sd_[sm]) / np.dot(ed[sm], ed[sm])); kl = float(np.dot(ed[~sm], sd_[~sm]) / np.dot(ed[~sm], ed[~sm]))
    return {"k_lin": slope_fe(spread, e, g), "w_quad": slope_fe(C, e ** 2, g), "k_small": ks, "k_large": kl, "log_large_over_small": float(np.log(kl / ks)) if kl > 0 and ks > 0 else float("nan")}

def block_boot(e, spread, g, block, B, seed):
    """Resample whole blocks (calendar weeks) with replacement; percentile 95% CIs."""
    rng = np.random.default_rng(seed)
    ub, binv = np.unique(block, return_inverse=True)
    idx = [np.flatnonzero(binv == k) for k in range(ub.size)]
    pt = estimates(e, spread, g)
    bs = {k: [] for k in pt}
    for _ in range(B):
        ix = np.concatenate([idx[j] for j in rng.integers(0, ub.size, ub.size)])
        r = estimates(e[ix], spread[ix], g[ix])
        for k in r: bs[k].append(r[k])
    out = {}
    for k, v in pt.items():
        a = np.array(bs[k])
        out[k] = {"est": v, "lo": float(np.nanpercentile(a, 2.5)), "hi": float(np.nanpercentile(a, 97.5)), "se": float(np.nanstd(a, ddof=1))}
    return out

def exog_r2(e, g, lag2_same_hour, lag2_daymean):
    """Incremental R^2 of e on information known when the DA forecast is issued (errors of day D-2), beyond stratum FE."""
    ok = np.isfinite(lag2_same_hour) & np.isfinite(lag2_daymean)
    y = fe_demean(e[ok], g[ok])
    X = np.column_stack([fe_demean(lag2_same_hour[ok], g[ok]), fe_demean(lag2_daymean[ok], g[ok])])
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ b
    return float(1 - res.var() / y.var()), int(ok.sum())

def winsor(x, p=0.5):
    lo, hi = np.percentile(x, [p, 100 - p])
    return np.clip(x, lo, hi)

def relprec(r):
    """(hi - lo) / (2 |est|): half-width relative to the estimate."""
    return (r["hi"] - r["lo"]) / (2 * abs(r["est"])) if r["est"] != 0 else np.inf
