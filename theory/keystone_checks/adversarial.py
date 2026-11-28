"""Adversarial search for a counterexample to N60's premise in Model S with J = 3 OU modes.
eps_3 = 0 exactly (three real stores realize the causal Wiener filter), so eps_K is convex on K = 1..3
iff r := eps_2/eps_1 <= 1/2. We maximize r over (tau ratios, variances, read noise).
E_K: stores.py's closed-form MSE, but store rates are kept >= 2% apart and the MSE is re-evaluated at the
returned rates (the #116 review's fix for the near-coincident-store bug, stores.py:39-50).
E_inf: Yovits-Jackson integral by adaptive quadrature. Run: nice -n 19 python3 adversarial.py"""
import numpy as np, json
from scipy.optimize import minimize
from scipy.integrate import quad
from multiprocessing import Pool
from stores import mse_given_b

def E_inf(a, v, N):
    S = lambda w: np.sum(v * 2 * a / (a**2 + w**2))
    f = lambda x: np.log1p(S(np.exp(x)) / N) * np.exp(x)
    lo = np.log(a.min()) - 14; hi = np.log(max(a.max(), np.sum(v*2*a)/N)) + 16
    e = np.linspace(lo, hi, 50)
    return N/np.pi*sum(quad(f, x0, x1, epsrel=1e-12, epsabs=0, limit=200)[0] for x0, x1 in zip(e[:-1], e[1:]))

def safe_b(x):
    x = np.sort(x)
    for i in range(1, len(x)):
        x[i] = max(x[i], x[i-1] + np.log(1.02))
    return np.exp(x)

def E_K(a, v, N, K, seed=0, starts=10):
    rng = np.random.default_rng(seed); la = np.log(a); lo, hi = la.min()-4, la.max()+7
    obj = lambda x: mse_given_b(a, v, safe_b(np.clip(x, -50, 50)), N)[0]
    best, bx = np.inf, None
    for x0 in [np.linspace(lo+2, hi-2, K)] + [np.sort(rng.uniform(lo, hi, K)) for _ in range(starts)]:
        r = minimize(obj, x0, method='Nelder-Mead', options=dict(xatol=1e-9, fatol=1e-15, maxiter=4000*K))
        if r.fun < best: best, bx = r.fun, r.x
    return mse_given_b(a, v, safe_b(bx), N)[0], np.sort(safe_b(bx))

def ratio(p):
    l21, l32, lv1, lv2, lv3, lN = p
    taus = np.exp(np.cumsum([0, abs(l21), abs(l32)])); a = 1/taus
    v = np.exp([lv1, lv2, lv3]); N = np.exp(lN)
    Ei = E_inf(a, v, N); E1 = E_K(a, v, N, 1)[0]; E2 = E_K(a, v, N, 2)[0]
    e1, e2 = E1/Ei - 1, E2/Ei - 1
    if e1 < 1e-3: return 0.0, e1, e2      # ignore worlds where layers do not matter
    return e2/e1, e1, e2

def climb(seed):
    rng = np.random.default_rng(seed)
    p0 = np.r_[rng.uniform(0.5, 5, 2), rng.uniform(-4, 4, 3), rng.uniform(-5, 2)]
    r = minimize(lambda p: -ratio(p)[0], p0, method='Nelder-Mead', options=dict(maxiter=250, xatol=1e-3, fatol=1e-5))
    rr, e1, e2 = ratio(r.x)
    l21, l32 = abs(r.x[0]), abs(r.x[1])
    return dict(seed=seed, r=rr, eps1=e1, eps2=e2, taus=list(np.exp(np.cumsum([0, l21, l32]))), v=list(np.exp(r.x[2:5])), N=float(np.exp(r.x[5])))

if __name__ == '__main__':
    with Pool(4) as pool:
        out = pool.map(climb, range(12))
    out.sort(key=lambda o: -o['r'])
    for o in out:
        print('r=%.4f eps1=%.4g eps2=%.4g taus=%s v=%s N=%.3g' % (o['r'], o['eps1'], o['eps2'], np.round(o['taus'], 2), np.round(o['v'], 4), o['N']))
    print('max eps2/eps1 = %.4f (non-convex iff > 0.5)' % out[0]['r'])
    json.dump(out, open('adversarial.json', 'w'), indent=1)
