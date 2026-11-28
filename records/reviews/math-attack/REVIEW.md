# REVIEW: hostile review of MATH_ATTACK.md and theorem-v2/GENERAL_THEOREM.md

Reviewer: Grok Bot executor, acting as an independent, hostile mathematical-physics referee. I did not write either file. Saturday 2026-11-14, about 10:35–11:50 PM ET. Neither reviewed file was edited. Nothing was posted or sent.

**Scope**
- `attack/math/MATH_ATTACK.md` and its `checks/`.
- `theorem-v2/GENERAL_THEOREM.md` and its `checks/` (added by the parent mid-review).
- The theory they attack, read for context: `X_TEXT.txt` (v9) and `public-repo/theorems/THEOREMS.md`.
- The C3 numbers, checked against `tests/C3/RESULTS.md`.

**Reproduction**
- `attack/math/checks/run_all.sh` was rerun (33 s). All 6 `.out` files came out **byte-identical** to the committed ones; pre-run copies are in `review_rerun/`.
- `theorem-v2/checks/run_all.sh` was rerun (2 min 51 s). All 8 `.out` files came out **byte-identical**; pre-run copies are in `review_rerun/tv2/`.
- My own checks are in `review_checks/review_checks.py`, with output in `review_checks.out`, using the same venv.

**Notation warning (affects anyone reading both files).** MATH_ATTACK uses z = B/(σ√τ). GENERAL_THEOREM uses z = σ√τ/B, the reciprocal. So "hot" is small z in one file and large z in the other. Below I write z_M and z_G. C3b's preregistration should pin one convention explicitly.

---

## 1. Errors found, by severity

### MATH_ATTACK.md

**M1. HIGH: "C3's τ null is what the theory itself predicts / C3 was uninformative by construction" (§0 item 5, §2.5.2, §6).** The arithmetic is right: under equal attenuation a, β_τ = β_σ/2 − β_σ/ε_σ. The inference fails for four reasons.
- **It ignores the hazard level.** In any single-τ first-passage model, h·τ = F(z), so C3's observed hazard (0.071/yr) plus τ (median 44 d) pins the regime without any units for σ or B. The result is h·τ ≈ 0.009, deep in the cold regime: z_M ≈ 2.4–3.9 depending on the fix mechanism (`review_checks.out` R2). That excludes ε_σ ≈ 2. Yet the lower end of the "[0, 0.14)" range comes precisely from ε_σ ≈ 2. In the pinned regime, ε_σ ≈ 4.4 (Poisson-rate fix), 9.9 (fixed delay) or 16.8 (OU).
- **Its key assumption contradicts its own diagnostics.** Equal attenuation across σ and τ is assumed, yet §2.5.3 argues that σ *specifically* is a noisy proxy (counting noise, collinear with B). Errors-in-variables attenuation is proxy-specific. With corr(ln σ, ln B) = 0.79 it is not even proportional, and bias can transfer between coefficients.
- **It anchors on the weakest coefficient.** The identity also gives ε_B = −ε_σ. Anchoring on |β_B| = 0.47 (literal) or 0.57 (coding A), which is the better-measured coefficient and the one C3 actually detected, gives predicted β_τ = 0.13–0.25 in the pinned regime. C3's CI excludes that (upper bound 0.10 literal, 0.12 coding A). C3's own RESULTS.md already made this point.
- **It ignores the uncertainty in β_σ.** β_σ's own CI is [−0.10, 0.66]. Anchoring on its upper end gives a predicted β_τ of up to 0.29.

Even under M1's own equal-attenuation assumption, once the regime is pinned, the σ-anchored prediction is 0.08–0.12, which sits at the upper edge of C3's CI. The B-anchored prediction is outside it. **Verdict:** "the theory predicts C3's null" is false. The supportable statement is narrower: C3 is weak evidence against the τ term in general, and strong evidence against one specific operationalization (§6 below).

**M2. MEDIUM: O1 ("new result: the physics floor has exactly the EOQ form, c = kT per nat") is overstated in four ways.**
- **The floor itself is not new.** For a Kalman–Bucy tracker, the information flow equals the transfer-entropy rate, and the memory's heat is at least kT times the information flow. This is Mitter & Newton 2005 (J. Stat. Phys. 118:145, "Information and entropy flow in the Kalman–Bucy filter") and Horowitz & Sandberg 2014 (New J. Phys. 16:125007, eqs. 37, 66 and 70, fetched). In H&S's notation, I_flow = σ²/(2E) − γ/m. Its random-walk limit γ → 0 is exactly O1's σ²/(2D). See also Sandberg, Delvenne, Newton & Mitter, Allerton 2014, "Thermodynamic costs in implementing Kalman–Bucy filters". Adding w·D and minimizing is a one-line corollary.
- **"Minimal heat cost is kT·σ²/(2D)" (§0 item 2) should read "is at least".** Barato–Hartich–Seifert gives only an inequality, η = l_y/σ_y ≤ 1. Attainability is not shown, so J\* = σ√(2kTw) is a lower bound on the optimum, not the optimum. (§1.2 says "≥"; the bottom line drops it.)
- **The "c = kT per nat" identity is formal.** EOQ's check rate is 1/T = σ²/(2·D_avg), where D_avg is the time average of a sawtooth error. The thermodynamic floor is σ²/(2D) with D a constant steady error. Identifying "one check" with "one nat" makes the two forms coincide by construction. A perfect check acquires unbounded information, and the information lost per sawtooth cycle diverges logarithmically (`review_checks.out` R5). So even the √2 prefactor match carries no physical content, not just the form.
- **"Cells are near it (Lan et al. 2012)" is unsupported.** Lan et al.'s bound is the energy–speed–accuracy bound, a different bound. The Barato–Hartich–Seifert paper cited for the floor says explicitly that its E. coli adaptation model "in an environment that changes at a very slow time-scale is quite inefficient, dissipating much more than it learns" (abstract, fetched). "Firms are ~10¹² above it" has no source.

**M3. MEDIUM: §3.6 says "form invariance … iff all four hold".** Only sufficiency is shown. The four failure examples show that violating a condition *can* break closure, not that every violation does. Separately, "the strong claim is FALSE" conflates two things:
- reduction to a *single* (σ, τ, B, c, w), which fails generically and correctly;
- closure of the *objective*: a sum of J_i is still an objective of the same type with many modes, and that closure is trivial.

What fails is one-parameter coarse-graining, not "a population of optimizers is an optimizer of the same kind of objective".

**M4. LOW: the weakest-link rule z' ≈ √(z² − ln N) is class-specific.** It holds for the OU tail (e^{−z²}). For fixed-delay fixing (tail e^{−z²/2}) it is √(z² − 2 ln N). For model A at z = 3, N = 16, the exact value is 2.02. The rule as stated gives 2.50, while √(z² − 2 ln N) gives 1.86 (`review_checks.out` R4). N_max ~ e^{z²−1} likewise changes to e^{(z²−1)/2}.

**M5. LOW: the toy-reversal numbers and framing are off.**
- **The crossing.** Under the renewal (1/MFPT) hazard, the crossing moves from 0.308 to **0.353**, not "≈0.38". Under the survival-decay hazard −ln(1−P)/τ, which is what a Cox analysis estimates, it is **0.343** (`review_checks.out` R1).
- **The "exact" hazard.** "The exact renewal hazard" is one of two legitimate definitions. They agree in the cold regime and differ exactly where the reversal happens.
- **The framing.** The per-window counting error shifts the crossing by only about 0.04. So "the reversal was partly an artifact" overstates. In the one-sided, symmetric-reset model the reversal is essentially real. MATH's own diagnosis of the mechanism (fixing erases favourable deviations, so reversal occurs iff ε_σ < 2) is correct.

**M6. LOW: "σ was mostly counting noise".** A Fano factor of 1.85 (the median) means about half the variance is Poisson. "Largely size-driven" is fair; "mostly noise" overstates.

**M7. LOW: "h = F(z)/τ for any fix mechanism".** This holds only for mechanisms with one time scale and no extra length or rate scale. Each of the following adds a second dimensionless group and breaks the identity:
- threshold-triggered fixes;
- detection thresholds;
- partial resets;
- bias μ (Péclet number);
- jump size or jump rate;
- an observation window.

GENERAL_THEOREM R1 and R5 show several of these. The two-sided resetting formula τ(cosh √2 z − 1) is labeled PROOF. It is correct (MC agrees within 2%), but it is probably already in the resetting-in-an-interval literature, so it should not be presented as new.

**M8. LOW (labeling).** The bottom line calls O1 and the dimensional identity "new results" despite §1.2's own caveat that the forms are forced. See the novelty table (§4).

### GENERAL_THEOREM.md

**G1. HIGH: R6 / §0 item 5 / §9 item 9 ("C3 rules out the mechanism … at most about 1–5% of dormancy hazard"; "the τ term as operationalized is dead").** The units-free pinning is a genuinely good idea, and the numbers reproduce exactly (my independent renewal code gives HR = 11.4 per doubling at 44 d for deterministic resets). But the conclusion rests on two unstated assumptions.
- **(a) The fix interval is deterministic or narrowly distributed.** Repeating the identical pinning with random fix intervals (exact renewal; `review_checks.out` R2b) gives:

| Fix-interval distribution | Predicted HR per doubling | Diffusive share of hazard compatible with C3 (HR ≤ 1.087) |
|---|---|---|
| Deterministic | 11.4 | ≈1% |
| Exponential | 3.0 | ≈4% |
| Lognormal, sd(ln) = 1 | 2.1 | ≈8% |
| Pareto, κ = 1.5 | 1.5 | ≈18% |
| Pareto, κ = 1.2 | 1.26 | ≈34% |
| Lognormal, sd(ln) = 2 | 1.20 | ≈43% |

  Issue-close times are notoriously heavy-tailed. This is MATH_ATTACK's §2.2 power-law case (ε_τ → κ − 1), which GENERAL_THEOREM does not consider.
- **(b) τ is exogenous given (σ, B).** If projects choose τ partly in response to their own z (a slow pace is affordable when buffers are large), the cross-sectional coefficient can sit anywhere from the causal ε_τ down to −1. The −1 end is the case where τ is tuned to hold z fixed, with σ and B measured badly.

  `c4` includes noise, jumps, frailty and selection, but neither heavy-tailed intervals nor endogenous τ.

**G2. MEDIUM: Theorem P's prior-art section misses the closest results, and the novelty claim is too generous.**
- **Stratonovich (1965), value of information** (Belavkin et al., eds., *Theory of Information and its Value*, Springer 2020). It defines exactly the best expected utility achievable with I nats under a general loss, i.e. D(R) for arbitrary loss.
- **The data-rate theorems** (Nair & Evans 2004, SIAM J. Control Optim.; Tatikonda & Mitter 2004). These are stochastic, quantitative "persistence requires bits" theorems: R > Σ log|λ_i| over unstable modes, which is stronger and has structural content.
- **Polani, Nehaniv, Martinetz & Kim (2006), "Relevant information in optimized persistence vs. progeny strategies"** (ALife X, fetched). Minimum relevant information for a given utility, in a persistence setting.

  P0 itself is a two-line corollary: the single-letter rate–distortion converse plus "negative-mean stationary increments imply ruin". It is correct. Also, P assumes a stationary world, so it excludes the random-walk worlds on which T1/EOQ and most of the theory rest.
- **Novelty verdict:** packaging only.

**G3. LOW: the boundary case in P1.** P1 says "if D(0) ≤ y − c̄, persistence with I_pred = 0 is possible". At equality, P0's own recurrence clause says ruin is certain, so the inequality must be strict. In addition, c̄ is policy-dependent (a blind agent pays no memory cost), so "the" threshold is not a single number.

**G4. LOW: L1's Lundberg bound applies to ruin checked at cycle ends.** Ruin within a cycle (between checks) is ignored, both in the bound and in the Monte Carlo. That should be stated.

**G5. LOW: R3 uses the one-window probability ∂P/∂ln τ (peak at z_G = 1) to "support" the post's qualifier.** That quantity is not a hazard. GENERAL_THEOREM's own calendar-hazard analysis (two-sided) shows no reversal and τ-invisibility in the hot regime, which reads against the qualifier's premise.

**G6. LOW: R2 calls the flat-barrier, zero-log-drift case "Black & Cox".** Black–Cox (1976) used an exponential barrier. The 2Φ(−DD) correction is right: the reflection principle at zero log-drift (c8a reproduces 0.2345 against MC 0.2326).

### Conflicts between the two files besides C3
- **Heavy tails.** MATH says "heavy tails roughly halve the τ effect, they do not erase it". GENERAL_THEOREM says "τ barely matters". Both are single parameter choices (MATH's single-jump share is 82% but the MFPT is far from the single-jump floor; GT's diffusion is tiny). Neither statement is general. The honest statement is that ε_τ interpolates from its diffusive value to 0 as the single-jump share goes to 1, slowly.
- **The post's qualifier** ("as long as slow fixers still usually survive a fix window"). MATH says it was derived from an artifact; GT says it is supported. Both are partly wrong (M5, G5). The calendar-hazard facts on which they agree:
  - two-sided, center-reset models never reverse (ε_σ ≥ 2);
  - one-sided, symmetric-reset models reverse for ε_σ < 2, around σ√τ/B ≈ 1;
  - τ is relatively most visible in the cold regime.

---

## 2. Claims that survive (checked step by step)

**(a) The thermodynamic floor.**
- Barato–Hartich–Seifert 2014 does say l_y ≤ σ_y for an internal process learning about an unaffected external one (fetched, eq. 7).
- The information-loss rate σ²/(2D) for a random walk at fixed estimator is right (limit Var x → ∞).
- The Duncan cross-check (P/(2r) = σ²/(2P) at P = σ√r) is right.
- Berger 1970 does give R(D) = 2σ²/(π²D) (abstract fetched), so the "2/π" ratio of J\* is right.
- The algebra J\* = σ√(2kTw) is right.

What survives is a correct lower bound (KNOWN, see M2) with a formal resemblance to EOQ.

**(b) The dimensional identity.**
- With one length B, one diffusivity σ² and one time τ, Buckingham-π forces h·τ = F(z).
- Then ε_σ = −d ln F/d ln z_M, ε_B = −ε_σ and ε_τ = −1 + ε_σ/2 follow identically, for any F.
- It is a log-elasticity identity, a restatement of the joint homogeneity of h:
  - degree 0 under (σ, B) → (λσ, λB);
  - degree −1 under (τ, σ, B) → (λτ, λ^{−1/2}σ, B) jointly.

So yes, it is **trivially true by dimensional analysis**. It holds only under M7's conditions. Its empirical content is nil unless σ, B and τ are measured in mutually consistent units on one clock. GENERAL_THEOREM's R4, r_τ = g/(2(2+g)), is algebraically the same identity: ½ − 1/ε_σ with ε_σ = 2 + g. The two files agree on it.
- Corollary (c), ε_τ|s = −1 at fixed stationary spread, is correct. It is the familiar Kramers result: rate ∝ relaxation rate at fixed barrier and variance. It does give a genuinely competitor-distinguishing sign, since static indices predict 0.
- ε_σ ≥ 2 in two-sided center-reset models is numerical in the file, but provable: center reset is survival-maximizing for a symmetric interval, so more frequent resets cannot raise the hazard.

**Exact laws.** These are all correct:
- reflection principle;
- strip (image/Fourier) series;
- Evans–Majumdar one-sided MFPT τ(e^{√2 z} − 1) (paper fetched: T = (e^{x₀√(r/D)} − 1)/r with r = 1/τ, D = σ²/2);
- the two-sided cosh form (MC within 2%);
- the two-sided OU MFPT and its Kramers tail.

Monte Carlo agrees within 0.4–2.5%.

**(c) C3 reanalysis.** Only the diagnostics survive:
- B is a flow;
- the Fano and slope statistics;
- corr(ln σ, ln B) = 0.79;
- the τ spread.

The "prereg band's upper half was unreachable" point also survives, and agrees with GENERAL_THEOREM R4.

**(e) Aggregation.**
- σ' = σ√(N(1 + (N − 1)ρ)) is correct (MC 9.364 vs 9.381).
- z_N = z√(N/(1 + (N − 1)ρ)), with ceiling z/√ρ, is correct.
- The weakest-link direction (heating) is correct, with the class caveat in M4.
- Granger aggregation is correct: d = 1 − q/2 = 0.4; the GPH estimate is 0.44.
- The single-τ misprediction (1.36×, 2.39×) is correct, though it depends on the fitting interval, as the file shows.
- The Cauchy–Schwarz bound and the unbounded penalty under heterogeneous c are correct.
- z ∝ N^{b−H−θ/2} is correct but trivial.
- Stanley et al. 1996 β ≈ 0.15 is confirmed; a later extended analysis reports 0.20 ± 0.03.

**GENERAL_THEOREM.**
- **P0–P3** are correct as stated (with G3's strict-inequality fix). P3's I\* formula is checked symbolically and by brute force.
- **G1–G4** are correct:
  - G2's λ_c = Φ/c follows because s(r_∞ − A(s)) = ∫₀ˢ(r_∞ − r) is nondecreasing, with supremum Φ;
  - Blackwell garbling gives G1;
  - Topkis gives G4.
- **R0–R4** are correct.
- **L1** is correct. The Cameron–Martin factor cos(τ√(2b))^{−½} is right, and so is the Lundberg equation.
- **S1–S4** are correct; the S3 exponent −p/(1 + pH) is re-derived.
- **c4/c2j** reproduce.

---

## 3. Claims overstated
- **MATH §0 item 2:** "minimal" heat cost (it is a lower bound); "new result"; "exactly EOQ with c = kT per nat" (formal; see M2).
- **MATH §0 item 3:** "for any fix mechanism" (single-scale mechanisms only).
- **MATH §0 item 5 and §6:** "uninformative by construction"; "the theory itself predicts" the null (M1).
- **MATH §0 item 6:** "partly an artifact" (the shift is small; see M5).
- **MATH §3.6:** "iff"; "strong form FALSE" (M3).
- **MATH §1.2:** "cells are near it", "firms ~10¹² above" (M2).
- **GENERAL_THEOREM §0 item 5, R6 and §9:** "C3 rules out", "at most 1–5%", "dead for that scale and proxy". This should be conditional on deterministic, exogenous fix intervals equal to median close time (G1).
- **GENERAL_THEOREM §0 item 2:** "the new statement most worth claiming". The near prior art is missing (G2).
- **GENERAL_THEOREM §8:** "R6 … to within a few percent of hazard" (G1).

---

## 4. Novelty verdict per result

| Result | Verdict | Closest prior art (checked) |
|---|---|---|
| MATH O1: tracking floor kT·σ²/(2D) | **KNOWN** | Mitter & Newton 2005; Horowitz & Sandberg 2014 (I_flow for the KB filter, heat ≥ kT·I_flow); Barato–Hartich–Seifert 2014 |
| MATH O1: "EOQ form, c = kT per nat" | Trivial corollary; formal identification | EOQ (Harris 1913) |
| Dimensional identity ε_τ = ε_σ/2 − 1, ε_B = −ε_σ (both files) | **Trivial / known in substance** (Buckingham-π) | First-passage scaling; Merton/Black–Cox distance to default |
| Fixed-spread ε_τ = −1 | Known physics (Kramers prefactor); the cross-scale test use may be new | Kramers 1940; Siegert 1951 |
| F classes (fixed delay / Poisson rate / OU / power-law fix times) | **KNOWN** formulas; "classes by fix mechanism" is a framing | Reflection principle; Evans–Majumdar 2011; Kramers; resetting in intervals; single-big-jump (Foss–Korshunov–Zachary) |
| Toy-reversal mechanism (reversal iff ε_σ < 2; erasing favourable deviations) | Correct, elementary; not publishable alone | n/a |
| C3 attenuation reanalysis (MATH) | **Wrong inference** (M1) | n/a |
| Pooling z_N, correlation ceiling | **KNOWN** | Risk pooling and diversification (Markowitz; insurance) |
| Weakest-link heating | **KNOWN** | Series-system reliability and extreme values |
| Heterogeneous τ gives long memory | **KNOWN** | Granger 1980 |
| Gorman-type closure | **KNOWN** (Cauchy–Schwarz); "Gorman" is an analogy | Roundy 1985; Gorman 1953 |
| z ∝ N^{b−H−θ/2} | Trivial | n/a |
| GT Theorem P (P0) | Elementary corollary; **packaging only** | Shannon/Stratonovich value of information; data-rate theorem (Nair–Evans, Tatikonda–Mitter); Polani et al. 2006; Kolchinsky–Wolpert 2018; Touchette–Lloyd 2000; Donaldson-Matasci et al. 2010 |
| GT P2 (lead-time cap) | Trivial (data-processing inequality) | Bialek–Nemenman–Tishby 2001 |
| GT P3 (first bit must pay; log model size) | **KNOWN** | Rational inattention (Sims 2003); reverse water-filling |
| GT G1 | **KNOWN** | Blackwell 1953; Sun & Cyr arXiv:1812.07241, Lemma 1 (MI version, confirmed) |
| GT G2: λ_c = Φ/c, any Markov world, any loss | Clean; likely known in substance; **low–moderate** novelty | Cho & Garcia-Molina 2003; age-of-information with sampling cost; renewal-reward |
| GT G3/G4 | **KNOWN** | Topkis 1978 |
| GT R0–R2, incl. the Black–Cox factor-2 correction | **KNOWN**; the correction is right and useful | Black & Cox 1976; Merton 1974 |
| GT R4 | Same identity as MATH; trivial | n/a |
| GT R6 (units-free pinning test) | **New as an analysis tool** and worth keeping; its conclusion is overstated (G1) | n/a |
| GT L1–L3 | **KNOWN** (Cramér–Lundberg; risk-sensitive control direction) | Asmussen & Albrecher 2010; Jacobson 1973; Whittle 1990 |
| GT S1–S4 | Trivial homogeneity / generalized EOQ | n/a |
| GT S5 | **KNOWN** | Kelly 1956; Donaldson-Matasci et al. 2010; Vinkler et al. 2016 |

**Citations verified this pass (WebSearch/WebFetch).** Each says what is claimed, except where marked:
- Barato–Hartich–Seifert 2014. Says l_y ≤ σ_y, as claimed. But it contradicts "cells near the floor" in slowly changing environments.
- Berger 1970: R(D) = 2σ²/(π²D), IEEE TIT 16(2):134.
- Evans & Majumdar 2011 MFPT.
- Flannery & Rangan 2008: 53%/yr adjustment for large BHCs.
- ShanghaiT1DM/T2DM: Zhao et al. 2023, Sci. Data; 12 T1DM + 100 T2DM; doi 10.6084/m9.figshare.20444397.
- GPDD: doi 10.5063/F1BZ63Z8.
- Stanley et al. 1996: β = 0.15.
- Virgo, Biehl, Baltieri & Capucci, arXiv:2508.06326: exists, and is described correctly.
- Sun & Cyr Lemma 1.
- Still 2020: the information bottleneck from a dissipation bound, PRL 124:050601.
- Kolchinsky & Wolpert 2018.
- Touchette & Lloyd 2000: ΔH_closed ≤ ΔH_open + I.
- Horowitz & Sandberg 2014.
- Sandberg et al. 2014.
- Polani et al. 2006.
- Stratonovich value of information.
- The data-rate theorem.

The remaining citations were checked from memory only: volume and page numbers are consistent with my knowledge, and none is suspicious, but none was web-fetched. They are:
- Kramers 1940; Granger 1980; Jona-Lasinio 1975; Gorman 1953; Howard 1966; Fudenberg & Levine 1993; Lan 2012; Horowitz & Esposito 2014; Bettencourt 2007; Kovatchev 1998; Dennis et al. 1991; Lande 1993; Schäfer 2018; Alchian 1950;
- Black & Cox; Merton; Embrechts & Veraverbeke; Biehl et al. 2021; England 2013/2015; Sims 2003; Ortega & Braun 2013; Bialek et al. 2001; Kelly 1956; Donaldson-Matasci 2010; Rivoire & Leibler 2011.

---

## 5. Bottom line

Every script reruns and reproduces exactly, and almost all of the algebra is right. The problem is what the algebra is taken to show.

Nearly everything either file labels new is known or trivial:
- MATH's "thermodynamic EOQ" floor is Mitter–Newton / Horowitz–Sandberg's information-flow bound for the Kalman–Bucy filter in the random-walk limit. "c = kT per nat" is a formal identification, not physics.
- The "universal identity" ε_τ = ε_σ/2 − 1 is Buckingham-π restated. It is true for any first-passage problem with one fix time scale, so it says nothing about adaptive organization as such.
- The F classes, pooling, weakest-link and Granger results are textbook.
- Theorem P is a two-line rate–distortion converse. Its closest prior art (Stratonovich's value of information, the data-rate theorems, Polani et al.'s relevant information) is not cited.

The genuinely useful contributions are three tools, not theorems:
- the fixed-spread sign ε_τ = −1 against static risk indices;
- GENERAL_THEOREM's units-free regime pinning;
- G2's clean hold-or-fade threshold.

On the C3 conflict, neither file is right as written. MATH's "the theory predicts C3's null" fails: it ignores the hazard-level pinning, assumes equal attenuation that its own diagnostics contradict, and anchors on the noisy σ coefficient rather than the well-measured B coefficient. GENERAL_THEOREM's "C3 rules out the mechanism; at most 1–5% of dormancy" holds only if fix intervals are deterministic and exogenous. With realistically heavy-tailed fix intervals, the same pinning predicts hazard ratios of 1.2–1.5 per doubling. That is compatible with C3 even if 18–43% of dormancy is diffusive.

The defensible statement is narrower. C3 decisively rejects "diffusive error reset on a fixed clock equal to median issue-close time". It is only weakly informative about a τ term in general. No result in either file yet distinguishes "the same physics at every scale" from "the same dimensional analysis at every scale".

---

## 6. Adjudication: C3, "uninformative" (MATH_ATTACK) vs "rules out" (GENERAL_THEOREM)

**Setup.**

| Quantity | Literal | Coding A |
|---|---|---|
| β_lnτ | 0.001, CI [−0.09, 0.10] | 0.03, CI [−0.05, 0.12] |
| β_lnσ | 0.28, CI [−0.10, 0.66] | n/a |
| β_lnB | −0.47 | −0.57 |

- Coding A's hazard is 0.071/yr; the median τ is 44 d.
- Coefficients are Cox, per unit of natural log.

**What each file assumes.**
- **MATH_ATTACK:**
  - (i) the observed coefficients are true elasticities scaled by one common attenuation factor a;
  - (ii) a is identified from β_σ;
  - (iii) ε_σ can be anywhere in [2, ∞).
  - Then β_τ ∈ [0, 0.14).
- **GENERAL_THEOREM:**
  - (i) failure is two-sided diffusive first passage with **deterministic** resets every τ;
  - (ii) C3's median close time *is* τ (same clock, factor ≈ 1);
  - (iii) the population is homogeneous in mechanism;
  - (iv) τ varies exogenously given σ and B.
  - Then h·τ pins z_G ≈ 0.35, giving ε_τ ≈ 3.5 and HR ≈ 11 per doubling. C3's HR ≤ 1.087 then caps the diffusive share at ≈ 1%.

**Which is right where.**
1. **On the regime, GENERAL_THEOREM is right and MATH_ATTACK is wrong.** In any single-τ model, h·τ = F(z), so the observed event rate excludes the hot regime and with it MATH's lower end ε_σ ≈ 2. Once that is used, MATH's own equal-attenuation framework predicts β_τ = 0.08–0.12 from the σ anchor (marginal against the CI) and 0.13–0.25 from the B anchor (excluded). MATH's equal-attenuation assumption is also unjustified and contradicted by its own §2.5.3. "C3 was uninformative by construction / the theory predicts the null" should be withdrawn.
2. **On the conclusion, GENERAL_THEOREM overreaches.** Its pinning is mechanism-specific. Holding everything else fixed (`review_checks.out` R2b, exact renewal):

| Fix-interval distribution | Predicted HR per doubling of τ |
|---|---|
| Deterministic | 11.4 |
| Poisson-rate resets (MATH model B) | 3.4 |
| OU | 16.6 |
| Lognormal, sd(ln) = 1 | 2.1 |
| Lognormal, sd(ln) = 2 | 1.20 |
| Pareto, κ = 1.2 | 1.26 |

   Heavy-tailed issue-close times are the realistic case. Under them, a mostly diffusive mechanism is compatible with C3's HR ≤ 1.087 at 34–43% diffusive share, approaching 100% as κ → 1 (leading order ε_τ → κ − 1, as in MATH §2.2). Endogenous τ, chosen given z, can push the measured coefficient anywhere from the causal value down to −1, independently of all of the above.
3. **Net ruling.** C3 *is* informative. It rejects, at roughly 1% residual share, the conjunction {diffusive failure, deterministic resets, fix clock = median issue-close time, exogenous τ}. That is the mechanism as naively operationalized in the post, and in that sense GENERAL_THEOREM's "kills the mechanism as posted for this proxy" is fair. It does **not** rule out a τ effect with heavy-tailed or endogenous fix times, or with a different true fix clock. "At most 1–5% of dormancy" must be restated as conditional on deterministic, exogenous fix intervals.

**What would settle it.** Measure the within-project *distribution* of fix intervals, not just the median, and repeat the pinning with that distribution. GENERAL_THEOREM's R6 extends directly. Then use exogenous τ variation, which is what C3b's upstream-release shocks do. Preregister the predicted HR per doubling under each fix-interval class before looking at outcomes.

---

*Files written by this review:*
- `REVIEW.md` (this file);
- `review_checks/review_checks.py` and `review_checks/review_checks.out`;
- `review_rerun/` (pre-rerun copies of both checks folders' `.out` files, plus the rerun logs).
