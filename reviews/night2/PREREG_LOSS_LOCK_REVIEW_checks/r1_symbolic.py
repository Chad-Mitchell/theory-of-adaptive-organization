"""Reviewer's own symbolic derivation (imports nothing from the author's checks).
Reset reads (exact reads, hold-last-value or any rescaling-closed predictor), fBm H=(alpha-1)/2, loss |e|^p, Gaussian errors.
Time-averaged loss over a read interval T: (1/T) int_0^T k_p (q t^{2H})^{p/2} dt = k_p q^{p/2} T^{pH}/(1+pH).
Precision effort r=1/N, linear price c*r, filtering error V = K q^{1/alpha} N^{1-1/alpha} (Yovits-Jackson scaling; r3 checks it).
"""
import sympy as sp
a, p, w, q, c, T, k, r, K = sp.symbols('alpha p w q c T k r K', positive=True)
H = (a-1)/2
# reset reads
J = c/T + w*k*q**(p/2)*T**(p*H)/(1+p*H)
Tstar = sp.solve(sp.diff(J, T), T)[0]
rate = sp.simplify(1/Tstar)
aw = sp.simplify(sp.diff(sp.log(rate), w)*w)
bq = sp.simplify(sp.diff(sp.log(rate), q)*q)
print('reset reads: a_p =', sp.simplify(aw), ' b_p =', sp.simplify(bq))
print('  equals 2/(2+p(a-1))?', sp.simplify(aw - 2/(2+p*(a-1))) == 0, ' p/(2+p(a-1))?', sp.simplify(bq - p/(2+p*(a-1))) == 0)
print('  p=2:', sp.simplify(aw.subs(p, 2)), sp.simplify(bq.subs(p, 2)))
print('  a_p=b_p solve for p:', sp.solve(sp.Eq(aw, bq), p))
print('  alpha=2 (formal Lemma 1(iv) 2/(p+2), p/(p+2)):', sp.simplify(aw.subs(a, 2) - 2/(p+2)) == 0, sp.simplify(bq.subs(a, 2) - p/(p+2)) == 0)
print('  alpha=2,p=1:', aw.subs({a: 2, p: 1}), bq.subs({a: 2, p: 1}))
# precision effort
V = K*q**(1/a)*(1/r)**(1-1/a)
J2 = c*r + w*k*V**(p/2)
# FOC: c = d/dr(-w k V^{p/2}) ; solve r* as power law: r^{e} = const*w*q^{p/(2a)}
e = 1 + (p/2)*(1-1/a)
rstar = (w*k*K**(p/2)*q**(p/(2*a))*(p/2)*(1-1/a)/c)**(1/e)
foc = sp.simplify(sp.diff(J2, r).subs(r, rstar))
print('precision: FOC residual at r* =', sp.simplify(foc))
aw2 = sp.simplify(sp.diff(sp.log(rstar), w)*w); bq2 = sp.simplify(sp.diff(sp.log(rstar), q)*q)
print('  a =', aw2, ' b =', bq2)
print('  equals 2a/(2a+p(a-1))?', sp.simplify(aw2 - 2*a/(2*a+p*(a-1))) == 0, ' p/(2a+p(a-1))?', sp.simplify(bq2 - p/(2*a+p*(a-1))) == 0)
print('  p=2:', sp.simplify(aw2.subs(p, 2)), sp.simplify(bq2.subs(p, 2)))
print('  ratio b/a =', sp.simplify(bq2/aw2), '(=p/(2 alpha); a=b impossible for alpha>1 unless p=2 alpha)')
# separable onset exponent at the lone-member exponents, alpha=2: -(1-b)/(1-a) (formal Thm 4 table: -2 at p=1, -1/2 at p=4, -4 at p=1/2)
eg = sp.simplify(-(1-bq)/(1-aw))
print('separable lone-member onset -(1-b_p)/(1-a_p) =', eg, '; alpha=2: p=1/2,1,2,4 ->', [eg.subs({a: 2, p: v}) for v in (sp.Rational(1, 2), 1, 2, 4)])
# Theorem 4 H3 for R1 at general alpha: kappa_l = E_t[L'(V_u(t))], L'(v) ~ v^{p/2-1}, V_u(t) ~ t^{alpha-1}; finite iff (alpha-1)(p/2-1) > -1
pmin = sp.solve(sp.Eq((a-1)*(p/2-1), -1), p)[0]
print('H3 (R1, fBm) finite iff p >', sp.simplify(pmin), '; alpha=1.5,2,2.5 ->', [sp.simplify(pmin.subs(a, v)) for v in (sp.Rational(3, 2), 2, sp.Rational(5, 2))])
import random
random.seed(1)
for _ in range(5):
    vals = {a: sp.Rational(random.randint(11, 29), 10), p: sp.Rational(random.randint(1, 40), 10), w: random.uniform(.1, 9), q: random.uniform(.1, 9),
            c: random.uniform(.1, 9), k: random.uniform(.1, 3), K: random.uniform(.1, 3)}
    print('  precision FOC residual (numeric, 30 digits):', sp.N(foc.subs(vals), 30))
