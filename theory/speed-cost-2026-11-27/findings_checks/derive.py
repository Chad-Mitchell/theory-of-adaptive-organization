"""Derivations for FINDINGS.md. Run: nice -n 19 python3 derive.py"""
import sympy as sp
kT,a,v,w,g,eps,q,k,N,tau,mud = sp.symbols('kT a v w g epsilon q k N tau mu_d', positive=True)
print("== D1: finite-speed linear memory on one OU signal ==")
n = 1 + g/a
Q = kT*a*n*(v-eps)/(n*eps - v)           # from speed_heat2.py, feasible iff eps > a v/(a+g)
J = Q + w*eps
dJ = sp.simplify(sp.diff(J, eps))
print("dJ/deps =", sp.factor(dJ))
Delta = sp.sqrt(kT*a*n*(n-1)*v/w)
epsstar = (v + Delta)/n
print("FOC at eps*:", sp.simplify(dJ.subs(eps, epsstar)))
Jstar = sp.simplify(J.subs(eps, epsstar))
target = 2*sp.sqrt(kT*a*v*w*g/(a+g)) - kT*a + w*v*a/(a+g)
print("J* - claimed form =", sp.simplify(sp.expand(Jstar - target)))
print("g->oo limit of claimed J*:", sp.limit(target, g, sp.oo), " (CORE.md:91 is 2*sqrt(kT a v w) - kT a)")
# threshold: eps* <= v  <=>  w >= kT a (a+g)/(g v)
print("memory pays iff w*v/(kT*a) >", sp.simplify((a+g)/g))
# blind cost w v; check J*=wv at threshold
wth = kT*a*(a+g)/(g*v)
print("J* - w v at threshold:", sp.simplify(target.subs(w, wth) - wth*v))
# numeric brute-force check at one point
import numpy as np
from scipy.optimize import minimize_scalar
vals = {kT:1.0, a:1.0, v:1.0, w:10.0, g:5.0}
f = sp.lambdify(eps, J.subs(vals), 'numpy')
emin = vals[a]*vals[v]/(vals[a]+vals[g])
res = minimize_scalar(f, bounds=(emin*1.0000001, 1.0), method='bounded', options={'xatol':1e-12})
print("numeric min J =", res.fun, " closed form =", float(target.subs(vals)), " CORE limit =", float((2*sp.sqrt(kT*a*v*w)-kT*a).subs(vals)))

print("\n== D2: Brownian (Markov-jump) computer of depth N, deadline tau ==")
b = sp.symbols('b', positive=True)
# rates k e^{b/2} forward, k e^{-b/2} backward; mean net velocity 2k sinh(b/2); entropy per net step b
bsol = 2*sp.asinh(N/(2*k*tau))
print("check velocity*tau = N:", sp.simplify(2*k*sp.sinh(bsol/2)*tau - N))
Qc = 2*kT*N*sp.asinh(N/(2*k*tau))
print("Q_comp =", Qc)
print("slow series (tau large):", sp.series(Qc.subs(tau, 1/sp.Symbol('z',positive=True)), sp.Symbol('z',positive=True), 0, 2))
# J with lateness on a random walk (error grows q*tau), decisions at rate mu_d, slow regime
Jc = mud*kT*N**2/(k*tau) + w*q*tau
ts = sp.solve(sp.diff(Jc, tau), tau)[0]
print("tau* =", sp.simplify(ts), "  J_comp* =", sp.simplify(Jc.subs(tau, ts)))
# compare to CT7 info floor sigma*sqrt(2 kT w) with sigma^2=q
ratio = sp.simplify(Jc.subs(tau, ts)/(sp.sqrt(q)*sp.sqrt(2*kT*w)))
print("J_comp*/J_info* (CT7) =", ratio, " => equal at N =", sp.solve(sp.Eq(ratio,1), N))
# self-consistency of slow regime: N/(2 k tau*) small
print("N/(2k tau*) =", sp.simplify(N/(2*k*ts)))
