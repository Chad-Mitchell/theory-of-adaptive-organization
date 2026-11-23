#!/usr/bin/env python3
"""Checks for theory/GRAVITY_BARRIER_PROBE_2026-11-23.md (OPEN_WORK T64).

Code identities and worked evaluations in the classes named in the note.
A green run is not a proof, and nothing here is evidence about a real system.
Run from anywhere:  nice -n 19 python3 theory/gravity_barrier_checks/gravity_barrier_checks.py
"""
from __future__ import annotations

import heapq
import itertools
import math
import os
import re
import sys

import numpy as np
from scipy.linalg import eigh, expm

FAILS = 0
CHECKS = 0


def check(name, ok, detail=""):
    global FAILS, CHECKS
    CHECKS += 1
    if not ok:
        FAILS += 1
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  [" + detail + "]") if detail else ""))


# CODATA 2018 exact / recommended values (SI)
c = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34
kB = 1.380649e-23
eV = 1.602176634e-19
u = 1.66053906660e-27
lp2 = G * hbar / c ** 3
rng = np.random.default_rng(20261123)


def gen_reversible(pi, W):
    """Generator of a reversible chain: k(x,y) = W[x,y]/pi[x], W symmetric >= 0."""
    n = len(pi)
    K = W / pi[:, None]
    np.fill_diagonal(K, 0.0)
    K[np.arange(n), np.arange(n)] = -K.sum(axis=1)
    return K


def gap(K, pi):
    s = np.sqrt(pi)
    S = (s[:, None] * K) / s[None, :]
    S = (S + S.T) / 2
    ev = np.sort(eigh(S, eigvals_only=True))
    return -ev[-2]


# ---------------------------------------------------------------- 1. retention lemma (PROVED; spot check)
print("== 1. retention lemma: P_{pi|A0}(X_t in A1) >= pi(A1) (1 - exp(-lambda_2 t))")
worst = 1e9
for trial in range(300):
    n = int(rng.integers(3, 9))
    pi = rng.random(n) + 0.05
    pi /= pi.sum()
    W = rng.random((n, n)) * (rng.random((n, n)) < 0.7)
    W = np.triu(W, 1); W = W + W.T
    # keep connected: add a path
    for i in range(n - 1):
        W[i, i + 1] = W[i + 1, i] = W[i, i + 1] + 0.01
    K = gen_reversible(pi, W)
    A0 = rng.random(n) < 0.5
    if A0.all() or (~A0).all():
        A0[0] = True; A0[-1] = False
    lam = gap(K, pi)
    for t in [0.01, 0.3, 1.0, 5.0]:
        P = expm(K * t)
        start = np.where(A0, pi, 0.0); start /= start.sum()
        err = start @ P @ (~A0).astype(float)
        lb = pi[~A0].sum() * (1 - math.exp(-lam * t))
        worst = min(worst, err - lb)
check("300 random reversible chains x 4 times: error >= pi(A1)(1-e^{-lambda t}) (min slack %.2e)" % worst, worst > -1e-10)

# ---------------------------------------------------------------- 2. two-state Arrhenius record (PROVED in the model)
print("== 2. two-state Arrhenius record: B >= kT ln(nu tau / eps~), eps~ = -ln(1-2 eps)/2")
for eps in [1e-3, 1e-6, 1e-9]:
    nu, tau, kT = 1e12, 3.15576e7, 1.0
    et = -math.log1p(-2 * eps) / 2
    Bmin = kT * math.log(nu * tau / et)
    G_ = nu * math.exp(-Bmin / kT)
    err = -math.expm1(-2 * G_ * tau) / 2
    check("eps=%g: at B = B_min the error at tau is eps (%.6e)" % (eps, err), abs(err - eps) / eps < 1e-6)
    check("eps=%g: eps~/eps - 1 = %.2e (eps~ = eps + O(eps^2))" % (eps, et / eps - 1), abs(et / eps - 1) < 2.1 * eps)

# ---------------------------------------------------------------- 3. Eyring-Kramers slope on a Metropolis double well (NUMERICAL)
print("== 3. Metropolis chain on a 1D double well: ln(mean passage time) vs 1/kT has slope +B")
x = np.arange(-20, 21)
Bwell = 3.0
E = Bwell * ((x / 20.0) ** 2 - 1) ** 2  # barrier height Bwell at x=0, minima at +-20
betas = np.array([8.0, 10.0, 12.0, 14.0, 16.0])
lnT = []
for b in betas:
    w = np.exp(-b * (E - E.min()))  # unnormalized Gibbs weights
    # birth-death passage time from the left minimum to the right minimum, Metropolis rates (nu = 1):
    # T = sum_k (sum_{j<=k} w_j) / (w_k k_{k,k+1}),  w_k k_{k,k+1} = min(w_k, w_{k+1})
    cum = np.cumsum(w)
    T = sum(cum[k] / min(w[k], w[k + 1]) for k in range(len(x) - 1))
    lnT.append(math.log(T))
slope = np.polyfit(betas, lnT, 1)[0]
check("fitted slope %.4f vs B = %.4f (within 5%%; the Eyring-Kramers prefactor carries a power of 1/kT)" % (slope, Bwell), abs(slope - Bwell) / Bwell < 0.05)

# ---------------------------------------------------------------- 4. entropic barrier: zero energy barrier, slow escape (NUMERICAL counterexample to 'barrier must be energy')
print("== 4. entropic barrier: two complete graphs K_M joined by one edge, all energies equal")
ent_rows = []
for M in [5, 10, 20, 40, 80]:
    n = 2 * M
    W = np.zeros((n, n))
    W[:M, :M] = 1.0; W[M:, M:] = 1.0
    np.fill_diagonal(W, 0.0)
    W[M - 1, M] = W[M, M - 1] = 1.0
    pi = np.ones(n) / n
    W = W / n  # rates nu = 1 per edge
    lam = gap(gen_reversible(pi, W), pi)
    ent_rows.append((M, lam))
    print("   M=%3d  lambda_2=%.5e  M lambda_2=%.4f" % (M, lam, M * lam))
check("lambda_2 falls with M at zero energy barrier (monotone)", all(ent_rows[i][1] > ent_rows[i + 1][1] for i in range(len(ent_rows) - 1)))
check("lambda_2 ~ 2 nu/M at large M (M lambda_2 within 5%% of 2 at M=80: %.4f)" % (80 * ent_rows[-1][1]), abs(80 * ent_rows[-1][1] - 2) / 2 < 0.05)

# ---------------------------------------------------------------- 5. barrier <= energy span <= 2 sum|J| (PROVED; spot check)
print("== 5. single-flip minimax barrier between the two ground states <= span of H <= 2 sum|J|")


def minimax_barrier(n, Ef, a, b):
    """Min over single-flip paths a->b of the max energy along the path, minus E(a)."""
    best = {a: Ef[a]}
    pq = [(Ef[a], a)]
    while pq:
        m, s = heapq.heappop(pq)
        if s == b:
            return m - Ef[a]
        if m > best.get(s, 1e18):
            continue
        for i in range(n):
            t = s ^ (1 << i)
            mt = max(m, Ef[t])
            if mt < best.get(t, 1e18):
                best[t] = mt
                heapq.heappush(pq, (mt, t))
    return float("inf")


def ising_energies(n, bonds, J):
    Ef = np.zeros(2 ** n)
    for s in range(2 ** n):
        e = 0.0
        for (i, j), Jb in zip(bonds, J):
            si = 1 if (s >> i) & 1 else -1
            sj = 1 if (s >> j) & 1 else -1
            e -= Jb * si * sj
        Ef[s] = e
    return Ef


ok = True
for trial in range(40):
    n = int(rng.integers(3, 9))
    bonds = [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.5] or [(0, 1)]
    J = rng.random(len(bonds)) + 0.1  # ferromagnetic, so all-0 and all-1 are ground states
    Ef = ising_energies(n, bonds, J)
    B = minimax_barrier(n, Ef, 0, 2 ** n - 1)
    span = Ef.max() - Ef.min()
    ok &= (B <= span + 1e-12) and (span <= 2 * J.sum() + 1e-12)
check("40 random ferromagnetic graphs: B <= max H - min H <= 2 sum|J|", ok)

print("== 5b. 2D Ising L x L block, free boundary: exact single-flip barrier and B / (2 sum J)")
sq = {}
for Lside in [2, 3, 4]:
    n = Lside * Lside
    bonds = []
    for r in range(Lside):
        for q in range(Lside):
            i = r * Lside + q
            if q + 1 < Lside: bonds.append((i, i + 1))
            if r + 1 < Lside: bonds.append((i, i + Lside))
    J = np.ones(len(bonds))
    Ef = ising_energies(n, bonds, J)
    B = minimax_barrier(n, Ef, 0, 2 ** n - 1)
    sq[Lside] = (B, len(bonds))
    print("   L=%d  m=%2d  bonds=%2d  barrier=%.1f J  barrier/(2 sum J)=%.4f  barrier/m=%.4f J" % (Lside, n, len(bonds), B, B / (2 * len(bonds)), B / n))
check("L=2,3,4 barriers are 4J, 8J, 10J, between 2JL and 2J(L+1)", [round(float(sq[l][0]), 9) for l in sq] == [4.0, 8.0, 10.0] and all(2 * l <= sq[l][0] <= 2 * (l + 1) for l in sq))
check("barrier per site falls with block size (B/m: %.3f > %.3f > %.3f)" % tuple(sq[l][0] / (l * l) for l in sq),
      sq[2][0] / 4 > sq[3][0] / 9 > sq[4][0] / 16)

# ---------------------------------------------------------------- 6. saddle occupancy (assumption A3 gives no per-record charge)
print("== 6. equilibrium mean number of records at the saddle: N e^{-B/kT} << 1")
N6, lnr = 1e60, math.log(1e12 * 3.15576e7 / 1e-9)
occ = N6 * math.exp(-lnr) * 1.0  # two-state picture, saddle weight ~ e^{-B/kT}
check("N=1e60, B = kT ln(nu tau/eps), nu=1e12/s, tau=1 yr, eps=1e-9: mean saddle occupancy %.3e" % occ, occ > 1 and occ < N6 * 1e-28)
check("the saddle energy present at once is occupancy x B, not N x B (ratio %.2e)" % (occ / N6), occ / N6 < 1e-28)

# ---------------------------------------------------------------- 7. the cap and its circularity (ELEMENTARY identities)
print("== 7. cap N <= beta R c^4/(2 G kT ln) and its temperature-floor forms")
R = 1.0
Emax = R * c ** 4 / (2 * G)
A = 4 * math.pi * R ** 2
for R_ in [1e-3, 1.0, 1e3, 1.5e11]:
    E_ = R_ * c ** 4 / (2 * G); A_ = 4 * math.pi * R_ ** 2
    kTu = hbar * c / (2 * math.pi * R_)
    kTh = hbar * c / (4 * math.pi * R_)
    check("R=%g m: E_max/kT_Unruh(a=c^2/R) = A/(4 l_p^2) (ratio %.12f)" % (R_, E_ / kTu / (A_ / (4 * lp2))), abs(E_ / kTu / (A_ / (4 * lp2)) - 1) < 1e-12)
    check("R=%g m: E_max/kT_Hawking = 2 x A/(4 l_p^2) (ratio %.12f)" % (R_, E_ / kTh / (A_ / (4 * lp2))), abs(E_ / kTh / (A_ / (4 * lp2)) - 2) < 1e-12)
    # Bekenstein form: E/kT_U = 2 pi E R/(hbar c)
    check("R=%g m: E/kT_Unruh = 2 pi E R/(hbar c) (Bekenstein's ratio)" % R_, abs(E_ / kTu / (2 * math.pi * E_ * R_ / (hbar * c)) - 1) < 1e-12)
# first law with T_H integrates to S_BH
Msun = 1.98892e30
Ms = np.linspace(0, Msun, 200001)
integrand = np.zeros_like(Ms)
TH = hbar * c ** 3 / (8 * math.pi * G * Ms[1:] * kB)
integrand[1:] = c ** 2 / (kB * TH)  # dS/dM in nats; T_H -> infinity at M -> 0
S_int = np.trapezoid(integrand, Ms) if hasattr(np, "trapezoid") else np.trapz(integrand, Ms)
rs = 2 * G * Msun / c ** 2
S_BH = 4 * math.pi * rs ** 2 / (4 * lp2)
check("first law dS = c^2 dM / T_H integrates to A/(4 l_p^2) for 1 M_sun (ratio %.8f)" % (S_int / S_BH), abs(S_int / S_BH - 1) < 1e-6)

# ---------------------------------------------------------------- 7b. emergent-gravity angle (ELEMENTARY)
print("== 7b. without G: dimensional analysis and a Jacobson-style read-off")
# Inputs without G: hbar, c, k, R, T_U = hbar c/(2 pi k R), nu, tau, eps. Dimensionless groups: nu*tau, R*nu/c, eps
# (kT_U R/(hbar c) = 1/(2 pi) is a pure number). Exponent matrix over (m, s, kg) for R, c, hbar, nu:
Mdim = np.array([[1, 1, 2, 0], [0, -1, -1, -1], [0, 0, 1, 0]], dtype=float)  # columns R, c, hbar, nu
null = np.linalg.svd(Mdim)[2][-1]
null = null / null[0]
check("the only G-free dimensionless group from R, c, hbar, nu is R nu / c (null vector %s)" % np.round(null, 6).tolist(),
      np.allclose(null, [1, -1, 0, 1], atol=1e-9))
# An area cap N = eta A needs eta ~ (nu/c)^2: the attempt rate plays the Planck role only if nu ~ 1/t_p
nu_star = math.sqrt(c ** 5 / (hbar * G))
print("   nu* such that (nu/c)^2 = 1/l_p^2: %.4e /s (inverse Planck time)" % nu_star)
check("nu* = c/l_p = 1.85e43 /s", abs(nu_star / 1.855e43 - 1) < 0.002)
# Jacobson 1995 read-off: entropy density eta (nats per area) on local Rindler horizons gives G = c^3/(4 hbar eta)
eta = 1 / (4 * lp2)
check("Jacobson read-off: eta = 1/(4 l_p^2) returns G (ratio %.12f)" % (c ** 3 / (4 * hbar * eta) / G), abs(c ** 3 / (4 * hbar * eta) / G - 1) < 1e-12)
lnr7 = math.log(1e12 * 3.15576e7 / 1e-9)
check("records at density eta_rec with ln nats each read off G/ln: a record-count density 1/(4 l_p^2) would give G_read = G/%.2f" % lnr7,
      abs(c ** 3 / (4 * hbar * eta * lnr7) / G - 1 / lnr7) < 1e-12)

# ---------------------------------------------------------------- 8. worked numbers
print("== 8. worked numbers (beta = 1 unless stated)")
nu, tau, eps, T = 1e12, 3.15576e7, 1e-9, 300.0
lnr = math.log(nu * tau / eps)
kT = kB * T
Ncap = Emax / (kT * lnr)
Nholo = A / (4 * lp2)
print("   ln(nu tau/eps) = %.4f ; E_max(1 m) = %.4e J ; cap(300 K) = %.4e ; A/(4 l_p^2) = %.4e ; ratio = %.4e" % (lnr, Emax, Ncap, Nholo, Ncap / Nholo))
check("ln(nu tau/eps) = 65.62", abs(lnr - 65.62) < 0.005)
check("E_max(R=1 m) = 6.05e43 J", abs(Emax / 6.05e43 - 1) < 0.002)
check("cap at 300 K, R = 1 m: 2.23e62 records", abs(Ncap / 2.23e62 - 1) < 0.003)
check("A/(4 l_p^2) at R = 1 m: 1.20e70", abs(Nholo / 1.20e70 - 1) < 0.003)
check("fixed-T cap sits 7.7 orders below the holographic count at R = 1 m", abs(math.log10(Nholo / Ncap) - 7.73) < 0.01)
Rx = hbar * c / (2 * math.pi * kT * lnr)
print("   crossover radius at 300 K (cap = A/(4 l_p^2)): %.4e m" % Rx)
check("crossover radius at 300 K is 1.85e-8 m", abs(Rx / 1.85e-8 - 1) < 0.005)
TU1 = hbar * c / (2 * math.pi * kB * 1.0)
print("   hbar c/(2 pi k R) at R = 1 m: %.4e K" % TU1)
check("Unruh-type floor at R = 1 m is 3.64e-4 K (labs reach ~1e-9 K)", abs(TU1 / 3.64e-4 - 1) < 0.003)
Nu = Nholo / lnr
check("with the Unruh-type floor: cap = A/(4 l_p^2 ln) = 1.83e68 at R = 1 m", abs(Nu / 1.83e68 - 1) < 0.003)
# union bound
Ntot = 1e60
check("all-records error 1e-9 over 1e60 records: ln grows from 65.62 to %.2f" % math.log(nu * tau * Ntot / eps), abs(math.log(nu * tau * Ntot / eps) - 203.78) < 0.01)

print("== 8b. barrier-to-mass ratios beta in ordinary media (illustrative inputs, not measurements)")
beta_chem = 1.0 * eV / (12 * u * c ** 2)
Vgr = (8e-9) ** 3; mgr = 1.6e4 * Vgr
beta_hdd = 60 * kB * 300 / (mgr * c ** 2)
print("   1 eV barrier on a carbon-12 atom: beta = %.3e ; 60 kT grain of (8 nm)^3 at 16 g/cm^3: beta = %.3e" % (beta_chem, beta_hdd))
check("chemical beta = 8.94e-11", abs(beta_chem / 8.94e-11 - 1) < 0.003)
check("HDD-grain beta = 3.37e-16", abs(beta_hdd / 3.37e-16 - 1) < 0.005)

print("== 8c. black holes against the barrier cap; Lloyd's ultimate laptop")
check("Hawking-floor cap / S_BH = 2 beta / ln < 1 whenever ln(nu tau/eps) > 2 beta (beta = 1, ln = 65.62: %.4f)" % (2 / lnr), 2 / lnr < 1)
E_l, T_l = 1.0 * c ** 2, 5.87e8
S_l_nats = 2.04e8 / kB
EkT = E_l / (kB * T_l)
print("   Lloyd laptop: E/kT = %.4e nats ; Lloyd S/k = %.4e nats (= %.4e bits) ; ratio S/(E/kT) = %.4f" % (EkT, S_l_nats, S_l_nats / math.log(2), S_l_nats / EkT))
check("Lloyd 2000: S = 2.04e8 J/K is 2.13e31 bits", abs(S_l_nats / math.log(2) / 2.13e31 - 1) < 0.003)
check("Lloyd's laptop entropy is (4/3) E/kT, the black-body ratio (%.4f)" % (S_l_nats / EkT), abs(S_l_nats / EkT - 4 / 3) < 0.01)

# ---------------------------------------------------------------- 9. block accounting under the per-bond input
print("== 9. block accounting: under J <= kappa mu per bond, beta_block = B/(m mu) <= 2 kappa z/2 and falls as m^{-1/d}")
kappa = 1.0
rat = {l: sq[l][0] / (l * l) / (kappa) for l in sq}  # B/(m mu) with J = kappa mu
for l in sq:
    print("   L=%d: B/(m mu) = %.4f (2D bound 2 kappa z/2 = %.1f)" % (l, rat[l], 2 * kappa * 2))
check("2D blocks: B/(m mu) <= 2 kappa x (bonds per site <= 2)", all(rat[l] <= 4 * kappa for l in rat))
check("2D blocks: B/(m mu) = 1, 0.8889, 0.625 for L = 2, 3, 4, decreasing in L", abs(rat[2] - 1) < 1e-12 and abs(rat[3] - 8 / 9) < 1e-12 and abs(rat[4] - 0.625) < 1e-12)

# ---------------------------------------------------------------- 10. note text
print("== 10. note text")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
note = os.path.join(ROOT, "theory", "GRAVITY_BARRIER_PROBE_2026-11-23.md")
with open(note, encoding="utf-8") as fh:
    txt = fh.read()
hyp = "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."
check("hypothesis sentence present exactly once, byte-identical", txt.count(hyp) == 1)
low = txt.lower()
check("no 'theory of everything', 'solved', 'solves', or 'bill'",
      "theory of everything" not in low and " solved" not in low and " solves" not in low and " bill" not in low)
for s in ["65.62", "6.05\\times10^{43}", "2.23\\times10^{62}", "1.20\\times10^{70}", "1.85\\times10^{-8}", "3.64\\times10^{-4}",
          "1.83\\times10^{68}", "8.94\\times10^{-11}", "3.37\\times10^{-16}", "2.13\\times10^{31}", "203.78", "0.625", "1.85\\times10^{43}"]:
    check("note quotes %s" % s, s in txt)
with open(os.path.join(ROOT, "theory", "gravity_barrier_checks", "crossref.out"), encoding="utf-8") as fh:
    cr = [ln.split(" | ")[0] for ln in fh if ln.startswith("10.")]
note_dois = [d.rstrip(".):") for d in re.findall(r"doi (10\.\d{4,9}/[^\s,;`]+)", txt)]
missing = [d for d in note_dois if d not in cr]
unused = [x for x in cr if x not in txt]
check("every DOI cited in the note is in crossref.out (%d cited, %d resolved)" % (len(set(note_dois)), len(cr)), not missing, ",".join(missing))
check("every DOI in crossref.out is cited in the note", not unused, ",".join(unused))

print()
print("CHECKS %d  FAILS %d" % (CHECKS, FAILS))
if FAILS == 0:
    print("ALL GRAVITY-BARRIER CHECKS PASS")
sys.exit(1 if FAILS else 0)
