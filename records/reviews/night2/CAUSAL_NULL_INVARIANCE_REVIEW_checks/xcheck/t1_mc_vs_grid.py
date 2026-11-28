import math, numpy as np
import sys; sys.path.insert(0, "..")
from mc import sim
import sys; sys.path.insert(0, "..")
from gridengine import kalman_pole
N=1.0; D=0.01
for name,(lam,mu) in {"A":(0.01,2.0),"B":(0.02,math.sqrt(2))}.items():
    pole,K=kalman_pole(lam,mu,N,D)
    for t in (1.0, 2.0):
        a=1-(1-pole)*t
        r=np.array([sim(lam,mu,N,D,a,0.0,1.0,20_000_000,s,True) for s in range(16)])
        print(name, t, "pole",pole, "err",r[:,0].mean(), r[:,0].std(ddof=1)/4, "tA", D*r[:,1].sum()/r[:,3].sum(), flush=True)
