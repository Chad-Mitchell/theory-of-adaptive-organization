#!/usr/bin/env python3
"""Checks for C12C_ONSET.md (local notes; numpy/scipy only; no network)."""
import numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy.stats import norm
LN2=np.log(2)
print("== 1. Gaussian AR(1) (CT4 class): I* = max(I_w, I_req), w_eff = max(w, w*(D))")
a,Var,kap=0.8,1.0,0.05
sn2=(1-a*a)*Var
f=lambda I: Var*((1-a*a)+a*a*2**(-2*I))
w1=kap/(2*LN2*a*a*Var)
Iw=lambda w: max(0.0,0.5*np.log2(2*LN2*w*a*a*Var/kap))
Ireq=lambda D: max(0.0,0.5*np.log2(a*a*Var/(D-sn2))) if D>sn2 else np.inf
wstar=lambda D: kap/(2*LN2*(D-sn2)) if D<Var else w1
grid=np.linspace(0,12,1200001)
maxerr=0;cnt=0
for w in [0.0,0.02,w1*0.999,w1*1.001,0.2,1.0,5.0]:
  for D in [sn2*1.0001,0.4,0.6,0.9,0.999,1.2]:
    feas=f(grid)<=D
    J=w*f(grid)+kap*grid; J[~feas]=np.inf
    Ib=grid[np.argmin(J)]; Ip=max(Iw(w),Ireq(D))
    maxerr=max(maxerr,abs(Ib-Ip)); cnt+=1
    # KKT: if binding, w+mu = w*(D)
    if Ireq(D)>Iw(w):
      g=-(f(Ireq(D)+1e-7)-f(Ireq(D)))/1e-7
      mu=kap/g-w
      assert abs((w+mu)-wstar(D))/wstar(D)<1e-4, (w,D)
print(f"  w1={w1:.6f}; {cnt} (w,D) cases, max |I_brute - I_formula| = {maxerr:.2e} (grid 1e-5)")
print(f"  w*(D) at D->Var: {wstar(Var-1e-9):.6f} (equals w1); w*(D) nonincreasing in D:",
      all(np.diff([wstar(D) for D in np.linspace(sn2+1e-3,Var-1e-6,500)])<=0))
print("== 2. per-step two-sided chance cap P(|e|>=B)<=eps <=> D <= (B/z_eps)^2 (Gaussian error)")
eps=1e-3; z=norm.isf(eps/2); print(f"  z_eps={z:.3f} (CT25 lists 3.291 at 1e-3)")
B0=z*np.sqrt(Var); Bfl=z*np.sqrt(sn2)
print(f"  B_floor={Bfl:.4f}  B_0={B0:.4f}")
rng=np.random.default_rng(1)
for B in [Bfl*1.05,(Bfl+B0)/2,B0*0.99,B0*1.01]:
  I=Ireq((B/z)**2); D=f(I)
  # simulate: world AR(1), memory = X_t + Gaussian noise with I bits, linear MMSE predictor
  n=2_000_000; X=rng.normal(0,np.sqrt(Var),n); eta=rng.normal(0,np.sqrt(sn2),n)
  Xn=a*X+eta
  if np.isfinite(I) and I>0:
    nv=Var/(2**(2*I)-1); M=X+rng.normal(0,np.sqrt(nv),n); xh=(Var/(Var+nv))*M
  else: xh=0*X
  e=Xn-a*xh; p=np.mean(np.abs(e)>=B)
  print(f"  B={B:.4f}: I_req={I:.4f} bits, D={D:.4f}, MC ruin {p:.2e} (cap {eps:.0e}); w*={wstar(D):.4f}")
print("  B_slack(w) for w>w1 = z*sqrt(sn2 + kap/(2 ln2 w)):",
      [round(z*np.sqrt(sn2+kap/(2*LN2*w)),4) for w in [w1,0.2,1,5,100]])
print("== 3. CT22 path (Lemma B9 point y=1,c=1/20,sigma=1,s0^2=0.09,eps=1e-3): band [B_min,B_slack] vs w")
y,c,s02,sig=1.0,0.05,0.09,1.0
L=np.log(1/eps)
for w in [1.0,0.3,0.1,0.03,0.01,0.001,1e-4]:
  al=w*sig**2/2; be=w*w*sig**4/3
  th=lambda t: 2*(y-c/t-al*t)/(s02+be*t**3)
  tE=np.sqrt(c/al)
  r=minimize_scalar(lambda t:-th(t),bounds=(c/y*1.0001,tE),method='bounded',options={'xatol':1e-12})
  tS=r.x; Bmin=L/th(tS); Bsl=L/th(tE)
  print(f"  w={w:<7g} tau_S={tS:9.4f} tau_E={tE:9.4f} B_min={Bmin:.5f} B_slack={Bsl:.5f} width={(Bsl-Bmin):.2e}")
print(f"  w=0 limit: theta(tau)=2(y-c/tau)/s0^2 increasing, sup=2y/s0^2 -> B_min=B_slack={L*s02/(2*y):.5f}; judgment cannot raise survival")
print("== 4. CT25 reset path: tau* = min(tau_E(w), tau_max(B)); w*(B) = 2c z^4 sigma^2 / B^4")
c,sig=0.05,1.0
for w,B in [(0.0,1.0),(0.01,1.0),(1.0,1.0),(1.0,3.0),(10.0,0.5)]:
  tmax=B*B/(z*z*sig*sig); wst=2*c*z**4*sig**2/B**4
  Jf=lambda t: c/t+w*sig**2*t/2
  r=minimize_scalar(Jf,bounds=(1e-9,tmax),method='bounded',options={'xatol':1e-14})
  tE=np.sqrt(2*c/(w*sig**2)) if w>0 else np.inf
  print(f"  w={w:<5} B={B}: tau*_num={r.x:.6f} formula={min(tE,tmax):.6f} w*(B)={wst:.4f} -> regime {'cap' if wst>w else 'stake'}")
print("== 5. Still 2020 two-bath reading: Gaussian channel M=X+N, objective I_mem - beta*I_rel; nontrivial iff beta > 1/rho^2")
for rho in [0.5,0.8,0.95]:
  s=np.linspace(1e-9,1-1e-9,200001)
  Imem=0.5*np.log(1/(1-s)); Irel=-0.5*np.log(1-rho*rho*s)
  ratio=np.min(Imem/Irel)
  print(f"  rho={rho}: inf_s I_mem/I_rel = {ratio:.6f}; 1/rho^2 = {1/rho**2:.6f}")
