/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Theorem CA1b and Corollary CA1c of `theory/COADAPTATION.md` (CLAIM_MAP U2).
For OPEN_WORK T19.
-/
module

public import GTAO.Coadaptation
public import Mathlib.Algebra.Order.Star.Real
public import Mathlib.LinearAlgebra.Matrix.Trace
public import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.Ring

/-!
# CA1b / CA1c: per-party Boltzmann and team excess

`theory/COADAPTATION.md` Theorem CA1b and Corollary CA1c, CLAIM_MAP U2.

From an exact potential, `Ψ - β_i J_i` is independent of party `i`'s
design, so the Gibbs law is conditionally Boltzmann in `J_i`.  The
quadratic mean identities (CA1b (2) and the team split) are proved from
a covariance input, in the same style as DS1: if the (centred) second
moment is `(∇²Ψ)⁻¹` and the mean excess is the corresponding trace, then
`E[Ψ]−Ψ* = d/2` and the team excess is the absolute potential-to-team
gap plus `½ Tr(H_T (∇²Ψ)⁻¹)`.

CA1c: aligned shares `J_i = s_i J_T + h_i(x_{-i})` give exact potential
`γ J_T` when `β_i s_i = γ`; with `h_i = 0` and `∑ s_i = 1` the
potential-to-team gap vanishes.  The fractional form
`(E[J_T]−J_T*)/J_T* = d/(2σ N_e)` takes `γ = σ N_e / J_T*` from A2-L as
an input (A2-L itself is not formalized).

Not formalized: the integral against a Gaussian (or Haar) measure that
supplies the covariance; that step is `Equipartition` in the
single-system case and is an input here.
-/

@[expose] public section

set_option linter.unusedSectionVars false
set_option linter.unusedVariables false

open scoped BigOperators
open Finset Function Real Matrix

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

/-- Trace of the identity on `Fin d` is `d`. -/
lemma trace_one_fin {d : ℕ} :
    trace (1 : Matrix (Fin d) (Fin d) ℝ) = (d : ℝ) := by
  rw [trace_one, Fintype.card_fin]

/-- **CA1b (2).**  Granted the mean potential excess equals
`½ Tr(H P)` and the covariance identity `H P = I`, one has
`E[Ψ]−Ψ* = d/2`. -/
theorem ca1b_potential_excess {d : ℕ}
    (H P : Matrix (Fin d) (Fin d) ℝ) {ePsi : ℝ}
    (hcov : H * P = 1)
    (hexcess : ePsi = (2 : ℝ)⁻¹ * trace (H * P)) :
    ePsi = (2 : ℝ)⁻¹ * d := by
  rw [hexcess, hcov, trace_one_fin]

/-- **CA1b (3), team split.**  Granted the quadratic identity
`E[J_T] = J_T(x^Ψ) + ½ Tr(H_T P)` and `P = HΨ⁻¹` (as `HΨ P = I`),
the team excess is the absolute potential-to-team gap plus the scatter
`½ Tr(H_T (∇²Ψ)⁻¹)`. -/
theorem ca1b_team_split {d : ℕ}
    (HT HΨ P : Matrix (Fin d) (Fin d) ℝ) {eJT jTpsi jTmin scatter : ℝ}
    (hquad : eJT = jTpsi + (2 : ℝ)⁻¹ * trace (HT * P))
    (_hcov : HΨ * P = 1)
    (hsc : scatter = (2 : ℝ)⁻¹ * trace (HT * P)) :
    eJT - jTmin = (jTpsi - jTmin) + scatter := by
  rw [hquad, hsc]
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

/-- **CA1c, gap vanishes.**  If `h_i = 0` and `∑ s_i = 1`, the parties'
summed cost is `J_T`, so the potential-to-team gap is zero once the
potential minimizer is a minimizer of `J_T`. -/
theorem ca1c_gap_zero {s : ι → ℝ} {JT : (∀ i, S i) → ℝ} {xPsi : ∀ i, S i}
    {jTmin : ℝ}
    (hJ : ∀ x i, J i x = s i * JT x)
    [Fintype ι]
    (hsum : (∑ i, s i) = 1)
    (hmin : JT xPsi = jTmin) :
    (∑ i, J i xPsi) - jTmin = 0 := by
  have : (∑ i, J i xPsi) = JT xPsi := by
    have : (∑ i, J i xPsi) = (∑ i, s i) * JT xPsi := by
      simp_rw [hJ, ← sum_mul]
    rw [this, hsum, one_mul]
  rw [this, hmin, sub_self]

/-- **CA1c, fractional excess.**  Given the potential excess `d/(2γ)`
and the A2-L identification `γ = σ N_e / J_T*` as inputs,
`(E[J_T]−J_T*)/J_T* = d/(2σ N_e)`. -/
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
