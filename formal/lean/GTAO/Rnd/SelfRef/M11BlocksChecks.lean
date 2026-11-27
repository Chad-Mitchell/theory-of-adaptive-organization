/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, Lean round 6: two checks written by the hostile reviewer of Lean round 5 in scratch files
(`sep_necessary`, the A-flip non-vacuity), moved here under new names with only this header, the
module lines and the docstrings changed.
-/
module

public import GTAO.Rnd.SelfRef.M11Blocks

@[expose] public section

/-!
# Two checks from the hostile review of Lean round 5 (Lean round 6)

Written by the round 5 reviewer in scratch files and moved here under new names (no committed theorem
renamed). `sep_necessary`: among diagonal symmetries, the separating condition of `diag_of_separating` is
necessary for that step (not for the conclusion of M11′). `flipA_pureSetB`, `flipA_hull_pureSetB`: the
A-side flips map `pureSetB` and `conv(pureSetB)` onto themselves, part of the symmetry hypotheses of
`m11_blocks_polytope_flips` for `S = conv(pureSetB)`; the B side, the coordinate permutations and the
other hypotheses are not stated here.
-/

namespace GTAORnd.SelfRef.LR3.M11Blocks

open Matrix GTAORnd.SelfRef.LR3.M11Cube

/-- if `d u * d v = 1`, the symmetric off-diagonal matrix `E_uv + E_vu` is invariant under
conjugation by `diag d`, so no diagonal family without a separating member forces a diagonal
invariant form (necessity for the Schur step only) -/
theorem sep_necessary {mA mB : ℕ} (u v : Idx mA mB) (huv : u ≠ v) (d : Idx mA mB → ℝ)
    (h : d u * d v = 1) :
    (diagonal d)ᵀ * (Matrix.single u v (1:ℝ) + Matrix.single v u 1) * diagonal d =
      Matrix.single u v 1 + Matrix.single v u 1 := by
  ext a b
  rw [diagonal_transpose, Matrix.mul_diagonal, Matrix.diagonal_mul]
  simp only [Matrix.add_apply, Matrix.single_apply]
  split_ifs <;> simp_all <;> nlinarith [mul_comm (d u) (d v)]

/-- a linear map that maps a set onto itself maps its convex hull onto itself. -/
theorem image_convexHull_of_image_eq {ι : Type*} [Fintype ι] [DecidableEq ι] (M : Matrix ι ι ℝ) (V : Set (ι → ℝ))
    (h : (fun x => M *ᵥ x) '' V = V) : (fun x => M *ᵥ x) '' convexHull ℝ V = convexHull ℝ V := by
  have := (Matrix.mulVecLin M).image_convexHull V
  have h' : ⇑(Matrix.mulVecLin M) '' V = V := h
  rw [h'] at this
  exact this

/-- the A-flip on block vertices -/
theorem flipA_pureSetB {mA mB rA rB : ℕ} (bA : Fin mA → Fin rA) (bB : Fin mB → Fin rB) (i : Fin mA) :
    (fun x => diagonal (rowSign (mB := mB) i) *ᵥ x) '' pureSetB bA bB = pureSetB bA bB := by
  have key : ∀ v w, IsBlockVert bA v → IsBlockVert bB w →
      diagonal (rowSign (mB := mB) i) *ᵥ pureProd v w =
        pureProd (fun k => if k = i then -v k else v k) w ∧
      IsBlockVert bA (fun k => if k = i then -v k else v k) := by
    intro v w hv hw
    refine ⟨?_, ?_⟩
    · funext u
      rcases u with ⟨_ | a, o⟩ <;> simp [mulVec_diagonal, rowSign, pureProd, ext1]
    · intro k
      obtain ⟨i0, σ, h0, hσ, hv'⟩ := hv k
      refine ⟨i0, if i0 = i then -σ else σ, h0, ?_, fun i' hi' => ?_⟩
      · split_ifs <;> rcases hσ with e | e <;> simp [e]
      · show (if i' = i then -v i' else v i') = _
        rw [hv' i' hi']; split_ifs <;> simp_all
  ext x; constructor
  · rintro ⟨_, ⟨v, w, hv, hw, rfl⟩, rfl⟩
    obtain ⟨e, hv2⟩ := key v w hv hw
    exact ⟨_, w, hv2, hw, e⟩
  · rintro ⟨v, w, hv, hw, rfl⟩
    obtain ⟨e, hv2⟩ := key (fun k => if k = i then -v k else v k) w (key v w hv hw).2 hw
    refine ⟨_, ⟨_, w, (key v w hv hw).2, hw, rfl⟩, ?_⟩
    show diagonal (rowSign (mB := mB) i) *ᵥ _ = _
    rw [e]; congr 1; funext k; split_ifs <;> simp

/-- `S = conv(pureSetB)` meets the A-flip hypothesis `hfA` of `m11_blocks_polytope_flips` -/
theorem flipA_hull_pureSetB {mA mB rA rB : ℕ} (bA : Fin mA → Fin rA) (bB : Fin mB → Fin rB)
    (i : Fin mA) :
    (fun x => diagonal (rowSign (mB := mB) i) *ᵥ x) '' convexHull ℝ (pureSetB bA bB) =
      convexHull ℝ (pureSetB bA bB) :=
  image_convexHull_of_image_eq _ _ (flipA_pureSetB bA bB i)

end GTAORnd.SelfRef.LR3.M11Blocks
