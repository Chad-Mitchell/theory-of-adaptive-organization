/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Theorem DS2 of `theory/DRIFT_SELECTION.md` §6 (CLAIM_MAP S2): the
exact-chain speed limit and growing lag.  For OPEN_WORK T19.
-/
module

public import Mathlib.Algebra.Order.Star.Real
public import Mathlib.Order.Filter.AtTopBot.Field
public import Mathlib.Order.Filter.AtTopBot.Group
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.Positivity

/-!
# DS2: exact-chain speed limit and growing lag

`theory/DRIFT_SELECTION.md` Theorem DS2, CLAIM_MAP S2.  The Moran
fixation probability `φ < 1` is the reason the instantaneous drift of
each coordinate is strictly inside `(-v_max, v_max)` with
`v_max = Nμδ/(2d)`.  That strict speed bound on the mean position,
`|E[θ_k(t)] − E[θ_k(0)]| < v_max t`, is the input (the jump-process
construction of the chain is not formalized).  From it we prove the lag
lower bound, the quadratic cost bound once a Rayleigh lower bound
`λ_min` and the moment inequalities `E[|L|] ≥ |E[L]|` and
`E[L²] ≥ (E[|L|])²` are granted, and that a half-window lower bound on
the time-averaged excess diverges.

The equality case `|v_k| = v_max` is excluded, as in the note.
-/

@[expose] public section

open Filter

namespace DriftSpeed

/-- Mutational speed bound `v_max = N μ δ / (2 d)`.  Here `dim` is the
number of coordinates (`d` in the note). -/
noncomputable def vMax (N μ δ : ℝ) (dim : ℕ) : ℝ :=
  N * μ * δ * (2 * dim : ℝ)⁻¹

lemma vMax_pos {N μ δ : ℝ} {dim : ℕ}
    (hN : 0 < N) (hμ : 0 < μ) (hδ : 0 < δ) (hdim : 0 < dim) :
    0 < vMax N μ δ dim := by
  have hdim' : (0 : ℝ) < dim := Nat.cast_pos.mpr hdim
  have hden : (0 : ℝ) < 2 * dim := mul_pos (by norm_num) hdim'
  exact mul_pos (mul_pos (mul_pos hN hμ) hδ) (inv_pos.mpr hden)

/-- Mean lag `E[L_k(t)]` when the mean coordinate is `θt` and the
optimum is `θstar0 + vk * t`.  The initial mean `θ0` is an argument of
the lag theorems (via `L_k(0) = θ0 - θstar0`) but is not part of this
value. -/
noncomputable def meanLag (θt θstar0 vk t : ℝ) : ℝ :=
  θt - θstar0 - vk * t

lemma meanLag_decomp (θ0 θt θstar0 vk t : ℝ) :
    meanLag θt θstar0 vk t = (θt - θ0) + (θ0 - θstar0) - vk * t := by
  unfold meanLag
  ring

/-- **DS2, lag bound, `v_k > v_max`.**  With the mean-speed bound and
`t ≥ |L_k(0)| / (v_k − v_max)`, one has `E[L_k(t)] ≤ −B` for
`B = (v_k − v_max) t − |L_k(0)| ≥ 0`. -/
theorem meanLag_of_faster {θ0 θt θstar0 vk vmax t : ℝ}
    (hspeed : |θt - θ0| < vmax * t)
    (hfast : vmax < vk)
    (ht : |θ0 - θstar0| * (vk - vmax)⁻¹ ≤ t) :
    let B := (vk - vmax) * t - |θ0 - θstar0|
    0 ≤ B ∧ meanLag θt θstar0 vk t ≤ -B := by
  intro B
  have hα : 0 < vk - vmax := sub_pos.mpr hfast
  have htcomm : (vk - vmax)⁻¹ * |θ0 - θstar0| ≤ t := by
    rw [mul_comm]; exact ht
  have htmul : |θ0 - θstar0| ≤ (vk - vmax) * t := (inv_mul_le_iff₀ hα).mp htcomm
  have hB : 0 ≤ B := by
    change 0 ≤ (vk - vmax) * t - |θ0 - θstar0|
    exact sub_nonneg.mpr htmul
  have hθ : θt - θ0 < vmax * t := (abs_lt.mp hspeed).2
  have hL0 : θ0 - θstar0 ≤ |θ0 - θstar0| := le_abs_self _
  refine ⟨hB, ?_⟩
  have hlt : meanLag θt θstar0 vk t < vmax * t + |θ0 - θstar0| - vk * t := by
    have hsum : (θt - θ0) + (θ0 - θstar0) < vmax * t + |θ0 - θstar0| :=
      add_lt_add_of_lt_of_le hθ hL0
    rw [meanLag_decomp θ0]
    exact sub_lt_sub_right hsum (vk * t)
  have hrew : vmax * t + |θ0 - θstar0| - vk * t = -((vk - vmax) * t - |θ0 - θstar0|) := by
    ring
  have : meanLag θt θstar0 vk t < -B := by
    change meanLag θt θstar0 vk t < -((vk - vmax) * t - |θ0 - θstar0|)
    rwa [← hrew]
  exact this.le

/-- **DS2, lag bound, `v_k < −v_max`.** -/
theorem meanLag_of_faster_neg {θ0 θt θstar0 vk vmax t : ℝ}
    (hspeed : |θt - θ0| < vmax * t)
    (hfast : vk < -vmax)
    (ht : |θ0 - θstar0| * (-vk - vmax)⁻¹ ≤ t) :
    let B := (-vk - vmax) * t - |θ0 - θstar0|
    0 ≤ B ∧ B ≤ meanLag θt θstar0 vk t := by
  intro B
  have hα : 0 < -vk - vmax := by linarith
  have htcomm : (-vk - vmax)⁻¹ * |θ0 - θstar0| ≤ t := by
    rw [mul_comm]; exact ht
  have htmul : |θ0 - θstar0| ≤ (-vk - vmax) * t := (inv_mul_le_iff₀ hα).mp htcomm
  have hB : 0 ≤ B := by
    change 0 ≤ (-vk - vmax) * t - |θ0 - θstar0|
    exact sub_nonneg.mpr htmul
  have hθ : -(vmax * t) < θt - θ0 := (abs_lt.mp hspeed).1
  have hL0 : -|θ0 - θstar0| ≤ θ0 - θstar0 := neg_abs_le _
  refine ⟨hB, ?_⟩
  have hgt : -vmax * t - |θ0 - θstar0| - vk * t ≤ meanLag θt θstar0 vk t := by
    have hsum : -(vmax * t) + (-|θ0 - θstar0|) ≤ (θt - θ0) + (θ0 - θstar0) :=
      add_le_add (le_of_lt hθ) hL0
    have hsum' : -vmax * t - |θ0 - θstar0| ≤ (θt - θ0) + (θ0 - θstar0) := by
      convert hsum using 1
      ring
    rw [meanLag_decomp θ0]
    exact sub_le_sub_right hsum' (vk * t)
  have hrew : -vmax * t - |θ0 - θstar0| - vk * t = (-vk - vmax) * t - |θ0 - θstar0| := by
    ring
  have : B ≤ meanLag θt θstar0 vk t := by
    change (-vk - vmax) * t - |θ0 - θstar0| ≤ meanLag θt θstar0 vk t
    rwa [← hrew]
  exact this

/-- Combine both directions: `|v_k| > v_max` and `t` large enough give
`|E[L_k(t)]| ≥ B = (|v_k| − v_max) t − |L_k(0)| ≥ 0`. -/
theorem meanLag_abs {θ0 θt θstar0 vk vmax t : ℝ}
    (hspeed : |θt - θ0| < vmax * t)
    (hfast : vmax < |vk|)
    (ht : |θ0 - θstar0| * (|vk| - vmax)⁻¹ ≤ t) :
    let B := (|vk| - vmax) * t - |θ0 - θstar0|
    0 ≤ B ∧ B ≤ |meanLag θt θstar0 vk t| := by
  intro B
  rcases le_total 0 vk with hv | hv
  · have hvk : |vk| = vk := abs_of_nonneg hv
    have hfast' : vmax < vk := by
      rw [← hvk]; exact hfast
    have ht' : |θ0 - θstar0| * (vk - vmax)⁻¹ ≤ t := by
      rw [← hvk]; exact ht
    obtain ⟨hB0, hle⟩ := meanLag_of_faster hspeed hfast' ht'
    have hBeq : B = (vk - vmax) * t - |θ0 - θstar0| := by
      change (|vk| - vmax) * t - |θ0 - θstar0| = (vk - vmax) * t - |θ0 - θstar0|
      rw [hvk]
    refine ⟨?_, ?_⟩
    · rw [hBeq]; exact hB0
    · have hle' : meanLag θt θstar0 vk t ≤ -B := by
        rw [hBeq]; exact hle
      have hnonpos : meanLag θt θstar0 vk t ≤ 0 :=
        hle'.trans (neg_nonpos.mpr (by rw [hBeq]; exact hB0))
      have hneg : B ≤ -meanLag θt θstar0 vk t := (le_neg).mp hle'
      rw [abs_of_nonpos hnonpos]
      exact hneg
  · have hvk : |vk| = -vk := abs_of_nonpos hv
    have hfast' : vk < -vmax := by
      have : vmax < -vk := by
        rw [← hvk]; exact hfast
      linarith
    have ht' : |θ0 - θstar0| * (-vk - vmax)⁻¹ ≤ t := by
      rw [← hvk]; exact ht
    obtain ⟨hB0, hge⟩ := meanLag_of_faster_neg hspeed hfast' ht'
    have hBeq : B = (-vk - vmax) * t - |θ0 - θstar0| := by
      change (|vk| - vmax) * t - |θ0 - θstar0| = (-vk - vmax) * t - |θ0 - θstar0|
      rw [hvk]
    refine ⟨?_, ?_⟩
    · rw [hBeq]; exact hB0
    · have hge' : B ≤ meanLag θt θstar0 vk t := by
        rw [hBeq]; exact hge
      exact hge'.trans (le_abs_self _)

/-- **DS2, cost bound.**  Granted `eAbs ≥ |E[L]|` (triangle / Jensen),
`eSq ≥ eAbs²` (Cauchy–Schwarz on `|L|`), and a Rayleigh bound
`(1/2) λ_min E[L_k²] ≤ E[J−J*]` (`λ_min` a lower bound on the smallest
eigenvalue of `H`, taken as input), the excess is at least
`(1/2) λ_min B²` once `B ≥ 0`. -/
theorem ds2_excess {θ0 θt θstar0 vk vmax t eAbs eSq eCost lamMin : ℝ}
    (hspeed : |θt - θ0| < vmax * t)
    (hfast : vmax < |vk|)
    (ht : |θ0 - θstar0| * (|vk| - vmax)⁻¹ ≤ t)
    (hAbs : |meanLag θt θstar0 vk t| ≤ eAbs)
    (hSq : eAbs ^ 2 ≤ eSq)
    (hlam : 0 < lamMin)
    (hCost : (2 : ℝ)⁻¹ * lamMin * eSq ≤ eCost) :
    let B := (|vk| - vmax) * t - |θ0 - θstar0|
    0 ≤ B ∧ (2 : ℝ)⁻¹ * lamMin * B ^ 2 ≤ eCost := by
  intro B
  obtain ⟨hB, hle⟩ := meanLag_abs hspeed hfast ht
  have hBeq : B = (|vk| - vmax) * t - |θ0 - θstar0| := rfl
  rw [← hBeq] at hB hle
  refine ⟨hB, ?_⟩
  have hBe : B ≤ eAbs := hle.trans hAbs
  have heAbs : 0 ≤ eAbs := hB.trans hBe
  have hBsq : B ^ 2 ≤ eAbs ^ 2 := pow_le_pow_left₀ hB hBe 2
  have hhalf : (0 : ℝ) ≤ (2 : ℝ)⁻¹ := inv_nonneg.mpr (by norm_num)
  have h1 : lamMin * B ^ 2 ≤ lamMin * eSq :=
    mul_le_mul_of_nonneg_left (hBsq.trans hSq) hlam.le
  have h2 : (2 : ℝ)⁻¹ * lamMin * B ^ 2 ≤ (2 : ℝ)⁻¹ * lamMin * eSq := by
    have : (2 : ℝ)⁻¹ * (lamMin * B ^ 2) ≤ (2 : ℝ)⁻¹ * (lamMin * eSq) :=
      mul_le_mul_of_nonneg_left h1 hhalf
    convert this using 1 <;> ring
  exact h2.trans hCost

/-- The half-window lower bound used for the time average,
`(c/2)(α T/2 − β)²`, tends to infinity when `α, c > 0`.  If the excess
is at least `c (α t − β)²` on `[T/2, T]`, any average that puts mass at
least `1/2` on that window is at least this quantity, and therefore
diverges. -/
theorem halfWindow_diverges {α β c : ℝ} (hα : 0 < α) (hc : 0 < c) :
    Tendsto (fun T : ℝ => (c * (2 : ℝ)⁻¹) * (α * T * (2 : ℝ)⁻¹ - β) ^ 2) atTop atTop := by
  have hα2 : (0 : ℝ) < α * (2 : ℝ)⁻¹ := mul_pos hα (inv_pos.mpr (by norm_num))
  have hlin : Tendsto (fun T : ℝ => α * T * (2 : ℝ)⁻¹ - β) atTop atTop := by
    have hmul : Tendsto (fun T : ℝ => (α * (2 : ℝ)⁻¹) * T) atTop atTop :=
      tendsto_id.const_mul_atTop hα2
    have hadd : Tendsto (fun T : ℝ => (α * (2 : ℝ)⁻¹) * T + (-β)) atTop atTop :=
      tendsto_atTop_add_const_right atTop (-β) hmul
    convert hadd using 1
    funext T
    ring
  have hsq : Tendsto (fun T : ℝ => (α * T * (2 : ℝ)⁻¹ - β) ^ 2) atTop atTop := by
    have hem : ∀ᶠ T in atTop, (1 : ℝ) ≤ α * T * (2 : ℝ)⁻¹ - β :=
      hlin.eventually (eventually_ge_atTop 1)
    refine tendsto_atTop_mono' atTop ?_ hlin
    filter_upwards [hem] with T hT
    nlinarith
  have hc2 : (0 : ℝ) < c * (2 : ℝ)⁻¹ := mul_pos hc (inv_pos.mpr (by norm_num))
  exact hsq.const_mul_atTop hc2

end DriftSpeed
