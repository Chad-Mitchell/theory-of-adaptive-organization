"""Range of dln t_A (A->B) over one-pole poles whose loss is within 0.5% of the minimum (author's flatness band), from the
exact-grid scan in r4_telegraph_grid_M6.json (61 poles per point; tA interpolated in ln pole)."""
import json, numpy as np, sys
R = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'r4_telegraph_grid_M6.json'))
out = {}
for loss in ('err', 'mse', 'abs'):
    band = {}
    for pt in ('A', 'B'):
        sc = R[pt]['scan']; x = np.array([s['lnrel'] for s in sc]); L = np.array([s[loss] for s in sc]); t = np.log([s['tA'] for s in sc])
        xf = np.linspace(x[0], x[-1], 4001); Lf = np.interp(xf, x, L); tf = np.interp(xf, x, t)
        Lmin = R[pt]['best_'+loss][loss]; ok = Lf <= 1.005*Lmin
        band[pt] = (tf[ok].min(), tf[ok].max())
    lo = band['B'][0]-band['A'][1]; hi = band['B'][1]-band['A'][0]
    out[loss] = dict(point=R['dln_'+loss], band=[lo, hi])
    print(loss, 'dln at argmin %.4f; range within 0.5%% of min loss [%.3f, %.3f]' % (R['dln_'+loss], lo, hi))
json.dump(out, open('r5_flatness.json', 'w'), indent=1)
