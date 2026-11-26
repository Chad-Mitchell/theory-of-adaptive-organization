/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost: `theory/RECORD_COST_ROUND10_2026-11-25.md` §14 (gentle transport, the 7-gon
against the disk at T = 3). Lean round 3 of the side session; written in a private Lake
project (library `GTAORnd`, same Lean and Mathlib pins) and moved here with only this header
and the module lines changed.
-/
module

public import Mathlib

@[expose] public section

/-!
# Gentle transport at T = 3: the 7-gon beats the disk (round 10 note §14)

Model (round 10 note §14, "gentle transport"): move a pure record to a perfectly
distinguishable partner in T ticks through pure states (reversible moves), at cost `c·d²` per
tick, where `d` is the operational distance `sup_e (e x − e y)` over effects. Both state spaces
here have affine dimension 2, so the `κ`-per-dimension term is the same and is dropped; `c = 1`.

State spaces in ℝ² (the normalization coordinate is implicit). Effects are affine maps
`e(s) = c + b₁ s₁ + b₂ s₂` with `0 ≤ e ≤ 1` on the state space.
* the 7-gon `K7`: convex hull of `v k = (cos(2πk/7), sin(2πk/7))`, `k ∈ ℤ`;
* the disk `KD`: `s₁² + s₂² ≤ 1`; pure states `p θ = (cos θ, sin θ)`.

Results (PROVED-IN-MODEL):
* `hept_step_le`: neighbouring 7-gon vertices are at distance `≤ λ = sin(π/7)/sin(3π/7)`;
* `hept_partner`: `v 0` and `v 3` are perfectly distinguishable;
* `hept_path_cost`: the path `v0 → v1 → v2 → v3` costs `≤ 3λ² < 0.67` (numerically 0.594);
* `disk_cost_ge`: every 3-tick pure path from `p 0` to its partner `p π` costs `≥ 3/4`;
* `disk_cost_attained`: equal thirds cost exactly `3/4`;
* `hept_beats_disk`: at T = 3 the 7-gon is strictly cheaper.
Not formalized: that `0.594` is the exact 7-gon optimum, the other horizons and polygons,
uniqueness of the disk partner.
-/

namespace GTAORnd.SelfRef.LR3.Transport

open Real

/-- an affine effect on ℝ² -/
structure Eff where
  c : ℝ
  b1 : ℝ
  b2 : ℝ

/-- value of an effect at a point -/
def ev (e : Eff) (s : ℝ × ℝ) : ℝ := e.c + e.b1 * s.1 + e.b2 * s.2

/-- an effect is valid on `K` if its values on `K` lie in `[0,1]` -/
def Valid (K : Set (ℝ × ℝ)) (e : Eff) : Prop := ∀ s ∈ K, 0 ≤ ev e s ∧ ev e s ≤ 1

/-- operational distance: the largest difference of an effect's values -/
noncomputable def opDist (K : Set (ℝ × ℝ)) (x y : ℝ × ℝ) : ℝ :=
  sSup ((fun e => ev e x - ev e y) '' {e | Valid K e})

lemma valid_zero (K : Set (ℝ × ℝ)) : Valid K ⟨0, 0, 0⟩ := fun s _ => by simp [ev]

lemma bdd {K : Set (ℝ × ℝ)} {x y : ℝ × ℝ} (hx : x ∈ K) (hy : y ∈ K) :
    BddAbove ((fun e => ev e x - ev e y) '' {e | Valid K e}) :=
  ⟨1, by rintro _ ⟨e, he, rfl⟩; linarith [(he x hx).2, (he y hy).1]⟩

lemma opDist_le {K : Set (ℝ × ℝ)} {x y : ℝ × ℝ} {l : ℝ}
    (h : ∀ e, Valid K e → ev e x - ev e y ≤ l) : opDist K x y ≤ l :=
  csSup_le ⟨_, ⟨_, valid_zero K, rfl⟩⟩ (by rintro _ ⟨e, he, rfl⟩; exact h e he)

lemma le_opDist {K : Set (ℝ × ℝ)} {x y : ℝ × ℝ} (hx : x ∈ K) (hy : y ∈ K) {e : Eff}
    (he : Valid K e) : ev e x - ev e y ≤ opDist K x y :=
  le_csSup (bdd hx hy) ⟨e, he, rfl⟩

lemma opDist_nonneg {K : Set (ℝ × ℝ)} {x y : ℝ × ℝ} (hx : x ∈ K) (hy : y ∈ K) :
    0 ≤ opDist K x y := by
  have := le_opDist hx hy (valid_zero K); simpa [ev] using this

/-- validity on a convex hull follows from validity on the generating points -/
lemma valid_hull {S : Set (ℝ × ℝ)} {e : Eff} (h : Valid S e) : Valid (convexHull ℝ S) e := by
  have hc : Convex ℝ {s : ℝ × ℝ | 0 ≤ ev e s ∧ ev e s ≤ 1} := by
    intro a ha b hb t u ht hu htu
    simp only [Set.mem_ofPred_eq, ev, Prod.fst_add, Prod.snd_add, Prod.smul_fst,
      Prod.smul_snd, smul_eq_mul] at ha hb ⊢
    have : e.c + e.b1 * (t * a.1 + u * b.1) + e.b2 * (t * a.2 + u * b.2)
        = t * (e.c + e.b1 * a.1 + e.b2 * a.2) + u * (e.c + e.b1 * b.1 + e.b2 * b.2) := by
      linear_combination (-e.c) * htu
    rw [this]
    constructor <;> nlinarith [ha.1, ha.2, hb.1, hb.2]
  intro s hs
  exact convexHull_min (fun x hx => h x hx) hc hs

/-! ## The 7-gon -/

/-- the central angle `2π/7` -/
noncomputable def a7 : ℝ := 2 * π / 7

/-- the vertices of the regular 7-gon -/
noncomputable def v (k : ℤ) : ℝ × ℝ := (cos (k * a7), sin (k * a7))

/-- the 7-gon state space -/
noncomputable def K7 : Set (ℝ × ℝ) := convexHull ℝ (Set.range v)

/-- `λ = sin(π/7)/sin(3π/7)` -/
noncomputable def lam7 : ℝ := sin (a7 / 2) / sin (3 * a7 / 2)

lemma v_mem (k : ℤ) : v k ∈ K7 := subset_convexHull ℝ _ ⟨k, rfl⟩

lemma sin_half_pos : 0 < sin (a7 / 2) := by
  unfold a7; apply sin_pos_of_pos_of_lt_pi <;> nlinarith [pi_pos]

lemma sin_3half_pos : 0 < sin (3 * a7 / 2) := by
  unfold a7; apply sin_pos_of_pos_of_lt_pi <;> nlinarith [pi_pos]

lemma lam7_nonneg : 0 ≤ lam7 := div_nonneg sin_half_pos.le sin_3half_pos.le

/-- parallel chords: `v k − v (k+1) = λ (v (k−1) − v (k+2))`, coordinatewise -/
lemma chord_parallel (k : ℤ) :
    (v k).1 - (v (k + 1)).1 = lam7 * ((v (k - 1)).1 - (v (k + 2)).1) ∧
    (v k).2 - (v (k + 1)).2 = lam7 * ((v (k - 1)).2 - (v (k + 2)).2) := by
  have hs := sin_3half_pos.ne'
  set t : ℝ := k * a7
  have e1 : ((k + 1 : ℤ) : ℝ) * a7 = t + a7 := by push_cast; ring
  have e2 : ((k - 1 : ℤ) : ℝ) * a7 = t - a7 := by push_cast; ring
  have e3 : ((k + 2 : ℤ) : ℝ) * a7 = t + 2 * a7 := by push_cast; ring
  simp only [v, e1, e2, e3]
  -- write everything through the half angle h = a7/2 and m = t + h
  have hc : ∀ x y : ℝ, cos x - cos y = -2 * sin ((x + y) / 2) * sin ((x - y) / 2) := by
    intro x y; rw [show x = (x + y) / 2 + (x - y) / 2 by ring,
      show y = (x + y) / 2 - (x - y) / 2 by ring]
    simp only [cos_add, cos_sub]; ring_nf
  have hsn : ∀ x y : ℝ, sin x - sin y = 2 * cos ((x + y) / 2) * sin ((x - y) / 2) := by
    intro x y; rw [show x = (x + y) / 2 + (x - y) / 2 by ring,
      show y = (x + y) / 2 - (x - y) / 2 by ring]
    simp only [sin_add, sin_sub]; ring_nf
  unfold lam7
  constructor
  · rw [hc, hc]
    rw [show (t + (t + a7)) / 2 = t + a7 / 2 by ring, show (t - (t + a7)) / 2 = -(a7 / 2) by ring,
      show (t - a7 + (t + 2 * a7)) / 2 = t + a7 / 2 by ring,
      show (t - a7 - (t + 2 * a7)) / 2 = -(3 * a7 / 2) by ring, sin_neg, sin_neg]
    rw [div_mul_eq_mul_div, eq_div_iff hs]; ring
  · rw [hsn, hsn]
    rw [show (t + (t + a7)) / 2 = t + a7 / 2 by ring, show (t - (t + a7)) / 2 = -(a7 / 2) by ring,
      show (t - a7 + (t + 2 * a7)) / 2 = t + a7 / 2 by ring,
      show (t - a7 - (t + 2 * a7)) / 2 = -(3 * a7 / 2) by ring, sin_neg, sin_neg]
    rw [div_mul_eq_mul_div, eq_div_iff hs]; ring

/-- **Neighbouring vertices of the 7-gon are at operational distance `≤ λ`.** -/
theorem hept_step_le (k : ℤ) : opDist K7 (v k) (v (k + 1)) ≤ lam7 := by
  apply opDist_le
  intro e he
  obtain ⟨h1, h2⟩ := chord_parallel k
  have hd : ev e (v k) - ev e (v (k + 1)) = lam7 * (ev e (v (k - 1)) - ev e (v (k + 2))) := by
    simp only [ev]; linear_combination e.b1 * h1 + e.b2 * h2
  rw [hd]
  have := he _ (v_mem (k - 1)); have := he _ (v_mem (k + 2))
  have hl := lam7_nonneg
  nlinarith

/-- `cos(2πk/7) ≥ cos(6π/7)` for every integer `k` -/
lemma cos_ge_cos3 (k : ℤ) : cos (3 * a7) ≤ cos (k * a7) := by
  have h7 : (7 : ℝ) * a7 = 2 * π := by unfold a7; ring
  -- reduce k mod 7
  obtain ⟨q, r, hr0, hr7, rfl⟩ : ∃ q r : ℤ, 0 ≤ r ∧ r < 7 ∧ k = 7 * q + r :=
    ⟨k / 7, k % 7, Int.emod_nonneg _ (by norm_num), Int.emod_lt_of_pos _ (by norm_num),
      by omega⟩
  have hper : cos (((7 * q + r : ℤ) : ℝ) * a7) = cos ((r : ℝ) * a7) := by
    push_cast
    rw [show (7 * (q : ℝ) + r) * a7 = (r : ℝ) * a7 + (q : ℤ) * (2 * π) by rw [← h7]; ring]
    exact cos_add_int_mul_two_pi _ q
  rw [hper]
  have ha : 0 < a7 := by unfold a7; positivity
  have h3 : 3 * a7 ≤ π := by unfold a7; linarith [pi_pos]
  interval_cases r
  · simp; exact cos_le_one _
  · exact cos_le_cos_of_nonneg_of_le_pi (by positivity) h3 (by push_cast; linarith)
  · exact cos_le_cos_of_nonneg_of_le_pi (by positivity) h3 (by push_cast; linarith)
  · push_cast; exact le_rfl
  all_goals
    push_cast
    first
    | (rw [show (4 : ℝ) * a7 = 2 * π - 3 * a7 by linarith, cos_two_pi_sub])
    | (rw [show (5 : ℝ) * a7 = 2 * π - 2 * a7 by linarith, cos_two_pi_sub]
       exact cos_le_cos_of_nonneg_of_le_pi (by positivity) h3 (by linarith))
    | (rw [show (6 : ℝ) * a7 = 2 * π - a7 by linarith, cos_two_pi_sub]
       exact cos_le_cos_of_nonneg_of_le_pi (by positivity) h3 (by linarith))

/-- the effect separating `v 0` from `v 3` -/
noncomputable def e3 : Eff :=
  ⟨-cos (3 * a7) / (1 - cos (3 * a7)), 1 / (1 - cos (3 * a7)), 0⟩

/-- **`v 0` and `v 3` are perfectly distinguishable** in the 7-gon. -/
theorem hept_partner : Valid K7 e3 ∧ ev e3 (v 0) = 1 ∧ ev e3 (v 3) = 0 := by
  have hlt : cos (3 * a7) < 1 := by
    have : cos (3 * a7) < 0 := by
      apply cos_neg_of_pi_div_two_lt_of_lt <;> unfold a7 <;> linarith [pi_pos]
    linarith
  have hpos : 0 < 1 - cos (3 * a7) := by linarith
  have hval : ∀ k : ℤ, ev e3 (v k) = (cos (k * a7) - cos (3 * a7)) / (1 - cos (3 * a7)) := by
    intro k; simp only [ev, e3, v]; field_simp; ring
  refine ⟨valid_hull ?_, ?_, ?_⟩
  · rintro _ ⟨k, rfl⟩
    rw [hval]
    constructor
    · exact div_nonneg (by linarith [cos_ge_cos3 k]) hpos.le
    · rw [div_le_one hpos]; linarith [cos_le_one (k * a7)]
  · rw [hval]; simp only [Int.cast_zero, zero_mul, cos_zero]; exact div_self hpos.ne'
  · rw [hval]; push_cast; simp

/-- numerics: `λ < 0.47`, so `3λ² < 0.67 < 3/4` -/
lemma lam7_lt : lam7 < 0.47 := by
  have hpi := pi_lt_d2
  have hpi' := pi_gt_d2
  have h1 : sin (a7 / 2) < a7 / 2 := sin_lt (by unfold a7; positivity)
  have ha : a7 / 2 < 0.45 := by unfold a7; linarith
  have h2 : sin (3 * a7 / 2) = cos (π / 14) := by
    rw [← cos_pi_div_two_sub]; congr 1; unfold a7; ring
  have h3 : 1 - (π / 14) ^ 2 / 2 ≤ cos (π / 14) := one_sub_sq_div_two_le_cos
  have hs : 0.97 < sin (3 * a7 / 2) := by rw [h2]; nlinarith
  unfold lam7
  rw [div_lt_iff₀ (by linarith)]
  linarith

/-- **The 7-gon path `v0 → v1 → v2 → v3` costs at most `3λ² < 0.67`.** -/
theorem hept_path_cost :
    opDist K7 (v 0) (v 1) ^ 2 + opDist K7 (v 1) (v 2) ^ 2 + opDist K7 (v 2) (v 3) ^ 2
      ≤ 3 * lam7 ^ 2 ∧ 3 * lam7 ^ 2 < 0.67 := by
  have b : ∀ k : ℤ, opDist K7 (v k) (v (k + 1)) ^ 2 ≤ lam7 ^ 2 := fun k =>
    pow_le_pow_left₀ (opDist_nonneg (v_mem _) (v_mem _)) (hept_step_le k) 2
  have b0 := b 0; have b1 := b 1; have b2 := b 2
  norm_num at b0 b1 b2
  refine ⟨by linarith, ?_⟩
  have := lam7_lt; have := lam7_nonneg; nlinarith

/-! ## The disk -/

/-- the disk state space -/
def KD : Set (ℝ × ℝ) := {s | s.1 ^ 2 + s.2 ^ 2 ≤ 1}

/-- pure states of the disk -/
noncomputable def p (θ : ℝ) : ℝ × ℝ := (cos θ, sin θ)

lemma p_mem (θ : ℝ) : p θ ∈ KD := by simp [KD, p, cos_sq_add_sin_sq]

/-- the effect `1/2 + (σ/2)(−sin m · s₁ + cos m · s₂)` is valid on the disk for `σ = ±1` -/
lemma valid_dir (m σ : ℝ) (hσ : σ ^ 2 = 1) :
    Valid KD ⟨1 / 2, -(σ / 2) * sin m, (σ / 2) * cos m⟩ := by
  intro s hs
  simp only [KD, Set.mem_ofPred_eq] at hs
  simp only [ev]
  have hcs := sin_sq_add_cos_sq m
  -- (−sin m s₁ + cos m s₂)² ≤ s₁² + s₂² ≤ 1
  have hcau : (-sin m * s.1 + cos m * s.2) ^ 2 ≤ 1 := by
    nlinarith [sq_nonneg (cos m * s.1 + sin m * s.2)]
  have hw := abs_le.mp ((sq_le_one_iff_abs_le_one _).mp hcau)
  have hσ' : σ = 1 ∨ σ = -1 := by
    have : (σ - 1) * (σ + 1) = 0 := by ring_nf; linarith
    rcases mul_eq_zero.mp this with h | h
    · left; linarith
    · right; linarith
  rcases hσ' with rfl | rfl <;> constructor <;> nlinarith [hw.1, hw.2]

/-- **Disk distance lower bound:** `opDist (p φ) (p ψ) ≥ |sin((φ − ψ)/2)|`. -/
theorem disk_dist_ge (φ ψ : ℝ) : |sin ((φ - ψ) / 2)| ≤ opDist KD (p φ) (p ψ) := by
  set m := (φ + ψ) / 2
  set δ := (φ - ψ) / 2
  have hφ : φ = m + δ := by simp only [m, δ]; ring
  have hψ : ψ = m - δ := by simp only [m, δ]; ring
  have key : ∀ σ : ℝ, σ ^ 2 = 1 →
      ev ⟨1 / 2, -(σ / 2) * sin m, (σ / 2) * cos m⟩ (p φ)
        - ev ⟨1 / 2, -(σ / 2) * sin m, (σ / 2) * cos m⟩ (p ψ) = σ * sin δ := by
    intro σ _
    simp only [ev, p]
    rw [hφ, hψ]; simp only [cos_add, cos_sub, sin_add, sin_sub]
    have := sin_sq_add_cos_sq m
    linear_combination (σ * sin δ) * this
  have hp := le_opDist (p_mem φ) (p_mem ψ) (valid_dir m 1 (by norm_num))
  have hn := le_opDist (p_mem φ) (p_mem ψ) (valid_dir m (-1) (by norm_num))
  rw [key 1 (by norm_num)] at hp
  rw [key (-1) (by norm_num)] at hn
  rw [abs_le']; constructor <;> linarith

/-- valid disk effects have `b₁² + b₂² ≤ 1/4` -/
lemma valid_disk_b (e : Eff) (he : Valid KD e) : e.b1 ^ 2 + e.b2 ^ 2 ≤ 1 / 4 := by
  set r := Real.sqrt (e.b1 ^ 2 + e.b2 ^ 2)
  rcases eq_or_lt_of_le (Real.sqrt_nonneg (e.b1 ^ 2 + e.b2 ^ 2)) with h0 | hr
  · have : e.b1 ^ 2 + e.b2 ^ 2 = 0 := by
      have := Real.sq_sqrt (add_nonneg (sq_nonneg e.b1) (sq_nonneg e.b2)); rw [← h0] at this
      linarith
    linarith
  have hr2 : r ^ 2 = e.b1 ^ 2 + e.b2 ^ 2 := Real.sq_sqrt (by positivity)
  have hu : (e.b1 / r) ^ 2 + (e.b2 / r) ^ 2 ≤ 1 := by
    rw [div_pow, div_pow, ← add_div, hr2, div_self (by rw [← hr2]; positivity)]
  have hu' : (-(e.b1 / r)) ^ 2 + (-(e.b2 / r)) ^ 2 ≤ 1 := by simpa using hu
  have h1 := (he (e.b1 / r, e.b2 / r) hu).2
  have h2 := (he (-(e.b1 / r), -(e.b2 / r)) hu').1
  simp only [ev] at h1 h2
  have hsum : e.b1 * (e.b1 / r) + e.b2 * (e.b2 / r) = r := by
    rw [show e.b1 * (e.b1 / r) + e.b2 * (e.b2 / r) = (e.b1 ^ 2 + e.b2 ^ 2) / r by ring, ← hr2,
      pow_two, mul_div_assoc, div_self hr.ne', mul_one]
  have : 2 * r ≤ 1 := by nlinarith
  nlinarith

/-- **Disk distance upper bound:** `opDist (p φ) (p ψ) ≤ |sin((φ − ψ)/2)|`. -/
theorem disk_dist_le (φ ψ : ℝ) : opDist KD (p φ) (p ψ) ≤ |sin ((φ - ψ) / 2)| := by
  apply opDist_le
  intro e he
  set m := (φ + ψ) / 2
  set δ := (φ - ψ) / 2
  have hφ : φ = m + δ := by simp only [m, δ]; ring
  have hψ : ψ = m - δ := by simp only [m, δ]; ring
  have hd : ev e (p φ) - ev e (p ψ) = 2 * sin δ * (-e.b1 * sin m + e.b2 * cos m) := by
    simp only [ev, p]; rw [hφ, hψ]; simp only [cos_add, cos_sub, sin_add, sin_sub]; ring
  rw [hd]
  have hb := valid_disk_b e he
  have hcs := sin_sq_add_cos_sq m
  have hw : (-e.b1 * sin m + e.b2 * cos m) ^ 2 ≤ 1 / 4 := by
    nlinarith [sq_nonneg (e.b1 * cos m + e.b2 * sin m)]
  have hw' : |(-e.b1 * sin m + e.b2 * cos m)| ≤ 1 / 2 := by
    rw [← abs_of_pos (by norm_num : (0:ℝ) < 1 / 2)]
    exact sq_le_sq.mp (by norm_num; linarith)
  calc 2 * sin δ * (-e.b1 * sin m + e.b2 * cos m)
      ≤ |2 * sin δ * (-e.b1 * sin m + e.b2 * cos m)| := le_abs_self _
    _ = 2 * |sin δ| * |(-e.b1 * sin m + e.b2 * cos m)| := by
        rw [abs_mul, abs_mul, abs_of_pos (by norm_num : (0:ℝ) < 2)]
    _ ≤ 2 * |sin δ| * (1 / 2) := by gcongr
    _ = |sin δ| := by ring

/-- **Disk distance** equals `|sin((φ − ψ)/2)|`. -/
theorem disk_dist (φ ψ : ℝ) : opDist KD (p φ) (p ψ) = |sin ((φ - ψ) / 2)| :=
  le_antisymm (disk_dist_le φ ψ) (disk_dist_ge φ ψ)

/-- `cos A + cos B + cos C ≤ 3/2` when `A + B + C = π` -/
lemma cos_sum_le (A B C : ℝ) (h : A + B + C = π) : cos A + cos B + cos C ≤ 3 / 2 := by
  have hAB : cos A + cos B = 2 * cos ((A + B) / 2) * cos ((A - B) / 2) := by
    rw [show A = (A + B) / 2 + (A - B) / 2 by ring, show B = (A + B) / 2 - (A - B) / 2 by ring]
    simp only [cos_add, cos_sub]; ring_nf
  have hs : cos ((A + B) / 2) = sin (C / 2) := by
    rw [show (A + B) / 2 = π / 2 - C / 2 by linarith, cos_pi_div_two_sub]
  have hC : cos C = 1 - 2 * sin (C / 2) ^ 2 := by
    rw [show C = 2 * (C / 2) by ring, cos_two_mul, show 2 * (C / 2) / 2 = C / 2 by ring]
    nlinarith [sin_sq_add_cos_sq (C / 2)]
  rw [hAB, hs, hC]
  have hc1 := abs_le.mp (abs_cos_le_one ((A - B) / 2))
  set s := sin (C / 2)
  set c := cos ((A - B) / 2)
  -- 2 s c ≤ 2|s| and 2|s| − 2 s² ≤ 1/2
  have : 2 * s * c ≤ 2 * |s| := by
    have := abs_mul s c
    have : |s * c| ≤ |s| := by rw [abs_mul]; exact mul_le_of_le_one_right (abs_nonneg _) (abs_cos_le_one _)
    nlinarith [le_abs_self (s * c)]
  nlinarith [sq_nonneg (2 * |s| - 1), sq_abs s]

/-- `|sin(x/2)|² = (1 − cos x)/2` -/
lemma abs_sin_half_sq (x : ℝ) : |sin (x / 2)| ^ 2 = (1 - cos x) / 2 := by
  rw [sq_abs]
  have : cos x = 1 - 2 * sin (x / 2) ^ 2 := by
    rw [show x = 2 * (x / 2) by ring, cos_two_mul, show 2 * (x / 2) / 2 = x / 2 by ring]
    nlinarith [sin_sq_add_cos_sq (x / 2)]
  linarith

/-- **Every 3-tick pure path from `p 0` to `p π` in the disk costs at least `3/4`.** -/
theorem disk_cost_ge (θ₁ θ₂ : ℝ) :
    3 / 4 ≤ opDist KD (p 0) (p θ₁) ^ 2 + opDist KD (p θ₁) (p θ₂) ^ 2
      + opDist KD (p θ₂) (p π) ^ 2 := by
  rw [disk_dist, disk_dist, disk_dist]
  have e1 : |sin ((0 - θ₁) / 2)| ^ 2 = (1 - cos θ₁) / 2 := by
    rw [abs_sin_half_sq, show (0 : ℝ) - θ₁ = -θ₁ by ring, cos_neg]
  have e2 : |sin ((θ₁ - θ₂) / 2)| ^ 2 = (1 - cos (θ₂ - θ₁)) / 2 := by
    rw [abs_sin_half_sq, ← cos_neg]; ring_nf
  have e3 : |sin ((θ₂ - π) / 2)| ^ 2 = (1 - cos (π - θ₂)) / 2 := by
    rw [abs_sin_half_sq, ← cos_neg]; ring_nf
  rw [e1, e2, e3]
  have := cos_sum_le θ₁ (θ₂ - θ₁) (π - θ₂) (by ring)
  linarith

/-- **Equal thirds attain `3/4`.** -/
theorem disk_cost_attained :
    opDist KD (p 0) (p (π / 3)) ^ 2 + opDist KD (p (π / 3)) (p (2 * π / 3)) ^ 2
      + opDist KD (p (2 * π / 3)) (p π) ^ 2 = 3 / 4 := by
  rw [disk_dist, disk_dist, disk_dist]
  rw [show (0 - π / 3) / 2 = -(π / 6) by ring, show (π / 3 - 2 * π / 3) / 2 = -(π / 6) by ring,
    show (2 * π / 3 - π) / 2 = -(π / 6) by ring, sin_neg, abs_neg, sin_pi_div_six]
  norm_num

/-- `p π` is the disk partner of `p 0`: they are perfectly distinguishable. -/
theorem disk_partner : Valid KD ⟨1 / 2, 1 / 2, 0⟩ ∧ ev ⟨1 / 2, 1 / 2, 0⟩ (p 0) = 1 ∧
    ev ⟨1 / 2, 1 / 2, 0⟩ (p π) = 0 := by
  refine ⟨fun s hs => ?_, by simp [ev, p]; norm_num, by simp [ev, p]⟩
  simp only [KD, Set.mem_ofPred_eq] at hs
  simp only [ev]
  have : s.1 ^ 2 ≤ 1 := by nlinarith [sq_nonneg s.2]
  have := abs_le.mp ((sq_le_one_iff_abs_le_one _).mp this)
  constructor <;> linarith [this.1, this.2]

/-- **At T = 3 the 7-gon beats the disk** (PROVED-IN-MODEL): the 7-gon has a 3-tick vertex path
from `v 0` to a perfectly distinguishable vertex costing less than every 3-tick pure path in
the disk from `p 0` to its partner `p π`. -/
theorem hept_beats_disk (θ₁ θ₂ : ℝ) :
    opDist K7 (v 0) (v 1) ^ 2 + opDist K7 (v 1) (v 2) ^ 2 + opDist K7 (v 2) (v 3) ^ 2
      < opDist KD (p 0) (p θ₁) ^ 2 + opDist KD (p θ₁) (p θ₂) ^ 2
      + opDist KD (p θ₂) (p π) ^ 2 := by
  have h := hept_path_cost
  have := disk_cost_ge θ₁ θ₂
  linarith [h.1, h.2]

end GTAORnd.SelfRef.LR3.Transport
