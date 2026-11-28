"""LEARNSIM world + learners.  Fresh code (does not import any earlier GTAO simulator).
No expected-cost formula appears anywhere in this file.  Trackers only ever see:
  * their own observations (reads / noisy samples), and
  * realized payoffs (money spent + realized squared error x stakes) after an episode.
Tech R: a read costs C_R and returns the current value exactly; estimate held until next read.
        Policy = integer read interval T (learned from payoffs); random phase.
Tech A: each step the tracker buys k units of sample rate at C_A per unit; it observes
        y_t = x_t + sqrt(SIG2/k) z_t and smooths x_hat += alpha (y - x_hat).
        Policy = k (learned from payoffs).  alpha is self-tuned from the tracker's OWN
        observations only (minimise squared innovation y_t - x_hat_{t-1}); no payoff, no truth.
"""
import numpy as np
from numba import njit

C_R = 800.0
C_A = 1.0
SIG2 = 1.0e4

def bm(rng, L, q, M=None):
    if M is None:
        return np.cumsum(rng.normal(0.0, np.sqrt(q), L))
    return np.cumsum(rng.normal(0.0, np.sqrt(q), (M, L)), axis=1)

# ---------------- tech R -----------------
def r_errors(x, T, phase):
    """x: 1-D path. Reads at phase, phase+T, ... ; returns (errors on counted window, reads in window).
    Counted window is t in [T, len(x)) so every counted step has a prior read."""
    L = x.shape[-1]
    t = np.arange(T, L)
    last = phase + ((t - phase) // T) * T
    e = x[..., t] - x[..., last]
    nreads = np.count_nonzero(((t - phase) % T) == 0)
    return e, nreads

# ---------------- tech A -----------------
@njit(cache=True)
def _innov(y, alpha, burn):
    xh = y[0]
    s = 0.0
    for t in range(1, y.shape[0]):
        v = y[t] - xh
        if t >= burn:
            s += v * v
        xh += alpha * v
    return s

@njit(cache=True)
def _errs(y, x, alpha):
    n = y.shape[0]
    e = np.empty(n)
    xh = y[0]
    e[0] = x[0] - xh
    for t in range(1, n):
        xh += alpha * (y[t] - xh)
        e[t] = x[t] - xh
    return e

GR = (np.sqrt(5) - 1) / 2

def tune_alpha(y, burn, lo=-9.0, hi=0.0, it=22):
    """golden-section on ln(alpha) minimising the tracker's own innovation SSE (observations only)."""
    a, b = lo, hi
    c = b - GR * (b - a); d = a + GR * (b - a)
    fc = _innov(y, np.exp(c), burn); fd = _innov(y, np.exp(d), burn)
    for _ in range(it):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - GR * (b - a); fc = _innov(y, np.exp(c), burn)
        else:
            a, c, fc = c, d, fd
            d = a + GR * (b - a); fd = _innov(y, np.exp(d), burn)
    return float(np.exp((a + b) / 2))

def a_errors(x, k, rng, burn):
    y = x + np.sqrt(SIG2 / k) * rng.standard_normal(x.shape[0])
    al = tune_alpha(y, burn)
    e = _errs(y, x, al)
    return e[burn:], al

# ------------- realized cost of ONE episode for a lone/level tracker -------------
def episode_cost(tech, effort, Wt, q, rng, L=None):
    """Realized per-step cost (spend + Wt * mean squared error) of one fresh episode.
    effort: T (int, tech R) or k (tech A).  This is what the learner observes."""
    if tech == 'R':
        T = int(effort)
        Lc = max(400, 20 * T)
        x = bm(rng, Lc + T, q)
        e, nr = r_errors(x, T, int(rng.integers(T)))
        return (C_R * nr + Wt * np.dot(e, e)) / e.shape[0]
    else:
        Lc = 4000 if L is None else L
        x = bm(rng, Lc, q)
        e, al = a_errors(x, effort, rng, Lc // 4)
        return C_A * effort + Wt * np.dot(e, e) / e.shape[0]

# ---------------- learner: noisy (1+1)-ES on log effort ----------------
BOUNDS = {'R': (1.0, 2000.0), 'A': (0.01, 1.0e7)}

def es_learn(tech, Wt, q, rng, n_ep=300):
    lo, hi = np.log(BOUNDS[tech][0]), np.log(BOUNDS[tech][1])
    def eff(z):
        return max(1, int(round(np.exp(z)))) if tech == 'R' else float(np.exp(z))
    z = rng.uniform(lo, hi)           # uninformed start
    if tech == 'R': z = np.log(eff(z))
    s = 1.0
    inc_sum = episode_cost(tech, eff(z), Wt, q, rng); inc_n = 1
    for ep in range(n_ep):
        if ep % 2 == 0:
            inc_sum += episode_cost(tech, eff(z), Wt, q, rng); inc_n += 1
        else:
            for _try in range(50):   # reflecting bounds; mutant must be a different policy
                zm = z + s * rng.standard_normal()
                if zm < lo: zm = 2 * lo - zm
                if zm > hi: zm = 2 * hi - zm
                zm = float(np.clip(zm, lo, hi))
                if eff(zm) != eff(z): break
            cm = episode_cost(tech, eff(zm), Wt, q, rng)
            if cm < inc_sum / inc_n:
                z, inc_sum, inc_n = (np.log(eff(zm)) if tech == 'R' else zm), cm, 1
                s = min(2.0, s * np.exp(0.8))
            else:
                s = max(0.1, s * np.exp(-0.2))
    return eff(z)

# ---------------- learner (robustness): population selection on one long common path ----------------
def pop_learn(tech, Wt, q, rng, L=200000):
    """all grid variants live through the same long realized path; keep the cheapest realized."""
    if tech == 'R':
        grid = np.unique(np.round(np.exp(np.linspace(0, np.log(2000), 120))).astype(int))
        x = bm(rng, L + grid.max(), q)
        best, bc = None, np.inf
        for T in grid:
            e, nr = r_errors(x, int(T), int(rng.integers(T)))
            c = (C_R * nr + Wt * np.dot(e, e)) / e.shape[0]
            if c < bc: best, bc = int(T), c
        return best
    grid = np.exp(np.linspace(np.log(0.01), np.log(1e7), 140))
    Lc = 40000
    x = bm(rng, Lc, q); z = rng.standard_normal(Lc)
    best, bc = None, np.inf
    for k in grid:
        y = x + np.sqrt(SIG2 / k) * z
        al = tune_alpha(y, Lc // 4)
        e = _errs(y, x, al)[Lc // 4:]
        c = C_A * k + Wt * np.dot(e, e) / e.shape[0]
        if c < bc: best, bc = float(k), c
    return best
