"""Check: raw sampling effort of a level at scope s, in class P(a,b), when the
shared driver at scope s drifts at q_s = q0 * N_s**(-kappa).
Optimal effort for R1 (reset reads): n* = sqrt(W q / (2c)) (minimise c n + W q/(2n)).
Claim: d ln n*/d ln N_s = a - kappa*b  (= (1-kappa)/2 for a=b=1/2).
Also: if the scope-s driver is the mean of N_s independent unit-level shocks, Var(increment) ~ 1/N_s -> kappa = 1.
"""
import numpy as np
from scipy.optimize import minimize_scalar
rng=np.random.default_rng(1)
def nstar(W,q,c=1.0):
    f=lambda n: c*n + W*q/(2*n)
    return minimize_scalar(f,bounds=(1e-9,1e9),method='bounded',options={'xatol':1e-12}).x
for kappa in [0,0.5,1.0,1.5]:
    Ns=np.array([3,9,27,81,243.0])
    eff=[nstar(W=N*1.0,q=N**(-kappa)) for N in Ns]
    slope=np.polyfit(np.log(Ns),np.log(eff),1)[0]
    print(f"kappa={kappa}: fitted elasticity {slope:.4f}  predicted {(1-kappa)/2:.4f}")
# general (a,b): phi = k p^(1-a) W^a q^b ; effort elasticities = (a,b) by Lemma 1 / A5, so slope = a - kappa*b
# aggregation null: driver at scope s = mean of N_s iid unit shocks
for N in [3,9,27,81,243]:
    x=rng.normal(size=(20000,N)).mean(axis=1)
    print(N, "var of scope driver increment:", round(x.var(),5), " 1/N:", round(1/N,5))
