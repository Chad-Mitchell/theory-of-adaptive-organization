"""One (alpha, rho, seed) job: learn flat members, residual members and the level (for every N on the grid) on
training paths; evaluate on fresh test paths with common random numbers. Output: per-N per-member realized costs.
usage: run.py ALPHA RHO SEED OUT.jsonl
"""
import sys, json, numpy as np
from world import fbm, reset_err, mse_curve, learn, TGRID
L, M = 2 ** 18, 16
CREAD = {1.5: 84.3, 2.0: 800.0, 2.5: 6072.0}   # read cost per alpha: puts a lone member's learned T near 40 (unit choice)

def main(alpha, rho, seed, out, centre):
    rng = np.random.default_rng([int(alpha * 100), int(round(rho * 1e4)), seed, 32])
    C = CREAD[alpha]
    Ns = centre * np.exp(np.linspace(np.log(1 / 16), np.log(16), 161))
    # training
    gtr = fbm(rng, L, alpha, rho)[0]
    utr = fbm(rng, L, alpha, 1.0, M)
    Tf = [learn(mse_curve(gtr + utr[i], rng), C, 1.0) for i in range(M)]
    Tu = [learn(mse_curve(utr[i], rng), C, 1.0) for i in range(M)]
    mg = mse_curve(gtr, rng)
    Tg = [learn(mg, C, N) for N in Ns]
    # test (fresh paths, CRN between flat and levelled)
    gte = fbm(rng, L, alpha, rho)[0]
    ute = fbm(rng, L, alpha, 1.0, M)
    flat = np.mean([C / Tf[i] + np.mean(reset_err(gte + ute[i], Tf[i], int(rng.integers(Tf[i])))[0] ** 2) for i in range(M)])
    # residual members: align errors to a common time index
    Lc = L - 2 * 700
    eu = []; spend_u = []
    for i in range(M):
        ph = int(rng.integers(Tu[i])); e, r = reset_err(ute[i], Tu[i], ph)
        eu.append(e[700 - ph:700 - ph + Lc] if ph <= 700 else None); spend_u.append(C * r)
    eu = np.array(eu)
    lev = {}
    for T in sorted(set(Tg)):
        ph = int(rng.integers(T)); e, r = reset_err(gte, T, ph)
        eg = e[700 - ph:700 - ph + Lc]
        lev[T] = (C * r, np.mean((eg[None, :] + eu) ** 2))
    levelled = [lev[T][0] / N + lev[T][1] + np.mean(spend_u) for N, T in zip(Ns, Tg)]
    rec = dict(alpha=alpha, rho=rho, seed=seed, centre=centre, N=list(Ns), flat=flat, levelled=levelled,
               Tf=Tf, Tu=Tu, Tg=Tg)
    with open(out, 'a') as f: f.write(json.dumps(rec) + "\n")

if __name__ == '__main__':
    a, r, s, o = float(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    from theory import nstar
    main(a, r, s, o, nstar(a, r))
