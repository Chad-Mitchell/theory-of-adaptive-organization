"""Each special case listed in THEORY.md v2.1 §5 is the master equation J restricted as stated.

J(D) = kappa*I_mem + h*K + w*E[loss] + A(D) + L(D), subject to P(ruin) <= eps_r, world exogenous (g = 0).

Every block below writes J under the restriction named in THEORY §5's table, solves it, and asserts the
published result (Appendix B / theory/LAYERS.md). A failed assertion exits nonzero. stdlib + numpy + scipy + sympy.
Run from anywhere:  nice -n 19 python3 theory/meq_checks/meq_derive.py   (a few seconds)
"""
import os, sys, math
import numpy as np, sympy as sp
from scipy.optimize import minimize_scalar, brentq
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "layers_checks"))
from stores import E_inf, E_K  # noqa: E402

results = []
def check(name, ok, detail=""):
    results.append((name, bool(ok)))
    print(("PASS " if ok else "FAIL ") + name + (": " + detail if detail else ""))

# --- CT12 read-rate rule: K=1, kappa=h=L=0, A = c/T (exact reset reads), hold-last-value, W-b world
T, c, w, q, a = sp.symbols("T c w q alpha", positive=True)
s = sp.symbols("s", positive=True)
J = c / T + w * sp.integrate(q * s ** (a - 1), (s, 0, T)) / T
Tst = (a * c / ((a - 1) * w * q)) ** (1 / a)
ok = True
for al in (1.3, 1.6, 2.0, 2.5, 2.9):
    vals = {c: 0.7, w: 2.0, q: 0.3, a: al}
    f = sp.lambdify(T, J.subs(vals))
    r = minimize_scalar(f, bounds=(1e-6, 1e3), method="bounded", options={"xatol": 1e-12})
    ok &= abs(r.x - float(Tst.subs(vals))) < 1e-5 * float(Tst.subs(vals))
el = [sp.simplify(sp.diff(sp.log(1 / Tst), v) * v) for v in (w, q, c)]
ok &= el == [1 / a, 1 / a, -1 / a]
check("CT12 read rate (wq/c)^(1/alpha) from J(T)=c/T+wqT^(alpha-1)/alpha", ok, "elasticities %s" % el)

# --- CT13 / M3 robustness: same restriction, interval off by k
k = sp.symbols("k", positive=True)
pen = sp.simplify(J.subs(T, k * Tst) / J.subs(T, Tst))
ok = all(abs(float(pen.subs({a: al, k: 2.0, c: 1, w: 1, q: 1})) - ((al - 1) / 2.0 + 2.0 ** (al - 1)) / al) < 1e-9
         for al in (1.3, 2.0, 2.7))
ok &= sp.simplify(pen.subs(a, 2) - (k + 1 / k) / 2) == 0
check("CT13 interval-error penalty [(alpha-1)/k + k^(alpha-1)]/alpha", ok)

# --- CT4 / P3 first bit must pay: only kappa*I_mem + w*E, Gaussian E = a^2 Var 2^(-2I) (I in bits)
I, kap, A2V = sp.symbols("I kappa V", positive=True)
Jp = kap * I + A2V * 2 ** (-2 * I)
slope0 = sp.diff(Jp, I).subs(I, 0)
dJp = sp.lambdify((I, kap, A2V), sp.diff(Jp, I))
ok = True
for kv, vv in ((0.1, 1.0), (0.5, 3.0), (2.0, 7.0)):
    sub = {kap: kv, A2V: vv}
    ok &= abs(float(slope0.subs(sub)) - (kv - 2 * math.log(2) * vv)) < 1e-12
    ok &= abs(brentq(lambda i: dJp(i, kv, vv), 0, 50) - 0.5 * math.log2(2 * math.log(2) * vv / kv)) < 1e-12
check("CT4 carry a model iff kappa < 2 ln2 a^2 Var; I* = 1/2 log2(2 ln2 a^2 Var/kappa)", ok)

# --- CT7 floor: A priced per nat acquired at lambda >= kT; random walk sigma^2; it is a BOUND, not a solution
D, sig, lam = sp.symbols("D sigma lambda", positive=True)
Jn = lam * sig ** 2 / (2 * D) + w * D
Dst = sp.solve(sp.diff(Jn, D), D)[0]
ok = sp.simplify(Jn.subs(D, Dst) - sig * sp.sqrt(2 * lam * w)) == 0
check("CT7 floor sigma*sqrt(2 lambda w), lambda >= kT (inequality on the acquisition price)", ok)

# --- CT21 (L1-L3): kappa=L=0, A fixed by sensing noise N -> J_K = hK + w E_K
A1, V1, N1 = [0.3], [1.0], 0.1
e_inf, e1 = E_inf(A1, V1, N1), E_K(A1, V1, N1, 1)[0]
check("L1 one pole -> one layer exact (E_1 = E_inf)", abs(e1 / e_inf - 1) < 1e-4, "E_1/E_inf-1=%.2e" % (e1 / e_inf - 1))
A2, V2, N2 = [1.0, 0.1], [0.5, 0.5], 0.1
e_inf, e1, e2 = E_inf(A2, V2, N2), E_K(A2, V2, N2, 1)[0], E_K(A2, V2, N2, 2)[0]
d1 = e1 / e_inf - 1
ok = d1 > 1e-3 and abs(e2 / e_inf - 1) < 1e-4
Rstar = 1 / d1
ks = []
for R in (1, 10, 30, 100, 300, 1000):
    ww = R / e_inf
    ks.append(1 if 1 + ww * e1 <= 2 + ww * e2 else 2)
ok &= ks == sorted(ks) and ks[0] == 1 and ks[-1] == 2
ok &= all((K == 2) == (R > Rstar) for R, K in zip((1, 10, 30, 100, 300, 1000), ks))
check("L2 two modes -> two layers exact; K* switches 1->2 at R* = 1/Delta_1; K* nondecreasing in w/h", ok,
      "Delta_1=%.3f%% R*=%.1f K*=%s" % (100 * d1, Rstar, ks))
Af, Vf = 1 / np.logspace(0, 3, 13), np.ones(13) / 13
e_inf3 = E_inf(Af, Vf, 0.01)
eks = [E_K(Af, Vf, 0.01, K, starts=4)[0] for K in (1, 2, 3)]
ok = eks[0] > eks[1] > eks[2] > e_inf3 * (1 + 1e-6)
check("L3 continuum (dense mixture) -> E_K strictly above E_inf and falling with K", ok,
      "E_K/E_inf-1 = %s" % ["%.4f" % (e / e_inf3 - 1) for e in eks])

# --- Result 4 / B2: L = 0 (h = 0), pooled stakes, sqrt rule. Shared level iff N > N*(rho)
def gain(N, rho, cc=1.0, ww=1.0, qu=1.0):
    qg = rho * qu
    local = N * math.sqrt(2 * cc * ww * (qg + qu))
    shared = math.sqrt(2 * cc * N * ww * qg) + N * math.sqrt(2 * cc * ww * qu)
    return local - shared
ok = True
for rho in (0.05, 0.3, 1.0, 3.0):
    Nst = (math.sqrt(1 + rho) + 1) ** 2 / rho
    ok &= abs(brentq(lambda n: gain(n, rho), 1e-6, 1e9) - Nst) < 1e-6 * Nst
check("Result 4 onset N* = (sqrt(1+rho)+1)^2/rho from J with pooled stakes", ok)

# --- CT16 telling price: L = N*d per read of the shared driver
def gain_d(N, rho, t, ww=1.0, qu=1.0):
    qg = rho * qu
    return N * math.sqrt(2 * ww * (qg + qu)) - math.sqrt(2 * (1 + N * t) * N * ww * qg) - N * math.sqrt(2 * ww * qu)
ok = True
for rho, N in ((0.5, 40.0), (1.0, 20.0), (2.0, 100.0)):
    tcrit = 1 / ((math.sqrt(1 + rho) + 1) ** 2 / rho) - 1 / N
    ok &= gain_d(N, rho, tcrit * 0.99) > 0 > gain_d(N, rho, tcrit * 1.01)
check("CT16 telling price: sharing pays iff d/c < 1/N*(rho) - 1/N", ok)

# --- B12 broadcast break (formal Thm 2b): per-read broadcast c_b, level pays for some N iff rho > 4t/(1-t)^2
ok = True
for t in (0.01, 0.1, 0.4):
    rb = 4 * t / (1 - t) ** 2
    lim = lambda rho: math.sqrt(1 + rho) - math.sqrt(t * rho) - 1
    ok &= lim(rb * 1.02) > 0 > lim(rb * 0.98)
check("B12 broadcast threshold rho_b = 4t/(1-t)^2", ok)

# --- CT19 LAT-1: E evaluated at latency l is at least q l^(alpha-1) -> L_max = v (D*/q)^(1/(alpha-1))
L_, v, Ds = sp.symbols("L v Dstar", positive=True)
Lmax = sp.solve(sp.Eq(q * (L_ / v) ** (a - 1), Ds), L_)
ok = len(Lmax) == 1 and sp.simplify(Lmax[0] - v * (Ds / q) ** (1 / (a - 1))) == 0
check("CT19 LAT-1 reach L_max = v (D*/q)^(1/(alpha-1))", ok)

# --- CT17 one clock for several parts (Gorman): equality iff c_i/(w_i sigma_i^2) equal
def one_clock(cs, ws):
    return 2 * math.sqrt(sum(cs) * sum(ws) / 2)
def own(cs, ws):
    return sum(2 * math.sqrt(ci * wi / 2) for ci, wi in zip(cs, ws))
ok = abs(one_clock([1, 2], [3, 6]) - own([1, 2], [3, 6])) < 1e-12 and one_clock([1, 2], [6, 3]) > own([1, 2], [6, 3])
check("CT17 one clock >= separate clocks, equality iff c_i/(w_i sigma_i^2) equal", ok)

# --- CT22 survival lemma and CL2 Theorem L: ruin constraint via Lundberg theta(tau) >= ln(1/eps)/B
y, cc, ww, sg, s0, eps = 1.0, 0.05, 1.0, 1.0, 0.3, 1e-3
m = lambda t: y - cc / t - ww * sg ** 2 * t / 2
th = lambda t, s0=s0: 2 * m(t) / (s0 ** 2 + ww ** 2 * sg ** 4 * t ** 3 / 3)
tE = math.sqrt(2 * cc / (ww * sg ** 2))
tS = minimize_scalar(lambda t: -th(t), bounds=(1e-3, 3), method="bounded").x
Bmin, Bslack = math.log(1 / eps) / th(tS), math.log(1 / eps) / th(tE)
def tau_star(B):
    tmin = math.log(1 / eps) / B
    if tmin > th(tS): return None
    if th(tE) >= tmin: return tE
    return brentq(lambda t: th(t) - tmin, tS, tE)
taus = [tau_star(B) for B in (0.49, 0.5, 0.505, 0.6, 5.0)]
ok = tau_star(0.48) is None and abs(Bmin - 0.4864) < 1e-3 and abs(Bslack - 0.5079) < 1e-3
ok &= all(x is not None for x in taus) and taus == sorted(taus) and abs(taus[-1] - tE) < 1e-12 and taus[0] > tS
check("CT22 survival: infeasible below B_min, binding between, slack (EOQ, mu_s=0) above B_slack", ok,
      "B_min=%.4f B_slack=%.4f tau*=%s" % (Bmin, Bslack, ["%.4f" % x for x in taus]))
tS_big = minimize_scalar(lambda t: -th(t, 3.0), bounds=(1e-3, 3), method="bounded").x
ok = tS < tE and abs(tS_big - tE) < 0.01 * tE
check("CL2 Theorem L: survival-optimal interval < EOQ, independent of B; -> EOQ when reserve noise dominates", ok,
      "tau_S=%.4f (s0=0.3), %.4f (s0=3), EOQ=%.4f" % (tS, tS_big, tE))

# --- CT23 local regret: picture error is second order (one layer, drift misjudged by m)
def regret(m_, al):
    return ((al - 1) * m_ ** (-1 / al) + m_ ** ((al - 1) / al)) / al - 1
ok = True
for al in (1.3, 2.0, 2.7):
    for m_ in (1.01, 1.1):
        approx = (al - 1) * math.log(m_) ** 2 / (2 * al ** 2)
        ok &= abs(regret(m_, al) / approx - 1) < 0.1
ok &= 0.03 < regret(2, 1.3) < 0.07 and 0.055 < regret(2, 2.0) < 0.07
check("CT23 regret of a drift picture off by m is (alpha-1)(ln m)^2/(2 alpha^2) + o", ok,
      "2x error: %.1f%% (alpha=1.3), %.1f%% (alpha=2)" % (100 * regret(2, 1.3), 100 * regret(2, 2.0)))

# --- N55 scatter: relative curvature of J in ln T at the optimum is alpha - 1
x = sp.symbols("x")
curv = sp.simplify(sp.diff(J.subs(T, Tst * sp.exp(x)), x, 2).subs(x, 0) / J.subs(T, Tst))
ok = all(abs(float(curv.subs({a: al, c: 0.7, w: 2.0, q: 0.3})) - (al - 1)) < 1e-9 for al in (1.2, 1.5, 2.0, 2.8))
check("N55 relative curvature of J in ln T at the optimum = alpha - 1", ok)

nf = sum(not ok for _, ok in results)
print("\n%d checks, %d FAIL" % (len(results), nf))
print("RESULT:", "PASS" if nf == 0 else "FAIL")
sys.exit(1 if nf else 0)
