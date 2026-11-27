# T0 currency audit: algebra checks (sympy). Replace kT by kappa; check that the minimizers depend on kappa only via ratios.
import sympy as sp
k,w,a,v,s,I,e,lam,mu,b=sp.symbols('kappa w a v sigma I epsilon lambda mu beta',positive=True)
def ratio_check(expr, name):
    # homogeneity: scaling every currency (kappa,w) by lam leaves the design unchanged
    sub=sp.simplify(expr.subs({k:lam*k,w:lam*w},simultaneous=True)-expr)
    print(f"{name}: design = {sp.simplify(expr)} ; invariant under (kappa,w)->lam*(kappa,w): {sub==0}")
# A1 OU
Is=sp.sqrt(a*v*w/k)-a; ratio_check(Is,'A1 OU I*')
# A3 sum of two modes, one rank-one memory with heat kappa*mu, error sum v_i a_i/(a_i+mu)
a1,a2,v1,v2=sp.symbols('a1 a2 v1 v2',positive=True)
J3=k*mu+w*(v1*a1/(a1+mu)+v2*a2/(a2+mu)); foc=sp.together(sp.diff(J3,mu)/k)
print('A3 FOC/kappa depends on kappa only via w/kappa:', sp.simplify(foc.subs(w,sp.Symbol('x')*k)).has(k)==False)
# A5 drifting spring: heat c*kappa*s^2/(2e) + w e, c=1 (fast spring) or 2 (Kalman)
c=sp.symbols('c',positive=True); J5=c*k*s**2/(2*e)+w*e; es=sp.solve(sp.diff(J5,e),e)[0]; ratio_check(es,'A5 spring eps*')
# A10 concavity in v of J* = 2 sqrt(kappa a v w) - kappa a
Js=2*sp.sqrt(k*a*v*w)-k*a; print('A10 d2J*/dv2 =',sp.simplify(sp.diff(Js,v,2)),'(<0 for all kappa>0)')
# A12 selection: beta*J for J = kappa*I + w*eps(I); written as (beta*kappa)*(I + (w/kappa) eps)
x=sp.symbols('x',positive=True); J12=k*I+w*a*v/(I+a)
print('A12 beta*J - (beta*kappa)*(I + (w/kappa) eps) =',sp.simplify(b*J12-(b*k)*(I+(w/k)*a*v/(I+a))))
