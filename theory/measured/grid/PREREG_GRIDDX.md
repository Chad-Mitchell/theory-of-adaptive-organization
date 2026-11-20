# GRID-DX preregistration: qualification audit, GB prescriptive diagnosis, cross-grid selection test

Written Friday 20 November 2026, 1:22 PM ET (America/New_York), on branch `v2.6-griddx`, **before** (i) recording a qualification verdict, (ii) running any optimizer or computing a predicted saving, (iii) scoring any 2020–2024 reform direction, and (iv) recording any non-GB grid's layer count, delivery times, or distance to a cost minimum.

This file is the lock. Later notes may add sources or implementation details; they may not change the verdict rules, the selection-strength rubric, the distance metrics, the rank test, or the wording map.

## Disclosed prior knowledge

- The GRID-2 / G3a / GRID-4 / GRID-S results in this repository, including GB's four locked layers, γ ≈ 2.09 (2026) and 2.02 (2024), the G1 "FAIL on proxy" arm score, G3b, and the post-hoc actuation/ruin diagnosis, were read before this prereg. Parts A and B concern that already-public GB case. They do not use any new outcome statistic computed after this lock.
- GRID-2's lock commit is `36416d2835f4afe5b6efca8e4b5eeda24620fca8` (Friday 20 November 2026, 9:56:21 AM ET). The operational definition of "strongly selected" applied in Part A is the text in `THEORY.md` §3 and `measurement/FRAMEWORK.md` §9 **as those files stood at that commit**, not any later wording.
- The author has general prior knowledge that other named markets have frequency-control products (for example FCAS, DS3, FCR/aFRR, ERCOT responsive reserve). That knowledge is not used as a recorded layer count or a distance. Part C is two-pass: selection-strength scores are computed from institutional sources and committed **before** any layer-design numbers for those grids are recorded or used in a test.

## What this is, and what it is not

Part A asks whether GB's balancing system **qualified**, under the definition as written at the GRID-2 lock, as a test of the hypothesis. Part B asks what the cost says the GB layering should be, and whether recent reforms moved toward that minimum: a prescriptive diagnosis of a system, whether or not the system qualifies. Part C asks whether, across grids, stronger selection as defined here goes with a design closer to the cost minimum.

No existing GRID-2 or G3a number is recomputed, patched, or deleted.

The word "law" is not used here except when quoting the hypothesis sentence or the mandated Part A label below.

---

## Part A — Qualification audit (GB balancing system, at the GRID-2 lock)

### A.1 Definition applied (verbatim at `36416d2`)

From `THEORY.md` §3 at that commit:

> **Strongly selected (operational; every item preregistered before any measurement).** A substrate class qualifies for a test of the hypothesis only if all five hold, with the evidence recorded:
> (a) *a cost-to-fitness map:* σ, the fractional change in the class's growth, survival or reproduction rate per fractional change in J (for cells, the measured growth-rate cost of the design variable; for firms, the elasticity of survival or profit margin to J, with its source); no map, no qualification;
> (b) *a population proxy:* N_e, the number of independent lineages competing in the same world per redesign time (cells and microbes: measured; firms: independent firms in one market over one redesign time, with entry and exit); **cities, nation-states, global economies and the biosphere are excluded until a class-specific proxy is preregistered**, because for them N_e is not defined;
> (c) *selection resolves the band:* ε = 10/(σ·N_e) … the predicted band around argmin J is at least ε wide whatever the measurement error …;
> (d) *power:* the band, with the measurement error added, must exclude the design of at least one named rival (R1–R3, `measurement/FRAMEWORK.md` §9);
> (e) *a defined redesign time:* T_red is the time the class's design takes to close 1 − 1/e of the gap to its new argmin J after a step change in the prices or in the world's statistics, measured or preregistered from the class's turnover; the lineage must have faced the same world for at least 10 T_red …

And: "A class that does not qualify is not evidence either way."

From `measurement/FRAMEWORK.md` §9 at the same commit: "Qualifying (decide before any measurement; all five, with the evidence recorded)." A class that fails any item "is excluded and is not evidence either way."

The README "How it dies" paragraph at that commit is the short form of the same five items. No other definition is used. Later scope rule G3b is **not** used to decide qualification: it was written after the GRID-2 miss and applies only to tests locked after `b7f69e8`.

### A.2 What is inspected

1. `theory/measured/grid/PREREG_GRID2.md` at and after `36416d2`, and the GRID-1 / GRID-1b preregs then in force: whether (a)–(e) were recorded before measurement.
2. The repository at `36416d2` for any preregistered class-specific population proxy for grids, electricity system operators, or national infrastructure.
3. Public official sources (NESO, National Grid ESO, Ofgem, DESNZ/GOV.UK, and documents they host) for: a sourced σ; an N_e; a defined T_red; and a count of qualifying redesigns in the window below. Every factual claim carries a real URL. Nothing is invented. A date without a primary official source is not counted.

**Qualifying redesign (for (e) and for the later S_red score):** a dated official go-live of a new GB frequency-response or reserve *product*, or a dated official cessation or named replacement of such a product. Not counted: consultations, roadmaps, or webinars without a go-live; monthly or daily tender-parameter changes; volume-target changes; performance-monitoring tweaks; organisational renames (including ESO → NESO) unless they changed the product set; Grid Code typographical amendments. Mandatory Frequency Response is one standing Grid Code obligation; its existence is noted, but routine holding-volume updates are not redesigns.

**Window for the (e) count:** 1 January 2011 to 20 November 2026 (from fifteen years before the GRID-2 lock through the lock day). A sourced go-live outside the window may be listed for context and is not counted in R. If a product's start year cannot be sourced, it is not counted.

**Same-world check:** official NESO/ESO/National Grid evidence that system inertia and/or the generation mix changed materially in the window (a published inertia time series, or a published statement of falling inertia or a changing mix as a reason for new products) means the lineage did not face "the same world" for the whole window.

### A.3 Verdict rules

All five items must have been **preregistered with recorded evidence before GRID-2's measurement**, and must hold.

- **QUALIFIED** if and only if (a)–(e) were each recorded in a lock-time prereg with evidence, and the evidence gathered now confirms that each item holds.
- **NOT QUALIFIED** if any of: (a) no sourced σ was recorded, or none can be cited that matches the definition ("no map, no qualification"); (b) no N_e was recorded, or N_e is not defined for this system and no class-specific proxy was preregistered (the nation-state/city exclusion is applied if the system is a single national operator with no such proxy); (c) or (d) cannot be computed because (a) or (b) failed, or the computed band fails the stated test; (e) T_red was not preregistered, or 10 T_red in the same world is not met. One failed item is enough.
- **UNDETERMINED** only if no item has failed, and at least one remaining item cannot be decided from the sources found. Absence of a map is not undetermined: it is a failed (a).

A regulatory incentive scheme, a Value of Lost Load used in planning, or a not-for-profit allowed-revenue model is **not** σ unless a source gives the defined elasticity of growth, survival, or profit margin of the operator lineage (or of a declared firm class) to J. Competition among *providers* of a product is **not** N_e of *design lineages*.

### A.4 Wording map (locked; Chad t2005)

If the verdict is **QUALIFIED**: say so plainly. The locked G1 arm score and the CLAIM_MAP P19 / P21 PROXY-FAIL statuses are left unchanged.

If the verdict is **NOT QUALIFIED**:

- The correct record is that GRID-2 tested the cost's prescriptive design on an unqualified system: it is **not** a test of the hypothesis. The measured mismatch (a random-walk imbalance, γ in [1.7, 2.3], against four operational layers) is kept as a **diagnosis of a patient**.
- Label, used in `theory/measured/SYNTHESIS.md`, README (if it names the GRID-2 verdict), and the CLAIM_MAP **headline status**: `NOT APPLICABLE (system not qualified): a diagnosis of a patient, not a test of the law`.
- In CLAIM_MAP, add a dated retype and a status-mapping row (new status **NOT APPLICABLE**). P19 and P21 (the 2024 replication, locked under the same un-checked qualification) move to **NOT APPLICABLE** by that mapping. The previous PROXY-FAIL label and the locked G1 numbers stay in the cell text and in `RESULTS_GRID2.md` / `RESULTS_GRID3_4.md` as historical record. Those result files are not rewritten so as to delete the FAIL arm score; a dated note is appended. History is not deleted.
- Record, as a dated note and a DEVIATIONS entry, that the qualification check required by THEORY §3 and FRAMEWORK §9 ("decide before any measurement; all five, with the evidence recorded") **should have been done before scoring and was not**.
- Do not use "FAIL" as the headline verdict for GRID-2 or G3a in SYNTHESIS, README, or the CLAIM_MAP status column.

If **UNDETERMINED**: report which items are open, change no headline status, and do not soften the locked arm scores.

### A.5 Claim-map versioning

Current main is CLAIM_MAP v2.63 (commit `b4f264f`). Open draft PR #112 already uses v2.64. This work, if it edits the map, uses **v2.65** so the notes do not collide.

---

## Part B — Prescriptive diagnosis (GB)

Computed only after this file is committed. Uses measured inputs already in the repository where they exist. Public NESO/Elexon data are re-downloaded only if a stated input is missing; any such file is deleted after use, with SHA-256 and URL recorded in `DATA_SOURCES_GRIDDX.md`.

### B.1 Two cost functions, stated in advance

**B1. Sensing-limited J, ruin slack** (the J under which Master Theorem (iii) / Theorem L1 were applied in GRID-2). For a world whose spectrum in the scored band is a power law with γ ∈ [1.7, 2.3], or a single first-order mode, K\* = 1. GB's reconstructed imbalance in the repo is of that kind (GRID-2 main γ = 2.09; G3a γ = 2.02). The current layering, locked in `PREREG_GRID2.md`, is four layers (DC and DM share a speed and count as one; DR; Balancing Mechanism and Quick Reserve; Slow Reserve). Inputs used: those already in `grid2_results.json`, `grid3a_results.json`, and `PREREG_GRID2.md`. No new fit is required for K\*.

A sterling *saving* under B1 requires a measured upkeep h of an extra layer and a measured stake w. Neither is in the repository as a measured GB figure. Therefore any numerical £ saving under B1 is **INCONCLUSIVE**. The diagnostic gap under B1 is the integer K_obs − K\* = 3, reported as a diagnosis, not as a demonstrated inefficiency in money.

**B2. Extended J, ruin and actuation included.**

```
J_ext(𝒟) = Σ_k p_k Q_k  +  w E[ℓ_𝒟]  +  h_prod K_used
subject to  P(f ∉ [f_min, f_max]) ≤ ε_r
            and each product k's official full-delivery time and minimum energy duration.
```

Design 𝒟 is a vector of non-negative procured volumes Q_k over a stated product menu, with K_used the number of products with Q_k > 0 after the GRID-2 speed-grouping rule (DC and DM count as one speed if both are used).

**Measured, if present in the repo or in a cited official service description:**

- volume-weighted clearing prices p_k for DCL, DCH, DML, DMH, DRL, DRH from `grid2_diag.json` (Nov 2025–Oct 2026);
- γ and the reconstructed-imbalance diagnosis already recorded;
- official full-activation times and energy durations for DC, DM, DR from NESO service descriptions already cited in `PREREG_GRID2.md` (documents 187066, 246741, 246766, or the current NESO pages that replace them, with URLs recorded);
- official operational frequency limits, if a primary source is found (expected: statutory ±1% of 50 Hz, and a tighter operational band if sourced).

**Assumed unless a primary official source is found and quoted before the computation:** w, h_prod, ε_r, Value of Lost Load, prices and durations for MFR, BM, Quick Reserve, Slow Reserve, Balancing Reserve, and pre-2020 FFR/EFR, and any cap on available Q_k. A stochastic model that turns (Q, durations) into P(ruin) is also assumed unless taken from a cited official dimensioning rule.

**INCONCLUSIVE rule (applies to K\* under B2, to the sign of J_ext(current) − J_ext(opt), and to the £ gap):** if any of those quantities **changes sign, changes the integer K\*, or moves the £ gap by more than a factor of two** when the assumed terms are varied over the ranges below, that quantity is **INCONCLUSIVE**. A saving computed from assumed costs is a hypothesis for engineers, not a demonstrated inefficiency.

Assumed-term ranges (used only if the term is not sourced): h_prod / (mean p_k Q_k of one populated layer) ∈ {0, 0.01, 0.1}; w chosen so that the unconstrained one-layer error cost is 0.3×, 1×, or 3× the measured DC+DM+DR procurement cost; ε_r ∈ {10^{-3}, 10^{-4}, 10^{-5}} per hour if no official cap is found; VoLL ∈ {£10,000, £20,000, £60,000}/MWh if used (GB planning has used figures in this area — only a cited official value is "measured").

The optimizer under B2 is a discrete enumeration: each product on the menu may be off or on, and when on, Q_k is set either to the measured 2026 mean holding for that product (from `grid2_results.json` / `grid2_diag.json` where it exists) or to zero. No continuous volume optimisation is attempted in this pass (it would require an assumed P(ruin) model at every Q). If that enumeration cannot be scored without the assumed P(ruin) model, B2's K\* and saving are **INCONCLUSIVE** and the reason is stated.

### B.2 Directional prediction (GB reforms, 2020–2024)

**Before suite:** the frequency-response and reserve products in official force on 1 January 2020 (MFR; FFR; EFR if still in force; Fast Reserve; STOR; and any other product with a sourced in-force holding). Layer count K_before uses the same speed-grouping rule, from official service times, not from a new spectrum fit.

**After suite:** the products locked in `PREREG_GRID2.md` for the 2026 sample (DC/DM, DR, BM/Quick Reserve, Slow Reserve), plus any other response/reserve product sourced as in force in that sample (for example Balancing Reserve, MFR, residual static FFR). K_after = 4 as already locked for the count arm, unless a sourced in-force product requires a disclosed addition, which is then reported and K_after restated.

**B3a, under B1:** the reforms moved **toward** the B1 minimum if K_after < K_before, **away** if K_after > K_before, **neither** if K_after = K_before (both still above 1, or both equal to 1). This arm does not use assumed £ terms.

**B3b, under B2:** toward if J_ext(after) < J_ext(before) on the same world (γ from G3a and/or GRID-2, both reported); away if the inequality reverses; **INCONCLUSIVE** if the sign flips inside the assumed-term ranges, or if before-suite prices or durations cannot be sourced.

If B3a and B3b disagree, the single headline direction is **INCONCLUSIVE**, and both arms are reported.

Historical facts used to score B3 (go-live and cessation dates) come only from official URLs recorded in the results file.

---

## Part C — Cross-grid selection strength and distance to the minimum

### C.1 Grids, in this order

1. Great Britain (NESO / former National Grid ESO) — the same system as Parts A–B.
2. Australia NEM (AEMO).
3. ERCOT (Texas).
4. Ireland and Northern Ireland (EirGrid / SONI; one synchronous island).
5. Nordic synchronous area (shared FCR / aFRR markets).
6. Continental Europe (shared FCR / aFRR markets).
7. An island system with public data, first choice Hawaii (Hawaiian Electric), otherwise the first of: New Zealand, Cyprus, or another official-data island named in the results as a substitution, with the reason.

If a pass cannot complete all seven, the results list what was scored, what is **UNTESTED**, and what remains.

Public data only. No account creation, no paywalled login, no emailed FOI. A landing page that requires a form or an account is treated as unavailable; the grid's missing field is **UNTESTED**.

### C.2 Two-pass protocol

**Pass 1 (this pass starts after this file is committed; no layer-design numbers are written down for grids 2–7).** For each grid, compute the selection-strength score S from the rubric below, citing URLs, and commit `theory/measured/grid/SELECTION_SCORES.md` (and a machine-readable `selection_scores.json`) **before** Pass 2. During Pass 1, a product *introduction* may be counted as a redesign (a dated institutional event). Its delivery time, duration, and the resulting layer count are not recorded in Pass 1 files.

**Pass 2** starts only after that commit. It records K_obs, any measured or official world spectrum, d1 / d2, and then runs the rank test. A grid whose Pass 1 score is complete but whose Pass 2 inputs cannot be sourced is **UNTESTED** on the distance and is dropped from the rank test.

GB may use layer counts already locked in this repository; those counts are already public and are not a Pass 1 leak.

### C.3 Selection-strength rubric (locked before Pass 1)

Window, for every grid: **1 January 2011 to 20 November 2026**, the same window as Part A.

S = S_σ + S_N + S_red + S_ruin, each in {0, 1, 2}, so S ∈ {0, …, 8}. Higher means stronger selection as operationalised here, from the four clusters in the definition (cost-to-survival map, population / competitive pressure, redesigns in a defined window, ruin cost). Scores use only documented official or primary regulator / TSO / ISO / statutory sources, with URLs. Where a source is missing, that component is 0, not guessed.

**S_σ — cost-to-survival or cost-to-fitness map**

- 2: a sourced σ as defined in THEORY §3 (elasticity of growth, survival, or profit margin of the operator lineage, or of a declared competing-firm class, to J or to a stated proxy for J), with URL.
- 1: a documented, priced link from balancing / frequency-control cost or from blackout risk to the operator's or the market's financial outcome (an official VoLL or scarcity price used in reserve planning; an official financial incentive on balancing cost or reliability). This is weaker than σ and is not treated as qualification under Part A.
- 0: none found.

**S_N — population / competitive pressure on the *design***

- 2: a sourced N_e ≥ 10 independent *design-setting* authorities (TSO/ISO or equivalent that can choose the product suite) competing in the same synchronous area or the same officially coupled market, with entry and exit or a published comparison.
- 1: more than one design-setting TSO/ISO in the synchronous area, **or** legally required competitive procurement of the services (providers compete; a single buyer still sets the suite).
- 0: a single system operator sets the product suite, and no class-specific N_e was preregistered.

Competition among providers is not competition among designs. Score 1 is the usual single-buyer, competitive-procurement ISO/TSO. Score 2 is reserved for genuine design-lineage competition.

**S_red — redesign count in the window, with the same-world caveat**

R is the number of qualifying redesigns (the Part A definition, applied to that grid) with a sourced official date in the window.

- 2: R ≥ 10 **and** official evidence that the world's statistics (inertia, generation mix, or imbalance spectrum) were stable enough to call it the same world for 10 T_red, or a sourced T_red with at least 10 T_red in a sourced same-world period.
- 1: 3 ≤ R ≤ 9, **or** R ≥ 10 but official evidence that inertia or the generation mix changed materially in the window, **or** T_red cannot be defined from sources.
- 0: R ≤ 2, or redesigns not documented with dates.

**S_ruin — ruin cost**

- 2: a published official VoLL, scarcity-pricing mechanism, ORDC or equivalent, or reliability standard, documented as an *input to* reserve or frequency-response design, with a numerical value and URL.
- 1: a published frequency or loss-of-load standard exists (for example a statutory frequency band, or a 1-in-N resource-adequacy standard) but is not shown in the cited source as a priced input to the product suite.
- 0: none found.

No component is scored from how close the grid's products already look to an optimum.

### C.4 Distance metrics (locked; computed only in Pass 2)

**Counting rule for K_obs** (the GRID-2 rule, applied to official in-force products on a stated date in 2025–2026, or the latest official date in the window): group products by official full-delivery time; two products that share a speed (as DC and DM do in GRID-2) count as one layer; mandatory generator droop that is a standing code obligation is counted as one layer if it is in force and has a distinct official time, else noted and excluded consistently with GRID-2's "MFR is added to the reconstruction, layers are the four listed products" choice, which will be stated per grid. The date and the product list are cited.

**d1 (sensing-limited, ruin slack).** If a measured open-loop or official pre-control imbalance spectrum for that grid, in a band of at least two decades that includes 1 min–1 h, is a power law with γ ∈ [1.7, 2.3] or a single first-order mode, then K\* = 1 and d1 = max(0, K_obs − 1). If no such spectrum is available, d1 is **UNTESTED** for that grid (an official prose statement that "imbalance is like a random walk," without a number, is not enough). GB uses the already-recorded GRID-2 / G3a fits.

**d2 (extended J).** Analogous to B2, using that grid's official prices and durations if they can be sourced without an account. If assumed terms decide the integer K\* or the sign of the gap, d2 is **INCONCLUSIVE** for that grid and is not used in the rank test.

### C.5 Rank test and allowance

Population: every grid in C.1 that has a complete integer S and a complete (not UNTESTED, not INCONCLUSIVE) distance.

**Prediction (preregistered):** grids with higher S sit closer to the cost minimum: Spearman rank correlation ρ(S, d) is negative, for d = d1 as the primary test and d = d2 as a secondary test if at least five grids have a complete d2.

**Test:** Spearman's ρ and two-sided p-value, exact or permutation if n < 10, otherwise the usual large-sample p. Code and seed (if any) committed.

**Allowance / verdict:**

- If n < 5 complete pairs, the test is **UNTESTED**. Ranks may be reported descriptively; no pass or fail.
- If n ≥ 5: **PASS on proxy** if ρ < 0 and p < 0.10; **FAIL on proxy** if ρ > 0 and p < 0.10; **NEITHER** otherwise (including ρ = 0).
- If including or dropping any single grid, or assigning every UNTESTED grid the most extreme d in {0, max observed d} in either direction, would change the verdict, the headline is **INCONCLUSIVE** and the leave-one-out table is reported.
- A missing official source makes that grid UNTESTED on the missing field; it does not licence a guessed number.

This test does not re-qualify GB under Part A. A low S for GB is consistent with a NOT QUALIFIED verdict, and is not a second, quieter reclassification.

---

## Implementation notes

- Compute at nice 19. Do not touch `/workspace/looper`.
- "Law" appears in maintained or new headline text only in the hypothesis sentence, or in the mandated Part A label of §A.4.
- Tests: a pytest module will check that committed JSON agrees with the locked rules (qualification enum, wording map, score ranges, rank-test verdict implied by the recorded ρ, n, p).
- Push incrementally: this prereg first; then Part A plus the deviation note; then Part C Pass 1 scores; then Parts B and C Pass 2 and the claim-map / synthesis edits.

## Predicted claims (for CLAIM_MAP after the runs, v2.65)

- P23 (new): GRID-DX Part A, qualification of GB's balancing system at the GRID-2 lock. Status follows the A.3 verdict (and A.4 wording).
- P24 (new): GRID-DX Part B, prescriptive GB layering, saving, and 2020–2024 direction. Status follows B.1–B.2 (INCONCLUSIVE if assumed terms decide the headline).
- P25 (new): GRID-DX Part C, selection strength versus distance, rank test. Status follows C.5.
- P19 / P21: retyped only under the A.4 map, and only if Part A is NOT QUALIFIED.

---

## Dated note (20 Nov 2026, about 1:42 PM ET; after independent review of PR #113, NOT READY)

This note does not change the locked verdict rules, rubric, distance metrics, or rank-test allowance. It records wording and disclosure corrections required by that review and by Chad's decisions.

- **Labels.** §A.4's mandated headline (`NOT APPLICABLE … not a test of the law`) is superseded for labels, JSON, tests, SYNTHESIS, README, and the CLAIM_MAP status column. The headline status is the compound form required after the confirm round: **NOT A TEST (qualification not established; proxy: passed|failed|INVALID)**, or for GB **NOT A TEST (not qualified; proxy: failed)**. The word "law" is not used in those labels. "Patient" is used in prose only, glossed as "examined to prescribe; no inefficiency shown," and is not a CLAIM_MAP status.
- **Symmetric mapping.** The qualification rule is applied to every field claim that lacked a recorded pre-test qualification check, passes included, not only to misses. Each original PROXY-PASS / PROXY-FAIL (and numbers) stays in the cell as history; nothing is deleted.
- **§A.3 incentive gloss.** The sentence that a regulatory incentive scheme "is not σ unless a source gives the defined elasticity" is a gloss written after the GRID-2 miss; it is not in the definition at `b311a40` / `36416d2`. Item (a) is scored **not established** (Ofgem BSIS made σ computable; it was not computed), not as a substantive fail on that gloss.
- **Definition cites.** The operational definition first entered a main-reachable commit at `b311a40` (20 Nov 2026, 2:06:58 AM ET). `36416d2` is PR #110's head (not on main), squash-merged to main as `e1be66e`.
- **The definition qualifies a class**, not a single system (THEORY §3 at lock). The class used in Part A is synchronous-area balancing designs. No class-specific N_e, n_min, or coverage was preregistered.
- **No blinding for Part A.** Official sources for the qualification audit were gathered before this lock. QUALIFICATION.md was first committed 2 minutes 26 seconds later (original `7ce323a`; rebased as `50350e0`). The two-pass protocol still blinds Part C Pass 1 to non-GB layer designs.
- **S_N rubric ambiguity.** Score 0 ("a single system operator sets the product suite, and no class-specific N_e was preregistered") and score 1's second branch ("legally required competitive procurement … a single buyer still sets the suite") can both be read as covering the usual single-buyer ISO/TSO. Pass 1 applied the score-1 procurement branch, which is also the "usual single-buyer" sentence at the end of §C.3. Those locked Pass 1 numbers are not changed after Pass 2. The ambiguity is disclosed, not resolved by rescoring.
- **Missing sources.** §C.3 says a missing official source scores 0. Where a cited URL returned HTTP 403 or was not found, that component is recorded as **MISSING** and the grid's S is a **lower bound**, not a demonstrated zero.
- **Part B ruin-slack caveat** is a results interpretation, not a change to B1: the integer gap K* = 1 vs K_obs = 4 is reported under B1. B1 assumes ruin slack; GB's ruin constraint binds (FRCR DC sized for an 1,800 MW largest loss). The gap may reflect costs or constraints the design space does not represent (e.g. ruin-binding reserve sizing, short-duration fast units, actuation limits); it is not shown to be excess, and no mechanism is established. See `theory/ROBUSTNESS.md` (separate draft PR in progress).
- **B3 headline** is reported as **UNTESTED/INCONCLUSIVE** when B3a is untested and B3b is inconclusive.
- **Rebase.** This prereg was originally `5d0c11a` (1:22:47 PM ET, 20 Nov 2026) and is `d70c540` after rebase onto main `45a70cf`.
