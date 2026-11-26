/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost rounds 4–9: `theory/RECORD_COST_ROUNDS4-9_2026-11-25.md` §10. Moved from a private Lake
project (library `GTAORnd`, same Lean and Mathlib pins). Statements and proofs unchanged; only this header,
the module lines and doc-comment wording and paths differ.
-/
module

public import Mathlib

@[expose] public section

/-!
# SFP: every reversible map fixes some pure state (theory/RECORD_COST_ROUNDS4-9_2026-11-25.md §5)

`SFP G X`: for a group `G` of reversible maps acting on a set `X` of pure states, every
`g : G` fixes some `x : X`. All results below are PROVED-IN-MODEL; the model is stated in
each docstring.

1. Jordan's derangement theorem (proved here from Mathlib's Burnside lemma; Mathlib has no
   direct statement) and the corollary that finite transitive groups fail SFP
   (classical simplex with Sₙ, the square's rotation).
2. Every element of SO(2m+1) (in particular SO(3)) fixes a unit vector, and its antipode:
   odd balls with SO(2m+1), including the qubit (Bloch) ball, satisfy SFP.
3. Every non-identity element of SO(2) fixes no non-zero vector: the disk/rebit fails SFP.
4. `-1 ∈ SO(2m)` (m ≥ 1) fixes no non-zero vector: even balls with SO(2m) fail SFP.
-/

namespace GTAORnd.SelfRef.R78

open Matrix

/-- **SFP** (strong fixed-point property): every reversible map fixes some pure state. -/
def SFP (G X : Type*) [Group G] [MulAction G X] : Prop := ∀ g : G, ∃ x : X, g • x = x

/-! ## 1. Jordan's derangement theorem -/

/-- **Jordan's derangement theorem.** A finite group acting transitively on a finite set with
at least two elements has an element with no fixed point. (Proof: Burnside's lemma gives
`Σ_g |Fix g| = |G|` for one orbit; the identity alone contributes `|X| ≥ 2`.) -/
theorem jordan_derangement (G X : Type*) [Group G] [MulAction G X] [Fintype G] [Fintype X]
    [DecidableEq X] [MulAction.IsPretransitive G X] (hX : 2 ≤ Fintype.card X) :
    ∃ g : G, ∀ x : X, g • x ≠ x := by
  classical
  by_contra hcon
  push Not at hcon
  -- one orbit
  have hΩ : Fintype.card (MulAction.orbitRel.Quotient G X) = 1 := by
    obtain ⟨x0⟩ : Nonempty X := Fintype.card_pos_iff.mp (by omega)
    rw [Fintype.card_eq_one_iff]
    refine ⟨(Quotient.mk (MulAction.orbitRel G X) x0 : MulAction.orbitRel.Quotient G X),
      fun q => ?_⟩
    induction q using Quotient.inductionOn with
    | h y =>
      apply Quotient.sound
      exact MulAction.orbitRel_apply.mpr
        (MulAction.mem_orbit_iff.mpr (MulAction.exists_smul_eq G x0 y))
  have hB := MulAction.sum_card_fixedBy_eq_card_orbits_mul_card_group G X
  rw [hΩ, one_mul] at hB
  -- each term ≥ 1, the identity term = |X| ≥ 2
  have hpos : ∀ g : G, 1 ≤ Fintype.card (MulAction.fixedBy X g) := by
    intro g
    obtain ⟨x, hx⟩ := hcon g
    exact Fintype.card_pos_iff.mpr ⟨⟨x, hx⟩⟩
  have hone : Fintype.card (MulAction.fixedBy X (1 : G)) = Fintype.card X := by
    rw [Fintype.card_eq.mpr ⟨(Equiv.subtypeUnivEquiv (fun x => by simp))⟩]
  have hsum : Fintype.card G + 1 ≤ ∑ g : G, Fintype.card (MulAction.fixedBy X g) := by
    rw [← Finset.add_sum_erase _ _ (Finset.mem_univ (1 : G)), hone]
    have : (Finset.univ.erase (1 : G)).card ≤
        ∑ g ∈ Finset.univ.erase (1 : G), Fintype.card (MulAction.fixedBy X g) := by
      rw [Finset.card_eq_sum_ones]; exact Finset.sum_le_sum fun g _ => hpos g
    rw [Finset.card_erase_of_mem (Finset.mem_univ _), Finset.card_univ] at this
    have hG : 1 ≤ Fintype.card G := Fintype.card_pos
    omega
  omega

/-- **Corollary.** A finite group acting transitively on finitely many (≥ 2) pure states fails
SFP. -/
theorem finite_transitive_not_SFP (G X : Type*) [Group G] [MulAction G X] [Fintype G]
    [Fintype X] [DecidableEq X] [MulAction.IsPretransitive G X] (hX : 2 ≤ Fintype.card X) :
    ¬ SFP G X := by
  intro h
  obtain ⟨g, hg⟩ := jordan_derangement G X hX
  obtain ⟨x, hx⟩ := h g
  exact hg x hx

/-- Classical simplex with n ≥ 2 vertices and the full permutation group fails SFP. -/
theorem simplex_not_SFP (n : ℕ) (hn : 2 ≤ n) : ¬ SFP (Equiv.Perm (Fin n)) (Fin n) :=
  finite_transitive_not_SFP _ _ (by simpa using hn)

/-- The square: its vertex set `ZMod 4` under the rotation group `Multiplicative (ZMod 4)`
(a transitive subgroup of D₄) fails SFP; explicitly, the quarter turn moves every vertex. -/
theorem square_rotation_moves_all : ∀ v : ZMod 4, v + 1 ≠ v := by decide

/-- D₄ ⊇ rotations, so the square's full reversible group fails SFP too: the quarter turn is a
element with no fixed vertex. (Stated through the explicit action `sqAct` of D₄ on vertices.) -/
def sqAct : DihedralGroup 4 → ZMod 4 → ZMod 4
  | .r i, v => v + i
  | .sr i, v => i - v

theorem square_not_SFP : ∃ g : DihedralGroup 4, ∀ v : ZMod 4, sqAct g v ≠ v :=
  ⟨.r 1, by decide⟩

/-! ## 2–4. Balls with rotation groups -/

/-- Pure states of the n-ball: unit vectors of ℝⁿ (dot product). -/
def IsUnit' {n : ℕ} (v : Fin n → ℝ) : Prop := v ⬝ᵥ v = 1

/-- **Odd dimension.** Every element of SO(2m+1) fixes a unit vector (eigenvalue 1). -/
theorem SO_odd_fixes_unit (m : ℕ) (A : Matrix (Fin (2 * m + 1)) (Fin (2 * m + 1)) ℝ)
    (hA : A ∈ specialOrthogonalGroup (Fin (2 * m + 1)) ℝ) :
    ∃ v : Fin (2 * m + 1) → ℝ, IsUnit' v ∧ A *ᵥ v = v := by
  rw [mem_specialOrthogonalGroup_iff, mem_orthogonalGroup_iff'] at hA
  obtain ⟨horth, hdet⟩ := hA
  -- det(A − 1) = 0
  have hdet0 : (A - 1).det = 0 := by
    have h1 : A - 1 = A * (1 - Aᵀ) := by
      rw [mul_sub, mul_one]
      have : A * Aᵀ = 1 := by
        have := horth  -- Aᵀ * A = 1
        exact mul_eq_one_comm.mp this
      rw [this]
    have h2 : (A - 1).det = (1 - A).det := by
      rw [h1, det_mul, hdet, one_mul, ← det_transpose]
      congr 1; simp [transpose_sub]
    have h3 : (1 - A).det = -(A - 1).det := by
      rw [show (1 : Matrix _ _ ℝ) - A = -(A - 1) by abel, det_neg]
      simp [pow_succ, pow_mul]
    linarith
  obtain ⟨w, hw0, hw⟩ := (exists_mulVec_eq_zero_iff).mpr hdet0
  have hAw : A *ᵥ w = w := by
    rw [sub_mulVec, one_mulVec, sub_eq_zero] at hw; exact hw
  have hpos : 0 < w ⬝ᵥ w := by
    have hnn : 0 ≤ w ⬝ᵥ w := Finset.sum_nonneg fun i _ => mul_self_nonneg _
    exact lt_of_le_of_ne hnn (Ne.symm (dotProduct_self_eq_zero.not.mpr hw0))
  refine ⟨(Real.sqrt (w ⬝ᵥ w))⁻¹ • w, ?_, ?_⟩
  · unfold IsUnit'
    rw [smul_dotProduct, dotProduct_smul, smul_eq_mul, smul_eq_mul, ← mul_assoc,
      ← sq, inv_pow, Real.sq_sqrt hpos.le, inv_mul_cancel₀ hpos.ne']
  · rw [mulVec_smul, hAw]

/-- The antipode of a fixed unit vector is fixed too: under every element of SO(2m+1) a whole
distinguishable pair (the axis poles) persists. -/
theorem SO_odd_fixes_poles (m : ℕ) (A : Matrix (Fin (2 * m + 1)) (Fin (2 * m + 1)) ℝ)
    (hA : A ∈ specialOrthogonalGroup (Fin (2 * m + 1)) ℝ) :
    ∃ v : Fin (2 * m + 1) → ℝ, IsUnit' v ∧ A *ᵥ v = v ∧ IsUnit' (-v) ∧ A *ᵥ (-v) = -v := by
  obtain ⟨v, hv, hAv⟩ := SO_odd_fixes_unit m A hA
  refine ⟨v, hv, hAv, ?_, ?_⟩
  · unfold IsUnit' at *; simpa using hv
  · rw [mulVec_neg, hAv]

/-- **Qubit (Bloch) ball.** Every element of SO(3) fixes a pair of antipodal unit vectors. -/
theorem SO3_fixes_poles (A : Matrix (Fin 3) (Fin 3) ℝ)
    (hA : A ∈ specialOrthogonalGroup (Fin 3) ℝ) :
    ∃ v : Fin 3 → ℝ, IsUnit' v ∧ A *ᵥ v = v ∧ IsUnit' (-v) ∧ A *ᵥ (-v) = -v :=
  SO_odd_fixes_poles 1 A hA

/-- the action of SO(n) on the unit sphere (pure states of the n-ball) -/
def sphere (n : ℕ) : Type := {v : Fin n → ℝ // IsUnit' v}

noncomputable instance (n : ℕ) : MulAction (specialOrthogonalGroup (Fin n) ℝ) (sphere n) where
  smul A v := ⟨(A : Matrix _ _ ℝ) *ᵥ v.1, by
    have hA := A.2
    rw [mem_specialOrthogonalGroup_iff, mem_orthogonalGroup_iff'] at hA
    unfold IsUnit'
    rw [dotProduct_mulVec, ← mulVec_transpose, mulVec_mulVec, hA.1, one_mulVec]
    exact v.2⟩
  one_smul v := Subtype.ext (by simp [HSMul.hSMul, SMul.smul])
  mul_smul A B v := Subtype.ext (by simp [HSMul.hSMul, SMul.smul, mulVec_mulVec])

/-- **Odd balls satisfy SFP** (SO(2m+1) on the unit sphere of ℝ^{2m+1}); m = 1 is the qubit. -/
theorem odd_ball_SFP (m : ℕ) : SFP (specialOrthogonalGroup (Fin (2 * m + 1)) ℝ) (sphere (2 * m + 1)) := by
  intro A
  obtain ⟨v, hv, hAv⟩ := SO_odd_fixes_unit m A A.2
  exact ⟨⟨v, hv⟩, Subtype.ext hAv⟩

/-- **Disk / rebit.** A non-identity element of SO(2) fixes no non-zero vector. -/
theorem SO2_nonid_no_fixed (A : Matrix (Fin 2) (Fin 2) ℝ)
    (hA : A ∈ specialOrthogonalGroup (Fin 2) ℝ) (hne : A ≠ 1) :
    ∀ v : Fin 2 → ℝ, v ≠ 0 → A *ᵥ v ≠ v := by
  rw [mem_specialOrthogonalGroup_iff, mem_orthogonalGroup_iff'] at hA
  obtain ⟨horth, hdet⟩ := hA
  have e00 := congrFun (congrFun horth 0) 0
  have e01 := congrFun (congrFun horth 0) 1
  have e11 := congrFun (congrFun horth 1) 1
  simp [Matrix.mul_apply, Fin.sum_univ_two] at e00 e01 e11
  rw [det_fin_two] at hdet
  have hd : A 1 1 = A 0 0 := by
    nlinarith [sq_nonneg (A 0 0 - A 1 1), sq_nonneg (A 0 1 + A 1 0)]
  have hc : A 1 0 = -A 0 1 := by
    nlinarith [sq_nonneg (A 0 0 - A 1 1), sq_nonneg (A 0 1 + A 1 0)]
  intro v hv hfix
  have h0 := congrFun hfix 0
  have h1 := congrFun hfix 1
  simp [mulVec, dotProduct, Fin.sum_univ_two] at h0 h1
  rw [hc] at h1; rw [hd] at h1
  have hq0 : ((A 0 0 - 1) ^ 2 + A 0 1 ^ 2) * v 0 = 0 := by linear_combination (A 0 0 - 1) * h0 - A 0 1 * h1
  have hq1 : ((A 0 0 - 1) ^ 2 + A 0 1 ^ 2) * v 1 = 0 := by linear_combination (A 0 0 - 1) * h1 + A 0 1 * h0
  have hab : (A 0 0 - 1) ^ 2 + A 0 1 ^ 2 ≠ 0 := by
    intro h
    have ha : A 0 0 = 1 := by nlinarith [sq_nonneg (A 0 0 - 1), sq_nonneg (A 0 1)]
    have hb : A 0 1 = 0 := by nlinarith [sq_nonneg (A 0 0 - 1), sq_nonneg (A 0 1)]
    apply hne
    ext i j; fin_cases i <;> fin_cases j <;> simp [ha, hb, hc, hd]
  apply hv
  funext i; fin_cases i
  · exact (mul_eq_zero.mp hq0).resolve_left hab
  · exact (mul_eq_zero.mp hq1).resolve_left hab

/-- **The disk fails SFP**: the half turn `-1 ∈ SO(2)` fixes no pure state. -/
theorem disk_not_SFP : ¬ SFP (specialOrthogonalGroup (Fin 2) ℝ) (sphere 2) := by
  intro h
  have hm : (-1 : Matrix (Fin 2) (Fin 2) ℝ) ∈ specialOrthogonalGroup (Fin 2) ℝ := by
    rw [mem_specialOrthogonalGroup_iff, mem_orthogonalGroup_iff']
    refine ⟨by simp, by simp [det_neg]⟩
  obtain ⟨x, hx⟩ := h ⟨-1, hm⟩
  have hx' := congrArg Subtype.val hx
  have hv0 : x.1 ≠ 0 := by
    intro h0; have := x.2; unfold IsUnit' at this; rw [h0] at this; simp at this
  exact SO2_nonid_no_fixed (-1) hm (by
    intro h1; have := congrFun (congrFun h1 0) 0; simp at this; linarith) x.1 hv0 hx'

/-- **Even balls.** For every m (m = 0: the 0-sphere is empty, vacuous), `-1 ∈ SO(2m)` fixes no non-zero vector, so SO(2m) on the
(2m)-ball fails SFP. -/
theorem even_ball_not_SFP (m : ℕ) :
    ¬ SFP (specialOrthogonalGroup (Fin (2 * m)) ℝ) (sphere (2 * m)) := by
  intro h
  have hmem : (-1 : Matrix (Fin (2 * m)) (Fin (2 * m)) ℝ) ∈
      specialOrthogonalGroup (Fin (2 * m)) ℝ := by
    rw [mem_specialOrthogonalGroup_iff, mem_orthogonalGroup_iff']
    refine ⟨by simp, ?_⟩
    rw [det_neg]; simp [pow_mul]
  obtain ⟨x, hx⟩ := h ⟨-1, hmem⟩
  have hx' := congrArg Subtype.val hx
  change (-1 : Matrix (Fin (2 * m)) (Fin (2 * m)) ℝ) *ᵥ x.1 = x.1 at hx'
  rw [neg_mulVec, one_mulVec, neg_eq_iff_add_eq_zero, ← two_smul ℝ] at hx'
  have : x.1 = 0 := by
    have := congrArg (fun w => (1 / 2 : ℝ) • w) hx'
    simpa [smul_smul] using this
  have h1 := x.2; unfold IsUnit' at h1; rw [this] at h1; simp at h1

end GTAORnd.SelfRef.R78
