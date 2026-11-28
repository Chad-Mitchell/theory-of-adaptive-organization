"""ANTS1 world generator. Written BEFORE any ant code (rule d).

A single food source on a ring of M sites. Its position x_t (float in [0, M)) follows one of three
relocation processes. Ant observations are x_t + Gaussian noise (sd SIGMA_OBS); the noise draws are made
inside the ant code from a seeded stream, but the noise model is fixed here.

Worlds (drift levels index 0,1,2 = slow, mid, fast):
  RW    : Gaussian random walk, step sd SIGMA_D[k] sites per step (T4's home regime).
  POIS  : food stays put, relocates to a uniform random site at Poisson rate LAMBDA[k] per step.
  HEAVY : same uniform relocation, but holding times are Pareto (alpha = 1.5) with the SAME mean 1/LAMBDA[k]
          (bursty: many short stays, a few very long ones).
"""
import numpy as np

M = 1024                 # ring sites
T = 60000                # steps per run
BURN = 10000             # steps discarded before scoring
SIGMA_D = [0.03, 0.2, 1.0]          # RW step sd (sites/step)
LAMBDA = [2e-4, 1e-3, 5e-3]         # POIS/HEAVY mean relocation rate (per step)
PARETO_ALPHA = 1.5
SIGMA_OBS = [4.0, 16.0]             # ant observation noise sd (sites)
WORLDS = ["RW", "POIS", "HEAVY"]


def world_seed(world, drift, seed):
    return 1_000_003 * (WORLDS.index(world) + 1) + 10_007 * drift + seed


def generate(world, drift, seed, T=T):
    """Return x[0..T-1] (float64, in [0, M)) and the relocation step indices (empty for RW)."""
    rng = np.random.default_rng(world_seed(world, drift, seed))
    x0 = rng.uniform(0, M)
    if world == "RW":
        x = (x0 + np.cumsum(rng.normal(0.0, SIGMA_D[drift], T))) % M
        return x, np.array([], dtype=np.int64)
    lam = LAMBDA[drift]
    jumps = []
    t = 0.0
    while True:
        if world == "POIS":
            hold = rng.exponential(1.0 / lam)
        else:  # Pareto(alpha) with mean 1/lam: x_m = mean*(alpha-1)/alpha
            xm = (1.0 / lam) * (PARETO_ALPHA - 1) / PARETO_ALPHA
            hold = xm * (1.0 + rng.pareto(PARETO_ALPHA))
        t += hold
        if t >= T:
            break
        jumps.append(int(np.ceil(t)))
    x = np.empty(T)
    pos = x0
    j = 0
    jumps = np.array(sorted(set(jumps)), dtype=np.int64)
    for t in range(T):
        while j < len(jumps) and jumps[j] == t:
            pos = rng.uniform(0, M)
            j += 1
        x[t] = pos
    return x, jumps


if __name__ == "__main__":
    for w in WORLDS:
        for d in range(3):
            x, J = generate(w, d, 0)
            print(w, d, "jumps", len(J), "x range", round(x.min(), 1), round(x.max(), 1))
