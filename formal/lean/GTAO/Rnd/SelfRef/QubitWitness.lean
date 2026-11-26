/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost: `theory/RECORD_COST_CHAIN_2026-11-25.md` step S2 (a Lean witness that the qubit
ball attains `d = N + 1`). Lean round 3 of the side session; written in a private Lake
project (library `GTAORnd`, same Lean and Mathlib pins) and moved here with only this header
and the module lines changed.
-/
module

public import Mathlib
public import GTAO.Rnd.SelfRef.DimBound

@[expose] public section

/-!
# The qubit ball meets the bound `d ≥ N + 1` with equality

`dim_bound` (R3): a preconnected set of linear isometries containing the identity and a
non-identity map, all fixing `N` affinely independent points, forces `finrank ≥ N + 1`.
Witness: `V = ℝ³` (the qubit ball's affine span, `d = 3`), the two poles `±e₃` (`N = 2`, a
one-bit record), and the rotations about the `e₃` axis (a continuous drift). Every hypothesis
of `dim_bound` holds and `finrank ℝ V = 3 = N + 1`, so the bound is attained.
-/

namespace GTAORnd.SelfRef.LR3

open GTAORnd.SelfRef Real

local notation "V3" => EuclideanSpace ℝ (Fin 3)

/-- rotation by `θ` about the third axis -/
noncomputable def rotL (θ : ℝ) : V3 →ₗ[ℝ] V3 where
  toFun v := !₂[cos θ * v 0 - sin θ * v 1, sin θ * v 0 + cos θ * v 1, v 2]
  map_add' x y := by
    ext i; fin_cases i <;> simp <;> ring
  map_smul' c x := by
    ext i; fin_cases i <;> simp <;> ring

/-- as a continuous linear map -/
noncomputable def rotZ (θ : ℝ) : V3 →L[ℝ] V3 := LinearMap.toContinuousLinearMap (rotL θ)

lemma rotZ_apply (θ : ℝ) (v : V3) :
    rotZ θ v = !₂[cos θ * v 0 - sin θ * v 1, sin θ * v 0 + cos θ * v 1, v 2] := rfl

/-- the north pole `e₃` -/
noncomputable def north : V3 := !₂[0, 0, 1]

lemma rotZ_iso (θ : ℝ) (v : V3) : ‖rotZ θ v‖ = ‖v‖ := by
  rw [EuclideanSpace.norm_eq, EuclideanSpace.norm_eq, rotZ_apply]
  congr 1
  simp only [Fin.sum_univ_three, Real.norm_eq_abs, sq_abs]
  simp
  have := sin_sq_add_cos_sq θ
  linear_combination (v 0 ^ 2 + v 1 ^ 2) * this

lemma rotZ_zero : rotZ 0 = ContinuousLinearMap.id ℝ V3 := by
  ext v i; fin_cases i <;> simp [rotZ_apply]

lemma rotZ_fix_north (θ : ℝ) : rotZ θ north = north := by
  ext i; fin_cases i <;> simp [rotZ_apply, north]

lemma rotZ_fix_south (θ : ℝ) : rotZ θ (-north) = -north := by
  rw [map_neg, rotZ_fix_north]

lemma rotZ_cont : Continuous rotZ := by
  rw [continuous_clm_apply]
  intro v
  simp only [rotZ_apply]
  apply (EuclideanSpace.equiv (Fin 3) ℝ).symm.continuous.comp
  apply continuous_pi
  intro i; fin_cases i <;> simp <;> fun_prop

/-- **The qubit attains `d = N + 1`** (PROVED-IN-MODEL): every hypothesis of `dim_bound` holds
for the poles `±e₃` of ℝ³ under the rotations about `e₃`, and `finrank ℝ ℝ³ = (1 + 1) + 1`. -/
theorem qubit_attains_bound :
    let p : Fin 2 → V3 := ![north, -north]
    let S : Set (V3 →L[ℝ] V3) := Set.range rotZ
    AffineIndependent ℝ p ∧ IsPreconnected S ∧ ContinuousLinearMap.id ℝ V3 ∈ S ∧
    (∀ g ∈ S, ∀ x, ‖g x‖ = ‖x‖) ∧ (∀ g ∈ S, ∀ i, g (p i) = p i) ∧
    (∃ g ∈ S, g ≠ ContinuousLinearMap.id ℝ V3) ∧ Module.finrank ℝ V3 = (1 + 1) + 1 := by
  intro p S
  have hns : north ≠ -north := by
    intro h; have := congrArg (fun w : V3 => w 2) h; simp [north] at this; linarith
  refine ⟨?_, isPreconnected_range rotZ_cont, ⟨0, rotZ_zero⟩, ?_, ?_, ?_, ?_⟩
  · exact affineIndependent_of_ne ℝ hns
  · rintro _ ⟨θ, rfl⟩ x; exact rotZ_iso θ x
  · rintro _ ⟨θ, rfl⟩ i; fin_cases i
    · exact rotZ_fix_north θ
    · exact rotZ_fix_south θ
  · refine ⟨rotZ π, ⟨π, rfl⟩, fun h => ?_⟩
    have := congrArg (fun g : V3 →L[ℝ] V3 => (g !₂[1, 0, 0]) 0) h
    simp [rotZ_apply] at this; linarith
  · simp

/-- consequently `dim_bound` applies to this witness and its bound `3 ≤ finrank` is an
equality -/
theorem qubit_bound_tight :
    3 ≤ Module.finrank ℝ V3 ∧ Module.finrank ℝ V3 = 3 := by
  obtain ⟨hp, hS, hid, hiso, hfix, hnt, hd⟩ := qubit_attains_bound
  exact ⟨dim_bound_one_bit _ hp _ hS hid hiso hfix hnt, by rw [hd]⟩

end GTAORnd.SelfRef.LR3
