"""GRID-4: local log-log slope of the full reconstruction at 2-60 s (same method as grid2_diag.py 'full')."""
import json, os, sys, numpy as np, pandas as pd
import grid2_run as g
E = g.inertia(); eacv = g.eac() if g.FLAT_Q is None else None; mf = g.mfr() if g.FLAT_Q is None else None
xs, idxs, Bs = [], [], []
for w in g.WEEKS:
    days = pd.date_range(w, periods=7, freq="1D")
    fw = g.freq([(int(w[:4]), int(w[5:7]))]); fw = fw[~fw.index.duplicated()]
    idx = pd.date_range(days[0], days[-1] + pd.Timedelta("1D"), freq="1s", inclusive="left")
    xs.append(fw.reindex(idx).to_numpy()); idxs.append(idx)
    Bm = pd.concat([g.bm(d.strftime("%Y-%m-%d")) for d in days]); Bs.append(Bm.reindex(Bm.index.union(idx)).interpolate().reindex(idx).to_numpy())
f = pd.Series(np.concatenate(xs)).interpolate(limit=60, limit_area="inside").to_numpy(); idx = idxs[0].append(idxs[1:]); B = np.concatenate(Bs)
E1, vol, M = g.align(idx, E, eacv, mf)
out = {}
for lab, x in [("main", 1.0)] + [(f"Q_x{q}", q) for q in g.CFG.get("q_variants", [])]:
    D = g.desched(g.reconstruct(f, idx, E1, vol, M, B, mfr_x=x), idx)
    fr, P = g.day_periodograms(D, 1.0, 4*3600, 86400); fb, Pb = g.logbin(fr, P.mean(0), 2, 4*3600)
    m = (fb >= 1/60) & (fb <= 1/2)
    out[lab] = float(-np.polyfit(np.log(fb[m]), np.log(Pb[m]), 1)[0])
print(json.dumps(out)); json.dump(out, open(os.path.join(g.OUT, g.CFG.get("slope_out", "grid4_slope.json")), "w"), indent=1)
