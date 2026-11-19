"""S2. Theorems 2-4 (pooling onset, opposite effects, vigilance) in the power class
phi(W,q;p) = k p^(1-a) W^a q^b  (0<=a<1, 0<b<1).  Flat: N phi(w,qg+qu;p).  Level: phi(Nw,qg;pg) + N phi(w,qu;p) + h.
All exact (no first-order expansion) unless labelled 'first order'."""
import sympy as sp, numpy as np
from scipy.optimize import brentq
rng=np.random.default_rng(2)
a,b,rho,N,hp,g=sp.symbols('a b rho N hprime gamma',positive=True)
print("=== (1) exact onset at h=0 (units k w^a qu^b, equal prices) ===")
Ns=(rho**b/((1+rho)**b-1))**(1/(1-a))
G=N*((1+rho)**b-1)-N**a*rho**b
print("G(N*) symbolic simplify:",sp.simplify(G.subs(N,Ns)))
for av,bv in [(0.5,0.5),(2/3,1/3),(0.3,0.7),(0.8,0.2)]:
    for rv in [1e-3,1.0,50.0]:
        print(f"  a={av:.3f} b={bv:.3f} rho={rv:g}: G(N*)={float(G.subs({a:av,b:bv,rho:rv,N:Ns.subs({a:av,b:bv,rho:rv})})):.2e}")
lim=sp.limit((rho**(b/(1-a)-1/(1-a))*0+1)*0+((rho**b/((1+rho)**b-1))*rho**(1-b)).subs({a:sp.Rational(1,3),b:sp.Rational(1,3)}),rho,0)
print("lim_{rho->0} [rho^b/((1+rho)^b-1)] * rho^(1-b)  (b=1/3) =",lim,"(claim: 1/b = 3)")
for bv in [sp.Rational(1,2),sp.Rational(1,3),sp.Rational(2,3),sp.Rational(1,5)]:
    print(f"  b={bv}: limit = {sp.limit((rho**bv/((1+rho)**bv-1))*rho**(1-bv),rho,0)}  (1/b = {1/bv})")
print("  => N* rho^((1-b)/(1-a)) -> b^(-1/(1-a)) as rho->0 (raise the limit to 1/(1-a)).")
T3a=(sp.sqrt(1+rho)+1)**2/rho
print("a=b=1/2: N* - T3a =",sp.simplify(Ns.subs({a:sp.Rational(1,2),b:sp.Rational(1,2)})-T3a))
ln_Ns=(b*sp.log(rho)-sp.log((1+rho)**b-1))/(1-a)
eg=sp.simplify(sp.diff(ln_Ns,rho)*rho)
print("exact e_g(rho) at h=0 =",eg)
print("  rho->0 limit, (a,b)=(1/2,1/2):",sp.limit(eg.subs({a:sp.Rational(1,2),b:sp.Rational(1,2)}),rho,0),
      "; (2/3,1/3):",sp.limit(eg.subs({a:sp.Rational(2,3),b:sp.Rational(1,3)}),rho,0),
      "; rho->oo (1/2,1/2):",sp.limit(eg.subs({a:sp.Rational(1,2),b:sp.Rational(1,2)}),rho,sp.oo))

# ---------- numeric exact root in raw units ----------
def Nstar(qg,qu,w,h,a_,b_,p=1.0,pg=1.0,kb=0.0,k=1.0,Nmax=1e30):
    """smallest N>=1 with flat-level>0 (level wins).  kb: per-member broadcast cost per unit time."""
    phi=lambda W,q,pp: k*pp**(1-a_)*W**a_*q**b_
    Gf=lambda n: n*phi(w,qg+qu,p)-(phi(n*w,qg,pg)+n*phi(w,qu,p)+h+kb*n)
    if Gf(1.0)>0: return 1.0
    lo,hi=1.0,2.0
    while Gf(hi)<=0:
        lo=hi; hi*=2
        if hi>Nmax: return np.inf
    return brentq(Gf,lo,hi,xtol=1e-12*hi,rtol=1e-14,maxiter=500)
def el(f,x,eps=1e-4):
    return (np.log(f(x*np.exp(eps)))-np.log(f(x*np.exp(-eps))))/(2*eps)

print("\n=== (2) opposite effects: sign of e_g and e_u, exact roots, random (a,b,rho,h,w,prices) ===")
bad_g=bad_u=n=0; worst=[]
for _ in range(20000):
    a_=rng.uniform(0,0.95); b_=rng.uniform(0.05,0.95); qu=10**rng.uniform(-3,1); rv=10**rng.uniform(-4,4); qg=rv*qu
    w=10**rng.uniform(-2,2); h=0 if rng.random()<0.3 else 10**rng.uniform(-3,3); p=10**rng.uniform(-1,1); pg=10**rng.uniform(-1,1)
    if not np.isfinite(Nstar(qg,qu,w,h,a_,b_,p,pg)) or Nstar(qg,qu,w,h,a_,b_,p,pg)<=1.0001: continue
    eg_=el(lambda x: Nstar(x,qu,w,h,a_,b_,p,pg),qg); eu_=el(lambda x: Nstar(qg,x,w,h,a_,b_,p,pg),qu); n+=1
    if not eg_<0: bad_g+=1; worst.append(('g',a_,b_,rv,h,eg_))
    if not eu_>0: bad_u+=1; worst.append(('u',a_,b_,rv,h,eu_))
print(f"  draws with interior onset: {n};  e_g>=0 violations: {bad_g};  e_u<=0 violations: {bad_u}"); print("  ",worst[:5])
print("  counterexample (b=1, cost linear in drift): e_u =",round(el(lambda x: Nstar(1e-3,x,1,1.0,0.5,1.0),1.0),6),"(0 expected: no private-drift effect)")
print("  counterexample (a=1, cost linear in stakes): N* =",Nstar(1e-2,1,1,0.0,1.0,0.5,Nmax=1e12),"(inf expected: no level at any N)")

print("\n=== (3) small-rho exponents, exact roots (rho=1e-5 vs 2e-5), with and without upkeep ===")
for (a_,b_) in [(0.5,0.5),(2/3,1/3),(0.5,0.25),(0.8,0.2),(1/3,2/3),(0.2,0.6)]:
    row=[]
    for h in [0.0,1.0,100.0]:
        qu=1.0; e=(np.log(Nstar(2e-6,qu,1,h,a_,b_))-np.log(Nstar(1e-6,qu,1,h,a_,b_)))/np.log(2)
        row.append(e)
    print(f"  a={a_:.3f} b={b_:.3f}: e_g(h=0,1,100) = {row[0]:+.4f} {row[1]:+.4f} {row[2]:+.4f};  -(1-b)/(1-a) = {-(1-b_)/(1-a_):+.4f};  prediction with h>0: {(-(1-b_)/(1-a_) if a_>b_ else -1.0):+.4f}")

print("\n=== (4) invariant N* rho^((1-b)/(1-a)) -> b^(-1/(1-a)) (h=0) ===")
for (a_,b_) in [(0.5,0.5),(2/3,1/3),(0.5,0.25),(0.25,0.25),(0.4,0.4)]:
    r=1e-6; print(f"  a={a_:.3f} b={b_:.3f}: N* rho^.. = {Nstar(r,1,1,0,a_,b_)*r**((1-b_)/(1-a_)):.5f}  vs b^(-1/(1-a)) = {b_**(-1/(1-a_)):.5f}")

print("\n=== (5) large rho: N*->1 at h=0; intermediate -gamma regime with big upkeep (a=b=1/2) ===")
for rv in [1e1,1e2,1e3,1e4]:
    print(f"  rho={rv:g}: N*(h=0)={Nstar(rv,1,1,0,0.5,0.5):.4f};  h=1e6: e_g={el(lambda x: Nstar(x,1,1,1e6,0.5,0.5),rv):+.4f};  h=1e6 e(N*-1)={el(lambda x: Nstar(x,1,1,1e6,0.5,0.5)-1,rv):+.4f}")

print("\n=== (6) total volatility (scale qg and qu by lam) and stakes ===")
for (a_,b_) in [(0.5,0.5),(2/3,1/3)]:
    for h in [0.0,5.0]:
        f=lambda lam: Nstar(1e-3*lam,1.0*lam,1,h,a_,b_); fw=lambda w: Nstar(1e-3,1.0,w,h,a_,b_)
        print(f"  a={a_:.3f} b={b_:.3f} h={h}: elasticity of N* in total drift scale = {el(f,1.0):+.4f} (pred 0 if h=0, <0 if h>0);  in stakes w = {el(fw,1.0):+.4f}")

print("\n=== (7) vigilance V = level effort / flat member effort, effort = spend/price, spend = s*phi ===")
def V(qg,qu,w,h,a_,b_,p=1.0,pg=1.0):
    n=Nstar(qg,qu,w,h,a_,b_,p,pg)
    return (pg**(1-a_)*(n*w)**a_*qg**b_/pg)/(p**(1-a_)*w**a_*(qg+qu)**b_/p), n
viol=0; tot=0; minV=9e9
for _ in range(20000):
    b_=rng.uniform(0.05,0.95); a_=rng.uniform(b_,0.97); rv=10**rng.uniform(-4,4); h=0 if rng.random()<0.3 else 10**rng.uniform(-3,3)
    v,n=V(rv,1.0,1.0,h,a_,b_,1.0,10**rng.uniform(-1,1))
    if not np.isfinite(n) or n<=1.0001: continue
    tot+=1; minV=min(minV,v)
    if v<=1: viol+=1
print(f"  a>=b: V<=1 at onset in {viol}/{tot} random cases; min V = {minV:.4f}")
for rv in [1e-2,1e-4,1e-6]:
    print(f"  counterexample a=1/3<b=2/3, h=0, rho={rv:g}: V = {V(rv,1,1,0,1/3,2/3)[0]:.4f}  (V ~ rho^((b-a)/(1-a)) -> 0)")
print("  price invariance at h=0 (a=b=1/2, rho=1e-5): ",end="")
print(", ".join(f"pg/p={pg:g}: V={V(1e-5,1,1,0,0.5,0.5,1.0,pg)[0]:.4f}" for pg in [0.01,1,100,1e4]))
print("  price invariance at h=0 (class A: a=2/3,b=1/3, rho=1e-4): ",end="")
print(", ".join(f"pg/p={pg:g}: V={V(1e-4,1,1,0,2/3,1/3,1.0,pg)[0]:.2f}" for pg in [0.01,1,100]),f"; b^(-a/(1-a)) rho^((b-a)/(1-a)) = {(1/3)**(-2)*1e-4**(-1):.2f}")
print("  with upkeep (a=b=1/2, h'=1, rho=1e-5): ",", ".join(f"pg/p={pg:g}: V={V(1e-5,1,1,1.0,0.5,0.5,1.0,pg)[0]:.4f}" for pg in [0.25,1,4]),"(price-dependent when h>0)")
print("  a=b=gamma, h=0, all rho: V = (N* rho/(1+rho))^gamma > 1 check:")
for gm in [0.2,0.5,0.8]:
    print(f"    gamma={gm}: min over rho in [1e-4,1e4] of V = {min(V(r,1,1,0,gm,gm)[0] for r in np.logspace(-4,4,81)):.5f}; small-rho V={V(1e-7,1,1,0,gm,gm)[0]:.5f} vs gamma^(-gamma/(1-gamma))={gm**(-gm/(1-gm)):.5f}")

print("\n=== (8) per-member broadcast cost (per unit time) -> rho threshold (first order: b*rho*phi(w,qu) > kb) ===")
for kb in [1e-3,1e-2]:
    out=[]
    for rv in [1e-3,2e-3,5e-3,1e-2,2e-2,5e-2,1e-1]:
        out.append(f"rho={rv:g}:N*={Nstar(rv,1,1,0.0,0.5,0.5,kb=kb,Nmax=1e14):.3g}")
    # exact asymptotic threshold: N[(1+rho)^b-1] - N kb (units k w^a qu^b=1) ... rho_b solves (1+rho)^b - 1 = kb
    print(f"  kb={kb}: "+"; ".join(out)+f";  exact threshold rho_b=(1+kb)^(1/b)-1={(1+kb)**2-1:.4g}")
