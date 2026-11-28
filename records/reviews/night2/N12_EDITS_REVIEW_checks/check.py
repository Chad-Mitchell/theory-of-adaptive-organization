# Independent spot-check of N12 (reviewer's own code; not derived from author/referee scripts)
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy.special import gamma
w=1.0; c=1.0; qu=1.0
def onsetN(flat, pooled, lo=1.0001, hi=1e40):
    f=lambda lnN: np.log(pooled(np.exp(lnN))) - np.log(flat(np.exp(lnN)))
    return np.exp(brentq(f, np.log(lo), np.log(hi), xtol=1e-12))
def slope(Nfun, rho, d=0.05):
    return (np.log(Nfun(rho*np.exp(d)))-np.log(Nfun(rho*np.exp(-d))))/(2*d)
# --- A: continuous sensing, MMSE = K q^{1/a} r^{1-1/a}, precision price c r^{-theta}
def cont(alpha,theta):
    K=1/np.sin(np.pi/alpha)
    def unit(W,q):  # min_r W K q^{1/al} r^{1-1/al} + c r^{-theta}
        g=lambda lr: W*K*q**(1/alpha)*np.exp(lr*(1-1/alpha))+c*np.exp(-theta*lr)
        return minimize_scalar(g,bounds=(-80,80),method='bounded',options={'xatol':1e-11}).fun
    def Nstar(rho):
        qg=rho*qu
        flat=lambda N: N*unit(w,qg+qu)
        pooled=lambda N: unit(N*w,qg)+N*unit(w,qu)
        return onsetN(flat,pooled)
    return Nstar
# --- B: exact reset reads, hold-last-value, fBm increment var q tau^{alpha-1}
def reset(alpha):
    def unit(W,q):  # min_T c/T + W q T^{alpha-1}/alpha  (time-avg of q t^{alpha-1})
        g=lambda lT: c*np.exp(-lT)+W*q*np.exp(lT*(alpha-1))/alpha
        return minimize_scalar(g,bounds=(-80,80),method='bounded',options={'xatol':1e-11}).fun
    def Nstar(rho):
        qg=rho*qu
        return onsetN(lambda N:N*unit(w,qg+qu), lambda N:unit(N*w,qg)+N*unit(w,qu))
    return Nstar
print("A. priced precision: local slope dlnN*/dln rho at rho=1e-4 (expect -(1+theta))")
for th in (0.5,1,2):
    print(" theta",th,[round(float(slope(cont(al,th),1e-3 if th==2 else 1e-4)),4) for al in (1.2,1.5,2,2.5,3.5)])
print("B. exact reset reads, expect -1:",[round(float(slope(reset(al),1e-4)),4) for al in (1.2,1.5,2,2.5,2.9)])
print("   finite rho=0.1:",[round(float(slope(reset(al),0.1)),3) for al in (1.5,2,2.5)])
# --- C: noisy periodic reads, optimal (Gaussian conditioning) estimator, fBm H=(alpha-1)/2
def mfun(H, s_grid, M=120, nt=8):
    # time-avg MSE over (0,1) of x(t) given M noisy reads at -M+1..0 (T=1, q=1), noise var s
    tk=np.arange(-M+1,1,dtype=float); t0=-M-0.5  # anchor fBm far in past
    cov=lambda a,b: 0.5*(np.abs(a-t0)**(2*H)+np.abs(b-t0)**(2*H)-np.abs(a-b)**(2*H))
    C=cov(tk[:,None],tk[None,:]); ts=(np.arange(nt)+0.5)/nt
    out=[]
    for s in s_grid:
        A=C+s*np.eye(M); errs=[]
        for t in ts:
            k=cov(tk,t); v=cov(t,t)-k@np.linalg.solve(A,k); errs.append(v)
        out.append(np.mean(errs))
    return np.array(out)
def noisy(alpha,sig2):
    H=(alpha-1)/2; sg=np.logspace(-8,14,221); m=mfun(H,sg)
    lm=lambda s: np.exp(np.interp(np.log(s),np.log(sg),np.log(m)))
    def mse(T,q): return q*T**(2*H)*lm(np.clip(sig2/(q*T**(2*H)),1e-8,1e14))
    def unit(W,q):
        g=lambda lT: c*np.exp(-lT)+W*mse(np.exp(lT),q)
        return minimize_scalar(g,bounds=(-40,60),method='bounded',options={'xatol':1e-9}).fun
    def Nstar(rho):
        qg=rho*qu
        return onsetN(lambda N:N*unit(w,qg+qu), lambda N:unit(N*w,qg)+N*unit(w,qu))
    return Nstar
print("C. noisy reads sigma2=1e-3: local slopes at rho = 1e-1,1e-2,1e-3,1e-4,1e-5 (expect drift to -2)")
for al in (1.5,2,2.5):
    f=noisy(al,1e-3); print(" alpha",al,[round(float(slope(f,r,0.15)),3) for r in (1e-1,1e-2,1e-3,1e-4,1e-5)])
print("   sigma2=1e-6 (second noise level):")
for al in (1.5,2,2.5):
    f=noisy(al,1e-6); print(" alpha",al,[round(float(slope(f,r,0.15)),3) for r in (1e-1,1e-3,1e-5,1e-7)])
