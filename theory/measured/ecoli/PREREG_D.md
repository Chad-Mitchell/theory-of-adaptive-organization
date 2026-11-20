# ECOLI-MEM follow-up D: the remaining factor of about 4 (preregistration)

Written Friday 20 November 2026 (commit time is the record), **before any script for these computations was written or
run**. Context: with the measured store-noise exponent s = 0.31 (CI 0.24–0.37; `RESULTS_F2.md`) the tracking optimum is
1.9–3.6 s against the measured τ2 = 9.9 ± 0.3 s. Three candidate causes are tested here. Inputs are those already in
`ecoli_calc.py` and `f2/f2_results.json` unless stated.

**Disclosure, before lock.** While reading Celani & Vergassola 2010 (doi 10.1073/pnas.0909673107) for its method I saw
their maximin kernel and noticed algebraically that its rate equals twice the run-and-tumble velocity decorrelation rate,
which suggests a memory well under 1 s. For D2, I derived on paper that a gain-bounded linear-response drift objective has
the same optimum as the tracking objective. For E2, I did a mental order-of-magnitude estimate suggesting the measured
dissipation is too small. So these computations are **not blind to their likely outcome**; the lock fixes the rules and
inputs so that the numbers cannot be tuned.

## Common verdict rule (the original ECOLI-MEM rule, unchanged)
For a candidate giving a predicted range [L, U] for the slow memory: **EXPLAINS** iff M = [9.3, 10.5] s ⊂ [L/2, 2U];
**DOES NOT EXPLAIN** iff M lies wholly outside [L/3, 3U]; otherwise **NEITHER**.

## D1. Drift/uptake objective without noise (Celani & Vergassola 2010 maximin)
Their maximin kernel to concentration is K(t) ∝ λ_CV e^{−λ_CV t}[λ_CV t − (λ_CV t)²/2] with λ_CV = 4(1 + 3Dτ_r)/(3τ_r).
Its kernel to u = d ln c/dt decays with rate λ_CV (double pole), so the comparable slow memory is 1/λ_CV.
Inputs, two ways: (a) λ_CV = 2σ with σ = (6Dτ_r + 2)/(3τ_r), the paper's velocity decorrelation rate, set equal to
Mattingly's measured λ = 0.862 ± 0.005 s⁻¹; (b) the paper's own numbers, τ_r ≈ 1 s and λτ_r = 8/3. [L, U] spans (a)
and (b).

## D2. Up-gradient drift with Model S+ noise, gain bounded
Objective: maximize drift ∝ Cov(a(t), u(t)) (OU velocity: a tumble at t forfeits displacement ∝ v_x(t)/λ) subject to a
fixed activity variance (the motor's operating range), i.e. maximize corr(a, u). Store noise exponent s ∈ [0.24, 0.37],
gradients 0.1–0.4 mm⁻¹, single store, everything else as locked. [L, U] = range of the optimum over that box.

## E2. Speed-priced upkeep from measured dissipation
Lan et al. 2012 (doi 10.1038/nphys2276): adaptation dissipation ≈ 3×10⁴ kT/s ≈ 10³ ATP/s at τ ≈ 10 s, scaling with
adaptation speed (P ∝ 1/τ at fixed accuracy). Take P = 10³ ATP/s × [1/3, 3]. Cell budget 7×10⁵ to 6.4×10⁶ ATP/s
(10¹⁰ ATP per division, BioNumbers 101981/101983, over 0.7–4 h doublings; 6.4×10⁶ ATP/s measured in fast growth,
doi 10.1186/s12915-021-01023-2). Benefit of chemotaxis B = 0.02–1 of growth (Ni et al. 2020, as in `coords.py`).
Benefit model: benefit ∝ drift ∝ corr(a, u)^k, k = 1 (main) and k = 2 (sensitivity).
At the optimum, B·k·|d ln corr/d ln τ| = P/budget at τ = 9.9 s. Required ratio ρ_req = k·|d ln corr/d ln τ| at 9.9 s
(s over its CI, g over 0.1–0.4 mm⁻¹); measured ρ = (P/budget)/B over the box above.
**CONSISTENT** iff the ρ_req range overlaps the measured ρ range; **EXCLUDED** iff ρ_req's whole range is above 3× the
measured maximum or below ⅓ of the measured minimum; otherwise **MARGINAL**.

## H. Slow habitat modes (diagnostic only, no verdict)
Compute the slow mode (rate μ, share φ of u's variance) that would put the single-store optimum at 9.9 s with s = 0.31,
then search for field measurements of chemoattractant-gradient time scales in E. coli habitats. Reported, not scored.
