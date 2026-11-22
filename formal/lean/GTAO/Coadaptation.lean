/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Finite-state Theorem CA1 (and Corollary CA1a) of `theory/COADAPTATION.md`
(PR #148), for OPEN_WORK T19.
-/
module

public import Mathlib.Analysis.SpecialFunctions.Log.Basic
public import Mathlib.Logic.Relation
public import Mathlib.Algebra.BigOperators.Group.Finset.Basic

/-!
# CA1: a Gibbs (detailed-balance) form iff an exact β-scaled potential

Parties `i : ι` each hold a design `x i : S i`; the joint state is
`x : ∀ i, S i`.  Party `i`'s design graph is a symmetric relation `G i`.
A move changes one party's design along one edge of its graph:
`y = update x i s` with `G i (x i) s`.  The rates `q x y` are arbitrary
(they carry any clocks `u_i` and any fixation probabilities) subject only to

* `q x y = 0` when `y` is not one move away from `x`,
* `q x y > 0` on moves, and
* the log-linear ratio `q x y = exp(-β_i (J_i y - J_i x)) · q y x` on a move
  of party `i` (the selection note's Moran ratio, or logit / Metropolis).

Machine-checked:

* `detailedBalance_of_potential`: if `Ψ` is an exact potential for the game
  `(β_i J_i)`, then `π = exp(-Ψ)` satisfies detailed balance, whatever the
  clocks;
* `potential_of_detailedBalance`: if each `G i` is connected and some `π > 0`
  satisfies detailed balance, then `Ψ = -log π` is an exact potential for
  `(β_i J_i)` (on every unilateral change, not only on edges), and
  `π = exp(-Ψ)`;
* `ca1_iff`: hence detailed balance with a positive `π` iff an exact
  β-scaled potential exists;
* `stationary_of_detailedBalance`: detailed balance implies stationarity;
* `ca1a_weighted` and `ca1a_square`: Corollary CA1a, both halves.

Not formalized: irreducibility implies uniqueness of the stationary law
(Perron–Frobenius), so "the stationary law is reversible" is stated here as
"some positive `π` satisfies detailed balance"; with a unique stationary law
the two readings agree.
-/

@[expose] public section

namespace Coadaptation

open Real Function

variable {ι : Type*} [DecidableEq ι] {S : ι → Type*}

/-- `y` is one move away from `x`: one party changes design along an edge. -/
def IsMove (G : ∀ i, S i → S i → Prop) (x y : ∀ i, S i) : Prop :=
  ∃ i s, G i (x i) s ∧ y = update x i s

/-- The hypotheses on the joint chain's rates. -/
structure LogLinearChain (G : ∀ i, S i → S i → Prop) (β : ι → ℝ)
    (J : ι → (∀ i, S i) → ℝ) (q : (∀ i, S i) → (∀ i, S i) → ℝ) : Prop where
  symm : ∀ i a b, G i a b → G i b a
  zero : ∀ x y, ¬ IsMove G x y → q x y = 0
  pos : ∀ x i s, G i (x i) s → 0 < q x (update x i s)
  ratio : ∀ x i s, G i (x i) s →
    q x (update x i s) = exp (-(β i * (J i (update x i s) - J i x))) * q (update x i s) x

/-- `Ψ` is an exact potential for the game with costs `β_i J_i`. -/
def IsExactPotential (β : ι → ℝ) (J : ι → (∀ i, S i) → ℝ) (Ψ : (∀ i, S i) → ℝ) : Prop :=
  ∀ x i s, Ψ (update x i s) - Ψ x = β i * (J i (update x i s) - J i x)

/-- Detailed balance of `π` for rates `q`. -/
def DetailedBalance (q : (∀ i, S i) → (∀ i, S i) → ℝ) (π : (∀ i, S i) → ℝ) : Prop :=
  ∀ x y, π x * q x y = π y * q y x

variable {G : ∀ i, S i → S i → Prop} {β : ι → ℝ} {J : ι → (∀ i, S i) → ℝ}
  {q : (∀ i, S i) → (∀ i, S i) → ℝ}

lemma isMove_symm (hC : LogLinearChain G β J q) {x y : ∀ i, S i} (h : IsMove G x y) :
    IsMove G y x := by
  obtain ⟨i, s, hG, rfl⟩ := h
  refine ⟨i, x i, ?_, ?_⟩
  · simpa using hC.symm _ _ _ hG
  · simp

/-- **CA1 (if).**  An exact potential for `(β_i J_i)` gives detailed balance
for `π = exp(-Ψ)`, for any clocks. -/
theorem detailedBalance_of_potential (hC : LogLinearChain G β J q) {Ψ : (∀ i, S i) → ℝ}
    (hΨ : IsExactPotential β J Ψ) : DetailedBalance q (fun x => exp (-Ψ x)) := by
  intro x y
  by_cases hm : IsMove G x y
  · obtain ⟨i, s, hG, rfl⟩ := hm
    rw [hC.ratio x i s hG, ← mul_assoc, ← exp_add]
    have := hΨ x i s
    congr 2
    linarith
  · have hm' : ¬ IsMove G y x := fun h => hm (isMove_symm hC h)
    simp [hC.zero x y hm, hC.zero y x hm']

/-- **CA1 (only if).**  If every party graph is connected and some `π > 0`
satisfies detailed balance, then `Ψ = -log π` is an exact potential for
`(β_i J_i)` on every unilateral change. -/
theorem potential_of_detailedBalance (hC : LogLinearChain G β J q)
    (hconn : ∀ i a b, Relation.ReflTransGen (G i) a b)
    {π : (∀ i, S i) → ℝ} (hπ : ∀ x, 0 < π x) (hdb : DetailedBalance q π) :
    IsExactPotential β J (fun x => -log (π x)) := by
  -- on an edge
  have hedge : ∀ x i s, G i (x i) s →
      -log (π (update x i s)) - -log (π x) = β i * (J i (update x i s) - J i x) := by
    intro x i s hG
    have hq := hC.ratio x i s hG
    have hback : 0 < q (update x i s) x := by
      have h := hC.pos (update x i s) i (x i) (by simpa using hC.symm _ _ _ hG)
      simpa using h
    have hd := hdb x (update x i s)
    rw [hq] at hd
    -- π x * e * q' = π y * q'  ⇒  π y = π x * e
    have hy : π (update x i s) = π x * exp (-(β i * (J i (update x i s) - J i x))) := by
      have := mul_right_cancel₀ hback.ne' (by linarith [hd] : π x * exp (-(β i *
        (J i (update x i s) - J i x))) * q (update x i s) x = π (update x i s) * q (update x i s) x)
      exact this.symm
    rw [hy, log_mul (hπ x).ne' (exp_pos _).ne', log_exp]
    ring
  intro x i s
  -- extend along a path in `G i` with the other designs fixed
  induction hconn i (x i) s with
  | refl => simp
  | @tail b c _ hab ih =>
    have he := hedge (update x i b) i c (by simpa using hab)
    simp only [update_idem] at he
    simp only at ih ⊢
    linarith

/-- **CA1 (iff).**  With connected party graphs, a positive `π` satisfying
detailed balance exists iff the game `(β_i J_i)` has an exact potential;
then `π = exp(-Ψ)` for that potential. -/
theorem ca1_iff (hC : LogLinearChain G β J q)
    (hconn : ∀ i a b, Relation.ReflTransGen (G i) a b) :
    (∃ π : (∀ i, S i) → ℝ, (∀ x, 0 < π x) ∧ DetailedBalance q π) ↔
      ∃ Ψ, IsExactPotential β J Ψ := by
  constructor
  · rintro ⟨π, hπ, hdb⟩
    exact ⟨_, potential_of_detailedBalance hC hconn hπ hdb⟩
  · rintro ⟨Ψ, hΨ⟩
    exact ⟨_, fun x => exp_pos _, detailedBalance_of_potential hC hΨ⟩

omit [DecidableEq ι] in
/-- The Gibbs form: the reversible `π` is exactly `exp(-Ψ)` with `Ψ = -log π`. -/
lemma gibbs_form {π : (∀ i, S i) → ℝ} (hπ : ∀ x, 0 < π x) (x : ∀ i, S i) :
    π x = exp (-(-log (π x))) := by
  rw [neg_neg, exp_log (hπ x)]

omit [DecidableEq ι] in
/-- Detailed balance implies stationarity (global balance) on a finite state
space: total inflow equals total outflow at every state. -/
theorem stationary_of_detailedBalance [Fintype (∀ i, S i)] {π : (∀ i, S i) → ℝ}
    (hdb : DetailedBalance q π) (x : ∀ i, S i) :
    ∑ y, π y * q y x = ∑ y, π x * q x y :=
  Finset.sum_congr rfl fun y _ => (hdb x y).symm

/-- **CA1a (weighted potential, matched strengths).**  If
`Δ_i J_i = ω_i Δ_i Φ` and `β_i ω_i = γ` for all `i`, then `γ Φ` is an exact
potential for `(β_i J_i)`, so `π ∝ exp(-γ Φ)`. -/
theorem ca1a_weighted {ω : ι → ℝ} {Φ : (∀ i, S i) → ℝ} {γ : ℝ}
    (hw : ∀ x i s, J i (update x i s) - J i x = ω i * (Φ (update x i s) - Φ x))
    (hγ : ∀ i, β i * ω i = γ) : IsExactPotential β J (fun x => γ * Φ x) := by
  intro x i s
  rw [hw, ← mul_assoc, hγ]; ring

/-- **CA1a (mismatched strengths break reversibility).**  If `(J_i)` is a
weighted potential game with weights `ω_i`, then for any exact potential of
`(β_i J_i)` and any elementary square in parties `i ≠ j`,
`(β_i ω_i - β_j ω_j) · (mixed difference of Φ) = 0`.  So if
`β_i ω_i ≠ β_j ω_j` and `Φ` has a nonzero mixed difference, there is no
exact potential, and (by `ca1_iff`) no positive `π` in detailed balance. -/
theorem ca1a_square {ω : ι → ℝ} {Φ : (∀ i, S i) → ℝ} {Ψ : (∀ i, S i) → ℝ}
    (hw : ∀ x i s, J i (update x i s) - J i x = ω i * (Φ (update x i s) - Φ x))
    (hΨ : IsExactPotential β J Ψ) (x : ∀ i, S i) {i j : ι} (hij : i ≠ j) (a : S i) (b : S j) :
    (β i * ω i - β j * ω j) *
      (Φ (update (update x i a) j b) - Φ (update x i a) - Φ (update x j b) + Φ x) = 0 := by
  have hcomm : update (update x j b) i a = update (update x i a) j b :=
    update_comm hij.symm b a x
  have h1 := hΨ x i a
  have h2 := hΨ (update x i a) j b
  have h3 := hΨ x j b
  have h4 := hΨ (update x j b) i a
  rw [hw] at h1 h2 h3 h4
  rw [hcomm] at h4
  linear_combination h2 + h1 - h4 - h3

end Coadaptation
