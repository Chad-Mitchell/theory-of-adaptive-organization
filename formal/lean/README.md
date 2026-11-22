# Lean 4 formalization of the GTAO core (OPEN_WORK T19)

This directory is a Lean 4 + Mathlib project.  It machine-checks a
finite-menu fragment of the core in `THEORY.md` (canonical) and `CORE.md`,
and (since 21 November 2026, branch `lean-core-2026-11-21`) four further
core results: the layer-lifetime optimum `T* = √(6k/(wσ²))` as the
minimizer of the repository's zero-discount average cost, the
local-vs-shared crossing (D5), the selection-axioms stationary excess
`E_π[J] − J* = d/(2β)` (equipartition, SA1b), and the lower-hull increment
test equals argmin for an arbitrary `ε` (KEYSTONE_NOTE §4).
Formalization cannot establish the hypothesis in CORE §3, which is a claim
about the real world.

- Toolchain: `lean-toolchain` pins `leanprover/lean4:v4.37.0-rc1`.
- Mathlib: `lakefile.toml` and `lake-manifest.json` pin `v4.37.0-rc1`.
  This is a release candidate, not a stable tag.  It is pinned because
  this formalization uses Lean 4.37's module system (`module`,
  `public import`, `@[expose] public section`), which is not in the
  previous stable (`v4.36.0`); Mathlib's published `lean-toolchain` at
  the time of the formalization resolved to `v4.37.0-rc1`, and the
  Mathlib olean cache at `cache.mathlib.org` serves that pin.  A later
  bump to the next stable Lean/Mathlib tag is open work.
- Build: from the repo root, `tools/check_lean.sh` (or, in this
  directory, `lake exe cache get` then `lake build`).
- There is no `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`, or
  `implemented_by` in the project sources (`GTAO.lean`, `GTAO/*.lean`).
  The checker searches only those files, not `.lake/` or
  `lake-packages/`.  Anything not listed as proved below is
  **not formalized**, not “proved with a hole.”
- Axiom audit: `scripts/AxiomAudit.lean` (run by `tools/check_lean.sh`
  after the build) checks that every declaration in a `GTAO.*` module
  depends only on `propext`, `Classical.choice` and `Quot.sound`.  A
  `sorry` anywhere would show up as `sorryAx` and fail the check.  Last
  run (21 November 2026): 312 declarations, OK.

## How to build

Lean 4 is installed with [elan](https://github.com/leanprover/elan).
Then, from this directory:

```bash
lake exe cache get   # cached Mathlib oleans; do not compile Mathlib from source
lake build
```

`tools/check_lean.sh` does the same and also rejects `sorry`, `admit`,
`axiom`, `native_decide`, `unsafe`, and `implemented_by` in project
sources (not in `.lake/` or `lake-packages/`), then runs the axiom audit
(`lake env lean scripts/AxiomAudit.lean`).  Builds run at `nice -n 19`.
The pytest wrapper `tools/test_lean.py` runs that script whenever `lake`
is on `PATH` or in `~/.elan/bin`, and skips cleanly if Lean is not
installed.

## Mapping: Lean declarations to THEORY CT numbers

Hypotheses are part of the claim.  A finite nonempty design set, and a
stake-independent menu (ruin slack or absent), are standing hypotheses
wherever `FiniteDesignMenu` is used.

| Lean name | THEORY / source | What is assumed | What is proved |
|---|---|---|---|
| `FiniteDesignMenu.J` | CORE §1, THEORY §3 | Finite menu; `J = S + w E`; ruin slack or absent, so the menu does not depend on `w` | Definition of the split cost |
| `FiniteDesignMenu.exists_minimizer` | CT20 (i), finite case | `𝒟` nonempty and finite | A minimizer exists at every stake |
| `FiniteDesignMenu.Jstar`, `Jstar_concave`, `IsOptimal.Jstar_eq`, `Jstar_le_affine` | CT33 envelope | Same finite menu | `J*` is the min of affine functions of `w`, hence concave on `ℝ`, with supporting slope `E` at an optimum |
| `FiniteDesignMenu.optimality_inequalities`, `error_diff_sign` | CT33 | Same; two optima at `w₁`, `w₂` | The two revealed-preference inequalities, and `(w₂−w₁)(E₂−E₁) ≤ 0` |
| `FiniteDesignMenu.error_nonincreasing` | CT33 | `w₁ < w₂` (strict: at a tie, two optima may differ in error) | `E*` is nonincreasing |
| `FiniteDesignMenu.spend_nondecreasing` | CT33 | `0 ≤ w₁ < w₂`; ruin slack or absent | `S*` is nondecreasing |
| `FiniteDesignMenu.spend_nondecreasing_in_R` | CT33 | `h > 0` and the same stake hypotheses | `S*/h` is nondecreasing in `w` (equivalently in `R = w/h` at fixed `h`) |
| `FiniteDesignMenu.layer_count_bound` | CT20 (i) bound | `h > 0`, `h K ≤ S`, `0 ≤ w E` (so `J ≥ h K`) | Any design matching or beating a reference `d₁` has `K ≤ J(d₁;w)/h` |
| `FiniteDesignMenu.layer_count_nondecreasing` | CT20 (ii), sensing fixed | Spend is exactly `h K` with `h > 0`; `0 ≤ w₁ < w₂`; menu independent of `w` | The layer count itself is nondecreasing.  This fails once reads are also chosen (THEORY's counterexample); total spend still obeys CT33 |
| `effortJ_decreasing_differences`, `effort_nondecreasing` | CT10 | Error is nonincreasing along a frequency coordinate; check price `c > 0`; `w₁ < w₂` | Decreasing differences, and the discrete Topkis conclusion: optimal effort does not fall as stakes rise |
| `jointOptimal_iff`, `exact_nesting_value` | CT34 (i) | Parent and team design sets finite and nonempty; `J(x,y)=F(x)+G(y;θ(x))` | Partial minimization is exact, and the minimizers agree |
| `parentOptimal_of_constant_theta` | CT34 (ii) | `θ` does not depend on the parent's design | The team's optimized cost is a constant (an upkeep); the parent's argmin is the argmin of `F` alone |
| `strongConvex_lipschitz_gap`, `weak_coupling_pointwise`, `weak_coupling_gap`, `weak_coupling_parent_regret` | CT34 (iii) | `μ > 0`, `ε ≥ 0`; `G` satisfies the strong-convexity inequality in a distance `dist`; `Φ` is `L`-Lipschitz in `y` in the one-sided sense used in THEORY | Freezing the team at a `G`-minimizer overshoots by at most `(ε L)²/(2μ)`, and the parent's regret from optimizing the frozen cost is at most that bound.  The coupling sign `ε ≥ 0` is stated (needed to keep the Lipschitz bound's direction) |
| `D_comp_IB_convex`, `L_convex` | CT4, convex lower bound | `D` convex and nonincreasing on the image of `IB`; `IB` concave on `s` | `D ∘ IB` is convex, and `L(I)=D(IB(I))+κ I` is convex (the `κ I` term is affine at every sign of `κ`).  That `L` is a lower bound on cost is not formalized |
| `zero_isMinOn_iff`, `not_minOn_zero_iff_neg_right_slope`, `pos_min_of_neg_right_slope`, `exists_neg_right_slope_of_not_min` | helpers (right slopes of an arbitrary `L`) | None beyond `L : ℝ → ℝ` and the stated point in `[0, ∞)` | `0` is a minimizer iff every right slope from `0` is nonnegative; hence `0` fails to minimize iff some right slope is negative, and any minimizer is then strictly positive.  These are not the CT4 first-bit criterion |
| `L_right_slope`, `first_bit_sign`, `first_bit_positive_minimizer` | CT4, first-bit sign | `L(I)=D(IB(I))+κ I`; stated with right slopes from `0` on `[0, ∞)`, not a two-sided derivative | Every right slope of `L` from `0` equals the corresponding right slope of `D ∘ IB` plus `κ`.  Therefore `0` fails to minimize `L` iff `∃ x > 0, (D(IB x)−D(IB 0))/x + κ < 0`.  This is THEORY's `κ < -(D∘IB)'(0⁺)` in slope form: if the right derivative exists, it is the infimum of those slopes (for convex `D∘IB`).  A minimizer, if one exists, is then strictly positive.  Existence of a minimizer on `[0, ∞)` is not proved |
| `not_certified_below_Bmin` | CT22, certified `B_min` | `0 < max θ`, `0 ≤ B < B_min` | No design is Lundberg-certified (THEORY's wording: the bound is sufficient, not that every design ruins).  THEORY also takes `0 < ε < 1`, which makes `B_min` positive (`Bmin_pos`) so that the interval is inhabited; the comparison itself is algebraic in `log(1/ε)` |
| `certified_at_Bslack` | CT22, `B_slack` | `θ(d_E) > 0`, `B ≥ B_slack` | The expected-cost optimum is certified |
| `expected_cost_opt_at_or_above_Bslack` | CT22, slack case | `d_E` minimizes `J` over all designs; `θ(d_E) > 0`; `B ≥ B_slack` | `d_E` is Lundberg-certified and is therefore optimal among certified designs; the cap is slack.  Composes `certified_at_Bslack` with that restriction.  No KKT is used |
| `Bmin_le_Bslack` | CT22 | `0 < ε < 1`, `0 < θ(d_E)` (hence `0 < max θ`) | `B_min ≤ B_slack` |
| `minimizer_on_lower_hull` | KEYSTONE_NOTE §4, first sentence | `R ≥ 0`; `φ(K)=K+R(1+ε_K)` on `{0,…,n}` | Every minimizer of `φ` lies on the lower convex hull of `{(K, ε_K)}` |
| `n60_from_zero_leftmost` | KEYSTONE_NOTE §4, adjacent test | `R ≥ 0` and discrete convexity of `ε` (first differences nondecreasing) | Walking from `0` and taking every paying adjacent step returns a leftmost minimizer of `φ` |
| `n60_as_written_zero_hole` | N60 as written; the `K*=0` hole | Same, and the first step does not pay | No later step pays, and the true leftmost minimizer is `0`.  The cardinality formula `1 + #{k ≥ 2 : step k−1 pays}` is not defined in Lean, so the theorem does not conclude that N60 as written equals `1` (those two ingredients are what would make it equal `1`) |
| `LayerLifetime.cost`, `Tstar`, `cost_ge`, `Tstar_isMin`, `Tstar_unique`, `cost_Tstar` | CORE §3; `theory/LAYER_LIFETIME_2026-11-21.md` §2 (CL19 (a)) | The zero-discount average cost of a lumpy layer is `C(T) = k/T + c·wσ²·T` with `c·wσ² > 0`, `k > 0`; the stochastic derivation of that expression (mean exit time `b²/σ²`, time-average square gap `b²/6`; Dixit 1991, exact at zero discount per Chalkley 1997) is **assumed**, not formalized | On `T > 0`, `C` has the unique minimizer `T* = √(k/(c wσ²))`, with minimum `2√(c k wσ²)` (AM–GM identity `C(T) − 2√(k a) = (√a T − √k)²/T`) |
| `LayerLifetime.layer_lifetime` | CORE §3, `T* = √(6k/(wσ²))` | Barrier coefficient `c = 1/6`; `k, w, σ² > 0` | `T* = √(6k/(wσ²))` is the unique minimizer of `k/T + wσ²T/6` on `T > 0`, with minimum `2√(kwσ²/6)` |
| `LayerLifetime.fixed_period_lifetime`, `barrier_eq_sqrt3_fixed` | LAYER_LIFETIME §2, fixed-period cousin | `c = 1/2`; `k, w, σ² > 0` | `T*_fix = √(2k/(wσ²))` minimizes `k/T + wσ²T/2`, minimum `√(2kwσ²)`; the barrier lifetime is `√3` times the fixed-period one |
| `LayerLifetime.Tstar_scale_k`, `lifetime_ratio` | CORE §3 (`√k` scaling); LAYER_LIFETIME §3a (Model LS spacing) | `r ≥ 0`; for the ratio, `c, w > 0`, `k_j > 0`, `σ_i², σ_j² > 0`, equal stakes | `T*(r k) = √r · T*(k)`; `T*_i/T*_j = √((k_i/k_j)(σ_j²/σ_i²))` |
| `LayerLifetime.barrier_band_identities` | `theory/SELECTION_AXIOMS.md` SA2 proof | `k, w, σ² > 0`; `b*² = √(6kσ²/w)` | `w b*²/6 = kσ²/b*² = √(kwσ²/6)`, and `b*²/σ² = T*` |
| `LocalShared.localCost`, `sharedCost`, `sigma2Star`, `const_lt_iff` | CORE §1/§4; LAYER_LIFETIME §5 (D5) | Costs taken from the repository as given: local `N e √(k_L w σ²)`, shared `e √(k_S N w σ²) + N w σ² ℓ` (delay floor on the shared observation only), `e > 0` the excess coefficient (`√2` fixed period, `2/√6` barrier); `N, w > 0`, `k_S, k_L ≥ 0`.  The stochastic derivation of these costs is not formalized | `e√(k_S N w) < N e √(k_L w)` iff `k_S < N k_L` |
| `LocalShared.no_switch_without_delay`, `shared_never_wins` | D5 | As above; `σ² > 0`; `ℓ = 0`, resp. `ℓ ≥ 0` and `k_S ≥ N k_L` | At `ℓ = 0`, shared wins iff `k_S < N k_L`, at every drift (no switch); if `k_S ≥ N k_L`, shared never wins |
| `LocalShared.crossing` | D5, the crossing `σ²*` | As above; `ℓ > 0`; `k_S < N k_L`; `σ² > 0` | Shared is strictly cheaper iff `σ² < σ²* = ((√(k_L w) − √(k_S w/N)) e/(wℓ))²` |
| `LocalShared.switch_iff` | D5 / CORE §1 "needs delay on the shared channel only, and a shared lump cheaper than `N` local ones" | As above; `ℓ ≥ 0` | A drift switch (shared strictly cheaper at some `σ² > 0`, not cheaper at another) exists **iff** `ℓ > 0` and `k_S < N k_L` |
| `LocalShared.equal_delay_no_switch`, `barrier_crossing_eq_fixed_div_three` | LAYER_LIFETIME §5 | As above | An equal delay floor on both sides cancels (comparison is the `ℓ = 0` one at every drift); the barrier crossing is the fixed-period crossing divided by exactly 3 |
| `Equipartition.HomogCost`, `Z_scale`, `Nm_scale`, `Nm_one`, `gibbs_mean_homog` | SA1b, general form | `E` a finite-dimensional real normed space of dimension `d ≥ 1`, `μ` any additive Haar measure (Lebesgue); `q` continuous, `q ≥ 0`, `q(x) > 0` for `x ≠ 0`, `q(r x) = r^p q(x)` for `r > 0`, `p > 0`; `β > 0` | `e^{−βq}` and `q e^{−βq}` are integrable, `Z(β) = β^{−d/p} Z(1)`, and `∫ q e^{−βq} / ∫ e^{−βq} = d/(pβ)` (proof: scaling plus Fubini on `β ∈ [1,2]`) |
| `Equipartition.gibbs_excess` | SA1b, `E[J] − J* = d/(pβ)` | As above, with `J(x) = J* + q(x − x*)` | For `π ∝ e^{−βJ}`, `E_π[J] − J* = d/(pβ)` exactly |
| `Equipartition.homogCost_quadratic`, `gibbs_excess_quadratic` | SA1b / Corollary SA1c, `d/(2β)`; CORE §3, THEORY §4 | `J(x) = J* + ½(x − x*)ᵀH(x − x*)` on `ℝ^d` (`Fin d → ℝ`, Lebesgue), `d ≥ 1`, `H` positive definite (Mathlib `Matrix.PosDef`, so symmetric), `β > 0`; π is the Gibbs/Boltzmann law `∝ e^{−βJ}` on all of `ℝ^d` | `E_π[J] − J* = d/(2β)` exactly.  SA1 (that the stationary law of the origination–fixation chain is this Boltzmann weight, Sella–Hirsh), SA1b's "treat the measure as supported on the quadratic well", and the per-model `β` (Moran `α(N−1)`, Wright–Fisher `α(2N−1)`) are **not** formalized; they are the inputs that make this identity the selection result |
| `HullWalk.HullVertices`, `IsLowerHull`, `Pays`, `hull_walk_stop_exists`, `hull_walk_leftmost_argmin` | KEYSTONE_NOTE §4, the hull-vertex walk (edges may skip integers) | `R ≥ 0`; `ε : ℕ → ℝ` arbitrary (no convexity); vertex data `v 0 = 0 < v 1 < ⋯ < v m = n` with every point on or above its hull edge and nondecreasing edge slopes | The walk that jumps from `v i` to `v(i+1)` iff `R(ε(v i) − ε(v(i+1))) > v(i+1) − v i` stops, and the stopping vertex is a minimizer of `φ(K) = K + R(1+ε_K)` on `{0,…,n}`, strictly below `φ` at every `K` to its left (leftmost minimizer) |
| `HullWalk.greedy`, `greedy_isLowerHull`, `hull_increment_test_eq_argmin` | KEYSTONE_NOTE §4 Proposition, unconditional | `R ≥ 0`; `ε` arbitrary | Every `ε` has lower-hull vertex data (greedy minimum-slope chords), so the hull increment test returns the leftmost argmin of `φ` for **every** `ε`, with no convexity hypothesis |

## What is not formalized

None of the following is claimed as proved in Lean.

- The hypothesis in CORE §3 (a claim about the real world).
- Convexity of `ε_K` in Model S, still unproved on paper (CORE §4, KEYSTONE_NOTE).  The increment *formula* in N60 is formalized only as a consequence of discrete convexity, which is an assumption here.
- The stochastic derivations behind the layer-lifetime and local-vs-shared cost expressions (Brownian exit times, the time-average square gap `b²/6`, the delay floor `N w σ² ℓ`, and Chalkley's exactness at zero discount).  The optimization and comparison on those expressions are formalized; the expressions are inputs.
- The OU (mean-reverting) version of D5 and the `T*`-versus-correlation-time failure regime (NUMERICAL in the repository).
- SA1 (the Sella–Hirsh stationary weight of the origination–fixation chain), the per-process `β` (Moran, Wright–Fisher), SA1b's well-supported approximation, SA2's lag term as a selection statement, and the fractional form `≈ d/(2σN_e)`.  Only the exact equipartition identity for a Gibbs law on a homogeneous (in particular positive definite quadratic) cost is formalized.
- The Model-S hull is formalized for any measured `ε`; what stays open is a formula for `ε_K` from the world's time scales and its convexity (above).
- The N60-as-written cardinality `1 + #{k ≥ 2 : step k−1 pays}` (and the equality of that cardinality to `1` in the zero-hole case).  The ingredients (no later step pays; leftmost minimizer is `0`) are proved.
- CT4 as a lower bound on cost: only the convexity of `L(I)=D(IB(I))+κ I` is proved, not that `L` bounds a cost functional.  Monotonicity of the information-bottleneck curve `IB` is not used and not formalized.
- CT4's Gaussian AR(1) closed form `I* = ½ log₂(2 ln 2 · a² · Var / κ)`.
- The right derivative `(D∘IB)'(0⁺)` as a real (or extended-real) number; the first-bit sign condition is proved in right-slope form.
- CT20 (i) in a continuous parameter set (Weierstrass on a compact rate set).  Only the finite-menu existence result and the `K ≤ J(d₁)/h` bound are formalized.
- CT20 (ii)'s second clause: for one layer whose error grows with the age of its reading, `f*` is nondecreasing in `w/c`.  The sensing-fixed layer-count clause is formalized.
- CT34 (ii)'s "generically only if" converse (only the "if `θ` is independent of `x`" direction is proved).
- CT34 (iv): a shared driver is not weak coupling (the numerical illustration).
- CT21 (L1–L3): Kalman–Bucy, Wiener spectral factorization, interlacing, degree.
- CT22's in-between binding region, the multiplier `μ_s = −m'/θ'`, and the quasiconvexity / uniqueness hypotheses that justify it.
- CT1–CT3 (rate–distortion, ergodic theorem, lead-time cap).
- CT5, CT6, CT7, CT8, CT9 (Blackwell/garbling, hold-or-fade, and the neighbouring short CTs).
- CT11–CT19, CT23, CT24, CT25, CT26–CT32, CT35–CT43, and the Master Theorem in the class `𝓜_LG`.
- Any information-theoretic construction of `D` or `IB`; they enter CT4 as functions with the stated convexity and monotonicity.

## Layout

```
formal/lean/
  lakefile.toml         # package `gtao`, library `GTAO`, Mathlib pin
  lean-toolchain
  lake-manifest.json
  GTAO.lean             # root import
  GTAO/Cost.lean        # J, argmin, J*
  GTAO/CT33.lean
  GTAO/CT20.lean
  GTAO/CT10.lean
  GTAO/CT34.lean
  GTAO/CT4.lean
  GTAO/CT22.lean
  GTAO/Hull.lean
  GTAO/LayerLifetime.lean   # T* = √(6k/(wσ²)) and the fixed-period cousin
  GTAO/LocalShared.lean     # D5 crossing; switch iff ℓ > 0 and k_S < N k_L
  GTAO/Equipartition.lean   # E_π[J] − J* = d/(pβ); d/(2β) for PD quadratics
  GTAO/HullWalk.lean        # hull increment test = leftmost argmin, any ε
  scripts/AxiomAudit.lean   # every GTAO declaration uses only standard axioms
```

Build artifacts under `.lake/` are gitignored.
