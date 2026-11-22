/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lean 4 formalization of Lemma L1 of `theory/LAYER_CONVEXITY.md` (PR #145):
the N60 increment count equals the leftmost argmin for every stake ratio iff
the decrements are non-increasing.  For OPEN_WORK T19.
-/
module

public import GTAO.Hull
public import Mathlib.Data.Finset.Card
public import Mathlib.Order.Interval.Finset.Nat

/-!
# L1: when the N60 count is exact

On `{0,…,n}` with `φ(K) = K + R(1 + ε_K)`, the N60 count from `0` is the
number of paying adjacent steps,
`count R = #{i < n : 1 < R (ε_i - ε_{i+1})}`
(equivalently `#{K ∈ [1,n] : R d_K > 1}` with `d_K = ε_{K-1} - ε_K`).

* `count_isLeftmostArgmin`: if the decrements are non-increasing
  (`DiscreteConvexOn n ε`) and `R ≥ 0`, `count R` is the leftmost minimizer.
* `exists_R_count_not_argmin`: if the step decrements are positive and
  pairwise distinct and some decrement rises (`d_m < d_{m+1}`), there is an
  `R > 0` at which `count R` is not a minimizer at all.
* `count_exact_iff_convex`: with positive, distinct decrements, the count is
  the leftmost argmin for every `R > 0` iff the decrements are non-increasing.
-/

@[expose] public section

open Finset

namespace N60Exact

/-- The N60 count from `0`: the number of paying adjacent steps. -/
noncomputable def count (R : ℝ) (ε : ℕ → ℝ) (n : ℕ) : ℕ := by
  classical exact ((range n).filter (fun i => IncrementPays R ε i)).card

/-- `k` is the leftmost minimizer of `φ` on `{0,…,n}`. -/
def IsLeftmostArgmin (R : ℝ) (ε : ℕ → ℝ) (n k : ℕ) : Prop :=
  k ≤ n ∧ (∀ j ≤ n, phi R ε k ≤ phi R ε j) ∧ ∀ j < k, phi R ε k < phi R ε j

/-- **L1 (⇒).**  Non-increasing decrements and `R ≥ 0`: the N60 count is the
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

/-- Positive, pairwise distinct step decrements realize every count: for every
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

/-- **L1 (⇐).**  If the step decrements `g i = ε_i - ε_{i+1}` (`i < n`) are
positive and pairwise distinct and some decrement rises
(`g j < g (j+1)`, `j + 2 ≤ n`), then for some `R > 0` the N60 count is not a
minimizer of `φ` (so in particular not the leftmost argmin). -/
theorem exists_R_count_not_argmin {n : ℕ} {ε : ℕ → ℝ}
    (hpos : ∀ i < n, 0 < ε i - ε (i + 1))
    (hdist : ∀ i < n, ∀ i' < n, i ≠ i' → ε i - ε (i + 1) ≠ ε i' - ε (i' + 1))
    {j : ℕ} (hj : j + 2 ≤ n) (hrise : ε j - ε (j + 1) < ε (j + 1) - ε (j + 2)) :
    ∃ R, 0 < R ∧ ∃ k ≤ n, phi R ε k < phi R ε (count R ε n) := by
  classical
  obtain ⟨i0, hi0, hcard⟩ := exists_threshold (fun i => ε i - ε (i + 1)) hdist
    (c := j + 1) (by omega)
  have hg0 := hpos i0 hi0
  refine ⟨1 / (ε i0 - ε (i0 + 1)), by positivity, ?_⟩
  have hcount : count (1 / (ε i0 - ε (i0 + 1))) ε n = j + 1 := by
    rw [← hcard]; unfold count; congr 1
    apply filter_congr
    intro k _
    unfold IncrementPays
    rw [one_div, inv_mul_eq_div, one_lt_div hg0]
  rw [hcount]
  exact not_min_of_rise (by positivity) hj hrise

/-- **L1 (iff).**  With positive, pairwise distinct step decrements, the N60
count is the leftmost argmin for every `R > 0` iff the decrements are
non-increasing. -/
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
    obtain ⟨R, hR, k', hk', hlt⟩ := exists_R_count_not_argmin hpos hdist (by omega) hrise
    exact absurd ((h R hR).2.1 k' hk') (not_le.mpr hlt)
  · intro hconv R hR
    exact count_isLeftmostArgmin hR.le hconv

end N60Exact
