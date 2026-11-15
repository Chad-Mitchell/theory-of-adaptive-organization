"""LEARNSIM locked analysis.  Usage: python analyze.py RESULTS.jsonl THEORY_PREDICTIONS.json [MEASURED_AB.json] > out
Estimators (locked in PREREG.md section 6):
  N*hat(rho): seed-mean of D_rel(N) on the 17-point grid -> isotonic (non-decreasing) fit by PAVA ->
              last grid point with fitted value < 0 (j_last); valid iff fitted first point < 0 and last >= 0;
              ln N* linearly interpolated between j_last and j_last+1 on the fitted values.
  e_hat: OLS slope of ln N*hat on ln rho over valid rho.  CI: 2000 seed-bootstrap replicates (seeds resampled
         independently per rho; replicates with any invalid crossing among the valid set are dropped and counted).
"""
import sys, json, numpy as np
from collections import defaultdict

B = 2000
TOL = 0.15

def load(path):
    R = defaultdict(list)
    for line in open(path):
        d = json.loads(line)
        R[(d['learner'], d['arm'], d['cell'])].append(d)
    for k in R:
        R[k].sort(key=lambda d: d['seed'])
    return R

def mat(runs, key='D_rel'):
    return np.array([[r[key] for r in d['rows']] for d in runs])  # seeds x NG

def pava(y):
    """isotonic (non-decreasing) least-squares fit, pool-adjacent-violators."""
    v = list(map(float, y)); wts = [1.0] * len(v); idx = [[i] for i in range(len(v))]
    i = 0
    while i < len(v) - 1:
        if v[i] > v[i + 1]:
            nv = (v[i] * wts[i] + v[i + 1] * wts[i + 1]) / (wts[i] + wts[i + 1])
            v[i] = nv; wts[i] += wts[i + 1]; idx[i] += idx[i + 1]
            del v[i + 1], wts[i + 1], idx[i + 1]
            i = max(i - 1, 0)
        else:
            i += 1
    out = np.empty(len(y))
    for val, ii in zip(v, idx): out[ii] = val
    return out

def crossing(lnN, m):
    """onset = upward zero crossing of the isotonic (monotone) fit of seed-mean D_rel over ln N."""
    m = pava(m)
    if m[0] >= 0 or m[-1] < 0: return None
    neg = np.where(m < 0)[0]
    if len(neg) == 0: return None
    j = neg[-1]
    if j >= len(m) - 1: return None
    return lnN[j] + (0 - m[j]) / (m[j + 1] - m[j]) * (lnN[j + 1] - lnN[j])

def slope(x, y):
    return float(np.polyfit(x, y, 1)[0])

def ci(a):
    a = np.asarray(a); return [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]

def verdict(e, lo, hi, pred, tol=TOL):
    if abs(e - pred) <= tol * abs(pred): return 'PASS'
    if not (lo <= pred <= hi): return 'MISS'
    return 'INCONCLUSIVE'

def scan(R, learner, arm, rhos, key='D_rel', rng=None):
    cells = ['rho=%g' % r for r in rhos]
    data = {}
    for r, c in zip(rhos, cells):
        runs = R.get((learner, arm, c), [])
        if not runs: continue
        lnN = np.log([x['N'] for x in runs[0]['rows']])
        data[r] = (lnN, mat(runs, key), runs)
    est = {r: crossing(lnN, M.mean(0)) for r, (lnN, M, _) in data.items()}
    # bootstrap validity per rho
    boots = {r: [] for r in data}
    for b in range(B):
        for r, (lnN, M, _) in data.items():
            idx = rng.integers(M.shape[0], size=M.shape[0])
            boots[r].append(crossing(lnN, M[idx].mean(0)))
    valid = [r for r in data if est[r] is not None and np.mean([x is not None for x in boots[r]]) >= 0.9]
    out = {'nseeds': {str(r): data[r][1].shape[0] for r in data}, 'Nstar_hat': {str(r): (float(np.exp(est[r])) if est[r] is not None else None) for r in data},
           'Nstar_ci': {str(r): (ci(np.exp([x for x in boots[r] if x is not None])) if any(x is not None for x in boots[r]) else None) for r in data},
           'valid_rhos': valid}
    if len(valid) >= 2:
        x = np.log(valid); e = slope(x, [est[r] for r in valid])
        bs = []; dropped = 0
        for b in range(B):
            ys = [boots[r][b] for r in valid]
            if any(y is None for y in ys): dropped += 1; continue
            bs.append(slope(x, ys))
        out.update(e_hat=e, e_ci=ci(bs), boot_dropped=dropped, boot_slopes=bs)
    return out, data, est, boots

def logistic_n50(lnN, dec):
    """2-parameter logistic in ln N fitted by Newton MLE on pooled 0/1 decisions; returns ln N50 or None."""
    x = np.repeat(lnN[None, :], dec.shape[0], 0).ravel(); y = dec.ravel().astype(float)
    if y.mean() in (0.0, 1.0): return None
    xc = x - x.mean(); th = np.array([0.0, 1.0])
    for _ in range(100):
        z = np.clip(th[0] + th[1] * xc, -30, 30); p = 1 / (1 + np.exp(-z))
        g = np.array([np.sum(y - p), np.sum((y - p) * xc)])
        Wt = p * (1 - p) + 1e-9
        H = np.array([[Wt.sum(), (Wt * xc).sum()], [(Wt * xc).sum(), (Wt * xc * xc).sum()]])
        step = np.linalg.solve(H + 1e-9 * np.eye(2), g); th = th + step
        if np.abs(step).max() < 1e-8: break
    if th[1] <= 0: return None
    l50 = -th[0] / th[1] + x.mean()
    if l50 < lnN[0] or l50 > lnN[-1]: return None
    return float(l50)

def effort(tech, e):
    return 1.0 / e if tech == 'R' else e

def main():
    R = load(sys.argv[1]); TH = json.load(open(sys.argv[2]))
    MAB = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else None
    rhos = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32]
    techs = {'RR': ('R', 'R'), 'RRh': ('R', 'R'), 'AA': ('A', 'A'), 'AR': ('A', 'R'), 'RA': ('R', 'A')}
    rng = np.random.default_rng(2026)
    rep = {'primary': {}, 'contrasts': {}, 'V': {}, 'factorial': {}, 'findability': {}, 'robust_pop': {}, 'measured_ab': {}}
    learners = sorted(set(k[0] for k in R))
    store = {}
    for learner in learners:
        for arm in techs:
            if not any(k[0] == learner and k[1] == arm for k in R): continue
            o, data, est, boots = scan(R, learner, arm, rhos, 'D_rel', rng)
            th = TH['arms'][arm]
            v = o['valid_rhos']
            o['theory_Nstar'] = {str(r): th['Nstar'][rhos.index(r)] for r in rhos}
            o['Pi_ratio'] = {str(r): (o['Nstar_hat'][str(r)] / th['Nstar'][rhos.index(r)] if o['Nstar_hat'][str(r)] else None) for r in rhos if str(r) in o['Nstar_hat']}
            if len(v) >= 4 and np.log(max(v) / min(v)) >= np.log(10) and 'e_hat' in o:
                e_pred = slope(np.log(v), np.log([th['Nstar'][rhos.index(r)] for r in v]))
                o['e_pred'] = e_pred; o['verdict'] = verdict(o['e_hat'], *o['e_ci'], e_pred)
                o['rival_member_tech'] = th['rival_member_tech_e_g']
            else:
                o['verdict'] = 'INCONCLUSIVE (fewer than 4 valid rho spanning a decade)'
            # secondary: logistic N50 on CRN decisions
            l50 = {}
            for r, (lnN, M, _) in data.items():
                l50[r] = logistic_n50(lnN, M > 0)
            vv = [r for r in data if l50[r] is not None]
            o['logistic_N50'] = {str(r): (float(np.exp(l50[r])) if l50[r] is not None else None) for r in data}
            if len(vv) >= 2: o['logistic_slope'] = slope(np.log(vv), [l50[r] for r in vv])
            bs = o.pop('boot_slopes', None)
            store[(learner, arm)] = (o, data, est, boots, bs)
            (rep['primary'] if learner == 'es' else rep['robust_pop'])[arm] = o
    # contrasts (ES learner)
    def bsl(arm):
        return store[('es', arm)][4] if ('es', arm) in store else None
    if bsl('AA') and bsl('RR'):
        n = min(len(bsl('AA')), len(bsl('RR'))); d = np.array(bsl('AA')[:n]) - np.array(bsl('RR')[:n])
        pd = rep['primary']['AA'].get('e_pred', np.nan) - rep['primary']['RR'].get('e_pred', np.nan)
        dh = rep['primary']['AA']['e_hat'] - rep['primary']['RR']['e_hat']
        lo, hi = ci(d)
        rep['contrasts']['C1_AA_minus_RR'] = dict(diff=dh, ci=[lo, hi], pred=pd,
            rival_tech_independent_killed=bool(hi < -0.4), theory_miss=bool(not (lo <= pd <= hi) and abs(dh - pd) > 0.3))
    for arm in ['AR', 'RA']:
        o = rep['primary'].get(arm)
        if o and 'e_hat' in o:
            rv = TH['arms'][arm]['rival_member_tech_e_g']; lo, hi = o['e_ci']
            o['rival_killed'] = bool(not (lo <= rv <= hi) and abs(o['e_hat'] - rv) > 0.3)
    # V at emergent onset (common-tech arms)
    for arm in ['RR', 'RRh', 'AA']:
        if ('es', arm) not in store: continue
        o, data, est, boots, _ = store[('es', arm)]
        lt = techs[arm][0]; res = {}
        for r in o['valid_rhos']:
            lnN, M, runs = data[r]
            def Vhat(idx, lnNs):
                Lf = np.log([effort(lt, e) for i in idx for e in runs[i]['flat_eff']]).mean()
                j = int(np.argmin(np.abs(lnN - lnNs))); js = range(max(0, j - 4), min(len(lnN), j + 5))
                xs = np.array([lnN[jj] for i in idx for jj in js]); ys = np.log([effort(lt, runs[i]['lev_eff'][jj]) for i in idx for jj in js])
                p = np.polyfit(xs, ys, 1)
                return float(np.exp(np.polyval(p, lnNs) - Lf))
            n = len(runs); v0 = Vhat(range(n), est[r])
            bv = []
            for b in range(400):
                idx = rng.integers(n, size=n); lb = crossing(lnN, M[idx].mean(0))
                if lb is not None: bv.append(Vhat(idx, lb))
            vp = TH['arms'][arm]['V_at_Nstar'][rhos.index(r)]
            res[str(r)] = dict(V_hat=v0, ci=ci(bv), V_pred=vp)
        if res:
            lr = [np.log(x['V_hat'] / x['V_pred']) for x in res.values()]
            g = float(np.exp(np.mean(lr)))
            # bootstrap of the geometric-mean ratio: use per-rho CIs pooled conservatively (independent rho)
            sd = np.sqrt(np.sum([((np.log(x['ci'][1]) - np.log(x['ci'][0])) / 3.92) ** 2 for x in res.values()])) / len(res)
            glo, ghi = float(np.exp(np.log(g) - 1.96 * sd)), float(np.exp(np.log(g) + 1.96 * sd))
            vd = 'PASS' if abs(np.log(g)) <= np.log(1.15) else ('MISS' if not (glo <= 1 <= ghi) else 'INCONCLUSIVE')
            rep['V'][arm] = dict(per_rho=res, geo_mean_ratio=g, ratio_ci=[glo, ghi], verdict=vd)
    # factorial
    for arm in ['RR', 'RRh', 'AR', 'RA']:
        cells = {c: R.get(('es', arm, 'fact:' + c)) for c in ['base', 'shared_x2', 'private_x2', 'both_x2']}
        if not all(cells.values()): continue
        lnNs = {c: np.log([x['N'] for x in v[0]['rows']]) for c, v in cells.items()}
        Ms = {c: mat(v) for c, v in cells.items()}
        n = min(M.shape[0] for M in Ms.values())
        e0 = {c: crossing(lnNs[c], Ms[c][:n].mean(0)) for c in cells}
        bd = {c: [] for c in ['shared_x2', 'private_x2', 'both_x2']}
        for b in range(B):
            idx = rng.integers(n, size=n)
            eb = {c: crossing(lnNs[c], Ms[c][idx].mean(0)) for c in cells}
            for c in bd:
                if eb[c] is not None and eb['base'] is not None: bd[c].append(eb[c] - eb['base'])
        fr = TH['factorial'][arm]; out = {}
        for c, key in [('shared_x2', 'dlnN_shared'), ('private_x2', 'dlnN_private'), ('both_x2', 'dlnN_both')]:
            if e0[c] is None or e0['base'] is None: out[c] = dict(verdict='INCONCLUSIVE (no crossing)'); continue
            d = e0[c] - e0['base']; lo, hi = ci(bd[c]); p = fr[key]
            if c == 'both_x2' and abs(p) < 0.05:
                vd = 'PASS' if (lo <= 0 <= hi and abs(d) < 0.1) else ('MISS' if not (lo <= 0 <= hi) else 'INCONCLUSIVE')
            else:
                s = np.sign(p)
                vd = 'PASS' if (s * lo > 0 and s * hi > 0) else ('MISS' if (s * hi < 0) else 'INCONCLUSIVE')
            out[c] = dict(dlnN=d, ci=[lo, hi], pred=p, verdict=vd)
        if out.get('shared_x2', {}).get('verdict') == 'PASS' and out.get('private_x2', {}).get('verdict') == 'PASS':
            out['contingency_same_sign_rival_killed'] = True
        rep['factorial'][arm] = out
    # findability (ES learner): (a) no common random numbers, (b) perception noise, (c) tolerance rule (P10)
    for arm in ['RR', 'AA']:
        if ('es', arm) not in store: continue
        o2, *_ = scan(R, 'es', arm, rhos, 'D_rel_ind', rng)
        o2.pop('boot_slopes', None)
        f = {'no_CRN': {k: o2.get(k) for k in ['e_hat', 'e_ci', 'valid_rhos', 'Nstar_hat']}}
        data = store[('es', arm)][1]
        nz = {}
        for eps in [0.0, 0.001, 0.003, 0.01, 0.03]:
            sl = []; nv = []
            for rep_i in range(100 if eps > 0 else 1):
                l50 = {}
                for r, (lnN, M, _) in data.items():
                    l50[r] = logistic_n50(lnN, (M + eps * rng.standard_normal(M.shape)) > 0)
                vv = [r for r in data if l50[r] is not None]; nv.append(len(vv))
                if len(vv) >= 3: sl.append(slope(np.log(vv), [l50[r] for r in vv]))
            nz[str(eps)] = dict(mean_slope=(float(np.mean(sl)) if sl else None), slope_ci=(ci(sl) if len(sl) > 5 else None), mean_valid_rho=float(np.mean(nv)))
        f['perception_noise_logistic'] = nz
        tol = {}
        for eps in [0.003, 0.01, 0.03]:
            tol[str(eps)] = {str(r): float(np.mean(M[:, -1] > eps)) for r, (lnN, M, _) in data.items()}
        f['tolerance_rule_adoption_at_Nmax'] = tol
        f['P10_threshold'] = TH['P10']
        rep['findability'][arm] = f
    if MAB:
        for arm, key in [('RR', ('R', 'R')), ('AA', ('A', 'A')), ('AR', ('A', 'R')), ('RA', ('R', 'A'))]:
            o = rep['primary'].get(arm)
            if not o or 'e_hat' not in o: continue
            aL, bL = MAB[key[0]]['a'], MAB[key[0]]['b']; em = -(1 - bL) / (1 - aL)
            rep['measured_ab'][arm] = dict(e_from_measured_level_ab=em, e_hat=o['e_hat'], e_ci=o['e_ci'], verdict=verdict(o['e_hat'], *o['e_ci'], em))
    print(json.dumps(rep, indent=1, default=float))

if __name__ == '__main__':
    main()
