"""Referee check R2: (a) int_0^inf ln(1+u^-alpha) du = pi/sin(pi/alpha) (numeric quadrature);
(b) effort elasticities under priced precision P=1/N: minimize c*P + W*q^(1/alpha)*P^(-(1-1/alpha))/sin(pi/alpha)
numerically over 4 decades of W and q; compare with alpha/(2alpha-1) and 1/(2alpha-1)."""
import numpy as np, json
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
out={"integral":{},"elasticity":{}}
for a in (1.5,2.0,2.5,3.0):
    v=quad(lambda x: np.log1p(np.exp(-a*x))*np.exp(x),-50,50,limit=400)[0]
    out["integral"][str(a)]=[round(v,6),round(float(np.pi/np.sin(np.pi/a)),6)]
    def Pstar(W,q,c=1.0):
        f=lambda x: c*np.exp(x)+W*q**(1/a)*np.exp(-x*(1-1/a))/np.sin(np.pi/a)
        return np.exp(minimize_scalar(f,bounds=(-60,60),method="bounded",options=dict(xatol=1e-10)).x)
    Ws=np.logspace(-2,2,9)
    eW=np.polyfit(np.log(Ws),np.log([Pstar(W,1.0) for W in Ws]),1)[0]
    eq=np.polyfit(np.log(Ws),np.log([Pstar(1.0,q) for q in Ws]),1)[0]
    out["elasticity"][str(a)]=dict(stakes=round(float(eW),4),pred_stakes=round(a/(2*a-1),4),drift=round(float(eq),4),pred_drift=round(1/(2*a-1),4))
print(json.dumps(out,indent=1)); json.dump(out,open("r2_elasticities.json","w"),indent=1)
