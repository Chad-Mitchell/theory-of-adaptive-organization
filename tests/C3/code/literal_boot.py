"""Bootstrap ratio CIs (1000, seed 20261113) for the literal-prereg outcome coding (L)."""
import numpy as np, pandas as pd, json
from lifelines import CoxPHFitter
d0 = pd.read_csv('/workspace/gtao/tests/C3/data/analysis_dataset.csv')
T0=pd.Timestamp('2023-07-01',tz='UTC'); TEND=pd.Timestamp('2025-10-31T23:59:59',tz='UTC')
arch=pd.to_datetime(d0.archivedAt,utc=True); inwin=arch.notna()&(arch>=T0)&(arch<=TEND)
lit=d0.flag_lc_before_t0 & ~inwin
d=d0.assign(E=np.where(lit,0,d0.E), T=np.where(lit,(TEND-T0).total_seconds()/86400,d0['T']))
rng=np.random.RandomState(20261113); bs=[]
for i in range(1000):
    s=d.iloc[rng.randint(0,len(d),len(d))]
    p=CoxPHFitter().fit(s[['ls','lB','ltau','T','E']],'T','E').params_; bs.append((p.lB/p.ls,p.ltau/p.ls))
bs=np.array(bs); out={'r_B_ci':np.percentile(bs[:,0],[2.5,97.5]).tolist(),'r_tau_ci':np.percentile(bs[:,1],[2.5,97.5]).tolist()}
json.dump(out,open('/workspace/gtao/tests/C3/literal_boot.json','w')); print(out)
