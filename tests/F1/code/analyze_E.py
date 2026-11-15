"""Secondary arm E analysis (non-decisive for the F1 verdict)."""
import numpy as np, pandas as pd, json, statsmodels.formula.api as smf
from lifelines import CoxPHFitter
d=pd.read_csv('/workspace/gtao/tests/F1/data/analysis_dataset_E.csv').dropna(subset=['shockE'])
# risk window starts 2020-04-01: drop firms with event before then; re-base time
d=d[~((d.D==1)&(d['T']<91))].copy(); d['TE']=(d['T']-91).clip(lower=1)
d['zE']=np.log1p(d.shockE*d.rev_q_mean/d.B)
d['ltau']=np.log(d.tau); d['la']=np.log(d.assets)
for v in ['ltau','zE','la']: d['c_'+v]=d[v]-d[v].mean()
m=smf.ols('D ~ c_ltau*c_zE + c_la',d).fit(cov_type='HC1'); k='c_ltau:c_zE'
d['cx']=d.c_ltau*d.c_zE
c=CoxPHFitter().fit(d[['c_ltau','c_zE','cx','c_la','TE','D']],'TE','D')
R={'n':int(len(d)),'events':int(d.D.sum()),'LPM_inter':[float(m.params[k]),float(m.conf_int().loc[k,0]),float(m.conf_int().loc[k,1]),float(m.pvalues[k])],
   'LPM_all':{x:float(m.params[x]) for x in m.params.index},
   'cox':{x:[float(c.params_[x]),float(c.confidence_intervals_.loc[x].iloc[0]),float(c.confidence_intervals_.loc[x].iloc[1])] for x in c.params_.index}}
R['label']='SUPPORT' if R['LPM_inter'][1]>0 else ('AGAINST' if R['LPM_inter'][2]<=0 else 'NULL/INCONCLUSIVE')
json.dump(R,open('/workspace/gtao/tests/F1/results_E.json','w'),indent=1); print(json.dumps(R,indent=1))
