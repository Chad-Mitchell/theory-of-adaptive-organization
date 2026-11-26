/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, stepback Lemma R (`theory/lemma-r-2026-11-26/LEMMA_R.md`, ledger RC20): product vectors of
polygon composites. Folklore-level, novelty not claimed: the dual-functional step is Marcus–Moyls,
as Al-Safi–Richens 2015 Lemma 4; the line argument is the rook's-graph automorphism fact. Lean
round 6 of the side session; written in a private Lake project (same Lean and Mathlib pins) and moved
here with only this header and the module lines changed.
-/
module

public import Mathlib

@[expose] public section

/-!
# Lemma R for polygon composites (Lean round 6)

Folklore-level; novelty is not claimed (the dual-functional step of Marcus–Moyls / Al-Safi–Richens
2015 Lemma 4, and the automorphisms of the rook's graph, Harary 1958; Al-Safi and Richens 2015 use
the same adjacency idea for effects). Source: `rnd/stepback/LEMMA_R.md` with its §9 corrections.
-/

namespace GTAORnd.SelfRef.LR3.LemmaR

open Matrix Finset

variable {K : Type*} [Field K]

/-- the product vector `a_i ⊗ b_j`, as the matrix `a_i b_jᵀ` -/
def kr {m n dA dB : ℕ} (a : Fin m → Fin dA → K) (b : Fin n → Fin dB → K) (p : Fin m × Fin n) :
    Matrix (Fin dA) (Fin dB) K :=
  vecMulVec (a p.1) (b p.2)

/-- S2: any set of at most three vectors of the family is linearly independent -/
def Indep3 {N d : ℕ} (v : Fin N → Fin d → K) : Prop :=
  ∀ s : Finset (Fin N), s.card ≤ 3 → LinearIndepOn K v (s : Set (Fin N))

section Helpers
variable {dA dB : ℕ}

lemma vecMulVec_sum_right {ι : Type*} (s : Finset ι) (x : Fin dA → K) (c : ι → K)
    (y : ι → Fin dB → K) :
    vecMulVec x (∑ i ∈ s, c i • y i) = ∑ i ∈ s, c i • vecMulVec x (y i) := by
  ext r t
  simp only [vecMulVec_apply, Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Matrix.sum_apply,
    Matrix.smul_apply, Finset.mul_sum]
  exact Finset.sum_congr rfl fun i _ => by ring

/-- **The dual-functional step** (Marcus–Moyls; Al-Safi–Richens 2015 Lemma 4): if the `v i` are
independent and `∑ v_i ⊗ β_i = 0`, every `β_i` is zero. -/
lemma dual_step {ι : Type*} {s : Finset ι} {v : ι → Fin dA → K} (hv : LinearIndepOn K v (s : Set ι))
    (β : ι → Fin dB → K) (h : ∑ i ∈ s, vecMulVec (v i) (β i) = 0) : ∀ i ∈ s, β i = 0 := by
  intro i hi
  funext t
  have hcol : ∑ j ∈ s, β j t • v j = 0 := by
    funext r
    have := congrFun (congrFun h r) t
    simp only [Matrix.sum_apply, vecMulVec_apply, Matrix.zero_apply] at this
    simp only [Finset.sum_apply, Pi.smul_apply, smul_eq_mul, Pi.zero_apply]
    rw [← this]
    exact Finset.sum_congr rfl fun j _ => by ring
  exact linearIndepOn_finset_iff.1 hv (fun j => β j t) hcol i hi

/-- a dual vector picking out one member of an independent family -/
lemma exists_dual {ι : Type*} [DecidableEq ι] {s : Finset ι} {v : ι → Fin dA → K}
    (hv : LinearIndepOn K v (s : Set ι)) {i0 : ι} (hi0 : i0 ∈ s) :
    ∃ f : Fin dA → K, ∀ i ∈ s, f ⬝ᵥ v i = if i = i0 then 1 else 0 := by
  have hli : LinearIndependent K (fun i : (s : Set ι) => v i) := hv
  let B := Module.Basis.span hli
  obtain ⟨g, hg⟩ := LinearMap.exists_extend (B.coord ⟨i0, hi0⟩)
  refine ⟨fun r => g (Pi.single r 1), fun i hi => ?_⟩
  have hgv : g (v i) = B.coord ⟨i0, hi0⟩ (B ⟨i, hi⟩) := by
    rw [← hg, LinearMap.comp_apply, Submodule.subtype_apply, Module.Basis.span_apply]
  have hdot : (fun r => g (Pi.single r 1)) ⬝ᵥ v i = g (v i) := by
    rw [LinearMap.pi_apply_eq_sum_univ g (v i)]
    simp only [dotProduct, smul_eq_mul]
    refine Finset.sum_congr rfl fun r _ => ?_
    have e : (fun j => if r = j then (1 : K) else 0) = Pi.single r 1 := by
      funext j; simp [Pi.single_apply, eq_comm]
    rw [e, mul_comm]
  rw [hdot, hgv, Module.Basis.coord_apply, Module.Basis.repr_self]
  by_cases h : i = i0
  · subst h; simp
  · rw [Finsupp.single_apply]
    simp [h]

/-- contracting the first factor with a dual vector -/
lemma vecMul_vecMulVec (f x : Fin dA → K) (y : Fin dB → K) :
    f ᵥ* vecMulVec x y = (f ⬝ᵥ x) • y := by
  funext t
  simp only [vecMul, dotProduct, vecMulVec_apply, Pi.smul_apply, smul_eq_mul, Finset.sum_mul]
  exact Finset.sum_congr rfl fun r _ => by ring

end Helpers

section LemmaD
variable {m n dA dB : ℕ} {a : Fin m → Fin dA → K} {b : Fin n → Fin dB → K}

/-- Lemma D, case of at most three rows, none holding all of `Y`. -/
lemma indep_of_rows (hA : Indep3 a) (hB : Indep3 b) {Y : Finset (Fin m × Fin n)}
    (hI : (Y.image Prod.fst).card ≤ 3) (hF : ∀ i, (Y.filter (fun p => p.1 = i)).card ≤ 3) :
    LinearIndepOn K (kr a b) (Y : Set (Fin m × Fin n)) := by
  classical
  rw [linearIndepOn_finset_iff]
  intro c hc
  have hgroup : ∑ i ∈ Y.image Prod.fst,
      vecMulVec (a i) (∑ p ∈ Y with p.1 = i, c p • b p.2) = 0 := by
    rw [← hc, ← Finset.sum_fiberwise_of_maps_to (s := Y) (t := Y.image Prod.fst) (g := Prod.fst)
      (fun p hp => Finset.mem_image_of_mem _ hp)]
    refine Finset.sum_congr rfl fun i _ => ?_
    rw [vecMulVec_sum_right]
    refine Finset.sum_congr rfl fun p hp => ?_
    rw [kr, (Finset.mem_filter.1 hp).2]
  have hrow := dual_step (hA _ hI) (fun i => ∑ p ∈ Y with p.1 = i, c p • b p.2) hgroup
  intro p hp
  have hpI : p.1 ∈ Y.image Prod.fst := Finset.mem_image_of_mem _ hp
  have hinj : Set.InjOn Prod.snd ((Y.filter (fun q => q.1 = p.1) : Finset _) : Set (Fin m × Fin n)) := by
    intro x hx y hy hxy
    have hx' := (Finset.mem_filter.1 (Finset.mem_coe.1 hx)).2
    have hy' := (Finset.mem_filter.1 (Finset.mem_coe.1 hy)).2
    exact Prod.ext (hx'.trans hy'.symm) hxy
  have hsum : ∑ j ∈ (Y.filter (fun q => q.1 = p.1)).image Prod.snd, c (p.1, j) • b j = 0 := by
    rw [Finset.sum_image hinj, ← hrow p.1 hpI]
    refine Finset.sum_congr rfl fun q hq => ?_
    rw [← (Finset.mem_filter.1 hq).2]
  have hcard : ((Y.filter (fun q => q.1 = p.1)).image Prod.snd).card ≤ 3 :=
    Finset.card_image_le.trans (hF p.1)
  have := linearIndepOn_finset_iff.1 (hB _ hcard) (fun j => c (p.1, j)) hsum p.2
    (Finset.mem_image_of_mem _ (Finset.mem_filter.2 ⟨hp, rfl⟩))
  simpa using this

/-- Lemma D, case of at most three columns, none holding all of `Y` (transpose of the rows case). -/
lemma indep_of_cols (hA : Indep3 a) (hB : Indep3 b) {Y : Finset (Fin m × Fin n)}
    (hJ : (Y.image Prod.snd).card ≤ 3) (hF : ∀ j, (Y.filter (fun p => p.2 = j)).card ≤ 3) :
    LinearIndepOn K (kr a b) (Y : Set (Fin m × Fin n)) := by
  classical
  have hY' : LinearIndepOn K (kr b a) ((Y.image Prod.swap : Finset _) : Set (Fin n × Fin m)) := by
    apply indep_of_rows hB hA
    · rw [Finset.image_image]; exact hJ
    · intro j
      refine (Finset.card_le_card (t := (Y.filter (fun p => p.2 = j)).image Prod.swap) ?_).trans
        (Finset.card_image_le.trans (hF j))
      intro q hq
      simp only [Finset.mem_filter, Finset.mem_image] at hq ⊢
      obtain ⟨⟨x, hx, rfl⟩, h⟩ := hq
      exact ⟨x, ⟨hx, h⟩, rfl⟩
  rw [linearIndepOn_finset_iff] at hY' ⊢
  intro c hc p hp
  have h := hY' (fun q => c q.swap) ?_ p.swap (Finset.mem_image_of_mem _ hp)
  · simpa using h
  · rw [Finset.sum_image (fun x _ y _ h => Prod.swap_injective h)]
    have := congrArg Matrix.transpose hc
    rw [transpose_sum, transpose_zero] at this
    rw [← this]
    refine Finset.sum_congr rfl fun q _ => ?_
    simp [kr, transpose_smul, transpose_vecMulVec]

/-- **Lemma D** (any dimensions): under S2 for both families, any four product vectors `a_i ⊗ b_j`
whose index pairs lie neither in one row nor in one column are linearly independent. -/
theorem lemmaD (hA : Indep3 a) (hB : Indep3 b) {Y : Finset (Fin m × Fin n)} (hY : Y.card = 4)
    (h1 : ∃ p ∈ Y, ∃ q ∈ Y, p.1 ≠ q.1) (h2 : ∃ p ∈ Y, ∃ q ∈ Y, p.2 ≠ q.2) :
    LinearIndepOn K (kr a b) (Y : Set (Fin m × Fin n)) := by
  classical
  have hF1 : ∀ i, (Y.filter (fun p => p.1 = i)).card ≤ 3 := by
    intro i
    by_contra hc
    have heq : Y.filter (fun p => p.1 = i) = Y :=
      Finset.eq_of_subset_of_card_le (Finset.filter_subset _ Y) (by omega)
    obtain ⟨p, hp, q, hq, hpq⟩ := h1
    rw [← heq, Finset.mem_filter] at hp hq
    exact hpq (hp.2.trans hq.2.symm)
  have hF2 : ∀ j, (Y.filter (fun p => p.2 = j)).card ≤ 3 := by
    intro j
    by_contra hc
    have heq : Y.filter (fun p => p.2 = j) = Y :=
      Finset.eq_of_subset_of_card_le (Finset.filter_subset _ Y) (by omega)
    obtain ⟨p, hp, q, hq, hpq⟩ := h2
    rw [← heq, Finset.mem_filter] at hp hq
    exact hpq (hp.2.trans hq.2.symm)
  by_cases hI : (Y.image Prod.fst).card ≤ 3
  · exact indep_of_rows hA hB hI hF1
  by_cases hJ : (Y.image Prod.snd).card ≤ 3
  · exact indep_of_cols hA hB hJ hF2
  have hI4 : (Y.image Prod.fst).card = Y.card := by
    have := Finset.card_image_le (s := Y) (f := Prod.fst); omega
  have hJ4 : (Y.image Prod.snd).card = Y.card := by
    have := Finset.card_image_le (s := Y) (f := Prod.snd); omega
  have inj1 := Finset.card_image_iff.1 hI4
  have inj2 := Finset.card_image_iff.1 hJ4
  rw [linearIndepOn_finset_iff]
  intro c hc p0 hp0
  have h3 : (Y.erase p0).card = 3 := by rw [Finset.card_erase_of_mem hp0, hY]
  obtain ⟨q, r, t, hqr, hqt, hrt, hE⟩ := Finset.card_eq_three.1 h3
  have hq : q ∈ Y.erase p0 := by rw [hE]; simp
  have hr : r ∈ Y.erase p0 := by rw [hE]; simp
  have ht : t ∈ Y.erase p0 := by rw [hE]; simp
  have hne : ∀ x ∈ Y.erase p0, x.1 ≠ p0.1 ∧ x.2 ≠ p0.2 := by
    intro x hx
    obtain ⟨hxp, hxY⟩ := Finset.mem_erase.1 hx
    exact ⟨fun e => hxp (inj1 hxY hp0 e), fun e => hxp (inj2 hxY hp0 e)⟩
  obtain ⟨f, hf⟩ := exists_dual (hA {p0.1, q.1, r.1} Finset.card_le_three) (i0 := p0.1) (by simp)
  have hf0 : f ⬝ᵥ a p0.1 = 1 := by simpa using hf p0.1 (by simp)
  have hfq : f ⬝ᵥ a q.1 = 0 := by simpa [(hne q hq).1] using hf q.1 (by simp)
  have hfr : f ⬝ᵥ a r.1 = 0 := by simpa [(hne r hr).1] using hf r.1 (by simp)
  have hrel := congrArg (fun M => f ᵥ* M) hc
  simp only [vecMul_sum, vecMul_smul, kr, vecMul_vecMulVec, vecMul_zero] at hrel
  rw [← Finset.insert_erase hp0, Finset.sum_insert (Finset.notMem_erase p0 Y), hE,
    Finset.sum_insert (by simp [hqr, hqt]), Finset.sum_insert (by simp [hrt]),
    Finset.sum_singleton, hf0, hfq, hfr] at hrel
  simp only [zero_smul, smul_zero, one_smul, zero_add, smul_smul] at hrel
  have hpt : p0.2 ≠ t.2 := fun e => (hne t ht).2 e.symm
  have hB2 := linearIndepOn_finset_iff.1
    (hB {p0.2, t.2} ((Finset.card_pair_eq_two_iff.2 hpt).le.trans (by norm_num)))
  have := hB2 (fun j => if j = p0.2 then c p0 else c t * (f ⬝ᵥ a t.1)) (by
      rw [Finset.sum_pair hpt]; simpa [hpt.symm] using hrel) p0.2 (by simp)
  simpa using this

end LemmaD

section Rook

/-- rook's-graph adjacency: same row or same column (a point is adjacent to itself) -/
def RookAdj {α β : Type*} (x y : α × β) : Prop := x.1 = y.1 ∨ x.2 = y.2

/-- three distinct pairwise adjacent points lie in one row or one column -/
lemma line_of_triangle {α β : Type*} {x y z : α × β} (hxy : x ≠ y) (hxz : x ≠ z) (_hyz : y ≠ z)
    (h1 : RookAdj x y) (h2 : RookAdj x z) (h3 : RookAdj y z) :
    (x.1 = y.1 ∧ x.1 = z.1) ∨ (x.2 = y.2 ∧ x.2 = z.2) := by
  unfold RookAdj at h1 h2 h3
  rcases h1 with h1 | h1 <;> rcases h2 with h2 | h2
  · exact Or.inl ⟨h1, h2⟩
  · exfalso
    rcases h3 with h3 | h3
    · exact hxz (Prod.ext (h1.trans h3) h2)
    · exact hxy (Prod.ext h1 (h2.trans h3.symm))
  · exfalso
    rcases h3 with h3 | h3
    · exact hxy (Prod.ext (h2.trans h3.symm) h1)
    · exact hxz (Prod.ext h2 (h1.trans h3))
  · exact Or.inr ⟨h1, h2⟩

variable {m n p q : ℕ} {f : Fin m × Fin n → Fin p × Fin q}

/-- a row whose first two images share a row maps into that row -/
lemma row_line (hf : Function.Injective f) (hadj : ∀ x y, RookAdj (f x) (f y) ↔ RookAdj x y)
    {j0 j1 : Fin n} (h01 : j0 ≠ j1) (i : Fin m) (hrow : (f (i, j0)).1 = (f (i, j1)).1)
    (j : Fin n) : (f (i, j)).1 = (f (i, j0)).1 := by
  by_cases hj0 : j = j0
  · rw [hj0]
  by_cases hj1 : j = j1
  · rw [hj1, hrow]
  have ne : ∀ {a b : Fin n}, a ≠ b → f (i, a) ≠ f (i, b) :=
    fun hab e => hab (congrArg Prod.snd (hf e))
  have ad : ∀ a b : Fin n, RookAdj (f (i, a)) (f (i, b)) := fun a b => (hadj _ _).2 (Or.inl rfl)
  rcases line_of_triangle (ne h01) (ne (Ne.symm hj0)) (ne (Ne.symm hj1)) (ad _ _) (ad _ _)
    (ad _ _) with h | h
  · exact h.2.symm
  · exact absurd (hf (Prod.ext hrow h.1)) (fun e => h01 (congrArg Prod.snd e))

/-- a row whose first two images do not share a row maps into one column -/
lemma row_col (hf : Function.Injective f) (hadj : ∀ x y, RookAdj (f x) (f y) ↔ RookAdj x y)
    {j0 j1 : Fin n} (h01 : j0 ≠ j1) (i : Fin m) (hrow : (f (i, j0)).1 ≠ (f (i, j1)).1)
    (j : Fin n) : (f (i, j)).2 = (f (i, j0)).2 := by
  have h01' : (f (i, j0)).2 = (f (i, j1)).2 := ((hadj (i, j0) (i, j1)).2 (Or.inl rfl)).resolve_left hrow
  by_cases hj0 : j = j0
  · rw [hj0]
  by_cases hj1 : j = j1
  · rw [hj1, h01']
  have ne : ∀ {a b : Fin n}, a ≠ b → f (i, a) ≠ f (i, b) :=
    fun hab e => hab (congrArg Prod.snd (hf e))
  have ad : ∀ a b : Fin n, RookAdj (f (i, a)) (f (i, b)) := fun a b => (hadj _ _).2 (Or.inl rfl)
  rcases line_of_triangle (ne h01) (ne (Ne.symm hj0)) (ne (Ne.symm hj1)) (ad _ _) (ad _ _)
    (ad _ _) with h | h
  · exact absurd h.1 hrow
  · exact h.2.symm

/-- all rows have the same type -/
lemma same_type (hadj : ∀ x y, RookAdj (f x) (f y) ↔ RookAdj x y)
    {j0 j1 : Fin n} (h01 : j0 ≠ j1) {i i' : Fin m} (hii : i ≠ i')
    (hr : (f (i, j0)).1 = (f (i, j1)).1) : (f (i', j0)).1 = (f (i', j1)).1 := by
  by_contra hr'
  have hc : (f (i', j0)).2 = (f (i', j1)).2 := ((hadj (i', j0) (i', j1)).2 (Or.inl rfl)).resolve_left hr'
  have a1 : RookAdj (f (i, j0)) (f (i', j0)) := (hadj _ _).2 (Or.inr rfl)
  have n1 : ¬ RookAdj (f (i, j1)) (f (i', j0)) := fun h => by
    rcases (hadj _ _).1 h with h | h
    · exact hii h
    · exact h01 h.symm
  have n2 : ¬ RookAdj (f (i, j0)) (f (i', j1)) := fun h => by
    rcases (hadj _ _).1 h with h | h
    · exact hii h
    · exact h01 h
  rcases a1 with a | a
  · exact n1 (Or.inl (hr.symm.trans a))
  · exact n2 (Or.inr (a.trans hc))

/-- if every row maps into a row, the map is a product map -/
lemma assemble (hf : Function.Injective f) (hadj : ∀ x y, RookAdj (f x) (f y) ↔ RookAdj x y)
    {j0 j1 : Fin n} (h01 : j0 ≠ j1) (i0 : Fin m) (hall : ∀ i, (f (i, j0)).1 = (f (i, j1)).1) :
    ∀ x, f x = ((f (x.1, j0)).1, (f (i0, x.2)).2) := by
  rintro ⟨i, j⟩
  refine Prod.ext (row_line hf hadj h01 i (hall i) j) ?_
  show (f (i, j)).2 = (f (i0, j)).2
  by_cases hi : i = i0
  · rw [hi]
  rcases (hadj (i, j) (i0, j)).2 (Or.inr rfl) with h | h
  · exfalso
    obtain ⟨j', hj'⟩ : ∃ j', j' ≠ j := by
      by_cases hj : j = j0
      · exact ⟨j1, by rw [hj]; exact h01.symm⟩
      · exact ⟨j0, Ne.symm hj⟩
    have e1 := row_line hf hadj h01 i0 (hall i0) j
    have e2 := row_line hf hadj h01 i0 (hall i0) j'
    have hadj' : RookAdj (f (i, j)) (f (i0, j')) := Or.inl (h.trans (e1.trans e2.symm))
    rcases (hadj _ _).1 hadj' with h' | h'
    · exact hi h'
    · exact hj' h'.symm
  · exact h

/-- **Rook's-graph step** (Harary 1958 for the automorphisms; here for injective maps preserving
adjacency both ways, `m ≥ 1`, `n ≥ 2`): such a map is a product map, or a product map composed with
the swap of the two coordinates. -/
theorem rook_aut (hm : 0 < m) (hn : 2 ≤ n) (hf : Function.Injective f)
    (hadj : ∀ x y, RookAdj (f x) (f y) ↔ RookAdj x y) :
    (∃ α : Fin m → Fin p, ∃ β : Fin n → Fin q, ∀ x, f x = (α x.1, β x.2)) ∨
    (∃ α : Fin n → Fin p, ∃ β : Fin m → Fin q, ∀ x, f x = (α x.2, β x.1)) := by
  let j0 : Fin n := ⟨0, by omega⟩
  let j1 : Fin n := ⟨1, by omega⟩
  have h01 : j0 ≠ j1 := by simp [j0, j1, Fin.ext_iff]
  let i0 : Fin m := ⟨0, hm⟩
  by_cases h : (f (i0, j0)).1 = (f (i0, j1)).1
  · have hall : ∀ i, (f (i, j0)).1 = (f (i, j1)).1 := fun i => by
      by_cases hi : i0 = i
      · rw [← hi]; exact h
      · exact same_type hadj h01 hi h
    exact Or.inl ⟨fun i => (f (i, j0)).1, fun j => (f (i0, j)).2, assemble hf hadj h01 i0 hall⟩
  · let g : Fin m × Fin n → Fin q × Fin p := fun x => (f x).swap
    have hg : Function.Injective g := fun x y e => hf (Prod.swap_injective e)
    have hgadj : ∀ x y, RookAdj (g x) (g y) ↔ RookAdj x y := fun x y => by
      rw [← hadj]; unfold RookAdj; simp only [g, Prod.fst_swap, Prod.snd_swap]; exact or_comm
    have hall : ∀ i, (g (i, j0)).1 = (g (i, j1)).1 := fun i => by
      have hi : (f (i, j0)).1 ≠ (f (i, j1)).1 := fun e => by
        by_cases hi : i = i0
        · rw [hi] at e; exact h e
        · exact h (same_type hadj h01 hi e)
      exact ((hadj (i, j0) (i, j1)).2 (Or.inl rfl)).resolve_left hi
    refine Or.inr ⟨fun j => (g (i0, j)).2, fun i => (g (i, j0)).1, fun x => ?_⟩
    have e : f x = (g x).swap := (Prod.swap_swap _).symm
    rw [e, assemble hg hgadj h01 i0 hall x]
    rfl

end Rook

end GTAORnd.SelfRef.LR3.LemmaR
