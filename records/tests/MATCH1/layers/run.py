import sys,json,glob,zipfile,io,numpy as np,pandas as pd
sys.path.insert(0,'layers'); sys.path.insert(0,'.'); from layerlib import *
curves={}
def loadcsv(p):
    a=np.loadtxt(p,delimiter=",",skiprows=1); return a[:,0],a[:,1],a[:,2]
l,n,d=loadcsv("news/needodds_full.csv"); curves["news_need"]=logbin_counts(l,n,d)
N=None
for p in glob.glob("code/*_filtered_L3650.csv"):
    l,n,d=loadcsv(p); N=(n,d) if N is None else (N[0]+n,N[1]+d)
curves["code_need_pooled"]=logbin_counts(l,N[0],N[1])
l,n,d=loadcsv("wiki/needodds_nobots_L3650.csv"); curves["wiki_need"]=logbin_counts(l,n,d)
# Meeter recall odds, open recall, expts 1-2, raw
z=zipfile.ZipFile("sources/meeter2005_data.zip"); P="DNMT-forget txtdata-oct04/"
E=[]
for i in (1,2):
    e=pd.read_csv(io.BytesIO(z.read(P+f"DNMT-expt{i}.txt")),sep="\t",low_memory=False); e.columns=[c.strip() for c in e.columns]
    e=e[pd.to_numeric(e.SCORE,errors="coerce").notna()&pd.to_numeric(e.Q_AGE,errors="coerce").notna()]; E.append(e)
e=pd.concat(E); e=e[e.Q_TYPE.astype(int)==1]; age=e.Q_AGE.astype(float).values; sc=e.SCORE.astype(float).values
m=(age>=1)&(age<=730)
lagv=np.arange(1,731); num=np.bincount(age[m].astype(int),weights=sc[m],minlength=731)[1:]; tot=np.bincount(age[m].astype(int),minlength=731)[1:]
curves["news_memory_recall"]=logbin_counts(lagv,num,tot)   # odds of correct recall
# OpenAlex reference-age curve
oa=json.load(open("openalex/ref_years.json")); vol={int(g["key"]):g["count"] for g in json.load(open("openalex/volume_by_year.json")) if str(g["key"]).isdigit()}
ages=np.arange(1,101); share=np.array([oa["years"].get(str(2023-a),0)/vol.get(2023-a,np.nan) for a in ages])
ok=np.isfinite(share)&(share>0)
# treat as positive curve directly (no odds): fake num/den so logbin gives f = share/(1+share)~share -> use direct binning
def logbin_direct(t,f,per_decade=10):
    e=np.logspace(0,np.log10(t.max()+1),int(np.ceil(per_decade*np.log10(t.max()+1)))+1); T=[];F=[]
    for a,b in zip(e[:-1],e[1:]):
        mm=(t>=a)&(t<b)
        if mm.sum(): T.append(t[mm].mean()); F.append(f[mm].mean())
    return np.array(T),np.array(F)
curves["science_reference_age"]=logbin_direct(ages[ok],share[ok]/np.nanmax(share[ok]))
# antibody: viral titers vs age (descriptive)
s=pd.read_excel("sources/antia2018_S1Data.xlsx","FigS1_data"); v=s[s.infection.str.contains("Measles|Rubella|Mumps|VZV|Vaccinia")]
v=v[v.titer>0]; g=v.groupby(pd.cut(v.age-5,np.logspace(np.log10(15),np.log10(65),8)),observed=True)
curves["antibody_viral_vs_age(descriptive)"]=(np.array([x.age.mean()-5 for _,x in g]),np.array([np.exp(np.mean(np.log(x.titer/x.groupby('infection').titer.transform('median')))) for _,x in g]))
out={}
for k,(t,f) in curves.items():
    span=np.log10(t.max()/t.min()); ser=span_series(t,f)
    out[k]=dict(span_decades=float(span),series=ser); print(k,"span %.2f"%span,[(x["span"],x["K"]) for x in ser],flush=True)
    pd.DataFrame(dict(t=t,f=f)).to_csv(f"layers/curve_{k.split('(')[0]}.csv",index=False)
json.dump(out,open("layers/results.json","w"),indent=1)
