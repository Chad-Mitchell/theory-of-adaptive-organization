#!/usr/bin/env python3
"""Checks for the closed forms in THEORY.md v2.0 Appendix B (CT1-CT19 and lemmas).

Symbolic identities are checked with sympy; inequalities and optima against brute-force
numerical minimization at random parameter draws (fixed seed). Prints one line per check
and 'ALL OK' at the end; exit code 0 iff every check passes. Runtime: a few seconds.
These are the authors' own checks (same bot family), not an independent review."""
import math, sys
import numpy as np
import sympy as sp
from scipy.optimize import minimize_scalar

rng = np.random.default_rng(20261119)
results = []

def check(name, ok, detail=""):
    results.append(bool(ok))
    print("%-4s %s %s" % ("OK" if ok else "FAIL", name, detail))

def argmin_pos(f, lo=1e-8, hi=1e8):
    r = minimize_scalar(lambda lx: f(math.exp(lx)), bounds=(math.log(lo), math.log(hi)), method="bounded",
                        options={"xatol": 1e-12})
    return math.exp(r.x), r.fun

# CT4 (P3, Gaussian AR(1)): loss(I) = Var[(1-a^2) + a^2 2^{-2I}], plus kappa*I
a, V, k, I = sp.symbols("a V kappa I", positive=True)
loss = V * ((1 - a**2) + a**2 * 2**(-2 * I)) + k * I
d0 = sp.diff(loss, I).subs(I, 0)
check("CT4 first-bit threshold", sp.simplify(d0 - (k - 2 * sp.log(2) * a**2 * V)) == 0)
Istar = sp.Rational(1, 2) * sp.log(2 * sp.log(2) * a**2 * V / k, 2)
check("CT4 optimum I*", sp.simplify(sp.diff(loss, I).subs(I, Istar)) == 0)

# CT7 (O1): J = kT s^2/(2D) + w D  ->  J* = s sqrt(2 kT w)
s_, kT, w, D = sp.symbols("sigma kT w D", positive=True)
J = kT * s_**2 / (2 * D) + w * D
Dst = sp.solve(sp.diff(J, D), D)[0]
check("CT7 tracking floor J* = sigma sqrt(2 kT w)", sp.simplify(J.subs(D, Dst) - s_ * sp.sqrt(2 * kT * w)) == 0)

# CT9 (G2): two-state chain, flip rate 1 each way, 0-1 loss: r(u) = (1 - e^{-2u})/2, r_inf = 1/2, Phi = 1/4
u = sp.symbols("u", positive=True)
Phi = sp.integrate(sp.Rational(1, 2) - (1 - sp.exp(-2 * u)) / 2, (u, 0, sp.oo))
check("CT9 Phi for the two-state chain", Phi == sp.Rational(1, 4))
c_chk = 0.05  # lambda_c = Phi / c = 5
def best_hold(lam):
    A = lambda s: (0.5 - (1 - math.exp(-2 * s)) / (4 * s))  # (1/s) int_0^s r
    f = lambda s: lam * c_chk / s + A(s)
    return argmin_pos(f, 1e-6, 1e6)[1]
check("CT9 holds below lambda_c", best_hold(4.9) < 0.5 - 1e-6)
check("CT9 fades above lambda_c", best_hold(5.1) >= 0.5 - 1e-9)

# CT11 (T8): edges, band condition, N^2 widening
bad = 0
for _ in range(2000):
    W, q_, c, h, mu, uu, tl = rng.uniform(0.1, 10, 7)
    if mu * uu <= h:
        continue
    qf = 2 * c / (W * tl**2); qc = (mu * uu - h)**2 / (2 * c * W)
    band = qf < qc
    if band != (mu * uu * tl > 2 * c + h * tl):
        bad += 1
    # freeze edge: interior optimum T* = sqrt(2c/(Wq)) >= tl iff q <= qf
    if (math.sqrt(2 * c / (W * q_)) >= tl) != (q_ <= qf):
        bad += 1
    # lookup edge: sqrt(2cWq)+h > mu u iff q > qc
    if (math.sqrt(2 * c * W * q_) + h > mu * uu) != (q_ > qc):
        bad += 1
check("CT11 T8 edges and band condition", bad == 0, "(%d mismatches)" % bad)
Wn, cn, mun, un, Ns = sp.symbols("W c mu u N", positive=True)
qf1 = 2 * cn / (Wn); qc1 = (mun * un)**2 / (2 * cn * Wn)          # tl = 1, h = 0
qfN = 2 * cn / (Ns * Wn); qcN = (Ns * mun * un)**2 / (2 * cn * Ns * Wn)
check("CT11 shared store widens the band by N^2", sp.simplify((qcN / qfN) / (qc1 / qf1) - Ns**2) == 0)

# CT12 (read-rate rule): J(T) = c/T + w q T^{al-1}/al, optimum rate ~ (wq/c)^{1/al}
bad = 0
for _ in range(300):
    al = rng.uniform(1.1, 2.9); c, w_, q_ = rng.uniform(0.1, 10, 3)
    f = lambda T: c / T + w_ * q_ * T**(al - 1) / al
    T_num, _ = argmin_pos(f)
    T_cf = (al * c / ((al - 1) * w_ * q_))**(1 / al)
    bad += abs(T_num / T_cf - 1) > 1e-4
check("CT12 read interval closed form", bad == 0, "(%d mismatches)" % bad)
# cost exponents a = b = 1/al
al_ = 2.4; c, w_, q_ = 1.3, 0.7, 2.1
Jst = lambda c, w_, q_: argmin_pos(lambda T: c / T + w_ * q_ * T**(al_ - 1) / al_)[1]
ea = math.log(Jst(c, 2 * w_, q_) / Jst(c, w_, q_)) / math.log(2)
eb = math.log(Jst(c, w_, 2 * q_) / Jst(c, w_, q_)) / math.log(2)
check("CT12 a = b = 1/alpha", abs(ea - 1 / al_) < 1e-6 and abs(eb - 1 / al_) < 1e-6, "(a=%.6f b=%.6f 1/al=%.6f)" % (ea, eb, 1 / al_))
# periodic reading optimal: convexity of T^al (Jensen) is assumed in the proof; spot-check unequal gaps
gaps = np.array([0.5, 1.5]); check("CT12 equal gaps beat unequal (al=2.4)", (gaps**al_).sum() > 2 * (gaps.mean())**al_)

# CT13 (robustness): J(kT*)/J* = ((al-1)/k + k^{al-1})/al ; at al=2, (k+1/k)/2 ; inputs off by m -> k = sqrt(m)
bad = 0
for _ in range(200):
    al = rng.uniform(1.1, 2.9); c, w_, q_ = rng.uniform(0.1, 10, 3); kk = rng.uniform(0.2, 5)
    f = lambda T: c / T + w_ * q_ * T**(al - 1) / al
    Ts, Js = argmin_pos(f)
    bad += abs(f(kk * Ts) / Js - ((al - 1) / kk + kk**(al - 1)) / al) > 1e-6
check("CT13 robustness formula", bad == 0)
r2 = (math.sqrt(2) + 1 / math.sqrt(2)) / 2 - 1; r10 = (math.sqrt(10) + 1 / math.sqrt(10)) / 2 - 1
check("CT13 +6% at m=2, +74% at m=10", round(r2, 2) == 0.06 and round(r10, 2) == 0.74, "(%.4f, %.4f)" % (r2, r10))

# CT14 (pooling onset): G(N) = N[(1+rho)^b - 1] - N^a rho^b; root N* ; T3a identity at a=b=1/2; small-rho exponent
rho, aa, bb = sp.symbols("rho a b", positive=True)
Nst = (rho**bb / ((1 + rho)**bb - 1))**(1 / (1 - aa))
t3a = Nst.subs({aa: sp.Rational(1, 2), bb: sp.Rational(1, 2)})
check("CT14 T3a identity at a=b=1/2", sp.simplify(t3a - (sp.sqrt(1 + rho) + 1)**2 / rho) == 0)
bad = 0
for _ in range(300):
    a_ = rng.uniform(0, 0.95); b_ = rng.uniform(0.05, 0.95); r_ = 10**rng.uniform(-3, 2)
    Ns_ = (r_**b_ / ((1 + r_)**b_ - 1))**(1 / (1 - a_))
    G = lambda N: N * ((1 + r_)**b_ - 1) - N**a_ * r_**b_
    bad += not (G(Ns_ * 0.999) < 0 < G(Ns_ * 1.001))
check("CT14 single crossing at N*", bad == 0, "(%d mismatches)" % bad)
for a_, b_ in [(0.5, 0.5), (2 / 3, 1 / 3), (0.5, 0.25), (0.8, 0.2)]:
    r1, r2_ = 1e-6, 1e-7
    N1 = (r1**b_ / ((1 + r1)**b_ - 1))**(1 / (1 - a_)); N2 = (r2_**b_ / ((1 + r2_)**b_ - 1))**(1 / (1 - a_))
    e = math.log(N1 / N2) / math.log(r1 / r2_)
    check("CT14 small-rho exponent (a,b)=(%.3f,%.3f)" % (a_, b_), abs(e + (1 - b_) / (1 - a_)) < 1e-4, "(e=%.5f)" % e)

# CT15 (N12): priced precision a = al*th/(al(th+1)-1), b = th/(al(th+1)-1): (1-b)/(1-a) = 1+th for every al
al, th = sp.symbols("alpha theta", positive=True)
A_ = al * th / (al * (th + 1) - 1); B_ = th / (al * (th + 1) - 1)
check("CT15 precision class exponent 1+theta, alpha-free", sp.simplify((1 - B_) / (1 - A_) - (1 + th)) == 0)
check("CT15 reset class exponent 1", sp.simplify((1 - 1 / al) / (1 - 1 / al) - 1) == 0)
# the precision-class (a, b) follow from minimizing W q^{1/al} r^{(al-1)/al} + c' r^{-th} over r
bad = 0
for _ in range(100):
    alv = rng.uniform(1.2, 2.8); thv = rng.uniform(0.3, 3); cp = rng.uniform(0.5, 2)
    Jp = lambda W, q: argmin_pos(lambda r: W * q**(1 / alv) * r**((alv - 1) / alv) + cp * r**(-thv), 1e-12, 1e12)[1]
    ea = math.log(Jp(2.0, 1.0) / Jp(1.0, 1.0)) / math.log(2); eb = math.log(Jp(1.0, 2.0) / Jp(1.0, 1.0)) / math.log(2)
    a_cf = alv * thv / (alv * (thv + 1) - 1); b_cf = thv / (alv * (thv + 1) - 1)
    bad += abs(ea - a_cf) > 1e-5 or abs(eb - b_cf) > 1e-5
check("CT15 precision-class (a, b) from the minimization", bad == 0, "(%d mismatches)" % bad)

# CT16 (telling price): hybrid sqrt(2(c+Nd)N w qg) + N sqrt(2 c w qu) < N sqrt(2 c w (qg+qu)) iff d/c < 1/N*(rho) - 1/N
bad = 0
for _ in range(5000):
    c, d, w_, qg, qu = rng.uniform(0.01, 5, 5); N = int(rng.integers(1, 400))
    hyb = math.sqrt(2 * (c + N * d) * N * w_ * qg) + N * math.sqrt(2 * c * w_ * qu)
    loc = N * math.sqrt(2 * c * w_ * (qg + qu))
    r_ = qg / qu; Nst_ = (math.sqrt(1 + r_) + 1)**2 / r_
    lhs = hyb < loc; rhs = d / c < 1 / Nst_ - 1 / N
    if abs((d / c) - (1 / Nst_ - 1 / N)) > 1e-9:
        bad += lhs != rhs
check("CT16 telling-price rule", bad == 0, "(%d mismatches in 5000)" % bad)

# CT17 (Gorman/externality): aggregate clock >= sum of separate optima, equality iff c_i/(w_i s_i^2) equal
bad = 0
for _ in range(2000):
    K = int(rng.integers(2, 6)); c = rng.uniform(0.1, 5, K); w_ = rng.uniform(0.1, 5, K); s2 = rng.uniform(0.1, 5, K)
    sep = np.sum(np.sqrt(2 * c * w_ * s2)); agg = math.sqrt(2 * c.sum() * (w_ * s2).sum())
    bad += agg < sep * (1 - 1e-12)
check("CT17 aggregate clock never cheaper", bad == 0)
c = np.array([1.0, 2.0, 4.0]); ws2 = 3.0 * c
check("CT17 equality when c_i/(w_i s_i^2) is equal", abs(math.sqrt(2 * c.sum() * ws2.sum()) - np.sum(np.sqrt(2 * c * ws2))) < 1e-12)
check("CT17 relatedness r=3/4 at alpha=2 under-watches by ~13%", round(1 - math.sqrt(0.75), 2) == 0.13)

# CT18 (temperature identity): h = F(z)/tau, z = B/(sigma sqrt(tau))
B_, sg, ta = sp.symbols("B sigma tau", positive=True); Fz = sp.Function("F")
h = Fz(B_ / (sg * sp.sqrt(ta))) / ta
el = lambda X: sp.simplify(sp.diff(sp.log(h), X) * X)
check("CT18 eps_B = -eps_sigma", sp.simplify(el(B_) + el(sg)) == 0)
check("CT18 eps_tau = eps_sigma/2 - 1", sp.simplify(el(ta) - (el(sg) / 2 - 1)) == 0)
sobs = sp.symbols("s", positive=True)
h_fixed = (Fz(B_ / sobs) / ta)
check("CT18 eps_tau = -1 at fixed observed spread", sp.simplify(sp.diff(sp.log(h_fixed), ta) * ta + 1) == 0)
# CL4: one-sided per-window first passage for Brownian motion = erfc(z/sqrt 2) (reflection); Monte Carlo
zz = 1.2; n, steps = 20000, 2000; dt = 1.0 / steps
X = np.zeros(n); hit = np.zeros(n, bool); sd = 1.0 / zz  # B = 1, sigma sqrt(tau) = 1/z
rng2 = np.random.default_rng(7)
for _ in range(steps):
    X += rng2.normal(0, sd * math.sqrt(dt), n); hit |= X >= 1.0
p_mc = hit.mean(); p_ex = math.erfc(zz / math.sqrt(2))
check("CL4 per-window ruin erfc(z/sqrt2) (MC, discrete monitoring biases low)", p_ex - 0.03 < p_mc <= p_ex + 0.01, "(MC %.4f vs exact %.4f)" % (p_mc, p_ex))

# CT19 (LAT-1): mean error over a read cycle with latency l is >= q l^{al-1} and tends to it as T -> 0
bad = 0
for _ in range(500):
    al = rng.uniform(1.1, 2.9); q_ = rng.uniform(0.1, 5); l = rng.uniform(0.01, 3); T = rng.uniform(1e-4, 3)
    ss = np.linspace(0, T, 2001); mean_err = np.trapezoid(q_ * (l + ss)**(al - 1), ss) / T
    bad += mean_err < q_ * l**(al - 1) * (1 - 1e-12)
check("CT19 latency floor q l^(al-1)", bad == 0)
Ds, qv, alv, v = 0.5, 2.0, 1.7, 3.0
Lmax = v * (Ds / qv)**(1 / (alv - 1)); check("CT19 L_max inverts the floor", abs(qv * (Lmax / v)**(alv - 1) - Ds) < 1e-12)

print("ALL OK" if all(results) else "SOME FAILED", "(%d checks)" % len(results))
sys.exit(0 if all(results) else 1)
