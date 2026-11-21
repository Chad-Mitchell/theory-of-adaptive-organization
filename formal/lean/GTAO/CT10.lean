/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lean 4 formalization of THEORY CT10, for OPEN_WORK T19.
-/
module

public import Mathlib.Algebra.Order.Archimedean.Real.Basic
public import Mathlib.Tactic.Linarith

/-!
# CT10: effort rises with stakes

From THEORY.md Appendix B (CT10):

> With check frequency \(f\) and stake \(w\), \(J(f;w)=c\cdot f+w\cdot A(\lambda/f)\).
> The minimizing \(f\) is nondecreasing in \(w\).

The written proof is that `A` nondecreasing makes `A(λ/f)` nonincreasing in
`f`, so `J` has decreasing differences in `(f, w)`, and Topkis (1978) applies.
This file proves the decreasing-differences step and the resulting monotone
comparative static on a finite set of frequencies (the discrete Topkis
conclusion used for designs).  The argument needs only that error is
nonincreasing along a frequency coordinate and that the check price `c` is
positive.
-/

@[expose] public section

/-- Checking cost at frequency `f` and stake `w`: price `c` times a
frequency coordinate, plus `w` times an error that does not increase with
that coordinate. -/
def effortJ {F : Type*} (c : ℝ) (err : F → ℝ) (coord : F → ℝ) (w : ℝ) (f : F) : ℝ :=
  c * coord f + w * err f

/-- Decreasing differences in `(f, w)` whenever error is nonincreasing
along the frequency coordinate. -/
theorem effortJ_decreasing_differences {F : Type*} (c : ℝ) (err : F → ℝ)
    (coord : F → ℝ) {f f' : F} (hErr : err f' ≤ err f)
    {w w' : ℝ} (hw : w ≤ w') :
    effortJ c err coord w' f' - effortJ c err coord w' f ≤
      effortJ c err coord w f' - effortJ c err coord w f := by
  simp only [effortJ]
  nlinarith

/-- CT10, discrete Topkis: if `f₁` is optimal at `w₁` and `f₂` is optimal at
`w₂`, with `w₁ < w₂` and a positive check price, then the frequency
coordinate does not fall. -/
theorem effort_nondecreasing {F : Type*} (c : ℝ) (hc : 0 < c)
    (err : F → ℝ) (coord : F → ℝ)
    (hErr : ∀ f f' : F, coord f ≤ coord f' → err f' ≤ err f)
    {w1 w2 : ℝ} (hw : w1 < w2) {f1 f2 : F}
    (h1 : ∀ f : F, effortJ c err coord w1 f1 ≤ effortJ c err coord w1 f)
    (h2 : ∀ f : F, effortJ c err coord w2 f2 ≤ effortJ c err coord w2 f) :
    coord f1 ≤ coord f2 := by
  by_contra hlt
  have hf : coord f2 < coord f1 := lt_of_not_ge hlt
  have hErr21 : err f1 ≤ err f2 := hErr f2 f1 hf.le
  have i1 := h1 f2
  have i2 := h2 f1
  have hsum : (w2 - w1) * (err f2 - err f1) ≤ 0 := by
    simp only [effortJ] at i1 i2
    linarith
  have hwpos : 0 < w2 - w1 := sub_pos.mpr hw
  have hE : err f2 - err f1 ≤ 0 := nonpos_of_mul_nonpos_right hsum hwpos
  have hEeq : err f1 = err f2 := le_antisymm hErr21 (sub_nonpos.mp hE)
  -- With equal errors, optimality at w₁ is c * coord f1 ≤ c * coord f2.
  have : c * coord f1 ≤ c * coord f2 := by
    simp only [effortJ, hEeq] at i1
    linarith
  have : coord f1 ≤ coord f2 := (mul_le_mul_iff_right₀ hc).mp this
  exact (not_le_of_gt hf) this
