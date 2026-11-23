"""Rival-gate check for the real-system screen of 23 November 2026 (REALSYS_SCREEN_2026-11-23.md).

Closed forms and root-finding only. No data is read. Not a simulation of a real system.
Checks, on the same quantity (steady mean squared error eps at a fixed stake w):
  G1  diffusive world, T49 class A floor kT*D*(1/eps - I):        d ln eps*/d ln D      = 1/2
  G2  reset-shock world, T49 class C floor kT*lam*[1.5 ln(v/eps) - gamma - ln 2]:
                                                                   d ln eps*/d ln lam    = 1
  G3  same shock world with the attaining core-plus-reserve gap (3.0033 + eps/4v)*lam added:
                                                                   slope within 0.02 of 1 for eps*/v <= 0.01
  R1  linear (Kalman-Bucy) filter, fixed white sensor noise R, on the second-order-matched
      world (autocovariance v*exp(-lam|t|), same for the reset world and the OU world):
                                                                   d ln P/d ln lam -> 1/2 at high precision
  S1  stake elasticity: diffusive -1/2, shock -1; linear filter at fixed R: 0
"""
import math

KT = 1.0
GAMMA_E = 0.5772156649015329
FAILS = 0


def check(name, ok, detail):
    global FAILS
    print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    if not ok:
        FAILS += 1


def golden_min(f, lo, hi, it=400):
    g = (math.sqrt(5) - 1) / 2
    a, b = math.log(lo), math.log(hi)
    c, d = b - g * (b - a), a + g * (b - a)
    for _ in range(it):
        if f(math.exp(c)) < f(math.exp(d)):
            b = d
        else:
            a = c
        c, d = b - g * (b - a), a + g * (b - a)
    return math.exp((a + b) / 2)


def eps_diff(D, w, I=0.0):
    return golden_min(lambda e: KT * D * (1 / e - I) + w * e, 1e-12, 1e6)


def eps_shock(lam, w, v=1.0, gap=False):
    def J(e):
        h = KT * lam * (1.5 * math.log(v / e) - GAMMA_E - math.log(2))
        if gap:
            h += KT * lam * (3.0033 + e / (4 * v))
        return h + w * e
    return golden_min(J, 1e-14, v)


def kalman_P(lam, v, R):
    # steady Riccati for dX = -lam X dt + sqrt(2 lam v) dW, dY = X dt + sqrt(R) dV
    return R * (-lam + math.sqrt(lam * lam + 2 * lam * v / R))


def slope(f, x, h=1e-3):
    return (math.log(f(x * math.exp(h))) - math.log(f(x * math.exp(-h)))) / (2 * h)


w = 1e4
for D in (1e-3, 1e-1, 10.0):
    s = slope(lambda d: eps_diff(d, w), D)
    check("G1 diffusive d ln eps*/d ln D", abs(s - 0.5) < 1e-3, f"D={D:g} w={w:g} slope={s:.6f}")
for lam in (1e-3, 1e-1, 10.0):
    e = eps_shock(lam, w)
    check("G2 closed form eps*=1.5 kT lam/w", abs(e / (1.5 * KT * lam / w) - 1) < 1e-6, f"lam={lam:g} eps*={e:.6e}")
    s = slope(lambda l: eps_shock(l, w), lam)
    check("G2 shock d ln eps*/d ln lam", abs(s - 1.0) < 1e-3, f"lam={lam:g} slope={s:.6f}")
    sg = slope(lambda l: eps_shock(l, w, gap=True), lam)
    eg = eps_shock(lam, w, gap=True)
    check("G3 with attaining gap", eg <= 0.01 and abs(sg - 1.0) < 0.02, f"lam={lam:g} eps*={eg:.3e} slope={sg:.6f}")
for R in (1e-6, 1e-4):
    s = slope(lambda l: kalman_P(l, 1.0, R), 1e-2)
    check("R1 linear filter d ln P/d ln lam", abs(s - 0.5) < 0.01, f"R={R:g} lam=0.01 slope={s:.6f}")
sd = slope(lambda ww: eps_diff(1e-1, ww), w)
ss = slope(lambda ww: eps_shock(1e-1, ww), w)
check("S1 stake elasticity diffusive", abs(sd + 0.5) < 1e-3, f"slope={sd:.6f}")
check("S1 stake elasticity shock", abs(ss + 1.0) < 1e-3, f"slope={ss:.6f}")
print("Rival gap on the shock-rate exponent at matched second-order statistics: GTAO 1, linear filter 1/2")
print(f"FAILS {FAILS}")
if FAILS == 0:
    print("ALL REALSYS-SCREEN CHECKS PASS")
raise SystemExit(1 if FAILS else 0)
