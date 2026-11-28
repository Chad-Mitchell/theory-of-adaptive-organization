import GTAO.Rnd.SelfRef.M11Blocks
open Matrix GTAORnd.SelfRef.LR3.M11Cube GTAORnd.SelfRef.LR3.M11Blocks

/-- Reviewer check: a linear map that maps a set onto itself maps its convex hull onto itself. -/
theorem img_hull {ι : Type*} [Fintype ι] [DecidableEq ι] (M : Matrix ι ι ℝ) (V : Set (ι → ℝ))
    (h : (fun x => M *ᵥ x) '' V = V) : (fun x => M *ᵥ x) '' convexHull ℝ V = convexHull ℝ V := by
  have := (Matrix.mulVecLin M).image_convexHull V
  have h' : ⇑(Matrix.mulVecLin M) '' V = V := h
  rw [h'] at this
  exact this

/-- the A-flip on block vertices -/
theorem flipA_pure {mA mB rA rB : ℕ} (bA : Fin mA → Fin rA) (bB : Fin mB → Fin rB) (i : Fin mA) :
    (fun x => diagonal (rowSign (mB := mB) i) *ᵥ x) '' pureSetB bA bB = pureSetB bA bB := by
  have key : ∀ v w, IsBlockVert bA v → IsBlockVert bB w →
      diagonal (rowSign (mB := mB) i) *ᵥ pureProd v w =
        pureProd (fun k => if k = i then -v k else v k) w ∧
      IsBlockVert bA (fun k => if k = i then -v k else v k) := by
    intro v w hv hw
    refine ⟨?_, ?_⟩
    · funext u
      rcases u with ⟨_ | a, o⟩ <;> simp [mulVec_diagonal, rowSign, pureProd, ext1] <;> split_ifs <;> simp_all
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

/-- so `S = conv(pureSetB)` satisfies `hfA` of `m11_blocks_polytope_flips` -/
example {mA mB rA rB : ℕ} (bA : Fin mA → Fin rA) (bB : Fin mB → Fin rB) (i : Fin mA) :
    (fun x => diagonal (rowSign (mB := mB) i) *ᵥ x) '' convexHull ℝ (pureSetB bA bB) =
      convexHull ℝ (pureSetB bA bB) := img_hull _ _ (flipA_pure bA bB i)
