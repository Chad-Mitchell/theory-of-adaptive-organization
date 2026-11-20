"""GRID-2 diagnosis (after the verdict; does not change it): which component carries the f^-2 spectrum,
and the preregistered speed-price check (GRID-1 kill condition) on GB capacity prices."""
import json, os, numpy as np, pandas as pd
import grid2_run as g
from scipy.optimize import least_squares
E = g.inertia(); eacv = g.eac(); mf = g.mfr()
xs, idxs, Bs = [], [], []
for w in g.WEEKS:
    days = pd.date_range(w, periods=7, freq="1D")
    fw = g.freq([(int(w[:4]), int(w[5:7]))]); fw = fw[~fw.index.duplicated()]
    idx = pd.date_range(days[0], days[-1] + pd.Timedelta("1D"), freq="1s", inclusive="left")
    xs.append(fw.reindex(idx).to_numpy()); idxs.append(idx)
    Bm = pd.concat([g.bm(d.strftime("%Y-%m-%d")) for d in days]); Bs.append(Bm.reindex(Bm.index.union(idx)).interpolate().reindex(idx).to_numpy())
f = pd.Series(np.concatenate(xs)).interpolate(limit=60, limit_area="inside").to_numpy(); idx = idxs[0].append(idxs[1:]); B = np.concatenate(Bs)
E1, vol, M = g.align(idx, E, eacv, mf)
Z = np.zeros_like(f)
full = g.reconstruct(f, idx, E1, vol, M, B)
comp = {"B_only": B, "R_only": g.reconstruct(f, idx, E1, vol, M, Z) + 0.02*28000*(f-50) + (2*E1*1000/50)*np.gradient(f),
        "inertia_term": -(2*E1*1000/50)*np.gradient(f), "full": full}
out = {}
for k, x in comp.items():
    x = g.desched(x, idx); fr, P = g.day_periodograms(x, 1.0, 4*3600, 86400); fb, Pb = g.logbin(fr, P.mean(0), 2, 4*3600)
    for lo_p, hi_p, lab in [(2, 60, "2-60s"), (60, 900, "60-900s"), (900, 4*3600, "900s-4h")]:
        m = (fb >= 1/hi_p) & (fb <= 1/lo_p)
        out.setdefault(k, {})[lab] = float(-np.polyfit(np.log(fb[m]), np.log(Pb[m]), 1)[0])
    out[k]["var_share_of_full"] = float(np.nanvar(x) / np.nanvar(g.desched(full, idx)))
# speed price: mean clearing price (GBP/MW/h) per product over Nov 2025-Oct 2026
d = pd.concat([pd.read_csv(os.path.join(g.DATA, f)) for f in ["eac_fy2025.csv", "eac_summary.csv"]])
d["t"] = pd.to_datetime(d.deliveryStart); d = d[(d.t >= "2025-11-01") & (d.t < "2026-11-01")]
pr = d[d.auctionProduct.isin(["DCL", "DCH", "DML", "DMH", "DRL", "DRH"])].groupby("auctionProduct").apply(
    lambda x: float(np.average(x.clearingPrice, weights=x.clearedVolume.clip(lower=1e-9)))).to_dict()
out["mean_price_GBP_per_MW_h"] = pr
print(json.dumps(out, indent=1)); json.dump(out, open("grid2_diag.json", "w"), indent=1)
