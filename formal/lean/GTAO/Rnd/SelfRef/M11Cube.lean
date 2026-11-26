/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost: Theorem M11′ (round 10 note §15, as amended by the side session's hostile
review), assembled for hypercube and cross-polytope parts. Lean round 4 of the side session; written
in a private Lake project (library `GTAORnd`, same Lean and Mathlib pins) and moved here with only
this header, the module lines, the namespace and the last step of the assembled theorems (which call
`M11Prime.final_assembly` in place of a local copy) changed.
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

/-! ### Cross-polytope parts

The cross-polytope `{a : ∑ |a_i| ≤ 1}` in `ℝ^m` has vertices `±e_i` and facet functionals
`1 + s·a` for the sign vectors `s`. -/

/-- the A-Bloch vector of a tensor-coordinate vector -/
def avec (x : Idx mA mB → ℝ) : Fin mA → ℝ := fun i => x (some i, none)
/-- the B-Bloch vector -/
def bvec (x : Idx mA mB → ℝ) : Fin mB → ℝ := fun j => x (none, some j)
/-- the correlation matrix -/
def cmat (x : Idx mA mB → ℝ) (i : Fin mA) (j : Fin mB) : ℝ := x (some i, some j)

/-- the maximal tensor product of two cross-polytopes (normalized states): `x₀₀ = 1` and every
product of facet effects `(1 + s·a)(1 + t·b)`, `s, t` sign vectors, is nonnegative. -/
def maxSetX (mA mB : ℕ) : Set (Idx mA mB → ℝ) :=
  {x | x (none, none) = 1 ∧ ∀ s : Fin mA → ℝ, ∀ t : Fin mB → ℝ, IsSign s → IsSign t →
    0 ≤ 1 + ∑ i, s i * avec x i + ∑ j, t j * bvec x j + ∑ i, ∑ j, s i * t j * cmat x i j}

/-- the vertex `σ e_i` of the cross-polytope -/
def vert {m : ℕ} (i : Fin m) (σ : ℝ) : Fin m → ℝ := fun k => if k = i then σ else 0

/-- products of cross-polytope vertices -/
def pureSetX (mA mB : ℕ) : Set (Idx mA mB → ℝ) :=
  {x | ∃ (i : Fin mA) (j : Fin mB) (σ τ : ℝ), (σ = 1 ∨ σ = -1) ∧ (τ = 1 ∨ τ = -1) ∧
    x = pureProd (vert i σ) (vert j τ)}

lemma sum_vert {m : ℕ} (s : Fin m → ℝ) (i : Fin m) (σ : ℝ) :
    ∑ k, s k * vert i σ k = s i * σ := by
  simp [vert, mul_ite]

theorem pureProdX_mem_maxSetX {i : Fin mA} {j : Fin mB} {σ τ : ℝ} (hσ : σ = 1 ∨ σ = -1)
    (hτ : τ = 1 ∨ τ = -1) : pureProd (vert i σ) (vert j τ) ∈ maxSetX mA mB := by
  refine ⟨by simp [pureProd, ext1], fun s t hs ht => ?_⟩
  have ha : ∑ k, s k * avec (pureProd (vert i σ) (vert j τ)) k = s i * σ := by
    simpa [avec, pureProd, ext1] using sum_vert s i σ
  have hb : ∑ l, t l * bvec (pureProd (vert i σ) (vert j τ)) l = t j * τ := by
    simpa [bvec, pureProd, ext1] using sum_vert t j τ
  have hc : ∑ k, ∑ l, s k * t l * cmat (pureProd (vert i σ) (vert j τ)) k l
      = (s i * σ) * (t j * τ) := by
    simp only [cmat, pureProd, ext1]
    rw [← sum_vert s i σ, Finset.sum_mul]
    refine Finset.sum_congr rfl fun k _ => ?_
    rw [← sum_vert t j τ, Finset.mul_sum]
    refine Finset.sum_congr rfl fun l _ => ?_
    ring
  rw [ha, hb, hc]
  have h1 : 0 ≤ 1 + s i * σ := by
    rcases hs i with h | h <;> rcases hσ with h' | h' <;> rw [h, h'] <;> norm_num
  have h2 : 0 ≤ 1 + t j * τ := by
    rcases ht j with h | h <;> rcases hτ with h' | h' <;> rw [h, h'] <;> norm_num
  nlinarith [mul_nonneg h1 h2]

lemma isSign_neg {m : ℕ} {s : Fin m → ℝ} (hs : IsSign s) : IsSign (-s) := fun i => by
  rcases hs i with h | h <;> simp [h]

/-- the marginal and correlation bounds `abs(s·a) ≤ 1`, `abs(sᵀ C t) ≤ 1` on the maximal tensor
product of two cross-polytopes -/
theorem maxSetX_bounds {x : Idx mA mB → ℝ} (hx : x ∈ maxSetX mA mB) {s : Fin mA → ℝ}
    {t : Fin mB → ℝ} (hs : IsSign s) (ht : IsSign t) :
    (∑ i, s i * avec x i) ^ 2 ≤ 1 ∧ (∑ j, t j * bvec x j) ^ 2 ≤ 1 ∧
      (∑ i, ∑ j, s i * t j * cmat x i j) ^ 2 ≤ 1 := by
  obtain ⟨-, hc⟩ := hx
  have e1 := hc s t hs ht
  have e2 := hc (-s) (-t) (isSign_neg hs) (isSign_neg ht)
  have e3 := hc s (-t) hs (isSign_neg ht)
  have e4 := hc (-s) t (isSign_neg hs) ht
  simp only [Pi.neg_apply, neg_mul, mul_neg, neg_neg, Finset.sum_neg_distrib] at e2 e3 e4
  refine ⟨?_, ?_, ?_⟩ <;> nlinarith

/-- the sign vector of a Boolean vector -/
def sgn {m : ℕ} (b : Fin m → Bool) : Fin m → ℝ := fun i => if b i then 1 else -1

lemma isSign_sgn {m : ℕ} (b : Fin m → Bool) : IsSign (sgn b) := fun i => by
  unfold sgn; split_ifs <;> simp

lemma sum_sgn_mul {m : ℕ} (i k : Fin m) :
    ∑ b : Fin m → Bool, sgn b i * sgn b k = if i = k then (2 : ℝ) ^ m else 0 := by
  split_ifs with hik
  · subst hik
    have : ∀ b : Fin m → Bool, sgn b i * sgn b i = 1 := fun b => by unfold sgn; split_ifs <;> norm_num
    simp only [this, Finset.sum_const, Finset.card_univ, Fintype.card_fun, Fintype.card_bool,
      Fintype.card_fin, nsmul_eq_mul, mul_one]
    norm_num
  · let e : Equiv.Perm (Fin m → Bool) :=
      Function.Involutive.toPerm (fun b => Function.update b i (!b i)) (fun b => by
        funext l; by_cases hl : l = i
        · subst hl; simp
        · simp [Function.update_of_ne hl])
    have hflip : ∀ b, sgn (e b) i * sgn (e b) k = -(sgn b i * sgn b k) := fun b => by
      show sgn (Function.update b i (!b i)) i * sgn (Function.update b i (!b i)) k = _
      simp only [sgn, Function.update_self, Function.update_of_ne (Ne.symm hik)]
      cases b i <;> cases b k <;> norm_num
    have h := Fintype.sum_equiv e (fun b => sgn b i * sgn b k) (fun b => -(sgn b i * sgn b k))
      (fun b => by rw [hflip, neg_neg])
    rw [Finset.sum_neg_distrib] at h
    linarith

/-- averaging over the sign vectors: `∑_s (s·u)² = 2^m ‖u‖²` -/
theorem sum_sgn_sq {m : ℕ} (u : Fin m → ℝ) :
    ∑ b : Fin m → Bool, (∑ i, sgn b i * u i) ^ 2 = 2 ^ m * ∑ i, u i ^ 2 := by
  have : ∀ b : Fin m → Bool, (∑ i, sgn b i * u i) ^ 2 =
      ∑ i, ∑ k, (sgn b i * sgn b k) * (u i * u k) := fun b => by
    rw [sq, Finset.sum_mul_sum]
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun k _ => ?_
    ring
  simp only [this]
  rw [Finset.sum_comm]
  simp only [Finset.mul_sum]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [Finset.sum_comm]
  simp only [← Finset.sum_mul, sum_sgn_mul, ite_mul, zero_mul, Finset.sum_ite_eq, Finset.mem_univ,
    if_true]
  ring

/-- **Lemma 1 for cross-polytope parts**: on the maximal tensor product of two cross-polytopes,
`‖C‖²_F ≤ 1 = R_A² R_B²`, and `‖a‖² ≤ 1`, `‖b‖² ≤ 1`. -/
theorem maxSetX_frob {x : Idx mA mB → ℝ} (hx : x ∈ maxSetX mA mB) :
    ∑ i, ∑ j, cmat x i j ^ 2 ≤ 1 := by
  have key : ∑ bs : Fin mA → Bool, ∑ bt : Fin mB → Bool,
      (∑ i, ∑ j, sgn bs i * sgn bt j * cmat x i j) ^ 2 =
      2 ^ mA * 2 ^ mB * ∑ i, ∑ j, cmat x i j ^ 2 := by
    have h1 : ∀ bs bt, (∑ i, ∑ j, sgn bs i * sgn bt j * cmat x i j) =
        ∑ i, sgn bs i * (∑ j, sgn bt j * cmat x i j) := fun bs bt => by
      simp only [Finset.mul_sum]; refine Finset.sum_congr rfl fun i _ =>
        Finset.sum_congr rfl fun j _ => by ring
    simp only [h1]
    rw [Finset.sum_comm]
    simp only [sum_sgn_sq, ← Finset.mul_sum]
    rw [Finset.sum_comm]
    simp only [sum_sgn_sq, ← Finset.mul_sum]
    ring
  have hle : ∑ bs : Fin mA → Bool, ∑ bt : Fin mB → Bool,
      (∑ i, ∑ j, sgn bs i * sgn bt j * cmat x i j) ^ 2 ≤ 2 ^ mA * 2 ^ mB := by
    calc _ ≤ ∑ _bs : Fin mA → Bool, ∑ _bt : Fin mB → Bool, (1 : ℝ) :=
          Finset.sum_le_sum fun bs _ => Finset.sum_le_sum fun bt _ =>
            (maxSetX_bounds hx (isSign_sgn bs) (isSign_sgn bt)).2.2
      _ = 2 ^ mA * 2 ^ mB := by simp
  rw [key] at hle
  have hp : (0 : ℝ) < 2 ^ mA * 2 ^ mB := by positivity
  nlinarith

theorem sum_abs_le_of_bound {m : ℕ} (u : Fin m → ℝ)
    (h : ∀ s : Fin m → ℝ, IsSign s → (∑ i, s i * u i) ^ 2 ≤ 1) : ∑ i, |u i| ≤ 1 := by
  let s : Fin m → ℝ := fun i => if 0 ≤ u i then 1 else -1
  have hs : IsSign s := fun i => by simp only [s]; split_ifs <;> simp
  have he : ∑ i, s i * u i = ∑ i, |u i| := Finset.sum_congr rfl fun i _ => by
    simp only [s]; split_ifs with h0
    · rw [abs_of_nonneg h0, one_mul]
    · rw [abs_of_neg (lt_of_not_ge h0)]; ring
  have := h s hs
  rw [he] at this
  nlinarith [Finset.sum_nonneg fun i (_ : i ∈ Finset.univ) => abs_nonneg (u i)]

/-- `‖u‖² ≤ 1` when `∑ abs u_i ≤ 1`, with equality only at a vertex `±e_i` -/
theorem sq_le_of_l1 {m : ℕ} (u : Fin m → ℝ) (h : ∑ i, |u i| ≤ 1) :
    ∑ i, u i ^ 2 ≤ 1 ∧ (∑ i, u i ^ 2 = 1 → ∃ i σ, (σ = 1 ∨ σ = -1) ∧ u = vert i σ) := by
  have h1 : ∀ i, |u i| ≤ 1 := fun i =>
    le_trans (Finset.single_le_sum (fun k _ => abs_nonneg (u k)) (Finset.mem_univ i)) h
  have h2 : ∀ i, u i ^ 2 ≤ |u i| := fun i => by
    rw [← sq_abs]; nlinarith [abs_nonneg (u i), h1 i]
  have hle : ∑ i, u i ^ 2 ≤ 1 := le_trans (Finset.sum_le_sum fun i _ => h2 i) h
  refine ⟨hle, fun heq => ?_⟩
  have hz : ∑ i, (|u i| - u i ^ 2) ≤ 0 := by rw [Finset.sum_sub_distrib]; linarith
  have hz' := (Finset.sum_eq_zero_iff_of_nonneg (fun i _ => sub_nonneg.2 (h2 i))).1
    (le_antisymm hz (Finset.sum_nonneg fun i _ => sub_nonneg.2 (h2 i)))
  obtain ⟨i, hi⟩ : ∃ i, u i ≠ 0 := by
    by_contra hall; push Not at hall; simp [hall] at heq
  have hai : |u i| = u i ^ 2 := by linarith [hz' i (Finset.mem_univ _)]
  have hsq : u i ^ 2 = 1 := by
    have : |u i| * (|u i| - 1) = 0 := by rw [← sq_abs] at hai; nlinarith
    rcases mul_eq_zero.1 this with h0 | h0
    · exact absurd (abs_eq_zero.1 h0) hi
    · rw [← sq_abs]; nlinarith
  refine ⟨i, u i, sign_of_sq hsq, funext fun k => ?_⟩
  simp only [vert]
  split_ifs with hk
  · rw [hk]
  · have : u i ^ 2 + u k ^ 2 ≤ ∑ l, u l ^ 2 := by
      rw [← Finset.sum_pair (f := fun l => u l ^ 2) (Ne.symm hk)]
      exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ _)
        fun l _ _ => sq_nonneg _
    nlinarith [sq_nonneg (u k)]

/-- the unit-vector inequalities on the maximal tensor product of two cross-polytopes:
`0 ≤ 1 + σ a_i + τ b_j + στ C_ij` for `σ, τ = ±1` (average two sign vectors on each side) -/
theorem maxSetX_unit {x : Idx mA mB → ℝ} (hx : x ∈ maxSetX mA mB) (i : Fin mA) (j : Fin mB)
    {σ τ : ℝ} (hσ : σ = 1 ∨ σ = -1) (hτ : τ = 1 ∨ τ = -1) :
    0 ≤ 1 + σ * avec x i + τ * bvec x j + σ * τ * cmat x i j := by
  obtain ⟨-, hc⟩ := hx
  set s1 : Fin mA → ℝ := fun k => if k = i then σ else 1
  set s2 : Fin mA → ℝ := fun k => if k = i then σ else -1
  set t1 : Fin mB → ℝ := fun l => if l = j then τ else 1
  set t2 : Fin mB → ℝ := fun l => if l = j then τ else -1
  have hs1 : IsSign s1 := fun k => by simp only [s1]; split_ifs <;> simp [hσ]
  have hs2 : IsSign s2 := fun k => by simp only [s2]; split_ifs <;> simp [hσ]
  have ht1 : IsSign t1 := fun l => by simp only [t1]; split_ifs <;> simp [hτ]
  have ht2 : IsSign t2 := fun l => by simp only [t2]; split_ifs <;> simp [hτ]
  have hs : ∀ k, s1 k + s2 k = if k = i then 2 * σ else 0 := fun k => by
    simp only [s1, s2]; split_ifs <;> ring
  have ht : ∀ l, t1 l + t2 l = if l = j then 2 * τ else 0 := fun l => by
    simp only [t1, t2]; split_ifs <;> ring
  have hA : ∑ k, s1 k * avec x k + ∑ k, s2 k * avec x k = 2 * σ * avec x i := by
    rw [← Finset.sum_add_distrib]
    simp only [← add_mul, hs, ite_mul, zero_mul, Finset.sum_ite_eq', Finset.mem_univ, ite_true]
  have hB : ∑ l, t1 l * bvec x l + ∑ l, t2 l * bvec x l = 2 * τ * bvec x j := by
    rw [← Finset.sum_add_distrib]
    simp only [← add_mul, ht, ite_mul, zero_mul, Finset.sum_ite_eq', Finset.mem_univ, ite_true]
  have hC : (∑ k, ∑ l, s1 k * t1 l * cmat x k l) + (∑ k, ∑ l, s1 k * t2 l * cmat x k l) +
      (∑ k, ∑ l, s2 k * t1 l * cmat x k l) + (∑ k, ∑ l, s2 k * t2 l * cmat x k l) =
      4 * σ * τ * cmat x i j := by
    have e : ∀ k l, s1 k * t1 l * cmat x k l + s1 k * t2 l * cmat x k l +
        s2 k * t1 l * cmat x k l + s2 k * t2 l * cmat x k l =
        (s1 k + s2 k) * ((t1 l + t2 l) * cmat x k l) := fun k l => by ring
    simp only [← Finset.sum_add_distrib, e, hs, ht, ite_mul, zero_mul]
    simp [Finset.sum_ite_irrel, mul_ite, ite_mul, Finset.sum_ite_eq']
    ring
  have e1 := hc s1 t1 hs1 ht1
  have e2 := hc s1 t2 hs1 ht2
  have e3 := hc s2 t1 hs2 ht1
  have e4 := hc s2 t2 hs2 ht2
  nlinarith

lemma sum_pair_le {α : Type*} [Fintype α] [DecidableEq α] (u : α → ℝ) {i k : α} (hk : k ≠ i) :
    u i ^ 2 + u k ^ 2 ≤ ∑ l, u l ^ 2 := by
  rw [← Finset.sum_pair (f := fun l => u l ^ 2) (Ne.symm hk)]
  exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ _) fun l _ _ => sq_nonneg _

/-- **Equality case for cross-polytope parts**: a point of the maximal tensor product with
`‖a‖² = ‖b‖² = ‖C‖²_F = 1` is a product of cross-polytope vertices -/
theorem pure_of_eqX {x : Idx mA mB → ℝ} (hx : x ∈ maxSetX mA mB)
    (ha : ∑ i, avec x i ^ 2 = 1) (hb : ∑ j, bvec x j ^ 2 = 1)
    (hc : ∑ i, ∑ j, cmat x i j ^ 2 = 1) : x ∈ pureSetX mA mB := by
  have t0 : IsSign (sgn (fun _ : Fin mB => true)) := isSign_sgn _
  have s0 : IsSign (sgn (fun _ : Fin mA => true)) := isSign_sgn _
  obtain ⟨i, σ, hσ, hai⟩ := (sq_le_of_l1 (avec x) (sum_abs_le_of_bound (avec x)
    fun s hs => (maxSetX_bounds hx hs t0).1)).2 ha
  obtain ⟨j, τ, hτ, hbj⟩ := (sq_le_of_l1 (bvec x) (sum_abs_le_of_bound (bvec x)
    fun t ht => (maxSetX_bounds hx s0 ht).2.1)).2 hb
  have hnσ : -σ = 1 ∨ -σ = -1 := by rcases hσ with h | h <;> simp [h]
  have hnτ : -τ = 1 ∨ -τ = -1 := by rcases hτ with h | h <;> simp [h]
  have hu := maxSetX_unit hx i j hnσ hnτ
  have hai' : avec x i = σ := by rw [hai]; simp [vert]
  have hbj' : bvec x j = τ := by rw [hbj]; simp [vert]
  rw [hai', hbj'] at hu
  have hσ2 : σ ^ 2 = 1 := sq_one_of_sign hσ
  have hτ2 : τ ^ 2 = 1 := sq_one_of_sign hτ
  -- the full double sum, as a sum over pairs
  have hcp : ∑ p : Fin mA × Fin mB, cmat x p.1 p.2 ^ 2 = 1 := by
    rw [Fintype.sum_prod_type]; exact hc
  have hCij2 : cmat x i j ^ 2 ≤ 1 := by
    rw [← hcp]
    exact Finset.single_le_sum (f := fun p : Fin mA × Fin mB => cmat x p.1 p.2 ^ 2)
      (fun p _ => sq_nonneg _) (Finset.mem_univ (i, j))
  have hCij : cmat x i j = σ * τ := by
    have h1 : 1 ≤ σ * τ * cmat x i j := by nlinarith
    have h2 : (σ * τ * cmat x i j) ^ 2 ≤ 1 := by
      rw [mul_pow, mul_pow, hσ2, hτ2]; linarith
    have h3 : σ * τ * cmat x i j = 1 := by nlinarith
    calc cmat x i j = (σ ^ 2 * τ ^ 2) * cmat x i j := by rw [hσ2, hτ2]; ring
      _ = σ * τ * (σ * τ * cmat x i j) := by ring
      _ = σ * τ := by rw [h3, mul_one]
  have hrest : ∀ k l, (k, l) ≠ (i, j) → cmat x k l = 0 := by
    intro k l hkl
    have := sum_pair_le (fun p : Fin mA × Fin mB => cmat x p.1 p.2) hkl
    simp only at this
    rw [hcp, hCij, mul_pow, hσ2, hτ2] at this
    nlinarith [sq_nonneg (cmat x k l)]
  refine ⟨i, j, σ, τ, hσ, hτ, funext fun u => ?_⟩
  rcases u with ⟨_ | k, _ | l⟩
  · simp [pureProd, ext1, hx.1]
  · have := congrFun hbj l; simpa [pureProd, ext1, bvec] using this
  · have := congrFun hai k; simpa [pureProd, ext1, avec] using this
  · simp only [pureProd, ext1, vert]
    by_cases hk : k = i
    · by_cases hl : l = j
      · subst hk; subst hl; simpa [cmat] using hCij
      · rw [if_pos hk, if_neg hl, mul_zero]
        exact hrest k l (fun h => hl (Prod.mk.inj h).2)
    · rw [if_neg hk, zero_mul]
      exact hrest k l (fun h => hk (Prod.mk.inj h).1)

/-- the quadratic form of a diagonal matrix that is constant on the A, B and C blocks -/
theorem quad_blocks (A : Matrix (Idx mA mB) (Idx mA mB) ℝ) (α β γ : ℝ)
    (hα : ∀ i, A (some i, none) (some i, none) = α) (hβ : ∀ j, A (none, some j) (none, some j) = β)
    (hγ : ∀ i j, A (some i, some j) (some i, some j) = γ) (x : Idx mA mB → ℝ) :
    ∑ u, A u u * x u ^ 2 = A (none, none) (none, none) * x (none, none) ^ 2 +
      α * ∑ i, avec x i ^ 2 + β * ∑ j, bvec x j ^ 2 + γ * ∑ i, ∑ j, cmat x i j ^ 2 := by
  rw [Fintype.sum_prod_type, Fintype.sum_option]
  simp only [Fintype.sum_option, Finset.sum_add_distrib, hα, hβ, hγ, avec, bvec, cmat,
    Finset.mul_sum]
  ring

lemma pureX_sums {i : Fin mA} {j : Fin mB} {σ τ : ℝ} (hσ : σ = 1 ∨ σ = -1)
    (hτ : τ = 1 ∨ τ = -1) :
    ∑ k, avec (pureProd (vert i σ) (vert j τ)) k ^ 2 = 1 ∧
    ∑ l, bvec (pureProd (vert i σ) (vert j τ)) l ^ 2 = 1 ∧
    ∑ k, ∑ l, cmat (pureProd (vert i σ) (vert j τ)) k l ^ 2 = 1 := by
  have hσ2 := sq_one_of_sign hσ
  have hτ2 := sq_one_of_sign hτ
  refine ⟨?_, ?_, ?_⟩
  · simp [avec, pureProd, ext1, vert, ite_pow, hσ2]
  · simp [bvec, pureProd, ext1, vert, ite_pow, hτ2]
  · simp only [cmat, pureProd, ext1, mul_pow]
    simp [← Finset.mul_sum, ← Finset.sum_mul, vert, ite_pow, hσ2, hτ2]

/-- **No reversible map entangles, cross-polytope parts** (PROVED-IN-MODEL). As `m11_cube_into`,
for two cross-polytopes (`m_A, m_B ≥ 1`), with the local coordinate swaps as well as the sign flips
in the image of `Γ` (together they generate the hyperoctahedral group, the symmetry group of the
cross-polytope): every element of `Γ` that maps `S` into `S`, `pureSetX ⊆ S ⊆ maxSetX`, maps each
product state to a product state. The averaged form is diagonal (`flip_invariant_diag`) and constant
on the A, B and C blocks (`swap_invariant_blocks`), so `q = q₀₀ + α‖a‖² + β‖b‖² + γ‖C‖²_F`; on
`maxSetX` each norm is at most 1 (`sq_le_of_l1`, `maxSetX_frob`) and all three equal 1 only at
product states (`pure_of_eqX`). -/
theorem m11_cross_into {Γ : Type*} [Group Γ] [Fintype Γ] (hA : 0 < mA) (hB : 0 < mB)
    (ρ : Γ →* Matrix (Idx mA mB) (Idx mA mB) ℝ)
    (hr : ∀ i, ∃ g, ρ g = diagonal (rowSign i)) (hc : ∀ j, ∃ g, ρ g = diagonal (colSign j))
    (hrs : ∀ i i', ∃ g, ρ g = permMat (rowSwap i i'))
    (hcs : ∀ j j', ∃ g, ρ g = permMat (colSwap j j'))
    (S : Set (Idx mA mB → ℝ)) (hS : S ⊆ maxSetX mA mB) (hP : pureSetX mA mB ⊆ S)
    (g : Γ) (hg : ∀ x ∈ S, ρ g *ᵥ x ∈ S) :
    ∀ p ∈ pureSetX mA mB, ρ g *ᵥ p ∈ pureSetX mA mB := by
  set A := avgGram ρ with hAdef
  have hinv : ∀ g, (ρ g)ᵀ * A * ρ g = A := avgGram_invariant ρ
  have hdiag : ∀ u v, u ≠ v → A u v = 0 := flip_invariant_diag A
    (fun i => by obtain ⟨g, hg⟩ := hr i; rw [← hg]; exact hinv g)
    (fun j => by obtain ⟨g, hg⟩ := hc j; rw [← hg]; exact hinv g)
  obtain ⟨hbA, hbB, hbC⟩ := swap_invariant_blocks A
    (fun i i' => by obtain ⟨g, hg⟩ := hrs i i'; rw [← hg]; exact hinv g)
    (fun j j' => by obtain ⟨g, hg⟩ := hcs j j'; rw [← hg]; exact hinv g)
  have hpos : ∀ u, 0 < A u u := fun u => lt_of_lt_of_le one_pos (avgGram_diag_ge_one ρ u)
  set i0 : Fin mA := ⟨0, hA⟩
  set j0 : Fin mB := ⟨0, hB⟩
  have hq := quad_blocks A _ _ _ (fun i => hbA i i0) (fun j => hbB j j0)
    (fun i j => hbC i i0 j j0)
  set α := A (some i0, none) (some i0, none)
  set β := A (none, some j0) (none, some j0)
  set γ := A (some i0, some j0) (some i0, some j0)
  have hα : 0 < α := hpos _
  have hβ : 0 < β := hpos _
  have hγ : 0 < γ := hpos _
  intro p hp
  have hpS := hg p (hP hp)
  obtain ⟨i, j, σ, τ, hσ, hτ, rfl⟩ := hp
  set y := ρ g *ᵥ pureProd (vert i σ) (vert j τ)
  have hyS := hS hpS
  have heq : y ⬝ᵥ (A *ᵥ y) = pureProd (vert i σ) (vert j τ) ⬝ᵥ (A *ᵥ pureProd (vert i σ) (vert j τ)) := by
    rw [quad_conj, hinv]
  rw [quad_of_diag A hdiag, quad_of_diag A hdiag, hq, hq] at heq
  obtain ⟨p1, p2, p3⟩ := pureX_sums (i := i) (j := j) hσ hτ
  have h00 : pureProd (vert i σ) (vert j τ) (none, none) = 1 := by simp [pureProd, ext1]
  rw [p1, p2, p3, h00, hyS.1] at heq
  have t0 : IsSign (sgn (fun _ : Fin mB => true)) := isSign_sgn _
  have s0 : IsSign (sgn (fun _ : Fin mA => true)) := isSign_sgn _
  have ya := (sq_le_of_l1 (avec y) (sum_abs_le_of_bound (avec y)
    fun s hs => (maxSetX_bounds hyS hs t0).1)).1
  have yb := (sq_le_of_l1 (bvec y) (sum_abs_le_of_bound (bvec y)
    fun t ht => (maxSetX_bounds hyS s0 ht).2.1)).1
  have yc := maxSetX_frob hyS
  have ea : ∑ i, avec y i ^ 2 = 1 := by nlinarith
  have eb : ∑ j, bvec y j ^ 2 = 1 := by nlinarith
  have ec : ∑ i, ∑ j, cmat y i j ^ 2 = 1 := by nlinarith
  exact pure_of_eqX hyS ea eb ec

/-- **Theorem M11′, assembled for two cross-polytope parts** (PROVED-IN-MODEL). Setting as in
`m11_cross_into`; the intended instance is `Γ = Aut(S)` (finiteness of `Aut(S)` is not formalized:
`Γ` and `ρ` are hypotheses). Every element of `Γ` that maps `S` onto `S` maps the product states
onto the product states. The last step is `M11Prime.final_assembly` with `E := S`. -/
theorem m11_cross {Γ : Type*} [Group Γ] [Fintype Γ] (hA : 0 < mA) (hB : 0 < mB)
    (ρ : Γ →* Matrix (Idx mA mB) (Idx mA mB) ℝ)
    (hr : ∀ i, ∃ g, ρ g = diagonal (rowSign i)) (hc : ∀ j, ∃ g, ρ g = diagonal (colSign j))
    (hrs : ∀ i i', ∃ g, ρ g = permMat (rowSwap i i'))
    (hcs : ∀ j j', ∃ g, ρ g = permMat (colSwap j j'))
    (S : Set (Idx mA mB → ℝ)) (hS : S ⊆ maxSetX mA mB) (hP : pureSetX mA mB ⊆ S)
    (γ0 : Γ) (hT : (fun x => ρ γ0 *ᵥ x) '' S = S) :
    (fun x => ρ γ0 *ᵥ x) '' pureSetX mA mB = pureSetX mA mB := by
  set A := avgGram ρ with hAdef
  have hinv : ∀ g, (ρ g)ᵀ * A * ρ g = A := avgGram_invariant ρ
  have hdiag : ∀ u v, u ≠ v → A u v = 0 := flip_invariant_diag A
    (fun i => by obtain ⟨g, hg⟩ := hr i; rw [← hg]; exact hinv g)
    (fun j => by obtain ⟨g, hg⟩ := hc j; rw [← hg]; exact hinv g)
  obtain ⟨hbA, hbB, hbC⟩ := swap_invariant_blocks A
    (fun i i' => by obtain ⟨g, hg⟩ := hrs i i'; rw [← hg]; exact hinv g)
    (fun j j' => by obtain ⟨g, hg⟩ := hcs j j'; rw [← hg]; exact hinv g)
  have hpos : ∀ u, 0 < A u u := fun u => lt_of_lt_of_le one_pos (avgGram_diag_ge_one ρ u)
  set i0 : Fin mA := ⟨0, hA⟩
  set j0 : Fin mB := ⟨0, hB⟩
  have hq := quad_blocks A _ _ _ (fun i => hbA i i0) (fun j => hbB j j0)
    (fun i j => hbC i i0 j j0)
  set α := A (some i0, none) (some i0, none)
  set β := A (none, some j0) (none, some j0)
  set γ := A (some i0, some j0) (some i0, some j0)
  have hα : 0 < α := hpos _
  have hβ : 0 < β := hpos _
  have hγ : 0 < γ := hpos _
  refine M11Prime.final_assembly S (pureSetX mA mB) hP (fun x => x ⬝ᵥ (A *ᵥ x))
    (fun x => ρ γ0 *ᵥ x) hT (fun x => by rw [quad_conj, hinv]) ?_
  intro p hp e he hne
  show e ⬝ᵥ (A *ᵥ e) < p ⬝ᵥ (A *ᵥ p)
  rw [quad_of_diag A hdiag, quad_of_diag A hdiag, hq, hq]
  obtain ⟨i, j, σ, τ, hσ, hτ, rfl⟩ := hp
  obtain ⟨p1, p2, p3⟩ := pureX_sums (i := i) (j := j) hσ hτ
  have h00 : pureProd (vert i σ) (vert j τ) (none, none) = 1 := by simp [pureProd, ext1]
  have heS := hS he
  rw [p1, p2, p3, h00, heS.1]
  have t0 : IsSign (sgn (fun _ : Fin mB => true)) := isSign_sgn _
  have s0 : IsSign (sgn (fun _ : Fin mA => true)) := isSign_sgn _
  have ya := (sq_le_of_l1 (avec e) (sum_abs_le_of_bound (avec e)
    fun s hs => (maxSetX_bounds heS hs t0).1)).1
  have yb := (sq_le_of_l1 (bvec e) (sum_abs_le_of_bound (bvec e)
    fun t ht => (maxSetX_bounds heS s0 ht).2.1)).1
  have yc := maxSetX_frob heS
  by_contra hge
  push Not at hge
  have ea : ∑ i, avec e i ^ 2 = 1 := by nlinarith
  have eb : ∑ j, bvec e j ^ 2 = 1 := by nlinarith
  have ec : ∑ i, ∑ j, cmat e i j ^ 2 = 1 := by nlinarith
  exact hne (pure_of_eqX heS ea eb ec)

end GTAORnd.SelfRef.LR3.M11Cube
