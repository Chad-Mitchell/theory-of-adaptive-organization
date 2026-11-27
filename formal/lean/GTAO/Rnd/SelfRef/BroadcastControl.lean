/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost rounds 4–9: `theory/RECORD_COST_ROUNDS4-9_2026-11-25.md` §10, item L5
(copyable records are perfectly distinguishable). Lean round 3 of the side session; written in
a private Lake project (library `GTAORnd`, same Lean and Mathlib pins) and moved here with only
this header and the module lines changed.
-/
module

public import Mathlib
public import GTAO.Rnd.SelfRef.Broadcast

@[expose] public section

/-!
# Non-vacuity control for L5: a classical bit satisfies every hypothesis

`bitModel`: the n-fold composite has the deterministic states `Fin n → Fin 2`; every
non-negative normalized measurement and every map are allowed. All hypotheses of
`L5_perfect` hold for the two distinct states `0, 1` with the copier `s ↦ (s, s)`, and the
conclusion (perfect distinguishability) is non-trivial there. So the hypotheses are jointly
satisfiable with `x ≠ y`.
-/

namespace GTAORnd.SelfRef.LR3

open Finset CopyModel

/-- the classical bit with all non-negative normalized measurements and all maps -/
def bitModel : CopyModel where
  St n := Fin n → Fin 2
  Meas n ι _ := {m | (∀ i s, 0 ≤ m i s) ∧ ∀ s, ∑ i, m i s = 1}
  Chan _ _ := Set.univ
  prod n ω := fun j => ω j 0
  prod_one ω := by funext j; fin_cases j; rfl
  meas_sum hm s := hm.2 s
  chan_id _ := trivial
  chan_comp _ _ := trivial
  meas_pullback hM _ := ⟨fun i s => hM.1 i _, fun s => hM.2 _⟩
  prod_meas n e he := ⟨fun b s => ∏ j, e j (b j) (fun _ => s j),
    ⟨fun b s => Finset.prod_nonneg fun j _ => (he j).1 _ _, fun s => by
      have := Finset.prod_univ_sum (fun _ : Fin n => (Finset.univ : Finset (Fin 2)))
        (fun j c => e j c (fun _ => s j))
      rw [Fintype.piFinset_univ] at this
      rw [← this]
      exact Finset.prod_eq_one fun j _ => (he j).2 _⟩,
    fun b ω => by
      apply Finset.prod_congr rfl; intro j _
      congr 1; funext i; fin_cases i; rfl⟩
  local_ext n T _ := ⟨fun s => Fin.snoc (α := fun _ => Fin 2)
      (Fin.snoc (α := fun _ => Fin 2) (Fin.init s) (T (fun _ => s (Fin.last n)) 0))
      (T (fun _ => s (Fin.last n)) 1), trivial, fun ω a b h => by
      have hω : (fun _ : Fin 1 => (fun j => ω j 0 : Fin (n + 1) → Fin 2) (Fin.last n))
          = ω (Fin.last n) := by funext i; fin_cases i; rfl
      simp only [hω, h]
      funext j
      refine Fin.lastCases ?_ (fun j => ?_) j
      · simp
      · refine Fin.lastCases ?_ (fun j => ?_) j
        · simp
        · simp [Fin.init]⟩

/-- the two deterministic bit states -/
def b0 : bitModel.St 1 := fun _ => 0
def b1 : bitModel.St 1 := fun _ => 1

lemma b01 : b0 ≠ b1 := by
  intro h; have := congrFun h 0; simp [b0, b1] at this

theorem bit_coarseGrain : CoarseGrain bitModel := by
  intro n ι κ _ _ _ M d hM
  refine ⟨fun k s => Finset.sum_nonneg fun i _ => hM.1 i s, fun s => ?_⟩
  rw [Finset.sum_fiberwise_of_maps_to (g := d) (fun i _ => Finset.mem_univ _)]
  exact hM.2 s

theorem bit_nonNeg : NonNeg bitModel := fun hM i s => hM.1 i s

theorem bit_clones : bitModel.Clones 2 (fun s => fun _ => s 0) ![b0, b1] :=
  ⟨trivial, fun z => by fin_cases z <;> rfl⟩

/-- the measurement firing with probability `p` on `b0` and `q` on `b1` -/
def bitMeas (p q : ℝ) : Fin 2 → (Fin 1 → Fin 2) → ℝ :=
  fun i s => if i = 1 then (if s 0 = 0 then p else q) else (if s 0 = 0 then 1 - p else 1 - q)

theorem bit_achSet : achSet bitModel b0 b1 = Set.Icc 0 1 ×ˢ Set.Icc 0 1 := by
  ext ⟨p, q⟩
  simp only [achSet, Set.mem_prod, Set.mem_Icc]
  constructor
  · rintro ⟨m, hm, hp, hq⟩
    have h1 := ach_le_one bit_nonNeg hm b0
    have h2 := ach_le_one bit_nonNeg hm b1
    rw [hp] at h1; rw [hq] at h2
    exact ⟨h1, h2⟩
  · rintro ⟨⟨hp0, hp1⟩, ⟨hq0, hq1⟩⟩
    refine ⟨bitMeas p q, ⟨fun i s => ?_, fun s => ?_⟩, by simp [bitMeas, b0], ?_⟩
    · unfold bitMeas; split_ifs <;> linarith
    · simp only [bitMeas, Fin.sum_univ_two]
      split_ifs <;> simp_all
    · simp [bitMeas, b1]

theorem bit_closed : IsClosed (achSet bitModel b0 b1) := by
  rw [bit_achSet]; exact isClosed_Icc.prod isClosed_Icc

theorem bit_sep : ∃ m ∈ bitModel.Meas 1 (Fin 2), m 1 b0 ≠ m 1 b1 := by
  have h := (bit_achSet ▸ (show ((1 : ℝ), (0 : ℝ)) ∈ Set.Icc (0:ℝ) 1 ×ˢ Set.Icc (0:ℝ) 1 by
    simp)) 
  obtain ⟨m, hm, h1, h0⟩ := h
  exact ⟨m, hm, by simp at h1 h0; rw [h1, h0]; norm_num⟩

/-- **Control** (PROVED-IN-MODEL): every hypothesis of `L5_perfect` holds in `bitModel` for the
distinct states `b0`, `b1`, so `L5_perfect` applies non-vacuously. -/
theorem L5_control : bitModel.Distinguishable ![b0, b1] :=
  L5_perfect bit_coarseGrain bit_nonNeg bit_clones bit_sep bit_closed

end GTAORnd.SelfRef.LR3
