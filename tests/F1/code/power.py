"""Power analysis on the real pre-2020 predictor matrix with simulated outcomes (no outcome data)."""
import numpy as np, pandas as pd, warnings, json
import statsmodels.formula.api as smf
from lifelines import CoxPHFitter
warnings.filterwarnings('ignore')
fs=[]
for coh,lf in [('C1','2014-07-01'),('C2','2019-07-01')]:
    d=pd.read_csv(f'/workspace/gtao/tests/F1/data/measures_{coh}.csv')
    fs.append(d[(d.lastfiled>=lf)&d.tau.notna()&d.sigma.notna()&(d.sigma>0)&(d.B>0)&(d.assets>0)&(d.rev_q_mean>=2.5e6)].copy())
f=pd.concat(fs)
f=f.sample(frac=0.8,random_state=1)  # approx. post-SIC-filter n
X=pd.DataFrame({'ls':np.log(f.sigma),'lb':np.log(f.B),'ltau':np.log(f.tau),'la':np.log(f.assets)}).reset_index(drop=True)
for c in X: X[c]=X[c]
rng=np.random.default_rng(7); out={}
for rate in [0.025,0.04]:
  for bt in [0.0,0.25,0.5]:
    hits=0; ints=0; N=150
    for r in range(N):
        lp=0.5*X.ls-0.5*X.lb+bt*X.ltau-0.2*X.la; lp=lp-lp.mean()
        # exponential hazard over 5 years; calibrate baseline to target event rate
        lo,hi=-20,5
        for _ in range(40):
            mid=(lo+hi)/2; p=1-np.exp(-np.exp(mid+lp)*5)
            lo,hi=(mid,hi) if p.mean()<rate else (lo,mid)
        t=rng.exponential(1/np.exp(mid+lp)); D=(t<5).astype(int); T=np.minimum(t,5)
        dd=X.assign(T=T,D=D)
        c=CoxPHFitter().fit(dd,'T','D'); 
        if c.summary.loc['ltau','p']<0.05 and c.params_['ltau']>0: hits+=1
        for v in ['ltau','la']: dd['c_'+v]=dd[v]-dd[v].mean()
        dd['c_lsb']=(dd.ls-dd.lb)-(dd.ls-dd.lb).mean()
        m=smf.ols('D ~ c_ltau*c_lsb + c_la',dd).fit(cov_type='HC1')
        if m.conf_int().loc['c_ltau:c_lsb',0]>0: ints+=1
    out[f'rate{rate}_bt{bt}']={'n':len(X),'events_mean':float(rate*len(X)),'power_tau':hits/N,'power_P2_inter':ints/N}
    print(rate,bt,out[f'rate{rate}_bt{bt}'],flush=True)
json.dump(out,open('/workspace/gtao/tests/F1/power/power.json','w'),indent=1)
