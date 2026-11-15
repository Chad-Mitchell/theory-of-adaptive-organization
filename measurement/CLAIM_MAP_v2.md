# CLAIM_MAP_v2: A Theory of Adaptive Organization (GTAO), with proxy-aware statuses

Sunday 15 November 2026, about 08:15–08:20 AM ET (America/New_York). Grok Bot executor for Chad Mitchell, via Ace. Private. Nothing was posted, sent or made public. This map **supersedes the status column** of `reviews/night1/CLAIM_MAP_FINAL.md`. That file still holds the full evidence, scope and credit for each row, and row IDs are unchanged. The reason for every change is the measurement re-audit in `FRAMEWORK.md` (same folder). Gates MV1–MV9 are defined in FRAMEWORK §2.2.

**v2.1 note (15 Nov 2026, ~09:30 AM ET).** Section N adds night-2 results and the audit corrections (`reviews/night2/AUDIT_DIVERGENCE.md`). Rows are interpreted under THEORY.md v1.2 §2.5: a constant quoted for class R (a = b = ½) is the H = ½ instance; for reset reads with Hurst H, a = b = 1/(1+2H). The headline hypothesis is rows K12–K13 and N7; it is untested, not peripheral.

**Why v2 exists.** Chad (t1908): no field test so far measured GTAO's quantities validly, so field "kills" and "hits" were results about **proxies**. v2 says so in every row. It does **not** soften the mathematics. Statements refuted by proof stay refuted (as MATH-CORRECTED, with their replacement), and failed locked simulations stay failed (SIM-FAIL).

## Statuses (exactly one per row)
| Status | Meaning |
|---|---|
| **PROVED (in-model)** | A theorem in 𝓜 that survived the hostile math review, with corrected scope. Nothing about nature |
| **MATH-CORRECTED** | The original statement was false (proof, counterexample, or superseded derivation). A corrected replacement is named |
| **PROXY-FAIL** | A locked prediction failed on an instrument that fails ≥ 1 validity gate. A valid fail **of that mapping**, not of GTAO |
| **PROXY-PASS** | A locked prediction passed on such an instrument. Not support for GTAO |
| **OPEN** | Not tested on a valid instrument (including proxy nulls where no locked rule fired) |
| **PRIOR ART** | Published by others |
| **SIM-FAIL** | A locked prediction about the authors' own simulator failed. Not a measurement issue |
| **NOT EVIDENCE** | Circular or by construction, or descriptive data that cannot discriminate |
| **WITHDRAWN** | A miscitation, or a framing claim withdrawn |
| **DECIDED** | A naming or method decision, not a claim about the world |
| *(reserved)* FIELD-FAIL / FIELD-PASS | A Tier-1 result on an instrument passing MV1–MV8. **No row has either yet** |

**Bottom line.** In real systems GTAO's distinctive content is **untested, not refuted**. Every field result so far is PROXY-FAIL or PROXY-PASS. Inside the model, the corrected mathematics stands. The three decisive next tests are in FRAMEWORK §7.


## A. Sensing classes and the single-tracker lemma

| # | Claim (short; full text in CLAIM_MAP_FINAL) | v1 status | **v2 status** | Why |
|---|---|---|---|---|
| A1 | √ sampling cost for reset reads / entropy-priced filtering (a = b = ½) | PRIOR ART | **PRIOR ART** | Unchanged. EOQ; M&R 1972 ch. 7 eq. 5.13 [OCR]; Reis 2006. **Regime A (H = ½) only**; R1 with Hurst H gives 1/(1+2H) (Lemma 1(i); THEORY §2.5) |
| A2 | A_θ, |e|^p and α-stable rows of Lemma 1 | PROVED | **PROVED (in-model)** | Unchanged |
| A3 | (a, b) chart classifies technologies | PROVED | **PROVED (in-model)** | Unchanged. **Measurement now specified**: FRAMEWORK §3.4 class gate |
| A4 | Periodic reading optimal in R1 (no observation between reads) | PROVED | **PROVED (in-model)** | Unchanged; event-triggered sampling dominates with continuous observation |
| A5 | Effort elasticities = (a, b), so the class is measurable on a lone unit | PROVED | **PROVED (in-model)** | Unchanged. Now the basis of the class gate (FRAMEWORK §3.4). Members' and level's classes must be measured on different units |

## B. Pooling onset (T1, T2)

| # | Claim (short; full text in CLAIM_MAP_FINAL) | v1 status | **v2 status** | Why |
|---|---|---|---|---|
| B1 | T1.1 single crossing | PROVED | **PROVED (in-model)** | Unchanged |
| B2 | T1.2 exact onset N* closed form | PROVED | **PROVED (in-model)** | Unchanged |
| B3 | T1.3 small-ρ exponent −(1−b)/(1−a) | PROVED | **PROVED (in-model)** | Unchanged; asymptotic. Field test spec: FRAMEWORK §6.1 |
| B4 | −1 onset when a = b; amortizing a fixed information cost | PRIOR ART | **PRIOR ART** | Unchanged (V&W 2007; VZR 2001) |
| B5 | T1.4 exact elasticity, negative for all ρ | PROVED | **PROVED (in-model)** | Unchanged |
| B6 | T1.5 upkeep dichotomy | PROVED | **PROVED (in-model)** | Unchanged |
| B7 | T1.6 N* ∝ p_g/p (exact at h = 0) | PROVED | **PROVED (in-model)** | Unchanged; substance PRIOR ART (Bloom et al. 2014) |
| B8 | T1.7 volatility/stakes invariance at h = 0 | PROVED | **PROVED (in-model)** | Unchanged; zero-delay assumption |
| B9 | T1.8 mixed technologies: the level's class sets e_g | PROVED | **PROVED (in-model)** | Unchanged (ρ → 0). **The key contrast for FRAMEWORK §6.1/§7 test 1** |
| B10 | T1.8 'opposite signs survive whenever b_m, b_L < 1' | KILLED | **MATH-CORRECTED** | False away from small ρ (math C2). Replacement: B9 at small ρ; C1 with a common technology. The private-drift sign survives at all ρ |
| B11 | T1.9 N* > 1 | PROVED | **PROVED (in-model)** | Unchanged (needs p_g ≥ p) |
| B12 | T2 broadcast break and ρ thresholds | PROVED | **PROVED (in-model)** | Unchanged; mechanism prior art, closed form apparently new |

## C. Shared versus private drift (T3)

| # | Claim (short; full text in CLAIM_MAP_FINAL) | v1 status | **v2 status** | Why |
|---|---|---|---|---|
| C1 | T3 ∂N*/∂q_g < 0 < ∂N*/∂q_u at every ρ (common technology) | PROVED | **PROVED (in-model)** | Unchanged. Field spec: FRAMEWORK §6.4 (factorial) |
| C2 | Qualitative 'centralize common, decentralize local' | PRIOR ART | **PRIOR ART** | Unchanged |
| C3 | ADM 2008 states C2 | KILLED | **WITHDRAWN** | Miscitation withdrawn |
| C4 | Cor 3.1 vs contingency theory | OPEN | **OPEN** | Unchanged; zero-delay model |

## D. Bundled loss (T4)

| # | Claim (short; full text in CLAIM_MAP_FINAL) | v1 status | **v2 status** | Why |
|---|---|---|---|---|
| D1 | T4: technology, not loss shape, sets e_g under bundled decisions | PROVED | **PROVED (in-model)** | Unchanged; proof a sketch for R1. Spec: FRAMEWORK §6.2 |
| D2 | Kalman technologies: N* exactly loss-independent | PROVED | **PROVED (in-model)** | Unchanged; not re-checked by a second party |
| D3 | Cor 4.1 'iff' → 'if, and generically only if' | PROVED (downgraded) | **MATH-CORRECTED** | The original 'iff' was overstated; the corrected form is PROVED |
| D4 | Cor 4.2 separable loss only for different decisions | OPEN | **OPEN** | Modeling statement. Measurement: FRAMEWORK §3.3 records bundled vs separable |
| D5 | DP1 original: lone member's actual-loss exponent predicts e_g | KILLED | **MATH-CORRECTED** | Superseded by T4 (D1) |
| D6 | POOLING_REVIEW: absolute −2, quartic −½ (bundled) | KILLED | **MATH-CORRECTED** | True for split loss only |

## E. Vigilance at birth (T5)

| # | Claim (short; full text in CLAIM_MAP_FINAL) | v1 status | **v2 status** | Why |
|---|---|---|---|---|
| E1 | T5.1 V(N*) formula at equal prices | PROVED | **PROVED (in-model)** | Unchanged |
| E2 | T5.2 pointwise 'iff a ≥ b' | KILLED | **MATH-CORRECTED** | Counterexample (math C4). Replacement: E3 |
| E3 | T5.2 uniform: V > 1 for all (ρ, h, r) iff a ≥ b | PROVED | **PROVED (in-model)** | Unchanged |
| E4 | T5.3 small-ρ limit (2 at γ = ½) — a supremum, not a floor | PROVED | **PROVED (in-model)** | Unchanged |
| E5 | T5.6 'V ≥ 2 for every upkeep and price' | KILLED | **MATH-CORRECTED** | False as mathematics (math Issue 1). Replacement: E6/E7. **This is a real kill, not a proxy issue** |
| E6 | Exact V(N*) formula with upkeep and price | PROVED | **PROVED (in-model)** | Unchanged |
| E7 | Floor V(N*) ≥ 1 + (1+ρ)^{−1/2} | PROVED | **PROVED (in-model)** | Unchanged; not independently re-checked |
| E8 | T5.4 price invariance at h = 0 | PROVED | **PROVED (in-model)** | Unchanged; never tested. Spec: FRAMEWORK §6.3 |
| E9 | T5.5 V grows as N^a | PRIOR ART | **PRIOR ART** | Unchanged |
| E10 | V ∝ ρ^{−θ} in A_θ | PROVED | **PROVED (in-model)** | Unchanged |
| E11 | F15: VIGIL's 1.15 cannot come from upkeep/prices in class R | KILLED | **MATH-CORRECTED** | Holds only as ρ → 0 |
| E12 | '≈ 2× at every rank'; 'V > 1 always'; 'V ∝ √(c/c_g) at onset' | KILLED | **MATH-CORRECTED** | Replaced by T5.2–T5.5 |

## F. Lattice, ordering, freeze/hold/lookup, architecture

| # | Claim (short; full text in CLAIM_MAP_FINAL) | v1 status | **v2 status** | Why |
|---|---|---|---|---|
| F1 | T6(a)–(c) submodularity, lattice | PROVED | **PROVED (in-model)** | Unchanged; math prior (Topkis) |
| F2 | T6(d) stakes accretion (common degree a) | PROVED | **PROVED (in-model)** | Unchanged |
| F3 | T6 lookup counterexample | PROVED | **PROVED (in-model)** | Unchanged |
| F4 | 'bundled reads make J non-submodular' | KILLED | **MATH-CORRECTED** | 0/93,207 |
| F5 | 'cheaper memory never dissolves a level' | KILLED | **MATH-CORRECTED** | True for h; false for lookup u |
| F6 | P7.1 depth avalanches | OPEN | **OPEN** | Numerical only |
| F7 | T7(a) ordering threshold κ* (iff at h = 0) | PROVED | **PROVED (in-model)** | Unchanged. **κ now has a measurement procedure** (FRAMEWORK §3.9); spec §6.5 |
| F8 | T7(b) class dependence example (h = 0 only) | PROVED | **PROVED (in-model)** | Unchanged |
| F9 | T7(c) location rule as 'iff' | KILLED | **MATH-CORRECTED** | Only sufficient. Replacement: F10 |
| F10 | T7(c) as sufficient condition | PROVED | **PROVED (in-model)** | Unchanged |
| F11 | Knife edge at κ = 1 in general | KILLED | **MATH-CORRECTED** | True only for a = b |
| F12 | T8 cliff and hold-vs-lookup break-even | PRIOR ART | **PRIOR ART** | Unchanged |
| F13 | T8 closed forms: freeze/lookup edges, band iff μuH_l > 2c + hH_l, N² widening | PROVED | **PROVED (in-model)** | Unchanged. Spec: FRAMEWORK §6.6; Wikidata test §7 #3 |
| F14 | P9 clock cap | PRIOR ART | **PRIOR ART** | Unchanged |
| F15 | P10 selection resolution ρ ≲ ε/b | PROVED | **PROVED (in-model)** | Unchanged. **Now the MV8-ii gate** (FRAMEWORK §3.10) |
| F16 | P11 readability moves the constant, not the exponent | OPEN | **OPEN** | Numerical |
| F17 | E1 depth ∝ log N | PROVED | **PROVED (in-model)** | Unchanged |
| F18 | E2–E3 extremes | PROVED | **PROVED (in-model)** | Unchanged |
| F19 | E4 dissolution order under cheap lookup | PROVED | **PROVED (in-model)** | Unchanged |
| F20 | 'private holding dissolves first' | KILLED | **MATH-CORRECTED** | Refuted in-model by F19 |
| F21 | Cheap lookup / cheap central sensing centralizes | PRIOR ART | **PRIOR ART** | Unchanged |
| F22 | Architecture equation first-order rule | PROVED | **PROVED (in-model)** | Unchanged |
| F23 | Eigen reading under rotation-invariant cost | PRIOR ART | **PRIOR ART** | Unchanged |
| F24 | Cross-axis coupling | OPEN | **OPEN** | Conjecture |
| F25 | Structure mirrors environmental change (qualitative) | PRIOR ART | **PRIOR ART** | Unchanged |
| F26 | Quantitative: levels are a cost-thresholded copy of shared-drift structure | OPEN | **OPEN** | Untested anywhere; now measurable via FRAMEWORK §3.2 |

## G. Simulations (the measurement critique does not apply; quantities are exact by construction)

| # | Claim (short; full text in CLAIM_MAP_FINAL) | v1 status | **v2 status** | Why |
|---|---|---|---|---|
| G1 | POOLSIM onset slopes | CIRCULAR | **NOT EVIDENCE** | Circular |
| G2 | POOLSIM W5 / W5_CHECK bundled absolute loss → −1 | CIRCULAR (valid in-model) | **NOT EVIDENCE** | Valid in-model computation supporting D1; not about nature |
| G3 | POOLSIM V ≈ 2, 9.3 | CIRCULAR | **NOT EVIDENCE** | Circular |
| G4 | Onset invisible at ≥ 1% decision noise | CIRCULAR (valid in-model) | **NOT EVIDENCE** | Valid in-model; it motivates the MV8-ii selection gate |
| G5 | SENSING class A, A2 | CIRCULAR | **NOT EVIDENCE** | (a, b) were a readback |
| G6 | SENSING class R learner recovers −1 | KILLED (in-model) | **SIM-FAIL** | Locked in-model miss (−0.920) |
| G7 | SENSING rival killed | OPEN | **OPEN** | Unchanged |
| G8 | 'Members' class predicts the group's exponent' | KILLED | **MATH-CORRECTED** | Mis-statement superseded by T1.8/T4 (level's class) |
| G9 | SENSING2 EVO_A locked e_pred −2.118 | KILLED (in-model) | **SIM-FAIL** | Locked in-model fail (−0.488), caveats documented post-lock |
| G10 | SENSING2 EVO_R, OU_R, JUMP_R, FBM_R | OPEN | **OPEN** | Inconclusive (locked flat-arm bug) |
| G11 | SENSING2 QUART_R | OPEN | **OPEN** | Inconclusive; spec FRAMEWORK §6.2 |
| G12 | SENSING2 rival killed | OPEN | **OPEN** | Unchanged |
| G13 | ANTS1 C0, C1, P1-MEAN, P3-MEAN, P7 | CIRCULAR | **NOT EVIDENCE** | By construction |
| G14 | ANTS1 P1-MODE, P2, P4, P5(a,b), P8 | CIRCULAR (in-model) | **NOT EVIDENCE** | Checks of the authors' own mean field |
| G15 | ANTS1 P3-MODE N^{−½} pooling with an ant-like readout | KILLED (in-model) | **SIM-FAIL** | Locked in-model fail; **not** a proxy issue. It limits N1 to linear readouts |
| G16 | ANTS1 P5(c) | KILLED (in-model) | **SIM-FAIL** | Locked in-model fail |
| G17 | ANTS1 P6 interior forgetting optimum | KILLED (in-model) | **SIM-FAIL** | Locked in-model fail |
| G18 | Fade rate does not diagnose pooling; error scaling does | CIRCULAR (valid in-model) | **NOT EVIDENCE** | Valid design rule; used in FRAMEWORK §6.8 |
| G19 | LAYERS1 P1 | CIRCULAR | **NOT EVIDENCE** | Uninformative |
| G20 | LAYERS1 P2 span invariance | KILLED (in-model) | **SIM-FAIL** | Locked in-model fail (6/12) |
| G21 | LAYERS1 P3 | CIRCULAR | **NOT EVIDENCE** | By construction |
| G22 | AI1 shared memory adoption 'supported by POOLSIM' | CIRCULAR | **NOT EVIDENCE** | Needs agents not given the cost; FRAMEWORK §7 test 1 |

## H. Real-data tests (relabeled by the measurement re-audit; gates from FRAMEWORK §2.2)

| # | Claim (short; full text in CLAIM_MAP_FINAL) | v1 status | **v2 status** | Why |
|---|---|---|---|---|
| H1 | P1 item-level news recall slope ∈ [0.5, 1.2] | KILLED | **PROXY-FAIL** | Fails MV2 (need = headline-word recurrence; open recall ≠ holding), MV3 (d ≥ 1 assumed), MV5, MV7. **Strongest proxy fail**: memory measure valid, need proxy and derivation not. FRAMEWORK §4.1 |
| H2 | Forgetting exponent = need exponent (strong form) | KILLED | **PROXY-FAIL** | MV2, MV3, MV6 (heterogeneity). Weak form PRIOR ART. §4.2 |
| H3 | PIAAC P1 direction: supervisors read external material more | PASSED | **PROXY-PASS** | MV1–MV4, MV7, MV8 fail; also PRIOR ART (Mintzberg). §4.4 |
| H4 | PIAAC P2 specificity to shared external drivers | OPEN | **OPEN** | Proxy null (correct contrast 1.06, 0.98–1.16); locked estimator misspecified; no kill fired. §4.4 |
| H5 | PIAAC P3 √span gradient | OPEN | **OPEN** | Proxy null (0.036; CI includes 0); the 0.5 band assumed κ = 0 (FRAMEWORK §3.9). §4.4 |
| H6 | PIAAC P4 size ≈ 2 | OPEN | **NOT EVIDENCE** | Declared non-decisive by its prereg; the target itself was wrong as a floor |
| H7 | Enron: external share of received mail rises with rank | KILLED | **PROXY-FAIL** | MV1–MV4, MV6, MV7, MV9 fail (received ≠ sought; one channel; no driver, span, ρ or κ); MV8 power passed. Valid fail of that instrument. §4.5 |
| H8 | Vigilance in firms as a whole | OPEN | **OPEN** | Unchanged. Fair-kill spec FRAMEWORK §6.3 (adds κ and the class gate to night-1 §3.2) |
| H9 | MATCH1 measles freeze-or-hold | PASSED | **PROXY-PASS** | MV2 (town recurrence = use rate μ, not antigenic drift q; titer waning ≠ refresh effort), MV3, MV5, MV6, MV7, MV9 fail. Substance PRIOR ART (Mayer et al. 2016). §4.3 |
| H10 | Need exponents 0.6–0.8 across news, code, Wikipedia | CIRCULAR | **NOT EVIDENCE** | Measures use recurrence, not drift; heterogeneity explains it |
| H11 | DECISIVE banks: τ predicts failure at fixed shock and buffer | sign-only | **PROXY-FAIL** | τ = capital AR(1); sign only; **out of scope** for the structural core (AXIOMS §3). §4.7 |
| H12 | DECISIVE glucose fixed-spread slope −1 | literal kill fired | **PROXY-FAIL** | Best-measured τ of the set; size and structure failed; out of scope for the structural core. §4.7 |
| H13 | DECISIVE populations fixed-spread slope | literal kill fired | **PROXY-FAIL** | Out of scope; generic OU-barrier baseline makes the same sign. §4.7 |
| H14 | F1 firms: τ × shock ÷ buffer | INCONCLUSIVE | **PROXY-FAIL** | τ measured fixed-cost share (MV2); out of scope. §4.7 |
| H15 | C3 open source: τ term | INCONCLUSIVE/MISS | **PROXY-FAIL** | τ = issue-close habit (MV2); out of scope. §4.7 |
| H16 | BIO1 P3a immune lifetime tracks pathogen drift | contradiction | **OPEN** | Original measure invalid (half-life depends on age at measurement; COLLAPSE1). §4.8 |
| H17 | COLLAPSE1 C2 inventory buffers track demand volatility | KILLED | **PROXY-FAIL** | MV1, MV3, MV6 (aggregate inventory; volatility not decomposed). §4.8 |
| H18 | COLLAPSE1 A1 immune cue model | KILLED | **PROXY-FAIL** | MV5 (literature proxies). §4.8 |
| H19 | MATCH1 D3 redness sign | opposite sign (exploratory) | **PROXY-FAIL** | No derived spectrum→exponent mapping, so no valid construct. §4.9 |
| H20 | DRIFT1 which worlds are scale-free | descriptive | **OPEN** | Measured event-rate distributions, not target drift q (MV2 for T7's condition). §4.9 |

## I. Cross-substrate implications (each conditional on an unmeasured mapping; FRAMEWORK §3 now gives a procedure per scale)

| # | Claim (short; full text in CLAIM_MAP_FINAL) | v1 status | **v2 status** | Why |
|---|---|---|---|---|
| I1 | Cells: averaging receptors give e_g = −2 | OPEN | **OPEN** | Class measurable: Keegstra 2017 FRET data (FRAMEWORK §5 rank 5) |
| I2 | Averaging pathways build bottom-up cascades when κ > ½ | OPEN | **OPEN** | Unchanged |
| I3 | Shared sensors born far more vigilant in A₁ | OPEN | **OPEN** | Unchanged |
| I4 | Immune freeze/hold/lookup by antigenic drift | PRIOR ART | **PRIOR ART** | Mayer et al. 2016. Valid drift measure exists (Bedford 2014 HI data, Dryad) |
| I5 | Conserved epitopes as levels; herd memory as shared store | OPEN | **OPEN** | Unchanged |
| I6 | Ant trail onset ∝ 1/ρ; opposite effects | OPEN | **OPEN** | Public tracking sets lack drift manipulation (FRAMEWORK §5 rank 6) |
| I7 | People: RI monitor born ≈ 2× vigilant | OPEN | **OPEN** | Wording: → 2 as ρ → 0 at h = 0; in (1, 2) at finite ρ |
| I8 | Offloading by drift q_c ∝ u^{1/b} | OPEN | **OPEN** | Unchanged |
| I9 | Firms: central tracking at N* ≈ Π*/ρ | PRIOR ART | **PRIOR ART** | Unchanged |
| I10 | Common shocks centralize | PRIOR ART | **PRIOR ART** | Unchanged |
| I11 | Volatility promotes central tracking when h > 0 | OPEN | **OPEN** | Unchanged; conflicts with delay theory |
| I12 | AI cheapens lookup: relay levels dissolve first | OPEN | **OPEN** | Unchanged |
| I13 | Cheap central sensing centralizes | PRIOR ART | **PRIOR ART** | Unchanged |
| I14 | Cities: sublinear monitoring, tiers, depth ∝ log N | OPEN | **OPEN** | Unchanged |
| I15 | Theory describes 'judgment' in machines | OPEN | **OPEN** | Speculative |
| I16 | DP1 programme: measure the level's class, predict the group | OPEN | **OPEN** | **Now specified**: FRAMEWORK §3.4 + §6.1 |
| I17 | DP3–DP5 software/human designs | OPEN | **OPEN** | See FRAMEWORK §7 test 2 |

## J. Framing and cross-substrate claims

| # | Claim (short; full text in CLAIM_MAP_FINAL) | v1 status | **v2 status** | Why |
|---|---|---|---|---|
| J1 | Same constants (Π* ≈ 4, V ≈ 2, 29%) on every substrate | KILLED | **MATH-CORRECTED** | Constants are functions of (a, b) and H. Replacement: J6 (same *relations*, with measured classes) |
| J2 | −1 onset is a universality class | KILLED | **MATH-CORRECTED** | It is a Buckingham-Π homogeneity identity |
| J3 | GTAO is a law | OPEN | **WITHDRAWN** | **Withdrawn by decision** (Chad: never call it a law). GTAO is a general causal theory |
| J4 | Cross-substrate recursive organization (qualitative) | PRIOR ART | **PRIOR ART** | Beer's VSM |
| J5 | 'Nobody has stated them across substrates' | KILLED | **WITHDRAWN** | Should read 'not quantitatively' |
| J6 | Same (a, b) exponent relation in each substrate, with independently measured classes | OPEN | **OPEN** | The theory's real cross-substrate content (FRAMEWORK §1.4, §3.11) |
| J7 | Fractal vigilance (qualitative) | PRIOR ART | **PRIOR ART** | Quantitative version untested on a valid instrument |
| J8 | 'No one in charge, at every level' | KILLED | **WITHDRAWN** | Narrowed to J9 |
| J9 | No one *needs* to be in charge when shared memory is privately rewarded | OPEN | **OPEN** | Unchanged |
| J10 | Energy / second law *governs* adaptive organization above the cell | KILLED | **WITHDRAWN** | Strong form withdrawn (the theory itself: not literal above the cell). Replaced by J10′ |
| J10′ | **Physics applies at every level as a floor; it constrains design only where the binding ratio β_phys (actual cost ÷ thermodynamic floor) is near 1** (Chad, t1908) | new | **OPEN** | Measurable per scale (FRAMEWORK §3.11). No theorem in 𝓜 currently uses a physical floor, so the physics is idle in the proofs, not false. Cell scale is the test |
| J11 | In cells R2 is 'the thermodynamic floor', fixing the class | OPEN | **OPEN** | Derivation still owed; FRAMEWORK §7 fourth test |
| J12 | 'Team theory is static' | KILLED | **WITHDRAWN** | Our audit claim was false |
| J13 | 'No dynamic drift → structure theory exists' | KILLED | **WITHDRAWN** | MOVZ 2001; Aoki 1986 |
| J14 | Title 'A Theory of Adaptive Organization' | KILLED (as distinctive) | **DECIDED** | **Decided (Chad, t1908): keep the title**; cite Dessein & Santos 2006 prominently |
| J15 | Core mechanism C (drift destroys information; re-buying costs; selection keeps cheapest allocation) | OPEN | **OPEN** | Unchanged; no valid field test yet |
| J16 | Same three costs (upkeep/memory, prediction error, reads) at every level | new | **PRIOR ART** | True **by construction** of Axiom 5 (definitional), so not itself testable; the universal content is J6. Recursion qualitatively prior art (Beer's VSM) |

## K. Earlier repo claims (THEORY v1.0 and public X posts)

| # | Claim (short; full text in CLAIM_MAP_FINAL) | v1 status | **v2 status** | Why |
|---|---|---|---|---|
| K1 | Variational FE = thermodynamic FE (general) | KILLED | **WITHDRAWN** | General identity withdrawn. Replaced by K1′ |
| K1′ | **VFE = thermodynamic FE in the special case where the physical energy function equals −kT ln of the generative model** (Chad, t1908) | new | **OPEN** | Definitional coincidence under that identification [FRAMEWORK §1.3; no source verified this session]; needs a system where both sides are measured |
| K2 | Correction costs rise with temperature like Landauer | KILLED | **WITHDRAWN** | Metaphor replaced; τ tests are H11–H15 |
| K3 | Judgment = staying alive under the second law | OPEN | **OPEN** | Framing, not testable as stated |
| K4 | Risk ∝ shock × √(time to fix) ÷ buffer; ε_τ = −1 | KILLED | **PROXY-FAIL** | All five τ tests fail MV2 to varying degrees (H11–H15); out of scope for the structural core |
| K5 | Watching rises then collapses (cliff) | PRIOR ART | **PRIOR ART** | Unchanged |
| K6 | Copy error grows with hops and drift | PROVED | **PROVED (in-model)** | Unchanged (Markov states) |
| K7 | Stress strengthens up to a ceiling | OPEN | **OPEN** | Unchanged |
| K8 | Higher levels track slower causes | PRIOR ART | **PRIOR ART** | Refined by T7; level speed now measurable (FRAMEWORK §3.9) |
| K9 | √N fade of shared memory (math) | PRIOR ART | **PRIOR ART** | Kalman averaging |
| K10 | √N fade applied to languages (LANG1) | KILLED | **PROXY-FAIL** | MV2 (stable target, non-independent depositors, 91% uncoded forms), MV3, MV7, MV8. Out of the theorem's domain. FRAMEWORK §4.6 |
| K11 | Austronesian test | OPEN | **OPEN** | Not run; must pass FRAMEWORK §6.8 preconditions first |
| K12 | Geometric layers iff scale-free drift; level count | OPEN | **OPEN** | Unchanged |
| K13 | Spectrum → exponent relation | OPEN | **OPEN** | Mapping must be derived before any lock (FRAMEWORK §6.10). **The theory's headline; first theory item in QUEUE.md (SPECTRUM-MAP-DERIVE)** |
| K14 | Internal-model bound | PROVED | **PROVED (in-model)** | Self-checked; probably folklore |
| K15 | Universality classes of fixing | OPEN | **OPEN** | Unchanged |
| K16 | Pooling cools | PROVED | **PROVED (in-model)** | Standard algebra |
| K17 | Drift reduction substitutes for tracking | OPEN | **OPEN** | Unchanged |
| K18 | 'Every system pays for a model' | KILLED | **MATH-CORRECTED** | Counterexample: Kussell & Leibler 2005 bet-hedging; holds only with the population as the agent |
| K19 | Immune memory lifetime tracks drift | OPEN | **OPEN** | Same as H16 |
| K20 | Design rules 1 and 4 | OPEN | **OPEN** | Near-tautologies |
| K21 | Design rule 3 | PRIOR ART | **PRIOR ART** | Kalman; Muth |

## M. New rows from the measurement layer (night 2)

| # | Claim (short; full text in CLAIM_MAP_FINAL) | v1 status | **v2 status** | Why |
|---|---|---|---|---|
| M1 | **Raw sampling-rate rank gradient = a − κb** (class R: (1−κ)/2); rises with rank iff κ < a/b, which for class R coincides with T7's top-down condition κ < 1 | new | **PROVED (in-model)** | [DERIVED HERE] in FRAMEWORK §3.9; numerically checked (`checks/kappa_rank_gradient.py`); **not independently reviewed**. Shows the Enron/PIAAC growth bands assumed κ = 0. Must not be used to rescue Enron; spec §6.9 |
| M2 | Validity gates MV1–MV9 and the admissibility (anti-rescue) rule | new | **DECIDED** | Method, fixed before any new data (FRAMEWORK §2.2). Needs Chad's sign-off to be binding |
| M3 | Selection gate: mis-setting a class-R read rate by factor k costs (k + 1/k)/2 − 1 of tracking cost | new | **PROVED (in-model)** | [DERIVED HERE] FRAMEWORK §3.10; elementary |
| M4 | Bot self-application: high-drift shared project facts need a frequently refreshed shared store | new | **OPEN** | Anecdote (stale night-1 FORMAL/CLAIM_MAP); a cheap logged AI-scale test is possible (FRAMEWORK §3.12) |

---

## N. Night-2 results and audit corrections (v2.1, 15 Nov 2026)

| # | Claim | v1 status | **v2.1 status** | Why |
|---|---|---|---|---|
| N1 | VIGIL_ONA H1: higher rank seeks more outside its unit | new | **PROXY-PASS (downgraded)** | Locked fixed-effect rule met; random-effects/HKSJ pool includes 0; prior art (Mintzberg). Referee `reviews/night2/REFEREE/REPORT.md` |
| N2 | VIGIL_ONA H2: outward tilt beyond status | new | **PROXY-PASS (downgraded)** | Barely met; 82% one law firm; not robust to seniority/age; the advice item measures own-task advice |
| N3 | VIGIL_ONA H3: growth with span | new | **OPEN** | Overturned: N was a function of level; measured spans give ε ≈ 0 |
| N4 | SELF P1: item change is scale-free (regime B) | new | **OPEN (regime not established)** | Passed a Poisson null on statement times, but the observer-schedule null (0.60–0.92) contains 0.82; burstiness alone does not identify a scale-free spectrum |
| N5 | SELF P2/P3b: checks ∝ √(drift × stakes) | new | **PROXY-FAIL (scope)** | Regime-A instance; premise (stable per-item drift) unmet, P3a ρ = −0.06; stakes elasticity 2.0 excludes 0.5. Not a test of the spectrum core |
| N6 | SELF P4a: closed items freeze | new | **NOT EVIDENCE** | 0/21, every rival predicts it |
| N7 | Bridge: R1 elasticities a = b = 1/(1+2H), so the formal constants are functions of the spectrum | in Lemma 1(i) | **PROVED (in-model)** | Restating Lemma 1(i) as the link between the formal layer and THEORY §2; hold-last-value is a restricted estimator for H ≠ ½ |
| N8 | Proposition SG: surprise threshold for follow-up rises as ln(dormancy) with slope 1 in regime B, flat in regime A | new | **PROVED (in-model); PRIOR ART close** | Elementary Bayes + renewal hazard; Monte Carlo check `reviews/night2/AUDIT_checks/sg_check.out`; restless bandits, crawler revisit, Bayesian surprise are close. Not independently reviewed |
| N9 | SG ranking beats uniform and unaided judgment at picking follow-ups that change a claim status | new | **OPEN** | Locked in `queue/sg_rank.py`; scored from `queue/LEDGER.jsonl` after ≥ 15 completed items |

## Counts (167 rows in v2; section N adds 9 in v2.1, total 176)

| v2 status | Rows |
|---|---|
| PROVED (in-model) | 41 |
| MATH-CORRECTED | 17 |
| PROXY-FAIL | 13 |
| PROXY-PASS | 2 |
| OPEN | 44 |
| PRIOR ART | 20 |
| SIM-FAIL | 6 |
| NOT EVIDENCE | 13 |
| WITHDRAWN | 9 |
| DECIDED | 2 |

**Changes from v1, in one place.**
- The five 'killed on real data' rows (H1, H2, H7, K4, K10) are now **PROXY-FAIL**, with their failed gates named.
- The two 'passed' rows (H3, H9) are now **PROXY-PASS**. Both are also prior art in substance.
- Ten older field tests that had no row of their own are added as H11–H20 (the τ tests, BIO1, COLLAPSE1, MATCH1 D3, DRIFT1). Most are PROXY-FAIL, and the τ tests are out of scope for the structural core.
- Proof-level kills are relabeled **MATH-CORRECTED**: E5 (V ≥ 2), B10, E2, F9, F11, J1, J2, K18 and others. Locked simulation fails are relabeled **SIM-FAIL**: G6, G9, G15–G17, G20.
- Chad's decisions are recorded:
  - J14 (keep the title) and J3 (never 'law') are **DECIDED** / **WITHDRAWN**.
  - The physics claim is restated as J10′ (floors at every level, binding where β_phys ≈ 1).
  - The free-energy special case is K1′.
  - The 'same three costs' framing is J16 (definitional).
- New rows M1–M4 come from the measurement layer.

**Caveats.** This relabel was done by one executor and is not independently reviewed. M1 and M3 are elementary self-checked derivations. The gates (M2) become binding only once Chad signs off on them and they are locked before new data.
