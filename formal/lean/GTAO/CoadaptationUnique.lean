/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Uniqueness of the stationary law for CA1, by irreducibility of a finite
chain (the Perron–Frobenius step named in `theory/COADAPTATION.md`).
Mathlib 4.37 does not prove the spectral Perron–Frobenius theorem; this
file uses the elementary max-ratio argument for a finite irreducible
stochastic matrix, then uniformization.  For OPEN_WORK T19.
-/
module

public import GTAO.Coadaptation
public import Mathlib.Algebra.Order.Star.Real
public import Mathlib.Data.Finset.Max
public import Mathlib.Algebra.BigOperators.Group.Finset.Basic
public import Mathlib.Algebra.BigOperators.Ring.Finset
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.Positivity
public import Mathlib.Tactic.Ring

/-!
# CA1 uniqueness (finite irreducible chain)

`theory/COADAPTATION.md` Theorem CA1: on connected party move graphs the
joint chain has a unique stationary distribution `π > 0` (by
irreducibility).  This file proves that uniqueness for a finite
irreducible row-stochastic matrix (max-ratio), transfers it to a
continuous-time chain by uniformization, records that the Cartesian
product of connected party graphs is connected, and identifies the
unique stationary probability of a log-linear chain with an exact
potential as the normalized Gibbs law `exp(−Ψ) / ∑ exp(−Ψ)`, independent
of the clocks.

Inputs disclosed: finiteness of the joint state space; irreducibility of
the move graph (which follows from connectedness of each party's graph);
a uniformization rate strictly larger than every exit rate.
-/

@[expose] public section

set_option linter.unusedSectionVars false

open Finset Function Real

namespace Coadaptation

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- A nonnegative row-stochastic matrix. -/
def IsRowStochastic (P : n → n → ℝ) : Prop :=
  (∀ i j, 0 ≤ P i j) ∧ (∀ i, ∑ j, P i j = 1)

/-- A probability vector invariant under `P`. -/
def IsStationaryProb (P : n → n → ℝ) (π : n → ℝ) : Prop :=
  (∀ i, 0 ≤ π i) ∧ (∑ i, π i = 1) ∧ (∀ j, ∑ i, π i * P i j = π j)

/-- The directed graph of strictly positive entries is strongly connected. -/
def IsIrreducibleStochastic (P : n → n → ℝ) : Prop :=
  ∀ i j, Relation.ReflTransGen (fun a b => 0 < P a b) i j

/-- If a nonnegative path-closed function is positive at one vertex of an
irreducible chain, it is positive everywhere. -/
theorem stationary_pos {P : n → n → ℝ} {π : n → ℝ}
    (hP : IsRowStochastic P) (hirr : IsIrreducibleStochastic P)
    (hnonneg : ∀ i, 0 ≤ π i) (hinv : ∀ j, ∑ i, π i * P i j = π j)
    (hnz : ∃ i, 0 < π i) (i : n) : 0 < π i := by
  classical
  obtain ⟨i0, hi0⟩ := hnz
  have hclosed : ∀ a b, 0 < π a → 0 < P a b → 0 < π b := by
    intro a b ha hab
    have hterm : ∀ k, 0 ≤ π k * P k b := fun k => mul_nonneg (hnonneg k) (hP.1 k b)
    have hle : π a * P a b ≤ ∑ k, π k * P k b :=
      Finset.single_le_sum (fun k _ => hterm k) (mem_univ a)
    have hpos : 0 < π a * P a b := mul_pos ha hab
    have : 0 < ∑ k, π k * P k b := lt_of_lt_of_le hpos hle
    rwa [hinv b] at this
  have hpath : ∀ {a b}, Relation.ReflTransGen (fun x y => 0 < P x y) a b →
      0 < π a → 0 < π b := by
    intro a b h
    induction h with
    | refl => exact id
    | tail _ hab ih =>
      intro ha
      exact hclosed _ _ (ih ha) hab
  exact hpath (hirr i0 i) hi0

/-- A first edge from the complement of `S` into `S` along a path. -/
lemma exists_edge_into {α : Type*} {r : α → α → Prop} (S : α → Prop)
    {a b : α} (h : Relation.ReflTransGen r a b) :
    ¬ S a → S b → ∃ x y, r x y ∧ ¬ S x ∧ S y := by
  induction h with
  | refl =>
    intro ha hb
    exact (ha hb).elim
  | @tail c d _hcd hcd ih =>
    intro ha hd
    by_cases hc : S c
    · exact ih ha hc
    · exact ⟨c, d, hcd, hc, hd⟩

/-- **Uniqueness for a finite irreducible stochastic matrix.**  Two
stationary probabilities coincide (max-ratio argument). -/
theorem unique_stationary_prob [Nonempty n] {P : n → n → ℝ} {π σ : n → ℝ}
    (hP : IsRowStochastic P) (hirr : IsIrreducibleStochastic P)
    (hπ : IsStationaryProb P π) (hσ : IsStationaryProb P σ) : π = σ := by
  classical
  have hσex : ∃ i, 0 < σ i := by
    by_contra h
    push Not at h
    have hz : ∀ i, σ i = 0 := fun i => le_antisymm (h i) (hσ.1 i)
    have hsum : (∑ i, σ i) = 0 := by
      simp_rw [hz]
      exact sum_const_zero
    have : (1 : ℝ) = 0 := hσ.2.1.symm.trans hsum
    exact zero_ne_one this.symm
  have hσpos : ∀ i, 0 < σ i := fun i =>
    stationary_pos hP hirr hσ.1 hσ.2.2 hσex i
  obtain ⟨i0, -, hi0max⟩ :=
    (univ : Finset n).exists_max_image (fun i => π i * (σ i)⁻¹) univ_nonempty
  set M := π i0 * (σ i0)⁻¹
  have hle : ∀ i, π i * (σ i)⁻¹ ≤ M := fun i => hi0max i (mem_univ i)
  have hle' : ∀ i, π i ≤ M * σ i := by
    intro i
    have hcomm : (σ i)⁻¹ * π i ≤ M := by
      rw [mul_comm]; exact hle i
    have : π i ≤ σ i * M := (inv_mul_le_iff₀ (hσpos i)).mp hcomm
    rw [mul_comm]; exact this
  have hMeq : ∀ {j}, π j * (σ j)⁻¹ = M → π j = M * σ j := by
    intro j hj
    have hne : σ j ≠ 0 := (hσpos j).ne'
    have : π j * ((σ j)⁻¹ * σ j) = M * σ j := by
      rw [← mul_assoc, hj]
    rwa [inv_mul_cancel₀ hne, mul_one] at this
  have hclosed : ∀ i j, π j * (σ j)⁻¹ = M → 0 < P i j → π i * (σ i)⁻¹ = M := by
    intro i j hj hij
    have hπj : π j = M * σ j := hMeq hj
    have hinvj : (∑ k, π k * P k j) = π j := hπ.2.2 j
    have hterm : ∀ k, π k * P k j ≤ (M * σ k) * P k j := fun k =>
      mul_le_mul_of_nonneg_right (hle' k) (hP.1 k j)
    have hsumle : (∑ k, π k * P k j) ≤ ∑ k, (M * σ k) * P k j :=
      sum_le_sum fun k _ => hterm k
    have hσinv : (∑ k, σ k * P k j) = σ j := hσ.2.2 j
    have hrhs : (∑ k, (M * σ k) * P k j) = M * σ j := by
      have : (∑ k, (M * σ k) * P k j) = M * ∑ k, σ k * P k j := by
        simp_rw [mul_assoc]
        exact (mul_sum univ (fun k => σ k * P k j) M).symm
      rw [this, hσinv]
    have hsumeq : (∑ k, π k * P k j) = ∑ k, (M * σ k) * P k j := by
      apply le_antisymm hsumle
      rw [hinvj, hπj, hrhs]
    have hdiff : (∑ k, ((M * σ k) * P k j - π k * P k j)) = 0 := by
      rw [sum_sub_distrib, hsumeq, sub_self]
    have hnn : ∀ k, 0 ≤ (M * σ k) * P k j - π k * P k j := fun k =>
      sub_nonneg.mpr (hterm k)
    have hzero : (M * σ i) * P i j - π i * P i j = 0 :=
      (sum_eq_zero_iff_of_nonneg (fun k _ => hnn k)).1 hdiff i (mem_univ i)
    have hfact : (M * σ i - π i) * P i j = 0 := by
      convert hzero using 1
      ring
    have : M * σ i - π i = 0 :=
      (mul_eq_zero.mp hfact).resolve_right hij.ne'
    have hπi : π i = M * σ i := by linarith
    have : π i * (σ i)⁻¹ = M := by
      have hcancel : M * σ i * (σ i)⁻¹ = M := by
        rw [mul_assoc, mul_inv_cancel₀ (hσpos i).ne', mul_one]
      rw [hπi, hcancel]
    exact this
  have hconst : ∀ i, π i * (σ i)⁻¹ = M := by
    by_contra h
    push Not at h
    obtain ⟨k, hk⟩ := h
    obtain ⟨x, y, hPxy, hx, hy⟩ :=
      exists_edge_into (fun i => π i * (σ i)⁻¹ = M) (hirr k i0) hk rfl
    exact hx (hclosed x y hy hPxy)
  have hπσ : ∀ i, π i = M * σ i := fun i => hMeq (hconst i)
  have hM : M = 1 := by
    have hsum : (∑ i, π i) = M * ∑ i, σ i := by
      have : (∑ i, π i) = ∑ i, M * σ i := sum_congr rfl fun i _ => hπσ i
      rw [this, ← mul_sum]
    have hπ1 : (∑ i, π i) = 1 := hπ.2.1
    have hσ1 : (∑ i, σ i) = 1 := hσ.2.1
    have hM1 : (1 : ℝ) = M * 1 := by
      calc
        (1 : ℝ) = ∑ i, π i := hπ1.symm
        _ = M * ∑ i, σ i := hsum
        _ = M * 1 := by rw [hσ1]
    linarith
  funext i
  rw [hπσ i, hM, one_mul]

/-- Exit rate at `i`, ignoring any self-loop. -/
noncomputable def exitRate (q : n → n → ℝ) (i : n) : ℝ :=
  ∑ j, if i = j then (0 : ℝ) else q i j

/-- Uniformization of a rate matrix at rate `lam`. -/
noncomputable def uniformize (q : n → n → ℝ) (lam : ℝ) : n → n → ℝ :=
  fun i j => if i = j then 1 - exitRate q i * lam⁻¹ else q i j * lam⁻¹

lemma exitRate_eq_erase (q : n → n → ℝ) (i : n) :
    exitRate q i = ∑ j ∈ univ.erase i, q i j := by
  classical
  unfold exitRate
  have hsplit := add_sum_erase (univ : Finset n)
    (fun j => if i = j then (0 : ℝ) else q i j) (mem_univ i)
  have hii : (if i = i then (0 : ℝ) else q i i) = 0 := ite_eq_left rfl
  have hoff : (∑ j ∈ univ.erase i, if i = j then (0 : ℝ) else q i j) =
      ∑ j ∈ univ.erase i, q i j :=
    sum_congr rfl fun j hj => ite_eq_right (ne_of_mem_erase hj).symm
  calc
    (∑ j, if i = j then (0 : ℝ) else q i j)
        = (if i = i then (0 : ℝ) else q i i) +
            ∑ j ∈ univ.erase i, if i = j then (0 : ℝ) else q i j := hsplit.symm
    _ = 0 + ∑ j ∈ univ.erase i, q i j := by rw [hii, hoff]
    _ = ∑ j ∈ univ.erase i, q i j := zero_add _

lemma uniformize_row_sum (q : n → n → ℝ) (lam : ℝ) (i : n) :
    ∑ j, uniformize q lam i j = 1 := by
  classical
  have hsplit := add_sum_erase (univ : Finset n) (uniformize q lam i) (mem_univ i)
  have hdiag : uniformize q lam i i = 1 - exitRate q i * lam⁻¹ := ite_eq_left rfl
  have hoff : (∑ j ∈ univ.erase i, uniformize q lam i j) =
      ∑ j ∈ univ.erase i, q i j * lam⁻¹ :=
    sum_congr rfl fun j hj => ite_eq_right (ne_of_mem_erase hj).symm
  have hmul : (∑ j ∈ univ.erase i, q i j * lam⁻¹) =
      (∑ j ∈ univ.erase i, q i j) * lam⁻¹ := (sum_mul _ _ _).symm
  calc
    (∑ j, uniformize q lam i j)
        = uniformize q lam i i + ∑ j ∈ univ.erase i, uniformize q lam i j :=
          hsplit.symm
    _ = (1 - exitRate q i * lam⁻¹) + (∑ j ∈ univ.erase i, q i j) * lam⁻¹ := by
          rw [hdiag, hoff, hmul]
    _ = (1 - exitRate q i * lam⁻¹) + exitRate q i * lam⁻¹ := by
          rw [← exitRate_eq_erase]
    _ = 1 := by ring

/-- Off-diagonal global balance for a continuous-time chain. -/
def IsGlobalBalance (q : n → n → ℝ) (π : n → ℝ) : Prop :=
  ∀ j, (∑ i, if i = j then (0 : ℝ) else π i * q i j) = π j * exitRate q j

lemma global_balance_of_detailed {q : n → n → ℝ} {π : n → ℝ}
    (hdb : ∀ x y, π x * q x y = π y * q y x) :
    (∀ x, ∑ y, π y * q y x = ∑ y, π x * q x y) :=
  fun x => sum_congr rfl fun y _ => (hdb x y).symm

lemma sum_offdiag_eq_erase (f : n → ℝ) (x : n) :
    (∑ i, if i = x then (0 : ℝ) else f i) = ∑ i ∈ univ.erase x, f i := by
  classical
  have hsplit := add_sum_erase (univ : Finset n)
    (fun i => if i = x then (0 : ℝ) else f i) (mem_univ x)
  have hxx : (if x = x then (0 : ℝ) else f x) = 0 := ite_eq_left rfl
  have hoff : (∑ i ∈ univ.erase x, if i = x then (0 : ℝ) else f i) =
      ∑ i ∈ univ.erase x, f i :=
    sum_congr rfl fun i hi => ite_eq_right (ne_of_mem_erase hi)
  calc
    (∑ i, if i = x then (0 : ℝ) else f i)
        = (if x = x then (0 : ℝ) else f x) +
            ∑ i ∈ univ.erase x, if i = x then (0 : ℝ) else f i := hsplit.symm
    _ = 0 + ∑ i ∈ univ.erase x, f i := by rw [hxx, hoff]
    _ = ∑ i ∈ univ.erase x, f i := zero_add _

lemma sum_split_at (f : n → ℝ) (x : n) :
    (∑ y, f y) = f x + ∑ y ∈ univ.erase x, f y := by
  classical
  exact (add_sum_erase (univ : Finset n) f (mem_univ x)).symm

lemma IsGlobalBalance_of_inflow {q : n → n → ℝ} {π : n → ℝ}
    (h : ∀ x, ∑ y, π y * q y x = ∑ y, π x * q x y) :
    IsGlobalBalance q π := by
  classical
  intro x
  have hL := sum_split_at (fun y => π y * q y x) x
  have hR : (∑ y, π x * q x y) = π x * q x x + π x * exitRate q x := by
    rw [sum_split_at (fun y => π x * q x y) x, exitRate_eq_erase, mul_sum]
  have hoff := sum_offdiag_eq_erase (fun i => π i * q i x) x
  have := h x
  linarith

lemma inflow_of_IsGlobalBalance {q : n → n → ℝ} {π : n → ℝ}
    (h : IsGlobalBalance q π) :
    ∀ x, ∑ y, π y * q y x = ∑ y, π x * q x y := by
  classical
  intro x
  have hL := sum_split_at (fun y => π y * q y x) x
  have hR : (∑ y, π x * q x y) = π x * q x x + π x * exitRate q x := by
    rw [sum_split_at (fun y => π x * q x y) x, exitRate_eq_erase, mul_sum]
  have hoff := sum_offdiag_eq_erase (fun i => π i * q i x) x
  have := h x
  linarith

lemma uniformize_invariant {q : n → n → ℝ} {lam : ℝ} {π : n → ℝ} (j : n) :
    (∑ i, π i * uniformize q lam i j) - π j =
      lam⁻¹ * ((∑ i, if i = j then (0 : ℝ) else π i * q i j) - π j * exitRate q j) := by
  classical
  have hdiag : uniformize q lam j j = 1 - exitRate q j * lam⁻¹ := ite_eq_left rfl
  have hsplit := add_sum_erase (univ : Finset n)
    (fun i => π i * uniformize q lam i j) (mem_univ j)
  have hoff : (∑ i ∈ univ.erase j, π i * uniformize q lam i j) =
      ∑ i ∈ univ.erase j, π i * (q i j * lam⁻¹) :=
    sum_congr rfl fun i hi => by
      have hne : i ≠ j := ne_of_mem_erase hi
      have hP : uniformize q lam i j = q i j * lam⁻¹ := ite_eq_right hne
      rw [hP]
  have hmul : (∑ i ∈ univ.erase j, π i * (q i j * lam⁻¹)) =
      lam⁻¹ * ∑ i ∈ univ.erase j, π i * q i j := by
    have : (∑ i ∈ univ.erase j, π i * (q i j * lam⁻¹)) =
        (∑ i ∈ univ.erase j, π i * q i j) * lam⁻¹ := by
      have hassoc : ∀ i, π i * (q i j * lam⁻¹) = (π i * q i j) * lam⁻¹ :=
        fun i => (mul_assoc (π i) (q i j) lam⁻¹).symm
      rw [sum_congr rfl (fun i _ => hassoc i)]
      exact (sum_mul (univ.erase j) (fun i => π i * q i j) lam⁻¹).symm
    rw [this, mul_comm]
  have hoff' := sum_offdiag_eq_erase (fun i => π i * q i j) j
  have hsum : (∑ i, π i * uniformize q lam i j) =
      π j * (1 - exitRate q j * lam⁻¹) +
        lam⁻¹ * ∑ i ∈ univ.erase j, π i * q i j := by
    calc
      (∑ i, π i * uniformize q lam i j)
          = π j * uniformize q lam j j +
              ∑ i ∈ univ.erase j, π i * uniformize q lam i j := hsplit.symm
      _ = π j * (1 - exitRate q j * lam⁻¹) +
            ∑ i ∈ univ.erase j, π i * (q i j * lam⁻¹) := by
            rw [hdiag, hoff]
      _ = π j * (1 - exitRate q j * lam⁻¹) +
            lam⁻¹ * ∑ i ∈ univ.erase j, π i * q i j := by rw [hmul]
  rw [hsum, hoff']
  ring

theorem uniformize_stationary {q : n → n → ℝ} {lam π}
    (hlam : lam ≠ 0) :
    (∀ j, ∑ i, π i * uniformize q lam i j = π j) ↔ IsGlobalBalance q π := by
  constructor
  · intro hinv j
    have hid := uniformize_invariant (q := q) (lam := lam) (π := π) j
    have h0 : (∑ i, π i * uniformize q lam i j) - π j = 0 := by
      rw [hinv j, sub_self]
    have hmul0 : lam⁻¹ * ((∑ i, if i = j then (0 : ℝ) else π i * q i j) -
        π j * exitRate q j) = 0 := by
      rw [← hid, h0]
    have hlam' : (lam⁻¹ : ℝ) ≠ 0 := inv_ne_zero hlam
    have hparen := (mul_eq_zero.mp hmul0).resolve_left hlam'
    linarith
  · intro hgb j
    have hid := uniformize_invariant (q := q) (lam := lam) (π := π) j
    have hz : (∑ i, if i = j then (0 : ℝ) else π i * q i j) - π j * exitRate q j = 0 := by
      rw [hgb j, sub_self]
    have : (∑ i, π i * uniformize q lam i j) - π j = 0 := by
      rw [hid, hz, mul_zero]
    linarith

/-- A convenient uniformization rate: one plus the sum of exit rates. -/
noncomputable def unifRate (q : n → n → ℝ) : ℝ :=
  (∑ i, exitRate q i) + 1

lemma unifRate_pos {q : n → n → ℝ} (hq : ∀ i, 0 ≤ exitRate q i) :
    0 < unifRate q := by
  have : (0 : ℝ) ≤ ∑ i, exitRate q i := sum_nonneg fun i _ => hq i
  simp only [unifRate]
  linarith

lemma unifRate_gt_exit {q : n → n → ℝ} (hq : ∀ i, 0 ≤ exitRate q i) (i : n) :
    exitRate q i < unifRate q := by
  have hle : exitRate q i ≤ ∑ j, exitRate q j :=
    single_le_sum (fun j _ => hq j) (mem_univ i)
  simp only [unifRate]
  linarith

lemma exitRate_nonneg {q : n → n → ℝ} (hq : ∀ i j, i ≠ j → 0 ≤ q i j) (i : n) :
    0 ≤ exitRate q i :=
  sum_nonneg fun j _ => by
    split_ifs
    · exact le_rfl
    · exact hq i j ‹_›

lemma uniformize_stochastic {q : n → n → ℝ} {lam : ℝ}
    (hq : ∀ i j, i ≠ j → 0 ≤ q i j) (hlam : 0 < lam)
    (hexit : ∀ i, exitRate q i < lam) :
    IsRowStochastic (uniformize q lam) := by
  refine ⟨?_, fun i => uniformize_row_sum q lam i⟩
  intro i j
  classical
  by_cases hij : i = j
  · subst hij
    have : 0 ≤ 1 - exitRate q i * lam⁻¹ := by
      have h1 : exitRate q i * lam⁻¹ < 1 := by
        have := hexit i
        have : exitRate q i < lam * 1 := by simpa using this
        exact (mul_inv_lt_iff₀ hlam).mpr (by linarith)
      linarith
    have hdiag : uniformize q lam i i = 1 - exitRate q i * lam⁻¹ := ite_eq_left rfl
    rwa [hdiag]
  · have : 0 ≤ q i j * lam⁻¹ :=
      mul_nonneg (hq i j hij) (inv_nonneg.mpr hlam.le)
    have hoff : uniformize q lam i j = q i j * lam⁻¹ := ite_eq_right hij
    rwa [hoff]

theorem unique_global_balance [Nonempty n] {q : n → n → ℝ} {π σ : n → ℝ}
    {lam : ℝ} (hq : ∀ i j, i ≠ j → 0 ≤ q i j) (hlam : 0 < lam)
    (hexit : ∀ i, exitRate q i < lam)
    (hirr : IsIrreducibleStochastic (uniformize q lam))
    (hπ : (∀ i, 0 ≤ π i) ∧ (∑ i, π i = 1) ∧ IsGlobalBalance q π)
    (hσ : (∀ i, 0 ≤ σ i) ∧ (∑ i, σ i = 1) ∧ IsGlobalBalance q σ) :
    π = σ := by
  have hP : IsRowStochastic (uniformize q lam) :=
    uniformize_stochastic hq hlam hexit
  have hne : lam ≠ 0 := hlam.ne'
  have hπs : IsStationaryProb (uniformize q lam) π :=
    ⟨hπ.1, hπ.2.1, (uniformize_stationary hne).mpr hπ.2.2⟩
  have hσs : IsStationaryProb (uniformize q lam) σ :=
    ⟨hσ.1, hσ.2.1, (uniformize_stationary hne).mpr hσ.2.2⟩
  exact unique_stationary_prob hP hirr hπs hσs

variable {ι : Type*} [DecidableEq ι] {S : ι → Type*}
variable {G : ∀ i, S i → S i → Prop} {β : ι → ℝ}
  {J : ι → (∀ i, S i) → ℝ} {q : (∀ i, S i) → (∀ i, S i) → ℝ}

lemma isMove_path_one_party {x : ∀ i, S i} {i : ι} {a b : S i}
    (h : Relation.ReflTransGen (G i) a b) :
    Relation.ReflTransGen (IsMove G) (update x i a) (update x i b) := by
  induction h with
  | refl => exact Relation.ReflTransGen.refl
  | @tail c d _hac hcd ih =>
    refine ih.tail ?_
    refine ⟨i, d, ?_, ?_⟩
    · simpa [update_self] using hcd
    · simp [update_idem]

lemma isMove_path_to_update {x : ∀ i, S i} {i : ι} {s : S i}
    (h : Relation.ReflTransGen (G i) (x i) s) :
    Relation.ReflTransGen (IsMove G) x (update x i s) := by
  have hx : update x i (x i) = x := update_eq_self i x
  have hpath := isMove_path_one_party (x := x) h
  rwa [hx] at hpath

/-- The Cartesian product of connected party graphs is connected under
single-party moves. -/
theorem joint_connected [Fintype ι]
    (hconn : ∀ i a b, Relation.ReflTransGen (G i) a b)
    (x y : ∀ i, S i) :
    Relation.ReflTransGen (IsMove G) x y := by
  classical
  have go : ∀ t : Finset ι, ∃ z,
      (∀ i ∈ t, z i = y i) ∧ (∀ i ∉ t, z i = x i) ∧
        Relation.ReflTransGen (IsMove G) x z := by
    intro t
    induction t using Finset.induction with
    | empty =>
      exact ⟨x, by simp, by simp, Relation.ReflTransGen.refl⟩
    | @insert i s hi ih =>
      obtain ⟨z, hz_in, hz_out, hzpath⟩ := ih
      have hzi : z i = x i := hz_out i (by simp [hi])
      have hpathi : Relation.ReflTransGen (G i) (z i) (y i) := by
        rw [hzi]; exact hconn i (x i) (y i)
      refine ⟨update z i (y i), ?_, ?_, hzpath.trans (isMove_path_to_update hpathi)⟩
      · intro j hj
        rcases mem_insert.mp hj with hji | hjs
        · subst hji; simp
        · have hji : j ≠ i := fun h => hi (h ▸ hjs)
          simp [update_of_ne hji, hz_in j hjs]
      · intro j hj
        have hji : j ≠ i := fun h => hj (by simp [h])
        have hjs : j ∉ s := fun h => hj (mem_insert_of_mem h)
        simp [update_of_ne hji, hz_out j hjs]
  obtain ⟨z, hin, _, hpath⟩ := go (univ : Finset ι)
  have hz : z = y := funext fun i => hin i (mem_univ i)
  rwa [hz] at hpath

/-- Normalized Gibbs law for a potential `Ψ`. -/
noncomputable def gibbsProb [Fintype (∀ i, S i)] (Ψ : (∀ i, S i) → ℝ)
    (x : ∀ i, S i) : ℝ :=
  exp (-Ψ x) * (∑ y : ∀ i, S i, exp (-Ψ y))⁻¹

lemma gibbsProb_Z_pos [Fintype (∀ i, S i)] [Nonempty (∀ i, S i)]
    (Ψ : (∀ i, S i) → ℝ) :
    0 < ∑ y : ∀ i, S i, exp (-Ψ y) := by
  obtain ⟨x0⟩ := ‹Nonempty (∀ i, S i)›
  have hterm : 0 < exp (-Ψ x0) := exp_pos _
  have hle : exp (-Ψ x0) ≤ ∑ y : ∀ i, S i, exp (-Ψ y) :=
    single_le_sum (fun y _ => (exp_pos (-Ψ y)).le) (mem_univ x0)
  exact lt_of_lt_of_le hterm hle

lemma gibbsProb_pos [Fintype (∀ i, S i)] [Nonempty (∀ i, S i)]
    (Ψ : (∀ i, S i) → ℝ) (x : ∀ i, S i) : 0 < gibbsProb Ψ x :=
  mul_pos (exp_pos _) (inv_pos.mpr (gibbsProb_Z_pos Ψ))

lemma gibbsProb_nonneg [Fintype (∀ i, S i)] [Nonempty (∀ i, S i)]
    (Ψ : (∀ i, S i) → ℝ) (x : ∀ i, S i) : 0 ≤ gibbsProb Ψ x :=
  (gibbsProb_pos Ψ x).le

lemma gibbsProb_sum [Fintype (∀ i, S i)] [Nonempty (∀ i, S i)]
    (Ψ : (∀ i, S i) → ℝ) :
    ∑ x, gibbsProb Ψ x = 1 := by
  simp only [gibbsProb]
  rw [← sum_mul, mul_inv_cancel₀ (gibbsProb_Z_pos Ψ).ne']

lemma detailedBalance_gibbsProb (hC : LogLinearChain G β J q)
    {Ψ : (∀ i, S i) → ℝ} (hΨ : IsExactPotential β J Ψ)
    [Fintype (∀ i, S i)] :
    DetailedBalance q (gibbsProb Ψ) := by
  intro x y
  have hdb := detailedBalance_of_potential hC hΨ x y
  simp only [gibbsProb]
  have : exp (-Ψ x) * (∑ z, exp (-Ψ z))⁻¹ * q x y =
      exp (-Ψ y) * (∑ z, exp (-Ψ z))⁻¹ * q y x := by
    have h := hdb
    -- multiply both sides of π₀ x * q x y = π₀ y * q y x by Z⁻¹
    have := congrArg (fun t => t * (∑ z, exp (-Ψ z))⁻¹) h
    convert this using 1 <;> ring
  exact this

lemma q_nonneg (hC : LogLinearChain G β J q) (x y : ∀ i, S i) : 0 ≤ q x y := by
  by_cases hm : IsMove G x y
  · obtain ⟨i, s, hG, rfl⟩ := hm
    exact (hC.pos x i s hG).le
  · rw [hC.zero x y hm]

lemma isMove_imp_q_pos (hC : LogLinearChain G β J q) {x y : ∀ i, S i}
    (h : IsMove G x y) : 0 < q x y := by
  obtain ⟨i, s, hG, rfl⟩ := h
  exact hC.pos x i s hG

lemma uniformize_irreducible
    [Fintype ι] [∀ i, Fintype (S i)] [DecidableEq (∀ i, S i)]
    (hC : LogLinearChain G β J q)
    (hconn : ∀ i a b, Relation.ReflTransGen (G i) a b) {lam : ℝ}
    (hlam : 0 < lam) :
    IsIrreducibleStochastic (n := ∀ i, S i) (uniformize q lam) := by
  intro x y
  have hpath := joint_connected (G := G) hconn x y
  induction hpath with
  | refl => exact Relation.ReflTransGen.refl
  | @tail z w _hz hab ih =>
    classical
    by_cases heq : z = w
    · subst heq
      exact ih
    · have hq : 0 < q z w := isMove_imp_q_pos hC hab
      have hform : uniformize q lam z w = q z w * lam⁻¹ := ite_eq_right heq
      have hP : 0 < uniformize q lam z w := by
        have : 0 < q z w * lam⁻¹ := mul_pos hq (inv_pos.mpr hlam)
        rwa [hform]
      exact ih.tail hP

/-- **CA1 uniqueness.**  On connected party move graphs, a log-linear chain
has at most one stationary probability (global balance).  If the game has
an exact potential `Ψ`, that unique law is the normalized Gibbs weight
`exp(−Ψ)/∑ exp(−Ψ)`, independent of the clocks. -/
theorem unique_gibbs_stationary
    [Fintype ι] [∀ i, Fintype (S i)] [DecidableEq (∀ i, S i)]
    [Nonempty (∀ i, S i)]
    (hC : LogLinearChain G β J q)
    (hconn : ∀ i a b, Relation.ReflTransGen (G i) a b)
    {Ψ : (∀ i, S i) → ℝ} (hΨ : IsExactPotential β J Ψ)
    {π : (∀ i, S i) → ℝ}
    (hπ : (∀ x, 0 ≤ π x) ∧ (∑ x, π x = 1) ∧
      ∀ x, ∑ y, π y * q y x = ∑ y, π x * q x y) :
    π = gibbsProb Ψ := by
  classical
  have hq : ∀ x y : ∀ i, S i, x ≠ y → 0 ≤ q x y := fun x y _ => q_nonneg hC x y
  have hexit_nn : ∀ x, 0 ≤ exitRate (n := ∀ i, S i) q x :=
    fun x => exitRate_nonneg hq x
  set lam := unifRate (n := ∀ i, S i) q
  have hlam : 0 < lam := unifRate_pos hexit_nn
  have hexit : ∀ x, exitRate (n := ∀ i, S i) q x < lam :=
    fun x => unifRate_gt_exit hexit_nn x
  have hirr : IsIrreducibleStochastic (n := ∀ i, S i) (uniformize q lam) :=
    uniformize_irreducible hC hconn hlam
  have hπgb : IsGlobalBalance (n := ∀ i, S i) q π :=
    IsGlobalBalance_of_inflow hπ.2.2
  have hγgb : IsGlobalBalance (n := ∀ i, S i) q (gibbsProb Ψ) :=
    IsGlobalBalance_of_inflow
      (global_balance_of_detailed (detailedBalance_gibbsProb hC hΨ))
  refine unique_global_balance (n := ∀ i, S i) hq hlam hexit hirr
    ⟨hπ.1, hπ.2.1, hπgb⟩
    ⟨gibbsProb_nonneg Ψ, gibbsProb_sum Ψ, hγgb⟩

end Coadaptation
