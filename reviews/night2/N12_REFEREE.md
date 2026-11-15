# N12 referee: is the formal pooling-onset exponent independent of the world's spectral slope α?

15 Nov 2026, about 10:30 AM ET. Executor n12-referee (for Ace, Chad t1914). QUEUE item ONSET-SPECTRUM-FREE-REFEREE, post-protocol pick 3 (unaided slot; ledger 22–24, outcome 25). Private repo; nothing posted or sent.

**Claim refereed (CLAIM_MAP N12, THEORY v1.4 §2.5, merge a1d7e02).** In the power class φ = k p^{1−a} W^a q^b, the onset exponent e_g = −(1−b)/(1−a) is −1 for reset reads (a = b = 1/α) and −(1+θ) for continuous sensing with precision priced ∝ precision^θ (a = αθ/(α(θ+1)−1), b = θ/(α(θ+1)−1)), at every α; small-share vigilance ∝ ρ^{−θ}. Scope stated: power class, h = 0, equal prices, small ρ, 1 < α < 3 for continuous sensing.

The author's checks (`THEORY14_checks/`) were not used. Everything below was rederived from the premises with new code (`N12_REFEREE_checks/`, c1–c5, all run at nice 19, each under 3 minutes). An independent algebra check by the v1.4 reviewer (`V14_REVIEW.md` §4, PR #13) arrived during this referee and was verified separately (§3).

## Verdict: **CORRECTED (narrowed).** The core exponent is confirmed, and is more general than stated. Four scope corrections. Novelty: elementary corollary; not found stated; low.

### 1. What is confirmed (and why it is true)

- **Onset exponent, priced precision: −(1+θ) at every α. CONFIRMED.** Rederived from a weaker premise (c1 §1): any tracker whose error is degree-1 homogeneous and a power, E = K q^u r^{1−u}, with precision 1/r priced c·r^{−θ}, gives a = θ/(1−u+θ), b = u·a and e_g = −(1+θ) **for every u**. The spectrum enters only through u (u = 1/α for S ∝ q|ω|^{−α}), so it cancels. Homogeneity is not a power-law accident: scaling signal and noise spectra together by λ leaves the optimal linear filter unchanged and scales its MSE by λ (exact for any Gaussian/linear problem). **Reason for the α-independence: the dimensional homogeneity of linear MMSE in (signal level, noise level).** That is the correct one-line explanation and should replace "the spectrum drops out" as a surprise.
- **Independent numerics (c2).** Causal MMSE computed by quadrature of the Yovits–Jackson integral (validated against the Kalman algebraic Riccati solution at α = 2, 4, 6 to ≤ 3·10⁻¹⁶), cost minimised numerically over r, N\* found by root-finding G(N) = 0 with no closed-form (a, b). Local slopes between ρ = 10^{−3} and 10^{−3.5}: −1.9994 (θ = 1) at α = 1.2, 1.5, 2, 2.5, 2.9, 3.5, 4; −1.4996 (θ = ½); −2.9991 (θ = 2). Matches −(1+θ) at every α tested.
- **Scope is wider than stated.** The causal MMSE q^{1/α} r^{1−1/α}/sin(π/α) holds for every α > 1 (the integral converges iff α > 1), checked exactly against Kalman at α = 4 and 6. "1 < α < 3" can be replaced by "α > 1". At α → 1⁺, a, b → 1 (sensing becomes worthless), the exponent stays −(1+θ) and Π\* → e^{1+θ} (c1 §5).
- **Reset reads: −1 at every α. CONFIRMED** for exact reads with hold-last-value or any rescaling-closed predictor: loss depends on (W, q) only through Wq, so a = b (formal Lemma 1(ix)), and a = b gives −1 for any a (c1 §3; c3 noise-free rows: −1.000 at α = 1.5, 2, 2.5 by Gaussian conditioning on 200 past reads).
- **Third class, same answer.** Information-rate (entropy) pricing at any α (Duncan: rate = MMSE/2r) gives a = b = 1/α, so −1 (c1 §4).
- **Finite ρ.** Even away from ρ → 0 the exponent barely moves with α: local e_g(0.1) = −0.953 to −0.954 (reset) and −1.907 (θ = 1) over α = 1.2–2.9; fitted slope over ρ ∈ [0.01, 1] = −0.93 and −1.86 (c4 §A). Integer rounding of N\* is negligible beyond N\* ≈ 30.
- **Premises of the onset definition.** Within architecture class 𝒜₁ (fixed flat vs one-level architectures, κ_b = 0) the definition is sensible and the exponent is robust to upkeep (T1.5: a = b keeps −1; a > b keeps the h = 0 exponent) and to unequal prices (prefactor only). With a per-member broadcast cost κ_b > 0 there is no onset exponent at all (formal Theorem 2: a ρ threshold); N12 should say so.

### 2. Corrections (what N12 must not say)

- **C1. Exact reads are a knife-edge (new).** With any read noise σ² > 0, the level, whose shared drift is small (ρ → 0), becomes noise-limited and its reads act as averaged precision with θ = 1. The small-ρ onset exponent then tends to **−2, not −1, at every α** (c3, σ² = 10⁻³ in member units: last local slope −1.985, −1.996, −2.011 at α = 1.5, 2, 2.5). The crossover's location depends on α, so over a finite window the measured exponent does: between ρ = 10^{−2} and 10^{−2.5} the local slope is −1.28, −1.40, −1.58 for α = 1.5, 2, 2.5. "Reset reads → −1" holds only when read noise is negligible at the **level's** operating point (σ² ≪ q_g T\*^{α−1}).
- **C2. Same α for shared and private drift is a premise (confirms V14_REVIEW).** With α_g ≠ α_u, ρ is no longer unit-free; the exponent of N\* in q_g at fixed q_u is −(1+θ) iff α_g − α_u < 1 (the flat member's marginal error ∫S_g r/(r+S_u) converges at ω → 0). Convergence is slow near the boundary (−1.92 at q_g = 10⁻⁶ for a difference of 0.9; −1.81 for 1.0, log-divergent). For α_g − α_u = Δ > 1 the flat gain scales as q_g^{1/Δ} and the exponent becomes −(1/Δ − b_g)/(1 − a_g), which depends on α: predicted −1.385 and −0.960, numerically −1.354 and −0.952 (still drifting toward the prediction) for (α_u, α_g) = (1.2, 2.5) and (1.2, 2.9) (c5). For exact reset reads the q_g-exponent stays −1 for any α_g, α_u (the flat error is linear in q_g).
- **C3. Vigilance units.** "Small-share vigilance ∝ ρ^{−θ}" is true for vigilance measured as **spend** ratio. Measured as **precision** (physical sensing effort), it is ∝ ρ^{−1} for every θ and every α (c1 §1: precision ∝ spend^{1/θ}). Formal Lemma 1(viii) ("effort = spend/price, so effort elasticities are (a, b)") holds only at θ = 1; for θ ≠ 1 precision elasticities are (a/θ, b/θ). A vigilance test must name the unit.
- **C4. "Only constants depend on α" is false (confirms V14_REVIEW §4, fix 1).** Exponents that do move with α: vigilance growth beyond onset V ∝ N^a (a = 1/α reset; αθ/(α(θ+1)−1) priced precision); the mixed-technology private-drift exponent e_u = (1−b_m)/(1−a_L) = θ + 1 − 1/α for a precision-priced level over reset-read members, and α(θ+1)/(α(θ+1)−1) for the reverse (c4 §D; e_g stays −(1+θ) and −1 respectively, set by the level). Constants: Π\* = 3.38, 4, 4.61 (reset, α = 1.5, 2, 2.5) and 16, 27, 40.3 (θ = 1); onset vigilance value 2.25, 2, 1.84 (reset).

### 3. Independent verification of the steering input (V14_REVIEW)

All three points verified with my own code: V ∝ N^a with a = 1/α (c4 §B; THEOREMS T5.5); e_u = θ + 1 − 1/α (sympy, c4 §D); the same-α premise is needed (C2 above, with the exact condition α_g − α_u < 1 and the Δ > 1 formula, which V14_REVIEW did not give). V14_REVIEW's "first two confirmed" (onset exponents) agrees with §1.

### 4. Prior art (only verified sources)

- **Veldkamp & Wolfers 2007**, J. Monetary Economics 54(S1):37–55 (verified: RePEc record and NBER w12557 text): firms share a fixed discovery cost of aggregate information, whose price per buyer is χ/λ; this is the −1 (a = b, large upkeep) onset in substance, already credited in THEOREMS T1 "Status".
- **Wilson 1975**, "Informational Economies of Scale", Bell J. Econ. 6(1):184–195 (verified: DOI 10.2307/3003221 record and abstract): information costs create scale economies; abstract-level only, full text paywalled, not read.
- **Yovits & Jackson 1955** (causal MMSE = (1/snr)∫log(1+snr·S)dω/2π), verified as cited in Guo, Shamai & Verdú 2005 (arXiv cs/0412108, eq. 107), which also states mutual-information rate = causal MMSE × snr/2 (the Duncan relation used for entropy pricing). The MMSE homogeneity used in §1 is immediate from this formula.
- **Afterman et al. 2022** (already verified by SPECTRUM_MAP_REFEREE) gives the q^{1/α}N^{1−1/α}/sin(π/α) rate; it agrees with the Yovits–Jackson evaluation here.
- **Sensor fusion / distributed estimation** (searched: centralized vs distributed fusion, optimal number of sensors under power constraints, e.g. "Bayesian Fusion Performance and System Optimization for Distributed Stochastic Gaussian Signal Detection Under Communication Constraints", IEEE TSP, doi 10.1109/tsp.2006.888888, abstract read): optimal-group-size results exist, but none states an onset group size scaling with a shared/private drift ratio, or its independence of the spectral slope.
- **Team theory (Marschak & Radner 1972; Radner 1962), collective sensing:** not re-read in full here; the repo's night-1 sweep (`REVIEW_PRIORART.md`) already credits Marschak–Radner and Van Zandt–Radner for the −1 case. Google Scholar not searched (PRIORART-SCHOLAR).
- **Novelty:** the statement "e_g = −(1+θ) independent of the spectrum because linear MMSE is degree-1 homogeneous" was **not found stated**. It is an elementary corollary of known pieces (Yovits–Jackson / Wiener scaling + formal Theorem 1), so its novelty is low; C1 (noisy reads drive the level to the θ = 1 class as ρ → 0) and the C2 Δ-condition were also not found stated and are elementary.

### 5. Narrowed N12 (text for CLAIM_MAP and THEORY §2.5)

> **N12 (CORRECTED, narrowed; refereed `reviews/night2/N12_REFEREE.md`).** In architecture class 𝒜₁ (h = 0 or a ≥ b, equal or fixed price ratio, no per-member broadcast cost, small ρ), the pooling-onset exponent is set by the level's sensing technology and not by the world's spectral slope: **−1** for exact reset reads (hold or any rescaling-closed predictor) and for information-rate pricing, and **−(1+θ)** for precision priced ∝ precision^θ, for every α > 1. Reason: linear MMSE is degree-1 homogeneous in (signal level, noise level), so α enters (a, b) only in a ratio that cancels. Premises: (i) shared and private drift share α (for priced precision it suffices that α_g − α_u < 1; otherwise the exponent is −(1/Δ − b_g)/(1−a_g) and depends on α); (ii) reads exact at the level's operating point (any read noise sends the small-ρ exponent to −2 with an α-dependent crossover). Small-share onset vigilance ∝ ρ^{−θ} in spend units, ρ^{−1} in precision units. **Not α-free:** vigilance growth V ∝ N^a, the mixed-technology e_u (θ + 1 − 1/α for a precision level over reset members), and all constants (Π\*, the vigilance value). In-model only; untested in the field.

### 6. Consequences for tests

- A cross-system test of N2's onset exponent (THEORY §2.5 consequence (iii)) must classify the level's technology **including its read noise relative to drift per read**, check α_g − α_u < 1 (or measure both), and use ρ ≪ 1 or the finite-ρ closed form (fits over [0.01, 1] give −0.93 / −1.86, not −1 / −2).
- ONSET-ACROSS-ALPHA-SIM's locked prediction should be the narrowed form: same α for shared and private drift, exact reads (or noise reported), ρ window stated.
- SENSE-CELL: a cell's receptor reads are noisy, so the relevant class at small ρ is priced precision (C1); θ is the quantity to measure.

### 7. Unresolved

- Periodic reading is assumed, not proved optimal, for α ≠ 2 with noisy reads (c3 uses periodic reads).
- C1 was shown for one noise level and three α; a closed form for the crossover ρ_c(α, σ²) is not derived (queued).
- C2's Δ > 1 formula is an asymptotic argument confirmed numerically to within 3%, with slow convergence; not proved.
- Team-theory full texts and Scholar not searched.

## Files
`N12_REFEREE_checks/`: `c1_symbolic.py/.out` (general homogeneity derivation; vigilance units; reset; entropy pricing; α → 1), `c2_numeric_onset.py/.out` (Yovits–Jackson + Kalman validation; numerical onset at α = 1.2–4, θ = ½, 1, 2; mixed α), `c3_noisy_reads.py/.out` (noisy periodic reads, Gaussian conditioning, H = ¼, ½, ¾), `c4_scope.py/.out` (finite ρ, Π\*, vigilance growth, mixed technologies), `c5_mixed_alpha.py/.out` (α_g − α_u ≥ 1).
