import numpy as np, pandas as pd, warnings, statsmodels.formula.api as smf
warnings.filterwarnings('ignore')
fs=[]
for coh,lf in [('C1','2014-07-01'),('C2','2019-07-01')]:
    d=pd.read_csv(f'data/measures_{coh}.csv')
    fs.append(d[(d.lastfiled>=lf)&d.tau.notna()&d.sigma.notna()&(d.sigma>0)&(d.B>0)&(d.assets>0)&(d.rev_q_mean>=2.5e6)].copy())
f=pd.concat(fs,ignore_index=True)
X=pd.DataFrame({'ls':np.log(f.sigma),'lb':np.log(f.B),'ltau':np.log(f.tau),'la':np.log(f.assets),'cik':f.cik.values,'cohort':f.cohort.values})
for v in ['ltau','la']: X['c_'+v]=X[v]-X[v].mean()
X['c_lsb']=(X.ls-X.lb)-(X.ls-X.lb).mean()
rng=np.random.default_rng(3)
specs={'base':'D ~ c_ltau*c_lsb + c_la + C(cohort)','flex':'D ~ c_ltau*c_lsb + c_la + I(c_lsb**2) + I(c_la**2) + c_la:c_lsb + c_ltau:c_la + I(c_ltau**2) + C(cohort)'}
for bt in [0.0,0.25]:
  rej={k:0 for k in specs}; N=150
  for r in range(N):
    lp=0.5*X.ls-0.5*X.lb+bt*X.ltau-0.2*X.la; lp-=lp.mean()
    lo,hi=-20,5
    for _ in range(40):
        mid=(lo+hi)/2; p=1-np.exp(-np.exp(mid+lp)*5); lo,hi=(mid,hi) if p.mean()<0.03 else (lo,mid)
    X['D']=(rng.random(len(X))<1-np.exp(-np.exp(mid+lp)*5)).astype(int)
    for k,fm in specs.items():
        m=smf.ols(fm,X).fit(cov_type='cluster',cov_kwds={'groups':X.cik})
        if m.conf_int().loc['c_ltau:c_lsb',0]>0: rej[k]+=1
  print(bt,{k:v/N for k,v in rej.items()},flush=True)
