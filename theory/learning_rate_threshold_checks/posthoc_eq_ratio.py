"""POST HOC (NOT preregistered): does the 2D threshold offset come from the fixed ratio L/n of the preregistered ladders?
Equilibrium strip judge, exact and cheap (precision = K, so only L x L blocks per transverse mode).
Fixed ladder L = (16, 32, 64); torus side n grows so L/n shrinks."""
import os, sys, numpy as np
from scipy.linalg import toeplitz
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from t67lib import coupling_vector, approach_exponent, p_crossing, ALPHA

def I_eq_strip(n, p, Ls):
    J = coupling_vector(2, n, p).reshape(n, n)
    Jh = np.fft.rfft(np.fft.fft(J, axis=0).real, axis=1).real  # axis0 k_x (full), axis1 k_y (0..n/2); J even so transforms are real
    out = np.zeros(len(Ls))
    for m in range(Jh.shape[1]):
        lam = (ALPHA + 1.0) - Jh[:, m]
        c = np.fft.ifft(1.0 / lam).real      # covariance along x for this k_y
        kx = np.fft.ifft(lam).real           # K along x for this k_y
        w = 1.0 if (m == 0 or m == n // 2) else 2.0
        for i, L in enumerate(Ls):
            S = toeplitz(c[:L]); Kk = toeplitz(kx[:L])
            out[i] += w * 0.5 * (np.linalg.slogdet(S)[1] + np.linalg.slogdet(Kk)[1])
    return out / (2 * n)

grid = [round(1.1 + 0.1 * i, 1) for i in range(15)]
for Ls in [(16, 32, 64), (8, 16, 32)]:
    for n in [512, 1024, 2048, 4096]:
        if n < 8 * Ls[-1]: continue
        ss = [approach_exponent(I_eq_strip(n, p, list(Ls))) for p in grid]
        pc = p_crossing(grid, ss)
        print(f"ladder {Ls} n={n} (L_max/n=1/{n//Ls[-1]}): p_c(I_EQ) = {pc['p_c']:.3f}  s(1.5) = {ss[4]:.4f}", flush=True)
