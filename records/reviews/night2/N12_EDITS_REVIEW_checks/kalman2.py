# alpha=2 exact steady-state Kalman with periodic noisy reads (no truncation)
import numpy as np
from scipy.optimize import minimize_scalar, brentq
c=w=qu=1.0
def mse(T,q,s):
    Q=q*T; Pm=(Q+np.sqrt(Q*Q+4*Q*s))/2; Pp=Pm*s/(Pm+s); return Pp+Q/2
def unit(W,q,s):
    return minimize_scalar(lambda lT:c*np.exp(-lT)+W*mse(np.exp(lT),q,s),bounds=(-60,120),method='bounded',options={'xatol':1e-11}).fun
def Ns(rho,s):
    qg=rho*qu; f=lambda l:np.log(unit(np.exp(l)*w,qg,s)+np.exp(l)*unit(w,qu,s))-np.log(np.exp(l)*unit(w,qg+qu,s))
    return np.exp(brentq(f,1e-6,np.log(1e60),xtol=1e-13))
sl=lambda r,s,d=0.15:(np.log(Ns(r*np.exp(d),s))-np.log(Ns(r*np.exp(-d),s)))/(2*d)
for s in (1e-3,1e-6,0.0):
    print("sigma2",s,[round(float(sl(r,s)),3) for r in (1e-1,1e-2,1e-3,1e-4,1e-5,1e-7)])
