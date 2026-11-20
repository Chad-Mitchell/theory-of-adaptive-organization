# GRID-DX Part A: qualification audit of GB's balancing system at the GRID-2 lock

Written Friday 20 November 2026, after the lock `PREREG_GRIDDX.md` (original commit `5d0c11a`, 1:22:47 PM ET; rebased onto main `45a70cf` as `d70c540`). This is the Part A verdict under that prereg, using only the operational definition of "strongly selected" as written at the GRID-2 lock. The definition first entered a main-reachable commit at `b311a40a6590fbe2dc15d9dc4eaf1e8416c7aa34` (20 November 2026, 2:06:58 AM ET). The same wording is on PR #110 head `36416d2835f4afe5b6efca8e4b5eeda24620fca8` (9:56:21 AM ET); that head is not on main, and was squash-merged to main as `e1be66e`. G3b is not used.

**Blinding (disclosed).** The prereg gave no blinding for Part A. Official sources for this audit were gathered before the prereg lock, and this file was first committed 2 minutes 26 seconds after that lock (original `7ce323a`, 1:25:13 PM ET; rebased as `50350e0`). The verdict was effectively known when the "lock" was written. That is a process fact, not a change to the definition.

**Verdict: NOT QUALIFIED.** Qualification was not established before scoring (required by THEORY §3 at the GRID-2 lock; the definition first entered main at `b311a40`). On the lock-time definition, the decisive item is the population proxy: one design-setting operator with no entry or exit (N_e = 1), so no selection-resolvable band could exclude a rival ((c)–(d)), and T_red was never defined while the world (outturn inertia) changed (229 GVA·s in 2019/20 to 168 GVA·s in 2026) ((e)). A profit link to balancing cost existed under Ofgem's Balancing Services Incentive Scheme (BSIS, sourced below for 2013–18), but σ was never computed ((a) not established).

The definition qualifies a *class*, not a single system. The relevant class here is synchronous-area balancing designs. No class-specific N_e, n_min, or coverage was preregistered at lock, and the one system audited in full (GB) is not qualified.

GRID-2 is therefore **NOT A TEST OF THE HYPOTHESIS (qualification not established)**. The measured mismatch (reconstructed pre-control imbalance a power law with γ = 2.09 in 2026 and γ = 2.02 in 2024, both inside [1.7, 2.3], against four operational layers) is kept as a diagnosis of a system examined to prescribe; no inefficiency is shown. The locked G1 arm score "FAIL on proxy" in `RESULTS_GRID2.md` and the G3a replication in `RESULTS_GRID3_4.md` are not deleted. The qualification check required by THEORY §3 and FRAMEWORK §9 at the lock ("decide before any measurement; all five, with the evidence recorded") should have been done before scoring and was not.

## 1. What the lock-time definition required

Quoted in `PREREG_GRIDDX.md` §A.1 from THEORY.md §3 and FRAMEWORK.md §9 at `36416d2` (wording also at main-reachable `b311a40`). All five items had to be preregistered with evidence before measurement. "No map, no qualification." "A class that does not qualify is not evidence either way." Cities, nation-states, global economies and the biosphere are excluded until a class-specific population proxy is preregistered.

## 2. What was recorded at the GRID-2 lock

`theory/measured/grid/PREREG_GRID2.md` at `36416d2` does not record a cost-to-fitness map σ, a population proxy N_e, a selection-resolvable band ε, a power check against a named rival, a redesign time T_red, or any qualification decision. A search of the measured, measurement, and THEORY files at that commit finds the definition itself, and no class-specific N_e for grids, electricity system operators, or national infrastructure.

So the protocol item "decide before any measurement; all five, with the evidence recorded" was not met. That alone means qualification was **not established** before scoring. The rest of this file checks, after the fact, which items fail on substance and which remain only not established.

## 3. Item-by-item, from official sources

### (a) Cost-to-fitness map — not established

No sourced σ — the fractional change in growth, survival or reproduction rate of a lineage per fractional change in J, or, for firms, the elasticity of survival or profit margin to J, with a source — was recorded at lock, and none has been computed since.

A profit link to balancing cost did exist, and σ was therefore computable, but it was not computed. Ofgem's Balancing Services Incentive Scheme (BSIS) placed National Grid Electricity Transmission plc (NGET), then the electricity system operator, under a documented sharing factor: "the share of any under or overspend against the target borne by the SO." Official final proposals record the following scheme parameters:

- Scheme in force immediately before April 2015 (the 2013–15 parameters, which Ofgem first proposed to retain): 25% sharing factor and a cap/floor of £25m per annum.
- 2015–17: sharing factor increased to 30% and cap/floor to ±£30m for each year of the scheme.
  - Source: Ofgem, *Electricity System Operator incentives 2015-17: Final Proposals*, 19 March 2015, https://www.ofgem.gov.uk/sites/default/files/docs/2015/03/electricity_so_incentives_-_final_proposals_2.pdf
- 1 April 2017 to 31 March 2018: cap and floor of ±£10m and sharing factor of 10%.
  - Source: Ofgem, *Final proposals for electricity System Operator incentives from April 2017*, 1 March 2017, https://www.ofgem.gov.uk/sites/default/files/docs/2017/03/final_proposals_for_electricity_system_operator_incentives_from_april_2017.pdf

Those documents name NGET, a for-profit plc subsidiary, as the SO. A later RIIO-2 evaluative scheme, Ofgem's ESO Reporting and Incentives (ESORI) arrangements, also existed (guidance: https://www.ofgem.gov.uk/sites/default/files/2023-03/ESORI%20Guidance%20Document%202023-2025.pdf). From 1 October 2024, NESO is a not-for-profit public corporation (https://www.neso.energy/news/national-energy-system-operator-launches-today ; https://www.gov.uk/government/publications/designation-of-the-national-energy-system-operator-neso ; https://www.neso.energy/about/operational-information/regulatory-finance). The earlier BSIS link is the one that made σ computable for the operator lineage in the window.

The prereg's §A.3 sentence that a regulatory incentive scheme "is not σ unless a source gives the defined elasticity" is a gloss written after the GRID-2 miss; it is not in the lock-time definition at `b311a40` / `36416d2`. It is not used here to treat (a) as a substantive fail. Because the map was computable under BSIS and was never computed, (a) is **not established**.

### (b) Population proxy — failed (not qualified)

N_e is "the number of independent lineages competing in the same world per redesign time." Firms: "independent firms in one market over one redesign time, with entry and exit." "Cities, nation-states, global economies and the biosphere are excluded until a class-specific proxy is preregistered, because for them N_e is not defined."

GB has one electricity system operator for one synchronous island (joined to neighbours only by HVDC, as GRID-2 itself stated). No second design-setting operator competes to set GB's frequency-response and reserve suite, and there is no entry or exit of design lineages. No class-specific N_e for grids or national system operators was preregistered at lock (section 2).

Competition among *providers* in NESO auctions is not N_e of *design lineages*. The product suite is set by the single buyer (and its regulator), not by competing system designs with entry and exit.

N_e = 1. This is a substantive fail, not a mere recording gap.

### (c) Selection-resolvable band — failed (not qualified)

ε = 10/(σ·N_e). With N_e = 1, ε = 10/σ, which is at least 100% of J for any σ ≤ 10. No selection-resolvable band can exclude a rival at that width, whatever σ would have been had it been computed. No band was preregistered before measurement. This fails on substance, via (b).

### (d) Power — failed (not qualified)

The band, with measurement error added, must exclude a named rival's design. With N_e = 1 the band cannot exclude a rival, so (d) fails on substance with (c). It was not checked at lock.

### (e) Redesign time and 10 T_red in the same world — failed (not qualified)

T_red is a gap-closing time: "the time the class's design takes to close 1 − 1/e of the gap to its new argmin J after a step change in the prices or in the world's statistics," measured or preregistered from the class's turnover. It was not measured and was not preregistered at the GRID-2 lock. Under the definition that already fails (e).

The same-world clause also fails on a measured world statistic. In this repository's already-recorded NESO outturn inertia, the GRID-4 2019/20 sample mean is 229 GVA·s and the GRID-2 2026 sample mean is 168 GVA·s (`RESULTS_GRID3_4.md`, `grid2_results.json`). The lineage did not face the same world for the whole window.

A falling *minimum-inertia requirement* (FRCR 2025: 140 GVA·s, reduced to 120 GVA·s under FRCR 2023, with a 2025 proposal of 102 GVA·s; https://www.neso.energy/document/356356/download) is a **design choice**, not a change in the world. It is not used here as evidence that the world changed. The EFR invitation to tender's statement that the changing generation mix was reducing system inertia (https://www.neso.energy/document/88946/download) is consistent with the outturn-inertia evidence above; the requirement reductions are not.

The product go-live count below is recorded for information only. T_red was never defined, so a count of product introductions is not a test of "10 T_red." It is not used to decide (e), and is not treated as ten redesigns.

**Qualifying go-lives in the window (official dates; informational):**

| # | Event | Official date | Source |
|---|---|---|---|
| 1 | Enhanced Frequency Response (EFR): eight accepted tenders, earliest official estimated start Apr-17 | Tender 2016; estimated starts Apr-17 to Mar-18 | https://www.neso.energy/document/61786/download |
| 2 | Dynamic Containment soft launch; first delivery 23:00 on 1 October 2020 | 1 October 2020 | https://www.neso.energy/news/national-grid-eso-debuts-dynamic-containment-frequency-response-service ; https://www.neso.energy/document/181431/download |
| 3 | Dynamic Regulation first auction | 8 April 2022 | https://www.neso.energy/document/289686/download (Power Responsive Annual Report 2022); https://www.neso.energy/document/266976/download |
| 4 | Dynamic Moderation first auction | 6 May 2022 | same two sources |
| 5 | Balancing Reserve first day-ahead auction (delivery 13 March) | 12 March 2024 | https://www.neso.energy/news/new-balancing-reserve-service-goes-live-reduce-balancing-costs-and-improve-system-security ; https://www.neso.energy/document/302791/download |
| 6 | Quick Reserve Phase 1: first co-optimised auction (platform open 19 November 2024) | 3 December 2024 | https://www.neso.energy/news/neso-launch-new-quick-reserve-service |
| 7 | Slow Reserve go-live | 31 March 2026 | https://www.neso.energy/document/378736/download (Designation Notice for SR Go-Live Date, 16 March 2026) |

**Official cessations in the window (informational):**

| # | Event | Official date | Source |
|---|---|---|---|
| 8 | Final EFR contracts lapsed | 2022 | https://www.neso.energy/document/289686/download ; https://www.neso.energy/document/188666/download ("four-year EFR contracts which will end in 2022") |
| 9 | Dynamic FFR: final tender round 166 (October) for final delivery month November 2023; no further DFFR procurement | November 2023 | https://www.neso.energy/document/321111/download (Frequency Response Market Information Report, November 2023); https://www.neso.energy/document/320951/download (Power Responsive Annual Report 2023, §4.4) |

**Not counted**, under the locked rule: the 2019 Frequency Response Auction Trial (a procurement-method trial of FFR-like products, https://www.neso.energy/document/176721/download); Static FFR's move to day-ahead auctions in April 2023 (a procurement-route change of an existing product, Annual Report 2023 §4.4); the ESO→NESO designation on 1 October 2024 (organisational, not a product change); consultations and roadmaps without go-live; volume-target changes. Firm Frequency Response was already being tendered before the window (National Grid documents from 2013 and 2015 discuss ongoing FFR tenders: https://www.neso.energy/document/61656/download , https://www.neso.energy/document/59791/download). No official introduction date inside the window was found, and none is counted.

R_go-live = 7; with the two cessations, R ≤ 9. Those figures are a product-event count, not 10 T_red.

**Sample note (pre-existing GRID-2 issue, not used in this verdict).** Slow Reserve went live on 31 March 2026, partway through the GRID-2 sample (November 2025–October 2026). The locked four-layer count includes a product that was not in force for the whole sample.

## 4. Verdict

**NOT QUALIFIED.** Qualification was not established before scoring (required by THEORY §3 at the GRID-2 lock; definition first on main at `b311a40`). On the lock-time definition: (a) is not established (BSIS made σ computable; it was never computed); (b) fails on substance (N_e = 1); (c) and (d) fail on substance because that N_e cannot yield a band that excludes a rival; (e) fails on substance (T_red was never defined, and measured outturn inertia changed from 229 to 168 GVA·s). The falling inertia requirement is a design choice, not world change, and the go-live count is not a test of 10 T_red.

This is not a rescue of the measured mismatch, and it is not a retroactive application of G3b. It is the application of the qualification rule that was already in force at lock and was not applied then. A class that does not qualify "is not evidence either way." GRID-2 and G3a are **not a test of the hypothesis**. They remain a diagnosis of a system examined to prescribe; no inefficiency is shown. The locked arm scores are not deleted.

The lesson, recorded also in `DEVIATIONS.md`: qualification should have been checked before scoring, and was not.
