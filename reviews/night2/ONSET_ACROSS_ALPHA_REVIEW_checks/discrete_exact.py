"""Reviewer check 1 (own code, imports nothing from tests/ONSET_ACROSS_ALPHA).
Exact *expected* discrete-time onset with integer read intervals, no simulation noise:
reset read every T steps, random phase, drift increments Var = q*tau^(alpha-1) (exact for discrete fBm at integer lags)
=> E[mse](T) = q * (1/T) * sum_{tau=0}^{T-1} tau^(alpha-1).
flat per member: min_T C/T + (1+rho) m(T); levelled per member: min_T [C/(N T) + rho m(T)] + min_T [C/T + m(T)].
Also the continuous closed form (own derivation): onset N^(1/a-1) rho^(1/a) = (1+rho)^(1/a) - 1.
Reports window OLS exponents over rho in {.01..0.32} for a sweep of C (bias from per-alpha read cost / discreteness)."""
import numpy as np, json
from scipy.optimize import brentq
R = np.array([0.01, 0.02, 0.04, 0.08, 0.16, 0.32])
Tmax = 20000
def mcurve(alpha):
    t = np.arange(Tmax, dtype=float)
    return np.cumsum(t ** (alpha - 1)) / np.arange(1, Tmax + 1)   # index T-1 -> m(T)
def opt(Cw, m):   # min over integer T of Cw/T + m(T)  (Cw = C/W, cost per unit stake)
    T = np.arange(1, Tmax + 1)
    return np.min(Cw / T + m)
def onset_discrete(alpha, rho, C, m):
    flat = opt(C / (1 + rho), m) * (1 + rho)
    mem = opt(C, m)
    f = lambda lnN: (opt(C / (np.exp(lnN) * rho), m) * rho + mem) - flat   # levelled - flat (per member)
    # levelled - flat decreasing in N; find root on wide bracket
    a, b = np.log(1.0001), np.log(1e9)
    if f(a) * f(b) > 0: return float('nan')   # no onset (degenerate: T = 1 everywhere)
    return float(np.exp(brentq(f, a, b, xtol=1e-10)))
def onset_cont(alpha, rho):
    a = 1 / alpha
    return float(np.exp(brentq(lambda x: (a - 1) * x + a * np.log(rho) - np.log((1 + rho) ** a - 1), -20, 40)))
out = {}
for alpha in (1.5, 2.0, 2.5):
    m = mcurve(alpha)
    ec = np.polyfit(np.log(R), np.log([onset_cont(alpha, r) for r in R]), 1)[0]
    row = dict(cont_exponent=round(ec, 4), cont_Nstar=[round(onset_cont(alpha, r), 2) for r in R])
    sweep = {}
    for C in [1, 5, 20, 84.3, 300, 800, 2000, 6072, 2e4, 1e5]:
        Tlone = int(np.argmin(C / np.arange(1, Tmax + 1) + m) + 1)
        Ns = [onset_discrete(alpha, r, C, m) for r in R]
        sweep[str(C)] = dict(T_lone=Tlone, exponent=(round(float(np.polyfit(np.log(R), np.log(Ns), 1)[0]), 4) if np.all(np.isfinite(Ns)) else None),
                             Nstar=[round(x, 2) for x in Ns])
    row['discrete'] = sweep
    out[str(alpha)] = row
for a in out:
    print(a, 'cont', out[a]['cont_exponent'])
    for C, v in out[a]['discrete'].items(): print('   C', C, 'Tlone', v['T_lone'], 'e', v['exponent'])
e15 = out['1.5']['discrete']['84.3']['exponent']; e25 = out['2.5']['discrete']['6072']['exponent']
out['delta_at_author_C'] = round(e25 - e15, 4)
print('discrete-exact Delta at author C:', out['delta_at_author_C'])
json.dump(out, open('discrete_exact.json', 'w'), indent=1)
