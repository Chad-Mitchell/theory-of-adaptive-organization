/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, stepback Lemma R (`theory/lemma-r-2026-11-26/LEMMA_R.md`, ledger RC20): product vectors of
polygon composites. Folklore-level, novelty not claimed: the dual-functional step is Marcus–Moyls,
as Al-Safi–Richens 2015 Lemma 4; the adjacency argument is Al-Safi–Richens 2015 Lemma 2; the rook's
graph is Harary 1958 (line group of K_{m,n}) with Whitney 1932 (`rook_aut` is proved directly). Lean
round 6 of the side session; written in a private Lake project (same Lean and Mathlib pins) and moved
here with only this header and the module lines changed.
-/
module

public import GTAO.Rnd.SelfRef.LemmaR

@[expose] public section

/-!
# Non-vacuity of `lemmaR` for the square over ℚ (Lean round 6 review fix)

Written by the round 6 reviewer in a scratch file and moved here under new names: S2 (`Indep3`) for
the square's vertices (1, ±1, 0), (1, 0, ±1) in homogeneous coordinates, the instance of `lemmaR`
with them, and a non-identity map (the transpose, the swap) meeting its premise `T '' P = P`.
One polygon over ℚ only; regular n-gons with n ≠ 4 need ℝ, and S2 for a general convex polygon
(no three vertices collinear) is on paper.
-/

namespace GTAORnd.SelfRef.LR3.LemmaR

/-- square vertices in homogeneous coordinates `(1, x, y)` over ℚ -/
def sqV : Fin 4 → Fin 3 → ℚ := ![![1, 1, 0], ![1, 0, 1], ![1, -1, 0], ![1, 0, -1]]

theorem sqV_indep3 : Indep3 sqV := by
  intro s hs
  rw [linearIndepOn_finset_iff]
  intro c hc i hi
  have e0 := congrFun hc 0
  have e1 := congrFun hc 1
  have e2 := congrFun hc 2
  simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply] at e0 e1 e2
  have hs' : s ∈ (Finset.univ : Finset (Finset (Fin 4))) := Finset.mem_univ s
  fin_cases s <;> simp [sqV] at e0 e1 e2 hi hs ⊢ <;>
    first
    | (rcases hi with rfl | rfl | rfl <;> linarith)
    | (rcases hi with rfl | rfl <;> linarith)
    | (subst hi; linarith)

/-- the hypotheses of `lemmaR` are jointly satisfiable: square × square, dimensions 3, `m = n = 4` -/
theorem square_lemmaR :
    ∀ T : Matrix (Fin 3) (Fin 3) ℚ ≃ₗ[ℚ] Matrix (Fin 3) (Fin 3) ℚ,
    T '' Set.range (kr sqV sqV) = Set.range (kr sqV sqV) →
    ∃ f : Fin 4 × Fin 4 → Fin 4 × Fin 4, Function.Bijective f ∧
      (∀ x, T (kr sqV sqV x) = kr sqV sqV (f x)) ∧
      ((∃ α : Fin 4 → Fin 4, ∃ β : Fin 4 → Fin 4, ∀ x, f x = (α x.1, β x.2)) ∨
       (∃ α : Fin 4 → Fin 4, ∃ β : Fin 4 → Fin 4, ∀ x, f x = (α x.2, β x.1))) :=
  fun T hP => lemmaR sqV_indep3 sqV_indep3 le_rfl le_rfl le_rfl le_rfl T hP

/-- the premise `T '' P = P` is met by a map other than the identity: the transpose (the swap) -/
theorem square_transpose_preserves :
    (Matrix.transposeLinearEquiv (Fin 3) (Fin 3) ℚ ℚ) '' Set.range (kr sqV sqV) =
      Set.range (kr sqV sqV) := by
  ext M; constructor
  · rintro ⟨_, ⟨x, rfl⟩, rfl⟩
    exact ⟨x.swap, by simp [kr, Matrix.transpose_vecMulVec]⟩
  · rintro ⟨x, rfl⟩
    exact ⟨_, ⟨x.swap, rfl⟩, by simp [kr, Matrix.transpose_vecMulVec]⟩

end GTAORnd.SelfRef.LR3.LemmaR
