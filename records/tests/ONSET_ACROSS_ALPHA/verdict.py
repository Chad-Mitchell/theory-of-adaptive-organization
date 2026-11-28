"""Locked verdict rules (PREREG.md section 5). Prints JSON."""
import json, numpy as np
from analyze import analyse
from theory import window_exponent
D = 0.267; Z = 1.959964
o = analyse('results.jsonl', (1.5, 2.5))
out = {}
for a in (1.5, 2.5):
    r = o[a]; rhos_v = [x for x, v in zip(r['rhos'], r['valid']) if v]
    if 'e' not in r: out[a] = dict(r, verdict='INCONCLUSIVE (validity)'); continue
    ep = window_exponent(a, rhos_v); e = r['e']; lo, hi = r['e_ci']
    v = 'PASS' if abs(e - ep) <= 0.15 * abs(ep) else ('MISS' if (ep < lo or ep > hi) else 'INCONCLUSIVE')
    out[a] = {k: x for k, x in r.items() if k != 'e_boot'}; out[a].update(e_pred=ep, verdict=v)
if all('e' in o[a] for a in (1.5, 2.5)):
    db = o[2.5]['e_boot'] - o[1.5]['e_boot']
    d = o[2.5]['e'] - o[1.5]['e']; se = float(np.nanstd(db))
    lo, hi = float(np.nanpercentile(db, 2.5)), float(np.nanpercentile(db, 97.5))
    dpred = out[2.5]['e_pred'] - out[1.5]['e_pred']
    if lo > dpred - D and hi < dpred + D: v = 'PASS'
    elif (lo > dpred or hi < dpred) and abs(d - dpred) >= D / 2: v = 'FAIL'
    else: v = 'INCONCLUSIVE'
    out['contrast'] = dict(delta=d, delta_pred=dpred, se=se, ci=[lo, hi], margin=D, verdict=v,
                           exploratory=bool(se > D / 2.80))
print(json.dumps(out, indent=1))
