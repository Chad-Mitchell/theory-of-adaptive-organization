# GRID-DX results

Prereg lock: `PREREG_GRIDDX.md`, originally `5d0c11a3c4ca5146d3a2e806a46524eb3dcba25f` (Friday 20 November 2026, 1:22:47 PM ET); after rebase onto main `45a70cf`, `d70c54066e9f85e4e4e25b88ad58d1f9997178ab`. Qualification audit: `QUALIFICATION.md` (originally `7ce323a`, 1:25:13 PM ET; rebased as `50350e0`). Part C Pass 1 scores: `SELECTION_SCORES.md` (originally `eae72a9`, 1:28:32 PM ET; rebased as `9683e27`), committed before any non-GB layer design was recorded. The prereg gave no blinding for Part A (sources were gathered before the lock).

## Part A — Qualification

**Verdict: NOT QUALIFIED** (full evidence and URLs in `QUALIFICATION.md`).

Headline status: **NOT A TEST (not qualified; proxy: failed)**.

Qualification was not established before scoring (required by THEORY §3 at the GRID-2 lock; the definition first entered main at `b311a40`). On the lock-time definition, GB is **not qualified**: one design-setting operator with no entry or exit (N_e = 1), so no selection-resolvable band could exclude a rival ((c)–(d)), and T_red was never defined while measured outturn inertia changed from 229 GVA·s (2019/20) to 168 GVA·s (2026) ((e)). A profit link to balancing cost existed under Ofgem BSIS (2013–18 sourced), but σ was never computed ((a) not established). The falling inertia requirement is a design choice, not world change. The definition qualifies a class (synchronous-area balancing designs), not a single system; no class-level N_e or n_min was preregistered.

The locked G1 arm score in `RESULTS_GRID2.md` (γ = 2.09; four operational layers against a one-layer sensing-limited prediction) and the G3a replication (γ = 2.02) are not deleted. They are a diagnosis of a system examined to prescribe; no inefficiency is shown. The qualification check required at the GRID-2 lock should have been done before scoring and was not.

## Part B — Prescriptive diagnosis (GB)

### B1. Sensing-limited J, ruin slack

No new spectrum fit was run. From the already-recorded GRID-2 and G3a results, γ = 2.09 (2026) and γ = 2.02 (2024), both inside [1.7, 2.3], so K* = 1 by Theorem L1 / Master Theorem (iii) **under the B1 premise that ruin is slack**. The current layering, locked in `PREREG_GRID2.md`, is K_obs = 4. The diagnostic gap is K_obs − K* = 3 **only under that ruin-slack premise**.

NESO's Frequency Risk and Control Report 2025 sizes Dynamic Containment for post-fault risks against an 1,800 MW largest loss (https://www.neso.energy/document/356356/download). B1 assumes ruin slack; GB's ruin constraint binds (FRCR DC sized for an 1,800 MW largest loss). The gap may reflect costs or constraints the design space does not represent (e.g. ruin-binding reserve sizing, short-duration fast units, actuation limits); it is not shown to be excess, and no mechanism is established. That question is not resolved here; it is the subject of a robustness extension (`theory/ROBUSTNESS.md`, a separate draft PR in progress). Here, "diagnosis" means a reading under B1's premises only.

A sterling saving under B1 requires a measured layer upkeep h and a measured stake w. Neither is in the repository as a measured GB figure. Under the locked rule the £ saving is **INCONCLUSIVE**. The integer gap is a diagnosis, not a demonstrated inefficiency.

### B2. Extended J, ruin and actuation included

Measured prices and mean holdings already in the repository (`grid2_diag.json`, `grid2_results.json`): volume-weighted £/MW/h DCL 3.20, DCH 2.04, DML 7.00, DMH 0.06, DRL 16.31, DRH −8.03; mean holdings DCL 1,270 MW, DRL 480 MW, MFR primary 72 MW (Nov 2025–Oct 2026 sample). Official operational frequency limits and a full P(ruin) model that maps (Q, durations) into the ruin constraint were not sourced as a closed official dimensioning rule in this pass. w, h_prod and ε_r remain assumed. The FRCR 1,800 MW largest-loss figure above is a sourced ruin input, but is not by itself the locked stochastic model for J_ext.

The locked discrete enumeration cannot be scored for K* or for the sign of J_ext(current) − J_ext(opt) without that assumed ruin model. Under the locked INCONCLUSIVE rule, **B2's K* and the predicted £ saving are INCONCLUSIVE**. A saving computed from assumed costs would be a hypothesis for engineers, not a demonstrated inefficiency, and is not reported as a number here.

A procurement-only sum of p_k Q_k, which is not J_ext, is therefore not used as an optimum.

### B3. Direction of the 2020–2024 reforms

**B3a (under B1).** K_after = 4 as locked for the 2026 count arm. A speed-grouped K_before for the official 1 January 2020 suite (MFR, FFR, EFR if still in force, Fast Reserve, STOR) was not computed, because official full-delivery times for each of those products, needed by the locked counting rule, were not all retrieved and quoted in this pass. B3a is therefore **UNTESTED** as an integer comparison. What is sourced, and is not a K count, is that the reforms introduced DC (1 October 2020), DR (8 April 2022) and DM (6 May 2022), later Balancing Reserve, Quick Reserve and Slow Reserve, and retired EFR (2022) and dynamic FFR (final delivery November 2023). That is a replacement of one multi-product suite by another, not a documented move to a single layer. It is not scored as toward or away under the locked integer rule. Any such comparison under B1 would also inherit the B1 caveat: B1 assumes ruin slack; GB's ruin constraint binds (FRCR DC sized for an 1,800 MW largest loss). The gap may reflect costs or constraints the design space does not represent (e.g. ruin-binding reserve sizing, short-duration fast units, actuation limits); it is not shown to be excess, and no mechanism is established. See `theory/ROBUSTNESS.md` (separate draft PR in progress).

**B3b (under B2).** Before-suite prices and durations were not fully sourced, and B2 itself is INCONCLUSIVE on assumed terms. **INCONCLUSIVE**.

**Headline direction:** **UNTESTED/INCONCLUSIVE** (B3a untested; B3b inconclusive).

## Part C — Selection strength and distance (Pass 2)

Pass 1 scores, already committed, are GB S = 5, ERCOT S = 4, Australia NEM = Ireland/NI = Nordic = Continental Europe = 1, Hawaii UNTESTED. Where a cited official URL returned HTTP 403 (AEMC reliability-settings PDF; EirGrid System Services PDFs), those components are **MISSING** and the affected S totals are **lower bounds**, not demonstrated zeros (`SELECTION_SCORES.md`).

S is a rubric, not qualification. GB scored highest (S = 5) and is **not qualified** under Part A (N_e = 1). No grid in this set qualifies under the operational definition as scored: none has a recorded pre-test check of (a)–(e), and none is a class with competing design lineages (typical S_N = 1 is a single-buyer or jointly acting TSO). The rank test therefore **cannot test the hypothesis as scored**. What would test it is a class with real competing design lineages, with σ computed, N_e large enough that the band excludes a named rival, T_red defined, and the same world for at least 10 T_red, with qualification recorded before any distance is measured.

**d1.** GB uses the already-recorded GRID-2 / G3a fits: K* = 1, K_obs = 4, d1 = 3, **under B1's ruin-slack premise**. B1 assumes ruin slack; GB's ruin constraint binds (FRCR DC sized for an 1,800 MW largest loss). The gap may reflect costs or constraints the design space does not represent (e.g. ruin-binding reserve sizing, short-duration fast units, actuation limits); it is not shown to be excess, and no mechanism is established. See `theory/ROBUSTNESS.md` (separate draft PR in progress). For Australia NEM, ERCOT, Ireland/NI, Nordic, Continental Europe and Hawaii, no measured open-loop or official pre-control imbalance spectrum in a band of at least two decades that includes 1 min–1 h was retrieved in this pass (public form-gated or account-gated portals are treated as unavailable). d1 is **UNTESTED** for those six. Official in-force product lists and delivery times were not used to form a K_obs where d1 cannot be scored, so no unofficial distance is reported.

**d2.** Not scored (same assumed-term barrier as B2). **UNTESTED** / not used in the rank test.

**Rank test.** Complete pairs with both S and a complete d1: n = 1 (GB only). Under the locked allowance, n < 5 ⇒ the test is **UNTESTED**. No pass or fail is recorded. Independently of that sample-size rule, and as scored, the test cannot test the hypothesis, because no grid in the set qualifies. A later pass can add spectra or substitute an island grid; it cannot patch this verdict after seeing a correlation.

## What remains

- Official delivery times for the 1 January 2020 GB suite, so B3a can be scored.
- A sourced official GB (and, if possible, other-grid) ruin-dimensioning rule, so B2 / d2 are not assumed-term inconclusive, and the B1 gap can be interpreted under binding ruin (`theory/ROBUSTNESS.md`).
- Public imbalance spectra for the other grids, or a declared UNTESTED if none exist without an account.
- Hawaii (or New Zealand / Cyprus) Pass 1 score, still UNTESTED.
- AEMC reliability-settings and EirGrid System Services PDFs that returned HTTP 403 in this pass, if they can be retrieved another public way (currently MISSING; those S totals are lower bounds).
- A class with real competing design lineages, if the hypothesis is to be tested rather than diagnosed.
