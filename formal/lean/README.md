# Lean 4 formalization of the GTAO core (T19)

This directory is a Lean 4 + Mathlib project.  It machine-checks a
finite-menu fragment of the core in `THEORY.md` (canonical) and `CORE.md`,
and (since 21 November 2026, PR #147) four further core results: the
layer-lifetime optimum `T* = √(6k/(wσ²))` as the minimizer of the
repository's zero-discount average cost, the local-vs-shared crossing
(D5), the selection-axioms stationary excess `E_π[J] − J* = d/(2β)`
(equipartition, SA1b), and the lower-hull increment test equals argmin
for an arbitrary `ε` (KEYSTONE_NOTE §4).  This branch adds the
from-0 layer-count exactness lemma (L1 / N64), the finite-cell band-model
convexity theorems (M, Z, X, B) with the `W ≥ 0` necessity check, a
finite-state CA1 / CA1a statement, the Lyapunov-trace identity for
the drift-selection excess DS1, including `d/(2β)(1+D/D_m)`, and
(this branch, batch 2) the DS2 lag and cost bounds, uniqueness of
the CA1 stationary law, CA1b/CA1c (U2), and CA7 (U11) on the
load-bearing chain.
Formalization cannot establish the hypothesis at the top of CORE.md, which is a claim
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
  `sorry` anywhere would show up as `sorryAx` and fail the check.  The
  current total is `audit_count` in `AUDIT.json`, its one source.

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

"CORE §" numbers below refer to earlier versions of the one-pager, kept in git history ([`2026-11-21_CORE_before_onepage.md`](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/blob/1eed183f3888e8e3eead5956bbf1e8cb4233510a/history/2026-11-21_CORE_before_onepage.md), [`2026-11-21_CORE_before_shannon.md`](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/blob/1eed183f3888e8e3eead5956bbf1e8cb4233510a/history/2026-11-21_CORE_before_shannon.md), [`2026-11-22_CORE_before_front.md`](https://github.com/Chad-Mitchell/theory-of-adaptive-organization/blob/1eed183f3888e8e3eead5956bbf1e8cb4233510a/history/2026-11-22_CORE_before_front.md)). The current `CORE.md` was rewritten on 22 November 2026 and has different section numbers.

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
| `Equipartition.homogCost_quadratic`, `gibbs_excess_quadratic` | SA1b / Corollary SA1c, `d/(2β)`; CORE §8, THEORY §4 | `J(x) = J* + ½(x − x*)ᵀH(x − x*)` on `ℝ^d` (`Fin d → ℝ`, Lebesgue), `d ≥ 1`, `H` positive definite (Mathlib `Matrix.PosDef`, so symmetric), `β > 0`; π is the Gibbs/Boltzmann law `∝ e^{−βJ}` on all of `ℝ^d` | `E_π[J] − J* = d/(2β)` exactly.  SA1 (that the stationary law of the origination–fixation chain is this Boltzmann weight, Sella–Hirsh), SA1b's "treat the measure as supported on the quadratic well", and the per-model `β` (Moran `α(N−1)`, Wright–Fisher `α(2N−1)`) are **not** formalized; they are the inputs that make this identity the selection result |
| `HullWalk.HullVertices`, `IsLowerHull`, `Pays`, `hull_walk_stop_exists`, `hull_walk_leftmost_argmin` | KEYSTONE_NOTE §4, the hull-vertex walk (edges may skip integers) | `R ≥ 0`; `ε : ℕ → ℝ` arbitrary (no convexity); vertex data `v 0 = 0 < v 1 < ⋯ < v m = n` with every point on or above its hull edge and nondecreasing edge slopes | The walk that jumps from `v i` to `v(i+1)` iff `R(ε(v i) − ε(v(i+1))) > v(i+1) − v i` stops, and the stopping vertex is a minimizer of `φ(K) = K + R(1+ε_K)` on `{0,…,n}`, strictly below `φ` at every `K` to its left (leftmost minimizer) |
| `HullWalk.greedy`, `greedy_isLowerHull`, `hull_increment_test_eq_argmin` | KEYSTONE_NOTE §4 Proposition, unconditional | `R ≥ 0`; `ε` arbitrary | Every `ε` has lower-hull vertex data (greedy minimum-slope chords), so the hull increment test returns the leftmost argmin of `φ` for **every** `ε`, with no convexity hypothesis |
| `N60Exact.count`, `count_isLeftmostArgmin` | `theory/LAYER_CONVEXITY.md` L1 / CLAIM_MAP N64, "if" | Finite domain `{0,…,n}`; `R ≥ 0`; `ε` discrete-convex (decrements non-increasing) | The from-0 count `K*_0(R) = #{K≥1 : R d_K > 1}` is the leftmost minimizer of `K + R(1+ε_K)` |
| `N60Exact.not_min_of_rise`, `exists_threshold`, `threshold_pos`, `exists_R_interval_count_not_argmin`, `exists_R_count_not_argmin`, `exists_R_count_not_argmin_of_pos`, `count_exact_iff_convex` | L1, converse and the iff | Pairwise distinct decrements; the threshold decrement `d_{(m)}` positive (equivalently at least `m` positive decrements) suffices; all-positive is the special case used by the iff | If some `d_m < d_{m+1}`, there is an open interval of `R > 0` on which `K*_0(R) = m` (with `m` one past the rise) and the count is not a minimizer (`exists_R_interval_count_not_argmin`); the single-`R` form is a projection of that statement. Hence with positive distinct decrements, (count = leftmost argmin for all `R > 0`) ⇔ discrete convexity |
| `N60Exact.exists_nonconvex_count_exact` | L1, counterexample to a bare iff | `d = (−2, −1)`, i.e. `ε = (−3, −1, 0)` on `{0,1,2}` | The sequence is not discrete-convex, yet `K*_0(R) = 0` is the unique minimizer for every `R ≥ 0` (`φ(0) < φ(j)` for `j = 1, 2`) |
| `BandCounterexample.clusterE_values`, `bandE0`, `bandE1_lower`, `bandE1_attained`, `bandE2_attained`, `not_convex` | LAYER_CONVEXITY minimal counterexample | `W = (0,1,0)`, weights `(2,1,1)`; bands of a non-monotone profile with a terminal zero band | Optimal band costs `E = (1, 2/3, 0)` (exact ℚ check by kernel `decide`, and over all real cutoffs and levels), so `E_0 − E_1 < E_1 − E_2`: not convex |
| `BandMonge.merge_gain`, `quadrangle_core`, `terminal_core` | LAYER_CONVEXITY §3, the algebra behind Lemmas M and Z | Positive block masses; non-increasing block means; for Z also `m_B ≥ 0` | Merge-gain identity `f(X)+f(Y)−f(X∪Y) = M_XM_Y/(M_X+M_Y)·(m_X−m_Y)²`, the three-block quadrangle, and the terminal bound |
| `BandMonge.quadrangle`, `terminal`, `linkCost_monge`, `terminal_needs_nonneg` | Lemma M, Lemma Z | Finitely many cells `0,…,n−1`, weights `μ > 0`, `W` non-increasing; Lemma Z also needs `W ≥ 0` | `w(a,c)+w(b,d) ≤ w(a,d)+w(b,c)` for `a ≤ b ≤ c ≤ d ≤ n` (`w` = weighted within-band variance); `w(a,c)+z(b) ≤ z(a)+w(b,c)`; the combined cost on `0,…,n+1` is Monge.  `W ≥ 0` is necessary: `W = (0,−1)` with equal weights gives `w(0,2)+z(1)=3/2 ≰ 1 = z(0)+w(1,2)` |
| `BandMonge.exchange`, `convex_of_monge`, `exists_optimal`, `exists_path`, `band_convex`, `bandE`, `bandE_is_min`, `bandE_second_difference` | Lemma X; Theorem B (finite-cell form) | Any Monge link cost; `k ≥ 1` links; for `bandE_second_difference`, also `μ > 0` and `W` nonincreasing and nonnegative | Tail swap at the first crossing turns a `k`- and a `(k+2)`-link path into two `(k+1)`-link paths of no larger total cost; a feasible path exists for every `k ≥ 1`, so an optimal path exists; `E_k` is defined as that minimum path cost and satisfies `2 E_{k+1} ≤ E_k + E_{k+2}` |
| `DriftSelection.ou_excess` | `theory/DRIFT_SELECTION.md` DS1(a); CLAIM_MAP section S | The OU stationary moment equations of (L) (Itô at stationarity) as inputs; `H` positive definite, `Q` Hermitian, `D_m, β, γ > 0` | `½ Tr(H P) = d/(2β) + ½ Tr[H (A+γI)⁻¹ Q]` with `A = D_m β H`.  The derivation of (L) from the origination–fixation chain, and existence/ergodicity of the stationary law, are **not** formalized |
| `DriftSelection.bm_excess`, `bm_excess_isotropic`, `bm_excess_static` | DS1(b) and the `Q=0` case of DS1(d) | Brownian lag-covariance equation (`γ = 0`); same `H`, `D_m, β > 0` | `½ Tr(H P) = d/(2β) + Tr(Q)/(2β D_m)`; with `Q = D I` this is `d/(2β)(1+D/D_m)`; with `Q = 0` this is the SA1b excess `d/(2β)` |
| `DriftSelection.velocity_mean_excess` | DS1(c), the mean-lag term | `A μ = −v` with `A = D_m β H`; `H` positive definite, `D_m, β > 0` | `½ μᵀ H μ = vᵀ H⁻¹ v / (2 β² D_m²)`.  The fluctuation contribution `d/(2β)` is SA1b / `Equipartition` and is added outside this identity |
| `DriftSelection.ou_excess_fast_remainder` | DS1(d), exact remainder to the fast-`γ` floor | `γ > 0`, `H` positive definite | `½ Tr[H (A+γI)⁻¹ Q] − ½ Tr[H (Q/γ)] = −½ Tr[H (A+γI)⁻¹ A (Q/γ)]` (the topological limit `γ→∞` is not formalized) |
| `Coadaptation.LogLinearChain`, `detailedBalance_of_potential`, `potential_of_detailedBalance`, `ca1_iff`, `stationary_of_detailedBalance` | `theory/COADAPTATION.md` (PR #148) CA1 | One party moves at a time; symmetric move graphs, each party's graph connected; positive rates with `q(x→y)/q(y→x) = e^{−β_i ΔJ_i}`.  Finiteness of the product state space is used only by `stationary_of_detailedBalance` | Some positive `π` satisfies detailed balance ⇔ the `β`-scaled game has an exact potential `Ψ`; then `π x = exp(-Ψ x)` (`detailedBalance_of_potential`) and `Ψ = -log π` (`potential_of_detailedBalance`).  Global balance (`stationary_of_detailedBalance`) is on a finite product |
| `Coadaptation.ca1a_weighted`, `ca1a_square` | CA1a | Weighted potential `Δ_i J_i = ω_i Δ_i Φ` | If `β_iω_i = γ` for all `i`, `γΦ` is an exact potential; if a potential exists, `(β_iω_i − β_jω_j)` times every mixed difference of `Φ` is `0` (so unequal `β_iω_i` with a nonzero mixed difference rules out detailed balance) |
| `DriftSpeed.meanLag_abs`, `ds2_excess`, `halfWindow_diverges` | CLAIM_MAP S2 / DS2 | Mean-speed bound `|E[θ(t)−θ(0)]| < v_max t` as input (jump-process construction not formalized); `v_max` is a free parameter, not identified with `Nμδ/(2d)`; equality `|v_k|=v_max` excluded; `λ_min > 0` is a Rayleigh lower bound on a free quadratic | **WEAKER.**  The lag theorem bounds `|E[L]|`, not S2's `E[|L|]`.  The cost theorem is a free-real Rayleigh/CS lower bound `½ λ_min B²`, not `E[J−J*]`.  There is no time-average statement.  The half-window lower bound `(c/2)(αT/2−β)²` diverges |
| `Coadaptation.unique_stationary_prob`, `unique_global_balance`, `joint_connected`, `unique_gibbs_stationary` | CA1 uniqueness (U1) | Finite joint state space; irreducibility of the move graph, which follows from connectedness of each party's graph; uniformization rate strictly larger than every exit rate.  Mathlib has no spectral Perron–Frobenius theorem; uniqueness is the elementary max-ratio argument | At most one stationary probability; when an exact potential `Ψ` exists it is the normalized Gibbs law `exp(−Ψ)/∑exp(−Ψ)`, independent of the clocks.  Faithful |
| `Coadaptation.potential_shift_independent`, `conditional_boltzmann`, `ca1b_potential_excess`, `ca1b_team_split` | CLAIM_MAP U2 / CA1b | Exact potential; for the Gibbs excess, a quadratic PD potential at strength `1`; for the team split, the mean of `½ δᵀ H_T δ` is supplied as the entrywise contraction `∑_{i,j} (H_T)_{ij} P_{ji}`, and `HΨ P = I` | `Ψ−β_i J_i` is independent of party `i`'s design, so the Gibbs law is conditionally Boltzmann (`potential_shift_independent`, `conditional_boltzmann`: Faithful).  `ca1b_potential_excess` is the Gibbs quadratic excess `d/2` at `β=1`, wrapping `Equipartition.gibbs_excess_quadratic` (Faithful).  `ca1b_team_split` identifies the entrywise contraction with `½ Tr(H_T (∇²Ψ)⁻¹)` (**WEAKER**: the identification of that mean with the contraction against `P` is an input).  U2's per-party `E[R_i]=d_i/(2β_i)` is not a declaration |
| `Coadaptation.ca1c_potential`, `ca1c_summed_cost`, `ca1c_gap_zero`, `ca1c_fraction` | CLAIM_MAP U2 / CA1c | `J_i = s_i J_T + h_i(x_{-i})`; `β_i s_i = γ`; `ca1c_summed_cost` uses `h_i=0` and `∑ s_i=1`; `ca1c_gap_zero` additionally takes `J_T(x^Ψ)=min` as input; `ca1c_fraction` takes `E[J_T]−J_T*=d/(2γ)` and `γ = σ N_e / J_T*` as inputs | `ca1c_potential` and `ca1c_summed_cost` (`∑_i J_i = J_T` at every state) are Faithful.  `ca1c_gap_zero` is **WEAKER** (`J_T(x^Ψ)=min` is an input; the coincidence of minimizers is not proved).  `ca1c_fraction` is **WEAKER**: it cancels `J_T*` between those two inputs (A2-L and the potential excess `d/(2γ)` are not proved here).  U2's `E[Φ]−Φ*=d/(2γ)` is not a declaration |
| `CoadaptationDrift.virial_trace`, `ca7_potential_excess` | CLAIM_MAP U11 / CA7 (1) | Lyapunov equation `V K Σ + Σ Kᵀ V = 2V+2Q` as input; `V` invertible, `Σ` symmetric, `Aᵀ=−A`, `K=S+A`; excess identified with `½ Tr(S Σ)`.  Symmetry of `S` is not a hypothesis | `E[Ψ]−Ψ* = ½(d + Tr(V⁻¹ Q))`.  Faithful with the Lyapunov equation as input.  The Hurwitz half of CA7 (1) (`−VK` is Hurwitz) is not formalized |
| `CoadaptationDrift.s8b_lyapunov`, `s8b_regret_party0`, `s8b_regret_party1`, `s8b_naive_party0`, `s8b_naive_party1`, `s8bP0_right_inv`, `s8bP0_lyapunov`, `s8b_static_regret`, `ca7_regret_not_naive` | CLAIM_MAP U11 / CA7 (4) | The exact s8b datum of `tools/coadaptation_checks.py` (`S=[[2,9/10],[9/10,1]]`, `w=[1,2]`, `γ=5`, `V=diag(1,2/5)`, `Q=diag(3/10,3/10)`, `M_{ij}=S_{ij} w_i/γ`); regrets are `½ (g_iᵀ P g_i)/M_{ii}` on a symmetric Lyapunov solution `P` (uniqueness of that symmetric solution is outside Lean) | Lyapunov `V S P + P S V = 2V+2Q` holds for `P=[[2323/1904,−603/476],[−603/476,13757/4760]]`; drift regrets are `10643/80000` and `2557/8000`, against naive uncoupled `13/100` and `7/20`.  At `Q=0`, the quadratic form on `P₀=S⁻¹=[[100/119,−90/119],[−90/119,200/119]]` gives regrets `1/10` and `1/5`, i.e. `1/(2β_i)`.  Faithful for the negative finding on the note's s8b covariance |


## Batch 1: representation, the two obstructions, finite partitions

Every declaration added in `GTAO/Cauchy.lean`, `GTAO/Representation.lean`,
`GTAO/Obstruction.lean`, and `GTAO/ContinuousA6.lean` is labeled against
the sentence it checks. Debreu's theorem, von Neumann–Morgenstern
linearity, and the Gelfand–Yaglom–Dobrushin reverse inequality are
hypotheses. They are not proofs.

| Lean name | Paper | Label |
|---|---|---|
| `AdditiveOnPos`, `Concatenates`, `mul_nat`, `below_gap`, `above_gap`, `ratBelow`, `ratAbove`, `ratBelow_bounds`, `ratAbove_bounds`, `tendsto_mul_div`, `tendsto_mul_div_above`, `tendsto_ratBelow`, `tendsto_ratAbove`, `eq_of_squeeze`, `f_one_nonneg_of_nondecreasing`, `f_one_nonpos_of_nonincreasing` | `theory/REPRESENTATION.md:68`–74, the estimates inside Lemma C | **Faithful.** Auxiliary definitions and bounds for the squeeze. The domain stays `(0, ∞)`. |
| `cauchy_rat`, `cauchy_monotone`, `cauchy_continuous` | Lemma C, lines 68–74 | **Faithful.** Positive rationals need no monotonicity. Either monotone direction gives `f(x) = x f(1)`. Continuity gives the same line. Both signs of `f(1)` are allowed. |
| `pexider_monotone`, `pexider_continuous` | Lemma P, line 76 | **Faithful.** `g = f + c` is additive, and `f(z) = p z - c` with `p` allowed to be negative. |
| `cauchy_nat` | Lemma C on the nonnegative integers, line 78 | **Faithful.** `f(0) = 0` and `f(n) = n f(1)`, with no topology. |
| `slope_nonneg_of_nondecreasing`, `price_zero_of_independent`, `Represents`, `IndependentOf` | Lemma M, line 80 | **Faithful.** A nondecreasing line has nonnegative slope. A coordinate the preorder ignores, on the positive orthant, has price 0. The witnesses are the constant-`1` vector and the vector that is `2` in that coordinate. The linear form is a hypothesis only for strictly positive vectors. |
| `DebreuAdditive`, `r1_linear_components` | Theorem R1, lines 84 and 102–118 | **Faithful** as packaging. `n ≥ 3`, a sum of continuous coordinate functions, and the Pexider equation are hypotheses. The conclusion is `C(z) = ∑ p_i z_i + b` on positive vectors, prices unsigned. Debreu's theorem is not proved. |
| `r1_vnm_scale` | lines 100 and 118 | **WEAKER.** Two positive affine writings of one index agree when that index takes two values. Von Neumann–Morgenstern linearity is a hypothesis. Debreu's common scale does not appear, so the declaration does not identify it with the currency regraduation. |
| `r1_nonneg_of_A8` | lines 92 and 120 | **Faithful.** A8, each concatenating component nondecreasing, gives each price `≥ 0`. |
| `r1_zero_of_not_essential` | lines 25 and 90 | **Faithful.** Same statement as `price_zero_of_independent`. The linear form and the preorder are used only on the positive orthant. |
| `r1_with_layer_count` | lines 94 and 112 | **Faithful.** Separability `C(z, K) = C_interval(z) + f(K)` is a hypothesis. Concatenation of counts then gives `h K`. No declaration drops it. |
| `r1_layer_price_nonneg_of_A8` | line 112 | **Faithful.** A8 on the integer count is the hypothesis that `fn` is nondecreasing. Then `h = fn 1 ≥ 0`. |
| `negative_price_example` | lines 90 and 64 | **WEAKER.** The declaration is the arithmetic of `z₀ + z₁ - z₂`: the components are continuous and the third price is `-1`. Line 90 also says the example satisfies A1–A7. That check is not in the declaration. |
| `IsArgmin`, `affine_argmin_iff`, `strictMono_argmin_iff` | line 126 | **Faithful.** For `a > 0`, and for any strictly increasing transform, the argmin on a menu that does not depend on the numerical cost is unchanged. |
| `affine_excess_scale`, `affine_excess_eq_iff` | lines 128–142 | **Faithful.** On one weight, `E[C] - C* = a (E[J] - J*)` and `b` cancels. Against the fixed Gibbs weight of `J`, `Equipartition.gibbs_excess_quadratic` gives equality with `d/(2β)` if and only if `a = 1`. |
| `affine_excess_refit` | line 142 | **Faithful.** `β_new = β / a` and `(a • H)` positive definite. The excess of `C` under its own Gibbs weight is `d / (2 β_new)`. |
| `fractional_excess_scale`, `fractional_excess_shift` | lines 144–150 | **Faithful** for `b = 0`, and for the rationals `E[J] = 2`, `J* = 1`, `b = 1`, which change the fraction from `1` to `1/2`. The general quotient `(a (E[J] - J*)) / (a J* + b)` is not a theorem. |
| `constrained_argmin_not_affine` | line 152 | **Faithful.** Two designs, costs `1` and `6/5`, variances `4` and `1`, level `3`, threshold `18/100`, shift `17/10`. Both designs are feasible before the shift and the cheaper one is design 0. After the shift only design 1 is feasible. |
| `sharedGrowth`, `kelly_qstar`, `log_le_tangent`, `log_lt_tangent`, `kelly_foc_sign` | line 160 and `theory/DYNAMICS.md:159` | **Faithful.** `q* = 13/50` is the unique maximizer of shared-shock log growth on `(0, 1]`. The printed growth value `0.128` is not an equality. |
| `kelly_not_expected_factor` | line 160 | **Faithful.** Lean expected factor `247/200`, robust `417/400`. The linear objective on `[0, 1]` is maximised only at pure lean, which is not `13/50`. |
| `intervalCost`, `expected_cost_interval` | line 162 | **Faithful.** `LayerLifetime.Tstar 1 (1/20) 1 (1/2) = √(1/10)` is the unique positive minimizer of `c/τ + α τ`. |
| `phi`, `quintic`, `cubic`, `quintic_eq_phi`, `hasDerivAt_quintic`, `cubic_neg`, `quintic_anti` | the numerator identity behind line 162 | **Faithful.** Exact polynomial arithmetic. `6000 t² φ(t)` is the quintic, and the quintic is strictly decreasing on `[0, 2]`. |
| `survival_interval_lt` | line 162 | **WEAKER.** The unique zero of `φ` on `(0, 2]` lies in `(23615/100000, 189/800)` and is strictly below `√(1/10)`, which itself lies in `(31622/100000, 31623/100000)`. The printed figures `0.2362` and `0.3162` are not equalities. The sentence also says this zero is the survival-optimal interval. Maximality of `θ` is not proved. That gap is appended in `BATCH1_PLAN.md`. |
| `klDiv_prob_integral` | `theory/CONTINUOUS_A6_2026-11-23.md:77` | **Faithful.** Probability measures, absolute continuity, and integrability of the log-likelihood are hypotheses. The divergence then equals `ENNReal.ofReal` of the integral. Without integrability Mathlib sets the divergence to `⊤`. |
| `klDiv_nonneg` | line 77, the interval `[0, ∞]` | **Faithful** to `0 ≤ klDiv` in `ℝ≥0∞`. That order is the codomain. Nonnegativity of the integral is a different fact. |
| `klDiv_zero_iff_eq` | line 111 | **Faithful** for the divergence: on probability measures it is `0` if and only if the measures are equal. The mutual-information form of that biconditional is not a separate declaration. |
| `mutualInfo`, `mi_swap`, `mi_data_processing` | line 145, symmetry and data processing | **Faithful.** Symmetry is the coordinate swap. Data processing is Mathlib's `klDiv_map_le` on the product map. |
| `klDiv_compProd_chain` | line 145 names a chain rule | **Faithful** to Mathlib's kernel identity `klDiv_compProd_eq_add`. It is not the mutual-information chain rule. That identification is a puzzle in `BATCH1_PLAN.md`, not a weaker equation. |
| `partitionMI`, `partition_mi_le`, `refinement_mono`, `finite_identity_attains`, `FiniteLabel`, `finitePartitionMI`, `finite_partition_le` | lines 99 and 101 | **Faithful.** A finite labeling does not raise mutual information. A coarser labeling, being a measurable function of a finer one, does not raise it either. On a finite alphabet the identity labeling attains the value. |
| `GYDSup`, `gyd_equiv` | lines 91 and 21 | **Faithful** as a hypothesis. `GYDSup` is the reverse inequality, joint divergence at most the supremum of finite-partition mutual informations. `gyd_equiv` adds that hypothesis to the proved inequality. The supremum is not constructed. |

## Batch 2: heat and repair floors

Declarations in `GTAO/HeatFloor.lean`, `GTAO/FiniteFloor.lean`,
`GTAO/FiniteFloorBounds.lean`, and `GTAO/RepairFloor.lean`. The two-state
floor, the finite-alphabet divergence, the class-indicator and 3-cycle
witnesses, and the one-carrier comparison `L ≥ 4 (log 2 - h)` are checked.
Four declarations are **WEAKER**, each with the missing clause in
`INVENTORY.md` and a miss row in `BATCH2_PLAN.md`. The telegraph lower
bound, the pairwise bound, the path bound, the product inequality on
`{0,1}^n`, and the two-distribution decoder bound are not declarations.

## LEAN-PHYS: diffusion heat step, T60 pairwise and path, T63 product

Declarations in `GTAO/DiffusionHeat.lean`, `GTAO/FiniteFloorPairwise.lean`,
`GTAO/FiniteFloorPath.lean`, and `GTAO/RepairTensor.lean`, planned in
`LEAN_PHYS_PLAN.md` before any proof (commit `07ce4e5`). This adds to the
Batch 2 paragraph above: the pairwise bound, the path bound, and the
product inequality on `{0,1}^n` are now declarations. Every assumption is
a named hypothesis or structure field.

| Declaration | Paper sentence | Label |
|---|---|---|
| `eq_heat_identity`, `eq_heat_steady`, `eq_heat_floor` | `theory/GENERALITY_2026-11-22.md:39-68`, Proposition EQ-heat | **WEAKER.** Integration by parts and the marginal-entropy identity are fields of `EQHeatHyp`, not derived from the SDE. Miss LP-eqheat. |
| `pairwise_L_ennreal` | `theory/GENERAL_FLOOR_FINITE_2026-11-23.md:115` | **Faithful** on the extended sum `iAlt`, no extra hypothesis. `pairwise_L` is the real form under absolute continuity. |
| `path_pinsker_ennreal`, `path_pinsker_stronglyConnected`, `telegraph_K` | `theory/GENERAL_FLOOR_FINITE_2026-11-23.md:117-129` | **Faithful.** `pathWeight` counts each edge with its multiplicity. `path_pinsker` is the real form under absolute continuity on used edges. |
| `pairwise_telegraph` | `theory/GENERAL_FLOOR_FINITE_2026-11-23.md:107` | **Faithful** to the lower bound `I_alt ≥ r L(ε)` for `ε < 1/2`. Equality and the converse are not declarations. |
| `cube_tensorization` | `theory/RECORD_REPAIR_FLOOR_2026-11-23.md:75` | **WEAKER.** Strictly positive `p`; the zero-atom case, where the note's `σ` is `+∞`, is miss LP-tensor-zero. |

## What is not formalized

None of the following is claimed as proved in Lean.

- The hypothesis at the top of CORE.md (a claim about the real world).
- Convexity of `ε_K` in Model S, still unproved on paper (CORE §4, KEYSTONE_NOTE).  The increment *formula* in N60 is formalized only as a consequence of discrete convexity, which is an assumption here.
- The stochastic derivations behind the layer-lifetime and local-vs-shared cost expressions (Brownian exit times, the time-average square gap `b²/6`, the delay floor `N w σ² ℓ`, and Chalkley's exactness at zero discount).  The optimization and comparison on those expressions are formalized; the expressions are inputs.  `MemoryRule.occupation_integrals` computes the two integrals of the assumed density `b − |x|`; the density, the exit-time identification, and the optimality of a barrier policy among all re-check policies stay inputs.
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
- CT11, CT12 beyond its minimizer, CT13–CT16, CT17 (i), CT18, CT19, CT23, CT24, CT25, CT26–CT32, CT35–CT43, and the Master Theorem in the class `𝓜_LG`.
- Any information-theoretic construction of `D` or `IB`; they enter CT4 as functions with the stated convexity and monotonicity.
- LAYER_CONVEXITY: N60 started from `k_0 > 0` (the from-1 formula); Theorem B for a continuous frequency measure (only finitely many cells with positive weights are formalized); the identification of the finite-cell minimum `bandE` with the staircase cost `BandCounterexample.cost`; the corollary that `K*_0` equals the leftmost argmin in 𝓑; the Wiener-gain reading `W = 1/(1+N/S)`; Model S convexity for `J≥3`; Model S convexity for `J≤2` (N64(iii); Kalman/Wiener, not formalized in this batch).
- DRIFT_SELECTION: the generator expansion from the origination–fixation chain to the Langevin equation (L), existence and uniqueness of the stationary law and the ergodic theorem (time average = stationary mean); DS1(b) for a general mutation matrix `M` (`d/(2β) + Tr(M^{-1} Q)/(2β)`); DS1(c) as the single excess `d/(2β) + vᵀH⁻¹v/(2 β² D_m²)` (only the mean-lag term is formalized; the fluctuation `d/(2β)` is not supplied here by `Equipartition`); the jump-process construction behind the DS2 mean-speed bound; S2's `E[|L|]`, `E[J−J*]`, and time average (the formalized DS2 lag, cost, and half-window theorems are WEAKER: they bound `|E[L]|`, give a Rayleigh lower bound on a free quadratic, and have no time-average statement); DS3; Corollary DS1c (the fractional form with `β = σ N_e / J*`); the topological limit `γ→∞` in DS1(d).
- COADAPTATION: the origination–fixation derivation of the log-linear rate ratio; CA2–CA4 and CA5–CA6; CA7 (2) the blockwise virial and CA7 (3) the team mismatch bracket (order-preserving Lyapunov inverse from CA3); the Hurwitz half of CA7 (1) (`−VK` is Hurwitz); the §6 counterexamples; U2's per-party `E[R_i]=d_i/(2β_i)` and `E[Φ]−Φ*=d/(2γ)` (not declarations); the A2-L identification `γ = σ N_e / J_T*` and the derivation of equal-`σ N_e`; uniqueness of the symmetric s8b Lyapunov solution.  CA1 uniqueness and the CA7 (1) excess identity are Faithful in this batch.  CA1b's shift, Boltzmann, and Gibbs quadratic excess are Faithful; the team split is WEAKER (the second-moment contraction is an input).  CA1c's potential and summed-cost identity are Faithful; `ca1c_gap_zero` and `ca1c_fraction` are WEAKER (`J_T(x^Ψ)=min`, and cancellation of `J_T*` between `d/(2γ)` and `γ = σ N_e / J_T*`).  CA7 (4) is the s8b negative finding, Faithful on that datum, including the `Q=0` quadratic-form static regrets.

## RND-RECORD-COST: copy ban under drift, dimension bound, pricing (side R&D)

Modules under `GTAO/Rnd/`, moved unchanged (apart from the module header)
from a private Lake project with the same pins. Paper:
`theory/RECORD_COST_CHAIN_2026-11-25.md`. `scripts/RndAxioms.lean` runs
`#print axioms` on the 253 listed theorems (19 for the rounds 4–9
note, 4 for the round 10 note, and the Lean rounds 3 to 6 theorems, below); each depends only on
`propext`, `Classical.choice`, `Quot.sound`, or a subset. Every modelling
input is a named hypothesis, a structure field, or a definition. None is a
Lean `axiom`. The named assumptions NA1–NA6 are those of §5 of the paper (the
"NA" prefix keeps them apart from the theory's axioms A1–A8): NA1 the SO(3)
connected-subgroup classification, NA2 the inner-product-preserving drift, NA3
the polygon `V` and `σ` as definitions, NA4 "the disk pays 0" as a definition,
NA5 the Lie setting, NA6 the modelling fields (`CopyModel`, the tensor property
in `gbit_no_local_write`, the cost-dial refresh term).

| Declaration | Paper step | Label |
|---|---|---|
| `GTAORnd.SelfRef.fourier_core`, `no_linear_clone_gpt`, `no_linear_clone_circle` | S1 (copy ban on a moved circle orbit) | **Faithful** to the trigonometric and GPT forms. That a compact connected drift contains such a circle orbit is the setting (assumption NA5), not a declaration. |
| `GTAORnd.SelfRef.R3_full`, `dim_bound` | S2 (`d ≥ N + 1`) | **WEAKER.** "H compact" is replaced by the declared hypothesis `hinv`: the drift's linear parts preserve one inner product and depend continuously on the group element (assumption NA2). |
| `GTAORnd.ring_bound`, `factor_ge_two`, `discrete_oneParam_trivial`, `disk_oneParam`, `disk_strictly_cheaper` | S3 (polygon cost `≥ 2Θ²/V`) | **WEAKER.** `V`, `σ` and "the disk pays 0" are definitions (assumptions NA3, NA4), not derived from a path measure. |
| `GTAORnd.SelfRef.normal_fixer_bot`, `normal_nontrivial_fixes_nothing`, `SelfRefRun.normal_fixer_trivial` | S4 (ball in `d = 3`) | **Partial.** Group step only. Ball uniqueness rests on the SO(3) connected-subgroup classification, not in Mathlib (assumption NA1). |
| `GTAORnd.Composition.P1`, `log_additive_iff`, `P2_entries` | S5 (additive price is `c log` count) | **Faithful.** |
| `GTAORnd.CopyModel.lemmaB1`, `lemmaB1_k`, `clone2_to_k` | S6 (Lemma B1) | **Faithful** under the `CopyModel` fields; capacity is weakened to `≤ N` (a stronger lemma); the 1→2 form needs at least one effect; the `CopyModel` fields are assumption NA6. Controls: `unitModel_clones`, `square_B1_hypotheses`. |
| `SelfRefRun.perm_periodic`, `SelfRefRun.no_zero_drift_while_recording` | S7, S8 | **Faithful.** |
| `GTAORnd.SelfRef.liar_half`, `sharp_flip_no_fixed` | S9 | **Faithful.** |
| `GTAORnd.SelfRef.Jdial_stationary_iff`, `Jdial_midpoint`, `Jdial_midpoint_60` | S10 (cost dial) | **WEAKER.** Stationarity only here; the global minimum for `β ≤ π/2` is in Lean round 3 below (`Jdial_midpoint_global`), and for `β > π/2` it is open. The refresh term is a modelling choice (assumption NA6). |

Not formalized here: the SO(3) classification and the convex-geometry steps
of S4; Haar averaging behind `hinv`; the scripted counts (boxworld's 128
symmetries, the complete-record table, the zero-drift prices). The witness that the
qubit ball attains `d = N + 1` is in Lean round 3 below (`qubit_bound_tight`).

Rounds 4–9 (`theory/RECORD_COST_ROUNDS4-9_2026-11-25.md` §10): `GTAO/Rnd/SelfRef/SFP.lean`
and `GTAO/Rnd/SelfRef/Precision.lean`, namespace `GTAORnd.SelfRef.R78`, moved with only the
header, the module lines and doc-comment wording changed. `SFP G X` says every element of `G`
fixes some point of `X`.

| Declaration | Note item | Label |
|---|---|---|
| `jordan_derangement`, `finite_transitive_not_SFP`, `simplex_not_SFP`, `square_rotation_moves_all`, `square_not_SFP` | L1 (finite transitive groups fail SFP) | **Faithful.** Jordan's theorem is proved from Mathlib's Burnside lemma. |
| `SO_odd_fixes_unit`, `SO_odd_fixes_poles`, `SO3_fixes_poles`, `odd_ball_SFP` | L2 (odd balls with SO(2m+1) satisfy SFP) | **Faithful** for the full SO(2m+1); other transitive groups are not covered. |
| `SO2_nonid_no_fixed`, `disk_not_SFP`, `even_ball_not_SFP` | L3 (disk and even balls fail SFP) | **Faithful** for SO(2) and SO(2m). |
| `ball_record_bound`, `chord`, `disk_record_error`, `disk_error_linear`, `disk_exceeds_ball` | L4 (finite precision) | **Faithful** to the toy: the ball record sits at angle δ from the true axis; the disk residual per step is ε. Re-learning cost is not modelled. |
| `mixture_copy_core`, `no_copy_mixture` | L5 (copyable records are distinguishable) | **Partial.** Linear core only. The full step is in Lean round 3 below (`L5_perfect`, `L5_pairwise`). |

Not formalized here: the maximal-torus criterion for SFP in general, the O(3) subgroup
classification, G₂ and quaternionic quantum theory, and the orbitope and cost results of
the rounds 4–9 note. The cases SO(n) on balls (iff n odd), complex quantum theory and real
quantum theory with its orthogonal group are in Lean round 3 below.

Round 10 (`theory/RECORD_COST_ROUND10_2026-11-25.md` §11): `GTAO/Rnd/SelfRef/ContinuousTime.lean`,
namespace `GTAORnd.SelfRef.R10`.

| Declaration | Note item | Label |
|---|---|---|
| `continuous_line_discrete_const`, `finite_group_no_continuous_motion`, `continuous_change_infinite_group` | §3 (continuous time with change forces an infinite reversible group) | **Faithful.** That a polytope's reversible group is finite is not formalized. |
| `never_returns_infinite_order` | §5 (a never-returning orbit forces infinite order of the global map) | **Faithful.** |

Lean round 3 (side session, 26 November 2026): `GTAO/Rnd/SelfRef/Broadcast.lean` and
`GTAO/Rnd/SelfRef/BroadcastControl.lean`, namespace `GTAORnd.SelfRef.LR3`. The setting is the
`CopyModel` of `LemmaB1.lean`, plus two hypotheses passed as arguments, not new fields:
`CoarseGrain` (classical post-processing of an allowed measurement is allowed) and `NonNeg`
(measurement values are non-negative).

| Declaration | Note item | Label |
|---|---|---|
| `amplify` | L5, analysis step | **Faithful.** For `0 ≤ q < p ≤ 1` and `ε > 0`, some `k, m` give `1 − (1 − p^k)^m ≥ 1 − ε` and `1 − (1 − q^k)^m ≤ ε` (AND/OR amplification). |
| `L5_asymptotic` | L5 (copyable records are distinguishable) | **Faithful**, asymptotic form. If one allowed channel clones `x` and `y` into two copies and some allowed measurement separates them, then for every `ε > 0` an allowed two-outcome measurement fires on `x` with probability at least `1 − ε` and on `y` with probability at most `ε`. The no-broadcasting theorem is not used: the proof measures both copies and iterates through the cloner. |
| `L5_perfect`, `L5_pairwise` | L5 | **Faithful** under the extra hypothesis that the set of achievable firing-probability pairs on `(x, y)` is closed (true when the effect set is compact). Then `x` and `y` are perfectly distinguishable. Over a family cloned by one channel, with separating measurements, any two distinct members are perfectly distinguishable. Purity of records is not derived. Cloning is assumed, not broadcasting of mixed states. |
| `bit_achSet`, `L5_control` | control | **Faithful.** In the classical bit model (`bitModel`) every hypothesis of `L5_perfect` holds for two distinct states, so the theorem applies non-vacuously. |

Further Lean round 3 modules, same namespace: `SFPCriterion.lean`, `Transport.lean`
(namespace `GTAORnd.SelfRef.LR3.Transport`), `CostDialGlobal.lean`, `QubitWitness.lean`,
`FiniteGeometry.lean`, `Composite.lean`.

| Declaration | Note item | Label |
|---|---|---|
| `ball_SFP_iff_odd` | rounds 4–9 §5 (maximal-torus criterion), ball case | **Special case.** SO(n) on the unit sphere of ℝⁿ satisfies SFP iff n is odd. The general criterion (rank H = rank G) is not formalized. |
| `complex_fixes_ray`, `unitary_fixes_ray` | rounds 4–9 §5, complex quantum theory | **Special case, faithful.** Every complex d×d matrix (d ≥ 1), in particular every unitary, has an eigenvector, so it fixes a pure state. |
| `real_odd_fixes_ray`, `real_even_not_SFP` | rounds 4–9 §5, real quantum theory | **Special case, faithful.** Every element of O(2m+1) has eigenvalue 1 or −1. The quarter turn in O(2m) has no real eigenvector. Pure states are rays. |
| `hept_step_le`, `hept_partner`, `hept_path_cost` | round 10 §14 (gentle transport, 7-gon) | **WEAKER.** The operational distance is defined as a supremum over the 7-gon's effects. Neighbouring vertices are at distance at most `λ = sin(π/7)/sin(3π/7)`. `v 0` and `v 3` are perfectly distinguishable. The path `v0 → v1 → v2 → v3` costs at most `3λ² < 0.67`. That 0.594 is the exact optimum is not formalized. |
| `disk_dist`, `disk_partner`, `disk_cost_ge`, `disk_cost_attained` | round 10 §14 (gentle transport, disk) | **Faithful** for T = 3. The disk distance between pure states equals `abs (sin ((φ − ψ)/2))`. Every 3-tick path through pure states from `p 0` to its partner `p π` costs at least 3/4, and equal thirds attain it. |
| `hept_beats_disk` | round 10 §14 (odd polygons beat the disk at T = 3) | **Faithful** to the T = 3 comparison at unit price per squared distance (both spaces have affine dimension 2, so the per-dimension term cancels). Other horizons and polygons are not formalized. |
| `Jdial_midpoint_global`, `Jdial_midpoint_unique`, `Jdial_60_global`, `rho_60` | chain S10 (cost dial, global minimum) | **Special case.** At `ρ = 1/(2cos(β/2))` the midpoint `β/2` is a global minimizer for `0 < β ≤ π/2`, and the unique one modulo 2π for `β < π/2`. For `β = 60°` (`ρ = 1/√3`), 30° is the unique global minimizer. For `β > π/2` the midpoint is not the global minimizer (numerically); that is not formalized. |
| `qubit_attains_bound`, `qubit_bound_tight` | chain S2 (`d ≥ N + 1` is attained) | **Faithful.** In ℝ³, the poles `±e₃` under the rotations about `e₃` meet every hypothesis of `dim_bound`, and `finrank = 3 = N + 1`. |
| `finite_divring_comm`, `chevalley_nonzero_zero`, `diag_form_isotropic`, `norm_form_isotropic` | round 10 §8 (finite-geometry step, the algebra after Piron) | **Partial.** A finite division ring is commutative (Mathlib's `littleWedderburn`). Diagonal quadratic forms in at least 3 variables over a finite field have a non-zero zero (from Mathlib's Chevalley–Warning). Norm forms `a₁N(x₁) + a₂N(x₂)` over a finite extension do too. Not formalized: Piron's representation, diagonalization of Hermitian forms, the classification of involutions of finite fields, and Baer's rank-3 case. |
| `cube_corr_bound`, `square_corr_bound`, `cube_corr_tight` | `theory/RECORD_COST_ROUND10_2026-11-25.md` §15, Lemma 1 for hypercube parts | **Faithful** for hypercube parts (square, cube). Positivity on products of facet effects gives every `abs Cᵢⱼ ≤ 1`, so `‖C‖²_F ≤ m_A m_B = R_A² R_B²` (square: ≤ 4). Products of vertices attain it. Cross-polytope parts are not covered. |
| `pure_marginal_product`, `pure_marginal_factorizes` | `theory/RECORD_COST_ROUND10_2026-11-25.md` §15, Lemma 2 | **Faithful, abstract form.** If the marginal is an extreme point, every conditional unnormalized state is a multiple of it, so the joint statistics factorize. That the max composite with no-restriction parts supplies these conditional states is a hypothesis. |
| `square_C_bound`, `square_pure_marginal`, `pure_marginal_finite` | `theory/RECORD_COST_ROUND10_2026-11-25.md` §15, the two Lean candidates (square case of Lemma 1, finite Lemma 2) | **Faithful** to the stated candidates. L1: in the max product of two squares (coordinates in [−1,1]², facets (1 ± x_i)/2), positivity on the sixteen facet products gives Σ C_ij² ≤ 4 = R_A²R_B². L2 square instance: if a marginal coordinate is ±1 then C_ij = a_i b_j. L2 general finite form: facet functionals of A, a vertex whose tight facets cut out only its line, facet functionals of B that span B's dual with a positive combination equal to the unit; a matrix non-negative on all facet products whose A-marginal is the vertex is a product v yᵀ. |

Lean round 3, third batch (same namespace): `OControl.lean`, `Modular.lean` (namespace
`GTAORnd.SelfRef.LR3.Modular`), `Entangle.lean` (`...LR3.Entangle`) and `M11Prime.lean`
(`...LR3.M11Prime`). The first two answer a hostile review of the Lean layer; `Entangle.lean`
holds the entanglement round's candidates LE0–LE5; `M11Prime.lean` holds the Lean-able steps of
Theorem M11 as amended by a hostile review (M11′).

| Declaration | Note item | Label |
|---|---|---|
| `ball_O_not_SFP`, `qubit_O3_not_SFP` | rounds 4–9 note §10, control for `R78.odd_ball_SFP` | **Faithful.** For every n ≥ 1, the n-ball under the full orthogonal group O(n) fails SFP, because `-1` fixes no pure state; the qubit (n = 3) under O(3) fails. So the group choice SO(2m+1) in `odd_ball_SFP` carries weight. |
| `SO1_trivial`, `sphere_one_two_points` | control for `R78.odd_ball_SFP` at m = 0 | **Faithful.** SO(1) is the trivial group and the 0-sphere is `{±1}`: the m = 0 case of `odd_ball_SFP` is SFP of the trivial group on a classical bit. |
| `r_covBy`, `r_step_le`, `modular_of_semimodular` | round 10 note §8, the lattice route (finite-height step) | **Faithful.** In a finite lattice that is upper and lower semimodular, the height rank goes up by exactly one along covers (Jordan–Dedekind), the rank identity `r a + r b = r (a ⊔ b) + r (a ⊓ b)` holds, and the lattice is modular (Dilworth–Birkhoff). |
| `lower_of_upper_ortho`, `modular_of_upper_ortho`, `orthomodular_of_upper_ortho`, `finite_of_atomistic`, `upper_of_atomistic_covering`, `orthomodular_of_atomistic` | round 10 note §8 | **Faithful.** An orthocomplementation (antitone involution giving complements) turns upper into lower semimodularity; so a finite upper semimodular orthocomplemented lattice is modular and orthomodular (`a ≤ b → a ⊔ (a⊥ ⊓ b) = b`), the property Piron's theorem needs. An atomistic complete lattice with finitely many atoms is finite. Atomistic plus the covering property gives upper semimodular, and `orthomodular_of_atomistic` puts the steps together: an atomistic complete lattice with finitely many atoms, the covering property and an orthocomplementation is orthomodular. Whether the GPT face lattice carries an orthocomplementation is a premise of the round 10 note, not proved here. |
| `pure_marginal_extreme` | entanglement round, LE1 | **Faithful, normalization written out.** If B's effects span and a positive combination is the unit, every conditional `X f_q` lies in the cone over A's convex normalized state space `Ω` (unit functional equal to 1 on `Ω`, stated as a hypothesis), and the marginal `X u_B` is an extreme point of `Ω`, then `X = x yᵀ`. Same core as `pure_marginal_finite` (which uses tight facets instead of an extreme point). |
| `reversible_preserves_pure` | entanglement round, LE2 | **Faithful.** A linear automorphism `T` with `T '' Ω = Ω` maps the extreme points of `Ω` exactly onto themselves. |
| `local_perm_tprod`, `local_map_tmul`, `swap_tmul` | entanglement round, LE0 | **Faithful, elementary.** `(⊗ g_i) ∘ P_σ` sends `⊗ ω_i` to `⊗ g_i ω_{σ⁻¹ i}`; the two-part versions restate Mathlib's `TensorProduct.map_tmul` and `comm_tmul`. |
| `simplex_extreme_iff`, `classical_pure_product` | entanglement round, LE5 (classical control) | **Faithful.** The extreme points of the probability simplex on a finite set are exactly the point masses; on `Fin m × Fin n` each is a product `δ_i ⊗ δ_j`. |
| `le4_bound`, `le4_attained` | entanglement round, LE4 | **Faithful, arithmetic.** `∑ abs β_i ≤ 1/2` over three rationals gives `∑ β_i ≤ 1/2` and success `1/2 + (1/3)∑β ≤ 2/3`; the value `1/2 + (1/3)(3/2) = 1`. |
| `classical_no_purification` | purification (control) | **Faithful, a control.** In classical theory every pure joint state on `Fin m × Fin n` has a point-mass marginal, so a mixed state has no purification in any classical composite. Purification itself is not formalized and is not implied by the other premises. |
| `extreme_trivial_decomp`, `cnot_mixed_correlated` | entanglement round C, items C1 and C3 | **Faithful.** C1: an extreme point of a convex set has only the trivial finite convex decomposition (every component with positive weight equals it). C3 countermodel: the classical 2-bit state `½δ₀₀ + ½δ₁₁` (CNOT on `(½δ₀ + ½δ₁) ⊗ δ₀`) is a valid state, is not an extreme point, and is not the product of its marginals. |
| `moment_quad`, `moment_trace`, `star_equiv` | M11′, 2-level hypothesis | **Faithful.** With vertices on a sphere `‖v‖² = R²`, facet normals of equal squared length `s` with second moment `∑ n nᵀ = c I`, and `abs(n·v) ≤ 1`: the part is 2-level (`abs(n·v) = 1` throughout) iff `R² s = m`. |
| `max_pos_corr`, `lemma1_general` | M11′, Lemma 1 | **Faithful.** The four product-facet inequalities give `abs(nᵀ C k) ≤ 1`; with second moments `(#N_A s_A / m_A) I` and `(#N_B s_B / m_B) I` this gives `‖C‖²_F ≤ m_A m_B / (s_A s_B)`, generalizing `cube_corr_bound`. |
| `hull_strict` | M11′, strictness | **Faithful.** A point of the convex hull of points on the sphere of radius R that is not one of them has norm `< R`. |
| `average_invariant` | M11′, averaging in place of John for polytopes | **Faithful.** For a finite group acting linearly and a symmetric positive definite `M`, `∑_g ρ(g)ᵀ M ρ(g)` is symmetric, positive definite and invariant. |
| `final_assembly` | M11′, last step | **Faithful, elementary.** A bijection of the extreme points that preserves `q`, with `q` strictly larger at product pure states than elsewhere, maps the product pure states onto themselves. The Schur block step and the Löwner/Haar step for non-polyhedral S are not formalized. |
| `invariant_form_scalar`, `cross_term_zero` | M11′, Schur step (partial) | **Special case.** For an orthogonal representation whose commutant is the scalars (absolute irreducibility, as a hypothesis), every invariant form is a multiple of the identity; and an invariant coupling to a part the group leaves fixed vanishes once `-1` is in the group (central symmetry), so the A–B, A–C and B–C cross terms drop. That the C block (the tensor product representation) is absolutely irreducible is not formalized. |

Lean round 4 (namespace `GTAORnd.SelfRef.LR3.M11Cube`, file `M11Cube.lean`): Theorem M11′ assembled
for hypercube parts and for cross-polytope parts. Tensor coordinates are indexed by `Option (Fin m_A) × Option (Fin m_B)`
(unit, Bloch and correlation coordinates); `maxSet` is the maximal tensor product of the cubes
`[-1,1]^{m_A}`, `[-1,1]^{m_B}` (normalized, nonnegative on every product of facet effects) and
`pureSet` the products of cube vertices.

| Declaration | Note item | Label |
|---|---|---|
| `flip_invariant_diag` | M11′, Schur step, tensor block (hyperoctahedral case) | **Faithful.** A matrix on the tensor coordinates invariant under every local coordinate sign flip of A and of B is diagonal: this covers the cross terms and the off-diagonal part of the C block. |
| `swap_invariant_blocks` | M11′, Schur step, tensor block (hyperoctahedral case) | **Faithful.** Invariance under local coordinate swaps makes the diagonal constant on the A, B and C blocks. Not needed for the hypercube assembly; used for cross-polytope parts. |
| `pureProd_mem_maxSet`, `maxSet_sq_le`, `pure_of_sq_one` | M11′, Lemma 1 and strictness for hypercube parts | **Faithful** (`m_A, m_B ≥ 1` for the bound). Products of cube vertices lie in the maximal tensor product; there every tensor coordinate lies in [−1,1]; a point of it with every coordinate ±1 is a product of cube vertices. |
| `avgGram_invariant`, `avgGram_diag_ge_one` | M11′, averaging over a finite group | **Faithful.** `A = ∑_γ ρ(γ)ᵀρ(γ)` over a finite group is invariant and has every diagonal entry ≥ 1. |
| `diag_form_max` | M11′, strictness for hypercube parts | **Faithful.** On the maximal tensor product a diagonal form with positive diagonal is at most its trace, with equality only where every coordinate is ±1. |
| `m11_cube_into`, `m11_cube` | M11′, assembled for hypercube parts | **Faithful for hypercube parts, with `Γ` as a hypothesis.** For any finite group `Γ` acting linearly on the tensor coordinates whose image contains the local sign flips, and any `S` with `pureSet ⊆ S ⊆ maxSet`: an element of `Γ` mapping `S` into `S` maps product states to product states, and one mapping `S` onto `S` maps them onto themselves (`m11_cube`, whose last step is `M11Prime.final_assembly` with `E := S`). The intended instance is `Γ = Aut(S)`; that `Aut(S)` is finite for a polytope is not formalized. Cross-polytope parts: `m11_cross` below; mixed parts (cube with cross-polytope) are not covered. |
| `pureProdX_mem_maxSetX`, `maxSetX_bounds`, `maxSetX_unit` | M11′ for cross-polytope parts (vertices `±e_i`, facets `1 + s·a` for sign vectors `s`) | **Faithful.** `maxSetX` is the maximal tensor product of two cross-polytopes. Products of vertices lie in it; on it `(s·a)² ≤ 1`, `(t·b)² ≤ 1`, `(sᵀCt)² ≤ 1` for sign vectors, and `0 ≤ 1 + σa_i + τb_j + στC_ij` for `σ, τ = ±1`. |
| `sum_sgn_sq`, `maxSetX_frob`, `sq_le_of_l1` | M11′, Lemma 1 for cross-polytope parts | **Faithful.** Averaging over sign vectors, `∑_s (s·u)² = 2^m ‖u‖²`; hence `‖C‖²_F ≤ 1 = R_A²R_B²` on `maxSetX`. A vector with `∑ abs u_i ≤ 1` has `‖u‖² ≤ 1`, with equality only at a vertex `±e_i`. |
| `pure_of_eqX`, `quad_blocks` | M11′, strictness for cross-polytope parts | **Faithful.** A point of `maxSetX` with `‖a‖² = ‖b‖² = ‖C‖²_F = 1` is a product of vertices; a diagonal form constant on the A, B and C blocks is `q₀₀x₀₀² + α‖a‖² + β‖b‖² + γ‖C‖²_F`. |
| `m11_cross_into`, `m11_cross` | M11′, assembled for cross-polytope parts | **Faithful for cross-polytope parts, with `Γ` as a hypothesis.** For any finite group `Γ` acting linearly on the tensor coordinates whose image contains the local sign flips and coordinate swaps (these generate the hyperoctahedral group, the cross-polytope's symmetry group), and any `S` with `pureSetX ⊆ S ⊆ maxSetX`: an element of `Γ` mapping `S` into `S` maps product states to product states, and one mapping `S` onto `S` maps them onto themselves. Chain: averaging, `flip_invariant_diag` and `swap_invariant_blocks` (the tensor Schur block for this group), `sq_le_of_l1` and `maxSetX_frob` (Lemma 1), `pure_of_eqX` (strictness), `M11Prime.final_assembly` with `E := S`. The finiteness of `Aut(S)` is not formalized. |
| `autSet_finite`, `pureSet_span`, `pureSetX_span` | M11′, finiteness of `Aut(S)` for polytopes | **Faithful.** The reversible maps of `S` (invertible matrices `T` with `T '' S = S`) form a group, finite when `S` is the convex hull of a finite set spanning the space: each `T` permutes the extreme points, and Krein–Milman makes `T` determined by them. The products of cube vertices span the tensor coordinates, and so do the products of cross-polytope vertices (`m_A, m_B ≥ 1`). |
| `m11_cube_polytope`, `m11_cross_polytope` | Theorem M11′ for polytope composites of two hypercubes or two cross-polytopes | **Faithful for these parts, no group hypothesis.** Let `S` be the convex hull of a finite set with `pureSet ⊆ S ⊆ maxSet` (resp. `pureSetX ⊆ S ⊆ maxSetX`), `m_A, m_B ≥ 1`, invariant under the local sign flips (and, for cross-polytopes, the local coordinate swaps). Then every reversible map of `S` maps the product states onto the product states. `Γ = Aut(S)` is built and shown finite, then `m11_cube` / `m11_cross` apply; the steps are chained and the strict separation is derived. Not covered: other 2-level parts, mixed parts (cube with cross-polytope), non-polyhedral `S`, and composites not invariant under the full local hyperoctahedral group. |

Lean round 4, transport (namespace `GTAORnd.SelfRef.LR3.TransportHorizons`, file
`TransportHorizons.lean`; same model as `Transport.lean`).

| Declaration | Note item | Label |
|---|---|---|
| `disk_cost_T2` | round 10 §14 (gentle transport, disk), T = 2 | **Faithful.** Every 2-tick path through pure states from `p 0` to its partner `p π` costs exactly 1. |
| `cos_sum4_le`, `disk_cost_T4_ge`, `disk_cost_T4_attained` | round 10 §14 (gentle transport, disk), T = 4 | **Faithful** for T = 4. `cos A + cos B + cos C + cos D ≤ 2√2` when the angles sum to π, so every 4-tick pure path from `p 0` to `p π` costs at least `2 − √2`, and equal quarters attain it. The polygon side at T = 2, and horizons other than 2, 3 and 4, are not formalized. |
| `nona_step_le`, `nona_partner`, `nona_path_cost`, `nona_beats_disk` | round 10 §14 (odd polygons beat the disk), T = 4 | **WEAKER** on the 9-gon side, **faithful** on the disk side. In the 9-gon, neighbouring vertices are at operational distance at most `μ = sin(π/9)/sin(5π/9)`, `w 0` and `w 4` are perfectly distinguishable, and the path `w0 → … → w4` costs at most `4μ² < 0.52`; so it costs less than every 4-tick pure path in the disk (at least `2 − √2`). That the note's 0.483 is the 9-gon's exact optimum is not formalized; same unit price per squared distance as `hept_beats_disk`. |

Lean round 4, cost dial (file `CostDialBeyond.lean`, namespace `GTAORnd.SelfRef.LR3`).

| Declaration | Note item | Label |
|---|---|---|
| `Jdial_midpoint_not_global`, `Jdial_tie_at_right_angle` | chain S10 (cost dial, `β > π/2`) | **Faithful** at the tuned weight `ρ = 1/(2cos(β/2))`. For every `π/2 < β < π`, `α = β/2 + π/2` costs strictly less than the midpoint, so the midpoint is not a global minimizer; at `β = π/2` the two tie. This settles the converse left open in the `Jdial_midpoint_global` row and corrects "from β ≈ 1.61" in the `CostDialGlobal.lean` docstring: the midpoint stops being the global minimizer right after π/2. Where the minimizer lies for `β > π/2` is not formalized. |

Lean round 5 (namespace `GTAORnd.SelfRef.LR3.M11Blocks`, file `M11Blocks.lean`): Theorem M11′ for
parts that are products of cross-polytopes, under a minimal symmetry hypothesis. A *block part* has
its coordinates grouped into blocks (`b : Fin m → Fin r`) and state space
`{a : ∑_{i ∈ block k} |a_i| ≤ 1 for every block k}`: singleton blocks give the cube, one block the
cross-polytope, and other labellings e.g. octahedron × octahedron. `maxSetB` is the maximal tensor
product of two block parts (facet effects `1 + s·a` with `s` a sign vector on one block, zero
elsewhere) and `pureSetB` the products of their vertices. This covers the mixed composite (cube with
cross-polytope) that the round 4 rows leave open.

| Declaration | Note item | Label |
|---|---|---|
| `diag_of_separating`, `flips_separate` | M11′, Schur step, tensor block, minimal diagonal form | **Faithful.** A matrix on the tensor coordinates invariant under a family of diagonal matrices that separates every pair of distinct coordinates (for `u ≠ v` some `diag d` in the family with `d u * d v ≠ 1`) is diagonal. The local sign flips form such a family; so does any smaller set of sign patterns that tells all coordinates apart. Among diagonal symmetries the condition is also necessary for this step: if no `d` in the family separates `u ≠ v`, the matrix `E_uv + E_vu` is invariant under all of them. (Appended after the hostile review of Lean round 5: this necessity sentence was on paper, not stated in Lean, at round 5; it is now `sep_necessary`, Lean round 6, below, for the Schur step only.) |
| `pure_mem_maxSetB`, `maxSetB_bounds`, `maxSetB_unit` | M11′, Lemma 1 setting for block parts | **Faithful.** Products of block vertices lie in `maxSetB` (so the hypotheses below are consistent); on `maxSetB` the block marginals and block correlations obey `(s·a)², (t·b)², (sᵀCt)² ≤ 1` for block sign vectors, and `0 ≤ 1 + σa_i + τb_j + στC_ij` for `σ, τ = ±1`. |
| `maxSetB_blockA`, `maxSetB_blockB`, `sum_sgn_sq2`, `maxSetB_blockC` | M11′, Lemma 1 for block parts | **Faithful** (at least one block label on each side). Each block of `a` and of `b` has squared norm at most 1, with equality only at a vertex `±e_i` of that block; each block of `C` has squared Frobenius norm at most 1. |
| `pure_of_eqB`, `quad_blockw` | M11′, strictness for block parts | **Faithful.** A point of `maxSetB` at which every block of `a`, of `b` and of `C` has norm 1 is a product of block vertices. A diagonal form constant on each block is `q₀₀x₀₀² + ∑_k α_k‖a_k‖² + ∑_l β_l‖b_l‖² + ∑_{k,l} γ_{kl}‖C_{kl}‖²_F`, with weights that may differ between blocks. |
| `m11_blocks` | M11′, assembled for block parts, with `Γ` as a hypothesis | **Faithful for products of cross-polytopes, with `Γ` as a hypothesis.** For any finite group `Γ` acting linearly whose image contains (i) a separating family of diagonal matrices (as in `diag_of_separating`) and (ii) for any two coordinates of the same block of either part, the permutation matrix of a coordinate permutation of that part sending one to the other, and any `S` with `pureSetB ⊆ S ⊆ maxSetB`: an element of `Γ` mapping `S` onto `S` maps the product states onto themselves. Exactly these two properties are used. (i) makes the averaged form diagonal. (ii) makes it constant within blocks; without (ii) the weights inside a block can differ, `q` then separates only the top-weight vertices, and this proof route fails. Coordinate swaps between blocks, swaps of a cube's coordinates (singleton blocks, where (ii) is vacuous) and the rest of the hyperoctahedral group are not used. |
| `pureSetB_span`, `m11_blocks_polytope`, `m11_blocks_polytope_flips` | Theorem M11′ for polytope composites of block parts | **Faithful for these parts; no hypothesis on the symmetry group** (`Aut(S)` is built and proved finite); the local-symmetry premise of M11′ stays, as the invariance assumptions below. Let `S` be the convex hull of a finite set with `pureSetB ⊆ S ⊆ maxSetB`. Assume it is invariant under ±1 diagonal maps separating the coordinates (`_flips`: under the local sign flips) and under the within-block coordinate permutations of (ii). Then every reversible map of `S` maps the product states onto the product states; `Aut(S)` is built and shown finite (the products of block vertices span), then `m11_blocks` applies. |
| `maxSet_eq_blocks`, `pureSet_eq_blocks`, `maxSetX_eq_blocks`, `pureSetX_eq_blocks`, `maxSetCX_eq_blocks`, `pureSetCX_eq_blocks` | instances | **Faithful.** Round 4's cube composite is the singleton-block case and its cross-polytope composite the one-block case (`m_A, m_B ≥ 1` for the pure sets). The mixed cube × cross-polytope composite `maxSetCX` / `pureSetCX`, written out directly, is the labelling `(id, fun _ => 0)`. |
| `m11_cube_cross_polytope` | Theorem M11′ for a polytope composite of a hypercube and a cross-polytope | **Faithful; no hypothesis on the symmetry group** (`Aut(S)` is built); the local-symmetry premise stays, as the invariance assumptions below. `pureSetCX ⊆ S ⊆ maxSetCX`, `S` the convex hull of a finite set, `m_A, m_B ≥ 1`. If `S` is invariant under the local sign flips of both parts and the coordinate swaps of the cross-polytope (none of the cube), every reversible map of `S` maps the product states onto the product states. |
| `maxSetB_convex`, `pureSetB_finite`, `blocks_hyps_consistent` | non-vacuity of the round 5 hypotheses | **Faithful.** `maxSetB` is convex and there are finitely many product states, so `S = conv(pureSetB)` is a polytope with `pureSetB ⊆ S ⊆ maxSetB`. Its invariance under the local symmetries is not stated in Lean. |

Lean round 5 add-on, finite Theorem O (namespace `GTAORnd.SelfRef.LR3.OnsetO`, file `OnsetO.lean`;
source: the stepback session note C12C §3.1 as corrected after its hostile review, not in the repo; appended after the hostile review of Lean round 5: the Lean spec with items (i)–(v) is now committed as `theory/onset-o-2026-11-26/C12C_LEAN_SPEC.md`, ledger row RC21).
KNOWN in substance: a one-variable Everett / KKT instance for a discrete convex error curve; no
novelty is claimed. Setting over ℚ: designs `k = 0..n`, error `f` nonincreasing and discrete convex,
`g w k = w f k + κ k` (`κ > 0`, `w ≥ 0`), cap `f k ≤ D` with strict feasibility `f n < D`; `xD` the
least design meeting the cap, `xw` the least minimizer of `g w`.

| Declaration | Note item | Label |
|---|---|---|
| `isMin_iff_local` | C12C, discrete convexity | **Faithful.** With nondecreasing steps on `0..n`, `k` minimizes on `0..n` iff its left step is `≤ 0` and its right step `≥ 0`. |
| `Setting.projection` | C12C (i) | **Faithful.** `max xw xD` meets the cap, is optimal under the cap, and is the least such design. |
| `Setting.onset_union` | C12C (ii) | **Faithful** (`n ≥ 1`). `0 < max xw xD ↔ κ < w(−Δ0) ∨ D < f 0`. |
| `Setting.supporting_iff`, `Setting.tie_at_wstar`, `Setting.wstar_one` | C12C (iii a, b) | **Faithful** (`xD ≥ 1`, `v ≥ 0`). `xD` minimizes `g v` iff `wstar = κ/(−Δ(xD−1)) ≤ v` and (`xD = n` or `v(−Δ xD) ≤ κ`); at `v = wstar`, `xD − 1` and `xD` tie, so `wstar` is the least supporting stake, not a stake at which `xD` is the least minimizer; at `xD = 1`, `wstar = κ/(−Δ0)`. Appended after the hostile review of Lean round 5: the other half of (iii b), that `xD` is the least minimizer for every `v` strictly between the bounds, is not formalized. |
| `Setting.kkt` | C12C (iii c, d) | **Faithful in the combined form.** For `xD ≥ 1`, `max xw xD` minimizes `g (max w wstar)`: the multiplier is `max 0 (wstar − w)`. The separate statement "`xD > xw'` implies `μ > 0`" is not stated. Appended after the hostile review of Lean round 5: (iii d), that `xw ≤ xD ≤ xw'` implies `wstar ≤ w`, is not formalized (it appears only inside the proof, for `xD ≤ xw`), and the greatest minimizer `xw'` is not defined in Lean. |
| `Setting.wstar_anti` | C12C (iv) | **Faithful.** A looser cap (`D ≤ D'`, same `f`, `κ`) meets no later and needs no larger supporting stake. |
| `Setting.zero_stake`, `example_values` | C12C (v), the spec's instance | **Faithful.** At `w = 0` the least optimum under the cap is 0 iff `f 0 ≤ D`; for `f = [4, 2, 1, 1/2]`, `κ = 1`, `D = 3/2`: `xD = 2`, `wstar = 1`, supporting stakes `[1, 2]`. |

Lean round 6, checks from the hostile review of Lean round 5 (namespace `GTAORnd.SelfRef.LR3.M11Blocks`,
file `M11BlocksChecks.lean`; written by the reviewer in scratch files and moved here under new names).

| Declaration | Note item | Label |
|---|---|---|
| `sep_necessary` | M11′, Schur step | **Faithful.** For `u ≠ v` and `d u · d v = 1`, `(diag d)ᵀ (E_uv + E_vu) diag d = E_uv + E_vu`: without a separating member, a diagonal family leaves a non-diagonal invariant form. Necessity for this step only, not for the conclusion of M11′. |
| `flipA_pureSetB`, `flipA_hull_pureSetB` | non-vacuity of `m11_blocks_polytope_flips` | **Faithful, partial.** Each A-side flip `diag(rowSign i)` maps `pureSetB` and `conv(pureSetB)` onto themselves, so `S = conv(pureSetB)` meets `hfA`. `hfB` (symmetric, on paper), the coordinate permutations and the hypotheses of `m11_blocks_polytope` are not stated in Lean. |

Lean round 6, Lemma R (namespace `GTAORnd.SelfRef.LR3.LemmaR`, file `LemmaR.lean`; source:
`theory/lemma-r-2026-11-26/LEMMA_R.md` §§1–3 with its §9 corrections, and `LEMMA_R_LEAN_SPEC.md`;
ledger RC20). **Proved-in-model; folklore-level; novelty not claimed.** Credit: the dual-functional
step is the Marcus–Moyls argument as used by Al-Safi and Richens 2015 (Lemma 4); the line argument is
the automorphism fact for the rook's graph (Harary 1958, cited, not read; corrected after the hostile review of Lean round 6: Harary 1958, DOI 10.2140/pjm.1958.8.743, gives the line group of K_{m,n}, and the full automorphism group of the rook's graph follows from Whitney's line-graph theorem, Whitney 1932, DOI 10.2307/2371086, Crossref-checked, cited, not read; `rook_aut` is proved directly, so no result depends on either paper; the adjacency argument is Al-Safi and Richens 2015 Lemma 2, stated there for effects in maximal composites, and the whole argument is folklore-level). Setting over a field `K`:
families `a : Fin m → K^dA`, `b : Fin n → K^dB` with S2 (`Indep3`: any set of at most three
members is linearly independent); product vectors `kr a b (i, j) = a_i b_jᵀ`.

| Declaration | Note item | Label |
|---|---|---|
| `dual_step` | D, the dual-functional step | **Faithful.** If the `v i` (`i ∈ s`) are independent and `∑ v_i ⊗ β_i = 0`, every `β_i = 0`. |
| `exists_dual` | D | **Faithful.** For an independent finite family and a member `i0`, some `f` has `f · v_i = [i = i0]` on the family. |
| `indep_of_rows`, `indep_of_cols` | D.1, D.2 | **Faithful** (cases of D). Product vectors on index pairs meeting at most three rows (columns), none holding all of them, are independent. |
| `lemmaD` | Lemma D | **Faithful, any dimensions.** Four distinct index pairs lying neither in one row nor in one column give independent product vectors. |
| `line_of_triangle`, `row_line`, `row_col`, `same_type`, `assemble` | R.2–R.4, rook's-graph steps | **Faithful.** Three distinct pairwise adjacent points of a grid lie in one line; for an injective map of index pairs preserving adjacency both ways (`RookAdj`: same row or same column), each row maps into one line, all rows map into lines of the same kind, and if rows map into rows the map is a product map. |
| `rook_aut` | rook's-graph automorphisms (Harary 1958 line group of K_{m,n} and Whitney 1932, cited; Al-Safi–Richens 2015 Lemma 2 for the adjacency argument; see the credit paragraph above) | **Faithful, slightly more general** (`m ≥ 1`, `n ≥ 2`, any target grid `Fin p × Fin q`). An injective map of index pairs preserving adjacency both ways is `(i, j) ↦ (α i, β j)` or `(i, j) ↦ (α j, β i)`. Pure combinatorics; no linear algebra. |
| `indep_small`, `kr_injective` | R, injectivity of `(i, j) ↦ a_i ⊗ b_j` | **Faithful.** Under S2 any at most three product vectors are independent; distinct index pairs give distinct product vectors. |
| `not_indep_row`, `not_indep_col`, `exists_line4` | R.1, four points of a line are dependent | **Faithful** (`dB ≤ 3`, resp. `dA ≤ 3`). Four product vectors in one row (column) are dependent; with `m, n ≥ 4` every adjacent pair lies in four points of its line. |
| `adj_of_map` | R.1, lines map into lines | **Faithful** (`m, n ≥ 4`, `dA, dB ≤ 3`). If a linear equivalence `T` of `Matrix (Fin dA) (Fin dB) K` sends `a_x ⊗ b_x` to the product vector of `f x`, then `f` maps adjacent index pairs to adjacent ones (Lemma D on the images against the dependence of the preimages). |
| `lemmaR` | Lemma R (`LEMMA_R_LEAN_SPEC.md` item 4; note §1–3 with §9) | **Faithful in the abstract form.** For `a : Fin m → K^dA`, `b : Fin n → K^dB` with S2, `m, n ≥ 4`, `dA, dB ≤ 3`, every linear equivalence `T` with `T '' P = P` (`P` the set of product vectors) permutes `P` by a bijection `f` of index pairs with `f (i, j) = (α i, β j)` for all pairs, or `f (i, j) = (α j, β i)`. |
| `factors_bijective`, `lemmaR_perm` | spec item 4, σ and τ permutations, m = n (added after the hostile review of Lean round 6, finding L1) | **Faithful.** In `lemmaR`'s conclusion the factors `α`, `β` are bijections; in the swap case also `m = n`. |
| `sqV_indep3`, `square_lemmaR`, `square_transpose_preserves` (`LemmaRNonVac.lean`, from the reviewer's scratch, finding M3) | non-vacuity of `lemmaR` | **Faithful, one polygon over ℚ.** S2 holds for the square's vertices (1, ±1, 0), (1, 0, ±1); `lemmaR` applies to them; the transpose, a map other than the identity, meets `T '' P = P`. Regular n-gons with n ≠ 4 need ℝ; S2 for a general convex polygon (no three vertices collinear) is on paper, and S2 needs no regularity. |

Not covered by Lean round 6: the corollary that `T` itself is `g_A ⊗ g_B` or `(g_A ⊗ g_B) ∘ swap` as a linear map (spec item 5); S2 for the vertex vectors of polygons (the instance; on paper in the note for any convex polygon, no regularity needed; in Lean only for the square, `LemmaRNonVac.lean`); the combination with RC15 (reversible maps of locally symmetric composites); parts other than two polygons. The S2 hypothesis forces `dA, dB ≥ 3`, so with `dA, dB ≤ 3` the dimensions are exactly 3, as for polygons. Wording after the hostile review of Lean round 6: read "dimensions at most 3" as dimension 3 (polygon parts); bit and trit parts are where Lemma R fails and are not covered.

**Scope notes after the hostile review of Lean round 4 (26 November 2026; appended, no theorem
renamed).** "No group hypothesis" in the `m11_cube_polytope`, `m11_cross_polytope` row means no
hypothesis on the symmetry group: `Aut(S)` is built and proved finite. The local-symmetry premise of
M11′ stays, as invariance of `S` under the local sign flips (and, for cross-polytopes, the coordinate
swaps). That row's "not covered: composites not invariant under the full local hyperoctahedral group"
understates the cube version, which needs only invariance under the sign flips; round 5 below
(`m11_blocks_polytope`) needs only a separating family of `±1` diagonal symmetries and transitivity
within blocks. The 9-gon comparison `nona_beats_disk` is against 4-tick paths through pure states in
the disk only; a 4-tick disk path through mixed states costs 0.25, less than the 9-gon bound.

Not covered by round 5: 2-level centrally symmetric parts that are not products of cross-polytopes
(free sums such as cube ⊕ cube, the dual of octahedron × octahedron, and the other Hanner and non-Hanner
2-level parts); composites with no separating diagonal symmetries or without within-block
transitivity; non-polyhedral `S`.

**Scope notes on earlier names (hostile review of the Lean layer, 26 November 2026).** No locked
or committed theorem is renamed or edited; these lines give each one's actual content.
`disk_strictly_cheaper` shows only that the ring's Σ is positive (`lam*0 < lam*ringSigma`); the
disk's 0 is the definition NA4, not derived. `R78.ball_record_bound` is the triangle inequality
`‖Rᵏp − p‖ ≤ 2‖p‖` for an isometry; the content is the model. `SelfRefRun.no_zero_drift_while_recording`
is a tautology (it uses no axioms) and is elementary; the S8 conclusion is modelling, not Lean.
`R78.odd_ball_SFP` at m = 0 is SFP of the trivial group (see `SO1_trivial`), and the group choice
carries weight (see `ball_O_not_SFP`); the `SFP` definition has no transitivity hypothesis.
`R78.disk_exceeds_ball` compares the ball under a static axis-angle error δ with the disk under a
per-step rate error δ: the same symbol names two different errors, so "the ball beats the disk"
holds only under that identification. `SelfRef.liar_half` and `SelfRefRun.liar_half` are the same
one-line fact in two namespaces; `Composition.P2_entries` is four numeric facts; `SelfRefRun.perm_periodic`
is the existence of `orderOf`. Theorem count without padding: of the 253 names in
`scripts/RndAxioms.lean`, 248 remain after dropping the duplicate `SelfRefRun.liar_half`,
`Composition.P2_entries`, and the Lean round 3 restatements `local_map_tmul`, `swap_tmul` and the
numeric `le4_attained`. Raw counts are not a measure of depth: the load-bearing steps (NA1, the
general maximal-torus criterion, the Jordan-class classification, Piron, Solèr, Baer, the tensor-product block of the Schur step for parts other than products of cross-polytopes (Lean round 5) and the
Löwner step of M11, M12, purification and the cost-selection step) are not in Lean.

**Scope notes after the hostile review of Lean round 3 (26 November 2026; appended, no theorem
renamed).** `classical_no_purification` shows only that classical theory lacks purification; it does
not show that purification is independent of the other premises (classical theory fails U), so the
clause "is not implied by the other premises" in its row is withdrawn. `orthomodular_of_atomistic`
assumes finitely many atoms (a finite lattice), not only finite height, and its orthocomplement is an
abstract antitone involution; identifying it with perfect distinguishability on a GPT face lattice is
a premise. The `SFPCriterion.lean` docstring's "the cases the survivor table uses" covers SO(n) on
balls, complex QM and real QM only; quaternionic QM, octonionic d = 3, even balls under any
transitive group, G₂ on B⁷ and the C1 orbitope are not in Lean. `L5_perfect` takes closedness of the
achievable set as a hypothesis; its docstring's remark that this holds for compact effect sets is
true of finite-dimensional GPTs but is not provable in `CopyModel`, which has no topology. The
`Jdial_*_global` results hold only at the tuned weight, `ρ = 1/(2cos(β/2))`, `0 < β ≤ π/2`.
`hept_beats_disk` is T = 3 only, for one fixed 7-gon path (cost bounded by `3λ²`, not computed), disk
paths through pure states, the disk partner fixed to `p π` and unit price per squared distance.
`le4_attained` is the all-reads value at `β = (½, ½, ½)`, a point outside `le4_bound`'s hypothesis,
not attainment of the 2/3 bound; the name misleads. `cnot_mixed_correlated` defines the state
directly; the CNOT map is not formalized. `final_assembly` assumes only `T '' E = E` (its docstring
says bijection) and is an elementary set lemma: it takes the invariance of q and the strict
separation of product pure states as hypotheses, and the `M11Prime.lean` steps are not chained; the
separation is derived, and the steps chained, only in `M11Cube.lean` for hypercube and
cross-polytope parts and in `M11Blocks.lean` for products of cross-polytopes. Depth of
the count: besides the five dropped above, about twelve more names are one-line instances,
restatements or Mathlib wrappers: `unitary_fixes_ray`, `qubit_O3_not_SFP`, `reversible_preserves_pure`,
`final_assembly`, `finite_divring_comm` (`littleWedderburn`), `chevalley_nonzero_zero` (Mathlib's
Chevalley–Warning), `rho_60`, `Jdial_60_global`, `SO1_trivial`, `sphere_one_two_points`,
`moment_trace`, and the second conjunct of `qubit_bound_tight`. So the 187 names are not a measure
of depth.

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
  GTAO/MemoryRule.lean      # memory hold rule, T*, band b*; CT12 minimizer; CT17 (ii)
  GTAO/LocalShared.lean     # D5 crossing; switch iff ℓ > 0 and k_S < N k_L
  GTAO/Equipartition.lean   # E_π[J] − J* = d/(pβ); d/(2β) for PD quadratics
  GTAO/DriftSelection.lean  # DS1 Lyapunov identity, including d/(2β)(1+D/D_m)
  GTAO/HullWalk.lean        # hull increment test = leftmost argmin, any ε
  GTAO/N60Exact.lean        # L1: from-0 count = argmin for all R ⇔ convex
  GTAO/BandCounterexample.lean  # W=(0,1,0), μ=(2,1,1): E=(1,2/3,0)
  GTAO/BandMonge.lean       # Lemmas M, Z, X; Theorem B (finite cells, 2E_{k+1}≤E_k+E_{k+2}); Z needs W≥0
  GTAO/Coadaptation.lean    # CA1 (finite state), CA1a
  GTAO/DriftSpeed.lean      # DS2 lag, cost, half-window divergence
  GTAO/CoadaptationUnique.lean  # CA1 uniqueness (max-ratio + uniformization)
  GTAO/CoadaptationExcess.lean  # CA1b / CA1c (U2)
  GTAO/CoadaptationDrift.lean   # CA7 (U11): potential excess and regret counterexample
  GTAO/Cauchy.lean          # Lemmas C, P, C on the nonnegative integers, M
  GTAO/Representation.lean  # R1 packaging and the affine block
  GTAO/Obstruction.lean     # R2: Kelly and the Lundberg interval comparison
  GTAO/ContinuousA6.lean    # probability-measure klDiv, finite partitions, GYDSup
  GTAO/HeatFloor.lean       # two-state heat floor, T59
  GTAO/FiniteFloor.lean     # finite-alphabet learning rate, T60
  GTAO/FiniteFloorBounds.lean  # connectivity, class indicator, 3-cycle
  GTAO/RepairFloor.lean     # one-carrier repair comparison, T63
  GTAO/DiffusionHeat.lean   # EQ-heat step on any measure space, named hypotheses
  GTAO/FiniteFloorPairwise.lean  # log-sum, Jeffreys, pairwise L bound, T60
  GTAO/FiniteFloorPath.lean # Pinsker, walks, path bound, K = 1/(4r), T60
  GTAO/RepairTensor.lean    # product inequality on {0,1}^n, T63
  scripts/AxiomAudit.lean   # every GTAO declaration uses only standard axioms
```

Build artifacts under `.lake/` are gitignored.

## MEMORY-RULE: hold rule, re-check interval, band, and CT17 (ii)

Declarations in `GTAO/MemoryRule.lean` (27 November 2026). They check the
rules in `applications/GROK_BOT_MEMORY_2026-11-23.md` §4–§5 and the
externality half of CT17 (`THEORY.md:384`; `theory/MATH_ATTACK.md:273`),
which the public reply
[2126422798096646198](https://x.com/i/status/2126422798096646198) calls proved
in models.  The per-item cost is written with a drift weight `a` and a drop
loss `L`, `h (c + k/T + aσ²T/6) + (1 − h) L`, and every theorem in general `a`
holds for any `a > 0`.

**Units miss M45 (`NOTES/MISSES-LEDGER.md`).**  As printed on 23 November,
§4 used `a = w`.  Under §4's own definitions (`w` the stake when the item is
needed, `p` the need rate) that reading is dimensionally inconsistent, and no
consistent reading keeps it: the drift weight is forced to `a = w p / g²`,
where `g` is the gap at which a held item is as costly as a dropped one
(independent review, `reviews/pr301_2026-11-27/UNITS_REVIEW.md` §1–§2).  So the
need rate belongs inside the root of the hold threshold, in `T*` and in the
band (`fixed_hold_rule`); the printed worked example reverses
(`printed_example_flips`: hold, not drop); and the public reply's keep and
band lines are wrong as stated.  The reply's role-bot line (a bot that counts
a share of the loss re-checks at the square root of that share of the right
rate) holds under either reading, assuming the bot and the whole have the
same check cost and drift (`part_rate_ratio`).  `doc_hold_rule` and
`doc_example` check the printed `a = w` text, not the corrected rule; the
application page is corrected in the same PR (`corrected_example` checks its
new example).

`T` here is the barrier rule's *mean* interval between re-checks
(GROK_BOT_MEMORY §5), not a fixed clock: the form `k/T + aσ²T/6` is valid only
in that parametrization (the fixed clock is `k/T + aσ²T/2`).  Range: the
quadratic loss holds only while the band stays inside the gap at which the item
is useless, `b* ≤ g`, i.e. `w p ≥ 6kσ²/g²`; past that the formulas are an
upper-bound guide only.  This sits beside the Brownian and correlation-time
caveats of GROK_BOT_MEMORY §5.

Independent review of head `43c4c81acb0417512dfa30aba0c5b2c7c17818d5`:
`reviews/pr301_2026-11-27/REVIEW301.md` (no Lean blockers; blocker B1 was the
text of M45, this section and the MEM-RULE row).  The reviewer rebuilt in a
separate tree (`/tmp/gtao-lean2`) and got the same AxiomAudit count, 2333, as
`AUDIT.json` records for `/tmp/gtao-lean`.

| Declaration | Source sentence | Label |
|---|---|---|
| `held_min` | GROK_BOT_MEMORY:44, 55 | **Faithful.** For `k, a, σ² > 0`, `c + k/T + aσ²T/6` (with `T` the barrier's mean interval) has the unique minimizer `T* = √(6k/(aσ²))` on `T > 0`, with minimum `c + 2√(kaσ²/6)`. Built on `LayerLifetime.layer_lifetime`. |
| `hold_strictly_better_iff`, `drop_optimal_iff`, `joint_min`, `doc_hold_rule` | GROK_BOT_MEMORY:54 | **Faithful.** Some held interval is strictly cheaper than dropping iff `L > c + 2√(kaσ²/6)`; dropping is optimal iff `L ≤` that value (at equality both are optimal, so "hold only if" is exact and "hold iff" needs the strict sign); the joint minimum over the hold bit and `T` is `min(c + 2√(kaσ²/6), L)`. `doc_hold_rule` is the printed `a = w`, `L = w p` reading, which M45 records as dimensionally inconsistent: Faithful to the printed text only. |
| `doc_example` | GROK_BOT_MEMORY:57 as printed on 23 Nov | **Faithful to the printed text** in the `a = w` reading, which M45 records as dimensionally inconsistent. At `c = 1`, `w = 10`, `p = 0.2`, `k = 0.5`, `σ² = 1`: `w p = 2 > c`, `2.82 < c + 2√(kwσ²/6) < 2.83`, and no held interval beats dropping. |
| `fixed_hold_rule` | GROK_BOT_MEMORY:44–55 after M45 | **Faithful.** With `a = w p / g²`: holding strictly beats dropping iff `w p > c + 2√(k w p σ²/(6g²))`; `T* = √(6kg²/(wpσ²))`; `b* = (6kσ²g²/(wp))^{1/4}`. |
| `printed_example_flips` | GROK_BOT_MEMORY:57 as printed, in the consistent reading | **Faithful.** At `c = 1`, `w = 10`, `p = 0.2`, `k = 0.5`, `σ² = 1`, `g = 1`: `1.81 < c + 2√(kwpσ²/6) < 1.82 < wp = 2`, so holding wins; the free band exceeds `g`, and the capped band `b = g` already costs `11/6 < 2`. |
| `corrected_example` | GROK_BOT_MEMORY:57 after M45 | **Faithful.** At `c = 2.5`, `w = 15`, `p = 0.2`, `k = 0.4`, `σ² = 1`, `g = 1`: `wp = 3 > c`, `3.39 < c + 2√(kwpσ²/6) < 3.40`, no held interval beats dropping, and `0.94 < b*/g < 0.95`, inside the quadratic range. |
| `band_rule`, `band_sq` | GROK_BOT_MEMORY:69 | **WEAKER.** The algebraic part only: `b* = (6kσ²/a)^{1/4} > 0`, `b*²/σ² = T*`, the two cost terms `kσ²/b*²` and `a b*²/6` both equal `√(kaσ²/6)`, and `b*` is the unique positive minimizer of `kσ²/b² + a b²/6`. That a Brownian gap reset at `±b` has mean exit time `b²/σ²` and time-average square gap `b²/6`, and that a barrier policy is optimal among all re-check policies (Dixit 1991; Chalkley 1997 at zero discount), are assumptions, not declarations. |
| `occupation_integrals`, `barrier_cost_from_occupation` | GROK_BOT_MEMORY:69 (the coefficient 6) | **WEAKER.** Given the assumed occupation density `(b − |x|)/σ²` of Brownian motion from `0` absorbed at `±b`, the integrals are computed: `∫_{−b}^{b} (b − |x|) dx = b²` and `∫_{−b}^{b} (b − |x|) x² dx = b⁴/6`, so the mean exit time is `b²/σ²`, the mean square gap is `b²/6`, and `k/M + a·b²/6` is `LayerLifetime.cost (1/6)` at `T = b²/σ²`. The density is an input. |
| `barrier_cheaper_than_fixed` | GROK_BOT_MEMORY:70 | **Faithful** to the comparison of the two minimized refresh costs: `2√(kaσ²/6) < √(2kaσ²)` (the fixed-clock value is `LayerLifetime.fixed_period_lifetime`). |
| `part_rate_ratio` | MATH_ATTACK:273 in the memory model; the reply's "√(its loss / total loss)" | **Faithful** in the memory model, for any drift weight (so under either reading of M45): if the whole's drift weight is `Λ u` and a part counts `Λᵢ u`, with the **same check cost `k` and drift `σ²`** for both, the part's mean re-check rate `1/T*` is `√(Λᵢ/Λ)` times the whole's, and strictly lower when `Λᵢ < Λ`. It applies to items the part still holds; the part's own hold threshold is also stricter, so it may drop items the whole would keep. |
| `ct12Cost`, `ct12Tstar`, `ct12_min`, `bern`, `ct12Cost_scaled`, `ct12Tstar_pow` | THEORY.md:87 (CT12's cost) | **Faithful** to the minimizer: for `α > 1`, `c, w, q > 0`, `c/T + wqT^{α−1}/α` has the unique minimizer `T* = (αc/((α−1)wq))^{1/α}` on `T > 0` (real Bernoulli inequality). CT12's error-sensitivity remark (a 2× input error costs about 6%) is not a declaration. |
| `ct17_part_rate`, `ct17_alpha_two` | THEORY.md:384, CT17 (ii) | **Faithful** within CT12's cost: a part that sets its interval with stake `Λᵢ` instead of `Λ` reads at `(Λᵢ/Λ)^{1/α}` of the whole's optimal rate; at `α = 2` that factor is `√(Λᵢ/Λ)`. CT17 (i) (the shared clock and Cauchy–Schwarz) is not formalized. |
| `watch_sq_prop` | MATH_ATTACK:273 (`f*² ∝ Λ ∂h/∂τ`) | **WEAKER.** Takes `f*² = κΛ` with `κ` fixed as a hypothesis (row 7c's proportionality, `∂h/∂τ` held fixed) and concludes `fᵢ = √(Λᵢ/Λ) f`. Row 7c itself is not formalized. |
