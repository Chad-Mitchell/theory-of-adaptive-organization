/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lean 4 formalization of THEORY CT20 (finite-menu existence and monotone layer
count with sensing fixed), for OPEN_WORK T19.
-/
module

public import GTAO.CT33
public import Mathlib.Tactic.Linarith

/-!
# CT20: existence, and monotone layer count with sensing fixed

From THEORY.md Appendix B.9 (CT20):

> (i) If any design is feasible, a minimizer exists, and
> \(K^*\le J(\mathcal D_1)/h\) for any feasible one-layer \(\mathcal D_1\).
> (ii) *With the sensing (read rates, noise) held fixed and the ruin
> constraint slack or absent*, \(K^*\) is nondecreasing in \(w/h\).

Finite-menu existence is `FiniteDesignMenu.exists_minimizer` in `GTAO.Cost`.
This file records the layer-count bound (from `J ≥ h K`) and the monotone
comparative static for a menu whose spend is exactly `h K` (sensing fixed,
so the menu does not depend on the stake).  The general spend result is
CT33; when spend is `h K` with `h > 0`, the layer count itself is
nondecreasing.  CT20 (ii) does **not** hold once reads are also chosen
(THEORY's counterexample: layers can fall as stakes rise, while total spend
still rises).
-/

@[expose] public section

namespace FiniteDesignMenu

variable {𝒟 : Type*} [Fintype 𝒟] [Nonempty 𝒟] (M : FiniteDesignMenu 𝒟)

omit [Nonempty 𝒟] in
/-- The remaining terms of `J` besides layer upkeep are a nonnegative cost
when `0 ≤ S - h K` and `0 ≤ w * E`.  Then `J ≥ h K`. -/
lemma J_ge_hK {h w : ℝ} (K : 𝒟 → ℝ) (hS : ∀ d, h * K d ≤ M.S d)
    (hWE : ∀ d, 0 ≤ w * M.E d) (d : 𝒟) :
    h * K d ≤ M.J w d := by
  have : h * K d ≤ M.S d := hS d
  simp only [J]
  linarith [hWE d]

omit [Nonempty 𝒟] in
/-- CT20 (i), the layer-count bound: if `J ≥ h K` and `h > 0`, every design
that beats or matches a feasible reference `d₁` at stake `w` satisfies
`K ≤ J(d₁; w) / h`. -/
theorem layer_count_bound {h w : ℝ} (hh : 0 < h) (K : 𝒟 → ℝ)
    (hS : ∀ d, h * K d ≤ M.S d) (hWE : ∀ d, 0 ≤ w * M.E d) (d1 d : 𝒟)
    (hd : M.J w d ≤ M.J w d1) :
    K d ≤ M.J w d1 / h := by
  have hJK : h * K d ≤ M.J w d1 :=
    (M.J_ge_hK K hS hWE d).trans hd
  exact (le_div_iff₀ hh).mpr (by linarith [hJK])

/-- A menu whose spend on judgment is exactly `h` times a layer count. -/
def spendIsLayerUpkeep (h : ℝ) (K : 𝒟 → ℝ) : Prop :=
  ∀ d, M.S d = h * K d

omit [Nonempty 𝒟] in
/-- CT20 (ii), sensing fixed: if spend is `h K` with `h > 0`, then for
`0 ≤ w₁ < w₂` any optimal layer count at `w₂` is at least any optimal layer
count at `w₁`.  This is CT33's spend comparison plus `S = h K`. -/
theorem layer_count_nondecreasing {h w1 w2 : ℝ} (hh : 0 < h)
    (hw1 : 0 ≤ w1) (hw : w1 < w2) (K : 𝒟 → ℝ)
    (hS : M.spendIsLayerUpkeep h K) {d1 d2 : 𝒟}
    (h1 : M.IsOptimal w1 d1) (h2 : M.IsOptimal w2 d2) :
    K d1 ≤ K d2 := by
  have hSpend : M.S d1 ≤ M.S d2 := M.spend_nondecreasing hw1 hw h1 h2
  have eq1 : M.S d1 = h * K d1 := hS d1
  have eq2 : M.S d2 = h * K d2 := hS d2
  have : h * K d1 ≤ h * K d2 := by linarith
  exact (mul_le_mul_iff_right₀ hh).mp this

end FiniteDesignMenu
