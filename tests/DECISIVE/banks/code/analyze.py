# OUTCOME analysis for the bank test. Run only after PREREG.md is hashed and committed.
import numpy as np, pandas as pd, statsmodels.api as sm, statsmodels.formula.api as smf, requests, json, os
from scipy import stats
import sys; sys.path.insert(0,"banks/code"); from sklearn_free_auc import auc
CLL=sm.families.Binomial(sm.families.links.CLogLog())
# 1. outcomes
if not os.path.exists("banks/data/failures.csv"):
    r=requests.get("https://api.fdic.gov/banks/failures",params=dict(fields="CERT,NAME,FAILDATE,RESTYPE,RESTYPE1,QBFASSET",limit=10000,format="json"),timeout=120).json()
    pd.DataFrame([x["data"] for x in r["data"]]).to_csv("banks/data/failures.csv",index=False)
F=pd.read_csv("banks/data/failures.csv"); F["FAILDATE"]=pd.to_datetime(F.FAILDATE,format="%m/%d/%Y")
F=F[(F.RESTYPE=="FAILURE")&(F.FAILDATE>="2008-01-01")&(F.FAILDATE<="2014-12-31")]
p=pd.read_csv("banks/data/predictors.csv")
p["tau_p"]=-1/np.log(np.clip(p.phi_car_detr,0.05,0.95))
p=p[(p.B>0)&(p.sigma>0)].dropna(subset=["tau_p"]).copy()
p["fail"]=p.CERT.isin(F.CERT).astype(int)
p["lsig"]=np.log(p.sigma); p["lB"]=np.log(p.B); p["lt"]=np.log(p.tau_p)
p["z"]=p.B/(p.sigma*np.sqrt(p.tau_p)); p["lz"]=np.log(p.z); p["lzc"]=(p.lz-p.lz.mean())/p.lz.std()
p["lZ"]=np.log(p.Zscore.clip(lower=0.01)); p["lA"]=np.log(p.asset07)
R=dict(n=len(p),failures=int(p.fail.sum()),failures_in_list_2008_2014=len(F),unmatched_failures=int((~F.CERT.isin(p.CERT)).sum()))
ci=lambda m,k:[round(m.params[k],3),round(m.conf_int().loc[k,0],3),round(m.conf_int().loc[k,1],3)]
g=lambda f,d=p: smf.glm(f,data=d,family=CLL).fit()
m1=g("fail~lsig+lB+lt"); R["P1"]=dict(b_tau=ci(m1,"lt"),b_sigma=ci(m1,"lsig"),b_B=ci(m1,"lB"),p_one_sided=float(1-stats.norm.cdf(m1.params["lt"]/m1.bse["lt"])))
R["P1_wald"]=dict(eps_B_eq_minus_eps_sigma=float(m1.wald_test("lB + lsig = 0",scalar=True).pvalue),
                  identity_continuous=float(m1.wald_test("lt - 0.5*lsig = -1",scalar=True).pvalue),
                  identity_incident=float(m1.wald_test("lt - 0.5*lsig = 0",scalar=True).pvalue))
# P2 cold tercile ratio with bootstrap
cold=p[p.z>=p.z.quantile(2/3)]; mc=g("fail~lsig+lB+lt",cold); R["cold_tercile"]=dict(n=len(cold),failures=int(cold.fail.sum()),b_tau=ci(mc,"lt"),b_sigma=ci(mc,"lsig"),r_tau=round(mc.params["lt"]/mc.params["lsig"],3))
rng=np.random.default_rng(1); rs=[]
for b in range(1000):
    s=cold.sample(len(cold),replace=True,random_state=int(rng.integers(1e9)))
    try: mm=g("fail~lsig+lB+lt",s); rs.append(mm.params["lt"]/mm.params["lsig"])
    except Exception: pass
R["cold_tercile"]["r_tau_boot95"]=[round(float(np.percentile(rs,2.5)),3),round(float(np.percentile(rs,97.5)),3)]
c15=p[p.z>=1.5]; m15=g("fail~lsig+lB+lt",c15); R["cold_z_ge_1.5"]=dict(n=len(c15),failures=int(c15.fail.sum()),b_tau=ci(m15,"lt"))
# P3 interaction
m3=g("fail~lsig+lB+lt+lt:lzc"); R["P3_interaction_lt_x_lnz"]=ci(m3,"lt:lzc")
# P4 bank-specific horizon vs fixed 1-year horizon
a=g("fail~I(np.log(B/(sigma*np.sqrt(tau_p))))"); b=g("fail~I(np.log(B/(sigma*2.0)))")
R["P4_dAIC_bank_horizon_minus_fixed"]=round(b.aic-a.aic,2)
# baseline Z-score
z0=g("fail~lZ"); z1=g("fail~lZ+lt")
R["baseline_Z"]=dict(b_tau_given_Z=ci(z1,"lt"),LR_p=float(1-stats.chi2.cdf(2*(z1.llf-z0.llf),1)),dAIC=round(z0.aic-z1.aic,2),
     AUC_Z=round(auc(p.fail,z0.fittedvalues),4),AUC_Z_tau=round(auc(p.fail,z1.fittedvalues),4),AUC_theory=round(auc(p.fail,m1.fittedvalues),4))
# sensitivities
R["S1_plus_size"]=ci(g("fail~lsig+lB+lt+lA"),"lt")
p["lt_own"]=np.log(p.tau); R["S2_tau_own_mean"]=ci(g("fail~lsig+lB+lt_own"),"lt_own")
p["lt_roa"]=np.log(p.tau_roa); R["S3_tau_roa"]=ci(g("fail~lsig+lB+lt_roa"),"lt_roa")
R["S4_logit"]=ci(smf.logit("fail~lsig+lB+lt",data=p).fit(disp=0),"lt")
p["lsig_in"]=np.log(p.sd_car_innov.clip(lower=1e-4)); R["S5_sigma_capital_innovation"]=ci(g("fail~lsig_in+lB+lt"),"lt")
# jump-share check: largest single-quarter loss (2008 -> failure) relative to B (2007Q4)
if not os.path.exists("banks/data/failed_fin.csv"):
    rows=[]
    for c in p.loc[p.fail==1,"CERT"]:
        r=requests.get("https://api.fdic.gov/banks/financials",params=dict(filters=f"CERT:{c} AND REPDTE:[20080101 TO 20141231]",fields="CERT,REPDTE,NETINC,ASSET",limit=100,format="json"),timeout=60).json()
        rows+=[x["data"] for x in r["data"]]
    pd.DataFrame(rows).to_csv("banks/data/failed_fin.csv",index=False)
ff=pd.read_csv("banks/data/failed_fin.csv"); ff["REPDTE"]=pd.to_datetime(ff.REPDTE.astype(str)); ff=ff.sort_values(["CERT","REPDTE"])
ff["yr"]=ff.REPDTE.dt.year; ff["q"]=ff.REPDTE.dt.quarter
ff["niq"]=np.where(ff.q==1,ff.NETINC,ff.NETINC-ff.groupby(["CERT","yr"]).NETINC.shift(1))
ff["lossq"]=-100*ff.niq/ff.ASSET
mx=ff.groupby("CERT").lossq.max().rename("maxloss").reset_index().merge(p[["CERT","B","sigma"]],on="CERT")
R["jump_share"]=dict(n_failed_with_fin=len(mx),share_one_quarter_loss_gt_B=round(float((mx.maxloss>mx.B).mean()),3),
     share_gt_half_B=round(float((mx.maxloss>mx.B/2).mean()),3),median_maxloss_over_sigma=round(float((mx.maxloss/mx.sigma).median()),1))
# verdict
b,lo,hi=R["P1"]["b_tau"]; cb,clo,chi=R["cold_z_ge_1.5"]["b_tau"]
kill = (cb<=0 and chi<0.2)
hit = (lo>0) and (R["P3_interaction_lt_x_lnz"][0]>0)
R["verdict"]="KILL (firm scale)" if kill else ("HIT" if hit else ("SIGN-WRONG" if hi<0 else "INCONCLUSIVE"))
json.dump(R,open("banks/results.json","w"),indent=1); print(json.dumps(R,indent=1))
