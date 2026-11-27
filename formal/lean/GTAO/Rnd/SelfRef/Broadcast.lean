/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost rounds 4–9: `theory/RECORD_COST_ROUNDS4-9_2026-11-25.md` §10, item L5
(copyable records are perfectly distinguishable). Lean round 3 of the side session; written in
a private Lake project (library `GTAORnd`, same Lean and Mathlib pins) and moved here with only
this header and the module lines changed.
-/
module

public import Mathlib
public import GTAO.Rnd.LemmaB1

@[expose] public section

/-!
# L5: copyable records are perfectly distinguishable (CopyModel form)

Setting: the `CopyModel` GPT of `LemmaB1.lean`, plus two standard GPT hypotheses passed as
explicit arguments (not new fields, so earlier theorems are untouched):
* `hcg` (classical post-processing): coarse-graining an allowed measurement along a decoding
  `d : ι → κ` gives an allowed measurement;
* `hnn` (probabilities): allowed measurement values are non-negative.

`Ach x y p q`: some allowed two-outcome measurement fires with probability `p` on `x`
and `q` on `y`. If one channel clones `x` and `y` (into 2 copies), `Ach` is closed under
products (measure both copies, accept iff both fire) and complements. AND/OR amplification
(`1 - (1 - p^k)^m`) then separates `x` from `y` to any accuracy (`L5_asymptotic`). If the
achievable set of value pairs is closed (true when the effect set is compact, e.g. any
finite-dimensional GPT with a closed effect cone), the separation is perfect (`L5_perfect`).
Over a cloned family: every two members that some measurement tells apart are perfectly
distinguishable (`L5_pairwise`).
-/

namespace GTAORnd.SelfRef.LR3

open Finset CopyModel

variable (G : CopyModel)

/-- classical post-processing (coarse-graining) of allowed measurements is allowed -/
def CoarseGrain : Prop :=
  ∀ {n : ℕ} {ι κ : Type} [Fintype ι] [Fintype κ] [DecidableEq κ] {M : ι → G.St n → ℝ}
    (d : ι → κ), M ∈ G.Meas n ι →
      (fun k s => ∑ i ∈ univ.filter (fun i => d i = k), M i s) ∈ G.Meas n κ

/-- allowed measurement values are non-negative -/
def NonNeg : Prop :=
  ∀ {n : ℕ} {ι : Type} [Fintype ι] {M : ι → G.St n → ℝ}, M ∈ G.Meas n ι → ∀ i s, 0 ≤ M i s

/-- achievable pair of firing probabilities on `x`, `y` -/
def Ach (x y : G.St 1) (p q : ℝ) : Prop :=
  ∃ m ∈ G.Meas 1 (Fin 2), m 1 x = p ∧ m 1 y = q

variable {G}

lemma ach_le_one (hnn : NonNeg G) {m : Fin 2 → G.St 1 → ℝ} (hm : m ∈ G.Meas 1 (Fin 2))
    (s : G.St 1) : 0 ≤ m 1 s ∧ m 1 s ≤ 1 := by
  have h := G.meas_sum hm s
  rw [Fin.sum_univ_two] at h
  exact ⟨hnn hm 1 s, by linarith [hnn hm 0 s]⟩

lemma ach_compl (hcg : CoarseGrain G) {x y : G.St 1} {p q : ℝ} (h : Ach G x y p q) :
    Ach G x y (1 - p) (1 - q) := by
  obtain ⟨m, hm, hp, hq⟩ := h
  refine ⟨_, hcg (fun i : Fin 2 => 1 - i) hm, ?_, ?_⟩
  · have := G.meas_sum hm x; rw [Fin.sum_univ_two] at this
    rw [← hp]; simp [Finset.sum_filter]; linarith
  · have := G.meas_sum hm y; rw [Fin.sum_univ_two] at this
    rw [← hq]; simp [Finset.sum_filter]; linarith

lemma ach_one (hcg : CoarseGrain G) {x y : G.St 1} {p q : ℝ} (h : Ach G x y p q) :
    Ach G x y 1 1 := by
  obtain ⟨m, hm, -, -⟩ := h
  refine ⟨_, hcg (fun _ : Fin 2 => (1 : Fin 2)) hm, ?_, ?_⟩ <;>
  · simp only
    exact G.meas_sum hm _

/-- products: with a 2-copy cloner of `x` and `y`, measuring both copies and accepting iff
both fire multiplies the firing probabilities. -/
lemma ach_mul (hcg : CoarseGrain G) {x y : G.St 1} {T : G.St 1 → G.St 2}
    (hT : G.Clones 2 T ![x, y]) {p q p' q' : ℝ} (h : Ach G x y p q) (h' : Ach G x y p' q') :
    Ach G x y (p * p') (q * q') := by
  obtain ⟨m, hm, hp, hq⟩ := h
  obtain ⟨m', hm', hp', hq'⟩ := h'
  obtain ⟨E, hE, hEp⟩ := G.prod_meas 2 ![m, m'] (by intro j; fin_cases j <;> assumption)
  have hF := G.meas_pullback hE hT.1
  let d : (Fin 2 → Fin 2) → Fin 2 := fun b => if b = ![1, 1] then 1 else 0
  refine ⟨_, hcg d hF, ?_, ?_⟩
  all_goals
    rw [Finset.sum_eq_single (![1, 1] : Fin 2 → Fin 2)]
    rotate_left
    · intro b hb hne; simp [d, hne] at hb
    · intro h; simp [d] at h
  · have := hT.2 0; simp only [Matrix.cons_val_zero] at this
    rw [this, hEp, Fin.prod_univ_two]; simp [hp, hp']
  · have := hT.2 1
    simp only [Matrix.cons_val_one, Matrix.cons_val_fin_one] at this
    rw [this, hEp, Fin.prod_univ_two]; simp [hq, hq']

lemma ach_pow (hcg : CoarseGrain G) {x y : G.St 1} {T : G.St 1 → G.St 2}
    (hT : G.Clones 2 T ![x, y]) {p q : ℝ} (h : Ach G x y p q) (k : ℕ) :
    Ach G x y (p ^ k) (q ^ k) := by
  induction k with
  | zero => simpa using ach_one hcg h
  | succ k ih => rw [pow_succ, pow_succ]; exact ach_mul hcg hT ih h

/-- AND of `k` then OR of `m`: `1 - (1 - p^k)^m` -/
lemma ach_andor (hcg : CoarseGrain G) {x y : G.St 1} {T : G.St 1 → G.St 2}
    (hT : G.Clones 2 T ![x, y]) {p q : ℝ} (h : Ach G x y p q) (k m : ℕ) :
    Ach G x y (1 - (1 - p ^ k) ^ m) (1 - (1 - q ^ k) ^ m) :=
  ach_compl hcg (ach_pow hcg hT (ach_compl hcg (ach_pow hcg hT h k)) m)

/-- `(1 - a)^m (1 + m a) ≤ 1` for `a ∈ [0,1]` -/
lemma pow_mul_bound (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) (m : ℕ) :
    (1 - a) ^ m * (1 + m * a) ≤ 1 := by
  have hb : 1 + m * a ≤ (1 + a) ^ m := one_add_mul_le_pow (by linarith) m
  have h1 : 0 ≤ (1 - a) ^ m := pow_nonneg (by linarith) m
  calc (1 - a) ^ m * (1 + m * a) ≤ (1 - a) ^ m * (1 + a) ^ m :=
        mul_le_mul_of_nonneg_left hb h1
    _ = (1 - a ^ 2) ^ m := by rw [← mul_pow]; ring
    _ ≤ 1 := pow_le_one₀ (by nlinarith) (by nlinarith)

/-- **Amplification (real analysis).** For `0 ≤ q < p ≤ 1` and `ε > 0` there are `k, m`
with `1 - (1-p^k)^m ≥ 1 - ε` and `1 - (1-q^k)^m ≤ ε`. -/
theorem amplify (p q ε : ℝ) (hq : 0 ≤ q) (hqp : q < p) (hp : p ≤ 1) (hε : 0 < ε) :
    ∃ k m : ℕ, 1 - ε ≤ 1 - (1 - p ^ k) ^ m ∧ 1 - (1 - q ^ k) ^ m ≤ ε := by
  have hp0 : 0 < p := lt_of_le_of_lt hq hqp
  set L : ℝ := 1 / ε with hL
  have hL0 : 0 < L := by positivity
  have hr : q / p < 1 := (div_lt_one hp0).mpr hqp
  have hr0 : 0 ≤ q / p := div_nonneg hq hp0.le
  obtain ⟨k1, hk1⟩ := exists_pow_lt_of_lt_one (by positivity : 0 < ε / (2 * L)) hr
  obtain ⟨k2, hk2⟩ := exists_pow_lt_of_lt_one (by positivity : 0 < ε / 2) (lt_of_lt_of_le hqp hp)
  set k := max k1 k2
  have hrk : (q / p) ^ k ≤ ε / (2 * L) :=
    le_trans (pow_le_pow_of_le_one hr0 hr.le (le_max_left _ _)) hk1.le
  have hqk : q ^ k ≤ ε / 2 :=
    le_trans (pow_le_pow_of_le_one hq (by linarith) (le_max_right _ _)) hk2.le
  have hpk0 : 0 < p ^ k := pow_pos hp0 k
  have hpk1 : p ^ k ≤ 1 := pow_le_one₀ hp0.le hp
  set m := ⌈L / p ^ k⌉₊
  have hm1 : L / p ^ k ≤ m := Nat.le_ceil _
  have hm2 : (m : ℝ) < L / p ^ k + 1 := Nat.ceil_lt_add_one (by positivity)
  refine ⟨k, m, ?_, ?_⟩
  · -- (1 - p^k)^m ≤ 1/(1+L) ≤ ε
    have hb := pow_mul_bound (p ^ k) hpk0.le hpk1 m
    have hmL : L ≤ m * p ^ k := by rwa [div_le_iff₀ hpk0] at hm1
    have hpos : 0 ≤ (1 - p ^ k) ^ m := pow_nonneg (by linarith) m
    have : (1 - p ^ k) ^ m * (1 + L) ≤ 1 := by nlinarith
    have hε' : (1 - p ^ k) ^ m ≤ ε := by
      have h1L : 1 / ε < 1 + L := by rw [← hL]; linarith
      have : (1 - p ^ k) ^ m * (1 / ε) < 1 := by nlinarith
      rw [mul_one_div, div_lt_one hε] at this; linarith
    linarith
  · -- 1 - (1 - q^k)^m ≤ m q^k ≤ L (q/p)^k + q^k ≤ ε
    have hqk0 : 0 ≤ q ^ k := pow_nonneg hq k
    have hbern : 1 - m * q ^ k ≤ (1 - q ^ k) ^ m := by
      have := one_add_mul_le_pow (a := -q ^ k) (by nlinarith [pow_le_one₀ hq (show q ≤ 1 by linarith) (n := k)]) m
      simpa [sub_eq_add_neg, mul_neg] using this
    have hmq : (m : ℝ) * q ^ k ≤ L * (q / p) ^ k + q ^ k := by
      have : (m : ℝ) * q ^ k ≤ (L / p ^ k + 1) * q ^ k := mul_le_mul_of_nonneg_right hm2.le hqk0
      rw [div_pow]; calc (m : ℝ) * q ^ k ≤ (L / p ^ k + 1) * q ^ k := this
        _ = L * (q ^ k / p ^ k) + q ^ k := by field_simp
    have hLr : L * (q / p) ^ k ≤ ε / 2 := by
      calc L * (q / p) ^ k ≤ L * (ε / (2 * L)) := mul_le_mul_of_nonneg_left hrk hL0.le
        _ = ε / 2 := by field_simp
    linarith

/-- **L5, asymptotic form** (PROVED-IN-MODEL). In a `CopyModel` with coarse-graining and
non-negative probabilities, if one allowed channel clones `x` and `y` into two copies and some
allowed two-outcome measurement gives them different firing probabilities, then for every
`ε > 0` an allowed two-outcome measurement fires on `x` with probability `≥ 1 - ε` and on `y`
with probability `≤ ε`. -/
theorem L5_asymptotic (hcg : CoarseGrain G) (hnn : NonNeg G) {x y : G.St 1}
    {T : G.St 1 → G.St 2} (hT : G.Clones 2 T ![x, y])
    (hsep : ∃ m ∈ G.Meas 1 (Fin 2), m 1 x ≠ m 1 y) (ε : ℝ) (hε : 0 < ε) :
    ∃ m ∈ G.Meas 1 (Fin 2), 1 - ε ≤ m 1 x ∧ m 1 y ≤ ε := by
  obtain ⟨m, hm, hne⟩ := hsep
  -- orient so that p > q
  obtain ⟨p, q, hach, hqp⟩ : ∃ p q, Ach G x y p q ∧ q < p := by
    rcases lt_or_gt_of_ne hne with h | h
    · exact ⟨1 - m 1 x, 1 - m 1 y, ach_compl hcg ⟨m, hm, rfl, rfl⟩, by linarith⟩
    · exact ⟨m 1 x, m 1 y, ⟨m, hm, rfl, rfl⟩, h⟩
  have hb : 0 ≤ q ∧ p ≤ 1 := by
    obtain ⟨m', hm', hp, hq⟩ := hach
    exact ⟨hq ▸ (ach_le_one hnn hm' y).1, hp ▸ (ach_le_one hnn hm' x).2⟩
  obtain ⟨k, n, h1, h2⟩ := amplify p q ε hb.1 hqp hb.2 hε
  obtain ⟨m', hm', hp', hq'⟩ := ach_andor hcg hT hach k n
  exact ⟨m', hm', hp' ▸ h1, hq' ▸ h2⟩

/-- the set of achievable firing-probability pairs on `(x, y)` -/
def achSet (G : CopyModel) (x y : G.St 1) : Set (ℝ × ℝ) := {pq | Ach G x y pq.1 pq.2}

/-- **L5, perfect form** (PROVED-IN-MODEL). If moreover the achievable set of pairs is closed,
then `x` and `y` are perfectly distinguishable (`Distinguishable ![x, y]` of `LemmaB1.lean`). -/
theorem L5_perfect (hcg : CoarseGrain G) (hnn : NonNeg G) {x y : G.St 1}
    {T : G.St 1 → G.St 2} (hT : G.Clones 2 T ![x, y])
    (hsep : ∃ m ∈ G.Meas 1 (Fin 2), m 1 x ≠ m 1 y) (hclosed : IsClosed (achSet G x y)) :
    G.Distinguishable ![x, y] := by
  have hmem : ((1 : ℝ), (0 : ℝ)) ∈ achSet G x y := by
    apply hclosed.closure_subset
    rw [Metric.mem_closure_iff]
    intro ε hε
    obtain ⟨m, hm, h1, h2⟩ := L5_asymptotic hcg hnn hT hsep (ε / 2) (by linarith)
    refine ⟨(m 1 x, m 1 y), ⟨m, hm, rfl, rfl⟩, ?_⟩
    have hx := ach_le_one hnn hm x
    have hy := ach_le_one hnn hm y
    rw [Prod.dist_eq, Real.dist_eq, Real.dist_eq]
    apply max_lt
    · rw [abs_lt]; constructor <;> linarith
    · rw [abs_lt]; constructor <;> linarith
  obtain ⟨m, hm, h1, h0⟩ := hmem
  refine ⟨Fin 2, inferInstance, m, fun i => 1 - i, hm, ?_⟩
  have hs : ∀ s, m 0 s + m 1 s = 1 := fun s => by
    have := G.meas_sum hm s; rwa [Fin.sum_univ_two] at this
  intro j
  fin_cases j
  · simp [Finset.sum_filter]; simp at h1; linarith [hs x]
  · simp [Finset.sum_filter]; simp at h0; linarith [hs y]

/-- **L5, pairwise form** (PROVED-IN-MODEL). If one allowed channel clones a whole family
`ω` into two copies, measurements separate states (tomography), and each pair's achievable set
is closed, then any two distinct members are perfectly distinguishable. -/
theorem L5_pairwise (hcg : CoarseGrain G) (hnn : NonNeg G) {M : ℕ} (ω : Fin M → G.St 1)
    {T : G.St 1 → G.St 2} (hT : G.Clones 2 T ω)
    (htomo : ∀ a b : G.St 1, (∀ m ∈ G.Meas 1 (Fin 2), m 1 a = m 1 b) → a = b)
    (hclosed : ∀ a b : G.St 1, IsClosed (achSet G a b)) :
    ∀ i j, ω i ≠ ω j → G.Distinguishable ![ω i, ω j] := by
  intro i j hij
  have hT2 : G.Clones 2 T ![ω i, ω j] := ⟨hT.1, fun z => by fin_cases z <;> simp [hT.2]⟩
  have hsep : ∃ m ∈ G.Meas 1 (Fin 2), m 1 (ω i) ≠ m 1 (ω j) := by
    by_contra h; push Not at h; exact hij (htomo _ _ h)
  exact L5_perfect hcg hnn hT2 hsep (hclosed _ _)

end GTAORnd.SelfRef.LR3
