# In-model check: cost-optimal record-count clock (biased random walk of ticks).
# Net-tick entropy sigma=ln(k+/k-) (units of k); heat per net tick = kT*sigma.
# Relative variance of elapsed-time estimate from N net ticks: coth(sigma/2)/N (biased walk, standard).
# Cost J = N*kT*sigma + w*coth(sigma/2)/N. Minimise over sigma>0 at fixed N, then over N.
import numpy as np
from scipy.optimize import minimize_scalar
kT=1.0
def J(s,N,w): return N*kT*s + w/np.tanh(s/2)/N
# Monte-Carlo check of the variance formula
rng=np.random.default_rng(0)
for s in [0.5,2.0,5.0]:
    kp=1.0; km=np.exp(-s); t=200.0
    n=rng.poisson(kp*t,200000)-rng.poisson(km*t,200000)
    pred=(kp+km)/(kp-km)**2/t  # Var(n)/mean^2
    print(f"sigma={s}: MC relvar={n.var()/n.mean()**2:.5e}  formula coth(s/2)/<n>={1/np.tanh(s/2)/n.mean():.5e}")
print("w, N*, sigma*, relvar*, J*")
for w in [1e2,1e3,1e4,1e5,1e6]:
    best=None
    for N in np.unique(np.round(np.logspace(0,4,400)).astype(int)):
        r=minimize_scalar(lambda s:J(s,N,w),bounds=(1e-4,60),method='bounded')
        if best is None or r.fun<best[0]: best=(r.fun,N,r.x)
    Jb,N,s=best
    print(f"{w:.0e} {N} {s:.3f} {1/np.tanh(s/2)/N:.3e} {Jb:.3f}")
