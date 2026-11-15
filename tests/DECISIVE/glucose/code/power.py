# Power + theory-implied slope for glucose, predictors only. Tabulate G(z)=rate*tau for the smooth process,
# then simulate NB counts per subject using first-block length as a proxy for outcome-block length.
import numpy as np, pandas as pd, statsmodels.api as sm, statsmodels.formula.api as smf, sys
sys.path.insert(0,"glucose/code"); from simproc import simulate, episodes
rng=np.random.default_rng(7)
P=pd.read_csv("glucose/data/predictors.csv")
# tabulate G on a grid for dt/tau = 5/150 and 15/110
TAUS=[50,80,130,200,320,500]; zs=np.linspace(0.3,3.5,17); tab={}
for dt,minrun in [(5,3),(15,2)]:
    M=[]
    for tau in TAUS:
        n=int(600*1440/dt); y=simulate(n,dt,tau,rng)
        M.append([episodes(y<-z*np.sqrt(2),minrun)/(n*dt)*tau for z in zs])
    tab[dt]=np.log(np.maximum(np.array(M),1e-7)); print("dt",dt,"rate*tau at z=1:",np.round(np.exp(tab[dt][:,4]),4).tolist(),flush=True)
from scipy.interpolate import RegularGridInterpolator
def Gf(z,dt,tau):
    out=np.empty(len(z))
    for k in (5,15):
        f=RegularGridInterpolator((np.log(TAUS),zs),tab[k],bounds_error=False,fill_value=None)
        i=dt==k
        out[i]=np.exp(f(np.c_[np.log(np.clip(tau[i],TAUS[0],TAUS[-1])),np.clip(z[i],zs[0],zs[-1])]))
    return out
np.save("glucose/data/G_table.npy",np.stack([tab[5],tab[15]]))
res=[]
for coh in [["REPLACEBG_T1D"],["SH_T1DM","SH_T2DM"]]:
    d=P[P.cohort.isin(coh)&(P.B_hypo>0)].copy()
    mu_true=Gf(d.z_hypo.values,d.dt.values,d.tau.values)/d.tau.values*d.days1.values*1440
    ests=[];R=300
    for r in range(R):
        het=np.exp(rng.normal(0,0.5,len(d)))  # unexplained subject heterogeneity
        lam=mu_true*het; y=rng.poisson(lam)
        d["y"]=y; d["lt"]=np.log(d.tau); d["off"]=np.log(d.days1)
        try:
            m=smf.glm("y~lt+cr(z_hypo,df=3)",data=d,offset=d.off,family=sm.families.NegativeBinomial(alpha=0.25)).fit()
            ests.append((m.params["lt"],m.bse["lt"]))
        except Exception as e: pass
    e=np.array(ests); b,se=e[:,0],e[:,1]
    hit=np.mean((b+1.96*se<0)&(b-1.96*se<=-0.6)&(b+1.96*se>=-1.4))
    kill=np.mean((b>-0.5)&(b-1.96*se>-1))
    print(coh,"n",len(d),"mean events/subj",np.round(mu_true.mean(),1),"theory-implied slope mean",np.round(b.mean(),3),"SE",np.round(se.mean(),3),
          "P(CI excludes 0)",np.round(np.mean(b+1.96*se<0),2),"P(false kill)",np.round(kill,3),flush=True)
