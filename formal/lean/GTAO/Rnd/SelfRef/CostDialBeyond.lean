/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost: `theory/RECORD_COST_CHAIN_2026-11-25.md` step S10 (the cost dial), the converse
for `β > π/2` left open in `CostDialGlobal.lean`. Lean round 4 of the side session.
-/
module

public import Mathlib
public import GTAO.Rnd.SelfRef.CostDialGlobal

@[expose] public section

/-!
# Cost dial for `π/2 < β < π`

At the tuned weight `ρ = 1/(2cos(β/2))` the midpoint `α = β/2` is stationary. For `0 < β ≤ π/2` it is
a global minimizer (`Jdial_midpoint_global`). Here: for every `π/2 < β < π`, the point
`α = β/2 + π/2` costs strictly less, so the midpoint is not a global minimizer; at `β = π/2` the two
tie. (This corrects the remark in `CostDialGlobal.lean` that the midpoint stops being the global
minimizer "from β ≈ 1.61": it stops right after `π/2`.) Where the global minimizer lies for
`β > π/2` is not formalized.
-/

namespace GTAORnd.SelfRef.LR3

open Real GTAORnd.SelfRef

/-- **The midpoint is not a global minimizer for `π/2 < β < π`** (PROVED-IN-MODEL). At the tuned
weight `wRD = qκ/(4cos(β/2))` (`ρ = 1/(2cos(β/2))`, where the midpoint is stationary), the point
`α = β/2 + π/2` has strictly lower cost than the midpoint `α = β/2`. At `β = π/2` both cost the same
(`Jdial_midpoint_global` gives that the midpoint is still a global minimizer there). -/
theorem Jdial_midpoint_not_global (qk β : ℝ) (hq : 0 < qk) (hβ0 : π / 2 < β) (hβ : β < π) :
    Jdial qk (qk / (4 * cos (β / 2))) β (β / 2 + π / 2)
      < Jdial qk (qk / (4 * cos (β / 2))) β (β / 2) := by
  have hc : 0 < cos (β / 2) := cos_pos_of_mem_Ioo ⟨by linarith [pi_pos], by linarith⟩
  have hsc : cos (β / 2) < sin (β / 2) := by
    rw [← sin_pi_div_two_sub]
    apply sin_lt_sin_of_lt_of_le_pi_div_two <;> linarith [pi_pos]
  have hd := dial_diff qk β (π / 2) hc.ne'
  rw [cos_pi_div_two, sin_pi_div_two] at hd
  have h1 : cos (β / 2) ^ 2 - sin (β / 2) ^ 2 < 0 := by nlinarith
  have h2 : (cos (β / 2) ^ 2 - sin (β / 2) ^ 2) / (2 * cos (β / 2)) < 0 :=
    div_neg_of_neg_of_pos h1 (by linarith)
  have : qk / 2 * ((1 - 0) * (cos (β / 2) - sin (β / 2) * 1)
      + 1 ^ 2 * (cos (β / 2) ^ 2 - sin (β / 2) ^ 2) / (2 * cos (β / 2))) < 0 := by
    apply mul_neg_of_pos_of_neg (by linarith)
    have : (1 : ℝ) ^ 2 * (cos (β / 2) ^ 2 - sin (β / 2) ^ 2) / (2 * cos (β / 2))
        = (cos (β / 2) ^ 2 - sin (β / 2) ^ 2) / (2 * cos (β / 2)) := by ring
    rw [this]; linarith
  linarith

/-- at `β = π/2` the point `β/2 + π/2` ties with the midpoint (two global minimizers) -/
theorem Jdial_tie_at_right_angle (qk : ℝ) :
    Jdial qk (qk / (4 * cos (π / 2 / 2))) (π / 2) (π / 2 / 2 + π / 2)
      = Jdial qk (qk / (4 * cos (π / 2 / 2))) (π / 2) (π / 2 / 2) := by
  have hc : 0 < cos (π / 2 / 2) := cos_pos_of_mem_Ioo ⟨by linarith [pi_pos], by linarith [pi_pos]⟩
  have hd := dial_diff qk (π / 2) (π / 2) hc.ne'
  rw [cos_pi_div_two, sin_pi_div_two, show π / 2 / 2 = π / 4 by ring, cos_pi_div_four,
    sin_pi_div_four] at hd
  rw [show π / 2 / 2 = π / 4 by ring, cos_pi_div_four]
  linarith [show qk / 2 * ((1 - 0) * (√2 / 2 - √2 / 2 * 1) + 1 ^ 2 * ((√2 / 2) ^ 2 - (√2 / 2) ^ 2) /
    (2 * (√2 / 2))) = 0 by ring]

end GTAORnd.SelfRef.LR3
