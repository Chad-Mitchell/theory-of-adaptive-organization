"""Independent reviewer check for CAUSAL-KILL-INPUTS (pick 17). Not derived from holes.py.
Units: telegraph world, levels +/-mu, switch rate lam, white obs noise N; q := lam*mu^2 (drift level up to a constant).
(1) N16 leading-order Bayes t_A = (N/2mu^2)[ln(2mu^2/(lam N)) - gamma - 1]; (2) exact Bayes MSE mu^2*2K0(k)/(K0+K1), k=lam N/mu^2;
(3) linear (Kalman, same spectrum: OU rate 2lam, var mu^2) time constant 1/sqrt(4lam^2+4lam mu^2/N... ) exact;
(4) Monte Carlo of exact Wonham log-odds filter: mean first passage of L to 0 after a switch (own definition-matched estimate)."""
import numpy as np, json, sys
from scipy.special import k0e, k1e
from scipy.optimize import brentq
G=np.euler_gamma
def tA(lam,mu,N): return N/(2*mu**2)*(np.log(2*mu**2/(lam*N))-G-1)
def mse(lam,mu,N): k=lam*N/mu**2; return mu**2*2*k0e(k)/(k0e(k)+k1e(k))
def lin_tau(lam,mu,N):
    a=2*lam; Q=2*a*mu**2  # OU dx=-a x dt + sqrt(Q) dW
    P=N*(-a+np.sqrt(a*a+Q/N)); return 1/(a+P/N)  # closed-loop time constant
N=1.0; lam0,mu0=0.01,2.0; q0=lam0*mu0**2
out={"base":dict(lam=lam0,mu=mu0,N=N,q=q0,tA=tA(lam0,mu0,N),mse=mse(lam0,mu0,N),lin=lin_tau(lam0,mu0,N))}
def pct(a,b): return 100*(a/b-1)
# hole (a): q fixed, lam scaled
for s in [0.5,2.0,0.25,4.0]:
    lam=lam0*s; mu=np.sqrt(q0/lam)
    out[f"a_lam_x{s}"]=dict(tA_pct=pct(tA(lam,mu,N),tA(lam0,mu0,N)),mse_pct=pct(mse(lam,mu,N),mse(lam0,mu0,N)),
        lin_pct=pct(lin_tau(lam,mu,N),lin_tau(lam0,mu0,N)),valid=2*mu**2/(lam*N))
# hole (b): q x2, find lam-scale s (mu^2 = 2 q0/lam) with tA unchanged; my own root find
f=lambda s: tA(lam0*s,np.sqrt(2*q0/(lam0*s)),N)-tA(lam0,mu0,N)
s=brentq(f,1.01,10); lam=lam0*s; mu=np.sqrt(2*q0/lam)
out["b"]=dict(lam_x=s,mu2_x=mu**2/mu0**2,tA_pct=pct(tA(lam,mu,N),tA(lam0,mu0,N)),mse_pct=pct(mse(lam,mu,N),mse(lam0,mu0,N)),
    lin_pct=pct(lin_tau(lam,mu,N),lin_tau(lam0,mu0,N)),valid=2*mu**2/(lam*N))
# MC of exact Wonham filter (Euler, log-odds), first passage to 0 after each switch
def mc(lam,mu,N,npath=1000,T=None,dt=2e-3,seed=1):
    rng=np.random.default_rng(seed); T=T or 4/lam
    x=np.where(rng.random(npath)<.5,1.,-1.); L=np.zeros(npath); since=np.full(npath,np.nan); fp=[]
    burn=1/lam
    for i in range(int(T/dt)):
        t=i*dt
        sw=rng.random(npath)<lam*dt; x[sw]*=-1
        if t>burn: since[sw]=0.0
        dy=x*mu*dt+np.sqrt(N*dt)*rng.standard_normal(npath)
        Lc=np.clip(L,-40,40)
        L=L+lam*(np.exp(-Lc)-np.exp(Lc))*dt+(2*mu/N)*dy
        act=~np.isnan(since); since[act]+=dt
        hit=act&(np.sign(L)==np.sign(x))
        fp+=list(since[hit]); since[hit]=np.nan
    fp=np.array(fp); return fp.mean(), fp.std()/np.sqrt(len(fp)), len(fp)
if "--mc" in sys.argv:
    pts={"base":(lam0,mu0),"a_x0.5":(lam0*.5,np.sqrt(q0/(lam0*.5))),"a_x2":(lam0*2,np.sqrt(q0/(lam0*2))),"b":(lam,mu)}
    out["mc"]={k:dict(zip(["mean","se","n"],mc(l,m,N,seed=7))) for k,(l,m) in pts.items()}
json.dump(out,open("/tmp/rv17/rev_holes.json","w"),indent=1,default=float); print(json.dumps(out,indent=1,default=float))
