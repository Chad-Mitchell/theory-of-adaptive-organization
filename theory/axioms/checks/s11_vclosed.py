"""S11. Closed form V(N*) = 1 + sqrt(1 + 2h'/r) at a=b=1/2, small rho (T5.6)."""
import numpy as np
from scipy.optimize import brentq
rng=np.random.default_rng(11); worst=0
for _ in range(2000):
    rho=10**rng.uniform(-7,-5); h=10**rng.uniform(-3,3); r=10**rng.uniform(-2,2)
    G=lambda n: n*(np.sqrt(1+rho)-1)-np.sqrt(r*n*rho)-h
    hi=2.0
    while G(hi)<=0: hi*=2
    N=brentq(G,1,hi,xtol=1e-12*hi)
    V=np.sqrt(N*rho/(1+rho)/r)
    worst=max(worst,abs(V-(1+np.sqrt(1+2*h/r)))/V)
print(f"max rel error over 2000 draws (rho in 1e-7..1e-5): {worst:.2e}; min possible V = 2 (h'=0)")

# F16: V(N*) > 1 for a >= b at ANY price ratio and upkeep (exact roots, no small-rho approximation)
bad=0; mn=1e9
for _ in range(20000):
    b=rng.uniform(0.05,0.95); a=rng.uniform(b,0.97); rho=10**rng.uniform(-4,4); r=10**rng.uniform(-3,3)
    h=0.0 if rng.random()<0.3 else 10**rng.uniform(-3,3)
    G=lambda n: n*((1+rho)**b-1)-r**(1-a)*n**a*rho**b-h
    lo,hi=1e-12,2.0
    while G(hi)<=0: lo=hi; hi*=2
    if h==0.0 and G(1e-12)>=0: lo=1e-300
    N=brentq(G,lo,hi,xtol=1e-12*hi)
    V=(N/r)**a*(rho/(1+rho))**b
    mn=min(mn,V); bad+= V<=1
print(f"F16: a>=b, random prices r in [1e-3,1e3], h in {{0}}U[1e-3,1e3]: violations {bad}/20000, min V = {mn:.4f}")
