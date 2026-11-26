/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost: `theory/RECORD_COST_CHAIN_2026-11-25.md` step S10 (the cost dial: global
minimum, open in `CostDial.lean`). Lean round 3 of the side session; written in a private Lake
project (library `GTAORnd`, same Lean and Mathlib pins) and moved here with only this header
and the module lines changed.
-/
module

public import Mathlib
public import GTAO.Rnd.SelfRef.CostDial

@[expose] public section

/-!
# Cost dial: the midpoint is the global minimizer for β ≤ π/2

`Jdial qk wRD β α = qκ(1 − cos(β − α))/2 + wRD·sin²α` (`CostDial.lean`). At
`ρ = 2wRD/qκ = 1/(2cos(β/2))` the midpoint `α = β/2` is stationary (`Jdial_midpoint`). Here:
* `Jdial_midpoint_global`: for `0 < β ≤ π/2` it is a global minimizer over all real `α`;
* `Jdial_midpoint_unique`: for `0 < β < π/2` it is the unique minimizer modulo `2π`;
* `Jdial_60_global`: the note's case `β = 60°`, `ρ = 1/√3`: `α = 30°` is the unique global
  minimizer modulo `2π`.
Key identity, with `u = α − β/2`, `c = cos(β/2)`, `s = sin(β/2)`:
`(J(α) − J(β/2))·(2/qκ) = (1 − cos u)(c − s·sin u) + sin²u·(c² − s²)/(2c)`.
For `β > π/2` the midpoint is not the global minimizer (numerically, from β ≈ 1.61); that
converse is not formalized.
-/

namespace GTAORnd.SelfRef.LR3

open Real GTAORnd.SelfRef

/-- the key identity -/
lemma dial_diff (qk β u : ℝ) (hc : cos (β / 2) ≠ 0) :
    Jdial qk (qk / (4 * cos (β / 2))) β (β / 2 + u) - Jdial qk (qk / (4 * cos (β / 2))) β (β / 2)
      = qk / 2 * ((1 - cos u) * (cos (β / 2) - sin (β / 2) * sin u)
        + sin u ^ 2 * (cos (β / 2) ^ 2 - sin (β / 2) ^ 2) / (2 * cos (β / 2))) := by
  unfold Jdial
  have hb : β - (β / 2 + u) = β / 2 - u := by ring
  have hb2 : β - β / 2 = β / 2 := by ring
  rw [hb, hb2, cos_sub, sin_add]
  have h1 := sin_sq_add_cos_sq u
  have h2 := sin_sq_add_cos_sq (β / 2)
  field_simp
  linear_combination (4 * qk * sin (β / 2) ^ 2) * h1

/-- **Global minimum** (PROVED-IN-MODEL): for `qκ > 0`, `0 < β ≤ π/2` and
`wRD = qκ/(4 cos(β/2))` (that is `ρ = 1/(2cos(β/2))`), `J(β/2) ≤ J(α)` for every real `α`. -/
theorem Jdial_midpoint_global (qk β α : ℝ) (hq : 0 < qk) (hβ0 : 0 < β) (hβ : β ≤ π / 2) :
    Jdial qk (qk / (4 * cos (β / 2))) β (β / 2) ≤ Jdial qk (qk / (4 * cos (β / 2))) β α := by
  have hc : 0 < cos (β / 2) := cos_pos_of_mem_Ioo ⟨by linarith [pi_pos], by linarith⟩
  have hsc : sin (β / 2) ≤ cos (β / 2) := by
    rw [← cos_pi_div_two_sub]
    apply cos_le_cos_of_nonneg_of_le_pi <;> linarith [pi_pos]
  have hs0 : 0 ≤ sin (β / 2) := sin_nonneg_of_nonneg_of_le_pi (by linarith) (by linarith [pi_pos])
  have hd := dial_diff qk β (α - β / 2) hc.ne'
  rw [show β / 2 + (α - β / 2) = α by ring] at hd
  have h1 : 0 ≤ 1 - cos (α - β / 2) := by linarith [cos_le_one (α - β / 2)]
  have h2 : 0 ≤ cos (β / 2) - sin (β / 2) * sin (α - β / 2) := by
    nlinarith [sin_le_one (α - β / 2), neg_one_le_sin (α - β / 2)]
  have h3 : 0 ≤ sin (α - β / 2) ^ 2 * (cos (β / 2) ^ 2 - sin (β / 2) ^ 2) / (2 * cos (β / 2)) := by
    apply div_nonneg _ (by linarith)
    exact mul_nonneg (sq_nonneg _) (by nlinarith)
  have : 0 ≤ qk / 2 * ((1 - cos (α - β / 2)) * (cos (β / 2) - sin (β / 2) * sin (α - β / 2))
      + sin (α - β / 2) ^ 2 * (cos (β / 2) ^ 2 - sin (β / 2) ^ 2) / (2 * cos (β / 2))) := by
    apply mul_nonneg (by linarith); exact add_nonneg (mul_nonneg h1 h2) h3
  linarith

/-- **Uniqueness** (PROVED-IN-MODEL): for `0 < β < π/2` every global minimizer is `β/2 + 2πk`. -/
theorem Jdial_midpoint_unique (qk β α : ℝ) (hq : 0 < qk) (hβ0 : 0 < β) (hβ : β < π / 2)
    (hmin : Jdial qk (qk / (4 * cos (β / 2))) β α ≤ Jdial qk (qk / (4 * cos (β / 2))) β (β / 2)) :
    ∃ k : ℤ, α = β / 2 + k * (2 * π) := by
  have hc : 0 < cos (β / 2) := cos_pos_of_mem_Ioo ⟨by linarith [pi_pos], by linarith⟩
  have hsc : sin (β / 2) < cos (β / 2) := by
    rw [← cos_pi_div_two_sub]
    apply cos_lt_cos_of_nonneg_of_le_pi_div_two <;> linarith [pi_pos]
  have hs0 : 0 ≤ sin (β / 2) := sin_nonneg_of_nonneg_of_le_pi (by linarith) (by linarith [pi_pos])
  set u := α - β / 2
  have hd := dial_diff qk β u hc.ne'
  rw [show β / 2 + u = α by simp [u]] at hd
  have h1 : 0 ≤ 1 - cos u := by linarith [cos_le_one u]
  have h2 : 0 < cos (β / 2) - sin (β / 2) * sin u := by
    nlinarith [sin_le_one u, neg_one_le_sin u]
  have hk : 0 < cos (β / 2) ^ 2 - sin (β / 2) ^ 2 := by nlinarith
  have h3 : 0 ≤ sin u ^ 2 * (cos (β / 2) ^ 2 - sin (β / 2) ^ 2) / (2 * cos (β / 2)) :=
    div_nonneg (mul_nonneg (sq_nonneg _) hk.le) (by linarith)
  -- the bracket is ≤ 0, so both non-negative terms vanish
  have hbr : (1 - cos u) * (cos (β / 2) - sin (β / 2) * sin u)
      + sin u ^ 2 * (cos (β / 2) ^ 2 - sin (β / 2) ^ 2) / (2 * cos (β / 2)) ≤ 0 := by
    have : qk / 2 * ((1 - cos u) * (cos (β / 2) - sin (β / 2) * sin u)
      + sin u ^ 2 * (cos (β / 2) ^ 2 - sin (β / 2) ^ 2) / (2 * cos (β / 2))) ≤ 0 := by linarith
    by_contra hpos; push Not at hpos
    have := mul_pos (by linarith : 0 < qk / 2) hpos; linarith
  have hA : (1 - cos u) * (cos (β / 2) - sin (β / 2) * sin u) = 0 := by
    nlinarith [mul_nonneg h1 h2.le]
  have hcos : cos u = 1 := by
    rcases mul_eq_zero.mp hA with h | h
    · linarith
    · linarith
  obtain ⟨k, hk⟩ := (cos_eq_one_iff u).mp hcos
  exact ⟨k, by simp only [u] at hk; linarith⟩

/-- **The note's case β = 60°** (PROVED-IN-MODEL): with `ρ = 1/√3` (`wRD = qκ/(4 cos 30°)`),
`α = 30°` is a global minimizer, and every global minimizer is `30° + 2πk`. -/
theorem Jdial_60_global (qk α : ℝ) (hq : 0 < qk) :
    Jdial qk (qk / (4 * cos (π / 3 / 2))) (π / 3) (π / 3 / 2)
      ≤ Jdial qk (qk / (4 * cos (π / 3 / 2))) (π / 3) α ∧
    (Jdial qk (qk / (4 * cos (π / 3 / 2))) (π / 3) α
      ≤ Jdial qk (qk / (4 * cos (π / 3 / 2))) (π / 3) (π / 3 / 2) →
      ∃ k : ℤ, α = π / 6 + k * (2 * π)) := by
  refine ⟨Jdial_midpoint_global qk (π / 3) α hq (by positivity) (by linarith [pi_pos]),
    fun h => ?_⟩
  obtain ⟨k, hk⟩ := Jdial_midpoint_unique qk (π / 3) α hq (by positivity)
    (by linarith [pi_pos]) h
  exact ⟨k, by rw [hk]; ring⟩

/-- the β = 60° weight is `ρ = 2wRD/qκ = 1/√3` -/
theorem rho_60 (qk : ℝ) (hq : 0 < qk) :
    2 * (qk / (4 * cos (π / 3 / 2))) / qk = 1 / Real.sqrt 3 := by
  rw [show π / 3 / 2 = π / 6 by ring, cos_pi_div_six]
  field_simp
  have := Real.sq_sqrt (show (0:ℝ) ≤ 3 by norm_num)
  nlinarith [Real.sqrt_nonneg 3]

end GTAORnd.SelfRef.LR3
