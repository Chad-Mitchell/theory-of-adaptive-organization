"""C1: data, driver Whittle fits (full, R1 split, in-band free and fixed noise), locked W21 estimator + bootstrap."""
import json, math, numpy as np, rlib
y, z, d = rlib.load()
out = {'n': len(y), 'dates': [d[0], d[-1]], 'vix_missing': int(np.isnan(z).sum())}
B = 2 * math.pi / 21
out['full'] = rlib.whittle(y)
out['R1_low_T>20'] = rlib.whittle(y, wmax=2 * math.pi / 20)
out['R1_high_T<=20'] = rlib.whittle(y, wmin=2 * math.pi / 20)
out['band_free'] = rlib.whittle(y, wmax=B)
out['band_fixnoise'] = rlib.whittle(y, wmax=B, fix_logs2=out['full']['logs2'])
out['T>126'] = rlib.whittle(y, wmax=2 * math.pi / 126)
out['T21-126'] = rlib.whittle(y, wmin=2 * math.pi / 126, wmax=B)
# profile: in-band alpha as the fixed noise level varies (how much does the choice drive alpha?)
out['profile_fixnoise'] = {f'{ls:.2f}': rlib.whittle(y, wmax=B, fix_logs2=ls)['alpha'] for ls in
                           [-13.9, -3.0, -2.0, -1.5, -1.2, -0.9, -0.7, -0.5]}
for blk, seed in [(126, 11), (252, 12), (63, 13)]:
    r = rlib.fit_w21(z, y, block=blk, nboot=999, seed=seed); r.pop('beta')
    out[f'W21_block{blk}'] = r
r = rlib.fit_w21(z, y); out['bin_share'] = (r['beta'] * np.diff(rlib.EDGES) / (r['beta'] * np.diff(rlib.EDGES)).sum()).round(3).tolist()
out['sum_slope'] = float((r['beta'] * np.diff(rlib.EDGES)).sum())
json.dump(out, open('c1.json', 'w'), indent=1, default=float)
for k, v in out.items(): print(k, v if not isinstance(v, dict) else {a: (round(b, 4) if isinstance(b, float) else b) for a, b in v.items()})
