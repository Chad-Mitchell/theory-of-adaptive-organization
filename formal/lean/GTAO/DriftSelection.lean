/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Lean 4 formalization of the Lyapunov-trace identity in Theorem DS1 of
`theory/DRIFT_SELECTION.md` (PR #146, CLAIM_MAP section S): the
stationary excess of a quadratic cost against a moving centre.  For
OPEN_WORK T19.
-/
module

public import Mathlib.Algebra.Order.Star.Real
public import Mathlib.LinearAlgebra.Matrix.PosDef
public import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
public import Mathlib.LinearAlgebra.Matrix.Trace
public import Mathlib.LinearAlgebra.Matrix.ConjTranspose
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.Positivity
public import Mathlib.Tactic.Ring
public import Mathlib.Tactic.FieldSimp
public import Mathlib.Tactic.Abel

/-!
# DS1: tracking excess in the diffusion limit

`theory/DRIFT_SELECTION.md` Theorem DS1.  The derivation of the Langevin
equation (L) from the origination–fixation chain, and the existence of a
unique stationary law for that linear SDE (with time averages equal to
stationary means), are **not** formalized: they are inputs, as SA1's
Boltzmann weight is an input to `Equipartition`.  What is machine-checked
is the Lyapunov-trace identity that produces the excess formula from the
stationary moment equations of (L).

Under DS-A, the excess is `½ Lᵀ H L`, so its stationary mean is
`½ Tr(H P)` for `P = E[L Lᵀ]`.

* `ou_excess`: DS1(a), Ornstein–Uhlenbeck world (`γ > 0`).
* `bm_excess`, `bm_excess_isotropic`: DS1(b), including
  `d/(2β)(1 + D/D_m)` when `Q = D I`.
* `velocity_mean_excess`: DS1(c), the mean-lag contribution
  `vᵀ H⁻¹ v / (2 β² D_m²)`.
* `ou_excess_static`, `ou_excess_fast_remainder`: DS1(d), the static
  reduction `Q = 0` and the exact remainder to the fast-`γ` floor
  `½ Tr(H (Q/γ))`.
-/

@[expose] public section

open Matrix

namespace DriftSelection

set_option linter.unusedSectionVars false

variable {d : ℕ} [NeZero d] [DecidableEq (Fin d)]

/-- The mutational drift matrix `A = D_m β H`. -/
noncomputable def driftMatrix (Dm β : ℝ) (H : Matrix (Fin d) (Fin d) ℝ) :
    Matrix (Fin d) (Fin d) ℝ :=
  (Dm * β) • H

lemma driftMatrix_posDef {Dm β : ℝ} {H : Matrix (Fin d) (Fin d) ℝ}
    (hDm : 0 < Dm) (hβ : 0 < β) (hH : H.PosDef) :
    (driftMatrix Dm β H).PosDef :=
  hH.smul (mul_pos hDm hβ)

lemma driftMatrix_add_posDef {Dm β γ : ℝ} {H : Matrix (Fin d) (Fin d) ℝ}
    (hDm : 0 < Dm) (hβ : 0 < β) (hγ : 0 ≤ γ) (hH : H.PosDef) :
    (driftMatrix Dm β H + γ • (1 : Matrix (Fin d) (Fin d) ℝ)).PosDef :=
  (driftMatrix_posDef hDm hβ hH).add_posSemidef (PosSemidef.smul PosSemidef.one hγ)

/-- Stationary moment equations for an OU world (`γ > 0`):
`S = E[θ* θ*ᵀ] = Q/γ`, `C = E[L θ*ᵀ]`, `P = E[L Lᵀ]`, from Itô's rule
at stationarity in `theory/DRIFT_SELECTION.md` §4. -/
structure OUMoments (Dm β γ : ℝ) (H Q P C S : Matrix (Fin d) (Fin d) ℝ) : Prop where
  world_cov : γ • S = Q
  world :
    (0 : Matrix (Fin d) (Fin d) ℝ) =
      -((driftMatrix Dm β H + γ • (1 : Matrix (Fin d) (Fin d) ℝ)) * C)
        + γ • S - (2 : ℝ) • Q
  lag :
    (0 : Matrix (Fin d) (Fin d) ℝ) =
      -(driftMatrix Dm β H * P) - (P * driftMatrix Dm β H)
        + γ • (C + Cᵀ)
        + (2 * Dm) • (1 : Matrix (Fin d) (Fin d) ℝ)
        + (2 : ℝ) • Q

/-- Stationary lag-covariance equation for a Brownian world (`γ = 0`). -/
structure BMMoments (Dm β : ℝ) (H Q P : Matrix (Fin d) (Fin d) ℝ) : Prop where
  lag :
    (0 : Matrix (Fin d) (Fin d) ℝ) =
      -(driftMatrix Dm β H * P) - (P * driftMatrix Dm β H)
        + (2 * Dm) • (1 : Matrix (Fin d) (Fin d) ℝ)
        + (2 : ℝ) • Q

lemma card_fin : (Fintype.card (Fin d) : ℝ) = d := by
  simp [Fintype.card_fin]

lemma trace_one_fin : trace (1 : Matrix (Fin d) (Fin d) ℝ) = (d : ℝ) := by
  rw [trace_one, card_fin]

lemma sub_two_smul (Q : Matrix (Fin d) (Fin d) ℝ) :
    Q - (2 : ℝ) • Q = -Q := by
  calc
    Q - (2 : ℝ) • Q = (1 : ℝ) • Q - (2 : ℝ) • Q := by rw [one_smul]
    _ = ((1 : ℝ) - 2) • Q := by rw [sub_smul]
    _ = (-1 : ℝ) • Q := by norm_num
    _ = -Q := by rw [neg_one_smul]

lemma isHermitian_transpose {A : Matrix (Fin d) (Fin d) ℝ} (hA : A.IsHermitian) :
    Aᵀ = A :=
  (conjTranspose_eq_transpose_of_trivial A).symm.trans hA

/-- From the world-lag Itô equation, `C = -(A+γI)⁻¹ Q`. -/
lemma ou_C_eq {Dm β γ : ℝ} {H Q P C S : Matrix (Fin d) (Fin d) ℝ}
    (hDm : 0 < Dm) (hβ : 0 < β) (hγ : 0 < γ) (hH : H.PosDef)
    (hM : OUMoments Dm β γ H Q P C S) :
    C = -((driftMatrix Dm β H + γ • (1 : Matrix (Fin d) (Fin d) ℝ))⁻¹ * Q) := by
  have hPos : (driftMatrix Dm β H + γ • (1 : Matrix (Fin d) (Fin d) ℝ)).PosDef :=
    driftMatrix_add_posDef hDm hβ hγ.le hH
  have hU : IsUnit (driftMatrix Dm β H + γ • (1 : Matrix (Fin d) (Fin d) ℝ)).det :=
    (isUnit_iff_isUnit_det _).mp hPos.isUnit
  have h0 : (0 : Matrix (Fin d) (Fin d) ℝ) =
      -((driftMatrix Dm β H + γ • (1 : Matrix (Fin d) (Fin d) ℝ)) * C)
        + Q - (2 : ℝ) • Q := by
    have := hM.world
    rwa [hM.world_cov] at this
  have h0' : (0 : Matrix (Fin d) (Fin d) ℝ) =
      -((driftMatrix Dm β H + γ • (1 : Matrix (Fin d) (Fin d) ℝ)) * C) - Q := by
    have hQ : Q - (2 : ℝ) • Q = -Q := sub_two_smul Q
    rw [add_sub_assoc, hQ] at h0
    exact h0
  have hAC : (driftMatrix Dm β H + γ • (1 : Matrix (Fin d) (Fin d) ℝ)) * C = -Q := by
    have h := congr_arg
      (fun M => M + (driftMatrix Dm β H + γ • (1 : Matrix (Fin d) (Fin d) ℝ)) * C + Q) h0'
    -- 0 + IγC + Q = -(IγC) - Q + IγC + Q
    simp only [zero_add] at h
    have hsum : (driftMatrix Dm β H + γ • (1 : Matrix (Fin d) (Fin d) ℝ)) * C + Q = 0 := by
      -- right-hand side cancels
      simpa [sub_eq_add_neg, add_assoc, add_left_comm, add_comm, add_neg_cancel, add_zero]
        using h
    exact eq_neg_iff_add_eq_zero.mpr hsum
  have hL := congr_arg
    (fun M => (driftMatrix Dm β H + γ • (1 : Matrix (Fin d) (Fin d) ℝ))⁻¹ * M) hAC
  rw [← mul_assoc,
    nonsing_inv_mul (driftMatrix Dm β H + γ • (1 : Matrix (Fin d) (Fin d) ℝ)) hU,
    one_mul, mul_neg] at hL
  exact hL

/-- Cyclic property for a product of three real Hermitian matrices:
`Tr(X H Q) = Tr(H X Q)`. -/
lemma trace_mul₃_herm {X H Q : Matrix (Fin d) (Fin d) ℝ}
    (hX : X.IsHermitian) (hH : H.IsHermitian) (hQ : Q.IsHermitian) :
    trace (X * H * Q) = trace (H * X * Q) := by
  have hXt := isHermitian_transpose hX
  have hHt := isHermitian_transpose hH
  have hQt := isHermitian_transpose hQ
  calc
    trace (X * H * Q) = trace (X * H * Q)ᵀ := (trace_transpose _).symm
    _ = trace (Qᵀ * (X * H)ᵀ) := by rw [transpose_mul]
    _ = trace (Qᵀ * (Hᵀ * Xᵀ)) := by rw [transpose_mul]
    _ = trace (Qᵀ * Hᵀ * Xᵀ) := by rw [← mul_assoc]
    _ = trace (Q * H * X) := by rw [hXt, hHt, hQt]
    _ = trace (H * X * Q) := by rw [trace_mul_cycle H X Q]

/-- **DS1(a).**  Under the OU stationary moment equations, the stationary
mean excess is `d/(2β) + ½ Tr[H (A+γI)⁻¹ Q]`. -/
theorem ou_excess {Dm β γ : ℝ} {H Q P C S : Matrix (Fin d) (Fin d) ℝ}
    (hDm : 0 < Dm) (hβ : 0 < β) (hγ : 0 < γ) (hH : H.PosDef) (hQ : Q.IsHermitian)
    (hM : OUMoments Dm β γ H Q P C S) :
    (1 / 2) * trace (H * P) =
      (d : ℝ) / (2 * β)
        + (1 / 2) *
          trace (H * (driftMatrix Dm β H + γ • (1 : Matrix (Fin d) (Fin d) ℝ))⁻¹ * Q) := by
  set A := driftMatrix Dm β H
  set Iγ : Matrix (Fin d) (Fin d) ℝ := A + γ • (1 : Matrix (Fin d) (Fin d) ℝ)
  have hPos : Iγ.PosDef := driftMatrix_add_posDef hDm hβ hγ.le hH
  have hU : IsUnit Iγ.det := (isUnit_iff_isUnit_det _).mp hPos.isUnit
  have hC : C = -(Iγ⁻¹ * Q) := ou_C_eq hDm hβ hγ hH hM
  have htr : (0 : ℝ) =
      -trace (A * P) - trace (P * A)
        + γ * trace (C + Cᵀ)
        + (2 * Dm) * (d : ℝ)
        + 2 * trace Q := by
    have ht := congr_arg trace hM.lag
    -- Unfold `A` and expand `trace (γ • (C+Cᵀ))` to the form `simp` produces,
    -- then pack it back (module exposure blocks some defeq).
    have hpack : γ * trace C + γ * trace C = γ * trace (C + Cᵀ) := by
      rw [trace_add, trace_transpose]
      ring
    have h1 : trace ((2 * Dm) • (1 : Matrix (Fin d) (Fin d) ℝ)) = (2 * Dm) * (d : ℝ) := by
      rw [trace_smul, trace_one_fin, smul_eq_mul]
    have h2 : trace ((2 : ℝ) • Q) = 2 * trace Q := by
      rw [trace_smul, smul_eq_mul]
    have ht' : (0 : ℝ) =
        -trace (A * P) - trace (P * A)
          + (γ * trace C + γ * trace C)
          + (2 * Dm) * (d : ℝ) + 2 * trace Q := by
      simpa [trace_zero, trace_add, trace_neg, h1, h2, A] using ht
    rw [hpack] at ht'
    exact ht'
  have hcomm : trace (A * P) = trace (P * A) := trace_mul_comm _ _
  have hCsym : trace (C + Cᵀ) = 2 * trace C := by
    rw [trace_add, trace_transpose, two_mul]
  have hCtr : trace C = -trace (Iγ⁻¹ * Q) := by
    rw [hC, trace_neg]
  have hAP : trace (A * P) = Dm * (d : ℝ) + trace Q - γ * trace (Iγ⁻¹ * Q) := by
    rw [hcomm, hCsym, hCtr] at htr
    linarith
  have hAPtr : trace (A * P) = (Dm * β) * trace (H * P) := by
    have : A = (Dm * β) • H := rfl
    rw [this, smul_mul, trace_smul, smul_eq_mul]
  have hid : Iγ⁻¹ * Iγ = 1 := nonsing_inv_mul Iγ hU
  have hmat : Q - γ • (Iγ⁻¹ * Q) = Iγ⁻¹ * A * Q := by
    have hsp : Iγ⁻¹ * Iγ * Q = Q := by rw [hid, one_mul]
    have hI : Iγ = A + γ • (1 : Matrix (Fin d) (Fin d) ℝ) := rfl
    have hsplit : Iγ⁻¹ * A * Q + γ • (Iγ⁻¹ * Q) = Q := by
      have h1 : Iγ⁻¹ * (A + γ • (1 : Matrix (Fin d) (Fin d) ℝ)) * Q = Q := by
        rw [← hI, hsp]
      have h2 :
          (Iγ⁻¹ * A) * Q + (Iγ⁻¹ * (γ • (1 : Matrix (Fin d) (Fin d) ℝ))) * Q = Q := by
        rw [mul_add, add_mul] at h1
        exact h1
      have hsmul : (Iγ⁻¹ * (γ • (1 : Matrix (Fin d) (Fin d) ℝ))) * Q = γ • (Iγ⁻¹ * Q) := by
        calc
          (Iγ⁻¹ * (γ • (1 : Matrix (Fin d) (Fin d) ℝ))) * Q
              = (γ • (Iγ⁻¹ * (1 : Matrix (Fin d) (Fin d) ℝ))) * Q := by
                rw [mul_smul_comm]
            _ = (γ • Iγ⁻¹) * Q := by rw [mul_one]
            _ = γ • (Iγ⁻¹ * Q) := by rw [smul_mul]
      have hA : (Iγ⁻¹ * A) * Q = Iγ⁻¹ * A * Q := by rw [mul_assoc]
      rw [hA, hsmul] at h2
      exact h2
    exact (eq_sub_of_add_eq hsplit).symm
  have hrest : trace Q - γ * trace (Iγ⁻¹ * Q) = trace (Iγ⁻¹ * A * Q) := by
    have := congr_arg trace hmat
    simpa [trace_sub, trace_smul, smul_eq_mul] using this
  have hmain : (Dm * β) * trace (H * P) = Dm * (d : ℝ) + trace (Iγ⁻¹ * A * Q) := by
    have := hAP
    rw [add_sub_assoc, hrest] at this
    rw [← hAPtr, this]
  have hAas : Iγ⁻¹ * A * Q = (Dm * β) • (Iγ⁻¹ * H * Q) := by
    have : A = (Dm * β) • H := rfl
    rw [this, mul_smul_comm, smul_mul]
  have htrA : trace (Iγ⁻¹ * A * Q) = (Dm * β) * trace (Iγ⁻¹ * H * Q) := by
    rw [hAas, trace_smul, smul_eq_mul]
  have hcycle : trace (Iγ⁻¹ * H * Q) = trace (H * Iγ⁻¹ * Q) :=
    trace_mul₃_herm hPos.inv.isHermitian hH.isHermitian hQ
  calc
    (1 / 2) * trace (H * P)
        = ((Dm * β) * trace (H * P)) / (2 * Dm * β) := by
          field_simp [hDm.ne', hβ.ne']
    _ = (Dm * (d : ℝ) + (Dm * β) * trace (Iγ⁻¹ * H * Q)) / (2 * Dm * β) := by
          rw [hmain, htrA]
    _ = (d : ℝ) / (2 * β) + (1 / 2) * trace (Iγ⁻¹ * H * Q) := by
          field_simp [hDm.ne', hβ.ne']
    _ = (d : ℝ) / (2 * β) + (1 / 2) * trace (H * Iγ⁻¹ * Q) := by
          rw [hcycle]

/-- **DS1(b).**  Brownian world: `d/(2β) + Tr(Q)/(2β D_m)`.  Independent of `H`. -/
theorem bm_excess {Dm β : ℝ} {H Q P : Matrix (Fin d) (Fin d) ℝ}
    (hDm : 0 < Dm) (hβ : 0 < β) (_hH : H.PosDef)
    (hM : BMMoments Dm β H Q P) :
    (1 / 2) * trace (H * P) =
      (d : ℝ) / (2 * β) + trace Q / (2 * β * Dm) := by
  set A := driftMatrix Dm β H
  have htr : (0 : ℝ) =
      -trace (A * P) - trace (P * A)
        + (2 * Dm) * (d : ℝ) + 2 * trace Q := by
    have ht := congr_arg trace hM.lag
    have h1 : trace ((2 * Dm) • (1 : Matrix (Fin d) (Fin d) ℝ)) = (2 * Dm) * (d : ℝ) := by
      rw [trace_smul, trace_one_fin, smul_eq_mul]
    have h2 : trace ((2 : ℝ) • Q) = 2 * trace Q := by
      rw [trace_smul, smul_eq_mul]
    simpa [trace_zero, trace_add, trace_neg, h1, h2] using ht
  have hcomm : trace (A * P) = trace (P * A) := trace_mul_comm _ _
  have hAP : trace (A * P) = Dm * (d : ℝ) + trace Q := by
    rw [hcomm] at htr
    linarith
  have hAPtr : trace (A * P) = (Dm * β) * trace (H * P) := by
    have : A = (Dm * β) • H := rfl
    rw [this, smul_mul, trace_smul, smul_eq_mul]
  have hmain : (Dm * β) * trace (H * P) = Dm * (d : ℝ) + trace Q := by
    rw [← hAPtr, hAP]
  field_simp [hDm.ne', hβ.ne']
  linarith

/-- **DS1(b), isotropic case.**  `Q = D I` gives `d/(2β)(1 + D/D_m)`. -/
theorem bm_excess_isotropic {Dm β D : ℝ} {H P : Matrix (Fin d) (Fin d) ℝ}
    (hDm : 0 < Dm) (hβ : 0 < β) (hH : H.PosDef)
    (hM : BMMoments Dm β H (D • (1 : Matrix (Fin d) (Fin d) ℝ)) P) :
    (1 / 2) * trace (H * P) = ((d : ℝ) / (2 * β)) * (1 + D / Dm) := by
  have h := bm_excess hDm hβ hH hM
  have hQ : trace (D • (1 : Matrix (Fin d) (Fin d) ℝ)) = D * (d : ℝ) := by
    rw [trace_smul, trace_one_fin, smul_eq_mul]
  rw [h, hQ]
  field_simp [hDm.ne', hβ.ne']

/-- **DS1(d), static reduction.**  `Q = 0` recovers the SA1b excess `d/(2β)`. -/
theorem bm_excess_static {Dm β : ℝ} {H P : Matrix (Fin d) (Fin d) ℝ}
    (hDm : 0 < Dm) (hβ : 0 < β) (hH : H.PosDef)
    (hM : BMMoments Dm β H 0 P) :
    (1 / 2) * trace (H * P) = (d : ℝ) / (2 * β) := by
  have h := bm_excess hDm hβ hH hM
  simpa [trace_zero] using h

/-- **DS1(c), mean-lag term.**  If the mean lag satisfies `A μ = -v`
with `A = D_m β H`, then `½ μᵀ H μ = vᵀ H⁻¹ v / (2 β² D_m²)`.  The
fluctuation contribution `d/(2β)` is SA1b / `Equipartition` and is
added outside this identity. -/
theorem velocity_mean_excess {Dm β : ℝ} {H : Matrix (Fin d) (Fin d) ℝ}
    {v μ : Fin d → ℝ} (hDm : 0 < Dm) (hβ : 0 < β) (hH : H.PosDef)
    (hmean : driftMatrix Dm β H *ᵥ μ = -v) :
    (1 / 2) * (μ ⬝ᵥ (H *ᵥ μ)) =
      (v ⬝ᵥ (H⁻¹ *ᵥ v)) / (2 * β ^ 2 * Dm ^ 2) := by
  have hc : Dm * β ≠ 0 := mul_ne_zero hDm.ne' hβ.ne'
  have hHdet : IsUnit H.det := (isUnit_iff_isUnit_det _).mp hH.isUnit
  have hApos : (driftMatrix Dm β H).PosDef := driftMatrix_posDef hDm hβ hH
  have hU : IsUnit (driftMatrix Dm β H).det := (isUnit_iff_isUnit_det _).mp hApos.isUnit
  have hscale : (Dm * β) • (H *ᵥ μ) = -v := by
    have : driftMatrix Dm β H *ᵥ μ = ((Dm * β) • H) *ᵥ μ := rfl
    rw [this] at hmean
    rwa [smul_mulVec] at hmean
  have hHμ : H *ᵥ μ = -((Dm * β)⁻¹ • v) := by
    have := congr_arg (fun x => (Dm * β)⁻¹ • x) hscale
    -- (Dm*β)⁻¹ • ((Dm*β) • (H *ᵥ μ)) = (Dm*β)⁻¹ • (-v)
    rw [inv_smul_smul₀ hc] at this
    simpa [smul_neg] using this
  have hAinv : (driftMatrix Dm β H)⁻¹ = (Dm * β)⁻¹ • H⁻¹ := by
    have hL : driftMatrix Dm β H * ((Dm * β)⁻¹ • H⁻¹) = 1 := by
      simp only [driftMatrix]
      calc
        ((Dm * β) • H) * ((Dm * β)⁻¹ • H⁻¹)
            = (Dm * β) • (H * ((Dm * β)⁻¹ • H⁻¹)) := by rw [smul_mul]
          _ = (Dm * β) • ((Dm * β)⁻¹ • (H * H⁻¹)) := by rw [Matrix.mul_smul]
          _ = ((Dm * β) * (Dm * β)⁻¹) • (H * H⁻¹) := by rw [smul_smul]
          _ = (1 : ℝ) • (H * H⁻¹) := by rw [mul_inv_cancel₀ hc]
          _ = H * H⁻¹ := by rw [one_smul]
          _ = 1 := mul_nonsing_inv H hHdet
    exact inv_eq_right_inv hL
  have hμ : μ = -((driftMatrix Dm β H)⁻¹ *ᵥ v) := by
    have h1 := mulVec_mulVec μ ((driftMatrix Dm β H)⁻¹) (driftMatrix Dm β H)
    -- h1 : A⁻¹ *ᵥ A *ᵥ μ = (A⁻¹ * A) *ᵥ μ
    have h2 := h1.symm
    rw [nonsing_inv_mul _ hU, one_mulVec] at h2
    -- h2 : μ = A⁻¹ *ᵥ A *ᵥ μ
    rw [hmean] at h2
    simpa [mulVec_neg] using h2
  -- Substitute `H *ᵥ μ` first (it contains `μ`), then `μ`.
  have hleft : μ ⬝ᵥ (H *ᵥ μ) =
      ((Dm * β)⁻¹ • (H⁻¹ *ᵥ v)) ⬝ᵥ ((Dm * β)⁻¹ • v) := by
    calc
      μ ⬝ᵥ (H *ᵥ μ)
          = μ ⬝ᵥ (-((Dm * β)⁻¹ • v)) := by rw [hHμ]
        _ = (-((driftMatrix Dm β H)⁻¹ *ᵥ v)) ⬝ᵥ (-((Dm * β)⁻¹ • v)) := by
            rw [hμ]
        _ = ((driftMatrix Dm β H)⁻¹ *ᵥ v) ⬝ᵥ ((Dm * β)⁻¹ • v) := by
            rw [neg_dotProduct, dotProduct_neg, neg_neg]
        _ = ((Dm * β)⁻¹ • (H⁻¹ *ᵥ v)) ⬝ᵥ ((Dm * β)⁻¹ • v) := by
            rw [hAinv, smul_mulVec]
  have hright :
      ((Dm * β)⁻¹ • (H⁻¹ *ᵥ v)) ⬝ᵥ ((Dm * β)⁻¹ • v) =
        (Dm * β)⁻¹ * (Dm * β)⁻¹ * ((H⁻¹ *ᵥ v) ⬝ᵥ v) := by
    rw [smul_dotProduct, dotProduct_smul]
    simp [smul_eq_mul]
    ring
  have hsym : (H⁻¹ *ᵥ v) ⬝ᵥ v = v ⬝ᵥ (H⁻¹ *ᵥ v) := dotProduct_comm _ _
  rw [hleft, hright, hsym]
  field_simp [hDm.ne', hβ.ne']

/-- **DS1(d), exact remainder to the fast-γ floor.**
`½ Tr[H (A+γI)⁻¹ Q] - ½ Tr[H (Q/γ)] = -½ Tr[H (A+γI)⁻¹ A (Q/γ)]`. -/
theorem ou_excess_fast_remainder {Dm β γ : ℝ} {H Q : Matrix (Fin d) (Fin d) ℝ}
    (hDm : 0 < Dm) (hβ : 0 < β) (hγ : 0 < γ) (hH : H.PosDef) :
    let A := driftMatrix Dm β H
    let Iγ := A + γ • (1 : Matrix (Fin d) (Fin d) ℝ)
    (1 / 2) * trace (H * Iγ⁻¹ * Q)
      - (1 / 2) * trace (H * (γ⁻¹ • Q))
      = - (1 / 2) * trace (H * Iγ⁻¹ * A * (γ⁻¹ • Q)) := by
  intro A Iγ
  have hPos : Iγ.PosDef := driftMatrix_add_posDef hDm hβ hγ.le hH
  have hU : IsUnit Iγ.det := (isUnit_iff_isUnit_det _).mp hPos.isUnit
  have hid : Iγ⁻¹ * Iγ = 1 := nonsing_inv_mul Iγ hU
  have hIγQ : Iγ * (γ⁻¹ • Q) = A * (γ⁻¹ • Q) + Q := by
    simp only [Iγ, add_mul]
    have h1 : (γ • (1 : Matrix (Fin d) (Fin d) ℝ)) * (γ⁻¹ • Q) = Q := by
      rw [smul_mul, one_mul, smul_smul, mul_inv_cancel₀ hγ.ne', one_smul]
    rw [h1]
  have hdiff : Iγ⁻¹ * Q - γ⁻¹ • Q = -((Iγ⁻¹ * A) * (γ⁻¹ • Q)) := by
    have h := congr_arg (fun M => Iγ⁻¹ * M) hIγQ
    -- Iγ⁻¹ * (Iγ * (γ⁻¹ • Q)) = Iγ⁻¹ * (A * (γ⁻¹ • Q) + Q)
    have h' : γ⁻¹ • Q = (Iγ⁻¹ * A) * (γ⁻¹ • Q) + Iγ⁻¹ * Q := by
      rw [← mul_assoc, hid, one_mul, mul_add] at h
      simpa [mul_assoc] using h
    nth_rw 1 [h']
    abel
  have htr := congr_arg (fun M => (1 / 2 : ℝ) * trace (H * M)) hdiff
  simpa [mul_sub, mul_neg, trace_sub, trace_neg, mul_assoc] using htr

end DriftSelection
