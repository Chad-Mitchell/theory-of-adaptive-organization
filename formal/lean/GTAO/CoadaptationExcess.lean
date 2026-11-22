/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Theorem CA1b and Corollary CA1c of `theory/COADAPTATION.md` (CLAIM_MAP U2).
For OPEN_WORK T19.
-/
module

public import GTAO.Coadaptation
public import GTAO.Equipartition
public import Mathlib.Algebra.Order.Star.Real
public import Mathlib.LinearAlgebra.Matrix.Trace
public import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
public import Mathlib.LinearAlgebra.Matrix.PosDef
public import Mathlib.MeasureTheory.Measure.Haar.NormedSpace
public import Mathlib.Tactic.NormNum
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.Ring

/-!
# CA1b / CA1c: per-party Boltzmann and team excess

`theory/COADAPTATION.md` Theorem CA1b and Corollary CA1c, CLAIM_MAP U2.

From an exact potential, `Ψ - β_i J_i` is independent of party `i`'s
design, so the Gibbs law is conditionally Boltzmann in `J_i`.  For a
quadratic potential the Gibbs excess at strength `1` is `d/2`
(`ca1b_potential_excess`, wrapping `Equipartition.gibbs_excess_quadratic`).
The team split takes the entrywise second-moment sum of the quadratic
`½ δᵀ H_T δ` and the covariance identity `HΨ P = I`, and identifies the
excess with the potential-to-team gap plus `½ Tr(H_T (∇²Ψ)⁻¹)`.

CA1c: aligned shares `J_i = s_i J_T + h_i(x_{-i})` give exact potential
`γ J_T` when `β_i s_i = γ`; with `h_i = 0` and `∑ s_i = 1` one has
`∑_i J_i = J_T` at every state, so the potential-to-team gap vanishes
when the potential minimizer is a minimizer of `J_T`.  The fractional
form `(E[J_T]−J_T*)/J_T* = d/(2σ N_e)` is the cancellation of `J_T*`
between the two inputs `E[J_T]−J_T* = d/(2γ)` and `γ = σ N_e / J_T*`
(A2-L itself is not formalized).
-/

@[expose] public section

set_option linter.unusedSectionVars false
set_option linter.unusedVariables false

open scoped BigOperators
open Finset Function Real Matrix MeasureTheory

namespace Coadaptation

variable {ι : Type*} [DecidableEq ι] {S : ι → Type*}
variable {β : ι → ℝ} {J : ι → (∀ i, S i) → ℝ}

/-- **CA1b (1), algebraic half.**  An exact potential differs from
`β_i J_i` by a function of the other parties' designs only. -/
theorem potential_shift_independent {Ψ : (∀ i, S i) → ℝ}
    (hΨ : IsExactPotential β J Ψ) (x : ∀ i, S i) (i : ι) (s : S i) :
    Ψ (update x i s) - β i * J i (update x i s) = Ψ x - β i * J i x := by
  have := hΨ x i s
  linarith

/-- **CA1b (1), conditional Boltzmann.**  For the unnormalized Gibbs
weight `π = exp(−Ψ)`, a unilateral change of party `i` multiplies `π`
by `exp(−β_i Δ J_i)`. -/
theorem conditional_boltzmann {Ψ : (∀ i, S i) → ℝ}
    (hΨ : IsExactPotential β J Ψ) (x : ∀ i, S i) (i : ι) (s : S i) :
    exp (-Ψ (update x i s)) =
      exp (-(β i * (J i (update x i s) - J i x))) * exp (-Ψ x) := by
  have h := hΨ x i s
  have : -Ψ (update x i s) = -(β i * (J i (update x i s) - J i x)) + -Ψ x := by
    linarith
  rw [this, exp_add]

/-- The entrywise second-moment sum that is `Tr(H P)`. -/
lemma trace_mul_eq_sum {d : ℕ} (H P : Matrix (Fin d) (Fin d) ℝ) :
    trace (H * P) = ∑ i, ∑ j, H i j * P j i := by
  simp [Matrix.trace, Matrix.mul_apply]

/-- **CA1b (2).**  For a confining quadratic potential, the Gibbs excess
at strength `1` is `d/2`.  This is `Equipartition.gibbs_excess_quadratic`
(SA1b) at `β = 1`, which is the proof route in
`theory/COADAPTATION.md` CA1b (2). -/
theorem ca1b_potential_excess {d : ℕ} [NeZero d]
    (H : Matrix (Fin d) (Fin d) ℝ) (hH : H.PosDef)
    (PsiStar : ℝ) (xStar : Fin d → ℝ) :
    let Ψ : (Fin d → ℝ) → ℝ := fun x =>
      PsiStar + (1 / 2) * ((x - xStar) ⬝ᵥ (H *ᵥ (x - xStar)))
    (∫ x, Ψ x * exp (-((1 : ℝ) * Ψ x))) / (∫ x, exp (-((1 : ℝ) * Ψ x))) - PsiStar
      = (d : ℝ) / (2 * 1) :=
  Equipartition.gibbs_excess_quadratic H hH PsiStar (1 : ℝ) xStar (by norm_num)

/-- **CA1b (3), team split.**  If the mean of the quadratic `½ δᵀ H_T δ`
is the second-moment entry sum against `P`, and `HΨ P = I` (so
`P = (∇²Ψ)⁻¹`), the team excess is the potential-to-team gap plus
`½ Tr(H_T (∇²Ψ)⁻¹)`. -/
theorem ca1b_team_split {d : ℕ}
    (HT HΨ P : Matrix (Fin d) (Fin d) ℝ) {eJT jTpsi jTmin : ℝ}
    (hquad : eJT = jTpsi + (2 : ℝ)⁻¹ * ∑ i, ∑ j, HT i j * P j i)
    (hcov : HΨ * P = 1) :
    P = HΨ⁻¹ ∧
      eJT - jTmin = (jTpsi - jTmin) + (2 : ℝ)⁻¹ * trace (HT * HΨ⁻¹) := by
  have hP : P = HΨ⁻¹ := (Matrix.inv_eq_right_inv hcov).symm
  have htr : (∑ i, ∑ j, HT i j * P j i) = trace (HT * P) :=
    (trace_mul_eq_sum HT P).symm
  refine ⟨hP, ?_⟩
  have : eJT = jTpsi + (2 : ℝ)⁻¹ * trace (HT * HΨ⁻¹) := by
    rw [hquad, htr, hP]
  rw [this]
  ring

/-- **CA1c, exact potential.**  If `J_i = s_i J_T + h_i` with `h_i` independent
of party `i`'s own design, and `β_i s_i = γ` for every party, then
`γ J_T` is an exact potential for `(β_i J_i)`. -/
theorem ca1c_potential {s : ι → ℝ} {JT : (∀ i, S i) → ℝ}
    {h : ι → (∀ i, S i) → ℝ} {γ : ℝ}
    (hJ : ∀ x i, J i x = s i * JT x + h i x)
    (hh : ∀ x i t, h i (update x i t) = h i x)
    (hγ : ∀ i, β i * s i = γ) :
    IsExactPotential β J (fun x => γ * JT x) := by
  intro x i t
  have hJΔ : J i (update x i t) - J i x =
      s i * (JT (update x i t) - JT x) := by
    rw [hJ, hJ, hh]
    ring
  rw [hJΔ, ← mul_assoc, hγ]
  ring

/-- **CA1c, summed cost.**  If `h_i = 0` and `∑ s_i = 1`, then
`∑_i J_i = J_T` at every state. -/
theorem ca1c_summed_cost {s : ι → ℝ} {JT : (∀ i, S i) → ℝ}
    (hJ : ∀ x i, J i x = s i * JT x)
    [Fintype ι] (hsum : (∑ i, s i) = 1) (x : ∀ i, S i) :
    (∑ i, J i x) = JT x := by
  have : (∑ i, J i x) = (∑ i, s i) * JT x := by
    simp_rw [hJ, ← sum_mul]
  rw [this, hsum, one_mul]

/-- **CA1c, gap vanishes.**  Under `ca1c_summed_cost`, if the potential
minimizer is a minimizer of `J_T` (input `hmin`), the potential-to-team
gap at that state is zero. -/
theorem ca1c_gap_zero {s : ι → ℝ} {JT : (∀ i, S i) → ℝ} {xPsi : ∀ i, S i}
    {jTmin : ℝ}
    (hJ : ∀ x i, J i x = s i * JT x)
    [Fintype ι]
    (hsum : (∑ i, s i) = 1)
    (hmin : JT xPsi = jTmin) :
    (∑ i, J i xPsi) - jTmin = 0 := by
  rw [ca1c_summed_cost hJ hsum xPsi, hmin, sub_self]

/-- **CA1c, fractional excess.**  This is the cancellation of `J_T*`
between the two inputs `E[J_T]−J_T* = d/(2γ)` and `γ = σ N_e / J_T*`.
The A2-L identification of `γ` and the potential excess itself are not
proved here. -/
theorem ca1c_fraction {d eJT jTstar γ σNe : ℝ}
    (hj : 0 < jTstar) (_hσ : 0 < σNe)
    (hexcess : eJT - jTstar = d * (2 : ℝ)⁻¹ * γ⁻¹)
    (hγ : γ = σNe * jTstar⁻¹) :
    (eJT - jTstar) * jTstar⁻¹ = d * (2 : ℝ)⁻¹ * σNe⁻¹ := by
  have hγinv : γ⁻¹ = σNe⁻¹ * jTstar := by
    rw [hγ, mul_inv, inv_inv]
  have : (eJT - jTstar) * jTstar⁻¹ =
      d * (2 : ℝ)⁻¹ * (σNe⁻¹ * jTstar) * jTstar⁻¹ := by
    rw [hexcess, hγinv, mul_assoc]
  calc
    (eJT - jTstar) * jTstar⁻¹
        = d * (2 : ℝ)⁻¹ * (σNe⁻¹ * jTstar) * jTstar⁻¹ := this
    _ = d * (2 : ℝ)⁻¹ * σNe⁻¹ * (jTstar * jTstar⁻¹) := by ring
    _ = d * (2 : ℝ)⁻¹ * σNe⁻¹ * 1 := by rw [mul_inv_cancel₀ hj.ne']
    _ = d * (2 : ℝ)⁻¹ * σNe⁻¹ := by ring

end Coadaptation
