# PAPER-approx (not the scored model): pooled per-member cost with the approximate member heat u/delta
# a=v=kT=1. Level heat exact a v/((a+b)u); member heat approx u/delta (fast copy of a level with quadratic variation 2u)
import numpy as np
from scipy.optimize import minimize
def F(p,K,w):
    b,u,d=np.exp(p)
    eps=1-1/((1+b)/b+(1+b)**2*(u/b+d))
    return 1/(K*(1+b)*u)+u/d+w*eps
for w in [3.0,10.0,100.0]:
    Jdir=2*np.sqrt(w)-1
    for K in [2,4,8,12,16,24,32,48,64,96,128]:
        best=min((minimize(F,x0,args=(K,w),method='Nelder-Mead',options=dict(xatol=1e-10,fatol=1e-12,maxiter=20000)) for x0 in
                  [np.array([i,j,k]) for i in (-1,1,3) for j in (-3,-1,1) for k in (-5,-3,-1)]),key=lambda r:r.fun)
        print(w,K,round(best.fun,4),round(Jdir,4),round(best.fun/Jdir,4),np.round(np.exp(best.x),4))
