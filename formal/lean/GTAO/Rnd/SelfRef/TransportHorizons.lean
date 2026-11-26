/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost: round 10 note (`theory/RECORD_COST_ROUND10_2026-11-25.md`) §14, gentle transport
in the disk at horizons T = 2 and T = 4, and the 9-gon at T = 4 (`Transport.lean` has T = 3). Lean round 4 of the side session.
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
steps. The exact optimum is `T sin²(π/(2T))`: 1 at T = 2, `2 − √2` at T = 4. At T = 4 the 9-gon has a
vertex path to a perfectly distinguishable vertex costing at most `4μ² < 0.52`, `μ = sin(π/9)/sin(5π/9)`,
so it beats the disk there (`nona_beats_disk`); that `4μ²` is the 9-gon's exact optimum, and the
polygon sides at other horizons, are not formalized.
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

/-! ## The 9-gon at T = 4 -/

/-- the central angle `2π/9` -/
noncomputable def a9 : ℝ := 2 * π / 9

/-- the vertices of the regular 9-gon -/
noncomputable def w (k : ℤ) : ℝ × ℝ := (cos (k * a9), sin (k * a9))

/-- the 9-gon state space -/
noncomputable def K9 : Set (ℝ × ℝ) := convexHull ℝ (Set.range w)

/-- `μ = sin(π/9)/sin(5π/9)` -/
noncomputable def mu9 : ℝ := sin (a9 / 2) / sin (5 * a9 / 2)

lemma w_mem (k : ℤ) : w k ∈ K9 := subset_convexHull ℝ _ ⟨k, rfl⟩

lemma sin9_half_pos : 0 < sin (a9 / 2) := by
  unfold a9; apply sin_pos_of_pos_of_lt_pi <;> nlinarith [pi_pos]

lemma sin9_5half_pos : 0 < sin (5 * a9 / 2) := by
  unfold a9; apply sin_pos_of_pos_of_lt_pi <;> nlinarith [pi_pos]

lemma mu9_nonneg : 0 ≤ mu9 := div_nonneg sin9_half_pos.le sin9_5half_pos.le

/-- parallel chords: `w k − w (k+1) = μ (w (k−2) − w (k+3))`, coordinatewise -/
lemma chord9_parallel (k : ℤ) :
    (w k).1 - (w (k + 1)).1 = mu9 * ((w (k - 2)).1 - (w (k + 3)).1) ∧
    (w k).2 - (w (k + 1)).2 = mu9 * ((w (k - 2)).2 - (w (k + 3)).2) := by
  have hs := sin9_5half_pos.ne'
  set t : ℝ := k * a9
  have e1 : ((k + 1 : ℤ) : ℝ) * a9 = t + a9 := by push_cast; ring
  have e2 : ((k - 2 : ℤ) : ℝ) * a9 = t - 2 * a9 := by push_cast; ring
  have e3 : ((k + 3 : ℤ) : ℝ) * a9 = t + 3 * a9 := by push_cast; ring
  simp only [w, e1, e2, e3]
  have hc : ∀ x y : ℝ, cos x - cos y = -2 * sin ((x + y) / 2) * sin ((x - y) / 2) := by
    intro x y; rw [show x = (x + y) / 2 + (x - y) / 2 by ring,
      show y = (x + y) / 2 - (x - y) / 2 by ring]
    simp only [cos_add, cos_sub]; ring_nf
  have hsn : ∀ x y : ℝ, sin x - sin y = 2 * cos ((x + y) / 2) * sin ((x - y) / 2) := by
    intro x y; rw [show x = (x + y) / 2 + (x - y) / 2 by ring,
      show y = (x + y) / 2 - (x - y) / 2 by ring]
    simp only [sin_add, sin_sub]; ring_nf
  unfold mu9
  constructor
  · rw [hc, hc]
    rw [show (t + (t + a9)) / 2 = t + a9 / 2 by ring, show (t - (t + a9)) / 2 = -(a9 / 2) by ring,
      show (t - 2 * a9 + (t + 3 * a9)) / 2 = t + a9 / 2 by ring,
      show (t - 2 * a9 - (t + 3 * a9)) / 2 = -(5 * a9 / 2) by ring, sin_neg, sin_neg]
    rw [div_mul_eq_mul_div, eq_div_iff hs]; ring
  · rw [hsn, hsn]
    rw [show (t + (t + a9)) / 2 = t + a9 / 2 by ring, show (t - (t + a9)) / 2 = -(a9 / 2) by ring,
      show (t - 2 * a9 + (t + 3 * a9)) / 2 = t + a9 / 2 by ring,
      show (t - 2 * a9 - (t + 3 * a9)) / 2 = -(5 * a9 / 2) by ring, sin_neg, sin_neg]
    rw [div_mul_eq_mul_div, eq_div_iff hs]; ring

/-- **Neighbouring vertices of the 9-gon are at operational distance `≤ μ`.** -/
theorem nona_step_le (k : ℤ) : opDist K9 (w k) (w (k + 1)) ≤ mu9 := by
  apply opDist_le
  intro e he
  obtain ⟨h1, h2⟩ := chord9_parallel k
  have hd : ev e (w k) - ev e (w (k + 1)) = mu9 * (ev e (w (k - 2)) - ev e (w (k + 3))) := by
    simp only [ev]; linear_combination e.b1 * h1 + e.b2 * h2
  rw [hd]
  have := he _ (w_mem (k - 2)); have := he _ (w_mem (k + 3))
  have hl := mu9_nonneg
  nlinarith

/-- `cos(2πk/9) ≥ cos(8π/9)` for every integer `k` -/
lemma cos_ge_cos4 (k : ℤ) : cos (4 * a9) ≤ cos (k * a9) := by
  have h9 : (9 : ℝ) * a9 = 2 * π := by unfold a9; ring
  obtain ⟨q, r, hr0, hr9, rfl⟩ : ∃ q r : ℤ, 0 ≤ r ∧ r < 9 ∧ k = 9 * q + r :=
    ⟨k / 9, k % 9, Int.emod_nonneg _ (by norm_num), Int.emod_lt_of_pos _ (by norm_num),
      by omega⟩
  have hper : cos (((9 * q + r : ℤ) : ℝ) * a9) = cos ((r : ℝ) * a9) := by
    push_cast
    rw [show (9 * (q : ℝ) + r) * a9 = (r : ℝ) * a9 + (q : ℤ) * (2 * π) by rw [← h9]; ring]
    exact cos_add_int_mul_two_pi _ q
  rw [hper]
  have ha : 0 < a9 := by unfold a9; positivity
  have h4 : 4 * a9 ≤ π := by unfold a9; linarith [pi_pos]
  interval_cases r
  · simp; exact cos_le_one _
  · exact cos_le_cos_of_nonneg_of_le_pi (by positivity) h4 (by push_cast; linarith)
  · exact cos_le_cos_of_nonneg_of_le_pi (by positivity) h4 (by push_cast; linarith)
  · exact cos_le_cos_of_nonneg_of_le_pi (by positivity) h4 (by push_cast; linarith)
  · push_cast; exact le_rfl
  all_goals
    push_cast
    first
    | (rw [show (5 : ℝ) * a9 = 2 * π - 4 * a9 by linarith, cos_two_pi_sub])
    | (rw [show (6 : ℝ) * a9 = 2 * π - 3 * a9 by linarith, cos_two_pi_sub]
       exact cos_le_cos_of_nonneg_of_le_pi (by positivity) h4 (by linarith))
    | (rw [show (7 : ℝ) * a9 = 2 * π - 2 * a9 by linarith, cos_two_pi_sub]
       exact cos_le_cos_of_nonneg_of_le_pi (by positivity) h4 (by linarith))
    | (rw [show (8 : ℝ) * a9 = 2 * π - a9 by linarith, cos_two_pi_sub]
       exact cos_le_cos_of_nonneg_of_le_pi (by positivity) h4 (by linarith))

/-- the effect separating `w 0` from `w 4` -/
noncomputable def f4 : Eff :=
  ⟨-cos (4 * a9) / (1 - cos (4 * a9)), 1 / (1 - cos (4 * a9)), 0⟩

/-- **`w 0` and `w 4` are perfectly distinguishable** in the 9-gon. -/
theorem nona_partner : Valid K9 f4 ∧ ev f4 (w 0) = 1 ∧ ev f4 (w 4) = 0 := by
  have hlt : cos (4 * a9) < 1 := by
    have : cos (4 * a9) < 0 := by
      apply cos_neg_of_pi_div_two_lt_of_lt <;> unfold a9 <;> linarith [pi_pos]
    linarith
  have hpos : 0 < 1 - cos (4 * a9) := by linarith
  have hval : ∀ k : ℤ, ev f4 (w k) = (cos (k * a9) - cos (4 * a9)) / (1 - cos (4 * a9)) := by
    intro k; simp only [ev, f4, w]; field_simp; ring
  refine ⟨valid_hull ?_, ?_, ?_⟩
  · rintro _ ⟨k, rfl⟩
    rw [hval]
    constructor
    · exact div_nonneg (by linarith [cos_ge_cos4 k]) hpos.le
    · rw [div_le_one hpos]; linarith [cos_le_one (k * a9)]
  · rw [hval]; simp only [Int.cast_zero, zero_mul, cos_zero]; exact div_self hpos.ne'
  · rw [hval]; push_cast; simp

/-- numerics: `μ < 0.36` -/
lemma mu9_lt : mu9 < 0.36 := by
  have hpi := pi_lt_d2
  have hpi' := pi_gt_d2
  have h1 : sin (a9 / 2) < a9 / 2 := sin_lt (by unfold a9; positivity)
  have ha : a9 / 2 < 0.35 := by unfold a9; linarith
  have h2 : sin (5 * a9 / 2) = cos (π / 18) := by
    rw [← cos_neg, ← cos_pi_div_two_sub]; congr 1; unfold a9; ring
  have h3 : 1 - (π / 18) ^ 2 / 2 ≤ cos (π / 18) := one_sub_sq_div_two_le_cos
  have hs : 0.98 < sin (5 * a9 / 2) := by rw [h2]; nlinarith
  unfold mu9
  rw [div_lt_iff₀ (by linarith)]
  linarith

/-- **The 9-gon path `w0 → w1 → w2 → w3 → w4` costs at most `4μ² < 0.52`.** -/
theorem nona_path_cost :
    opDist K9 (w 0) (w 1) ^ 2 + opDist K9 (w 1) (w 2) ^ 2 + opDist K9 (w 2) (w 3) ^ 2
      + opDist K9 (w 3) (w 4) ^ 2 ≤ 4 * mu9 ^ 2 ∧ 4 * mu9 ^ 2 < 0.52 := by
  have b : ∀ k : ℤ, opDist K9 (w k) (w (k + 1)) ^ 2 ≤ mu9 ^ 2 := fun k =>
    pow_le_pow_left₀ (opDist_nonneg (w_mem _) (w_mem _)) (nona_step_le k) 2
  have b0 := b 0; have b1 := b 1; have b2 := b 2; have b3 := b 3
  norm_num at b0 b1 b2 b3
  refine ⟨by linarith, ?_⟩
  have := mu9_lt; have := mu9_nonneg; nlinarith

/-- **At T = 4 the 9-gon beats the disk** (PROVED-IN-MODEL): the 9-gon has a 4-tick vertex path
from `w 0` to a perfectly distinguishable vertex costing less than every 4-tick pure path in the
disk from `p 0` to its partner `p π` (at least `2 − √2`). -/
theorem nona_beats_disk (θ₁ θ₂ θ₃ : ℝ) :
    opDist K9 (w 0) (w 1) ^ 2 + opDist K9 (w 1) (w 2) ^ 2 + opDist K9 (w 2) (w 3) ^ 2
      + opDist K9 (w 3) (w 4) ^ 2
      < opDist KD (p 0) (p θ₁) ^ 2 + opDist KD (p θ₁) (p θ₂) ^ 2
      + opDist KD (p θ₂) (p θ₃) ^ 2 + opDist KD (p θ₃) (p π) ^ 2 := by
  have h := nona_path_cost
  have hd := disk_cost_T4_ge θ₁ θ₂ θ₃
  have hs : √2 < 1.42 := by
    rw [Real.sqrt_lt' (by norm_num)]; norm_num
  linarith [h.1, h.2]

end GTAORnd.SelfRef.LR3.TransportHorizons
