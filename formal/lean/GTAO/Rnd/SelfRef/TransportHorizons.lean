/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost: round 10 note (`theory/RECORD_COST_ROUND10_2026-11-25.md`) §14, gentle transport
in the disk at horizons T = 2 and T = 4 (`Transport.lean` has T = 3). Lean round 4 of the side session.
-/
module

public import Mathlib
public import GTAO.Rnd.SelfRef.Transport

@[expose] public section

/-!
# Exact disk transport costs at T = 2 and T = 4

Same model as `Transport.lean`: the disk `KD`, its pure states `p θ`, the operational distance
`opDist KD` (a supremum over the disk's effects, equal to `abs (sin ((φ − ψ)/2))` by `disk_dist`), and
the cost of a T-tick path through pure states from `p 0` to its partner `p π` as the sum of squared
steps. The exact optimum is `T sin²(π/(2T))`: 1 at T = 2, `2 − √2` at T = 4. The 7-gon side at these
horizons is not formalized.
-/

namespace GTAORnd.SelfRef.LR3.TransportHorizons

open Real GTAORnd.SelfRef.LR3.Transport

/-- **Every 2-tick pure path in the disk from `p 0` to `p π` costs exactly 1.** -/
theorem disk_cost_T2 (θ : ℝ) :
    opDist KD (p 0) (p θ) ^ 2 + opDist KD (p θ) (p π) ^ 2 = 1 := by
  rw [disk_dist, disk_dist, abs_sin_half_sq, abs_sin_half_sq,
    show (0 : ℝ) - θ = -θ by ring, cos_neg, show θ - π = -(π - θ) by ring, cos_neg, cos_pi_sub]
  ring

/-- `cos A + cos B + cos C + cos D ≤ 2√2` when `A + B + C + D = π` -/
lemma cos_sum4_le (A B C D : ℝ) (h : A + B + C + D = π) :
    cos A + cos B + cos C + cos D ≤ 2 * √2 := by
  have pair : ∀ X Y : ℝ, cos X + cos Y ≤ 2 * |cos ((X + Y) / 2)| := fun X Y => by
    have e : cos X + cos Y = 2 * cos ((X + Y) / 2) * cos ((X - Y) / 2) := by
      rw [show X = (X + Y) / 2 + (X - Y) / 2 by ring, show Y = (X + Y) / 2 - (X - Y) / 2 by ring]
      simp only [cos_add, cos_sub]; ring_nf
    rw [e]
    have h1 : cos ((X + Y) / 2) * cos ((X - Y) / 2) ≤ |cos ((X + Y) / 2)| := by
      calc _ ≤ |cos ((X + Y) / 2) * cos ((X - Y) / 2)| := le_abs_self _
        _ = |cos ((X + Y) / 2)| * |cos ((X - Y) / 2)| := abs_mul _ _
        _ ≤ |cos ((X + Y) / 2)| := mul_le_of_le_one_right (abs_nonneg _) (abs_cos_le_one _)
    linarith
  have hw : cos ((C + D) / 2) = sin ((A + B) / 2) := by
    rw [show (C + D) / 2 = π / 2 - (A + B) / 2 by linarith, cos_pi_div_two_sub]
  have h1 := pair A B
  have h2 := pair C D
  rw [hw] at h2
  set c := cos ((A + B) / 2)
  set s := sin ((A + B) / 2)
  have hcs : c ^ 2 + s ^ 2 = 1 := by rw [add_comm]; exact sin_sq_add_cos_sq _
  have hsq : (|c| + |s|) ^ 2 ≤ 2 := by
    nlinarith [sq_abs c, sq_abs s, sq_nonneg (|c| - |s|)]
  have := Real.abs_le_sqrt hsq
  rw [abs_of_nonneg (by positivity)] at this
  linarith

/-- **Every 4-tick pure path in the disk from `p 0` to `p π` costs at least `2 − √2`.** -/
theorem disk_cost_T4_ge (θ₁ θ₂ θ₃ : ℝ) :
    2 - √2 ≤ opDist KD (p 0) (p θ₁) ^ 2 + opDist KD (p θ₁) (p θ₂) ^ 2
      + opDist KD (p θ₂) (p θ₃) ^ 2 + opDist KD (p θ₃) (p π) ^ 2 := by
  rw [disk_dist, disk_dist, disk_dist, disk_dist]
  have e : ∀ a b : ℝ, |sin ((a - b) / 2)| ^ 2 = (1 - cos (b - a)) / 2 := fun a b => by
    rw [abs_sin_half_sq, ← cos_neg]; ring_nf
  rw [e, e, e, e]
  have := cos_sum4_le (θ₁ - 0) (θ₂ - θ₁) (θ₃ - θ₂) (π - θ₃) (by ring)
  linarith

/-- **Equal quarters attain `2 − √2`.** -/
theorem disk_cost_T4_attained :
    opDist KD (p 0) (p (π / 4)) ^ 2 + opDist KD (p (π / 4)) (p (π / 2)) ^ 2
      + opDist KD (p (π / 2)) (p (3 * π / 4)) ^ 2 + opDist KD (p (3 * π / 4)) (p π) ^ 2
      = 2 - √2 := by
  rw [disk_dist, disk_dist, disk_dist, disk_dist]
  have e : ∀ a b : ℝ, b - a = π / 4 → |sin ((a - b) / 2)| ^ 2 = (1 - √2 / 2) / 2 := fun a b h => by
    rw [abs_sin_half_sq, show a - b = -(π / 4) by linarith, cos_neg, cos_pi_div_four]
  rw [e _ _ (by ring), e _ _ (by ring), e _ _ (by ring), e _ _ (by ring)]
  ring

end GTAORnd.SelfRef.LR3.TransportHorizons
