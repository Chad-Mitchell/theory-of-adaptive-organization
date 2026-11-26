/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost: Theorem M11′ (round 10 note §15, as amended by the side session's hostile
review) for parts that are products of cross-polytopes (cubes, cross-polytopes, mixed and
block-product parts), under a minimal symmetry hypothesis. Lean round 5 of the side session; written
in a private Lake project (library `GTAORnd`, same Lean and Mathlib pins) and moved here with only
this header and the module lines changed.
-/
module

public import Mathlib
public import GTAO.Rnd.SelfRef.M11Cube

@[expose] public section

/-!
# Theorem M11′ for products of cross-polytopes, under minimal symmetry (Lean round 5)
-/

namespace GTAORnd.SelfRef.LR3.M11Blocks

open Matrix GTAORnd.SelfRef.LR3.M11Cube

variable {mA mB rA rB : ℕ}

/-! ### Part 1: the Schur step under a separating family of diagonal symmetries -/

/-- **Schur step, minimal diagonal form** (PROVED-IN-MODEL): if for every pair of distinct tensor
coordinates `u ≠ v` some diagonal matrix `diag d` with `d u * d v ≠ 1` leaves `M` invariant, then
`M` is diagonal. -/
theorem diag_of_separating (M : Matrix (Idx mA mB) (Idx mA mB) ℝ)
    (h : ∀ u v : Idx mA mB, u ≠ v → ∃ d : Idx mA mB → ℝ,
      (diagonal d)ᵀ * M * diagonal d = M ∧ d u * d v ≠ 1) :
    ∀ u v : Idx mA mB, u ≠ v → M u v = 0 := by
  intro u v huv
  obtain ⟨d, hd, hne⟩ := h u v huv
  have e := diag_conj_entry d M hd u v
  have : (d u * d v - 1) * M u v = 0 := by linear_combination e
  rcases mul_eq_zero.1 this with h0 | h0
  · exact absurd (by linarith) hne
  · exact h0

/-- the local sign flips separate every pair of distinct tensor coordinates -/
theorem flips_separate (u v : Idx mA mB) (huv : u ≠ v) :
    (∃ i, rowSign i u * rowSign i v = (-1 : ℝ)) ∨ (∃ j, colSign j u * colSign j v = (-1 : ℝ)) := by
  by_cases h1 : u.1 = v.1
  · have h2 : u.2 ≠ v.2 := fun h2 => huv (Prod.ext h1 h2)
    right
    rcases hu : u.2 with _ | j
    · rcases hv : v.2 with _ | j'
      · exact absurd (hu.trans hv.symm) h2
      · exact ⟨j', by simp [colSign, hu, hv]⟩
    · have : v.2 ≠ some j := fun e => h2 (hu.trans e.symm)
      exact ⟨j, by simp [colSign, hu, this]⟩
  · left
    rcases hu : u.1 with _ | i
    · rcases hv : v.1 with _ | i'
      · exact absurd (hu.trans hv.symm) h1
      · exact ⟨i', by simp [rowSign, hu, hv]⟩
    · have : v.1 ≠ some i := fun e => h1 (hu.trans e.symm)
      exact ⟨i, by simp [rowSign, hu, this]⟩

/-- the coordinate permutation of the composite induced by a permutation of A's coordinates -/
def liftA (π : Equiv.Perm (Fin mA)) : Equiv.Perm (Idx mA mB) :=
  Equiv.prodCongr (Equiv.optionCongr π) (Equiv.refl _)
/-- the coordinate permutation induced by a permutation of B's coordinates -/
def liftB (π : Equiv.Perm (Fin mB)) : Equiv.Perm (Idx mA mB) :=
  Equiv.prodCongr (Equiv.refl _) (Equiv.optionCongr π)

/-! ### Part 2: products of cross-polytopes (block parts)

A *block part* has coordinates `Fin m` grouped into blocks by a labelling `b : Fin m → Fin r`; its
state space is the product (`ℓ∞`-sum) of the cross-polytopes of the blocks,
`{a : ∑_{i ∈ block k} |a_i| ≤ 1 for every block k}`. Singleton blocks give the cube, one block the
cross-polytope; mixed labellings give e.g. octahedron × octahedron. Its facet functionals are
`1 + s·a` with `s` a *block sign vector* (`±1` on one block, `0` elsewhere); its vertices are the
*block vertices* (on each block, one coordinate `±1` and the rest `0`). -/

/-- `s` is a sign vector on block `k` and zero elsewhere -/
def IsBlockSign {m r : ℕ} (b : Fin m → Fin r) (k : Fin r) (s : Fin m → ℝ) : Prop :=
  ∀ i, (b i = k → s i = 1 ∨ s i = -1) ∧ (b i ≠ k → s i = 0)

/-- `v` is a vertex of the product of the block cross-polytopes -/
def IsBlockVert {m r : ℕ} (b : Fin m → Fin r) (v : Fin m → ℝ) : Prop :=
  ∀ i, ∃ i0 σ, b i0 = b i ∧ (σ = 1 ∨ σ = -1) ∧ ∀ i', b i' = b i → v i' = if i' = i0 then σ else 0

/-- the maximal tensor product of two block parts (normalized states) -/
def maxSetB (bA : Fin mA → Fin rA) (bB : Fin mB → Fin rB) : Set (Idx mA mB → ℝ) :=
  {x | x (none, none) = 1 ∧ ∀ k l (s : Fin mA → ℝ) (t : Fin mB → ℝ), IsBlockSign bA k s →
    IsBlockSign bB l t →
    0 ≤ 1 + ∑ i, s i * avec x i + ∑ j, t j * bvec x j + ∑ i, ∑ j, s i * t j * cmat x i j}

/-- the product states of two block parts -/
def pureSetB (bA : Fin mA → Fin rA) (bB : Fin mB → Fin rB) : Set (Idx mA mB → ℝ) :=
  {x | ∃ v w, IsBlockVert bA v ∧ IsBlockVert bB w ∧ x = pureProd v w}

/-- restriction of a vector to block `k` -/
def msk {m r : ℕ} (b : Fin m → Fin r) (k : Fin r) (u : Fin m → ℝ) : Fin m → ℝ :=
  fun i => if b i = k then u i else 0

section Block
variable {m r : ℕ} (b : Fin m → Fin r)

lemma isBlockSign_neg {k : Fin r} {s : Fin m → ℝ} (hs : IsBlockSign b k s) :
    IsBlockSign b k (-s) := fun i => by
  refine ⟨fun h => ?_, fun h => ?_⟩
  · rcases (hs i).1 h with e | e <;> simp [e]
  · simp [(hs i).2 h]

lemma isBlockSign_msk (k : Fin r) {s : Fin m → ℝ} (hs : IsSign s) : IsBlockSign b k (msk b k s) :=
  fun i => ⟨fun h => by simp only [msk, ite_eq_left h]; exact hs i, fun h => by simp [msk, h]⟩

lemma sum_msk (k : Fin r) (s u : Fin m → ℝ) :
    ∑ i, s i * msk b k u i = ∑ i, msk b k s i * u i :=
  Finset.sum_congr rfl fun i _ => by simp only [msk]; split_ifs <;> ring

/-- a block sign vector pairs with a block vertex to `-1, 0` or `1` -/
lemma blockSign_vert {k : Fin r} {s v : Fin m → ℝ} (hs : IsBlockSign b k s) (hv : IsBlockVert b v) :
    ∃ c : ℝ, (c = 1 ∨ c = -1 ∨ c = 0) ∧ ∑ i, s i * v i = c := by
  by_cases hk : ∃ i, b i = k
  · obtain ⟨i, rfl⟩ := hk
    obtain ⟨i0, σ, hi0, hσ, hv⟩ := hv i
    refine ⟨s i0 * σ, ?_, ?_⟩
    · rcases (hs i0).1 hi0 with h | h <;> rcases hσ with h' | h' <;> simp [h, h']
    · rw [Finset.sum_eq_single i0]
      · rw [hv i0 hi0, ite_eq_left rfl]
      · intro k _ hk
        by_cases hb : b k = b i
        · rw [hv k hb, ite_eq_right hk, mul_zero]
        · rw [(hs k).2 hb, zero_mul]
      · simp
  · refine ⟨0, Or.inr (Or.inr rfl), Finset.sum_eq_zero fun i _ => ?_⟩
    rw [(hs i).2 (fun h => hk ⟨i, h⟩), zero_mul]

/-- the mask of a block vertex on a nonempty block is a cross-polytope vertex -/
lemma msk_vert {v : Fin m → ℝ} (hv : IsBlockVert b v) (i : Fin m) :
    ∃ i0 σ, b i0 = b i ∧ (σ = 1 ∨ σ = -1) ∧ msk b (b i) v = vert i0 σ := by
  obtain ⟨i0, σ, hi0, hσ, hv⟩ := hv i
  refine ⟨i0, σ, hi0, hσ, funext fun k => ?_⟩
  simp only [msk, vert]
  split_ifs with h1 h2 h2
  · rw [hv k h1, ite_eq_left h2]
  · rw [hv k h1, ite_eq_right h2]
  · exact absurd (h2 ▸ hi0) h1
  · rfl

end Block

lemma sum_sq_vert {m : ℕ} (i : Fin m) {σ : ℝ} (hσ : σ = 1 ∨ σ = -1) :
    ∑ k, vert i σ k ^ 2 = 1 := by
  simp [vert, ite_pow, sq_one_of_sign hσ]

/-- the product states lie in the maximal tensor product (so the hypotheses below are consistent) -/
theorem pure_mem_maxSetB (bA : Fin mA → Fin rA) (bB : Fin mB → Fin rB) :
    pureSetB bA bB ⊆ maxSetB bA bB := by
  rintro _ ⟨v, w, hv, hw, rfl⟩
  refine ⟨by simp [pureProd, ext1], fun k l s t hs ht => ?_⟩
  obtain ⟨c, hc, hsv⟩ := blockSign_vert bA hs hv
  obtain ⟨d, hd, htw⟩ := blockSign_vert bB ht hw
  have ha : ∑ i, s i * avec (pureProd v w) i = c := by
    simpa [avec, pureProd, ext1] using hsv
  have hb : ∑ j, t j * bvec (pureProd v w) j = d := by
    simpa [bvec, pureProd, ext1] using htw
  have hcm : ∑ i, ∑ j, s i * t j * cmat (pureProd v w) i j = c * d := by
    rw [← hsv, ← htw, Finset.sum_mul_sum]
    refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
    simp only [cmat, pureProd, ext1]; ring
  rw [ha, hb, hcm]
  have h1 : 0 ≤ 1 + c := by rcases hc with h | h | h <;> rw [h] <;> norm_num
  have h2 : 0 ≤ 1 + d := by rcases hd with h | h | h <;> rw [h] <;> norm_num
  nlinarith [mul_nonneg h1 h2]


/-! ### Part 3: the bounds on the maximal tensor product of two block parts -/

section Bounds
variable {bA : Fin mA → Fin rA} {bB : Fin mB → Fin rB}

theorem maxSetB_bounds {x : Idx mA mB → ℝ} (hx : x ∈ maxSetB bA bB) {k l} {s : Fin mA → ℝ}
    {t : Fin mB → ℝ} (hs : IsBlockSign bA k s) (ht : IsBlockSign bB l t) :
    (∑ i, s i * avec x i) ^ 2 ≤ 1 ∧ (∑ j, t j * bvec x j) ^ 2 ≤ 1 ∧
      (∑ i, ∑ j, s i * t j * cmat x i j) ^ 2 ≤ 1 := by
  obtain ⟨-, hc⟩ := hx
  have e1 := hc k l s t hs ht
  have e2 := hc k l (-s) (-t) (isBlockSign_neg bA hs) (isBlockSign_neg bB ht)
  have e3 := hc k l s (-t) hs (isBlockSign_neg bB ht)
  have e4 := hc k l (-s) t (isBlockSign_neg bA hs) ht
  simp only [Pi.neg_apply, neg_mul, mul_neg, neg_neg, Finset.sum_neg_distrib] at e2 e3 e4
  refine ⟨?_, ?_, ?_⟩ <;> nlinarith

/-- a block sign vector exists on every block -/
lemma exists_blockSign {m r : ℕ} (b : Fin m → Fin r) (k : Fin r) : ∃ s, IsBlockSign b k s :=
  ⟨_, isBlockSign_msk b k (isSign_sgn fun _ => true)⟩

/-- the A-marginal of each block lies in the block's cross-polytope: `‖a|_k‖² ≤ 1`, with equality
only at a vertex -/
theorem maxSetB_blockA (hrB : 0 < rB) {x : Idx mA mB → ℝ} (hx : x ∈ maxSetB bA bB) (k : Fin rA) :
    ∑ i, msk bA k (avec x) i ^ 2 ≤ 1 ∧ (∑ i, msk bA k (avec x) i ^ 2 = 1 →
      ∃ i σ, (σ = 1 ∨ σ = -1) ∧ msk bA k (avec x) = vert i σ) := by
  obtain ⟨t, ht⟩ := exists_blockSign bB ⟨0, hrB⟩
  exact sq_le_of_l1 _ (sum_abs_le_of_bound _ fun s hs => by
    rw [sum_msk]; exact (maxSetB_bounds hx (isBlockSign_msk bA k hs) ht).1)

theorem maxSetB_blockB (hrA : 0 < rA) {x : Idx mA mB → ℝ} (hx : x ∈ maxSetB bA bB) (l : Fin rB) :
    ∑ j, msk bB l (bvec x) j ^ 2 ≤ 1 ∧ (∑ j, msk bB l (bvec x) j ^ 2 = 1 →
      ∃ j τ, (τ = 1 ∨ τ = -1) ∧ msk bB l (bvec x) = vert j τ) := by
  obtain ⟨s, hs⟩ := exists_blockSign bA ⟨0, hrA⟩
  exact sq_le_of_l1 _ (sum_abs_le_of_bound _ fun t ht => by
    rw [sum_msk]; exact (maxSetB_bounds hx hs (isBlockSign_msk bB l ht)).2.1)

/-- restriction of a matrix to the block pair `(k, l)` -/
def mskC (bA : Fin mA → Fin rA) (bB : Fin mB → Fin rB) (k : Fin rA) (l : Fin rB)
    (M : Fin mA → Fin mB → ℝ) : Fin mA → Fin mB → ℝ :=
  fun i j => if bA i = k ∧ bB j = l then M i j else 0

/-- averaging over pairs of sign vectors: `∑_{s,t} (sᵀ M t)² = 2^{m_A} 2^{m_B} ‖M‖²_F` -/
theorem sum_sgn_sq2 (M : Fin mA → Fin mB → ℝ) :
    ∑ bs : Fin mA → Bool, ∑ bt : Fin mB → Bool, (∑ i, ∑ j, sgn bs i * sgn bt j * M i j) ^ 2 =
      2 ^ mA * 2 ^ mB * ∑ i, ∑ j, M i j ^ 2 := by
  have h1 : ∀ bs bt, (∑ i, ∑ j, sgn bs i * sgn bt j * M i j) =
      ∑ i, sgn bs i * (∑ j, sgn bt j * M i j) := fun bs bt => by
    simp only [Finset.mul_sum]; refine Finset.sum_congr rfl fun i _ =>
      Finset.sum_congr rfl fun j _ => by ring
  simp only [h1]
  rw [Finset.sum_comm]
  simp only [sum_sgn_sq, ← Finset.mul_sum]
  rw [Finset.sum_comm]
  simp only [sum_sgn_sq, ← Finset.mul_sum]
  ring

/-- the correlation block `(k, l)` has Frobenius norm at most 1 -/
theorem maxSetB_blockC {x : Idx mA mB → ℝ} (hx : x ∈ maxSetB bA bB) (k : Fin rA) (l : Fin rB) :
    ∑ i, ∑ j, mskC bA bB k l (cmat x) i j ^ 2 ≤ 1 := by
  have hm : ∀ bs bt, ∑ i, ∑ j, sgn bs i * sgn bt j * mskC bA bB k l (cmat x) i j =
      ∑ i, ∑ j, msk bA k (sgn bs) i * msk bB l (sgn bt) j * cmat x i j := fun bs bt =>
    Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => by
      simp only [mskC, msk]; split_ifs <;> simp_all
  have hle : ∑ bs : Fin mA → Bool, ∑ bt : Fin mB → Bool,
      (∑ i, ∑ j, sgn bs i * sgn bt j * mskC bA bB k l (cmat x) i j) ^ 2 ≤ 2 ^ mA * 2 ^ mB := by
    calc _ ≤ ∑ _bs : Fin mA → Bool, ∑ _bt : Fin mB → Bool, (1 : ℝ) :=
          Finset.sum_le_sum fun bs _ => Finset.sum_le_sum fun bt _ => by
            rw [hm]; exact (maxSetB_bounds hx (isBlockSign_msk bA k (isSign_sgn bs))
              (isBlockSign_msk bB l (isSign_sgn bt))).2.2
      _ = 2 ^ mA * 2 ^ mB := by simp
  rw [sum_sgn_sq2] at hle
  have hp : (0 : ℝ) < 2 ^ mA * 2 ^ mB := by positivity
  nlinarith

/-- the unit inequalities `0 ≤ 1 + σ a_i + τ b_j + στ C_ij` on the maximal tensor product of two
block parts -/
theorem maxSetB_unit {x : Idx mA mB → ℝ} (hx : x ∈ maxSetB bA bB) (i : Fin mA) (j : Fin mB)
    {σ τ : ℝ} (hσ : σ = 1 ∨ σ = -1) (hτ : τ = 1 ∨ τ = -1) :
    0 ≤ 1 + σ * avec x i + τ * bvec x j + σ * τ * cmat x i j := by
  obtain ⟨-, hc⟩ := hx
  set s1 : Fin mA → ℝ := fun k => if k = i then σ else if bA k = bA i then 1 else 0
  set s2 : Fin mA → ℝ := fun k => if k = i then σ else if bA k = bA i then -1 else 0
  set t1 : Fin mB → ℝ := fun l => if l = j then τ else if bB l = bB j then 1 else 0
  set t2 : Fin mB → ℝ := fun l => if l = j then τ else if bB l = bB j then -1 else 0
  have hs1 : IsBlockSign bA (bA i) s1 := fun k => ⟨fun h => by simp only [s1]; split_ifs <;> simp [hσ],
    fun h => by simp only [s1]; split_ifs with h1 <;> simp_all⟩
  have hs2 : IsBlockSign bA (bA i) s2 := fun k => ⟨fun h => by simp only [s2]; split_ifs <;> simp [hσ],
    fun h => by simp only [s2]; split_ifs with h1 <;> simp_all⟩
  have ht1 : IsBlockSign bB (bB j) t1 := fun l => ⟨fun h => by simp only [t1]; split_ifs <;> simp [hτ],
    fun h => by simp only [t1]; split_ifs with h1 <;> simp_all⟩
  have ht2 : IsBlockSign bB (bB j) t2 := fun l => ⟨fun h => by simp only [t2]; split_ifs <;> simp [hτ],
    fun h => by simp only [t2]; split_ifs with h1 <;> simp_all⟩
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
    simp [Finset.sum_ite_irrel, mul_ite, Finset.sum_ite_eq']
    ring
  have e1 := hc _ _ s1 t1 hs1 ht1
  have e2 := hc _ _ s1 t2 hs1 ht2
  have e3 := hc _ _ s2 t1 hs2 ht1
  have e4 := hc _ _ s2 t2 hs2 ht2
  nlinarith

end Bounds


/-! ### Part 4: the equality case -/

section Eq
variable {bA : Fin mA → Fin rA} {bB : Fin mB → Fin rB}

/-- a vector supported on block `k` that is a cross-polytope vertex has its vertex in block `k` -/
lemma vert_in_block {m r : ℕ} (b : Fin m → Fin r) (k : Fin r) (u : Fin m → ℝ) {i0 : Fin m} {σ : ℝ}
    (hσ : σ = 1 ∨ σ = -1) (h : msk b k u = vert i0 σ) : b i0 = k := by
  by_contra hne
  have := congrFun h i0
  simp only [msk, vert, ite_true] at this
  rw [ite_eq_right hne] at this
  rcases hσ with e | e <;> rw [e] at this <;> norm_num at this

/-- **Equality case for block parts** (PROVED-IN-MODEL): a point of the maximal tensor product of
two block parts at which every block marginal and every correlation block has norm 1 is a product
of block vertices. -/
theorem pure_of_eqB (hrA : 0 < rA) (hrB : 0 < rB) {x : Idx mA mB → ℝ} (hx : x ∈ maxSetB bA bB)
    (ha : ∀ i, ∑ k, msk bA (bA i) (avec x) k ^ 2 = 1)
    (hb : ∀ j, ∑ l, msk bB (bB j) (bvec x) l ^ 2 = 1)
    (hc : ∀ i j, ∑ k, ∑ l, mskC bA bB (bA i) (bB j) (cmat x) k l ^ 2 = 1) :
    x ∈ pureSetB bA bB := by
  have va : ∀ i, ∃ i0 σ, (σ = 1 ∨ σ = -1) ∧ bA i0 = bA i ∧ msk bA (bA i) (avec x) = vert i0 σ :=
    fun i => by
      obtain ⟨i0, σ, hσ, h⟩ := (maxSetB_blockA hrB hx (bA i)).2 (ha i)
      exact ⟨i0, σ, hσ, vert_in_block bA _ _ hσ h, h⟩
  have vb : ∀ j, ∃ j0 τ, (τ = 1 ∨ τ = -1) ∧ bB j0 = bB j ∧ msk bB (bB j) (bvec x) = vert j0 τ :=
    fun j => by
      obtain ⟨j0, τ, hτ, h⟩ := (maxSetB_blockB hrA hx (bB j)).2 (hb j)
      exact ⟨j0, τ, hτ, vert_in_block bB _ _ hτ h, h⟩
  -- on a block, `avec x` agrees with its mask
  have ea : ∀ i i', bA i' = bA i → avec x i' = msk bA (bA i) (avec x) i' := fun i i' h => by
    simp [msk, h]
  have eb : ∀ j j', bB j' = bB j → bvec x j' = msk bB (bB j) (bvec x) j' := fun j j' h => by
    simp [msk, h]
  have hvA : IsBlockVert bA (avec x) := fun i => by
    obtain ⟨i0, σ, hσ, hi0, h⟩ := va i
    exact ⟨i0, σ, hi0, hσ, fun i' hi' => by rw [ea i i' hi', h]; rfl⟩
  have hvB : IsBlockVert bB (bvec x) := fun j => by
    obtain ⟨j0, τ, hτ, hj0, h⟩ := vb j
    exact ⟨j0, τ, hj0, hτ, fun j' hj' => by rw [eb j j' hj', h]; rfl⟩
  refine ⟨avec x, bvec x, hvA, hvB, funext fun u => ?_⟩
  rcases u with ⟨_ | i, _ | j⟩
  · simp [pureProd, ext1, hx.1]
  · simp [pureProd, ext1, bvec]
  · simp [pureProd, ext1, avec]
  · obtain ⟨i0, σ, hσ, hi0, hA⟩ := va i
    obtain ⟨j0, τ, hτ, hj0, hB⟩ := vb j
    have hσ2 : σ ^ 2 = 1 := sq_one_of_sign hσ
    have hτ2 : τ ^ 2 = 1 := sq_one_of_sign hτ
    have ai0 : avec x i0 = σ := by rw [ea i i0 hi0, hA]; simp [vert]
    have bj0 : bvec x j0 = τ := by rw [eb j j0 hj0, hB]; simp [vert]
    set F : Fin mA × Fin mB → ℝ := fun p => mskC bA bB (bA i) (bB j) (cmat x) p.1 p.2
    have hF : ∑ p, F p ^ 2 = 1 := by rw [Fintype.sum_prod_type]; exact hc i j
    have Fi0 : F (i0, j0) = cmat x i0 j0 := by simp [F, mskC, hi0, hj0]
    have hC2 : cmat x i0 j0 ^ 2 ≤ 1 := by
      rw [← Fi0, ← hF]
      exact Finset.single_le_sum (f := fun p => F p ^ 2) (fun p _ => sq_nonneg _)
        (Finset.mem_univ (i0, j0))
    have hu := maxSetB_unit hx i0 j0 (σ := -σ) (τ := -τ)
      (by rcases hσ with h | h <;> simp [h]) (by rcases hτ with h | h <;> simp [h])
    rw [ai0, bj0] at hu
    have hCij : cmat x i0 j0 = σ * τ := by
      have h1 : 1 ≤ σ * τ * cmat x i0 j0 := by nlinarith
      have h2 : (σ * τ * cmat x i0 j0) ^ 2 ≤ 1 := by
        rw [mul_pow, mul_pow, hσ2, hτ2]; linarith
      have h3 : σ * τ * cmat x i0 j0 = 1 := by nlinarith
      calc cmat x i0 j0 = (σ ^ 2 * τ ^ 2) * cmat x i0 j0 := by rw [hσ2, hτ2]; ring
        _ = σ * τ * (σ * τ * cmat x i0 j0) := by ring
        _ = σ * τ := by rw [h3, mul_one]
    have hrest : ∀ p, p ≠ (i0, j0) → F p = 0 := by
      intro p hp
      have := sum_pair_le F hp
      rw [hF, Fi0, hCij, mul_pow, hσ2, hτ2] at this
      nlinarith [sq_nonneg (F p)]
    have avi : avec x i = vert i0 σ i := by rw [ea i i rfl, hA]
    have bvj : bvec x j = vert j0 τ j := by rw [eb j j rfl, hB]
    show cmat x i j = ext1 (avec x) (some i) * ext1 (bvec x) (some j)
    simp only [ext1, avi, bvj, vert]
    by_cases h1 : i = i0
    · by_cases h2 : j = j0
      · subst h1; subst h2; simp [hCij]
      · rw [ite_eq_right h2, mul_zero]
        have := hrest (i, j) (fun h => h2 (Prod.mk.inj h).2)
        simpa [F, mskC] using this
    · rw [ite_eq_right h1, zero_mul]
      have := hrest (i, j) (fun h => h1 (Prod.mk.inj h).1)
      simpa [F, mskC] using this

end Eq


/-! ### Part 5: the block-weighted quadratic form and the assembled theorem -/

lemma sum_fiber {m r : ℕ} (b : Fin m → Fin r) (f : Fin r → ℝ) (u : Fin m → ℝ) :
    ∑ i, f (b i) * u i ^ 2 = ∑ k, f k * ∑ i, msk b k u i ^ 2 := by
  simp only [msk, ite_pow, Finset.mul_sum, mul_ite]
  rw [Finset.sum_comm]
  refine Finset.sum_congr rfl fun i _ => ?_
  simp [Finset.sum_ite_eq]

lemma sum_fiber2 (bA : Fin mA → Fin rA) (bB : Fin mB → Fin rB) (f : Fin rA → Fin rB → ℝ)
    (M : Fin mA → Fin mB → ℝ) :
    ∑ i, ∑ j, f (bA i) (bB j) * M i j ^ 2 =
      ∑ k, ∑ l, f k l * ∑ i, ∑ j, mskC bA bB k l M i j ^ 2 := by
  set F : Fin rA → Fin rB → Fin mA → Fin mB → ℝ := fun k l i j =>
    if bA i = k then (if bB j = l then f k l * M i j ^ 2 else 0) else 0
  have hF : ∀ k l, f k l * ∑ i, ∑ j, mskC bA bB k l M i j ^ 2 = ∑ i, ∑ j, F k l i j :=
    fun k l => by
      simp only [Finset.mul_sum, F, mskC]
      refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
      split_ifs <;> simp_all
  simp only [hF]
  calc ∑ i, ∑ j, f (bA i) (bB j) * M i j ^ 2 = ∑ i, ∑ j, ∑ k, ∑ l, F k l i j := by
        refine Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun j _ => ?_
        simp [F, Finset.sum_ite_eq]
    _ = ∑ i, ∑ k, ∑ j, ∑ l, F k l i j := Finset.sum_congr rfl fun i _ => Finset.sum_comm
    _ = ∑ i, ∑ k, ∑ l, ∑ j, F k l i j :=
        Finset.sum_congr rfl fun i _ => Finset.sum_congr rfl fun k _ => Finset.sum_comm
    _ = ∑ k, ∑ i, ∑ l, ∑ j, F k l i j := Finset.sum_comm
    _ = ∑ k, ∑ l, ∑ i, ∑ j, F k l i j := Finset.sum_congr rfl fun k _ => Finset.sum_comm

lemma weighted_le {ι : Type*} [Fintype ι] (w f g : ι → ℝ) (hw : ∀ k, 0 < w k)
    (hfg : ∀ k, f k ≤ g k) :
    0 ≤ ∑ k, w k * (g k - f k) ∧ (∑ k, w k * (g k - f k) ≤ 0 → ∀ k, f k = g k) := by
  have hnn : ∀ k, 0 ≤ w k * (g k - f k) := fun k => mul_nonneg (hw k).le (sub_nonneg.2 (hfg k))
  refine ⟨Finset.sum_nonneg fun k _ => hnn k, fun h k => ?_⟩
  have := (Finset.sum_eq_zero_iff_of_nonneg (fun k _ => hnn k)).1
    (le_antisymm h (Finset.sum_nonneg fun k _ => hnn k)) k (Finset.mem_univ _)
  rcases mul_eq_zero.1 this with h0 | h0
  · exact absurd h0 (hw k).ne'
  · linarith

section Assembly
variable {bA : Fin mA → Fin rA} {bB : Fin mB → Fin rB}

/-- block norms of a vector -/
def NA (bA : Fin mA → Fin rA) (k : Fin rA) (x : Idx mA mB → ℝ) : ℝ :=
  ∑ i, msk bA k (avec x) i ^ 2
def NB (bB : Fin mB → Fin rB) (l : Fin rB) (x : Idx mA mB → ℝ) : ℝ :=
  ∑ j, msk bB l (bvec x) j ^ 2
def NC (bA : Fin mA → Fin rA) (bB : Fin mB → Fin rB) (k : Fin rA) (l : Fin rB)
    (x : Idx mA mB → ℝ) : ℝ :=
  ∑ i, ∑ j, mskC bA bB k l (cmat x) i j ^ 2

/-- a diagonal form whose diagonal is constant on the blocks -/
theorem quad_blockw (A : Matrix (Idx mA mB) (Idx mA mB) ℝ) (α : Fin rA → ℝ) (β : Fin rB → ℝ)
    (γ : Fin rA → Fin rB → ℝ)
    (hα : ∀ i, A (some i, none) (some i, none) = α (bA i))
    (hβ : ∀ j, A (none, some j) (none, some j) = β (bB j))
    (hγ : ∀ i j, A (some i, some j) (some i, some j) = γ (bA i) (bB j)) (x : Idx mA mB → ℝ) :
    ∑ u, A u u * x u ^ 2 = A (none, none) (none, none) * x (none, none) ^ 2 +
      ∑ k, α k * NA bA k x + ∑ l, β l * NB bB l x + ∑ k, ∑ l, γ k l * NC bA bB k l x := by
  have e1 := sum_fiber bA α (avec x)
  have e2 := sum_fiber bB β (bvec x)
  have e3 := sum_fiber2 bA bB γ (cmat x)
  simp only [NA, NB, NC, ← e1, ← e2, ← e3]
  rw [Fintype.sum_prod_type, Fintype.sum_option]
  simp only [Fintype.sum_option, Finset.sum_add_distrib, hα, hβ, hγ, avec, bvec, cmat]
  ring

lemma mskC_pure (k : Fin rA) (l : Fin rB) (v : Fin mA → ℝ) (w : Fin mB → ℝ) (i : Fin mA)
    (j : Fin mB) : mskC bA bB k l (cmat (pureProd v w)) i j = msk bA k v i * msk bB l w j := by
  simp only [mskC, msk, cmat, pureProd, ext1]
  split_ifs <;> simp_all

lemma NA_pure {v : Fin mA → ℝ} {w : Fin mB → ℝ} (hv : IsBlockVert bA v) (i : Fin mA) :
    NA bA (bA i) (pureProd v w) = 1 := by
  obtain ⟨i0, σ, -, hσ, h⟩ := msk_vert bA hv i
  have : msk bA (bA i) (avec (pureProd v w)) = msk bA (bA i) v := by
    funext k; simp [msk, avec, pureProd, ext1]
  rw [NA, this, h, sum_sq_vert i0 hσ]

lemma NB_pure {v : Fin mA → ℝ} {w : Fin mB → ℝ} (hw : IsBlockVert bB w) (j : Fin mB) :
    NB bB (bB j) (pureProd v w) = 1 := by
  obtain ⟨j0, τ, -, hτ, h⟩ := msk_vert bB hw j
  have : msk bB (bB j) (bvec (pureProd v w)) = msk bB (bB j) w := by
    funext k; simp [msk, bvec, pureProd, ext1]
  rw [NB, this, h, sum_sq_vert j0 hτ]

lemma NC_pure {v : Fin mA → ℝ} {w : Fin mB → ℝ} (hv : IsBlockVert bA v) (hw : IsBlockVert bB w)
    (i : Fin mA) (j : Fin mB) : NC bA bB (bA i) (bB j) (pureProd v w) = 1 := by
  obtain ⟨i0, σ, -, hσ, h⟩ := msk_vert bA hv i
  obtain ⟨j0, τ, -, hτ, h'⟩ := msk_vert bB hw j
  simp only [NC, mskC_pure, h, h', mul_pow]
  rw [← Finset.sum_mul_sum, sum_sq_vert i0 hσ, sum_sq_vert j0 hτ, one_mul]

/-- per block, the norms of a point of the maximal tensor product are at most those of a product
state -/
lemma block_le (hrA : 0 < rA) (hrB : 0 < rB) {v : Fin mA → ℝ} {w : Fin mB → ℝ}
    (hv : IsBlockVert bA v) (hw : IsBlockVert bB w) {e : Idx mA mB → ℝ} (he : e ∈ maxSetB bA bB) :
    (∀ k, NA bA k e ≤ NA bA k (pureProd v w)) ∧ (∀ l, NB bB l e ≤ NB bB l (pureProd v w)) ∧
      (∀ p : Fin rA × Fin rB, NC bA bB p.1 p.2 e ≤ NC bA bB p.1 p.2 (pureProd v w)) := by
  refine ⟨fun k => ?_, fun l => ?_, fun ⟨k, l⟩ => ?_⟩
  · by_cases hk : ∃ i, bA i = k
    · obtain ⟨i, rfl⟩ := hk
      rw [NA_pure hv]; exact (maxSetB_blockA hrB he _).1
    · push Not at hk; simp [NA, msk, hk]
  · by_cases hl : ∃ j, bB j = l
    · obtain ⟨j, rfl⟩ := hl
      rw [NB_pure hw]; exact (maxSetB_blockB hrA he _).1
    · push Not at hl; simp [NB, msk, hl]
  · by_cases hk : ∃ i, bA i = k
    · by_cases hl : ∃ j, bB j = l
      · obtain ⟨i, rfl⟩ := hk
        obtain ⟨j, rfl⟩ := hl
        rw [NC_pure hv hw]; exact maxSetB_blockC he _ _
      · push Not at hl; simp [NC, mskC, hl]
    · push Not at hk; simp [NC, mskC, hk]

/-- **No reversible map entangles, block parts, minimal symmetry** (PROVED-IN-MODEL).

Parts: products of cross-polytopes (`bA`, `bB` group the coordinates into blocks; singleton blocks
give a cube, a single block a cross-polytope). Composite: any `S` with `pureSetB ⊆ S ⊆ maxSetB`.
`Γ` is any finite group acting linearly (`ρ`) whose image contains

* (`hsep`) for every pair of distinct tensor coordinates `u ≠ v`, a diagonal matrix `diag d` with
  `d u * d v ≠ 1` (the local coordinate sign flips provide these, `flips_separate`; nothing else
  about signs is used);
* (`htrA`, `htrB`) for any two coordinates `i, i'` of the same block, the permutation matrix of
  some coordinate permutation of that part sending `i` to `i'` (transitivity on each block; for
  cubes this is vacuous, so only the sign hypothesis is used).

Then every element of `Γ` mapping `S` onto `S` maps the product states onto the product states.
The averaged form is diagonal (`diag_of_separating`) and constant on each block (transitivity), so
`q = q₀₀ + ∑_k α_k ‖a|_k‖² + ∑_l β_l ‖b|_l‖² + ∑_{k,l} γ_{kl} ‖C|_{kl}‖²_F` with positive weights
that may differ from block to block; each norm is at most 1 on `maxSetB` and all equal 1 only at
product states (`pure_of_eqB`). The last step is `M11Prime.final_assembly` with `E := S`. -/
theorem m11_blocks {Γ : Type*} [Group Γ] [Fintype Γ] (hrA : 0 < rA) (hrB : 0 < rB)
    (bA : Fin mA → Fin rA) (bB : Fin mB → Fin rB)
    (ρ : Γ →* Matrix (Idx mA mB) (Idx mA mB) ℝ)
    (hsep : ∀ u v : Idx mA mB, u ≠ v → ∃ g d, ρ g = diagonal d ∧ d u * d v ≠ 1)
    (htrA : ∀ i i', bA i = bA i' → ∃ π : Equiv.Perm (Fin mA), π i = i' ∧
      ∃ g, ρ g = permMat (liftA (mB := mB) π))
    (htrB : ∀ j j', bB j = bB j' → ∃ π : Equiv.Perm (Fin mB), π j = j' ∧
      ∃ g, ρ g = permMat (liftB (mA := mA) π))
    (S : Set (Idx mA mB → ℝ)) (hS : S ⊆ maxSetB bA bB) (hP : pureSetB bA bB ⊆ S)
    (γ0 : Γ) (hT : (fun x => ρ γ0 *ᵥ x) '' S = S) :
    (fun x => ρ γ0 *ᵥ x) '' pureSetB bA bB = pureSetB bA bB := by
  set A := avgGram ρ with hAdef
  have hinv : ∀ g, (ρ g)ᵀ * A * ρ g = A := avgGram_invariant ρ
  have hdiag : ∀ u v, u ≠ v → A u v = 0 := diag_of_separating A fun u v huv => by
    obtain ⟨g, d, hg, hd⟩ := hsep u v huv
    exact ⟨d, hg ▸ hinv g, hd⟩
  have hge : ∀ u, 1 ≤ A u u := avgGram_diag_ge_one ρ
  have cA : ∀ i i' (y : Option (Fin mB)), bA i = bA i' →
      A (some i, y) (some i, y) = A (some i', y) (some i', y) := by
    intro i i' y h
    obtain ⟨π, hπ, g, hg⟩ := htrA i i' h
    have := perm_conj_entry (liftA π) A (hg ▸ hinv g) (some i, y) (some i, y)
    simpa [liftA, hπ] using this.symm
  have cB : ∀ (y : Option (Fin mA)) j j', bB j = bB j' →
      A (y, some j) (y, some j) = A (y, some j') (y, some j') := by
    intro y j j' h
    obtain ⟨π, hπ, g, hg⟩ := htrB j j' h
    have := perm_conj_entry (liftB π) A (hg ▸ hinv g) (y, some j) (y, some j)
    simpa [liftB, hπ] using this.symm
  classical
  let α : Fin rA → ℝ := fun k =>
    if h : ∃ i, bA i = k then A (some h.choose, none) (some h.choose, none) else 1
  let β : Fin rB → ℝ := fun l =>
    if h : ∃ j, bB j = l then A (none, some h.choose) (none, some h.choose) else 1
  let γ : Fin rA → Fin rB → ℝ := fun k l =>
    if h : (∃ i, bA i = k) ∧ (∃ j, bB j = l) then
      A (some h.1.choose, some h.2.choose) (some h.1.choose, some h.2.choose) else 1
  have hα : ∀ i, A (some i, none) (some i, none) = α (bA i) := fun i => by
    have h : ∃ i', bA i' = bA i := ⟨i, rfl⟩
    simp only [α, dite_eq_left h]
    exact cA _ _ _ h.choose_spec.symm
  have hβ : ∀ j, A (none, some j) (none, some j) = β (bB j) := fun j => by
    have h : ∃ j', bB j' = bB j := ⟨j, rfl⟩
    simp only [β, dite_eq_left h]
    exact cB _ _ _ h.choose_spec.symm
  have hγ : ∀ i j, A (some i, some j) (some i, some j) = γ (bA i) (bB j) := fun i j => by
    have h : (∃ i', bA i' = bA i) ∧ (∃ j', bB j' = bB j) := ⟨⟨i, rfl⟩, ⟨j, rfl⟩⟩
    simp only [γ, dite_eq_left h]
    exact (cA _ _ _ h.1.choose_spec.symm).trans (cB _ _ _ h.2.choose_spec.symm)
  have pα : ∀ k, 0 < α k := fun k => by
    simp only [α]; split_ifs
    · exact lt_of_lt_of_le one_pos (hge _)
    · exact one_pos
  have pβ : ∀ l, 0 < β l := fun l => by
    simp only [β]; split_ifs
    · exact lt_of_lt_of_le one_pos (hge _)
    · exact one_pos
  have pγ : ∀ p : Fin rA × Fin rB, 0 < γ p.1 p.2 := fun p => by
    simp only [γ]; split_ifs
    · exact lt_of_lt_of_le one_pos (hge _)
    · exact one_pos
  have hq := quad_blockw A α β γ hα hβ hγ
  refine M11Prime.final_assembly S (pureSetB bA bB) hP (fun x => x ⬝ᵥ (A *ᵥ x))
    (fun x => ρ γ0 *ᵥ x) hT (fun x => by rw [quad_conj, hinv]) ?_
  intro p hp e he hne
  show e ⬝ᵥ (A *ᵥ e) < p ⬝ᵥ (A *ᵥ p)
  rw [quad_of_diag A hdiag, quad_of_diag A hdiag, hq, hq]
  obtain ⟨v, w, hv, hw, rfl⟩ := hp
  have heS := hS he
  have h00 : pureProd v w (none, none) = 1 := by simp [pureProd, ext1]
  rw [h00, heS.1]
  obtain ⟨l1, l2, l3⟩ := block_le hrA hrB hv hw heS
  obtain ⟨g1, g1e⟩ := weighted_le α _ _ pα l1
  obtain ⟨g2, g2e⟩ := weighted_le β _ _ pβ l2
  obtain ⟨g3, g3e⟩ := weighted_le (fun p : Fin rA × Fin rB => γ p.1 p.2) _ _ pγ l3
  rw [Fintype.sum_prod_type] at g3 g3e
  simp only [mul_sub, Finset.sum_sub_distrib] at g1 g1e g2 g2e g3 g3e
  by_contra hlt
  push Not at hlt
  have z1 := g1e (by linarith)
  have z2 := g2e (by linarith)
  have z3 := g3e (by linarith)
  apply hne
  exact pure_of_eqB hrA hrB heS (fun i => (z1 (bA i)).trans (NA_pure hv i))
    (fun j => (z2 (bB j)).trans (NB_pure hw j)) (fun i j => (z3 (bA i, bB j)).trans (NC_pure hv hw i j))

end Assembly


/-! ### Part 6: the product states span; M11′ for polytope composites with `Γ = Aut(S)` -/

section Span
variable {m r : ℕ} (b : Fin m → Fin r)

/-- every block part has a vertex -/
lemma exists_blockVert : ∃ v, IsBlockVert b v := by
  classical
  let rep : Fin m → Fin m := fun i => (Finset.univ.filter (fun k => b k = b i)).min' ⟨i, by simp⟩
  have rep_mem : ∀ i, b (rep i) = b i := fun i => by
    have := Finset.min'_mem (Finset.univ.filter (fun k => b k = b i)) ⟨i, by simp⟩
    simpa using this
  have rep_eq : ∀ i i', b i' = b i → rep i' = rep i := fun i i' h => by
    simp only [rep, h]
  refine ⟨fun k => if k = rep k then 1 else 0, fun i => ⟨rep i, 1, rep_mem i, Or.inl rfl,
    fun i' hi' => ?_⟩⟩
  simp only [rep_eq i i' hi']

/-- a block vertex with the block of `i` moved to `σ e_i` -/
lemma blockVert_set {v0 : Fin m → ℝ} (h0 : IsBlockVert b v0) (i : Fin m) {σ : ℝ}
    (hσ : σ = 1 ∨ σ = -1) :
    IsBlockVert b (fun k => if b k = b i then (if k = i then σ else 0) else v0 k) := by
  intro i1
  by_cases h1 : b i1 = b i
  · refine ⟨i, σ, h1.symm, hσ, fun i' hi' => ?_⟩
    simp only [hi'.trans h1, ite_true]
  · obtain ⟨i0, σ0, hi0, hσ0, hv⟩ := h0 i1
    refine ⟨i0, σ0, hi0, hσ0, fun i' hi' => ?_⟩
    have : b i' ≠ b i := fun e => h1 (hi'.symm.trans e)
    simp only [this, ite_false]
    exact hv i' hi'

/-- a linear functional (with constant term) vanishing on all block vertices is zero -/
lemma blockVert_lin (h : Option (Fin m) → ℝ)
    (H : ∀ v, IsBlockVert b v → ∑ o, h o * ext1 v o = 0) : h = 0 := by
  obtain ⟨v0, h0⟩ := exists_blockVert b
  have hs : ∀ i, h (some i) = 0 := fun i => by
    have e1 := H _ (blockVert_set b h0 i (Or.inl rfl))
    have e2 := H _ (blockVert_set b h0 i (Or.inr rfl))
    rw [Fintype.sum_option] at e1 e2
    simp only [ext1] at e1 e2
    have hd : ∑ k, h (some k) * (if b k = b i then (if k = i then (1 : ℝ) else 0) else v0 k) -
        ∑ k, h (some k) * (if b k = b i then (if k = i then (-1 : ℝ) else 0) else v0 k) =
        2 * h (some i) := by
      rw [← Finset.sum_sub_distrib, Finset.sum_eq_single i]
      · simp; ring
      · intro k _ hk
        split_ifs <;> simp_all
      · simp
    linarith
  funext o
  rcases o with _ | i
  · have e := H v0 h0
    rw [Fintype.sum_option] at e
    simp only [ext1, hs, zero_mul, Finset.sum_const_zero, add_zero, mul_one] at e
    exact e
  · exact hs i

end Span

/-- **The products of block vertices span the tensor coordinates** -/
theorem pureSetB_span (bA : Fin mA → Fin rA) (bB : Fin mB → Fin rB) :
    Submodule.span ℝ (pureSetB bA bB) = ⊤ := by
  apply span_eq_top_of_functional
  intro c hc
  have h1 : ∀ v w, IsBlockVert bA v → IsBlockVert bB w →
      ∑ o, (∑ o', c (o, o') * ext1 w o') * ext1 v o = 0 := fun v w hv hw => by
    have := hc _ ⟨v, w, hv, hw, rfl⟩
    rw [Fintype.sum_prod_type] at this
    rw [← this]
    refine Finset.sum_congr rfl fun o _ => ?_
    rw [Finset.sum_mul]
    refine Finset.sum_congr rfl fun o' _ => ?_
    simp only [pureProd]; ring
  have h2 : ∀ w, IsBlockVert bB w → ∀ o, ∑ o', c (o, o') * ext1 w o' = 0 := fun w hw o => by
    have := blockVert_lin bA (fun o => ∑ o', c (o, o') * ext1 w o') (fun v hv => h1 v w hv hw)
    exact congrFun this o
  funext u
  have := blockVert_lin bB (fun o' => c (u.1, o')) (fun w hw => h2 w hw u.1)
  exact congrFun this u.2

/-- a `±1` diagonal matrix as an invertible matrix -/
def diagUnit (d : Idx mA mB → ℝ) (hd : ∀ u, d u = 1 ∨ d u = -1) :
    (Matrix (Idx mA mB) (Idx mA mB) ℝ)ˣ :=
  ⟨diagonal d, diagonal d, diag_sign_sq hd, diag_sign_sq hd⟩

/-- **Theorem M11′ for polytope composites of block parts, minimal symmetry** (PROVED-IN-MODEL; no
hypothesis on the symmetry group, which is built as `Aut(S)`; the local-symmetry premise of M11′
stays, as the invariance hypotheses below). Parts: products of cross-polytopes (`bA`, `bB`, at least one block label each).
`S` is the convex hull of a finite set with `pureSetB ⊆ S ⊆ maxSetB`. Symmetry assumed of `S`:
(`hsep`) for every pair of distinct tensor coordinates a `±1` diagonal map of `S` onto itself that
separates them, and (`htrA`, `htrB`) for any two coordinates of the same block a coordinate
permutation of that part, mapping `S` onto itself, that sends one to the other. Then every
reversible map of `S` maps the product states onto the product states. -/
theorem m11_blocks_polytope (hrA : 0 < rA) (hrB : 0 < rB) (bA : Fin mA → Fin rA)
    (bB : Fin mB → Fin rB) (V : Set (Idx mA mB → ℝ)) (hV : V.Finite)
    (hS : convexHull ℝ V ⊆ maxSetB bA bB) (hP : pureSetB bA bB ⊆ convexHull ℝ V)
    (hsep : ∀ u v : Idx mA mB, u ≠ v → ∃ d : Idx mA mB → ℝ, (∀ w, d w = 1 ∨ d w = -1) ∧
      d u * d v = -1 ∧ (fun x => diagonal d *ᵥ x) '' convexHull ℝ V = convexHull ℝ V)
    (htrA : ∀ i i', bA i = bA i' → ∃ π : Equiv.Perm (Fin mA), π i = i' ∧
      (fun x => permMat (liftA (mB := mB) π) *ᵥ x) '' convexHull ℝ V = convexHull ℝ V)
    (htrB : ∀ j j', bB j = bB j' → ∃ π : Equiv.Perm (Fin mB), π j = j' ∧
      (fun x => permMat (liftB (mA := mA) π) *ᵥ x) '' convexHull ℝ V = convexHull ℝ V)
    (T : (Matrix (Idx mA mB) (Idx mA mB) ℝ)ˣ)
    (hT : (fun x => (T : Matrix (Idx mA mB) (Idx mA mB) ℝ) *ᵥ x) '' convexHull ℝ V = convexHull ℝ V) :
    (fun x => (T : Matrix (Idx mA mB) (Idx mA mB) ℝ) *ᵥ x) '' pureSetB bA bB = pureSetB bA bB := by
  set S := convexHull ℝ V
  have hspan : Submodule.span ℝ S = ⊤ :=
    eq_top_iff.2 (pureSetB_span bA bB ▸ Submodule.span_mono hP)
  have : Finite (autSet S) := autSet_finite V hV hspan
  let : Fintype (autSet S) := Fintype.ofFinite _
  let ρ : autSet S →* Matrix (Idx mA mB) (Idx mA mB) ℝ :=
    (Units.coeHom (Matrix (Idx mA mB) (Idx mA mB) ℝ)).comp (autSet S).subtype
  refine m11_blocks hrA hrB bA bB ρ (fun u v huv => ?_) (fun i i' h => ?_) (fun j j' h => ?_)
    S hS hP ⟨T, hT⟩ hT
  · obtain ⟨d, hd, hdd, hdS⟩ := hsep u v huv
    exact ⟨⟨diagUnit d hd, hdS⟩, d, rfl, by rw [hdd]; norm_num⟩
  · obtain ⟨π, hπ, hπS⟩ := htrA i i' h
    exact ⟨π, hπ, ⟨permUnit _, hπS⟩, rfl⟩
  · obtain ⟨π, hπ, hπS⟩ := htrB j j' h
    exact ⟨π, hπ, ⟨permUnit _, hπS⟩, rfl⟩

/-- **The same, with the local sign flips** (PROVED-IN-MODEL): `hsep` holds as soon as `S` is
invariant under the local coordinate sign flips of both parts (`flips_separate`). -/
theorem m11_blocks_polytope_flips (hrA : 0 < rA) (hrB : 0 < rB) (bA : Fin mA → Fin rA)
    (bB : Fin mB → Fin rB) (V : Set (Idx mA mB → ℝ)) (hV : V.Finite)
    (hS : convexHull ℝ V ⊆ maxSetB bA bB) (hP : pureSetB bA bB ⊆ convexHull ℝ V)
    (hfA : ∀ i, (fun x => diagonal (rowSign i) *ᵥ x) '' convexHull ℝ V = convexHull ℝ V)
    (hfB : ∀ j, (fun x => diagonal (colSign j) *ᵥ x) '' convexHull ℝ V = convexHull ℝ V)
    (htrA : ∀ i i', bA i = bA i' → ∃ π : Equiv.Perm (Fin mA), π i = i' ∧
      (fun x => permMat (liftA (mB := mB) π) *ᵥ x) '' convexHull ℝ V = convexHull ℝ V)
    (htrB : ∀ j j', bB j = bB j' → ∃ π : Equiv.Perm (Fin mB), π j = j' ∧
      (fun x => permMat (liftB (mA := mA) π) *ᵥ x) '' convexHull ℝ V = convexHull ℝ V)
    (T : (Matrix (Idx mA mB) (Idx mA mB) ℝ)ˣ)
    (hT : (fun x => (T : Matrix (Idx mA mB) (Idx mA mB) ℝ) *ᵥ x) '' convexHull ℝ V = convexHull ℝ V) :
    (fun x => (T : Matrix (Idx mA mB) (Idx mA mB) ℝ) *ᵥ x) '' pureSetB bA bB = pureSetB bA bB := by
  refine m11_blocks_polytope hrA hrB bA bB V hV hS hP (fun u v huv => ?_) htrA htrB T hT
  rcases flips_separate u v huv with ⟨i, hi⟩ | ⟨j, hj⟩
  · exact ⟨rowSign i, fun w => by unfold rowSign; split_ifs <;> simp, hi, hfA i⟩
  · exact ⟨colSign j, fun w => by unfold colSign; split_ifs <;> simp, hj, hfB j⟩


/-! ### Part 7: the instances: cube × cube, cross × cross, and the mixed cube × cross-polytope

Singleton blocks (`id`) give the cube, one block (`fun _ => 0`) the cross-polytope. The maximal
tensor products and product states of round 4 are recovered exactly (`maxSet_eq_blocks`,
`maxSetX_eq_blocks`, ...), and the mixed composite of a cube and a cross-polytope is the labelling
`(id, fun _ => 0)`. -/

section Instances

lemma blockSign_id {m : ℕ} {k : Fin m} {s : Fin m → ℝ} (hs : IsBlockSign (id : Fin m → Fin m) k s) :
    (s k = 1 ∨ s k = -1) ∧ s = vert k (s k) := by
  refine ⟨(hs k).1 rfl, funext fun i => ?_⟩
  simp only [vert]
  split_ifs with h
  · rw [h]
  · exact (hs i).2 h

lemma isBlockSign_id_vert {m : ℕ} (k : Fin m) {σ : ℝ} (hσ : σ = 1 ∨ σ = -1) :
    IsBlockSign (id : Fin m → Fin m) k (vert k σ) := fun i =>
  ⟨fun h => by simp only [id] at h; simp [vert, h, hσ], fun h => by simp only [id] at h; simp [vert, h]⟩

lemma blockSign_one_iff {m : ℕ} (l : Fin 1) (t : Fin m → ℝ) :
    IsBlockSign (fun _ : Fin m => (0 : Fin 1)) l t ↔ IsSign t := by
  have hl : l = 0 := Subsingleton.elim _ _
  subst hl
  exact ⟨fun h i => (h i).1 rfl, fun h i => ⟨fun _ => h i, fun h' => absurd rfl h'⟩⟩

lemma blockVert_id_iff {m : ℕ} (v : Fin m → ℝ) : IsBlockVert (id : Fin m → Fin m) v ↔ IsSign v := by
  constructor
  · intro h i
    obtain ⟨i0, σ, hi0, hσ, hv⟩ := h i
    simp only [id] at hi0
    subst hi0
    rw [hv i0 rfl, ite_eq_left rfl]; exact hσ
  · intro h i
    exact ⟨i, v i, rfl, h i, fun i' hi' => by simp only [id] at hi'; subst hi'; simp⟩

lemma blockVert_one_iff {m : ℕ} (hm : 0 < m) (w : Fin m → ℝ) :
    IsBlockVert (fun _ : Fin m => (0 : Fin 1)) w ↔ ∃ j τ, (τ = 1 ∨ τ = -1) ∧ w = vert j τ := by
  constructor
  · intro h
    obtain ⟨j0, τ, -, hτ, hw⟩ := h ⟨0, hm⟩
    exact ⟨j0, τ, hτ, funext fun j => hw j rfl⟩
  · rintro ⟨j, τ, hτ, rfl⟩ i
    exact ⟨j, τ, rfl, hτ, fun i' _ => rfl⟩

lemma sum_vert_left {m : ℕ} (k : Fin m) (σ : ℝ) (u : Fin m → ℝ) :
    ∑ i, vert k σ i * u i = σ * u k := by
  simp [vert]

lemma sum2_vert_left {m n : ℕ} (k : Fin m) (σ : ℝ) (t : Fin n → ℝ) (M : Fin m → Fin n → ℝ) :
    ∑ i, ∑ j, vert k σ i * t j * M i j = ∑ j, σ * t j * M k j := by
  simp [vert, ite_mul]

/-- the maximal tensor product of a cube (A) and a cross-polytope (B), written out: `x₀₀ = 1` and
`0 ≤ (1 + s a_i)(1 + t·b)` read linearly, for each coordinate `i` of A, `s = ±1`, and each sign
vector `t` of B -/
def maxSetCX (mA mB : ℕ) : Set (Idx mA mB → ℝ) :=
  {x | x (none, none) = 1 ∧ ∀ (i : Fin mA) (s : ℝ) (t : Fin mB → ℝ), (s = 1 ∨ s = -1) → IsSign t →
    0 ≤ 1 + s * avec x i + ∑ j, t j * bvec x j + ∑ j, s * t j * cmat x i j}

/-- products of a cube vertex and a cross-polytope vertex -/
def pureSetCX (mA mB : ℕ) : Set (Idx mA mB → ℝ) :=
  {x | ∃ (v : Fin mA → ℝ) (j : Fin mB) (τ : ℝ), IsSign v ∧ (τ = 1 ∨ τ = -1) ∧ x = pureProd v (vert j τ)}

theorem maxSetCX_eq_blocks :
    maxSetB (id : Fin mA → Fin mA) (fun _ : Fin mB => (0 : Fin 1)) = maxSetCX mA mB := by
  ext x
  constructor
  · rintro ⟨h0, h⟩
    refine ⟨h0, fun i s t hs ht => ?_⟩
    have := h i 0 (vert i s) t (isBlockSign_id_vert i hs) ((blockSign_one_iff 0 t).2 ht)
    rwa [sum_vert_left, sum2_vert_left] at this
  · rintro ⟨h0, h⟩
    refine ⟨h0, fun k l s t hs ht => ?_⟩
    obtain ⟨hk, hsv⟩ := blockSign_id hs
    have := h k (s k) t hk ((blockSign_one_iff l t).1 ht)
    rw [hsv, sum_vert_left, sum2_vert_left]; exact this

theorem pureSetCX_eq_blocks (hB : 0 < mB) :
    pureSetB (id : Fin mA → Fin mA) (fun _ : Fin mB => (0 : Fin 1)) = pureSetCX mA mB := by
  ext x
  constructor
  · rintro ⟨v, w, hv, hw, rfl⟩
    obtain ⟨j, τ, hτ, rfl⟩ := (blockVert_one_iff hB w).1 hw
    exact ⟨v, j, τ, (blockVert_id_iff v).1 hv, hτ, rfl⟩
  · rintro ⟨v, j, τ, hv, hτ, rfl⟩
    exact ⟨v, vert j τ, (blockVert_id_iff v).2 hv, (blockVert_one_iff hB _).2 ⟨j, τ, hτ, rfl⟩, rfl⟩

/-- round 4's cross-polytope composite is the one-block case -/
theorem maxSetX_eq_blocks :
    maxSetB (fun _ : Fin mA => (0 : Fin 1)) (fun _ : Fin mB => (0 : Fin 1)) = maxSetX mA mB := by
  ext x
  constructor
  · rintro ⟨h0, h⟩
    exact ⟨h0, fun s t hs ht => h 0 0 s t ((blockSign_one_iff 0 s).2 hs) ((blockSign_one_iff 0 t).2 ht)⟩
  · rintro ⟨h0, h⟩
    exact ⟨h0, fun k l s t hs ht => h s t ((blockSign_one_iff k s).1 hs) ((blockSign_one_iff l t).1 ht)⟩

theorem pureSetX_eq_blocks (hA : 0 < mA) (hB : 0 < mB) :
    pureSetB (fun _ : Fin mA => (0 : Fin 1)) (fun _ : Fin mB => (0 : Fin 1)) = pureSetX mA mB := by
  ext x
  constructor
  · rintro ⟨v, w, hv, hw, rfl⟩
    obtain ⟨i, σ, hσ, rfl⟩ := (blockVert_one_iff hA v).1 hv
    obtain ⟨j, τ, hτ, rfl⟩ := (blockVert_one_iff hB w).1 hw
    exact ⟨i, j, σ, τ, hσ, hτ, rfl⟩
  · rintro ⟨i, j, σ, τ, hσ, hτ, rfl⟩
    exact ⟨_, _, (blockVert_one_iff hA _).2 ⟨i, σ, hσ, rfl⟩,
      (blockVert_one_iff hB _).2 ⟨j, τ, hτ, rfl⟩, rfl⟩

/-- round 4's cube composite is the singleton-block case -/
theorem maxSet_eq_blocks :
    maxSetB (id : Fin mA → Fin mA) (id : Fin mB → Fin mB) = maxSet mA mB := by
  ext x
  constructor
  · rintro ⟨h0, h⟩
    refine ⟨h0, fun i j s t hs ht => ?_⟩
    have := h i j (vert i s) (vert j t) (isBlockSign_id_vert i hs) (isBlockSign_id_vert j ht)
    rw [sum_vert_left, sum_vert_left, sum2_vert_left] at this
    simpa [vert, avec, bvec, cmat] using this
  · rintro ⟨h0, h⟩
    refine ⟨h0, fun k l s t hs ht => ?_⟩
    obtain ⟨hk, hsv⟩ := blockSign_id hs
    obtain ⟨hl, htv⟩ := blockSign_id ht
    rw [hsv, htv, sum_vert_left, sum_vert_left, sum2_vert_left]
    have := h k l (s k) (t l) hk hl
    simpa [vert, avec, bvec, cmat] using this

theorem pureSet_eq_blocks :
    pureSetB (id : Fin mA → Fin mA) (id : Fin mB → Fin mB) = pureSet mA mB := by
  ext x
  simp only [pureSetB, pureSet, blockVert_id_iff]

lemma liftA_one : liftA (mB := mB) (1 : Equiv.Perm (Fin mA)) = 1 := by
  ext u <;> simp [liftA]

/-- **Theorem M11′ for a polytope composite of a hypercube and a cross-polytope** (PROVED-IN-MODEL;
no hypothesis on the symmetry group, which is built as `Aut(S)`; the local-symmetry premise stays as the
invariance hypotheses). `S` is the convex hull of a finite set with `pureSetCX ⊆ S ⊆ maxSetCX`
(`m_A, m_B ≥ 1`), invariant under the local coordinate sign flips of both parts and the coordinate
swaps of the cross-polytope B (no coordinate swaps of the cube A are needed). Every reversible map
of `S` maps the product states onto the product states. -/
theorem m11_cube_cross_polytope (hA : 0 < mA) (hB : 0 < mB) (V : Set (Idx mA mB → ℝ))
    (hV : V.Finite) (hS : convexHull ℝ V ⊆ maxSetCX mA mB) (hP : pureSetCX mA mB ⊆ convexHull ℝ V)
    (hfA : ∀ i, (fun x => diagonal (rowSign i) *ᵥ x) '' convexHull ℝ V = convexHull ℝ V)
    (hfB : ∀ j, (fun x => diagonal (colSign j) *ᵥ x) '' convexHull ℝ V = convexHull ℝ V)
    (hsB : ∀ j j', (fun x => permMat (colSwap j j') *ᵥ x) '' convexHull ℝ V = convexHull ℝ V)
    (T : (Matrix (Idx mA mB) (Idx mA mB) ℝ)ˣ)
    (hT : (fun x => (T : Matrix (Idx mA mB) (Idx mA mB) ℝ) *ᵥ x) '' convexHull ℝ V = convexHull ℝ V) :
    (fun x => (T : Matrix (Idx mA mB) (Idx mA mB) ℝ) *ᵥ x) '' pureSetCX mA mB = pureSetCX mA mB := by
  rw [← maxSetCX_eq_blocks] at hS
  rw [← pureSetCX_eq_blocks hB] at hP ⊢
  refine m11_blocks_polytope_flips hA one_pos id (fun _ => 0) V hV hS hP hfA hfB
    (fun i i' h => ⟨1, h, ?_⟩) (fun j j' _ => ⟨Equiv.swap j j', Equiv.swap_apply_left j j', hsB j j'⟩)
    T hT
  rw [liftA_one, permMat_one]
  simp

end Instances


/-! ### Part 8: the hypotheses can be met -/

/-- the maximal tensor product of two block parts is convex -/
theorem maxSetB_convex (bA : Fin mA → Fin rA) (bB : Fin mB → Fin rB) :
    Convex ℝ (maxSetB bA bB) := by
  intro x hx y hy a b ha hb hab
  refine ⟨by simp [hx.1, hy.1, hab], fun k l s t hs ht => ?_⟩
  have e1 := hx.2 k l s t hs ht
  have e2 := hy.2 k l s t hs ht
  have hlin : 1 + ∑ i, s i * avec (a • x + b • y) i + ∑ j, t j * bvec (a • x + b • y) j +
      ∑ i, ∑ j, s i * t j * cmat (a • x + b • y) i j =
      a * (1 + ∑ i, s i * avec x i + ∑ j, t j * bvec x j + ∑ i, ∑ j, s i * t j * cmat x i j) +
      b * (1 + ∑ i, s i * avec y i + ∑ j, t j * bvec y j + ∑ i, ∑ j, s i * t j * cmat y i j) := by
    simp only [avec, bvec, cmat, Pi.add_apply, Pi.smul_apply, smul_eq_mul, mul_add,
      Finset.sum_add_distrib, Finset.mul_sum]
    have h1 : ∀ i, s i * (a * x (some i, none)) = a * (s i * x (some i, none)) := fun i => by ring
    have h2 : ∀ i, s i * (b * y (some i, none)) = b * (s i * y (some i, none)) := fun i => by ring
    have h3 : ∀ j, t j * (a * x (none, some j)) = a * (t j * x (none, some j)) := fun j => by ring
    have h4 : ∀ j, t j * (b * y (none, some j)) = b * (t j * y (none, some j)) := fun j => by ring
    have h5 : ∀ i j, s i * t j * (a * x (some i, some j)) = a * (s i * t j * x (some i, some j)) :=
      fun i j => by ring
    have h6 : ∀ i j, s i * t j * (b * y (some i, some j)) = b * (s i * t j * y (some i, some j)) :=
      fun i j => by ring
    simp only [h1, h2, h3, h4, h5, h6]
    linear_combination (-1 : ℝ) * hab
  rw [hlin]
  exact add_nonneg (mul_nonneg ha e1) (mul_nonneg hb e2)

/-- there are finitely many product states -/
theorem pureSetB_finite (bA : Fin mA → Fin rA) (bB : Fin mB → Fin rB) :
    (pureSetB bA bB).Finite := by
  have hfin : (Set.pi Set.univ (fun _ : Idx mA mB => ({-1, 0, 1} : Set ℝ))).Finite :=
    Set.Finite.pi fun _ => Set.toFinite _
  refine hfin.subset ?_
  rintro _ ⟨v, w, hv, hw, rfl⟩ u _
  have hvals : ∀ {m r : ℕ} (b : Fin m → Fin r) (z : Fin m → ℝ), IsBlockVert b z →
      ∀ o, ext1 z o = -1 ∨ ext1 z o = 0 ∨ ext1 z o = 1 := by
    intro m r b z hz o
    rcases o with _ | i
    · simp [ext1]
    · obtain ⟨i0, σ, -, hσ, h⟩ := hz i
      simp only [ext1, h i rfl]
      split_ifs
      · rcases hσ with e | e <;> simp [e]
      · simp
  simp only [pureProd, Set.mem_insert_iff, Set.mem_singleton_iff]
  rcases hvals bA v hv u.1 with h | h | h <;> rcases hvals bB w hw u.2 with h' | h' | h' <;>
    rw [h, h'] <;> norm_num

/-- **The hypotheses of `m11_blocks_polytope` on `S` can be met** (PROVED-IN-MODEL): `S` = the
convex hull of the product states is a polytope between the product states and the maximal tensor
product. (Its invariance under the local symmetries is not stated here.) -/
theorem blocks_hyps_consistent (bA : Fin mA → Fin rA) (bB : Fin mB → Fin rB) :
    ∃ V : Set (Idx mA mB → ℝ), V.Finite ∧ convexHull ℝ V ⊆ maxSetB bA bB ∧
      pureSetB bA bB ⊆ convexHull ℝ V :=
  ⟨pureSetB bA bB, pureSetB_finite bA bB,
    convexHull_min (pure_mem_maxSetB bA bB) (maxSetB_convex bA bB), subset_convexHull ℝ _⟩

end GTAORnd.SelfRef.LR3.M11Blocks
