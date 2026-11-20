# Y4 preregistration: speed-priced upkeep (E2) vs slow habitat modes (H) for E. coli's remaining factor

Written Friday 20 November 2026 (commit time is the record), after `RESULTS_D.md` and **before searching for any
measurement of E. coli adaptation time across growth conditions**. I have read Ni et al. 2020 (benefit and motility
investment vary with carbon source) and Lan et al. 2012 (adaptation slows under de-energization) for other purposes; I do
not know of an adaptation-time measurement across carbon sources.

## Predictions
Across ≥ 3 growth conditions in one strain, with the chemotaxis benefit ordered by an independent measure (Ni et al. 2020
or the source's own growth-advantage data) and the adaptation time τ measured by FRET step response or a motor
assay (same method across conditions):
- **E2:** τ falls as the benefit rises: Spearman ρ(benefit, τ) < 0, and the ratio of τ between the lowest- and highest-
  benefit conditions ≥ 1.5.
- **H:** τ does not track benefit: |ln(τ_low-benefit/τ_high-benefit)| < ln 1.5.
- Verdict **E2 SUPPORTED** iff the E2 conditions hold; **H SUPPORTED** iff the H condition holds; otherwise **NEITHER**.
  **INVALID** if conditions differ in temperature or medium viscosity enough to change τ mechanically (Q10 confound)
  without a correction the source provides, or if τ falls with benefit only because CheR/CheB copy number changes
  with growth rate (then the result is reported but scored NEITHER, because it does not separate optimisation from mechanism).
- **UNTESTED** if no open source measures τ in ≥ 3 conditions.
