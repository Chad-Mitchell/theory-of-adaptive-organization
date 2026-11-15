"""Independent re-implementation for AQN-REFEREE (does NOT import measurement/estimators/aqn.py).
Aliasing via the Hurwitz zeta function (exact), own Davies-Harte fGn, own Whittle and expected information."""
import numpy as np
from scipy.special import zeta, gamma
from scipy.optimize import minimize
TWO_PI = 2*np.pi

def alias_exact(w, a):
    x = w/TWO_PI
    return TWO_PI**(-a)*(zeta(a, x) + zeta(a, 1-x))

def fbm_incr_var_const(a):
    # increment variance of a process with S(w)=|w|^-a, var = (1/2pi) int S |1-e^{iw}|^2 dw  (numerical)
    from scipy.integrate import quad
    f = lambda w: w**(-a)*4*np.sin(w/2)**2
    v = 0
    for lo, hi in [(0,1),(1,50),(50,np.inf)]:
        v += quad(f, lo, hi, limit=400)[0]
    return 2*v/TWO_PI

def fgn_dh(n, H, rng):
    k = np.arange(0, n+1, dtype=float)
    g = 0.5*((k+1)**(2*H) - 2*k**(2*H) + np.abs(k-1)**(2*H))
    row = np.r_[g, g[n-1:0:-1]]
    lam = np.real(np.fft.fft(row)); lam[lam < 0] = 0
    M = row.size
    W = np.fft.fft(np.sqrt(lam/(2*M)) * (rng.standard_normal(M) + 1j*rng.standard_normal(M)))
    return np.sqrt(2)*W.real[:n]

def f_inc(w, lq, a, ls):
    return 4*np.sin(w/2)**2/TWO_PI*(np.exp(lq)*alias_exact(w, a) + np.exp(ls))

def pgram_incr(y):
    d = np.diff(y); n = d.size
    F = np.fft.fft(d - d.mean())
    j = np.arange(1, (n-1)//2 + 1)
    return TWO_PI*j/n, np.abs(F[j])**2/(TWO_PI*n)

def whittle(y, band=None, abounds=(1.01, 2.99)):
    w, I = pgram_incr(y)
    if band is not None:
        s = (w >= band[0]) & (w <= band[1]); w, I = w[s], I[s]
    def nll(p):
        f = f_inc(w, *p); return np.sum(np.log(f) + I/f)
    v = np.var(np.diff(y)); best = None
    for a0 in (1.5, 2.0, 2.5):
        for frac in (0.05, 0.5):
            x0 = [np.log(v*(1-frac)), a0, np.log(v*frac/2)]
            r = minimize(nll, x0, method="L-BFGS-B", bounds=[(x0[0]-30, x0[0]+30), abounds, (x0[2]-40, x0[2]+20)])
            if best is None or r.fun < best.fun: best = r
    th = best.x
    # expected information, analytic-free central differences
    G = []
    for i in range(3):
        e = np.zeros(3); e[i] = 1e-5
        G.append((np.log(f_inc(w, *(th+e))) - np.log(f_inc(w, *(th-e))))/2e-5)
    G = np.array(G); cov = np.linalg.inv(G @ G.T)
    return dict(lq=th[0], a=th[1], ls=th[2], se=np.sqrt(np.diag(cov)), nll=best.fun, m=w.size, w=w, I=I)
