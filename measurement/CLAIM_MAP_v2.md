# CLAIM_MAP_v2: A Theory of Adaptive Organization (GTAO), with proxy-aware statuses

Sunday 15 November 2026, about 08:15–08:20 AM ET (America/New_York). Grok Bot executor for Chad Mitchell, via Ace. Private. Nothing was posted, sent or made public. This map **supersedes the status column** of `reviews/night1/CLAIM_MAP_FINAL.md`. That file still holds the full evidence, scope and credit for each row, and row IDs are unchanged. The reason for every change is the measurement re-audit in `FRAMEWORK.md` (same folder). Gates MV1–MV9 are defined in FRAMEWORK §2.2.

**v2.1 note (15 Nov 2026, 09:02 AM ET).** Section N adds night-2 results and the audit corrections (`reviews/night2/AUDIT_DIVERGENCE.md`). Rows are interpreted under THEORY.md v1.2 §2.5: a constant quoted for class R (a = b = ½) is the H = ½ instance; for reset reads with Hurst H, a = b = 1/(1+2H). The headline hypothesis was rows K12–K13 and N7; it is untested, not peripheral. *(v2.3: superseded; see the v2.3 note.)*

**v2.3 note (15 Nov 2026, about 10:00 AM ET; THEORY.md v1.4).** THEORY v1.4 demotes the tracking layer (K12, K13, N11) to classical filtering and approximation theory plus a price; the headline is now the empirical bet N13 (measured-input optimality, OPEN) and its cross-scale form J6 (OPEN). Added: LEARNSIM rows G23–G29 (from `reviews/night2/LEARNSIM_REFEREE.md` §8, applied here with two in-model statuses defined below), N12 (formal exponents are α-independent for the two sensing technologies; self-checked, not refereed) and N13. N7's scope is updated. No existing row changes status.

**v2.4 note (15 Nov 2026; THEORY.md v1.4.1).** Per `reviews/night2/V14_REVIEW.md` Fix 2, J16 moves PRIOR ART → OPEN: definitional inside the model (Axiom 5), but as a claim about real systems it has testable content (sufficiency: no fourth cost type needed at any level, plus J6). The tally table is updated (PRIOR ART 20 → 19, OPEN 42 → 43). N12 is unchanged here; its narrowing (V14_REVIEW Fix 1) is pending a separate referee.

**v2.5 note (15 Nov 2026; THEORY.md v1.4.2, PR #18; edits independently reviewed, `reviews/night2/N12_EDITS_REVIEW.md`).** N12 PROVED (in-model) → **MATH-CORRECTED** per `reviews/night2/N12_REFEREE.md`: onset exponent confirmed for every α > 1; premises (same α for shared and private drift, exact reads at the level) and the α-dependent formal exponents (vigilance growth, mixed-technology e_u) stated; "only through constants" withdrawn.

**v2.6 note (15 Nov 2026, about 11:20 AM ET; QUEUE PRIORART-LFK-ALPHA, ledger 34–35).** N11 qualifier PRIOR ART (in substance) → **PRIOR ART (stated in mapped form)**, per `reviews/night2/PRIORART_LFK_ALPHA/REPORT.md` (locked decision rule D1). Status word unchanged, so the tally is unchanged. THEORY.md not edited; proposed credit and premise edits E1–E3 are queued (PRIORART-CREDIT-EDITS, TELEGRAPH-LINEAR-PREMISE) for independent review.

**v2.7 note (15 Nov 2026, about 11:21 AM ET; GITHUB-UPSTREAM, ledger 36).** Adds N14–N15 from `night2/GITHUB/RESULTS.md` (locked under THEORY v1.1/v1.2; read here under v1.4.2 §2.2). No existing row changes status; THEORY.md not edited.

**v2.8 note (15 Nov 2026, about 11:30 AM ET; QUEUE TELEGRAPH-LINEAR-PREMISE, ledger 37–40).** New row **N16** (PROVED in-model, leading order + numerics; self-checked; not refereed): for a two-state jump world the Bayes-optimal tracker's exponents differ from the linear tracker's at the same spectrum; exact reset reads and projection kernels are unaffected (`reviews/night2/TELEGRAPH_LINEAR_PREMISE/REPORT.md`). N11 evidence gets a pointer; no existing status changes, so the v2 tally is unchanged. THEORY.md not edited; edits E2′, E4–E6 proposed for independent review (TLP-EDITS-REVIEW). (Written as N14/v2.7 on branch queue-pick6; renumbered at merge after GITHUB-UPSTREAM took N14–N15/v2.7.)

**v2.9 note (15 Nov 2026, about 11:48 AM ET; QUEUE TELEGRAPH-REFEREE, pick 7, ledger 41–44).** N16 PROVED (in-model, not refereed) → **MATH-CORRECTED** (in-model; refereed) per `reviews/night2/TELEGRAPH_REFEREE/REPORT.md`: core results and the Conti & Mora diagnosis confirmed with independent code; the adaptation constant corrected (−0.7 → −(γ+1)); the projection-kernel invariance narrowed to regressions on the tracker's own observations; precision vs effort elasticity label fixed; leading-order error asymptotics PRIOR ART (Khasminskii & Zeitouni 1996; Golubev 2000) and the single-log form PRIOR ART in form (quickest detection). Section N is outside the 167-row tally, so the table is unchanged. THEORY.md not edited.

**v2.10 note (15 Nov 2026, about 12:35 PM ET; QUEUE D3-TWO-EXPONENT-OOS, pick 8, uniform slot, ledger 45–48).** New row **N17** (PROXY-FAIL for pure renewal) from `tests/D3_OOS/RESULTS.md` (lock `83aba94`; not refereed). N10 gains a pointer; no existing row changes status (H19 stays MATH-CORRECTED, N10 stays PROXY-PASS non-discriminating). Section N is outside the 167-row tally. THEORY.md not edited.

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
| **SIM-PASS** | (v2.3) A locked prediction about the authors' own non-circular simulator passed. In-model only; never support about nature |
| **SIM-INCONCLUSIVE** | (v2.3) A locked in-model test whose rule gave neither pass nor fail (including "NOT PASSED" composite tests with an inconclusive arm) |
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
| G23 | LEARNSIM ES onset exponents under the PREREG decade rule | new (v2.3) | **SIM-INCONCLUSIVE** | Locked; only 0.9 findable decade. `reviews/night2/LEARNSIM_REFEREE.md` §0, §8 |
| G24 | LEARNSIM C1, technology-independent exponent (rival) | new (v2.3) | **SIM-PASS** (downgraded) | Locked rule fires; not robust to dropping ρ = 0.04; RR N\* non-monotone. In-model, regime A |
| G25 | LEARNSIM PREREG_2 T1.8 overall | new (v2.3) | **SIM-INCONCLUSIVE** (T1.8 NOT PASSED) | RA PASS, AR INCONCLUSIVE (MV8 gate); RR known-groups INCONCLUSIVE. B9 stays PROVED (in-model) |
| G26 | LEARNSIM PREREG_2 RA: level class predicts ê; members'-class rival fails | new (v2.3) | **SIM-PASS** (in-model, regime A, RA only) | −0.736 [−1.03, −0.52] vs −0.759; rival −1.650. Robust under the referee's §4 checks. Not a T1.8 pass, not a field result |
| G27 | LEARNSIM V at onset, class R | new (v2.3) | **SIM-PASS** (locked rule) | RR and RRh geo-mean within ×/÷1.15; wide per-ρ CIs; in-model, regime A |
| G28 | LEARNSIM T3 factorial signs | new (v2.3) | **SIM-INCONCLUSIVE** | Two shared-side PASSes after an honest post-lock fix; no private-side confirmation |
| G29 | LEARNSIM pop-learner RR/RRh (secondary) | new (v2.3) | **NOT EVIDENCE** (robustness only) | Recovers T1 when learning noise is small; closer to an exhaustive optimiser |

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
| H19 | MATCH1 D3 redness sign | opposite sign (exploratory) | **MATH-CORRECTED** (v2.2, referee 15 Nov) | Was PROXY-FAIL. The locked negative sign was derived for the event autocorrelation, but MATCH1's a_need is a re-occurrence hazard; a and β co-move positively under renewal and under Cox worlds (`reviews/night2/SPECTRUM_MAP_REFEREE.md` §6, R7: Cox Spearman +0.975). Locked D3S: row N10 |
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
| J16 | Same three costs (upkeep/memory, prediction error, reads) at every level | new | **OPEN** (v2.4; was PRIOR ART) | Definitional inside the model (Axiom 5). Empirical content: sufficiency (no fourth cost type needed at any level) plus J6. OPEN. Recursion qualitatively prior art (Beer's VSM). The qualitative recursion is prior art; the three-cost sufficiency claim was not found stated (`reviews/night2/V14_REVIEW.md` Fix 2) |

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
| K12 | Geometric layers iff scale-free drift; level count | OPEN | **MATH-CORRECTED** (v2.2, referee 15 Nov) | One store iff rational spectrum (knife-edge at α = 2: one-store excess ≈ 0.14(α−2)²); K\* ∝ ln(span)·ln(stakes/upkeep) is prior-art exponential-sum complexity plus a price (Jiang et al. 2017; Benna & Fusi 2016); (log-span)^{2/3} withdrawn. `SPECTRUM_MAP_REFEREE.md` §4 |
| K13 | Spectrum → exponent relation | OPEN | **MATH-CORRECTED** (v2.2, referee 15 Nov) | Derived in-model (`reviews/night2/SPECTRUM_MAP/`, refereed in `SPECTRUM_MAP_REFEREE.md`). The stated exponents (½ for one pace; slope 1 and power-law forgetting for scale-free) are superseded: read rate 1/α (reset reads), memory ∝ (N/q)^{1/α} (τ_E^{1−1/α} only at fixed variance), kernel tail τ^{−(1+α/2)}. The replacement is mostly PRIOR ART (Wiener/Kalman, Afterman et al. 2022). Field relation untested |
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
| N7 | Bridge: R1 elasticities a = b = 1/(1+2H), so the formal constants are functions of the spectrum | in Lemma 1(i) | **PROVED (in-model)** | Restating Lemma 1(i) as the link between the formal layer and THEORY §2. v2.3: holds for hold-last-value and the optimal linear predictor (any rescaling-closed predictor class), not for a fixed-time-constant predictor (`SPECTRUM_MAP_REFEREE.md` §1, R1). THEORY v1.4 §2.5 |
| N8 | Proposition SG: surprise threshold for follow-up rises as ln(dormancy) with slope 1 **in the large-age limit** under a Lomax (decreasing-hazard) model of regime B (all-ages fit 0.947; exact 0.70 at a = 3Δ); flat in regime A | new | **PROVED (in-model); PRIOR ART close** | Elementary Bayes + renewal hazard; Monte Carlo check `reviews/night2/AUDIT_checks/sg_check.out`; restless bandits, crawler revisit, Bayesian surprise are close. Not independently reviewed |
| N10 | D3S (locked gap-shuffle): median Δβ in [−0.03, 0.05] | new | **PROXY-PASS (non-discriminating)** | Passed (0.024; reruns 0.021–0.023) on proxy "binary daily edit series"; a pure Cox world gives Δβ ≈ 0.045–0.05 at β ≈ 0.2, also inside the band (referee R6), so it does not support renewal over Cox. Out of sample (N17, v2.10) the renewal explanation itself failed on proxy (within-file gap order carries structure); N10 status unchanged |
| N11 | LFK generalisation τ_m ∝ τ_E^{1−1/α} (single store min(1−1/α, 2/3)) | new | **PRIOR ART** (stated in mapped form; v2.6) | Correct in-model (referee R5). Stated for general exponent as a Bayesian smoothing scale by Bialek, Callan & Strong 1996 (PRL 77:4693; arXiv cond-mat/9607180, read): ξ ∼ (ℓ^{2α_B−D}/NQ)^{1/2α_B}; with D = 1, α = 2α_B, N ∝ 1/NQ, q ∝ ℓ^{1−α} this is τ ∝ (N/q)^{1/α} and, at fixed noise, ℓ^{1−1/α} (`reviews/night2/PRIORART_LFK_ALPHA/REPORT.md`). Afterman et al. 2022 and Kleptsyna et al. 2020 state only the error rate (bandwidth is a one-line corollary). At fixed q the τ_E slope is 0. α = 2 geometric-mean form: BCS 1996 (smoothing); Mora & Nemenman 2019 (concentration sensing). Premise: Gaussian world or linear tracker; the Bayes-optimal tracker of a switching world adapts ∝ ln τ (Conti & Mora 2022); single log for the exact filter, C&M's own eq. 36 gives ln² from an incomplete Itô drift (N16, v2.8; confirmed by referee, v2.9) |
| N9 | SG ranking beats uniform and unaided judgment at picking follow-ups that change a claim status | new | **OPEN** | Locked in `queue/sg_rank.py`; scored from `queue/LEDGER.jsonl` after ≥ 15 completed items |
| N12 | Pooling-onset exponent −(1−b)/(1−a) does not depend on α: −1 for exact reset reads (a = b = 1/α) and information-rate pricing; −(1+θ) for continuous sensing with precision price ∝ precision^θ (a = αθ/(α(θ+1)−1), b = θ/(α(θ+1)−1)), every α > 1. Small-share onset vigilance ρ-free (reset), ∝ ρ^{−θ} in spend units and ρ^{−1} in precision units (priced precision). **Not α-free:** vigilance growth V ∝ N^a, mixed-technology e_u (θ + 1 − 1/α for a precision level over reset members), constants | new (v2.3); narrowed (v2.5) | **MATH-CORRECTED** (in-model): core exponent confirmed, scope narrowed; refereed | Referee `reviews/night2/N12_REFEREE.md` (checks `N12_REFEREE_checks/` c1–c5; also V14_REVIEW §4). Reason: degree-1 homogeneity of linear MMSE in (drift level, noise). Premises: same α for shared and private drift (priced precision: α_g − α_u < 1 suffices; else exponent −(1/Δ − b_g)/(1−a_g), asymptotic, numerically within ~3%, not proved); exact reads at the level (read noise → −2 at small ρ, α-dependent crossover; numerical, not proved); 𝒜₁, no broadcast cost, h = 0 or a ≥ b, small ρ. Withdrawn: "the spectrum enters the formal layer only through constants" and the 1 < α < 3 restriction (holds for α > 1). Novelty low: elementary corollary, not found stated. THEORY §2.5 |
| N13 | Measured-input optimality: with α, q, N and stakes measured on one strongly selected system, its read rate, memory time and store count lie near the THEORY §2.2 optima, at ≥ 2 scales | new (v2.3) | **OPEN** | THEORY v1.4 §0, §1 N6. The open empirical bet; no system has had all four inputs measured. Rivals: fixed budget share; universal ½ |
| N14 | GITHUB-UPSTREAM P1/P2: scheduled-CI read rate of unpinned upstreams has drift and stakes elasticities b = a = ½ (class R; v1.1 §2.2 Regime A), with regime-conditional bands (P1-R b ∈ [0.75, 1.25]; Allan 1/(1+2Ĥ) ± 0.15) | new (v2.7) | **PROXY-FAIL** | Failed on proxy "weekly CI-state change rate (q) vs nominal cron reads/week (E); stargazers (W)": b̂ = −0.06 [−0.24, 0.17], â = −0.10 [−0.17, −0.04]; KILL-CONDITION under all three bands. Gates failed: MV5 (q vs leave-one-out 0.07, vs upstream commits 0.04), MV7(i) (pinned/unpinned q ratio 1.10 [0.87, 1.41]), MV8(ii) (prize 0.13 < ε̂ 0.46); Tier 3, logged only. 81% of E at 1 or 7/week; 48% of units never changed state. Interpretation: switching world; exact reset reads keep the √ optimum at qT ≪ 1 (DERIVED HERE), so this is a failure of the drift instrument, not of A1. `night2/GITHUB/RESULTS.md` |
| N15 | GITHUB-UPSTREAM P3 (a = b), P5 (rank gradient a − κb), P6 (level vigilance ≥ 1 + (1+ρ)^{−½}) | new (v2.7) | **OPEN** | P3 consistent (â − b̂ CI [−0.27, 0.14]) but non-discriminating (both ≈ 0, the convention-crons rival). P5/P6 NOT ANALYSED (5 levels; 0 with ≥ 3 same-upstream comparators). Measured: ρ = 0.10 [−0.03, 0.38], κ = 0.82 [0.50, 1.49]. Vigilance stays OPEN |
| N16 | Jump-world premise of §2.2: two-state switching world (rate λ, levels ±μ), white noise N, κ = λN/μ² ≪ 1. Bayes-optimal adaptation time t_A = (N/2μ²)[ln(2μ²/λN) − γ − 1] + o(1) (single log; elasticities 1/ℓ, 1 − 1/ℓ, −2 + 2/ℓ in switching time, N, μ with ℓ = ln(2μ²/λN) − γ − 1, ≈ 0.17, 0.83, −1.67 at κ = 10⁻³; linear ½, ½, −1); MSE = μ²·2K₀(κ)/(K₀(κ)+K₁(κ)) ≈ 2λN[ln(2μ²/λN) − γ] (η → 1 in λ and N, 2 − 2η in μ; linear ½, ½, 1); precision elasticities 1/(θp+η), η/(θp+η), 2(1−η)/(θp+η) (effort: ×θp). q alone does not set them. Unaffected: exact reset reads (Bayes predictor = linear; MSE = OU's) and a regression kernel **on the tracker's own observations** (= Kalman kernel by iterated projections); a kernel on the true driver does discriminate | new (v2.8); corrected (v2.9) | **MATH-CORRECTED** (in-model): core confirmed, constant and kernel scope corrected; refereed; leading-order error PRIOR ART | Original `reviews/night2/TELEGRAPH_LINEAR_PREMISE/` (lock 4d55366). Referee `reviews/night2/TELEGRAPH_REFEREE/REPORT.md` (independent code `checks/`): Wonham/log-odds form, single log (quadrature slope 0.499θ/e-fold; own MC agrees), η (0.854/0.879/0.891) and reset-read invariance **confirmed**; "t_A ≈ (θ/2)[ln(4τ/θ) − 0.7]" **corrected** to −(γ+1) (quadrature 1.577; derivation §2); "any projection kernel" **narrowed** (Bayes kernel on the true driver differs from Kalman's by rel. L2 0.61 at κ = 1/60); precision vs effort label fixed. C&M 2022 eq. (20) read as Itô omits −x(1−x²)/θ: **confirmed** (published PRE text, author copy, unchanged; no erratum found); it also produces their eq. (41) P_wrong ≈ α/4 and eq. (42) α ln²α, which for the exact filter are (α/4)[ln(4/α) − γ] and K₀(α/2)/(K₀+K₁); their cross-correlation t_A is also single-log for the exact filter. Prior art: leading-order error, Khasminskii & Zeitouni 1996 (error probability) and Golubev 2000 (MSE), continuous time per Chigansky 2005 (read; originals not read); single-log delay = quickest-detection asymptotic (Shiryaev 1963; Tartakovsky & Veeravalli 2005; excerpts only); closed form 2K₀/(K₀+K₁) and γ+1 DERIVED HERE (likely classical; exact d = 2 density is Wonham 1964 / Liptser–Shiryaev per Chigansky). Pooling onset in jump worlds not derived (JUMP-WORLD-ONSET). Consistent with N14's interpretation note |
| N17 | D3-TWO-EXPONENT-OOS (locked, out of sample: 27 new GitHub repos, 5 Wikipedia category groups). Hypothesis R: each file's edit days form a renewal process (the D3S renewal explanation of D3) | new (v2.10) | **PROXY-FAIL** (pure renewal) | Failed on proxy "within-file consecutive log-gap correlation, binary daily edit series": M_w above its within-file-shuffle renewal null in 27/27 repos and 5/5 groups (median 0.225 vs null ≈ −0.01; locked rule ≥ 0.50 rejects; synthetic size 0–0.10 on renewal, power 1.00 on R6 Cox at β ≈ 0.2). Δβ > 0 detected (Wilcoxon p = 0.00027, median 0.046). The item's own statistics passed again but are non-discriminating (P1 Spearman(β, β_shuf) 0.863; P2 median Δβ 0.046 in band). D3's positive sign replicated (+0.645; expected under renewal and Cox, R7). Does not separate Cox, life-cycle trend and self-excitation (post hoc: survives trimming each file's first year and the repo's last year, 27/27). Lock `83aba94`; `tests/D3_OOS/RESULTS.md`. Not refereed |

## Counts (167 rows in v2; section N adds 9 in v2.1, 2 in v2.2, 2 in v2.3, 2 in v2.7 and 1 in v2.8 (N16 status corrected in v2.9) and 1 in v2.10; section G adds 7 in v2.3; total 191)

The table counts the 167 v2 rows only (section N and rows G23–G29 are not in it). v2.2 (referee, 15 Nov 09:40 AM ET) moved K12 and K13 OPEN → MATH-CORRECTED and H19 PROXY-FAIL → MATH-CORRECTED; v2.4 moved J16 PRIOR ART → OPEN; the table below reflects both.

| v2 status | Rows |
|---|---|
| PROVED (in-model) | 41 |
| MATH-CORRECTED | 20 |
| PROXY-FAIL | 12 |
| PROXY-PASS | 2 |
| OPEN | 43 |
| PRIOR ART | 19 |
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
  - The 'same three costs' framing is J16 (definitional in the model; OPEN as an empirical claim since v2.4).
- New rows M1–M4 come from the measurement layer.

**Caveats.** This relabel was done by one executor and is not independently reviewed. M1 and M3 are elementary self-checked derivations. The gates (M2) become binding only once Chad signs off on them and they are locked before new data.
