#!/usr/bin/env python3
"""Checks for theory/TRANSPORT_BARRIER_2026-11-23.md (OPEN_WORK T66).

Code identities and worked evaluations in the classes named in the note.
A green run is not a proof, and nothing here is evidence about a real system.
Run from anywhere:  nice -n 19 python3 theory/transport_barrier_checks/transport_barrier_checks.py
"""
from __future__ import annotations

import math
import os
import re
import sys

import numpy as np
from scipy.integrate import quad, solve_bvp
from scipy.optimize import brentq

FAILS = 0
CHECKS = 0


def check(name, ok, detail=""):
    global FAILS, CHECKS
    CHECKS += 1
    if not ok:
        FAILS += 1
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  [" + detail + "]") if detail else ""))


# CODATA 2018 (SI) and particle inputs (quoted in the note)
c = 299792458.0
G = 6.67430e-11
hbar = 1.054571817e-34
kB = 1.380649e-23
eV = 1.602176634e-19
alpha = 1 / 137.035999084
me = 0.51099895          # MeV
mp = 938.27208816        # MeV
mu = 931.49410242        # MeV per atomic mass unit
BA_max = 8.7945          # MeV, largest binding per nucleon (Ni-62; AME 2020)
lp2 = G * hbar / c ** 3
rng = np.random.default_rng(20261123)

# ---------------------------------------------------------------- 1. Lemma Z: two-sided barrier of an occupation record
print("== 1. Lemma Z: a carrier's two-sided barrier is at most its free rest energy")
m = 1.0
worst = 0.0
for _ in range(10000):
    I = rng.uniform(0, 2 * m)                  # binding of the carrier to its trap
    Bz = min(I, 2 * m - I)                     # leave route vs pair route (anti-carrier escapes)
    worst = max(worst, Bz - m)
check("min(I, 2m - I) <= m for every binding I in [0, 2m] (10^4 draws)", worst <= 1e-15)
Eb = np.linspace(-0.999, 0.999, 2001)          # bound level inside the gap (-m, m)
two = np.minimum(m - Eb, m + Eb)
check("for a level E_b in the gap the two-sided barrier is m - |E_b|, largest (= m) at the mid-gap zero mode",
      np.allclose(two, m - np.abs(Eb)) and abs(Eb[np.argmax(two)]) < 1e-12)

# ---------------------------------------------------------------- 2. Lemma P: translation is a flat path
print("== 2. Lemma P: rigidly translating a free composite costs no energy")
L = 64
phi = np.tanh((np.arange(L) - 20) / 3.0) - np.tanh((np.arange(L) - 30) / 3.0)   # a lump on a periodic lattice


def lattice_energy(f):
    return float(np.sum(0.5 * (np.roll(f, -1) - f) ** 2 + 0.25 * f ** 2 * (f - 2) ** 2))


E0 = lattice_energy(phi)
spread = max(abs(lattice_energy(np.roll(phi, s)) - E0) for s in range(L))
check("energy along the path of lattice translations is constant (barrier 0)", spread < 1e-9)

# ---------------------------------------------------------------- 3. monopole trap (Jackiw-Rebbi, Callias)
print("== 3. fermion zero modes on a BPS-bounded monopole")


def ps_integrand(xi):
    if xi < 1e-4:
        return 0.0
    K = xi / math.sinh(xi)
    H = xi / math.tanh(xi) - 1
    dK = (math.sinh(xi) - xi * math.cosh(xi)) / math.sinh(xi) ** 2
    dH = 1 / math.tanh(xi) - xi / math.sinh(xi) ** 2
    return dK ** 2 + (K * K - 1) ** 2 / (2 * xi * xi) + (xi * dH - H) ** 2 / (2 * xi * xi) + K * K * H * H / (xi * xi)


Ips = quad(ps_integrand, 0, 60, limit=400)[0] + 1 / 60.0   # tail beyond 60 is the magnetic Coulomb field, integrand 1/xi^2 up to e^-60
print("   Prasad-Sommerfield energy in units of 4 pi v/g: %.8f" % Ips)
check("BPS monopole energy equals 4 pi v/g (Bogomolny bound saturated)", abs(Ips - 1) < 1e-7)


def callias_per_charge(t):
    ms = [t - j for j in range(int(round(2 * t)) + 1)]
    return sum(abs(x) for x in ms)


cc = {t: callias_per_charge(t) for t in (0.5, 1.0, 1.5, 2.0)}
print("   zero modes per unit charge, isospin 1/2, 1, 3/2, 2: %s" % [cc[t] for t in (0.5, 1.0, 1.5, 2.0)])
check("Callias count per unit charge: 1 (isospinor), 2 (isovector), 4, 6", [cc[t] for t in (0.5, 1.0, 1.5, 2.0)] == [1, 2, 4, 6])


def beta_mon(y, g, S):
    return y * g * S / (4 * math.pi)


b_half = beta_mon(1.0, 0.65, 1)
b_one = beta_mon(1.0, 0.65, 2)
print("   beta_unbind <= y g S_t/(4 pi): g = 0.65, y = 1: isospinor %.4f, isovector %.4f" % (b_half, b_one))
check("monopole bound at g = 0.65, y = 1 is 0.052 (isospinor) and 0.103 (isovector)", abs(b_half - 0.0517) < 5e-4 and abs(b_one - 0.1035) < 5e-4)

# ---------------------------------------------------------------- 4. string loop trap (Jackiw-Rossi, Witten)
print("== 4. fermion zero modes on a BPS-bounded string loop")


def vortex_energy(n):
    # BPS equations, e = v = 1: f' = n f (1 - a)/r, a' = r (1 - f^2)/n; energy per length 2 pi int r [...] dr
    r0, r1 = 1e-3, 18.0

    def ode(r, y):
        f, a = y
        return np.vstack([n * f * (1 - a) / r, r * (1 - f * f) / n])

    def bc(ya, yb):
        return np.array([ya[1], yb[0] - 1])   # a(r0) = 0, f(r1) = 1

    r = np.linspace(r0, r1, 4000)
    y0 = np.vstack([np.tanh(r) ** n, 1 - np.exp(-r * r / 2)])
    sol = solve_bvp(ode, bc, r, y0, tol=1e-9, max_nodes=200000)
    rr = np.linspace(r0, r1, 200001)
    f, a = sol.sol(rr)
    df = n * f * (1 - a) / rr
    da = rr * (1 - f * f) / n
    dens = df ** 2 + n * n * f * f * (1 - a) ** 2 / rr ** 2 + (n * da) ** 2 / (2 * rr * rr) + 0.5 * (1 - f * f) ** 2
    return 2 * math.pi * np.trapezoid(rr * dens, rr), sol.status


for n in (1, 2):
    En, st = vortex_energy(n)
    print("   BPS vortex n = %d: energy per length %.5f (2 pi n = %.5f)" % (n, En, 2 * math.pi * n))
    check("BPS string tension equals 2 pi v^2 |n| for n = %d" % n, st == 0 and abs(En / (2 * math.pi * n) - 1) < 2e-3)


def beta_string(y, vL):
    return y * y / (4 * math.pi ** 2) + y / (2 * math.pi * vL)


bs = beta_string(1.0, 1e3)
print("   per-record beta <= y^2/(4 pi^2) + y/(2 pi v L): y = 1, v L = 1e3: %.5f" % bs)
check("string-loop bound at y = 1 is 0.0253 plus a 1/(vL) end term", abs(1 / (4 * math.pi ** 2) - 0.02533) < 1e-5 and bs < 0.0255)
# mode-count identity: modes with 0 <= E < m on a loop of length L number floor(L m/2pi) + 1 per zero mode
Lm = 37.3
modes = [2 * math.pi * j / Lm for j in range(0, 100) if 2 * math.pi * j / Lm < 1.0]
check("chiral modes below threshold on a loop number L m/(2 pi) + 1 at most", len(modes) <= Lm / (2 * math.pi) + 1)

# ---------------------------------------------------------------- 5. Coulomb traps (nuclei)
print("== 5. electrons held by nuclei")
per_charge = mp - BA_max       # lower bound on nuclear mass per unit charge: M >= A (m_p - B/A_max) >= Z (m_p - B/A_max)
b_coul = 2 * me / per_charge   # Lemma Z barrier <= m_e c^2; records per nucleus <= 2Z (Lieb 1984, N < 2Z + 1)
print("   nuclear mass per unit charge >= %.2f MeV; beta <= 2 m_e/(m_p - 8.79 MeV) = %.4e" % (per_charge, b_coul))
check("Coulomb nuclear-trap bound, single atoms (N_c < 2z + 1): beta <= 1.10e-3", abs(b_coul / 1.0995e-3 - 1) < 1e-3)
b_mol = 3 * me / per_charge    # molecules: N_c < 2Z + K <= 3Z (each nucleus has z >= 1)
print("   molecules (N_c < 2Z + K <= 3Z): beta <= 3 m_e/(m_p - 8.79 MeV) = %.4e" % b_mol)
check("Coulomb nuclear-trap bound, any molecule or solid: beta <= 1.65e-3", abs(b_mol / 1.6493e-3 - 1) < 1e-3)
mH = mp + me - 13.6057e-6
bH = 13.6057e-6 / mp
print("   hydrogen: 13.6 eV / m_p = %.3e" % bH)
check("hydrogen beta (trap charged) is 1.45e-8", abs(bH / 1.45e-8 - 1) < 0.01)
Z = 92
Ib = me * (1 - math.sqrt(1 - (Z * alpha) ** 2))           # point-nucleus Dirac 1s binding
MU = 238.0507884 * mu - 92 * me                             # U-238 nucleus (atomic mass minus electrons; binding of electrons neglected)
print("   U91+ point-nucleus Dirac 1s binding %.1f keV, nucleus %.1f GeV, beta = %.3e" % (Ib * 1e3, MU / 1e3, Ib / MU))
check("U91+ 1s binding is 132 keV and beta is 6.0e-7", abs(Ib * 1e3 - 132.3) < 0.5 and abs(Ib / MU / 5.97e-7 - 1) < 0.01)
check("every point-nucleus Dirac 1s binding (Z alpha <= 1) is below m_e c^2", all(me * (1 - math.sqrt(1 - (z * alpha) ** 2)) <= me for z in range(1, 138)))
check("light Coulomb trap, nonrelativistic hydrogenic sketch: beta <~ n (Z alpha)^2 / 2 = alpha^2 = 5.3e-5 at Z = 1, n = 2",
      abs(alpha ** 2 - 5.325e-5) < 1e-7)

# ---------------------------------------------------------------- 6. strong coupling: a light trap that binds a heavy fermion (bag)
print("== 6. fermion bag in mean field (classical sigma, one valence fermion, no Dirac sea)")
x_mit = brentq(lambda x: math.sin(x) / x - (math.sin(x) / x ** 2 - math.cos(x) / x), 1.5, 2.5)
print("   MIT-bag lowest mode x = %.4f" % x_mit)
check("bag-limit mode x = 2.0428 (j0 = j1)", abs(x_mit - 2.0428) < 1e-4)


def dirac_E(Sfun, Sinf, rmax, n=8000):
    """Lowest positive s1/2 (kappa = -1) energy for a scalar mass profile; vectorised RK4 shooting."""
    r0 = 1e-5
    h = (rmax - r0) / n

    def run(E):
        u = np.full_like(E, r0)
        w = -(E - Sfun(r0)) * r0 ** 2 / 3
        r = r0
        neg = np.zeros(E.shape, bool)

        def f(r, u, w):
            s = Sfun(r)
            return u / r + (E + s) * w, -w / r - (E - s) * u

        for _ in range(n):
            k1 = f(r, u, w)
            k2 = f(r + h / 2, u + h / 2 * k1[0], w + h / 2 * k1[1])
            k3 = f(r + h / 2, u + h / 2 * k2[0], w + h / 2 * k2[1])
            k4 = f(r + h, u + h * k3[0], w + h * k3[1])
            u = u + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            w = w + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            r += h
            neg |= u < 0
            sc = np.maximum(1, np.abs(u))
            u = u / sc
            w = w / sc
        return neg

    lo, hi = 0.0, Sinf * (1 - 1e-7)
    if not run(np.array([hi]))[0]:
        return None
    for _ in range(4):
        Es = np.linspace(lo, hi, 41)
        neg = run(Es)
        k = int(np.argmax(neg))
        if k == 0:
            return float(Es[0])
        lo, hi = Es[k - 1], Es[k]
    return float(0.5 * (lo + hi))


wall = lambda gg: (lambda r: gg * (np.tanh((r - 1.0) * gg * 2) + 1) / 2)
Ebag = dirac_E(wall(200.0), 200.0, 4.0, n=12000)
print("   sharp wall at R = 1 with outside mass 200: E = %.4f (bag limit x/R = %.4f, approached from below)" % (Ebag, x_mit))
check("Dirac solver reproduces the bag limit from below", 2.03 < Ebag < x_mit)
Rt, lam = 0.9, 1.0
rr = np.linspace(0, Rt * 8, 20001)
ex = np.exp(-(rr / Rt) ** 2)
s = 1 - ex
ds = 2 * rr / Rt ** 2 * ex
Ffield = 4 * math.pi * np.trapezoid(rr * rr * (0.5 * ds ** 2 + lam / 4 * (s * s - 1) ** 2), rr)
lower = {}
for gy in (10.0, 100.0, 1000.0):
    ED = dirac_E(lambda r, gy=gy: gy * (1 - np.exp(-(r / Rt) ** 2)), gy, Rt * 5 + 15 / gy + 3)
    Etrial = ED + Ffield
    lower[gy] = (gy - Etrial) / Etrial
    print("   g = %4.0f (g^2/4pi = %7.1f): trial soliton energy %.3f sigma_v vs free fermion %.0f; beta_unbind >= %.2f"
          % (gy, gy * gy / (4 * math.pi), Etrial, gy, lower[gy]))
check("variational lower bounds on beta_unbind: >= 0.40 at g = 10, >= 7.46 at g = 100, >= 45.2 at g = 1000",
      abs(lower[10.0] - 0.400) < 0.01 and abs(lower[100.0] - 7.46) < 0.02 and abs(lower[1000.0] - 45.18) < 0.05)
check("beta_unbind lower bound grows with the Yukawa coupling", lower[10.0] < lower[100.0] < lower[1000.0])
two_sided = {gy: min(gy - (gy / (1 + lower[gy])), 2 * gy / (1 + lower[gy])) / (gy / (1 + lower[gy])) for gy in lower}
print("   two-sided (review): empty state erased by bag + anti-bag at 2 E_1, so beta <= min(m - E_1, 2 E_1)/E_1: %s"
      % ", ".join("%.2f" % two_sided[gy] for gy in sorted(two_sided)))
check("bag record two-sided beta <= 2 at every g (one-sided unbind values do not carry over)", max(two_sided.values()) <= 2 + 1e-12)
check("with the two-state average E_rec = E_1/2 the unbind lower bounds double (0.80, 14.9, 90.4)",
      abs(2 * lower[10.0] - 0.80) < 0.01 and abs(2 * lower[100.0] - 14.93) < 0.02 and abs(2 * lower[1000.0] - 90.36) < 0.05)

# ---------------------------------------------------------------- 7. self-gravitating confinement (sketch)
print("== 7. confinement by the region's own gravity (Newtonian sketch with the hoop input)")
print("   hoop: G M/(R c^2) <= 1/2, so the escape barrier per object G M m/R <= m c^2/2 and beta <= 1/2 (SKETCH; no check)")

# ---------------------------------------------------------------- 8. A2 replaced for Coulomb matter (Lieb-Yau 1988)
print("== 8. A2 from relativistic stability of matter")
k_alpha = 0.686           # any kappa > 94 alpha = 0.68595 works (Lieb-Yau's alpha condition is strict)
check("94 alpha = 0.68595 < 0.686", 94 * alpha < k_alpha)
zmax_flat = max(z for z in range(1, 140) if math.pi * z * alpha / 2 <= k_alpha)
zmax_any = max(z for z in range(1, 140) if z * alpha <= 2 / math.pi)
print("   kappa_int = max(94 alpha, pi z alpha/2): 94 alpha = %.4f, governs for z <= %d; covered z <= %d" % (k_alpha, zmax_flat, zmax_any))
check("kappa_int = 0.686 for z <= 59; 1 - kappa_int = 0.314", abs(1 - k_alpha - 0.314) < 1e-12 and zmax_flat == 59)
check("Lieb-Yau's condition covers nuclear charges up to z = 87", zmax_any == 87)
k87 = math.pi * 87 * alpha / 2
check("at z = 87, 1 - kappa_int = 0.0027", abs((1 - k87) - 0.0027) < 1e-4)
CB = 0.75 * (9 * math.pi / 2) ** (1 / 3)
R = 1.0
N0 = (R * R / (2 * CB * lp2)) ** 0.75
N_LY = ((2 ** (1 / 3) / (1 - k_alpha)) * R * R / (2 * CB * lp2)) ** 0.75
print("   cap at R = 1 m: free carriers g = 1: %.3e; electrons (g = 2), z <= 59, Lieb-Yau: %.3e (factor %.2f)" % (N0, N_LY, N_LY / N0))
check("T65 cap at 1 m reproduced (5.86e51)", abs(N0 / 5.856e51 - 1) < 2e-3)
check("electron cap with Lieb-Yau's kappa is 1.66e52 at 1 m (factor 2.84)", abs(N_LY / 1.66e52 - 1) < 5e-3 and abs(N_LY / N0 - 2.84) < 0.006)

# ---------------------------------------------------------------- 9. GTAO read-off numbers
print("== 9. method read-off")
kT300 = kB * 300 / eV
Bstar = kT300 * math.log(1e12 * 3.15576e7 / 1e-9)
floor_coul = Bstar / b_mol
print("   B* = %.3f eV; least mass per record at B* in the nuclear-trap class: %.2f keV" % (Bstar, floor_coul / 1e3))
check("B* = 1.70 eV; nuclear-trap mass floor per record B*/beta >= 1.03 keV", abs(Bstar - 1.696) < 0.002 and abs(floor_coul / 1028 - 1) < 0.01)

# ---------------------------------------------------------------- 10. note text
print("== 10. note text")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
note = os.path.join(ROOT, "theory", "TRANSPORT_BARRIER_2026-11-23.md")
with open(note, encoding="utf-8") as fh:
    txt = fh.read()
hyp = "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."
check("hypothesis sentence present exactly once, byte-identical", txt.count(hyp) == 1)
low = txt.lower()
check("no 'theory of everything', 'solved', 'solves', or 'bill'",
      "theory of everything" not in low and " solved" not in low and " solves" not in low and " bill" not in low)
check("no kill or verdict words", not re.search(r"\b(kill|killed|verdict|falsified|refuted)\b", low))
for q in ["0.052", "0.103", "0.0253", "1.10\\times10^{-3}", "1.45\\times10^{-8}", "6.0\\times10^{-7}", "132", "5.3\\times10^{-5}",
          "2.0428", "7.46", "45.2", "0.40", "0.686", "0.314", "59", "87", "0.0027", "1.66\\times10^{52}", "2.84", "1.03", "1.70", "1.65\\times10^{-3}"]:
    check("note quotes %s" % q, q in txt)
with open(os.path.join(ROOT, "theory", "transport_barrier_checks", "crossref.out"), encoding="utf-8") as fh:
    cr = [ln.split(" | ")[0] for ln in fh if ln.startswith("10.")]
note_dois = [dd.rstrip(".):") for dd in re.findall(r"doi (10\.\d{4,9}/[^\s,;`]+)", txt)]
missing = [dd for dd in note_dois if dd not in cr]
unused = [xx for xx in cr if xx not in txt]
check("every DOI cited in the note is in crossref.out (%d cited, %d resolved)" % (len(set(note_dois)), len(cr)), not missing, ",".join(missing))
check("every DOI in crossref.out is cited in the note", not unused, ",".join(unused))

print()
print("CHECKS %d  FAILS %d" % (CHECKS, FAILS))
if FAILS == 0:
    print("ALL TRANSPORT-BARRIER CHECKS PASS")
sys.exit(1 if FAILS else 0)
