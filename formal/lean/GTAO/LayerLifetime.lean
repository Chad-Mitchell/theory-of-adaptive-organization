/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lean 4 formalization of the layer-lifetime rule (CORE §3,
`theory/LAYER_LIFETIME_2026-11-21.md` §2), for OPEN_WORK T19.
-/
module

public import Mathlib.Analysis.SpecialFunctions.Pow.Real
public import Mathlib.Analysis.SpecialFunctions.Sqrt
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.FieldSimp
public import Mathlib.Tactic.Positivity

/-!
# Layer lifetime `T* = √(6k/(wσ²))`

The repository's zero-discount average cost of a lumpy layer that is reset
every `T` (in expectation) at lump cost `k`, with stake `w` on the squared
gap and Brownian drift of variance rate `σ²`, is

`C(T) = k / T + c · w σ² · T`,

with `c = 1/6` for the optimal barrier (Dixit 1991; exact at zero discount,
Chalkley 1997) and `c = 1/2` for a fixed-period refresh.  The stochastic
derivation of this expression (mean exit time `b²/σ²`, time-average square
gap `b²/6`) is **KNOWN** and is *assumed* here, not formalized.  What is
machine-checked is the optimization: on `T > 0`, `C` has the unique
minimizer `T* = √(k/(c w σ²))`, which is `√(6k/(wσ²))` at `c = 1/6`, and
the minimum is `2√(c k w σ²)`.
-/

@[expose] public section

namespace LayerLifetime

open Real

/-- Zero-discount average cost of a lumpy layer with mean reset interval `T`:
`k / T + c · w · σ² · T` (`s` stands for `σ²`). -/
noncomputable def cost (c k w s T : ℝ) : ℝ := k / T + c * w * s * T

/-- The generic minimizer `√(k / (c w σ²))`. -/
noncomputable def Tstar (c k w s : ℝ) : ℝ := √(k / (c * w * s))

/-- AM–GM core: for `a, k > 0` and `T > 0`,
`k / T + a T - 2√(k a) = (√a T - √k)² / T ≥ 0`. -/
lemma amgm_identity {a k T : ℝ} (ha : 0 ≤ a) (hk : 0 ≤ k) (hT : 0 < T) :
    k / T + a * T - 2 * √(k * a) = (√a * T - √k) ^ 2 / T := by
  have h1 : √a ^ 2 = a := sq_sqrt ha
  have h2 : √k ^ 2 = k := sq_sqrt hk
  have h3 : √(k * a) = √k * √a := sqrt_mul hk a
  rw [h3]
  field_simp
  nlinarith [h1, h2]

lemma cost_ge (c k w s : ℝ) {T : ℝ} (ha : 0 ≤ c * w * s) (hk : 0 ≤ k) (hT : 0 < T) :
    2 * √(k * (c * w * s)) ≤ cost c k w s T := by
  have := amgm_identity ha hk hT
  have hnn : 0 ≤ (√(c * w * s) * T - √k) ^ 2 / T := by positivity
  unfold cost
  linarith

lemma Tstar_pos {c k w s : ℝ} (ha : 0 < c * w * s) (hk : 0 < k) : 0 < Tstar c k w s := by
  unfold Tstar; positivity

lemma sqrt_a_mul_Tstar {c k w s : ℝ} (ha : 0 < c * w * s) :
    √(c * w * s) * Tstar c k w s = √k := by
  unfold Tstar
  rw [← sqrt_mul ha.le, mul_div_cancel₀ _ ha.ne']

/-- The minimum value: `C(T*) = 2√(c k w σ²)`. -/
theorem cost_Tstar {c k w s : ℝ} (ha : 0 < c * w * s) (hk : 0 < k) :
    cost c k w s (Tstar c k w s) = 2 * √(k * (c * w * s)) := by
  have hT := Tstar_pos ha hk
  have hid := amgm_identity ha.le hk.le hT
  rw [sqrt_a_mul_Tstar (k := k) ha, sub_self] at hid
  unfold cost
  simp at hid
  linarith

/-- `T*` minimizes the average cost over all `T > 0`. -/
theorem Tstar_isMin {c k w s : ℝ} (ha : 0 < c * w * s) (hk : 0 < k) {T : ℝ} (hT : 0 < T) :
    cost c k w s (Tstar c k w s) ≤ cost c k w s T := by
  rw [cost_Tstar ha hk]; exact cost_ge c k w s ha.le hk.le hT

/-- `T*` is the unique minimizer on `T > 0`. -/
theorem Tstar_unique {c k w s : ℝ} (ha : 0 < c * w * s) (hk : 0 < k) {T : ℝ} (hT : 0 < T)
    (hmin : cost c k w s T ≤ cost c k w s (Tstar c k w s)) : T = Tstar c k w s := by
  have hid := amgm_identity ha.le hk.le hT
  rw [cost_Tstar ha hk] at hmin
  have hle : (√(c * w * s) * T - √k) ^ 2 / T ≤ 0 := by unfold cost at hmin; linarith
  have hsq : (√(c * w * s) * T - √k) ^ 2 = 0 := by
    have h0 := (div_le_iff₀ hT).mp hle
    exact le_antisymm (by linarith) (sq_nonneg _)
  have hlin : √(c * w * s) * T = √k := by nlinarith [pow_eq_zero_iff (n := 2) (two_ne_zero) |>.mp hsq]
  have hpos : 0 < √(c * w * s) := sqrt_pos.mpr ha
  have := sqrt_a_mul_Tstar (k := k) ha
  exact mul_left_cancel₀ hpos.ne' (hlin.trans this.symm)

/-- **Layer lifetime (barrier, `c = 1/6`).**  On `T > 0` the zero-discount
average cost `k/T + wσ²T/6` is uniquely minimized at `T* = √(6k/(wσ²))`,
with minimum `2√(k w σ²/6)`. -/
theorem layer_lifetime {k w s : ℝ} (hk : 0 < k) (hw : 0 < w) (hs : 0 < s) :
    Tstar (1 / 6) k w s = √(6 * k / (w * s)) ∧
    (∀ T, 0 < T → cost (1 / 6) k w s (√(6 * k / (w * s))) ≤ cost (1 / 6) k w s T) ∧
    (∀ T, 0 < T → cost (1 / 6) k w s T ≤ cost (1 / 6) k w s (√(6 * k / (w * s))) →
      T = √(6 * k / (w * s))) ∧
    cost (1 / 6) k w s (√(6 * k / (w * s))) = 2 * √(k * w * s / 6) := by
  have ha : 0 < 1 / 6 * w * s := by positivity
  have hT : Tstar (1 / 6) k w s = √(6 * k / (w * s)) := by
    unfold Tstar; congr 1; field_simp
  refine ⟨hT, ?_, ?_, ?_⟩
  · intro T hT0; rw [← hT]; exact Tstar_isMin ha hk hT0
  · intro T hT0 h; rw [← hT] at h ⊢; exact Tstar_unique ha hk hT0 h
  · rw [← hT, cost_Tstar ha hk]; congr 2; ring

/-- **Fixed-period refresh (`c = 1/2`).**  `T*_fix = √(2k/(wσ²))`, minimum
`√(2 k w σ²)`. -/
theorem fixed_period_lifetime {k w s : ℝ} (hk : 0 < k) (hw : 0 < w) (hs : 0 < s) :
    Tstar (1 / 2) k w s = √(2 * k / (w * s)) ∧
    (∀ T, 0 < T → cost (1 / 2) k w s (√(2 * k / (w * s))) ≤ cost (1 / 2) k w s T) ∧
    cost (1 / 2) k w s (√(2 * k / (w * s))) = √(2 * k * w * s) := by
  have ha : 0 < 1 / 2 * w * s := by positivity
  have hT : Tstar (1 / 2) k w s = √(2 * k / (w * s)) := by
    unfold Tstar; congr 1; field_simp
  refine ⟨hT, ?_, ?_⟩
  · intro T hT0; rw [← hT]; exact Tstar_isMin ha hk hT0
  · rw [← hT, cost_Tstar ha hk]
    rw [show k * (1 / 2 * w * s) = (2 * k * w * s) / 4 by ring, sqrt_div' _ (by norm_num : (0:ℝ) ≤ 4),
      show (4 : ℝ) = 2 ^ 2 by norm_num, sqrt_sq (by norm_num : (0:ℝ) ≤ 2)]
    ring

/-- The barrier lifetime is `√3` times the fixed-period lifetime. -/
theorem barrier_eq_sqrt3_fixed (k w s : ℝ) :
    √(6 * k / (w * s)) = √3 * √(2 * k / (w * s)) := by
  rw [← sqrt_mul (by norm_num)]; congr 1; ring

/-- Square-root scaling in the re-forming cost: scaling `k` by `r > 0`
scales `T*` by `√r` (so a cost 100 times lower gives a lifetime 10 times
shorter). -/
theorem Tstar_scale_k {c k w s r : ℝ} (hr : 0 ≤ r) :
    Tstar c (r * k) w s = √r * Tstar c k w s := by
  unfold Tstar; rw [mul_div_assoc, sqrt_mul hr]

/-- The spacing rule in a specialized stack (equal stakes):
`T*_i / T*_j = √((k_i/k_j)·(σ_j²/σ_i²))`. -/
theorem lifetime_ratio {c ki kj w si sj : ℝ} (hc : 0 < c) (hw : 0 < w)
    (hkj : 0 < kj) (hsi : 0 < si) (hsj : 0 < sj) :
    Tstar c ki w si / Tstar c kj w sj = √((ki / kj) * (sj / si)) := by
  unfold Tstar
  rw [← sqrt_div' _ (by positivity : 0 ≤ kj / (c * w * sj))]
  congr 1
  field_simp

/-- **Barrier-band identities used in SA2 (`theory/SELECTION_AXIOMS.md`).**
With `b*² = √(6kσ²/w)` (i.e. `b*⁴ = 6kσ²/w`): the mean square-gap cost
`w b*²/6` and the amortized lumps `kσ²/b*²` both equal `√(kwσ²/6)`, and the
mean exit time `b*²/σ²` is `T* = √(6k/(wσ²))`. -/
theorem barrier_band_identities {k w s : ℝ} (hk : 0 < k) (hw : 0 < w) (hs : 0 < s) :
    w * √(6 * k * s / w) / 6 = √(k * w * s / 6) ∧
    k * s / √(6 * k * s / w) = √(k * w * s / 6) ∧
    √(6 * k * s / w) / s = √(6 * k / (w * s)) := by
  have hB : 0 < √(6 * k * s / w) := sqrt_pos.mpr (by positivity)
  have hsq : √(6 * k * s / w) ^ 2 = 6 * k * s / w := sq_sqrt (by positivity)
  have hC : 0 ≤ √(k * w * s / 6) := sqrt_nonneg _
  have hCsq : √(k * w * s / 6) ^ 2 = k * w * s / 6 := sq_sqrt (by positivity)
  have hT : 0 ≤ √(6 * k / (w * s)) := sqrt_nonneg _
  have hTsq : √(6 * k / (w * s)) ^ 2 = 6 * k / (w * s) := sq_sqrt (by positivity)
  have h1 : w * √(6 * k * s / w) / 6 = √(k * w * s / 6) := by
    have hl : 0 ≤ w * √(6 * k * s / w) / 6 := by positivity
    rw [← sq_eq_sq₀ hl hC, hCsq, div_pow, mul_pow, hsq]
    field_simp
  refine ⟨h1, ?_, ?_⟩
  · rw [← h1, div_eq_iff hB.ne']
    have : w * √(6 * k * s / w) / 6 * √(6 * k * s / w) = w * √(6 * k * s / w) ^ 2 / 6 := by ring
    rw [this, hsq]; field_simp
  · have hl : 0 ≤ √(6 * k * s / w) / s := by positivity
    rw [← sq_eq_sq₀ hl hT, hTsq, div_pow, hsq]
    field_simp

end LayerLifetime
