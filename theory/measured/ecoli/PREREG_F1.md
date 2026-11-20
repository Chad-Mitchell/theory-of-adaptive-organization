# ECOLI-MEM follow-up F1 preregistration: does the best memory shorten in steeper gradients?

Written Friday 20 November 2026, about 8:20 AM ET (commit c402814), after the locked ECOLI-MEM run (`results.json`) and before searching
for or reading any data on chemotactic performance versus adaptation time. Locked by the commit that adds this file.

## Why (the diagnosis that motivates it; see ../README.md §E.4)
Arms A and B failed: both treat the binding noise as exogenous read noise. The data say the binding noise is the memory
store's own (τn/τ2 = 1.19; Berg–Purcell counting noise is ≤ 2×10⁻⁴ of the kinase-noise variance). For a store whose
noise has a fixed stationary variance (a copy-number limit, arm C), the input-referred noise falls as 1/τ², so the optimal
memory is long and falls with the signal strength. In the locked arm-C model at Mattingly's measured inputs
the optimum is τ\*(g) ≈ 6.6 s × (g / 1 mm⁻¹)^−0.97 over 0.01–10 mm⁻¹ (62 s at 0.1, 16 s at 0.4 mm⁻¹; measured τ2 = 9.9 s
would be optimal at g\* ≈ 0.65 mm⁻¹). Arm C was a diagnostic in the first prereg; this file turns it into a fresh,
falsifiable prediction. It does not rescue the first test: ECOLI-MEM arms A and B stay FAIL.

## Prediction (theory, arm-C noise model) and rival
- **P (theory):** across gradient steepness, the adaptation time that maximizes chemotactic performance falls with
  steepness, with log-slope d ln τ_best / d ln g in [−1.5, −0.5] (point value −0.97).
- **R1 (rival, "set at" the world scale):** τ_best ≈ τ_v independent of g (log-slope in [−0.2, 0.2]).
- **R2 (rival, opposite sign):** τ_best rises with g.

## Data rule
Any published measurement or published, data-calibrated simulation of E. coli chemotactic performance (drift speed or
accumulation in a static gradient) for cells or strains of different adaptation times, in at least two gradient
steepnesses. Measurements outrank simulations; a simulation-only source can give at most "consistent in model".

## Verdict
- **PASS** iff the best adaptation time is shorter in the steeper gradient and, where at least three steepnesses or a
  quantitative optimum are reported, the log-slope is within [−1.5, −0.5].
- **FAIL (on this proxy)** iff the best adaptation time is longer in the steeper gradient, or the log-slope is in [−0.2, 0.2].
- **INCONCLUSIVE** otherwise; **UNTESTED** if no source meets the data rule.
- Proxy caveat fixed now: drift speed is not the theory's squared error of u; the mapping (drift ∝ correlation of the
  tumble decision with u) is monotone in the explained variance, so the sign is a fair test and the slope a weaker one.
