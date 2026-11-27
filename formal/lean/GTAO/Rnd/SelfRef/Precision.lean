/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Side R&D, record-cost rounds 4–9: `theory/RECORD_COST_ROUNDS4-9_2026-11-25.md` §10. Moved from a private Lake
project (library `GTAORnd`, same Lean and Mathlib pins). Statements and proofs unchanged; only this header,
the module lines and doc-comment wording and paths differ.
-/
module

public import Mathlib

@[expose] public section

/-!
# Finite-precision toy (theory/RECORD_COST_ROUNDS4-9_2026-11-25.md §5) and the mixture no-copy core (§5, sharp records)

**Ball.** The true reversible map is a linear isometry `R` with a unit axis `u` (`R u = u`). The tracker
knows the axis only to angle `δ`: it stores its record at a unit vector `x` with
`⟪x, u⟫ = cos δ`. Then for every number of steps `k`, `‖R^[k] x - x‖ ≤ 2 sin δ`:
the record error is bounded uniformly in time.

**Disk.** The reversible maps are rotations of the unit circle in ℂ. No non-identity map fixes a record
(`SFP.lean`), so the tracker must compensate with its estimate of the angle; a residual angle
error `ε` per step leaves the record off by exactly `‖e^{ikε} x - x‖ = 2 |sin (kε/2)|`, which is
`≥ (2/π)·k|ε|` while `k|ε| ≤ π`: linear growth until saturation.

**Mixture no-copy core.** A linear map that copies (in the sense of every effect's statistics,
`f(Tx) = f(x)²` for product effects) two states and their equal mixture forces the two states to
give identical statistics for every effect; with separating effects they are equal.
-/

namespace GTAORnd.SelfRef.R78

open Real

/-- **Ball record error bound** (PROVED-IN-MODEL). -/
theorem ball_record_bound {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]
    (R : V →ₗᵢ[ℝ] V) (u x : V) (hu : ‖u‖ = 1) (hRu : R u = u) (hx : ‖x‖ = 1)
    (δ : ℝ) (hδ0 : 0 ≤ δ) (hδπ : δ ≤ π) (hxu : inner ℝ x u = cos δ) (k : ℕ) :
    ‖(R^[k]) x - x‖ ≤ 2 * sin δ := by
  set p := x - cos δ • u with hp
  -- iterates are linear, isometric, and fix u
  have hlin : ∀ k (a b : V), R^[k] (a + b) = R^[k] a + R^[k] b := by
    intro k; induction k with
    | zero => intro a b; rfl
    | succ k ih => intro a b; rw [Function.iterate_succ_apply, Function.iterate_succ_apply,
        Function.iterate_succ_apply, map_add, ih]
  have hfix : ∀ k (c : ℝ), R^[k] (c • u) = c • u := by
    intro k; induction k with
    | zero => intro c; rfl
    | succ k ih => intro c; rw [Function.iterate_succ_apply, map_smul, hRu, ih]
  have hnorm : ∀ k (a : V), ‖R^[k] a‖ = ‖a‖ := by
    intro k; induction k with
    | zero => intro a; rfl
    | succ k ih => intro a; rw [Function.iterate_succ_apply, ih, LinearIsometry.norm_map]
  have hxp : x = p + cos δ • u := by rw [hp]; abel
  have hdiff : R^[k] x - x = R^[k] p - p := by
    rw [hxp, hlin, hfix]; abel
  -- ‖p‖ = sin δ
  have hp2 : ‖p‖ ^ 2 = sin δ ^ 2 := by
    rw [hp, @norm_sub_sq_real, norm_smul, inner_smul_right, hxu, hx, hu,
      Real.norm_eq_abs]
    have := sin_sq_add_cos_sq δ
    nlinarith [sq_abs (cos δ)]
  have hs : 0 ≤ sin δ := sin_nonneg_of_nonneg_of_le_pi hδ0 hδπ
  have hpn : ‖p‖ = sin δ := by
    have := (sq_eq_sq₀ (norm_nonneg _) hs).mp hp2; exact this
  rw [hdiff]
  calc ‖R^[k] p - p‖ ≤ ‖R^[k] p‖ + ‖p‖ := norm_sub_le _ _
    _ = 2 * sin δ := by rw [hnorm, hpn]; ring

/-- chord length of a rotation of the unit circle -/
theorem chord (θ : ℝ) : ‖Complex.exp (θ * Complex.I) - 1‖ = 2 * |sin (θ / 2)| := by
  have h2 : ‖Complex.exp (θ * Complex.I) - 1‖ ^ 2 = (2 * |sin (θ / 2)|) ^ 2 := by
    rw [Complex.sq_norm, Complex.normSq_apply]
    simp only [Complex.sub_re, Complex.sub_im, Complex.exp_ofReal_mul_I_re,
      Complex.exp_ofReal_mul_I_im, Complex.one_re, Complex.one_im, sub_zero]
    rw [mul_pow, sq_abs]
    have hc : cos θ = 1 - 2 * sin (θ / 2) ^ 2 := by
      rw [show θ = 2 * (θ / 2) by ring, cos_two_mul]; rw [show 2 * (θ / 2) / 2 = θ / 2 by ring]
      nlinarith [sin_sq_add_cos_sq (θ / 2)]
    nlinarith [sin_sq_add_cos_sq θ]
  exact (sq_eq_sq₀ (norm_nonneg _) (by positivity)).mp h2

/-- **Disk record error** (PROVED-IN-MODEL): a unit record `x` under `k` steps of residual
rotation `ε` is off by exactly `2 |sin (kε/2)|`. -/
theorem disk_record_error (x : ℂ) (hx : ‖x‖ = 1) (ε : ℝ) (k : ℕ) :
    ‖Complex.exp ((k * ε : ℝ) * Complex.I) * x - x‖ = 2 * |sin (k * ε / 2)| := by
  rw [show Complex.exp ((k * ε : ℝ) * Complex.I) * x - x
      = (Complex.exp ((k * ε : ℝ) * Complex.I) - 1) * x by ring, norm_mul, hx, mul_one, chord]

/-- **Disk error grows linearly** (PROVED-IN-MODEL): while `k|ε| ≤ π`, the error is at least
`(2/π)·k|ε|`. -/
theorem disk_error_linear (x : ℂ) (hx : ‖x‖ = 1) (ε : ℝ) (k : ℕ) (hk : k * |ε| ≤ π) :
    2 / π * (k * |ε|) ≤ ‖Complex.exp ((k * ε : ℝ) * Complex.I) * x - x‖ := by
  rw [disk_record_error x hx]
  have hk0 : (0 : ℝ) ≤ k := Nat.cast_nonneg k
  have habs : |k * ε / 2| = k * |ε| / 2 := by
    rw [abs_div, abs_mul, abs_of_nonneg hk0]; norm_num
  have h := mul_le_sin (x := k * |ε| / 2) (by positivity) (by linarith)
  have hsin : |sin (k * ε / 2)| = sin (k * |ε| / 2) := by
    rw [← habs]
    rcases le_total 0 (k * ε / 2) with h0 | h0
    · rw [abs_of_nonneg h0, abs_of_nonneg (sin_nonneg_of_nonneg_of_le_pi h0 (by
        have : k * ε / 2 ≤ k * |ε| / 2 := by
          have := le_abs_self (k * ε / 2); rw [habs] at this; exact this
        linarith [pi_pos]))]
    · have hn := sin_nonneg_of_nonneg_of_le_pi (x := -(k * ε / 2)) (by linarith) (by
          have := neg_abs_le (k * ε / 2); rw [habs] at this; linarith [pi_pos])
      rw [sin_neg] at hn
      rw [abs_of_nonpos h0, sin_neg, abs_of_nonpos (by linarith)]
  rw [hsin]
  have : 2 / π * (k * |ε|) = 2 * (2 / π * (k * |ε| / 2)) := by ring
  linarith

/-- **The contrast** (PROVED-IN-MODEL, toy): with precision `δ ∈ (0, π/2]`, the ball record stays
within `2 sin δ` for all time, while a disk record with residual error `δ` per step reaches
error `≥ (2/π)·kδ` for every `k ≤ π/δ`, in particular exceeds `2 sin δ` once
`k > π sin δ / δ`. -/
theorem disk_exceeds_ball (δ : ℝ) (hδ : 0 < δ) (k : ℕ) (hk : k * δ ≤ π)
    (hbig : π * sin δ < k * δ) (x : ℂ) (hx : ‖x‖ = 1) :
    2 * sin δ < ‖Complex.exp ((k * δ : ℝ) * Complex.I) * x - x‖ := by
  have h := disk_error_linear x hx δ k (by rwa [abs_of_pos hδ])
  rw [abs_of_pos hδ] at h
  have : 2 * sin δ < 2 / π * (k * δ) := by
    rw [div_mul_eq_mul_div, lt_div_iff₀ pi_pos]; nlinarith
  linarith

/-! ## Mixture no-copy core (toy form used in R2a′ / R8.3) -/

/-- If, for an effect `f`, a copier's output statistics satisfy `F(x) = f(x)^2` (both copies
pass `f`) on states `x`, `y` and their equal mixture, and `F`, `f` are affine on that mixture,
then `f x = f y`. -/
theorem mixture_copy_core (fx fy Fx Fy Fm fm : ℝ)
    (hfm : fm = (fx + fy) / 2) (hFm : Fm = (Fx + Fy) / 2)
    (hx : Fx = fx ^ 2) (hy : Fy = fy ^ 2) (hm : Fm = fm ^ 2) : fx = fy := by
  subst hfm hFm hx hy
  nlinarith [sq_nonneg (fx - fy)]

/-- **No copying of a mixture** (PROVED-IN-MODEL): on a real vector space of unnormalised
states, let `T : V →ₗ W` be linear, and `prod : (V →ₗ ℝ) → (W →ₗ ℝ)` assign to each effect
`f` its two-copy product effect, with `prod f (T z) = f z ^ 2` whenever `T` copies `z`. If `T`
copies `x`, `y` and `(x+y)/2`, then every effect gives `x` and `y` the same value; if effects
separate states, `x = y`. So a copyable record set contains no non-trivial mixture of two of its
records. -/
theorem no_copy_mixture {V W : Type*} [AddCommGroup V] [Module ℝ V] [AddCommGroup W]
    [Module ℝ W] (T : V →ₗ[ℝ] W) (E : Set (V →ₗ[ℝ] ℝ)) (prod : (V →ₗ[ℝ] ℝ) → (W →ₗ[ℝ] ℝ))
    (x y : V)
    (hcopy : ∀ z ∈ ({x, y, (1 / 2 : ℝ) • (x + y)} : Set V), ∀ f ∈ E, prod f (T z) = f z ^ 2)
    (hsep : ∀ a b : V, (∀ f ∈ E, f a = f b) → a = b) : x = y := by
  apply hsep
  intro f hf
  have hx := hcopy x (by simp) f hf
  have hy := hcopy y (by simp) f hf
  have hm := hcopy ((1 / 2 : ℝ) • (x + y)) (by simp) f hf
  rw [map_smul, map_add, map_smul, map_smul, map_add, map_add, hx, hy,
    smul_eq_mul, smul_eq_mul] at hm
  exact mixture_copy_core (f x) (f y) (f x ^ 2) (f y ^ 2) ((1 / 2) * (f x ^ 2 + f y ^ 2))
    ((1 / 2) * (f x + f y)) (by ring) (by ring) rfl rfl (by rw [hm])

end GTAORnd.SelfRef.R78
