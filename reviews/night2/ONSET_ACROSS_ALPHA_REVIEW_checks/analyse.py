"""Reviewer analysis (own code). Two onset estimators on the seed-mean D_rel(N) = (flat - levelled)/flat:
  iso  : own re-implementation of the locked rule (increasing isotonic fit -> first upward zero crossing, linear in ln N)
  cubic: cubic polynomial in ln N fitted to the seed-mean curve, root nearest the iso crossing / sign change.
Validity: crossing in >= 90% of B seed-bootstrap replicates. e = OLS slope of ln N* on ln rho; percentile bootstrap.
Delta = e(2.5) - e(1.5); locked margin 0.267 around predicted Delta (continuous closed form -0.0002).
usage: analyse.py FILE.jsonl [label]"""
import sys, json, numpy as np
from collections import defaultdict
from sklearn.isotonic import IsotonicRegression
B = 2000; DELTA = 0.267; DPRED = -0.0002
def cross_iso(x, d):
    f = IsotonicRegression(increasing=True).fit_transform(x, d)
    if f[0] >= 0 or f[-1] < 0: return np.nan
    i = np.where((f[:-1] < 0) & (f[1:] >= 0))[0][0]
    return x[i] + (0 - f[i]) * (x[i + 1] - x[i]) / (f[i + 1] - f[i])
def cross_cubic(x, d):
    p = np.polyfit(x, d, 3); r = np.roots(p)
    r = r[np.isreal(r)].real; r = r[(r >= x[0]) & (r <= x[-1])]
    r = [z for z in r if np.polyval(np.polyder(p), z) > 0]
    return float(min(r)) if r else np.nan
def load(path):
    cells = defaultdict(list)
    for l in open(path):
        r = json.loads(l); d = (r['flat'] - np.array(r['levelled'])) / r['flat']
        cells[(r['alpha'], r['rho'])].append((np.log(r['N']), d))
    return cells
def run(path, est, seed=11):
    rng = np.random.default_rng(seed); cells = load(path); res = {}
    for a in sorted({k[0] for k in cells}):
        rhos = sorted(r for (al, r) in cells if al == a); pts, bss, val = [], [], []
        for r in rhos:
            x = cells[(a, r)][0][0]; D = np.array([c[1] for c in cells[(a, r)]]); S = len(D)
            pt = est(x, D.mean(0)); bs = np.array([est(x, D[rng.integers(S, size=S)].mean(0)) for _ in range(B)])
            pts.append(pt); bss.append(bs); val.append(np.isfinite(pt) and np.mean(np.isfinite(bs)) >= 0.9)
        lr = np.log(rhos); v = np.array(val); y = np.array(pts)
        e = np.polyfit(lr[v], y[v], 1)[0] if v.sum() >= 4 else np.nan
        eb = np.array([np.polyfit(lr[v], np.array([b[j] for b in bss])[v], 1)[0]
                       if np.all(np.isfinite([b[j] for b in bss])) else np.nan for j in range(B)])
        res[a] = dict(n_seeds=S, valid=v.tolist(), lnNstar=np.round(y, 3).tolist(), e=float(e), eb=eb,
                      se=float(np.nanstd(eb)), ci=[float(np.nanpercentile(eb, 2.5)), float(np.nanpercentile(eb, 97.5))],
                      medTf=float(np.median([np.median(json.loads(l)['Tf']) for l in open(path) if json.loads(l)['alpha'] == a])))
    out = {}
    for a, r in res.items(): out[str(a)] = {k: v for k, v in r.items() if k != 'eb'}
    if len(res) == 2:
        a1, a2 = sorted(res); db = res[a2]['eb'] - res[a1]['eb']; d = res[a2]['e'] - res[a1]['e']
        lo, hi = np.nanpercentile(db, [2.5, 97.5]); se = float(np.nanstd(db))
        v = 'PASS' if (lo > DPRED - DELTA and hi < DPRED + DELTA) else (
            'FAIL' if ((lo > DPRED or hi < DPRED) and abs(d - DPRED) >= DELTA / 2) else 'INCONCLUSIVE')
        out['contrast'] = dict(delta=round(float(d), 4), se=round(se, 4), ci=[round(float(lo), 4), round(float(hi), 4)], verdict=v)
    return out
if __name__ == '__main__':
    path = sys.argv[1]; allout = {}
    for name, est in (('iso', cross_iso), ('cubic', cross_cubic)):
        o = run(path, est); allout[name] = o
        print(path, name, json.dumps({k: (dict(e=round(v['e'], 4), se=round(v['se'], 4), ci=np.round(v['ci'], 3).tolist(), valid=sum(v['valid']), medTf=v['medTf']) if k != 'contrast' else v) for k, v in o.items()}))
    json.dump(allout, open(path.replace('.jsonl', '') + '_analysis.json', 'w'), indent=1)
