import numpy as np, json
from scipy.integrate import quad
from scipy.special import zeta
import bayes
from bayes import cont_ta
C1=-zeta(.5)/np.sqrt(2*np.pi)
out={}
for k,rhos in [(3e-2,[0.000625,0.00125,0.0025,0.005,0.01,0.02]),(1e-2,[0.000625,0.00125])]:
    T=cont_ta(k,'quiet')
    G=quad(lambda z: np.exp(-z-k*(np.cosh(z)-1)) if z<700 else 0,0,np.inf,limit=500)[0]
    for rho in rhos:
        t,_=bayes.grid_ta(k,rho,'quiet',0.4,8,9.0)
        g=(t-T)/np.sqrt(rho)
        out[f"{k}_{rho}"]=dict(t=t,T=T,g=g,C1x2g0=C1*G)
        print(k,rho,"t=%.9f g=%.5f  (g-C1)/sqrt(rho)=%.4f  (g-C1*2g0)/sqrt(rho)=%.4f  C1*2g0=%.5f"%(t,g,(g-C1)/np.sqrt(rho),(g-C1*G)/np.sqrt(rho),C1*G),flush=True)
json.dump(out,open('gscan2.json','w'),indent=1)
