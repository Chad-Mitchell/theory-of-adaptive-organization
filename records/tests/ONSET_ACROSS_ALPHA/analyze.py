"""Locked estimators (written before any design-cell outcome). usage: analyze.py results.jsonl [alphas...]
N*(rho): seed-mean D_rel(N) = (flat - levelled)/flat -> isotonic (increasing) fit -> upward zero crossing
interpolated in ln N. Valid if a crossing exists in >= 90% of 2000 seed-bootstrap replicates.
e(alpha): OLS slope of ln N* on ln rho over valid rho; CI = percentile seed bootstrap (seeds resampled per cell).
Delta = e(2.5) - e(1.5), bootstrap independent across alpha (independent seeds/paths)."""
import sys, json, numpy as np
from collections import defaultdict
from sklearn.isotonic import IsotonicRegression
B = 2000

def crossing(lnN, d):
    f = IsotonicRegression(increasing=True).fit_transform(lnN, d)
    idx = np.where((f[:-1] < 0) & (f[1:] >= 0))[0]
    if len(idx) == 0 or f[0] >= 0 or f[-1] < 0: return np.nan
    i = idx[0]
    return lnN[i] + (0 - f[i]) * (lnN[i + 1] - lnN[i]) / (f[i + 1] - f[i])

def load(path):
    cells = defaultdict(list)
    for l in open(path):
        r = json.loads(l)
        drel = (r['flat'] - np.array(r['levelled'])) / r['flat']
        cells[(r['alpha'], r['rho'])].append((np.log(r['N']), drel, r['seed']))
    return cells

def cell_boot(rows, rng):
    lnN = rows[0][0]; D = np.array([x[1] for x in rows]); S = len(rows)
    pt = crossing(lnN, D.mean(0))
    bs = np.array([crossing(lnN, D[rng.integers(S, size=S)].mean(0)) for _ in range(B)])
    return pt, bs

def analyse(path, alphas=(1.5, 2.5), seed=20261115):
    rng = np.random.default_rng(seed)
    cells = load(path); out = {}
    for a in alphas:
        rhos = sorted(r for (al, r) in cells if al == a)
        pts, bss, valid = [], [], []
        for r in rhos:
            pt, bs = cell_boot(cells[(a, r)], rng)
            ok = np.mean(np.isfinite(bs)) >= 0.9 and np.isfinite(pt)
            pts.append(pt); bss.append(bs); valid.append(ok)
        v = np.array(valid); lr = np.log(rhos)
        res = dict(rhos=rhos, lnNstar=[float(p) for p in pts], valid=[bool(x) for x in v],
                   sd_lnNstar=[float(np.nanstd(b)) for b in bss], n_seeds=len(cells[(a, rhos[0])]))
        if v.sum() >= 4 and lr[v].max() - lr[v].min() >= np.log(10):
            e = np.polyfit(lr[v], np.array(pts)[v], 1)[0]
            eb = []
            for j in range(B):
                y = np.array([bss[k][j] for k in range(len(rhos))])[v]
                eb.append(np.polyfit(lr[v], y, 1)[0] if np.all(np.isfinite(y)) else np.nan)
            eb = np.array(eb)
            res.update(e=float(e), e_boot=eb, e_se=float(np.nanstd(eb)), e_ci=[float(np.nanpercentile(eb, 2.5)), float(np.nanpercentile(eb, 97.5))])
        out[a] = res
    return out

if __name__ == '__main__':
    al = tuple(float(x) for x in sys.argv[2:]) or (1.5, 2.5)
    o = analyse(sys.argv[1], al)
    for a, r in o.items():
        r = {k: v for k, v in r.items() if k != 'e_boot'}
        print(a, json.dumps(r))
