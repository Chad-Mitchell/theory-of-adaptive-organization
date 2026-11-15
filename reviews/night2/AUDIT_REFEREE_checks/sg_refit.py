#!/usr/bin/env python3
"""Independent check of Proposition SG: derivation identities + Monte Carlo + slope refit."""
import numpy as np

rng = np.random.default_rng(20261116)  # different seed from the project's 20261115
n = 2_000_000
D = 1.0
g, a0 = 0.4, 1.0
w, L, c = 1.0, 10.0, 1.0

def lomax(g, a0, n):
    u = rng.random(n)
    return a0 * (u ** (-1.0 / g) - 1.0)

def p0_B(a):
    return 1 - ((a + a0) / (a + D + a0)) ** g

def p0_A(lam, a=None):
    return 1 - np.exp(-lam * D)

def lnLR_star(p0):
    # follow iff p > c/(wL)  =>  ln Λ* = ln(c/(wL-c)) - logit(p0)
    return np.log(c / (w * L - c)) - np.log(p0 / (1 - p0))

print("=== Algebraic identities ===")
# (i) memoryless
lam = 0.1
print(f"Regime A p0 = 1-exp(-λΔ) = {p0_A(lam):.10f} (independent of a)")

# (ii) asymptotic p0 ~ γΔ/a
print("Regime B p0 vs γΔ/a and slope of lnΛ* on ln a:")
ages_all = np.array([3, 10, 30, 100, 300, 1000, 3000, 10000], dtype=float)
p0 = p0_B(ages_all)
thr = lnLR_star(p0)
approx = g * D / ages_all
print(f"{'age':>8} {'p0 exact':>12} {'γΔ/a':>12} {'rel err':>10} {'lnΛ*':>10}")
for a, p, ap, t in zip(ages_all, p0, approx, thr):
    print(f"{a:8.0f} {p:12.6f} {ap:12.6f} {(p-ap)/p:10.4f} {t:10.4f}")

# slopes on various windows
def slope(ages, thr):
    return np.polyfit(np.log(ages), thr, 1)[0]

print()
print("Fitted slope d lnΛ*/d ln a:")
print(f"  project's last-3 window (100,300,1000): {slope(ages_all[3:6], thr[3:6]):.6f}")
print(f"  all 6 project ages (3..1000):          {slope(ages_all[:6], thr[:6]):.6f}")
print(f"  last 3 of extended (1e3,3e3,1e4):      {slope(ages_all[-3:], thr[-3:]):.6f}")
print(f"  ages 30..1000:                         {slope(ages_all[2:6], thr[2:6]):.6f}")
# analytic derivative
# p0 = 1 - ((a+a0)/(a+D+a0))^g
# d lnΛ*/d ln a = -a * d(logit p0)/da
# As a→∞, p0 ~ γΔ/a, logit p0 ~ ln(γΔ)-ln a, so -d logit/d ln a → 1
print("  theoretical limit a→∞:                   1.000000")

# exact derivative at project ages for honesty
# S ratio r = ((a+a0)/(a+D+a0))^g, p0=1-r
# d p0 / da = -g * r * (1/(a+a0) - 1/(a+D+a0)) wait
# d/da ln((a+a0)/(a+D+a0)) = 1/(a+a0) - 1/(a+D+a0)
# d r / da = g r * that
# d p0 / da = - g r (1/(a+a0)-1/(a+D+a0))
# d logit / da = (1/p0 + 1/(1-p0)) dp0/da = dp0/da / (p0(1-p0))
# d lnΛ*/d ln a = -a * d logit/da

def exact_slope(a):
    r = ((a + a0) / (a + D + a0)) ** g
    p0 = 1 - r
    dp0 = -g * r * (1/(a+a0) - 1/(a+D+a0))
    dlogit = dp0 / (p0 * (1-p0))
    return -a * dlogit

print("  exact d lnΛ*/d ln a at project ages:")
for a in [3, 10, 30, 100, 300, 1000]:
    print(f"    a={a:5d}: {exact_slope(float(a)):.6f}")

print()
print("=== Monte Carlo (independent seed 20261116, n=2e6) ===")
T = lomax(g, a0, n)
print("Regime B (Lomax γ=0.4, a0=1)")
for a in [0, 1, 3, 10, 30, 100]:
    alive = T > a
    n_al = alive.sum()
    mc = np.mean(T[alive] <= a + D)
    se = np.sqrt(mc * (1-mc) / n_al)
    form = p0_B(a)
    z = (mc - form) / se
    print(f"  age {a:7.1f}: MC {mc:.5f} ± {se:.5f}  formula {form:.5f}  z={z:+.2f}  n_alive={n_al}")

Texp = rng.exponential(1 / lam, n)
print("Regime A (exponential λ=0.1)")
for a in [0, 1, 3, 10, 30]:
    alive = Texp > a
    n_al = alive.sum()
    mc = np.mean(Texp[alive] <= a + D)
    se = np.sqrt(mc * (1-mc) / n_al)
    form = p0_A(lam)
    z = (mc - form) / se
    print(f"  age {a:7.1f}: MC {mc:.5f} ± {se:.5f}  formula {form:.5f}  z={z:+.2f}  n_alive={n_al}")

# decision threshold algebra check
print()
print("=== Decision rule algebra ===")
# follow iff w L p > c, p = LR p0 / (1-p0+LR p0)
# ⇔ LR > [c/(wL-c)] (1-p0)/p0
print("Threshold formula confirmed by rearranging p > c/(wL).")
print(f"Requires wL > c (here wL={w*L}, c={c}): otherwise never follow.")
# caveat: expected loss = w L p assumes a change costs w over the whole remaining horizon L,
# regardless of when in the Δ-window it occurs and regardless of residual life. This is an
# approximation, not an exact renewal-reward optimum (Whittle index, etc.).

# Reproduce project's printed threshold values
ages_p = np.array([3, 10, 30, 100, 300, 1000.0])
p0p = p0_B(ages_p)
thrp = lnLR_star(p0p)
print("Project ages lnΛ*:")
for a, t in zip(ages_p, thrp):
    print(f"  age {a:6.0f}: ln LR* = {t:.3f}")
print(f"  slope last 3: {slope(ages_p[-3:], thrp[-3:]):.3f}")
print(f"  Regime A threshold: {lnLR_star(p0_A(lam)):.15f}")
