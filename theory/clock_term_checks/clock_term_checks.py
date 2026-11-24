"""Cheap rerunnable checks for theory/CLOCK_TERM_2026-11-23.md (OPEN_WORK T68).
Locked by tools/test_clock_term_checks.py (stdout must equal clock_term_checks.out).
  1. symbolic CK minimum for the general loss a (om-w')^2/f^2 + b D/f: coefficient of f is c - Kb/a, onset 2Kb/a;
  2. CK closed form (interval-averaged loss) vs multistart numerical minimum, 6 seeded cases;
  3. onset brackets: interval-averaged 5.9 / 6.1, pre-look and Poisson 3.9 / 4.1;
  4. section 9 (information-priced looks, class CK-I): b/a = 1/2 exactly, local onset at 4 kap/lam nats
     (kap = lam = 1 and kap = 2, lam = 1), naive high-SNR closed form 4.83.
"""
import os, sys, warnings
import numpy as np
import sympy as sp
from scipy.optimize import minimize
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import info_reads as ir

fails = 0
print("1. symbolic CK minimum")
K, c, w, om, f, D, wp, a, b = sp.symbols("K c w omega f D wp a b", positive=True)
J = K*wp**2/D + c*f + w*(a*(om - wp)**2/f**2 + b*D/f)
Dopt = [d for d in sp.solve(sp.diff(J, D), D) if d.is_positive is not False][0]
J1 = sp.simplify(J.subs(D, Dopt)); wpo = sp.solve(sp.diff(J1, wp), wp)[0]
J2 = sp.expand(sp.simplify(J1.subs(wp, wpo)))
coef = sp.simplify(J2.coeff(f, 1))
ok = sp.simplify(coef - (c - K*b/a)) == 0
# J(f) = A f^-1/2 + B f with B = c - Kb/a; interior clock needs w' >= 0 at f* -> onset c = 2Kb/a
print(f"  coefficient of f: {coef}  (equals c - Kb/a: {ok}); onset c* = 2Kb/a: 6K at (a,b)=(1/3,1), 4K at (1,2)")
fails += not ok

def Jck(p, c, w, om, kap, a_, b_):
    lf, lD, u = p; f_ = np.exp(lf); D_ = np.exp(lD); wp_ = om/(1 + np.exp(-u))
    return kap*wp_**2/D_ + c*f_ + w*(a_*(om - wp_)**2/f_**2 + b_*D_/f_)

def numopt(c, w, om, kap, a_=1/3, b_=1.0):
    best = np.inf
    for lf0 in (-2, 0, 2):
        for lD0 in (-4, 0, 4):
            for u0 in (-4, 0, 4):
                r = minimize(Jck, [lf0, lD0, u0], args=(c, w, om, kap, a_, b_), method="Nelder-Mead",
                             options=dict(xatol=1e-12, fatol=1e-15, maxiter=20000, maxfev=40000))
                best = min(best, r.fun)
    f0 = (2*a_*w*om**2/c)**(1/3); jn = c*f0 + a_*w*om**2/f0**2   # no clock
    return min(best, jn), jn

print("2. CK closed form vs numerical minimum (interval-averaged)")
rng = np.random.default_rng(20261123); mx = 0.0
for _ in range(6):
    kap = rng.uniform(1, 3); cc = kap*np.exp(rng.uniform(0, np.log(200)))
    ww = np.exp(rng.uniform(-2, 4)); oo = np.exp(rng.uniform(-1, 2))
    jnum, _ = numopt(cc, ww, oo, kap)
    jcl = (9/4*cc**2*ww*oo**2)**(1/3) if cc <= 6*kap else 3*((cc - 3*kap)*kap*oo**2*ww)**(1/3)
    mx = max(mx, abs(jnum - jcl)/jcl)
print(f"  6 cases, max relative gap below 1e-9: {mx < 1e-9}"); fails += mx >= 1e-9

print("3. onset brackets (kap = kT = 1, w = 3, om = 1)")
for (a_, b_, lo, hi, name) in [(1/3, 1.0, 5.9, 6.1, "interval-averaged"), (1.0, 2.0, 3.9, 4.1, "pre-look / Poisson time-averaged")]:
    res = []
    for cc in (lo, hi):
        jm, jn = numopt(cc, 3.0, 1.0, 1.0, a_, b_); pays = jm < jn*(1 - 1e-10); res.append(pays)
    print(f"  {name}: clock at c={lo}: {res[0]}, at c={hi}: {res[1]}"); fails += res != [False, True]

print("4. information-priced looks (class CK-I, reset readout, exact information)")
r = 1e-4
for mu in (0.5, 0.2):
    hm = 1e-4*mu; hs = 1e-7*mu*mu
    Ie = lambda m, s2: ir.h_ALG(m, s2, 2*r, n=80001)
    aa = mu*(Ie(mu + hm, 0) - Ie(mu - hm, 0))/(2*hm); bb = mu*mu*(Ie(mu, hs) - Ie(mu, 0))/hs
    print(f"  mu/sqrt(2r)={mu/np.sqrt(2*r):.1f}: b/a = {bb/aa:.4f}"); fails += abs(bb/aa - 0.5) > 2e-3
for kap, lam in [(1, 1), (2, 1)]:
    v = ir.local_onset(kap, lam, r)
    print(f"  kap={kap}, lam={lam}: local onset at {v:.3f} nats (4 kap/lam = {4*kap/lam:.3f})")
    fails += abs(v - 4*kap/lam) > 0.006*4*kap/lam
print(f"  naive high-SNR closed form onset (kap=lam=1): {ir.Istar(1, 1):.4f} nats (not the class's onset)")
print(f"FAILS {fails}")
print("ALL T68 CHECKS PASS" if fails == 0 else "SOME T68 CHECKS FAIL")
