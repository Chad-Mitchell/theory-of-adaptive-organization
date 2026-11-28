"""Wider search for non-convex eps_K inside the linear-Gaussian class (M_LG), first-order real stores.
World autocovariance C(t) = Re sum_j v_j exp(-a_j |t|), a_j possibly complex (conjugate pairs = rhythms),
v_j possibly negative (smooth worlds), subject to S(w) >= 0. Stores: H = sum g_k b_k/(b_k + i w), b_k > 0.
MSE(b) closed form (stores.py generalised to complex a: formulas are linear in each (v_j, a_j) term).
E_inf: Yovits-Jackson (N/pi) int_0^inf ln(1+S/N) dw with adaptive quadrature on log-w.
Classes: A clustered OU, B rhythm + OU, C two rhythms, D smooth (OU through a low-pass), E OU with huge variance contrast.
Run: nice -n 19 python3 convexity_wide.py N"""
import numpy as np, json, sys
from multiprocessing import Pool
from scipy.optimize import minimize
from scipy.integrate import quad
KMAX = 4

def mats(a, v, b, N):
    a3 = a[:, None, None]; v3 = v[:, None, None]; bk = b[None, :, None]; bl = b[None, None, :]
    Ms = np.real((v3 * bk * bl / (bk + bl) * (1/(a3 + bk) + 1/(a3 + bl))).sum(0))
    Mn = N * b[:, None] * b[None, :] / (b[:, None] + b[None, :])
    r = np.real((v[:, None] * b[None, :] / (a[:, None] + b[None, :])).sum(0))
    return Ms + Mn, r

def var0(v): return float(np.real(np.sum(v)))

def mse(a, v, b, N):
    M, r = mats(a, v, b, N)
    try: g = np.linalg.solve(M, r)
    except np.linalg.LinAlgError: g = np.linalg.lstsq(M, r, rcond=None)[0]
    return var0(v) - r @ g

def S(w, a, v): return float(np.real(np.sum(v * 2 * a / (a**2 + w**2))))

def E_inf(a, v, N):
    f = lambda x: np.log1p(max(S(np.exp(x), a, v), 0) / N) * np.exp(x)
    lo = np.log(np.abs(a).min()) - 14; hi = np.log(max(np.abs(a).max(), var0(np.abs(v))*2*np.abs(a).max()/N)) + 16
    edges = np.linspace(lo, hi, 60); tot = 0.0
    for x0, x1 in zip(edges[:-1], edges[1:]):
        tot += quad(f, x0, x1, epsabs=0, epsrel=1e-11, limit=200)[0]
    return N / np.pi * tot

def safe_b(x):
    x = np.sort(np.clip(x, -40, 40))
    for i in range(1, len(x)):
        x[i] = max(x[i], x[i-1] + np.log(1.02))   # keep stores >= 2% apart (#116 review fix)
    return np.exp(x)

def E_K(a, v, N, K, rng, starts=8):
    la = np.log(np.abs(a)); lo, hi = la.min() - 3, la.max() + 6
    obj = lambda x: mse(a, v, safe_b(x), N)
    best, bx = np.inf, None
    for x0 in [np.linspace(lo + 2, hi - 2, K)] + [np.sort(rng.uniform(lo, hi, K)) for _ in range(starts)]:
        res = minimize(obj, x0, method='Nelder-Mead', options=dict(xatol=1e-8, fatol=1e-14, maxiter=5000*K))
        if res.fun < best: best, bx = res.fun, res.x
    return mse(a, v, safe_b(bx), N)                 # re-evaluated at the returned rates

def world(seed):
    rng = np.random.default_rng(5000 + seed); cls = 'ABCDE'[seed % 5]
    if cls == 'A':   # clustered OU: groups of close rates
        taus = np.sort(np.r_[10**rng.uniform(0, .5, 2), 10**rng.uniform(1.5, 2, 2)]); v = 10**rng.uniform(-1, 1, 4); a = 1/taus + 0j
    elif cls == 'B': # rhythm + slow and fast OU
        g, w0 = 10**rng.uniform(-2.5, -1), 10**rng.uniform(-1.5, 0); vr = 10**rng.uniform(-1, 1)
        a = np.array([g + 1j*w0, g - 1j*w0, 1/10**rng.uniform(2.5, 3.5), 1/10**rng.uniform(-1, 0)])
        v = np.array([vr/2, vr/2, 10**rng.uniform(-1, 1), 10**rng.uniform(-1, 1)]) + 0j
    elif cls == 'C': # two rhythms
        a, v = [], []
        for _ in range(2):
            g, w0 = 10**rng.uniform(-2.5, -1), 10**rng.uniform(-2, 0.5); vr = 10**rng.uniform(-1, 1)
            a += [g + 1j*w0, g - 1j*w0]; v += [vr/2, vr/2]
        a = np.array(a); v = np.array(v) + 0j
    elif cls == 'D': # OU (rate p) through low-pass (rate c): autocov  prop to  c e^{-p t}/(c^2-p^2)*... use partial fractions of S
        p, c = 1/10**rng.uniform(1, 3), 1/10**rng.uniform(-0.5, 0.5); q = 10**rng.uniform(-1, 1)
        # S(w) = q c^2/((p^2+w^2)(c^2+w^2)) = q c^2/(c^2-p^2) [1/(p^2+w^2) - 1/(c^2+w^2)]
        k = q*c*c/(c*c - p*p); a = np.array([p, c, 1/10**rng.uniform(3, 4)]) + 0j
        v = np.array([k/(2*p), -k/(2*c), 10**rng.uniform(-1, 1)]) + 0j
    else:            # E: OU with huge variance contrast
        taus = np.cumprod(np.r_[1, 10**rng.uniform(.5, 1.5, 3)]); v = 10**rng.uniform(-3, 3, 4); a = 1/taus + 0j
    N = 10**rng.uniform(-2.5, 0.5)
    return cls, a.astype(complex), v.astype(complex), N

def run(seed):
    cls, a, v, N = world(seed); rng = np.random.default_rng(11)
    ei = E_inf(a, v, N)
    E = list(np.minimum.accumulate([E_K(a, v, N, K, rng) for K in range(1, KMAX+1)]))
    ei = min(ei, E[-1])
    eps = [e/ei - 1 for e in E]
    dec = [eps[k]-eps[k+1] for k in range(KMAX-1)]
    viol = [k+1 for k in range(len(dec)-1) if dec[k+1] - dec[k] > max(1e-4, 0.02*abs(dec[k]))]
    return dict(seed=seed, cls=cls, a=[str(x) for x in a], v=[str(x) for x in v], N=N, eps=eps, dec=dec, viol=viol)

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    out = []
    with Pool(6) as p:
        for o in p.imap_unordered(run, range(n)):
            out.append(o); print('done', o['seed'], o['cls'], 'eps', np.round(o['eps'], 5), 'viol', o['viol'], flush=True)
            json.dump(out, open('convexity_wide.json', 'w'), indent=1)
    for c in 'ABCDE':
        oc = [o for o in out if o['cls'] == c]
        print(c, 'worlds', len(oc), 'non-convex', sum(1 for o in oc if o['viol']))
    for o in [o for o in out if o['viol']][:15]:
        print(o['seed'], o['cls'], 'N=%.3g' % o['N'], 'eps', np.round(o['eps'], 4), 'dec', np.round(o['dec'], 4), 'viol at k=', o['viol'])
    json.dump(out, open('convexity_wide.json', 'w'), indent=1)
