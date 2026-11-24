"""Reviewer check: does the stake-free onset c*=6 kap kT survive a periodic loss 1-cos(e) (no small-angle approx)?
e(s) ~ N((om-w')s, 2Ds) between perfect reads at interval T=1/f. E[1-cos e] = 1 - exp(-D s) cos((om-w') s).
Time average over s in [0,T] in closed form. Also: endpoint-scored squared loss (a=1,b=2) -> predicted onset 2b/a = 4."""
import numpy as np
from scipy.optimize import minimize
kT=kap=1.0; om=1.0
def avgcos(d,D,T):
    # (1/T) int_0^T exp(-D s) cos(d s) ds
    z=complex(-D,d); return (np.real((np.exp(z*T)-1)/z))/T if abs(z)>1e-14 else 1.0
def J(p,c,w):
    lf,lD,u=p; f,D=np.exp(lf),np.exp(lD); wp=om/(1+np.exp(-u)); T=1/f
    return kap*kT*wp**2/D + c*f + w*(1-avgcos(om-wp,D,T))
def J0(c,w):  # no clock (w'=0, D=0): loss 1 - sin(om T)/(om T)
    best=w  # blind: never read, loss -> 1
    for lf0 in np.linspace(-6,6,25):
        r=minimize(lambda q: c*np.exp(q[0])+w*(1-np.sinc(om/np.exp(q[0])/np.pi)), [lf0], method='Nelder-Mead',options=dict(xatol=1e-10,fatol=1e-13))
        best=min(best,r.fun)
    return best
def Jc(c,w):
    best=np.inf
    for a in (-2,0,2,4):
        for b in (-6,-3,0):
            for u in (-2,0,2,5):
                r=minimize(J,[a,b,u],args=(c,w),method='Nelder-Mead',options=dict(xatol=1e-10,fatol=1e-13,maxiter=8000))
                best=min(best,r.fun)
    return best
for w in (30,300,3000,3e4):
    cs=np.arange(3.0,12.01,0.25); on=None
    for c in cs:
        if Jc(c,w) < J0(c,w)*(1-1e-7): on=c; break
    print(f"1-cos loss, w/(c om) ~ {w/6:.0f}: clock first pays at c/kap kT ~ {on}")
# endpoint-scored quadratic: a=1,b=2 -> onset 4
def Je(p,c,w):
    lf,lD,u=p; f,D=np.exp(lf),np.exp(lD); wp=om/(1+np.exp(-u))
    return kap*kT*wp**2/D + c*f + w*((om-wp)**2/f**2 + 2*D/f)
def Je0(c,w): f=(2*w*om**2/c)**(1/3); return c*f+w*om**2/f**2
for w in (1,100):
    row=[]
    for c in (3.8,3.95,4.05,4.2):
        best=min(minimize(Je,[a,b,u],args=(c,w),method='Nelder-Mead',options=dict(xatol=1e-12,fatol=1e-14,maxiter=20000)).fun for a in (-2,0,2) for b in (-4,0,4) for u in (-3,0,3))
        row.append(f"c={c}: clock {'pays' if best<Je0(c,w)*(1-1e-9) else 'no'}")
    print(f"endpoint quadratic loss, w={w}: "+"  ".join(row))
