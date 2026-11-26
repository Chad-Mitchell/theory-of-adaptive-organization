/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost round 10: `theory/RECORD_COST_ROUND10_2026-11-25.md` §7.
-/
module

public import Mathlib

@[expose] public section

/-!
# Continuous time and finite reversible groups; never-ending novelty and infinite order

**Continuous time.** A continuous one-parameter family `f : ℝ → G` of reversible maps with
`f 0 = 1` is constant when `G` is finite with a T1 topology (so discrete): the image of the
connected line in a discrete space is a point. Hence a state space whose reversible group is
finite (a polytope) admits no non-trivial change in continuous time.

**Never-ending novelty.** If some orbit of a reversible map `T` never returns to its start,
then `T` has infinite order. This is a statement about the global map only; it says nothing
about the reversible group of any part.
-/

namespace GTAORnd.SelfRef.R10

/-- A continuous map from the real line into a discrete space is constant. -/
theorem continuous_line_discrete_const {G : Type*} [TopologicalSpace G] [DiscreteTopology G]
    (f : ℝ → G) (hf : Continuous f) (t : ℝ) : f t = f 0 :=
  hf.isConst_of_preconnectedSpace t 0

/-- In a finite group with a T1 topology, a continuous one-parameter family starting at the
identity never leaves it. -/
theorem finite_group_no_continuous_motion {G : Type*} [Group G] [Finite G] [TopologicalSpace G]
    [T1Space G] (f : ℝ → G) (hf : Continuous f) (h0 : f 0 = 1) (t : ℝ) : f t = 1 := by
  have : DiscreteTopology G := Finite.instDiscreteTopology
  rw [continuous_line_discrete_const f hf t, h0]

/-- Non-trivial continuous-time change forces the reversible group to be infinite
(for any T1 group topology in which the motion is continuous). -/
theorem continuous_change_infinite_group {G : Type*} [Group G] [TopologicalSpace G] [T1Space G]
    (f : ℝ → G) (hf : Continuous f) (h0 : f 0 = 1) (t : ℝ) (ht : f t ≠ 1) : Infinite G := by
  by_contra hfin
  have : Finite G := not_infinite_iff_finite.mp hfin
  exact ht (finite_group_no_continuous_motion f hf h0 t)

/-- Never-ending novelty: an orbit that never returns forces infinite order of the map. -/
theorem never_returns_infinite_order {X : Type*} (T : Equiv.Perm X) (x : X)
    (h : ∀ n : ℕ, 0 < n → (T ^ n) x ≠ x) : orderOf T = 0 := by
  by_contra h'
  apply h (orderOf T) (Nat.pos_of_ne_zero h')
  rw [pow_orderOf_eq_one]
  rfl

end GTAORnd.SelfRef.R10
