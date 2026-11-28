# Checks for C12B_ORDER.md §8 (Gaussian keep floor). OBSERVED numerics, not proofs. kT = 1.
import numpy as np
rng=np.random.default_rng(12)
x=np.linspace(-40,40,40001); dx=x[1]-x[0]
def npdf(m,v): return np.exp(-(x-m)**2/(2*v))/np.sqrt(2*np.pi*v)
def mix(ws,ms,vs):   # log-density and d/dx log-density of a Gaussian mixture, computed in log space (no underflow)
    L=np.array([np.log(w)-(x-m)**2/(2*v)-0.5*np.log(2*np.pi*v) for w,m,v in zip(ws,ms,vs)])
    mx=L.max(0); R=np.exp(L-mx); Z=R.sum(0); lq=mx+np.log(Z)
    dl=sum(R[i]*(-(x-ms[i])/vs[i]) for i in range(len(ws)))/Z
    return lq,dl
def D(ws,ms,vs,s2):
    lq,_=mix(ws,ms,vs); lp=-x**2/(2*s2)-0.5*np.log(2*np.pi*s2); return np.sum(np.exp(lq)*(lq-lp))*dx
def IF(ws,ms,vs,s2):
    lq,dl=mix(ws,ms,vs); g=dl+x/s2; return np.sum(np.exp(lq)*g*g)*dx
print("(1) Gaussian LSI (Step 2): s^2/2 * IF(q||pi) >= D(q||pi), pi=N(0,s^2), q = random 1-4 component Gaussian mixtures")
worst=np.inf
for t in range(300):
    s2=rng.uniform(0.3,3); k=rng.integers(1,5)
    ws=rng.dirichlet(np.ones(k)); ms=rng.normal(0,3,k); vs=rng.uniform(0.05,5,k)
    d=D(ws,ms,vs,s2); worst=min(worst,(s2/2*IF(ws,ms,vs,s2))/d)
print(f"   min ratio over 300 draws = {worst:.6f}  (>= 1 expected; equality only for shifted N(.,s^2))")
print(f"   equality case shift 1.3, s^2=1: ratio = {(0.5*IF([1],[1.3],[1.0],1.0))/D([1],[1.3],[1.0],1.0):.6f}")
print("(2) marginalization (Step 1'): leak EP on joint p(m,c) >= leak EP on marginal p_M; c in 3 states")
worst=np.inf
for t in range(200):
    s2=rng.uniform(0.5,2); wc=rng.dirichlet(np.ones(3)); ms=rng.normal(0,2,3); vs=rng.uniform(0.1,3,3)
    joint=sum(wc[c]*IF([1],[ms[c]],[vs[c]],s2) for c in range(3)); worst=min(worst,joint/IF(wc,ms,vs,s2))
print(f"   min (joint/marginal) = {worst:.6f}  (>= 1 expected)")
print("(3) identity (Step 3): E_x D(p_{M|x}||pi) = I(X;M) + D(p_M||pi), linear-Gaussian record M = a x + noise")
for a,n,s2,V in [(0.8,0.5,1.0,2.0),(2.0,1.0,1.0,1.0),(0.3,1.0,1.0,4.0)]:
    lhs=np.mean([D([1],[a*xx],[n],s2) for xx in rng.normal(0,np.sqrt(V),4000)])
    vm=a*a*V+n; I=0.5*np.log(vm/n); Dm=0.5*(vm/s2-1-np.log(vm/s2))
    print(f"   a={a},n={n}: E_x D = {lhs:.4f} (MC, 4000 x) ; I + D(p_M||pi) = {I+Dm:.4f}")
print("(4) two-channel OU, corrector that knows x (housekeeping case), steady state; analytic EP vs Langevin heat")
G,kap,s2,V=1.0,3.0,1.0,2.0       # leak rate, coupling rate, s^2 = s_C^2 (so stationary var = s^2)
a=kap/(G+kap); DL=G*s2; DC=kap*s2
sigL=G*a*a*V/s2; sigC=kap*(1-a)**2*V/s2; I=0.5*np.log(1+a*a*V/s2)
print(f"   analytic: sigma_L={sigL:.4f} sigma_C={sigC:.4f} total={sigL+sigC:.4f} ; 2*G*I={2*G*I:.4f} ; sigma_L/(2GI)={sigL/(2*G*I):.4f}")
N,dt,T=20000,2e-3,30.0; X=rng.normal(0,np.sqrt(V),N); m=a*X+rng.normal(0,np.sqrt(s2),N)
QL=np.zeros(N); QC=np.zeros(N); steps=int(T/dt); burn=int(5/dt)
for k in range(steps):
    dmL=-G*m*dt+np.sqrt(2*DL*dt)*rng.normal(size=N); dmC=-kap*(m-X)*dt+np.sqrt(2*DC*dt)*rng.normal(size=N)
    mid=m+0.5*(dmL+dmC)
    if k>=burn: QL+=(-mid/s2)*dmL; QC+=(-(mid-X)/s2)*dmC    # heat to bath = F_k ∘ dm_k (Stratonovich), kT=1
    m=m+dmL+dmC
tt=(steps-burn)*dt
print(f"   Langevin (N={N}, dt={dt}): heat rate total = {(QL+QC).mean()/tt:.4f} +- {(QL+QC).std()/tt/np.sqrt(N):.4f}  (steady: = sigma_L+sigma_C)")
print("(5) floor ratio u/ln(1+u) for this family (sigma_L / 2 G I), u = a^2 V/s^2 -> 1 as u -> 0")
for u in [10,1,0.1,0.01]: print(f"   u={u}: {u/np.log(1+u):.5f}")
print("(6) boundary term: S_range = (d/2) ln(2 pi e A^2) - S_0 ; with write included S_0 = (d/2) ln(2 pi e s^2) -> d ln(A/s)")
for d,A,s in [(1,10,1),(3,100,1)]: print(f"   d={d}, A/s={A/s}: S_range = {d*np.log(A/s):.4f} nats; floor penalty kT*S_range/tau -> 0 as tau -> inf")
