"""LOCKED data run (pick 33): proxy-validity checks of the pick-28 VIX kernel. Own code (plib); reads only the data
files of tests/KERNEL_MEASURE/data. Rules: ../KERNEL_PROXY_PREREG.md."""
import numpy as np, csv, json, math
from plib import *
DD = '../../../tests/KERNEL_MEASURE/data/'
END = '2026-10-30'; BLOCK = 126; NB = 999; SEED = 20261133
P1_PRED, SIG_PRED, DELTA = 0.2579, 0.0264, 0.13          # c0_power.json W_bar mean; locked sigma_pred; locked band
P2_REF, MARGIN = 0.0218, 0.065                           # c0_power.json D_zL0.45 mean; proxy equivalence margin
RIVALS = {'R1_kalman_alpha2': 0.000, 'R2_flat_1_5_22': 0.012, 'R3_matching': 0.725}
g = [r for r in csv.DictReader(open(DD + 'GSPC_ohlc.csv')) if r['date'] <= END]
vix = {r['observation_date']: r['VIXCLS'] for r in csv.DictReader(open(DD + 'VIXCLS.csv'))}
dates = [r['date'] for r in g]
O, Hh, Lo, C = (np.array([float(r[k]) for r in g]) for k in ('open', 'high', 'low', 'close'))
park = np.log(Hh / Lo) ** 2 / (4 * math.log(2))
y = np.log(park); n = len(y)
z = np.array([2 * math.log(float(vix[d])) if vix.get(d, '') not in ('', '.') else np.nan for d in dates])
import os
if os.environ.get('DRY'):                                 # dry run on simulated data (no outcome read)
    rr = np.random.default_rng(1); _, ys = driver(n + 2000, rr); ys = ys[2000:]; park = np.exp(ys); y = ys
    z = np.convolve(ys, blp_weights(1000))[:n] - 3 + 0.0 * ys
    print('DRY RUN (simulated)')
out = {'n': n, 'first': dates[0], 'last': dates[-1], 'nonfinite_y': int((~np.isfinite(y)).sum()), 'vix_missing': int(np.isnan(z).sum())}

def boot_fit(X, targets, rows, nb=NB, seed=SEED):
    """OLS W21 for each target on common rows; non-overlapping block bootstrap (blocks of BLOCK rows)."""
    ok = rows.copy()
    for v in targets.values(): ok &= np.isfinite(v)
    Xo = X[ok]; T = {k: v[ok] for k, v in targets.items()}
    m = len(Xo) // BLOCK * BLOCK; Xo = Xo[:m]; T = {k: v[:m] for k, v in T.items()}; nbk = m // BLOCK
    Xb = Xo.reshape(nbk, BLOCK, -1); XtX = np.einsum('bti,btj->bij', Xb, Xb)
    Xty = {k: np.einsum('bti,bt->bi', Xb, v.reshape(nbk, BLOCK)) for k, v in T.items()}
    def est(idx):
        A = XtX[idx].sum(0); res = {}
        for k in T:
            beta = np.linalg.solve(A, Xty[k][idx].sum(0)); mass = beta[1:] * np.diff(EDGES)
            res[k] = (W21(beta), mass.sum(), mass / mass.sum())
        return res
    full = est(np.arange(nbk)); rng = np.random.default_rng(seed)
    bs = [est(rng.integers(0, nbk, nbk)) for _ in range(nb)]
    o = {'rows': int(m), 'blocks': int(nbk)}
    for k in T:
        o[k] = {'W21': float(full[k][0]), 'sd': float(np.std([b[k][0] for b in bs], ddof=1)),
                'sum_beta': float(full[k][1]), 'bin_share': [round(float(s), 4) for s in full[k][2]]}
    o['_boot'] = {k: np.array([b[k][0] for b in bs]) for k in T}
    return o

X, t = binmat(y)
tgt = {'ybar': fut_mean(y)[t], 'L': np.log(fut_mean(park))[t], 'z': z[t]}
rows = t <= n - H - 1
A = boot_fit(X, tgt, rows)
bz, bL, bb = A['_boot']['z'], A['_boot']['L'], A['_boot']['ybar']
# P1: VIX-free realized-target kernel (rows with the target only)
A1 = boot_fit(X, {'ybar': tgt['ybar']}, rows)
W = A1['ybar']['W21']; s = math.hypot(A1['ybar']['sd'], SIG_PRED); D = W - P1_PRED
ci = (W - 1.96 * A1['ybar']['sd'], W + 1.96 * A1['ybar']['sd'])
excl = all(not (ci[0] <= v <= ci[1]) for v in RIVALS.values())
v1 = 'PASS' if abs(D) + 1.96 * s <= DELTA and excl else ('FAIL' if abs(D) - 1.96 * s > DELTA else 'INCONCLUSIVE')
out['P1'] = {'W21': W, 'boot_sd': A1['ybar']['sd'], 'pred': P1_PRED, 'D': D, 'sigma_D': s, 'CI_D': [D - 1.96 * s, D + 1.96 * s],
             'W_CI': ci, 'rivals_excluded': excl, 'verdict': v1, 'low_resolution': s > DELTA / 3.24,
             'sum_beta': A1['ybar']['sum_beta'], 'bin_share': A1['ybar']['bin_share'], 'rows': A1['rows']}
# P2: proxy gap, paired on common rows
d = A['z']['W21'] - A['L']['W21']; sd = float(np.std(bz - bL, ddof=1)); e = d - P2_REF
v2 = 'SMALL' if abs(e) + 1.96 * sd <= MARGIN else ('DISTORTS' if abs(e) - 1.96 * sd > MARGIN else 'UNRESOLVED')
out['P2'] = {'W_z': A['z']['W21'], 'W_L': A['L']['W21'], 'W_ybar': A['ybar']['W21'], 'Delta_zL': d, 'sd': sd, 'ref': P2_REF,
             'CI': [e - 1.96 * sd, e + 1.96 * sd], 'verdict': v2, 'Delta_Lybar': A['L']['W21'] - A['ybar']['W21'],
             'sd_Lybar': float(np.std(bL - bb, ddof=1)), 'rows': A['rows']}
out['common_rows'] = {k: {kk: vv for kk, vv in A[k].items()} for k in ('ybar', 'L', 'z')}
# C4 overnight, 2008-01-02 on (Yahoo open == previous close for most days before 2008)
i0 = dates.index(next(dd for dd in dates if dd >= '2008-01-02'))
eq = float(np.mean(np.abs(O[i0:] - C[i0 - 1:-1]) < 1e-6))
ron2 = np.zeros(n); ron2[1:] = np.log(O[1:] / C[:-1]) ** 2
ycc = np.log(park + ron2)
X2, t2 = binmat(ycc)
post = t >= i0 + LMAX - 1                              # all 504 lags inside the overnight-valid span
B1 = boot_fit(X, {'z': z[t], 'L': tgt['L'], 'Lcc': np.log(fut_mean(park + ron2))[t]}, rows & post)
B2 = boot_fit(X2, {'z': z[t2], 'Lcc': np.log(fut_mean(park + ron2))[t2]}, (t2 <= n - H - 1) & post)
out['C4_overnight'] = {'span_from': dates[i0], 'open_eq_prevclose_frac': eq,
    'driver_intraday': {k: {kk: B1[k][kk] for kk in ('W21', 'sd', 'sum_beta')} for k in ('z', 'L', 'Lcc')},
    'driver_close_to_close': {k: {kk: B2[k][kk] for kk in ('W21', 'sd', 'sum_beta')} for k in ('z', 'Lcc')},
    'rows': B1['rows'], 'mean_overnight_share': float(np.mean(ron2[i0:] / (park[i0:] + ron2[i0:])))}
# C5 Gaussian premise / jumps (descriptive)
dy = np.diff(y); k4 = float(np.mean((dy - dy.mean()) ** 4) / dy.var() ** 2)
d21 = y[21:] - y[:-21]; k21 = float(np.mean((d21 - d21.mean()) ** 4) / d21.var() ** 2)
lo, hi = np.percentile(y, [0.5, 99.5]); yw = np.clip(y, lo, hi); Xw, _ = binmat(yw)
Cw = boot_fit(Xw, {'z': z[t]}, rows, nb=299)
crisis = np.array([('2008-09-01' <= dates[i] <= '2009-06-30') or ('2020-02-15' <= dates[i] <= '2020-06-30') for i in t])
Cc = boot_fit(X, {'z': z[t]}, rows & ~crisis, nb=299)
out['C5_gauss'] = {'kurt_daily_dy': k4, 'kurt_21d_dy': k21, 'W_z_winsor_0.5_99.5': Cw['z']['W21'], 'sd_w': Cw['z']['sd'],
                   'W_z_no_crisis': Cc['z']['W21'], 'sd_nc': Cc['z']['sd']}
for o in (A, A1, B1, B2, Cw, Cc): o.pop('_boot', None)
json.dump(out, open('c1_data_dry.json' if os.environ.get('DRY') else 'c1_data.json', 'w'), indent=1, default=float)
print(json.dumps({k: out[k] for k in ('n', 'last', 'nonfinite_y', 'vix_missing', 'P1', 'P2', 'C4_overnight', 'C5_gauss')}, indent=1, default=float))
