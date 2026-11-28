#!/usr/bin/env python3
"""STORE-COEF-REVIEW: exact alpha -> 2 limit of c for one unit-gain EWMA in the scale-free continuous world.
E(lam) = q lam^(1-alpha)/(-2 cos(pi alpha/2)) + N lam/2 (two-sided spectrum, dw/2pi); e* = q^(1/alpha) N^(1-1/alpha)/sin(pi/alpha)."""
import sympy as sp
a, e = sp.symbols('a e', positive=True)
A = 1/(-2*sp.cos(sp.pi*a/2)); lam = (2*(a-1)*A)**(1/a); E = lam*a/(2*(a-1)); es = 1/sp.sin(sp.pi/a)
s = sp.series((E/es-1).subs(a, 2+e), e, 0, 3).removeO()
print("linear coefficient:", sp.simplify(s.coeff(e, 1)))
print("c(2) =", sp.nsimplify(sp.simplify(s.coeff(e, 2))), "=", sp.N(s.coeff(e, 2), 10))
