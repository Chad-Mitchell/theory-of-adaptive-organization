"""S7. (a) K-clock ceiling and the indivisible-read zero (Prop 9); (b) selection-resolution bound (Prop 10);
(c) hidden readability assumption: members read x_i (not u_i) and subtract the level's estimate (Prop 11)."""
import numpy as np, sympy as sp
from scipy.optimize import minimize, brentq
rng=np.random.default_rng(7)
print("=== (a) K clocks: saving = 1 - sum q_k^g / (K^(1-g) (sum q)^g)  in [0, 1-K^-(1-g)); indivisible reads: saving <= 0 ===")
worst_lo=1; worst_hi=-1; ind_pos=0
for _ in range(20000):
    K=int(rng.integers(2,9)); g=rng.uniform(0.05,0.95); qk=10**rng.uniform(-4,4,K)
    sv=1-np.sum(qk**g)/(K**(1-g)*np.sum(qk)**g); cap=1-K**(-(1-g))
    worst_lo=min(worst_lo,sv); worst_hi=max(worst_hi,sv-cap)
    ind=1-np.sum(qk**g)/np.sum(qk)**g; ind_pos+=(ind>1e-12)
print(f"  min saving {worst_lo:.2e} (>=0);  max(saving - cap) {worst_hi:.2e} (<0);  indivisible-read cases with positive saving: {ind_pos}/20000")
print("  two components, g=1/2, separation R=sqrt(q_fast/q_slow): ",", ".join(f"R={R}: {1-(1+R)/np.sqrt(2*(1+R**2)):.3f}" for R in [1,2,4,10,1e6]))
print("\n=== (b) resolution: max fractional saving of a level (N->inf) = 1-(1+rho)^-b <= b*rho ===")
b,rho,eps=sp.symbols('b rho epsilon',positive=True)
print("  rho threshold for relative resolution eps:",sp.solve(sp.Eq(1-(1+rho)**(-b),eps),rho))
viol=0
for _ in range(20000):
    bv=rng.uniform(0.01,0.99); rv=10**rng.uniform(-6,3); viol+=(1-(1+rv)**(-bv)>bv*rv*(1+1e-12))
print(f"  violations of 1-(1+rho)^-b <= b rho: {viol}/20000;  b=1/2, eps=1%: rho_min = {(0.99)**-2-1:.4f}; eps=5%: {(0.95)**-2-1:.4f}")
print("\n=== (c) readability: members read x_i and subtract the level's current estimate (R1, quadratic, Brownian) ===")
M=400000; U1=rng.random(M); U2=rng.random(M)
def mse_shared_factor(T,tau):
    s=U1*T; sp_=U2*tau                     # s: time since member read; sp_: age of level estimate now
    sigma=np.mod(-(s-sp_),tau)             # age of level estimate at the member's read time
    between=sp_<s
    return np.mean(np.where(between,sp_+sigma,s)), np.mean(s)
def nested(N,qg,qu,c=1.0,w=1.0):
    f=lambda x: c/np.exp(x[0])+c/(N*np.exp(x[1]))+w*(qu*np.exp(x[0])/2+qg*mse_shared_factor(np.exp(x[0]),np.exp(x[1]))[0])
    best=None
    for x0 in [(np.log(np.sqrt(2/qu)),np.log(np.sqrt(2/qu))-r) for r in [0.0,0.7,1.4]]:
        r=minimize(f,x0,method='Nelder-Mead',options={'xatol':1e-7,'fatol':1e-12,'maxiter':4000})
        best=r.fun if best is None else min(best,r.fun)
    return best
def nested_sep(N,qg,qu): return np.sqrt(2*qu)+np.sqrt(2*qg/N)
for rv in [3e-2,1e-2]:
    qg=rv; qu=1.0; flat=np.sqrt(2*(qg+qu))
    Ns=np.exp(brentq(lambda lN: flat-nested(np.exp(lN),qg,qu),np.log(20),np.log(5e3),xtol=1e-6))
    Nsep=np.exp(brentq(lambda lN: flat-nested_sep(np.exp(lN),qg,qu),np.log(1.01),np.log(1e8),xtol=1e-9))
    print(f"  rho={rv:g}: N*rho (subtract scheme) = {Ns*rv:.3f};  separable/aligned = {Nsep*rv:.3f}  (Pi* bounds 4 <= . <= 8)")
