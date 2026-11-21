"""Layers (K first-order stores) vs flat (K=1) for a Gaussian world seen in white noise.
World: s = sum_j OU components, autocov v_j exp(-a_j|t|); observation y = s + white noise (density N).
Agent: causal LTI filter H = sum_k g_k b_k/(b_k + i w)  (K parallel exponential stores / trackers at rates b_k).
E_K = min over (b,g) of MSE; E_inf = causal MMSE (Yovits-Jackson). Everything in closed form except the
outer minimisation over b (multi-start, log-parametrised).  Run: nice -n 19 python3 stores.py
"""
import numpy as np, itertools, json, sys
from scipy.optimize import minimize
from scipy.integrate import quad

def mats(a, v, b, N):
    a = np.asarray(a, float); v = np.asarray(v, float)
    a3 = a[:, None, None]; v3 = v[:, None, None]
    bk = b[None, :, None]; bl = b[None, None, :]
    # E[(phi_k*s)(phi_l*s)] for OU comps, plus noise part
    Ms = (v3 * bk * bl / (bk + bl) * (1/(a3 + bk) + 1/(a3 + bl))).sum(0)
    Mn = N * b[:, None] * b[None, :] / (b[:, None] + b[None, :])
    r = (v[:, None] * b[None, :] / (a[:, None] + b[None, :])).sum(0)
    return Ms + Mn, r

def mse_given_b(a, v, b, N):
    M, r = mats(a, v, b, N)
    try:
        g = np.linalg.solve(M, r)
    except np.linalg.LinAlgError:
        g = np.linalg.lstsq(M, r, rcond=None)[0]
    return float(np.sum(v) - r @ g), g

def E_inf(a, v, N):
    a = np.asarray(a); v = np.asarray(v)
    S = lambda w: np.sum(v * 2 * a / (a**2 + w**2))
    # (N/pi) int_0^inf ln(1+S/N) dw, on log scale
    f = lambda x: np.log1p(S(np.exp(x)) / N) * np.exp(x)
    lo, hi = np.log(a.min()) - 12, np.log(max(a.max(), np.sum(v*2*a)/N)) + 14
    xs = np.linspace(lo, hi, 20001)
    vals = np.array([f(x) for x in xs])
    return float(N / np.pi * np.trapezoid(vals, xs))

def E_K(a, v, N, K, starts=12, rng=None):
    rng = rng or np.random.default_rng(0)
    la = np.log(np.asarray(a)); lo, hi = la.min() - 3, la.max() + 6
    best = (np.inf, None)
    obj = lambda x: mse_given_b(a, v, np.exp(np.sort(x)) * (1 + 1e-9*np.arange(K)), N)[0]
    inits = [np.linspace(lo + 2, hi - 2, K)] + [np.sort(rng.uniform(lo, hi, K)) for _ in range(starts)]
    for x0 in inits:
        res = minimize(obj, x0, method='Nelder-Mead', options=dict(xatol=1e-7, fatol=1e-13, maxiter=4000*K))
        if res.fun < best[0]:
            best = (res.fun, np.sort(res.x))
    return best

def scalefree_world(alpha, span, per_decade=8, tau_min=1.0):
    """Lorentzian mixture over log-span: tau log-uniform in [tau_min, tau_min*span], v ∝ tau^(alpha-1).
    Spectrum ~ f^-alpha inside the band (0<alpha<2). Total variance normalised to 1."""
    J = max(2, int(round(per_decade * np.log10(span))) + 1)
    tau = tau_min * np.logspace(0, np.log10(span), J)
    v = tau ** (alpha - 1); v /= v.sum()
    return 1 / tau, v

def check_formulas():
    out = {}
    # 1) single OU: K=1 equals Kalman P = N(sqrt(a^2+2av/N) - a)  [q = 2 a v]
    a, v, N = 0.3, 1.0, 0.05
    P = N * (np.sqrt(a*a + 2*a*v/N) - a)
    e1 = E_K([a], [v], N, 1)[0]; ei = E_inf([a], [v], N)
    out['OU_single'] = dict(kalman=P, E1=e1, Einf_YJ=ei)
    # 2) Monte-Carlo check of the covariance formula for two stores on a two-OU world
    rng = np.random.default_rng(1); dt = 0.01; T = 400000
    aa = np.array([1.0, 0.02]); vv = np.array([0.5, 0.5]); bb = np.array([2.0, 0.1]); g = np.array([0.4, 0.5])
    s = np.zeros(2); f = np.zeros(2); se = 0.0; n = 0
    for t in range(T):
        s = s * np.exp(-aa*dt) + np.sqrt(vv*(1-np.exp(-2*aa*dt))) * rng.standard_normal(2)
        y = s.sum() + np.sqrt(N/dt) * rng.standard_normal()
        f = f + bb*dt*(y - f)
        if t > 20000:
            se += (s.sum() - g @ f)**2; n += 1
    M, r = mats(aa, vv, bb, N)
    out['MC_two_store'] = dict(mc=se/n, formula=float(vv.sum() - 2*g@r + g@M@g))
    return out

if __name__ == '__main__':
    res = {'formula_checks': check_formulas()}
    print(json.dumps(res['formula_checks'], indent=1)); sys.stdout.flush()
    json.dump(res, open('stores_checks.json', 'w'), indent=1)
