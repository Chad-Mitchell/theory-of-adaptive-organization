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

This file formalizes that convex-lower-bound structure and the first-bit
sign condition, stated with right slopes:

* `D` convex and nonincreasing, `IB` concave (on `[0, ∞)`), imply `D ∘ IB`
  convex, and so `L(I)=D(IB(I))+κ I` is convex (the linear term is affine,
  hence convex at every sign of `κ`);
* every right slope of `L` from `0` equals the corresponding right slope
  of `D ∘ IB` plus `κ`;
* therefore `0` fails to minimize `L` on `[0, ∞)` iff some right slope of
  `D ∘ IB` plus `κ` is negative, i.e. iff `κ` is strictly less than the
  negative of that slope.  This is THEORY's `κ < -(D∘IB)'(0⁺)`, written
  with right slopes: the right derivative need not exist as a real, and
  when it does (for convex `D∘IB`) it equals the infimum of those slopes.

Helper lemmas `zero_isMinOn_iff`, `not_minOn_zero_iff_neg_right_slope`,
`pos_min_of_neg_right_slope`, and `exists_neg_right_slope_of_not_min`
are slope facts about an arbitrary `L : ℝ → ℝ` on `[0, ∞)`; they are not
themselves the CT4 sign condition.

That `L` is a *lower bound on cost*, that `IB` is the information-bottleneck
curve (including monotonicity of `IB`, not needed for the convexity or
sign lemmas), and the Gaussian AR(1) closed form
`I* = (1/2) log₂(2 ln 2 · a² · Var / κ)` are not formalized here
(see `formal/lean/README.md`).  Existence of a minimizer of `L` on
`[0, ∞)` is also not proved (`Ici 0` is not a finite menu).
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

/-! ### Helper lemmas: right slopes of an arbitrary `L` on `[0, ∞)`

These do not use convexity and are not the CT4 first-bit criterion. -/

/-- `0` is a minimizer of `L` on `[0, ∞)` iff every right slope from `0`
is nonnegative.  True for any `L`, convex or not. -/
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

/-- `0` fails to minimize `L` on `[0, ∞)` iff some right slope from `0`
is negative.  A helper, not the CT4 sign condition. -/
theorem not_minOn_zero_iff_neg_right_slope {L : ℝ → ℝ} :
    ¬ IsMinOn L (Ici (0 : ℝ)) 0 ↔ ∃ x > 0, (L x - L 0) / x < 0 := by
  constructor
  · intro hnot
    have h : ¬ ∀ x > 0, 0 ≤ (L x - L 0) / x := by
      intro hs
      exact hnot (zero_isMinOn_iff.mpr hs)
    push Not at h
    exact h
  · intro ⟨x, hx, hs⟩ hmin
    exact (not_le_of_gt hs) (zero_isMinOn_iff.mp hmin x hx)

/-- If some right slope from `0` is negative, then any minimizer of `L`
on `[0, ∞)` is strictly positive.  A helper, not the CT4 sign condition. -/
theorem pos_min_of_neg_right_slope {L : ℝ → ℝ} {x : ℝ} (hx : 0 < x)
    (hslope : (L x - L 0) / x < 0) {y : ℝ} (hy : y ∈ Ici (0 : ℝ))
    (hmin : IsMinOn L (Ici (0 : ℝ)) y) :
    0 < y := by
  have h0not : ¬ IsMinOn L (Ici (0 : ℝ)) 0 :=
    not_minOn_zero_iff_neg_right_slope.mpr ⟨x, hx, hslope⟩
  have hy0 : y ≠ 0 := by
    intro h
    exact h0not (by simpa [h] using hmin)
  exact (eq_or_lt_of_le hy).resolve_left (Ne.symm hy0)

/-- Conversely, if `0` is not a minimizer on `[0, ∞)`, some right slope
from `0` is negative.  A helper, not the CT4 sign condition. -/
theorem exists_neg_right_slope_of_not_min {L : ℝ → ℝ}
    (hnot : ¬ IsMinOn L (Ici (0 : ℝ)) 0) :
    ∃ x > 0, (L x - L 0) / x < 0 :=
  not_minOn_zero_iff_neg_right_slope.mp hnot

/-! ### CT4 first-bit sign: `κ` versus the right slopes of `D ∘ IB` -/

/-- Right slope of `I ↦ F I + κ * I` from `0` equals the right slope of
`F` plus `κ`. -/
lemma right_slope_add_linear (F : ℝ → ℝ) (κ x : ℝ) (hx : x ≠ 0) :
    (F x + κ * x - (F 0 + κ * 0)) / x = (F x - F 0) / x + κ := by
  have hdiff : F x + κ * x - (F 0 + κ * 0) = F x - F 0 + κ * x := by
    ring
  rw [hdiff, add_div, mul_div_cancel_right₀ _ hx]

/-- Specialization: every right slope of `L I = D(IB I) + κ I` from `0`
is the corresponding right slope of `D ∘ IB` plus `κ`. -/
lemma L_right_slope (D IB : ℝ → ℝ) (κ x : ℝ) (hx : x ≠ 0) :
    (D (IB x) + κ * x - (D (IB 0) + κ * 0)) / x
      = (D (IB x) - D (IB 0)) / x + κ :=
  right_slope_add_linear (fun I => D (IB I)) κ x hx

/-- CT4 first-bit sign, slope form.  `0` fails to minimize
`L(I)=D(IB(I))+κ I` on `[0, ∞)` iff some right slope of `D ∘ IB` plus
`κ` is negative.  This is THEORY's `κ < -(D∘IB)'(0⁺)` stated with right
slopes.  Convexity of `L` is not required for the equivalence; THEORY
uses it to guarantee that a negative right derivative at `0` implies a
positive minimizer exists, and that the right derivative exists in the
extended reals. -/
theorem first_bit_sign (D IB : ℝ → ℝ) (κ : ℝ) :
    ¬ IsMinOn (fun I => D (IB I) + κ * I) (Ici (0 : ℝ)) 0
      ↔ ∃ x > 0, (D (IB x) - D (IB 0)) / x + κ < 0 := by
  rw [not_minOn_zero_iff_neg_right_slope]
  constructor
  · intro ⟨x, hx, hs⟩
    refine ⟨x, hx, ?_⟩
    rwa [L_right_slope D IB κ x hx.ne'] at hs
  · intro ⟨x, hx, hs⟩
    refine ⟨x, hx, ?_⟩
    rwa [L_right_slope D IB κ x hx.ne']

/-- If a point `y` minimizes `L(I)=D(IB(I))+κ I` on `[0, ∞)` and the
first-bit sign condition holds, then `y` is strictly positive.  (If `0`
were also a minimizer, the sign condition would fail.)  This does not
prove that a minimizer exists. -/
theorem first_bit_positive_minimizer (D IB : ℝ → ℝ) (κ : ℝ)
    {y : ℝ} (hy : y ∈ Ici (0 : ℝ))
    (hmin : IsMinOn (fun I => D (IB I) + κ * I) (Ici (0 : ℝ)) y)
    (hsign : ∃ x > 0, (D (IB x) - D (IB 0)) / x + κ < 0) :
    0 < y := by
  have h0not : ¬ IsMinOn (fun I => D (IB I) + κ * I) (Ici (0 : ℝ)) 0 :=
    (first_bit_sign D IB κ).mpr hsign
  have hy0 : y ≠ 0 := by
    intro h
    exact h0not (by simpa [h] using hmin)
  exact (eq_or_lt_of_le hy).resolve_left (Ne.symm hy0)
