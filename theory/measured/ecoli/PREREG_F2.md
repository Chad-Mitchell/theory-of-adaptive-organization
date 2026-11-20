# ECOLI-MEM follow-up F2 preregistration: which noise model is E. coli's (the decisive diagnostic)

Written Friday 20 November 2026 (commit time is the record), after the ECOLI-MEM run and F1 prereg, **before searching for
or reading any data on how kinase-activity noise changes when the adaptation time is changed**.

## Why
The ECOLI-MEM miss turns on one unmeasured fact: how the memory store's own noise scales with the store's speed.
- **Arm B (store noise of fixed density, white into the store):** activity-noise variance σn² ∝ τ (the store integrates
  white noise for longer), so σn ∝ τ^{1/2} and the optimal memory ≈ τ_v ≈ 1.1 s (measured 9.9 s: FAIL).
- **Arm C (store noise of fixed stationary variance, a copy-number limit):** σn independent of τ, and the optimal memory is
  long and falls with gradient (16–62 s across 0.1–0.4 mm⁻¹; measured 9.9 s optimal at 0.65 mm⁻¹).

## Prediction rule
From any published measurement of kinase-activity (or CheY-P, or motor-bias) noise amplitude in E. coli strains or cells
whose adaptation time was changed (CheR/CheB expression, methylation-site mutants, or natural cell-to-cell variation), fit
the log-log slope s = d ln σn / d ln τ (or d ln Var / d ln τ halved).
- **Arm C supported** iff s ∈ [−0.2, 0.25]; **arm B supported** iff s ∈ [0.35, 0.65]; otherwise neither.
- **UNTESTED** if no source reports noise amplitude together with adaptation time across at least two values of τ.
- Mechanism caveat fixed now: changing CheR/CheB also changes the adapted activity a0 and the gain, so a source that holds
  a0 roughly fixed (or reports it) outranks one that does not.
