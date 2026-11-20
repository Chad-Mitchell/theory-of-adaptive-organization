"""The face-figure model world, computed from J (no hand-drawn boundaries).
nice -n 19 python3 figures/face_model.py     (about 10-20 minutes on 6 cores; writes figures/face_tables.json)

WORLD (illustrative, one made-up spectrum): J0 = 14 non-oscillating (real-pole) OU modes with time scales
tau_j = 10^(j/2), j = 0..13 (two per decade, 1 to ~3e6 in units of the fastest, tau_fast = 1), equal variance v_j = 1/14, so the
spectrum is about 1/f across the band (alpha = 1) and Var = 1.  The world is seen through white noise of density N.
DESIGN: K = 0 (blind, error Var) or K first-order stores (K layers) at rates b_k chosen optimally, acting at lead l (the latency).
  E_K(N, l) = min_b MSE of the best K-store linear estimator of s(t+l) (same code as theory/layers_checks/lead.py).
  K = J0 = 14 is the exact optimum (McMillan degree, L2).  For real-pole worlds, store count = degree count (rhythms would count 2 each).
J (per unit time), the master-equation cost with its terms booked:
  J(K, N, l) = h*K + w*E_K(N, l) + c0/N        upkeep + error stake + sensing (a price on reading precision, 1/N)
  K = 0:  J = w*Var   (no sensing, no layers)
  SENSING OPTIMIZED: N is chosen in [N_MIN, N_MAX] to minimize J, for each K, w, l (this is what the figure shows; the fixed-sensing
  variant fixes N = N_FIX and is also tabulated).
FEDERATION: split into semi-independent units each reading locally (lead 0), at a fixed overhead hf:
  J_fed(K, N) = hf + h*K + w*E_K(N, 0) + c0/N.
The best design at (w, l) is the argmin over {K = 0, central K = 1..KMAX, federated K = 1..KMAX}.  Nothing else (no income cap,
no 'not viable' region: with no ruin constraint binding and no fixed income, every stake level has a best design).
Axes: R = w*Var/h (stakes over upkeep) and l/tau_fast.  Free parameters of the model world: c0/h, hf/h, N range, the spectrum."""
import os, sys, json, time
import numpy as np
from multiprocessing import Pool
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'theory', 'layers_checks'))
from stores import mats
from lead import E_opt

J0 = 14
TAU = 10 ** (np.arange(J0) / 2.0); A = 1 / TAU; V = np.ones(J0) / J0; VAR = 1.0
KMAX = 10
NGRID = np.logspace(-4, 0.5, 10)            # white-noise density; N_MIN = 1e-4 (max read rate), N_MAX ~ 3 (reads barely informative)
LEADS = np.concatenate([[0.0], np.logspace(-1.5, 4, 12)])   # latency in units of tau_fast
C0 = 0.003      # sensing price: cost per unit time of reading at precision 1/N is C0/N, in units of h (h = 1)
HF = 20.0       # federation overhead in units of h
N_FIX = 10 ** -1.5   # fixed-sensing variant (a node of NGRID)

def mse(x, N, k):
    b = np.exp(np.clip(np.sort(x), -30, 10)) * (1 + 1e-6 * np.arange(len(x)))
    M, _ = mats(A, V, b, N)
    r = (V[:, None] * np.exp(-A * k)[:, None] * b[None, :] / (A[:, None] + b[None, :])).sum(0)
    if not np.all(np.isfinite(M)): return 1e9
    try: g = np.linalg.lstsq(M, r, rcond=None)[0]
    except np.linalg.LinAlgError: return 1e9
    return float(VAR - r @ g)

def polish(x0, N, k):
    res = minimize(mse, x0, args=(N, k), method='Nelder-Mead', options=dict(xatol=1e-7, fatol=1e-14, maxiter=3000 * len(x0)))
    return res.fun, np.sort(res.x)

def column(args):
    """E_K for K = 1..KMAX at one (N, lead), warm-started so that E_{K+1} <= E_K."""
    iN, il = args; N = NGRID[iN]; k = LEADS[il]; rng = np.random.default_rng(1000 * iN + il)
    la = np.log(A); lo, hi = la.min() - 3, la.max() + 6
    out = []; prev = None
    for K in range(1, KMAX + 1):
        inits = []
        if prev is None:
            inits += [np.array([m]) for m in np.linspace(lo + 2, hi - 2, 7)]
        else:
            for pos in np.linspace(lo + 1, hi - 1, 9):
                inits.append(np.sort(np.append(prev, pos)))
            inits.append(np.sort(np.append(prev, prev.mean())))
        inits.append(np.linspace(lo + 2, hi - 2, K))
        inits += [np.sort(rng.uniform(lo, hi, K)) for _ in range(2)]
        best = (np.inf, None)
        for x0 in inits:
            r = polish(x0, N, k)
            if r[0] < best[0]: best = r
        if prev is not None and out and best[0] > out[-1]:   # E_K can never exceed E_{K-1}: an added store may be given zero weight
            best = (out[-1], np.sort(np.append(prev, prev[-1] + 8.0)))
        out.append(best[0]); prev = best[1]
    return iN, il, out

def main():
    t0 = time.time()
    E = np.zeros((KMAX, len(NGRID), len(LEADS)))
    jobs = [(i, l) for i in range(len(NGRID)) for l in range(len(LEADS))]
    with Pool(6) as p:
        for n, (iN, il, col) in enumerate(p.imap_unordered(column, jobs)):
            E[:, iN, il] = col
            if n % 10 == 0: print(f'{n}/{len(jobs)} {time.time() - t0:.0f}s', flush=True)
    Eex = np.array([[E_opt(A, V, N, k) for k in LEADS] for N in NGRID])      # exact optimum (K = J0 stores)
    json.dump(dict(J0=J0, tau=TAU.tolist(), v=V.tolist(), KMAX=KMAX, N=NGRID.tolist(), leads=LEADS.tolist(), C0=C0, HF=HF, N_FIX=N_FIX,
                   E=E.tolist(), Eexact=Eex.tolist()), open(os.path.join(HERE, 'face_tables.json'), 'w'))
    print('done', time.time() - t0)

if __name__ == '__main__':
    main()
