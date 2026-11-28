# EVO1 preregistration: a designed-world, in-silico evolution test of the hypothesis

Friday 20 November 2026, written by a Grok Bot executor for Chad Mitchell on branch `v2.6-evo`. Not reviewed. This file, the
code and the prediction file are locked by SHA-256 in `PREREG_EVO.sha256`, committed **before any evolution run in a test
world** (the commit time is the record; the time typed here is approximate). Nothing below is changed after a run; any
deviation goes in `DEVIATIONS_EVO.md` with its time (America/New_York, ET).

## 1. What is tested, and what a result can and cannot mean

The hypothesis as THEORY.md §3 states it: **The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**

EVO1 builds worlds whose spectrum, read noise and prices the experimenter sets, lets a population of agents evolve under
mutation and selection on **realized outcomes**, and asks whether the evolved designs sit inside the preregistered band
around the design that minimizes J, as computed separately from the theory's closed forms and optimizers.

**Honest caveat (fixed now).** An in-silico PASS shows that the theory's minimum is what selection finds when it acts on
outcomes priced with these costs, in these worlds; it does **not** show that nature obeys the hypothesis. It is evidence that
J books the costs a lineage actually experiences (continuous-time algebra vs a discrete, noisy, finite-life world with a
ruin gate) and that the optimizer the repository uses finds the same designs that selection does. A FAIL, however, would be a
real problem for the theory as stated: inside its own premises, strongly selected agents would not sit at argmin J. A FAIL
must be diagnosed causally (optimizer, selection strength, cost mismatch, discretization) and rerun under the rules in §8,
never explained away; the first verdict stays on record.

## 2. Non-circularity

- `evo.py` (the simulator) imports only numpy and numba. It does not import `predict_evo.py`, `stores.py`, `face_hybrid.py`
  or read `PREDICTIONS_EVO.json`. Fitness is built from what happened in each life: upkeep paid per store, a price per unit
  store rate, the stake times the **realized** squared error of the agent's estimate of the **realized** signal, and death
  when a reserve (buffer + income − realized costs) hits zero. No expected-cost formula appears in it.
- `predict_evo.py` (the J prediction) uses only repository code: `theory/layers_checks/stores.py` (Model S, CT21),
  `figures/face_hybrid.py` (B.11 class, CT35/CT36, with common read noise `Nc` and shared-store delay), and the Model S+
  store-noise covariance of `theory/STORE_NOISE.md` §2 (as in `theory/store_noise/checks.py`). It never runs the simulator.
- **Shared inputs, disclosed.** Both read `worlds.json`, the experimenter's world specification. Theory-informed choices in
  it, all made before any test-world run: (i) prices were chosen with `predict_evo.py` so that each world discriminates (for
  example h in W2 so that a second store pays by about 3.4%; hc in W4b so that X_S = 0.9 < 1 while κ_S = 1.27 > 1); (ii) the
  ruin gate income = 2·J*_pred and buffer = 0.05·T_score·income (a scale only; it carries no rate or count information);
  (iii) the counting band per world.
- **What the design cannot exclude** (the usual circularity, as LEARNSIM's referee put it): a good optimizer of realized cost
  approaches the world's true optimum, so agreement mainly tests J's bookkeeping and the repository's optimizer against
  selection. That is the point of the test, and the reason a PASS says nothing about nature.

## 3. The simulator (frozen)

Time unit one step (dt = 1). Each generation draws one fresh world realization that every agent lives in (common random
numbers; one population, one world). OU modes are exact AR(1) discretizations with stationary starts; the random walk starts
at 0. Reads y = s + private noise (variance N per step) + common noise (Nc, same for all units of a group). A store is a
leaky integrator z ← z + (1 − e^(−b))(input − z); local stores read their unit's y, shared stores read the group's mean y and
are used `delay` steps late. The estimate is Σ g·z. Store-noise arm: each store's output carries its own AR(1) noise at the
store's rate with stationary variance V0·(τ0·b)^(2−2s) (Model S+ E1, referred to the input). Cost per step = n·h·(local
stores) + hc·(shared stores) + h1·(sum of store rates, local counted per unit) + w·Σ_units (s − ŝ)²; scored after a burn-in.
Genome: up to 4 local and (group worlds) 4 shared stores, each a rate and a read weight. Mutation per offspring: every log
rate +N(0, 0.04); every weight + N(0, 0.03·(|g| + 0.05)); then one structural move with probability 0.02 duplicate-split
(copy at rate × e^(N(0,0.5)), the weight halved over the two), 0.02 delete (weight passed to the nearest store of its class),
0.01 class switch (group worlds). Selection: Wright–Fisher, P = 300, fitness exp(−β·(C − C_med)/C_med) with β = 30 for
survivors and 0 for the dead; C is the realized mean cost per step. Exponential fitness makes a lineage's long-run log growth
linear in its mean realized cost, so selection acts on expected cost (THEORY's J), not on cost variance, except through
death. 600 generations; seeds 0–7 per world (even seeds start every agent with one store at a random rate; odd seeds start
with four stores, or two local and two shared, at random rates); the evolved design is the modal store structure over the
last 10% of generations, then the median log rate and median weight of each rate-ordered store.

**Selection strength vs drift (THEORY §3 (c)).** σ = β = 30 (the fractional change in fitness per fractional change in
realized cost) and N_e ≤ P = 300, so ε = 10/(σ·N_e) = **EPS_BAND = 1/900 = 0.00111**. This is the band in J. The power
condition (d) is checked per rival below (β·P·gap ≥ 10). Fitness noise from finite lives was measured on fixed designs
(§4): per-generation paired noise is far below the rival gaps everywhere except the store-noise arms, where lives were
lengthened tenfold (T_score 400,000) before the lock to bring the noise to about 1% per generation.

## 4. Pre-lock work (disclosed in full)

1. **Pilots** (`pilot/`): two out-of-design worlds (PILOT_OU: one OU mode a = 0.02; PILOT_2M: two modes a = 0.001, 0.03),
   two seeds each, 600 generations, to set the number of generations. All four landed inside the band (J gaps 1.4e−12 to
   1.4e−4; rule-counted structure as predicted; populations stable after about 200 generations). One oddity was checked: in
   PILOT_OU seed 1 the consensus rate equals the predicted rate to 3e−6 relative (seed 0: −0.85%). The simulator has no
   path to the prediction (it imports nothing from the theory; worlds.json carries no rate), and the population's IQR is
   0.15 in log rate, so this is read as a coincidence; it is reported, not used.
2. **Calibration** (`calibrate_evo.py`, `CALIBRATION_EVO.json`): the predicted design and the alternative designs were run as
   FIXED designs in 40 independent worlds each (no selection, no search of the realized-cost landscape). Purpose: check that
   the simulator charges what the specification states, and measure fitness noise. Result: realized cost at the predicted
   design is 0.8–2.0% below J* in the OU and random-walk worlds (a discretization offset at dt = 1; it shifts every design,
   and both sides of the comparison use the same J, so it is not added to the band) and +0.4% in the store-noise arms.
3. The B.11 counting rule cannot resolve W4b's predicted design (its shared pole, τ = 16, lies within ×3 of its local pole,
   τ = 21; the rule's fitted "shared" pole at τ ≈ 2.3 is an artifact of the 1-step delay and the cancelling read weight).
   **Declared now:** in W4b the structure (criterion B) is scored on the genome (stores and their class, observable only in
   silico), not by the rule. Everywhere else the rule is used.

## 5. Predictions (from `PREDICTIONS_EVO.json`; λ = mode rate, τ = 1/b; group worlds n = 4)

| World | Setting | Predicted design (rule-counted) | Predicted time constants τ (steps) and λτ | Local/shared | J* | Rate band (|Δ ln τ|) |
|---|---|---|---|---|---|---|
| PC | OU a=[0.01], v=[1.0], N=13.3333, h=0.05, h1=0, w=1 | 1L0S (genome 1L0S) | τ=[25.0]; λτ=[[0.25]] | 1 local, 0 shared | 0.45000 | [0.072] |
| W1 | OU a=[0.01], v=[1.0], N=13.3333, h=0.05, h1=1, w=1 | 1L0S (genome 1L0S) | τ=[29.8]; λτ=[[0.298]] | 1 local, 0 shared | 0.48651 | [0.07] |
| W2 | OU a=[0.0005, 0.02], v=[0.7, 0.3], N=10, h=0.004, h1=0, w=1 | 2L0S (genome 2L0S) | τ=[241.3, 24.6]; λτ=[[0.121, 4.825], [0.012, 0.492]] | 2 local, 0 shared | 0.25103 | [0.225, 0.111] |
| W3 | random walk q=0.001, N=1, h=0.005, w=1 | 1L0S (genome 1 stores) | τ=[31.6]; λτ=— (no mode) | 1 local | 0.03662 | [0.051] |
| W4 | OU a=[0.001, 0.05], v=[0.6, 0.4], N=10, Nc=5, n=4, ρ=[1, 0], delay=20, h=0.02, hc=0.04, h1=0, w=1 | 1L1S (genome 1L1S) | τ=[14.1, 105.1]; λτ=[[0.014, 0.705], [0.105, 5.255]] | 1 local, 1 shared | 1.69158 | [0.134, 0.183] |
| W4b | OU a=[0.02], v=[1.0], N=11.905, Nc=22.09, n=4, ρ=[0.0443], delay=1, h=0.11002, hc=0.22592, h1=0, w=1 | 1L1S (genome 1L1S) | τ=[20.8, 16.0]; λτ=[[0.416], [0.319]] | 1 local, 1 shared | 3.08766 | [0.075, 0.159] |
| S031 | OU λ=0.01, σ²=1, exact reads, store noise V0=10 (τ0=100), s=0.31, h=0.004, w=1 | 1L0S (genome 4 stores) | τ=[152.7]; λτ=[1.527] | 1 time constant, 4 copies | 0.92850 | [0.211] |
| S07 | OU λ=0.01, σ²=1, exact reads, store noise V0=10 (τ0=100), s=0.7, h=0.004, w=1 | 1L0S (genome 4 stores) | τ=[38.4]; λτ=[0.384] | 1 time constant, 4 copies | 0.91487 | [0.228] |

Further locked predictions:
- **Count (THEORY §5 (iii), L1/L2):** one store for one OU mode (PC, W1) and for a random walk (W3; by L1, E_2 = E_1, so a
  second store only costs); two for two separated modes (W2); one distinct time constant in the store-noise arms, with
  copies (Model S+ E1-c; the optimum here is 4 copies, the genome cap).
- **Interlacing (L2, W2):** λ₁ < b₁ < λ₂ < b₂, i.e. 0.0005 < 0.00414 < 0.02 < 0.0407; every layer faster than its mode
  (λτ = 0.121 and 0.492), the slow layer about 8× faster than its mode, not set at it.
- **Local/shared (B.11, W4):** the fast private mode is tracked locally (τ 14), the slow common mode by one shared store
  (τ 105); no second store of either class. **W4b (CT36):** one local and one shared store, although X_S = 0.9 < 1 (the
  shared store does not pay on its own); the quadrant-edge rule (and "no sharing") predicts one local store only, 1.04% worse.
- **Speed price moves the design (W1 vs PC):** Δ ln b = ln(0.03356/0.04) = −0.176.
- **Store-noise threshold (Model S+, at these SNRs, full optimum):** s = 0.31 gives a store **slower** than its mode
  (λτ* = 1.527; the low-SNR closed form (1−s)/s = 2.23 is the limit, not the prediction); s = 0.7 gives a store faster
  than its mode (λτ* = 0.384; closed form 0.43). Model S's interlacing (every layer faster than its mode) is the rival for
  s = 0.31. Δ ln b from S031 to S07 = ln(152.7/38.4) = +1.381.

**Named rivals and power (THEORY §3 (d)).** "Set at" = one store per mode at τ = 1/λ with the best read-out; "one layer
always"; "more layers always better" = the cap (4 stores, or 2 + 2); "none"; in group worlds "no sharing" and "all shared".

| World | Rival | J gap over J* | β·P·gap (≥ 10 needed) | Excluded by the band |
|---|---|---|---|---|
| PC | set_at | 0.3529 | 3176 | yes |
| PC | one_layer | 0 (identical to the prediction in this world) | — | not a rival here |
| PC | more_layers | 0.3333 | 3000 | yes |
| PC | none | 1.2222 | 11000 | yes |
| W1 | set_at | 0.2720 | 2448 | yes |
| W1 | one_layer | 0 (identical to the prediction in this world) | — | not a rival here |
| W1 | more_layers | 0.3083 | 2775 | yes |
| W1 | none | 1.0555 | 9499 | yes |
| W2 | set_at | 0.0425 | 383 | yes |
| W2 | one_layer | 0.0344 | 309 | yes |
| W2 | more_layers | 0.0319 | 287 | yes |
| W2 | none | 2.9836 | 26852 | yes |
| W3 | more_layers_K4 | 0.4096 | 3686 | yes |
| W3 | set_at | undefined for a random walk (tau = infinity): the slowest store allowed | — | — |
| W3 | none | 0 (identical to the prediction in this world) | — | not a rival here |
| W4 | set_at | 0.0906 | 815 | yes |
| W4 | one_layer | 0.0812 | 730 | yes |
| W4 | more_layers | 0.0702 | 632 | yes |
| W4 | none | 1.3647 | 12282 | yes |
| W4 | no_sharing | 0.0680 | 612 | yes |
| W4 | all_shared | 0.2311 | 2080 | yes |
| W4b | set_at | 0.0524 | 472 | yes |
| W4b | one_layer | 0.0104 | 94 | yes |
| W4b | more_layers | 0.2048 | 1843 | yes |
| W4b | none | 0.2955 | 2659 | yes |
| W4b | no_sharing | 0.0104 | 94 | yes |
| W4b | all_shared | 0.3028 | 2725 | yes |
| S031 | modelS_faster_than_mode | lam*tau < 1 (Model S interlacing, exogenous noise) | — | — |
| S031 | set_at | 0.0045 | 40 | yes |
| S07 | modelS_faster_than_mode | lam*tau < 1 (Model S interlacing, exogenous noise) | — | — |
| S07 | set_at | 0.0195 | 175 | yes |

**Calibration (fixed designs, 40 worlds):**

| World | Cost level: realized mean at predicted design vs J* (δ_sim ± se) | Realized cost sd per generation (fraction) | Nearest alternative: realized paired gap ± sd per generation |
|---|---|---|---|
| PC | -0.0094 ± 0.0059 | 0.0377 | alt_2L0S: 0.1122 ± 0.0000 |
| W1 | -0.0092 ± 0.0057 | 0.0363 | alt_2L0S: 0.1037 ± 0.0000 |
| W2 | -0.0108 ± 0.0023 | 0.0149 | alt_3L0S: 0.0161 ± 0.0000 |
| W3 | -0.0084 ± 0.0066 | 0.0421 | alt_2stores: 0.1377 ± 0.0000 |
| W4 | -0.0128 ± 0.0015 | 0.0094 | alt_1L2S: 0.0236 ± 0.0003 |
| W4b | -0.0199 ± 0.0026 | 0.0169 | alt_1L0S: 0.0251 ± 0.0080 |
| S031 | +0.0042 ± 0.0025 | 0.0159 | alt_K4: 0.0013 ± 0.0133 |
| S07 | +0.0043 ± 0.0024 | 0.0150 | alt_K4: 0.0004 ± 0.0098 |


## 6. Scoring (locked in `analyze_evo.py`; `count_rule.py` implements THEORY §3's counting rule as frozen)

Per seed (converged seeds only):
- **Criterion A (THEORY §3, cost band to design band):** J(evolved rates, theory formula, optimal read-out)/J* − 1 must be
  ≤ EPS_BAND = 0.00111. A count that differs from the predicted one is a miss under A only through its J.
- **Criterion B (count and assignment):** the structure the counting rule returns for the evolved design (isolated and
  pooled step responses, sums of exponentials K ≤ 5, ΔBIC ≥ 10, measurement noise 1% of total gain with a fixed seed,
  poles outside the band ignored, local/shared classified before merging, merge within ×3, count by degree) must equal the
  structure the same rule returns for the predicted design (W4b: genome structure, §4.3).
- A seed **misses** if A or B fails.
- **World verdict (binomial allowance, coverage c = 0.90, α = 0.05, n = 8 seeds):** PASSED if misses ≤ 1; INCONCLUSIVE if
  2; FAILED if ≥ 3 (P(Bin(8, 0.10) ≥ 3) = 0.038 < 0.05).
- **Secondary (reported, each with its own verdict):** evolved rule-counted time constants within the rate band of §5
  (|Δ ln τ| ≤ √(2·EPS_BAND·J*/H), H the curvature of J in log rate); W2 interlacing (PASSED if ≥ 7 of 8 seeds interlace,
  FAILED if ≥ 3 do not); the store-noise threshold (S031 slower than its mode and S07 faster in ≥ 7 of 8 seeds each:
  PASSED; ≥ 3 disagreeing: FAILED); design moves with its inputs (median across seeds of Δ ln b for PC→W1 and S031→S07
  has the predicted sign and lies within √(band_a² + band_b²) of the prediction: PASSED, else FAILED).

## 7. Controls and INVALID conditions

- **Positive control (PC):** one OU mode, reading unpriced, no speed price: the optimum is the Kalman–Bucy store,
  b* = λ√(1 + 2v/(Nλ)) = 0.04 exactly (L1). If PC is not PASSED, every world is **INVALID** (the machinery cannot find a
  known optimum).
- **Null control:** 4 seeds per world (100–103) with selection off (β = 0, no death), same mutation and generations. If ≥ 2
  of 4 null seeds meet both criteria, the criteria do not discriminate in that world: **INVALID**.
- **INVALID** also if: fewer than 6 of 8 seeds converged (a seed whose median cost still falls between the last two 10%
  windows by more than 3 SE and more than EPS_BAND·J* is unscored); the nearest named rival has β·P·gap < 10; or the ruin
  gate binds (mean final-window death fraction > 10%), which takes the world outside THEORY's ruin-slack premise.

## 8. If a world fails (diagnosis protocol, fixed now)

A FAILED or INVALID world is diagnosed from first principles before anything is rerun, in this order, each step recorded in
`DEVIATIONS_EVO.md` with its time: (1) **optimizer:** recompute the predicted design with more starts and the exact
discrete-time cost (discrete Lyapunov at dt = 1); if the discrete optimum differs from the continuous one by more than the
band and the evolved design matches the discrete one, the verdict is INVALID (prediction mis-specified for the simulator's
step) and the world is rerun at dt/4 (sub-stepping), with the first verdict kept on record; (2) **selection strength:** if
null-like scatter, rerun with P ×4 and generations ×2; (3) **cost mismatch:** if neither, compare realized cost of the evolved
and predicted designs on fixed designs (as in §4.2): if the evolved design is realized-cheaper than J's minimum, J omits a
cost the world charges (or charges one it does not), which is a **real miss for the theory as stated**, reported as such.
Reruns never replace a first verdict; both are reported.

## 9. Locked files

`PREREG_EVO.sha256` lists SHA-256 of: this file, `worlds.json`, `predict_evo.py` (the J-prediction script),
`PREDICTIONS_EVO.json`, `evo.py`, `count_rule.py`, `analyze_evo.py`, `calibrate_evo.py`, `CALIBRATION_EVO.json`,
`runall.sh`, and the repository files the prediction imports (`theory/layers_checks/stores.py`, `figures/face_hybrid.py`).
