
## 6. SH-noise pre-statement (written 26 Nov 2026, about 13:15 ET, before any SH-noise number is computed; §§0–5 stand as written)

*The SHA-256 of this block, the bytes from the "## 6." heading line through the end of §6.9, is logged in WORKLOG.md before any computing. Nothing in §6 may be edited afterwards. Results go in §7.*

### 6.1 Why a leak, and which one (primary and robustness arm)

- **Premise taken from the theory.** The keep floor (C12B_ORDER §8.2, §9.1, §9.4: Q̄ ≥ 2kTΓ·I, separate-leak carriers) says a physical record relaxes toward its equilibrium unless it is paid for. The SR_B §1 class has no such leak, which is §5's break point. SH-noise adds one, with one physical rate.
- **Primary: angular diffusion plus snapping ("vertex confusion").**
  - Each tick, the stored pure state at angle φ is kicked to φ + θ, with θ ~ N(0, σ²) wrapped on the circle.
  - The record is then held at a pure state of its design, as SR_B §1's pure-jump rule requires. A polygon snaps to the nearest vertex. The disk keeps φ + θ, since every angle is pure.
  - A polygon record is **confused** in a tick iff θ (wrapped) lands outside its own arc (−π/n, π/n). Per-tick confusion probability: p_n(σ) = P(|θ|_wrapped > π/n).
  - Why primary: the keep floor is derived for continuous carriers (an OU memory, Fokker–Planck, log-Sobolev). Its leak consists of small continuous kicks. On the circle of pure states the analogue is rotational diffusion. Its ensemble mean decays toward the centre (the maximally mixed state) by the factor e^{−σ²/2} per tick, so it is a leak toward the centre with rate Γ = σ²/2 per tick.
- **Robustness arm R1: depolarizing replacement.** Each tick, with probability r the record is replaced by a uniformly random pure state of its design. Matched to the same ensemble leak rate: r := 1 − e^{−σ²/2}. Confusion probability: r(1 − 1/n) for an n-gon, r for the disk. Same σ grid.
- **What noise does not touch.** The transport cost J(D, T) stays exactly SR_B §1's, computed noise-free. The noise sets only the lifetime, the horizon at which the design is scored. The heat of holding the record against the leak (the keep floor itself) is **not** added to J. That is a stated limit: SH-noise tests the self-consistency rule, not the full cost.

### 6.2 Lifetime τ(D, σ): no level parameter in the primary

- **Primary (level-free): the mean time to the first change of the held record.** τ(n, σ) := 1/p_n(σ) (geometric first-confusion time). The disk's held state changes in every tick with probability 1 (θ ≠ 0 almost surely, and there is no snapping), so τ(disk, σ) = 1.
- **Horizon used:** T(D) := ⌊τ(D, σ)⌋, integer ticks. Robustness: ⌈τ⌉.
- **Level arm L (for the disk, and as a check).** "Any change" is level-free for polygons but strict for the disk. So a second lifetime is reported: τ_δ(D, σ) := the mean exit time of the held record from {states at operational distance < δ from the start}. Here δ ∈ {0.1, 0.2, 0.3, 0.5} is dimensionless (operational distance ∈ [0, 1]).
  - Polygons: an exact Markov chain on the vertices, with snapping kernel q_j = P(θ ∈ arc of v_j); mean exit time by a linear solve.
  - Disk: the discrete-tick Gaussian walk exiting the arc {|φ| < φ_δ}, sin(φ_δ/2) = δ, computed by a Nyström discretization. For δ < d_min(n), τ_δ(n) = 1/p_n, the primary.
  - **Insensitivity criterion, fixed now:** the qualitative items of §6.4 (exists, unique, no 2-cycle, disk status, monotone growth) must be the same at every δ in the set. Prefactors and exponents are reported, not scored.

### 6.3 Fixed-point rule

- **Menus.** (E) even n ∈ [4, N_E] plus the disk; (O) odd n ∈ [3, N_O] plus the disk; (F) all n plus the disk.
- **Target rules.** M3h (any vertex at d = 1) and the mixed rule (antipode for even n, the farthest vertices for odd n). For odd n both rules give the same targets. So there are five configurations: E-M3h, E-mixed, O, F-M3h, F-mixed.
- **Definitions.**
  - A(T) := argmin over the menu of J(·, T), with ties counted within relative 10⁻¹².
  - **n is self-consistent** iff T(n) ≥ 2 and n ∈ A(T(n)).
  - T(n) = 1 is **vacuous**: every design costs exactly 1 at T = 1, so nothing is selected. It is reported, not counted.
  - **The disk is self-consistent** iff T(disk) ≥ 2 and disk ∈ A(T(disk)).
- **2-cycle:** a ≠ b, both with T ≥ 2, b ∈ A(T(a)) and a ∈ A(T(b)), neither self-consistent.
- **Also reported:** the map Φ(n) := min A(T(n)); the continuous crossing n_c where Φ(n) − n changes sign; and the discrete slope |ΔΦ/Δn| across it (stability: < 1 attracting, > 1 repelling).
- **Range.** J(n, T) is computed exactly for T ≤ 400 for every n ≤ 4001 (even and odd), plus sparse grids (even to 64,000, odd to 16,001).
  - A polygon with T(n) > 400 is excluded as **proved not self-consistent** if T(n) > π²/(4·d_min(n)), by SR-b1(f) (the disk is strictly cheaper there). Otherwise it is **OPEN** at that σ.
  - A σ whose candidate needs T > 400, or whose argmin sits at the edge of the computed n-range, is **OPEN** at that σ.
- **The disk is decided by SH1 (§2.3, PIM), not by the computation.** Wherever T(disk) ≥ 2, some polygon is strictly cheaper, so the disk is not self-consistent. In the primary, T(disk) = 1, which is vacuous. This HIT item is pre-decided and is not a test.

### 6.4 HIT / MISS / OPEN (scored on the primary; σ grid fixed now)

- **σ grid:** 0.4, 0.3, 0.2, 0.15, 0.1, 0.07, 0.05, 0.035, 0.025, 0.018, 0.012, 0.008, 0.005, 0.0035.
- **HIT:** in all five configurations and at every σ in the grid, (i) exactly one self-consistent polygon n*(σ), (ii) no 2-cycle, (iii) the disk is not self-consistent, and (iv) n*(σ) is nondecreasing as σ falls and grows over the grid. A fitted log-log exponent n* ∝ σ^{−β} is reported.
- **MISS:** in any configuration, at any σ in the grid: a 2-cycle, no self-consistent polygon, two or more, n* bounded (no growth over the grid), or the disk self-consistent at some σ > 0.
- **OPEN:** neither of the above, including any σ that is OPEN by the range rule. Also OPEN if the level arm L changes a qualitative item.
- R1 and the ⌈τ⌉ rounding are reported as robustness and are not scored. If either changes a qualitative item, that is said plainly.

### 6.5 Expected outcome, from paper, before computing

- **Continuous crossing.** If the OBSERVED argmin rule n*(T) = 2T + 2 holds (E-M3h), the crossing solves n ≈ 2/p_n(σ) + 2, with p_n ≈ erfc(x) and x = π/(√2·nσ).
  - Asymptotically x² ≈ ln(1/σ) + O(ln ln), so **n_c ≈ (π/σ)/√(2 ln(1/σ))**. Hand check: σ = 0.01 gives n_c ≈ 125–130 (x ≈ 1.7).
- **Stability.** dτ/dn = −2x²τ/n, so |Φ′| ≈ 2x² ≈ 6 at σ = 0.01, which is > 1. **The crossing is expected to be repelling.**
- **Integer existence.** On the integers, Φ(n) − n changes by about 2x² per step near the crossing, so it can step over 0. **Expected: at some grid σ there is no exact self-consistent polygon**, with an oscillating orbit or a 2-cycle instead.
  - Uniqueness, when a fixed point exists, is ELEMENTARY: Φ is nonincreasing, by τ nonincreasing in n and A(T) nondecreasing in T. Both are to be checked numerically.
- **Prior for the scored outcome:** P(MISS) ≈ 0.6 (mostly "no exact fixed point" or a 2-cycle at some σ), P(HIT) ≈ 0.25, P(OPEN) ≈ 0.15.
- **R1 expectation.** τ ≈ 1/r is nearly design-independent, so n* ≈ 2/r + 2 ≈ 4/σ². A pure horizon relabelling (β = 2), with |Φ′| ≈ 0, so it is stable.
- **L expectation.** For δ ≫ d_min, τ_δ ≈ φ_δ²/σ², nearly design-independent, so n* ≈ 2φ_δ²/σ² (β = 2, prefactor ∝ φ_δ²).

### 6.6 Triviality checks, stated now

- **Trivial ("resolution ≈ noise"):** the primary fitted β ∈ [0.8, 1.3] **and** n*·σ·√(2 ln(1/σ)) constant within a factor 1.5 over the grid.
  - This is the known fact that a constellation or quantizer resolves about range/σ points under noise σ (Shannon 1949; optimal quantizer size under noise). The cost J would be doing no work beyond the argmin rule 2T + 2.
- **Trivial ("horizon relabelling"):** β = 2 with n* ≈ 2τ + 2 and τ design-independent (R1, L).
- **Non-trivial:** β outside [0.8, 1.3] in the primary, or a prefactor traced to J's geometry (for example π²/4, or the d_min structure) rather than to the confusion threshold, or a qualitative difference between the even and odd menus or between the two target rules.

### 6.7 The interruptible version (not computed)

- Here the horizon is known in advance (contract reading). In the interruptible reading the record's end time is random (geometric, mean τ) and the path cannot use it.
- Expected effect: horizon averaging favours finer designs. In the Bayes contract-mixture of SR_B §8.4, n* ≈ 0.06–0.1/(1−q)² (OBSERVED), which would give β ≈ 2 in p_n, not ≈ 1.
- An interruptible path must also be good at every stop time, which pushes toward the competitive (U-like) criterion. That is exactly the input under study.
- So the interruptible version **could change β and the stability**. It is named as the main untested alternative, not run here.

### 6.8 Computation plan (tools)

- An exact forward DP with the SR_B §8.4 step cap, in C. Distances come from the closed form for even n (SR_B §8.6) and from the breakpoint method (review_srb4 `rv_core.dist_row`) for odd n.
- Cross-checks: `sr_b4/curves_even.npy` (M3h), and `rv_core.J_circ` (full circular DP, no cap) on a sample.
- p_n(σ) in mpmath (wrapped normal, 50 digits).
- Argmin gaps below 10⁻⁹ relative are rechecked in mpmath.
- Scripts and outputs in `selfhorizon/`.

### 6.9 Labels planned

- Fixed points, cycles, n*(σ), β: OBSERVED.
- Disk status: PIM (SH1).
- The exclusion of polygons with T > π²/(4d_min): PIM (SR-b1(f)).
- Uniqueness given monotonicity: ELEMENTARY.
- Any scaling law: OBSERVED fit, plus the §6.5 heuristic.
