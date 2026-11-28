"""N12 referee, check 3: 'reset reads' with read noise. Periodic reads every T of x + eps, Var eps = s2, price c per read,
optimal linear (Gaussian-conditioning) predictor on the last M reads, fBm with Hurst H (alpha = 1+2H).
Exact reads (s2 = 0) are the N12 premise; any s2 > 0 is the realistic case. Onset solved as in check 2."""
import numpy as np, math, functools
from scipy import optimize, linalg

M = 200; S_PTS = (np.arange(16)+0.5)/16

@functools.lru_cache(maxsize=None)
def cov_parts(H):
    t0 = -M-1.0
    tk = np.arange(-M, 1, dtype=float)                     # read times (T = 1 units)
    K = lambda t, s: 0.5*(np.abs(t-t0)**(2*H) + np.abs(s-t0)**(2*H) - np.abs(t-s)**(2*H))
    Sxx = K(tk[:,None], tk[None,:]); Cs = K(tk[:,None], S_PTS[None,:]); Vs = K(S_PTS, S_PTS)
    return Sxx, Cs, Vs

def f_H(H, z):
    """time-averaged MSE over one read interval, in units q*T^(2H), read-noise ratio z = s2/(q T^2H)."""
    Sxx, Cs, Vs = cov_parts(H)
    L = linalg.cho_factor(Sxx + z*np.eye(len(Sxx)))
    return float(np.mean(Vs - np.sum(Cs*linalg.cho_solve(L, Cs), axis=0)))

def phi(W, q, H, s2, c=1.0):
    def obj(lT):
        T = math.exp(lT); scale = q*T**(2*H)
        return c/T + W*scale*f_H(H, s2/scale)
    return optimize.minimize_scalar(obj, bounds=(-40, 40), method='bounded', options={'xatol':1e-9}).fun

def onset(rho, H, s2):
    flat = phi(1.0, 1.0+rho, H, s2) - phi(1.0, 1.0, H, s2)
    G = lambda lN: math.exp(lN)*flat - phi(math.exp(lN), rho, H, s2)
    return math.exp(optimize.brentq(G, 1e-6, 50, xtol=1e-10))

if __name__ == "__main__":
    print("== validation at H=1/2 vs exact discrete Kalman (avg error = P+ + 1/2, P- = (1+sqrt(1+4z))/2) ==")
    for z in (0.0, 1e-3, 0.1, 1.0, 10.0):
        Pm = (1+math.sqrt(1+4*z))/2; Pp = Pm*z/(Pm+z) if z > 0 else 0.0
        print(f" z={z:<6} conditioning {f_H(0.5, z):.10f}  Kalman {Pp+0.5:.10f}")
    print(" M-convergence at H=0.75, z=1: M=200 ->", round(f_H(0.75,1.0),6))
    rhos = [10**(-k/2) for k in range(0, 9)]
    for s2 in (0.0, 1e-3):
        print(f"\n== read noise s2 = {s2} (member units: q_u = w = c = 1) ==")
        print(" H (alpha) | local slopes d ln N*/d ln rho between rho = 1, 10^-0.5, ..., 10^-4")
        for H in (0.25, 0.5, 0.75):
            Ns = [onset(r, H, s2) for r in rhos]
            sl = [math.log(Ns[i+1]/Ns[i])/math.log(rhos[i+1]/rhos[i]) for i in range(len(rhos)-1)]
            print(f" {H} ({1+2*H}) | " + " ".join(f"{s:+.3f}" for s in sl) + " | N* at rho=1e-4: %.3g" % Ns[-1], flush=True)
