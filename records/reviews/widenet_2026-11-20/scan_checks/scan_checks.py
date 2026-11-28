"""Wide-net scan checks (not part of the repo's suite). Run: nice -n 19 python3 scan_checks.py"""
import math, numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy.integrate import quad
rng = np.random.default_rng(0)
print("== C1 ergodicity ==")
# (a) Peters coin: x1.5 / x0.6. ensemble mean +5%/step, time-average growth ln(.9)/2 <0
ens = 0.5*1.5+0.5*0.6; tav = 0.5*math.log(1.5)+0.5*math.log(0.6)
W = np.exp(np.cumsum(np.log(rng.choice([1.5,0.6], size=(20000,1000))),axis=1))
print("coin: ensemble factor %.3f, time-avg log growth %.4f; P(W ever hits 0)=0; P(min W<0.01 by T=1000)=%.3f"%(ens,tav,(W.min(1)<0.01).mean()))
# (b) R1 copies, additive J vs multiplicative time-average growth
g,h,wE1,X,p = 0.10,0.004,0.01,0.6,0.2   # all-down window loses 60% of reserve
J = lambda n: n*h + wE1 + X*p**n
G = lambda n: (1-p**n)*math.log(1+g-n*h-wE1) + p**n*math.log(1+g-n*h-wE1-X)
nE = min(range(1,30), key=J); nG = max(range(1,30), key=G)
print("R1: n_E (additive/ensemble) = %d, n_G (time-average growth) = %d"%(nE,nG))
for n in range(1,8): print("  n=%d J=%.5f G=%.5f"%(n,J(n),G(n)))
# (c) Gaussian squared error, ranking monotone: E ln(1 - w e^2) decreasing in Var e (check), and exact under W'=W exp(-w l)
for v in (0.01,0.02,0.04):
    z = rng.standard_normal(10**6); print("  LG: var=%.2f E[l]=%.4f E ln(1-0.5 l)=%.5f"%(v, v, np.mean(np.log(1-0.5*v*z**2).clip(-50))))
print("== C2 bet-hedging vs common mode (CX7) ==")
beta=0.05   # common-mode shock prob per generation
a1,a0 = 1.30,0.0    # lean design: growth factor calm / shock (wiped)
b1,b0 = 1.05,0.90   # robust design
Gq = lambda q: (1-beta)*math.log((1-q)*a1+q*b1) + beta*math.log(max((1-q)*a0+q*b0,1e-300))
qs=np.linspace(1e-4,1,10001); Gs=[Gq(q) for q in qs]; qstar=qs[int(np.argmax(Gs))]
print("arith mean fitness lean %.3f robust %.4f (per-design expected-value picks lean)"%((1-beta)*a1+beta*a0,(1-beta)*b1+beta*b0))
print("geo growth: pure lean -inf, pure robust %.4f, best mixture q*=%.3f G=%.4f"%(Gq(1),qstar,max(Gs)))
print("== C3 barbell under a population-frequency ruin target (CT22 model) ==")
y,cc,ww,sg,s0,eps = 1.0,0.05,1.0,1.0,0.3,1e-3
m=lambda t: y-cc/t-ww*sg**2*t/2; th=lambda t: 2*m(t)/(s0**2+ww**2*sg**4*t**3/3); Jt=lambda t: cc/t+ww*sg**2*t/2
tE=math.sqrt(2*cc/(ww*sg**2)); tS=minimize_scalar(lambda t:-th(t),bounds=(1e-3,3),method='bounded').x
for B in (0.49,0.50,0.505):
    ts=np.linspace(tS,tE,4001); P=np.exp(-np.array([th(t) for t in ts])*B); Jv=np.array([Jt(t) for t in ts])
    tp=brentq(lambda t: th(t)-math.log(1/eps)/B, tS, tE); Jpure=Jt(tp)
    # best two-point mixture with mean P = eps: also allow a "lean" arm beyond tE (cheaper? no: tE is J-min) -> arms within [tS,tE]
    best=Jpure
    for i in range(0,len(ts),20):
        for j in range(i,len(ts),20):
            if P[i]<=eps<=P[j] and P[j]>P[i]:
                lam=(P[j]-eps)/(P[j]-P[i]); best=min(best,lam*Jv[i]+(1-lam)*Jv[j])
    print("B=%.3f pure J*=%.6f, best 2-design mix J=%.6f, gain %.2e (%.4f%%)"%(B,Jpure,best,Jpure-best,100*(Jpure-best)/Jpure))
print("== C4 Bode / Jensen for the tracker's error filter (two OU modes + white sensing noise) ==")
a=np.array([1/3.,1/90.]); v=np.array([1.,1.]); N=0.05
F=-np.diag(a); Q=np.diag(2*a*v); C=np.ones((1,2))
from scipy.linalg import solve_continuous_are
P_=solve_continuous_are(F.T,C.T,Q,np.array([[N]])); L=P_@C.T/N
Acl=F-L@C
H=lambda w_: (C@np.linalg.solve(1j*w_*np.eye(2)-Acl,L))[0,0]
lnS=lambda w_: math.log(abs(1-H(w_)))
I=quad(lnS,0,np.inf,limit=500)[0]; pred=-math.pi/2*(C@L).item()
wg=np.logspace(-5,3,4000); amp=[w_ for w_ in wg if lnS(w_)>1e-9]
print("int_0^inf ln|S| dw = %.5f ; -(pi/2)*lim sH = %.5f"%(I,pred))
print("amplification band |S|>1: %s"%( "none" if not amp else "%.3g..%.3g rad/time"%(min(amp),max(amp))))
print("== C5 redesign cost -> inaction band (Dixit 1991, quadratic loss, Brownian target) ==")
sig,w,k=1.0,1.0,0.01
b_th=(6*k*sig**2/w)**0.25
def avgcost(b,T=2000.,dt=1e-3):
    n=int(T/dt); x=0.; cost=0.; inc=rng.standard_normal(n)*sig*math.sqrt(dt)
    for e in inc:
        x+=e; cost+=w*x*x*dt
        if abs(x)>=b: cost+=k; x=0.
    return cost/T
for b in (0.5*b_th,b_th,2*b_th):
    print("  b=%.3f MC avg cost %.4f  theory %.4f"%(b,avgcost(b,T=400.),k*sig**2/b**2+w*b**2/6))
print("b* = (6 k s^2/w)^(1/4) = %.3f for k=%.3g; k 100x smaller -> b* only %.2fx smaller"%(b_th,k,100**0.25))
print("== C3b discrete designs (R1-b copies): mixing n and n+1 under a population-frequency eps ==")
p,N,eps,h=0.1,1000,5e-4,1.0
Pr=lambda n: 1-(1-p**n)**N
nR=next(n for n in range(1,50) if Pr(n)<=eps)
lam=(Pr(nR-1)-eps)/(Pr(nR-1)-Pr(nR))
print("n_R=%d (all systems), P(n_R-1)=%.4f; mix %.3f at n_R, rest at n_R-1 meets eps on average; mean copies %.3f vs %d"%(nR,Pr(nR-1),lam,lam*nR+(1-lam)*(nR-1),nR))
