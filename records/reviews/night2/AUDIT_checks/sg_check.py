# SURPRISE-GUIDED-SEARCH Proposition SG: Monte Carlo check of the prior change probability
# P(change in (a, a+D] | no change in (0, a]) for renewal processes, and the implied surprise threshold.
import numpy as np
rng = np.random.default_rng(20261115)
n = 2_000_000
D = 1.0
def lomax(g, a0, n):  # survival S(t) = (a0/(a0+t))^g  -> hazard g/(a0+t)
    u = rng.random(n); return a0 * (u ** (-1.0 / g) - 1.0)
def check(name, T, p_formula, ages):
    print(name)
    for a in ages:
        alive = T > a
        mc = np.mean(T[alive] <= a + D)
        print(f"  age {a:7.1f}: MC {mc:.4f}  formula {p_formula(a):.4f}")
g, a0 = 0.4, 1.0
check("Regime B (Lomax, gamma=0.4, a0=1)", lomax(g, a0, n),
      lambda a: 1 - ((a + a0) / (a + D + a0)) ** g, [0, 1, 3, 10, 30, 100])
lam = 0.1
check("Regime A (exponential, lambda=0.1)", rng.exponential(1 / lam, n),
      lambda a: 1 - np.exp(-lam * D), [0, 1, 3, 10, 30])
# Threshold log-LR for follow-up: follow iff p_post*w*L > c, p_post odds = LR * p0/(1-p0)
w, L, c = 1.0, 10.0, 1.0
print("Threshold ln LR vs ln(age) (regime B):")
ages = np.array([3, 10, 30, 100, 300, 1000.0])
p0 = 1 - ((ages + a0) / (ages + D + a0)) ** g
thr = np.log(c / (w * L - c)) - np.log(p0 / (1 - p0))
for a, t in zip(ages, thr): print(f"  age {a:6.0f}: ln LR* = {t:.3f}")
print("  slope d lnLR*/d ln a (last 3 points):", np.polyfit(np.log(ages[-3:]), thr[-3:], 1)[0].round(3))
print("Regime A threshold is independent of age:", np.log(c/(w*L-c)) - np.log((1-np.exp(-lam*D))/np.exp(-lam*D)))
