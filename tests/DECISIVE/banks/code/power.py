# Power for the bank test, predictors only (no outcomes). Simulated failures with a cloglog model.
import numpy as np, pandas as pd, statsmodels.api as sm
rng=np.random.default_rng(20261114)
p=pd.read_csv("banks/data/predictors.csv")
p["tau_p"]=-1/np.log(np.clip(p.phi_car_detr,0.05,0.95))
p=p[(p.B>0)&(p.sigma>0)].dropna(subset=["tau_p"])
X=pd.DataFrame(dict(lsig=np.log(p.sigma),lB=np.log(p.B),ltau=np.log(p.tau_p)))
X=(X-X.mean())
Xc=sm.add_constant(X)
out=[]
for btau in [0.0,0.1,0.2,0.3]:
    for nfail in [300,500]:
        rej=0; R=300
        for r in range(R):
            eta=0.3*X.lsig-0.8*X.lB+btau*X.ltau
            # calibrate intercept to give ~nfail failures
            a=np.log(-np.log(1-nfail/len(X)))
            pr=1-np.exp(-np.exp(a+eta)); y=rng.random(len(X))<pr
            m=sm.GLM(y.astype(float),Xc,family=sm.families.Binomial(sm.families.links.CLogLog())).fit()
            lo=m.params["ltau"]-1.645*m.bse["ltau"]
            rej+= lo>0
        out.append((btau,nfail,rej/R))
        print(f"beta_tau={btau} failures~{nfail}: power(one-sided 5%)={rej/R:.2f}",flush=True)
print("n banks:",len(X),"SD ln tau(detr):",X.ltau.std().round(3))
