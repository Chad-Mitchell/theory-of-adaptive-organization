"""Referee check R1: (a) sensitivity of kappa_opt/kappa_hold to the number of past reads P (executor used P=64);
(b) continuum limit (executor averaged s over integers 0..T-1); (c) a FIXED (non-scale-equivariant) predictor, an EWMA of
reads with a fixed time constant, does NOT give error ~ T^{2H}: the 'whatever linear predictor' wording is too strong."""
import numpy as np, json
def cov(t,u,H): return 0.5*(np.abs(t)**(2*H)+np.abs(u)**(2*H)-np.abs(t-u)**(2*H))
def ratio(H,P,T=1.0,ns=400):
    s=(np.arange(ns)+0.5)/ns*T; tp=-T*np.arange(1,P+1,dtype=float)
    C=cov(tp[:,None],tp[None,:],H); c=cov(tp[:,None],s[None,:],H); w=np.linalg.solve(C,c)
    err=s**(2*H)-np.sum(w*c,axis=0); return float(err.mean()/np.mean(s**(2*H)))
out={"ratio_vs_P":{}}
for H in (0.25,0.75):
    out["ratio_vs_P"][str(H)]={str(P):round(ratio(H,P),4) for P in (8,64,256,1024)}
# (c) fixed EWMA over reads with weight decay per unit TIME (tau=50 time units), predictor = sum_k w_k B(-kT), normalized
def ewma_err(H,T,tau=50.0,P=400,ns=50):
    s=(np.arange(ns)+0.5)/ns*T; tp=-T*np.arange(0,P,dtype=float)
    w=np.exp(tp/tau); w/=w.sum()
    # error of predicting B(s) by sum w_k B(tp_k), B(0)=0 included at k=0
    Cpp=cov(tp[:,None],tp[None,:],H); cps=cov(tp[:,None],s[None,:],H)
    e=s**(2*H)-2*w@cps+w@Cpp@w; return float(np.mean(e))
Ts=np.array([1,2,4,8,16,32,64,128.0])
for H in (0.25,0.75):
    e=np.array([ewma_err(H,T) for T in Ts]); out[f"fixed_ewma_local_slopes_H{H}"]=[round(float(x),3) for x in np.diff(np.log(e))/np.diff(np.log(Ts))]
    out[f"predicted_2H_H{H}"]=2*H
print(json.dumps(out,indent=1)); json.dump(out,open("r1_pastlen.json","w"),indent=1)
