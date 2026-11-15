# Build per-bank predictors from 2001Q1-2007Q4 FDIC financials. PREDICTORS ONLY.
import pandas as pd, numpy as np
d=pd.read_csv("data/financials_2001_2007.csv")
d["REPDTE"]=pd.to_datetime(d.REPDTE.astype(str))
d=d.sort_values(["CERT","REPDTE"])
d["yr"]=d.REPDTE.dt.year; d["q"]=d.REPDTE.dt.quarter
# quarterly net income from YTD
d["ni_prev"]=d.groupby(["CERT","yr"]).NETINC.shift(1)
d["ni_q"]=np.where(d.q==1,d.NETINC,d.NETINC-d.ni_prev)
# if previous quarter missing within the year, set NaN
prevq=d.groupby(["CERT","yr"]).q.shift(1)
d.loc[(d.q>1)&(prevq!=d.q-1),"ni_q"]=np.nan
d["asset_prev"]=d.groupby("CERT").ASSET.shift(1)
d["avgA"]=np.where(d.asset_prev.notna(),(d.ASSET+d.asset_prev)/2,d.ASSET)
d["roa_q"]=100*d.ni_q/d.avgA           # % of assets per quarter
d["car"]=100*d.EQ/d.ASSET              # equity/assets, %
def ar1(x):
    x=np.asarray(x,float); x=x[~np.isnan(x)]
    n=len(x)
    if n<12 or np.std(x)==0: return np.nan,np.nan,n
    y=x-x.mean(); a,b=y[:-1],y[1:]
    phi=(a@b)/(a@a); phi_bc=phi+(1+3*phi)/n   # Kendall bias correction
    res=b-phi*a
    return phi_bc,res.std(ddof=1),n
rows=[]
for cert,g in d.groupby("CERT"):
    g=g[g.ASSET>0]
    if len(g)<20 or g.REPDTE.max()!=pd.Timestamp("2007-12-31"): continue
    last=g.iloc[-1]
    phi_c,sd_c,n_c=ar1(g.car.values)
    yv=g.car.values; t=np.arange(len(yv)); 
    det=yv-np.polyval(np.polyfit(t,yv,1),t); phi_cd,_,_=ar1(det)
    r=g.roa_q.values
    phi_r,sd_r,_=ar1(r)
    rows.append(dict(CERT=cert,nq=len(g),asset07=last.ASSET,car07=last.car,
        B=last.car-2.0,sigma=np.nanstd(r,ddof=1),mu_roa=np.nanmean(r),
        phi_car=phi_c,sd_car_innov=sd_c,phi_car_detr=phi_cd,phi_roa=phi_r,sd_roa_innov=sd_r))
p=pd.DataFrame(rows)
clip=lambda f: np.clip(f,0.05,0.95)
p["tau"]=-1/np.log(clip(p.phi_car))          # quarters, primary
p["tau_detr"]=-1/np.log(clip(p.phi_car_detr))
p["tau_roa"]=-1/np.log(clip(p.phi_roa))
p["z"]=p.B/(p.sigma*np.sqrt(p.tau))
p["Zscore"]=(p.car07+p.mu_roa)/p.sigma
p.to_csv("data/predictors.csv",index=False)
ok=p[(p.B>0)&(p.sigma>0)&p.tau.notna()]
print("banks with 2007Q4 & >=20q:",len(p),"usable:",len(ok))
print(ok[["B","sigma","tau","tau_detr","tau_roa","z","Zscore"]].describe(percentiles=[.1,.5,.9]).T.round(3))
print("share phi_car clipped at .95:",(ok.phi_car>=0.95).mean().round(3)," at .05:",(ok.phi_car<=0.05).mean().round(3))
print("SD ln tau",np.log(ok.tau).std().round(3),"corr matrix of logs:")
print(np.log(ok[["B","sigma","tau"]]).corr().round(3))
