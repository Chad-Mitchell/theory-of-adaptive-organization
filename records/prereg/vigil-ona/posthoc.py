"""POST-HOC diagnostics (written after seeing results_real.json; not part of the locked rules)."""
import json, math, numpy as np, pandas as pd, ona_analyze as o
D = o.load_nodes(); D['krackhardt'] = o.krack_spans(D); L = o.load_layers(); out = {}
# 1. Lazega: does partner x outside survive a seniority (years with firm) x outside control?
l = pd.read_csv(f'{o.RAW}/lz/ELattr.dat', sep=r'\s+', header=None,
                names=['id', 'status', 'gender', 'office', 'yrs', 'age', 'practice', 'school']); l['id'] -= 1
for lay in ['advice', 'cowork']:
    d = o.dyads(D['lazega'], L['lazega'][lay])
    yrs = l.set_index('id').yrs; age = l.set_index('id').age
    d['sen_x_out'] = ((d.i.map(yrs) - yrs.mean()) / yrs.std()) * d.out
    d['age_x_out'] = ((d.i.map(age) - age.mean()) / age.std()) * d.out
    out[f'lazega_{lay}_ctrl_seniority'] = o.logit_fe(d, extra_terms=('a_hi', 'a_eq', 'sen_x_out'))
    out[f'lazega_{lay}_ctrl_sen_age'] = o.logit_fe(d, extra_terms=('a_hi', 'a_eq', 'sen_x_out', 'age_x_out'))
    # within-status: seniority alone among associates / partners (does seniority itself tilt outward?)
# 2. H3 robustness
tabs = {n: o.node_table(D[n], L[n]['advice']) for n in ['krackhardt', 'consulting', 'manufacturing']}
for drop in tabs:
    out[f'H3_without_{drop}'] = o.h3({k: v for k, v in tabs.items() if k != drop})
t = tabs['manufacturing']; out['H3_manuf_without_top_node'] = o.h3({**tabs, 'manufacturing': t[t.N < 76]})
out['H3_manuf_without_levels_1_2'] = o.h3({**tabs, 'manufacturing': t[t.N < 20]})
# H3 specificity: same elasticity for INSIDE-unit seeking (generic activity would give the same slope)
tin = {k: v.assign(y_out=v.y_in, n_out=v.n_in)[v.n_in > 0] for k, v in tabs.items()}
out['H3_inside_unit_same_model'] = o.h3(tin)
json.dump(out, open('posthoc.json', 'w'), indent=1, default=float)
for k, v in out.items(): print(k, {a: (round(b, 3) if isinstance(b, float) else b) for a, b in (v or {}).items()})
