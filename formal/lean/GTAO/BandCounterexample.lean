/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
The minimal non-convex band example of `theory/LAYER_CONVEXITY.md` §5
(PR #145), for OPEN_WORK T19.
-/
module

public import Mathlib.Data.Rat.Defs
public import Mathlib.Algebra.Order.Field.Rat
public import Mathlib.Basic.Real.Basic
public import Mathlib.Algebra.BigOperators.Fin
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.NormNum
public import Mathlib.Tactic.FinCases

/-!
# The peak counterexample: `W = (0,1,0)`, weights `(2,1,1)`

Three frequency cells, low to high, with Wiener gain `W = (0, 1, 0)` and
weights `μ = (2, 1, 1)`.  A `K`-layer band design is
`H(c) = Σ_{k<K} g_k · 1[c < b_k]` (ideal low-pass layers with free cutoffs
`b_k` and free real weights `g_k`), with cost `Σ_c μ_c (H(c) - W(c))²`.

* `clusterE` is the band-clustering cost (within-band weighted variance plus
  the terminal zero band) minimized over cutoffs, computed exactly in `ℚ`;
  `clusterE_values` checks `(1, 2/3, 0)` by `decide`.
* `bandE0`, `bandE1_lower`, `bandE1_attained`, `bandE2_attained` prove the same
  values for the real design problem itself: the minimum over all cutoffs
  and all real weights is `1`, `2/3`, `0` at `K = 0, 1, 2`.
* `not_convex`: the decrements are `1/3 < 2/3`, so the curve is not convex.
-/

@[expose] public section

namespace BandCounterexample

/-! ## The clustering cost, exactly in `ℚ` -/

/-- Weights `μ = (2,1,1)`. -/
def mu : ℕ → ℚ
  | 0 => 2
  | 1 => 1
  | 2 => 1
  | _ => 0

/-- Wiener gain `W = (0,1,0)`. -/
def W : ℕ → ℚ
  | 1 => 1
  | _ => 0

/-- Sum of `f c` over cells `a ≤ c < b` (`b ≤ 3`). -/
def segSum (f : ℕ → ℚ) (a b : ℕ) : ℚ :=
  ((List.range 3).filter (fun c => decide (a ≤ c ∧ c < b))).foldr (fun c acc => f c + acc) 0

/-- Within-band weighted variance of `W` on `[a, b)` (optimal free level). -/
def bandCost (a b : ℕ) : ℚ :=
  segSum (fun c => mu c * W c ^ 2) a b -
    (segSum (fun c => mu c * W c) a b) ^ 2 / segSum mu a b

/-- Terminal band `[a, 3)` held at level `0`. -/
def termCost (a : ℕ) : ℚ := segSum (fun c => mu c * W c ^ 2) a 3

/-- `min` over a list of rationals (`0` for the empty list). -/
def listMin : List ℚ → ℚ
  | [] => 0
  | [x] => x
  | x :: xs => min x (listMin xs)

/-- Optimal clustering cost with `K = 0, 1, 2` free bands (cutoffs in `0..3`). -/
def clusterE : ℕ → ℚ
  | 0 => termCost 0
  | 1 => listMin ((List.range 4).map fun x => bandCost 0 x + termCost x)
  | _ => listMin ((List.range 4).flatMap fun x1 => ((List.range 4).filter (x1 ≤ ·)).map
          fun x2 => bandCost 0 x1 + bandCost x1 x2 + termCost x2)

theorem clusterE_values : clusterE 0 = 1 ∧ clusterE 1 = 2 / 3 ∧ clusterE 2 = 0 := by
  decide +kernel

/-! ## The real design problem -/

/-- Real weights and gain. -/
noncomputable def muR (c : ℕ) : ℝ := (mu c : ℝ)
noncomputable def WR (c : ℕ) : ℝ := (W c : ℝ)

/-- A `K`-layer band design: `H(c) = Σ_k g_k 1[c < b_k]`. -/
noncomputable def bandH {K : ℕ} (b : Fin K → ℕ) (g : Fin K → ℝ) (c : ℕ) : ℝ :=
  ∑ k, if c < b k then g k else 0

/-- Its cost `Σ_{c<3} μ_c (H(c) - W(c))²`. -/
noncomputable def cost {K : ℕ} (b : Fin K → ℕ) (g : Fin K → ℝ) : ℝ :=
  ∑ c : Fin 3, muR c * (bandH b g c - WR c) ^ 2

lemma cost_eq {K : ℕ} (b : Fin K → ℕ) (g : Fin K → ℝ) :
    cost b g = 2 * bandH b g 0 ^ 2 + (bandH b g 1 - 1) ^ 2 + bandH b g 2 ^ 2 := by
  simp [cost, Fin.sum_univ_three, muR, WR, mu, W]

/-- `K = 0`: the only design is `H = 0`, cost `1`. -/
theorem bandE0 (b : Fin 0 → ℕ) (g : Fin 0 → ℝ) : cost b g = 1 := by
  rw [cost_eq]; simp [bandH]

/-- `K = 1`: every design costs at least `2/3`. -/
theorem bandE1_lower (b : Fin 1 → ℕ) (g : Fin 1 → ℝ) : 2 / 3 ≤ cost b g := by
  rw [cost_eq]
  simp only [bandH, Fin.sum_univ_one]
  set x := g 0
  rcases Nat.lt_or_ge (b 0) 1 with h0 | h0
  · simp [show ¬ (0 < b 0) by omega, show ¬ (1 < b 0) by omega, show ¬ (2 < b 0) by omega]
    norm_num
  rcases Nat.lt_or_ge (b 0) 2 with h1 | h1
  · simp [show (0 < b 0) by omega, show ¬ (1 < b 0) by omega, show ¬ (2 < b 0) by omega]
    nlinarith [sq_nonneg x]
  rcases Nat.lt_or_ge (b 0) 3 with h2 | h2
  · simp [show (0 < b 0) by omega, show (1 < b 0) by omega, show ¬ (2 < b 0) by omega]
    nlinarith [sq_nonneg (x - 1 / 3)]
  · simp [show (0 < b 0) by omega, show (1 < b 0) by omega, show (2 < b 0) by omega]
    nlinarith [sq_nonneg (x - 1 / 4)]

/-- `K = 1`: cutoff `2`, weight `1/3` attains `2/3`. -/
theorem bandE1_attained : cost (fun _ : Fin 1 => 2) (fun _ => 1 / 3) = 2 / 3 := by
  rw [cost_eq]; simp [bandH]; norm_num

/-- `K = 2`: cutoffs `2, 1` with weights `1, -1` give `H = (0,1,0)`, cost `0`. -/
theorem bandE2_attained : cost ![2, 1] ![1, -1] = 0 := by
  rw [cost_eq]; simp [bandH, Fin.sum_univ_two]

lemma cost_nonneg {K : ℕ} (b : Fin K → ℕ) (g : Fin K → ℝ) : 0 ≤ cost b g := by
  rw [cost_eq]; positivity

/-- **Not convex.**  The optimal band costs are `E_0 = 1`, `E_1 = 2/3`,
`E_2 = 0`, so the decrements `1/3 < 2/3` rise: `2 E_1 > E_0 + E_2`. -/
theorem not_convex :
    (∀ b g, cost (K := 0) b g = 1) ∧
    (∀ b g, 2 / 3 ≤ cost (K := 1) b g) ∧ (∃ b g, cost (K := 1) b g = 2 / 3) ∧
    (∀ b g, 0 ≤ cost (K := 2) b g) ∧ (∃ b g, cost (K := 2) b g = 0) ∧
    (1 : ℝ) - 2 / 3 < 2 / 3 - 0 :=
  ⟨bandE0, bandE1_lower, ⟨_, _, bandE1_attained⟩, cost_nonneg, ⟨_, _, bandE2_attained⟩,
    by norm_num⟩

end BandCounterexample
