"""PREREG_2 gated analysis.  Usage: python analyze2.py results_es.jsonl results_ext.jsonl PREDICTIONS_2.json"""
import sys, json, numpy as np
import analyze as A
R = A.load(sys.argv[1])
for k, v in A.load(sys.argv[2]).items(): R[k] = v
P = json.load(open(sys.argv[3])); rng = np.random.default_rng(2027); rep = {}
for arm, p in P['arms'].items():
    rhos = p['gated_rhos']
    o, data, est, boots = A.scan(R, 'es', arm, rhos, 'D_rel', rng)
    bs = o.pop('boot_slopes', None); v = o['valid_rhos']
    span = np.log10(max(v) / min(v)) if len(v) >= 2 else 0
    r = dict(scan=o, gate_ok=bool(len(v) >= 3 and span >= 0.6))
    if r['gate_ok'] and 'e_hat' in o:
        idx = [rhos.index(x) for x in v]
        sl = lambda y: float(np.polyfit(np.log(v), np.log([y[i] for i in idx]), 1)[0])
        ep, er = sl(p['Nstar_pred']), sl(p['Nstar_rival'])
        se = float(np.std(bs)); gap = abs(ep - er)
        r.update(e_pred=ep, e_rival=er, se=se, MV8_power_ok=bool(gap == 0 or se <= gap / 2.8))
        r['verdict'] = A.verdict(o['e_hat'], *o['e_ci'], ep)
        if gap > 0:
            lo, hi = o['e_ci']; r['rival_killed'] = bool(not (lo <= er <= hi) and abs(o['e_hat'] - er) > 0.3)
            if not r['MV8_power_ok']: r['verdict'] = 'INCONCLUSIVE (MV8 power gate failed)'
        r['Pi_ratio_vs_measured_pred'] = {str(x): o['Nstar_hat'][str(x)] / p['Nstar_pred'][rhos.index(x)] for x in v}
    else:
        r['verdict'] = 'INCONCLUSIVE (selection-gated set has <3 valid rho or <0.6 decade)'
    rep[arm] = r
ar, ra = rep.get('AR', {}), rep.get('RA', {})
rep['T1_8_level_class_sets_exponent'] = ('PASS' if ar.get('verdict') == 'PASS' and ra.get('verdict') == 'PASS' and ar.get('rival_killed') and ra.get('rival_killed')
                                         else ('MISS' if 'MISS' in (ar.get('verdict'), ra.get('verdict')) else 'NOT PASSED'))
print(json.dumps(rep, indent=1, default=float))
