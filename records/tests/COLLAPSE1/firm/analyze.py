import json,numpy as np,pandas as pd,statsmodels.formula.api as smf
def load(tag,fr):
    try: d=json.load(open(f"raw/{tag}_{fr}.json"))["data"]
    except: return pd.Series(dtype=float)
    s=pd.DataFrame(d).groupby("cik")["val"].last(); s.index=s.index.astype(str); return s
inv=load("InventoryNet","CY2023Q4I")
def cogs(y):
    a=load("CostOfGoodsAndServicesSold",f"CY{y}"); b=load("CostOfRevenue",f"CY{y}")
    return a.combine_first(b)
CG={y:cogs(y) for y in range(2019,2024)}
sic=json.load(open("sic.json"))
df=pd.DataFrame({"inv":inv,"cogs":CG[2023]}).dropna()
df=df[(df.inv>0)&(df.cogs>0)]
df["sic"]=[sic.get(c) for c in df.index]; df=df[df.sic.notna()&(df.sic!="")]
df["sic2"]=df.sic.astype(str).str[:2]
df["li"]=np.log(df.inv); df["lc"]=np.log(df.cogs)
rows=[]
for s,g in df.groupby("sic2"):
    if len(g)<30: continue
    m=smf.ols("li~lc",g).fit()
    lo,hi=m.conf_int().loc["lc"]
    rows.append(dict(sic2=s,n=len(g),slope=m.params.lc,ci_lo=lo,ci_hi=hi))
R=pd.DataFrame(rows).sort_values("slope"); print(R.round(3).to_string(index=False))
print("industries",len(R),"median slope",R.slope.median().round(3),"share<0.95",(R.slope<0.95).mean().round(2),"share CI excl 1",(R.ci_hi<1).mean().round(2),"share CI contains 0.5",((R.ci_lo<=0.5)&(R.ci_hi>=0.5)).mean().round(2))
fe=smf.ols("li~lc+C(sic2)",df[df.sic2.isin(R.sic2)]).fit(); print("pooled within-industry slope",round(fe.params.lc,3),fe.conf_int().loc["lc"].round(3).tolist(),"n",int(fe.nobs))
# C2 volatility
P=pd.DataFrame({y:CG[y] for y in CG})
lp=np.log(P.where(P>0)); dl=lp.diff(axis=1).iloc[:,1:]
vol=dl.std(axis=1,skipna=True); cnt=lp.notna().sum(axis=1)
df["vol"]=vol.reindex(df.index); df["cnt"]=cnt.reindex(df.index)
v=df[(df.cnt>=4)&(df.vol>0)&df.sic2.isin(R.sic2)].copy(); v["lv"]=np.log(v.vol); v["lr"]=v.li-v.lc
m2=smf.ols("lr~lv+lc+C(sic2)",v).fit(cov_type="HC1")
print("C2 partial slope of log(inv/cogs) on log(vol):",round(m2.params.lv,3),"CI",m2.conf_int().loc["lv"].round(3).tolist(),"p",float(m2.pvalues.lv),"n",int(m2.nobs))
R.to_csv("industry_slopes.csv",index=False); df.to_csv("firm_panel.csv")
json.dump(dict(median=float(R.slope.median()),n_ind=len(R),pooled=float(fe.params.lc),pooled_ci=fe.conf_int().loc["lc"].tolist(),c2=float(m2.params.lv),c2_ci=m2.conf_int().loc["lv"].tolist(),c2_p=float(m2.pvalues.lv),c2_n=int(m2.nobs)),open("summary.json","w"))
