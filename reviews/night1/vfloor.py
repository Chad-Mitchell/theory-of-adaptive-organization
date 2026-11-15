import numpy as np
from scipy.optimize import brentq
rng=np.random.default_rng(1)
bad=0;maxerr=0;n=20000
for _ in range(n):
    rho=10**rng.uniform(-3,2); h=10**rng.uniform(-4,2); r=10**rng.uniform(-1,1)
    if rng.random()<0.2: h=0.0
    A=np.sqrt(1+rho)-1
    G=lambda N: N*A-np.sqrt(r)*np.sqrt(N*rho)-h
    hi=10.0
    while G(hi)<=0: hi*=2
    lo=1e-12 if h>0 else ((np.sqrt(r*rho)/A)**2)*0.5
    N=brentq(G,max(lo,1e-12),hi,xtol=1e-14,rtol=1e-14)
    V=np.sqrt(N/r)*np.sqrt(rho/(1+rho))
    Vf=0.5*(1+(1+rho)**-0.5)*(1+np.sqrt(1+4*h*(np.sqrt(1+rho)-1)/(r*rho)))
    maxerr=max(maxerr,abs(V-Vf)/Vf)
    if V < 1+(1+rho)**-0.5 - 1e-9: bad+=1
print("draws",n,"max rel err vs closed form",maxerr,"floor violations",bad)
