/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lean 4 formalization of the hull-increment identity in
`core/KEYSTONE_NOTE.md` §4, for OPEN_WORK T19.
-/
module

public import Mathlib.Algebra.BigOperators.Ring.Finset
public import Mathlib.Algebra.Order.BigOperators.Group.Finset
public import Mathlib.Algebra.Order.Archimedean.Real.Basic
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.Ring

/-!
# Hull-increment identity (KEYSTONE_NOTE §4)

For \(\varphi(K)=K+R(1+\varepsilon_K)\) on \(\{0,\ldots,n\}\), every
minimizer lies on the lower convex hull of the points \((K,\varepsilon_K)\).
When \(\varepsilon\) is discrete-convex, the adjacent N60 increment test
(from \(K=0\)) returns a leftmost minimizer.  The N60 count as written in
THEORY, \(K^*=1+\#\{k\ge 2:R(\varepsilon_{k-1}-\varepsilon_k)>1\}\), agrees
with that minimizer when the first step already pays, and is the known
\(K^*=0\) hole otherwise.

Convexity of \(\varepsilon_K\) in Model S remains an unproved hypothesis
(CORE §4) and is not claimed here.
-/

@[expose] public section

open Finset

/-- \(\varphi(K)=K+R(1+\varepsilon_K)\). -/
def phi (R : ℝ) (ε : ℕ → ℝ) (k : ℕ) : ℝ :=
  (k : ℝ) + R * (1 + ε k)

/-- A point \(k\in\{0,\ldots,n\}\) lies on the lower convex hull of
\(\{(i,\varepsilon_i):0\le i\le n\}\) when no convex combination of those
points with the same first coordinate sits strictly below \(\varepsilon_k\). -/
def OnLowerHull (n : ℕ) (ε : ℕ → ℝ) (k : ℕ) : Prop :=
  ∀ w : ℕ → ℝ,
    (∀ i ∈ range (n + 1), 0 ≤ w i) →
    (∑ i ∈ range (n + 1), w i) = 1 →
    (∑ i ∈ range (n + 1), w i * (i : ℝ)) = (k : ℝ) →
    ε k ≤ ∑ i ∈ range (n + 1), w i * ε i

lemma phi_sum (R : ℝ) (ε w : ℕ → ℝ) (n : ℕ) :
    ∑ i ∈ range (n + 1), w i * phi R ε i =
      ∑ i ∈ range (n + 1), w i * (i : ℝ) +
        R * ∑ i ∈ range (n + 1), w i +
        R * ∑ i ∈ range (n + 1), w i * ε i := by
  calc
    ∑ i ∈ range (n + 1), w i * phi R ε i
        = ∑ i ∈ range (n + 1), (w i * (i : ℝ) + w i * (R * (1 + ε i))) := by
          simp [phi, mul_add]
    _ = ∑ i ∈ range (n + 1), w i * (i : ℝ)
          + ∑ i ∈ range (n + 1), w i * (R * (1 + ε i)) := by
          simp [sum_add_distrib]
    _ = ∑ i ∈ range (n + 1), w i * (i : ℝ)
          + ∑ i ∈ range (n + 1), R * (w i * (1 + ε i)) := by
          congr 1; exact sum_congr rfl fun i _ => by ring
    _ = ∑ i ∈ range (n + 1), w i * (i : ℝ)
          + R * ∑ i ∈ range (n + 1), w i * (1 + ε i) := by
          simp [← mul_sum]
    _ = ∑ i ∈ range (n + 1), w i * (i : ℝ)
          + R * (∑ i ∈ range (n + 1), w i
            + ∑ i ∈ range (n + 1), w i * ε i) := by
          congr 2; simp [mul_add, sum_add_distrib]
    _ = ∑ i ∈ range (n + 1), w i * (i : ℝ) +
          R * ∑ i ∈ range (n + 1), w i +
          R * ∑ i ∈ range (n + 1), w i * ε i := by ring

/-- If a convex combination of `φ` values is strictly less than `φ k`, some
point in the support has a strictly smaller `φ`. -/
lemma exists_phi_lt_of_combo_lt (R : ℝ) (ε w : ℕ → ℝ) (n k : ℕ)
    (hw0 : ∀ i ∈ range (n + 1), 0 ≤ w i)
    (hwsum : (∑ i ∈ range (n + 1), w i) = 1)
    (hcombo : ∑ i ∈ range (n + 1), w i * phi R ε i < phi R ε k) :
    ∃ i ∈ range (n + 1), phi R ε i < phi R ε k := by
  by_contra hall
  push Not at hall
  have hge : phi R ε k ≤ ∑ i ∈ range (n + 1), w i * phi R ε i := by
    have : ∑ i ∈ range (n + 1), w i * phi R ε k
        ≤ ∑ i ∈ range (n + 1), w i * phi R ε i :=
      sum_le_sum fun i hi => mul_le_mul_of_nonneg_left (hall i hi) (hw0 i hi)
    have hcancel : ∑ i ∈ range (n + 1), w i * phi R ε k
        = (∑ i ∈ range (n + 1), w i) * phi R ε k := by
      simp [← sum_mul]
    simpa [hcancel, hwsum] using this
  exact not_lt_of_ge hge hcombo

lemma combo_of_zero {w : ℕ → ℝ} {n : ℕ}
    (hw0 : ∀ i ∈ range (n + 1), 0 ≤ w i)
    (hwsum : (∑ i ∈ range (n + 1), w i) = 1)
    (hwK : (∑ i ∈ range (n + 1), w i * (i : ℝ)) = 0) :
    w 0 = 1 ∧ ∀ i ∈ range (n + 1), 0 < i → w i = 0 := by
  have hnn : ∀ i ∈ range (n + 1), 0 ≤ w i * (i : ℝ) :=
    fun i hi => mul_nonneg (hw0 i hi) (Nat.cast_nonneg _)
  have hterm : ∀ i ∈ range (n + 1), w i * (i : ℝ) = 0 :=
    (sum_eq_zero_iff_of_nonneg hnn).mp hwK
  have hi0 : ∀ i ∈ range (n + 1), 0 < i → w i = 0 := by
    intro i hi hi0
    exact (mul_eq_zero.mp (hterm i hi)).resolve_right
      (Nat.cast_ne_zero.mpr hi0.ne')
  have h0mem : (0 : ℕ) ∈ range (n + 1) := by
    simp [mem_range]
  have : (∑ i ∈ range (n + 1), w i) = w 0 := by
    refine (sum_eq_single 0 ?_ ?_).trans (by simp)
    · intro i hi hne
      have : 0 < i := Nat.pos_of_ne_zero hne
      exact hi0 i hi this
    · intro h; exact (h h0mem).elim
  exact ⟨by linarith, hi0⟩

/-- KEYSTONE_NOTE §4: every minimizer of `φ` on `{0,…,n}` lies on the lower
convex hull of `{(K, ε_K)}`.  Needs `R ≥ 0`. -/
theorem minimizer_on_lower_hull (n : ℕ) (ε : ℕ → ℝ) {R : ℝ} (hR : 0 ≤ R)
    {k : ℕ} (hk : k ≤ n)
    (hmin : ∀ k' : ℕ, k' ≤ n → phi R ε k ≤ phi R ε k') :
    OnLowerHull n ε k := by
  intro w hw0 hwsum hwK
  rcases eq_or_lt_of_le hR with hR0 | hRpos
  · -- R = 0: the unique minimizer is k = 0, which is a hull vertex.
    have hk0 : k = 0 := by
      have hcmp := hmin 0 (Nat.zero_le _)
      have hR0' : R = 0 := hR0.symm
      have hphi0 : phi R ε 0 = 0 := by
        simp only [phi, hR0']; ring
      have hphik : phi R ε k = (k : ℝ) := by
        simp only [phi, hR0']; ring
      have : (k : ℝ) ≤ 0 := by
        rw [← hphik, ← hphi0]; exact hcmp
      exact Nat.cast_eq_zero.mp (le_antisymm this (Nat.cast_nonneg _))
    subst hk0
    have hzeros := combo_of_zero hw0 hwsum (by rw [hwK, Nat.cast_zero])
    have h0mem : (0 : ℕ) ∈ range (n + 1) := by simp [mem_range]
    have : ∑ i ∈ range (n + 1), w i * ε i = ε 0 := by
      refine (sum_eq_single 0 ?_ ?_).trans ?_
      · intro i hi hne
        have : 0 < i := Nat.pos_of_ne_zero hne
        rw [hzeros.2 i hi this, zero_mul]
      · intro h; exact (h h0mem).elim
      · rw [hzeros.1, one_mul]
    simp [this]
  · -- R > 0: a strictly lower combination of ε would strictly lower φ.
    by_contra h
    have hlt : ∑ i ∈ range (n + 1), w i * ε i < ε k := lt_of_not_ge h
    have hcombo : ∑ i ∈ range (n + 1), w i * phi R ε i < phi R ε k := by
      rw [phi_sum, hwK, hwsum]
      simp only [phi]
      have : R * (1 + ∑ i ∈ range (n + 1), w i * ε i) < R * (1 + ε k) :=
        mul_lt_mul_of_pos_left (by linarith) hRpos
      linarith
    obtain ⟨i, hi, hφ⟩ := exists_phi_lt_of_combo_lt R ε w n k hw0 hwsum hcombo
    have hi' : i ≤ n := Nat.lt_succ_iff.mp (mem_range.mp hi)
    exact (hmin i hi').not_gt hφ

/-- Discrete (midpoint) convexity of `ε` on `{0,…,n}`: first differences
are nondecreasing. -/
def DiscreteConvexOn (n : ℕ) (ε : ℕ → ℝ) : Prop :=
  ∀ k, 0 < k → k < n → ε k - ε (k - 1) ≤ ε (k + 1) - ε k

lemma DiscreteConvexOn.adjacent {n : ℕ} {ε : ℕ → ℝ}
    (h : DiscreteConvexOn n ε) {i : ℕ} (hi : i + 1 < n) :
    ε (i + 1) - ε i ≤ ε (i + 2) - ε (i + 1) := by
  simpa [Nat.add_sub_cancel] using h (i + 1) (Nat.succ_pos _) hi

lemma DiscreteConvexOn.mono_increment {n : ℕ} {ε : ℕ → ℝ}
    (h : DiscreteConvexOn n ε) {i j : ℕ}
    (_hi : i < n) (hj : j < n) (hij : i ≤ j) :
    ε (i + 1) - ε i ≤ ε (j + 1) - ε j := by
  obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hij
  induction d with
  | zero => simp
  | succ d ih =>
    have hj' : i + d < n := by omega
    have hadj := h.adjacent (i := i + d) (by omega)
    have ih' : ε (i + 1) - ε i ≤ ε (i + d + 1) - ε (i + d) := ih hj' (by omega)
    have heqL : ε (i + (d + 1)) = ε (i + d + 1) := rfl
    have heqR : ε (i + (d + 1) + 1) = ε (i + d + 2) := rfl
    have hadj' : ε (i + d + 1) - ε (i + d) ≤ ε (i + (d + 1) + 1) - ε (i + (d + 1)) := by
      simpa [heqL, heqR] using hadj
    linarith [ih']

/-- The adjacent increment from `k` to `k+1` pays when its marginal error
drop exceeds the upkeep, i.e. when `φ` strictly falls. -/
def IncrementPays (R : ℝ) (ε : ℕ → ℝ) (k : ℕ) : Prop :=
  1 < R * (ε k - ε (k + 1))

lemma incrementPays_iff (R : ℝ) (ε : ℕ → ℝ) (k : ℕ) :
    IncrementPays R ε k ↔ phi R ε (k + 1) < phi R ε k := by
  simp only [IncrementPays, phi, Nat.cast_succ]
  constructor <;> intro h <;> linarith

lemma phi_diff (R : ℝ) (ε : ℕ → ℝ) (k : ℕ) :
    phi R ε (k + 1) - phi R ε k = 1 + R * (ε (k + 1) - ε k) := by
  simp [phi]; ring

lemma DiscreteConvexOn.mono_phi_diff {n : ℕ} {ε : ℕ → ℝ}
    (h : DiscreteConvexOn n ε) {R : ℝ} (hR : 0 ≤ R) {i j : ℕ}
    (hi : i < n) (hj : j < n) (hij : i ≤ j) :
    phi R ε (i + 1) - phi R ε i ≤ phi R ε (j + 1) - phi R ε j := by
  have hε := h.mono_increment hi hj hij
  simp only [phi_diff]
  have : R * (ε (i + 1) - ε i) ≤ R * (ε (j + 1) - ε j) :=
    mul_le_mul_of_nonneg_left hε hR
  linarith

/-- Under discrete convexity, if a later adjacent step pays, an earlier one
pays too. -/
lemma DiscreteConvexOn.pays_of_later {n : ℕ} {ε : ℕ → ℝ}
    (h : DiscreteConvexOn n ε) {R : ℝ} (hR : 0 ≤ R) {i j : ℕ}
    (hi : i < n) (hj : j < n) (hij : i ≤ j)
    (hp : IncrementPays R ε j) : IncrementPays R ε i := by
  have hmono := h.mono_phi_diff hR hi hj hij
  rw [incrementPays_iff] at hp ⊢
  linarith

lemma phi_strict_decrease_chain (R : ℝ) (ε : ℕ → ℝ) {k : ℕ}
    (hBefore : ∀ i < k, IncrementPays R ε i) :
    ∀ i j, i < j → j ≤ k → phi R ε j < phi R ε i := by
  intro i j hij hjk
  induction j with
  | zero => cases hij
  | succ j ih =>
    have hij' : i ≤ j := Nat.lt_succ_iff.mp hij
    have hpay : phi R ε (j + 1) < phi R ε j :=
      (incrementPays_iff R ε j).mp (hBefore j (by omega))
    rcases eq_or_lt_of_le hij' with hieq | hilt
    · simpa [hieq] using hpay
    · have : phi R ε j < phi R ε i := ih hilt (by omega)
      linarith

lemma phi_nondecreasing_after {n : ℕ} {ε : ℕ → ℝ} {R : ℝ} {k : ℕ}
    (hconv : DiscreteConvexOn n ε) (hR : 0 ≤ R) (hk : k ≤ n)
    (hStop : k = n ∨ ¬ IncrementPays R ε k) :
    ∀ d, k + d ≤ n → phi R ε k ≤ phi R ε (k + d) := by
  intro d hd
  induction d with
  | zero => simp
  | succ d ih =>
    have hkd : k + d < n := by omega
    have hkn : k < n := by omega
    have hstep : phi R ε (k + d) ≤ phi R ε (k + d + 1) := by
      have hΔk : phi R ε k ≤ phi R ε (k + 1) := by
        rcases hStop with rfl | hnp
        · omega
        · rw [incrementPays_iff] at hnp
          exact le_of_not_gt hnp
      have hmono :=
        hconv.mono_phi_diff hR (i := k) (j := k + d) hkn hkd (by omega)
      linarith
    have ih' : phi R ε k ≤ phi R ε (k + d) := ih (by omega)
    have hassoc : k + (d + 1) = k + d + 1 := by ring
    rw [hassoc]
    linarith [ih', hstep]

/-- The N60-from-0 adjacent increment test: walk from `0` and take every
paying step.  Under discrete convexity this returns a leftmost minimizer
of `φ`. -/
theorem n60_from_zero_leftmost (n : ℕ) (ε : ℕ → ℝ) {R : ℝ} (hR : 0 ≤ R)
    (hconv : DiscreteConvexOn n ε) {k : ℕ} (hk : k ≤ n)
    (hBefore : ∀ i < k, IncrementPays R ε i)
    (hStop : k = n ∨ ¬ IncrementPays R ε k) :
    (∀ k' : ℕ, k' ≤ n → phi R ε k ≤ phi R ε k')
      ∧ ∀ k' < k, phi R ε k < phi R ε k' := by
  have h_strict : ∀ k' < k, phi R ε k < phi R ε k' :=
    fun k' hk' => phi_strict_decrease_chain R ε hBefore k' k hk' (le_rfl)
  have h_after := phi_nondecreasing_after hconv hR hk hStop
  refine ⟨?_, h_strict⟩
  intro k' hk'
  rcases le_or_gt k k' with hge | hlt
  · obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hge
    exact h_after d hk'
  · exact (h_strict k' hlt).le

/-- The known `K* = 0` hole: if the first step does not pay, then under
discrete convexity no later step pays, the true leftmost minimizer is `0`,
and N60 as written — `1 + #{k ≥ 2 : the step k-1 pays}` — equals `1`. -/
theorem n60_as_written_zero_hole (n : ℕ) (ε : ℕ → ℝ) {R : ℝ} (hR : 0 ≤ R)
    (hconv : DiscreteConvexOn n ε) (hnp : ¬ IncrementPays R ε 0) :
    (∀ k : ℕ, 2 ≤ k → k ≤ n → ¬ IncrementPays R ε (k - 1))
      ∧ ∀ k' : ℕ, k' ≤ n → phi R ε 0 ≤ phi R ε k' := by
  have hnone : ∀ i < n, ¬ IncrementPays R ε i := by
    intro i hi hp
    exact hnp (hconv.pays_of_later hR (Nat.zero_lt_of_lt hi) hi
      (Nat.zero_le _) hp)
  have hcount : ∀ k : ℕ, 2 ≤ k → k ≤ n → ¬ IncrementPays R ε (k - 1) := by
    intro k hk2 hkn hp
    have : k - 1 < n := by omega
    exact hnone (k - 1) this hp
  have hmin :=
    n60_from_zero_leftmost n ε hR hconv (k := 0) (Nat.zero_le _)
      (fun i hi => (Nat.not_lt_zero _ hi).elim) (Or.inr hnp)
  exact ⟨hcount, hmin.1⟩
