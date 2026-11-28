"""MV10 gate for KERNEL-MEASURE design 2: run the LOCKED decision rule (decide.rule) on the simulated planned data
(power2/*.json; n = 9276, 100 reps per condition), adding prediction error N(0, SIG_PRED) per rep."""
import json, glob, numpy as np, decide
rng = np.random.default_rng(20261128)
out = {}
for f in sorted(glob.glob('power2/*.json')):
    d = json.load(open(f)); c = d['cond']
    if c.startswith('H0_0_'): continue
    rr = [decide.rule(r['W21'], r['W21_sd'], decide.W21_PRED + rng.normal(0, decide.SIG_PRED)) for r in d['res']]
    v = [x['verdict'] for x in rr]
    out[c] = {k: v.count(k) / len(v) for k in ('PASS', 'FAIL', 'INCONCLUSIVE')}
    out[c]['low_resolution'] = float(np.mean([x['low_resolution'] for x in rr]))
    print(c, out[c])
json.dump(out, open('gate.json', 'w'), indent=1)
