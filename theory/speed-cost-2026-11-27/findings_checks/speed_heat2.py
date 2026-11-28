import sympy as sp
a,v,kT,g,eps = sp.symbols('a v kT g epsilon', positive=True)
s = sp.symbols('s', positive=True)  # s = kappa r^2 v / kT, coupling signal-to-noise
# from speed_heat.py, divide num and den by kT:
eps_expr = v*(a**2 + 2*a*g + a*g*s + g**2)/((a+g)*(a + g + g*s))
Q_over_kT = a*g*s/(a+g)                     # Qdot/kT  (kappa r^2 v = s kT)
# check limit g->oo at fixed s
print('eps(g->oo)=', sp.limit(eps_expr, g, sp.oo))
# solve eps_expr = eps for s
ssol = sp.solve(sp.Eq(eps_expr, eps), s)
print('s(eps,g)=', [sp.simplify(x) for x in ssol])
s1 = sp.simplify(ssol[0])
Q1 = sp.simplify(Q_over_kT.subs(s, s1))
print('Qdot/kT at fixed eps =', sp.factor(Q1))
floor = a*(v-eps)/eps
R = sp.simplify(Q1/floor)
print('R = Qdot/floor =', sp.factor(R))
u = sp.symbols('u', positive=True)  # u = g/a
Ru = sp.simplify(R.subs(g, u*a))
print('R(u) =', sp.factor(Ru))
print('series u->oo:', sp.series(Ru.subs(u, 1/sp.Symbol('z',positive=True)), sp.Symbol('z',positive=True), 0, 2))
# feasibility: eps must exceed the minimum achievable error at speed g with s->oo
print('eps_min(g) = lim s->oo:', sp.simplify(sp.limit(eps_expr, s, sp.oo)))
import sympy
for uu in [1,3,10,30,100]:
    for x in [sp.Rational(1,2), sp.Rational(1,10)]:  # eps/v
        val = Ru.subs({u:uu, eps:x*v})
        print('u=',uu,' eps/v=',x,' R=', sp.N(val,8))
