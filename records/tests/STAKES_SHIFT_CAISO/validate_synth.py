#!/usr/bin/env python3
"""Synthetic check of D_stat / D_boot (before lock). Two Jan-Oct years of hours, hour x month strata with stratum means and
sds, AR(1) hourly errors with day-level weather shocks (weekly-correlated), seasonal-naive error built the same way.
Planted: dlog MSE(e) = 0.30, dlog MSE(naive) = 0.15 -> true D = 0.30 - 0.15/3 = 0.25. R = 100 replications, B = 200."""
import numpy as np, pandas as pd
from shift_lib import D_stat, D_boot
def year(rng, scale_e, scale_n, y):
    days = pd.date_range(f"{y}-01-01", f"{y}-10-31"); n = len(days) * 24
    dt = np.repeat(days.values, 24); hr = np.tile(np.arange(1, 25), len(days)); month = pd.DatetimeIndex(dt).month.values
    g = hr * 100 + month
    mu = rng.normal(0, 1500, 2500)[g % 2500]; sd = (0.6 + 0.4 * np.abs(np.sin(hr / 3.8)))
    wk = np.repeat(rng.normal(0, 1, len(days) // 7 + 2), 7)[: len(days)]
    dayshock = np.repeat(0.6 * wk + rng.normal(0, 0.8, len(days)), 24)
    def ar(s):
        x = np.empty(n); z = rng.normal(0, 1, n); x[0] = z[0]
        for t in range(1, n): x[t] = 0.85 * x[t - 1] + np.sqrt(1 - 0.85 ** 2) * z[t]
        return s * 800 * sd * (0.7 * x + 0.7 * dayshock)
    iso = pd.DatetimeIndex(dt).isocalendar()
    return pd.DataFrame({"g": g, "week": (iso.year * 100 + iso.week).values, "e_rt": mu + ar(scale_e), "e_naive": 2 * mu + ar(2 * scale_n)})
rng = np.random.default_rng(7); Ds, cov, ses = [], 0, []
for r in range(100):
    a = year(rng, 1.0, 1.0, 2025); b = year(rng, np.exp(0.15), np.exp(0.075), 2026)
    D = D_stat(a, b, "e_rt", 1 / 3); bs = D_boot(a, b, "e_rt", 1 / 3, 200, 1000 + r)
    lo, hi = np.percentile(bs, [2.5, 97.5]); cov += (lo <= 0.25 <= hi); Ds.append(D); ses.append(bs.std(ddof=1))
Ds = np.array(Ds)
print(f"true D 0.25: mean D {Ds.mean():.4f}, sd across reps {Ds.std(ddof=1):.4f}, mean boot se {np.mean(ses):.4f}, coverage {cov/100:.2f}")
