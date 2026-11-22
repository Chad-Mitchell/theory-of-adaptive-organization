/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lean 4 formalization of Lemma L1 of `theory/LAYER_CONVEXITY.md` (PR #145,
CLAIM_MAP N64): the from-0 count \(K^\star_0(R)=\#\{K\ge 1: R\,d_K>1\}\)
equals the leftmost argmin when decrements are non-increasing; the
converse holds under positive, pairwise distinct decrements (distinctness
with the threshold decrement positive suffices); and \(d=(-2,-1)\) is a
counterexample to a bare iff.  For OPEN_WORK T19.
-/
module

public import GTAO.Hull
public import Mathlib.Data.Finset.Card
public import Mathlib.Order.Interval.Finset.Nat

/-!
# L1: when the N60-from-0 count is exact

On `{0,…,n}` with `φ(K) = K + R(1 + ε_K)`, the from-0 count is the
number of paying adjacent steps,
`count R = #{i < n : 1 < R (ε_i - ε_{i+1})}`
(equivalently \(K^\star_0(R)=\#\{K\in[1,n]: R d_K>1\}\) with
`d_K = ε_{K-1} - ε_K`).

* `count_isLeftmostArgmin`: if the decrements are non-increasing
  (`DiscreteConvexOn n ε`) and `R ≥ 0`, `count R` is the leftmost minimizer.
* `exists_R_count_not_argmin`: if the step decrements are pairwise distinct,
  some decrement rises (`d_m < d_{m+1}`), and the threshold decrement
  `d_{(m)}` is positive (equivalently, at least `m` decrements are
  positive), there is an `R > 0` at which `count R` is not a minimizer.
  All-positive decrements are a special case.
* `count_exact_iff_convex`: with positive, distinct decrements, the count is
  the leftmost argmin for every `R > 0` iff the decrements are non-increasing.
* `exists_nonconvex_count_exact`: without positivity, the bare iff is false:
  `d = (-2, -1)` (`ε = (-3, -1, 0)`) is not convex, yet the count equals
  the unique minimizer for every `R ≥ 0`.
-/

@[expose] public section

open Finset

namespace N60Exact

/-- The N60 count from `0`: the number of paying adjacent steps.
This is \(K^\star_0(R)=\#\{K\ge 1: R(\varepsilon_{K-1}-\varepsilon_K)>1\}\). -/
noncomputable def count (R : ℝ) (ε : ℕ → ℝ) (n : ℕ) : ℕ := by
  classical exact ((range n).filter (fun i => IncrementPays R ε i)).card

/-- `k` is the leftmost minimizer of `φ` on `{0,…,n}`. -/
def IsLeftmostArgmin (R : ℝ) (ε : ℕ → ℝ) (n k : ℕ) : Prop :=
  k ≤ n ∧ (∀ j ≤ n, phi R ε k ≤ phi R ε j) ∧ ∀ j < k, phi R ε k < phi R ε j

/-- **L1 (⇒).**  Non-increasing decrements and `R ≥ 0`: the from-0 count is the
leftmost minimizer of `φ`. -/
theorem count_isLeftmostArgmin {n : ℕ} {ε : ℕ → ℝ} {R : ℝ} (hR : 0 ≤ R)
    (hconv : DiscreteConvexOn n ε) : IsLeftmostArgmin R ε n (count R ε n) := by
  classical
  have hex : ∃ s, s = n ∨ ¬ IncrementPays R ε s := ⟨n, Or.inl rfl⟩
  set s := Nat.find hex with hs_def
  have hsn : s ≤ n := Nat.find_min' hex (Or.inl rfl)
  have hBefore : ∀ i < s, IncrementPays R ε i := by
    intro i hi
    have := Nat.find_min hex hi
    push Not at this
    exact this.2
  have hStop : s = n ∨ ¬ IncrementPays R ε s := Nat.find_spec hex
  have hfilter : (range n).filter (fun i => IncrementPays R ε i) = range s := by
    ext i
    simp only [mem_filter, mem_range]
    constructor
    · rintro ⟨hin, hp⟩
      by_contra hge
      push Not at hge
      rcases hStop with h | h
      · omega
      · exact h (hconv.pays_of_later hR (by omega) hin hge hp)
    · intro hi
      exact ⟨by omega, hBefore i hi⟩
  have hc : count R ε n = s := by
    unfold count; rw [hfilter, card_range]
  rw [hc]
  obtain ⟨h1, h2⟩ := n60_from_zero_leftmost n ε hR hconv hsn hBefore hStop
  exact ⟨hsn, h1, h2⟩

/-- A point where the decrement rises is never a minimizer, for any `R > 0`. -/
lemma not_min_of_rise {n : ℕ} {ε : ℕ → ℝ} {R : ℝ} (hR : 0 < R) {j : ℕ} (hj : j + 2 ≤ n)
    (hrise : ε j - ε (j + 1) < ε (j + 1) - ε (j + 2)) :
    ∃ k ≤ n, phi R ε k < phi R ε (j + 1) := by
  have h1 := phi_diff R ε j
  have h2 := phi_diff R ε (j + 1)
  have hm : R * (ε j - ε (j + 1)) < R * (ε (j + 1) - ε (j + 2)) :=
    mul_lt_mul_of_pos_left hrise hR
  by_cases h : phi R ε (j + 1) ≤ phi R ε j
  · refine ⟨j + 2, hj, ?_⟩
    have : phi R ε (j + 1 + 1) - phi R ε (j + 1) < 0 := by
      rw [h2]; nlinarith
    simpa using this
  · exact ⟨j, by omega, lt_of_not_ge h⟩

/-- Pairwise distinct step decrements realize every count: for every
`c < n` some threshold decrement has exactly `c` decrements above it. -/
lemma exists_threshold {n : ℕ} (g : ℕ → ℝ)
    (hdist : ∀ i < n, ∀ i' < n, i ≠ i' → g i ≠ g i') {c : ℕ} (hc : c < n) :
    ∃ i0 < n, ((range n).filter (fun k => g i0 < g k)).card = c := by
  classical
  let F : ℕ → ℕ := fun i => ((range n).filter (fun k => g i < g k)).card
  let f : ∀ i ∈ range n, ℕ := fun i _ => F i
  have hf : ∀ i hi, f i hi ∈ range n := by
    intro i hi
    simp only [f, F, mem_range]
    have hsub : (range n).filter (fun k => g i < g k) ⊂ range n := by
      refine ⟨filter_subset _ _, fun h => ?_⟩
      have := h hi
      simp at this
    simpa using card_lt_card hsub
  have hlt : ∀ x y, y ∈ range n → g x < g y → F y < F x := by
    intro x y hy hxy
    simp only [F]
    apply card_lt_card
    refine ⟨fun k hk => ?_, fun h => ?_⟩
    · simp only [mem_filter] at hk ⊢; exact ⟨hk.1, hxy.trans hk.2⟩
    · have : y ∈ (range n).filter (fun k => g y < g k) := h (by simp [mem_filter, hy, hxy])
      simp at this
  have hinj : ∀ a₁ a₂ ha₁ ha₂, f a₁ ha₁ = f a₂ ha₂ → a₁ = a₂ := by
    intro a b ha hb hab
    simp only [f] at hab
    by_contra hne
    rcases lt_or_gt_of_ne (hdist a (mem_range.mp ha) b (mem_range.mp hb) hne) with h | h
    · exact absurd hab (hlt a b hb h).ne'
    · exact absurd hab (hlt b a ha h).ne
  obtain ⟨i0, hi0, heq⟩ := surj_on_of_inj_on_of_card_le f hf hinj (by simp) c (mem_range.mpr hc)
  exact ⟨i0, mem_range.mp hi0, heq.symm⟩

/-- If a decrement has exactly `c` values strictly above it and at least
`c+1` decrements are positive, then it is itself positive.  This is
`d_{(c+1)} > 0` under distinctness. -/
lemma threshold_pos {n : ℕ} {g : ℕ → ℝ} {i0 c : ℕ} (_hi0 : i0 < n)
    (hcard : ((range n).filter (fun k => g i0 < g k)).card = c)
    (hpos : c < ((range n).filter (fun k => 0 < g k)).card) :
    0 < g i0 := by
  classical
  by_contra hle
  have hle' : g i0 ≤ 0 := le_of_not_gt hle
  have hsub : (range n).filter (fun k => 0 < g k) ⊆
      (range n).filter (fun k => g i0 < g k) := by
    intro k hk
    simp only [mem_filter] at hk ⊢
    exact ⟨hk.1, lt_of_le_of_lt hle' hk.2⟩
  have := card_le_card hsub
  omega

/-- **L1 (⇐), general form.**  If the step decrements
`g i = ε_i - ε_{i+1}` (`i < n`) are pairwise distinct, some decrement
rises (`g j < g (j+1)`, `j + 2 ≤ n`), and the threshold decrement
`d_{(m)}` with `m = j+1` is positive (equivalently, at least `m`
decrements are positive), then for some `R > 0` the from-0 count is not
a minimizer of `φ`. -/
theorem exists_R_count_not_argmin {n : ℕ} {ε : ℕ → ℝ}
    (hdist : ∀ i < n, ∀ i' < n, i ≠ i' → ε i - ε (i + 1) ≠ ε i' - ε (i' + 1))
    {j : ℕ} (hj : j + 2 ≤ n) (hrise : ε j - ε (j + 1) < ε (j + 1) - ε (j + 2))
    (hthresh : j + 1 ≤ ((range n).filter (fun k => 0 < ε k - ε (k + 1))).card) :
    ∃ R, 0 < R ∧ ∃ k ≤ n, phi R ε k < phi R ε (count R ε n) := by
  classical
  set g : ℕ → ℝ := fun i => ε i - ε (i + 1)
  obtain ⟨i0, hi0, hcard0⟩ := exists_threshold g hdist (c := j) (by omega)
  have ht : 0 < g i0 :=
    threshold_pos hi0 hcard0 (lt_of_lt_of_le (Nat.lt_succ_self j) hthresh)
  obtain ⟨i1, hi1, hcard1⟩ := exists_threshold g hdist (c := j + 1) (by omega)
  have hlt : g i1 < g i0 := by
    have hne : i0 ≠ i1 := by
      intro heq
      rw [heq] at hcard0
      omega
    rcases lt_or_gt_of_ne (hdist i0 hi0 i1 hi1 hne) with h | h
    · have hg : g i0 < g i1 := h
      have : ((range n).filter (fun k => g i1 < g k)).card <
          ((range n).filter (fun k => g i0 < g k)).card := by
        apply card_lt_card
        refine ⟨fun k hk => ?_, fun hsub => ?_⟩
        · simp only [mem_filter] at hk ⊢; exact ⟨hk.1, hg.trans hk.2⟩
        · have : i1 ∈ (range n).filter (fun k => g i1 < g k) :=
            hsub (by simp [mem_filter, mem_range, hi1, hg])
          simp at this
      omega
    · exact h
  set t := g i0
  set u := g i1
  set rinv := (t + max u 0) / 2
  have hrinvpos : 0 < rinv := by
    have hmax0 : 0 ≤ max u 0 := le_max_right _ _
    have : 0 < t + max u 0 := add_pos_of_pos_of_nonneg ht hmax0
    positivity
  have hmax_lt : max u 0 < t := by
    cases le_total u 0 with
    | inl hu =>
      rw [max_eq_right hu]
      exact ht
    | inr hu =>
      rw [max_eq_left hu]
      exact hlt
  have hrinv_lt : rinv < t := by
    have h2 : (0 : ℝ) < 2 := by norm_num
    exact (div_lt_iff₀ h2).mpr (by linarith)
  have hu_lt_rinv : u < rinv := by
    have h2 : (0 : ℝ) < 2 := by norm_num
    have : u ≤ max u 0 := le_max_left _ _
    exact (lt_div_iff₀ h2).mpr (by linarith)
  -- Nothing sits strictly between `u` and `t`, so
  -- `{k | t < g k} ∪ {i0} = {k | u < g k}`.
  have hsub : (range n).filter (fun k => t < g k) ⊆
      (range n).filter (fun k => u < g k) := by
    intro k hk
    simp only [mem_filter] at hk ⊢
    exact ⟨hk.1, hlt.trans hk.2⟩
  have hi0_in : i0 ∈ (range n).filter (fun k => u < g k) := by
    simp [mem_filter, mem_range, hi0]
    exact hlt
  have hi0_not : i0 ∉ (range n).filter (fun k => t < g k) := by
    simp [mem_filter, t]
  have hdisj : Disjoint ((range n).filter (fun k => t < g k)) {i0} :=
    disjoint_singleton_right.mpr hi0_not
  have hunion_sub : (range n).filter (fun k => t < g k) ∪ {i0} ⊆
      (range n).filter (fun k => u < g k) := by
    intro k hk
    simp only [mem_union, mem_singleton] at hk
    rcases hk with hk | rfl
    · exact hsub hk
    · exact hi0_in
  have hcard_union : (((range n).filter (fun k => t < g k)) ∪ {i0}).card = j + 1 := by
    have hF0 : ((range n).filter (fun k => t < g k)).card = j := hcard0
    rw [card_union_of_disjoint hdisj, hF0, card_singleton]
  have heq : (range n).filter (fun k => t < g k) ∪ {i0} =
      (range n).filter (fun k => u < g k) :=
    eq_of_subset_of_card_le hunion_sub (by rw [hcard_union, hcard1])
  have hiff : ∀ k < n, rinv < g k ↔ u < g k := by
    intro k hk
    constructor
    · intro h; exact hu_lt_rinv.trans h
    · intro huk
      have : k ∈ (range n).filter (fun k => t < g k) ∪ {i0} := by
        rw [heq]
        simp [mem_filter, mem_range, hk, huk]
      simp only [mem_union, mem_singleton, mem_filter] at this
      rcases this with htk | rfl
      · exact hrinv_lt.trans htk.2
      · exact hrinv_lt
  refine ⟨1 / rinv, by positivity, ?_⟩
  have hcount : count (1 / rinv) ε n = j + 1 := by
    unfold count
    have : (range n).filter (fun i => IncrementPays (1 / rinv) ε i) =
        (range n).filter (fun i => u < g i) := by
      apply filter_congr
      intro k hk
      have hk' : k < n := mem_range.mp hk
      unfold IncrementPays
      change (1 < (1 / rinv) * g k) ↔ u < g k
      rw [one_div, inv_mul_eq_div, one_lt_div hrinvpos]
      exact hiff k hk'
    rw [this, hcard1]
  rw [hcount]
  exact not_min_of_rise (by positivity) hj hrise

/-- Special case of the converse: all decrements positive (which implies
the threshold decrement is positive). -/
theorem exists_R_count_not_argmin_of_pos {n : ℕ} {ε : ℕ → ℝ}
    (hpos : ∀ i < n, 0 < ε i - ε (i + 1))
    (hdist : ∀ i < n, ∀ i' < n, i ≠ i' → ε i - ε (i + 1) ≠ ε i' - ε (i' + 1))
    {j : ℕ} (hj : j + 2 ≤ n) (hrise : ε j - ε (j + 1) < ε (j + 1) - ε (j + 2)) :
    ∃ R, 0 < R ∧ ∃ k ≤ n, phi R ε k < phi R ε (count R ε n) := by
  classical
  refine exists_R_count_not_argmin hdist hj hrise ?_
  have : (range n).filter (fun k => 0 < ε k - ε (k + 1)) = range n := by
    ext k
    simp only [mem_filter, mem_range, and_iff_left_iff_imp]
    intro hk
    exact hpos k hk
  rw [this, card_range]
  omega

/-- **L1 (iff).**  With positive, pairwise distinct step decrements, the
from-0 count is the leftmost argmin for every `R > 0` iff the decrements
are non-increasing. -/
theorem count_exact_iff_convex {n : ℕ} {ε : ℕ → ℝ}
    (hpos : ∀ i < n, 0 < ε i - ε (i + 1))
    (hdist : ∀ i < n, ∀ i' < n, i ≠ i' → ε i - ε (i + 1) ≠ ε i' - ε (i' + 1)) :
    (∀ R, 0 < R → IsLeftmostArgmin R ε n (count R ε n)) ↔ DiscreteConvexOn n ε := by
  constructor
  · intro h k hk0 hkn
    by_contra hc
    push Not at hc
    obtain ⟨j, rfl⟩ : ∃ j, k = j + 1 := ⟨k - 1, by omega⟩
    have hrise : ε j - ε (j + 1) < ε (j + 1) - ε (j + 2) := by
      simp only [Nat.add_sub_cancel] at hc; linarith
    obtain ⟨R, hR, k', hk', hlt⟩ := exists_R_count_not_argmin_of_pos hpos hdist (by omega) hrise
    exact absurd ((h R hR).2.1 k' hk') (not_le.mpr hlt)
  · intro hconv R hR
    exact count_isLeftmostArgmin hR.le hconv

/-! ## The bare-iff counterexample `d = (-2, -1)` -/

/-- `ε = (-3, -1, 0)`, so the decrements are `d = (-2, -1)`. -/
def epsCE (k : ℕ) : ℝ := if k = 0 then (-3 : ℝ) else if k = 1 then (-1 : ℝ) else 0

lemma epsCE_not_convex : ¬ DiscreteConvexOn 2 epsCE := by
  intro h
  have := h 1 (by omega) (by omega)
  simp [epsCE] at this
  linarith

lemma epsCE_count_zero {R : ℝ} (hR : 0 ≤ R) : count R epsCE 2 = 0 := by
  classical
  unfold count
  have hempty : (range 2).filter (fun i => IncrementPays R epsCE i) = ∅ := by
    ext i
    constructor
    · intro h
      simp only [mem_filter, mem_range] at h
      obtain ⟨hi, hp⟩ := h
      unfold IncrementPays at hp
      have hi' : i = 0 ∨ i = 1 := by omega
      rcases hi' with rfl | rfl <;> simp [epsCE] at hp <;> linarith
    · intro h
      exact False.elim (notMem_empty _ h)
  rw [hempty, card_empty]

lemma epsCE_zero_min {R : ℝ} (hR : 0 ≤ R) : IsLeftmostArgmin R epsCE 2 0 := by
  refine ⟨by omega, ?_, by intro j hj; omega⟩
  intro j hj
  have hj' : j = 0 ∨ j = 1 ∨ j = 2 := by omega
  rcases hj' with rfl | rfl | rfl
  · simp [phi, epsCE]
  · simp [phi, epsCE]; linarith
  · simp [phi, epsCE]; linarith

/-- **Counterexample to a bare iff.**  `d = (-2, -1)` is not discrete-convex,
yet the from-0 count equals the unique minimizer for every `R ≥ 0`. -/
theorem exists_nonconvex_count_exact :
    ¬ DiscreteConvexOn 2 epsCE ∧
      ∀ R, 0 ≤ R → IsLeftmostArgmin R epsCE 2 (count R epsCE 2) := by
  refine ⟨epsCE_not_convex, ?_⟩
  intro R hR
  rw [epsCE_count_zero hR]
  exact epsCE_zero_min hR

end N60Exact
