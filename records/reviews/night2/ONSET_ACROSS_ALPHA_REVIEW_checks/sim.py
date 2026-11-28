"""Reviewer re-run (own code; imports nothing from tests/ONSET_ACROSS_ALPHA).
World: fBm with Var(B_t - B_s) = q |t-s|^(alpha-1), generated EXACTLY by Cholesky of the fBm covariance
on independent segments of 4096 steps (author used Davies-Harte circulant embedding of fGn on 2^18-step paths).
Errors scored on the window t in [600, 4096) of each segment; reads at phase + k*T (phase uniform in [0,T), T <= 600),
so every scored step has a read before it. Level and member segments share the segment/time index (CRN).
Learners (no cost formula anywhere; only realized costs):
  grid : selection on realized cost over an integer grid of T (own grid: 120 log points 1..600) on the training set
  es   : (mu/mu, lambda) evolution strategy on ln T, each candidate scored on 4 randomly drawn training segments
         with fresh phases (noisy, independent evaluations; independent ES run for every agent and every N).
usage: sim.py LEARNER ALPHA RHO SEED C OUT.jsonl
"""
import sys, json, numpy as np
LSEG, W0, NSEG, M = 4096, 600, 64, 16
TG = np.unique(np.round(np.exp(np.linspace(0, np.log(600), 120))).astype(int))
_chol = {}
def chol(alpha):
    if alpha not in _chol:
        t = np.arange(1, LSEG + 1, dtype=float); h2 = alpha - 1
        K = 0.5 * (t[:, None] ** h2 + t[None, :] ** h2 - np.abs(t[:, None] - t[None, :]) ** h2)
        _chol[alpha] = np.linalg.cholesky(K)
    return _chol[alpha]
def fbm(rng, alpha, q, n):
    X = rng.standard_normal((n, LSEG)) @ chol(alpha).T
    X = np.sqrt(q) * X
    return np.concatenate([np.zeros((n, 1)), X], axis=1)[:, :LSEG]     # B_0 = 0 prepended
TW = np.arange(W0, LSEG)
def errs(X, T, ph):
    """X: (S, LSEG); ph: (S,) phases. returns (S, len(TW)) reset-read errors."""
    last = ph[:, None] + ((TW[None, :] - ph[:, None]) // T) * T
    return X[:, TW] - np.take_along_axis(X, last, axis=1)
def mse(X, T, rng):
    return float(np.mean(errs(X, T, rng.integers(T, size=X.shape[0])) ** 2))
def learn_grid(X, C, W, rng):
    m = np.array([mse(X, int(T), rng) for T in TG])
    return lambda Ws: [int(TG[np.argmin(C / TG + w * m)]) for w in Ws]
def es(X, C, W, rng, lam=10, mu=5, gens=30, k=4):
    mlog = rng.uniform(np.log(2), np.log(300)); s = 1.0
    for _ in range(gens):
        z = mlog + s * rng.standard_normal(lam)
        Ts = np.clip(np.round(np.exp(z)), 1, 600).astype(int)
        cost = []
        for T in Ts:
            idx = rng.choice(X.shape[0], k, replace=False)
            cost.append(C / T + W * mse(X[idx], int(T), rng))
        best = np.argsort(cost)[:mu]
        mlog = float(np.mean(np.log(Ts[best]))); s *= 0.88
    return int(np.clip(round(np.exp(mlog)), 1, 600))
def nstar_cont(alpha, rho):
    from scipy.optimize import brentq
    a = 1 / alpha
    return float(np.exp(brentq(lambda x: (a - 1) * x + a * np.log(rho) - np.log((1 + rho) ** a - 1), -20, 40)))
def main(learner, alpha, rho, seed, C, out):
    rng = np.random.default_rng([7, int(alpha * 10), int(rho * 1e4), seed, int(C), 0 if learner == 'grid' else 1])
    nN = 81 if learner == 'grid' else 33
    Ns = nstar_cont(alpha, rho) * np.exp(np.linspace(-np.log(8), np.log(8), nN))   # grid placement only
    gtr = fbm(rng, alpha, rho, NSEG); utr = [fbm(rng, alpha, 1.0, NSEG) for _ in range(M)]
    if learner == 'grid':
        Tf = [learn_grid(gtr + utr[i], C, 1, rng)([1])[0] for i in range(M)]
        Tu = [learn_grid(utr[i], C, 1, rng)([1])[0] for i in range(M)]
        Tg = learn_grid(gtr, C, None, rng)(Ns)
    else:
        Tf = [es(gtr + utr[i], C, 1, rng) for i in range(M)]
        Tu = [es(utr[i], C, 1, rng) for i in range(M)]
        Tg = [es(gtr, C, N, rng) for N in Ns]
    gte = fbm(rng, alpha, rho, NSEG); ute = [fbm(rng, alpha, 1.0, NSEG) for _ in range(M)]
    flat = np.mean([C / Tf[i] + mse(gte + ute[i], Tf[i], rng) for i in range(M)])
    EU = np.stack([errs(ute[i], Tu[i], rng.integers(Tu[i], size=NSEG)) for i in range(M)])   # (M, S, t)
    spend_u = np.mean([C / T for T in Tu])
    cache = {}
    for T in set(Tg):
        eg = errs(gte, T, rng.integers(T, size=NSEG))
        cache[T] = (C / T, float(np.mean((eg[None] + EU) ** 2)))
    lev = [cache[T][0] / N + cache[T][1] + spend_u for N, T in zip(Ns, Tg)]
    rec = dict(learner=learner, alpha=alpha, rho=rho, seed=seed, C=C, N=list(map(float, Ns)), flat=float(flat),
               levelled=list(map(float, lev)), Tf=Tf, Tu=Tu, Tg=list(map(int, Tg)))
    with open(out, 'a') as f: f.write(json.dumps(rec) + "\n")
if __name__ == '__main__':
    l, a, r, s, c, o = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
    main(l, a, r, s, c, o)
