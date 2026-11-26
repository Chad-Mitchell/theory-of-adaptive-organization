/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost: Theorem M11′ (round 10 note §15, as amended by the side session's hostile
review), assembled for hypercube and cross-polytope parts. Lean round 4 of the side session; written
in a private Lake project (library `GTAORnd`, same Lean and Mathlib pins) and moved here with only
this header, the module lines, the namespace and the last step of the assembled theorems (which call
`M11Prime.final_assembly`) changed.
-/
module

public import Mathlib
public import GTAO.Rnd.SelfRef.M11Prime

@[expose] public section

/-!
# Theorem M11′ assembled for hypercube parts (Lean round 4)

Homogeneous tensor coordinates: the composite's vector space is `ℝ^{1+m_A} ⊗ ℝ^{1+m_B}`, indexed by
`Option (Fin m_A) × Option (Fin m_B)`: `(none,none)` is the unit coordinate, `(some i, none)` the
A-Bloch coordinate `a_i`, `(none, some j)` the B-Bloch coordinate `b_j`, `(some i, some j)` the
correlation `C_ij`. The local symmetries used are the coordinate sign flips and coordinate swaps of
each part (these generate the hyperoctahedral group, the symmetry group of the cube and of the
cross-polytope).
-/

namespace GTAORnd.SelfRef.LR3.M11Cube

open Matrix

abbrev Idx (mA mB : ℕ) := Option (Fin mA) × Option (Fin mB)

variable {mA mB : ℕ}

/-- sign flip of A's coordinate `i`, as a diagonal on the composite -/
def rowSign (i : Fin mA) : Idx mA mB → ℝ := fun u => if u.1 = some i then -1 else 1
/-- sign flip of B's coordinate `j` -/
def colSign (j : Fin mB) : Idx mA mB → ℝ := fun u => if u.2 = some j then -1 else 1
/-- swap of A's coordinates `i, i'` -/
def rowSwap (i i' : Fin mA) : Equiv.Perm (Idx mA mB) :=
  Equiv.prodCongr (Equiv.optionCongr (Equiv.swap i i')) (Equiv.refl _)
/-- swap of B's coordinates `j, j'` -/
def colSwap (j j' : Fin mB) : Equiv.Perm (Idx mA mB) :=
  Equiv.prodCongr (Equiv.refl _) (Equiv.optionCongr (Equiv.swap j j'))
/-- the permutation matrix of `σ`: `(P x) w = x (σ⁻¹ w)` -/
def permMat (σ : Equiv.Perm (Idx mA mB)) : Matrix (Idx mA mB) (Idx mA mB) ℝ :=
  Matrix.of fun w u => if w = σ u then 1 else 0

theorem diag_conj_entry (d : Idx mA mB → ℝ) (M : Matrix (Idx mA mB) (Idx mA mB) ℝ)
    (h : (diagonal d)ᵀ * M * diagonal d = M) (u v : Idx mA mB) :
    d u * M u v * d v = M u v := by
  have := congrFun (congrFun h u) v
  rw [diagonal_transpose, mul_diagonal, diagonal_mul] at this
  exact this

theorem perm_conj_entry (σ : Equiv.Perm (Idx mA mB)) (M : Matrix (Idx mA mB) (Idx mA mB) ℝ)
    (h : (permMat σ)ᵀ * M * permMat σ = M) (u v : Idx mA mB) :
    M (σ u) (σ v) = M u v := by
  have := congrFun (congrFun h u) v
  simp [permMat, Matrix.mul_apply] at this
  exact this

/-- **Schur step for hyperoctahedral parts, off-diagonal part** (PROVED-IN-MODEL): a matrix
invariant under every coordinate sign flip of A and of B is diagonal in tensor coordinates. -/
theorem flip_invariant_diag (M : Matrix (Idx mA mB) (Idx mA mB) ℝ)
    (hr : ∀ i, (diagonal (rowSign i))ᵀ * M * diagonal (rowSign i) = M)
    (hc : ∀ j, (diagonal (colSign j))ᵀ * M * diagonal (colSign j) = M) :
    ∀ u v : Idx mA mB, u ≠ v → M u v = 0 := by
  intro u v huv
  have key : ∀ (d : Idx mA mB → ℝ), (diagonal d)ᵀ * M * diagonal d = M →
      d u * d v = -1 → M u v = 0 := by
    intro d hd hneg
    have := diag_conj_entry d M hd u v
    have : M u v = - M u v := by
      calc M u v = d u * M u v * d v := this.symm
        _ = (d u * d v) * M u v := by ring
        _ = - M u v := by rw [hneg]; ring
    linarith
  by_cases h1 : u.1 = v.1
  · have h2 : u.2 ≠ v.2 := fun h2 => huv (Prod.ext h1 h2)
    rcases hu : u.2 with _ | j
    · rcases hv : v.2 with _ | j'
      · exact absurd (hu.trans hv.symm) h2
      · apply key (colSign j') (hc j')
        simp [colSign, hu, hv]
    · apply key (colSign j) (hc j)
      have : v.2 ≠ some j := fun e => h2 (hu.trans e.symm)
      simp [colSign, hu, this]
  · rcases hu : u.1 with _ | i
    · rcases hv : v.1 with _ | i'
      · exact absurd (hu.trans hv.symm) h1
      · apply key (rowSign i') (hr i')
        simp [rowSign, hu, hv]
    · apply key (rowSign i) (hr i)
      have : v.1 ≠ some i := fun e => h1 (hu.trans e.symm)
      simp [rowSign, hu, this]

/-- **Schur step, diagonal part** (PROVED-IN-MODEL): coordinate swaps make the diagonal constant on
each block. -/
theorem swap_invariant_blocks (M : Matrix (Idx mA mB) (Idx mA mB) ℝ)
    (hrs : ∀ i i', (permMat (rowSwap i i'))ᵀ * M * permMat (rowSwap i i') = M)
    (hcs : ∀ j j', (permMat (colSwap j j'))ᵀ * M * permMat (colSwap j j') = M) :
    (∀ i i', M (some i, none) (some i, none) = M (some i', none) (some i', none)) ∧
    (∀ j j', M (none, some j) (none, some j) = M (none, some j') (none, some j')) ∧
    (∀ i i' j j', M (some i, some j) (some i, some j) = M (some i', some j') (some i', some j')) := by
  have hr : ∀ i i' (y : Option (Fin mB)), M (some i, y) (some i, y) = M (some i', y) (some i', y) := by
    intro i i' y
    have := perm_conj_entry (rowSwap i i') M (hrs i i') (some i, y) (some i, y)
    simpa [rowSwap] using this.symm
  have hc : ∀ (x : Option (Fin mA)) j j', M (x, some j) (x, some j) = M (x, some j') (x, some j') := by
    intro x j j'
    have := perm_conj_entry (colSwap j j') M (hcs j j') (x, some j) (x, some j)
    simpa [colSwap] using this.symm
  exact ⟨fun i i' => hr i i' none, fun j j' => hc none j j',
    fun i i' j j' => (hr i i' (some j)).trans (hc (some i') j j')⟩

/-- the quadratic form of a matrix that is diagonal: `xᵀ M x = ∑ M_uu x_u²` -/
theorem quad_of_diag (M : Matrix (Idx mA mB) (Idx mA mB) ℝ) (hd : ∀ u v, u ≠ v → M u v = 0)
    (x : Idx mA mB → ℝ) : x ⬝ᵥ (M *ᵥ x) = ∑ u, M u u * x u ^ 2 := by
  simp only [dotProduct, mulVec]
  refine Finset.sum_congr rfl fun u _ => ?_
  rw [Finset.sum_eq_single u (fun v _ hv => by rw [hd u v (Ne.symm hv), zero_mul])
    (by simp)]
  ring

/-! ### The maximal tensor product of two cubes and its pure products -/

/-- the maximal tensor product of the cubes `[-1,1]^{m_A}` and `[-1,1]^{m_B}` (normalized states):
`x₀₀ = 1` and every product of facet functionals `(1 + s a_i)(1 + t b_j)` is nonnegative. -/
def maxSet (mA mB : ℕ) : Set (Idx mA mB → ℝ) :=
  {x | x (none, none) = 1 ∧ ∀ (i : Fin mA) (j : Fin mB) (s t : ℝ), (s = 1 ∨ s = -1) →
    (t = 1 ∨ t = -1) →
    0 ≤ 1 + s * x (some i, none) + t * x (none, some j) + s * t * x (some i, some j)}

/-- extend a coordinate vector by the unit coordinate -/
def ext1 {m : ℕ} (v : Fin m → ℝ) : Option (Fin m) → ℝ
  | none => 1
  | some i => v i

/-- the product state of `v` and `w` -/
def pureProd (v : Fin mA → ℝ) (w : Fin mB → ℝ) : Idx mA mB → ℝ := fun u => ext1 v u.1 * ext1 w u.2

/-- sign vector: a vertex of the cube -/
def IsSign {m : ℕ} (v : Fin m → ℝ) : Prop := ∀ i, v i = 1 ∨ v i = -1

/-- products of cube vertices: the pure states of the composite -/
def pureSet (mA mB : ℕ) : Set (Idx mA mB → ℝ) :=
  {x | ∃ v w, IsSign v ∧ IsSign w ∧ x = pureProd v w}

lemma sq_one_of_sign {a : ℝ} (h : a = 1 ∨ a = -1) : a ^ 2 = 1 := by
  rcases h with rfl | rfl <;> norm_num

lemma ext1_sq {m : ℕ} {v : Fin m → ℝ} (hv : IsSign v) (o : Option (Fin m)) : ext1 v o ^ 2 = 1 := by
  cases o with
  | none => simp [ext1]
  | some i => exact sq_one_of_sign (hv i)

theorem pureProd_mem_maxSet {v : Fin mA → ℝ} {w : Fin mB → ℝ} (hv : IsSign v) (hw : IsSign w) :
    pureProd v w ∈ maxSet mA mB := by
  refine ⟨by simp [pureProd, ext1], fun i j s t hs ht => ?_⟩
  have h1 : 0 ≤ 1 + s * v i := by rcases hs with rfl | rfl <;> rcases hv i with h | h <;> rw [h] <;> norm_num
  have h2 : 0 ≤ 1 + t * w j := by rcases ht with rfl | rfl <;> rcases hw j with h | h <;> rw [h] <;> norm_num
  have := mul_nonneg h1 h2
  simp only [pureProd, ext1]
  nlinarith

/-- every coordinate of a point of the maximal tensor product lies in `[-1,1]` (both parts have
dimension ≥ 1) -/
theorem maxSet_sq_le (hA : 0 < mA) (hB : 0 < mB) {x : Idx mA mB → ℝ} (hx : x ∈ maxSet mA mB)
    (u : Idx mA mB) : x u ^ 2 ≤ 1 := by
  obtain ⟨h0, hc⟩ := hx
  have i0 : Fin mA := ⟨0, hA⟩
  have j0 : Fin mB := ⟨0, hB⟩
  rcases u with ⟨_ | i, _ | j⟩
  · simp [h0]
  · have h1 := hc i0 j 1 1 (Or.inl rfl) (Or.inl rfl)
    have h2 := hc i0 j (-1) 1 (Or.inr rfl) (Or.inl rfl)
    have h3 := hc i0 j 1 (-1) (Or.inl rfl) (Or.inr rfl)
    have h4 := hc i0 j (-1) (-1) (Or.inr rfl) (Or.inr rfl)
    nlinarith
  · have h1 := hc i j0 1 1 (Or.inl rfl) (Or.inl rfl)
    have h2 := hc i j0 (-1) 1 (Or.inr rfl) (Or.inl rfl)
    have h3 := hc i j0 1 (-1) (Or.inl rfl) (Or.inr rfl)
    have h4 := hc i j0 (-1) (-1) (Or.inr rfl) (Or.inr rfl)
    nlinarith
  · have h1 := hc i j 1 1 (Or.inl rfl) (Or.inl rfl)
    have h2 := hc i j (-1) 1 (Or.inr rfl) (Or.inl rfl)
    have h3 := hc i j 1 (-1) (Or.inl rfl) (Or.inr rfl)
    have h4 := hc i j (-1) (-1) (Or.inr rfl) (Or.inr rfl)
    nlinarith

lemma sign_of_sq {a : ℝ} (h : a ^ 2 = 1) : a = 1 ∨ a = -1 := by
  have : (a - 1) * (a + 1) = 0 := by nlinarith
  rcases mul_eq_zero.1 this with h | h
  · left; linarith
  · right; linarith

/-- a point of the maximal tensor product all of whose coordinates are `±1` is a product of cube
vertices -/
theorem pure_of_sq_one {x : Idx mA mB → ℝ} (hx : x ∈ maxSet mA mB) (h1 : ∀ u, x u ^ 2 = 1) :
    x ∈ pureSet mA mB := by
  obtain ⟨h0, hc⟩ := hx
  refine ⟨fun i => x (some i, none), fun j => x (none, some j), fun i => sign_of_sq (h1 _),
    fun j => sign_of_sq (h1 _), ?_⟩
  funext u
  rcases u with ⟨_ | i, _ | j⟩
  · simp [pureProd, ext1, h0]
  · simp [pureProd, ext1]
  · simp [pureProd, ext1]
  · simp only [pureProd, ext1]
    have ha := sign_of_sq (h1 (some i, none))
    have hb := sign_of_sq (h1 (none, some j))
    have hC := sign_of_sq (h1 (some i, some j))
    have key := hc i j (-x (some i, none)) (-x (none, some j))
      (by rcases ha with h | h <;> rw [h] <;> norm_num)
      (by rcases hb with h | h <;> rw [h] <;> norm_num)
    rcases ha with ha | ha <;> rcases hb with hb | hb <;> rcases hC with hC | hC <;>
      (rw [ha, hb, hC] at key; rw [ha, hb, hC]; first | (norm_num at key; done) | norm_num)

/-! ### Finite-group averaging and the assembled theorem -/

section Avg

variable {Γ : Type*} [Group Γ] [Fintype Γ]

/-- the group-averaged Gram matrix `A = ∑_γ ρ(γ)ᵀ ρ(γ)` -/
def avgGram (ρ : Γ →* Matrix (Idx mA mB) (Idx mA mB) ℝ) : Matrix (Idx mA mB) (Idx mA mB) ℝ :=
  ∑ γ, (ρ γ)ᵀ * ρ γ

theorem avgGram_invariant (ρ : Γ →* Matrix (Idx mA mB) (Idx mA mB) ℝ) (h : Γ) :
    (ρ h)ᵀ * avgGram ρ * ρ h = avgGram ρ := by
  unfold avgGram
  rw [Finset.mul_sum, Finset.sum_mul]
  refine Fintype.sum_equiv (Equiv.mulRight h) _ _ fun γ => ?_
  simp only [Equiv.coe_mulRight, map_mul, transpose_mul, Matrix.mul_assoc]

theorem avgGram_diag_ge_one (ρ : Γ →* Matrix (Idx mA mB) (Idx mA mB) ℝ) (u : Idx mA mB) :
    1 ≤ avgGram ρ u u := by
  have hnn : ∀ γ, 0 ≤ ((ρ γ)ᵀ * ρ γ) u u := fun γ => by
    rw [Matrix.mul_apply]
    exact Finset.sum_nonneg fun w _ => by rw [transpose_apply]; exact mul_self_nonneg _
  have h1 : ((ρ 1)ᵀ * ρ 1) u u = 1 := by simp [map_one]
  unfold avgGram
  rw [Matrix.sum_apply]
  calc (1 : ℝ) = ((ρ 1)ᵀ * ρ 1) u u := h1.symm
    _ ≤ ∑ γ, ((ρ γ)ᵀ * ρ γ) u u := Finset.single_le_sum (fun γ _ => hnn γ) (Finset.mem_univ _)

end Avg

lemma quad_conj (A M : Matrix (Idx mA mB) (Idx mA mB) ℝ) (x : Idx mA mB → ℝ) :
    (M *ᵥ x) ⬝ᵥ (A *ᵥ (M *ᵥ x)) = x ⬝ᵥ ((Mᵀ * A * M) *ᵥ x) := by
  rw [← mulVec_mulVec, ← mulVec_mulVec, dotProduct_mulVec x Mᵀ, vecMul_transpose]

/-- on the maximal tensor product, a diagonal form with positive diagonal is bounded by its trace,
with equality exactly at the points all of whose coordinates are `±1` -/
theorem diag_form_max (hA : 0 < mA) (hB : 0 < mB) (A : Matrix (Idx mA mB) (Idx mA mB) ℝ)
    (hpos : ∀ u, 0 < A u u) {x : Idx mA mB → ℝ} (hx : x ∈ maxSet mA mB) :
    ∑ u, A u u * x u ^ 2 ≤ ∑ u, A u u ∧
      (∑ u, A u u * x u ^ 2 = ∑ u, A u u → ∀ u, x u ^ 2 = 1) := by
  have hle : ∀ u, A u u * x u ^ 2 ≤ A u u := fun u => by
    have := maxSet_sq_le hA hB hx u
    nlinarith [hpos u]
  refine ⟨Finset.sum_le_sum fun u _ => hle u, fun heq u => ?_⟩
  have hz : ∑ v, (A v v - A v v * x v ^ 2) = 0 := by
    rw [Finset.sum_sub_distrib, heq, sub_self]
  have := (Finset.sum_eq_zero_iff_of_nonneg (fun v _ => sub_nonneg.2 (hle v))).1 hz u
    (Finset.mem_univ _)
  have h2 : A u u * (1 - x u ^ 2) = 0 := by linarith
  rcases mul_eq_zero.1 h2 with h | h
  · exact absurd h (hpos u).ne'
  · linarith

/-- **No reversible map entangles, hypercube parts** (PROVED-IN-MODEL). Setting as in `m11_cube`:
every element of the finite group `Γ` that maps `S` into `S` maps each product state to a product
state. The quadratic form `q(x) = xᵀ A x`, `A = ∑_γ ρ(γ)ᵀ ρ(γ)`, is `Γ`-invariant; invariance under
the local sign flips makes `A` diagonal (`flip_invariant_diag`, the Schur step for the
hyperoctahedral group) with diagonal `≥ 1`; on `maxSet` `q` is at most `tr A`, with equality only at
the points with every coordinate `±1`, which are the product states (`pure_of_sq_one`). -/
theorem m11_cube_into {Γ : Type*} [Group Γ] [Fintype Γ] (hA : 0 < mA) (hB : 0 < mB)
    (ρ : Γ →* Matrix (Idx mA mB) (Idx mA mB) ℝ)
    (hr : ∀ i, ∃ g, ρ g = diagonal (rowSign i)) (hc : ∀ j, ∃ g, ρ g = diagonal (colSign j))
    (S : Set (Idx mA mB → ℝ)) (hS : S ⊆ maxSet mA mB) (hP : pureSet mA mB ⊆ S)
    (g : Γ) (hg : ∀ x ∈ S, ρ g *ᵥ x ∈ S) :
    ∀ p ∈ pureSet mA mB, ρ g *ᵥ p ∈ pureSet mA mB := by
  set A := avgGram ρ with hAdef
  have hinv : ∀ g, (ρ g)ᵀ * A * ρ g = A := avgGram_invariant ρ
  have hdiag : ∀ u v, u ≠ v → A u v = 0 := flip_invariant_diag A
    (fun i => by obtain ⟨g, hg⟩ := hr i; rw [← hg]; exact hinv g)
    (fun j => by obtain ⟨g, hg⟩ := hc j; rw [← hg]; exact hinv g)
  have hpos : ∀ u, 0 < A u u := fun u => lt_of_lt_of_le one_pos (avgGram_diag_ge_one ρ u)
  intro p hp
  have hpS := hg p (hP hp)
  obtain ⟨v, w, hv, hw, rfl⟩ := hp
  have hsq : ∀ u, pureProd v w u ^ 2 = 1 := fun u => by
    simp only [pureProd, mul_pow, ext1_sq hv, ext1_sq hw, mul_one]
  have hq : (ρ g *ᵥ pureProd v w) ⬝ᵥ (A *ᵥ (ρ g *ᵥ pureProd v w)) =
      pureProd v w ⬝ᵥ (A *ᵥ pureProd v w) := by rw [quad_conj, hinv]
  rw [quad_of_diag A hdiag, quad_of_diag A hdiag] at hq
  simp only [hsq, mul_one] at hq
  exact pure_of_sq_one (hS hpS) ((diag_form_max hA hB A hpos (hS hpS)).2 hq)

/-- **Theorem M11′, assembled for two hypercube parts** (PROVED-IN-MODEL).

Setting: the composite of the cubes `[-1,1]^{m_A}`, `[-1,1]^{m_B}` (`m_A, m_B ≥ 1`) is any set `S`
of normalized states with `pureSet ⊆ S ⊆ maxSet` (between the minimal and maximal tensor products).
`Γ` is any finite group acting linearly on the tensor coordinates (`ρ`) whose image contains the
local coordinate sign flips of both parts; the intended instance is `Γ = Aut(S)`, the linear symmetry
group of the polytope `S`, which is finite and contains the local symmetries (that instance, the
finiteness of `Aut(S)`, is not formalized here: `Γ` and `ρ` are hypotheses). Conclusion: every
element of `Γ` that maps `S` onto `S` maps the product states onto the product states. The last
step is `M11Prime.final_assembly` applied with `E := S`.

Proof route as in M11′: the averaged form `q = xᵀ A x` is `Γ`-invariant (finite-group averaging);
invariance under the local sign flips makes `A` diagonal (the Schur step for the hyperoctahedral
group, `flip_invariant_diag`); its diagonal is positive; on `maxSet` `q` is maximal exactly at the
`±1` points, which are the product states (`pure_of_sq_one`). -/
theorem m11_cube {Γ : Type*} [Group Γ] [Fintype Γ] (hA : 0 < mA) (hB : 0 < mB)
    (ρ : Γ →* Matrix (Idx mA mB) (Idx mA mB) ℝ)
    (hr : ∀ i, ∃ g, ρ g = diagonal (rowSign i)) (hc : ∀ j, ∃ g, ρ g = diagonal (colSign j))
    (S : Set (Idx mA mB → ℝ)) (hS : S ⊆ maxSet mA mB) (hP : pureSet mA mB ⊆ S)
    (γ0 : Γ) (hT : (fun x => ρ γ0 *ᵥ x) '' S = S) :
    (fun x => ρ γ0 *ᵥ x) '' pureSet mA mB = pureSet mA mB := by
  set A := avgGram ρ with hAdef
  have hinv : ∀ g, (ρ g)ᵀ * A * ρ g = A := avgGram_invariant ρ
  have hdiag : ∀ u v, u ≠ v → A u v = 0 := flip_invariant_diag A
    (fun i => by obtain ⟨g, hg⟩ := hr i; rw [← hg]; exact hinv g)
    (fun j => by obtain ⟨g, hg⟩ := hc j; rw [← hg]; exact hinv g)
  have hpos : ∀ u, 0 < A u u := fun u => lt_of_lt_of_le one_pos (avgGram_diag_ge_one ρ u)
  -- the last step is `M11Prime.final_assembly` with `E := S`
  refine M11Prime.final_assembly S (pureSet mA mB) hP (fun x => x ⬝ᵥ (A *ᵥ x))
    (fun x => ρ γ0 *ᵥ x) hT (fun x => by rw [quad_conj, hinv]) ?_
  intro p hp e he hne
  show e ⬝ᵥ (A *ᵥ e) < p ⬝ᵥ (A *ᵥ p)
  rw [quad_of_diag A hdiag, quad_of_diag A hdiag]
  obtain ⟨v, w, hv, hw, rfl⟩ := hp
  have hsq : ∀ u, pureProd v w u ^ 2 = 1 := fun u => by
    simp only [pureProd, mul_pow, ext1_sq hv, ext1_sq hw, mul_one]
  simp only [hsq, mul_one]
  obtain ⟨hle, heq⟩ := diag_form_max hA hB A hpos (hS he)
  exact lt_of_le_of_ne hle fun h => hne (pure_of_sq_one (hS he) (heq h))

end GTAORnd.SelfRef.LR3.M11Cube
