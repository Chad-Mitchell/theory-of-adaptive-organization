/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lean 4 formalization of the GTAO master-equation cost, for OPEN_WORK T19.
-/
module

public import Mathlib.Analysis.Convex.Function
public import Mathlib.Algebra.Order.Archimedean.Real.Basic
public import Mathlib.Data.Set.Finite.Lemmas
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.Ring

/-!
# The cost of judgment, on a finite design menu

`CORE.md` §1 and THEORY §3 define

\[
  J(\mathcal D)=\kappa I_{\mathrm{mem}}+hK+w\,\mathbb E[\ell_{\mathcal D}]+A(\mathcal D)+L(\mathcal D)
\]

subject to a ruin cap \(P(\mathrm{ruin})\le\varepsilon\).  When that cap is slack or
absent, the feasible set does not depend on the stake \(w\), and the cost splits as

\[
  J(\mathcal D;w)=S(\mathcal D)+w\cdot E(\mathcal D),
\]

with \(S\) the spend on judgment (upkeep, memory, reads, links, telling) and \(E\) the
expected error per unit stake.  This file takes a nonempty finite design set as the
menu, with \(S\) and \(E\) independent of \(w\).  Existence of a minimizer is then
immediate (CT20 (i) in this finite setting).
-/

@[expose] public section

open Set

/-- A finite menu of designs, with stake-independent spend and error.

The type `𝒟` is the design set.  Finiteness is the standing existence hypothesis
of the formalization (THEORY CT20 (i) in the special case of a finite menu). -/
structure FiniteDesignMenu (𝒟 : Type*) [Fintype 𝒟] where
  /-- Spend on judgment: layers' upkeep, memory, reads, links, telling. -/
  S : 𝒟 → ℝ
  /-- Expected error per unit stake. -/
  E : 𝒟 → ℝ

namespace FiniteDesignMenu

variable {𝒟 : Type*} [Fintype 𝒟] [Nonempty 𝒟] (M : FiniteDesignMenu 𝒟)

/-- The master-equation cost at stake `w`, with the ruin constraint slack or
absent, so the feasible set does not depend on `w` (THEORY CT33, CT22). -/
def J (w : ℝ) (d : 𝒟) : ℝ := M.S d + w * M.E d

/-- `d` is an optimal design at stake `w`: it attains `argmin J(·; w)`. -/
def IsOptimal (w : ℝ) (d : 𝒟) : Prop := ∀ d' : 𝒟, M.J w d ≤ M.J w d'

/-- CT20 (i), finite menu: if the design set is nonempty and finite, a minimizer
exists at every stake. -/
theorem exists_minimizer (w : ℝ) : ∃ d : 𝒟, M.IsOptimal w d := by
  have hFin : (univ : Set 𝒟).Finite := finite_univ
  have hNe : (univ : Set 𝒟).Nonempty := univ_nonempty
  obtain ⟨d, _, hd⟩ := exists_min_image (univ : Set 𝒟) (M.J w) hFin hNe
  exact ⟨d, fun d' => hd d' (mem_univ d')⟩

/-- The optimized cost \(J^*(w)=\min_{\mathcal D} J(\mathcal D;w)\), obtained by
choosing a minimizer (which exists by `exists_minimizer`). -/
noncomputable def Jstar (w : ℝ) : ℝ :=
  M.J w (Classical.choose (M.exists_minimizer w))

lemma isOptimal_choose (w : ℝ) :
    M.IsOptimal w (Classical.choose (M.exists_minimizer w)) :=
  Classical.choose_spec (M.exists_minimizer w)

lemma Jstar_le (w : ℝ) (d : 𝒟) : M.Jstar w ≤ M.J w d :=
  M.isOptimal_choose w d

lemma IsOptimal.Jstar_eq {w : ℝ} {d : 𝒟} (hd : M.IsOptimal w d) :
    M.Jstar w = M.J w d :=
  le_antisymm (M.Jstar_le w d) (hd _)

lemma exists_eq_Jstar (w : ℝ) : ∃ d : 𝒟, M.IsOptimal w d ∧ M.Jstar w = M.J w d := by
  obtain ⟨d, hd⟩ := M.exists_minimizer w
  exact ⟨d, hd, hd.Jstar_eq⟩

/-- Envelope: an optimal design at `w` is a supporting affine line of slope `E d`
for `J*` at `w`.  (THEORY CT33: "`J*(w)` is concave with slope `E*`".) -/
lemma Jstar_le_affine (d : 𝒟) (w' : ℝ) :
    M.Jstar w' ≤ M.S d + w' * M.E d :=
  M.Jstar_le w' d

/-- The cost is affine in the stake: a convex combination of stakes reassembles
when the weights sum to one. -/
lemma J_affine (d : 𝒟) {w1 w2 a b : ℝ} (hab : a + b = 1) :
    M.J (a * w1 + b * w2) d = a * M.J w1 d + b * M.J w2 d := by
  simp only [J]
  calc
    M.S d + (a * w1 + b * w2) * M.E d
        = (a + b) * M.S d + (a * w1 + b * w2) * M.E d := by rw [hab, one_mul]
    _ = a * M.S d + b * M.S d + (a * (w1 * M.E d) + b * (w2 * M.E d)) := by ring
    _ = a * (M.S d + w1 * M.E d) + b * (M.S d + w2 * M.E d) := by ring

/-- `J*` is the pointwise minimum of affine functions of `w`, hence concave on
all of `ℝ`. -/
theorem Jstar_concave : ConcaveOn ℝ univ M.Jstar := by
  refine ⟨convex_univ, fun w1 _ w2 _ a b ha hb hab => ?_⟩
  obtain ⟨d, -, hdEq⟩ := M.exists_eq_Jstar (a * w1 + b * w2)
  have hcalc : M.J (a * w1 + b * w2) d = a * M.J w1 d + b * M.J w2 d :=
    M.J_affine d hab
  have : a * M.Jstar w1 + b * M.Jstar w2 ≤ a * M.J w1 d + b * M.J w2 d := by
    have h1 : M.Jstar w1 ≤ M.J w1 d := M.Jstar_le w1 d
    have h2 : M.Jstar w2 ≤ M.J w2 d := M.Jstar_le w2 d
    nlinarith
  calc
    a * M.Jstar w1 + b * M.Jstar w2 ≤ a * M.J w1 d + b * M.J w2 d := this
    _ = M.J (a * w1 + b * w2) d := hcalc.symm
    _ = M.Jstar (a * w1 + b * w2) := hdEq.symm

end FiniteDesignMenu
