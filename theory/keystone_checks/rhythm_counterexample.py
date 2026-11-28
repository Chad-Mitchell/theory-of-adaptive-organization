"""Worked counterexample: N60's count formula can fail in M_LG when the world has rhythms
and stores are first-order (real poles). Outside Model S (sums of OU modes).

World: two lightly damped oscillators (seed 2 of convexity_wide.py, class C).
Cost J_K = K + R(1 + eps_K), eps_K = E_K/E_inf - 1.
N60(ii) says K* = 1 + #{k>=2: R(eps_{k-1}-eps_k)>1} if eps is convex decreasing.
Here the decrements are not monotone, and at R=3 the formula returns 2 while argmin is 3.

Run: nice -n 19 python3 rhythm_counterexample.py
Uses the same MSE and the #116 optimizer fix (stores kept >= 2% apart; MSE re-evaluated).
"""
import json, numpy as np
from scipy.optimize import minimize
from scipy.integrate import quad

# seed 2 of convexity_wide.py (class C: two rhythms)
a = np.array([0.015043913155370778+0.8245963835269933j,
              0.015043913155370778-0.8245963835269933j,
              0.005596688432223706+0.05512283118769611j,
              0.005596688432223706-0.05512283118769611j])
v = np.array([0.16591255090832438, 0.16591255090832438,
              0.1809360888442601,  0.1809360888442601], dtype=complex)
N = 0.04014640614993535

def mats(a, v, b, N):
    a3 = a[:, None, None]; v3 = v[:, None, None]
    bk = b[None, :, None]; bl = b[None, None, :]
    Ms = np.real((v3 * bk * bl / (bk + bl) * (1/(a3 + bk) + 1/(a3 + bl))).sum(0))
    Mn = N * b[:, None] * b[None, :] / (b[:, None] + b[None, :])
    r  = np.real((v[:, None] * b[None, :] / (a[:, None] + b[None, :])).sum(0))
    return Ms + Mn, r

def mse(b):
    M, r = mats(a, v, b, N)
    try: g = np.linalg.solve(M, r)
    except np.linalg.LinAlgError: g = np.linalg.lstsq(M, r, rcond=None)[0]
    return float(np.real(np.sum(v)) - r @ g)

def safe_b(x):
    x = np.sort(np.clip(x, -40, 40))
    for i in range(1, len(x)):
        x[i] = max(x[i], x[i-1] + np.log(1.02))
    return np.exp(x)

def E_K(K, starts=16, seed=0):
    rng = np.random.default_rng(seed)
    la = np.log(np.abs(a)); lo, hi = la.min()-4, la.max()+7
    obj = lambda x: mse(safe_b(x))
    best, bx = np.inf, None
    inits = [np.linspace(lo+2, hi-2, K)] + [np.sort(rng.uniform(lo, hi, K)) for _ in range(starts)]
    for x0 in inits:
        r = minimize(obj, x0, method='Nelder-Mead',
                     options=dict(xatol=1e-9, fatol=1e-15, maxiter=6000*K))
        if r.fun < best: best, bx = r.fun, r.x
    return mse(safe_b(bx)), np.sort(safe_b(bx))

def E_inf():
    S = lambda w: float(np.real(np.sum(v * 2 * a / (a**2 + w**2))))
    f = lambda x: np.log1p(max(S(np.exp(x)), 0)/N) * np.exp(x)
    lo = np.log(np.abs(a).min())-14
    hi = np.log(max(np.abs(a).max(), np.real(np.sum(v))*2*np.abs(a).max()/N))+16
    e = np.linspace(lo, hi, 60)
    return N/np.pi * sum(quad(f, x0, x1, epsrel=1e-11, epsabs=0, limit=200)[0]
                         for x0, x1 in zip(e[:-1], e[1:]))

if __name__ == '__main__':
    ei = E_inf()
    E, B = [], []
    for K in range(1, 5):
        e, b = E_K(K); E.append(e); B.append(b.tolist())
    E = list(np.minimum.accumulate(E))
    ei = min(ei, E[-1])
    eps = [e/ei - 1 for e in E]
    dec = [eps[k]-eps[k+1] for k in range(3)]
    R = 3.0
    J = [K + R*(1+eps[K-1]) for K in range(1,5)]
    kstar = int(np.argmin(J)+1)
    formula = 1 + sum(1 for k in range(2,5) if R*(eps[k-2]-eps[k-1]) > 1)
    out = dict(world='two lightly damped oscillators (outside Model S)',
               N=N, E=E, E_inf=ei, eps=eps, decrements=dec,
               R=R, J_at_R=J, argmin=kstar, formula=formula,
               mismatch=kstar!=formula, stores=B)
    print(json.dumps({k: ( [round(x,5) if isinstance(x,float) else x for x in v]
                           if isinstance(v, list) and v and isinstance(v[0], float) else v)
                      for k,v in out.items() if k!='stores'}, indent=2))
    print('decrements not monotone:', dec[1] > dec[0])
    print('at R=%.1f: argmin K*=%d, N60 formula=%d, mismatch=%s' % (R, kstar, formula, kstar!=formula))
    json.dump(out, open('rhythm_counterexample.json','w'), indent=1)
