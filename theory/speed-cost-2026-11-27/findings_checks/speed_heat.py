# Worked-class check: OU signal tracked by an overdamped linear memory with finite mobility.
# Signal: dx = -a x dt + sqrt(2 a v) dW1 (exogenous).  Memory: dm = mu*(-kap*m + lam*x) dt + sqrt(2 mu kT) dW2.
# Memory force F = -kap m + lam x (from U = kap m^2/2 - lam m x), local detailed balance on the memory bath.
# Heat into memory bath (rate): Qdot = mu<F^2> + kT mu <dF/dm> = mu<F^2> - kT mu kap.
import sympy as sp
a,v,mu,kap,lam,kT = sp.symbols('a v mu kappa lambda kT', positive=True)
S = sp.Matrix(2,2, sp.symbols('sxx sxm sxm smm'))
sxx,sxm,smm = sp.symbols('sxx sxm smm')
S = sp.Matrix([[sxx,sxm],[sxm,smm]])
A = sp.Matrix([[-a,0],[mu*lam,-mu*kap]])
B = sp.diag(2*a*v, 2*mu*kT)
eqs = A*S + S*A.T + B
sol = sp.solve([eqs[0,0],eqs[0,1],eqs[1,1]],[sxx,sxm,smm],dict=True)[0]
Sxx,Sxm,Smm = [sp.simplify(sol[s]) for s in (sxx,sxm,smm)]
print('Sxx',Sxx); print('Sxm',Sxm); print('Smm',Smm)
eps = sp.simplify(Sxx - Sxm**2/Smm)            # MMSE of x given m (decision error)
F2 = kap**2*Smm - 2*kap*lam*Sxm + lam**2*Sxx
Q = sp.simplify(mu*F2 - kT*mu*kap)
print('eps =', sp.factor(eps)); print('Qdot =', sp.factor(Q))
# Reparametrize: g = mu*kap (memory relaxation rate), r = lam/kap (gain)
g, r = sp.symbols('g r', positive=True)
sub = {mu: g/kap, lam: r*kap}
epsg = sp.simplify(eps.subs(sub)); Qg = sp.simplify(Q.subs(sub))
print('eps(g,r,kap)=', sp.factor(epsg)); print('Q(g,r,kap)=', sp.factor(Qg))
# Floor in CORE.md:90: kT a (v-eps)/eps. Compute excess ratio Q/floor at fixed eps.
floor = kT*a*(v-epsg)/epsg
ratio = sp.simplify(Qg/floor)
print('Q/floor =', sp.factor(ratio))
