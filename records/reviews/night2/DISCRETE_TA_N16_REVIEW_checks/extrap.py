# Extrapolate g(rho) = (t_grid - T)/sqrt(rho*theta) to rho -> 0 from gscan*.json; compare with C1 and the barrier-shift heuristic C1*int_0^inf exp(-z-kappa(cosh z - 1))dz
import json,numpy as np
from scipy.integrate import quad
from scipy.special import zeta
C1=-zeta(.5)/np.sqrt(2*np.pi)
d1=json.load(open('gscan.json')); d2=json.load(open('gscan2.json'))
pts={}
for k,dd in d1.items():
    for r,v in dd.items(): pts.setdefault(float(k),{})[float(r)]=v['g']
for key,v in d2.items():
    k,r=key.split('_'); pts.setdefault(float(k),{})[float(r)]=v['g']
for k in sorted(pts):
    r=np.array(sorted(pts[k])); g=np.array([pts[k][x] for x in r]); s=np.sqrt(r)
    c0=[np.linalg.lstsq(np.c_[np.ones(n),s[:n],r[:n]],g[:n],rcond=None)[0][0] for n in (4,5,len(r))]
    G=quad(lambda z: np.exp(-z-k*(np.cosh(z)-1)) if z<700 else 0,0,np.inf,limit=500)[0]
    print("kappa %g: rho in [%g,%g], g(finest)=%.5f; extrapolated c(kappa)=%.5f..%.5f (C1=%.5f, %.2f%% below); heuristic C1*2g(0)=%.5f explains %.0f%% of deficit"%(k,r[0],r[-1],g[0],min(c0),max(c0),C1,100*(1-np.mean(c0)/C1),C1*G,100*(C1-C1*G)/(C1-np.mean(c0))))
