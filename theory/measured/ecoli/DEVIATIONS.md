# ECOLI-MEM deviations from the locked files

1. **Riccati cross-check (8:22 AM ET, first run).** The locked `arm_a_poles_riccati` integrated the filter Riccati
   equation by explicit Euler; at the box centre r ≈ 10⁻⁸ s the equation is stiff and it overflowed (NaN) before any
   output was written. Replaced by `scipy.linalg.solve_continuous_are` for the same equation. This is an independent
   check of the arm-A poles only; no prediction formula, input, range or verdict rule changed. The locked version is in
   git at commit 6903de9.
