"""Acting ahead: predict s(t+k) from noisy past. Flat (1 store) vs layered (K stores) vs exact Kalman (J states).
Exact optimum via the continuous ARE.  Run: nice -n 19 python3 lead.py > lead.out"""
import numpy as np
from scipy.linalg import solve_continuous_are
from scipy.optimize import minimize
from stores import mats, scalefree_world

def E_opt(a, v, N, k):
    a = np.asarray(a, float); v = np.asarray(v, float); J = len(a)
    A = -np.diag(a); Q = np.diag(2*a*v); C = np.ones((1, J))
    P = solve_continuous_are(A.T, C.T, Q, np.array([[N]]))
    E = np.exp(-a*k)
    return float(E @ P @ E + np.sum(v*(1-np.exp(-2*a*k))))

def E_K_lead(a, v, N, K, k, starts=12, seed=0):
    a = np.asarray(a, float); v = np.asarray(v, float); rng = np.random.default_rng(seed)
    def f(x):
        b = np.exp(np.clip(np.sort(x),-30,10))*(1+1e-6*np.arange(K))
        M, _ = mats(a, v, b, N)
        r = (v[:, None]*np.exp(-a*k)[:, None]*b[None, :]/(a[:, None]+b[None, :])).sum(0)
        if not np.all(np.isfinite(M)): return 1e9
        try: g = np.linalg.lstsq(M, r, rcond=None)[0]
        except np.linalg.LinAlgError: return 1e9
        return float(v.sum() - r@g)
    la = np.log(a); lo, hi = la.min()-3, la.max()+6
    best = np.inf
    for x0 in [np.linspace(lo+2, hi-2, K)] + [np.sort(rng.uniform(lo, hi, K)) for _ in range(starts)]:
        res = minimize(f, x0, method='Nelder-Mead', options=dict(xatol=1e-7, fatol=1e-13, maxiter=4000*K))
        best = min(best, res.fun)
    return best

def fast_edge_noise(a, v):
    a = np.asarray(a); return float(np.sum(v*2*a/(a**2+a.max()**2)))

if __name__ == "__main__":
    print("Excess of K-store designs over the exact optimum, as % of the optimum, at lead k (time units: fastest tau = 1)")
    print("\n-- cadence world, tau = 1, 30, 1000, equal variance --")
    a = 1/np.array([1., 30., 1000.]); v = np.ones(3)/3; N = 0.1*fast_edge_noise(a, v)
    for k in [0, 1, 10, 100, 300]:
        eo = E_opt(a, v, N, k); ex = [E_K_lead(a, v, N, K, k)/eo - 1 for K in (1, 2, 3)]
        print(f" k={k:>4}: opt MSE={eo:.4f} (blind=1)  excess% K=1,2,3: {np.round(np.array(ex)*100,3)}")
    print("\n-- two modes tau=1 and 1000, equal variance --")
    a = 1/np.array([1., 1000.]); v = np.array([.5, .5]); N = 0.1*fast_edge_noise(a, v)
    for k in [0, 1, 3, 10, 100]:
        eo = E_opt(a, v, N, k); ex = [E_K_lead(a, v, N, K, k)/eo - 1 for K in (1, 2)]
        print(f" k={k:>4}: opt MSE={eo:.4f}  excess% K=1,2: {np.round(np.array(ex)*100,3)}")
    print("\n-- scale-free band alpha=1, span 1e4 (33 modes), exact optimum = 33-state Kalman --")
    a, v = scalefree_world(1.0, 1e4); N = fast_edge_noise(a, v)
    for k in [0, 3, 30, 300]:
        eo = E_opt(a, v, N, k); ex = [E_K_lead(a, v, N, K, k)/eo - 1 for K in (1, 2, 3, 4)]
        print(f" k={k:>4}: opt MSE={eo:.4f}  excess% K=1..4: {np.round(np.array(ex)*100,3)}")
