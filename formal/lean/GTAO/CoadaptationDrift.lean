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
public import Mathlib.Tactic.FinCases

/-!
# CA7: LQ drift plus co-adaptation

`theory/COADAPTATION.md` Theorem CA7, CLAIM_MAP U11.

The stationary covariance is an input, through the Lyapunov equation
`V K Cov + Cov Kᵀ V = 2 V + 2 Q`.  From it we prove the exact potential-part
excess `½(d + Tr(V⁻¹ Q))` for any antisymmetric coupling.  CA7 (4) is the
note's s8b datum: the Lyapunov equation and the party-wise drift regrets
are checked on that covariance, and they are not the naive uncoupled
values.

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

/-- Entrywise 2×2 matrix product, used because `Matrix` multiplication is
not exposed as a function in Lean 4.37. -/
def mul2 (A B : Fin 2 → Fin 2 → ℝ) (i j : Fin 2) : ℝ :=
  A i 0 * B 0 j + A i 1 * B 1 j

/-! The exact s8b datum of `tools/coadaptation_checks.py`
`s8b_lq_drift_regret_negative` and `theory/COADAPTATION.md` around the
LQ-drift remark: `S = [[2, 9/10], [9/10, 1]]`, `w = [1, 2]`, `γ = 5`,
`β = [5, 5/2]`, `V = diag(1, 2/5)`, `Q = diag(3/10, 3/10)`,
`M_{ij} = S_{ij} w_i / γ`, and the unique symmetric Lyapunov solution of
`V S P + P S V = 2V + 2Q`. -/

noncomputable def s8bS (i j : Fin 2) : ℝ :=
  if i = 0 then (if j = 0 then (2 : ℝ) else 9 * (10 : ℝ)⁻¹)
  else (if j = 0 then 9 * (10 : ℝ)⁻¹ else 1)

noncomputable def s8bW (i : Fin 2) : ℝ := if i = 0 then 1 else 2

noncomputable def s8bGamma : ℝ := 5

noncomputable def s8bBeta (i : Fin 2) : ℝ := s8bGamma * (s8bW i)⁻¹

noncomputable def s8bV (i j : Fin 2) : ℝ :=
  if i = j then (if i = 0 then 1 else 2 * (5 : ℝ)⁻¹) else 0

noncomputable def s8bQ (i j : Fin 2) : ℝ :=
  if i = j then 3 * (10 : ℝ)⁻¹ else 0

/-- Unique symmetric solution of the s8b Lyapunov equation. -/
noncomputable def s8bP (i j : Fin 2) : ℝ :=
  if i = 0 ∧ j = 0 then 2323 * (1904 : ℝ)⁻¹
  else if i = 0 ∧ j = 1 then -(603 * (476 : ℝ)⁻¹)
  else if i = 1 ∧ j = 0 then -(603 * (476 : ℝ)⁻¹)
  else 13757 * (4760 : ℝ)⁻¹

/-- The coupling row of party `i`: `M_{ij} = S_{ij} w_i / γ`. -/
noncomputable def s8bM (i j : Fin 2) : ℝ :=
  s8bS i j * s8bW i * s8bGamma⁻¹

/-- `g_iᵀ P g_i` with `g_i` the `i`-th row of `M`. -/
noncomputable def s8bQuad (i : Fin 2) : ℝ :=
  s8bM i 0 * (s8bP 0 0 * s8bM i 0 + s8bP 0 1 * s8bM i 1) +
    s8bM i 1 * (s8bP 1 0 * s8bM i 0 + s8bP 1 1 * s8bM i 1)

/-- Drift regret `½ (g_iᵀ P g_i) / M_{ii}` of party `i`. -/
noncomputable def s8bRegret (i : Fin 2) : ℝ :=
  (2 : ℝ)⁻¹ * s8bQuad i * (s8bM i i)⁻¹

/-- Naive uncoupled regret `½ (1/β_i) (1 + Q_{ii}/V_{ii})`. -/
noncomputable def s8bNaive (i : Fin 2) : ℝ :=
  (2 : ℝ)⁻¹ * (s8bBeta i)⁻¹ * (1 + s8bQ i i * (s8bV i i)⁻¹)

/-- The s8b covariance satisfies the Lyapunov equation
`V S P + P S V = 2V + 2Q`. -/
theorem s8b_lyapunov (i j : Fin 2) :
    mul2 s8bV (mul2 s8bS s8bP) i j + mul2 (mul2 s8bP s8bS) s8bV i j
      = (2 : ℝ) * s8bV i j + (2 : ℝ) * s8bQ i j := by
  fin_cases i <;> fin_cases j <;>
    (simp [mul2, s8bS, s8bV, s8bP, s8bQ]; norm_num)

theorem s8b_regret_party0 : s8bRegret 0 = 10643 * (80000 : ℝ)⁻¹ := by
  simp [s8bRegret, s8bQuad, s8bM, s8bS, s8bW, s8bGamma, s8bP]; norm_num

theorem s8b_regret_party1 : s8bRegret 1 = 2557 * (8000 : ℝ)⁻¹ := by
  simp [s8bRegret, s8bQuad, s8bM, s8bS, s8bW, s8bGamma, s8bP]; norm_num

theorem s8b_naive_party0 : s8bNaive 0 = 13 * (100 : ℝ)⁻¹ := by
  simp [s8bNaive, s8bBeta, s8bGamma, s8bW, s8bQ, s8bV]; norm_num

theorem s8b_naive_party1 : s8bNaive 1 = 7 * (20 : ℝ)⁻¹ := by
  simp [s8bNaive, s8bBeta, s8bGamma, s8bW, s8bQ, s8bV]; norm_num

/-- Static (no-drift) regrets recover the Boltzmann values `1/(2β_i)`. -/
theorem s8b_static_regret :
    (2 : ℝ)⁻¹ * (s8bBeta 0)⁻¹ = (10 : ℝ)⁻¹ ∧
      (2 : ℝ)⁻¹ * (s8bBeta 1)⁻¹ = (5 : ℝ)⁻¹ := by
  constructor
  · simp [s8bBeta, s8bGamma, s8bW]; norm_num
  · simp [s8bBeta, s8bGamma, s8bW]

/-- **CA7 (4), negative finding (s8b).**  On the note's s8b covariance,
party-wise drift regrets are not the naive uncoupled values:
`10643/80000 ≠ 13/100` and `2557/8000 ≠ 7/20`. -/
theorem ca7_regret_not_naive :
    s8bRegret 0 ≠ s8bNaive 0 ∧ s8bRegret 1 ≠ s8bNaive 1 := by
  rw [s8b_regret_party0, s8b_naive_party0, s8b_regret_party1, s8b_naive_party1]
  constructor <;> norm_num

end CoadaptationDrift
