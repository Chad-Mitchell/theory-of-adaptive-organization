"""S8. Theorem 2 (broadcast break), per-READ broadcast version in R1 (gamma=1/2), and vigilance at onset under it
(explains POOLSIM W3, where V ~ 2 although sqrt(N rho/(1+rho)) ~ 13.7)."""
import numpy as np, sympy as sp
from scipy.optimize import brentq
t,rho=sp.symbols('t rho',positive=True)
sol=sp.solve(sp.Eq(sp.sqrt(t*rho)+1,sp.sqrt(1+rho)),rho); print("exact threshold roots of sqrt(t rho)+1 = sqrt(1+rho):",sol," (claim 4t/(1-t)^2, t<1)")
def G(N,qg,qu,kap,c=1.0,w=1.0,h=0.0):
    return N*np.sqrt(2*c*w*(qg+qu))-np.sqrt(2*(c+N*kap)*N*w*qg)-N*np.sqrt(2*c*w*qu)-h
def Nstar(qg,qu,kap,h=0.0):
    if G(1.0,qg,qu,kap,h=h)>0: return 1.0
    lo,hi=1.0,2.0
    while G(hi,qg,qu,kap,h=h)<=0:
        lo=hi; hi*=2
        if hi>1e16: return np.inf
    return brentq(lambda n: G(n,qg,qu,kap,h=h),lo,hi,xtol=1e-10*hi)
for kap in [1e-4,1e-3,1e-2]:
    rb=4*kap/(1-kap)**2; print(f"\nkappa/c={kap}: rho_b={rb:.6g}")
    for f in [0.9,0.99,1.01,1.1,2,10,100]:
        r=f*rb; n=Nstar(r,1.0,kap)
        V=np.sqrt(n*r/((1+r)*(1+n*kap))) if np.isfinite(n) else float('nan')
        print(f"  rho={f:>6}*rho_b: N*={n:.4g}  V(N*)={V:.4f}")
print("\nPOOLSIM W3-like check: equal-cost formula sqrt(N*rho/(1+rho)) vs true V at onset (kappa=1e-3, rho=0.032):")
n=Nstar(0.032,1.0,1e-3); print(f"  N*={n:.1f}; naive formula={np.sqrt(n*0.032/1.032):.2f}; true V={np.sqrt(n*0.032/(1.032*(1+n*1e-3))):.3f}")
