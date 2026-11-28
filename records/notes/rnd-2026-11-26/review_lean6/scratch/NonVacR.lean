import GTAO.Rnd.SelfRef.LemmaR
open GTAORnd.SelfRef.LR3.LemmaR

/-- square vertices in homogeneous coordinates (1, x, y) over ℚ -/
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

/-- the hypotheses of `lemmaR` are jointly satisfiable: square × square, dims 3, m = n = 4 -/
example : ∀ T : Matrix (Fin 3) (Fin 3) ℚ ≃ₗ[ℚ] Matrix (Fin 3) (Fin 3) ℚ,
    T '' Set.range (kr sqV sqV) = Set.range (kr sqV sqV) →
    ∃ f : Fin 4 × Fin 4 → Fin 4 × Fin 4, Function.Bijective f ∧
      (∀ x, T (kr sqV sqV x) = kr sqV sqV (f x)) ∧
      ((∃ α : Fin 4 → Fin 4, ∃ β : Fin 4 → Fin 4, ∀ x, f x = (α x.1, β x.2)) ∨
       (∃ α : Fin 4 → Fin 4, ∃ β : Fin 4 → Fin 4, ∀ x, f x = (α x.2, β x.1))) :=
  fun T hP => lemmaR sqV_indep3 sqV_indep3 le_rfl le_rfl le_rfl le_rfl T hP

/-- and the hypothesis T '' P = P is met by a non-identity map: transpose (the swap) -/
example : (Matrix.transposeLinearEquiv (Fin 3) (Fin 3) ℚ ℚ) '' Set.range (kr sqV sqV) =
    Set.range (kr sqV sqV) := by
  ext M; constructor
  · rintro ⟨_, ⟨x, rfl⟩, rfl⟩
    exact ⟨x.swap, by simp [kr, Matrix.transpose_vecMulVec]⟩
  · rintro ⟨x, rfl⟩
    exact ⟨_, ⟨x.swap, rfl⟩, by simp [kr, Matrix.transpose_vecMulVec]⟩

#print axioms sqV_indep3
