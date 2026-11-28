"""Re-derive the data numbers of KERNEL_PROXY_REVIEW.md with own code (rlib). Own seeds; locked block 126 / 999 reps,
plus block-length and seed sensitivity of the P1 slack."""
import numpy as np, json, math
from rlib import *
g = load(); n = len(g); y = g['y'].values; z = g['z'].values; park = g['park'].values
X, t = design(y)
ybar = future_mean(y)[t]; L = np.log(future_mean(park))[t]; zz = z[t]
out = {'n': n, 'last': g['date'].iloc[-1], 'vix_missing_in_rows': int(np.isnan(zz).sum())}
okT = np.isfinite(ybar)
# P1 rows: target present
full, Wd, Sd, m = block_boot(X[okT], {'ybar': ybar[okT]}, seed=11)
Wb = full['ybar'][0]; sd = Wd['ybar'].std(ddof=1)
def p1(Wb, sd, pred=0.2579, sp=0.0264):
    s = math.hypot(sd, sp); D = Wb - pred
    return {'W': Wb, 'boot_sd': sd, 'D': D, 'sigma_D': s, 'stat': abs(D) + 1.96 * s, 'slack': 0.13 - (abs(D) + 1.96 * s),
            'verdict': 'PASS' if abs(D) + 1.96 * s <= 0.13 else ('FAIL' if abs(D) - 1.96 * s > 0.13 else 'INCONCLUSIVE')}
out['P1_rows'] = int(m); out['P1_untruncated_W'] = W(ols(X[okT], ybar[okT])); out['P1_rows_untrunc'] = int(okT.sum())
out['P1'] = p1(Wb, sd); out['P1']['sum_beta'] = full['ybar'][1]
sens = {}
for blk in (63, 126, 252):
    for sd_seed in (11, 12, 13):
        f, Wd2, _, _ = block_boot(X[okT], {'ybar': ybar[okT]}, block=blk, seed=sd_seed)
        r = p1(f['ybar'][0], Wd2['ybar'].std(ddof=1)); sens[f'b{blk}_s{sd_seed}'] = {k: r[k] for k in ('W', 'boot_sd', 'stat', 'verdict')}
out['P1_sensitivity'] = sens
# joint-sigma variant (ledger-139 reviewer's joint sigma_pred 0.023)
out['P1_sigma_pred_0.023'] = p1(Wb, sd, sp=0.023)
# common rows: z, ybar, L
ok = okT & np.isfinite(zz) & np.isfinite(L)
full, Wd, Sd, m = block_boot(X[ok], {'z': zz[ok], 'ybar': ybar[ok], 'L': L[ok]}, seed=21)
cr = {k: {'W': full[k][0], 'W_sd': Wd[k].std(ddof=1), 'sum_beta': full[k][1], 'sum_sd': Sd[k].std(ddof=1),
          'bin_share': [round(float(s), 4) for s in full[k][2]]} for k in full}
cr['rows'] = int(m)
cr['z_minus_ybar'] = {'W': full['z'][0] - full['ybar'][0], 'sd': (Wd['z'] - Wd['ybar']).std(ddof=1),
                      'sum': full['z'][1] - full['ybar'][1], 'sum_sd': (Sd['z'] - Sd['ybar']).std(ddof=1)}
cr['z_minus_L'] = {'W': full['z'][0] - full['L'][0], 'sd': (Wd['z'] - Wd['L']).std(ddof=1),
                   'sum': full['z'][1] - full['L'][1], 'sum_sd': (Sd['z'] - Sd['L']).std(ddof=1)}
cr['L_minus_ybar'] = {'W': full['L'][0] - full['ybar'][0], 'sd': (Wd['L'] - Wd['ybar']).std(ddof=1)}
e = cr['z_minus_L']['W'] - 0.0218; s = cr['z_minus_L']['sd']
cr['P2'] = {'e': e, 'sd': s, 'verdict': 'SMALL' if abs(e) + 1.96 * s <= 0.065 else ('DISTORTS' if abs(e) - 1.96 * s > 0.065 else 'UNRESOLVED')}
# exact linearity check of the identity in sample: beta(z) - beta(ybar) == beta(z - ybar)
bz, bb, bd = ols(X[ok], zz[ok]), ols(X[ok], ybar[ok]), ols(X[ok], zz[ok] - ybar[ok])
cr['identity_maxabs'] = float(np.abs(bz - bb - bd).max())
dk = bd[1:] * WID; cr['distortion_kernel'] = {'mass': float(dk.sum()), 'tail': float(dk[TAIL].sum()),
                                             'W_of_distortion': float(dk[TAIL].sum() / dk.sum())}
out['common'] = cr
# overnight, 2008-01-02 on, all 504 lags in span
i0 = int(np.argmax(g['date'].values >= '2008-01-02'))
ycc = np.log(park + g['on2'].values)
X2, t2 = design(ycc)
post = t >= i0 + MAXAGE
Lcc = np.log(future_mean(park + g['on2'].values))[t]
ok1 = okT & np.isfinite(zz) & post & np.isfinite(Lcc)
f1, W1, S1, m1 = block_boot(X[ok1], {'z': zz[ok1], 'Lcc': Lcc[ok1], 'L': L[ok1]}, seed=31)
ok2 = ok1  # same t indexing (t2 == t)
assert (t2 == t).all()
f2, W2, S2, m2 = block_boot(X2[ok2], {'z': zz[ok2], 'Lcc': Lcc[ok2]}, seed=32)
out['overnight'] = {'rows': int(m1), 'from': g['date'].iloc[i0],
    'intraday_driver': {k: {'W': f1[k][0], 'sd': W1[k].std(ddof=1), 'sum': f1[k][1], 'sum_sd': S1[k].std(ddof=1)} for k in f1},
    'cc_driver': {k: {'W': f2[k][0], 'sd': W2[k].std(ddof=1), 'sum': f2[k][1], 'sum_sd': S2[k].std(ddof=1)} for k in f2},
    'mean_overnight_share': float(np.mean((g['on2'] / (g['park'] + g['on2'])).values[i0:]))}
json.dump(out, open('r1_data.json', 'w'), indent=1, default=float)
print(json.dumps(out, indent=1, default=float))
