"""Make a SIMULATED analysis dataset (fake outcomes) to dry-run analyze.py before real outcomes exist."""
import pandas as pd, numpy as np
fs=[]
for coh,lf in [('C1','2014-07-01'),('C2','2019-07-01')]:
    d=pd.read_csv(f'/workspace/gtao/tests/F1/data/measures_{coh}.csv')
    fs.append(d[(d.lastfiled>=lf)&d.tau.notna()&d.sigma.notna()&(d.sigma>0)&(d.B>0)&(d.assets>0)&(d.rev_q_mean>=2.5e6)].copy())
f=pd.concat(fs,ignore_index=True); rng=np.random.default_rng(1)
lp=0.5*np.log(f.sigma)-0.5*np.log(f.B)+0.25*np.log(f.tau)-0.2*np.log(f.assets); lp-=lp.mean()
h=np.exp(-4.3+lp); t=rng.exponential(1/h)*365; f['D']=(t<1826).astype(int); f['T']=np.minimum(t,1826).astype(int).clip(1)
f['D2']=np.maximum(f.D,(rng.random(len(f))<0.03).astype(int)); f['T2']=f['T']
f.to_csv('/workspace/gtao/tests/F1/power/sim_dataset.csv',index=False); print(len(f),f.D.sum())
