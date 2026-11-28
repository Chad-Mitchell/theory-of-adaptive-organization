import numpy as np, pandas as pd, statsmodels.api as sm, statsmodels.formula.api as smf
D=pd.read_csv("populations/data/analysis_table.csv")
ci=lambda m,k:[round(m.params[k],3),round(m.conf_int().loc[k,0],3),round(m.conf_int().loc[k,1],3)]
def pois(f,d,g=None):
    m=smf.glm(f,data=d,offset=d.off,family=sm.families.Poisson())
    return m.fit(cov_type="cluster",cov_kwds=dict(groups=pd.factorize(d[g])[0])) if g else m.fit()
print("clipped phi<=0.05:",(D.phi<=0.05).sum()," >=0.95:",(D.phi>=0.95).sum())
D["q"]=pd.qcut(D["lt"],5,labels=False)
print(D.groupby("q").apply(lambda g: pd.Series(dict(n=len(g),rate=g.y.sum()/g.expo.sum(),meanz=g.z.mean(),clip_lo=(g.phi<=0.05).mean(),src12=(g.source==12).mean()))).round(3))
print("P1 cluster taxon:",ci(pois("y~lt+cr(z,df=3)",D,"taxon"),"lt"))
ev=D.groupby("source").y.transform("sum")>0; De=D[ev]
print("P1 + source FE (sources with events, n=%d):"%len(De),ci(pois("y~lt+cr(z,df=3)+C(source)",De,"source"),"lt"))
print("P1 excl fastest quintile:",ci(pois("y~lt+cr(z,df=3)",D[D.q>0],"source"),"lt"))
s12=D[D.source==12]
print("src12 only, cluster taxon:",ci(pois("y~lt+cr(z,df=3)",s12,"taxon"),"lt"), "n taxa",s12.taxon.nunique())
print("src12 units:",s12.units.value_counts().to_dict())
print("non-clipped & no src12:",ci(pois("y~lt+cr(z,df=3)",D[(D.phi>0.05)&(D.phi<0.95)&(D.source!=12)],"source"),"lt"))
# NB with source FE
m=smf.glm("y~lt+cr(z,df=3)",data=D,offset=D.off,family=sm.families.NegativeBinomial(alpha=1.0)).fit(cov_type="cluster",cov_kwds=dict(groups=D.source))
print("NB alpha=1:",ci(m,"lt"))
