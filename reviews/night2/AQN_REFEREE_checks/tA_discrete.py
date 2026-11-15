"""Own discrete-time check of the plug-in t_A = (N/2mu^2)[ln(2mu^2/(lam N)) - gamma - 1], N = s2*dt, dt = 1, on the
block-C cells. Discrete two-state HMM filter (exact forward recursion, flip prob p = (1-e^{-2 lam})/2), levels +-mu
(mu = 1), noise sd sigma. After a long run in state -1, force a switch to +1 at a random time; t_A_disc = mean number of
steps until the filtered log-odds first crosses 0 (posterior favours the new state). Mean over many switches."""
import numpy as np
EG = 0.5772156649
def run(sig, lam, nsw=4000, seed=7):
    rng = np.random.default_rng(seed); p = (1-np.exp(-2*lam))/2; mu = 1.0
    out = []
    for k in range(nsw):
        # burn-in in state -1 long enough for the log-odds to reach its stationary resting distribution
        # (conditioned on no switch: we keep the state fixed, as the formula's derivation does)
        L = 0.0
        for t in range(int(3/lam) if lam > 0.005 else 1500):
            y = -mu + sig*rng.standard_normal()
            Lp = np.log(((1-p)*np.exp(L) + p)/(p*np.exp(L) + (1-p)))   # prior log-odds (+1 vs -1)
            L = Lp + 2*mu*y/sig**2
        n = 0
        while True:
            y = mu + sig*rng.standard_normal(); n += 1
            Lp = np.log(((1-p)*np.exp(L) + p)/(p*np.exp(L) + (1-p)))
            L = Lp + 2*mu*y/sig**2
            if L > 0: break
        out.append(n)
    return np.mean(out), np.std(out)/np.sqrt(nsw)
if __name__ == "__main__":
      for sig in (0.5, 1.5, 3.0):
        for lam in (0.002, 0.01):
            N = sig**2; f = N/2*(np.log(2/(lam*N)) - EG - 1)
            m, se = run(sig, lam, nsw=1500)
            print(f"sigma {sig} lam {lam}: plug-in t_A {f:6.2f} steps; discrete filter crossing time {m:6.2f} +- {se:.2f}; ratio {m/f:.2f}")
