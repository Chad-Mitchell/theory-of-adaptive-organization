"""Master-equation review checks. Run: nice -n 19 python3 meq_checks.py"""
import sympy as sp, numpy as np, sys
from scipy.optimize import minimize_scalar, brentq
sys.path.insert(0,'/workspace/gtao-spine/checks')
print("== S1 CT12: K=1, kappa=0, g=0, hold-last-value, exact reads ==")
T,c,w,q,a,s,k=sp.symbols('T c w q alpha s k',positive=True)
Ebar=sp.integrate(q*s**(a-1),(s,0,T))/T
J=c/T+w*Ebar
print(" mean error over cycle:",sp.simplify(Ebar))
Ts=sp.solve(sp.diff(J,T),T)
print(" T* =",[sp.simplify(t) for t in Ts])
Tst=(a*c/((a-1)*w*q))**(1/a)
print(" matches CT12 T*:",sp.simplify(sp.diff(J,T).subs(T,Tst))==0)
f=1/Tst
for v in (w,q,c):
    print(f"  elasticity of read rate in {v}:",sp.simplify(sp.diff(sp.log(f),v)*v))
print(" second derivative >0 (alpha>1):",sp.simplify(sp.diff(J,T,2)))
Jst=sp.simplify(J.subs(T,Tst))
print(" J* at alpha=2:",sp.simplify(Jst.subs(a,2)), " (inventory sigma*sqrt(2cw) with q=sigma^2)")
print(" CT13 penalty J(kT*)/J*:",sp.simplify((J.subs(T,k*Tst)/Jst)), "-> at a=2:",sp.simplify((J.subs(T,k*Tst)/Jst).subs(a,2)))

print("\n== S2 CT7: read term re-priced per nat acquired (lam per nat), world sigma^2 random walk ==")
D,sig,lam=sp.symbols('D sigma lambda',positive=True)
Jn=lam*sig**2/(2*D)+w*D
Dst=sp.solve(sp.diff(Jn,D),D)[0]; print(" D* =",sp.simplify(Dst)," J* =",sp.simplify(Jn.subs(D,Dst)))
print(" -> with lam=kT: sigma*sqrt(2 kT w). Note: this is a LOWER BOUND over trackers whose learning rate <= entropy production; it uses a per-nat price, not c_k*f_k per read.")

print("\n== S3 L1-L3: J_K = hK + w E_K (sensing priced by fixed noise density N; read rates not chosen) ==")
from stores import E_inf, E_K
A=[1.0,0.1]; V=[0.5,0.5]; N=0.1
Einf=E_inf(A,V,N); E1=E_K(A,V,N,1)[0]; E2=E_K(A,V,N,2)[0]
print(f" two OU modes a={A}, v={V}, N={N}: E_inf={Einf:.6f} E_1={E1:.6f} E_2={E2:.6f}  eps1={(E1/Einf-1)*100:.3f}%  R*={1/(E1/Einf-1):.1f}")
print(" monotone comparative statics: K* over w/h grid:")
for R in [1,10,30,100,300,1000]:
    h=1.0; ww=R*h/Einf
    Js={1:h+ww*E1,2:2*h+ww*E2}
    print(f"   R={R:5}: J1={Js[1]:.3f} J2={Js[2]:.3f} K*={min(Js,key=Js.get)}")

print("\n== S4 Theorem L vs the chance constraint P(ruin)<=eps (diffusion approx, GENERAL_THEOREM s5 setting) ==")
y,cc,ww,sg,s0=1.0,0.05,1.0,1.0,0.3
m=lambda t: y-cc/t-ww*sg**2*t/2
s2=lambda t: s0**2+ww**2*sg**4*t**3/3
th=lambda t: 2*m(t)/s2(t)
tE=np.sqrt(2*cc/(ww*sg**2))
r=minimize_scalar(lambda t:-th(t),bounds=(1e-3,3),method='bounded'); tS=r.x
print(f" cost-optimal (EOQ) tau={tE:.4f}; survival-optimal argmax theta tau={tS:.4f}; theta(EOQ)={th(tE):.3f}, theta_max={th(tS):.3f}")
eps=1e-3
print(f" constrained: min expected cost s.t. theta(tau) >= ln(1/eps)/B  (sufficient via Lundberg P<=e^-thetaB), eps={eps}")
for B in [0.5,0.8,1.0,1.5,3,10]:
    tmin=np.log(1/eps)/B
    if tmin>th(tS): print(f"   B={B:5}: infeasible (theta_min={tmin:.2f} > theta_max) -> no design survives at this eps"); continue
    if th(tE)>=tmin: print(f"   B={B:5}: constraint slack, tau*=EOQ {tE:.4f}, multiplier 0"); continue
    # boundary on EOQ side between tS and tE
    tb=brentq(lambda t: th(t)-tmin, tS, tE)
    h_=1e-6
    dm=(m(tb+h_)-m(tb-h_))/(2*h_); dth=(th(tb+h_)-th(tb-h_))/(2*h_)
    mu=-dm/dth   # Lagrange multiplier: d(max mean margin)/d(theta_min) = -mu
    print(f"   B={B:5}: binding, tau*={tb:.4f} (between {tS:.3f} and EOQ {tE:.3f}); cost premium={(m(tE)-m(tb)):.5f}; multiplier mu={mu:.5f} per unit theta; value of buffer dJ*/dB={-mu*np.log(1/eps)/B**2:.5f}")
print(" Note: argmax theta does not depend on B (L3); in the CONSTRAINED form B enters through theta_min, and large B makes the constraint slack -> EOQ.")
print(" Policy-insensitive variance check (s0 large):")
s0b=3.0
s2b=lambda t: s0b**2+ww**2*sg**4*t**3/3
r2=minimize_scalar(lambda t:-2*m(t)/s2b(t),bounds=(1e-3,3),method='bounded')
print(f"   s0={s0b}: argmax theta={r2.x:.4f} vs EOQ {tE:.4f}")

print("\n== S5 recursion/closure: pooled tracker in power class phi = k p^(1-a) W^a q^b ==")
p,W,qq,aa,bb,n=sp.symbols('p W q a b n',positive=True)
phi=lambda W_,q_: p**(1-aa)*W_**aa*q_**bb
# R1 at alpha=2: a=b=1/2
print(" R1(alpha=2) phi(W,q) = sqrt(2cWq):",sp.simplify(Jst.subs(a,2).subs({w:W,q:qq})))
print(" n identical members pooled into one level: phi(nW, q) / (n phi(W,q)) =",sp.simplify(phi(n*W,qq)/(n*phi(W,qq))), "-> n^(a-1): pooling gain grows with n since a<1")
