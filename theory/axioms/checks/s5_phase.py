"""S5. Theorem 7 (freeze / hold / look up) and the fallback cliff; shared-store widening; power-class generalisation;
T5 (Poisson change, bounded loss) interior-peak condition."""
import sympy as sp, numpy as np
from scipy.optimize import minimize_scalar
rng=np.random.default_rng(5)
c,W,q,h,mu,u,Hl,N,T=sp.symbols('c W q h mu u H_l N T',positive=True)
qf=2*c/(W*Hl**2); qc=(mu*u-h)**2/(2*c*W)
print("=== (1) symbolic edges ===")
Tst=sp.sqrt(2*c/(W*q)); print("  freeze edge: T*(q_f) - H_l =",sp.simplify(Tst.subs(q,qf)-Hl))
print("  lookup edge: sqrt(2cW q_c)+h - mu u =",sp.simplify(sp.sqrt(2*c*W*qc)+h-mu*u)," (for mu u>h)")
cond=sp.simplify(sp.factor(qc-qf)); print("  q_c - q_f =",cond)
print("  q_c>q_f  <=>  H_l(mu u - h) > 2c  <=>  mu u H_l > 2c + h H_l   [ (mu u-h)^2 H_l^2 > 4c^2, mu u>h ]")
qcN=(N*mu*u-h)**2/(2*c*N*W); qfN=2*c/(N*W*Hl**2)
print("  shared store, h=0: (q_c/q_f)_N / (q_c/q_f)_1 =",sp.simplify((qcN/qfN/(qc/qf)).subs(h,0)))
print("  elasticity of q_c in u:",sp.simplify(sp.diff(sp.log(qc),u)*u)," (=2 at h=0); of sigma_c=sqrt(q_c):",sp.simplify(sp.diff(sp.log(sp.sqrt(qc)),u)*u))
print("\n=== (2) numeric phase diagram on a q-grid, 2000 random parameter sets ===")
def mode(qv,cv,Wv,hv,muu,H):
    Ts=np.sqrt(2*cv/(Wv*qv)); T_=min(Ts,H); hold=cv/T_+Wv*qv*T_/2+hv
    if muu<hold: return 'L'
    return 'F' if Ts>=H else 'H'
mism=0; edge_err=0; n=0
for _ in range(2000):
    cv,Wv=10**rng.uniform(-1,1,2); H=10**rng.uniform(0,2); hv=10**rng.uniform(-3,0); muu=10**rng.uniform(-1,1.5)
    qs=np.logspace(-8,6,1400); ms=[mode(x,cv,Wv,hv,muu,H) for x in qs]
    band='H' in ms; pred=(muu*H>2*cv+hv*H) and (muu>hv)
    n+=1; mism+=(band!=pred)
    if band:
        qH=[x for x,m in zip(qs,ms) if m=='H']; qc_=(muu-hv)**2/(2*cv*Wv); qf_=2*cv/(Wv*H**2)
        edge_err=max(edge_err,abs(np.log(qH[-1]/qc_)),abs(np.log(qH[0]/qf_)))
print(f"  band existence mismatches vs (mu u H_l > 2c + h H_l): {mism}/{n};  max |log edge error| = {edge_err:.4f} (grid step {np.log(qs[1]/qs[0]):.4f})")
print("\n=== (3) power class hold cost k W^a q^b + h vs lookup mu u: q_c = ((mu u - h)/(k W^a))^(1/b) ===")
a,b,k=sp.symbols('a b k',positive=True)
qc2=((mu*u-h)/(k*W**a))**(1/b); print("  elasticity in u at h=0:",sp.simplify((sp.diff(sp.log(qc2),u)*u).subs(h,0)))
qc2N=((N*mu*u)/(k*(N*W)**a))**(1/b); print("  shared (N users) / single, h=0:",sp.simplify(qc2N/qc2.subs(h,0)))
print("\n=== (4) fallback cliff: effort just below q_c is strictly positive (R1: 1/T* = sqrt(Wq/2c)) ===")
print("  effort at q_c^- =",sp.simplify(sp.sqrt(W*qc/(2*c)))," > 0 whenever mu u > h ; effort above q_c = 0  => discontinuity")
print("\n=== (5) T5: Poisson change rate lam, use rate mu, bounded miss loss Wb, refresh cost c: f*>0 iff lam < mu Wb/c ===")
bad=0
for _ in range(3000):
    lam,muv,Wb,cv=10**rng.uniform(-2,2,4)
    F=lambda f: (f/lam)*(1-np.exp(-lam/f)) if f>0 else 0.0
    cost=lambda lf: cv*np.exp(lf)+muv*Wb*(1-F(np.exp(lf)))
    r=minimize_scalar(cost,bounds=(-30,10),method='bounded',options={'xatol':1e-10})
    interior = r.fun < muv*Wb*(1-1e-9)
    if interior != (lam<muv*Wb/cv) and abs(lam-muv*Wb/cv)/lam>1e-3: bad+=1
print(f"  mismatches: {bad}/3000")
