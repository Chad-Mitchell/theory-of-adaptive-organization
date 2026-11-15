# EXPLORATORY (not preregistered): is the bank tau effect explained by growth, profitability or size?
import numpy as np, pandas as pd, statsmodels.api as sm, statsmodels.formula.api as smf, json
CLL=sm.families.Binomial(sm.families.links.CLogLog())
d=pd.read_csv("banks/data/financials_2001_2007.csv"); d["REPDTE"]=pd.to_datetime(d.REPDTE.astype(str))
gr=d.sort_values("REPDTE").groupby("CERT").agg(a0=("ASSET","first"),a1=("ASSET","last"),n=("ASSET","size"))
gr["growth"]=(np.log(gr.a1.clip(lower=1)/gr.a0.clip(lower=1))/(gr.n/4)).clip(-0.5,1.0)
F=pd.read_csv("banks/data/failures.csv"); F["FAILDATE"]=pd.to_datetime(F.FAILDATE,format="%m/%d/%Y")
F=F[(F.RESTYPE=="FAILURE")&(F.FAILDATE>="2008-01-01")&(F.FAILDATE<="2014-12-31")]
p=pd.read_csv("banks/data/predictors.csv"); p["tau_p"]=-1/np.log(np.clip(p.phi_car_detr,0.05,0.95))
p=p[(p.B>0)&(p.sigma>0)].dropna(subset=["tau_p"]).merge(gr[["growth"]],left_on="CERT",right_index=True)
p["mu_roa"]=p.mu_roa.clip(-1,1); p["fail"]=p.CERT.isin(F.CERT).astype(int); p["lsig"]=np.log(p.sigma); p["lB"]=np.log(p.B); p["lt"]=np.log(p.tau_p); p["lA"]=np.log(p.asset07)
ci=lambda m,k:[round(m.params[k],3),round(m.conf_int().loc[k,0],3),round(m.conf_int().loc[k,1],3)]
R={}
R["E1_plus_growth_size_muROA"]=ci(smf.glm("fail~lsig+lB+lt+growth+lA+mu_roa",data=p,family=CLL).fit(),"lt")
R["E2_drop_clipped_phi"]=ci(smf.glm("fail~lsig+lB+lt",data=p[(p.phi_car_detr>0.05)&(p.phi_car_detr<0.95)],family=CLL).fit(),"lt")
p["tq"]=pd.qcut(p["lt"],5,labels=False); R["E3_fail_rate_by_tau_quintile_%"]=(p.groupby("tq").fail.mean()*100).round(2).tolist()
p["lt_own"]=np.log(p.tau); R["E4_both_taus"]={k:ci(smf.glm("fail~lsig+lB+lt+lt_own",data=p,family=CLL).fit(),k) for k in ["lt","lt_own"]}
R["corr_ln_tau_detr_vs_own"]=round(float(np.corrcoef(p["lt"],p["lt_own"])[0,1]),3)
json.dump(R,open("banks/exploratory.json","w"),indent=1); print(json.dumps(R,indent=1))
