#!/usr/bin/env python3
"""T28 / SIM-1 helpers: simulation as a mechanism already inside J.

A design chooses layer count K and rehearsal count m (simulation rollouts
per decision). No new term is added to the master equation. The pieces are:

    J(K, m) = κ I(m) + h K + c m + (w + λ χ) E(K, m)

- κ I(m): model memory, I(m) = I_0 if m ≥ 1 else 0 (the model is held only
  if the system actually rehearses). This is the existing κ I_mem term.
- h K: existing layer upkeep.
- c m: compute paid per rollout. Booked as part of A(𝒟), the cost of
  reading — here, reading an internal model rather than the world.
- w E[ℓ]: existing stake times expected real-trial loss.
- λ χ E[ℓ]: ruin *exposure*, a stand-in for L, proportional to residual
  error. This is not the Lundberg cap P(ruin) ≤ ε. When that cap binds,
  the feasible set can depend on w and CT33 monotonicity can fail; this
  package keeps the cap slack and prices exposure additively.

Expected real-trial loss, with model fidelity φ ∈ (0, 1]:

    E(K, m) = e_0(K) [ 1 − φ + φ / (1 + φ m) ]
    e_0(K) = e_base / (1 + γ K)

So simulation drives error from e_0(K) toward the fidelity floor
e_0(K)(1 − φ), with diminishing returns 1/(1 + φ m). Layers shrink the
pre-simulation residual e_0; they do not change φ. Consequently K and m
are substitutes: m*_cont(K) falls as e_0(K) falls. Official monotone
gates for m* are therefore stated at fixed K, in the same spirit as
CT20 (ii) (sensing held fixed). Joint (K*, m*) can jump down in m when
a new layer is added; that is not a refutation of the Topkis claim at
fixed K, and CT33 still says total judgment spend is nondecreasing and
error nonincreasing in w when the cap is slack.

The library does not import or modify CORE.md. Moran / Boltzmann helpers
are reused from theory/bridge_2026-11-21/bridge_lib.py.
"""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path

import numpy as np

DIR = Path(__file__).resolve().parent
REPO = DIR.parents[1]
BRIDGE_PY = REPO / "core" / "bridge_2026-11-21" / "bridge_lib.py"

spec = importlib.util.spec_from_file_location("bridge_lib_t27_for_sim1", BRIDGE_PY)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)

# Re-exported Moran / Boltzmann tools (not modified).
moran_fixation = bridge.moran_fixation
exact_boltzmann = bridge.exact_boltzmann
run_moran_ct = bridge.run_moran_ct
tv_distance = bridge.tv_distance
argmin_unique = bridge.argmin_unique
connected_from = bridge.connected_from
adjacency_from_edges = bridge.adjacency_from_edges
birth_rates_from_J = bridge.birth_rates_from_J
alpha_from_beta = bridge.alpha_from_beta
beta_from_alpha = bridge.beta_from_alpha

# ---------------------------------------------------------------------------
# Seeds already used in this repository (do not reuse).
# ---------------------------------------------------------------------------
S5_RNG_SEEDS = set(range(1000, 1120))
CONV_SEARCH_SEEDS = set(range(0, 120)) | {7}
WIDE_RNG_SEEDS = set(range(5000, 5120))
NAMED_SEEDS = {20261120, 2026112020, 1, 11, 3}
# T27 official candidate worlds and the reserved chain-seed block.
T27_WORLD_SEEDS = set(range(2026112100, 2026112116))
T27_CHAIN_SEEDS = set(range(20261121500, 20261122000))


def seed_collides(rng_seed: int) -> bool:
    """True if the seed is already used by a prior test set in this repo."""
    if rng_seed in S5_RNG_SEEDS or rng_seed in CONV_SEARCH_SEEDS:
        return True
    if rng_seed in WIDE_RNG_SEEDS or rng_seed in NAMED_SEEDS:
        return True
    if rng_seed in T27_WORLD_SEEDS or rng_seed in T27_CHAIN_SEEDS:
        return True
    return False


# ---------------------------------------------------------------------------
# Cost of judgment with a simulate option (already inside J)
# ---------------------------------------------------------------------------

def e0(K: int, e_base: float, gamma: float) -> float:
    return float(e_base / (1.0 + gamma * K))


def expected_loss(K: int, m: int, e_base: float, gamma: float, phi: float) -> float:
    """Real-trial expected loss after m rollouts of a model with fidelity φ."""
    if m < 0:
        raise ValueError("m must be >= 0")
    e = e0(K, e_base, gamma)
    return float(e * (1.0 - phi + phi / (1.0 + phi * m)))


def I_mem(m: int, I0: float) -> float:
    """Model memory: paid iff the system actually simulates (m ≥ 1)."""
    return float(I0 if m >= 1 else 0.0)


def effective_stake(w: float, lam: float, chi: float) -> float:
    return float(w + lam * chi)


def J_cost(K, m, w, c, kappa, h, I0, e_base, gamma, phi, lam, chi) -> float:
    """J(K, m) as booked above. All prices nonnegative."""
    W = effective_stake(w, lam, chi)
    return float(
        kappa * I_mem(m, I0)
        + h * K
        + c * m
        + W * expected_loss(K, m, e_base, gamma, phi)
    )


def m_cont(K, w, c, e_base, gamma, phi, lam=0.0, chi=1.0) -> float:
    """Unconstrained continuous minimizer of c m + W E(K, m) for m > 0,
    ignoring the fixed model cost κ I_0 (that cost is paid for all m ≥ 1
    and so does not shift the interior FOC). Clipped at 0.

        m_cont = [sqrt(W e_0(K) / c) − 1/φ]_+

    Derived from dE/dm = − e_0 φ² / (1 + φ m)², so the FOC is
    c = W e_0 φ² / (1 + φ m)².
    """
    if c <= 0 or phi <= 0:
        return 0.0
    W = effective_stake(w, lam, chi)
    e = e0(K, e_base, gamma)
    raw = math.sqrt(W * e / c) - 1.0 / phi
    return float(max(0.0, raw))


def W_first_rollout(K, c, e_base, gamma, phi) -> float:
    """Effective-stake threshold at which the continuous FOC first wants m > 0,
    ignoring the fixed cost κ I_0: W = c / (e_0(K) φ²).
    """
    e = e0(K, e_base, gamma)
    return float(c / (e * phi * phi))


def J_table(K_max, m_max, w, c, kappa, h, I0, e_base, gamma, phi, lam, chi):
    """J on the discrete grid K=0..K_max, m=0..m_max, row-major in (K, m)."""
    nK, nM = K_max + 1, m_max + 1
    J = np.empty((nK, nM), dtype=float)
    for K in range(nK):
        for m in range(nM):
            J[K, m] = J_cost(
                K, m, w, c, kappa, h, I0, e_base, gamma, phi, lam, chi
            )
    return J


def design_index(K: int, m: int, m_max: int) -> int:
    return int(K * (m_max + 1) + m)


def km_of_index(i: int, m_max: int):
    nM = m_max + 1
    return int(i // nM), int(i % nM)


def flatten_J(J):
    return np.asarray(J, float).ravel()


def argmin_discrete(J, tie_tol=1e-14):
    """Least (K, m) in lexicographic order among discrete minimizers.

    The least and the greatest selections of a sublattice of minimizers are
    both monotone under Topkis when −J has increasing differences. Official
    m* uses this least selection (smallest K, then smallest m).
    """
    J = np.asarray(J, float)
    K_max, m_max = J.shape[0] - 1, J.shape[1] - 1
    flat = J.ravel()
    star, ties = argmin_unique(flat, tol=tie_tol)
    K, m = km_of_index(int(star), m_max)
    # argmin_unique returns the first flat index, which *is* lexicographically
    # least because of row-major (K, m) packing. Confirm.
    return dict(
        K=K,
        m=m,
        index=int(star),
        J=float(flat[star]),
        n_ties=int(len(ties)),
        tie_indices=[int(t) for t in ties],
    )


def m_star_at_K(J, K: int, tie_tol=1e-14) -> int:
    """Least minimizer of J[K, :] (K held fixed)."""
    row = np.asarray(J[K], float)
    m0, ties = argmin_unique(row, tol=tie_tol)
    return int(m0)


def W_threshold_at_K(K, c, kappa, h, I0, e_base, gamma, phi, lam, chi,
                     m_max, w_hi=1e6, n_bisect=80):
    """Exact (up to bisection) infimum of w such that m*_K(w) ≥ 1, at fixed
    prices and λ, χ. Returns +inf if m* stays 0 even at w_hi.

    Single-crossing is a theorem: −J has increasing differences in (m, w)
    at fixed K, so the set {w : m*(w) ≥ 1} is an upper interval (or empty).
    """
    def m_of(w):
        J = J_table(K, m_max, w, c, kappa, h, I0, e_base, gamma, phi, lam, chi)
        # only row K is needed, but the helper builds a small table
        return m_star_at_K(J, K)

    if m_of(0.0) >= 1:
        return 0.0
    if m_of(w_hi) < 1:
        return math.inf
    lo, hi = 0.0, float(w_hi)
    for _ in range(n_bisect):
        mid = 0.5 * (lo + hi)
        if m_of(mid) >= 1:
            hi = mid
        else:
            lo = mid
    return float(hi)


# ---------------------------------------------------------------------------
# Mutation graph on (K, m)
# ---------------------------------------------------------------------------

def design_edges(K_max: int, m_max: int):
    """Undirected mutation graph.

    Edges:
      - local: (K, m) — (K±1, m) and (K, m±1), staying in range;
      - adopt/drop: (K, 0) — (K, m) for every m ≥ 1.

    The adopt/drop edges are there because κ I_0 is a fixed cost paid at
    every m ≥ 1. J(m) for m ≥ 1 is convex, but J(1) can exceed J(0) even
    when some larger m beats J(0), so ±1 steps in m would have to cross a
    fitness valley to reach m*. Connecting 0 to every positive m makes
    that valley traversable in one mutation, the same way a lineage can
    start rehearsing at a useful number of rollouts rather than only at
    m = 1. The graph is connected, and equal edge clocks plus Moran
    fixation still give π ∝ exp(−β J).
    """
    edges = []
    seen = set()

    def add(i, j):
        if i == j:
            return
        a, b = (i, j) if i < j else (j, i)
        if (a, b) not in seen:
            seen.add((a, b))
            edges.append((a, b))

    for K in range(K_max + 1):
        for m in range(m_max + 1):
            i = design_index(K, m, m_max)
            if K + 1 <= K_max:
                add(i, design_index(K + 1, m, m_max))
            if m + 1 <= m_max:
                add(i, design_index(K, m + 1, m_max))
            if m == 0:
                for mp in range(1, m_max + 1):
                    add(i, design_index(K, mp, m_max))
    return edges


# ---------------------------------------------------------------------------
# Worlds
# ---------------------------------------------------------------------------

# Locked price defaults (also written into predictions.json at lock).
DEFAULT_PRICES = dict(
    h=0.25,
    c=0.05,
    kappa=0.2,
    lam=0.0,
    chi=1.0,
    K_max=3,
    m_max=40,
)

# Official / pilot ladders (locked).
W_LADDER = (0.02, 0.05, 0.10, 0.20, 0.50, 1.0, 2.0, 5.0, 10.0, 20.0)
C_LADDER = (0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1.0)
LAM_LADDER = (0.0, 0.5, 1.0, 2.0, 5.0, 10.0)
# Locked cells used for the "below / above threshold" clauses and for P4.
W_LOW = 0.02
W_HIGH = 20.0
P4_W = 20.0
P4_C = 0.05
P4_LAM = 0.0
P3_W = 5.0
P3_LAM = 0.0


def draw_world(rng: np.random.Generator) -> dict:
    """A world is a residual scale, a layer return, a model fidelity, and a
    model size. Ranges are locked so that, at the locked prices, the
    first-bit threshold at every K ∈ {0..3} sits strictly between W_LOW
    and W_HIGH, and the joint m* at P4_W = 20 is at least 2 and strictly
    below m_max, at every corner of the locked box (checked pre-lock).
    Official-valid still requires those properties on the drawn world.
    """
    return dict(
        e_base=float(10 ** rng.uniform(-0.3, 0.3)),  # ~0.50 .. 2.00
        gamma=float(10 ** rng.uniform(-0.3, 0.3)),   # ~0.50 .. 2.00
        phi=float(rng.uniform(0.35, 0.80)),
        I0=float(10 ** rng.uniform(-1.0, -0.3)),     # 0.10 .. 0.50
    )


def world_from_seed(rng_seed: int) -> dict:
    if seed_collides(rng_seed):
        raise ValueError(f"seed {rng_seed} collides with a prior test set")
    rng = np.random.default_rng(rng_seed)
    w = draw_world(rng)
    w["rng_seed"] = int(rng_seed)
    return w


# ---------------------------------------------------------------------------
# Monotone checks (exact, discrete)
# ---------------------------------------------------------------------------

def is_nondecreasing(seq) -> bool:
    seq = list(seq)
    return all(seq[i] <= seq[i + 1] for i in range(len(seq) - 1))


def is_nonincreasing(seq) -> bool:
    seq = list(seq)
    return all(seq[i] >= seq[i + 1] for i in range(len(seq) - 1))


def m_star_ladder_in_w(world, prices, w_ladder, K: int, lam=None):
    lam = prices["lam"] if lam is None else lam
    out = []
    for w in w_ladder:
        J = J_table(
            prices["K_max"], prices["m_max"], w, prices["c"], prices["kappa"],
            prices["h"], world["I0"], world["e_base"], world["gamma"],
            world["phi"], lam, prices["chi"],
        )
        out.append(m_star_at_K(J, K))
    return out


def m_star_ladder_in_c(world, prices, c_ladder, K: int, w=None, lam=None):
    w = P3_W if w is None else w
    lam = P3_LAM if lam is None else lam
    out = []
    for c in c_ladder:
        J = J_table(
            prices["K_max"], prices["m_max"], w, c, prices["kappa"],
            prices["h"], world["I0"], world["e_base"], world["gamma"],
            world["phi"], lam, prices["chi"],
        )
        out.append(m_star_at_K(J, K))
    return out


def m_star_ladder_in_lam(world, prices, lam_ladder, K: int, w=None):
    w = prices.get("w_for_lam", 1.0) if w is None else w
    out = []
    for lam in lam_ladder:
        J = J_table(
            prices["K_max"], prices["m_max"], w, prices["c"], prices["kappa"],
            prices["h"], world["I0"], world["e_base"], world["gamma"],
            world["phi"], lam, prices["chi"],
        )
        out.append(m_star_at_K(J, K))
    return out


def joint_star_ladder_in_w(world, prices, w_ladder, lam=None):
    lam = prices["lam"] if lam is None else lam
    rows = []
    for w in w_ladder:
        J = J_table(
            prices["K_max"], prices["m_max"], w, prices["c"], prices["kappa"],
            prices["h"], world["I0"], world["e_base"], world["gamma"],
            world["phi"], lam, prices["chi"],
        )
        star = argmin_discrete(J)
        spend = (
            prices["kappa"] * I_mem(star["m"], world["I0"])
            + prices["h"] * star["K"]
            + prices["c"] * star["m"]
        )
        E = expected_loss(
            star["K"], star["m"], world["e_base"], world["gamma"], world["phi"]
        )
        rows.append(dict(w=w, K=star["K"], m=star["m"], spend=spend, E=E, J=star["J"]))
    return rows


# ---------------------------------------------------------------------------
# P4 occupation statistics
# ---------------------------------------------------------------------------

P4_BETA = 40.0
P4_TOL_M = 1.5  # official bar on |mean m − m*|; exact Boltzmann on the
# tightened box sat inside 0.77 on 20 pilots and 4000 box draws were not
# used for this number; the 20-pilot exact max at β=40 was 0.767.


def occupation_m_stats(occ, m_max: int, m_star: int):
    """From a flattened occupation vector, return marginal-m diagnostics."""
    occ = np.asarray(occ, float)
    n = occ.size
    ms = np.array([km_of_index(i, m_max)[1] for i in range(n)])
    Ks = np.array([km_of_index(i, m_max)[0] for i in range(n)])
    if occ.sum() <= 0:
        return dict(
            mean_m=float("nan"), mean_K=float("nan"),
            marg_mode_m=-1, mass_at_mstar=0.0,
            mass_within_1=0.0, abs_err=float("inf"),
        )
    p = occ / occ.sum()
    mean_m = float(np.dot(p, ms))
    mean_K = float(np.dot(p, Ks))
    marg = np.array([float(p[ms == m].sum()) for m in range(m_max + 1)])
    marg_mode = int(np.argmax(marg))
    return dict(
        mean_m=mean_m,
        mean_K=mean_K,
        marg_mode_m=marg_mode,
        mass_at_mstar=float(marg[m_star]) if 0 <= m_star <= m_max else 0.0,
        mass_within_1=float(p[np.abs(ms - m_star) <= 1].sum()),
        abs_err=float(abs(mean_m - m_star)),
        marg=marg.tolist(),
    )


def p4_prices(base=None):
    P = dict(base or DEFAULT_PRICES)
    return dict(w=P4_W, c=P4_C, lam=P4_LAM, **{k: P[k] for k in
                ("h", "kappa", "chi", "K_max", "m_max")})
