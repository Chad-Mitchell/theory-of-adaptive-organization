"""POST-LOCK (written after outcomes were seen; labelled as such in RESULTS.md).
Fixes two bugs in the locked analyze.py where the CODE disagreed with the locked PREREG TEXT; the text governs:
 (1) factorial MISS rule used s*hi<0 for both signs; the text says MISS only if the CI excludes 0 on the WRONG side.
 (2) measured-(a,b) verdicts ignored the '>=4 valid rho spanning a decade' requirement of section 6.
Also adds (3) the C1 predicted difference over the common valid rho set, and (4) per-seed noise of D_rel vs the prize."""
import json, numpy as np
import analyze as A, theory as T
d = json.load(open('ANALYSIS_1.json')); out = {}
fx = {}
for arm, cells in d['factorial'].items():
    fx[arm] = {}
    for c, v in cells.items():
        if not isinstance(v, dict) or 'dlnN' not in v: fx[arm][c] = v; continue
        lo, hi = v['ci']; p = v['pred']
        if c == 'both_x2' and abs(p) < 0.05:
            vd = 'PASS' if (lo <= 0 <= hi and abs(v['dlnN']) < 0.1) else ('MISS' if not (lo <= 0 <= hi) else 'INCONCLUSIVE')
        else:
            s = np.sign(p)
            vd = 'PASS' if (s * lo > 0 and s * hi > 0) else ('MISS' if (s * lo < 0 and s * hi < 0) else 'INCONCLUSIVE')
        fx[arm][c] = dict(v, verdict_locked_code=v['verdict'], verdict=vd)
out['factorial_fixed'] = fx
out['measured_ab_fixed'] = {a: dict(v, verdict_locked_code=v['verdict'], verdict='INCONCLUSIVE (valid rho span < 1 decade)')
                            for a, v in d['measured_ab'].items()}
v = sorted(set(d['primary']['RR']['valid_rhos']) & set(d['primary']['AA']['valid_rhos']))
sl = lambda arm: float(np.polyfit(np.log(v), np.log([T.nstar(*{'RR': ('R', 'R'), 'AA': ('A', 'A')}[arm], r, 1.0, 0.0) for r in v]), 1)[0])
out['C1_pred_diff_on_valid_set'] = dict(rhos=v, pred_RR=sl('RR'), pred_AA=sl('AA'), pred_diff=sl('AA') - sl('RR'))
R = A.load('results_es.jsonl'); nz = {}
for arm, b in [('RR', 0.5), ('AA', 1 / 3), ('AR', 0.5), ('RA', 1 / 3)]:
    nz[arm] = {}
    for r in [0.01, 0.02, 0.04, 0.08, 0.16, 0.32]:
        M = A.mat(R[('es', arm, 'rho=%g' % r)])
        nz[arm][str(r)] = dict(sd_seed_D_rel_at_grid_centre=float(M[:, 8].std(ddof=1)), se_mean=float(M[:, 8].std(ddof=1) / 4),
                               prize_b_rho=b * r, max_mean_D_rel=float(M.mean(0).max()))
out['noise_vs_prize'] = nz
print(json.dumps(out, indent=1))
