#!/usr/bin/env python3
"""Time-boxed analytic / special-case probe for Model S convexity.

Aims:
  1. J=2, including K=0: is 2 E_1 <= Var + E_inf always (the first nontrivial
     inequality, since convexity on {K=1,2} is vacuous)?
  2. Well-separated equal-variance modes: decrements ordered by mode value.
  3. Identify where a general argument fails.

Uses the merged solver. Not a proof.
"""
import importlib.util, time, json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar

DIR = Path(__file__).resolve().parent
REPO = DIR.parents[1]  # repo root
spec = importlib.util.spec_from_file_location(
    "stores_merged_s5", REPO / "theory" / "layers_checks" / "stores.py"
)
st = importlib.util.module_from_spec(spec); spec.loader.exec_module(st)

def E1_grid(a, v, N, n=80):
    """Best single-store MSE, 1-D in log-rate (plus a few closed starts)."""
    a = np.asarray(a, float); v = np.asarray(v, float)
    lo, hi = np.log(a.min()) - 4, np.log(a.max()) + 6
    def f(x):
        return st.mse_given_b(a, v, np.array([np.exp(x)]), N)[0]
    xs = np.linspace(lo, hi, n)
    best = min(f(x) for x in xs)
    # polish from the best grid point and from each mode rate
    starts = [xs[int(np.argmin([f(x) for x in xs]))]] + list(np.log(a))
    for x0 in starts:
        r = minimize_scalar(f, bracket=(x0-2, x0, x0+2) if False else None,
                            bounds=(lo, hi), method="bounded", options=dict(xatol=1e-12))
        best = min(best, r.fun)
    # also the closed-form Kalman rate of each single mode and of the variance-pooled mode
    def kalman_rate(aa, vv):
        # optimal store rate for one OU is sqrt(a^2 + 2 a v / N)  (the filter pole)
        return np.sqrt(aa*aa + 2*aa*vv/N)
    for aa, vv in zip(a, v):
        best = min(best, st.mse_given_b(a, v, np.array([kalman_rate(aa, vv)]), N)[0])
    ap, vp = np.sum(v*a)/np.sum(v), np.sum(v)  # precision-weighted pool
    best = min(best, st.mse_given_b(a, v, np.array([kalman_rate(ap, vp)]), N)[0])
    return float(best)

def check_J2(n=400, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    worst = dict(margin=np.inf)
    for i in range(n):
        sep = 10 ** rng.uniform(0, 4)          # 1 to 10^4
        t1 = 10 ** rng.uniform(-1, 2)
        taus = np.array([t1, t1*sep])
        v = 10 ** rng.uniform(-2, 1, 2)
        N = 10 ** rng.uniform(-3, 1)
        a = 1/taus
        E0 = float(v.sum())
        Einf = float(st.E_inf(a, v, N))
        E1 = E1_grid(a, v, N)
        # 2 E1 <= E0 + Einf  iff margin = (E0 + Einf)/2 - E1 >= 0
        margin = (E0 + Einf)/2 - E1
        # also relative to reducible error
        rel = (E0 - E1) / (E1 - Einf) if (E1 - Einf) > 1e-14 else np.inf
        rec = dict(i=i, taus=taus.tolist(), v=v.tolist(), N=float(N),
                   E0=E0, E1=E1, Einf=Einf, margin=float(margin),
                   rel_dec=float(rel), sep=float(sep))
        rows.append(rec)
        if margin < worst["margin"]:
            worst = rec
    margins = np.array([r["margin"] for r in rows])
    rels = np.array([r["rel_dec"] for r in rows])
    return dict(
        n=n,
        n_viol=int(np.sum(margins < -1e-10)),
        min_margin=float(margins.min()),
        min_rel_dec=float(np.min(rels[np.isfinite(rels)])) if np.any(np.isfinite(rels)) else None,
        # rel_dec = (E0-E1)/(E1-Einf); convexity iff rel_dec >= 1
        n_rel_lt_1=int(np.sum(rels < 1 - 1e-10)),
        worst=worst,
        q_margin=list(map(float, np.quantile(margins, [0, 0.01, 0.1, 0.5]))),
        q_rel=list(map(float, np.quantile(rels[np.isfinite(rels)], [0, 0.01, 0.1, 0.5]))),
    )

def check_separated_J3():
    """Equal-variance, widely separated 3-mode worlds: decrements should be ~equal
    in a scaled sense, or ordered. Just a sanity special case."""
    rows = []
    for sep in (10, 30, 100, 300):
        for N in (0.01, 0.1, 1.0):
            taus = np.array([1.0, sep, sep**2])
            v = np.array([1.0, 1.0, 1.0])
            a = 1/taus
            E0 = 3.0
            Einf = float(st.E_inf(a, v, N))
            # use 1-D for K=1; for K=2, a cheap 2-D NM
            E1 = E1_grid(a, v, N)
            # K=2: start at the two fastest / two slowest / all-pairs of kalman rates
            def kalman_rate(aa, vv):
                return np.sqrt(aa*aa + 2*aa*vv/N)
            rates = [kalman_rate(aa, vv) for aa, vv in zip(a, v)]
            cands = []
            for i in range(3):
                for j in range(i+1, 3):
                    b = np.sort([rates[i], rates[j]])
                    cands.append(st.mse_given_b(a, v, b, N)[0])
            # also a short NM from those
            from scipy.optimize import minimize
            def obj(x):
                b = np.exp(np.sort(x))
                if b[1] < 1.02*b[0]:
                    b[1] = 1.02*b[0]
                return st.mse_given_b(a, v, b, N)[0]
            for b0 in ([rates[0], rates[1]], [rates[0], rates[2]], [rates[1], rates[2]]):
                r = minimize(obj, np.log(b0), method="Nelder-Mead",
                             options=dict(xatol=1e-8, fatol=1e-14, maxiter=2000))
                cands.append(obj(r.x))
            E2 = float(min(cands))
            eps = [E0/Einf-1, E1/Einf-1, E2/Einf-1, 0.0]
            dec = [eps[k]-eps[k+1] for k in range(3)]
            convex = all(dec[k+1] <= dec[k] + 1e-6 for k in range(2))
            rows.append(dict(sep=sep, N=N, E=[E0,E1,E2,Einf], eps=eps, dec=dec, convex=convex,
                             ratio=None if eps[1]<=0 else eps[2]/eps[1] if eps[1]>1e-12 else 0))
    return rows

if __name__ == "__main__":
    t0 = time.time()
    j2 = check_J2(500, seed=20261120)
    print("J2 including K=0:", json.dumps({k: j2[k] for k in j2 if k!="worst"}, indent=2))
    print("worst J2:", j2["worst"])
    sep = check_separated_J3()
    print("separated J3 convex?", all(r["convex"] for r in sep))
    for r in sep:
        print(f"  sep={r['sep']} N={r['N']} dec={np.round(r['dec'],4)} ratio_eps2/eps1={None if r['ratio'] is None else round(r['ratio'],4)} convex={r['convex']}")
    print("elapsed", time.time()-t0)
    json.dump(dict(j2=j2, separated_j3=sep), open("/tmp/s5_analytic_probe.json","w"), indent=1, default=float)
