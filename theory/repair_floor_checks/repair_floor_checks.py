#!/usr/bin/env python3
"""Checks for theory/RECORD_REPAIR_FLOOR_2026-11-23.md (OPEN_WORK T63).

Code identities and worked evaluations in the classes named in the note.
A green run is not a proof, and nothing here is evidence about a real system.
Run from anywhere:  nice -n 19 python3 theory/repair_floor_checks/repair_floor_checks.py
"""
from __future__ import annotations

import itertools
import math
import os
import sys

import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.special import logsumexp, softmax

FAILS = 0
CHECKS = 0


def check(name, ok, detail=""):
    global FAILS, CHECKS
    CHECKS += 1
    if not ok:
        FAILS += 1
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  [" + detail + "]") if detail else ""))


def h(e):
    return -e * math.log(e) - (1 - e) * math.log(1 - e)


def L(e):
    return (1 - 2 * e) * math.log((1 - e) / e)


def kl(a, q):
    return a * math.log(a / q) + (1 - a) * math.log((1 - a) / (1 - q))


def floor4(e):
    """General lower bound on g(eps) for independent symmetric carriers: 4(ln2 - h(eps))."""
    return 4 * (math.log(2) - h(e))


# ---------------------------------------------------------------- hypercube tools
def hypercube_sigma(p, rates):
    """Entropy production (nats/time) of symmetric independent flips on {0,1}^n.
    p: array of length 2^n indexed by bit pattern; rates[i]: flip rate of carrier i."""
    n = len(rates)
    s = 0.0
    for x in range(2 ** n):
        for i in range(n):
            y = x ^ (1 << i)
            if y > x:
                a, b = p[x], p[y]
                s += rates[i] * (a - b) * math.log(a / b)
    return s


def rel_ent_uniform(p):
    n2 = len(p)
    return float(np.sum(p * np.log(p * n2)))


# ---------------------------------------------------------------- 1. basic numbers
print("== 1. basic numbers")
check("L(0.2) = 0.6 ln 4 = 0.831776616672 (T59/T60 telegraph number)", abs(L(0.2) - 0.6 * math.log(4)) < 1e-12,
      "%.12f" % L(0.2))
check("ln2 - h(0.2) = 0.192744757022 (T62 binary stock)", abs(math.log(2) - h(0.2) - 0.192744757022) < 1e-12)
check("4(ln2 - h(0.2)) = 0.770979028088", abs(floor4(0.2) - 0.770979028088) < 1e-11, "%.12f" % floor4(0.2))
check("4(ln2 - h(1e-9)) = 2.772588635 (tends to 4 ln 2 = 2.772588722)",
      abs(floor4(1e-9) - 2.772588635) < 1e-8 and abs(4 * math.log(2) - 2.772588722) < 1e-9, "%.9f" % floor4(1e-9))

# ---------------------------------------------------------------- 2. single-carrier MLSI
print("== 2. single carrier: sigma = Gamma L(eps) and sigma >= 4 Gamma (ln2 - h)")
G = 0.37
ok = True
for e in np.linspace(1e-6, 0.5 - 1e-6, 2001):
    p = np.array([1 - e, e])
    sig = hypercube_sigma(p, [G])
    if abs(sig - G * L(e)) > 1e-9 * max(1, sig):
        ok = False
check("one carrier at error eps: leak entropy production = Gamma L(eps) (grid of 2001)", ok)
ratios = [L(e) / (math.log(2) - h(e)) for e in np.linspace(1e-6, 0.5 - 1e-4, 4001)]
check("one carrier: L(eps) / (ln2 - h(eps)) >= 4 on the grid", min(ratios) >= 4 - 1e-9, "min %.9f" % min(ratios))
x = 1e-3
e = (1 - x) / 2
check("ratio tends to 4 as eps -> 1/2 (x = 1 - 2 eps = 1e-3)", abs(L(e) / (math.log(2) - h(e)) - 4) < 1e-5,
      "%.9f" % (L(e) / (math.log(2) - h(e))))
# termwise series: LHS coeff of x^(2k): 2/(2k-1); RHS: 2/(k(2k-1))
ok = all(2 / (2 * k - 1) >= 2 / (k * (2 * k - 1)) for k in range(1, 200))
check("series: 2/(2k-1) >= 2/(k(2k-1)) for every k >= 1, equality only at k = 1", ok)
x = 0.3
lhs = x * math.log((1 + x) / (1 - x))
rhs = (1 + x) * math.log(1 + x) + (1 - x) * math.log(1 - x)
check("change of variables x = 1 - 2 eps: L = x ln((1+x)/(1-x)), 4(ln2-h) = 2[(1+x)ln(1+x)+(1-x)ln(1-x)]",
      abs(lhs - L(0.35)) < 1e-12 and abs(2 * rhs - floor4(0.35)) < 1e-12)

# ---------------------------------------------------------------- 3. tensorized MLSI on hypercubes
print("== 3. tensorization: sigma(p) >= 4 Gamma_min D(p || uniform) on {0,1}^n")
rng = np.random.default_rng(20261123)
ok = True
worst = 1e9
for n in range(1, 6):
    for trial in range(300):
        rates = list(G * (1 + rng.exponential(1.0, n)))
        rates[0] = G
        conc = rng.choice([0.05, 0.3, 1.0, 5.0])
        p = rng.dirichlet(conc * np.ones(2 ** n))
        p = np.maximum(p, 1e-300)
        p /= p.sum()
        sig = hypercube_sigma(p, rates)
        d = rel_ent_uniform(p)
        if d > 1e-12:
            worst = min(worst, sig / (4 * G * d))
        if sig < 4 * G * d - 1e-9:
            ok = False
check("1500 random distributions, n = 1..5, rates >= Gamma: sigma >= 4 Gamma D", ok, "min ratio %.6f" % worst)

# ---------------------------------------------------------------- 4. log-sum (marginalizing a controller)
print("== 4. coarse-graining a controller only lowers the leak entropy production")
ok = True
for trial in range(500):
    ny = int(rng.integers(1, 6))
    a = rng.exponential(1.0, ny)
    b = rng.exponential(1.0, ny)
    joint = float(np.sum((a - b) * np.log(a / b)))
    A, B = a.sum(), b.sum()
    marg = (A - B) * math.log(A / B)
    if joint < marg - 1e-12:
        ok = False
check("sum_y (a_y - b_y) ln(a_y/b_y) >= (A - B) ln(A/B), 500 random cases", ok)

# ---------------------------------------------------------------- 5. pair bound, any decoder
print("== 5. any code, any decoder: average over b of sigma >= 4 Gamma (ln2 - h(eps))")
ok = True
for n in range(1, 5):
    states = 2 ** n
    for trial in range(400):
        Dmask = rng.random(states) < rng.uniform(0.1, 0.9)
        if Dmask.all() or (~Dmask).all():
            continue
        p0 = rng.dirichlet(rng.choice([0.1, 1.0]) * np.ones(states))
        p1 = rng.dirichlet(rng.choice([0.1, 1.0]) * np.ones(states))
        # push mass into the correct decoding sets
        p0 = np.maximum(np.where(Dmask, p0 * 20, p0), 1e-300)
        p0 /= p0.sum()
        p1 = np.maximum(np.where(~Dmask, p1 * 20, p1), 1e-300)
        p1 /= p1.sum()
        e0 = p0[~Dmask].sum()
        e1 = p1[Dmask].sum()
        eps = max(e0, e1)
        if eps >= 0.5:
            continue
        avg = 0.5 * (hypercube_sigma(p0, [G] * n) + hypercube_sigma(p1, [G] * n))
        if avg < G * floor4(eps) - 1e-9:
            ok = False
check("random codes and decoders, n = 1..4: (sigma_0 + sigma_1)/2 >= Gamma * 4(ln2 - h(eps))", ok)
# the decoder-mass minimization: min over delta of F1 + F2 = 2(ln2 - h)
for eps in [0.2, 0.01]:
    def F(d, eps=eps):
        f1 = kl(1 - eps, d) if d <= 1 - eps else 0.0
        f2 = kl(1 - eps, 1 - d) if 1 - d <= 1 - eps else 0.0
        return f1 + f2
    grid = np.linspace(1e-6, 1 - 1e-6, 200001)
    m = min(F(d) for d in grid)
    check("min over decoder mass delta of F1+F2 = 2(ln2 - h(eps)) at eps = %g" % eps,
          abs(m - 2 * (math.log(2) - h(eps))) < 1e-8, "%.10f" % m)
check("kl(1-eps||eps) = L(eps) >= 2 kl(1-eps||1/2) at eps = 0.2", abs(kl(0.8, 0.2) - L(0.2)) < 1e-12 and L(0.2) >= 2 * kl(0.8, 0.5))

# ---------------------------------------------------------------- 6. leak entropy production = -dD/dt
print("== 6. symmetric leak: sigma = -dD(p||u)/dt")
n = 3
rates = [G] * n
p = rng.dirichlet(np.ones(2 ** n))
Q = np.zeros((2 ** n, 2 ** n))
for xx in range(2 ** n):
    for i in range(n):
        Q[xx, xx ^ (1 << i)] = rates[i]
    Q[xx, xx] = -sum(rates)
dt = 1e-6
p2 = p + dt * (p @ Q)
dDdt = (rel_ent_uniform(p2) - rel_ent_uniform(p)) / dt
check("finite-difference -dD/dt matches sigma (n = 3)", abs(-dDdt - hypercube_sigma(p, rates)) < 1e-5,
      "%.8f vs %.8f" % (-dDdt, hypercube_sigma(p, rates)))

# ---------------------------------------------------------------- 7. rho <= 2 * gap
print("== 7. modified log-Sobolev constant <= 2 x spectral gap (near-equilibrium expansion)")
ok = True
for trial in range(50):
    k = int(rng.integers(2, 7))
    pi = rng.dirichlet(np.ones(k))
    S = rng.exponential(1.0, (k, k))
    S = (S + S.T) / 2
    np.fill_diagonal(S, 0)
    W = S / pi[:, None]  # W[x,y] = S[x,y]/pi[x]: reversible w.r.t. pi
    Qm = W.copy()
    np.fill_diagonal(Qm, -W.sum(1))
    Dh = np.diag(np.sqrt(pi))
    Dhi = np.diag(1 / np.sqrt(pi))
    Ssym = Dh @ Qm @ Dhi
    Ssym = (Ssym + Ssym.T) / 2
    ev, evec = np.linalg.eigh(Ssym)
    gap = -ev[-2]
    f = Dhi @ evec[:, -2]
    eta = 1e-4
    pp = pi * (1 + eta * f / np.max(np.abs(f)))
    sig = 0.0
    for a_ in range(k):
        for b_ in range(a_ + 1, k):
            ja, jb = pp[a_] * W[a_, b_], pp[b_] * W[b_, a_]
            sig += (ja - jb) * math.log(ja / jb)
    Dkl = float(np.sum(pp * np.log(pp / pi)))
    if abs(sig / Dkl - 2 * gap) > 1e-3 * 2 * gap:
        ok = False
check("50 random reversible chains: sigma/D along the gap mode -> 2 * gap, so rho <= 2 * gap", ok)

# ---------------------------------------------------------------- 8. finite b-blind fully leaky schemes forget
print("== 8. a finite, irreducible, b-blind scheme has one stationary state (the record is lost)")
n = 3
k_fix = 50.0
Qc = np.zeros((2 ** n, 2 ** n))
for xx in range(2 ** n):
    w = bin(xx).count("1")
    for i in range(n):
        y = xx ^ (1 << i)
        Qc[xx, y] += G  # leak
        bit = (xx >> i) & 1
        majority = 1 if w >= 2 else 0
        if bit != majority:
            Qc[xx, y] += k_fix  # b-blind corrector: flip a minority bit toward the majority
    Qc[xx, xx] = -Qc[xx].sum()
ev = np.sort(np.real(np.linalg.eigvals(Qc)))[::-1]
check("majority corrector on 3 leaky carriers: exactly one zero eigenvalue", abs(ev[0]) < 1e-9 and ev[1] < -1e-9,
      "second eigenvalue %.6e" % ev[1])
from scipy.linalg import expm
P0 = np.zeros(2 ** n); P0[0] = 1
P1 = np.zeros(2 ** n); P1[-1] = 1
T = 2000.0 / G
dec0 = np.array([1.0 if bin(xx).count("1") >= 2 else 0.0 for xx in range(2 ** n)])
e_late = float((P0 @ expm(Qc * T)) @ dec0)
check("logical error after t >> lifetime tends to 1/2", abs(e_late - 0.5) < 1e-3, "%.6f" % e_late)
lifetime = -1 / ev[1]
check("logical lifetime of that scheme is finite (%.3f / Gamma)" % (lifetime * G), lifetime < 1e6)

# ---------------------------------------------------------------- 9. repetition codes: numerical floor
print("== 9. repetition codes, majority decoder: numerical minimum of the leak entropy production")


def rep_floor(n, eps):
    k = (n + 1) // 2
    w = np.arange(n)
    ln_up = np.log(n - w)
    ln_dn = np.log(w + 1)

    def f(z):
        Z = logsumexp(z)
        la = ln_up + z[:-1] - Z
        lb = ln_dn + z[1:] - Z
        d = np.clip(la - lb, -700, 700)
        s = float(np.sum((np.exp(la) - np.exp(lb)) * d))
        dTa = d + 1 - np.exp(-d)
        dTb = -d + 1 - np.exp(d)
        gP = np.zeros(n + 1)
        gP[:-1] += (n - w) * dTa
        gP[1:] += (w + 1) * dTb
        P = np.exp(z - Z)
        return s, P * (gP - np.dot(P, gP))

    def c(z):
        return math.log(eps) - logsumexp(z[k:]) + logsumexp(z)

    def cj(z):
        g = softmax(z).copy()
        t = np.zeros_like(z)
        t[k:] = softmax(z[k:])
        return g - t

    best = None
    for s in [0.5, 1, 2, 4]:
        z0 = -s * np.arange(n + 1) * math.log(1 / eps) / k
        r = minimize(f, z0, jac=True, constraints=[{"type": "ineq", "fun": c, "jac": cj}], method="SLSQP",
                     options={"maxiter": 5000, "ftol": 1e-14})
        if c(r.x) > -1e-7 and (best is None or r.fun < best):
            best = float(r.fun)
    return best


table = {}
with np.errstate(all="ignore"):
    for eps in [0.2, 1e-3, 1e-9]:
        for n in [1, 3, 5, 9, 21, 41]:
            table[(eps, n)] = rep_floor(n, eps)
            print("    eps=%-6g n=%-3d  g_rep=%.4f   4(ln2-h)=%.4f   L=%.4f" % (eps, n, table[(eps, n)], floor4(eps), L(eps)))
check("n = 1 reproduces L(eps) at all three errors",
      all(abs(table[(e, 1)] - L(e)) < 1e-6 for e in [0.2, 1e-3, 1e-9]))
check("every repetition value >= the general bound 4(ln2 - h(eps))",
      all(v >= floor4(e) - 1e-9 for (e, n), v in table.items()))
check("eps = 1e-9: redundancy lowers the floor below L (n = 41 value %.4f < L = %.4f)" % (table[(1e-9, 41)], L(1e-9)),
      table[(1e-9, 41)] < L(1e-9) and table[(1e-9, 41)] < table[(1e-9, 21)] < table[(1e-9, 9)])
check("eps = 0.2: redundancy raises the floor (n = 1 is best among those tried)",
      all(table[(0.2, n)] >= table[(0.2, 1)] - 1e-9 for n in [3, 5, 9, 21, 41]))
check("quoted values: eps=1e-9 n=21 -> 9.2378, n=41 -> 8.8335; eps=1e-3 n=41 -> 6.7153",
      abs(table[(1e-9, 21)] - 9.2378) < 2e-4 and abs(table[(1e-9, 41)] - 8.8335) < 2e-4 and abs(table[(1e-3, 41)] - 6.7153) < 2e-4)
# diffusion-limit heuristic: half-line Dirichlet ground state of the Hermite operator has eigenvalue 1
ys = np.linspace(0, 12, 400001)
phi = np.exp(-ys ** 2 / 2) / math.sqrt(2 * math.pi)
psi2 = 2 * ys ** 2
norm = np.trapezoid(psi2 * phi, ys)
dir_energy = np.trapezoid(2 * phi, ys)  # (psi')^2 = 2
check("diffusion limit: psi = sqrt(2) y on y > 0 is normalized and has relative Fisher information 4 (so 2 Gamma * 4 = 8 Gamma)",
      abs(norm - 1) < 1e-6 and abs(4 * dir_energy - 4) < 1e-6)

# ---------------------------------------------------------------- 10. GTAO minimum of the floor cost
print("== 10. minimum of kT rho (ln2 - h(eps)) + w eps over eps")
for ratio in [2.0, 10.0, 30.0]:
    r = minimize_scalar(lambda e: (math.log(2) - h(e)) + ratio * e, bounds=(1e-15, 0.5), method="bounded",
                        options={"xatol": 1e-14})
    pred = 1 / (1 + math.exp(ratio))
    check("w/(kT rho) = %g: eps* = 1/(1+e^{w/(kT rho)}) = %.6e" % (ratio, pred), abs(r.x - pred) < 1e-6 * max(1, pred / 1e-6) * 1e-3 + 1e-9,
          "numeric %.6e" % r.x)

# ---------------------------------------------------------------- 11. worked transport-limited cap
print("== 11. worked cap: records kept <= q A / (kT * 4 Gamma (ln2 - h(eps)))")
kB = 1.380649e-23
Tk = 300.0
kT = kB * Tk
eV = 1.602176634e-19
nu = 1e12
q = 1e6
rho_c = 1e28
eps = 1e-9
g_low = floor4(eps)
rows = []
for dE in [0.5, 0.75, 1.0, 1.25]:
    Gam = nu * math.exp(-dE * eV / kT)
    per_area = q / (kT * Gam * g_low)
    Rstar = 3 * per_area / rho_c
    rows.append((dE, Gam, per_area, Rstar))
    print("    dE=%.2f eV  Gamma=%.3e /s  lifetime=%.3e s  cap per m^2 of boundary=%.3e  R*=%.3e m" % (dE, Gam, 1 / Gam, per_area, Rstar))
check("dE = 1.0 eV: Gamma = 1.59e-5 /s, cap 5.48e30 records per m^2, crossover radius 1.65e3 m",
      abs(rows[2][1] / 1.5876e-5 - 1) < 1e-3 and abs(rows[2][2] / 5.485e30 - 1) < 1e-3 and abs(rows[2][3] / 1.6455e3 - 1) < 1e-3,
      "%.4e %.4e %.4e" % rows[2][1:])
check("dE = 0.5 eV: crossover radius is microscopic (%.3e m)" % rows[0][3], rows[0][3] < 1e-3)
lp2 = 6.67430e-11 * 1.054571817e-34 / 2.99792458e8 ** 3
holo = 1 / (4 * lp2)
check("holographic stock density A/(4 l_p^2) = 9.57e68 nats per m^2 (for comparison only)", abs(holo / 9.57e68 - 1) < 2e-3, "%.4e" % holo)
check("the heat-shed cap at 1.0 eV sits about 38 orders of magnitude below it, and depends on q, Gamma, T",
      37 < math.log10(holo / rows[2][2]) < 39, "%.2f decades" % math.log10(holo / rows[2][2]))
# dimensionless cube, kT = Gamma = q = rho = 1, eps = 0.2
ncrit = 6 / floor4(0.2)
check("dimensionless cube (kT=Gamma=q=1, one carrier per site, eps=0.2): room n^3 vs heat 6 n^2/0.770979, crossover side 7.782",
      abs(ncrit - 7.782303) < 1e-5 and 7 ** 3 < 6 * 49 / floor4(0.2) and 8 ** 3 > 6 * 64 / floor4(0.2), "%.6f" % ncrit)

# ---------------------------------------------------------------- 12. self-correcting media
print("== 12. self-correcting media: block size needed and stock scaling")
for d, b in [(3, 2.0), (2, 2.0)]:
    tau = 1e9
    m = (math.log(nu * tau / eps) / b) ** (d / (d - 1))
    print("    d=%d  barrier exponent b=%.1f  tau=1e9 s  eps=1e-9  carriers per record m(tau)=%.1f" % (d, b, m))
    lam = nu * math.exp(-b * m ** ((d - 1) / d))
    check("d = %d: lambda(m(tau)) * tau = eps (passive hold, zero ongoing heat)" % d, abs(lam * tau / eps - 1) < 1e-6)
m3 = (math.log(nu * 1e9 / eps) / 2.0) ** 1.5
check("d = 3, b = 2: m(tau) = 203.0 carriers per record", abs(m3 - 203.0) < 0.05, "%.2f" % m3)
# power-law leak Gamma(m) = Gamma0 m^-kappa, under the conditional repair-cost assumption
for kappa in [0.0, 1.0, 3.0]:
    Rs = np.logspace(2, 6, 9)
    Ns = []
    for R in Rs:
        V, A = 4 / 3 * math.pi * R ** 3, 4 * math.pi * R ** 2
        # maximize min(V/m, A m^kappa / c) over m >= 1, with c = 1
        mstar = max(1.0, (V / A) ** (1 / (1 + kappa)))
        Ns.append(min(V / mstar, A * mstar ** kappa))
    slope = np.polyfit(np.log(Rs), np.log(Ns), 1)[0]
    pred = 3 - 1 / (1 + kappa)
    check("power-law leak kappa = %g: stock exponent %.4f = 3 - 1/(1+kappa) = %.4f" % (kappa, slope, pred), abs(slope - pred) < 1e-3)

# ---------------------------------------------------------------- 13. note text
print("== 13. note text")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
note = os.path.join(ROOT, "theory", "RECORD_REPAIR_FLOOR_2026-11-23.md")
with open(note, encoding="utf-8") as fh:
    txt = fh.read()
hyp = "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."
check("hypothesis sentence present exactly once, byte-identical", txt.count(hyp) == 1)
low = txt.lower()
check("no 'theory of everything', 'solved', 'solves', or 'bill'",
      "theory of everything" not in low and " solved" not in low and " solves" not in low and " bill" not in low)
for s in ["9.2378", "8.8335", "6.7153", "0.770979", "2.7726", "1.59\\times10^{-5}", "5.48\\times10^{30}", "1.65\\times10^{3}", "9.57\\times10^{68}", "7.78", "203.0", "1193"]:
    check("note quotes %s" % s, s in txt)

import re
with open(os.path.join(ROOT, "theory", "repair_floor_checks", "crossref.out"), encoding="utf-8") as fh:
    cr = [ln.split(" | ")[0] for ln in fh if ln.startswith("10.")]
note_dois = re.findall(r"doi (10\.\d{4,9}/\S+)", txt)
missing = [d for d in note_dois if not any(d.startswith(x) for x in cr)]
unused = [x for x in cr if x not in txt]
check("every DOI cited in the note is in crossref.out (%d cited, %d resolved)" % (len(note_dois), len(cr)), not missing, ",".join(missing))
check("every DOI in crossref.out is cited in the note", not unused, ",".join(unused))

print()
print("CHECKS %d  FAILS %d" % (CHECKS, FAILS))
if FAILS == 0:
    print("ALL REPAIR-FLOOR CHECKS PASS")
sys.exit(1 if FAILS else 0)
