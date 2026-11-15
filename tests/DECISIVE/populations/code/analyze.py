# OUTCOME analysis for the population test. Run only after PREREG.md is hashed and committed.
import numpy as np, pandas as pd, statsmodels.api as sm, statsmodels.formula.api as smf, json
from scipy import stats
P=pd.read_csv("populations/data/predictors.csv"); P=P[P.n2>=15].copy()
O=pd.read_csv("populations/data/outcome_block.csv")
L=dict(zip(P.MainID,P.lmean-np.log(5)))
rows=[]
for mid,g in O[O.MainID.isin(P.MainID)].groupby("MainID"):
    g=g.sort_values("SeriesStep"); v=g.PopulationUntransformed.astype(float).values; st=g.SeriesStep.values
    below=np.where(v>0,np.log(np.where(v>0,v,1))<L[mid],True)   # zeros count as below
    adj=np.diff(st)==1
    dc=int(np.sum(below[1:]&~below[:-1]&adj)); ex=int(adj.sum())
    rows.append(dict(MainID=mid,y=dc,expo=ex,any=int(below.any())))
D=P.merge(pd.DataFrame(rows),on="MainID")
D["lt"]=np.log(D.tau); D["lsig"]=np.log(D.sigma); D["ls"]=np.log(D.s); D["off"]=np.log(D.expo)
# Dennis et al. 1991 density-independent probability of reaching the threshold within T2 from the last first-block value
xd=D.last1-(D.lmean-np.log(5)); mu=D.mu_di; s2=D.s2_di.clip(lower=1e-6); T=D.T2
pd_=stats.norm.cdf((-xd-mu*T)/np.sqrt(s2*T))+np.exp(np.clip(-2*mu*xd/s2,-50,50))*stats.norm.cdf((-xd+mu*T)/np.sqrt(s2*T))
D["p_dennis"]=np.where(xd<=0,0.999,np.clip(pd_,1e-4,0.999)); D["lg_dennis"]=np.log(D.p_dennis/(1-D.p_dennis))
D.to_csv("populations/data/analysis_table.csv",index=False)
ci=lambda m,k:[round(m.params[k],3),round(m.conf_int().loc[k,0],3),round(m.conf_int().loc[k,1],3)]
def pois(f,d): return smf.glm(f,data=d,offset=d.off,family=sm.families.Poisson()).fit(cov_type="cluster",cov_kwds=dict(groups=d.source))
R=dict(n=len(D),events=int(D.y.sum()),series_with_any_crossing=int((D.y>0).sum()),n_sources=int(D.source.nunique()))
BSTAR=-0.34
m1=pois("y~lt+cr(z,df=3)",D); R["P1_fixed_spread_slope"]=ci(m1,"lt")
m2=pois("y~lt+lsig",D); R["P2_fixed_sigma"]=dict(b_tau=ci(m2,"lt"),b_sigma=ci(m2,"lsig"),implied_b_tau=0.70,implied_b_sigma=1.97)
D["zc"]=(D.z-D.z.mean())/D.z.std(); m3=pois("y~lt*zc+lsig",D); R["P3_interaction"]=ci(m3,"lt:zc")
dc=D[D.z>=1.5]; R["n_cold"]=len(dc); R["events_cold"]=int(dc.y.sum())
mc1=pois("y~lt+cr(z,df=3)",dc); R["cold_fixed_spread_slope"]=ci(mc1,"lt")
mc2=pois("y~lt+lsig",dc); R["cold_b_tau_given_sigma"]=ci(mc2,"lt")
# collapse across taxonomic classes
d4=D[D.tclass.isin(["Mammalia","Aves","Osteichthyes","Insecta"])].copy(); d4["off"]=np.log(d4.expo)-np.log(d4.tau)
mcol=smf.glm("y~cr(z,df=3)+C(tclass,Treatment('Mammalia'))",data=d4,offset=d4.off,family=sm.families.Poisson()).fit(cov_type="cluster",cov_kwds=dict(groups=d4.source))
R["P4_collapse_class_offsets"]={k:ci(mcol,k) for k in mcol.params.index if "tclass" in k}
# baselines
s0=pois("y~cr(z,df=3)",D); R["static_spread_vs_plus_tau"]=dict(dAIC=round(s0.aic-m1.aic,2))
b0=smf.logit("any~lg_dennis",data=D).fit(disp=0); b1=smf.logit("any~lg_dennis+lt+ls",data=D).fit(disp=0)
R["P5_dennis_baseline"]=dict(b_tau_given_dennis=ci(b1,"lt"),LR_p=float(1-stats.chi2.cdf(2*(b1.llf-b0.llf),2)),dAIC=round(b0.aic-b1.aic,2))
# circularity / robustness
R["S1_state_space_tau"]=ci(pois("y~I(np.log(tau_ss))+cr(z,df=3)",D),"I(np.log(tau_ss))")
R["S2_reliability_ge2"]=ci(pois("y~lt+cr(z,df=3)",D[D.rel>=2]),"lt") if (D.rel>=2).sum()>40 else "n<40"
R["S3_negbin"]=ci(smf.glm("y~lt+cr(z,df=3)",data=D,offset=D.off,family=sm.families.NegativeBinomial(alpha=1.0)).fit(),"lt")
R["S4_plus_first_block_trend"]=ci(pois("y~lt+cr(z,df=3)+trend",D),"lt")
R["S5_drop_clipped_tau"]=ci(pois("y~lt+cr(z,df=3)",D[(D.phi>0.05)&(D.phi<0.95)]),"lt")
# permutation null: shuffle tau within z-quintiles (2000x)
rng=np.random.default_rng(3); D["zq"]=pd.qcut(D.z,5,labels=False); null=[]
for i in range(2000):
    d=D.copy(); d["lt"]=d.groupby("zq").lt.transform(lambda x: rng.permutation(x.values))
    null.append(smf.glm("y~lt+cr(z,df=3)",data=d,offset=d.off,family=sm.families.Poisson()).fit().params["lt"])
R["permutation_p_one_sided_negative"]=float(np.mean(np.array(null)<=m1.params["lt"]))
# in-block circular contrast: crossings within the first block itself
def verdict(sl,bstar):
    b,lo,hi=sl
    if abs(b)<abs(b-bstar) and (lo>bstar or hi<bstar): return "KILL"
    if hi<0 and lo<=bstar<=hi: return "HIT"
    if hi<0: return "SIGN-RIGHT, SIZE-OFF"
    return "INCONCLUSIVE"
R["verdict_primary"]=verdict(R["P1_fixed_spread_slope"],BSTAR)
R["verdict_literal_minus1"]=verdict(R["P1_fixed_spread_slope"],-1.0)
cb,clo,chi=R["cold_b_tau_given_sigma"]; R["cold_kill_rule_fires"]=bool(cb<=0 and chi<0.2)
json.dump(R,open("populations/results.json","w"),indent=1); print(json.dumps(R,indent=1))
