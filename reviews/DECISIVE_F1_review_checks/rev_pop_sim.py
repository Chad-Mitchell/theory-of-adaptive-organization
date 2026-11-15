# Theory shape check: exact per-year downcrossing prob for a stationary annual-sampled Gaussian AR(1)
# with each series' first-block phi (clipped) and z, vs observed, by tau quintile.
import numpy as np, pandas as pd
from scipy.stats import multivariate_normal as mvn, norm
D=pd.read_csv("populations/data/analysis_table.csv")
phi=np.clip(D.phi,0.05,0.95).values; c=np.log(5)/D.s.values  # threshold in SD units
p=[]
for f,k in zip(phi,c):
    # P(X_t > -k, X_{t+1} < -k), standard bivariate normal corr f
    both_below=mvn(mean=[0,0],cov=[[1,f],[f,1]]).cdf([-k,-k])
    p.append(norm.cdf(-k)-both_below)
D["p_theory"]=p
D["q"]=pd.qcut(np.log(D.tau),5,labels=False)
g=D.groupby("q").apply(lambda g: pd.Series(dict(obs_rate=g.y.sum()/g.expo.sum(),theory_rate=(g.p_theory*g.expo).sum()/g.expo.sum(),med_tau=g.tau.median())))
print(g.round(4))
import statsmodels.api as sm, statsmodels.formula.api as smf
D["off"]=np.log(D.expo)
# regress theory-expected counts (as pseudo outcome, quasi-Poisson) on lt + spline z : theory slope on this design
D["yth"]=D.p_theory*D.expo
m=smf.glm("yth~lt+cr(z,df=3)",data=D,offset=D.off,family=sm.families.Poisson()).fit()
print("theory-implied P1 slope on actual design (stationary, no obs error):",round(m.params["lt"],3))
dc=D[D.z>=1.5].copy()
m=smf.glm("yth~lt+cr(z,df=3)",data=dc,offset=dc.off,family=sm.families.Poisson()).fit()
print("theory-implied cold (z>=1.5) slope:",round(m.params["lt"],3),"n",len(dc))
