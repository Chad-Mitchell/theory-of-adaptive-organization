/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lean 4 formalization of the convex-lower-bound structure of THEORY CT4,
for OPEN_WORK T19.
-/
module

public import Mathlib.Analysis.Convex.Function
public import Mathlib.Analysis.Convex.Slope
public import Mathlib.Algebra.Order.Archimedean.Real.Basic
public import Mathlib.Tactic.Linarith

/-!
# CT4: the first bit must pay (convex lower bound)

From THEORY.md Appendix B.1 (CT4):

> Let \(IB(I)=\sup\{I(M;X_{t+k}):I(M;\mathrm{past})\le I\}\), the predictive
> information-bottleneck curve (concave, nondecreasing).  Then
> \(L(I)=D(IB(I))+\kappa I\) is a convex lower bound on cost at memory size
> \(I\), and its minimizer is positive iff \(\kappa<-(D\circ IB)'(0^+)\).

This file formalizes that convex lower-bound structure:

* `D` convex and nonincreasing, `IB` concave (on `[0, ∞)`), imply `D ∘ IB`
  convex, and so `L(I)=D(IB(I))+κ I` is convex (the linear term is affine,
  hence convex at every sign of `κ`);
* a convex `L` on `[0, ∞)` has `0` as a minimizer iff every right slope
  from `0` is nonnegative, and therefore has a strictly positive minimizer
  (when one exists) iff some right slope from `0` is negative.

The Gaussian AR(1) closed form
`I* = (1/2) log₂(2 ln 2 · a² · Var / κ)` is not formalized here
(see `formal/lean/README.md`).
-/

@[expose] public section

open Set

/-- A cleaner affine identity. -/
lemma affine_mul_combo (κ a b x y : ℝ) :
    κ * (a * x + b * y) = a * (κ * x) + b * (κ * y) := by
  ring

lemma convexOn_affine_mul' (κ : ℝ) (s : Set ℝ) (hs : Convex ℝ s) :
    ConvexOn ℝ s (fun I : ℝ => κ * I) := by
  refine ⟨hs, fun x _ y _ a b _ _ _hab => (affine_mul_combo κ a b x y).le⟩

/-- CT4, convex lower bound: if `D` is convex and nonincreasing on the
image of `IB`, and `IB` is concave on `s`, then `D ∘ IB` is convex on `s`. -/
theorem D_comp_IB_convex {s : Set ℝ} {D IB : ℝ → ℝ}
    (hD : ConvexOn ℝ (IB '' s) D) (hIB : ConcaveOn ℝ s IB)
    (hDanti : AntitoneOn D (IB '' s)) :
    ConvexOn ℝ s (D ∘ IB) :=
  hD.comp_concaveOn hIB hDanti

/-- CT4, `L(I) = D(IB(I)) + κ I` is convex on `s`. -/
theorem L_convex {s : Set ℝ} {D IB : ℝ → ℝ} (κ : ℝ)
    (hD : ConvexOn ℝ (IB '' s) D) (hIB : ConcaveOn ℝ s IB)
    (hDanti : AntitoneOn D (IB '' s)) :
    ConvexOn ℝ s (fun I => D (IB I) + κ * I) := by
  have hcomp : ConvexOn ℝ s (D ∘ IB) := D_comp_IB_convex hD hIB hDanti
  have haff : ConvexOn ℝ s (fun I => κ * I) := convexOn_affine_mul' κ s hIB.1
  have hadd := hcomp.add haff
  change ConvexOn ℝ s (D ∘ IB + fun I => κ * I)
  exact hadd

/-- For a convex function on `[0, ∞)`, the right slopes from `0` are
nonnegative iff `0` is a minimizer on `[0, ∞)`. -/
theorem zero_isMinOn_iff {L : ℝ → ℝ} :
    IsMinOn L (Ici (0 : ℝ)) 0 ↔ ∀ x > 0, 0 ≤ (L x - L 0) / x := by
  constructor
  · intro hmin x hx
    have : L 0 ≤ L x := hmin hx.le
    exact div_nonneg (sub_nonneg.mpr this) hx.le
  · intro hslopes y hy
    rcases eq_or_lt_of_le hy with h0 | hpos
    · simp [h0.symm]
    · have hdiv := (le_div_iff₀ hpos).mp (hslopes y hpos)
      have : 0 ≤ L y - L 0 := by
        simpa using hdiv
      exact sub_nonneg.mp this

/-- If some right slope from `0` is negative, then `0` is not a minimizer,
and any minimizer on `[0, ∞)` is strictly positive.  This is the
"minimizer is positive iff the right derivative at 0 is negative" direction
used in CT4, stated with slopes (the right derivative need not exist as a
real number). -/
theorem convexOn_pos_min_of_neg_right_slope {L : ℝ → ℝ}
    (_hL : ConvexOn ℝ (Ici (0 : ℝ)) L) {x : ℝ} (hx : 0 < x)
    (hslope : (L x - L 0) / x < 0) {y : ℝ} (_hy : y ∈ Ici (0 : ℝ))
    (hmin : IsMinOn L (Ici (0 : ℝ)) y) :
    0 < y := by
  have h0not : ¬ IsMinOn L (Ici (0 : ℝ)) 0 := by
    intro hmin0
    have : 0 ≤ (L x - L 0) / x :=
      (zero_isMinOn_iff).mp hmin0 x hx
    linarith
  have hy0 : y ≠ 0 := by
    intro h
    exact h0not (by simpa [h] using hmin)
  exact (eq_or_lt_of_le _hy).resolve_left (Ne.symm hy0)

/-- Conversely, if `0` is not a minimizer on `[0, ∞)`, some right slope
from `0` is negative. -/
theorem exists_neg_right_slope_of_not_min {L : ℝ → ℝ}
    (_hL : ConvexOn ℝ (Ici (0 : ℝ)) L)
    (hnot : ¬ IsMinOn L (Ici (0 : ℝ)) 0) :
    ∃ x > 0, (L x - L 0) / x < 0 := by
  have h : ¬ ∀ x > 0, 0 ≤ (L x - L 0) / x := by
    intro hs
    exact hnot ((zero_isMinOn_iff).mpr hs)
  push Not at h
  exact h

/-- CT4's sign condition, packaged: on a convex `L`, `0` fails to minimize
on `[0, ∞)` iff there is a negative right slope from `0`. -/
theorem first_bit_pays_iff {L : ℝ → ℝ}
    (hL : ConvexOn ℝ (Ici (0 : ℝ)) L) :
    ¬ IsMinOn L (Ici (0 : ℝ)) 0 ↔ ∃ x > 0, (L x - L 0) / x < 0 :=
  ⟨exists_neg_right_slope_of_not_min hL,
    fun ⟨x, hx, hs⟩ hmin =>
      (not_le_of_gt hs) ((zero_isMinOn_iff).mp hmin x hx)⟩
