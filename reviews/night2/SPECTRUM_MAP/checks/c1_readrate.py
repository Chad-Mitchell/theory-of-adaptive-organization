"""C1: read-rate exponent under fBm(H) for complete reads, hold-last-value vs optimal linear predictor.
Claim tested (THEORY §2.5; formal Lemma 1(i)): elasticity of optimal read rate wrt stakes W (and drift q) = 1/(1+2H) = 1/alpha.
New claim tested here: the same exponent holds for the OPTIMAL linear predictor using all past reads (self-similarity)."""
import numpy as np, json
from fgn import fbm
P=64   # number of past reads used by the predictor (approximates the infinite past)
def cov(t,u,H): return 0.5*(np.abs(t)**(2*H)+np.abs(u)**(2*H)-np.abs(t-u)**(2*H))
def ebar_hold(T,H): s=np.arange(T); return np.mean(s**(2*H))
def opt_weights(T,H,svals):
    """Origin = last read time (B(0)=0 known). Past reads at -T,...,-P*T. Predict B(s), s in svals.
    Returns weights (len(s) x P) and error variances."""
    tp=-T*np.arange(1,P+1,dtype=float)
    C=cov(tp[:,None],tp[None,:],H)
    c=cov(tp[:,None],svals[None,:].astype(float),H)       # P x S
    w=np.linalg.solve(C,c)                                 # P x S
    err=np.abs(svals.astype(float))**(2*H)-np.sum(w*c,axis=0)
    return w.T,err
def ebar_opt(T,H):
    s=np.arange(T); _,err=opt_weights(T,H,s); return float(np.mean(err))
out={}
Hs=(0.25,0.5,0.75); Ts=np.unique(np.round(np.logspace(np.log10(2),np.log10(4096),70)).astype(int))
for H in Hs:
    eh=np.array([ebar_hold(T,H) for T in Ts]); eo=np.array([ebar_opt(T,H) for T in Ts])
    ratio=eo/eh
    # scaling check: log-slope of ebar vs T at large T
    big=Ts>=64
    sl_h=np.polyfit(np.log(Ts[big]),np.log(eh[big]),1)[0]; sl_o=np.polyfit(np.log(Ts[big]),np.log(eo[big]),1)[0]
    # brute force optimum over W, both estimators (c=1, q=1)
    Ws=np.logspace(-6,-1,26); Tst={}
    Tf=np.unique(np.round(np.logspace(np.log10(2),np.log10(4096),400)).astype(int))
    ehf=np.interp(np.log(Tf),np.log(Ts),np.log(eh)); eof=np.interp(np.log(Tf),np.log(Ts),np.log(eo))
    for name,lf in (("hold",ehf),("opt",eof)):
        Tstar=[]
        for W in Ws:
            J=1.0/Tf+W*np.exp(lf); Tstar.append(Tf[np.argmin(J)])
        Tstar=np.array(Tstar,float); ok=(Tstar>=16)&(Tstar<=2048)
        el=-np.polyfit(np.log(Ws[ok]),np.log(Tstar[ok]),1)[0]   # elasticity of read rate 1/T* wrt W
        Tst[name]=dict(elasticity=round(float(el),4),n=int(ok.sum()))
    out[str(H)]=dict(predicted=round(1/(1+2*H),4),ebar_slope_hold=round(float(sl_h),4),ebar_slope_opt=round(float(sl_o),4),
                     predicted_slope=2*H,ratio_opt_over_hold_T64_T4096=[round(float(ratio[np.argmin(abs(Ts-64))]),4),round(float(ratio[-1]),4)],
                     brute_force=Tst)
# Monte Carlo check of the analytic optimal-predictor error with exact Davies-Harte paths
rng=np.random.default_rng(20261115); mc={}
for H in Hs:
    T=32; n=T*(P+2); s=np.arange(T)
    w,err=opt_weights(T,H,s)
    B=fbm(n,H,rng,size=3000)
    t0=T*(P+1)                      # last read time index
    past=np.stack([B[:,t0-T*k]-B[:,t0] for k in range(1,P+1)],axis=1)  # increments relative to last read
    pred=past@w.T                    # 3000 x T
    truth=B[:,t0+s]-B[:,t0][:,None]
    e_mc=np.mean((truth-pred)**2,axis=0); e_hold_mc=np.mean(truth**2,axis=0)
    mc[str(H)]=dict(T=T,analytic_opt=round(float(err.mean()),4),mc_opt=round(float(e_mc.mean()),4),
                    analytic_hold=round(ebar_hold(T,H),4),mc_hold=round(float(e_hold_mc.mean()),4))
out["monte_carlo_davies_harte"]=mc
print(json.dumps(out,indent=1))
