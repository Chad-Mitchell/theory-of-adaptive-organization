# WORLD_TRACK (FOR-40): Step 0 TASK-LEVER, then Step 1 WORLD-TRACK

*26 Nov 2026, started 18:35 ET. Local note only (not committed or pushed). Append-only. Each step is written in the order: pre-statement, hash logged in the WORKLOG, computation, results, hostile self-review. Repo text is cited from main `8b553c6`. The corrected CORE cites are J at CORE.md:27 and w at CORE.md:29 (REQUIREMENTS_FIRST §8 C5). Labels: **PIM** = proved in-model; **ELEMENTARY**; **KNOWN**; **HYP**; **OBSERVED** = numerical output of the scripts in `worldtrack/`. "Open miss" marks a prediction that did not come out. DOIs were checked on Crossref this session (`worldtrack/crossref_wt.txt`, 12 of 12 OK).*

## Step 0. TASK-LEVER: pre-statement (written before any Step 0 number was computed)

### 0.1 Question

In SR_B §1's class (pure-state jumps, all effects, move cost Σ d_t² with the operational distance), does the **form of the scored task alone** decide between the disk and the polygons?

- REQUIREMENTS_FIRST P15 (PIM, self-checked only): a positional loss gives the disk.
- SR-b3 (PIM): reaching a perfectly distinguishable vertex gives the (2T+2)-gon.
- What happens to a mixture of the two? Is there one switch point α*?

### 0.2 Model

- **Designs.** The regular n-gon with all effects, n = 3 … N(T) with N(T) = max(60, 6T + 10), or the disk. Vertex k sits at angle 2πk/n. The start is v₀ at angle 0.
- **Distances.** d(u, w) = max over directions θ of ⟨u − w, θ⟩ / width_θ(P).
  - For a polygon this is evaluated exactly at the breakpoints of the width function (edge normals and their negatives). Between breakpoints the ratio is monotone in θ, so the maximum lies on one of them.
  - For the disk, d = sin(Δφ/2).
- **Moves.** T ticks. Each tick jumps to a pure state, and staying put (cost 0) is allowed. Move cost M = Σ d_t².
- **Score at the end** (endpoint angle φ, endpoint state e), with stake λ and mixing weight α ∈ [0, 1]:
  - **positional loss** L_pos = (1 + cos φ)/2: the error to the target angle π, which depends only on the angle;
  - **reach loss** L_reach = 1 − d_D(v₀, e): the shortfall from perfect distinguishability, in the design's own geometry;
  - **cost** C_D(α) = min over paths of [M + λ(α·L_pos + (1 − α)·L_reach)].
- **Computing C_D.**
  - **Polygons:** an exact min-plus DP over vertices for the minimal move cost to each vertex in ≤ T steps. The score is then a minimum over endpoints.
  - **Disk:** endpoint move cost D(φ) = min over k ≤ T of k·sin²(φ/(2k)), an achievable path. A DP on a 3600-point angle grid checks this: the DP must never fall below the formula by more than 1e−9. If it does, the DP value is used and the discrepancy reported. The minimum over φ ∈ [0, π] uses a 20 001-point grid plus golden refinement.
- **Reproduction gate.** Before anything else, the hard-constraint values must reproduce SR_B: the hexagon 0.5 at T = 2, the 7-gon 0.5942 at T = 3, the 9-gon 0.4825 at T = 4 (M3h rule). If any fails, Step 0 stops and reports.

### 0.3 Ranges (fixed now)

T ∈ {2, 3, 4, 5, 6, 8, 10, 12, 16, 20}; λ ∈ {2, 5, 10, 30, 100, 1000}; α on a grid of step 0.005 (201 points), with every sign change of Δ bisected to 1e−10. That makes 60 (T, λ) cells.

### 0.4 Predictions, and HIT, MISS, OPEN

Write Δ(α) = C_disk(α) − min_n C_n(α), and let W = {α : Δ(α) > 1e−12} be the set where some polygon is strictly cheaper.

- **P15 check (must hold; PIM claim):** Δ(1) ≤ 1e−12 in all 60 cells. More strongly, at α = 1 every polygon endpoint costs at least the disk endpoint at the same angle. Any violation means P15 is false as stated, and that is reported first.
- **HIT:** the switch is a single threshold. Among the cells where W is a proper non-empty subset of [0, 1], at least 95% have W = [0, α*) (one crossing).
- **MISS:** more than 5% of those cells have W that is not a single initial interval (designs interleave in α).
- **OPEN:** ties (|Δ| < 1e−9 over more than 10% of the α grid) make more than 20% of the cells ambiguous, or fewer than 10 cells have a proper W.
- **Secondary (HYP, heuristic, not part of the score):** at λ ≥ 30 and T ≥ 4, α*·λ lies in [1, 3].
  - Reason: the (2T+2)-gon's transport advantage over the disk is ≈ π²/(2T²). Its endpoint misses angle π by π/(T+1), which costs λα·sin²(π/(2T+2)) ≈ λα·π²/(4T²). So α* ≈ 2/λ.
  - Reading: at a large stake, a small positional share is enough to make the disk win.
- **p(HIT) = 0.75** (stated now). Each design's C(α) is concave (a minimum of affine functions), so Δ is a difference of concave functions, and a single crossing is not automatic.

### 0.5 Triviality test (fixed now)

- **Trivial in substance:** in at least 80% of the crossing cells the arg-minimizers (the best polygon's n and endpoint, and the disk's endpoint) do not change across α. Then Δ is affine, and one crossing is automatic.
- **Even if non-trivial,** Step 0 is ELEMENTARY: it maps which task form selects which geometry. It does not derive a geometry from the cost alone.

### 0.6 Inputs chosen by us (listed as required)

- **Task parameters, chosen on purpose to map the lever:** T, λ, α. In the theory these are task inputs (the loss and the stake, CORE.md:27, :29), not derived.
- **Model choices:** pure-state jumps (P8 shows mixed states tie everything); Σd²; the vertex-to-angle embedding 2πk/n; the shapes (1 + cos φ)/2 and 1 − d; the start at v₀; the menu.

### 0.7 Disclosure added after hashing (fix 8 of REVIEW_P15, received 18:36; appended before the results below were written)

- **How ties count at α = 1.** The §0.2–§0.4 pre-statement, hashed `645e5857…b105`, did not say this in words. It is fixed by the definition W = {α : Δ(α) > 1e−12}.
  - An α where a polygon only ties the disk (|Δ| ≤ 1e−12) is **not** in W. It counts on the disk's side ("disk weakly best").
  - So "the disk above α*" means "no polygon strictly cheaper above α*". It does not mean the disk is uniquely best there.
  - The rule was fixed by the hashed definition before any computation. This paragraph states it in words, and nothing in the rule is new.
- **In the data the rule did not matter.** Δ(1) < 0 strictly in all 60 cells: the largest Δ(1) is −6.1e−6, so the disk was strictly cheaper at α = 1 everywhere. No α-grid point in any cell had |Δ| < 1e−9 (0 ambiguous cells).
- **REVIEW_P15's class split, applied here.** L_pos is a geometric, design-independent loss, so it is in P15's class. L_reach is operational and design-dependent, so it is outside. Step 0 therefore measures the switch between the two loss classes, as REQUIREMENTS_FIRST §10.4 states it.

## Step 0. TASK-LEVER: results (computed after the pre-statement hash was logged at 18:31)

Scripts and outputs in `worldtrack/`:
- `tl_core.py`, `tl_gate.py` → `tl_gate.out`;
- `tl_run.py` → `tl_run.json`, `tl_run.log`;
- `tl_analyse.py` → `tl_analyse.out`;
- `tl_mono.out`;
- `tl_fine.py` → `tl_fine.out`.

### 0.8 Gate and checks (OBSERVED)

- **Reproduction gate passed:** the hexagon 0.5000 at T = 2, the 7-gon 0.5942 at T = 3, the 9-gon 0.4825 at T = 4. The even-n closed form matches the edge-normal evaluation to 2e−16 for n = 8, 10, 12.
- **Disk move cost.** The formula D(φ) = min over k ≤ T of k·sin²(φ/(2k)) never exceeds the grid DP by more than rounding on the 3600-point grid at any tested T. The minimum of (DP − formula) is −0.0, so the formula is the disk's optimum on the grid. A first gate run also used a 1440-point grid, with the same result.
- **P15 check:** 0 violations. Every polygon endpoint, at every T, costs at least as much as the disk endpoint at the same angle. This is OBSERVED, and consistent with REQUIREMENTS_FIRST §10.

### 0.9 The score

| class | cells (of 60) |
|---|---|
| proper W, single crossing W = [0, α*) | **60** |
| proper W, several crossings | 0 |
| W empty (the disk always) | 0 |
| W everything (a polygon always) | 0 |
| ambiguous (ties) | 0 |

- **HIT** (pre-stated ≥ 95% single crossing; observed 60 of 60).
- **Post-hoc robustness check:** on a 1001-point α grid (step 0.001) all 60 cells are still single-crossing. This check is not part of the score.
- **α* by cell** (bisected to 1e−12; full table in `tl_analyse.out`):
  - T = 2: 0.958, 0.997, 0.971, 0.777, 0.312, 0.036 for λ = 2, 5, 10, 30, 100, 1000;
  - T = 20: 0.875, 0.902, 0.783, 0.336, 0.112, 0.0118.
  - At large stakes, a small positional share is enough for the disk not to be beaten.
- **Triviality test: NOT trivial by the pre-stated test.** In 0 of 60 crossing cells were the argmins fixed across α. The disk's best endpoint moves with α in every cell. The best polygon changes along α: at T = 20, λ = 1000, from the 42-gon (2T + 2) to the 80-gon to the 121-gon.
  - Δ is also not monotone in 38 of 60 cells, with increases ≤ 3e−5, all inside the disk-side region (`tl_mono.out`). So the single crossing does not follow from monotonicity either.
- **Secondary prediction, an open miss.** α*·λ ∈ [1, 3] at λ ≥ 30, T ≥ 4 held in **0 of 24** cells.
  - Observed: α*·λ ≈ 9.7–11.8 for T ≥ 8 (approaching ≈ 12 as λ grows) and 14–25 at T = 4–6.
  - Why the heuristic failed: it kept the (2T+2)-gon fixed. As α rises, the best polygon moves to larger n whose perfectly distinguishable vertex sits closer to angle π: at T = 20 the 80-gon, then the odd 121-gon. That shrinks the positional miss by a factor of about 5–6, so the disk needs a larger positional share.
  - OBSERVED; the mechanism is HYP and not proved.

### 0.10 What Step 0 shows (labels)

| claim | label |
|---|---|
| In SR_B §1's class with all effects, with stake λ and horizon T in the tested ranges, the scored task's mix of geometric (positional) and operational (reach) loss switches the winning geometry at a single threshold α*(T, λ): polygons strictly cheaper below it, no polygon strictly cheaper above it | **OBSERVED** (60 of 60 cells, two α grids). Not proved for all (T, λ) |
| At α = 1 the disk is strictly cheapest in every tested cell | OBSERVED (consistent with P15, which proves only weak domination) |
| α* decreases with the stake λ, with α*·λ approaching ≈ 12 for T ≥ 8 | OBSERVED; mechanism HYP |
| The selecting number is a task input (α, the loss form) together with λ and T, all supplied by the task, not by the record | ELEMENTARY (by construction of the test) |

### 0.11 Hostile self-review of Step 0: **PASS-WITH-FIXES**

- **R1, high: circularity.** The test is built so that the loss decides. Finding that the loss decides is therefore the expected result, not a discovery about the theory's cost.
  - What is non-trivial is only the shape: one switch rather than an interleaving, in every cell, with moving argmins. It is ELEMENTARY in kind: a parametric comparison of two concave value functions that happens to cross once.
  - **Fix:** Step 0 is quoted only as "the loss class is the lever, with a clean single switch", never as the cost selecting a geometry.
- **R2, medium: the reach loss shape 1 − d is chosen.** A different operational shortfall (for example (1 − d)²) could move α* and in principle the crossing count. Not tested. It is listed in §0.6. **Fix:** name it as an open sensitivity.
- **R3, medium: the polygon menu is truncated at N(T).** Some best n (121 at T = 20) are well below N(20) = 130, but close to it. A larger menu can only lower polygon costs, which raises α*, and could in principle add crossings near α = 1. The 0.001-grid check does not test n > N(T). **Fix:** flag it. The rise of α* with N is HYP. The count of single crossings is OBSERVED for this menu only.
- **R4, low: the disk optimum** uses the path formula, checked against a 3600-point DP. Off-grid angles are covered by the formula, which is an achievable path, so the disk value is exact or an upper bound. An upper bound can only make polygons look better, so it does not create disk wins.
- **R5, low: the secondary prediction** was a heuristic and missed. It is reported as an open miss, not dropped.
- **Score on the stepback §13 scale** (judgment): HIT as predicted (p 0.75). Value ≈ 2.5 as planned; it confirms the lever with structure and corrects the P15 reading. Next: Step 1.

## Step 1. WORLD-TRACK: pre-statement (written before any Step 1 number was computed)

### 1.1 Question

A record tracks a drifting world under CORE's cost: J = Q̇ + w·E[ℓ] subject to P(ruin) ≤ ε (CORE.md:27), where w converts loss into the currency of heat (CORE.md:29). The heat Q̇ is the keep floor plus the read (learning-rate) floor.

- When **both the noise and the stake come from the tracked world's own statistics**, is there a unique interior design (n*, s*)?
- How does it scale with the world's drift σ_w, with the stake x set by the world's events, and with the medium's leak Γ?
- **Novelty bar (stated up front, as required).** n* ∝ √x is the known quantizer result (Gish–Pierce 1968; Gray–Neuhoff 1998). A HIT counts as **new** only if the keep and read floors produce a σ_w dependence or a prefactor beyond that. See §1.6 for both bars.

### 1.2 Model

- **World (every world input is a world statistic).**
  - The world angle is a wrapped Gaussian walk, θ_{t+1} = θ_t + σ_w·ξ_t with ξ_t ~ N(0, 1), per tick. **σ_w is the world's drift.**
  - Events arrive at rate r per tick from direction θ_t. The system responds at its record's angle φ_t and pays E_ev·(1 − cos(θ_t − φ_t)) in kT units. **The stake is x := r·E_ev/kT** (event rate × event cost). Only the product enters.
- **Record (the design; correction to REQUIREMENTS_FIRST §7 Route 1).**
  - The record is a **classical n-level register**: the n equal cells of the circle, R = the nearest of the angles 2πk/n. It is **not** a GPT n-gon.
  - Reason: acting on the record requires reading it, and the vertices of a GPT polygon with n ≥ 5 are not perfectly distinguishable in one shot. The pentagon carries ≈ 1.02 bits (REQUIREMENTS_FIRST P12). A GPT polygon record would add a readout loss, a design choice that is not the world's.
  - n = 1 is the **blind** design (CORE.md:91: heat 0, error v). The continuum register (the disk-like limit n → ∞) is in the menu only as a limit.
- **Read schedule (renewal checks, THEORY §B.2 A3 / CT9).** Every s ticks the record is overwritten with the cell of the current θ. Sensing is perfect (listed in §1.7). The agent acts at ages u = 0 … s − 1 (primary timing a = 0). Arm a = 1 uses ages 1 … s.
- **Cost per tick (kT units).**
  1. **Keep floor:** c_K·Γ·I_stored with I_stored = H(R) = ln n (uniform θ) and c_K = 2 (the G-keep floor Q̄ ≥ 2kTΓ·I; C12B_ORDER §9.1, §9.4; THEORY §B.2). Γ is the **medium's** leak rate per tick. Arm: c_K = 4.
  2. **Read floor:** H(R_{k+1} | R_k)/s, the information each read writes about the world.
     - This is the learning-rate floor Q̇ ≥ kT × the learning rate (CORE.md:19–21; Horowitz & Esposito 2014). It is also the measurement-plus-erasure minimum (Sagawa & Ueda 2009). Attained by assumption.
     - Computed exactly for ρ := σ_w√s/Δ ≤ 20 (Δ = 2π/n), using uniform-in-cell × Gaussian with closed-form integrals of Φ, folded mod n.
     - For ρ > 20: H = h_wN(σ_w√s) − ln Δ + ½·ln(1 + 1/(12ρ²)), where h_wN is the differential entropy of the wrapped normal (numerical; Gaussian closed form for τ < 0.2). The two must agree at ρ = 20 within 1e−3 nats, or the run stops.
  3. **Stake on loss:** x·L(n, s), with L = 1 − [sin(π/n)/(π/n)]·(1/s)·Σ_{u=a}^{s−1+a} e^{−σ_w²u/2}. This is exact: the quantisation error is uniform on the cell and independent of the drift, and E cos is a product. Blind: L = 1.
- **The disk's exclusion is cost-side (REVIEW_P15 fix 8).** As n → ∞ the keep cost c_KΓ ln n → ∞ for Γ > 0, and the read cost H → ∞ for any Γ, since each read writes ln n − O(1) nats. The exclusion comes from the keep and read costs. It is **not** loss-side: on the loss alone, the continuum register is never worse (P15's weak domination; the loss term falls monotonically in n).
- **Search.**
  - Coarse grid: n ∈ {1 … 3000} ∪ geometric (ratio 1.02) up to 3e6; s ∈ {1 … 3000} ∪ geometric (ratio 1.02) up to 1e8.
  - Refinement: integers (or ratio 1.0001 when > 2000 points) within a factor 1.05 of the coarse argmin.
  - **Edge rule:** n* or s* at an upper grid edge is a corner (a failed cell). n* = 1 (blind) and s* = 1 (a read every tick) are stated regimes, not corners.

### 1.3 Ranges (fixed now)

- σ_w ∈ {1e−3, 3e−3, 1e−2, 3e−2, 0.1, 0.3}.
- x ∈ {1, 3, 10, 30, 100, 300, 1e3, 3e3, 1e4, 3e4, 1e5, 1e6}.
- Γ ∈ {0, 1e−5, 1e−4, 1e−3, 1e−2, 1e−1}.
- 432 cells in the primary run (a = 0, c_K = 2). The arms (a = 1; c_K = 4) use the same grid.
- **Regime label at the optimum:** keep-dominated if the keep cost ≥ 2 × the read cost; read-dominated if the read cost ≥ 2 × the keep cost; mixed otherwise.

### 1.4 Paper predictions (HYP, derived before computing; heuristics, not proofs)

- **K regime (keep dominates):** n*² ≈ x·π²/(3c_KΓ), so n* ≈ π√(x/(3c_KΓ)). That gives e_x(n*) ≈ ½ and e_σ(n*) ≈ 0. This is the Gish–Pierce form with a holding price per nat.
- **R regime (read dominates, including Γ = 0).**
  - The high-resolution approximation has no self-consistent optimum: paper algebra gives ρ = √((ln(√(2πe)ρ) − ½)/3) < ρ for every ρ. So the optimum is at **low resolution, ρ* = O(0.1–0.6)**: the cell width matches the world's drift per read interval.
  - Then s* ∝ (xσ_w²)^{−1/2} and n* ∝ x^{1/4}·σ_w^{−1/2}, with logarithmic corrections. The read writes a roughly constant number of nats.
- **Hold interval:** s* ∝ σ_w^{−1} in both regimes, with log corrections. That gives e_σ(s*) ≈ −1.
- **Crossover:** at fixed (σ_w, Γ > 0), e_x(n*) falls from ≈ ½ toward ≈ ¼ as x grows (read cost ∝ √x·σ_w overtakes keep ∝ Γ ln n).
- **Blind below a threshold x_c(σ_w, Γ),** reported and compared with CT9's hold-or-fade criterion. Not scored.

### 1.5 HIT, MISS, OPEN (primary; these keep REQUIREMENTS_FIRST §7 Route 1's criteria, made operational)

- **H-a uniqueness:** in **every** non-blind cell, the coarse-grid landscape has no second local minimum (8-neighbour, in log n and log s) with J ≤ (1 + 1e−3)·J_min lying more than a factor 1.2 away in n or s.
- **H-b:** across adjacent-x pairs where both cells are keep-dominated and non-blind, the median local slope e_x(n*) is in [0.35, 0.65], and at least 75% of pairs are in that window.
- **H-c:** across adjacent-σ_w pairs with s* ≥ 3 in both cells and both non-blind, the median of |e_σ(s*)| is in [0.8, 1.2], and at least 75% of pairs are in that window.
- **H-d:** no n* or s* at an upper grid edge.
- **HIT** = H-a, H-b, H-c and H-d all pass.
- **MISS** = H-a fails in more than 2% of non-blind cells, or H-b or H-c fails.
- **OPEN** = fewer than 10 qualifying pairs for H-b or H-c, or H-d fails in more than 5% of cells, or the ρ = 20 continuity check fails.
- **Secondary (scored separately, not part of HIT):**
  - **S1:** R-regime ρ* ∈ [0.05, 0.8] in ≥ 75% of read-dominated cells with s* ≥ 3.
  - **S2:** R-regime median e_x(n*) ∈ [0.15, 0.35] and median e_σ(n*) ∈ [−0.65, −0.35].
  - **S3:** the crossover. In ≥ 75% of (σ_w, Γ > 0) rows that span both regimes, the local e_x(n*) is lower at the largest x than at the smallest non-blind x.
- **p(HIT) = 0.55; p(S1–S3 all) = 0.4** (stated now).

### 1.6 Triviality and novelty test (fixed now)

- **Bar A (the brief's bar: beyond Gish–Pierce / Gray–Neuhoff).** Pure GP has a fixed price per nat and no time, so it predicts n* independent of σ_w. The keep and read floors are **beyond GP** if either holds:
  - **(A1)** the median |e_σ(n*)| ≥ 0.2 over read-dominated adjacent-σ pairs; or
  - **(A2)** in keep-dominated cells, the median |ln(n*/n_GPK)| ≥ ln 1.25, with n_GPK = π√(x/(3c_KΓ)).
- **Bar B (strict: beyond all prior art listed here).** The list is GP; GN; Berger 1970 (rate-distortion of the Wiener process); Kipnis, Goldsmith & Eldar 2019; Sims 2003; and the theory's own CT9 and CT11 for the hold rule.
  - Kipnis–Goldsmith–Eldar show (abstract read this session) that for a sampled Wiener process the ratio of the sampled distortion-rate function to the unsampled one is a function only of the bits per sample. So **"the read writes a constant number of nats" (the R regime, S1) is KNOWN in substance**, although their cost is a bitrate with block coding, not a Landauer heat with a scalar register.
  - The keep-to-read crossover (S3) is a composition of two regimes. Its location x× follows from equating the two regimes' costs.
  - **Genuine at Bar B** only if the computation shows a feature neither regime formula gives: a non-monotone n*(x) at fixed σ_w and Γ; a hold-mode switch not given by CT9; or an x× more than a factor 3 off the composition estimate. Otherwise the call is **trivial in substance at Bar B (a composition, ELEMENTARY)**.
- **Pre-stated expectations:** beyond GP at Bar A, p 0.75; trivial at Bar B, p 0.85.

### 1.7 Inputs, sorted (as required: nothing chosen by us except what is listed)

| input | kind | set by |
|---|---|---|
| σ_w | **world** (drift per tick) | the tracked world, measured in Part 2 (N13, N56) |
| x = r·E_ev/kT | **world** (event rate × event cost) | the tracked world, measured |
| Γ | **medium** (carrier leak per tick) | the record's physical carrier, measured. **Not a world statistic**; listed because it is not the world's |
| c_K = 2 | the theory's floor constant (G-keep) | C12B_ORDER §9; arm c_K = 4. Floor attainment is OPEN (SELF_HORIZON H3) |
| loss shape 1 − cos | **chosen** (event-payoff geometry) | us; it stands in for the world's measured payoff curve |
| classical n-level register with equal cells and nearest-cell writes | **chosen** (the named class, CORE.md:13) | us |
| renewal reads at fixed s; perfect sensing; floors attained | **chosen** | us; sensing noise would be a world or sensor statistic, set to 0 here |
| timing a = 0 (act in the read tick) | **chosen**; arm a = 1 | us |
| tick as the time unit; grid ranges | scan choices, not model inputs | us |
| ruin cap ε | not binding in this class (no reserve); omitted | listed as omitted |

**Nothing about the record (n, s) is chosen. Two world numbers (σ_w, x) and one medium number (Γ) set it.**

## Step 1. WORLD-TRACK: results (computed after the Step 1 pre-statement hash was logged at 18:42)

Scripts and outputs are in `worldtrack/`:
- `wt_core.py`; `wt_check.py` → `wt_check.out`;
- `wt_run.py` → `wt_run.jsonl` (1296 records, 3 arms × 432 cells) and `wt_run.log` (about 12.5 min, run detached);
- `wt_analyse.py` → `wt_analyse.out`; `wt_post.py` → `wt_post.out`; `wt_berger.out`.

### 1.8 Checks before scoring (OBSERVED)

- **ρ = 20 continuity:** the exact and asymptotic read entropies differ by ≤ 1.0e−4 nats (n = 10 … 1e5). The pre-stated tolerance was 1e−3, so the check passes.
- **Table interpolation:** relative error ≤ 2e−7 against the exact value (ρ = 1e−6 … 19.9).
- **Monte Carlo** (n = 7, τ = 0.5, 4 million draws): H = 1.0483 against 1.0485 exact.
- **A floor to compare against.** At Γ = 0 the optimum costs J* = 1.75–1.99 × J_B, median 1.95. Here J_B = 2σ_w√x/π, obtained from Berger 1970's distortion-rate function for the Wiener process, D(R) = 2σ²/(π²R) with R in nats. That formula is **recalled, not re-read this session**, so this check is labelled HYP.
  - The ratio is never below 1, as expected: a causal scalar design with renewal reads cannot beat a block-coding bound.

### 1.9 The score (primary arm: a = 0, c_K = 2)

| criterion | pre-stated | observed | |
|---|---|---|---|
| H-a: a unique minimum in every non-blind cell | 0 non-unique cells | **0 of 432** (no cell is blind) | pass |
| H-b: keep-dominated adjacent-x pairs, e_x(n*) | median in [0.35, 0.65], ≥ 75% of pairs in the window | 56 pairs, median **0.454**, 98.2% in the window | pass |
| H-c: adjacent-σ_w pairs with s* ≥ 3, \|e_σ(s*)\| | median in [0.8, 1.2], ≥ 75% in the window | 180 pairs, median **0.968**, 85.0% in the window (10th percentile 0.78) | pass |
| H-d: no optimum at an upper grid edge | 0 edge cells | 0 | pass |

**Score: HIT** (p 0.55, stated before computing). Regimes at the optimum: K 67 cells, R 327, mixed 38. Arms:
- **a = 1:** the same call on every criterion. n* changes by 1 in 73 cells, and the summary statistics are identical to 3 decimals.
- **c_K = 4:** HIT. K 85 cells; H-b median 0.465 with 97.2% in the window; H-c median 0.957 with 82.2% in the window; 0 non-unique cells, 0 edge cells.

**Secondary predictions** (scored separately):
- **S1, pass.** R regime with s* ≥ 3 (157 cells): ρ* has median **0.604**, range 0.534–0.668, so 100% of cells fall in [0.05, 0.8]. The read writes **H* ≈ 1.10 nats (≈ 1.59 bits)** per read; range 1.02–1.18.
- **S2, pass.** R regime: median e_x(n*) = **0.254** (128 pairs); median e_σ(n*) = **−0.497** (104 pairs).
  - At Γ = 0 with s* ≥ 3: **n* ≈ 2.89 · x^{1/4} · σ_w^{−1/2}** (C ranges 2.74–3.02) and **s* ≈ 1.75/(σ_w√x)** (range 1.56–2.10). Both are OBSERVED fits.
- **S3, fail (an open miss).** The crossover held in 5 of 8 rows; 75% was required.
  - **Cause (OBSERVED, `wt_post.out` (3)):** in all 8 rows, the local e_x(n*) falls from ≈ 0.45 toward ≈ 0.26 while s* ≥ 3. In the 3 failing rows, s* then reaches **1**, and e_x climbs back to ≈ 0.5.
  - At s* = 1 the read rate is pinned at the tick. n then trades against a fixed price per nat, which is the Gish–Pierce form again.
  - A post-hoc reading (not a rescore): restricted to s* ≥ 3, the drop from ½ toward ¼ shows in 8 of 8 rows.

### 1.10 Triviality and novelty calls (pre-stated bars, §1.6)

**Bar A (beyond Gish–Pierce / Gray–Neuhoff): beyond GP. YES on (A1), NO on (A2).**
- **(A1) yes.** The median |e_σ(n*)| over R pairs is **0.497** (threshold 0.2). n* depends on the world's drift as σ_w^{−1/2}, which pure GP (a fixed price per nat, no time) cannot produce.
- **(A2) no.** In the K regime n* matches π√(x/(3c_KΓ)), GP with the keep floor as the price per nat: median |ln(n*/n_GPK)| = **0.073** (threshold 0.223), with a largest departure of 0.52 near the regime boundary. The keep floor adds no prefactor beyond GP.

**Bar B (beyond all prior art listed in §1.6): trivial in substance (a composition, ELEMENTARY).**
- **The R regime:** a constant number of nats per read, with resolution matched to the drift per read interval (ρ* ≈ 0.6). This is the read-floor version of Kipnis–Goldsmith–Eldar's finding that bits per sample is the controlling variable. KNOWN in substance; the constants are new only to this class.
- **The composition:** n*^{−2} = n_K^{−2} + n_R^{−2} reproduces every Γ > 0 cell, with median |ln error| **0.002**, 95th percentile 0.040 and maximum 0.082 (`wt_post.out` (5)).
  - This is the first-order condition with **additive marginal prices per nat** (keep c_KΓ, plus the read's marginal price), so it is ELEMENTARY.
  - The crossover x× (where keep equals read) is predicted by the composition to within a factor of **0.76–1.27** in 12 of 12 rows. The pre-stated threshold was a factor of 3.
- **Searched for and not found:** no non-monotone n*(x) in any row, and no s* rising with σ_w. No hold-mode switch beyond CT9: no blind cells occur, because x ≥ 1 everywhere in the grid.
- **One structural observation, also ELEMENTARY:** at Γ = 0 the read cost equals the stake loss at the optimum. The median ratio is 1.02 (range 0.90–1.43), the usual equal split at the minimum of A/s + B·s.

**Link to the theory's own closed form (mapping by me; HYP until checked against `theory/INFO_PHYSICS_ATTAINABILITY.md`).**
- CORE.md:90 gives the heat infimum kT·a(v − ε)/ε; CORE.md:91 gives the cost 2√(kT·a·v·w) − kT·a.
- In the random-walk limit (a → 0 with 2av = σ_w² fixed), with stake x/2 per unit squared error (since 1 − cos ≈ e²/2), the CORE cost is **σ_w√x** in kT units.
- Here J* = **1.244·σ_w√x** (median, Γ = 0, s* ≥ 3). So the **scaling of the cost is the theory's own** (√(stake × drift rate), the README.md:13 master-curve form). The discrete register pays about 24% above CORE's continuous linear memory.

### 1.11 Inputs that turned out to be chosen (listed as required)

| input | listed in §1.7 as | what the run showed |
|---|---|---|
| the tick, i.e. the fastest possible read | a scan choice | **It binds in 150 of 432 cells (s* = 1)**, and it is the cause of S3's open miss. It is a model input: the fastest look the sensor allows. It should be a **measured world or sensor statistic**, not ours. Reclassified as a chosen input. |
| noiseless, deterministic writes to an n-level register | a chosen class | It decides that the design is a **finite integer n**; see review W1. |
| timing a | chosen | It does not change any call (the a = 1 arm). |
| c_K | the theory's floor constant | c_K = 4 does not change any call. |
| loss 1 − cos | chosen | Not varied. |

σ_w and x (world) and Γ (medium) were the only inputs that set (n*, s*). **No record parameter was chosen.**

### 1.12 Labels (Step 1)

| claim | label |
|---|---|
| In the noiseless n-level register class with keep and read floors, the world's drift σ_w, the world's stake x and the medium's leak Γ select a unique interior (n*, s*) in all 432 × 3 cells | OBSERVED |
| R regime: n* ≈ 2.89·x^{1/4}·σ_w^{−1/2}, s* ≈ 1.75/(σ_w√x), ρ* ≈ 0.60, ≈ 1.10 nats per read, J* ≈ 1.244·σ_w√x | OBSERVED (fits on the grid) |
| K regime: n* ≈ π√(x/(3c_KΓ)) (GP with a keep price) | OBSERVED; ELEMENTARY on paper (first-order condition) |
| n*^{−2} = n_K^{−2} + n_R^{−2} | OBSERVED (median error 0.2%); ELEMENTARY (additive marginal prices) |
| The high-resolution approximation has no self-consistent optimum, so the optimum sits at ρ = O(1) | paper argument (§1.4), confirmed by OBSERVED ρ* ≈ 0.6 |
| The cost scaling σ_w√x is CORE.md:91's in the random-walk limit | HYP (my mapping) |
| Beyond GP (Bar A) | yes, through the σ_w dependence. That dependence is KNOWN in substance (Bar B) |
| The disk / continuum register is excluded on the cost side | PIM for noiseless writes (H → ∞); **not** for noisy continuous memories (review W1) |

### 1.13 Hostile self-review of Step 1: **PASS-WITH-FIXES**

- **W1, high: the integer n* depends on the class.** The register writes the exact cell, so a continuum costs infinite heat, which is the cost-side exclusion stated in §1.2. But CORE's own worked class (CORE.md:84–91) uses **noisy continuous linear memories at finite heat**, and in the random-walk limit that class reaches cost σ_w√x (my mapping, HYP). That is *below* this register's 1.244·σ_w√x.
  - So inside the theory's proved class, a continuous noisy memory beats every finite register here. **"A peak in n exists" holds only in the noiseless-register class.**
  - What survives a change of class is the **information budget**: ≈ 1.1 nats per read; a stored ln n* ≈ ln(2.89) + ¼ ln x − ½ ln σ_w; a read interval ∝ 1/(σ_w√x); a cost ∝ σ_w√x.
  - **Fix:** quote the result as "the world sets the information budget and the look rate", not "the world selects a polygon or an integer n". This bears directly on Chad's working premise: the peak is in **information**, and n is one realisation of it.
- **W2, medium: the tick binds in 35% of cells** (§1.11). H-b and H-c are unaffected (H-b restricted to s* ≥ 3: 53 pairs, median 0.459, 98.1% in the window; H-c already required s* ≥ 3). S3's open miss is a property of the tick. **Fix:** make the fastest look a measured world or sensor statistic in any follow-up.
- **W3, medium: floors are assumed attained.** The read uses kT·H(R′|R): Landauer erasure of the old record given the new one, which equals H(R′|R) by stationarity, plus Sagawa–Ueda for measurement. The keep uses 2kTΓ·ln n. Real costs are higher. Attainability is OPEN (SELF_HORIZON H3); a c_K = 4 arm does not change the calls.
- **W4, medium: the Berger formula and the CORE mapping are mine,** recalled or derived, not re-read this session. They are used only as checks (J*/J_B ≥ 1) and as a link (the σ_w√x scaling). Labelled HYP.
- **W5, low: circularity.** σ_w, x and Γ are numbers we set in-model. "Nothing chosen" means only that nothing *about the record* is chosen (REQUIREMENTS_FIRST §6). The novelty bars were pre-stated and applied as written. Bar A passes and Bar B does not; neither is upgraded.
- **W6, low: uniqueness** was tested on the coarse grid with tolerance 1e−3. No cell was close to failing it: there were 0 far near-minima in any cell.
- **W7, low:** no blind cells, because the grid's smallest x is 1. CT9's blind or hold edge is therefore not exercised. Not scored, as pre-stated.

## 2. Next step (proposed; nothing run)

1. **INFO-BUDGET (top; ready for a pre-statement).**
   - **Model:** repeat Step 1 inside CORE's own worked class: a noisy continuous linear memory with the keep floor 2kTΓ·I and the learning-rate floor, with the fastest look (the tick) set as a measured sensor statistic.
   - **Question:** does the world (σ_w, x) with the medium (Γ) select the same **information budget** (stored I*, nats per look, look rate) that the register found?
   - **HIT:** I* within ±0.3 nats of ln n* − (the register's quantisation overhead), and the look rate ∝ σ_w√x.
   - **Value:** this tests whether "the peak is in information" (W1) is class-independent, which is the version of Chad's peak premise that today's evidence supports.
   - **Estimate:** p ≈ 0.6, about 3 h.
2. **KELLY-TRACK** (REQUIREMENTS_FIRST Route 2), on Step 1's world. It replaces x by the world's payoff structure, so the stake also comes from the world's dynamics.
3. **TASK-LEVER sensitivity** (Step 0 R2, R3): vary the reach-loss shape and extend the polygon menu, to see whether α* rises with N and the single switch survives.

## Step 2. INFO-BUDGET: pre-statement (appended 26 Nov 2026, about 19:15 ET, before any Step 2 number was computed)

### 2.1 Sources checked before writing (as asked)

- **The CORE.md:91 mapping, checked against the source text.**
  - Source: `theory/INFO_PHYSICS_ATTAINABILITY.md` (main `8b553c6`).
    - :14 gives the signal as dX = −aX dt + √(2av) dW, so the noise variance rate is **q = 2av**.
    - :22 and :25: ε is the **decision error**, the MMSE E[Var(X | M)].
    - :30 gives the Kalman rate R(ε) = a(v − ε)/ε.
    - :35: the infimum of the heat is kT·R(ε), approached at finite heat by linear springs (PROVED in-model, AT-attain :155).
    - :44–47: J* = min over ε of [kT·a(v − ε)/ε + w·ε], which equals 2√(kT·a·v·w) − kT·a above w = kT·a/v.
  - Mapping. With q = σ_w² per tick held fixed and a → 0, J* → √(2·kT·q·w). The loss 1 − cos e ≈ e²/2 puts a stake of w = x/2 per unit squared error, so J* → **kT·σ_w√x**.
  - **WORLD_TRACK §1.10's mapping is confirmed against the source.** It moves from HYP to ELEMENTARY: a limit of a PROVED in-model formula.
  - Caveat: the limit a → 0 leaves CORE's equilibrium OU class. Step 2 therefore stays at finite a (§2.2).
- **The Berger formula, now verified from a source.**
  - Kipnis, Goldsmith & Eldar 2019 (doi 10.1109/TIT.2018.2878446; arXiv 1608.04679 v-latest, eq. (4) and §III-A, read this session) state Berger's distortion-rate function of the Wiener process as **D_W(R) = 2σ²/(π² ln 2 · R) ≈ 0.292σ²/R**.
    - R is in bits per unit time, and K_W(t, s) = σ²·min{t, s}, so σ² is the variance rate.
    - The distortion is time-averaged, with a non-causal decoder that may use any functional of the path.
  - In nats, D = 2σ²/(π²·R_nats). This is the formula WORLD_TRACK §1.8 used, so its J_B = 2σ_w√x/π and the ratio J*/J_B ≈ 1.95 stand. The label moves from HYP to **KNOWN (verified)**.
  - Berger 1970 itself (doi 10.1109/TIT.1970.1054423, Crossref OK) was not read. The formula is taken as KGE state it.

### 2.2 Model: inside CORE's class (CORE.md:84–91)

- **World: an equilibrium OU signal** (CORE's class), with a = 3σ_w²/(2π²) and v = π²/3.
  - This matches Step 1's world in its two statistics: the drift rate q = 2av = σ_w² per tick, and the variance of a uniform angle, π²/3.
  - With these values ½ ln(v/P) equals Step 1's ln n when P = Δ²/12. That makes the stored information directly comparable.
  - a and v are set by σ_w plus the circle's variance, not by us (listed in §2.6).
- **Memory: a linear Gaussian memory holding the MMSE estimate,** with error variance P(u) at age u since the last look.
  - At each look the memory takes a Gaussian measurement whose precision is the **design choice**: it sets P₊, the error variance just after the look.
  - Between looks P(u) = e^{−2au}·P₊ + v(1 − e^{−2au}). The value just before the next look is P₋ = P(s).
  - The finite-heat noisy continuous memory of CORE's class is the limit s → 0 (continuous observation).
- **Looks:** every s ≥ s_min, with s real. **s_min is the sensor's fastest look, a measured figure**, not a choice. It is scanned as an input: s_min ∈ {1, 0.1, 0.01} ticks.
- **Cost per tick, in kT units:**
  1. **Look heat** = the information gained per look, divided by s: ½ ln(P₋/P₊)/s.
     - This is the learning-rate floor (CORE.md:19–21) for discrete looks; Sagawa–Ueda 2009 for the measurement cost.
     - In the limit s → 0 it becomes the Kalman rate R(ε) of the source (:30), checked in §2.4 (C0).
  2. **Keep floor** = c_K·Γ·½ ln(v/P₊), the stored information at writing (C12B G-keep; c_K = 2). Arm: the cycle-averaged ½ ln(v/P(u)).
  3. **Per-look price** c·(1/s): CT9's read price (THEORY.md:311), a world or sensor price. Primary c = 0; arms c ∈ {0.1, 1, 10}.
  4. **Stake:** (x/2)·(1/s)∫₀ˢ P(u) du. The decision error is the MMSE, and x/2 per squared error matches Step 1.
- **Search:**
  - log P₊ on 900 points from 1e−14 to v;
  - log s on 900 points from s_min to 1e8;
  - then a bounded Nelder–Mead polish from the grid argmin.
- **"Pinned"** means s* ≤ 1.02·s_min.

### 2.3 Ranges (fixed now)

- The same 432 world/medium cells as Step 1: σ_w ∈ {1e−3, 3e−3, 0.01, 0.03, 0.1, 0.3}, x ∈ {1, 3, …, 1e6}, Γ ∈ {0, 1e−5, …, 0.1}.
- Configurations: (s_min, c) ∈ {1, 0.1, 0.01} × {0, 0.1, 1, 10}, giving 12 × 432 = 5184 cells.
- The **primary is s_min = 1, c = 0**, Step 1's tick with no per-look price.
- Keep arm (cycle-averaged I): primary configuration only.

### 2.4 Predictions (HYP; paper algebra before computing)

- **Random-walk algebra.** With r := q·s/P₊ and Γ = 0, optimizing s at fixed r gives J = √(x·q·f(r)) with f(r) = ln(1 + r)·(1/r + 1/2) = 1 + r²/12 + O(r³). The minimum is at r → 0, i.e. at s → 0.
- **So without a per-look price the memory wants to look as often as possible.** The look rate is set by **the sensor's s_min, not by the world**: the cost is pinned at s_min in every cell. Step 1's look rate ∝ σ_w√x is then a property of the register, not of the information budget.
- **With a per-look price c > 0:**
  - s* ≈ 2√(c/(x·q)), the CT11 form, so the look rate ∝ σ_w√x/√c;
  - the nats per look are ≈ ½ ln(1 + 2√c), set by **the price alone** and the same in every world.
  - **HYP:** the register's constant ≈ 1.1 nats per look (Step 1 S1) is what a per-look price of about 16 kT would give. The register's discreteness acts like a per-look price.
- **Stored information I* = ½ ln(v/P₊*):**
  - read-dominated: P₊* ≈ √(q/x), so dI*/d ln x ≈ ¼ and dI*/d ln σ_w ≈ −½ (Step 1's exponents for ln n*);
  - keep-dominated: P₊* ≈ c_K·Γ/x, so dI*/d ln x ≈ ½, with no σ_w.
- **Cost:** J* → 2√(a·v·x/2) − a ≈ σ_w√x as s_min·σ_w√x → 0, against Step 1's register at 1.244·σ_w√x. When s_min·σ_w√x is not small, J*/(σ_w√x) is a function of that product alone (a scaling collapse).
- **C0, the mapping check (a numerical gate).** At Γ = 0, c = 0 and s_min = 0.01, in cells with s_min·σ_w√x ≤ 1e−3, J* agrees with the source's 2√(a·v·w) − a (w = x/2) within 1%. If it fails, Step 2 stops and reports.

### 2.5 Score (fixed now)

Four components of the "same information budget" (Step 1, R regime). Each is scored on the primary configuration unless stated:

- **B1, nats per look:** the median over R-regime cells is within 1.10 ± 0.30 nats.
- **B2, look rate ∝ σ_w√x:**
  - fewer than 25% of non-blind cells pinned;
  - and over non-pinned adjacent-σ_w pairs, the median |e_σ(s*)| is in [0.8, 1.2];
  - and over non-pinned adjacent-x pairs, the median e_x(s*) is in [−0.65, −0.35].
- **B3, stored information:**
  - R regime: median dI*/d ln x in [0.2, 0.3] and median dI*/d ln σ_w in [−0.6, −0.4];
  - K regime: median dI*/d ln x in [0.4, 0.6].
- **B4, J ∝ σ_w√x:**
  - at Γ = 0 and s_min = 0.01, in cells with s_min·σ_w√x ≤ 0.1, J*/(σ_w√x) lies within ±10% of a single constant;
  - and that constant is ≤ 1.244, Step 1's register.

**Overall outcomes:**
- **HIT ("the same budget comes out")**: B1, B2, B3 and B4 all pass.
- **PARTIAL**: B3 and B4 pass, and B1 or B2 fails.
- **MISS**: B3 or B4 fails.
- **OPEN**: C0 fails, or more than 5% of cells end at the upper grid edge.

Stated now: **p(HIT) = 0.10, p(PARTIAL) = 0.65, p(MISS) = 0.20, p(OPEN) = 0.05.** The prediction is PARTIAL: B1 and B2 fail because the look rate is pinned at s_min.

**Secondary, S-eq (scored separately).** A single price c_eff exists such that the Gaussian memory with s_min = 1 and price c_eff reproduces Step 1's register s* within 25% in at least 75% of Step 1's Γ = 0, s* ≥ 3 cells. c_eff is fitted on those cells, on a grid of 61 values from 0.01 to 1000. p = 0.5.

### 2.6 Triviality test, and inputs

- **Triviality (fixed now).** Inside CORE's class this is a closed-form exercise. Its continuous limit *is* CORE.md:91, a PROVED in-model frontier. Whatever comes out is **ELEMENTARY, not a new result about the theory's cost**.
- **Genuine content, if any,** is the **class comparison**:
  - which parts of Step 1's budget hold in both classes (predicted: the stored-information exponents and the cost scaling);
  - which parts the register's discreteness creates (predicted: the nats per look and the world-set look rate);
  - whether that discreteness equals a per-look price (S-eq).
- **Inputs:**

| input | kind |
|---|---|
| σ_w, x | world |
| a = 3σ_w²/(2π²), v = π²/3 | world, fixed by σ_w and the circle's variance. **Matching Step 1 is our choice;** an OU world measures its own a and v |
| Γ | medium |
| s_min | **sensor, measured.** Scanned, not chosen |
| c | world or sensor price (CT9). Scanned; the primary is 0 |
| c_K = 2 | the theory's floor constant |
| keep charged on I at writing | **chosen**; arm: cycle-averaged |
| Gaussian linear memory with Gaussian looks | CORE's class (CORE.md:84) |
| floors attained | assumed. Proved for continuous observation (AT-attain); assumed for discrete looks |
| loss (x/2)·MSE | chosen, to match Step 1 (1 − cos ≈ e²/2) |

### 2.7 Timing note

§2's heading says "about 19:15 ET". The pre-statement was actually appended and hashed at **19:05 ET** (WORKLOG). Computing started after that.

## Step 2. INFO-BUDGET: results

Scripts and outputs, all in `worldtrack/`:
- `ib_run.py` → `ib_run.jsonl` (5616 records: 12 configurations × 432 cells, plus the keep arm) and `ib_run.log`. Run detached; about 45 s.
- `ib_analyse.py` → `ib_analyse.out`.
- `ib_post.py` → `ib_post.out`.

### 2.8 Gate and checks (OBSERVED)

- **C0, the mapping check: passed.** In the 25 cells with Γ = 0, c = 0, s_min = 0.01 and s_min·σ_w√x ≤ 1e−3, J* matches the source frontier 2√(a·v·w) − a (w = x/2) to a largest relative difference of **4.2e−8**. So discrete looks priced at the information they gain reproduce INFO_PHYSICS_ATTAINABILITY :44–47 in the continuous limit.
- **No cell falls below CORE's proved infimum.** At Γ = 0 and c = 0, across all s_min, J*/(source frontier) ranges from **1.000000 to 74.3**, so 0 cells are below it. That is consistent with the heat floor (AT-attain, :35).
- No cell ended at a grid edge; no cell was blind.

### 2.9 Score (primary configuration: s_min = 1, c = 0, as pre-stated)

| component | pre-stated test | primary result |
|---|---|---|
| B1, nats per look | median within 1.10 ± 0.30 | median **0.451** (10th–90th percentile 0.009–3.40). It follows the product u = s_min·σ_w√x (log–log correlation 0.984). **FAIL** |
| B2, look rate ∝ σ_w√x | fewer than 25% of cells pinned, plus the slopes | **432 of 432 pinned at s_min.** **FAIL** |
| B3, stored-information exponents | R regime: dI/d ln x in [0.2, 0.3] and dI/d ln σ_w in [−0.6, −0.4]; K regime: dI/d ln x in [0.4, 0.6] | R: **0.337** and **−0.288**; K: 0.409. **FAIL** |
| B4, J ∝ σ_w√x | within ±10% of one constant, at most 1.244 | 63 cells: median **0.9999**, range 0.954–1.0004. **PASS** |

**Score: MISS** by the pre-stated rule (B3 failed). The pre-stated p(MISS) was 0.20.

**Why B3 failed (OBSERVED).**
- The pinned look interval is s_min = 1. When u = s_min·σ_w√x is not small, each look must carry many nats and the stored information shifts.
- That is the same tick effect that caused Step 1's S3 open miss.
- **Post hoc, not a rescore:** restricting the primary configuration to u ≤ 0.1 gives R-regime slopes of **0.255** and **−0.492**, the predicted values.
- **In the other 11 configurations B3 passes** (s_min = 0.1 or 0.01, or c > 0). R-regime dI/d ln x is 0.250–0.261 and dI/d ln σ_w is −0.475 to −0.500. K-regime dI/d ln x is 0.401–0.465.

**The other configurations, for B1 and B2:**
- **With c = 0 the look interval sits at the sensor's limit:** 100%, 100% and 99.5% of cells are pinned at s_min = 1, 0.1 and 0.01. The nats per look scale with u: about 0.005 at s_min = 0.01. **Without a per-look price, the look rate is set by the sensor, not the world.** This was predicted.
- **With a per-look price c > 0, the look rate is set by the world and the price:** median |e_σ(s*)| = 0.989–0.997 and median e_x(s*) = −0.499 to −0.500 over non-pinned pairs. B2 passes in every configuration with c > 0 and fewer than 25% pinned.
- **Nats per look depend on c alone:** median **0.521 / 1.061 / 1.931** nats at c = 0.1 / 1 / 10. They are nearly the same in every world, 10th–90th percentile within ±0.03 at s_min = 0.01.
  - B1 passes only at c = 1 (1.06 nats).
- **My §2.4 formula for this was wrong by about a factor of 2.** I predicted ½ ln(1 + 2√c) = 0.245 / 0.549 / 0.996; the observed values are close to ln(1 + 2√c) = 0.490 / 1.099 / 1.992. This is an open miss in my paper algebra. Not traced.
- **Keep-cost arm** (cycle-averaged I): the same calls as the primary (B3 R slopes 0.337 / −0.287).

**Secondary, S-eq: pass.**
- With a single **c_eff = 0.383 kT per look**, the Gaussian memory reproduces Step 1's register look interval s* within 25% in **41 of 41** cells (median |ln ratio| 0.017; ratios 0.89–1.14).
- At the same c_eff, the register's ln n* exceeds the Gaussian's stored I* by **0.066 nats** (median; range 0.028–0.114).
- My §2.4 guess of c ≈ 16 was wrong; it came from the factor-2 error above.

### 2.10 Trivial or genuine

- **Trivial in substance, as pre-stated.** Inside CORE's class the computation is ELEMENTARY, and its continuous limit is CORE.md:91 (C0 to 4e−8). Nothing here is a new result about the theory's cost.
- **Genuine content (the class comparison):**
  1. **Holds in both classes** (OBSERVED in the register and in the Gaussian memory wherever the tick does not bind):
     - stored information grows with x at ¼ per e-fold when reads dominate and about ½ when keep dominates, and falls with σ_w at −½;
     - **cost ∝ σ_w√x**, with constant 1.000 for CORE's class and 1.244 for the register.
     - So **the stored-information budget and the cost are set by the world (σ_w, x) and the medium (Γ) in both classes.**
  2. **Not class-independent:** the look rate and the nats per look.
     - In CORE's class with no per-look price, the memory looks as fast as the sensor allows. The nats per look then follow s_min·σ_w√x.
     - A look rate ∝ σ_w√x and a world-independent number of nats per look appear only with a per-look price c, the CT9/CT11 read price, which is a world or sensor price.
  3. **The register behaves like CORE's memory plus a per-look price of ≈ 0.38 kT** (S-eq). That is OBSERVED as a one-parameter fit; the mechanism is HYP.
     - Hostile caveat: both classes already have s* ∝ 1/(σ_w√x), so one constant matching them is close to automatic. Only the small spread (0.89–1.14) is evidence.

### 2.11 Inputs, as found

| input | status after the run |
|---|---|
| σ_w, x | world. They set the stored information and the cost |
| Γ | medium. It sets the K regime |
| s_min, the sensor's fastest look | **measured, scanned. With c = 0 it decides the look rate and the nats per look in essentially every cell.** It must be measured on a real system, as REQUIREMENTS_FIRST's minimal set asks |
| c, the per-look price | world or sensor price, scanned. With c > 0 it sets the nats per look, and the look rate ∝ σ_w√x/√c |
| a and v matched to the circle | **chosen** (to compare with Step 1) |
| keep charged at writing | chosen; the cycle-averaged arm gives the same calls |
| loss (x/2)·MSE | chosen (to match Step 1) |
| floors attained for discrete looks | assumed. Consistent with CORE's floor (0 cells below it) |

### 2.12 Labels (Step 2)

| claim | label |
|---|---|
| WORLD_TRACK §1.10's mapping J* → kT·σ_w√x | **ELEMENTARY** (a limit of INFO_PHYSICS_ATTAINABILITY :44–47, checked against the source; C0 numeric 4e−8). Upgraded from HYP |
| Berger's D_W(R) = 2σ²/(π² ln 2·R) | **KNOWN, verified** (Kipnis–Goldsmith–Eldar 2019, eq. (4), read this session). Upgraded from HYP |
| In CORE's class with no per-look price, the optimum looks at the sensor's fastest rate | OBSERVED (99.5–100% pinned); paper algebra f(r) = 1 + r²/12, HYP |
| With a per-look price c, the nats per look depend on c only, ≈ ln(1 + 2√c) | OBSERVED; the closed form is a fit, HYP |
| The stored-information exponents and J ∝ σ_w√x are the same in both classes when the tick does not bind | OBSERVED (11 of 12 configurations; the primary configuration only after the post-hoc restriction) |
| The register ≈ CORE's memory plus about 0.38 kT per look | OBSERVED fit; close to automatic given a shared scaling |
| INFO-BUDGET score | **MISS** (the pre-stated primary; B3 failed because the tick binds) |

### 2.13 Hostile self-review of Step 2: **PASS-WITH-FIXES**

- **V1, high: the score is a MISS, and it stays one.** It comes from a pre-stated primary at s_min = 1, where the sensor limit binds. Every other configuration passes B3, and the post-hoc restriction passes it too. Those facts explain the MISS; they do not overturn it.
  - The finding that matters: **the information budget is not fully set by the world.** Its per-look part is set by the sensor (s_min) or by a per-look price (c). Only the stored part and the cost are world-set.
- **V2, high: B1 and B2 were not a fair test of "same budget".** In CORE's class those quantities are not world statistics at all without c. The pre-statement predicted that they would fail, so their failure confirms the prediction rather than adding evidence.
- **V3, medium: my §2.4 algebra was wrong by about a factor of 2** on the nats per look, and the c ≈ 16 guess was wrong. Both are reported, not hidden. The scored criteria did not depend on them.
- **V4, medium: uniqueness of the optimum was not tested in Step 2.** Step 2 used a grid argmin plus a polish and had no local-minimum test, unlike Step 1. **Fix** before quoting "a unique stored-information optimum" in CORE's class: add the local-minimum test.
- **V5, medium: matching a and v to the circle is our choice,** made for comparability. A measured OU world supplies its own a and v.
- **V6, low:** discrete-look heat priced at the information gained is assumed attainable. The 0-cells-below-the-floor check is consistent with that, but it does not prove attainability for discrete looks.
- **V7, low: circularity.** The world numbers are set in-model, as in Step 1. Nothing about the memory (P₊, s) was chosen.

### 2.14 Next step (proposed; nothing run)

1. **STORED-PEAK.**
   - Add the uniqueness test to Step 2. Then state, for CORE's class, the claim the evidence now supports: *the world (σ_w, x) and the medium (Γ) select a unique stored-information budget I* and a cost ∝ σ_w√x; the look rate needs a measured sensor limit or a per-look price.*
   - About 1 h; p(unique) ≈ 0.85.
2. **SENSOR-MEASURED.** Find, in the repository's qualified-system candidates (CLAIM_MAP N13), whether s_min and c are measurable for any one system. Reading only, no data invented.
3. **KELLY-TRACK** (REQUIREMENTS_FIRST Route 2).

## Step 3. STORED-PEAK: pre-statement (appended 26 Nov 2026, 19:1x ET, before any Step 3 number was computed; the exact time is in the WORKLOG)

### 3.1 Question

Is the stored-information optimum **unique** in both worked classes, at every sensor setting and per-look price? If it is, what exactly may be claimed?

### 3.2 Classes and configurations (fixed now)

- **G: CORE's class.** Step 2's model unchanged: an OU world with a = 3σ_w²/(2π²) and v = π²/3; a Gaussian memory; looks at s ≥ s_min; heat per look = the information gained; keep c_K·Γ·½ ln(v/P₊); price c per look; stake (x/2)·MSE.
  - Stored information: I = ½ ln(v/P₊).
  - Configurations: s_min ∈ {1, 0.1, 0.01} × c ∈ {0, 0.1, 1, 10}, giving 12 × 432 = 5184 cells. Also Step 2's cycle-averaged keep arm (s_min = 1, c = 0), 432 cells.
- **Reg: Step 1's register,** with a per-look price c added (cost c/s per tick) and sensor settings s_min ∈ {1, 0.1, 0.01}.
  - A sub-tick sensor is handled by **rescaling time to the sensor's look**: σ′ = σ_w√s_min, x′ = x·s_min, Γ′ = Γ·s_min per look-tick, with c unchanged per look. The register's integer s counts look-ticks.
  - This rescaling is exact for this model: every cost is per tick, and the loss uses whole ages.
  - Stored information: I = ln n.
  - Configurations: 12 × 432 = 5184 cells, primary timing a = 0, c_K = 2.
- **Grids:**
  - G: 600 × 600 in (log P₊, log s), as in Step 2.
  - Reg: Step 1's coarse grid in (n, s), integers up to 3000, then ratio 1.02 up to 3e6 and 1e8.

### 3.3 Tests (fixed now)

- **U1, global uniqueness:** no second local minimum of the 2-D grid (8-neighbour) with J ≤ (1 + 1e−3)·J_min lying more than a factor 1.2 away in the design (P₊ or n) or in s. This is Step 1's H-a.
- **U2, the profile in stored information:** J_prof(I) = min over s of J(I, s) on the grid has **exactly one** local minimum, counting only dips deeper than 1e−9·J_min.
- **Edge check:** no optimum at an upper grid edge, and no design at the lower P₊ edge.
- **HIT:** in every configuration of both classes, U1 holds in 100% of cells and U2 in at least 99%.
- **MISS:** in some configuration U1 fails in more than 1% of cells, or U2 holds in fewer than 95%.
- **OPEN:** anything in between, or more than 1% of cells at a grid edge.
- **p(HIT) = 0.8** (stated now).
- **Paper part, to be written with the results:**
  - **Claim:** in the continuous-look limit of class G, J(ε) = kT·a(v − ε)/ε + (c_K·Γ/2)·ln(v/ε) + w·ε (with the keep floor charged on the decision error ε) is strictly convex on (0, v).
  - **Sketch:** the second derivative is 2kT·a·v/ε³ + c_K·Γ/(2ε²) > 0.
  - **Consequence:** the minimiser is unique, either interior or the blind end ε = v. This would be PIM (ELEMENTARY), checked against the source formula at :44.

### 3.4 Claim to be stated if HIT (template fixed now; constants from data)

> *In two worked classes (CORE's OU class with Gaussian looks, and a noiseless n-level register), with costs at their floors (look heat = information gained; keep floor 2kTΓ·I), the world's drift σ_w and stake x and the medium's leak Γ select a unique stored-information optimum I\*. Where reads dominate and the sensor limit does not bind, I\* ≈ ¼ ln x − ½ ln σ_w + C; where keeping dominates, I\* ≈ ½ ln(x/Γ) + C′. The cost scales as σ_w√x. The look rate is not set by the world: it is the sensor's fastest look unless each look has a price. [Label.] Part 1 (in-model) only; no real system is claimed.*

- **The label will be OBSERVED (in-model, numerical) for discrete looks,** plus PIM for the continuous limit if the paper part holds.
- If the result is MISS, the claim is not stated and the failing cells are reported.

### 3.5 Inputs (unchanged from Steps 1–2)

- World: σ_w, x.
- Medium: Γ.
- Sensor: s_min (measured, scanned).
- Price: c (scanned).
- Chosen: the class choices listed in §1.11 and §2.11.
