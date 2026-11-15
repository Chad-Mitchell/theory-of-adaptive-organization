"""Own Whittle on the demo's committed DGS10 file: Wald SE vs contiguous-block dispersion (robustness of Wald SEs
to volatility clustering / fat tails). Same data window and cleaning rule as PREREG §3 (missing dropped)."""
import numpy as np, csv, sys
sys.path.insert(0, '.')
from ownlib import whittle, f_inc
rows = list(csv.reader(open('../../../measurement/estimators/data/DGS10.csv')))[1:]
y = np.array([float(v) for d, v in rows if v not in ('', '.') and '1990-01-02' <= d <= '2026-10-30'])
print("n", y.size)
r = whittle(y); print("full band: alpha %.3f Wald SE %.3f  logq %.2f  m %d" % (r['a'], r['se'][1], r['lq'], r['m']))
d = np.diff(y); k = ((d-d.mean())**4).mean()/d.var()**2 - 3; print("excess kurtosis of increments %.2f" % k)
# periodogram-ratio diagnostics: under Gaussian Whittle, I/f ~ Exp(1): var 1, and ratios ~ uncorrelated across j
R = r['I']/f_inc(r['w'], r['lq'], r['a'], r['ls'])
print("var(I/f) %.2f (Exp(1): 1)" % R.var())
# correlation of squared increments (volatility clustering) at lags 1..5
s = (d-d.mean())**2; print("acf of squared increments lags 1-5:", [round(np.corrcoef(s[:-L], s[L:])[0,1], 3) for L in range(1, 6)])
for K in (4, 8, 16):
    L = y.size//K; al = []; se = []
    for i in range(K):
        rr = whittle(y[i*L:(i+1)*L]); al.append(rr['a']); se.append(rr['se'][1])
    al = np.array(al)
    print(f"K={K} blocks of {L}: block alphas sd {al.std(ddof=1):.3f} vs median Wald SE {np.median(se):.3f}; ratio {al.std(ddof=1)/np.median(se):.2f}; implied full-sample SE {al.std(ddof=1)/np.sqrt(K):.3f}; block alphas {np.round(al,2).tolist()}")
