# Theory-implied slopes and power for populations, predictors only.
# H1 (theory): log-abundance is a stationary AR(1)=sampled OU with each series' phi and s; count downcrossings of mean-ln5.
import numpy as np, pandas as pd, statsmodels.api as sm, statsmodels.formula.api as smf
rng=np.random.default_rng(11)
P=pd.read_csv("populations/data/predictors.csv"); P=P[P.n2>=15].copy()
phi=np.exp(-1/P.tau.values); s=P.s.values; L=-np.log(5)
def sim_counts(phi,s,n2):
    c=np.zeros(len(phi)); ex=np.zeros(len(phi))
    for i in range(len(phi)):
        x=np.empty(n2[i]); x[0]=rng.normal(0,s[i]); e=rng.normal(0,s[i]*np.sqrt(1-phi[i]**2),n2[i])
        for t in range(1,n2[i]): x[t]=phi[i]*x[t-1]+e[t]
        b=x<L; c[i]=np.sum(b[1:]&~b[:-1]); ex[i]=n2[i]-1
    return c,ex
n2=P.n2.values.astype(int); R=300; B1=[];B2=[];SE=[];I=[]
for r in range(R):
    c,ex=sim_counts(phi,s,n2); d=P.assign(y=c,off=np.log(ex),lt=np.log(P.tau),ls=np.log(P.sigma))
    try:
        m1=smf.glm("y~lt+cr(z,df=3)",data=d,offset=d.off,family=sm.families.Poisson()).fit(cov_type="cluster",cov_kwds=dict(groups=d.source))
        m2=smf.glm("y~lt+ls",data=d,offset=d.off,family=sm.families.Poisson()).fit()
        B1.append(m1.params["lt"]);SE.append(m1.bse["lt"]);B2.append((m2.params["lt"],m2.params["ls"]))
        dc=d[d.z>=1.5]; mc=smf.glm("y~lt+cr(z,df=3)",data=dc,offset=dc.off,family=sm.families.Poisson()).fit(); I.append((mc.params["lt"],mc.bse["lt"]))
    except Exception as e: pass
B1=np.array(B1);SE=np.array(SE);B2=np.array(B2);I=np.array(I)
print("n series",len(P),"mean expected downcrossings/series",np.round(np.mean(sim_counts(phi,s,n2)[0]),2))
print("M1 fixed-spread theory-implied slope beta*: mean",B1.mean().round(3),"sd",B1.std().round(3),"mean cluster SE",SE.mean().round(3))
print("P(CI excludes 0 | H1):",np.mean(B1+1.96*SE<0).round(2))
print("P(false kill: closer to 0 than beta* and CI excludes beta*):",np.mean((B1>B1.mean()/2)&(B1-1.96*SE>B1.mean())).round(3))
print("M2 fixed-innovation: beta_tau mean",B2[:,0].mean().round(3),"beta_sigma mean",B2[:,1].mean().round(3),"identity beta_sig/2-1 =",(B2[:,1].mean()/2-1).round(3))
print("cold subset (z>=1.5) n",(P.z>=1.5).sum(),"implied slope",I[:,0].mean().round(3),"SE",I[:,1].mean().round(3))
