# GPDD: select annual series, split in time, compute PREDICTORS from the first block only.
import pandas as pd, numpy as np
from scipy.optimize import minimize
rd=lambda f: pd.read_csv(f"data/knb/{f}",lineterminator='\r',encoding='latin1')
M=rd("df35b.234.1"); D=rd("df35b.233.1"); T=rd("df35b.236.1")
M=M.merge(T[["TaxonID","TaxonomicClass","TaxonName"]],on="TaxonID",how="left")
HARVEST=["tonne","kill","catch","caught","harvest","landing","shot","bag","licen","yield","weight","biomass","pelt","pound","skin","fur","export","infect","damag"]
sel=M[(M.SamplingFrequency.astype(str).str.strip()=="1")&(M.DatasetLength>=40)]   # all Reliability levels; >=2 is a sensitivity
sel=sel[~sel.SamplingUnits.astype(str).str.lower().str.contains("|".join(HARVEST))]
GAP=1   # one year excluded between blocks
def kalman_negll(p,y):
    phi,ls,lo=p; mu=np.mean(y); q=np.exp(2*ls); r=np.exp(2*lo)
    if not (0<phi<0.999): return 1e10
    x=0.0; P=q/(1-phi**2); ll=0
    for i,yy in enumerate(y-mu):
        if i>0: x=phi*x; P=phi**2*P+q
        S=P+r; e=yy-x; ll+=0.5*(np.log(2*np.pi*S)+e*e/S); K=P/S; x+=K*e; P*=(1-K)
    return ll
P=[];O=[]
for _,mr in sel.iterrows():
    g=D[D.MainID==mr.MainID].sort_values("SeriesStep")
    steps=g.SeriesStep.values; n_exp=steps.max()-steps.min()+1
    if len(g)<40 or len(g)/n_exp<0.9: continue
    y=g.PopulationUntransformed.astype(float).values
    half=int(np.floor((steps.min()+steps.max())/2))
    a=g[g.SeriesStep<=half-GAP]; b=g[g.SeriesStep>half]
    ya=a.PopulationUntransformed.astype(float).values
    if (ya<=0).any() or np.isnan(ya).any() or len(a)<19 or np.std(np.log(ya))==0: continue
    x=np.log(ya); sa=a.SeriesStep.values
    # AR(1) on consecutive-year pairs, own mean, Kendall bias correction
    xm=x-x.mean(); pr=np.where(np.diff(sa)==1)[0]
    u,v=xm[pr],xm[pr+1]; phi=(u@v)/(u@u); n=len(x); phi_bc=phi+(1+3*phi)/n
    phi_c=np.clip(phi_bc,0.05,0.95); tau=-1/np.log(phi_c)
    # state-space Gompertz (AR1 + obs noise) by MLE, on the block treated as consecutive
    sd=x.std(ddof=1)
    best=None
    for ph0 in (0.3,0.6,0.85):
        r=minimize(kalman_negll,[ph0,np.log(sd*0.7),np.log(sd*0.3)],args=(x,),method="Nelder-Mead",options=dict(maxiter=2000,xatol=1e-4,fatol=1e-6))
        if best is None or r.fun<best.fun: best=r
    phi_ss=np.clip(best.x[0],0.05,0.95)
    # density-independent diffusion (Dennis et al. 1991): mu, sigma2 of log growth increments
    inc=np.diff(x)[np.diff(sa)==1]; mu_di=inc.mean(); s2_di=inc.var(ddof=1)
    P.append(dict(MainID=mr.MainID,rel=mr.Reliability,units=mr.SamplingUnits,taxon=mr.TaxonName,tclass=mr.TaxonomicClass,source=mr.DataSourceID,
        n1=len(a),n2=len(b),T2=b.SeriesStep.max()-b.SeriesStep.min()+1,
        lmean=x.mean(),s=sd,phi=phi_bc,tau=tau,phi_ss=best.x[0],tau_ss=-1/np.log(phi_ss),
        mu_di=mu_di,s2_di=s2_di,trend=np.polyfit(sa,x,1)[0],last1=x[-1]))
    O.append(b.assign(MainID=mr.MainID))
P=pd.DataFrame(P)
P["B"]=np.log(5)
P["z"]=P.B/(P.s*np.sqrt(2))
P["sigma"]=P.s*np.sqrt(2/P.tau)
P.to_csv("data/predictors.csv",index=False)
pd.concat(O).to_csv("data/outcome_block.csv",index=False)
print("candidate series:",len(sel),"usable:",len(P))
print(P[["n1","T2","s","tau","tau_ss","z"]].describe(percentiles=[.1,.5,.9]).T.round(3))
print(P.tclass.value_counts().head(10))
print("share tau clipped hi:",(P.phi>=0.95).mean().round(3),"lo:",(P.phi<=0.05).mean().round(3))
print("SD ln tau:",np.log(P.tau).std().round(3),"corr ln tau, ln s:",np.corrcoef(np.log(P.tau),np.log(P.s))[0,1].round(3),"corr ln tau ln tau_ss:",np.corrcoef(np.log(P.tau),np.log(P.tau_ss))[0,1].round(3))
print("share z>=1.5:",(P.z>=1.5).mean().round(3),"n sources:",P.source.nunique())
