import Mathlib

/-! Least action against the cost of judgment, class PATH (theory/least-action-2026-11-27).
Two finite statements behind DERIVATION.md §2:
* `discrete_heat_ge`: an n-step open-loop protocol with steps `d i` (each of duration dt) has
  drag heat `γ/dt * ∑ d i ^ 2` at least `γ/dt * (∑ d i)^2 / n`: equal steps (the free-particle path) are optimal.
* `terminal_gap`: with a terminal stake, the window cost of a constant velocity `v` exceeds its value at
  `vstar = w (x1 - x0) / (γ + w τ)` by exactly `(γ τ + w τ²)(v - vstar)²`. -/

theorem sq_sum_le_card_mul_sum_sq' (n : ℕ) (d : Fin n → ℝ) :
    (∑ i, d i) ^ 2 ≤ (n : ℝ) * ∑ i, d i ^ 2 := by
  have h := Finset.sum_mul_sq_le_sq_mul_sq (Finset.univ : Finset (Fin n)) (fun _ => (1 : ℝ)) d
  simpa using h

theorem equal_steps_attain (n : ℕ) (c : ℝ) :
    (∑ _i : Fin n, c) ^ 2 = (n : ℝ) * ∑ _i : Fin n, c ^ 2 := by
  simp [Finset.sum_const, Finset.card_univ]
  ring

theorem discrete_heat_ge (n : ℕ) (γ dt : ℝ) (hγ : 0 ≤ γ) (hdt : 0 < dt)
    (d : Fin n → ℝ) :
    γ / dt * (∑ i, d i) ^ 2 ≤ (n : ℝ) * (γ / dt * ∑ i, d i ^ 2) := by
  have h := sq_sum_le_card_mul_sum_sq' n d
  have hc : 0 ≤ γ / dt := div_nonneg hγ hdt.le
  calc γ / dt * (∑ i, d i) ^ 2 ≤ γ / dt * ((n : ℝ) * ∑ i, d i ^ 2) :=
        mul_le_mul_of_nonneg_left h hc
    _ = (n : ℝ) * (γ / dt * ∑ i, d i ^ 2) := by ring

def Jwin (γ w τ x0 x1 v : ℝ) : ℝ := γ * v ^ 2 * τ + w * (x0 + v * τ - x1) ^ 2

/-- `vstar` is any velocity with `vstar (γ + w τ) = w (x1 - x0)`. -/
theorem terminal_gap (γ w τ x0 x1 v vstar : ℝ) (hv : vstar * (γ + w * τ) = w * (x1 - x0)) :
    Jwin γ w τ x0 x1 v - Jwin γ w τ x0 x1 vstar = (γ * τ + w * τ ^ 2) * (v - vstar) ^ 2 := by
  unfold Jwin
  linear_combination (2 * τ * (v - vstar)) * hv

theorem terminal_min (γ w τ x0 x1 v : ℝ) (hγ : 0 < γ) (hw : 0 ≤ w) (hτ : 0 < τ) :
    Jwin γ w τ x0 x1 (w * (x1 - x0) / (γ + w * τ)) ≤ Jwin γ w τ x0 x1 v := by
  have hpos : γ + w * τ ≠ 0 := by positivity
  have hv : w * (x1 - x0) / (γ + w * τ) * (γ + w * τ) = w * (x1 - x0) := div_mul_cancel₀ _ hpos
  have := terminal_gap γ w τ x0 x1 v _ hv
  have hnn : 0 ≤ (γ * τ + w * τ ^ 2) * (v - w * (x1 - x0) / (γ + w * τ)) ^ 2 := by positivity
  linarith

#print axioms sq_sum_le_card_mul_sum_sq'
#print axioms equal_steps_attain
#print axioms discrete_heat_ge
#print axioms terminal_gap
#print axioms terminal_min
