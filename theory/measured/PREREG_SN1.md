# SN1 preregistration: Model S+ (store noise E1, speed-priced upkeep E2) on NEW systems

Written Friday 20 November 2026 (commit time is the record), after `theory/STORE_NOISE.md` was derived and **before
searching for or reading any noise-scaling, adaptation-time or input-statistics data for any system named below**.
Disclosure: I have general background knowledge that these systems adapt (orders of magnitude of seconds to minutes), but
I have not looked up or computed s, λ or τ for any of them in this project. E. coli chemotaxis is excluded (its data shaped
the extension).

## Quantities (all on the same store of the same system)
- τ: the store's memory (adaptation time, fitted slow time constant of the response kernel).
- λ: rate of the input the store tracks, measured in the organism's own conditions (1/correlation time of the input as
  the organism experiences it, e.g. along its own path).
- s: d ln σ_store / d ln τ, the store's own output-noise amplitude against its memory, measured across strains,
  manipulations or natural cell-to-cell variation (same estimator family as F2: reduced-major-axis log-log slope with
  bootstrap 95% CI when errors are in both variables; OLS when τ is set by the experimenter).
- Low-SNR premise: the store's own noise dominates read noise of the input (premise check: the noise share attributable to
  the store ≥ 50%, from a knockout or noise split like Colin et al. 2017 or Keegstra et al. 2017). If the premise fails or
  cannot be checked, the system is **INVALID** for SN1.

## Predictions (one-sided, because E2's price can only lengthen memory)
Let x\* = (1 − s)/s (E1-a). Use the CIs of λτ and of x\* (propagated from s).
- **PASS** iff the whole CI of λτ ≥ x\*/2 (lower end of x\*'s CI).
- **FAIL** iff the whole CI of λτ < x\*/3 (upper end of x\*'s CI). A FAIL refutes E1+E2 for that system's class unless a
  diagnosis finds a premise failure (then INVALID, reported, and any new prediction preregistered fresh).
- Otherwise **NEITHER**.
- **Upper side, only where upkeep is shown not to depend on speed** (h1 = 0, e.g. no dissipation scaling with rate):
  PASS also requires λτ ≤ 2·x\* (upper end of CI); without that evidence the upper side is UNTESTED.
- **s undetermined** (no source gives noise and τ at ≥ 2 values): UNTESTED.

## Rivals (scored by the same CIs)
- R1 Model S, exogenous noise: λτ ≤ 1 (the store at or faster than its mode).
- R2 "set at the world's time scale": λτ = 1 within ×2.
SN1 discriminates only where x\*/2 > 2 (s < 0.2) or x\*·2 < 1/2 (s > 0.8); otherwise any PASS is
**PASS-NONDISCRIMINATING** and is reported as such.

## Candidate systems, named before looking (first two with usable data get run; order fixed now)
1. Dictyostelium discoideum cAMP chemotaxis (adaptation of the Ras/PI3K response).
2. Bacillus subtilis chemotaxis (methylation and CheV/CheC-CheD adaptation).
3. Saccharomyces cerevisiae osmotic adaptation (Hog1) or pheromone response.
4. Drosophila or vertebrate photoreceptor light adaptation.
5. Caenorhabditis elegans AWC/ASH sensory adaptation.
6. Marine bacteria with run-reverse-flick chemotaxis (e.g. Vibrio).
7. Human-scale: an organisation's forecast-revision memory against its demand-signal correlation time (requires s from
   staff-turnover or record-churn noise; expected UNTESTED).

## Kill condition for the extension (fixed now)
E1+E2 are refuted as theory (not just on one setup) if two or more systems from different classes FAIL after diagnosis
and a preregistered rerun, with no premise failure found.
