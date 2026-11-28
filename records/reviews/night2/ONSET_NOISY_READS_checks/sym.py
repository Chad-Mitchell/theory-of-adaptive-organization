"""ONSET-NOISY-READS check 3 (sympy): branch algebra.
Exact branch: phi = min_T 1/T + A T^(a-1)  -> kappa A^(1/a); onset x D0 = kappa (x f0)^(1/a)  -> X0.
Noisy branch: level cost min_T 1/T + x g s^b T^b (b = 1-1/a)  [from x T^(a-1) * g (s/T^(a-1))^b]; onset x D0 = that -> x = C_inf s.
Also: Yovits-Jackson integral int_0^inf ln(1+u^-a) du = pi/sin(pi/a); class exponents of the noisy branch."""
import sympy as sp
a, A, T, x, s, f0, g = sp.symbols('alpha A T x s f0 g', positive=True)
b = 1-1/a
def tmin(expr):
    Ts = sp.solve(sp.diff(expr, T), T)
    return [sp.simplify(expr.subs(T, t)) for t in Ts]
# exact branch
ph = tmin(1/T + A*T**(a-1))[0]
kappa = sp.simplify(ph/A**(1/a))
print("kappa vs a (a-1)^(1/a-1) at (alpha, A):", [(av, Av, float(sp.N((kappa - a*(a-1)**(1/a-1)).subs({a: av, A: Av})))) for av in (1.5, 2, 2.5) for Av in (0.3, 7)])
kappa = a*(a-1)**(1/a-1)
D0 = sp.simplify(sp.diff(kappa*(1*f0)**(1/a)*sp.Symbol('q')**(1/a), sp.Symbol('q')).subs(sp.Symbol('q'), 1))
print("D0 =", D0)
X0 = sp.solve(sp.Eq(x*D0, kappa*(x*f0)**(1/a)), x); print("X0 =", [sp.simplify(v) for v in X0])
for av in (1.5, 2, 2.5): print("  X0 at", av, [sp.N(v.subs(a, av)) for v in X0])
# noisy branch: check x T^(a-1) g (s/T^(a-1))^b == x g s^b T^b
print("noisy integrand identity:", sp.simplify(x*T**(a-1)*g*(s/T**(a-1))**b - x*g*s**b*T**b) == 0)
B = sp.Symbol('B', positive=True)
phn = tmin(1/T + B*T**b)[0]; print("noisy level cost =", sp.simplify(phn))
Cinf = ((2*a-1)/((a-1)*D0))**((2*a-1)/(a-1))*(g*(a-1)/a)**(a/(a-1))
lhs = (Cinf*s)*D0; rhs = phn.subs(B, Cinf*s*g*s**b)
for av, gv, fv, sv in ((1.5, 0.8456, 0.591, 3.0), (2, 1, 0.5, 7.0), (2.5, 1.0258, 0.3231, 0.2)):
    print(f"  onset identity x=C_inf s at alpha={av}: lhs {sp.N(lhs.subs({a:av,g:gv,f0:fv,s:sv})):.10f} rhs {sp.N(rhs.subs({a:av,g:gv,f0:fv,s:sv})):.10f}")
# class exponents: noisy level phi ∝ W^{a_L} q^{b_L}; B = W g q^{1/a} sigma^{2b}
W, q = sp.symbols('W q', positive=True)
lp = sp.log(phn.subs(B, W*q**(1/a)))
for av in (1.5, 2, 2.5, 2.9):
    sub = {a: av, W: 3.7, q: 0.02}
    aL = float(sp.N((lp.diff(W)*W).subs(sub))); bL = float(sp.N((lp.diff(q)*q).subs(sub)))
    print(f"  alpha={av}: noisy class a_L={aL:.12f} (a/(2a-1)={av/(2*av-1):.12f}) b_L={bL:.12f} (1/(2a-1)={1/(2*av-1):.12f}) onset exponent {-(1-bL)/(1-aL):.12f}")
u = sp.Symbol('u', positive=True)
for av in (sp.Rational(3, 2), 2, sp.Rational(5, 2)):
    I = sp.Integral(sp.log(1+u**(-av)), (u, 0, sp.oo)).evalf(20); print(f"  int ln(1+u^-{av}) = {I}  pi/sin(pi/a) = {sp.N(sp.pi/sp.sin(sp.pi/av), 20)}")
