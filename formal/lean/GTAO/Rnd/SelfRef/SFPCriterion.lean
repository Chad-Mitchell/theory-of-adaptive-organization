/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost: `theory/RECORD_COST_ROUNDS4-9_2026-11-25.md` §5 and §10 (concrete cases of the
maximal-torus SFP criterion). Lean round 3 of the side session; written in a private Lake
project (library `GTAORnd`, same Lean and Mathlib pins) and moved here with only this header
and the module lines changed.
-/
module

public import Mathlib
public import GTAO.Rnd.SelfRef.SFP

@[expose] public section

/-!
# Concrete cases of the maximal-torus SFP criterion

The rounds 4–9 note states the criterion "for a compact connected transitive group G with
stabilizer H, SFP ⇔ rank H = rank G" (maximal torus theorem; Hopf–Samelson). It is not
formalized here. What is proved are the cases the survivor table uses, each directly:

* balls with SO(n): SFP ⇔ n odd (`ball_SFP_iff_odd`);
* complex quantum theory, every d ≥ 1: every complex d×d matrix, in particular every unitary,
  has an eigenvector, so it fixes a pure state (a ray) (`complex_fixes_ray`,
  `unitary_fixes_ray`);
* real quantum theory with the orthogonal group: odd d passes (`real_odd_fixes_ray`: every
  element of O(2m+1) has eigenvalue 1 or −1); even d fails (`real_even_not_SFP`: the
  quarter-turn J ∈ O(2m) has no real eigenvector).

Pure states of quantum theory are rays, so "U fixes a pure state" is "U has an eigenvector".
-/

namespace GTAORnd.SelfRef.LR3

open Matrix GTAORnd.SelfRef.R78

/-- **Balls with SO(n): SFP iff n is odd** (PROVED-IN-MODEL). -/
theorem ball_SFP_iff_odd (n : ℕ) :
    SFP (specialOrthogonalGroup (Fin n) ℝ) (sphere n) ↔ Odd n := by
  constructor
  · intro h
    by_contra hodd
    obtain ⟨m, rfl⟩ : ∃ m, n = 2 * m := by
      rcases Nat.not_odd_iff_even.mp hodd with ⟨m, hm⟩; exact ⟨m, by omega⟩
    exact even_ball_not_SFP m h
  · rintro ⟨m, rfl⟩
    have := odd_ball_SFP m
    simpa [Nat.mul_comm] using this

/-- **Complex quantum theory** (PROVED-IN-MODEL): every complex d×d matrix (d ≥ 1) has an
eigenvector, i.e. fixes a ray. -/
theorem complex_fixes_ray (d : ℕ) (hd : 0 < d) (U : Matrix (Fin d) (Fin d) ℂ) :
    ∃ v : Fin d → ℂ, v ≠ 0 ∧ ∃ μ : ℂ, U *ᵥ v = μ • v := by
  have : Nontrivial (Fin d → ℂ) := by
    have : Nonempty (Fin d) := ⟨⟨0, hd⟩⟩
    infer_instance
  obtain ⟨μ, hμ⟩ := Module.End.exists_eigenvalue (Matrix.toLin' U)
  obtain ⟨v, hv⟩ := hμ.exists_hasEigenvector
  refine ⟨v, hv.2, μ, ?_⟩
  have := Module.End.mem_eigenspace_iff.mp hv.1
  simpa [Matrix.toLin'_apply] using this

/-- every unitary fixes a pure state of complex quantum theory, in every d ≥ 1 -/
theorem unitary_fixes_ray (d : ℕ) (hd : 0 < d) (U : unitaryGroup (Fin d) ℂ) :
    ∃ v : Fin d → ℂ, v ≠ 0 ∧ ∃ μ : ℂ, (U : Matrix (Fin d) (Fin d) ℂ) *ᵥ v = μ • v :=
  complex_fixes_ray d hd U

/-- **Real quantum theory, odd d** (PROVED-IN-MODEL): every element of O(2m+1) has a real
eigenvector with eigenvalue 1 or −1, so it fixes a ray. -/
theorem real_odd_fixes_ray (m : ℕ) (A : Matrix (Fin (2 * m + 1)) (Fin (2 * m + 1)) ℝ)
    (hA : A ∈ orthogonalGroup (Fin (2 * m + 1)) ℝ) :
    ∃ v, v ≠ 0 ∧ (A *ᵥ v = v ∨ A *ᵥ v = -v) := by
  rw [mem_orthogonalGroup_iff'] at hA
  have hAAt : A * Aᵀ = 1 := mul_eq_one_comm.mp (by simpa [star_eq_conjTranspose] using hA)
  have hAtA : Aᵀ * A = 1 := by simpa [star_eq_conjTranspose] using hA
  have hdet2 : A.det * A.det = 1 := by
    have := congrArg det hAtA; rw [det_mul, det_transpose, det_one] at this; exact this
  have hodd : ((-1 : ℝ)) ^ (2 * m + 1) = -1 := by rw [pow_succ, pow_mul]; simp
  rcases mul_self_eq_one_iff.mp hdet2 with h1 | h1
  · -- det = 1: det(A − 1) = 0
    have h0 : (A - 1).det = 0 := by
      have e1 : A - 1 = A * (1 - Aᵀ) := by rw [mul_sub, mul_one, hAAt]
      have e2 : (A - 1).det = (1 - A).det := by
        rw [e1, det_mul, h1, one_mul, ← det_transpose]; congr 1; simp [transpose_sub]
      have e3 : (1 - A).det = -(A - 1).det := by
        rw [show (1 : Matrix _ _ ℝ) - A = -(A - 1) by abel, det_neg]; simp [hodd]
      linarith
    obtain ⟨v, hv, hAv⟩ := exists_mulVec_eq_zero_iff.mpr h0
    refine ⟨v, hv, Or.inl ?_⟩
    rw [sub_mulVec, one_mulVec, sub_eq_zero] at hAv; exact hAv
  · -- det = −1: det(A + 1) = 0
    have h0 : (A + 1).det = 0 := by
      have e1 : A + 1 = A * (1 + Aᵀ) := by rw [mul_add, mul_one, hAAt]
      have e2 : (A + 1).det = -(1 + A).det := by
        rw [e1, det_mul, h1, neg_one_mul, ← det_transpose (1 + A)]; congr 2; simp [transpose_add]
      rw [add_comm 1 A] at e2
      linarith
    obtain ⟨v, hv, hAv⟩ := exists_mulVec_eq_zero_iff.mpr h0
    refine ⟨v, hv, Or.inr ?_⟩
    rw [add_mulVec, one_mulVec, add_eq_zero_iff_eq_neg] at hAv; exact hAv

/-- the quarter turn on ℝ^{2m} = ℝ^m ⊕ ℝ^m -/
def quarterTurn (m : ℕ) : Matrix (Fin m ⊕ Fin m) (Fin m ⊕ Fin m) ℝ :=
  Matrix.fromBlocks 0 (-1) 1 0

/-- **Real quantum theory, even d** (PROVED-IN-MODEL): the quarter turn is orthogonal and has
no real eigenvector, so it fixes no ray: real quantum theory with its
orthogonal group fails SFP in every even dimension `2m ≥ 2`. -/
theorem real_even_not_SFP (m : ℕ) :
    quarterTurn m ∈ orthogonalGroup (Fin m ⊕ Fin m) ℝ ∧
    ∀ v : Fin m ⊕ Fin m → ℝ, ∀ μ : ℝ, quarterTurn m *ᵥ v = μ • v → v = 0 := by
  have hJJ : quarterTurn m * quarterTurn m = -1 := by
    simp [quarterTurn, fromBlocks_multiply, ← fromBlocks_one, fromBlocks_neg]
  refine ⟨?_, ?_⟩
  · rw [mem_orthogonalGroup_iff']
    simp [quarterTurn, fromBlocks_transpose, fromBlocks_multiply, ← fromBlocks_one]
  · intro v μ hv
    have h2 : quarterTurn m *ᵥ (quarterTurn m *ᵥ v) = (μ * μ) • v := by
      rw [hv, mulVec_smul, hv, smul_smul]
    rw [mulVec_mulVec, hJJ, neg_mulVec, one_mulVec] at h2
    have h3 : (μ * μ + 1) • v = 0 := by rw [add_smul, one_smul, ← h2]; abel
    have hpos : μ * μ + 1 ≠ 0 := by nlinarith [mul_self_nonneg μ]
    exact (smul_eq_zero.mp h3).resolve_left hpos

end GTAORnd.SelfRef.LR3
