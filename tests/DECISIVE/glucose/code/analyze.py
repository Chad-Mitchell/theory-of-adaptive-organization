# OUTCOME analysis for the glucose test. Run only after PREREG.md is hashed and committed.
import numpy as np, pandas as pd, statsmodels.api as sm, statsmodels.formula.api as smf, json, sys
sys.path.insert(0,"glucose/code"); from simproc import episodes
from features import grid, acf_tau
NB=sm.families.NegativeBinomial
P=pd.read_csv("glucose/data/predictors.csv"); O=pd.read_parquet("glucose/data/outcome_block.parquet")
MINRUN={5.0:3,15.0:2}
def count_eps(g,thr,below,dt):
    k=np.round((g.t_min.values-g.t_min.values.min())/dt).astype(int)
    x=np.full(k.max()+1,np.nan); x[k]=g.glucose.values
    # episodes counted within contiguous runs of valid data (gaps break runs)
    c=0; seg=[]
    for v in x:
        if np.isnan(v):
            if seg: c+=episodes(np.array(seg),MINRUN[dt]); seg=[]
        else: seg.append(v<thr if below else v>thr)
    if seg: c+=episodes(np.array(seg),MINRUN[dt])
    return c, len(g)*dt/1440
rows=[]
for sub,g in O.groupby("subject"):
    dt=P.loc[P.subject==sub,"dt"].iloc[0]; g=g.sort_values("t_min")
    h,days=count_eps(g,70,True,dt); H,_=count_eps(g,250,False,dt)
    rows.append(dict(subject=sub,hypo2=h,hyper2=H,days2=days))
Y=pd.DataFrame(rows); D=P.merge(Y,on="subject")
# circularity guard: tau from the first block with the lower half censored at the block median (upper-half dynamics only)
S=pd.read_parquet("glucose/data/series.parquet"); S=S[(S.glucose>=39)&(S.glucose<=401)]
tu=[]; inb=[]
for sub,g in S[S.subject.isin(D.subject)].groupby("subject"):
    dt=g.dt.iloc[0]; g=g.sort_values("t_min"); t=g.t_min.values; tmid=(t.min()+t.max())/2
    a=g[t<tmid-180]; med=a.glucose.median()
    x=grid(a.t_min.values,np.maximum(a.glucose.values,med),dt); tu.append((sub,acf_tau(x,dt)[0]))
    h1,d1=count_eps(a,70,True,dt); inb.append((sub,h1,d1))
D=D.merge(pd.DataFrame(tu,columns=["subject","tau_up"]),on="subject").merge(pd.DataFrame(inb,columns=["subject","hypo1","days1b"]),on="subject")
D["lt"]=np.log(D.tau); D["ls"]=np.log(D.s); D["lsig"]=np.log(D.sigma)
D.to_csv("glucose/data/analysis_table.csv",index=False)
R={}
def fit(f,d,y,off):
    d=d.assign(off=np.log(d[off]))
    # NB2 with alpha estimated by ML (statsmodels discrete NB), fallback GLM NB alpha=1
    mod=smf.negativebinomial(f.replace("y",y,1),data=d,offset=d.off)
    m=mod.fit(disp=0,maxiter=500)
    if np.isnan(np.asarray(m.bse)).any():   # DEVIATION D1 (numerical): Hessian failed -> BFGS, then GLM-NB with ML alpha + HC0 SEs
        m=mod.fit(disp=0,method="bfgs",maxiter=5000,start_params=m.params)
    if np.isnan(np.asarray(m.bse)).any():
        al=float(np.clip(m.params.get("alpha",1.0),1e-3,50))
        m=smf.glm(f.replace("y",y,1),data=d,offset=d.off,family=sm.families.NegativeBinomial(alpha=al)).fit(cov_type="HC0")
    return m
def ci(m,k): b=m.params[k]; s=m.bse[k]; return [round(b,3),round(b-1.96*s,3),round(b+1.96*s,3)]
BSTAR={"REPLACEBG_T1D":-0.82,"SHANGHAI":-0.65}
for name,coh in [("REPLACEBG_T1D",["REPLACEBG_T1D"]),("SHANGHAI",["SH_T1DM","SH_T2DM"]),("ALL4",["REPLACEBG_T1D","SH_T1DM","SH_T2DM","COLAS"])]:
    r={}
    d=D[D.cohort.isin(coh)&(D.B_hypo>0)].copy(); r["n_hypo"]=len(d); r["events_hypo"]=int(d.hypo2.sum())
    ce="+C(cohort)" if len(coh)>1 else ""
    m1=fit("y~lt+cr(z_hypo,df=3)"+ce,d,"hypo2","days2"); r["P1_fixed_spread_slope_hypo"]=ci(m1,"lt")
    d["lB"]=np.log(d.B_hypo)
    m2=fit("y~lt+lsig+lB"+ce,d,"hypo2","days2"); r["P2_fixed_sigma"]=dict(b_tau=ci(m2,"lt"),b_sigma=ci(m2,"lsig"),b_B=ci(m2,"lB"))
    try:
        w1=m2.wald_test("lB + lsig = 0",scalar=True); w2=m2.wald_test("lt - 0.5*lsig = -1",scalar=True); w3=m2.wald_test("lt - 0.5*lsig = 0",scalar=True)
        r["P2_wald_p"]=dict(eps_B_eq_minus_eps_sigma=float(w1.pvalue),identity_continuous=float(w2.pvalue),identity_incident=float(w3.pvalue))
    except Exception as e: r["P2_wald_p"]=str(e)
    d["zc"]=(d.z_hypo-d.z_hypo.mean())/d.z_hypo.std()
    m3=fit("y~lt*zc+lsig"+ce,d,"hypo2","days2"); r["P3_interaction_lt_x_z"]=ci(m3,"lt:zc")
    # baseline: LBGI only vs LBGI + ln tau
    d["llb"]=np.log(d.lbgi+1e-3)
    b0=fit("y~llb+I(llb**2)"+ce,d,"hypo2","days2"); b1=fit("y~llb+I(llb**2)+lt"+ce,d,"hypo2","days2")
    r["P5_LBGI_baseline"]=dict(b_tau_given_LBGI=ci(b1,"lt"),dAIC=round(b0.aic-b1.aic,2),LR_p=float(1-__import__("scipy").stats.chi2.cdf(2*(b1.llf-b0.llf),1)))
    # circularity guard: tau from upper-half dynamics only
    d["ltu"]=np.log(d.tau_up)
    g1=fit("y~ltu+cr(z_hypo,df=3)"+ce,d.dropna(subset=["ltu"]),"hypo2","days2"); r["G1_tau_upper_half_slope"]=ci(g1,"ltu")
    # in-block (circular) estimate for contrast
    g2=fit("y~lt+cr(z_hypo,df=3)"+ce,d,"hypo1","days1b"); r["G2_in_block_circular_slope"]=ci(g2,"lt")
    # conditional on first-block episode rate (robustness, not a kill)
    d["lh1"]=np.log((d.hypo1+0.5)/d.days1b)
    g3=fit("y~lt+cr(z_hypo,df=3)+lh1"+ce,d,"hypo2","days2"); r["G3_slope_given_first_block_rate"]=ci(g3,"lt")
    # cold regime
    dc=d[d.z_hypo>=1.5]; r["n_cold"]=len(dc)
    if len(dc)>=30:
        mc=fit("y~lt+lsig+lB"+ce,dc,"hypo2","days2"); r["cold_b_tau_given_sigma_B"]=ci(mc,"lt")
    # hyper (secondary)
    e=D[D.cohort.isin(coh)&(D.B_hyper>0)].copy(); r["n_hyper"]=len(e); r["events_hyper"]=int(e.hyper2.sum())
    if r["events_hyper"]>0:
        h1=fit("y~lt+cr(z_hyper,df=3)"+ce,e,"hyper2","days2"); r["S_hyper_fixed_spread_slope"]=ci(h1,"lt")
    # sensitivity: tau from AR(1) lag-1
    d["lta"]=np.log(d.tau_ar1); s1=fit("y~lta+cr(z_hypo,df=3)"+ce,d,"hypo2","days2"); r["S_tau_ar1_slope"]=ci(s1,"lta")
    R[name]=r
# collapse across cohorts: ln(rate*tau) vs z; cohort offsets after a common spline
d=D[D.B_hypo>0].copy(); d["off"]=np.log(d.days2)-np.log(d.tau)
d=d.rename(columns={"hypo2":"yy"}); mc=fit("y~cr(z_hypo,df=4)+C(cohort,Treatment('REPLACEBG_T1D'))",d.assign(days_tau=d.days2/d.tau),"yy","days_tau")
R["P4_collapse_offsets_vs_REPLACEBG"]={k:ci(mc,k) for k in mc.params.index if "cohort" in k}
# verdicts
def verdict(sl,bstar):
    b,lo,hi=sl
    if abs(b-0)<abs(b-bstar) and (lo>bstar or hi<bstar): return "KILL"
    if hi<0 and lo<=bstar<=hi: return "HIT"
    if hi<0: return "SIGN-RIGHT, SIZE-OFF"
    return "INCONCLUSIVE"
R["verdict_REPLACEBG_T1D"]=verdict(R["REPLACEBG_T1D"]["P1_fixed_spread_slope_hypo"],BSTAR["REPLACEBG_T1D"])
R["verdict_SHANGHAI"]=verdict(R["SHANGHAI"]["P1_fixed_spread_slope_hypo"],BSTAR["SHANGHAI"])
R["literal_minus1_check"]={k:verdict(R[k]["P1_fixed_spread_slope_hypo"],-1.0) for k in ["REPLACEBG_T1D","SHANGHAI"]}
json.dump(R,open("glucose/results.json","w"),indent=1); print(json.dumps(R,indent=1))
