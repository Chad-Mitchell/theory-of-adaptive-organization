/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost: round 10 note (`theory/RECORD_COST_ROUND10_2026-11-25.md`) §15, Theorem M11 as amended
by the side session's hostile review (Theorem M11′; a repository note for it is pending). Lean round 3 of the
side session; written in a private Lake project (library `GTAORnd`, same Lean and Mathlib pins) and moved
here with only this header, the module lines and the namespace changed.
-/
module

public import Mathlib

@[expose] public section

/-!
# Theorem M11′ (hostile review of M11): the Lean-able steps

Hypotheses as M11′ states them: centrally symmetric polytope parts with linear symmetry groups
`G_X = Aut(P_X)` that are vertex-transitive and absolutely irreducible, and 2-level
(`n·v ∈ {−1, +1}` for every facet normal `n` and vertex `v`); in `G_X`-invariant Euclidean
coordinates the facet normals have second moment `∑ n nᵀ = c I` (absolute irreducibility), all
normals have the same squared length `s` and all vertices the same squared radius `R²`
(transitivity). The steps below take exactly those consequences as hypotheses.
-/

namespace GTAORnd.SelfRef.LR3.M11Prime

open Matrix

/-- from a second-moment identity `∑ n nᵀ = c I`, the quadratic identity `∑ (n·x)² = c |x|²` -/
theorem moment_quad {m : ℕ} (N : Finset (Fin m → ℝ)) (c : ℝ)
    (hmom : ∑ n ∈ N, vecMulVec n n = c • (1 : Matrix (Fin m) (Fin m) ℝ)) (x : Fin m → ℝ) :
    ∑ n ∈ N, (n ⬝ᵥ x) ^ 2 = c * (x ⬝ᵥ x) := by
  have hent : ∀ i j, ∑ n ∈ N, n i * n j = c * (1 : Matrix (Fin m) (Fin m) ℝ) i j := by
    intro i j
    have := congrFun (congrFun hmom i) j
    simpa [Matrix.sum_apply, vecMulVec_apply] using this
  calc ∑ n ∈ N, (n ⬝ᵥ x) ^ 2
      = ∑ n ∈ N, ∑ i, ∑ j, x i * x j * (n i * n j) := by
        refine Finset.sum_congr rfl fun n _ => ?_
        simp only [dotProduct, sq, Finset.sum_mul, Finset.mul_sum]
        refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
        ring
    _ = ∑ i, ∑ j, x i * x j * ∑ n ∈ N, n i * n j := by
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl fun i _ => ?_
        rw [Finset.sum_comm]
        refine Finset.sum_congr rfl fun j _ => ?_
        rw [Finset.mul_sum]
    _ = c * (x ⬝ᵥ x) := by
        simp only [hent, dotProduct, Finset.mul_sum]
        refine Finset.sum_congr rfl fun i _ => ?_
        rw [Finset.sum_eq_single i]
        · simp; ring
        · intro j _ hj; simp [Ne.symm hj]
        · simp

/-- trace of the second moment: `∑ |n|² = c m` -/
theorem moment_trace {m : ℕ} (N : Finset (Fin m → ℝ)) (c : ℝ)
    (hmom : ∑ n ∈ N, vecMulVec n n = c • (1 : Matrix (Fin m) (Fin m) ℝ)) :
    ∑ n ∈ N, n ⬝ᵥ n = c * m := by
  have := congrArg Matrix.trace hmom
  simp only [Matrix.trace_sum, Matrix.trace_smul, Matrix.trace_one, Fintype.card_fin,
    smul_eq_mul] at this
  rw [← this]
  refine Finset.sum_congr rfl fun n _ => ?_
  simp [Matrix.trace, vecMulVec_apply, dotProduct]

/-- **(★) equivalence, finite form** (PROVED-IN-MODEL; hostile review, Lean-able step 1).
Vertices `V` on the sphere `|v|² = R²`, facet normals `N` with `|n|² = s` and `∑ n nᵀ = c I`,
and `|n·v| ≤ 1` throughout (facet inequalities at vertices of a centrally symmetric polytope).
Then the polytope is 2-level (`|n·v| = 1` for all `n, v`) iff `R² s = m`. -/
theorem star_equiv {m : ℕ} (V N : Finset (Fin m → ℝ)) (R2 s c : ℝ)
    (hV : ∀ v ∈ V, v ⬝ᵥ v = R2) (hN : ∀ n ∈ N, n ⬝ᵥ n = s)
    (hmom : ∑ n ∈ N, vecMulVec n n = c • (1 : Matrix (Fin m) (Fin m) ℝ))
    (hle : ∀ n ∈ N, ∀ v ∈ V, |n ⬝ᵥ v| ≤ 1)
    (hVne : V.Nonempty) (hNne : N.Nonempty) (hm : 0 < m) :
    (∀ n ∈ N, ∀ v ∈ V, |n ⬝ᵥ v| = 1) ↔ R2 * s = m := by
  have htr := moment_trace N c hmom
  rw [Finset.sum_congr rfl hN, Finset.sum_const, nsmul_eq_mul] at htr
  have hcard : (0 : ℝ) < N.card := by exact_mod_cast hNne.card_pos
  have hmR : (0 : ℝ) < m := by exact_mod_cast hm
  have hsq : ∀ v ∈ V, ∑ n ∈ N, (n ⬝ᵥ v) ^ 2 = c * R2 := fun v hv => by
    rw [moment_quad N c hmom v, hV v hv]
  constructor
  · intro h
    obtain ⟨v, hv⟩ := hVne
    have h1 : ∑ n ∈ N, (n ⬝ᵥ v) ^ 2 = N.card := by
      rw [Finset.card_eq_sum_ones, Nat.cast_sum]
      refine Finset.sum_congr rfl fun n hn => ?_
      rw [← sq_abs, h n hn v hv]; simp
    rw [hsq v hv] at h1
    -- c R2 = |N| and |N| s = c m
    have hc : c ≠ 0 := by intro hc; rw [hc] at h1; linarith
    have : c * (R2 * s) = c * m := by rw [← mul_assoc, h1, htr]
    exact mul_left_cancel₀ hc this
  · intro h n hn v hv
    have hsum : ∑ n ∈ N, (n ⬝ᵥ v) ^ 2 = N.card := by
      rw [hsq v hv]
      have : c * R2 * m = N.card * m := by
        calc c * R2 * m = R2 * (c * m) := by ring
          _ = R2 * (N.card * s) := by rw [htr]
          _ = N.card * (R2 * s) := by ring
          _ = N.card * m := by rw [h]
      exact mul_right_cancel₀ hmR.ne' this
    have hdef : ∑ n ∈ N, (1 - (n ⬝ᵥ v) ^ 2) = 0 := by
      rw [Finset.sum_sub_distrib, hsum]; simp
    have hnn : ∀ n ∈ N, 0 ≤ 1 - (n ⬝ᵥ v) ^ 2 := fun n hn => by
      have := hle n hn v hv
      have : (n ⬝ᵥ v) ^ 2 ≤ 1 := by
        rw [← sq_abs]; nlinarith [abs_nonneg (n ⬝ᵥ v)]
      linarith
    have h0 := (Finset.sum_eq_zero_iff_of_nonneg hnn).mp hdef n hn
    have : |n ⬝ᵥ v| ^ 2 = 1 := by rw [sq_abs]; linarith
    have ha := abs_nonneg (n ⬝ᵥ v)
    nlinarith

/-- **Max positivity ⇒ `|nᵀ C k| ≤ 1`** (PROVED-IN-MODEL; Lean-able step 3). The four products of
facet effects `(1 ± n·r)/2 ⊗ (1 ± k·r')/2` are non-negative on the state `(1, a, b, C)`. -/
theorem max_pos_corr {mA mB : ℕ} (a n : Fin mA → ℝ) (b k : Fin mB → ℝ)
    (C : Matrix (Fin mA) (Fin mB) ℝ)
    (h : ∀ s t : ℝ, (s = 1 ∨ s = -1) → (t = 1 ∨ t = -1) →
      0 ≤ 1 + s * (n ⬝ᵥ a) + t * (k ⬝ᵥ b) + s * t * (n ⬝ᵥ (C *ᵥ k))) :
    |n ⬝ᵥ (C *ᵥ k)| ≤ 1 := by
  have h1 := h 1 1 (Or.inl rfl) (Or.inl rfl)
  have h2 := h (-1) (-1) (Or.inr rfl) (Or.inr rfl)
  have h3 := h 1 (-1) (Or.inl rfl) (Or.inr rfl)
  have h4 := h (-1) 1 (Or.inr rfl) (Or.inl rfl)
  rw [abs_le]; constructor <;> nlinarith

/-- **Lemma 1, general finite form** (PROVED-IN-MODEL; Lean-able step 2, extends
`cube_corr_bound`). Second moments `∑ n nᵀ = (|N_A| s_A / m_A) I`, `∑ k kᵀ = (|N_B| s_B / m_B) I`
and `|nᵀ C k| ≤ 1` for all facet normals give `‖C‖²_F ≤ m_A m_B / (s_A s_B)`. -/
theorem lemma1_general {mA mB : ℕ} (NA : Finset (Fin mA → ℝ)) (NB : Finset (Fin mB → ℝ))
    (sA sB : ℝ) (hsA : 0 < sA) (hsB : 0 < sB) (hmA : 0 < mA) (hmB : 0 < mB)
    (hNA : NA.Nonempty) (hNB : NB.Nonempty)
    (hA : ∑ n ∈ NA, vecMulVec n n = (NA.card * sA / mA) • (1 : Matrix (Fin mA) (Fin mA) ℝ))
    (hB : ∑ k ∈ NB, vecMulVec k k = (NB.card * sB / mB) • (1 : Matrix (Fin mB) (Fin mB) ℝ))
    (C : Matrix (Fin mA) (Fin mB) ℝ) (hC : ∀ n ∈ NA, ∀ k ∈ NB, |n ⬝ᵥ (C *ᵥ k)| ≤ 1) :
    ∑ i, ∑ j, C i j ^ 2 ≤ mA * mB / (sA * sB) := by
  set cA := (NA.card * sA / mA : ℝ)
  set cB := (NB.card * sB / mB : ℝ)
  have hcA : 0 < (NA.card : ℝ) := by exact_mod_cast hNA.card_pos
  have hcB : 0 < (NB.card : ℝ) := by exact_mod_cast hNB.card_pos
  have hmA' : (0 : ℝ) < mA := by exact_mod_cast hmA
  have hmB' : (0 : ℝ) < mB := by exact_mod_cast hmB
  have hcApos : 0 < cA := by positivity
  have hcBpos : 0 < cB := by positivity
  -- ∑_n ∑_k (nᵀ C k)² = cA cB ‖C‖²
  have hid : ∑ n ∈ NA, ∑ k ∈ NB, (n ⬝ᵥ (C *ᵥ k)) ^ 2 = cA * cB * ∑ i, ∑ j, C i j ^ 2 := by
    have step1 : ∀ n, ∑ k ∈ NB, (n ⬝ᵥ (C *ᵥ k)) ^ 2 = cB * (vecMul n C ⬝ᵥ vecMul n C) := by
      intro n
      rw [← moment_quad NB cB hB (vecMul n C)]
      refine Finset.sum_congr rfl fun k _ => ?_
      rw [dotProduct_mulVec, dotProduct_comm]
    simp only [step1, ← Finset.mul_sum]
    have step2 : ∑ n ∈ NA, vecMul n C ⬝ᵥ vecMul n C = cA * ∑ i, ∑ j, C i j ^ 2 := by
      have : ∀ n, vecMul n C ⬝ᵥ vecMul n C = ∑ j, (n ⬝ᵥ (fun i => C i j)) ^ 2 := by
        intro n; simp [dotProduct, vecMul, sq]
      simp only [this]
      rw [Finset.sum_comm]
      simp only [moment_quad NA cA hA, ← Finset.mul_sum]
      congr 1
      rw [Finset.sum_comm]
      simp [dotProduct, sq]
    rw [step2]; ring
  have hle : ∑ n ∈ NA, ∑ k ∈ NB, (n ⬝ᵥ (C *ᵥ k)) ^ 2 ≤ NA.card * NB.card := by
    calc ∑ n ∈ NA, ∑ k ∈ NB, (n ⬝ᵥ (C *ᵥ k)) ^ 2 ≤ ∑ n ∈ NA, ∑ k ∈ NB, (1 : ℝ) := by
          refine Finset.sum_le_sum fun n hn => Finset.sum_le_sum fun k hk => ?_
          have := hC n hn k hk
          rw [← sq_abs]; nlinarith [abs_nonneg (n ⬝ᵥ (C *ᵥ k))]
      _ = NA.card * NB.card := by simp
  rw [hid] at hle
  rw [le_div_iff₀ (by positivity)]
  have : cA * cB = NA.card * NB.card * (sA * sB) / (mA * mB) := by
    simp only [cA, cB]; field_simp
  rw [this] at hle
  have hpos : (0 : ℝ) < NA.card * NB.card := by positivity
  have := hle
  rw [div_mul_eq_mul_div, div_le_iff₀ (by positivity)] at this
  nlinarith

/-- **Strictness** (PROVED-IN-MODEL; Lean-able step 4): a point of the convex hull of points on
the sphere of radius `R` that is not one of them has norm `< R` (strict convexity). -/
theorem hull_strict {m : ℕ} (V : Set (EuclideanSpace ℝ (Fin m))) (R : ℝ)
    (hV : ∀ v ∈ V, ‖v‖ = R) {x : EuclideanSpace ℝ (Fin m)} (hx : x ∈ convexHull ℝ V)
    (hxV : x ∉ V) : ‖x‖ < R := by
  have hball : convexHull ℝ V ⊆ Metric.closedBall 0 R :=
    convexHull_min (fun v hv => by simp [hV v hv]) (convex_closedBall 0 R)
  have hle : ∀ y ∈ convexHull ℝ V, ‖y‖ ≤ R := fun y hy => by
    simpa using hball hy
  rcases (hle x hx).lt_or_eq with h | h
  · exact h
  exfalso
  apply hxV
  apply extremePoints_convexHull_subset (𝕜 := ℝ)
  refine ⟨hx, fun x₁ h₁ x₂ h₂ hseg => ?_⟩
  obtain ⟨a, b, ha, hb, hab, hxe⟩ := hseg
  by_cases hne : x₁ = x₂
  · subst hne; rw [← add_smul, hab, one_smul] at hxe; exact hxe
  · have := norm_combo_lt_of_ne (hle x₁ h₁) (hle x₂ h₂) hne ha hb hab
    rw [hxe, h] at this; exact absurd this (lt_irrefl _)

/-- **Averaging instead of John, for polytopes** (PROVED-IN-MODEL; Lean-able step 6). For a
finite group `Γ` acting linearly by `ρ`, and `M` symmetric positive definite, the average
`∑_g ρ(g)ᵀ M ρ(g)` is symmetric, positive definite and `Γ`-invariant. -/
theorem average_invariant {m : ℕ} {Γ : Type*} [Group Γ] [Fintype Γ]
    (ρ : Γ →* Matrix (Fin m) (Fin m) ℝ) (M : Matrix (Fin m) (Fin m) ℝ)
    (hMs : Mᵀ = M) (hMp : ∀ x : Fin m → ℝ, x ≠ 0 → 0 < x ⬝ᵥ (M *ᵥ x)) :
    let A := ∑ g, (ρ g)ᵀ * M * ρ g
    Aᵀ = A ∧ (∀ x : Fin m → ℝ, x ≠ 0 → 0 < x ⬝ᵥ (A *ᵥ x)) ∧
      ∀ h : Γ, (ρ h)ᵀ * A * ρ h = A := by
  intro A
  refine ⟨?_, ?_, ?_⟩
  · simp only [A, transpose_sum, transpose_mul, transpose_transpose, hMs, Matrix.mul_assoc]
  · intro x hx
    have hterm : ∀ g, x ⬝ᵥ (((ρ g)ᵀ * M * ρ g) *ᵥ x) = (ρ g *ᵥ x) ⬝ᵥ (M *ᵥ (ρ g *ᵥ x)) := by
      intro g
      rw [← mulVec_mulVec, ← mulVec_mulVec, dotProduct_mulVec, vecMul_transpose]
    have hpos : ∀ g, 0 < x ⬝ᵥ (((ρ g)ᵀ * M * ρ g) *ᵥ x) := by
      intro g
      rw [hterm]
      apply hMp
      intro h0
      apply hx
      have : ρ g⁻¹ *ᵥ (ρ g *ᵥ x) = x := by
        rw [mulVec_mulVec, ← map_mul, inv_mul_cancel, map_one, one_mulVec]
      rw [← this, h0, mulVec_zero]
    simp only [A, sum_mulVec, dotProduct_sum]
    exact Finset.sum_pos (fun g _ => hpos g) Finset.univ_nonempty
  · intro h
    simp only [A, Matrix.sum_mul, Matrix.mul_sum]
    refine Fintype.sum_equiv (Equiv.mulRight h) _ _ (fun g => ?_)
    simp only [Equiv.coe_mulRight, map_mul, transpose_mul, Matrix.mul_assoc]

/-- **Final assembly** (PROVED-IN-MODEL; Lean-able step 7). `T` is a bijection of the extreme
points `E` preserving `q`, and `q` is strictly larger at the product pure states `P ⊆ E` than at
every other extreme point. Then `T` maps `P` onto `P`. -/
theorem final_assembly {X : Type*} (E P : Set X) (hPE : P ⊆ E) (q : X → ℝ) (T : X → X)
    (hTE : T '' E = E) (hq : ∀ x, q (T x) = q x)
    (hstrict : ∀ p ∈ P, ∀ e ∈ E, e ∉ P → q e < q p) : T '' P = P := by
  apply Set.Subset.antisymm
  · rintro _ ⟨p, hp, rfl⟩
    by_contra hn
    have hTp : T p ∈ E := hTE ▸ ⟨p, hPE hp, rfl⟩
    have := hstrict p hp (T p) hTp hn
    rw [hq] at this; exact lt_irrefl _ this
  · intro p hp
    have : p ∈ T '' E := hTE.symm ▸ hPE hp
    obtain ⟨e, he, rfl⟩ := this
    by_cases heP : e ∈ P
    · exact ⟨e, heP, rfl⟩
    · have := hstrict (T e) hp e he heP
      rw [hq] at this; exact absurd this (lt_irrefl _)


/-- **Schur step, scalar block** (PROVED-IN-MODEL; part of Lean-able step 8). For an orthogonal
representation `G` (`gᵀ g = 1`) whose commutant is the scalars (absolute irreducibility), every
`G`-invariant form `P` (`gᵀ P g = P`) is a multiple of the identity. -/
theorem invariant_form_scalar {m : ℕ} (G : Set (Matrix (Fin m) (Fin m) ℝ))
    (horth : ∀ g ∈ G, gᵀ * g = 1)
    (habs : ∀ X : Matrix (Fin m) (Fin m) ℝ, (∀ g ∈ G, X * g = g * X) → ∃ c : ℝ, X = c • 1)
    (P : Matrix (Fin m) (Fin m) ℝ) (hP : ∀ g ∈ G, gᵀ * P * g = P) : ∃ c : ℝ, P = c • 1 := by
  apply habs
  intro g hg
  have hinv : g * gᵀ = 1 := mul_eq_one_comm.mp (horth g hg)
  calc P * g = (g * gᵀ) * (P * g) := by rw [hinv, Matrix.one_mul]
    _ = g * (gᵀ * P * g) := by simp only [Matrix.mul_assoc]
    _ = g * P := by rw [hP g hg]

/-- **Schur step, no cross terms** (PROVED-IN-MODEL; part of Lean-able step 8). A coupling `L`
between a part on which `G` acts and a part it leaves fixed, invariant in the sense `gᵀ L = L`,
vanishes as soon as `-1 ∈ G` (central symmetry). -/
theorem cross_term_zero {m k : ℕ} (G : Set (Matrix (Fin m) (Fin m) ℝ))
    (hneg : (-1 : Matrix (Fin m) (Fin m) ℝ) ∈ G) (L : Matrix (Fin m) (Fin k) ℝ)
    (hL : ∀ g ∈ G, gᵀ * L = L) : L = 0 := by
  have h := hL _ hneg
  simp only [transpose_neg, transpose_one, Matrix.neg_mul, Matrix.one_mul] at h
  have : (2 : ℝ) • L = 0 := by rw [two_smul]; nth_rewrite 1 [← h]; simp
  exact (smul_eq_zero.mp this).resolve_left two_ne_zero


end GTAORnd.SelfRef.LR3.M11Prime
