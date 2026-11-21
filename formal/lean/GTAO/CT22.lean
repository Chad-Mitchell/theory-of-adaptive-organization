/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lean 4 formalization of the elementary comparisons in THEORY CT22,
for OPEN_WORK T19.
-/
module

public import Mathlib.Analysis.SpecialFunctions.Log.Basic
public import Mathlib.Tactic.Linarith

/-!
# CT22: the price of survival (certified feasible set)

From THEORY.md Appendix B.9 (CT22):

> Let \(\theta(\mathcal D)\) be the Lundberg exponent,
> \(B_{\min}=\ln(1/\varepsilon_r)/\max_{\mathcal D}\theta\) and
> \(B_{\mathrm{slack}}=\ln(1/\varepsilon_r)/\theta(\mathcal D_E)\), with
> \(\mathcal D_E\) the expected-cost optimum.  For \(B<B_{\min}\) no design
> is feasible.  For \(B\ge B_{\mathrm{slack}}\) the constraint is slack and
> \(\mathcal D_E\) is optimal (\(\mu_s=0\)).

THEORY is explicit that "no design is feasible below \(B_{\min}\)" means no
design is *certified* by the Lundberg bound (a sufficient condition), not
that every design ruins.  This file formalizes that certified-feasibility
comparison, and composes it with certification at \(B_{\mathrm{slack}}\):
for \(B\ge B_{\mathrm{slack}}\), the expected-cost optimum is certified
and is therefore a constrained optimum.  The in-between binding region,
the multiplier \(\mu_s=-m'/\theta'\), and quasiconvexity hypotheses are
**not** formalized.
-/

@[expose] public section

variable {𝒟 : Type*} [Fintype 𝒟] [Nonempty 𝒟]

/-- A design is Lundberg-certified at buffer `B` when `θ d * B ≥ log(1/ε)`. -/
def LundbergCertified (θ : 𝒟 → ℝ) (ε B : ℝ) (d : 𝒟) : Prop :=
  Real.log (1 / ε) ≤ θ d * B

/-- The largest Lundberg exponent on a nonempty finite design set. -/
noncomputable def thetaMax (θ : 𝒟 → ℝ) : ℝ :=
  (Finset.univ.image θ).max'
    (Finset.image_nonempty.mpr Finset.univ_nonempty)

lemma theta_le_max (θ : 𝒟 → ℝ) (d : 𝒟) : θ d ≤ thetaMax θ :=
  Finset.le_max' _ _ (Finset.mem_image.mpr ⟨d, Finset.mem_univ d, rfl⟩)

/-- \(B_{\min}=\log(1/\varepsilon)/\max\theta\). -/
noncomputable def Bmin (θ : 𝒟 → ℝ) (ε : ℝ) : ℝ :=
  Real.log (1 / ε) / thetaMax θ

/-- \(B_{\mathrm{slack}}=\log(1/\varepsilon)/\theta(\mathcal D_E)\). -/
noncomputable def Bslack (θ : 𝒟 → ℝ) (ε : ℝ) (dE : 𝒟) : ℝ :=
  Real.log (1 / ε) / θ dE

lemma log_one_div_pos {ε : ℝ} (hε0 : 0 < ε) (hε1 : ε < 1) :
    0 < Real.log (1 / ε) :=
  Real.log_pos (one_lt_one_div hε0 hε1)

/-- Under the standing hypotheses `0 < ε < 1` and `0 < max θ`, `Bmin` is
positive, so the range `0 ≤ B < Bmin` is nonempty. -/
lemma Bmin_pos (θ : 𝒟 → ℝ) {ε : ℝ} (hε0 : 0 < ε) (hε1 : ε < 1)
    (hθ : 0 < thetaMax θ) :
    0 < Bmin θ ε :=
  div_pos (log_one_div_pos hε0 hε1) hθ

/-- CT22: below `Bmin`, no design is Lundberg-certified.  The comparison
is algebraic in `log(1/ε)` and does not need `0 < ε < 1`; THEORY assumes
that range so that `Bmin` is positive (`Bmin_pos`) and the interval
`0 ≤ B < Bmin` is inhabited. -/
theorem not_certified_below_Bmin (θ : 𝒟 → ℝ) {ε B : ℝ}
    (hθ : 0 < thetaMax θ)
    (hB0 : 0 ≤ B) (hB : B < Bmin θ ε) (d : 𝒟) :
    ¬ LundbergCertified θ ε B d := by
  intro hcert
  have hle : θ d ≤ thetaMax θ := theta_le_max θ d
  have hprod : θ d * B ≤ thetaMax θ * B :=
    mul_le_mul_of_nonneg_right hle hB0
  have hstrict : thetaMax θ * B < thetaMax θ * Bmin θ ε :=
    mul_lt_mul_of_pos_left hB hθ
  have hcancel : thetaMax θ * Bmin θ ε = Real.log (1 / ε) :=
    mul_div_cancel₀ _ hθ.ne'
  have : θ d * B < Real.log (1 / ε) := by linarith [hprod, hstrict, hcancel]
  exact (not_le_of_gt this) hcert

omit [Fintype 𝒟] [Nonempty 𝒟] in
/-- CT22: at or above `Bslack`, the expected-cost optimum `dE` is certified,
provided its own exponent is positive. -/
theorem certified_at_Bslack (θ : 𝒟 → ℝ) (ε : ℝ) {dE : 𝒟} {B : ℝ}
    (hθE : 0 < θ dE) (hB : Bslack θ ε dE ≤ B) :
    LundbergCertified θ ε B dE := by
  have : θ dE * Bslack θ ε dE = Real.log (1 / ε) :=
    mul_div_cancel₀ _ hθE.ne'
  have : θ dE * Bslack θ ε dE ≤ θ dE * B :=
    mul_le_mul_of_nonneg_left hB hθE.le
  simp only [LundbergCertified]
  linarith

omit [Fintype 𝒟] [Nonempty 𝒟] in
/-- CT22, slack case: for `B ≥ B_slack`, the expected-cost optimum `dE`
is Lundberg-certified and is therefore optimal among certified designs.
Composes `certified_at_Bslack` with the observation that an unconstrained
minimizer is a constrained minimizer once it is feasible.  No KKT is
used; the binding region is not formalized. -/
theorem expected_cost_opt_at_or_above_Bslack
    (J : 𝒟 → ℝ) (θ : 𝒟 → ℝ) (ε : ℝ) {dE : 𝒟} {B : ℝ}
    (hE : ∀ d : 𝒟, J dE ≤ J d)
    (hθE : 0 < θ dE)
    (hB : Bslack θ ε dE ≤ B) :
    LundbergCertified θ ε B dE ∧
      ∀ d : 𝒟, LundbergCertified θ ε B d → J dE ≤ J d :=
  ⟨certified_at_Bslack θ ε hθE hB, fun d _ => hE d⟩

/-- `Bmin ≤ Bslack` when `θ dE` attains (or is at most) the maximum exponent.
In particular this holds for every `dE`.  The positivity of `thetaMax`
follows from `0 < θ dE`. -/
theorem Bmin_le_Bslack (θ : 𝒟 → ℝ) (ε : ℝ) (dE : 𝒟)
    (hθE : 0 < θ dE)
    (hε0 : 0 < ε) (hε1 : ε < 1) :
    Bmin θ ε ≤ Bslack θ ε dE := by
  have hle : θ dE ≤ thetaMax θ := theta_le_max θ dE
  have hL : 0 < Real.log (1 / ε) := log_one_div_pos hε0 hε1
  simp only [Bmin, Bslack]
  exact div_le_div_of_nonneg_left hL.le hθE hle
