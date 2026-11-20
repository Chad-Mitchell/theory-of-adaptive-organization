"""T7b beyond alpha=2: items log-uniform over log-span L share K clocks; relative penalty of running an item at
k*T* is p(u)=[(alpha-1)e^{-u}+e^{(alpha-1)u}]/alpha-1, u=ln k (THEORY CT13). Claim: psi(D)=min_y int_0^D p(x-y)dx is
convex, so equal log-widths (geometric levels) are optimal for every alpha in (1,3). Check: optimise widths directly.
Run: nice -n 19 python3 t7b_alpha.py > t7b_alpha.out"""
import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.integrate import quad
def psi(D, al):
    p = lambda u: ((al-1)*np.exp(-u)+np.exp((al-1)*u))/al - 1
    f = lambda y: quad(lambda x: p(x-y), 0, D)[0]
    return minimize_scalar(f, bounds=(0, D), method='bounded').fun
for al in [1.2, 1.5, 2.0, 2.5, 2.9]:
    for L, K in [(np.log(1e3), 3), (np.log(1e5), 5)]:
        tot = lambda w: sum(psi(d, al) for d in L*np.exp(w)/np.exp(w).sum())
        res = min((minimize(tot, np.random.default_rng(s).normal(0, .5, K), method='Nelder-Mead',
                            options=dict(xatol=1e-6, fatol=1e-12, maxiter=3000)) for s in range(3)), key=lambda r: r.fun)
        D = L*np.exp(res.x)/np.exp(res.x).sum()
        eq = sum(psi(L/K, al) for _ in range(K))
        print(f"alpha={al} span=e^{L:.1f} K={K}: optimal widths/equal = {np.round(D/(L/K),4)}  cost opt/equal = {res.fun/eq:.6f}")
# convexity of psi on a grid
for al in [1.2, 1.5, 2.5, 2.9]:
    Ds = np.linspace(0.1, 6, 60); ps = np.array([psi(d, al) for d in Ds])
    print(f"alpha={al}: min second difference of psi on grid = {np.min(np.diff(ps, 2)):.3e} (>=0 means convex)")
