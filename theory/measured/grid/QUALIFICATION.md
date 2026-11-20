# GRID-DX Part A: qualification audit of GB's balancing system at the GRID-2 lock

Written Friday 20 November 2026, after the lock `PREREG_GRIDDX.md` (commit `5d0c11a`, 1:22:47 PM ET). This is the Part A verdict under that prereg, using only the operational definition of "strongly selected" as written at the GRID-2 lock commit `36416d2835f4afe5b6efca8e4b5eeda24620fca8` (9:56:21 AM ET). G3b is not used.

**Verdict: NOT QUALIFIED.**

GRID-2 is therefore **NOT APPLICABLE (system not qualified): a diagnosis of a patient, not a test of the law**. The measured mismatch (reconstructed pre-control imbalance a power law with γ = 2.09 in 2026 and γ = 2.02 in 2024, both inside [1.7, 2.3], against four operational layers) is kept as a diagnosis. The locked G1 arm score "FAIL on proxy" in `RESULTS_GRID2.md` and the G3a replication in `RESULTS_GRID3_4.md` are not deleted. The qualification check required by THEORY §3 and FRAMEWORK §9 at the lock ("decide before any measurement; all five, with the evidence recorded") should have been done before scoring and was not.

## 1. What the lock-time definition required

Quoted in `PREREG_GRIDDX.md` §A.1 from THEORY.md §3 and FRAMEWORK.md §9 at `36416d2`. All five items had to be preregistered with evidence before measurement. "No map, no qualification." "A class that does not qualify is not evidence either way." Cities, nation-states, global economies and the biosphere are excluded until a class-specific population proxy is preregistered.

## 2. What was recorded at the GRID-2 lock

`theory/measured/grid/PREREG_GRID2.md` at `36416d2` does not record a cost-to-fitness map σ, a population proxy N_e, a selection-resolvable band ε, a power check against a named rival, a redesign time T_red, or any qualification decision. A search of the measured, measurement, and THEORY files at that commit finds the definition itself, and no class-specific N_e for grids, electricity system operators, or national infrastructure.

So the protocol item "decide before any measurement; all five, with the evidence recorded" was not met. That alone is enough, under A.3, for **NOT QUALIFIED**. The rest of this file checks whether the system would have qualified if the check had been done.

## 3. Item-by-item, from official sources

### (a) Cost-to-fitness map — failed

No sourced σ — the fractional change in growth, survival or reproduction rate of a lineage per fractional change in J, or, for firms, the elasticity of survival or profit margin to J, with a source — was recorded at lock, and none was found now.

The GB system operator is a single designated body, not a firm in a market of competing operators:

- From 1 October 2024, National Energy System Operator (NESO) was established as the Independent System Operator and Planner under the Energy Act 2023. DESNZ acquired 100% of National Grid Electricity System Operator Ltd. NESO "operates a not-for-profit model, is licensed and regulated by [Ofgem] and is funded through electricity and gas industry charges." "HMG does not receive an enduring financial return nor is it exposed to downside losses (including from incentives, disallowance, enforcement penalties, or damages imposed by third parties)."
  - https://www.neso.energy/news/national-energy-system-operator-launches-today
  - https://www.gov.uk/government/publications/designation-of-the-national-energy-system-operator-neso
  - https://www.neso.energy/about/operational-information/regulatory-finance

A not-for-profit public corporation funded by allowed charges does not have a profit-margin elasticity to J in the sense of THEORY §3. No official source was found that publishes σ, or any elasticity of NESO's or the former ESO's survival to the cost of judgment.

Ofgem's ESO Reporting and Incentives arrangements assessed the legally separated ESO's performance, including balancing costs, during RIIO-2 (guidance: https://www.ofgem.gov.uk/sites/default/files/2023-03/ESORI%20Guidance%20Document%202023-2025.pdf). That is a regulatory performance scheme. Under the locked definition it is not σ, and it is not used here as a substitute.

"No map, no qualification."

### (b) Population proxy — failed

N_e is "the number of independent lineages competing in the same world per redesign time." Firms: "independent firms in one market over one redesign time, with entry and exit." "Cities, nation-states, global economies and the biosphere are excluded until a class-specific proxy is preregistered, because for them N_e is not defined."

GB has one electricity system operator for one synchronous island (joined to neighbours only by HVDC, as GRID-2 itself stated). No second design-setting operator competes to set GB's frequency-response and reserve suite. No class-specific N_e for grids or national system operators was preregistered at `36416d2` (section 2).

Competition among *providers* in NESO auctions is not N_e of *design lineages*. The product suite is set by the single buyer (and its regulator), not by competing system designs with entry and exit.

A single national system operator is in the same position as the excluded nation-state class until a proxy is preregistered. None was.

### (c) Selection-resolvable band — failed

ε = 10/(σ·N_e) cannot be computed without σ and N_e. No band was preregistered before measurement.

### (d) Power — failed

Without a band, the requirement that the band plus measurement error exclude a named rival's design cannot be checked. It was not checked at lock.

### (e) Redesign time and 10 T_red in the same world — failed

T_red was not measured and was not preregistered from the class's turnover at the GRID-2 lock. Under A.3 that already fails (e).

The count below is recorded for information, under the locked window (1 January 2011 to 20 November 2026) and the locked redesign rule. It is not a substitute T_red.

**Qualifying go-lives in the window (official dates):**

| # | Event | Official date | Source |
|---|---|---|---|
| 1 | Enhanced Frequency Response (EFR): eight accepted tenders, earliest official estimated start Apr-17 | Tender 2016; estimated starts Apr-17 to Mar-18 | https://www.neso.energy/document/61786/download |
| 2 | Dynamic Containment soft launch; first delivery 23:00 on 1 October 2020 | 1 October 2020 | https://www.neso.energy/news/national-grid-eso-debuts-dynamic-containment-frequency-response-service ; https://www.neso.energy/document/181431/download |
| 3 | Dynamic Regulation first auction | 8 April 2022 | https://www.neso.energy/document/289686/download (Power Responsive Annual Report 2022); https://www.neso.energy/document/266976/download |
| 4 | Dynamic Moderation first auction | 6 May 2022 | same two sources |
| 5 | Balancing Reserve first day-ahead auction (delivery 13 March) | 12 March 2024 | https://www.neso.energy/news/new-balancing-reserve-service-goes-live-reduce-balancing-costs-and-improve-system-security ; https://www.neso.energy/document/302791/download |
| 6 | Quick Reserve Phase 1: first co-optimised auction (platform open 19 November 2024) | 3 December 2024 | https://www.neso.energy/news/neso-launch-new-quick-reserve-service |
| 7 | Slow Reserve go-live | 31 March 2026 | https://www.neso.energy/document/378736/download (Designation Notice for SR Go-Live Date, 16 March 2026) |

**Official cessations in the window (not used to push R over 10; listed for completeness):**

| # | Event | Official date | Source |
|---|---|---|---|
| 8 | Final EFR contracts lapsed | 2022 | https://www.neso.energy/document/289686/download ; https://www.neso.energy/document/188666/download ("four-year EFR contracts which will end in 2022") |
| 9 | Dynamic FFR: final tender round 166 (October) for final delivery month November 2023; no further DFFR procurement | November 2023 | https://www.neso.energy/document/321111/download (Frequency Response Market Information Report, November 2023); https://www.neso.energy/document/320951/download (Power Responsive Annual Report 2023, §4.4) |

**Not counted**, under the locked rule: the 2019 Frequency Response Auction Trial (a procurement-method trial of FFR-like products, https://www.neso.energy/document/176721/download); Static FFR's move to day-ahead auctions in April 2023 (a procurement-route change of an existing product, Annual Report 2023 §4.4); the ESO→NESO designation on 1 October 2024 (organisational, not a product change); consultations and roadmaps without go-live; volume-target changes. Firm Frequency Response was already being tendered before the window (National Grid documents from 2013 and 2015 discuss ongoing FFR tenders: https://www.neso.energy/document/61656/download , https://www.neso.energy/document/59791/download). No official introduction date inside the window was found, and none is counted.

R_go-live = 7; with the two cessations, R ≤ 9. Both are below 10. Even if a looser count were used, the same-world clause fails:

- The EFR invitation to tender already treated falling inertia from a changing generation mix as the reason for a new product: "The changing generation mix in Great Britain is reducing the contribution that synchronous generation makes … reducing the level of system inertia" (https://www.neso.energy/document/88946/download).
- NESO's Frequency Risk and Control Report 2025 (March 2025, https://www.neso.energy/document/356356/download) records a falling official *minimum inertia requirement*: 140 GVA·s, reduced to 120 GVA·s under FRCR 2023 (Ofgem approval 9 June 2023; implemented in two phases on 28 February 2024 and 19 June 2024), with a 2025 proposal to reduce it further to 102 GVA·s. The same report notes the 2024 phase-out of coal on the GB system.
- In this repository's already-recorded NESO outturn inertia, the GRID-4 2019/20 sample mean is 229 GVA·s and the GRID-2 2026 sample mean is 168 GVA·s (`RESULTS_GRID3_4.md`, `grid2_results.json`).

The lineage did not face "the same world" for the whole window. T_red was never defined. Item (e) fails.

## 4. Verdict

All five items fail, and the lock-time preregistered-evidence requirement fails. **NOT QUALIFIED.**

This is not a rescue of the measured mismatch, and it is not a retroactive application of G3b. It is the application of the qualification rule that was already in force at `36416d2` and was not applied then. A class that does not qualify "is not evidence either way." GRID-2 and G3a remain diagnoses of an unqualified system: useful as a prescriptive reading of how far the present design sits from the sensing-limited one-layer optimum, and not a test of the hypothesis.

The lesson, recorded also in `DEVIATIONS.md`: qualification should have been checked before scoring, and was not.
