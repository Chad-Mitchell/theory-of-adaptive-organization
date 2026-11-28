import sys,json,numpy as np,pandas as pd,rdata,statsmodels.formula.api as smf
sys.path.insert(0,'.'); from aslib import *
d=rdata.read_rda('sources/tsiR/data/twentymeas.RData')['twentymeas']
lists=[];ends=[]
num=None
for town,df in d.items():
    if not hasattr(df,'cases') : continue
    idx=np.where(df.cases.values>0)[0]
    n,dn=need_counts([idx],547,end=len(df)-1)
    num=n if num is None else num+n; den=dn if 'den' not in dir() else den+dn
lag=np.arange(548)
r=fit(lag[1:],num[1:],den[1:]); print("need",json.dumps({k:r[k] for k in ('exponent','power_wins')}),r['power']['r2'],r['exp']['r2'],"lags used",int(((num>0)&(den>num)).sum()))
np.savetxt("measles/needodds.csv",np.c_[lag[1:],num[1:],den[1:]],delimiter=",",fmt="%d",header="lag_biweeks,needed,at_risk")
s=pd.read_excel('sources/antia2018_S1Data.xlsx','FigS1_data'); m=s[s.infection.str.contains('Measles')].copy()
m=m[(m.titer>0)&(m.age>5)]; m["lt"]=np.log10(m.titer); m["la"]=np.log10(m.age-5)
mm=smf.mixedlm("lt~la",m,groups=m["indiv"]).fit()
print("memory measles: exponent",-mm.params.la,"CI",(-mm.conf_int().loc['la']).tolist(),"n obs",len(m),"indiv",m.indiv.nunique())
res=dict(need_exponent=r['exponent'],need_power_wins=r['power_wins'],need_r2_power=r['power']['r2'],need_r2_exp=r['exp']['r2'],mem_exponent=float(-mm.params.la),mem_ci=[float(x) for x in -mm.conf_int().loc['la']],n_obs=len(m),n_indiv=int(m.indiv.nunique()))
res["ratio"]=res["mem_exponent"]/res["need_exponent"]; print(res); json.dump(res,open("measles/results.json","w"),indent=1)
