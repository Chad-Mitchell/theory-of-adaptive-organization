import numpy as np
from scipy.optimize import brentq
from bayes import grid_ta, cont_ta, plugin
for k in [1e-6,1e-3,1e-2]:
    P=plugin(k)
    for law in ['quiet','switch']:
        for tol in [0.10,0.05]:
            for shift in [0.0,-0.5]:
                fn=lambda lr: (grid_ta(k,P/np.exp(lr),law)[0]+shift*P/np.exp(lr))/P-1-tol
                try: r=np.exp(brentq(fn,np.log(2),np.log(800),xtol=1e-3))
                except Exception as e: r=float('nan')
                print("kappa %g law %s tol %.2f clock-shift %+.1fDelta : r* = %.1f"%(k,law,tol,shift,r),flush=True)
