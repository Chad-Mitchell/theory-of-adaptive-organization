# C12c-G''' proof attempt: Fourier/Cauchy-Schwarz upper bound on V = 1 - 2e (C12CG §12).
# V = Re sum_m s_m r_m conj(f_m), |s_m| = 2/(pi|m|) (odd m); r(theta) in P (|r| = 1 at vertices), f(phi) in D° (polar of D=(P-P)/2).
# Proved constraints: sum|r_m|^2 <= 1; |r_{+-1}| <= sigma = mean support of P; sum|f_m|^2 <= R^2 (R = circumradius of D°); |f_{+-1}| <= tau = mean support of D°.
import numpy as np
from scipy.optimize import minimize
def consts(n):
    sig=n*np.sin(np.pi/n)/np.pi
    if n%2==0: tau=n*np.tan(np.pi/n)/np.pi; R=1/np.cos(np.pi/n)
    else:
        c=np.cos(np.pi/(2*n)); tau=2*n*np.tan(np.pi/(2*n))/(np.pi*c); R=1/c**2   # D=(P-P)/2 regular 2n-gon, circumradius c
    return sig,tau,R
def bound(n,mres):
    sig,tau,R=consts(n)
    def negV(x):
        a1,a2,b1,b2=x
        rz=max(1-a1*a1-a2*a2,0); rw=max(R*R-b1*b1-b2*b2,0)
        return -((2/np.pi)*(a1*b1+a2*b2)+(2/(np.pi*mres))*np.sqrt(rz*rw))
    best=0
    rng=np.random.default_rng(0)
    for _ in range(300):
        x0=rng.uniform(0,1,4)*np.array([sig,sig,tau,tau])
        cons=[{'type':'ineq','fun':lambda x:1-x[0]**2-x[1]**2},{'type':'ineq','fun':lambda x:R*R-x[2]**2-x[3]**2}]
        r=minimize(negV,x0,bounds=[(0,sig),(0,sig),(0,tau),(0,tau)],constraints=cons,method='SLSQP')
        if r.success: best=max(best,-r.fun)
    return best
enc={5:(4-np.sqrt(5))/10,8:(7-3*np.sqrt(2))/16}; need={5:0.176393-0.004135,8:0.172335-0.000800}
for n in (5,8):
    sig,tau,R=consts(n)
    for mres,label in ((3,"proved: residual at |m|>=3"),(n-1 if n%2==0 else 9,"HYP stability: residual only at aliasing |m|")):
        B=bound(n,mres); print(f"n={n} sigma={sig:.4f} tau={tau:.4f} R={R:.4f} | {label}: V<= {B:.5f} -> e >= {(1-B)/2:.5f} | e_nv={enc[n]:.6f} | gap needs e >= {need[n]:.5f}: {'CERTIFIED' if (1-B)/2>=need[n] else 'not enough'}")
