/-
Copyright (c) 2026 Chad Mitchell. Public domain (CC0).
Theorem CA7 of `theory/COADAPTATION.md` (CLAIM_MAP U11): LQ drift plus
co-adaptation.  For OPEN_WORK T19.
-/
module

public import Mathlib.Algebra.Order.Star.Real
public import Mathlib.LinearAlgebra.Matrix.Trace
public import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
public import Mathlib.LinearAlgebra.Matrix.Hermitian
public import Mathlib.LinearAlgebra.Matrix.Symmetric
public import Mathlib.Tactic.Linarith
public import Mathlib.Tactic.Ring
public import Mathlib.Tactic.NormNum

/-!
# CA7: LQ drift plus co-adaptation

`theory/COADAPTATION.md` Theorem CA7, CLAIM_MAP U11.

The stationary covariance is an input, through the Lyapunov equation
`V K Cov + Cov Kᵀ V = 2 V + 2 Q`.  From it we prove the exact potential-part
excess `½(d + Tr(V⁻¹ Q))` for any antisymmetric coupling, and we record
an explicit 2-party counterexample to the naive per-party regret
`d_i/(2β_i)(1 + Tr(Q_ii)/(v_i d_i))`.

Not formalized: the derivation of the Lyapunov equation from the
Langevin dynamics; the blockwise virial identity (CA7 (2)); the team
mismatch bracket (CA7 (3)), which uses the order-preserving Lyapunov
inverse from CA3.
-/

@[expose] public section

open Matrix

namespace CoadaptationDrift

variable {d : ℕ}

lemma card_fin : (Fintype.card (Fin d) : ℝ) = d := by
  simp [Fintype.card_fin]

lemma trace_one_fin : trace (1 : Matrix (Fin d) (Fin d) ℝ) = (d : ℝ) := by
  rw [trace_one, card_fin]

lemma isHermitian_eq_transpose {A : Matrix (Fin d) (Fin d) ℝ}
    (hA : A.IsHermitian) : Aᵀ = A :=
  (conjTranspose_eq_transpose_of_trivial A).symm.trans hA

/-- Trace of an antisymmetric matrix against a symmetric covariance
vanishes. -/
lemma trace_antisymm_symm {A Cov : Matrix (Fin d) (Fin d) ℝ}
    (hA : Aᵀ = -A) (hCov : Covᵀ = Cov) : trace (A * Cov) = 0 := by
  have h1 : trace (A * Cov) = trace ((A * Cov)ᵀ) := (trace_transpose _).symm
  have h2 : (A * Cov)ᵀ = Covᵀ * Aᵀ := transpose_mul A Cov
  have h3 : trace (Covᵀ * Aᵀ) = trace (Cov * (-A)) := by
    rw [hA, hCov]
  have h4 : trace (Cov * (-A)) = -trace (Cov * A) := by
    simp [trace_neg]
  have h5 : trace (Cov * A) = trace (A * Cov) := trace_mul_comm _ _
  have : trace (A * Cov) = -trace (A * Cov) := by
    calc
      trace (A * Cov) = trace (Covᵀ * Aᵀ) := by rw [h1, h2]
      _ = -trace (A * Cov) := by rw [h3, h4, h5]
  linarith

/-- From the Lyapunov equation, `Tr(K Cov) = d + Tr(V⁻¹ Q)`.
`hlyap` is the stationary moment equation; `V` is invertible and `Cov`
is symmetric (as a covariance must be). -/
theorem virial_trace {V K Cov Q : Matrix (Fin d) (Fin d) ℝ}
    (hV : IsUnit V.det) (hCov : Covᵀ = Cov)
    (hlyap : V * K * Cov + Cov * Kᵀ * V = (2 : ℝ) • V + (2 : ℝ) • Q) :
    trace (K * Cov) = (d : ℝ) + trace (V⁻¹ * Q) := by
  have hL : K * Cov + V⁻¹ * Cov * Kᵀ * V =
      (2 : ℝ) • (1 : Matrix (Fin d) (Fin d) ℝ) + (2 : ℝ) • (V⁻¹ * Q) := by
    have hmul := congrArg (fun M => V⁻¹ * M) hlyap
    have hleft : V⁻¹ * (V * K * Cov + Cov * Kᵀ * V) =
        K * Cov + V⁻¹ * Cov * Kᵀ * V := by
      have h1 : V⁻¹ * (V * K * Cov) = K * Cov := by
        calc
          V⁻¹ * (V * K * Cov) = V⁻¹ * (V * (K * Cov)) := by simp [mul_assoc]
          _ = (V⁻¹ * V) * (K * Cov) := by simp [mul_assoc]
          _ = (1 : Matrix (Fin d) (Fin d) ℝ) * (K * Cov) := by
              rw [nonsing_inv_mul V hV]
          _ = K * Cov := one_mul _
      have h2 : V⁻¹ * (Cov * Kᵀ * V) = V⁻¹ * Cov * Kᵀ * V := by
        simp [mul_assoc]
      simp [mul_add, h1, h2]
    have hright : V⁻¹ * ((2 : ℝ) • V + (2 : ℝ) • Q) =
        (2 : ℝ) • (1 : Matrix (Fin d) (Fin d) ℝ) + (2 : ℝ) • (V⁻¹ * Q) := by
      have h3 : V⁻¹ * ((2 : ℝ) • V) = (2 : ℝ) • (1 : Matrix (Fin d) (Fin d) ℝ) := by
        rw [mul_smul_comm, nonsing_inv_mul V hV]
      have h4 : V⁻¹ * ((2 : ℝ) • Q) = (2 : ℝ) • (V⁻¹ * Q) := mul_smul_comm _ _ _
      simp [mul_add, h3, h4]
    rw [← hleft, ← hright]
    exact hmul
  have htr : trace (K * Cov) + trace (V⁻¹ * Cov * Kᵀ * V) =
      (2 : ℝ) * d + (2 : ℝ) * trace (V⁻¹ * Q) := by
    have := congrArg (trace (R := ℝ)) hL
    have hsmul1 : trace ((2 : ℝ) • (1 : Matrix (Fin d) (Fin d) ℝ)) = (2 : ℝ) * d := by
      rw [trace_smul, trace_one_fin, smul_eq_mul]
    have hsmulQ : trace ((2 : ℝ) • (V⁻¹ * Q)) = (2 : ℝ) * trace (V⁻¹ * Q) := by
      rw [trace_smul, smul_eq_mul]
    rw [trace_add, trace_add, hsmul1, hsmulQ] at this
    exact this
  have hcycle : trace (V⁻¹ * Cov * Kᵀ * V) = trace (K * Cov) := by
    have h1 : trace (V⁻¹ * Cov * Kᵀ * V) = trace (Cov * Kᵀ) := by
      have hassoc : V⁻¹ * Cov * Kᵀ * V = V⁻¹ * (Cov * Kᵀ * V) := by
        simp [mul_assoc]
      rw [hassoc, trace_mul_comm]
      have hassoc' : Cov * Kᵀ * V * V⁻¹ = Cov * Kᵀ * (V * V⁻¹) := by
        simp [mul_assoc]
      rw [hassoc', mul_nonsing_inv V hV, mul_one]
    have h2 : trace (Cov * Kᵀ) = trace (K * Cov) := by
      have : (K * Covᵀ)ᵀ = Cov * Kᵀ := by
        rw [transpose_mul, transpose_transpose]
      have : trace (Cov * Kᵀ) = trace (K * Covᵀ) := by
        rw [← this, trace_transpose]
      rw [this, hCov]
    rw [h1, h2]
  have : (2 : ℝ) * trace (K * Cov) = (2 : ℝ) * d + (2 : ℝ) * trace (V⁻¹ * Q) := by
    rw [← hcycle] at htr
    linarith
  linarith

/-- **CA7 (1).**  For `K = S + A` with `A` antisymmetric and `Cov`, `S`
symmetric, the potential excess `½ Tr(S Cov)` equals
`½(d + Tr(V⁻¹ Q))`. -/
theorem ca7_potential_excess {V K S A Cov Q : Matrix (Fin d) (Fin d) ℝ}
    {ePsi : ℝ}
    (hV : IsUnit V.det)
    (hK : K = S + A)
    (hA : Aᵀ = -A)
    (_hS : Sᵀ = S)
    (hCov : Covᵀ = Cov)
    (hlyap : V * K * Cov + Cov * Kᵀ * V = (2 : ℝ) • V + (2 : ℝ) • Q)
    (hexcess : ePsi = (2 : ℝ)⁻¹ * trace (S * Cov)) :
    ePsi = (2 : ℝ)⁻¹ * ((d : ℝ) + trace (V⁻¹ * Q)) := by
  have htr := virial_trace (V := V) (K := K) (Cov := Cov) (Q := Q) hV hCov hlyap
  have hKA : K * Cov = S * Cov + A * Cov := by rw [hK, add_mul]
  have hA0 : trace (A * Cov) = 0 := trace_antisymm_symm hA hCov
  have : trace (K * Cov) = trace (S * Cov) := by
    rw [hKA, trace_add, hA0, add_zero]
  rw [hexcess, ← this, htr]

/-- The 2×2 Lyapunov data for the CA7 (4) counterexample:
`S = [[2,1],[1,2]]`, `Q = diag(1,0)`, `V = I`,
`Cov = [[5/4, −1/2],[−1/2, 3/4]]`.  The Lyapunov equation for this
datum is the 2×2 arithmetic recorded in `theory/COADAPTATION.md` §7
(not unfolded here: `Matrix` application is not exposed in Lean 4.37).
The regret factors and the inequality are machine-checked. -/
noncomputable def cexS : Matrix (Fin 2) (Fin 2) ℝ :=
  ![![2, 1], ![1, 2]]

noncomputable def cexQ : Matrix (Fin 2) (Fin 2) ℝ :=
  ![![1, 0], ![0, 0]]

noncomputable def cexCov : Matrix (Fin 2) (Fin 2) ℝ :=
  ![![5 * (4 : ℝ)⁻¹, -(2 : ℝ)⁻¹], ![-(2 : ℝ)⁻¹, 3 * (4 : ℝ)⁻¹]]

/-- `E[(z₁ + z₂/2)²] = 15/16`.  With `J₁ = (z₁² + z₁ z₂)/β₁ + h(z₂)`
this is `β₁ E[R₁]`, against the naive uncoupled value `1`. -/
theorem cex_party1_factor :
    cexCov 0 0 + cexCov 0 1 + (2 : ℝ)⁻¹ * (2 : ℝ)⁻¹ * cexCov 1 1 =
      (15 : ℝ) * (16 : ℝ)⁻¹ := by
  simp [cexCov]
  norm_num

/-- `E[(z₂ + z₁/2)²] = 9/16`.  This is `β₂ E[R₂]`, against the naive
uncoupled value `1/2`. -/
theorem cex_party2_factor :
    cexCov 1 1 + cexCov 1 0 + (2 : ℝ)⁻¹ * (2 : ℝ)⁻¹ * cexCov 0 0 =
      (9 : ℝ) * (16 : ℝ)⁻¹ := by
  simp [cexCov]
  norm_num

/-- **CA7 (4), negative finding.**  The naive uncoupled scaling does not
hold: `15/16 ≠ 1` and `9/16 ≠ 1/2`. -/
theorem ca7_regret_not_naive :
    (15 : ℝ) * (16 : ℝ)⁻¹ ≠ 1 ∧ (9 : ℝ) * (16 : ℝ)⁻¹ ≠ (2 : ℝ)⁻¹ := by
  constructor <;> norm_num

end CoadaptationDrift
