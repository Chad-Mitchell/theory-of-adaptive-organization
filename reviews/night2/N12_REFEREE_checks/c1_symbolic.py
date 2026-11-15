"""N12 referee, check 1 (symbolic, independent of THEORY14_checks/onset_classes.py).
Derives the onset exponent from a general homogeneity premise rather than from the closed (a,b) forms."""
import sympy as sp
q,r,W,c,th,u,al,rho,lam,p = sp.symbols('q r W c theta u alpha rho lambda p', positive=True)

print("== 1. Generic linear-Gaussian tracker: error E(q,r) = K q^u r^(1-u) (degree-1 homogeneous) ==")
K=sp.Symbol('K',positive=True)
E = K*q**u*r**(1-u)
J = W*E + c*r**(-th)            # precision 1/r priced c*(1/r)^theta
rstar = (c*th/(W*(1-u)*K*q**u))**(1/(1-u+th))   # FOC W(1-u)E = c*th*r^-th
assert sp.simplify(sp.diff(J,r).subs(r,rstar)*r**0)==0 or abs(sp.N(sp.diff(J,r).subs(r,rstar).subs({W:1.7,c:0.3,K:1.1,q:2.2,u:0.4,th:1.3})))<1e-12
phi = sp.simplify(J.subs(r,rstar))
a_ = sp.simplify(W*sp.diff(sp.log(phi),W)); b_ = sp.simplify(q*sp.diff(sp.log(phi),q))
print(" a =",sp.simplify(a_)," b =",sp.simplify(b_))
onset = sp.simplify(-(1-b_)/(1-a_))
print(" onset exponent -(1-b)/(1-a) =",onset, "  (u = the only place the spectrum enters)")
sub = {u:1/al}
print(" with u=1/alpha: a =",sp.simplify(a_.subs(sub)),"; b =",sp.simplify(b_.subs(sub)))
vs = sp.simplify((b_-a_)/(1-a_))
print(" small-share vigilance exponent in SPEND units (b-a)/(1-a) =",vs)
print(" ... in PRECISION units (precision = spend^(1/theta) up to a constant) =",sp.simplify(vs/th))
spend = c*rstar**(-th)
ss=sp.lambdify((W,q),(spend/phi).subs({c:0.3,K:1.1,u:0.4,th:1.3}))
print(" spend share of phi at (W,q)=(1,1),(50,0.01),(0.02,300):",[round(ss(*v),12) for v in [(1,1),(50,.01),(.02,300)]],"; theory (1-u)/(1-u+theta) =",round(0.6/1.9,12))

print("\n== 2. Homogeneity is exact for any spectrum shape (linear estimator, Gaussian) ==")
print(" Scaling signal spectrum S and noise density r by lam leaves the Wiener/Kalman gain unchanged and multiplies the")
print(" MMSE by lam, so E(lam q, lam r) = lam E(q, r); power-law spectra add E = q*g(r/q) with g a power -> E = K q^u r^(1-u).")
print(" Yovits-Jackson causal MMSE for S = q|w|^-alpha:  (r/2pi) Int ln(1+q/(r w^alpha)) dw")
x=sp.Symbol('x',positive=True)
for A in [2,4]:
    I = sp.integrate(sp.log(1+x**(-A)),(x,0,sp.oo))
    print(f"  alpha={A}: Int_0^inf ln(1+x^-{A}) dx =",sp.nsimplify(sp.simplify(I)),"; pi/sin(pi/alpha) =",sp.simplify(sp.pi/sp.sin(sp.pi/A)))
print("  -> MMSE = q^(1/alpha) r^(1-1/alpha)/sin(pi/alpha), i.e. u = 1/alpha, any alpha>1 (integral converges iff alpha>1)")

print("\n== 3. Reset reads (exact reads, hold or rescaling-closed predictor): loss depends on (W,q) only via W*q ==")
T,H=sp.symbols('T H',positive=True); C=sp.Symbol('C',positive=True)
J2 = c/T + W*q*C*T**(2*H)
Ts = sp.solve(sp.diff(J2,T),T)[0]; phi2=sp.simplify(J2.subs(T,Ts))
a2=sp.simplify(W*sp.diff(sp.log(phi2),W)); b2=sp.simplify(q*sp.diff(sp.log(phi2),q))
print(" a =",sp.simplify(sp.powsimp(sp.expand_power_base(a2,force=True),force=True)),"; numeric a,b at H=0.3,W=2,q=5:",[sp.N(e.subs({H:0.3,W:2,q:5,C:0.7,c:1.3}),12) for e in (a2,b2)],"; 1/(1+2H) =",1/1.6,"; onset =",sp.simplify(-(1-b2)/(1-a2)))

print("\n== 4. Information-rate (entropy) pricing, any alpha: Duncan: info rate = MMSE/(2r) ==")
z=sp.Symbol('z',positive=True)  # z = (q/r)^(1/alpha)
# MMSE = r z /s, with s=sin(pi/alpha); info rate iota = z/(2s); r = q z^-alpha  -> MMSE = q z^(1-alpha)/s
s=sp.Symbol('s',positive=True)
J4 = W*q*z**(1-al)/s + lam*z/(2*s)
zs = sp.solve(sp.diff(J4,z),z)[0]; phi4=sp.simplify(J4.subs(z,zs))
a4=sp.simplify(W*sp.diff(sp.log(phi4),W)); b4=sp.simplify(q*sp.diff(sp.log(phi4),q))
print(" a =",a4," b =",b4," onset =",sp.simplify(-(1-b4)/(1-a4)), "(a=b: same class as reset reads)")

print("\n== 5. Edge alpha -> 1+ for priced precision ==")
a1 = a_.subs(sub); b1=b_.subs(sub)
print(" lim a =",sp.limit(a1,al,1,'+')," lim b =",sp.limit(b1,al,1,'+'))
Pi = b1**(-1/(1-a1))
for t in [sp.Rational(1,2),1,2]:
    print(f"  theta={t}: Pi* = b^(-1/(1-a)) at alpha->1+ :", sp.limit(Pi.subs(th,t),al,1,'+'), "; at alpha=2:", sp.nsimplify(Pi.subs({th:t,al:2})))
print(" spend share of info at alpha->1:", sp.limit(sp.simplify((spend/phi).subs(sub)),al,1,'+'),"(sensing worthless: E indep of r)")
