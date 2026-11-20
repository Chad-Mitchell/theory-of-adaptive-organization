# GRID-DX results

Prereg lock: `PREREG_GRIDDX.md` commit `5d0c11a3c4ca5146d3a2e806a46524eb3dcba25f` (Friday 20 November 2026, 1:22:47 PM ET). Qualification audit: `QUALIFICATION.md` (`7ce323a`, 1:25:13 PM ET). Part C Pass 1 scores: `SELECTION_SCORES.md` (`eae72a9`, 1:28:32 PM ET), committed before any non-GB layer design was recorded.

## Part A — Qualification

**Verdict: NOT QUALIFIED** (full evidence and URLs in `QUALIFICATION.md`).

Headline label, as locked in §A.4: **NOT APPLICABLE (system not qualified): a diagnosis of a patient, not a test of the law**.

The locked G1 arm score in `RESULTS_GRID2.md` (γ = 2.09; four operational layers against a one-layer sensing-limited prediction) and the G3a replication (γ = 2.02) are not deleted. They are the diagnosis. The qualification check required at the GRID-2 lock should have been done before scoring and was not.

## Part B — Prescriptive diagnosis (GB)

### B1. Sensing-limited J, ruin slack

No new spectrum fit was run. From the already-recorded GRID-2 and G3a results, γ = 2.09 (2026) and γ = 2.02 (2024), both inside [1.7, 2.3], so K\* = 1 by Theorem L1 / Master Theorem (iii). The current layering, locked in `PREREG_GRID2.md`, is K_obs = 4. The diagnostic gap is K_obs − K\* = 3.

A sterling saving under B1 requires a measured layer upkeep h and a measured stake w. Neither is in the repository as a measured GB figure. Under the locked rule the £ saving is **INCONCLUSIVE**. The integer gap is a diagnosis, not a demonstrated inefficiency in money.

### B2. Extended J, ruin and actuation included

Measured prices and mean holdings already in the repository (`grid2_diag.json`, `grid2_results.json`): volume-weighted £/MW/h DCL 3.20, DCH 2.04, DML 7.00, DMH 0.06, DRL 16.31, DRH −8.03; mean holdings DCL 1,270 MW, DRL 480 MW, MFR primary 72 MW (Nov 2025–Oct 2026 sample). Official operational frequency limits and a full P(ruin) model that maps (Q, durations) into the ruin constraint were not sourced as a closed official dimensioning rule in this pass. w, h_prod and ε_r remain assumed.

The locked discrete enumeration cannot be scored for K\* or for the sign of J_ext(current) − J_ext(opt) without that assumed ruin model. Under the locked INCONCLUSIVE rule, **B2's K\* and the predicted £ saving are INCONCLUSIVE**. A saving computed from assumed costs would be a hypothesis for engineers, not a demonstrated inefficiency, and is not reported as a number here.

A procurement-only sum of p_k Q_k, which is not J_ext, is therefore not used as an optimum.

### B3. Direction of the 2020–2024 reforms

**B3a (under B1).** K_after = 4 as locked for the 2026 count arm. A speed-grouped K_before for the official 1 January 2020 suite (MFR, FFR, EFR if still in force, Fast Reserve, STOR) was not computed, because official full-delivery times for each of those products, needed by the locked counting rule, were not all retrieved and quoted in this pass. B3a is therefore **UNTESTED** as an integer comparison. What is sourced, and is not a K count, is that the reforms introduced DC (1 October 2020), DR (8 April 2022) and DM (6 May 2022), later Balancing Reserve, Quick Reserve and Slow Reserve, and retired EFR (2022) and dynamic FFR (final delivery November 2023). That is a replacement of one multi-product suite by another, not a documented move to a single layer. It is not scored as toward or away under the locked integer rule.

**B3b (under B2).** Before-suite prices and durations were not fully sourced, and B2 itself is INCONCLUSIVE on assumed terms. **INCONCLUSIVE**.

**Headline direction:** **INCONCLUSIVE** (B3a untested; B3b inconclusive).

## Part C — Selection strength and distance (Pass 2)

Pass 1 scores, already committed, are GB S = 5, ERCOT S = 4, Australia NEM = Ireland/NI = Nordic = Continental Europe = 1, Hawaii UNTESTED.

**d1.** GB uses the already-recorded GRID-2 / G3a fits: K\* = 1, K_obs = 4, d1 = 3. For Australia NEM, ERCOT, Ireland/NI, Nordic, Continental Europe and Hawaii, no measured open-loop or official pre-control imbalance spectrum in a band of at least two decades that includes 1 min–1 h was retrieved in this pass (public form-gated or account-gated portals are treated as unavailable). d1 is **UNTESTED** for those six. Official in-force product lists and delivery times were not used to form a K_obs where d1 cannot be scored, so no unofficial distance is reported.

**d2.** Not scored (same assumed-term barrier as B2). **UNTESTED** / not used in the rank test.

**Rank test.** Complete pairs with both S and a complete d1: n = 1 (GB only). Under the locked allowance, n < 5 ⇒ the test is **UNTESTED**. No pass or fail is recorded. A later pass can add spectra or substitute an island grid; it cannot patch this verdict after seeing a correlation.

## What remains

- Official delivery times for the 1 January 2020 GB suite, so B3a can be scored.
- A sourced official GB (and, if possible, other-grid) ruin-dimensioning rule, so B2 / d2 are not assumed-term inconclusive.
- Public imbalance spectra for the other grids, or a declared UNTESTED if none exist without an account.
- Hawaii (or New Zealand / Cyprus) Pass 1 score, still UNTESTED.
- AEMC reliability-settings and EirGrid System Services PDFs that returned HTTP 403 in this pass, if they can be retrieved another public way.
