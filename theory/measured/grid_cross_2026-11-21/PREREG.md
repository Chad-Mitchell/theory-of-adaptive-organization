# GRID-CROSS preregistration: selection pressure and distance from the cost minimum

Written Saturday 21 November 2026, America/New_York, on branch `grid-cross-2026-11-21`, beside `main` `54a4562`. This file, `run_grid_cross.py`, and `grid_cross_lib.py` are hash-locked in `LOCK.txt` **before** any new selection-pressure score is recorded and **before** any non-GB distance, layer count, or spectrum is computed. None of those three files is edited after lock except to correct a typo that does not change a criterion, which would itself be a dated deviation.

**This is a new prereg, not a re-score of GRID-DX Part C (CLAIM_MAP P25).** P25 stays **UNTESTED** as locked in `theory/measured/grid/PREREG_GRIDDX.md` and `RESULTS_GRIDDX.md`. This lock does not change P25's verdict, rubric, or numbers, and it does not patch a correlation after seeing one. The question is the same one already in the repository (OPEN_WORK T3 / P25): across grids, does distance from the cost minimum shrink as selection pressure rises? The earlier lock could not score it (n = 1 complete distance; Hawaii UNTESTED; some sources HTTP 403; no grid qualified). This prereg fixes the documented rubric ambiguities, restricts sources to URLs actually fetched without an account, writes the qualification and "not applicable" rules before any new outcome, and hash-locks the runner and library with the prereg (T27 / SIM-1 standing rule).

The word "law" is not used in any status label. It appears in this file only when naming the hypothesis sentence or saying that a result is not a test of that hypothesis.

---

## Disclosed prior knowledge

Read before this lock, and not treated as a result of this test:

- The GRID-1 / 1b / 2 / 3 / 4 / 4b / S / DX files in `theory/measured/grid/`, including GB's four locked layers, γ = 2.09 (2026) and 2.02 (2024), diagnostic gap d1 = 3 under the B1 ruin-slack premise, the Part A verdict **NOT QUALIFIED**, and the Part C Pass 1 scores (GB 5, ERCOT 4, Australia NEM / Ireland-NI / Nordic / Continental Europe 1 as lower bounds where sources were missing, Hawaii UNTESTED).
- The S_N rubric ambiguity and the "missing source = 0, later treated as a lower bound" correction in `SELECTION_SCORES.md`.
- FRAMEWORK §9 and THEORY §3 on *strongly selected* (qualify before measurement; a class that fails any of the five items is not evidence either way).
- T27 (`core/bridge_2026-11-21/`): official in-model result **FAILED** (P1 and P2 passed, P3 failed). This field comparison does not rest on T27 as confirmation. The qualitative idea that excess cost should shrink as selection strength rises is already in that package and is not claimed as new.
- The T27 / SIM-1 (T28) process lessons: hash-lock the runner and library at lock time; compute exact gate values before locking; do not lock a bar the official procedure already misses; fresh seeds; deviations go in a dated file before any further official scoring.
- GRID-2's reconstruction (DV-GB1.2) and the later caveat that the balancing-mechanism term carries most of the reconstructed variance.

No new official S score, and no non-GB K_obs, γ, or d, has been computed for this prereg. Reachability checks (HTTP status, content type, and file size) were made before lock and are recorded in `DATA_SOURCES_REACHABILITY.md`. Newly reachable PDFs (including the AEMC reliability-settings schedule, which returned 200 in this pass after a 403 in GRID-DX) were not opened for numbers before lock.

---

## 1. What this is, and what it is not

The comparison asks whether, across named synchronous-area balancing systems, a higher preregistered selection-pressure score S sits with a smaller measured distance d1 from the sensing-limited cost minimum, the same distance already used for GB in GRID-DX Part C.

It is **a test of the hypothesis** (strongly selected systems minimize the cost of judgment) only if the class qualifies under §2, with that verdict recorded before any distance is used in it. If the class does not qualify, the same numbers may still be reported as a **gradient diagnostic** under §8. A diagnostic result is not evidence for or against the hypothesis. That split is the point of Chad and Ace's agreement that a miss on an unqualified system is "not an applicable test," and that a comparison across selection pressure is the next measurement, not a relabelling of P25.

No existing GRID-DX number is recomputed, patched, or deleted.

---

## 2. Qualification rule (written before any new measurement)

The operational definition is THEORY §3 / FRAMEWORK §9. A substrate class qualifies for a test of the hypothesis only if all five items hold, with the evidence recorded, **before** distances from this prereg are used in a hypothesis-test verdict:

(a) A cost-to-fitness map σ (fractional change in growth, survival or reproduction rate per fractional change in J) with its source. A priced incentive or VoLL is not σ unless the defined elasticity is computed from a sourced map.
(b) A population proxy N_e. **Class-specific proxy, preregistered here:** N_e is the number of independent *design-setting* authorities (TSO, ISO, or equivalent that can choose the product suite) competing in the same synchronous area or the same officially coupled market, with entry and exit or a published comparison. Competition among service *providers* is not N_e. A usual single-buyer ISO/TSO has N_e = 1. Cities, nation-states, global economies and the biosphere remain excluded; a grid operator is not thereby a nation-state, but a single national TSO still has N_e = 1 under this proxy.
(c) The selection-resolvable band ε = 10/(σ·N_e). The prediction band is at least ε wide.
(d) Power: the band plus measurement error excludes the design of at least one named rival from FRAMEWORK §9 item 6 (R1 fixed budget share; R2 exponent ½; R3 the world's time scales with no price dependence).
(e) A redesign time T_red (time to close 1 − 1/e of the gap to the new argmin J after a step change in prices or in the world's statistics), with at least 10 T_red of the same world.

The class for this prereg is **synchronous-area balancing designs**, the same class as GRID-DX Part A. Qualification is recorded for the class as scored, not retrofitted after a correlation.

**If any item fails, or is not established, the comparison is not a test of the hypothesis.** The headline for that role is **NOT A TEST (not qualified)** or **NOT A TEST (qualification not established)**, and the result is not evidence either way. GRID-DX already found GB not qualified (N_e = 1; σ not computed; T_red never defined; outturn inertia changed). This prereg does not assume a different outcome; it requires the check to be written against this proxy and the sources in §5 *before* Pass 2 distances are used in a hypothesis verdict.

σ is not inferred from S. S is a rubric, not qualification.

---

## 3. Selection pressure (proxies locked before Pass 1)

Window, for every grid: **1 January 2011 to 21 November 2026**.

S = S_mkt + S_pen + S_rel + S_own, each in {0, 1, 2}, so S ∈ {0, …, 8}. Higher means stronger selection pressure as operationalised here. Scores use only official or primary regulator / TSO / ISO / statutory sources whose URLs were fetched without an account in this pass (or, after lock, the same class of URL, recorded in the Pass 1 file with its HTTP status). A missing official source is **MISSING**; that component is not guessed, and the grid's S is a **lower bound**, not a demonstrated zero.

No component is scored from how close the grid's products already look to an optimum.

These four proxies are the ones named for this prereg (market structure, penalty regimes, reliability standards with enforcement, ownership). They are related to, but not the same as, the GRID-DX S_σ, S_N, S_red, S_ruin rubric. Old Pass 1 numbers are not copied forward.

### 3.1 S_mkt — market structure / design competition

Written so that the GRID-DX S_N ambiguity cannot recur: score 0 and score 1 are mutually exclusive.

- **2:** a sourced N_e ≥ 10 independent *design-setting* authorities competing in the same synchronous area or the same officially coupled market, with entry and exit or a published comparison.
- **1:** more than one design-setting TSO/ISO in the synchronous area, acting jointly rather than as competing lineages, **or** legally required competitive procurement of the services (providers compete; a single buyer still sets the suite).
- **0:** a single system operator sets the product suite, **and** there is no sourced legally required competitive procurement, **and** no class-specific N_e ≥ 2.

If legally required competitive procurement is sourced, the score is 1, not 0, even when there is a single buyer. Score 2 is reserved for genuine design-lineage competition. Competition among providers is not competition among designs.

### 3.2 S_pen — penalty / incentive regime

- **2:** a sourced official financial incentive or penalty on the *operator lineage* (or residual claimant) that is a documented function of balancing or frequency-control cost, or of reliability outcomes, with a numerical rate, cap, or formula, in force for at least one year in the window.
- **1:** a documented, priced official link from balancing cost or blackout risk to market or operator financial outcomes that is not a formula on the operator lineage itself (an official VoLL or scarcity price used in reserve planning; a market-wide ORDC or equivalent). This is weaker than σ and is not qualification under §2.
- **0:** none found. If a cited URL could not be retrieved, **MISSING**.

### 3.3 S_rel — reliability standard with enforcement

- **2:** a published official reliability, frequency, or loss-of-load standard with a numerical value, documented as an *input to* reserve or frequency-response design, **and** a sourced enforcement mechanism (a financial penalty, a licence condition, a legally binding obligation, or an automatic scarcity-pricing rule that applies when the standard is missed).
- **1:** such a standard exists with a numerical value, but the cited source does not show enforcement, or does not show use as a design input (exactly one of those two is missing).
- **0:** none found, or **MISSING**.

### 3.4 S_own — ownership / residual claim

- **2:** the residual financial claimant for balancing or reliability cost is sourced as retaining a material share of cost over- or under-runs (no automatic full pass-through), whether for-profit or not.
- **1:** a legally unbundled not-for-profit ISO/RTO, public corporation, or state-owned TSO, with official cost recovery or pass-through of balancing costs, or with that ownership form sourced and no residual-claim share sourced.
- **0:** a vertically integrated monopoly with full official pass-through and no sourced residual claim, or ownership not documented (**MISSING** if a cited URL failed).

For-profit ownership alone does not score 2: a rate-of-return or full pass-through can weaken pressure, not strengthen it. The same fact is not given a 2 in both S_pen and S_own: if a single incentive scheme is the only evidence of a residual claim, it scores under S_pen, and S_own is at most 1 from the ownership form.

Product *introductions* may be noted as dated institutional events in Pass 1. Their delivery times and the resulting layer counts are not recorded in Pass 1 files.

---

## 4. Grids, in this order

1. Great Britain (NESO / former National Grid ESO) — the same system as GRID-2 and GRID-DX.
2. Australia NEM (AEMO).
3. ERCOT (Texas).
4. Ireland and Northern Ireland (EirGrid / SONI; one synchronous island).
5. Nordic synchronous area (shared FCR / aFRR markets).
6. Continental Europe (shared FCR / aFRR markets).
7. An island system with public data, first choice Hawaii (Hawaiian Electric), otherwise the first of New Zealand (Transpower) or Cyprus (TSOC) whose institutional sources can be scored without guesswork, named as a substitution with the reason.

If a pass cannot complete all seven, the results list what was scored, what is **UNTESTED**, and what remains. No grid is added to the official set unless its institutional landing page or a cited official file was fetched without an account in the reachability pass or in a dated note before Pass 1 scoring starts.

Public data only. No account creation, no paywalled login, no emailed request. A landing page or API that requires a form, a registration, or an API key is treated as unavailable; the missing field is **UNTESTED** or **MISSING**, not guessed.

---

## 5. Sources (only those actually fetched)

The reachability log, with HTTP status, content type, and (for files) content-length, is `DATA_SOURCES_REACHABILITY.md`. Only sources that returned a successful fetch without an account are eligible. "LOGIN_HINT" on a public page that still returned the official content (a header "Sign in" link) is not treated as a wall. A 403, a WAF challenge, a registration-only API, or a form-gated download is excluded.

**Included (fetched, no account), for institutional scoring and, where noted, as a data series that still is not by itself a d1 input:**

- NESO CKAN API, no login: system-frequency package and system-inertia package (`api.neso.energy`, HTTP 200, JSON). The 1-s frequency and inertia series used by GRID-2 remain the GB sources; they are not re-downloaded for a new GB spectrum before lock.
- Ofgem ESORI Guidance 2023–2025 PDF (HTTP 200, application/pdf, 509,297 bytes) and the 2017 BSIS final-proposals PDF already cited in `QUALIFICATION.md` (HTTP 200, 785,613 bytes).
- NESO Frequency Risk and Control Report 2025, document 356356 (HTTP 200, application/pdf, 1,142,444 bytes).
- Elexon BMRS API root responds without an account (JSON validation error when required query parameters are omitted). A new full BOALF/PN series was not downloaded in this pass; GRID-2 already used that API.
- AEMC *Schedule of reliability settings* PDF for 2026–27 (HTTP 200, application/pdf, 235,556 bytes). This URL returned 403 in GRID-DX; it is reachable now. **The PDF was not opened for numbers before this lock.**
- AEMC media release and primary-frequency-response rule-change pages (HTTP 200, HTML).
- AEMO quarterly Frequency Monitoring PDFs for Q1, Q2 and Q3 2026 under `/-/media/files/.../quarterly-reports/2026/` (HTTP 200, application/pdf, 3,004,168 / 2,711,586 / 2,666,439 bytes). These are reports, not a verified 4-s time series.
- ERCOT 2022 Biennial ORDC report PDF (HTTP 200, application/pdf, 1,251,273 bytes) and the 12 June 2023 ECRS news release (HTTP 200, HTML); ERCOT Grid Information and Data Access Portal pages (HTTP 200, HTML). The Data Access Portal and Public API text state that API use requires registration; those APIs are excluded.
- EirGrid DS3 programme page (HTTP 200, HTML); DS3 System Services Protocol v4.1 (October 2024) PDF (HTTP 200, 1,042,484 bytes); current System Services volume-requirements information paper (HTTP 200, 487,820 bytes); Gate 10 (9 January 2024) and Gate 13 (26 June 2025) bidder-session PDFs (HTTP 200, 1,192,561 and 1,276,763 bytes); EirGrid real-time system information page (HTTP 200, HTML); SONI homepage (HTTP 200). These System Services PDFs were the class of source that returned 403 in GRID-DX.
- Fingrid Open Data dataset 339 page (HTTP 200, HTML, CC BY 4.0) and direct monthly 10 Hz frequency archives, e.g. `https://data.fingrid.fi/files/339/2026/2026-09.7z` (HTTP 200, application/x-compressed, 65,757,645 bytes), **no API key**. The REST API itself requires a registered key and is excluded. These archives are closed-loop frequency, not pre-control imbalance, and were not downloaded before lock (HEAD only).
- Svenska kraftnät Nordic aFRR capacity-market notice of 7 December 2022 (HTTP 200, HTML).
- ENTSO-E FCR Cooperation page and PICASSO go-live notice (HTTP 200, HTML).
- NERC BAL-003-2 PDF (HTTP 200, application/pdf, 1,107,601 bytes) and the NERC reliability-standards landing page (HTTP 200, HTML, redirected).
- EIA Electricity Grid Monitor landing and US48 dashboard pages (HTTP 200, HTML). No sub-hourly official series was retrieved; Form 930 is hourly and cannot support the locked d1 band.
- Hawaiian Electric homepage and RSWG monthly-reports page (HTTP 200, HTML).
- Transpower system-operator page and quarterly system-performance-report page (HTTP 200, HTML).
- Cyprus TSOC homepage (HTTP 200, HTML).
- Netztransparenz 2022 1-s frequency zip, static link already recorded in `DATA_SOURCES.md` (HTTP 200, application/x-zip-compressed, 48,053,151 bytes). HEAD only; not re-downloaded. This is closed-loop frequency. The 1-s aFRR setpoint download remains form-gated, as already recorded.

**Fetched but not used as a d1 series, or excluded as unavailable:**

- AEMO HTML landing pages (`/about/what-we-do`, Fast Frequency Response, frequency-and-time-deviation-monitoring) returned HTTP 403 to curl from this environment. The frequency-monitoring landing page and the "What we do" page were retrieved by a separate HTTP fetch (WebFetch) as HTML text, without an account; guessed direct URLs for "Mainland frequency data 2026" annual files returned 302 to a 404/403. **The 4-s annual frequency files are not included**, because a direct file was not successfully fetched.
- ERCOT Public API / Data Access Portal: registration required; excluded.
- Fingrid REST API: API key required; excluded (static 7z files above are included).
- ENTSO-E Transparency Platform API and SFTP: registration required; the public web app is a JavaScript shell (the HTML root returned 200 but not a data table). Form-gated or account-gated export is unavailable. Typical published imbalance is 15 min, which cannot support a band that includes 1 min.
- EUR-Lex texts of Commission Regulation (EU) 2017/1485 (SOGL): WAF challenge / HTTP 403 from this environment; **not included**.
- EIA Open Data / Form 930 file downloads: the `/electricity/930/` path returned 503; a guessed Interchange xlsx URL returned HTML, not a spreadsheet. No EIA time series is included.
- Elia and TenneT system-information HTML pages: HTTP 403 from this environment; excluded.
- nationalgrideso.com: connection failed (the successor is neso.energy, already included).
- AEMC "reliability panel" path used as a guess: HTTP 404; excluded.

---

## 6. Distance from the minimum (consistent with the GB analysis)

The GRID-2 / GRID-DX distance is kept. A different proxy would not be a consistent comparison.

**Counting rule for K_obs** (the GRID-2 rule, applied to official in-force products on a stated date in 2025–2026, or the latest official date in the window): group products by official full-delivery time; two products that share a speed (as DC and DM do in GRID-2) count as one layer; mandatory generator droop that is a standing code obligation is counted as one layer if it is in force and has a distinct official time, else noted and excluded consistently with GRID-2's choice (MFR is added to the reconstruction; layers are the listed products), which will be stated per grid. The date and the product list are cited.

**d1 (sensing-limited, ruin slack).** If a measured *open-loop or official pre-control imbalance* spectrum for that grid, in a band of at least two decades that includes 1 min–1 h, is a power law with γ ∈ [1.7, 2.3] or a single first-order mode, then K* = 1 by Theorem L1 / Master Theorem (iii) under the ruin-slack premise, and d1 = max(0, K_obs − 1). If the same class of spectrum is measured and is *not* of that form, K* is the number of separated modes under the GRID-2 fit and separation rule (Lorentzian K = 0…5 + white versus power law + white, BIC; separated at ×2.5 and ≥ 5 % of band variance), and d1 = max(0, K_obs − K*). If no such spectrum is available, d1 is **UNTESTED** for that grid. An official prose statement that "imbalance is like a random walk," without a number, is not enough.

Closed-loop *frequency*, even at 0.1 s (Fingrid) or 1 s (NESO, Netztransparenz 2022), is not a pre-control imbalance spectrum. Using it for d1 would not be consistent with the GB analysis, which reconstructs D(t) from frequency, inertia, delivered response, and balancing-mechanism dispatch (DV-GB1.2). d1 is therefore UNTESTED unless an official open-loop imbalance series is fetched, or a reconstruction with the same ingredients as DV-GB1.2 is possible from no-account sources.

GB uses the already-recorded GRID-2 / G3a fits: K* = 1, K_obs = 4, d1 = 3, **under B1's ruin-slack premise**. B1 assumes ruin slack; GB's ruin constraint binds (FRCR DC sized for an 1,800 MW largest loss). That gap may reflect costs or constraints the design space does not represent; it is not shown to be excess. If official evidence shows the ruin constraint binds for a grid, that grid's d1 is tagged **BINDING-RUIN**. A locked sensitivity drops all BINDING-RUIN grids from the official diagnostic; if that leaves n < 5, the diagnostic is **UNTESTED** on the sensitivity (and the headline follows §8).

**d2 (extended J).** As in GRID-DX B2 / C.4: official prices and durations if they can be sourced without an account. If assumed terms decide the integer K* or the sign of the gap, d2 is **INCONCLUSIVE** for that grid and is not used in the rank test.

---

## 7. Two-pass protocol

**Pass 1** starts only after `LOCK.txt` is written and this file, the runner, and the library hash-match it. For each grid, compute S from the locked rubric, citing fetched URLs and HTTP statuses, and commit `SELECTION_SCORES.md` and `selection_scores.json` **before** Pass 2. Delivery times and layer counts are not recorded in Pass 1 files. GB may use institutional facts already in the repository; those are not a Pass 1 leak of a non-GB design.

**Pass 2** starts only after that commit. It records K_obs, any measured or official pre-control spectrum, d1 / d2, the §2 qualification record, and then the rank test. A grid with a complete Pass 1 score but unsourced Pass 2 inputs is **UNTESTED** on the distance and is dropped from the rank test.

If, after the lock, public no-account data are still insufficient for n ≥ 5 complete (S, d1) pairs, the official result of the comparison is **UNTESTED**. A RESULTS file then lists exactly what is missing. Pass 1 may still be completed and committed.

Compute at nice 19. Do not touch `/workspace/looper` or `/workspace/gtao-evo`.

---

## 8. Directional prediction, effect-size bar, kill criteria, and not applicable

**Prediction (preregistered):** grids with higher S sit closer to the cost minimum: Spearman rank correlation ρ(S, d1) is negative. d1 is the primary distance. d2 is a secondary test only if at least five grids have a complete d2; it is not required for the headline.

**Official test** (computed by `grid_cross_lib.py`, gates fixed before any official ρ): mid-rank Spearman correlation of the observed S and d values. The null is the exact permutation distribution of the observed d values against the fixed observed S values (all n! assignments for n ≤ 10; for n > 10, 100,000 permutations with RNG seed `20261121137`). One-sided p for the predicted direction is the share of permutations with ρ ≤ ρ_observed. The opposite-direction p uses ρ ≥ ρ_observed. Ties are kept; they are not broken.

**Effect-size bar:** ρ ≤ −0.5, in addition to the p-value bar. The p-value bar is exact (or the locked Monte Carlo for n > 10) at α = 0.10 one-sided. A no-tie reference table, computed before lock on permutations of distinct ranks 1…n and *not* used as the official gate once ties are present, is:

| n | max ρ with exact one-sided p ≤ 0.10 (no ties) | exact p at that ρ |
|---|---|---|
| 5 | −0.800000 | 0.066667 (8/120) |
| 6 | −0.657143 | 0.087500 (63/720) |
| 7 | −0.571429 | 0.100000 (504/5040) |
| 8 | −0.523810 | 0.098313 (3964/40320) |
| 9 | −0.466667 | 0.096900 (35163/362880) |

For n = 5–8 the exact no-tie p-bar is already at least as strict as ρ ≤ −0.5; for n ≥ 9 the effect-size floor is the stricter of the two.

**Population:** every grid in §4 that has a complete integer S (lower-bound S is not "complete" unless a sensitivity that takes the bound as the score is reported separately) and a complete (not UNTESTED, not INCONCLUSIVE) d1.

**Diagnostic verdict:**

- If n < 5 complete pairs, the diagnostic is **UNTESTED**. Ranks may be reported descriptively; no pass or fail.
- If every complete pair has the same S, the diagnostic is **NOT APPLICABLE** (no variation in the pressure proxy).
- If n ≥ 5: **PASS on diagnostic** if ρ ≤ −0.5 and p ≤ 0.10 in the predicted direction, and the robustness clause holds; **FAIL on diagnostic** if ρ > 0 and the opposite-direction p ≤ 0.10, and the robustness clause holds; **NEITHER** otherwise (including ρ = 0, and including a negative ρ that misses the effect-size or p bar).
- **Robustness clause.** If including or dropping any single complete grid, or assigning every UNTESTED grid the most extreme d in {0, max observed complete d} in either direction, or replacing every lower-bound S once by 0 and once by 8, would change the PASS / FAIL / NEITHER label, the headline is **INCONCLUSIVE** and the leave-one-out and bound tables are reported.
- If the BINDING-RUIN sensitivity of §6 leaves n < 5, the diagnostic is **UNTESTED** on that sensitivity; if it leaves n ≥ 5 and changes the label, the headline is **INCONCLUSIVE**.

**Not applicable, as a test of the hypothesis:** the class fails, or does not establish, any §2 item. This is reported even when the diagnostic is scored. A PASS or FAIL on diagnostic is then not a pass or fail of the hypothesis.

**Not applicable, as a gradient diagnostic:** n < 5; or no variation in S among complete pairs; or every complete d1 is BINDING-RUIN and dropping them leaves n < 5.

**Kill criteria.** A robust **FAIL on diagnostic** kills the *gradient prediction as operationalised here* for this set of systems. It does **not** refute the hypothesis unless the class qualified under §2 before distances were used. If the class had qualified, a robust FAIL would also be a miss for this substrate class under FRAMEWORK §9 item 5, with n_min = 5 and α = 0.10 as fixed here. A robust PASS on diagnostic supports the gradient prediction only as a proxy comparison; it supports the hypothesis only if the class qualified and the minimum also beats a named rival under the same error budget (FRAMEWORK §9 items 5–6). Predictions will not be patched after seeing official ρ. A change of criterion, if one is ever needed, goes in a dated DEVIATIONS file *before* any further official scoring; the original gates remain the official result of this prereg.

---

## 9. Pilot (not official)

The permutation algorithm, the no-tie reference table, the effect-size floor ρ ≤ −0.5, n_min = 5, and α = 0.10 were fixed before any official S or non-GB d of this prereg. They are design inputs, not results. Already-known GB d1 = 3 was not used to set the bar. Official seeds or permutation streams were not evaluated on official pairs, because no official pair list exists until Pass 2.

---

## 10. What would not be a rescue

- Changing the d1 rule to accept closed-loop frequency, a 15-min imbalance series, or a prose "random walk" claim after seeing official scores.
- Rescoring S after any distance is recorded, or copying GRID-DX S numbers into this rubric.
- Patching P25, or treating this lock as a re-score of P25.
- Treating a diagnostic PASS or FAIL as a test of the hypothesis when the class did not qualify under §2.
- Changing ρ ≤ −0.5, α, n_min, the permutation rule, or the robustness clause after seeing official ρ.
- Editing `run_grid_cross.py` or `grid_cross_lib.py` after lock (T27 standing rule).
- Dropping a failing grid and walking the substitution list to replace it after seeing ρ.

---

## 11. Predicted claims

P25 is unchanged (OPEN; rank test UNTESTED as locked). After this run, a new CLAIM_MAP row may record GRID-CROSS: qualification under §2, the diagnostic verdict under §8, and the not-applicable split. That row is not added in the lock commit.
