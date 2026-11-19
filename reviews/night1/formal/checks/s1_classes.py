"""S1. Lemma 1 (sensing classes): closed-form single-tracker cost phi(W,q), its stakes elasticity a and drift
elasticity b, and the information-spend share, for every class used in THEOREMS.md. Sympy for algebra;
numpy/scipy for random-parameter checks against brute-force minimisation."""
import sympy as sp, numpy as np
from scipy.optimize import minimize_scalar
rng=np.random.default_rng(1)
W,q,c,T,H,lam,kap,r,cp,th,p,al,C=sp.symbols('W q c T H lambda kappa r cprime theta p alpha C',positive=True)
import random
def numzero(expr,n=25):
    """identity check: |expr| at n random positive points, 40-digit precision"""
    syms=sorted(expr.free_symbols,key=str); worst=0
    for _ in range(n):
        sub={s_:sp.Rational(random.randint(1,40),random.randint(1,40)) for s_ in syms}
        if H in sub: sub[H]=sp.Rational(random.randint(1,19),20)
        if p in sub and al in sub: sub[p]=sub[al]*sp.Rational(random.randint(1,9),10)
        v=abs(sp.N(expr.subs(sub),40)); worst=max(worst,float(v))
    return worst
random.seed(7)
def report(name,J,var,sol,a_claim=None,b_claim=None):
    foc=sp.diff(J,var).subs(var,sol)
    phi=J.subs(var,sol)
    a=sp.diff(sp.log(phi),W)*W; b=sp.diff(sp.log(phi),q)*q
    print(f"--- {name}\n  argmin = {sp.simplify(sol)}\n  |FOC at argmin| max over random points (must be ~0): {numzero(foc):.1e}")
    if a_claim is not None:
        print(f"  a = {a_claim}: max|a - claim| = {numzero(a-a_claim):.1e};  b = {b_claim}: max|b - claim| = {numzero(b-b_claim):.1e}")
        a,b=a_claim,b_claim
    else:
        a=sp.simplify(a); b=sp.simplify(b); print(f"  a = {a}   b = {b}")
    return phi,a,b
# R1, fBm Hurst H, zero-order hold, periodic reads
J=c/T+W*q*T**(2*H)/(1+2*H)
Ts=(c*(1+2*H)/(2*H*W*q))**(1/(1+2*H))
phi,a,b=report("R1 fBm(H), periodic complete reads",J,T,Ts,1/(1+2*H),1/(1+2*H))
print("  spend share c/T*/phi = 2H/(1+2H): max dev",f"{numzero((c/Ts)/phi-2*H/(1+2*H)):.1e}")
print("  convexity d2J/dT2 at T* > 0:",sp.simplify(sp.diff(J,T,2).subs(T,Ts)).subs({H:sp.Rational(1,2)}))
# R1, Brownian, |e|^p loss (separable): avg loss = m_p (qT)^{p/2}/(1+p/2)
mp=sp.Symbol('m_p',positive=True)
J=c/T+W*mp*(q*T)**(p/2)/(1+p/2)
Ts=(2*c*(1+p/2)/(p*W*mp*q**(p/2)))**(1/(1+p/2))
phi,a,b=report("R1 Brownian, |e|^p loss",J,T,Ts,2/(p+2),p/(p+2))
print("  e_g=-(1-b)/(1-a) =",sp.simplify(-(1-b)/(1-a)))
# R1, alpha-stable drift (scale q^(1/alpha) t^(1/alpha)), |e|^p with p<alpha
J=c/T+W*C*(q*T)**(p/al)/(1+p/al)
Ts=(c*(1+p/al)*al/(p*W*C*q**(p/al)))**(1/(1+p/al))
phi,a,b=report("R1 alpha-stable, |e|^p",J,T,Ts,al/(al+p),p/(al+p))
print("  e_g=-(1-b)/(1-a) =",sp.simplify(-(1-b)/(1-a)))
# R2 entropy-priced: error variance q/(2 kappa); cost lambda per nat
J=W*q/(2*kap)+lam*kap; ks=sp.sqrt(W*q/(2*lam))
phi,a,b=report("R2 entropy-priced channel (Brownian, quadratic)",J,kap,ks)
# Kalman-Bucy: Riccati 0 = q - P^2/r  ->  P = sqrt(q r);  Duncan: info rate = P/(2r)
P=sp.Symbol('P',positive=True); Ps=sp.solve(sp.Eq(q-P**2/r,0),P); print("--- Kalman-Bucy steady state P =",Ps)
rate=sp.simplify(sp.sqrt(q*r)/(2*r)); print("  info rate P/(2r) =",rate," ; P expressed via rate kappa:",sp.simplify(sp.sqrt(q*r).subs(r,sp.solve(sp.Eq(rate,kap),r)[0])))
# Class A_theta: precision bought at cost c' r^(-theta)
J=W*sp.sqrt(q*r)+cp*r**(-th)
rs=(2*th*cp/(W*sp.sqrt(q)))**(1/(th+sp.Rational(1,2)))
phi,a,b=report("A_theta averaging (precision cost c' r^-theta)",J,r,rs,2*th/(1+2*th),th/(1+2*th))
print("  b - a/2 =",sp.simplify(b-a/2),"   e_g=-(1-b)/(1-a) =",sp.simplify(-(1-b)/(1-a)),"   (b-a)/(1-a) =",sp.simplify((b-a)/(1-a)))
print("  spend share = 1/(1+2theta): max dev",f"{numzero((cp*rs**(-th))/phi-1/(1+2*th)):.1e}")
for t_ in [1,sp.Rational(1,2)]:
    print(f"  theta={t_}: a={sp.simplify(a.subs(th,t_))}, b={sp.simplify(b.subs(th,t_))}, phi={sp.simplify(phi.subs(th,t_))}")
# Class A, absolute loss for lone member: E|e| = sqrt(2P/pi)
J=W*sp.sqrt(2/sp.pi)*(q*r)**sp.Rational(1,4)+cp/r
rs=sp.solve(sp.diff(J,r),r)[0]
phi,a,b=report("A_1 averaging, absolute loss (lone member)",J,r,rs)
print("  member-measured e_pred=-(1-b)/(1-a) =",sp.simplify(-(1-b)/(1-a)))

print("\n=== numeric: brute-force minimisation vs closed forms, 2000 random parameter sets per class ===")
def num_phi(f):
    res=minimize_scalar(lambda lz: f(np.exp(lz)),bounds=(-40,40),method='bounded',options={'xatol':1e-11})
    return res.fun
maxerr={}
for _ in range(2000):
    Wv,qv,cv=10**rng.uniform(-2,2,3); Hv=rng.uniform(0.1,0.9); pv=rng.uniform(0.3,4); thv=rng.uniform(0.2,2)
    # R1 fBm
    f=lambda T_: cv/T_+Wv*qv*T_**(2*Hv)/(1+2*Hv)
    Ts_=(cv*(1+2*Hv)/(2*Hv*Wv*qv))**(1/(1+2*Hv)); cf=f(Ts_)
    maxerr['R1fBm']=max(maxerr.get('R1fBm',0),abs(num_phi(f)-cf)/cf)
    # A_theta
    f=lambda r_: Wv*np.sqrt(qv*r_)+cv*r_**(-thv)
    rs_=(2*thv*cv/(Wv*np.sqrt(qv)))**(1/(thv+0.5)); cf=f(rs_)
    maxerr['Atheta']=max(maxerr.get('Atheta',0),abs(num_phi(f)-cf)/cf)
    # numeric elasticities of A_theta by finite differences vs closed form a=2th/(1+2th), b=th/(1+2th)
    def ph(Wx,qx): return num_phi(lambda r_: Wx*np.sqrt(qx*r_)+cv*r_**(-thv))
    e=1e-4; an=(np.log(ph(Wv*np.exp(e),qv))-np.log(ph(Wv*np.exp(-e),qv)))/(2*e); bn=(np.log(ph(Wv,qv*np.exp(e)))-np.log(ph(Wv,qv*np.exp(-e))))/(2*e)
    maxerr['A_a']=max(maxerr.get('A_a',0),abs(an-2*thv/(1+2*thv))); maxerr['A_b']=max(maxerr.get('A_b',0),abs(bn-thv/(1+2*thv)))
for k,v in maxerr.items(): print(f"  max error {k}: {v:.2e}")
print("\nKalman-Bucy Riccati by ODE integration (q=0.3, r=2): ",end="")
from scipy.integrate import solve_ivp
s=solve_ivp(lambda t,P_: 0.3-P_**2/2.0,(0,200),[5.0],rtol=1e-10); print(f"P(200)={s.y[0,-1]:.8f} vs sqrt(qr)={np.sqrt(0.6):.8f}")
