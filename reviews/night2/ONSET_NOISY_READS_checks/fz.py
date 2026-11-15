"""ONSET-NOISY-READS check 1 (own code). Time-averaged MSE f_alpha(z) of the optimal linear predictor of fBm
(Var increments q|dt|^{2H}, alpha = 1+2H) from noisy periodic reads every T (noise var s2), in units q T^{alpha-1},
z = s2/(q T^{alpha-1}). Built by Gaussian conditioning on the last M reads via one eigendecomposition per (H, M).
Checks: H=1/2 vs exact discrete Kalman; M-convergence; z->inf asymptote f ~ g z^{1-1/alpha},
g = (Gamma(alpha) sin(pi(alpha-1)/2))^{1/alpha} / sin(pi/alpha) (Yovits-Jackson for S = q C/|w|^alpha)."""
import numpy as np, math, functools, json, sys
from scipy import linalg
NS = 32; SP = (np.arange(NS)+0.5)/NS

@functools.lru_cache(maxsize=None)
def basis(H, M):
    t0 = -M-1.0; tk = np.arange(-M, 1, dtype=float)
    K = lambda t, s: 0.5*(np.abs(t-t0)**(2*H) + np.abs(s-t0)**(2*H) - np.abs(t-s)**(2*H))
    S = K(tk[:, None], tk[None, :]); C = K(tk[:, None], SP[None, :]); V = np.diag(K(SP[:, None], SP[None, :]))
    lam, U = linalg.eigh(S); P = (U.T @ C)**2
    return lam, P, V, S, C

def f(H, z, M=1000):
    lam, P, V, S, C = basis(H, M)
    if z < 1e-6:  # exact or near-exact reads: direct Cholesky (ill-conditioned spectrum)
        L = linalg.cho_factor(S + z*np.eye(len(S)) + 1e-12*np.eye(len(S)))
        return float(np.mean(V - np.sum(C*linalg.cho_solve(L, C), axis=0)))
    return float(np.mean(V - (P/(lam[:, None]+z)).sum(0)))

def g(alpha):
    return (math.gamma(alpha)*math.sin(math.pi*(alpha-1)/2))**(1/alpha)/math.sin(math.pi/alpha)

if __name__ == "__main__":
    out = {}
    print("== H=1/2 vs discrete Kalman: f = P+ + 1/2, P- = (1+sqrt(1+4z))/2, P+ = P- z/(P-+z) ==")
    for z in (0.0, 1e-3, 0.1, 1.0, 10.0, 1e3):
        Pm = (1+math.sqrt(1+4*z))/2; Pp = Pm*z/(Pm+z)
        print(f" z={z:<7g} cond {f(0.5, z):.10f}  Kalman {Pp+0.5:.10f}")
    for H in (0.25, 0.5, 0.75):
        a = 1+2*H; b = 1-1/a
        print(f"\n== H={H} alpha={a}: g_closed={g(a):.6f}")
        for M in (500, 1000, 2000):
            print(f"  M={M}: f(0)={f(H,0,M):.6f} f(1)={f(H,1,M):.6f} f(1e3)/z^b={f(H,1e3,M)/1e3**b:.6f} f(1e5)/z^b={f(H,1e5,M)/1e5**b:.6f}", flush=True)
        out[str(a)] = {"f0_M2000": f(H, 0, 2000), "g_closed": g(a),
                       "ratio": {str(z): f(H, z, 2000)/z**b for z in (1e2, 1e3, 1e4, 1e5, 1e6)}}
        print("  M=2000 f/(g z^b) at z=1e2..1e6:", [round(f(H, z, 2000)/(g(a)*z**b), 5) for z in (1e2, 1e3, 1e4, 1e5, 1e6)])
    json.dump(out, open("fz.json", "w"), indent=1)
