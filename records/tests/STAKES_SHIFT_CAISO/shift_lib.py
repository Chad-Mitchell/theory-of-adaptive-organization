"""STAKES-SHIFT-CAISO locked library (numpy/pandas). See PREREG.md."""
import glob, os, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
K = "INTERVALSTARTTIME_GMT"

def read(year, key):
    fs = [f for f in sorted(glob.glob(os.path.join(HERE, "data", "raw", str(year), f"{key}_*.csv"))) if os.path.getsize(f) > 0]
    return pd.concat([pd.read_csv(f) for f in fs], ignore_index=True) if fs else pd.DataFrame()

def hourly(year):
    """One row per operating hour of `year`: DA, 2DA, ACTUAL and hourly mean of the 5-min RTD forecast (>= 10 of 12)."""
    def h(key, col):
        d = read(year, key)
        if d.empty: return None
        d = d[d.TAC_AREA_NAME == "CA ISO-TAC"].drop_duplicates(K)
        return d[[K, "OPR_DT", "OPR_HR", "MW"]].rename(columns={"MW": col})
    da = h("load_da", "da")
    if da is None: return pd.DataFrame()
    out = da
    for key, col in (("load_2da", "da2"), ("load_act", "act")):
        x = h(key, col)
        out = out.merge(x[[K, col]], on=K, how="left") if x is not None else out.assign(**{col: np.nan})
    r = read(year, "load_rtd")
    if not r.empty:
        r = r[(r.TAC_AREA_NAME == "CA ISO-TAC") & (r.EXECUTION_TYPE == "RTD")].drop_duplicates(K)
        r["hour"] = pd.to_datetime(r[K], utc=True).dt.floor("h").dt.strftime("%Y-%m-%dT%H:%M:%S-00:00")
        r = r.groupby("hour").agg(rtd=("MW", "mean"), n_rtd=("MW", "size")).reset_index().rename(columns={"hour": K})
        r.loc[r.n_rtd < 10, "rtd"] = np.nan
        out = out.merge(r[[K, "rtd"]], on=K, how="left")
    else:
        out["rtd"] = np.nan
    out = out[out.OPR_DT.astype(str).str.startswith(str(year))].copy()
    dt = pd.to_datetime(out.OPR_DT)
    out["hr"] = out.OPR_HR.clip(1, 24).astype(int); out["month"] = dt.dt.month; out["dkey"] = dt
    out["g"] = out.hr * 100 + out.month
    iso = dt.dt.isocalendar(); out["week"] = iso.year.astype(int) * 100 + iso.week.astype(int)
    out["dow"] = dt.dt.dayofweek
    lag = out[["dkey", "hr", "rtd"]].copy(); lag["dkey"] = lag.dkey + pd.Timedelta(days=7)
    out = out.merge(lag.rename(columns={"rtd": "rtd_l7"}), on=["dkey", "hr"], how="left")
    out = out.drop_duplicates(["dkey", "hr"]).sort_values(["dkey", "hr"]).reset_index(drop=True)
    out["e_rt"] = out.rtd - out.da          # primary: DA forecast error against the near-real-time forecast (same definition)
    out["e_2da"] = out.rtd - out.da2        # report only
    out["e_act"] = out.act - out.da         # report only (N21's error; BTM-definition gap)
    out["e_naive"] = out.rtd - out.rtd_l7   # q control: seasonal-naive (same hour, 7 days earlier) error
    return out

def fe_demean(y, g):
    y = np.asarray(y, float); u, inv = np.unique(g, return_inverse=True)
    return y - (np.bincount(inv, weights=y) / np.bincount(inv))[inv]

def mse_fe(e, g):
    """Within-stratum (hour x month) mean squared error: removes the level gap and every stratum bias."""
    return float(np.mean(fe_demean(e, g) ** 2))

def k_lin(spread, e, g):
    ed, sd = fe_demean(e, g), fe_demean(spread, g)
    return float(np.dot(ed, sd) / np.dot(ed, ed))

def week_index(wk):
    ub, inv = np.unique(wk, return_inverse=True)
    return [np.flatnonzero(inv == j) for j in range(ub.size)]

def resample(idx, rng):
    return np.concatenate([idx[j] for j in rng.integers(0, len(idx), len(idx))])

def D_stat(a, b, col, bq):
    """D = dlog MSE(col) - bq * dlog MSE(e_naive), year b minus year a (dataframes already restricted)."""
    return (np.log(mse_fe(b[col].values, b.g.values)) - np.log(mse_fe(a[col].values, a.g.values))
            - bq * (np.log(mse_fe(b.e_naive.values, b.g.values)) - np.log(mse_fe(a.e_naive.values, a.g.values))))

def D_boot(a, b, col, bq, B, seed):
    rng = np.random.default_rng(seed); ia, ib = week_index(a.week.values), week_index(b.week.values)
    out = []
    for _ in range(B):
        out.append(D_stat(a.iloc[resample(ia, rng)], b.iloc[resample(ib, rng)], col, bq))
    return np.array(out)
