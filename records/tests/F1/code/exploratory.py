"""EXPLORATORY (not preregistered), run after seeing primary results."""
import json, numpy as np, pandas as pd, warnings, statsmodels.formula.api as smf
from lifelines import CoxPHFitter
warnings.filterwarnings('ignore')
d=pd.read_csv('data/analysis_dataset.csv')
d['ls']=np.log(d.sigma); d['lb']=np.log(d.B); d['ltau']=np.log(d.tau); d['la']=np.log(d.assets)
X={}
def cox(df,cols,strata=['cohort']):
    c=CoxPHFitter().fit(df[cols+['T','D','cik']+strata],'T','D',strata=strata,cluster_col='cik'); return c
def row(c,k): return [round(float(c.params_[k]),3),round(float(c.confidence_intervals_.loc[k].iloc[0]),3),round(float(c.confidence_intervals_.loc[k].iloc[1]),3)]
X['sd_ln_tau']=float(d.ltau.std()); X['HR_per_doubling_tau']=float(np.exp(0.693*0.3545))
# 1 industry: strata = cohort x SIC 1-digit
d['sic1']=(pd.to_numeric(d.sic)//1000).astype(int); d['cs']=d.cohort+'_'+d.sic1.astype(str)
c=CoxPHFitter().fit(d[['ls','lb','ltau','la','T','D','cik','cs']],'T','D',strata=['cs'],cluster_col='cik'); X['ind_strata']={k:row(c,k) for k in ['ls','lb','ltau']}
# 2 tau vs simple margin level: tau high may proxy thin/negative margins
d['margin']=(d.oi4/(4*d.rev_q_mean)).clip(-2,1)
s=d.dropna(subset=['margin']); c=cox(s,['ls','lb','ltau','la','margin']); X['plus_margin']={k:row(c,k) for k in ['ltau','margin']}
# 3 loss firm indicator
s['loss']=(s.oi4<0).astype(int); c=cox(s,['ls','lb','ltau','la','loss']); X['plus_loss']={k:row(c,k) for k in ['ltau','loss']}
# 4 split by impact vs lambda: which part of tau carries it
d['l_noimpact']=np.log(1+np.clip(1-d.impact,0,None)); d['l_lam']=np.log(d.lam.clip(0.01))
c=cox(d,['ls','lb','la','l_noimpact','l_lam']); X['tau_parts']={k:row(c,k) for k in ['l_noimpact','l_lam']}
# 5 P2 by cohort
for coh in ['C1','C2']:
    s=d[d.cohort==coh].copy()
    for v in ['ltau','la']: s['c_'+v]=s[v]-s[v].mean()
    s['c_lsb']=(s.ls-s.lb)-(s.ls-s.lb).mean()
    m=smf.ols('D ~ c_ltau*c_lsb + c_la + I(c_lsb**2) + I(c_la**2) + I(c_ltau**2) + c_la:c_lsb + c_ltau:c_la',s).fit(cov_type='HC1')
    k='c_ltau:c_lsb'; X[f'P2_{coh}']=[round(float(m.params[k]),4),round(float(m.conf_int().loc[k,0]),4),round(float(m.conf_int().loc[k,1]),4)]
# 6 index model fit: restricted with free tau weight
for w in [0.5,1.0,1.5]:
    d['idx']=d.ls-d.lb+w*d.ltau; c=CoxPHFitter().fit(d[['idx','la','T','D','cohort']],'T','D',strata=['cohort']); X[f'idx_w{w}_LL']=round(float(c.log_likelihood_),2)
# 7 risk table: event rate by sigma/B tercile x tau tercile
d['lsb']=d.ls-d.lb; d['tsb']=pd.qcut(d.lsb,3,labels=['lowSB','midSB','highSB']); d['tt']=pd.qcut(d.ltau.rank(method='first'),3,labels=['fast','mid','slow'])
X['rate_table_pct']=(d.pivot_table(index='tsb',columns='tt',values='D',aggfunc='mean')*100).round(1).to_dict()
X['n_table']=d.pivot_table(index='tsb',columns='tt',values='D',aggfunc='size').to_dict()
json.dump(X,open('exploratory.json','w'),indent=1,default=str); print(json.dumps(X,indent=1,default=str))
