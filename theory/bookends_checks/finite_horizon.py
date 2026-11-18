"""BOOKENDS §2.0 finite-horizon corollary check (i.i.d. bounded increments).
Blind reserve: R_t = B + sum_{s<=t} D_s, E[D_s] = -delta, |D_s + delta| <= b.
Claim: P(survive to T) <= P(R_T > 0) <= exp(-(delta*T - B)^2 / (2 b^2 T)) for T > B/delta (Azuma-Hoeffding)."""
import numpy as np
rng = np.random.default_rng(1)
B, delta, b, n = 5.0, 0.05, 1.0, 100000
for T in [200, 400, 800, 1600]:
    D = rng.choice([-b, b], size=(n, T)) - delta          # mean -delta, |D+delta| = b
    R = B + np.cumsum(D, axis=1)
    surv = np.mean((R > 0).all(axis=1))
    endpos = np.mean(R[:, -1] > 0)
    bound = np.exp(-(delta*T - B)**2 / (2*b*b*T))
    print(f"T={T:5d}  P(survive)={surv:.4f}  P(R_T>0)={endpos:.4f}  bound={bound:.4f}  ok={surv<=bound+1e-3}")
