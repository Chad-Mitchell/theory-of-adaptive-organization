#!/usr/bin/env python3
"""Checks for theory/BARRIER_MASS_FIELD_THEORY_2026-11-23.md (OPEN_WORK T65).

Code identities and worked evaluations in the classes named in the note.
A green run is not a proof, and nothing here is evidence about a real system.
Run from anywhere:  nice -n 19 python3 theory/barrier_mass_checks/barrier_mass_checks.py
"""
from __future__ import annotations

import math
import os
import re
import sys

import numpy as np
from scipy.linalg import eigh, qr

FAILS = 0
CHECKS = 0


def check(name, ok, detail=""):
    global FAILS, CHECKS
    CHECKS += 1
    if not ok:
        FAILS += 1
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  [" + detail + "]") if detail else ""))


# CODATA 2018 (SI) and PDG-style particle inputs (illustrative; quoted in the note)
c = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34
kB = 1.380649e-23
eV = 1.602176634e-19
lp2 = G * hbar / c ** 3
hbarc_eVm = hbar * c / eV
rng = np.random.default_rng(20261123)

# ---------------------------------------------------------------- 1. sphaleron-protected charge: beta
print("== 1. electroweak sphaleron barrier against the lightest Delta B = 3 record (in-model inputs)")
v = 246.22          # GeV, Higgs vev
mW = 80.37          # GeV
g = 2 * mW / v      # SU(2) coupling from m_W = g v / 2
pref = 4 * math.pi * v / g  # GeV, Klinkhamer-Manton prefactor 4 pi v / g = 2 m_W / alpha_W
alphaW = g * g / (4 * math.pi)
check("4 pi v/g equals 2 m_W/alpha_W", abs(pref / (2 * mW / alphaW) - 1) < 1e-12)
Blo, Bhi, Bmid = 1.56, 2.72, 1.9   # sphaleron branch, lambda/g^2 from 0 to infinity (review PR #244: lower end 1.56, not 1.52); ~1.9 at m_H = 125 GeV
Elo, Ehi, Emid = pref * Blo / 1e3, pref * Bhi / 1e3, pref * Bmid / 1e3
print("   g = %.4f, alpha_W = %.5f, 4 pi v/g = %.1f GeV; E_sph in [%.2f, %.2f] TeV, %.2f TeV at B = 1.9" % (g, alphaW, pref, Elo, Ehi, Emid))
check("E_sph range over all Higgs couplings is 7.4 to 12.9 TeV", abs(Elo - 7.39) < 0.01 and abs(Ehi - 12.89) < 0.01)
check("E_sph at B = 1.9 is 9.0 TeV", abs(Emid - 9.0) < 0.05)
# lightest state with B = 3 and L = 3 and zero charge: neutral helium-3 atom plus neutrinos making each L_i = 1
m_He3_atom = 3.0160293 * 931.49410242e-3  # GeV (atomic mass 3.0160293 u)
print("   lightest neutral B = 3 state (He-3 atom, plus neutrinos so each L_i = 1): %.4f GeV" % m_He3_atom)
check("He-3 atom mass is 2.809 GeV", abs(m_He3_atom - 2.8094) < 2e-4)
blo, bhi, bmid = Elo * 1e3 / m_He3_atom, Ehi * 1e3 / m_He3_atom, Emid * 1e3 / m_He3_atom
print("   beta_charge = E_sph / E_rec in [%.0f, %.0f], %.0f at B = 1.9" % (blo, bhi, bmid))
check("beta_charge is 2.6e3 to 4.6e3 (3.2e3 at B = 1.9): A1 holds only with beta >> 1", 2600 < blo < 2700 and 4550 < bhi < 4650 and 3150 < bmid < 3250)
supp = 4 * math.pi / alphaW
print("   zero-temperature tunneling exponent 4 pi/alpha_W = %.1f, rate factor 10^-%.0f" % (supp, supp / math.log(10)))
check("'t Hooft suppression exp(-4 pi/alpha_W) ~ 10^-161", abs(supp / math.log(10) - 161) < 0.5)
kT300 = kB * 300 / eV
Bstar = kT300 * math.log(1e12 * 3.15576e7 / 1e-9)
print("   retention need at 300 K (nu = 1e12/s, tau = 1 yr, eps = 1e-9): B* = %.3f eV; E_sph/B* = %.2e" % (Bstar, Emid * 1e12 / Bstar))
check("B* at 300 K is 1.70 eV; the sphaleron exceeds it by 5.3e12", abs(Bstar - 1.696) < 0.002 and abs(Emid * 1e12 / Bstar / 5.3e12 - 1) < 0.01)
# parametric toy: chiral fermions with Yukawa y, record = n fermions, m_f = y v / sqrt 2
def beta_toy(y, n=3, B=1.9):
    return (4 * math.pi * v * B / g) / (n * y * v / math.sqrt(2))
print("   Yang-Mills-Higgs toy, beta = 4 sqrt2 pi B/(g y n): y = 1e-2 -> %.3e, 1e-6 -> %.3e" % (beta_toy(1e-2), beta_toy(1e-6)))
check("toy beta scales as 1/y (unbounded as y -> 0)", abs(beta_toy(1e-6) / beta_toy(1e-2) - 1e4) < 1e-6)

# ---------------------------------------------------------------- 2. pure-gauge vacua are not locally readable
print("== 2. Lemma G: a gauge-invariant observable cannot tell U-related states apart")
worst = 0.0
for _ in range(200):
    n = 12
    Q = qr(rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n)))[0]
    ph = np.exp(1j * rng.uniform(0, 2 * np.pi, n))
    U = Q @ np.diag(ph) @ Q.conj().T            # the 'large gauge transformation'
    # random observable commuting with U: diagonal in U's eigenbasis, degenerate blocks ignored (generic phases)
    O = Q @ np.diag(rng.normal(size=n)) @ Q.conj().T
    psi = rng.normal(size=n) + 1j * rng.normal(size=n); psi /= np.linalg.norm(psi)
    a = np.vdot(psi, O @ psi).real
    b = np.vdot(U @ psi, O @ (U @ psi)).real
    worst = max(worst, abs(a - b))
check("<n|O|n> = <n+1|O|n+1> when |n+1> = U|n> and [O,U] = 0 (200 random cases)", worst < 1e-12, "" if worst < 1e-12 else "max diff %.1e" % worst)

# ---------------------------------------------------------------- 3. domain walls
print("== 3. Lemma W: a closed thin wall between degenerate vacua has no barrier against collapse")
sigma = 1.0
r = np.linspace(0, 5, 2001)
E = 4 * math.pi * sigma * r ** 2
check("E(r) = 4 pi sigma r^2 is increasing, so the minimax path r -> 0 has barrier 0", np.all(np.diff(E) > 0))
L = 3.0
check("uniform vacuum on a periodic box: flipping it needs two spanning walls, barrier 2 sigma L^2 = %.1f, at record energy 0 (one bit only)" % (2 * sigma * L * L), abs(2 * sigma * L * L - 18.0) < 1e-12)

# ---------------------------------------------------------------- 4. channel minimum
print("== 4. Lemma C: the effective barrier is the smallest over erasure channels")
def two_channel_gap(B1, B2, nu=1.0, kT=1.0):
    # states: 0 (record), 1 (erased); two parallel routes with saddles B1, B2
    k = nu * (math.exp(-B1 / kT) + math.exp(-B2 / kT))
    return 2 * k
for B1, B2 in [(30.0, 5.0), (8.0, 40.0), (12.0, 12.0)]:
    gp = two_channel_gap(B1, B2)
    Beff = -math.log(gp / 2)
    print("   B_charge = %.0f, B_transport = %.0f -> B_eff = %.3f kT" % (B1, B2, Beff))
    check("B_eff within ln 2 of min(B1, B2) for (%.0f, %.0f)" % (B1, B2), min(B1, B2) - math.log(2) - 1e-12 <= Beff <= min(B1, B2) + 1e-12)

# transport-channel sketch: field energy of an electrostatic well of depth U and size l, sources excluded
alpha = 1 / 137.035999
beta_field = 4 * math.pi * alpha * hbarc_eVm * 1e9 / (1.0 * 1.0)   # U = 1 eV, l = 1 nm
print("   sketch: field-only beta of a 1 eV, 1 nm electrostatic well = 4 pi alpha hbar c/(U l) = %.2f (source rest mass excluded)" % beta_field)
check("field-only transport beta sketch is 18.1", abs(beta_field - 18.09) < 0.01)
check("with one electron's rest mass as the source, beta <= 1 eV / 511 keV = 1.96e-6", abs(1.0 / 510998.95 / 1.957e-6 - 1) < 0.001)

# ---------------------------------------------------------------- 5. Berezin bound, discrete and exact
print("== 5. Lemma L (Berezin bathtub): sum of <phi_j, |p| phi_j> over N orthonormal states in a region")
Lg = 14
k1 = 2 * np.pi * np.fft.fftfreq(Lg)
KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing="ij")
f = np.sqrt(KX ** 2 + KY ** 2 + KZ ** 2)          # |k| on the periodic lattice
M = Lg ** 3
kern = np.fft.ifftn(f).real                         # kernel K(x - y) = (1/M) sum_k f(k) e^{ik(x-y)}
x1 = np.arange(Lg)
X, Y, Z = np.meshgrid(x1, x1, x1, indexing="ij")
cen = (Lg - 1) / 2
inside = ((X - cen) ** 2 + (Y - cen) ** 2 + (Z - cen) ** 2) <= 3.6 ** 2
pts = np.argwhere(inside)
nO = len(pts)
d = (pts[:, None, :] - pts[None, :, :]) % Lg
H = kern[d[..., 0], d[..., 1], d[..., 2]]
ev = np.sort(eigh(H, eigvals_only=True))
fs = np.sort(f.ravel())
w = nO / M
def bathtub(N):
    # fill the smallest f(k) with weight w each until total weight N
    full = int(N // w)
    tot = w * fs[:full].sum()
    rem = N - full * w
    if rem > 1e-15 and full < len(fs):
        tot += rem * fs[full]
    return tot
ok = True
worst = 1e9
for N in range(1, nO + 1):
    lhs = ev[:N].sum(); rhs = bathtub(N)
    worst = min(worst, lhs - rhs)
    ok &= lhs >= rhs - 1e-9
print("   grid %d^3, region of %d sites; min over N of (sum of lowest N eigenvalues - bathtub) >= -1e-9: %s" % (Lg, nO, worst >= -1e-9))
check("discrete Berezin bound holds for every N = 1..%d (exact eigenvalues)" % nO, ok)
okr = True
for _ in range(40):
    N = int(rng.integers(1, nO))
    Qm = qr(rng.normal(size=(nO, N)), mode="economic")[0]
    lhs = np.trace(Qm.T @ H @ Qm)
    okr &= lhs >= bathtub(N) - 1e-9
check("discrete Berezin bound holds for 40 random orthonormal sets", okr)
CB = 0.75 * (9 * math.pi / 2) ** (1 / 3)
print("   continuum constant C_B = (3/4)(9 pi/2)^(1/3) = %.4f  (sum E >= C_B N^(4/3) hbar c / R in a ball of radius R)" % CB)
check("C_B = 1.8135", abs(CB - 1.8135) < 5e-5)
# continuum identity: bathtub integral equals (3/4) N kF
R = 1.0; V = 4 * math.pi / 3 * R ** 3
for N in [1, 10, 1000]:
    kF = (6 * math.pi ** 2 * N / V) ** (1 / 3)
    integral = V / (2 * math.pi) ** 3 * math.pi * kF ** 4
    check("continuum bathtub integral = (3/4) N k_F = C_B N^(4/3)/R at N = %d" % N, abs(integral / (0.75 * N * kF) - 1) < 1e-12 and abs(integral / (CB * N ** (4 / 3)) - 1) < 1e-12)

# ---------------------------------------------------------------- 6. caps
print("== 6. the localization cap (hoop + Lemma L + A2), against T64's barrier cap")
Rm = 1.0
Emax = Rm * c ** 4 / (2 * G)
Nloc = (Rm ** 2 / (2 * CB * lp2)) ** 0.75
A = 4 * math.pi * Rm ** 2
Nloc_A = (A / (8 * math.pi * CB * lp2)) ** 0.75
print("   R = 1 m: E_max = %.3e J; N_loc = %.3e; A/(4 l_p^2) = %.3e; 8 pi C_B = %.2f" % (Emax, Nloc, A / (4 * lp2), 8 * math.pi * CB))
check("N_loc(1 m) = 5.86e51", abs(Nloc / 5.86e51 - 1) < 0.005)
check("same cap written with the area: (A/(45.58 l_p^2))^(3/4)", abs(Nloc_A / Nloc - 1) < 1e-12 and abs(8 * math.pi * CB - 45.58) < 0.005)
check("N_loc(1 m) is 18.3 orders below A/(4 l_p^2)", abs(math.log10(A / (4 * lp2) / Nloc) - 18.31) < 0.01)
for gs in [2, 4, 100]:
    check("g species/internal states multiply the cap by g^(1/4) (g = %d)" % gs,
          abs((Rm ** 2 * gs ** (1 / 3) / (2 * CB * lp2)) ** 0.75 / Nloc / gs ** 0.25 - 1) < 1e-12)
lnr = math.log(1e12 * 3.15576e7 / 1e-9)
check("retention log ln(nu tau/eps) = 65.62", abs(lnr - 65.62) < 0.005)
kTln = kB * 300 * lnr
beta_c = kTln * Nloc / Emax
print("   crossover beta_c = kT ln * N_loc / E_max at 1 m, 300 K: %.3e" % beta_c)
check("beta_c(1 m, 300 K) = 2.63e-11", abs(beta_c / 2.63e-11 - 1) < 0.005)
check("T64's carbon example (beta 8.94e-11) is above beta_c: localization cap binds", 8.94e-11 > beta_c)
check("T64's magnetic-grain example (beta 3.37e-16) is below beta_c: barrier cap binds", 3.37e-16 < beta_c)
# beta_c scales as T R^(1/2)
bc = lambda Rr, T: kB * T * lnr * (Rr ** 2 / (2 * CB * lp2)) ** 0.75 / (Rr * c ** 4 / (2 * G))
check("beta_c scales as T R^(1/2)", abs(bc(4.0, 300) / bc(1.0, 300) - 2) < 1e-9 and abs(bc(1.0, 600) / bc(1.0, 300) - 2) < 1e-9)
# R where N_loc reaches A/(4 l_p^2): (R^2/(2 CB lp2))^(3/4) = pi R^2/lp2
# solve (R/lp)^{3/2} (2 C_B)^{-3/4} = pi (R/lp)^2  ->  (R/lp)^{1/2} = (2 C_B)^{-3/4} / pi
Rx_lp = ((2 * CB) ** -0.75 / math.pi) ** 2
print("   N_loc equals A/(4 l_p^2) only at R = %.4f l_p (below the Planck length; outside any field-theory scope)" % Rx_lp)
check("crossover with the area count is at R = 0.0147 l_p", abs(Rx_lp - 0.0147) < 0.00005)
# general encodings: thermal maximum entropy at fixed energy (CKN form), one bosonic species
gdof = 1
kT_th = (30 * Emax * (hbar * c) ** 3 / (math.pi ** 2 * gdof * V)) ** 0.25
S_th = 4 / 3 * Emax / kT_th
print("   black-body S_max(E_max, V) at R = 1 m, g = 1: %.3e nats (kT = %.3e J)" % (S_th, kT_th))
check("thermal general-encoding bound at 1 m is 1.32e52 nats, same (R/l_p)^(3/2) scaling", abs(S_th / 1.32e52 - 1) < 0.005)
check("thermal bound scales as R^(3/2)",
      abs(((4 / 3) * (4 * Emax) / (30 * 4 * Emax * (hbar * c) ** 3 / (math.pi ** 2 * 64 * V)) ** 0.25) / S_th - 8) < 1e-9)

# ---------------------------------------------------------------- 7. Jacobson read-off
print("== 7. an A^(3/4) record count gives a patch-size-dependent eta = dS/dA")
eta = lambda Aa: 0.75 * Aa ** -0.25
check("eta(A) for S = A^(3/4) grows by 10 when A shrinks by 1e4 (no finite local limit)", abs(eta(1e-4) / eta(1.0) - 10) < 1e-9)

# ---------------------------------------------------------------- 8. note text
print("== 8. note text")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
note = os.path.join(ROOT, "theory", "BARRIER_MASS_FIELD_THEORY_2026-11-23.md")
with open(note, encoding="utf-8") as fh:
    txt = fh.read()
hyp = "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."
check("hypothesis sentence present exactly once, byte-identical", txt.count(hyp) == 1)
low = txt.lower()
check("no 'theory of everything', 'solved', 'solves', or 'bill'",
      "theory of everything" not in low and " solved" not in low and " solves" not in low and " bill" not in low)
check("no kill or verdict words", not re.search(r"\b(kill|killed|verdict|falsified|refuted)\b", low))
for s in ["7.4", "12.9", "9.0", "2.809", "3.2\\times10^{3}", "4.6\\times10^{3}", "1.70", "1.8135", "5.86\\times10^{51}", "45.58",
          "2.63\\times10^{-11}", "1.32\\times10^{52}", "0.0147", "10^{-161}", "18.3", "65.62", "18.1", "1.96\\times10^{-6}"]:
    check("note quotes %s" % s, s in txt)
with open(os.path.join(ROOT, "theory", "barrier_mass_checks", "crossref.out"), encoding="utf-8") as fh:
    cr = [ln.split(" | ")[0] for ln in fh if ln.startswith("10.")]
note_dois = [dd.rstrip(".):") for dd in re.findall(r"doi (10\.\d{4,9}/[^\s,;`]+)", txt)]
missing = [dd for dd in note_dois if dd not in cr]
unused = [xx for xx in cr if xx not in txt]
check("every DOI cited in the note is in crossref.out (%d cited, %d resolved)" % (len(set(note_dois)), len(cr)), not missing, ",".join(missing))
check("every DOI in crossref.out is cited in the note", not unused, ",".join(unused))

print()
print("CHECKS %d  FAILS %d" % (CHECKS, FAILS))
if FAILS == 0:
    print("ALL BARRIER-MASS CHECKS PASS")
sys.exit(1 if FAILS else 0)
