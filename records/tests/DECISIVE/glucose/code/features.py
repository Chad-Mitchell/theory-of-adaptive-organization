# Split each subject's CGM series in time; compute PREDICTORS from the first block only.
# Writes data/predictors.csv and data/outcome_block.parquet (second block, untouched here).
import pandas as pd, numpy as np
GAP=360.0   # minutes excluded around the split to cut autocorrelation leakage
MAXLAG_MIN=720.0
def grid(t,g,dt):
    k=np.round((t-t.min())/dt).astype(int); x=np.full(k.max()+1,np.nan); x[k]=g; return x
def acf_tau(x,dt):
    m=np.nanmean(x); v=np.nanvar(x); y=x-m; L=int(MAXLAG_MIN/dt)
    prev=1.0
    for lag in range(1,L+1):
        a,b=y[:-lag],y[lag:]; ok=~np.isnan(a)&~np.isnan(b)
        if ok.sum()<20: return np.nan, np.nan
        r=np.mean(a[ok]*b[ok])/v
        if lag==1: r1=r
        if r<np.exp(-1):
            frac=(prev-np.exp(-1))/(prev-r)       # linear interpolation
            return (lag-1+frac)*dt, r1
        prev=r
    return np.nan, r1
def lbgi_hbgi(g):
    g=np.clip(g,20,600); f=1.509*(np.log(g)**1.084-5.381); r=10*f**2
    return np.mean(np.where(f<0,r,0)), np.mean(np.where(f>0,r,0))
def main():
    d=pd.read_parquet("data/series.parquet")
    d=d[(d.glucose>=39)&(d.glucose<=401)]   # sensor reporting range
    P=[];O=[]
    for (sub,coh),g in d.groupby(["subject","cohort"]):
        g=g.sort_values("t_min"); dt=g.dt.iloc[0]; t=g.t_min.values
        tmid=(t.min()+t.max())/2
        a=g[t<tmid-GAP/2]; b=g[t>tmid+GAP/2]
        if len(a)*dt<12*60 or len(b)*dt<12*60: continue   # need >=12h valid data per block
        x=grid(a.t_min.values,a.glucose.values,dt)
        tau,r1=acf_tau(x,dt)
        m=a.glucose.mean(); s=a.glucose.std(ddof=1)
        lb,hb=lbgi_hbgi(a.glucose.values)
        tau_ar=-dt/np.log(np.clip(r1,1e-3,0.9999)) if r1==r1 else np.nan
        P.append(dict(subject=sub,cohort=coh,dt=dt,days1=len(a)*dt/1440,m=m,s=s,tau=tau,tau_ar1=tau_ar,
                      lbgi=lb,hbgi=hb))
        O.append(b.assign(subject=sub))
    P=pd.DataFrame(P)
    P["sigma"]=P.s*np.sqrt(2/P.tau)
    P["B_hypo"]=P.m-70; P["B_hyper"]=250-P.m
    P["z_hypo"]=P.B_hypo/(P.s*np.sqrt(2)); P["z_hyper"]=P.B_hyper/(P.s*np.sqrt(2))
    P.to_csv("data/predictors.csv",index=False)
    pd.concat(O).to_parquet("data/outcome_block.parquet")
    print(P.groupby("cohort")[["days1","m","s","tau","tau_ar1","z_hypo","z_hyper","lbgi"]].median().round(2))
    print(P.groupby("cohort").size())
    print("tau NaN:",P.tau.isna().sum()); print("SD ln tau by cohort:",P.groupby("cohort").tau.apply(lambda x:np.log(x).std()).round(3).to_dict())
    print("corr logs:",np.log(P[["tau","s"]]).corr().iloc[0,1].round(3), " corr ln tau vs z_hypo:",np.corrcoef(np.log(P.tau.dropna()),P.z_hypo[P.tau.notna()])[0,1].round(3))
    print("share z_hypo>=1.5:",P.groupby("cohort").z_hypo.apply(lambda z:(z>=1.5).mean()).round(2).to_dict())

if __name__=="__main__":
    main()
