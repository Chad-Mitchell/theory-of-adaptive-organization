"""SPECTRUM-MAP-FIXES own checks, pass 2 (pick 26): replaces fixes_check.py parts B2 and C, which were numerically unreliable
(B2: excess from c - w.b cancellation went below zero at alpha = 2; C: quad on a 1e28 dynamic range at alpha = 3.5 warned
'probably divergent'). Same models; B2 now integrates the error spectrum |1-H|^2 Sx + |H|^2 Nd directly with exact trapezoid
weights; C integrates in log-frequency on a fixed dense grid. Own code; imports nothing from the repo."""
import numpy as np, json, math
from scipy import optimize
R={}
# B2
def grid(L,taus):
    th=np.unique(np.concatenate([np.logspace(-14,np.log10(np.pi),60001)]))
    w=np.zeros_like(th); d=np.diff(th); w[:-1]+=d/2; w[1:]+=d/2; return th,w
def B2(a,L,taus=4.0):
    th,wt=grid(L,taus); wmin=10.0**(-L)/taus; Sx=(4*np.sin(th/2)**2+wmin**2)**(-a/2); Nd=taus**a; Sy=Sx+Nd
    eopt=Nd*(1-Nd/np.exp(np.sum(np.log(Sy)*wt)/np.pi))
    z=np.exp(-1j*th)
    def mse(lam):
        Am=np.array([z**k for k in range(4)]+[(1-np.exp(-lam))/(1-np.exp(-lam)*z)])
        Q=np.real(Am[:,None]*np.conj(Am[None])*Sy*wt).sum(-1); b=np.real(Am*Sx*wt).sum(-1)
        w=np.linalg.solve(Q,b); H=w@Am
        return float(np.sum((np.abs(1-H)**2*Sx+np.abs(H)**2*Nd)*wt)/np.pi)
    o=optimize.minimize_scalar(lambda ll:mse(np.exp(ll)),bounds=(np.log(10.0**(-L-1)/taus),0),method="bounded",options=dict(xatol=1e-6))
    return (o.fun-eopt)/eopt
B={}
for L in (2,4):
    for a in (1.8,1.9,1.95,2.0,2.05,2.1,2.2):
        ex=B2(a,L); B[f"L{L}_a{a}"]=dict(excess=float(f"{ex:.3g}"),c=None if a==2 else round(ex/(a-2)**2,4))
R["B2_discrete_taps_plus_one_ewma"]=B
# C
lw=np.linspace(math.log(1e-30),math.log(1e30),400001); W=np.exp(lw); dl=lw[1]-lw[0]
def ewma_tau(a,tauE,mode):
    pref=tauE if mode=="var" else tauE**a
    S=pref*np.exp(-(a/2)*np.logaddexp(0,2*np.log(W*tauE)))
    def mse(lt):
        t2=np.exp(2*lt); g=(W*W*t2/(1+W*W*t2))*S+1/(1+W*W*t2)
        return np.sum(g*W)*dl/np.pi
    o=optimize.minimize_scalar(mse,bounds=(-20,40),method="bounded",options=dict(xatol=1e-8)); return o.x
C={}
for mode in ("var","q"):
    for a in (1.5,2.0,2.5,3.5):
        t1,t2=ewma_tau(a,1e7,mode),ewma_tau(a,1e8,mode)
        th_=(min(1-1/a,2/3) if mode=="var" else (0.0 if a<3 else (3-a)/3))
        C[f"{mode}_a{a}"]=dict(slope=round((t2-t1)/math.log(10),3),theory=round(th_,3))
R["C_memory_time_slope"]=C
json.dump(R,open("fixes_check2.json","w"),indent=1)
for k,v in R.items(): print(k,json.dumps(v))
