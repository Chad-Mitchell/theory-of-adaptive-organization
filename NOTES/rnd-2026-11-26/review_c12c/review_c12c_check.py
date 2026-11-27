#!/usr/bin/env python3
"""Independent hostile-review checks for C12C_ONSET.md (does not import c12c_check.py)."""
import numpy as np
from scipy.stats import norm
from scipy.integrate import quad
from scipy.optimize import minimize_scalar, brentq
LN2=np.log(2)
print("== R1. Lemma A(b) as stated: point on lower hull, cap slack, no multiplier")
pts={'A':(0.0,1.0),'B':(1.0,0.0)}  # (E,S)
D=0.5
for w in [0.25,0.5,0.9]:
  feas={k:v for k,v in pts.items() if v[0]<=D}
  dstar=min(feas,key=lambda k:feas[k][1]+w*feas[k][0])
  # E*<D so complementary slackness forces mu=0; is d* unconstrained optimal at w?
  unc=min(pts,key=lambda k:pts[k][1]+w*pts[k][0])
  # any mu>=0 at all?
  ok=[mu for mu in np.linspace(0,50,50001) if min(pts,key=lambda k:pts[k][1]+(w+mu)*pts[k][0])==dstar]
  print(f"  w={w}: constrained d*={dstar} (E*={pts[dstar][0]}<D={D}, on hull: yes); unconstrained argmin at w: {unc};"
        f" mu with CS (mu=0) works: {unc==dstar}; smallest mu>=0 that works ignoring CS: {ok[0] if ok else None:.3f}")
print("== R2. V6 point C under a cap vs any stake")
P={'A':(0,1),'B':(1,0),'C':(0.6,0.6)}
capsel={D:min([k for k in P if P[k][0]<=D],key=lambda k:P[k][1]) for D in [0.0,0.3,0.6,0.8,1.0]}
stk=set(min(P,key=lambda k:P[k][1]+w*P[k][0]) for w in np.concatenate([np.linspace(0,10,100001),[1e9]]))
print("  cap-selected:",capsel," stake-selected set:",sorted(stk))
print("== R3. Theorem O(iii) with a flat segment of g_w (f piecewise linear)")
kap,w=1.0,1.0
f=lambda x: np.maximum(2-x, np.maximum(1.5-0.5*(x-1)*1.0, 0.0)*0+ (1.0-(x-1))*0 ) # placeholder
# explicit convex nonincreasing f: slope -2 on [0,0.5], -1 on [0.5,1.5], -0.25 on [1.5,inf)
def f(x):
  x=np.asarray(x,float)
  return np.where(x<=0.5,3-2*x,np.where(x<=1.5,2.0-(x-0.5),1.0-0.25*(x-1.5)))
g=lambda x: w*f(x)+kap*x
xs=np.linspace(0,4,400001); gv=g(xs); mins=xs[gv<=gv.min()+1e-9]
print(f"  argmin g_w = [{mins.min():.4f},{mins.max():.4f}] (x_w={mins.min():.4f}, x_w'={mins.max():.4f})")
Dcap=float(f(1.0)); xD=1.0
fl=(f(xD)-f(xD-1e-6))/1e-6
print(f"  cap D={Dcap}: x_D={xD} > x_w; note's mu = kap/|f'(x_D-)| - w = {kap/abs(fl)-w:.3e} (note claims >0)")
print("== R4. Class A recompute (a=0.8, Var=1, kap=0.05, eps=1e-3), independent root finding")
a,Var,kap,eps=0.8,1.0,0.05,1e-3; s2=(1-a*a)*Var; z=norm.isf(eps/2)
Df=lambda I: Var*((1-a*a)+a*a*2**(-2*I))
for B in [2.1,2.6,3.0,3.25]:
  DB=(B/z)**2
  I=brentq(lambda I: Df(I)-DB,0,40)
  dD=(Df(I+1e-7)-Df(I-1e-7))/2e-7; wst=kap/abs(dD)
  print(f"  B={B}: I_req root={I:.6f} closed={0.5*np.log2(a*a*Var*z*z/(B*B-z*z*s2)):.6f};"
        f" w* numeric={wst:.6f} closed={kap*z*z/(2*LN2*(B*B-z*z*s2)):.6f}")
print(f"  B0={z*np.sqrt(Var):.5f}, B_fl={z*np.sqrt(s2):.5f}, w1={kap/(2*LN2*a*a*Var):.6f}")
print("== R5. Class A scope: a non-Gaussian (tail-flag) memory vs I_req at B=0.99*B0")
B=0.99*z*np.sqrt(Var); sh=np.sqrt(s2)
Ig=0.5*np.log2(a*a*Var*z*z/(B*B-z*z*s2))
def ruin_flag(t,v):
  # M=+ if X>t, - if X<-t, 0 else; predictor a*v*sign for flagged, 0 otherwise
  pin=quad(lambda x: norm.pdf(x)*(norm.sf((B-a*x)/sh)+norm.cdf((-B-a*x)/sh)),-t,t,limit=200)[0]
  pout=2*quad(lambda x: norm.pdf(x)*(norm.sf((B-a*(x-v))/sh)+norm.cdf((-B-a*(x-v))/sh)),t,np.inf,limit=200)[0]
  return pin+pout
def Hbits(t):
  p=norm.sf(t); q=1-2*p
  return -(2*p*np.log2(p)+q*np.log2(q))
best=None
for t in np.linspace(2.0,4.5,126):
  r=minimize_scalar(lambda v: ruin_flag(t,v),bounds=(0,6),method='bounded')
  if r.fun<=eps and (best is None or Hbits(t)<best[0]): best=(Hbits(t),t,r.x,r.fun)
print(f"  Gaussian I_req = {Ig:.5f} bits")
print(f"  tail-flag memory: H(M)={best[0]:.5f} bits at t={best[1]:.3f}, v={best[2]:.3f}, ruin={best[3]:.3e}" if best else "  tail-flag: none feasible")
# Monte Carlo confirmation of R5
rng=np.random.default_rng(7); n=20_000_000
X=rng.normal(0,1,n); eta=rng.normal(0,sh,n); t,v=best[1],best[2]
xh=np.where(X>t,v,np.where(X<-t,-v,0.0)); e=a*X-a*xh+eta
blind=np.mean(np.abs(a*X+eta)>=B)
print(f"  MC (2e7): tail-flag ruin={np.mean(np.abs(e)>=B):.3e}; blind ruin={blind:.3e}; flag rate={np.mean(xh!=0):.2e}")
print("== R6. CT22 path: tau_S -> inf, B_slack monotone (closed form), width slope")
y,c,s02,sig,L=1.0,0.05,0.09,1.0,np.log(1e3)
def band(w):
  al=w*sig**2/2; be=w*w*sig**4/3
  th=lambda t: 2*(y-c/t-al*t)/(s02+be*t**3)
  tE=np.sqrt(c/al)
  r=minimize_scalar(lambda t:-th(t),bounds=(c/y*1.000001,tE),method='bounded',options={'xatol':1e-13})
  return r.x,tE,L/th(r.x),L/th(tE)
ws=np.logspace(-6,0,13); rows=[band(w) for w in ws]
for w,(tS,tE,bm,bs) in zip(ws,rows):
  thE=2*(y-np.sqrt(2*c*w*sig**2))/(s02+(sig**4/3)*(2*c/sig**2)**1.5*np.sqrt(w))
  print(f"  w={w:.1e} tau_S={tS:10.3f} tau_S*sqrt(w)={tS*np.sqrt(w):.4f} B_min={bm:.6f} B_slack={bs:.6f} (closed {L/thE:.6f}) width={bs-bm:.3e}")
wd=np.array([r[3]-r[2] for r in rows]); sl=np.polyfit(np.log(ws[:6]),np.log(wd[:6]),1)[0]
print(f"  log-log slope of width at small w: {sl:.4f}; B_slack increasing in w: {all(np.diff([r[3] for r in rows])>0)}")
print(f"  limit L*s0^2/(2y) = {L*s02/(2*y):.6f}")
print("== R7. CT25 reset path: w*(B) and a unit-rescaling test")
def wstar_num(c,sig,B):
  tmax=B*B/(z*z*sig*sig)
  return brentq(lambda w: np.sqrt(2*c/(w*sig*sig))-tmax,1e-12,1e12)
for c_,s_,B_ in [(0.05,1,1),(0.05,1,2),(0.2,0.5,1.3)]:
  print(f"  c={c_} sig={s_} B={B_}: w*_num={wstar_num(c_,s_,B_):.6g} formula={2*c_*z**4*s_**2/B_**4:.6g}")
lam=3.7  # rescale x-units: B->lam B, sig->lam sig ; w must scale lam^-2
print(f"  rescale x by {lam}: w* ratio={wstar_num(0.05,lam,lam)/wstar_num(0.05,1,1):.6f} vs lam^-2={lam**-2:.6f}")
print("== R8. Still 2020 Gaussian: sup_s I_rel/I_mem = rho^2 (efficiency condition I_rel/I_mem >= T/T')")
for rho in [0.5,0.8,0.95]:
  s=np.logspace(-12,np.log10(1-1e-12),400001)
  ratio=(-0.5*np.log(1-rho*rho*s))/(0.5*np.log(1/(1-s)))
  print(f"  rho={rho}: sup I_rel/I_mem={ratio.max():.8f} rho^2={rho*rho:.8f}")
print("== R9. Scores")
for name,ph,vh,pm,vm,h in [("residual review",0.85,2,0.12,3,1),("whole sunk",0.85,2,0.12,3,2.5),("C12c-L",0.9,2,0.08,1,2),("C12c-G",0.4,3,0.6,2,2),("C12d",0.6,2,0.3,2,1.5),("orig C12c",0.7,2,0.25,2,2)]:
  e=ph*vh+pm*vm; print(f"  {name}: EIV={e:.3f} per h={e/h:.3f} (p sum {ph+pm:.2f})")
