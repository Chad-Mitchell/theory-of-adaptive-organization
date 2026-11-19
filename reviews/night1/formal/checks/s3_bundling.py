"""S3. Theorem 5 (bundling / local quadraticity).  Members' loss is l(e_g+e_u) (the shared error enters the SAME loss
as the private error).  Claim: the level faces a variance-linear loss, so its exponents are the technology's
quadratic-loss exponents and e_g = -1 (R1) or -2 (A_1) for every loss l, although a lone member's measured
elasticities (a,b) under l predict something else (-2/p for |e|^p under R1).  Exact numerics, no expansion."""
import sympy as sp, numpy as np
from scipy.optimize import minimize_scalar, brentq
from scipy.special import gamma as Gf
# ---- symbolic: Gaussian closure and first-order term
v,vg,beta,qg,qu,Tg,Tu,s,u=sp.symbols('v v_g beta q_g q_u T_g T_u s u',positive=True)
print("=== (1) closed form of E[(qg s_g + qu s_u)^beta], s_g~U[0,Tg], s_u~U[0,Tu] ===")
inner=sp.integrate((qg*s+qu*u)**beta,(u,0,Tu),conds='none'); dbl=sp.integrate(sp.expand(inner),(s,0,Tg),conds='none')
claim=((qg*Tg+qu*Tu)**(beta+2)-(qg*Tg)**(beta+2)-(qu*Tu)**(beta+2))/((beta+1)*(beta+2)*qg*qu)
for bv in [sp.Rational(1,4),sp.Rational(1,2),2]:
    d=sp.simplify((dbl-claim).subs(beta,bv)); 
    num=float(sp.N(((dbl-claim)/(claim)).subs({beta:bv,qg:sp.Rational(3,7),qu:sp.Rational(5,3),Tg:2,Tu:sp.Rational(9,4)}),30))
    print(f"  beta={bv}: relative difference at a test point = {num:.1e}")
print("  first-order term in qg: d/dqg at qg->0 of E[(qg s_g+qu s_u)^beta] = beta*qu^(beta-1)*E[s_u^(beta-1)]*Tg/2,")
fo=sp.limit(sp.diff(claim/(Tg*Tu),qg).subs(beta,sp.Rational(1,2)),qg,0)
print("  sympy (beta=1/2):",sp.simplify(fo*Tg*Tu*0+sp.diff(claim,qg).subs(beta,sp.Rational(1,2)).subs(qg,0)/(Tg*Tu)) if False else sp.simplify(sp.limit(sp.diff(claim,qg).subs(beta,sp.Rational(1,2)),qg,0)/(Tg*Tu)),
      " vs claim beta*qu^(beta-1)*Tu^(beta-1)/beta*Tg/2 =",sp.simplify((sp.Rational(1,2)*qu**(-sp.Rational(1,2))*Tu**(-sp.Rational(1,2))/sp.Rational(1,2)*Tg/2)))
print("  (E[s_u^(beta-1)] = Tu^(beta-1)/beta is finite iff beta>0, i.e. p>0.)")

# ---- numeric exact onset, R1 sensing, |e|^p bundled
def mp(p): return 2**(p/2)*Gf((p+1)/2)/np.sqrt(np.pi)
def flat_cost(q,p,c=1.0,w=1.0):
    b=p/2; T=(c*(1+b)/(b*w*mp(p)*q**b))**(1/(1+b)); return c/T+w*mp(p)*(q*T)**b/(1+b)
def Ebund(qg,qu,Tg,Tu,b):
    A=qg*Tg; B=qu*Tu
    # stable evaluation for A<<B: (A+B)^(b+2)-A^(b+2)-B^(b+2) = B^(b+2)*[(1+x)^(b+2)-1-x^(b+2)], x=A/B
    x=A/B; core=np.expm1((b+2)*np.log1p(x))-x**(b+2)
    return B**(b+2)*core/((b+1)*(b+2)*qg*qu*Tg*Tu)
def nested_cost(N,qg,qu,p,c=1.0,w=1.0):
    b=p/2
    def inner(lTg):
        Tg=np.exp(lTg)
        f=lambda lTu: c/np.exp(lTu)+w*mp(p)*Ebund(qg,qu,Tg,np.exp(lTu),b)
        T0=np.log((c*(1+b)/(b*w*mp(p)*qu**b))**(1/(1+b)))
        r=minimize_scalar(f,bounds=(T0-3,T0+3),method='bounded',options={'xatol':1e-10}); return r.fun+c/(N*Tg)
    # level interval guess from linear-in-variance loss
    r=minimize_scalar(inner,bounds=(-40,40),method='bounded',options={'xatol':1e-10})
    return r.fun
def Nstar(qg,qu,p):
    F=flat_cost(qg+qu,p)
    Gn=lambda lN: F-nested_cost(np.exp(lN),qg,qu,p)
    lo,hi=0.0,1.0
    while Gn(hi)<=0: lo=hi; hi+=1.0
    return np.exp(brentq(Gn,lo,hi,xtol=1e-9))
print("\n=== (2) R1, bundled |e|^p loss: exact N* (joint T_g,T_u), qu=1 ===")
for p in [0.5,1.0,2.0,4.0]:
    rs=[1e-3,3e-3,1e-2]; Ns=[Nstar(r,1.0,p) for r in rs]
    sl=np.polyfit(np.log(rs),np.log(Ns),1)[0]
    a_m,b_m=2/(p+2),p/(p+2)
    print(f"  p={p}: N* = {', '.join(f'{x:.1f}' for x in Ns)} at rho={rs};  slope e_g = {sl:+.3f};  lone-member (a,b)=({a_m:.3f},{b_m:.3f}) would predict {-(1-b_m)/(1-a_m):+.3f}")
# separable (|e_g|^p + |e_u|^p) for contrast, continuous time: level is an |e|^p tracker
def sep_N(qg,qu,p):
    b=p/2; k=lambda W,q: flat_cost(q,p,w=W)
    Gn=lambda lN: flat_cost(qg+qu,p)-(flat_cost(qg,p,w=np.exp(lN))/np.exp(lN)+flat_cost(qu,p))
    lo,hi=0.0,1.0
    while Gn(hi)<=0: lo=hi; hi+=1.0
    return np.exp(brentq(Gn,lo,hi,xtol=1e-9))
print("  contrast, SEPARABLE loss |e_g|^p+|e_u|^p (the review's model):")
for p in [1.0,4.0]:
    rs=[1e-3,3e-3,1e-2]; Ns=[sep_N(r,1.0,p) for r in rs]; sl=np.polyfit(np.log(rs),np.log(Ns),1)[0]
    print(f"    p={p}: slope {sl:+.3f} (power-class prediction -2/p = {-2/p:+.3f})")

# ---- class A_1 (Kalman-Bucy, precision cost c'/r), bundled absolute loss
def flatA(q,c=1.0,w=1.0):
    f=lambda lr: w*np.sqrt(2/np.pi)*(np.sqrt(q*np.exp(lr)))**0.5+c/np.exp(lr)
    return minimize_scalar(f,bounds=(-60,60),method='bounded',options={'xatol':1e-11}).fun
def nestA(N,qg,qu,c=1.0,w=1.0):
    def inner(lrg):
        Pg=np.sqrt(qg*np.exp(lrg))
        f=lambda lru: w*np.sqrt(2/np.pi)*np.sqrt(np.sqrt(qu*np.exp(lru))+Pg)+c/np.exp(lru)
        return minimize_scalar(f,bounds=(-60,60),method='bounded',options={'xatol':1e-11}).fun+c/(N*np.exp(lrg))
    return minimize_scalar(inner,bounds=(-80,80),method='bounded',options={'xatol':1e-11}).fun
def NstarA(qg,qu):
    F=flatA(qg+qu); Gn=lambda lN: F-nestA(np.exp(lN),qg,qu)
    lo,hi=0.0,1.0
    while Gn(hi)<=0: lo=hi; hi+=1.0
    return np.exp(brentq(Gn,lo,hi,xtol=1e-9))
print("\n=== (3) class A_1 (averaging), bundled absolute loss ===")
rs=[3e-3,1e-2,3e-2]; Ns=[NstarA(r,1.0) for r in rs]; sl=np.polyfit(np.log(rs),np.log(Ns),1)[0]
print(f"  N* = {', '.join(f'{x:.4g}' for x in Ns)}; slope e_g = {sl:+.3f};  quadratic-class prediction -2;  lone-member (a,b)=(4/5,1/5) would predict -4")
print("\n=== (4) convergence for p=0.5 (remainder is O(rho^(p/2)) relative) ===")
rs=[1e-6,1e-5,1e-4,1e-3]; Ns=[Nstar(r,1.0,0.5) for r in rs]
for i in range(len(rs)-1): print(f"  local slope rho {rs[i]:g}->{rs[i+1]:g}: {np.log(Ns[i+1]/Ns[i])/np.log(rs[i+1]/rs[i]):+.4f}")
print("  N* rho:",", ".join(f"{n*r:.2f}" for n,r in zip(Ns,rs)))
