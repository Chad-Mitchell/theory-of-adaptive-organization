# Round-2 check (MATH_LOGIC): the i.i.d. Azuma bound in BOOKENDS §2.0.3 fails for a blind agent in a persistent Markov world.
# Blind agent: increment +0.9 in good state, -1.1 in bad; stationary 50/50 -> mean -0.1; |D+delta| <= 1; I_pred = 0.
import numpy as np
rng=np.random.default_rng(2)
B,delta,b,n=5.0,0.1,1.0,20000
for p in [0.5,0.01,0.001]:
  for T in [400,1600]:
    X=np.empty((n,T),bool); X[:,0]=rng.random(n)<0.5
    flip=rng.random((n,T))<p
    for t in range(1,T): X[:,t]=X[:,t-1]^flip[:,t]
    D=np.where(X,0.9,-1.1); R=B+np.cumsum(D,1)
    s=(R>0).all(1).mean(); bd=np.exp(-(delta*T-B)**2/(2*b*b*T))
    print(f"p={p} T={T} surv={s:.4f} iid-bound={bd:.4f} violated={s>bd}")
