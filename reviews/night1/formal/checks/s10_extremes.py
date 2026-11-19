"""S10. Extremes used in EXTENSIONS.md."""
import numpy as np, itertools
from scipy.optimize import brentq
def Nstar(rho,a,b,h=0.0,qu=1.0,lam=1.0):
    qg=rho*qu
    G=lambda n: n*((lam*(qg+qu))**b-(lam*qu)**b)-(n**a*(lam*qg)**b+h)
    lo,hi=1.0,2.0
    while G(hi)<=0: lo=hi; hi*=2
    return brentq(G,lo,hi,xtol=1e-10*hi)
print("=== E2 rho = 1 and rho -> inf (h=0) ===")
for a,b in [(.5,.5),(2/3,1/3),(.8,.2)]:
    print(f"  (a,b)=({a:.2f},{b:.2f}): N*(rho=1)={Nstar(1,a,b):.3f} formula={(1/(2**b-1))**(1/(1-a)):.3f};  N*(1e3)={Nstar(1e3,a,b):.4f}  N*(1e6)={Nstar(1e6,a,b):.5f}")
print("\n=== E3 total drift lam -> 0 with upkeep h=1 (rho=0.1, a=b=1/2): N* ~ lam^{-b}? ===")
lams=[1e-2,1e-3,1e-4,1e-5,1e-6]; Ns=[Nstar(0.1,.5,.5,h=1.0,lam=l) for l in lams]
for l,n,n2 in zip(lams[1:],Ns[1:],Ns[:-1]): print(f"  lam={l:.0e} N*={n:.4g}  local slope d lnN*/d ln lam={-np.log(n/n2)/np.log(10):.4f} (pred -> -b = -0.5)")
print("\n=== E1 depth vs log N in the nested tree (first-order rule, class R, kappa<kappa*) ===")
def first_order_depth(S,beta,q0,kap,qu,a,b,h=0.0):
    # scale s kept iff n^{1-a} q_s^{1-b} > R^{1-b}/b, R = qu + sum untracked q_s (iterate to fixed point)
    n=np.array([beta**s for s in range(1,S+1)],float); q=q0*n**(-kap); keep=np.zeros(S,bool)
    for _ in range(200):
        R=qu+q[~keep].sum()
        new=(n**(1-a)*q**(1-b)*b*R**(b-1) > 1+h/q*0)  # h=0 only
        if (new==keep).all(): break
        keep=new
    return keep.sum()
for kap in [0.3,0.7]:
    ds=[first_order_depth(S,2,1.0,kap,1.0,.5,.5) for S in range(4,41,4)]
    print(f"  kappa={kap}: depth at S=4..40 step 4 (log2 N = S): {ds}  increments {np.diff(ds).tolist()}")
for kap in [1.5]:
    ds=[first_order_depth(S,2,1.0,kap,1.0,.5,.5) for S in range(4,41,4)]
    print(f"  kappa={kap} (>kappa*): depth {ds}")
print("\n=== E4 lookup cost u -> 0 (R1 quadratic, c=1, w=1, mu=1, H_l=inf, h=0.05) ===")
# member item: drift q_u private + q_g shared. Options per member: hold flat sqrt(2 w (qg+qu)) + h, or lookup mu*u.
# level: sqrt(2 N w qg)+h, then member holds residual sqrt(2 w qu)+h or looks up the residual at mu*u.
# shared store: one holder for N users of a common item with drift qs: sqrt(2 N w qs)+h vs N mu u.
N=50; qg=0.1; qu=1.0; h=0.05; qs=1.0
for u in [3,2,1.5,1.2,1.0,0.8,0.5,0.3,0.2,0.1,0.05,0.02,0.01,0.005,0.002]:
    flat=N*min(np.sqrt(2*(qg+qu))+h,u)
    lev =np.sqrt(2*N*qg)+h+N*min(np.sqrt(2*qu)+h,u)
    level_used = lev<flat
    priv_hold = (np.sqrt(2*qu)+h)<u
    store = (np.sqrt(2*N*qs)+h) < N*u
    print(f"  u={u:<6} private holding:{'yes' if priv_hold else 'no '}  level optimal:{'yes' if level_used else 'no '}  shared store held:{'yes' if store else 'no '}")
ul=(np.sqrt(2*N*qg)+h)/N+np.sqrt(2*qu)+h; up=np.sqrt(2*qu)+h; us=(np.sqrt(2*N*qs)+h)/N
print(f"  exact edges: level dissolves below u={ul:.4f} (valid since < flat cost {np.sqrt(2*(qg+qu))+h:.4f}); private residual holding stops below u={up:.4f}; shared store stops below u={us:.4f}")
print("  ORDER: with whole-item lookup the level dissolves FIRST, then private residual holding, the shared store (component lookup) LAST.")
print("\n=== E5 vigilance beyond onset ~ N^a, and p_g/p -> 0 ===")
for a,b in [(.5,.5),(2/3,1/3)]:
    rho=1e-3; Ns=Nstar(rho,a,b)
    V=lambda n: n**a*(rho/(1+rho))**b
    print(f"  (a,b)=({a:.2f},{b:.2f}): V(N*)={V(Ns):.3f}, V(100N*)/V(N*)={V(100*Ns)/V(Ns):.2f} (pred {100**a:.2f})")
