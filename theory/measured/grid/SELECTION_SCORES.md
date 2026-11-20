# GRID-DX Part C, Pass 1: selection-strength scores

Written Friday 20 November 2026, after `PREREG_GRIDDX.md` (`5d0c11a`, 1:22:47 PM ET) and after the Part A audit (`7ce323a`). This is Pass 1 only: scores are computed from the locked rubric in §C.3, from official institutional sources, **before** any non-GB layer count, delivery time, or distance to a cost minimum is recorded.

Window for every grid: 1 January 2011 to 20 November 2026. S = S_σ + S_N + S_red + S_ruin, each in {0, 1, 2}. A missing official source scores 0 for that component, not a guess. Product *introductions* are counted as dated events; their official delivery times and the resulting layer counts are not written down here.

Procurement-platform go-lives and common markets for an *already existing* product (FCR Cooperation, PICASSO, the Nordic aFRR capacity market, the 2019 GB auction trial, Static FFR's move to day-ahead) are recorded as notes and **are not counted in R**, consistent with Part A's treatment of procurement-route changes.

Hawaii is **UNTESTED** in this pass: official pages were not retrieved in enough detail to score the four components without guesswork. No substitution island was scored.

## Summary

| Grid | S_σ | S_N | S_red | S_ruin | S | R (counted) | Notes |
|---|---|---|---|---|---|---|---|
| Great Britain (NESO / former NGESO) | 1 | 1 | 1 | 2 | **5** | 7 go-lives (≤ 9 with cessations) | From Part A sources plus Ofgem ESORI |
| Australia NEM (AEMO) | 0 | 1 | 0 | 0 | **1** (lower bound) | 2 | S_σ and S_ruin **MISSING** (AEMC reliability-settings PDF HTTP 403); S = 1 is a lower bound, not a demonstrated zero |
| ERCOT (Texas) | 1 | 1 | 0 | 2 | **4** | 1 | ORDC/VOLL official; ECRS is the one counted product go-live |
| Ireland and Northern Ireland (EirGrid / SONI) | 0 | 1 | 0 | 0 | **1** (lower bound) | 0 sourced go-lives | S_red **MISSING** as a complete count (EirGrid System Services PDFs HTTP 403); S = 1 is a lower bound |
| Nordic synchronous area | 0 | 1 | 0 | 0 | **1** | 0 | Shared aFRR capacity market is a procurement change |
| Continental Europe (FCR / aFRR platforms) | 0 | 1 | 0 | 0 | **1** | 0 | FCR Cooperation and PICASSO are procurement platforms |
| Hawaii (Hawaiian Electric) | — | — | — | — | **UNTESTED** | — | Insufficient official text retrieved this pass |

## Great Britain — S = 5

**S_σ = 1.** No σ as defined (Part A). During the window the legally separated ESO was subject to an official evaluative financial incentive: Ofgem's *Electricity System Operator Reporting and Incentives (ESORI) Arrangements* set "the methodology the Authority will use to determine an incentive reward or penalty" for each business plan cycle (BP1 from 1 April 2021, BP2 from 1 April 2023). Source: https://www.ofgem.gov.uk/sites/default/files/2023-03/ESORI%20Guidance%20Document%202023-2025.pdf . From 1 October 2024 NESO is a not-for-profit public corporation (Part A URLs). This is a priced official incentive on the operator, not σ, and is scored 1 as the rubric allows.

**S_N = 1.** One design-setting operator (NESO / former ESO) for one synchronous island. Providers compete in official day-ahead auctions for DC/DM/DR, Balancing Reserve and Quick Reserve (Part A URLs). Competition among providers is not N_e of designs; the single-buyer case is score 1.

**S_red = 1.** R_go-live = 7 in the window, with two official cessations giving R ≤ 9 (`QUALIFICATION.md`). 3 ≤ R ≤ 9, and the world (inertia, mix) changed, so 1, not 2.

**S_ruin = 2.** NESO's Frequency Risk and Control Report 2025 (March 2025, https://www.neso.energy/document/356356/download) is an official reliability assessment used as an input to the minimum inertia requirement and to "additional Dynamic Containment," with numerical values (reduction of the minimum inertia requirement from 140 GVA·s to 120 GVA·s, implemented 28 February and 19 June 2024; a 2025 proposal of 102 GVA·s; a stated £96m/year saving). That meets "reliability standard, documented as an input to reserve or frequency-response design, with a numerical value."

## Australia NEM — S = 1

**S_σ = 0.** No sourced σ. An official AEMC "Schedule of reliability settings" URL was requested (https://www.aemc.gov.au/sites/default/files/2026-02/Schedule%20of%20reliability%20settings%20-%202026-27%20financial%20year.pdf) and returned HTTP 403, so no VoLL/Market Price Cap figure is recorded or scored.

**S_N = 1.** AEMO is the single operator of the NEM's electricity system and wholesale market, including frequency-control services (https://www.aemo.com.au/about/what-we-do). The Very Fast FCAS markets are procured by AEMO under the existing FCAS arrangements (https://www.aemo.com.au/initiatives/major-programs/nem-reform-program/nem-reform-program-initiatives/fast-frequency-response). Single buyer, competitive procurement: score 1.

**S_red = 0.** Two sourced official go-lives in the window, below the band of 3: (1) mandatory primary frequency response, AEMC Rule 2020 No. 5, commencement 4 June 2020 (https://www.aemc.gov.au/rule-changes/primary-frequency-response-requirement ; media release of the final rule, 26 March 2020, https://www.aemc.gov.au/news-centre/media-releases/final-rule-better-control-power-system-frequency); (2) Very Fast raise and very Fast lower FCAS markets opened 9 October 2023 at 13:00 Market Time, counted as one go-live of a raise/lower pair on one day (same AEMO Fast Frequency Response page). AEMO's page notes a changing, lower-inertia system as context; the same-world clause would not support a 2 in any case.

**S_ruin = 0.** No official reliability-standard or VoLL text was successfully retrieved this pass (the schedule PDF above returned 403). Not guessed.

## ERCOT — S = 4

**S_σ = 1.** No σ for the ISO as a lineage. Official scarcity pricing of operating reserves: ERCOT's 2022 *Biennial Report on the ORDC* (https://www.ercot.com/files/docs/2022/10/31/2022%20Biennial%20ERCOT%20Report%20on%20the%20ORDC%20-%20Final_corr.pdf) describes the Operating Reserve Demand Curve as "a market mechanism that values operating reserves in the wholesale electric market based on the scarcity of those reserves" and states that multiplying the PBMCL curve by VOLL (then $5,000/MWh) yields the ORDC. That is a priced official link from blackout risk and reserve tightness to market outcomes, scored 1.

**S_N = 1.** ERCOT is the single Independent System Operator for the region, "subject to oversight by the Public Utility Commission of Texas and the Texas Legislature." Ancillary services are "purchased by ERCOT in the day-ahead market" and "can be provided by generators or consumers" (https://www.ercot.com/news/release/2023-06-12-ercot-adds-new). Single buyer, competitive procurement: score 1.

**S_red = 0.** One counted product go-live: ERCOT Contingency Reserve Service (ECRS), announced as launched in the 12 June 2023 news release above, "the first daily procured Ancillary Service introduced to the ERCOT market in more than 20 years." The 1 January 2022 ORDC parameter change (VOLL/SWCAP to $5,000/MWh and minimum contingency level 2,000 → 3,000 MW, same ORDC report) is a pricing-curve change, not a new product under the locked rule, and is not in R. R = 1.

**S_ruin = 2.** The same official ORDC report documents VOLL as an input to the reserve-valuation curve, with the numerical value $5,000/MWh from 1 January 2022 (and $2,000/MWh LCAP from 4 March 2021 to the end of 2021 after Winter Storm Uri).

## Ireland and Northern Ireland — S = 1

**S_σ = 0.** None found.

**S_N = 1.** EirGrid (Ireland) and SONI (Northern Ireland) are the two TSOs for one synchronous island; the DS3 programme is described on EirGrid's official page as "our" joint work to raise instantaneous renewable penetration, with an advisory council from 2011 to 2021 (https://www.eirgrid.ie/ds3-programme-delivering-secure-sustainable-electricity-system). Two TSOs in one area, acting jointly rather than as competing design lineages: score 1, not 2.

**S_red = 0.** The DS3 programme is documented on that page (targets met by 2020 and 75% in March 2022; "ten years in the making since the launch"). Official *product* go-live dates for DS3 System Services were not retrieved (EirGrid PDFs returned 403). Under the locked rule, a programme without a sourced product go-live date does not add to R. R = 0 this pass.

**S_ruin = 0.** The same page states operational SNSP targets (50% → 65% → 70% → 75%). Those are programme goals, not a published frequency or loss-of-load standard shown as a priced input to the product suite. Not scored as 1 or 2.

## Nordic synchronous area — S = 1

**S_σ = 0.** None found this pass.

**S_N = 1.** Four design-setting TSOs — Svenska kraftnät, Energinet, Statnett, and Fingrid — in one synchronous area, with a common aFRR capacity procurement (https://www.svk.se/press-och-nyheter/nyheter/nbm/2022/den-nordiska-kapacitetsmarknaden-afrr-startar-som-planerat-den-7-december-2022/). More than one TSO, but N_e ≥ 10 competing design-setters is not met: score 1.

**S_red = 0.** The common Nordic aFRR capacity market started for Svenska kraftnät, Energinet and Statnett on 7 December 2022 (first delivery 8 December 2022; Fingrid to join after national approval; same URL). That is a common procurement of an existing reserve, not a new product under the locked rule. R = 0.

**S_ruin = 0.** No official VoLL or frequency-standard text was retrieved this pass.

## Continental Europe — S = 1

**S_σ = 0.** None found this pass.

**S_N = 1.** The FCR Cooperation "currently involves twelve Transmission System Operators (TSOs) from nine countries" procuring FCR in a common market under a TSO-TSO model (https://www.entsoe.eu/network_codes/eb/fcr/). That is more than one TSO, but they share a harmonised product and a common merit order; they are not N_e ≥ 10 independent authorities competing with different product suites. Score 1, not 2.

**S_red = 0.** Official dated events in the window that are *not* counted in R: FCR Cooperation "started in 2017" (same ENTSO-E page; France joined 2017, Western Denmark and Slovenia 2021, Czech Republic March 2023); PICASSO, the European aFRR energy platform, "brought successfully into operation on 1 June 2022" (https://www.entsoe.eu/news/2022/06/01/go-live-of-picasso-the-pan-european-platform-for-the-international-coordination-of-automatic-frequency-restoration-reserves-and-stable-system-operation/). Both are common procurement platforms for existing FCR / aFRR, treated as procurement-route changes. R = 0.

**S_ruin = 0.** Commission Regulation (EU) 2017/2195 (EBGL) is cited on those pages as the legal framework; a numerical frequency or VoLL standard used as an input to product design was not retrieved as text this pass.

## Hawaii — UNTESTED

No official Hawaiian Electric or Hawaii PUC page was retrieved in this pass with enough text to score S_σ, S_N, S_red or S_ruin without guesswork. The grid is listed as UNTESTED, not given a low score by default. A later pass may score it, or substitute New Zealand or Cyprus, under the locked list in §C.1.

## What this pass does not do

No K_obs, no delivery times, no d1 or d2, and no rank test. Those wait for a later Pass 2 commit, after this file is on the branch.

## Dated note (20 Nov 2026, about 1:42 PM ET; after independent review of PR #113)

Pass 1 numbers in the table are not changed after Pass 2. Two disclosures:

**Missing sources as lower bounds, not zeros.** The locked rubric said a missing official source scores 0. Where a cited URL returned HTTP 403, that component is **MISSING** and the grid's S is a **lower bound**. Australia NEM: the AEMC "Schedule of reliability settings" PDF (https://www.aemc.gov.au/sites/default/files/2026-02/Schedule%20of%20reliability%20settings%20-%202026-27%20financial%20year.pdf) returned 403, so S_σ and S_ruin are MISSING and S = 1 is a lower bound. Ireland/NI: EirGrid System Services product go-live PDFs returned 403, so S_red is a lower bound on a complete count and S = 1 is a lower bound. Those 403s are not treated as demonstrated absence of an incentive or of a reliability standard.

**S_N rubric ambiguity.** Score 0 ("a single system operator sets the product suite, and no class-specific N_e was preregistered") and score 1's second branch ("legally required competitive procurement of the services; a single buyer still sets the suite") can both be read as covering the usual single-buyer ISO/TSO, including GB. Pass 1 applied the score-1 procurement branch, which matches the "usual single-buyer" sentence at the end of §C.3. Scores are not rescored. The ambiguity is disclosed.

S is not qualification. GB has the highest score in the set (S = 5) and is not qualified (Part A: N_e = 1). No grid in this set qualifies under the operational definition as scored. The Part C rank test therefore cannot test the hypothesis as scored. What would is a class with real competing design lineages, with qualification recorded before distances are measured.
