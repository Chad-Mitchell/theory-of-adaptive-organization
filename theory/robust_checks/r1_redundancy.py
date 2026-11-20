"""R1: copies of a layer under component failure (theory/ROBUSTNESS.md §3).

Model (one needed layer, windows of unit length): n independent copies, upkeep h each per
window; each copy is down in a window with probability p (independently, repaired by the next
window). Loss w*E1 if at least one copy is up, w*E0 if all are down; Delta = E0 - E1 > 0.
Every function returns plain numbers; run as a script to print the checks; pytest imports it.
"""
import math
import numpy as np
from scipy.optimize import brentq


def J(n, w, h, p, Delta, E1=0.0):
    return n * h + w * E1 + w * Delta * p ** n


def n_E_closed(w, h, p, Delta):
    """R1-a: expected-cost copy count, closed form."""
    if w * Delta * p * (1 - p) <= h:
        return 1
    return max(1, math.ceil(math.log(h / (w * Delta * (1 - p))) / math.log(p) - 1e-12))


def n_E_brute(w, h, p, Delta, nmax=2000):
    vals = [J(n, w, h, p, Delta) for n in range(1, nmax + 1)]
    return 1 + int(np.argmin(vals))  # first minimizer


def eps_window(eps, N):
    return 1.0 - (1.0 - eps) ** (1.0 / N)


def n_R_closed(p, eps, N):
    """R1-b: catastrophic all-down => ruin; smallest n with P(ruin over N windows) <= eps."""
    e1 = eps_window(eps, N)
    return max(1, math.ceil(math.log(e1) / math.log(p) - 1e-12))


def n_R_brute(p, eps, N, nmax=400):
    for n in range(1, nmax + 1):
        if 1 - (1 - p ** n) ** N <= eps * (1 + 1e-9):
            return n
    return None


def n_star_brute(w, h, p, Delta, eps, N, nmax=400):
    feas = [n for n in range(1, nmax + 1) if 1 - (1 - p ** n) ** N <= eps * (1 + 1e-9)]
    return min(feas, key=lambda n: (J(n, w, h, p, Delta), n))


def all_down_common(n, p, beta):
    """R1-c: common-cause shock (prob beta per window, takes every copy down) plus independent p."""
    return beta + (1 - beta) * p ** n


# R1-d: non-catastrophic blind windows paid from a reserve (diffusion + jumps, Dufresne-Gerber).
def lundberg_theta(n, y, w, h, p, X, s, E1=0.0):
    """Positive root of k(t) = -t*(y - n h - w E1) + t^2 s^2/2 + p^n (e^{tX} - 1); None if margin <= 0."""
    m = y - n * h - w * E1 - p ** n * X  # mean margin = y - J(n)
    if m <= 0:
        return None
    k = lambda t: -t * (y - n * h - w * E1) + 0.5 * t * t * s * s + p ** n * (math.expm1(t * X))
    hi = 1e-6
    while k(hi) <= 0:
        hi *= 2
        if hi > 1e6:
            return None
    # k(0)=0, k'(0)=-m<0, so the positive root is the sign change in (0, hi]
    lo = 1e-12
    while k(lo) >= 0:
        lo /= 10
        if lo < 1e-300:
            return None
    return brentq(k, lo, hi, xtol=1e-14, rtol=1e-12)


def constrained_n(y, w, h, p, X, s, B, eps, nmax=30):
    need = math.log(1 / eps) / B
    best = None
    for n in range(1, nmax + 1):
        th = lundberg_theta(n, y, w, h, p, X, s)
        if th is not None and th >= need:
            Jn = n * h + p ** n * X
            if best is None or Jn < best[1] - 1e-15:
                best = (n, Jn)
    return None if best is None else best[0]


def theta_argmax(y, w, h, p, X, s, nmax=30):
    th = [(lundberg_theta(n, y, w, h, p, X, s) or 0.0) for n in range(1, nmax + 1)]
    return 1 + int(np.argmax(th))


def mc_ruin(n, y, h, p, X, s, B, T=200.0, dt=0.01, paths=4000, seed=1):
    """Monte Carlo ruin probability by time T (Euler, jumps at rate p^n per unit time)."""
    rng = np.random.default_rng(seed)
    R = np.full(paths, B, dtype=float)
    alive = np.ones(paths, bool)
    lam = p ** n
    for _ in range(int(T / dt)):
        dR = (y - n * h) * dt + s * math.sqrt(dt) * rng.standard_normal(paths)
        dR -= X * (rng.random(paths) < lam * dt)
        R = np.where(alive, R + dR, R)
        alive &= R > 0
    return 1 - alive.mean()


def run():
    res = {}
    # R1-a: closed form = brute force on a grid
    bad = 0; cnt = 0
    for w in [0.5, 1, 3, 10, 100, 1e4]:
        for h in [0.01, 0.1, 1]:
            for p in [0.01, 0.05, 0.2, 0.5, 0.8, 0.95]:
                for D in [0.5, 1, 5]:
                    cnt += 1
                    bad += n_E_closed(w, h, p, D) != n_E_brute(w, h, p, D)
    res["a_grid_cases"] = cnt; res["a_mismatches"] = bad
    # monotone in w (nondecreasing), in h (nonincreasing); grows ~ ln(w)/ln(1/p)
    ws = np.logspace(0, 8, 60)
    nE = [n_E_closed(w, 0.1, 0.1, 1.0) for w in ws]
    res["a_monotone_w"] = all(b >= a for a, b in zip(nE, nE[1:]))
    hs = np.logspace(-4, 1, 60)
    nEh = [n_E_closed(100, h, 0.1, 1.0) for h in hs]
    res["a_monotone_h"] = all(b <= a for a, b in zip(nEh, nEh[1:]))
    # slope in ln w over 8 decades ~ 1/ln(1/p)
    res["a_slope_per_ln_w"] = (nE[-1] - nE[0]) / math.log(ws[-1] / ws[0])
    res["a_slope_theory"] = 1 / math.log(1 / 0.1)
    # not monotone in p: copies are useless at p -> 0 and at p -> 1
    ps = np.linspace(0.001, 0.999, 200)
    nEp = [n_E_closed(1e3, 1.0, p, 1.0) for p in ps]
    res["a_p_profile_ends"] = (nEp[0], max(nEp), nEp[-1])
    # R1-b: catastrophic, closed form = brute, independent of w and h
    bad = 0
    for p in [0.001, 0.01, 0.1, 0.3, 0.6]:
        for eps in [1e-2, 1e-3, 1e-6]:
            for N in [1, 10, 1000, 10 ** 5]:
                bad += n_R_closed(p, eps, N) != n_R_brute(p, eps, N)
    res["b_mismatches"] = bad
    res["b_example_p0.1_eps1e-3_N1e3"] = n_R_closed(0.1, 1e-3, 1000)
    # n* = max(n_E, n_R)
    bad = 0
    for w in [1, 10, 1e3]:
        for h in [0.01, 1]:
            for p in [0.01, 0.1, 0.5]:
                for eps in [1e-2, 1e-4]:
                    for N in [10, 1000]:
                        bad += n_star_brute(w, h, p, 1.0, eps, N) != max(n_E_closed(w, h, p, 1.0), n_R_closed(p, eps, N))
    res["b_nstar_mismatches"] = bad
    # infinite horizon: n_R -> infinity as N -> infinity
    res["b_nR_vs_N"] = [n_R_closed(0.1, 1e-3, N) for N in [1, 1e2, 1e4, 1e6, 1e8]]
    # R1-c: common-cause floor
    beta, p, eps, N = 1e-4, 0.1, 1e-3, 1000
    e1 = eps_window(eps, N)
    res["c_floor_beta"] = beta; res["c_window_budget"] = e1
    res["c_feasible_any_n"] = any(all_down_common(n, p, beta) <= e1 for n in range(1, 500))
    # R1-d: reserve with jumps. Case A: big jump vs buffer -> binding ruin raises copies above n_E.
    A = dict(y=1.0, w=1.0, h=0.05, p=0.2, X=2.0, s=0.5)
    nE_A = n_E_closed(1.0, A["h"], A["p"], A["X"])
    res["d_A_nE"] = nE_A
    res["d_A_ntheta"] = theta_argmax(**A)
    res["d_A_n_by_B"] = {B: constrained_n(B=B, eps=1e-3, **A) for B in [1.5, 2, 3, 5, 10, 50]}
    # Theorem R1-d on a random grid: theta_n <= theta_{n_E} for n < n_E, so the constrained
    # optimum is the smallest certified n >= n_E (copies never fall below n_E), and n*(B) is
    # nonincreasing in B.
    rng = np.random.default_rng(7)
    viol_theta = viol_nstar = viol_monoB = tested = 0
    for _ in range(300):
        P = dict(y=float(rng.uniform(1, 3)), w=1.0, h=float(10 ** rng.uniform(-2.5, -0.5)),
                 p=float(rng.uniform(0.05, 0.7)), X=float(10 ** rng.uniform(-0.5, 0.7)),
                 s=float(10 ** rng.uniform(-1, 0.3)))
        nE = n_E_closed(1.0, P["h"], P["p"], P["X"])
        thE = lundberg_theta(nE, **P)
        if thE is None or nE > 25:
            continue
        tested += 1
        for n in range(1, nE):
            th = lundberg_theta(n, **P)
            if th is not None and th > thE * (1 + 1e-9):
                viol_theta += 1
        prev = None
        for B in [0.3, 0.6, 1, 2, 4, 8, 16, 64]:
            ns = constrained_n(B=B, eps=1e-3, **P)
            need = math.log(1e3) / B
            first = next((n for n in range(nE, 31) if (lundberg_theta(n, **P) or 0) >= need), None)
            viol_nstar += ns != first
            if prev is not None and ns is not None and ns > prev:
                viol_monoB += 1
            if ns is not None:
                prev = ns
    res["d_grid_tested"] = tested
    res["d_viol_theta_below_nE"] = viol_theta
    res["d_viol_nstar_formula"] = viol_nstar
    res["d_viol_monotone_in_B"] = viol_monoB
    # Monte Carlo: Lundberg bound holds (ruin by T <= e^{-theta B}) for case A, n=1 and n=3
    mc = {}
    for n in [1, 3]:
        th = lundberg_theta(n, **A)
        Bv = 3.0
        mc[n] = (mc_ruin(n, A["y"], A["h"], A["p"], A["X"], A["s"], Bv), math.exp(-th * Bv))
    res["d_mc_ruin_vs_bound"] = mc
    return res


if __name__ == "__main__":
    for k, v in run().items():
        print(k, "=", v)
