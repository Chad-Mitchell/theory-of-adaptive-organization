/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lean 4 formalization of the local-vs-shared condition (CORE §1 and §4,
`theory/LAYER_LIFETIME_2026-11-21.md` §5, D5), for OPEN_WORK T19.
-/
module

public import Mathlib.Analysis.SpecialFunctions.Pow.Real
public import Mathlib.Analysis.SpecialFunctions.Sqrt
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.FieldSimp
public import Mathlib.Tactic.Positivity

/-!
# Local vs shared: the D5 crossing

`N` units track a common Brownian driver with variance rate `s = σ²`, each
with stake `w`.  Each lumpy tracker, optimized, costs `e · √(k · W · s)` per
unit time, where `W` is the stake it serves and `e` is the excess-cost
coefficient (`e = √2` for a fixed-period refresh, `e = 2/√6` for the optimal
barrier; see `GTAO.LayerLifetime`).  The repository's costs are

* local:  `N · e · √(k_L · w · s)` (N trackers, each serving stake `w`),
* shared: `e · √(k_S · (N w) · s) + N · w · s · ℓ` (one tracker serving
  stake `N w`, plus the delay floor from latency `ℓ` on the shared
  observation only).

These cost expressions (in particular the delay floor `N w σ² ℓ`) are taken
from the repository as given; their stochastic derivation is not formalized.
Machine-checked here:

* `no_switch_without_delay`: at `ℓ = 0`, shared wins at some (equivalently
  every) `σ² > 0` iff `k_S < N k_L`;
* `shared_never_wins`: if `k_S ≥ N k_L` and `ℓ ≥ 0`, shared never wins;
* `crossing`: with `ℓ > 0` and `k_S < N k_L`, shared wins iff `σ² < σ²*`,
  with `σ²* = ((√(k_L w) - √(k_S w / N)) · e / (w ℓ))²`;
* `switch_iff`: a switch (shared wins at some drift and loses at another)
  exists iff `ℓ > 0` and `k_S < N k_L`;
* `equal_delay_no_switch`: the same delay floor on both sides cancels;
* `barrier_crossing_eq_fixed_div_three`: the barrier crossing is the
  fixed-period crossing divided by 3.
-/

@[expose] public section

namespace LocalShared

open Real

/-- Total cost of `N` local trackers. -/
noncomputable def localCost (e N kL w s : ℝ) : ℝ := N * e * √(kL * w * s)

/-- Cost of one shared tracker with latency `ℓ` on the shared observation. -/
noncomputable def sharedCost (e N kS w ℓ s : ℝ) : ℝ := e * √(kS * (N * w) * s) + N * w * s * ℓ

/-- The crossing variance rate, in the repository's form. -/
noncomputable def sigma2Star (e N kL kS w ℓ : ℝ) : ℝ :=
  ((√(kL * w) - √(kS * w / N)) * e / (w * ℓ)) ^ 2

section

variable {e N kL kS w ℓ s : ℝ}

lemma localCost_eq (hkL : 0 ≤ kL) (hw : 0 ≤ w) :
    localCost e N kL w s = N * e * √(kL * w) * √s := by
  unfold localCost; rw [sqrt_mul (by positivity)]; ring

lemma sharedCost_eq (hkS : 0 ≤ kS) (hN : 0 ≤ N) (hw : 0 ≤ w) (hs : 0 ≤ s) :
    sharedCost e N kS w ℓ s = e * √(kS * (N * w)) * √s + N * w * ℓ * √s ^ 2 := by
  unfold sharedCost; rw [sqrt_mul (by positivity), sq_sqrt hs]; ring

/-- The key comparison of the two amortized constants:
`e √(k_S N w) < N e √(k_L w)` iff `k_S < N k_L`. -/
lemma const_lt_iff (he : 0 < e) (hN : 0 < N) (hw : 0 < w) (hkS : 0 ≤ kS) :
    e * √(kS * (N * w)) < N * e * √(kL * w) ↔ kS < N * kL := by
  have hNs : N * e * √(kL * w) = e * √(N ^ 2 * (kL * w)) := by
    rw [Real.sqrt_mul (sq_nonneg N) (kL * w), sqrt_sq hN.le]; ring
  rw [hNs, mul_lt_mul_iff_right₀ he, sqrt_lt_sqrt_iff (by positivity)]
  constructor
  · intro h; nlinarith [mul_pos hN hw]
  · intro h; nlinarith [mul_pos hN hw]

/-- The crossing in terms of `√σ²`: `(A - B)/(N w ℓ)` equals the repository's
`(√(k_L w) - √(k_S w/N)) e / (w ℓ)`. -/
lemma crossing_root_eq (hN : 0 < N) (hw : 0 < w) (hℓ : 0 < ℓ) :
    (N * e * √(kL * w) - e * √(kS * (N * w))) / (N * w * ℓ) =
      (√(kL * w) - √(kS * w / N)) * e / (w * ℓ) := by
  have h1 : √(kS * (N * w)) = N * √(kS * w / N) := by
    rw [show kS * (N * w) = N ^ 2 * (kS * w / N) by field_simp]
    rw [sqrt_mul (by positivity), sqrt_sq hN.le]
  rw [h1]
  field_simp

/-- **No delay, no switch.**  With `ℓ = 0`, at any `σ² > 0`, shared is
cheaper iff `k_S < N k_L`; the answer does not depend on the drift. -/
theorem no_switch_without_delay (he : 0 < e) (hN : 0 < N) (hw : 0 < w) (hkS : 0 ≤ kS)
    (hkL : 0 ≤ kL) (hs : 0 < s) :
    sharedCost e N kS w 0 s < localCost e N kL w s ↔ kS < N * kL := by
  rw [sharedCost_eq hkS hN.le hw.le hs.le, localCost_eq hkL hw.le, ← const_lt_iff he hN hw hkS]
  have hu : 0 < √s := sqrt_pos.mpr hs
  simp only [mul_zero, zero_mul, add_zero]
  exact mul_lt_mul_iff_left₀ hu

/-- **If `k_S ≥ N k_L`, shared never wins** (at any drift, with `ℓ ≥ 0`). -/
theorem shared_never_wins (he : 0 < e) (hN : 0 < N) (hw : 0 < w) (hkS : 0 ≤ kS)
    (hkL : 0 ≤ kL) (hℓ : 0 ≤ ℓ) (hk : N * kL ≤ kS) (hs : 0 ≤ s) :
    localCost e N kL w s ≤ sharedCost e N kS w ℓ s := by
  rw [sharedCost_eq hkS hN.le hw.le hs, localCost_eq hkL hw.le]
  have hc : N * e * √(kL * w) ≤ e * √(kS * (N * w)) :=
    not_lt.mp (fun h => absurd ((const_lt_iff he hN hw hkS).mp h) (not_lt.mpr hk))
  have hu : 0 ≤ √s := sqrt_nonneg s
  have : 0 ≤ N * w * ℓ * √s ^ 2 := by positivity
  nlinarith [mul_le_mul_of_nonneg_right hc hu]

/-- **The crossing.**  With latency `ℓ > 0` on the shared observation only
and `k_S < N k_L`, shared is cheaper exactly below `σ²*`:
for `σ² > 0`, `shared < local ↔ σ² < σ²*`. -/
theorem crossing (he : 0 < e) (hN : 0 < N) (hw : 0 < w) (hkS : 0 ≤ kS) (hkL : 0 ≤ kL)
    (hℓ : 0 < ℓ) (hk : kS < N * kL) (hs : 0 < s) :
    sharedCost e N kS w ℓ s < localCost e N kL w s ↔ s < sigma2Star e N kL kS w ℓ := by
  rw [sharedCost_eq hkS hN.le hw.le hs.le, localCost_eq hkL hw.le]
  set A := N * e * √(kL * w)
  set B := e * √(kS * (N * w))
  have hAB : B < A := (const_lt_iff he hN hw hkS).mpr hk
  have hu : 0 < √s := sqrt_pos.mpr hs
  have hc : 0 < N * w * ℓ := by positivity
  have hstar : sigma2Star e N kL kS w ℓ = ((A - B) / (N * w * ℓ)) ^ 2 := by
    unfold sigma2Star; rw [crossing_root_eq hN hw hℓ]
  have hr : 0 < (A - B) / (N * w * ℓ) := div_pos (by linarith) hc
  rw [hstar]
  conv_rhs => rw [← sq_sqrt hs.le]
  rw [sq_lt_sq₀ hu.le hr.le, lt_div_iff₀ hc]
  constructor
  · intro h; nlinarith
  · intro h; nlinarith

/-- **A drift switch exists iff the delay is on the shared channel and
`k_S < N k_L`.**  Here "switch" means shared is strictly cheaper at some
`σ² > 0` and not cheaper at some other `σ² > 0`.  (`ℓ ≥ 0` throughout.) -/
theorem switch_iff (he : 0 < e) (hN : 0 < N) (hw : 0 < w) (hkS : 0 ≤ kS) (hkL : 0 ≤ kL)
    (hℓ : 0 ≤ ℓ) :
    ((∃ s₁, 0 < s₁ ∧ sharedCost e N kS w ℓ s₁ < localCost e N kL w s₁) ∧
      (∃ s₂, 0 < s₂ ∧ localCost e N kL w s₂ ≤ sharedCost e N kS w ℓ s₂)) ↔
      (0 < ℓ ∧ kS < N * kL) := by
  constructor
  · rintro ⟨⟨s₁, hs₁, h₁⟩, ⟨s₂, hs₂, h₂⟩⟩
    have hk : kS < N * kL := by
      by_contra hk
      exact absurd h₁ (not_lt.mpr (shared_never_wins he hN hw hkS hkL hℓ (not_lt.mp hk) hs₁.le))
    refine ⟨?_, hk⟩
    rcases hℓ.lt_or_eq with h | h
    · exact h
    · subst h
      exact absurd ((no_switch_without_delay he hN hw hkS hkL hs₂).mpr hk) (not_lt.mpr h₂)
  · rintro ⟨hℓ', hk⟩
    have hpos : 0 < sigma2Star e N kL kS w ℓ := by
      unfold sigma2Star
      have hAB := (const_lt_iff he hN hw hkS).mpr hk
      rw [← crossing_root_eq hN hw hℓ']
      have : 0 < (N * e * √(kL * w) - e * √(kS * (N * w))) / (N * w * ℓ) :=
        div_pos (by linarith) (by positivity)
      positivity
    refine ⟨⟨sigma2Star e N kL kS w ℓ / 2, by positivity, ?_⟩,
      ⟨sigma2Star e N kL kS w ℓ, hpos, ?_⟩⟩
    · exact (crossing he hN hw hkS hkL hℓ' hk (by positivity)).mpr (by linarith)
    · exact not_lt.mp (fun h => lt_irrefl _ ((crossing he hN hw hkS hkL hℓ' hk hpos).mp h))

/-- **Equal delay on both sides cancels.**  If local updates carry the same
observation delay, both costs get the floor `N w σ² ℓ`, and the comparison
is the no-delay one at every drift: no switch. -/
theorem equal_delay_no_switch (he : 0 < e) (hN : 0 < N) (hw : 0 < w) (hkS : 0 ≤ kS)
    (hkL : 0 ≤ kL) (hs : 0 < s) :
    sharedCost e N kS w ℓ s < localCost e N kL w s + N * w * s * ℓ ↔ kS < N * kL := by
  rw [← no_switch_without_delay he hN hw hkS hkL hs]
  unfold sharedCost; constructor <;> intro h <;> linarith

end

/-- **Barrier crossing = fixed-period crossing / 3.**  With the barrier
excess coefficient `2/√6` in place of the fixed-period `√2`, `σ²*` is
divided by exactly 3. -/
theorem barrier_crossing_eq_fixed_div_three (N kL kS w ℓ : ℝ) :
    sigma2Star (2 / √6) N kL kS w ℓ = sigma2Star (√2) N kL kS w ℓ / 3 := by
  have hgen : ∀ e, sigma2Star e N kL kS w ℓ =
      e ^ 2 * ((√(kL * w) - √(kS * w / N)) / (w * ℓ)) ^ 2 := by
    intro e; unfold sigma2Star; ring
  have h6 : (2 / √6) ^ 2 = 2 / 3 := by
    rw [div_pow, sq_sqrt (by norm_num)]; norm_num
  have h2 : √2 ^ 2 = 2 := sq_sqrt (by norm_num)
  rw [hgen, hgen, h6, h2]
  ring

end LocalShared
