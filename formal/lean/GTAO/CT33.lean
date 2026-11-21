/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lean 4 formalization of THEORY CT33, for OPEN_WORK T19.
-/
module

public import GTAO.Cost
public import Mathlib.Tactic.Linarith

/-!
# CT33: judgment spend rises with stakes

From THEORY.md Appendix B.10 (CT33):

> Any design set \(\mathcal D\) with \(J(\mathcal D;w)=S(\mathcal D)+w\cdot E(\mathcal D)\),
> \(S\) the spend on judgment and \(E\) the expected error per unit stake; stakes \(w\),
> prices fixed.  For \(w_1<w_2\) with optimal designs \(\mathcal D_1,\mathcal D_2\):
> \(S_1+w_1 E_1\le S_2+w_1 E_2\) and \(S_2+w_2 E_2\le S_1+w_2 E_1\).  Adding gives
> \((w_2-w_1)(E_2-E_1)\le 0\), so **\(E^*(w)\) is nonincreasing**; then
> \(S_2-S_1\ge w_1(E_1-E_2)\ge 0\), so **\(S^*(w)\) is nondecreasing**.
> \(J^*(w)\) is concave with slope \(E^*\) (envelope).
>
> The design set must not depend on \(w\): the ruin constraint must be slack at
> the stakes compared (\(B\ge B_{\mathrm{slack}}\), CT22) or absent.
> Stakes are taken nonnegative in the spend comparison (the step
> \(w_1(E_1-E_2)\ge 0\) uses \(w_1\ge 0\)).

Nothing about the world, the loss, or whether \(K\) is discrete is used.  The
result does not say that the layer count rises (reads can replace layers).
-/

@[expose] public section

namespace FiniteDesignMenu

variable {𝒟 : Type*} [Fintype 𝒟] [Nonempty 𝒟] (M : FiniteDesignMenu 𝒟)

/-- Optimality at `w₁` and `w₂` gives the two revealed-preference inequalities. -/
theorem optimality_inequalities {w1 w2 : ℝ} {d1 d2 : 𝒟}
    (h1 : M.IsOptimal w1 d1) (h2 : M.IsOptimal w2 d2) :
    M.S d1 + w1 * M.E d1 ≤ M.S d2 + w1 * M.E d2 ∧
      M.S d2 + w2 * M.E d2 ≤ M.S d1 + w2 * M.E d1 :=
  ⟨h1 d2, h2 d1⟩

/-- Adding the two optimality inequalities: `(w₂ - w₁)(E₂ - E₁) ≤ 0`. -/
theorem error_diff_sign {w1 w2 : ℝ} {d1 d2 : 𝒟}
    (h1 : M.IsOptimal w1 d1) (h2 : M.IsOptimal w2 d2) :
    (w2 - w1) * (M.E d2 - M.E d1) ≤ 0 := by
  obtain ⟨i1, i2⟩ := M.optimality_inequalities h1 h2
  linarith

/-- CT33, error: `E*(w)` is nonincreasing.  The inequality is strict in the
stakes: at a tie, two optima may share `J*` with different errors. -/
theorem error_nonincreasing {w1 w2 : ℝ} (hw : w1 < w2) {d1 d2 : 𝒟}
    (h1 : M.IsOptimal w1 d1) (h2 : M.IsOptimal w2 d2) :
    M.E d2 ≤ M.E d1 := by
  have h := M.error_diff_sign h1 h2
  have hwpos : 0 < w2 - w1 := sub_pos.mpr hw
  have : M.E d2 - M.E d1 ≤ 0 := nonpos_of_mul_nonpos_right h hwpos
  linarith

/-- From optimality at `w₁`: `S₂ - S₁ ≥ w₁ (E₁ - E₂)`. -/
theorem spend_ge_stake_times_error_drop {w1 w2 : ℝ} {d1 d2 : 𝒟}
    (h1 : M.IsOptimal w1 d1) (_h2 : M.IsOptimal w2 d2) :
    w1 * (M.E d1 - M.E d2) ≤ M.S d2 - M.S d1 := by
  have i1 : M.S d1 + w1 * M.E d1 ≤ M.S d2 + w1 * M.E d2 := h1 d2
  linarith

/-- CT33, spend: `S*(w)` is nondecreasing, for nonnegative stakes, with the
ruin constraint slack or absent (the menu does not depend on `w`).  The
stake comparison is strict, as at a tie two optima may differ in spend. -/
theorem spend_nondecreasing {w1 w2 : ℝ} (hw1 : 0 ≤ w1) (hw : w1 < w2)
    {d1 d2 : 𝒟} (h1 : M.IsOptimal w1 d1) (h2 : M.IsOptimal w2 d2) :
    M.S d1 ≤ M.S d2 := by
  have hE : M.E d2 ≤ M.E d1 := M.error_nonincreasing hw h1 h2
  have hS := M.spend_ge_stake_times_error_drop h1 h2
  have : 0 ≤ w1 * (M.E d1 - M.E d2) := mul_nonneg hw1 (sub_nonneg.mpr hE)
  linarith

/-- CT33 in units of a positive upkeep `h`: `S*/h` is nondecreasing in
`R = w/h`.  Raising `w/h` at fixed prices is the same problem as raising `w`. -/
theorem spend_nondecreasing_in_R {h w1 w2 : ℝ} (hh : 0 < h)
    (hw1 : 0 ≤ w1) (hw : w1 < w2) {d1 d2 : 𝒟}
    (h1 : M.IsOptimal w1 d1) (h2 : M.IsOptimal w2 d2) :
    M.S d1 / h ≤ M.S d2 / h :=
  div_le_div_of_nonneg_right (M.spend_nondecreasing hw1 hw h1 h2) hh.le

end FiniteDesignMenu
