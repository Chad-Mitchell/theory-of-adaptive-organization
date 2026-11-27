/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost: `theory/RECORD_COST_ROUND10_2026-11-25.md` §8 (the finite-geometry step:
the algebra after Piron's representation). Lean round 3 of the side session; written in a
private Lake project (library `GTAORnd`, same Lean and Mathlib pins) and moved here with only
this header and the module lines changed.
-/
module

public import Mathlib

@[expose] public section

/-!
# The finite-geometry step: finite coordinates force isotropic vectors

Round 10 note §8 chain: an irreducible orthocomplemented lattice with the covering property
and rank ≥ 4 is coordinatized by a division ring `D` with an involution and an anisotropic
Hermitian form (Piron; Maeda–Maeda; KNOWN, **not formalized**). If there were finitely many
atoms, `D` would be finite. This file proves the algebraic steps after Piron:

* `finite_divring_comm`: a finite division ring is commutative (Wedderburn; Mathlib's
  `littleWedderburn`);
* `chevalley_nonzero_zero`: over a finite field, a polynomial in `n` variables with total
  degree `< n` and no constant term has a non-zero zero (from Mathlib's Chevalley–Warning);
* `diag_form_isotropic`: every diagonal quadratic form `Σ aᵢxᵢ²` in `n ≥ 3` variables over a
  finite field has a non-zero zero (the case of the trivial involution);
* `norm_form_isotropic`: for a finite extension `K'/K` of finite fields, every form
  `a₁N(x₁) + a₂N(x₂)` with `a₁ ≠ 0` has a non-zero zero (the norm form; for a quadratic
  extension `N(x) = x·x̄` is the Hermitian form of the non-trivial involution).
So a finite coordinatizing `*`-field admits no anisotropic diagonal Hermitian form in ≥ 3
variables. Not formalized: Piron's representation, that every Hermitian form diagonalizes,
that every involution of a finite field is trivial or the quadratic Frobenius, and the rank-3
case (Baer: polarities of finite planes have absolute points).
-/

namespace GTAORnd.SelfRef.LR3

open MvPolynomial

/-- **Wedderburn**: a finite division ring is commutative. -/
theorem finite_divring_comm (D : Type*) [DivisionRing D] [Finite D] (a b : D) : a * b = b * a := by
  have : Fintype D := Fintype.ofFinite D
  let _ := littleWedderburn D
  exact mul_comm a b

/-- **Chevalley**: over a finite field, a polynomial of total degree `< n` in `n` variables
vanishing at `0` has a non-zero zero. -/
theorem chevalley_nonzero_zero {K σ : Type*} [Field K] [Fintype K] [DecidableEq K]
    [Fintype σ] [DecidableEq σ] (f : MvPolynomial σ K) (hdeg : f.totalDegree < Fintype.card σ)
    (h0 : eval 0 f = 0) : ∃ x : σ → K, x ≠ 0 ∧ eval x f = 0 := by
  obtain ⟨p, hp⟩ := CharP.exists K
  have hpp : p.Prime :=
    (CharP.char_is_prime_or_zero K p).resolve_right (CharP.char_ne_zero_of_finite K p)
  have := Fact.mk hpp
  have hdvd := char_dvd_card_solutions (K := K) p hdeg
  by_contra hcon
  push Not at hcon
  -- the only solution is 0
  have hone : Fintype.card { x : σ → K // eval x f = 0 } = 1 := by
    rw [Fintype.card_eq_one_iff]
    refine ⟨⟨0, h0⟩, fun ⟨x, hx⟩ => ?_⟩
    by_contra hne
    exact hcon x (fun h => hne (Subtype.ext h)) hx
  rw [hone] at hdvd
  exact hpp.one_lt.ne' (Nat.dvd_one.mp hdvd)

/-- **Diagonal quadratic forms in ≥ 3 variables over a finite field are isotropic.** -/
theorem diag_form_isotropic {K : Type*} [Field K] [Fintype K] [DecidableEq K] (n : ℕ)
    (hn : 3 ≤ n) (a : Fin n → K) : ∃ x : Fin n → K, x ≠ 0 ∧ ∑ i, a i * x i ^ 2 = 0 := by
  let f : MvPolynomial (Fin n) K := ∑ i, C (a i) * X i ^ 2
  have hdeg : f.totalDegree < Fintype.card (Fin n) := by
    rw [Fintype.card_fin]
    have : f.totalDegree ≤ 2 := by
      apply (totalDegree_finsetSum _ _).trans
      apply Finset.sup_le
      intro i _
      apply (totalDegree_mul _ _).trans
      rw [totalDegree_C, zero_add]
      apply (totalDegree_pow _ _).trans
      rw [totalDegree_X]
    omega
  obtain ⟨x, hx, hfx⟩ := chevalley_nonzero_zero f hdeg (by simp [f])
  exact ⟨x, hx, by simpa [f] using hfx⟩

/-- **Norm forms in 2 variables over finite fields are isotropic.** For finite fields
`K ⊆ K'` and `a₁ ≠ 0`, some `(x₁, x₂) ≠ 0` has `a₁ N(x₁) + a₂ N(x₂) = 0`. -/
theorem norm_form_isotropic {K K' : Type*} [Field K] [Field K'] [Fintype K] [Fintype K']
    [Algebra K K'] (a₁ a₂ : K) (h₁ : a₁ ≠ 0) :
    ∃ x : K' × K', x ≠ 0 ∧ a₁ * Algebra.norm K x.1 + a₂ * Algebra.norm K x.2 = 0 := by
  obtain ⟨y, hy⟩ := FiniteField.norm_surjective (K := K) (K' := K') (-a₂ / a₁)
  refine ⟨(y, 1), fun h => by simpa using congrArg Prod.snd h, ?_⟩
  simp only [map_one, mul_one, hy]
  field_simp
  ring

end GTAORnd.SelfRef.LR3
