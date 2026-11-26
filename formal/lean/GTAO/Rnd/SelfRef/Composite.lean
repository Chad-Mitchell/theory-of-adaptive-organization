/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost: round 11 part M (Conjecture C test), Theorem M11, Lemmas 1 and 2, from the
side session's notes (a repository note for round 11 is pending). Lean round 3 of the side
session; written in a private Lake project (library `GTAORnd`, same Lean and Mathlib pins) and
moved here with only this header and the module lines changed.
-/
module

public import Mathlib

@[expose] public section

/-!
# Round 11-M Lean candidates: the hypercube correlation bound and "pure marginal ⇒ product"

**(a) Lemma 1 for hypercube parts (square: m = 2, cube: m = 3).** A part with Bloch vector
`r ∈ [-1,1]^m` has facet effects `(1 ± rᵢ)/2` and vertices at radius `R = √m`. A state of the
max composite of two such parts is `w = (1, a, b, C)`, and positivity on all products of facet
effects reads `0 ≤ 1 + s aᵢ + t bⱼ + s t Cᵢⱼ` for signs `s, t = ±1`. Then every `|Cᵢⱼ| ≤ 1`
and `‖C‖²_F ≤ m_A m_B = R_A² R_B²` (`cube_corr_bound`); the square case is
`square_corr_bound` (`‖C‖²_F ≤ 4`). Products of pure states attain it (`cube_corr_tight`).

**(b) Lemma 2, abstract finite form.** The max composite with a part `A` that has all
consistent reads gives, for each effect `f` of `B`, a conditional unnormalized state
`W f = λ_f ω_f` of `A` (`λ_f ≥ 0`, `ω_f ∈ Ω_A`), with `W f + W (u − f) = a`, the marginal.
These are hypotheses here. If `a` is an extreme point of `Ω_A` then every `W f` is a multiple
of `a`: the joint statistics factorize, `e(W f) = e(a)·u_A(W f)` (`pure_marginal_product`).
-/

namespace GTAORnd.SelfRef.LR3

/-- **Hypercube correlation bound** (PROVED-IN-MODEL). -/
theorem cube_corr_bound {mA mB : ℕ} (a : Fin mA → ℝ) (b : Fin mB → ℝ)
    (C : Matrix (Fin mA) (Fin mB) ℝ)
    (hpos : ∀ i j, ∀ s t : ℝ, s ^ 2 = 1 → t ^ 2 = 1 → 0 ≤ 1 + s * a i + t * b j + s * t * C i j) :
    (∀ i j, |C i j| ≤ 1) ∧ ∑ i, ∑ j, C i j ^ 2 ≤ mA * mB := by
  have hC : ∀ i j, |C i j| ≤ 1 := by
    intro i j
    have h1 := hpos i j 1 1 (by norm_num) (by norm_num)
    have h2 := hpos i j (-1) (-1) (by norm_num) (by norm_num)
    have h3 := hpos i j 1 (-1) (by norm_num) (by norm_num)
    have h4 := hpos i j (-1) 1 (by norm_num) (by norm_num)
    rw [abs_le]; constructor <;> linarith
  refine ⟨hC, ?_⟩
  have hsq : ∀ i j, C i j ^ 2 ≤ 1 := fun i j => (sq_le_one_iff_abs_le_one _).mpr (hC i j)
  calc ∑ i, ∑ j, C i j ^ 2 ≤ ∑ _i : Fin mA, ∑ _j : Fin mB, (1 : ℝ) :=
        Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j _ => hsq i j
    _ = mA * mB := by simp

/-- **Square case** (PROVED-IN-MODEL): `‖C‖²_F ≤ 2·2 = R_A² R_B²`. -/
theorem square_corr_bound (a b : Fin 2 → ℝ) (C : Matrix (Fin 2) (Fin 2) ℝ)
    (hpos : ∀ i j, ∀ s t : ℝ, s ^ 2 = 1 → t ^ 2 = 1 → 0 ≤ 1 + s * a i + t * b j + s * t * C i j) :
    ∑ i, ∑ j, C i j ^ 2 ≤ 4 := by
  have h := (cube_corr_bound a b C hpos).2
  simp only [Fin.sum_univ_two] at h ⊢; norm_num at h; linarith

/-- **Tightness**: a product of two vertices `a = v`, `b = w` (`vᵢ, wⱼ = ±1`), `C = v wᵀ`, is in
the max composite and has `‖C‖²_F = m_A m_B`. -/
theorem cube_corr_tight {mA mB : ℕ} (v : Fin mA → ℝ) (w : Fin mB → ℝ)
    (hv : ∀ i, v i ^ 2 = 1) (hw : ∀ j, w j ^ 2 = 1) :
    (∀ i j, ∀ s t : ℝ, s ^ 2 = 1 → t ^ 2 = 1 → 0 ≤ 1 + s * v i + t * w j + s * t * (v i * w j)) ∧
    ∑ i, ∑ j, (v i * w j) ^ 2 = mA * mB := by
  refine ⟨fun i j s t hs ht => ?_, ?_⟩
  · have : 1 + s * v i + t * w j + s * t * (v i * w j) = (1 + s * v i) * (1 + t * w j) := by ring
    rw [this]
    have h1 : 0 ≤ 1 + s * v i := by nlinarith [sq_nonneg (s - v i), sq_nonneg (s + v i), hv i]
    have h2 : 0 ≤ 1 + t * w j := by nlinarith [sq_nonneg (t - w j), sq_nonneg (t + w j), hw j]
    exact mul_nonneg h1 h2
  · simp [mul_pow, hv, hw]

/-- **Pure marginal ⇒ product** (PROVED-IN-MODEL, abstract form of Lemma 2). -/
theorem pure_marginal_product {V EB : Type*} [AddCommGroup V] [Module ℝ V]
    (Ω : Set V) (uA : V →ₗ[ℝ] ℝ) (huA : ∀ ω ∈ Ω, uA ω = 1)
    (a : V) (ha : a ∈ Set.extremePoints ℝ Ω)
    (compl : EB → EB) (W : EB → V) (hW : ∀ f, W f + W (compl f) = a)
    (hcone : ∀ f, ∃ l : ℝ, 0 ≤ l ∧ ∃ ω ∈ Ω, W f = l • ω) :
    ∀ f, W f = uA (W f) • a := by
  intro f
  obtain ⟨l, hl, ω, hω, hWf⟩ := hcone f
  obtain ⟨l', hl', ω', hω', hWf'⟩ := hcone (compl f)
  have haΩ := ha.1
  have hsum : l + l' = 1 := by
    have := congrArg uA (hW f)
    rw [map_add, hWf, hWf', map_smul, map_smul, huA ω hω, huA ω' hω', huA a haΩ] at this
    simpa using this
  have hu : uA (W f) = l := by rw [hWf, map_smul, huA ω hω, smul_eq_mul, mul_one]
  rw [hu]
  rcases eq_or_lt_of_le hl with h0 | hlpos
  · rw [hWf, ← h0, zero_smul, zero_smul]
  rcases eq_or_lt_of_le hl' with h0' | hl'pos
  · have hWf'0 : W (compl f) = 0 := by rw [hWf', ← h0', zero_smul]
    have : W f = a := by have := hW f; rwa [hWf'0, add_zero] at this
    rw [this, show l = 1 by linarith, one_smul]
  · -- a ∈ openSegment ω ω'
    have hseg : a ∈ openSegment ℝ ω ω' := ⟨l, l', hlpos, hl'pos, hsum, by rw [← hWf, ← hWf', hW]⟩
    have := ha.2 hω hω' hseg
    rw [hWf, this]

/-- consequence: the joint statistics factorize, `e(W f) = e(a)·u_A(W f)` for every linear `e` -/
theorem pure_marginal_factorizes {V EB : Type*} [AddCommGroup V] [Module ℝ V]
    (Ω : Set V) (uA : V →ₗ[ℝ] ℝ) (huA : ∀ ω ∈ Ω, uA ω = 1)
    (a : V) (ha : a ∈ Set.extremePoints ℝ Ω)
    (compl : EB → EB) (W : EB → V) (hW : ∀ f, W f + W (compl f) = a)
    (hcone : ∀ f, ∃ l : ℝ, 0 ≤ l ∧ ∃ ω ∈ Ω, W f = l • ω) (e : V →ₗ[ℝ] ℝ) (f : EB) :
    e (W f) = e a * uA (W f) := by
  rw [pure_marginal_product Ω uA huA a ha compl W hW hcone f, map_smul, smul_eq_mul, map_smul,
    smul_eq_mul, huA a ha.1]
  ring

/-! ## Exact forms of the round 12 note's Lean candidates L1 and L2 (R12-M.7) -/

/-- **L1 as stated in R12-M.7** (PROVED-IN-MODEL): the square case of `‖C‖ ≤ R_A R_B`. -/
theorem square_C_bound (a b : Fin 2 → ℝ) (C : Matrix (Fin 2) (Fin 2) ℝ)
    (h : ∀ i j : Fin 2, ∀ s t : ℝ, (s = 1 ∨ s = -1) → (t = 1 ∨ t = -1) →
          0 ≤ 1 + s * a i + t * b j + s * t * C i j) :
    ∑ i, ∑ j, (C i j) ^ 2 ≤ 4 := by
  apply square_corr_bound a b C
  intro i j s t hs ht
  have hs' : s = 1 ∨ s = -1 := by
    have : (s - 1) * (s + 1) = 0 := by ring_nf; linarith
    rcases mul_eq_zero.mp this with h | h
    · left; linarith
    · right; linarith
  have ht' : t = 1 ∨ t = -1 := by
    have : (t - 1) * (t + 1) = 0 := by ring_nf; linarith
    rcases mul_eq_zero.mp this with h | h
    · left; linarith
    · right; linarith
  exact h i j s t hs' ht'

/-- **L2, square instance** (PROVED-IN-MODEL): in the max product of two squares, if the
A-marginal coordinate `a i` is `±1` then `C i j = a i * b j` for every `j`; with both
coordinates `±1` (a pure marginal) the state is the product. -/
theorem square_pure_marginal (a b : Fin 2 → ℝ) (C : Matrix (Fin 2) (Fin 2) ℝ)
    (h : ∀ i j : Fin 2, ∀ s t : ℝ, (s = 1 ∨ s = -1) → (t = 1 ∨ t = -1) →
          0 ≤ 1 + s * a i + t * b j + s * t * C i j)
    (ha : ∀ i, a i = 1 ∨ a i = -1) : ∀ i j, C i j = a i * b j := by
  intro i j
  rcases ha i with h1 | h1
  · have p := h i j (-1) 1 (Or.inr rfl) (Or.inl rfl)
    have q := h i j (-1) (-1) (Or.inr rfl) (Or.inr rfl)
    rw [h1] at p q ⊢; linarith
  · have p := h i j 1 1 (Or.inl rfl) (Or.inl rfl)
    have q := h i j 1 (-1) (Or.inl rfl) (Or.inr rfl)
    rw [h1] at p q ⊢; linarith

/-- **L2, general finite form** (PROVED-IN-MODEL). Facet functionals `E r` of A (vectors on
homogeneous coordinates), a vertex `v` whose tight facets `T` cut out exactly the line through
`v`; facet functionals `F q` of B that span B's dual, with a positive combination equal to the
unit `uB`. If `X` is non-negative on every `E r ⊗ F q` and its A-marginal `X uB` is `v`, then
`X = v yᵀ` for some `y`. -/
theorem pure_marginal_finite {dA dB k l : ℕ} (E : Fin k → Fin dA → ℝ) (v : Fin dA → ℝ)
    (T : Finset (Fin k)) (hT : ∀ r ∈ T, E r ⬝ᵥ v = 0)
    (hline : ∀ y : Fin dA → ℝ, (∀ r ∈ T, E r ⬝ᵥ y = 0) → ∃ c : ℝ, y = c • v)
    (F : Fin l → Fin dB → ℝ) (uB : Fin dB → ℝ) (lam : Fin l → ℝ) (hlam : ∀ q, 0 < lam q)
    (hunit : ∑ q, lam q • F q = uB)
    (hspan : ∀ w : Fin dB → ℝ, (∀ q, w ⬝ᵥ F q = 0) → w = 0)
    (X : Matrix (Fin dA) (Fin dB) ℝ) (hpos : ∀ r q, 0 ≤ E r ⬝ᵥ (Matrix.mulVec X (F q)))
    (hmarg : Matrix.mulVec X (uB) = v) :
    ∃ y : Fin dB → ℝ, ∀ i j, X i j = v i * y j := by
  -- tight facets annihilate every X F q
  have hzero : ∀ r ∈ T, ∀ q, E r ⬝ᵥ (Matrix.mulVec X (F q)) = 0 := by
    intro r hr
    have hsum : ∑ q, lam q * (E r ⬝ᵥ (Matrix.mulVec X (F q))) = 0 := by
      rw [← hT r hr, ← hmarg, ← hunit, Matrix.mulVec_sum, dotProduct_sum]
      congr 1; funext q; rw [Matrix.mulVec_smul, dotProduct_smul, smul_eq_mul]
    have hnn : ∀ q ∈ Finset.univ, 0 ≤ lam q * (E r ⬝ᵥ (Matrix.mulVec X (F q))) :=
      fun q _ => mul_nonneg (hlam q).le (hpos r q)
    intro q
    have := (Finset.sum_eq_zero_iff_of_nonneg hnn).mp hsum q (Finset.mem_univ _)
    exact (mul_eq_zero.mp this).resolve_left (hlam q).ne'
  -- so Xᵀ E r = 0 for r ∈ T
  have hrow : ∀ r ∈ T, Matrix.vecMul (E r) X = 0 := by
    intro r hr
    apply hspan
    intro q
    rw [← Matrix.dotProduct_mulVec]
    exact hzero r hr q
  -- each column lies on the line through v
  have hcol : ∀ j, ∃ c : ℝ, (fun i => X i j) = c • v := by
    intro j
    apply hline
    intro r hr
    have := congrFun (hrow r hr) j
    simpa [Matrix.vecMul, dotProduct, mul_comm] using this
  choose c hc using hcol
  refine ⟨c, fun i j => ?_⟩
  have := congrFun (hc j) i
  simpa [mul_comm] using this

end GTAORnd.SelfRef.LR3
