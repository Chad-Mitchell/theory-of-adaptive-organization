"""POST-LOCK, EXPLORATORY descriptives for the interpretation section (no verdicts). Imports locked code unchanged."""
import json, os, sys, collections, numpy as np
from scipy import stats
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,os.path.join(HERE,'..','code'))
import analyze as A, addendum as AD
wf,pinned,fu,fo,um=A.build_real(); units=A.to_units(wf,fu); flat=[u for u in units if not u['is_level']]
for u in flat: u['q'],u['m']=A.drift(u['x'])
E=np.array([u['E'] for u in flat]); q=np.array([u['q'] for u in flat])
k=np.array([np.nansum(np.abs(np.diff(u['x']))) for u in flat])
fail=np.array([np.nanmean(u['x']) for u in flat])
sp=[d for u in flat for d in AD.spells(u['x'])]
out=dict(n_flat=len(flat), share_E_1_or_7=float(np.mean(np.isin(np.round(E,2),[1.0,7.0]))),
 spearman_E_q=float(stats.spearmanr(E,q)[0]), median_q_per_week=float(np.median(q)), share_units_zero_changes=float(np.mean(k==0)),
 median_changes_per_unit=float(np.median(k)), median_failure_share=float(np.median(fail)),
 spell_quantiles_weeks={p:float(np.percentile(sp,p)) for p in (50,75,90,99)}, n_spells=len(sp),
 share_spells_len1=float(np.mean(np.array(sp)==1)))
json.dump(out,open(os.path.join(HERE,'descriptives.json'),'w'),indent=1); print(json.dumps(out,indent=1))
