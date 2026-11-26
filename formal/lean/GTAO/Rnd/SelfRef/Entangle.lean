/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost: the side session's entanglement round (its note §5, Lean candidates LE0-LE5; a
repository note is pending). Lean round 3 of the side session; written in a private Lake project (library
`GTAORnd`, same Lean and Mathlib pins) and moved here with only this header, the module lines and the
namespace changed.
-/
module

public import Mathlib

@[expose] public section

/-!
# Entanglement round, Lean candidates LE0–LE5 (the side session's entanglement note, §5)
-/

namespace GTAORnd.SelfRef.LR3.Entangle

open Matrix

/-- **LE1, pure marginal ⇒ product, extreme-ray form** (PROVED-IN-MODEL). `Ω` is A's normalized
state space (convex, with unit functional `uA` equal to 1 on it — the normalization is written out
here); B's effects `f q` span `ℝ^dB` and a positive combination of them is the unit `uB`. If every
conditional `X f q` lies in the cone over `Ω` and the marginal `x = X uB` is an extreme point of
`Ω`, then `X = x yᵀ`. -/
theorem pure_marginal_extreme {dA dB l : ℕ} (Ω : Set (Fin dA → ℝ)) (hconv : Convex ℝ Ω)
    (uA : Fin dA → ℝ) (hnorm : ∀ w ∈ Ω, uA ⬝ᵥ w = 1)
    (f : Fin l → Fin dB → ℝ) (uB : Fin dB → ℝ) (lam : Fin l → ℝ) (hlam : ∀ q, 0 < lam q)
    (hunit : ∑ q, lam q • f q = uB)
    (hspan : ∀ v : Fin dB → ℝ, ∃ a : Fin l → ℝ, v = ∑ q, a q • f q)
    (X : Matrix (Fin dA) (Fin dB) ℝ)
    (hcone : ∀ q, ∃ c : ℝ, 0 ≤ c ∧ ∃ w ∈ Ω, X *ᵥ f q = c • w)
    (hext : X *ᵥ uB ∈ Ω.extremePoints ℝ) :
    ∃ y : Fin dB → ℝ, X = vecMulVec (X *ᵥ uB) y := by
  set x := X *ᵥ uB with hx
  choose c hc w hw hXf using hcone
  have hxsum : x = ∑ q, (lam q * c q) • w q := by
    rw [hx, ← hunit, mulVec_sum]
    refine Finset.sum_congr rfl fun q _ => ?_
    rw [mulVec_smul, hXf, smul_smul]
  have hμ0 : ∀ q, 0 ≤ lam q * c q := fun q => mul_nonneg (hlam q).le (hc q)
  have hμ1 : ∑ q, lam q * c q = 1 := by
    have hn : ∀ q, uA ⬝ᵥ w q = 1 := fun q => hnorm _ (hw q)
    have := congrArg (uA ⬝ᵥ ·) hxsum
    simp only [dotProduct_sum, dotProduct_smul, smul_eq_mul, hn, mul_one] at this
    rw [hnorm x hext.1] at this
    simpa using this.symm
  -- each conditional with positive weight is the marginal
  have hwq : ∀ q, 0 < lam q * c q → w q = x := by
    intro q hq
    by_cases h1 : lam q * c q = 1
    · have hothers : ∀ p ∈ Finset.univ.erase q, lam p * c p = 0 := by
        have hs := Finset.sum_erase_add Finset.univ (fun p => lam p * c p) (Finset.mem_univ q)
        rw [hμ1, h1] at hs
        have hz : ∑ p ∈ Finset.univ.erase q, lam p * c p = 0 := by linarith
        exact (Finset.sum_eq_zero_iff_of_nonneg (fun p _ => hμ0 p)).mp hz
      have : x = w q := by
        rw [hxsum, ← Finset.sum_erase_add _ _ (Finset.mem_univ q), h1, one_smul,
          Finset.sum_eq_zero (fun p hp => by rw [hothers p hp, zero_smul]), zero_add]
      exact this.symm
    · have hlt : lam q * c q < 1 := by
        have := Finset.single_le_sum (fun p _ => hμ0 p) (Finset.mem_univ q)
        rw [hμ1] at this; exact lt_of_le_of_ne this h1
      set t := lam q * c q
      set z := ∑ p ∈ Finset.univ.erase q, ((lam p * c p) / (1 - t)) • w p
      have hsum' : ∑ p ∈ Finset.univ.erase q, lam p * c p = 1 - t := by
        have hs := Finset.sum_erase_add Finset.univ (fun p => lam p * c p) (Finset.mem_univ q)
        rw [hμ1] at hs; simp only [t]; linarith
      have hz : z ∈ Ω := by
        apply hconv.sum_mem
        · intro p _; exact div_nonneg (hμ0 p) (by linarith)
        · rw [← Finset.sum_div, hsum']; field_simp [show (1 - t) ≠ 0 by linarith]
        · intro p _; exact hw p
      have hxz : x = t • w q + (1 - t) • z := by
        rw [hxsum, ← Finset.sum_erase_add _ _ (Finset.mem_univ q), add_comm]
        congr 1
        simp only [z, Finset.smul_sum, smul_smul]
        refine Finset.sum_congr rfl fun p _ => ?_
        congr 1; field_simp [show (1 - t) ≠ 0 by linarith]
      have hseg : x ∈ openSegment ℝ (w q) z :=
        ⟨t, 1 - t, hq, by linarith, by ring, hxz.symm⟩
      exact hext.2 (hw q) hz hseg
  -- so every X f q is a multiple of x
  have hXf' : ∀ q, X *ᵥ f q = c q • x := by
    intro q
    by_cases hcq : c q = 0
    · rw [hXf, hcq, zero_smul, zero_smul]
    · rw [hXf, hwq q (mul_pos (hlam q) (lt_of_le_of_ne (hc q) (Ne.symm hcq)))]
  choose a ha using fun j : Fin dB => hspan (Pi.single j 1)
  refine ⟨fun j => ∑ q, a j q * c q, ?_⟩
  ext i j
  have hcol : X *ᵥ Pi.single j 1 = (∑ q, a j q * c q) • x := by
    rw [ha j, mulVec_sum, Finset.sum_smul]
    refine Finset.sum_congr rfl fun q _ => ?_
    rw [mulVec_smul, hXf', smul_smul]
  have := congrFun hcol i
  simp [mulVec_single] at this
  simp [vecMulVec_apply, this, mul_comm]

/-- **LE2** (PROVED-IN-MODEL): a reversible map (a linear automorphism `T` with `T '' Ω = Ω`)
sends pure states (extreme points of `Ω`) exactly onto pure states. -/
theorem reversible_preserves_pure {V : Type*} [AddCommGroup V] [Module ℝ V]
    (T : V ≃ₗ[ℝ] V) (Ω : Set V) (hT : T '' Ω = Ω) :
    T '' (Ω.extremePoints ℝ) = Ω.extremePoints ℝ := by
  rw [image_extremePoints T Ω, hT]

/-- **LE0, two parts** (PROVED-IN-MODEL): local maps send pure tensors to pure tensors, and so
does the swap. -/
theorem local_map_tmul {V W V' W' : Type*} [AddCommGroup V] [Module ℝ V] [AddCommGroup W]
    [Module ℝ W] [AddCommGroup V'] [Module ℝ V'] [AddCommGroup W'] [Module ℝ W']
    (g : V →ₗ[ℝ] V') (h : W →ₗ[ℝ] W') (a : V) (b : W) :
    TensorProduct.map g h (a ⊗ₜ[ℝ] b) = g a ⊗ₜ[ℝ] h b := TensorProduct.map_tmul g h a b

theorem swap_tmul {V W : Type*} [AddCommGroup V] [Module ℝ V] [AddCommGroup W] [Module ℝ W]
    (a : V) (b : W) : TensorProduct.comm ℝ V W (a ⊗ₜ[ℝ] b) = b ⊗ₜ[ℝ] a :=
  TensorProduct.comm_tmul ℝ V W a b

/-- **LE0, n parts** (PROVED-IN-MODEL): the map `(⊗ g_i) ∘ P_σ` sends the pure tensor `⊗ ω_i`
to the pure tensor `⊗ g_i ω_{σ⁻¹ i}` (one system type `V`, so the permutation acts by reindexing). -/
theorem local_perm_tprod {n : ℕ} {V : Type*} [AddCommGroup V] [Module ℝ V]
    (σ : Equiv.Perm (Fin n)) (g : Fin n → V →ₗ[ℝ] V) (ω : Fin n → V) :
    PiTensorProduct.map g (PiTensorProduct.reindex ℝ (fun _ => V) σ (PiTensorProduct.tprod ℝ ω)) =
      PiTensorProduct.tprod ℝ (fun i => g i (ω (σ.symm i))) := by
  rw [PiTensorProduct.reindex_tprod, PiTensorProduct.map_tprod]

/-- the probability simplex on a finite type -/
def simplex (ι : Type*) [Fintype ι] : Set (ι → ℝ) := {p | (∀ i, 0 ≤ p i) ∧ ∑ i, p i = 1}

/-- **LE5 (classical control), part 1** (PROVED-IN-MODEL): the extreme points of the
probability simplex are exactly the deterministic states. -/
theorem simplex_extreme_iff {ι : Type*} [Fintype ι] [DecidableEq ι] (p : ι → ℝ) :
    p ∈ (simplex ι).extremePoints ℝ ↔ ∃ i, p = Pi.single i 1 := by
  constructor
  · rintro ⟨⟨hp0, hp1⟩, hext⟩
    obtain ⟨i, hi⟩ : ∃ i, 0 < p i := by
      by_contra h; push Not at h
      have : ∑ i, p i ≤ 0 := Finset.sum_nonpos fun i _ => h i
      linarith
    refine ⟨i, ?_⟩
    by_cases h1 : p i = 1
    · have hothers : ∀ j ∈ Finset.univ.erase i, p j = 0 := by
        have hs := Finset.sum_erase_add Finset.univ p (Finset.mem_univ i)
        rw [hp1, h1] at hs
        exact (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => hp0 j)).mp (by linarith)
      funext j
      by_cases hj : j = i
      · subst hj; simp [h1]
      · simp [hj, hothers j (Finset.mem_erase.mpr ⟨hj, Finset.mem_univ j⟩)]
    · exfalso
      have hlt : p i < 1 := by
        have := Finset.single_le_sum (fun j _ => hp0 j) (Finset.mem_univ i)
        rw [hp1] at this; exact lt_of_le_of_ne this h1
      set t := p i
      set q : ι → ℝ := fun j => (p j - t * (Pi.single i (1:ℝ) : ι → ℝ) j) / (1 - t)
      have hq : q ∈ simplex ι := by
        refine ⟨fun j => ?_, ?_⟩
        · apply div_nonneg _ (by linarith)
          by_cases hj : j = i
          · subst hj; simp [t]
          · simp [hj, hp0 j]
        · simp only [q, ← Finset.sum_div, Finset.sum_sub_distrib, ← Finset.mul_sum,
            Finset.sum_pi_single', Finset.mem_univ, ite_true, hp1, mul_one]
          field_simp [show (1 - t) ≠ 0 by linarith]
      have hd : (Pi.single i 1 : ι → ℝ) ∈ simplex ι := by
        refine ⟨fun j => ?_, by simp⟩
        by_cases hj : j = i
        · subst hj; simp
        · simp [hj]
      have hseg : p ∈ openSegment ℝ (Pi.single i 1) q := by
        refine ⟨t, 1 - t, hi, by linarith, by ring, ?_⟩
        funext j
        simp only [q, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
        field_simp [show (1 - t) ≠ 0 by linarith]
        ring
      have := hext hd hq hseg
      have := congrFun this i
      simp at this
      exact h1 this.symm
  · rintro ⟨i, rfl⟩
    have hd : (Pi.single i 1 : ι → ℝ) ∈ simplex ι := by
      refine ⟨fun j => ?_, by simp⟩
      by_cases hj : j = i
      · subst hj; simp
      · simp [hj]
    refine ⟨hd, fun x hx y hy hseg => ?_⟩
    obtain ⟨a, b, ha, hb, hab, hxy⟩ := hseg
    have hzero : ∀ z ∈ simplex ι, ∀ c : ℝ, 0 < c → ∀ z' ∈ simplex ι, ∀ c' : ℝ, 0 < c' →
        c • z + c' • z' = Pi.single i 1 → z = Pi.single i 1 := by
      intro z hz c hc z' hz' c' hc' he
      have hj : ∀ j, j ≠ i → z j = 0 := by
        intro j hj
        have := congrFun he j
        simp [hj] at this
        have h1 := hz.1 j; have h2 := hz'.1 j
        nlinarith [mul_nonneg hc.le h1, mul_nonneg hc'.le h2]
      have hzi : z i = 1 := by
        have hs := Finset.sum_erase_add Finset.univ z (Finset.mem_univ i)
        rw [hz.2, Finset.sum_eq_zero (fun k hk => hj k (Finset.ne_of_mem_erase hk))] at hs
        · linarith
      funext j
      by_cases h : j = i
      · subst h; simp [hzi]
      · simp [h, hj j h]
    exact hzero x hx a ha y hy b hb hxy

/-- **LE5, part 2** (PROVED-IN-MODEL): on `Fin m × Fin n`, every pure (deterministic) joint state
is a product `δ_i ⊗ δ_j`; a pure classical world contains no correlated pair. -/
theorem classical_pure_product {m n : ℕ} (p : Fin m × Fin n → ℝ)
    (hp : p ∈ (simplex (Fin m × Fin n)).extremePoints ℝ) :
    ∃ i j, ∀ a b, p (a, b) = (Pi.single i 1 : Fin m → ℝ) a * (Pi.single j 1 : Fin n → ℝ) b := by
  obtain ⟨⟨i, j⟩, rfl⟩ := (simplex_extreme_iff p).mp hp
  refine ⟨i, j, fun a b => ?_⟩
  by_cases ha : a = i <;> by_cases hb : b = j <;> simp [ha, hb, Prod.ext_iff]

/-- **LE4 (exact numbers)** (PROVED-IN-MODEL): with `∑ |β_i| ≤ 1/2`, the success
`1/2 + (1/3) ∑ β_i` is at most 2/3; and the value at `β = (1/2,1/2,1/2)` is 1. -/
theorem le4_bound (β : Fin 3 → ℚ) (h : ∑ i, |β i| ≤ 1 / 2) :
    ∑ i, β i ≤ 1 / 2 ∧ 1 / 2 + (1 / 3) * ∑ i, β i ≤ 2 / 3 := by
  have : ∑ i, β i ≤ ∑ i, |β i| := Finset.sum_le_sum fun i _ => le_abs_self (β i)
  constructor <;> linarith

theorem le4_attained : (1 / 2 : ℚ) + (1 / 3) * (3 / 2) = 1 := by norm_num

end GTAORnd.SelfRef.LR3.Entangle
