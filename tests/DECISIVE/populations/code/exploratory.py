# EXPLORATORY (not preregistered): dependence on the dominant data source (source 12 = half the series).
import numpy as np, pandas as pd, statsmodels.api as sm, statsmodels.formula.api as smf, json
D=pd.read_csv("populations/data/analysis_table.csv")
M=pd.read_csv("populations/data/knb/df35b.237.1",lineterminator='\r',encoding='latin1')
ci=lambda m,k:[round(m.params[k],3),round(m.conf_int().loc[k,0],3),round(m.conf_int().loc[k,1],3)]
def pois(f,d,cl=True):
    m=smf.glm(f,data=d,offset=d.off,family=sm.families.Poisson())
    return m.fit(cov_type="cluster",cov_kwds=dict(groups=d.source)) if cl else m.fit()
R={"source12":M.loc[M.DatasourceID==12,["Author","Year","Title"]].astype(str).values.tolist(),
   "n_source12":int((D.source==12).sum())}
R["without_source12"]=ci(pois("y~lt+cr(z,df=3)",D[D.source!=12]),"lt")
R["source12_only_(no_cluster)"]=ci(pois("y~lt+cr(z,df=3)",D[D.source==12],cl=False),"lt")
R["one_series_per_taxon_(median-length)"]=None
d1=D.sort_values("n1").groupby("taxon").tail(1); R["one_series_per_taxon"]=dict(n=len(d1),slope=ci(pois("y~lt+cr(z,df=3)",d1),"lt"))
json.dump(R,open("populations/exploratory.json","w"),indent=1); print(json.dumps(R,indent=1))
