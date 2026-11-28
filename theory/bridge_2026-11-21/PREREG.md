# Preregistration: T27, selection as a thermal search over Model S designs

**Locked:** Friday 20 November 2026, late evening ET (America/New_York), in `/workspace/gtao-thermo` on branch `thermo-bridge-2026-11-21`, beside `main` `7275c4b`. Written *before* any evaluation of reduced J, any Hessian, and any Moran chain on the official worlds of this test. A SHA-256 of this file and of `predictions.json` is recorded in `LOCK.txt` at lock time. Neither file is edited after lock except to correct a typo that does not change a criterion, which would itself be a dated deviation.

**This is a new prereg, not a re-score.** It does not reuse or re-score EVO1, S5, T20, or any other existing run. Official Model S worlds are drawn from the same *generator* as `theory/keystone_checks/s5_rerun.py` (`convexity_targeted.py`) but with fresh RNG seeds that do not collide with prior test sets (checked in `bridge_lib.seed_collides`).

**Hypothesis under test (may be wrong).** Under weak-mutation selection with Malthusian fitness proportional to minus the reduced cost J, the stationary distribution over a discretized design space is Boltzmann, π ∝ exp(−β J), with β set by selection strength. Consequently, at high β the typical design is the cost-minimizing one, the mean excess cost scales as (d/2)/β near a quadratic minimum (equipartition), and at low β the mass spreads and the mean stays above J*. This is an in-model numerical test of that mapping, not a field test of the hypothesis in `CORE.md`. Status labels later: `in-model`, `numerical`. Nothing here is `PROVED` about nature. Field-untested.

**What is not under test.** The thermodynamic floor (Landauer; Still, Sivak, Bell & Crooks 2012), CT4, SCALE_ENDS, and the operational qualification rule of THEORY §3 / FRAMEWORK §9 are already in the repository and are not re-tested here. This run tests only the selection-search consequences (mode, equipartition spread, low-β spread) in Model S.

---

## 0. What is already on disk (readable, not a result of this test)

- Merged solver: `theory/layers_checks/stores.py` (Jacobi-scaled truncated inverse, v2.67 / PR #116). Not modified.
- World generator: bit-identical in *distribution* to `s5_rerun.py` `world()`, with the RNG seed passed in directly. S5 itself uses `default_rng(1000 + seed)` for seed 0..119. Official seeds here start at 2026112100.
- Design work that informed the locked grid, β, and jump counts used *only* the already-published S5 world with rng seed 1000 (convexity_targeted seed 0). Those numbers are not official results and are not scored.
- No official candidate seed in `predictions.json` was evaluated before lock.

---

## 1. Reduced cost and fitness map

The master equation is unchanged. This test uses the same dimensionless reduction as N60 / T20:

$$J(\mathcal D)=K+R\,\frac{E(\mathcal D)}{E_\infty},\qquad R=100,$$

where E(𝒟) is the MSE of the *named* store rates of 𝒟 (not the optimized E_K), E_∞ is the Yovits–Jackson causal MMSE, and K=0 uses E=∑v (act blind). κ, A and L are not varied (set aside, as in N60).

**Assumption, not a theorem:** Malthusian fitness is m(𝒟) = −α J(𝒟), and Wrightian birth rates are r = exp(m). This is the “fitness proportional to −J” map of the design. Real fitness maps can be nonlinear; that is outside this test.

**Haploid Moran, weak mutation (standard).** On a connected undirected design graph with equal mutation clocks on each edge, the origination–fixation chain has stationary distribution

$$\pi(\mathcal D)\propto \exp(-\beta J(\mathcal D)),\qquad \beta=\alpha(N-1),$$

with N = N_POP the locked population size. This is detailed balance for the Moran fixation probability, not a new theorem. The official run *simulates* that process; it does not sample the Boltzmann distribution directly. The exact Boltzmann weights on the finite grid are computed as a mixing check and as a labeled diagnostic, never as an official pass bar.

---

## 2. Design spaces

**Coarse space (P1, P3).** Shared log-rate grid of N_GRID = 21 points, from ln(a_min)−LO_PAD to ln(a_max)+HI_PAD, with LO_PAD=2 and HI_PAD=5. Designs are K=0 and all strictly increasing index tuples for K=1,2,3. Mutation: move one index by ±1 (staying strictly increasing), or add/drop one index; for K≥2 a dropped/added index must be adjacent to the remaining set; K=1 ↔ K=0 is always allowed. The graph is required to be connected from the argmin (validity).

**Fine space (P2).** After a world passes the coarse validity screen, polish the unique interior K=2 coarse argmin by local L-BFGS-B on the two log-rates, estimate the Hessian H of reduced J there by central differences, and (if H is symmetric positive definite) build a product lattice in whitened coordinates y = Lᵀ(θ−θ_*), H = L Lᵀ, with each y_i on linspace(−P2_HALF, P2_HALF, P2_N_AXIS) = linspace(−3.5, 3.5, 51). Mutation on this lattice is 4-neighbor. d = 2. J* for P2 is the minimum of reduced J on this lattice, not the coarse minimum.

---

## 3. Official worlds

- Candidate rng seeds: BASE_WORLD_SEED + i for i = 0..15, i.e. 2026112100..2026112115, listed in `predictions.json`.
- These seeds must not collide with prior Model S generators (`seed_collides`); a collision is a protocol bug and aborts the run.
- Walk the candidates in listed order. A candidate is **official-valid** if and only if all of the following hold:
  1. Unique coarse argmin, at K=2, with both log-rates off the grid boundary.
  2. The coarse mutation graph is connected from that argmin.
  3. The polished Hessian is SPD, with the smaller eigenvalue > HESS_EV_MIN = 10^{−4}.
  4. At every locked high β, the exact Boltzmann mass on K=2 in the coarse space is ≥ MASS_K2_MIN = 0.95.
  5. The fine-lattice argmin is interior (not on the y-boundary).
  6. Every official Moran cell for that world mixes: total variation between the pooled empirical occupation and the exact Boltzmann weights is ≤ MIX_TV_MAX = 0.20.
- The first N_OFFICIAL = 3 official-valid candidates are the official worlds. Further candidates are not run once three are in hand.
- If fewer than three official-valid worlds are found in the 16 candidates, the test is **INCONCLUSIVE**, not a fail and not a pass.

---

## 4. Moran process (locked)

- Population N_POP = 201, haploid Moran fixation, equal edge clocks, continuous-time occupation (no degree bias).
- β_high = {8, 10, 12}; β_low = 0.5. α = β / (N_POP − 1).
- N_CHAINS = 8 independent chains per (world, β, space).
- High-β and P2: N_JUMPS = 200,000 jumps per chain, BURN_JUMPS = 20,000.
- Low-β (P3 only): N_JUMPS_LOW = 400,000, same burn.
- Chain RNG seeds: CHAIN_SEED_BASE + 1000·world_index + 10·round(10β) + c for the coarse space, and CHAIN_SEED_BASE + 1000·world_index + 70000 + 10·β + c for the fine space, with CHAIN_SEED_BASE = 20261121500 and c = 0..7.
- Coarse starts: chains 0–3 at the K=0 design (designs[0]); chains 4–7 at the coarse argmin.
- Fine starts: chains 0–1 at the lattice centre (y nearest 0); chains 2–7 at the fine argmin.
- Official occupation is the pooled continuous-time occupation after burn-in.

---

## 5. Numeric pass / fail gates (written before any official run)

### 5.1 Prediction (P1): mode = argmin at high β

On the coarse space, for each official world and each β in {8, 10, 12}: the unique mode of the pooled occupation equals the unique coarse argmin of J. The world passes P1 if all three β cells pass. Official P1 is the conjunction over the three official worlds.

### 5.2 Prediction (P2): equipartition at high β

On the fine K=2 lattice, for each official world and each β in {8, 10, 12}:

$$
\left|\frac{\beta\,(\bar J - J^\star) - d/2}{d/2}\right| \le 0.20,
$$

with d = 2, so the target is 1, and J* is the minimum on that lattice. The world passes P2 if all three β cells pass. Official P2 is the conjunction over the three official worlds.

Exact Boltzmann β-excess on the same lattice is reported as a diagnostic and is not an official gate.

### 5.3 Prediction (P3): spread at low β

On the coarse space, at β = 0.5, for each official world, all three of the following hold:

1. Mean reduced J is strictly greater than the coarse J*.
2. At least two distinct layer counts K have pooled occupation mass ≥ 0.10.
3. The low-β excess is at least P3_EXCESS_RATIO = 2 times the mean high-β *empirical* coarse excess for that world.

Official P3 is the conjunction over the three official worlds.

### 5.4 Overall

- **PASS** if and only if there are three official-valid worlds and P1, P2 and P3 all pass on every one of them.
- **FAIL** if there are three official-valid worlds and any of P1, P2, P3 fails on any official world.
- **INCONCLUSIVE** if fewer than three official-valid worlds are obtained from the 16 candidates.

A mixing miss or a fine-min-on-boundary is a validity miss for that world, not a prediction fail. Predictions will not be patched after seeing official data. A change of criterion, if one is ever needed, goes in a dated DEVIATIONS file *before* any further official scoring, and the original gates remain the official result of this prereg.

---

## 6. Pilot (not official)

Grid, β window, and jump counts were chosen on S5 rng seed 1000 only, where at R=100 the coarse argmin was an interior K=2, the Hessian was anisotropic (eigenvalues about 0.99 and 17.2), a raw log-rate grid was too coarse for equipartition, and a whitened 51×51 lattice of half-width 3.5 put the exact Boltzmann β-excess within a few percent of 1. Those pilot figures are design inputs, not results of T27.

---

## 7. What would not be a rescue

- Changing R, β, the grid, or the 20% band after seeing official scores.
- Scoring official P2 on the exact Boltzmann weights instead of the simulated occupation.
- Dropping a failing official world and walking further through the candidate list to replace it. The first three official-valid candidates are the official set; they are not replaced.
- Re-interpreting a mixing miss as a prediction pass or fail.
