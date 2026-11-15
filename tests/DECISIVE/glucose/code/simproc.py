# Theory-side simulator: smooth single-time-scale process (OU filtered by OU, ACF (1+u)e^-u),
# rescaled so its 1/e ACF time = tau, sampled every dt; counts threshold episodes with a duration rule.
import numpy as np
U=2.1462   # (1+U)e^-U = e^-1
def simulate(n,dt,tau,rng):
    t0=tau/U; a=np.exp(-dt/t0); e=rng.standard_normal(n)*np.sqrt(1-a*a)
    x=np.empty(n); y=np.empty(n); x[0]=rng.standard_normal(); y[0]=x[0]
    for i in range(1,n): x[i]=a*x[i-1]+e[i]
    for i in range(1,n): y[i]=a*y[i-1]+(1-a)*x[i]
    y=(y-0)/np.std(y[: min(n,10**6)]) if n>1000 else y/np.sqrt((1+a)/(2*(1+a*a)) if False else 1)
    return y
def episodes(below,minrun):
    """count episodes: >=minrun consecutive True; re-arm after >=minrun consecutive False"""
    c=0; run=0; armed=True; offrun=minrun
    for b in below:
        if b:
            run+=1; offrun=0
            if armed and run>=minrun: c+=1; armed=False
        else:
            run=0; offrun+=1
            if offrun>=minrun: armed=True
    return c
