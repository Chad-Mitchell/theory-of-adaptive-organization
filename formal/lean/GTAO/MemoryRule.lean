/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lean 4 formalization of the working-memory rules in
`applications/GROK_BOT_MEMORY_2026-11-23.md` §4–§5, and of the
externality half of CT17 (`THEORY.md` B.5; `theory/MATH_ATTACK.md` §3.4).
-/
module

public import GTAO.LayerLifetime
public import Mathlib.Analysis.SpecialFunctions.Pow.Real
public import Mathlib.Analysis.SpecialFunctions.Sqrt
public import Mathlib.Analysis.Convex.SpecificFunctions.Basic
public import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.FieldSimp
public import Mathlib.Tactic.Positivity

/-!
# Working-memory rules: hold, re-check, band, and the under-watching part

One item of the working notes.  If it is held (`h = 1`) it costs storage
upkeep `c` per unit time, a re-check of cost `k` every `T` on average, and the
drift loss `a σ² T / 6`; if it is dropped (`h = 0`) it costs `L` per unit
time.  `GROK_BOT_MEMORY` §4 writes `a = w` and `L = w p`:

`J = h (c + k/T + w σ² T/6) + (1 − h) w p`.

The theorems below are stated for a general drift weight `a` and drop loss
`L` and then specialized to `a = w`, `L = w p`, so they hold under either
reading of the stake in the drift term.

What is assumed, not formalized: the stochastic facts behind `k/T + aσ²T/6`
(Brownian drift reset to zero at the band `±b`: mean exit time `b²/σ²` and
occupation density proportional to `b − |x|`; Dixit 1991, exact at zero
discount per Chalkley 1997), and that a barrier policy is optimal among all
re-check policies.  What is machine-checked: every optimization and every
piece of algebra and calculus that turns those facts into the rules, including
the two integrals of the density `b − |x|`.
-/

@[expose] public section

namespace MemoryRule

open Real

/-! ## 1. The per-item cost and its minimum -/

/-- Cost per unit time of a held item: upkeep `c` plus the barrier refresh
`k/T + a σ² T/6` (`s` stands for `σ²`). -/
noncomputable def heldCost (c k a s T : ℝ) : ℝ := c + LayerLifetime.cost (1 / 6) k a s T

/-- The per-item cost `h (c + k/T + aσ²T/6) + (1 − h) L` with the hold bit
`h ∈ {0, 1}` written as a `Bool`. -/
noncomputable def itemCost (h : Bool) (c k a s L T : ℝ) : ℝ :=
  if h then heldCost c k a s T else L

/-- The re-check interval `T* = √(6k/(aσ²))`. -/
noncomputable def Tstar (k a s : ℝ) : ℝ := √(6 * k / (a * s))

/-- The full cost of holding at the best interval: `c + 2√(k a σ²/6)`. -/
noncomputable def holdMin (c k a s : ℝ) : ℝ := c + 2 * √(k * a * s / 6)

lemma heldCost_ge {c k a s T : ℝ} (hk : 0 < k) (ha : 0 < a) (hs : 0 < s) (hT : 0 < T) :
    holdMin c k a s ≤ heldCost c k a s T := by
  obtain ⟨_, hmin, _, hval⟩ := LayerLifetime.layer_lifetime hk ha hs
  have := hmin T hT
  unfold heldCost holdMin
  linarith

lemma heldCost_Tstar {c k a s : ℝ} (hk : 0 < k) (ha : 0 < a) (hs : 0 < s) :
    heldCost c k a s (Tstar k a s) = holdMin c k a s := by
  obtain ⟨_, _, _, hval⟩ := LayerLifetime.layer_lifetime hk ha hs
  unfold heldCost holdMin Tstar
  rw [hval]

lemma Tstar_pos {k a s : ℝ} (hk : 0 < k) (ha : 0 < a) (hs : 0 < s) : 0 < Tstar k a s := by
  unfold Tstar; positivity

/-- **Statement 1 (per-item cost).**  For a held item with `k, a, σ² > 0`,
`c + k/T + aσ²T/6` is minimized over `T > 0` exactly at
`T* = √(6k/(aσ²))`, with minimum `c + 2√(k a σ²/6)`. -/
theorem held_min {c k a s : ℝ} (hk : 0 < k) (ha : 0 < a) (hs : 0 < s) :
    0 < Tstar k a s ∧
    heldCost c k a s (Tstar k a s) = c + 2 * √(k * a * s / 6) ∧
    (∀ T, 0 < T → heldCost c k a s (Tstar k a s) ≤ heldCost c k a s T) ∧
    (∀ T, 0 < T → heldCost c k a s T ≤ heldCost c k a s (Tstar k a s) → T = Tstar k a s) := by
  obtain ⟨_, _, huniq, _⟩ := LayerLifetime.layer_lifetime hk ha hs
  refine ⟨Tstar_pos hk ha hs, heldCost_Tstar hk ha hs, ?_, ?_⟩
  · intro T hT; rw [heldCost_Tstar hk ha hs]; exact heldCost_ge hk ha hs hT
  · intro T hT h
    exact huniq T hT (by unfold heldCost Tstar at h; linarith)

/-! ## 2. The hold rule -/

/-- **Statement 2 (hold rule), strict form.**  Some held policy is strictly
cheaper than dropping iff `L > c + 2√(k a σ²/6)`. -/
theorem hold_strictly_better_iff {c k a s L : ℝ} (hk : 0 < k) (ha : 0 < a) (hs : 0 < s) :
    (∃ T, 0 < T ∧ heldCost c k a s T < L) ↔ c + 2 * √(k * a * s / 6) < L := by
  constructor
  · rintro ⟨T, hT, h⟩
    have := heldCost_ge (c := c) hk ha hs hT
    unfold holdMin at this; linarith
  · intro h
    refine ⟨Tstar k a s, Tstar_pos hk ha hs, ?_⟩
    rw [heldCost_Tstar hk ha hs]; exact h

/-- **Statement 2 (hold rule), weak form.**  Dropping is optimal (no held
policy is cheaper) iff `L ≤ c + 2√(k a σ²/6)`.  At equality both choices are
optimal. -/
theorem drop_optimal_iff {c k a s L : ℝ} (hk : 0 < k) (ha : 0 < a) (hs : 0 < s) :
    (∀ T, 0 < T → L ≤ heldCost c k a s T) ↔ L ≤ c + 2 * √(k * a * s / 6) := by
  constructor
  · intro h
    have := h (Tstar k a s) (Tstar_pos hk ha hs)
    rwa [heldCost_Tstar hk ha hs] at this
  · intro h T hT
    have := heldCost_ge (c := c) hk ha hs hT
    unfold holdMin at this; linarith

/-- The joint minimum over the hold bit and `T > 0` is
`min (c + 2√(kaσ²/6)) L`: attained, and a lower bound. -/
theorem joint_min {c k a s L : ℝ} (hk : 0 < k) (ha : 0 < a) (hs : 0 < s) :
    (∀ h T, 0 < T → min (holdMin c k a s) L ≤ itemCost h c k a s L T) ∧
    (∃ h T, 0 < T ∧ itemCost h c k a s L T = min (holdMin c k a s) L) := by
  refine ⟨?_, ?_⟩
  · intro h T hT
    cases h
    · simp [itemCost]
    · simp only [itemCost, ↓reduceIte]
      exact (min_le_left _ _).trans (heldCost_ge hk ha hs hT)
  · rcases le_total (holdMin c k a s) L with hle | hle
    · refine ⟨true, Tstar k a s, Tstar_pos hk ha hs, ?_⟩
      simp only [itemCost, ↓reduceIte, heldCost_Tstar hk ha hs, min_eq_left hle]
    · exact ⟨false, 1, one_pos, by simp [itemCost, min_eq_right hle]⟩

/-- **The document's form** (`a = w`, `L = w p`):  holding strictly beats
dropping iff `w p > c + 2√(k w σ²/6)`, and the best held interval is
`√(6k/(wσ²))`. -/
theorem doc_hold_rule {c k w s p : ℝ} (hk : 0 < k) (hw : 0 < w) (hs : 0 < s) :
    ((∃ T, 0 < T ∧ heldCost c k w s T < w * p) ↔ c + 2 * √(k * w * s / 6) < w * p) ∧
    Tstar k w s = √(6 * k / (w * s)) :=
  ⟨hold_strictly_better_iff hk hw hs, rfl⟩

/-- The worked check in §4: at `c = 1`, `w = 10`, `p = 0.2`, `k = 0.5`,
`σ² = 1`, `w p = 2 > c` but `2.82 < c + 2√(kwσ²/6) < 2.83`, so the item
fails the full-cost test. -/
theorem doc_example :
    (10 : ℝ) * (2 / 10) = 2 ∧ (1 : ℝ) < 10 * (2 / 10) ∧
    (282 / 100 : ℝ) < holdMin 1 (1 / 2) 10 1 ∧ holdMin 1 (1 / 2) 10 1 < 283 / 100 ∧
    ¬ (∃ T, 0 < T ∧ heldCost 1 (1 / 2) 10 1 T < 10 * (2 / 10)) := by
  have hv : (1 / 2 : ℝ) * 10 * 1 / 6 = 5 / 6 := by norm_num
  have lo : (912 / 1000 : ℝ) < √(5 / 6) := by
    rw [lt_sqrt (by norm_num)]; norm_num
  have hi : √(5 / 6 : ℝ) < 915 / 1000 := by
    rw [sqrt_lt' (by norm_num)]; norm_num
  refine ⟨by norm_num, by norm_num, ?_, ?_, ?_⟩
  · unfold holdMin; rw [hv]; linarith
  · unfold holdMin; rw [hv]; linarith
  · rw [hold_strictly_better_iff (by norm_num) (by norm_num) (by norm_num), hv]
    linarith

/-! ## 3. The band `b* = (6kσ²/a)^{1/4}` -/

/-- The band `b* = (6kσ²/a)^{1/4}`. -/
noncomputable def band (k a s : ℝ) : ℝ := (6 * k * s / a) ^ (1 / 4 : ℝ)

lemma band_sq {k a s : ℝ} (hk : 0 < k) (ha : 0 < a) (hs : 0 < s) :
    band k a s ^ 2 = √(6 * k * s / a) := by
  unfold band
  have hx : 0 ≤ 6 * k * s / a := by positivity
  rw [← rpow_natCast, ← rpow_mul hx, sqrt_eq_rpow]
  norm_num

/-- **Statement 3 (band and mean interval), algebraic part.**  With
`b* = (6kσ²/a)^{1/4}`: the mean exit time `b*²/σ²` equals
`T* = √(6k/(aσ²))`; at the band the two cost terms `kσ²/b*²` (lumps) and
`a b*²/6` (mean square gap) are equal, each `√(kaσ²/6)`; and `b*` is the
unique positive minimizer of `kσ²/b² + a b²/6`. -/
theorem band_rule {k a s : ℝ} (hk : 0 < k) (ha : 0 < a) (hs : 0 < s) :
    0 < band k a s ∧
    band k a s ^ 2 / s = Tstar k a s ∧
    k * s / band k a s ^ 2 = √(k * a * s / 6) ∧
    a * band k a s ^ 2 / 6 = √(k * a * s / 6) ∧
    (∀ b, 0 < b → k * s / band k a s ^ 2 + a * band k a s ^ 2 / 6 ≤ k * s / b ^ 2 + a * b ^ 2 / 6) ∧
    (∀ b, 0 < b → k * s / b ^ 2 + a * b ^ 2 / 6 ≤ k * s / band k a s ^ 2 + a * band k a s ^ 2 / 6 →
      b = band k a s) := by
  obtain ⟨h1, h2, h3⟩ := LayerLifetime.barrier_band_identities hk ha hs
  obtain ⟨_, hmin, huniq, _⟩ := LayerLifetime.layer_lifetime hk ha hs
  have hb : 0 < band k a s := by unfold band; positivity
  have hsq := band_sq hk ha hs
  -- cost in terms of b equals `LayerLifetime.cost (1/6) k a s (b²/σ²)`
  have conv : ∀ b, 0 < b → k * s / b ^ 2 + a * b ^ 2 / 6 =
      LayerLifetime.cost (1 / 6) k a s (b ^ 2 / s) := by
    intro b hb0; unfold LayerLifetime.cost; field_simp
  have hbT : band k a s ^ 2 / s = Tstar k a s := by rw [hsq]; exact h3
  refine ⟨hb, hbT, by rw [hsq]; exact h2, by rw [hsq]; exact h1, ?_, ?_⟩
  · intro b hb0
    rw [conv _ hb, conv _ hb0, hbT]
    exact hmin _ (by positivity)
  · intro b hb0 hle
    rw [conv _ hb, conv _ hb0, hbT] at hle
    have hT := huniq _ (by positivity) hle
    have : b ^ 2 = band k a s ^ 2 := by
      have : b ^ 2 / s = band k a s ^ 2 / s := by rw [hT, hbT]; rfl
      field_simp at this; linarith
    exact (pow_left_inj₀ hb0.le hb.le two_ne_zero).mp this

/-- The occupation integrals behind the coefficient `6`, for the assumed
density `g(x) = (b − |x|)/σ²` of Brownian motion from `0` absorbed at `±b`:
total mass `∫_{−b}^{b} (b − |x|) dx = b²` (so the mean exit time is
`b²/σ²`) and second moment `∫_{−b}^{b} (b − |x|) x² dx = b⁴/6` (so the
time-average square gap is `b²/6`). -/
theorem occupation_integrals {b : ℝ} (hb : 0 ≤ b) :
    (∫ x in (-b)..b, (b - |x|)) = b ^ 2 ∧
    (∫ x in (-b)..b, (b - |x|) * x ^ 2) = b ^ 4 / 6 := by
  -- split at 0 and use evenness
  have hsplit : ∀ f : ℝ → ℝ, Continuous f → (∀ x, f (-x) = f x) →
      (∫ x in (-b)..b, f x) = 2 * ∫ x in (0:ℝ)..b, f x := by
    intro f hf hev
    rw [← intervalIntegral.integral_add_adjacent_intervals (b := 0)
      (hf.intervalIntegrable _ _) (hf.intervalIntegrable _ _)]
    have : (∫ x in (-b)..0, f x) = ∫ x in (0:ℝ)..b, f x := by
      have := intervalIntegral.integral_comp_neg (a := (0:ℝ)) (b := b) f
      simp only [neg_zero] at this
      rw [← this]; simp [hev]
    rw [this]; ring
  have hpos1 : (∫ x in (0:ℝ)..b, (b - |x|)) = ∫ x in (0:ℝ)..b, (b - x) := by
    refine intervalIntegral.integral_congr (fun x hx => ?_)
    rw [Set.uIcc_of_le hb] at hx
    simp [abs_of_nonneg hx.1]
  have hpos2 : (∫ x in (0:ℝ)..b, (b - |x|) * x ^ 2) = ∫ x in (0:ℝ)..b, (b * x ^ 2 - x ^ 3) := by
    refine intervalIntegral.integral_congr (fun x hx => ?_)
    rw [Set.uIcc_of_le hb] at hx
    simp only [abs_of_nonneg hx.1]; ring
  refine ⟨?_, ?_⟩
  · rw [hsplit (fun x => b - |x|) (by fun_prop) (by intro x; simp), hpos1,
      intervalIntegral.integral_sub intervalIntegrable_const intervalIntegral.intervalIntegrable_id]
    simp [integral_id]; ring
  · rw [hsplit (fun x => (b - |x|) * x ^ 2) (by fun_prop) (by intro x; simp), hpos2,
      intervalIntegral.integral_sub (by apply Continuous.intervalIntegrable; fun_prop)
        (by apply Continuous.intervalIntegrable; fun_prop),
      intervalIntegral.integral_const_mul, integral_pow, integral_pow]
    ring

/-- The two assumed stochastic facts give the cost `k/T + aσ²T/6` at
`T = b²/σ²`: with mean exit time `M = ∫ g = b²/σ²` and mean square gap
`(∫ g x²)/(∫ g) = b²/6`, the cost per unit time `k/M + a·b²/6` equals
`LayerLifetime.cost (1/6) k a σ² (b²/σ²)`. -/
theorem barrier_cost_from_occupation {k a s b : ℝ} (hs : 0 < s) (hb : 0 < b) :
    let M := (∫ x in (-b)..b, (b - |x|)) / s
    let G := (∫ x in (-b)..b, (b - |x|) * x ^ 2) / (∫ x in (-b)..b, (b - |x|))
    M = b ^ 2 / s ∧ G = b ^ 2 / 6 ∧
      k / M + a * G = LayerLifetime.cost (1 / 6) k a s (b ^ 2 / s) := by
  obtain ⟨i1, i2⟩ := occupation_integrals hb.le
  intro M G
  have hM : M = b ^ 2 / s := by simp only [M, i1]
  have hG : G = b ^ 2 / 6 := by
    simp only [G, i1, i2]; field_simp
  refine ⟨hM, hG, ?_⟩
  rw [hM, hG]
  unfold LayerLifetime.cost; field_simp

/-- §5's comparison: the barrier's minimized refresh `2√(kaσ²/6)` is strictly
below the fixed clock's `√(2kaσ²)` (`LayerLifetime.fixed_period_lifetime`). -/
theorem barrier_cheaper_than_fixed {k a s : ℝ} (hk : 0 < k) (ha : 0 < a) (hs : 0 < s) :
    2 * √(k * a * s / 6) < √(2 * k * a * s) := by
  have h2 : (2 : ℝ) * √(k * a * s / 6) = √(4 * (k * a * s / 6)) := by
    rw [sqrt_mul (by norm_num), show (4 : ℝ) = 2 ^ 2 by norm_num, sqrt_sq (by norm_num)]
  rw [h2]
  exact sqrt_lt_sqrt (by positivity) (by nlinarith [mul_pos (mul_pos hk ha) hs])

/-! ## 4. CT17 (ii): the part that bears only part of the loss -/

/-- Re-check rate `1/T*` of an item whose drift weight is `a`. -/
noncomputable def rate (k a s : ℝ) : ℝ := 1 / Tstar k a s

/-- **Statement 4 (CT17 (ii) in the memory model).**  If the whole's drift
weight is `Λ u` and a part counts only `Λᵢ u` (`0 < Λᵢ`, `0 < Λ`), the part's
optimal re-check rate is `√(Λᵢ/Λ)` times the whole's, and strictly lower when
`Λᵢ < Λ`. -/
theorem part_rate_ratio {k u s Li L : ℝ} (hk : 0 < k) (hu : 0 < u) (hs : 0 < s)
    (hLi : 0 < Li) (hL : 0 < L) :
    rate k (Li * u) s = √(Li / L) * rate k (L * u) s ∧
    (Li < L → rate k (Li * u) s < rate k (L * u) s) := by
  have key : rate k (Li * u) s = √(Li / L) * rate k (L * u) s := by
    unfold rate Tstar
    rw [one_div, one_div, ← sqrt_inv, ← sqrt_inv, ← sqrt_mul (by positivity)]
    congr 1; field_simp
  refine ⟨key, fun hlt => ?_⟩
  rw [key]
  have hr : 0 < rate k (L * u) s := by
    unfold rate; exact one_div_pos.mpr (Tstar_pos hk (by positivity) hs)
  have h1 : √(Li / L) < 1 := by
    rw [sqrt_lt' one_pos, one_pow, div_lt_one hL]; exact hlt
  nlinarith

/-- The same in `theory/MATH_ATTACK.md` §3.4's form: if the chosen watch rate
satisfies `f*² = κ Λ` for a fixed `κ > 0` (row 7c's `f*² ∝ Λ ∂h/∂τ`, other
factors held fixed), the part's rate is `√(Λᵢ/Λ)` of the whole's. -/
theorem watch_sq_prop {κ Li L fi f : ℝ} (hκ : 0 < κ) (hL : 0 < L) (hLi : 0 ≤ Li)
    (hfi : 0 ≤ fi) (hf : 0 ≤ f) (hi : fi ^ 2 = κ * Li) (hw : f ^ 2 = κ * L) :
    fi = √(Li / L) * f := by
  have : fi = √(κ * Li) := by rw [← hi, sqrt_sq hfi]
  have h2 : f = √(κ * L) := by rw [← hw, sqrt_sq hf]
  rw [this, h2, ← sqrt_mul (by positivity)]
  congr 1; field_simp

/-! ### CT12 / CT17 (ii) at general `α > 1` -/

/-- CT12's one-layer cost `J(T) = c/T + w q T^{α−1}/α`. -/
noncomputable def ct12Cost (α c w q T : ℝ) : ℝ := c / T + w * q * T ^ (α - 1) / α

/-- CT12's interval `T* = (α c/((α−1) w q))^{1/α}`. -/
noncomputable def ct12Tstar (α c w q : ℝ) : ℝ := (α * c / ((α - 1) * w * q)) ^ (1 / α)

lemma ct12Tstar_pow {α c w q : ℝ} (hα : 1 < α) (hc : 0 < c) (hw : 0 < w) (hq : 0 < q) :
    ct12Tstar α c w q ^ α = α * c / ((α - 1) * w * q) := by
  have h1 : 0 < α - 1 := by linarith
  unfold ct12Tstar
  rw [← rpow_mul (by positivity), one_div_mul_cancel (by linarith), rpow_one]

/-- `J(T* x) = (c/T*)·(1/x + x^{α−1}/(α−1))` for `x > 0`. -/
lemma ct12Cost_scaled {α c w q x : ℝ} (hα : 1 < α) (hc : 0 < c) (hw : 0 < w) (hq : 0 < q)
    (hx : 0 < x) :
    ct12Cost α c w q (ct12Tstar α c w q * x) =
      c / ct12Tstar α c w q * (1 / x + x ^ (α - 1) / (α - 1)) := by
  have h1 : 0 < α - 1 := by linarith
  set S := ct12Tstar α c w q with hS
  have hSpos : 0 < S := by rw [hS]; unfold ct12Tstar; positivity
  have hpow := ct12Tstar_pow hα hc hw hq
  rw [← hS] at hpow
  have hSm : S ^ (α - 1) = S ^ α / S := by
    rw [rpow_sub hSpos, rpow_one]
  unfold ct12Cost
  rw [mul_rpow hSpos.le hx.le, hSm, hpow]
  field_simp

/-- Bernoulli: `1/x + x^{α−1}/(α−1) ≥ α/(α−1)`, strictly unless `x = 1`. -/
lemma bern {α x : ℝ} (hα : 1 < α) (hx : 0 < x) :
    α / (α - 1) ≤ 1 / x + x ^ (α - 1) / (α - 1) ∧
    (x ≠ 1 → α / (α - 1) < 1 / x + x ^ (α - 1) / (α - 1)) := by
  have h1 : 0 < α - 1 := by linarith
  have hxa : x ^ (α - 1) = x ^ α / x := by rw [rpow_sub hx, rpow_one]
  have eq : 1 / x + x ^ (α - 1) / (α - 1) - α / (α - 1) =
      ((x ^ α) - (1 + α * (x - 1))) / (x * (α - 1)) := by
    rw [hxa]; field_simp; ring
  have hB := one_add_mul_self_le_rpow_one_add (s := x - 1) (by linarith) hα.le
  simp only [add_sub_cancel] at hB
  refine ⟨?_, fun hne => ?_⟩
  · have : 0 ≤ ((x ^ α) - (1 + α * (x - 1))) / (x * (α - 1)) :=
      div_nonneg (by linarith) (by positivity)
    linarith
  · have hBs := one_add_mul_self_lt_rpow_one_add (s := x - 1) (by linarith)
      (sub_ne_zero.mpr hne) hα
    simp only [add_sub_cancel] at hBs
    have : 0 < ((x ^ α) - (1 + α * (x - 1))) / (x * (α - 1)) :=
      div_pos (by linarith) (by positivity)
    linarith

/-- **CT12, general `α > 1`.**  `T* = (αc/((α−1)wq))^{1/α}` is the unique
minimizer of `c/T + wqT^{α−1}/α` on `T > 0`. -/
theorem ct12_min {α c w q : ℝ} (hα : 1 < α) (hc : 0 < c) (hw : 0 < w) (hq : 0 < q) :
    0 < ct12Tstar α c w q ∧
    (∀ T, 0 < T → ct12Cost α c w q (ct12Tstar α c w q) ≤ ct12Cost α c w q T) ∧
    (∀ T, 0 < T → ct12Cost α c w q T ≤ ct12Cost α c w q (ct12Tstar α c w q) →
      T = ct12Tstar α c w q) := by
  have h1 : 0 < α - 1 := by linarith
  set S := ct12Tstar α c w q with hS
  have hSpos : 0 < S := by rw [hS]; unfold ct12Tstar; positivity
  have hS1 : ct12Cost α c w q S = c / S * (α / (α - 1)) := by
    have := ct12Cost_scaled hα hc hw hq one_pos
    rw [← hS, mul_one] at this
    rw [this]; congr 1; rw [one_rpow]; field_simp; ring
  have hcS : 0 < c / S := by positivity
  refine ⟨hSpos, fun T hT => ?_, fun T hT hle => ?_⟩
  · have hx : 0 < T / S := by positivity
    have hTx : T = S * (T / S) := by field_simp
    rw [hS1, hTx, ct12Cost_scaled hα hc hw hq hx, ← hS]
    exact mul_le_mul_of_nonneg_left (bern hα hx).1 hcS.le
  · have hx : 0 < T / S := by positivity
    have hTx : T = S * (T / S) := by field_simp
    by_contra hne
    have hne' : T / S ≠ 1 := by
      intro h; apply hne; rw [div_eq_one_iff_eq hSpos.ne'] at h; exact h
    rw [hS1, hTx, ct12Cost_scaled hα hc hw hq hx, ← hS] at hle
    have := mul_lt_mul_of_pos_left ((bern hα hx).2 hne') hcS
    linarith

/-- **CT17 (ii), general `α > 1` (THEORY B.5).**  A part that sets its
interval with stake `Λᵢ` instead of `Λ` reads at `(Λᵢ/Λ)^{1/α}` of the whole's
optimal rate. -/
theorem ct17_part_rate {α c q Li L : ℝ} (hα : 1 < α) (hc : 0 < c) (hq : 0 < q)
    (hLi : 0 < Li) (hL : 0 < L) :
    1 / ct12Tstar α c Li q = (Li / L) ^ (1 / α) * (1 / ct12Tstar α c L q) := by
  have h1 : 0 < α - 1 := by linarith
  have e : ∀ X, 0 < X → 1 / ct12Tstar α c X q = (X * ((α - 1) * q / (α * c))) ^ (1 / α) := by
    intro X hX
    unfold ct12Tstar
    rw [one_div, ← inv_rpow (by positivity)]
    congr 1; field_simp
  rw [e Li hLi, e L hL, ← mul_rpow (by positivity) (by positivity)]
  congr 1; field_simp

/-- At `α = 2` the general factor `(Λᵢ/Λ)^{1/α}` is the square root used in
`theory/MATH_ATTACK.md` §3.4 and in the memory model above. -/
theorem ct17_alpha_two (Li L : ℝ) :
    (Li / L) ^ (1 / (2 : ℝ)) = √(Li / L) := by
  rw [sqrt_eq_rpow]

end MemoryRule
