"""ROBUST-SLACK deviation D1: RS-2a with a calibrated null (simulation only; no real data).

Reviewer setup (rev115 prereg_sim2.py): n_i log-uniform on [5, 40], shocks Gaussian or Student t (nu = 3, 4).
Rival R-fixed: B_obs,i = k * sigma_true,i (constant safety factor), so r_i = k*sigma_true/sigma_hat_i.
Old rule: PASS iff Fisher 95% lower bound of Spearman rho(ln r, ln F) > +0.10 -> passes under heavy tails.
New rule (D1): fit the class tail nu_hat by MLE (Student t, loc 0) on pooled shocks standardized per system by
median and MAD; simulate the R-fixed null M times from t_{nu_hat} with each system's own n_i; q975 and mean of the
null rho. PASS iff lower bound > q975 + kappa; FAIL iff upper bound < null mean - kappa; else INCONCLUSIVE.
Fisher interval (se = 1.06/sqrt(N-3)) stands in for the locked bootstrap here, to keep the simulation cheap.
"""
import math, sys, json
import numpy as np
from scipy import stats

EPS, KAPPA = 1e-3, 0.10
Z = stats.norm.isf(EPS)


def F(n):
    return stats.t.isf(EPS, n - 1) * math.sqrt(1 + 1 / n) / Z


def draw(rng, kind, n):
    if kind == "gauss":
        return rng.standard_normal(n)
    return rng.standard_t(kind, n)


def sigma_hats(rng, kind, ns):
    return np.array([np.std(draw(rng, kind, int(m)), ddof=1) for m in ns]), None


def sample_class(rng, kind, ns):
    shocks = [draw(rng, kind, int(m)) for m in ns]
    return shocks


def fit_nu(shocks):
    z = []
    for x in shocks:
        mad = np.median(np.abs(x - np.median(x))) * 1.4826
        if mad > 0:
            z.append((x - np.median(x)) / mad)
    z = np.concatenate(z)
    nu, loc, sc = stats.t.fit(z, floc=0)
    return float(min(max(nu, 2.05), 200.0))


def null_rhos(rng, nu, ns, lnF, M):
    """Vectorized: for each distinct n, draw an (M, count, n) block of t_nu shocks."""
    sh = np.empty((M, len(ns)))
    for m in np.unique(ns):
        idx = np.where(ns == m)[0]
        sh[:, idx] = rng.standard_t(nu, (M, len(idx), int(m))).std(axis=2, ddof=1)
    rk_F = stats.rankdata(lnF)
    rk = np.apply_along_axis(stats.rankdata, 1, -np.log(sh))
    a = rk - rk.mean(1, keepdims=True); b = rk_F - rk_F.mean()
    return (a @ b) / np.sqrt((a * a).sum(1) * (b * b).sum())


def fisher(rho, N):
    se = 1.06 / math.sqrt(N - 3)
    a = math.atanh(max(min(rho, 0.999999), -0.999999))
    return math.tanh(a - 1.96 * se), math.tanh(a + 1.96 * se)


def one(rng, kind, N, M, alt_power=0.0):
    ns = np.exp(rng.uniform(math.log(5), math.log(40), N)).astype(int)
    lnF = np.log([F(m) for m in ns])
    shocks = sample_class(rng, kind, ns)
    sh = np.array([np.std(x, ddof=1) for x in shocks])
    # R-fixed: B = k sigma_true (sigma_true = 1 for every system without loss for Spearman);
    # alternative: B = k * F^alt_power * sigma_true
    lnr = alt_power * lnF - np.log(sh)
    rho = stats.spearmanr(lnr, lnF)[0]
    lo, hi = fisher(rho, N)
    old = lo > KAPPA
    nu = fit_nu(shocks)
    nr = null_rhos(rng, nu, ns, lnF, M)
    q975, mu = np.quantile(nr, 0.975), nr.mean()
    new = "PASS" if lo > q975 + KAPPA else ("FAIL" if hi < mu - KAPPA else "INCONCLUSIVE")
    return rho, old, new, nu, mu, q975


def run(reps, M, cases, seed=20261120):
    rng = np.random.default_rng(seed)
    res = {}
    for kind, N, alt in cases:
        R = [one(rng, kind, N, M, alt) for _ in range(reps)]
        res["%s|N=%d|alt=%.1f" % (kind, N, alt)] = dict(
            mean_rho=round(float(np.mean([r[0] for r in R])), 3),
            P_old_pass=round(float(np.mean([r[1] for r in R])), 3),
            P_new_pass=round(float(np.mean([r[2] == "PASS" for r in R])), 3),
            P_new_fail=round(float(np.mean([r[2] == "FAIL" for r in R])), 3),
            mean_nu_hat=round(float(np.mean([r[3] for r in R])), 2),
            null_mean=round(float(np.mean([r[4] for r in R])), 3),
            null_q975=round(float(np.mean([r[5] for r in R])), 3))
        print(kind, N, alt, res["%s|N=%d|alt=%.1f" % (kind, N, alt)], flush=True)
    return res


def _case(args):
    kind, N, alt, reps, M, seed = args
    return run(reps, M, [(kind, N, alt)], seed=seed)


if __name__ == "__main__":
    from multiprocessing import Pool
    quick = "--quick" in sys.argv
    reps, M = (20, 100) if quick else (200, 1000)
    cases = [(k, N, 0.0) for k in ("gauss", 4, 3) for N in (200, 1000)]  # R-fixed (size)
    cases += [(k, N, a) for k in (4,) for N in (20, 50, 200, 1000) for a in (1.0, 0.5)]  # power
    jobs = [(k, N, a, reps if N < 1000 else reps // 2, M, 20261120 + i) for i, (k, N, a) in enumerate(cases)]
    with Pool(int(sys.argv[sys.argv.index("--procs") + 1]) if "--procs" in sys.argv else 4) as pool:
        parts = pool.map(_case, jobs)
    res = {}
    for p_ in parts:
        res.update(p_)
    if not quick:
        json.dump(res, open("rs2a_null_sim.json", "w"), indent=1)
