# Reviewer exploratory: does detrended-tau proxy for capital-ratio curvature / late decline?
import numpy as np, pandas as pd, statsmodels.api as sm, statsmodels.formula.api as smf
CLL=sm.families.Binomial(sm.families.links.CLogLog())
d=pd.read_csv("banks/data/financials_2001_2007.csv"); d["REPDTE"]=pd.to_datetime(d.REPDTE.astype(str))
d=d[d.ASSET>0].sort_values(["CERT","REPDTE"]); d["car"]=100*d.EQ/d.ASSET
rows=[]
for c,g in d.groupby("CERT"):
    y=g.car.values; t=np.arange(len(y))
    if len(y)<20: continue
    q=np.polyfit(t,y,2); l=np.polyfit(t,y,1)
    late=y[-1]-y[-9] if len(y)>=9 else np.nan
    ag=np.log(g.ASSET.values[-1]/g.ASSET.values[-9]) if len(y)>=9 else np.nan
    rows.append(dict(CERT=c,curv=q[0]*len(y)**2,slope=l[0]*len(y),late=late,agrow2=ag))
X=pd.DataFrame(rows)
F=pd.read_csv("banks/data/failures.csv"); F["FAILDATE"]=pd.to_datetime(F.FAILDATE,format="%m/%d/%Y")
F=F[(F.RESTYPE=="FAILURE")&(F.FAILDATE>="2008-01-01")&(F.FAILDATE<="2014-12-31")]
p=pd.read_csv("banks/data/predictors.csv"); p["tau_p"]=-1/np.log(np.clip(p.phi_car_detr,0.05,0.95))
p=p[(p.B>0)&(p.sigma>0)].dropna(subset=["tau_p"]).merge(X,on="CERT")
p["fail"]=p.CERT.isin(F.CERT).astype(int); p["lsig"]=np.log(p.sigma); p["lB"]=np.log(p.B); p["lt"]=np.log(p.tau_p); p["lt_own"]=np.log(p.tau)
for v in ["curv","slope","late","agrow2"]: p[v]=p[v].clip(p[v].quantile(.01),p[v].quantile(.99))
print("n",len(p),"fails",p.fail.sum())
print("corr lt with curv,slope,late,agrow2:",[round(np.corrcoef(p["lt"],p[v])[0,1],3) for v in ["curv","slope","late","agrow2"]])
print("corr lt with |curv|:",round(np.corrcoef(p["lt"],p.curv.abs())[0,1],3))
for f in ["fail~lsig+lB+lt","fail~lsig+lB+lt+curv","fail~lsig+lB+lt+late","fail~lsig+lB+lt+curv+late+slope+agrow2","fail~lsig+lB+lt_own+curv+late+slope+agrow2"]:
    m=smf.glm(f,data=p,family=CLL).fit(); k="lt" if "lt+" in f or f.endswith("lt") else "lt_own"
    print(f, [round(x,3) for x in (m.params[k],*m.conf_int().loc[k])], {v:round(m.params[v],3) for v in m.params.index if v in("curv","late","slope","agrow2")})
