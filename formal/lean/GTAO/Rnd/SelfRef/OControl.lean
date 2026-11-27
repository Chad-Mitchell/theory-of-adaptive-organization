/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost rounds 4–9: `theory/RECORD_COST_ROUNDS4-9_2026-11-25.md` §10, the SFP ball cases.
Lean round 3 of the side session: controls asked for by a hostile review of the Lean layer. The
group choice in `R78.odd_ball_SFP` is load-bearing: under the full orthogonal group O(n), which
contains `-1`, no ball satisfies SFP; and at m = 0, SO(1) is the trivial group.
-/
module

public import Mathlib
public import GTAO.Rnd.SelfRef.SFP

@[expose] public section

namespace GTAORnd.SelfRef.LR3

open Matrix GTAORnd.SelfRef.R78

/-- the action of the full orthogonal group O(n) on the unit sphere (pure states of the n-ball) -/
noncomputable instance orthSphereAction (n : ℕ) : MulAction (orthogonalGroup (Fin n) ℝ) (sphere n) where
  smul A v := ⟨(A : Matrix _ _ ℝ) *ᵥ v.1, by
    have hA := A.2
    rw [mem_orthogonalGroup_iff'] at hA
    unfold IsUnit'
    rw [dotProduct_mulVec, ← mulVec_transpose, mulVec_mulVec, hA, one_mulVec]
    exact v.2⟩
  one_smul v := Subtype.ext (by simp [HSMul.hSMul, SMul.smul])
  mul_smul A B v := Subtype.ext (by simp [HSMul.hSMul, SMul.smul, mulVec_mulVec])

/-- **O(n) control** (PROVED-IN-MODEL): for every n ≥ 1, the n-ball under its full linear
symmetry group O(n) fails SFP, because `-1 ∈ O(n)` fixes no pure state. -/
theorem ball_O_not_SFP (n : ℕ) (_hn : 1 ≤ n) :
    ¬ SFP (orthogonalGroup (Fin n) ℝ) (sphere n) := by
  intro h
  have hm : (-1 : Matrix (Fin n) (Fin n) ℝ) ∈ orthogonalGroup (Fin n) ℝ := by
    rw [mem_orthogonalGroup_iff']; simp
  obtain ⟨x, hx⟩ := h ⟨-1, hm⟩
  have hx' : (-1 : Matrix (Fin n) (Fin n) ℝ) *ᵥ x.1 = x.1 := congrArg Subtype.val hx
  rw [neg_mulVec, one_mulVec] at hx'
  have h0 : x.1 = 0 := by
    funext i; have := congrFun hx' i; simp at this; simp; linarith
  have hu := x.2
  unfold IsUnit' at hu
  rw [h0] at hu; simp at hu

/-- **The qubit under O(3) fails SFP** (PROVED-IN-MODEL): the m = 1 case of the control. -/
theorem qubit_O3_not_SFP : ¬ SFP (orthogonalGroup (Fin 3) ℝ) (sphere 3) :=
  ball_O_not_SFP 3 (by norm_num)

/-- **SO(1) is trivial** (PROVED-IN-MODEL): the m = 0 case of `odd_ball_SFP` is SFP for the
trivial group acting on the two-point 0-sphere (a classical bit with no reversible change). -/
theorem SO1_trivial (A : specialOrthogonalGroup (Fin 1) ℝ) : A = 1 := by
  have hA := A.2
  rw [mem_specialOrthogonalGroup_iff] at hA
  have hd := hA.2
  rw [det_fin_one] at hd
  apply Subtype.ext
  ext i j
  fin_cases i; fin_cases j
  simp [hd]

/-- **The 0-sphere has two points** (PROVED-IN-MODEL): `±1` in ℝ¹. -/
theorem sphere_one_two_points (v : sphere 1) : v.1 0 = 1 ∨ v.1 0 = -1 := by
  have hu := v.2
  unfold IsUnit' at hu
  simp [dotProduct] at hu
  have : (v.1 0 - 1) * (v.1 0 + 1) = 0 := by ring_nf; linarith
  rcases mul_eq_zero.mp this with h | h
  · left; linarith
  · right; linarith

end GTAORnd.SelfRef.LR3
