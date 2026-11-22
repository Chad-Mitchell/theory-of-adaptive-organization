/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lean 4 formalization of the selection-axioms stationary excess
(CORE §3, THEORY §4: `E[J] - J* = d/(2β)`), for OPEN_WORK T19.
-/
module

public import Mathlib.MeasureTheory.Measure.Haar.NormedSpace
public import Mathlib.MeasureTheory.Constructions.HaarToSphere
public import Mathlib.MeasureTheory.Integral.Prod
public import Mathlib.Analysis.SpecialFunctions.Gaussian.GaussianIntegral
public import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
public import Mathlib.LinearAlgebra.Matrix.PosDef
public import Mathlib.Topology.Instances.Matrix

/-!
# Equipartition: the Gibbs excess `d/(pβ)`
-/

@[expose] public section

namespace Equipartition

open MeasureTheory Real Set Module

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [MeasurableSpace E]
  [BorelSpace E] [FiniteDimensional ℝ E] (μ : Measure E) [μ.IsAddHaarMeasure]

/-- Partition function `Z(β) = ∫ exp(-β q)`. -/
noncomputable def Z (q : E → ℝ) (β : ℝ) : ℝ := ∫ x, exp (-(β * q x)) ∂μ

/-- Unnormalized first moment `N(β) = ∫ q exp(-β q)`. -/
noncomputable def Nm (q : E → ℝ) (β : ℝ) : ℝ := ∫ x, q x * exp (-(β * q x)) ∂μ

/-- Standing hypotheses on the cost excess `q`: continuous, nonnegative... -/
structure HomogCost (q : E → ℝ) (p : ℝ) : Prop where
  p_pos : 0 < p
  cont : Continuous q
  nonneg : ∀ x, 0 ≤ q x
  pos : ∀ x, x ≠ 0 → 0 < q x
  homog : ∀ r : ℝ, 0 < r → ∀ x, q (r • x) = r ^ p * q x

variable {μ}

omit [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E] in
lemma scale_eq {q : E → ℝ} {p : ℝ} (hq : HomogCost q p) {β : ℝ} (hβ : 0 < β) (x : E) :
    q (β ^ (1 / p) • x) = β * q x := by
  rw [hq.homog _ (rpow_pos_of_pos hβ _), ← rpow_mul hβ.le, one_div_mul_cancel hq.p_pos.ne', rpow_one]

omit [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E] in
lemma pow_finrank_inv {p β : ℝ} (hp : 0 < p) (hβ : 0 < β) :
    ((β ^ (1 / p)) ^ finrank ℝ E)⁻¹ = β ^ (-(finrank ℝ E / p) : ℝ) := by
  rw [← rpow_natCast, ← rpow_mul hβ.le, rpow_neg hβ.le]
  congr 2; field_simp

/-- Scaling of the partition function: `Z(β) = β^{-d/p} Z(1)`. -/
theorem Z_scale {q : E → ℝ} {p : ℝ} (hq : HomogCost q p) {β : ℝ} (hβ : 0 < β) :
    Z μ q β = β ^ (-(finrank ℝ E / p) : ℝ) * Z μ q 1 := by
  have h := Measure.integral_comp_smul_of_nonneg μ (fun x => exp (-(1 * q x))) (β ^ (1 / p))
    (hR := (rpow_pos_of_pos hβ _).le)
  simp only [scale_eq hq hβ, one_mul, smul_eq_mul] at h
  unfold Z
  rw [pow_finrank_inv hq.p_pos hβ] at h
  simpa using h

/-- Scaling of the first moment: `N(β) = β^{-1} β^{-d/p} N(1)`. -/
theorem Nm_scale {q : E → ℝ} {p : ℝ} (hq : HomogCost q p) {β : ℝ} (hβ : 0 < β) :
    Nm μ q β = β⁻¹ * (β ^ (-(finrank ℝ E / p) : ℝ) * Nm μ q 1) := by
  have h := Measure.integral_comp_smul_of_nonneg μ (fun x => q x * exp (-(1 * q x))) (β ^ (1 / p))
    (hR := (rpow_pos_of_pos hβ _).le)
  simp only [scale_eq hq hβ, one_mul, smul_eq_mul] at h
  rw [pow_finrank_inv hq.p_pos hβ] at h
  unfold Nm
  simp only [one_mul]
  rw [← h, ← integral_const_mul]
  congr 1; ext x
  field_simp

omit [MeasurableSpace E] [BorelSpace E] in
/-- Coercivity: a continuous, degree-`p` homogeneous cost that is positive
away from `0` satisfies `q x ≥ m ‖x‖^p` for some `m > 0`. -/
lemma exists_lower_bound [Nontrivial E] {q : E → ℝ} {p : ℝ} (hq : HomogCost q p) :
    ∃ m, 0 < m ∧ ∀ x, m * ‖x‖ ^ p ≤ q x := by
  have hne : (Metric.sphere (0 : E) 1).Nonempty := NormedSpace.sphere_nonempty.mpr zero_le_one
  obtain ⟨u, hu, hmin⟩ :=
    (isCompact_sphere (0 : E) 1).exists_isMinOn hne hq.cont.continuousOn
  have hu0 : u ≠ 0 := by
    intro h; rw [h, mem_sphere_zero_iff_norm, norm_zero] at hu; exact zero_ne_one hu
  refine ⟨q u, hq.pos u hu0, fun x => ?_⟩
  rcases eq_or_ne x 0 with rfl | hx
  · rw [norm_zero, zero_rpow hq.p_pos.ne', mul_zero]; exact hq.nonneg 0
  · have hn : 0 < ‖x‖ := norm_pos_iff.mpr hx
    have hmem : ‖x‖⁻¹ • x ∈ Metric.sphere (0 : E) 1 := by
      rw [mem_sphere_zero_iff_norm, norm_smul, norm_inv, norm_norm, inv_mul_cancel₀ hn.ne']
    have h1 : q u ≤ q (‖x‖⁻¹ • x) := hmin hmem
    have h2 : q x = ‖x‖ ^ p * q (‖x‖⁻¹ • x) := by
      rw [← hq.homog _ hn, smul_smul, mul_inv_cancel₀ hn.ne', one_smul]
    rw [h2, mul_comm]
    exact mul_le_mul_of_nonneg_left h1 (rpow_nonneg hn.le _)

lemma integrable_exp_neg_norm_rpow [Nontrivial E] {p b : ℝ} (hp : 0 < p) (hb : 0 < b) :
    Integrable (fun x : E => exp (-(b * ‖x‖ ^ p))) μ := by
  have := (integrable_fun_norm_addHaar μ (f := fun y : ℝ => exp (-(b * y ^ p)))).mpr ?_
  · exact this
  have h := integrableOn_rpow_mul_exp_neg_mul_rpow
    (s := ((finrank ℝ E - 1 : ℕ) : ℝ))
    (by have := Nat.cast_nonneg (α := ℝ) (finrank ℝ E - 1); linarith) hp hb
  refine h.congr_fun (fun y hy => ?_) measurableSet_Ioi
  simp only [smul_eq_mul, rpow_natCast, neg_mul]

lemma integrable_exp {q : E → ℝ} {p : ℝ} [Nontrivial E] (hq : HomogCost q p) {β : ℝ}
    (hβ : 0 < β) : Integrable (fun x => exp (-(β * q x))) μ := by
  obtain ⟨m, hm, hlow⟩ := exists_lower_bound hq
  refine (integrable_exp_neg_norm_rpow (μ := μ) hq.p_pos (mul_pos hβ hm)).mono'
    (Continuous.aestronglyMeasurable (by have := hq.cont; fun_prop))
    (Filter.Eventually.of_forall fun x => ?_)
  rw [Real.norm_eq_abs, abs_of_pos (exp_pos _), exp_le_exp, mul_assoc]
  exact neg_le_neg (mul_le_mul_of_nonneg_left (hlow x) hβ.le)

lemma integrable_moment {q : E → ℝ} {p : ℝ} [Nontrivial E] (hq : HomogCost q p) {β : ℝ}
    (hβ : 0 < β) : Integrable (fun x => q x * exp (-(β * q x))) μ := by
  have hi := (integrable_exp (μ := μ) hq (half_pos hβ)).const_mul (2 / β)
  refine hi.mono' (Continuous.aestronglyMeasurable (by have := hq.cont; fun_prop)) (Filter.Eventually.of_forall fun x => ?_)
  have hqx := hq.nonneg x
  rw [Real.norm_eq_abs, abs_of_nonneg (mul_nonneg hqx (exp_pos _).le)]
  have h1 : β / 2 * q x + 1 ≤ exp (β / 2 * q x) := add_one_le_exp _
  have h2 : q x ≤ 2 / β * exp (β / 2 * q x) := by
    rw [div_mul_eq_mul_div, le_div_iff₀ hβ]; nlinarith [exp_pos (β / 2 * q x)]
  have h3 : exp (β / 2 * q x) * exp (-(β * q x)) = exp (-(β / 2 * q x)) := by
    rw [← exp_add]; congr 1; ring
  calc q x * exp (-(β * q x)) ≤ 2 / β * exp (β / 2 * q x) * exp (-(β * q x)) :=
        mul_le_mul_of_nonneg_right h2 (exp_pos _).le
    _ = 2 / β * exp (-(β / 2 * q x)) := by rw [mul_assoc, h3]

/-- The one-variable identity behind the swap:
`∫_1^2 t e^{-s t} ds = e^{-t} - e^{-2t}`. -/
lemma inner_ftc (t : ℝ) :
    ∫ s in (1 : ℝ)..2, t * exp (-(s * t)) = exp (-t) - exp (-(2 * t)) := by
  have hderiv : ∀ s ∈ uIcc (1 : ℝ) 2,
      HasDerivAt (fun s => -exp (-(s * t))) (t * exp (-(s * t))) s := by
    intro s _
    have h0 : HasDerivAt (fun s : ℝ => s * t) t s := by
      simpa using (hasDerivAt_id' s).mul_const t
    have h1 : HasDerivAt (fun s : ℝ => -(s * t)) (-t) s := h0.neg
    have h3 : HasDerivAt (fun s : ℝ => -exp (-(s * t))) (-(exp (-(s * t)) * -t)) s :=
      h1.exp.neg
    convert h3 using 1
    ring
  rw [intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv
    ((by fun_prop : Continuous fun s : ℝ => t * exp (-(s * t))).intervalIntegrable _ _)]
  simp only [one_mul]
  ring

lemma Z_sub_eq_integral_Nm [Nontrivial E] {q : E → ℝ} {p : ℝ} (hq : HomogCost q p) :
    Z μ q 1 - Z μ q 2 = ∫ s in (1 : ℝ)..2, Nm μ q s := by
  have hcont := hq.cont
  set ν : Measure ℝ := volume.restrict (Ioc (1 : ℝ) 2)
  have hint : Integrable (Function.uncurry fun (x : E) (s : ℝ) => q x * exp (-(s * q x)))
      (μ.prod ν) := by
    have hg : Integrable (fun z : E × ℝ => q z.1 * exp (-(1 * q z.1))) (μ.prod ν) :=
      (integrable_moment (μ := μ) hq one_pos).comp_fst ν
    refine hg.mono' (Continuous.aestronglyMeasurable (by fun_prop)) ?_
    filter_upwards [(Measure.quasiMeasurePreserving_snd (μ := μ) (ν := ν)).ae
      (ae_restrict_mem measurableSet_Ioc)] with z hz
    have hqz := hq.nonneg z.1
    show |q z.1 * exp (-(z.2 * q z.1))| ≤ q z.1 * exp (-(1 * q z.1))
    rw [abs_of_nonneg (mul_nonneg hqz (exp_pos _).le)]
    refine mul_le_mul_of_nonneg_left ?_ hqz
    rw [exp_le_exp, neg_le_neg_iff]
    nlinarith [hz.1]
  unfold Z Nm
  rw [← integral_sub (integrable_exp hq one_pos) (integrable_exp hq two_pos)]
  have h1 : ∀ x, exp (-(1 * q x)) - exp (-(2 * q x)) = ∫ s in Ioc (1 : ℝ) 2, q x * exp (-(s * q x)) := by
    intro x
    rw [← intervalIntegral.integral_of_le one_le_two, inner_ftc, one_mul]
  simp_rw [h1]
  rw [integral_integral_swap hint, intervalIntegral.integral_of_le one_le_two]

/-- **The equipartition identity at `β = 1`:** `N(1) = (d/p) Z(1)`. -/
theorem Nm_one [Nontrivial E] {q : E → ℝ} {p : ℝ} (hq : HomogCost q p) :
    Nm μ q 1 = (finrank ℝ E / p) * Z μ q 1 := by
  set a : ℝ := -(finrank ℝ E / p) with ha_def
  have hd : (0 : ℝ) < finrank ℝ E := Nat.cast_pos.mpr Module.finrank_pos
  have ha : a < 0 := by rw [ha_def]; exact neg_neg_of_pos (div_pos hd hq.p_pos)
  have hkey := Z_sub_eq_integral_Nm (μ := μ) hq
  rw [Z_scale hq two_pos] at hkey
  have hcongr : ∫ s in (1 : ℝ)..2, Nm μ q s = ∫ s in (1 : ℝ)..2, Nm μ q 1 * s ^ (a - 1) := by
    refine intervalIntegral.integral_congr (fun s hs => ?_)
    have hs0 : 0 < s := by
      rw [uIcc_of_le one_le_two] at hs; linarith [hs.1]
    rw [Nm_scale hq hs0, rpow_sub_one hs0.ne']
    field_simp
    rw [ha_def]; ring
  rw [hcongr, intervalIntegral.integral_const_mul,
    integral_rpow (Or.inr ⟨by linarith, by simp⟩)] at hkey
  simp only [sub_add_cancel, one_rpow] at hkey
  have h2 : (2 : ℝ) ^ a < 1 := rpow_lt_one_of_one_lt_of_neg one_lt_two ha
  have hne : (1 : ℝ) - 2 ^ a ≠ 0 := by linarith
  rw [← ha_def] at hkey
  have h' : Z μ q 1 * (1 - 2 ^ a) * a = Nm μ q 1 * (2 ^ a - 1) := by
    have h0 : Z μ q 1 * (1 - 2 ^ a) = Nm μ q 1 * ((2 ^ a - 1) / a) := by rw [← hkey]; ring
    rw [h0, mul_div_assoc', div_mul_cancel₀ _ ha.ne]
  have : (1 - 2 ^ a) * (Nm μ q 1 + a * Z μ q 1) = 0 := by
    linear_combination h'
  rcases mul_eq_zero.mp this with h | h
  · exact absurd h hne
  · rw [ha_def] at h; linarith

/-- **Equipartition (Gibbs excess).**  For `β > 0`, the Gibbs mean of a
continuous, nonnegative, degree-`p` homogeneous cost `q` that is positive
away from `0`, on a finite-dimensional space of dimension `d ≥ 1` with
Lebesgue/Haar measure, is `d/(pβ)`:
`(∫ q e^{-βq}) / (∫ e^{-βq}) = d / (p β)`. -/
theorem gibbs_mean_homog [Nontrivial E] {q : E → ℝ} {p : ℝ} (hq : HomogCost q p) {β : ℝ}
    (hβ : 0 < β) :
    Nm μ q β / Z μ q β = finrank ℝ E / (p * β) := by
  have hZ : 0 < Z μ q 1 := integral_exp_pos (integrable_exp hq one_pos)
  have hb : 0 < β ^ (-(finrank ℝ E / p) : ℝ) := rpow_pos_of_pos hβ _
  rw [Nm_scale hq hβ, Z_scale hq hβ, Nm_one hq]
  field_simp

/-- **Stationary excess of a Gibbs distribution (general form).**  Let
`J x = J* + q (x - x*)` with `q` as in `HomogCost q p`.  For `β > 0`, the
mean of `J` under `π ∝ exp(-β J)` (Lebesgue/Haar reference measure on a
space of dimension `d ≥ 1`) exceeds the minimum `J*` by exactly `d/(pβ)`. -/
theorem gibbs_excess [Nontrivial E] {q J : E → ℝ} {p Jstar β : ℝ} {xstar : E}
    (hq : HomogCost q p) (hJ : ∀ x, J x = Jstar + q (x - xstar)) (hβ : 0 < β) :
    (∫ x, J x * exp (-(β * J x)) ∂μ) / (∫ x, exp (-(β * J x)) ∂μ) - Jstar =
      finrank ℝ E / (p * β) := by
  have hnum : (∫ x, J x * exp (-(β * J x)) ∂μ) =
      exp (-(β * Jstar)) * (Jstar * Z μ q β + Nm μ q β) := by
    have := integral_sub_right_eq_self (μ := μ)
      (fun y => (Jstar + q y) * exp (-(β * (Jstar + q y)))) xstar
    simp only [← hJ] at this
    rw [this]
    have he : ∀ y, (Jstar + q y) * exp (-(β * (Jstar + q y))) =
        exp (-(β * Jstar)) * Jstar * exp (-(β * q y)) +
          exp (-(β * Jstar)) * (q y * exp (-(β * q y))) := by
      intro y; rw [mul_add β, neg_add, exp_add]; ring
    simp_rw [he]
    rw [integral_add ((integrable_exp hq hβ).const_mul _) ((integrable_moment hq hβ).const_mul _),
      integral_const_mul, integral_const_mul]
    unfold Z Nm; ring
  have hden : (∫ x, exp (-(β * J x)) ∂μ) = exp (-(β * Jstar)) * Z μ q β := by
    have := integral_sub_right_eq_self (μ := μ)
      (fun y => exp (-(β * (Jstar + q y)))) xstar
    simp only [← hJ] at this
    rw [this]
    have he : ∀ y, exp (-(β * (Jstar + q y))) = exp (-(β * Jstar)) * exp (-(β * q y)) := by
      intro y; rw [mul_add β, neg_add, exp_add]
    simp_rw [he]
    rw [integral_const_mul (μ := μ)]; rfl
  have hZ : 0 < Z μ q β := integral_exp_pos (integrable_exp hq hβ)
  rw [hnum, hden, ← gibbs_mean_homog (μ := μ) hq hβ]
  have hc : 0 < exp (-(β * Jstar)) := exp_pos _
  field_simp
  ring

open Matrix in
/-- A positive definite quadratic form `½ xᵀ H x` on `ℝ^d` satisfies
`HomogCost` with `p = 2`. -/
lemma homogCost_quadratic {d : ℕ} (H : Matrix (Fin d) (Fin d) ℝ) (hH : H.PosDef) :
    HomogCost (fun x : Fin d → ℝ => (1 / 2) * (x ⬝ᵥ (H *ᵥ x))) 2 where
  p_pos := two_pos
  cont := by
    have : Continuous fun x : Fin d → ℝ => x ⬝ᵥ (H *ᵥ x) :=
      continuous_id.dotProduct (continuous_const.matrix_mulVec continuous_id)
    exact continuous_const.mul this
  nonneg := by
    intro x
    rcases eq_or_ne x 0 with rfl | hx
    · simp
    · have := hH.dotProduct_mulVec_pos hx
      simp only [star_trivial] at this
      positivity
  pos := by
    intro x hx
    have := hH.dotProduct_mulVec_pos hx
    simp only [star_trivial] at this
    positivity
  homog := by
    intro r _ x
    rw [Matrix.mulVec_smul, smul_dotProduct, dotProduct_smul, rpow_two]
    simp only [smul_eq_mul]
    ring

open Matrix in
/-- **Selection-axioms stationary excess, `d/(2β)`.**  For a quadratic
positive definite cost `J(x) = J* + ½ (x - x*)ᵀ H (x - x*)` on `ℝ^d`
(`d ≥ 1`) and the Boltzmann/Gibbs distribution `π ∝ exp(-β J)` with
`β > 0`, `E_π[J] - J* = d / (2β)`. -/
theorem gibbs_excess_quadratic {d : ℕ} [NeZero d] (H : Matrix (Fin d) (Fin d) ℝ) (hH : H.PosDef)
    (Jstar β : ℝ) (xstar : Fin d → ℝ) (hβ : 0 < β) :
    let J : (Fin d → ℝ) → ℝ := fun x => Jstar + (1 / 2) * ((x - xstar) ⬝ᵥ (H *ᵥ (x - xstar)))
    (∫ x, J x * exp (-(β * J x))) / (∫ x, exp (-(β * J x))) - Jstar = d / (2 * β) := by
  intro J
  have h := gibbs_excess (μ := (volume : Measure (Fin d → ℝ))) (homogCost_quadratic H hH)
    (J := J) (Jstar := Jstar) (xstar := xstar) (fun x => rfl) hβ
  rwa [Module.finrank_fin_fun] at h

end Equipartition
