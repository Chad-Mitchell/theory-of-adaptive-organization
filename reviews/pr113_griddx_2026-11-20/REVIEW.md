# Independent hostile review: PR #113 (GRID-DX), head `da5b971`

Reviewer: independent executor (did not author this PR). Friday 20 November 2026, about 1:45 PM ET (America/New_York).
Scope: prereg `5d0c11a`, Part A `7ce323a`, Part C Pass 1 `eae72a9`, Part B and Pass 2 `da5b971`, compared with main `45a70cf`.

## Verdict: **NOT READY**

The core finding of Part A is defensible: GRID-2 was never a qualifying test under the definition in force at the time. But the PR (i) relabels only the two misses and leaves the passes standing under the same unchecked qualification, (ii) gives a wrong reason for item (a), (iii) reports the B1 "gap 3" without saying that GB breaks B1's own ruin-slack premise, (iv) puts "law" into a status label, and (v) does not rebase cleanly.

## Checks run

- `nice -n 19 python3 tools/check_consistency.py` on `da5b971`: **RESULT: PASS** (0 FAIL; length warnings only).
- `nice -n 19 python3 -m pytest -q tools/`: **98 passed** (85 s).
- Rebase onto `45a70cf`: **conflicts** in README.md, STATUS.md, THEORY.md and measurement/CLAIM_MAP_v2.md (the version pointers v2.64 vs v2.65, the v2.64 note placed next to the v2.65 note, and the tally header). They are mechanical to resolve. The v2.65 number is correct, since #112 took v2.64. Keep both notes, newest first. The tally math (OPEN 78, PROXY-FAIL 18, NOT APPLICABLE 2, DECIDED 5, INCONCLUSIVE 7, total 297) carries over, because #112 changed no rows. After resolving, re-run the check.
- The definition quote was verified verbatim at `36416d2` (THEORY §3 lines 45–51; FRAMEWORK §9 item 1). The definition text first entered at `b311a40` (02:06 AM ET), **before** the GRID-2 prereg (09:56 AM ET). So the definition itself was not written after the miss.
- `36416d2` is **not reachable from main**; it exists only on the PR #110 head, which was squash-merged as `e1be66e`. Anyone working from main cannot resolve the cited commit.
- All 21 URLs in QUALIFICATION.md return HTTP 200. The following were spot-checked against the source text:
  - FRCR 2025 (March 2025): 140 → 120 GVA·s, Ofgem approval 9 June 2023, phases on 28 Feb 2024 and 19 Jun 2024, the 102 GVA·s proposal, the £96m/yr saving, and coal phase-out in 2024. All ✔.
  - DC first delivery at 23:00 on 1 Oct 2020 ✔. DR first auction 8 Apr 2022 and DM 6 May 2022 ✔. (The PR 2022 annual report also says loosely "launched in May 2022"; the doc-266976 launch slide confirms the dates.)
  - EFR starts Apr-17 to Mar-18 ✔. EFR contracts "will end in 2022" ✔. DFFR final round 166, final delivery Nov 2023 ✔.
  - BR first auction 12 Mar 2024 for 13 Mar delivery ✔. QR platform 19 Nov 2024 and first auction 3 Dec 2024 ✔. SR go-live 31 Mar 2026 (notice dated 16 Mar 2026) ✔.
  - NESO launched 1 Oct 2024. The not-for-profit and "HMG … not exposed to downside losses" quotes are accurate. The EFR ITT quote on falling inertia ✔.
- DOIs: the PR adds no new DOI. The quoted Lynch et al. 2016, 10.1038/nrg.2016.104, resolves on Crossref ("Genetic drift, selection and the evolution of the mutation rate", Nat Rev Genet) ✔.

## Must-fix

**M1. Asymmetric application: miss relabeled, passes left standing.** Under the same lock-time definition, no field row in CLAIM_MAP has a recorded qualification (a)–(e). `rg qualif theory/measured` finds none outside GRID-DX, and the E. coli prereg says outright that it "does not meet that bar". Yet:
- P18 (GRID-1b, Continental Europe) and P20 (GRID-S, German) keep **PROXY-PASS**. They are the same substrate class (grid balancing), and the PR's own Part C scores Continental Europe at S = 1, *below* GB's 5.
- The other 8 PROXY-PASS rows and 18 PROXY-FAIL rows are untouched.

Relabeling only the two misses is exactly the pattern FRAMEWORK's anti-rescue rule exists to stop, whatever the intent. Fix with one of these:
- (a) Apply NOT APPLICABLE by the same mapping to every field row with no recorded qualification, passes included. At minimum, do P18 and P20 in this PR, because they are the same class.
- (b) Keep P19/P21 as PROXY-FAIL with a "system not qualified; not evidence either way" annotation. Under THEORY's status words, PROXY already means "a result about that instrument, not about the theory".

Either way, state the rule in the status-mapping row so that it applies to any row, not just these two.

**M2. Item (a): the stated reason is wrong.** QUALIFICATION.md says no source links the operator's profit to balancing cost, and dismisses ESORI. It misses Ofgem's **Balancing Services Incentive Scheme (BSIS)**, which ran inside the 2011–2026 window. Under BSIS, National Grid Electricity Transmission, a for-profit plc subsidiary, kept or paid 25–30% of any under- or over-spend against a balancing-cost target, capped at ±£25–30m a year (2013–17), then 10% and ±£10m in 2017/18. Sources:
- https://www.ofgem.gov.uk/sites/default/files/docs/2015/03/electricity_so_incentives_-_final_proposals_2.pdf
- https://www.ofgem.gov.uk/sites/default/files/docs/2017/03/final_proposals_for_electricity_system_operator_incentives_from_april_2017.pdf

The lock-time text of (a) says, for firms, "the elasticity of … profit margin to J, with its source". A sourced profit-margin link to a component of J existed, and a σ was computable; it was simply never computed. The A.3 gloss "a regulatory incentive scheme … is not σ" was written at 13:22, after the miss; it is not in the `36416d2` text. Correct wording: (a) **not established**, not "failed". Also, NESO's not-for-profit status dates only from 1 Oct 2024, while most of the 2020–24 redesign happened under the incentivised ESO.

**M3. "All five items fail" overstates; the honest label is narrower.** On the evidence:
- (a) Not established (M2).
- (b) The PR leans on "N_e is not defined", reached by extending the nation-state exclusion by analogy. That extension is an A.3 gloss; the lock-time list names cities, nation-states, economies and the biosphere, not system operators. The stronger and correct argument is positive: for firms N_e *is* defined, as "independent firms in one market … with entry and exit". GB has one design-setting operator, a regulated monopoly with no entry or exit, so **N_e = 1**.
- (c)/(d) With N_e = 1, ε = 10/σ, which is at least 100% of J for any σ ≤ 10. Such a band cannot exclude any rival, so (d) fails positively, not merely "cannot be computed".
- (e) T_red was never defined, and the "same world" condition positively fails on the outturn inertia already in the repo (229 → 168 GVA·s). Two cautions:
  - The falling minimum-inertia *requirement* (140 → 120 → 102) is the operator's own design choice, not a statistic of the world. Do not cite it as evidence that the world changed.
  - "R < 10 go-lives" is not a test of "10 T_red". T_red is a gap-closing time, not a count of redesigns. Keep R as information only, as the file half-says already.
- The procedural failure (nothing recorded before measurement) holds. On its own, though, it shows only that qualification was **never established**, not that the system fails the definition. The decisive substantive reason is N_e = 1 ⇒ (c)–(d).

Recommended exact verdict line:
> **NOT QUALIFIED.** Qualification was not established before scoring (required by THEORY §3 at `36416d2`). On the lock-time definition, the decisive item is the population proxy: one design-setting operator with no entry or exit (N_e = 1), so no selection-resolvable band could exclude a rival ((c)–(d)), and T_red was never defined while the world (outturn inertia) changed ((e)). A profit link to balancing cost existed under BSIS (2011–18), but σ was never computed ((a) not established).

**M4. "law" in a status label breaks the repo rule.** The rule is that "law" appears only in the hypothesis sentence. The PR adds it to the CLAIM_MAP status cells (P19, P21), SYNTHESIS, DEVIATIONS, both RESULTS notes, the JSON and the test, under an exception the prereg granted itself (§A.4, "mandated"). Chad's t2005 asked for "not an appropriate test / does not apply / patient", not for the word "law". Use "not a test of the hypothesis".

**M5. Part B: K\* = 1 holds only under ruin slack, and GB breaks that premise.** B1 is "sensing-limited J, ruin slack". The official sources show GB's layers are contingency and ruin products. The FRCR 2025 sizes DC for "post-fault frequency risks" against a largest loss of 1,800 MW, with DM/DR as pre-fault services. The repo's own SYNTHESIS (lines 46, 58) already says GB's layers are tiered by actuation and by deviation size ("ruin products such as DC").

So "K_obs − K\* = 3" is computed under a premise the system is known to violate. The extra layers may be redundancy against component failure or unmodelled tails, which B1's design space does not represent. RESULTS_GRIDDX B1, P24, SYNTHESIS and the "patient" framing do not say this. "Not a demonstrated inefficiency in money" is not enough, because it implies the gap is real and only its price is unknown. Add, wherever the gap is quoted:
> "Under B1's premises only. GB's ruin constraint binds (post-fault containment sized to the largest loss), which B1 assumes away, so the gap may be redundancy B1 cannot represent; it is not shown to be excess."

**M6. "Patient" presumes a sickness that is not shown.** "Diagnosis of a patient" asserts the system is suboptimal, yet Part B finds the saving and the direction INCONCLUSIVE, and M5 shows the gap may be redundancy. Read that way, the headline quietly treats the theory's prescription as correct and the grid as wrong. That is the same claim GRID-2 could not test, now in the other direction. Two options:
- Keep "patient" in prose with the gloss "a system examined prescriptively; no inefficiency is established".
- Drop it from the CLAIM_MAP status column.

Suggested status: `NOT APPLICABLE (system not qualified): a prescriptive diagnosis, not a test of the hypothesis`.

**M7. Rebase conflicts** (see Checks). Resolve onto `45a70cf`, keep v2.65, and re-run the check and pytest from the merged tree.

## Should-fix

**S1. Post-hoc risk, which should be disclosed in the prereg and results.** The definition predates the miss (good). But:
- The audit was triggered by the miss (b7f69e8 at 10:52 AM; GRID-DX prereg at 13:22) and the owner's pushback.
- The A.3 verdict rules and A.4 wording map were written knowing the outcome.
- QUALIFICATION.md, with about 21 sourced URLs, was committed **2 min 26 s** after the lock. Pass 1 followed about 3 min later and Pass 2 about 3 min after that.

The sources were clearly gathered, and the verdict effectively known, before the "lock". State plainly that Part A is an audit with a foreknown answer, and that the prereg gives no blinding for Part A. The Part C Pass 1/Pass 2 timing, minutes apart, also does not show that no Pass 2 information was seen; say so.

**S2. GB scored highest (S = 5) yet declared not qualified.** This is not incoherent, since the rubric gives partial credit for weaker proxies (BSIS/ESORI-type incentives, FRCR). But it has two consequences the PR should state:
- (i) The rubric measures something other than qualification. If the top-scoring grid fails, **no grid in the set qualifies**, so Part C can never test the hypothesis either; at most it is a descriptive correlation.
- (ii) The prereg sentence "A low S for GB is consistent with NOT QUALIFIED" is moot. Explain why a high S also does not re-qualify GB.

**S3. The scores largely reflect how hard each grid was searched.** GB was scored from sources already gathered for Part A. AU, IE/NI, Nordic and CE got 0s because PDFs returned 403 or "none found this pass". For example, the NEM has a widely published reliability standard and a market price cap, and AU's S_ruin = 0 follows only from a 403. Under the rubric, "missing official source → 0" is legal, but the result is that S ranks retrieval success. Mark those components UNTESTED (missing), not 0, or label S as a lower bound. Otherwise any future Pass-2 correlation is confounded.

**S4. Rubric ambiguity on S_N.** GB literally meets the 0 clause ("a single system operator sets the product suite, and no class-specific N_e was preregistered") and also the 1 clause (competitive procurement). The scorer chose 1. State the precedence rule; as written, 0 is reachable only by grids without competitive procurement.

**S5. Qualification is defined for a substrate *class*, not a single system.** THEORY §3 qualifies "a substrate class", and FRAMEWORK item 7 excludes classes below n_min. Part A audits one system. Name the class (for example, synchronous-area balancing designs) and note that the class itself has no preregistered n_min or N_e. This strengthens M1: P18/P20 belong to the same unqualified class.

**S6. Cite a reachable commit for the definition.** Add "(on PR #110 head; squash-merged to main as `e1be66e`)" or quote the main-reachable `b311a40`.

**S7. B3 headline.** B3a is UNTESTED and B3b INCONCLUSIVE. The prereg rule covers only the case where the two arms disagree. Report "UNTESTED / INCONCLUSIVE" rather than a bare INCONCLUSIVE.

## Nits

- N1. `tools/test_griddx.py` hard-codes the values it checks (S totals, verdict strings), so it is a snapshot test, not a test of the rules. Fine as a guard, but don't describe it as checking "the locked rules".
- N2. The CLAIM_MAP v2.65 note should mention that it follows the v2.64 note from #112 (after rebase), and list P23–P25.
- N3. The GRID-2 2026 sample (Nov 2025–Oct 2026) counts Slow Reserve as a layer, but SR went live only on 31 Mar 2026, partway through the sample. This is a pre-existing GRID-2 issue, not this PR's, but QUALIFICATION's go-live table makes it visible; worth a dated note.
- N4. QUALIFICATION §(a) quotes "HMG … not exposed to downside losses (including from incentives…)". That sentence is about the shareholder, and it implies NESO still faces incentives. It does not show that NESO lacks a cost link; drop it or reword.
- N5. Labels: "passed/failed on proxy", UNTESTED and INCONCLUSIVE are used correctly; "cost" is used throughout and no "bill" appears. The only "law" violation is M4; "power law" is fine.

## What is right

- History is preserved: the G1 "FAIL on proxy" text and numbers stay in RESULTS_GRID2/3_4 and in the CLAIM_MAP cells.
- G3b is correctly not used.
- No £ saving is invented, B2 is honestly INCONCLUSIVE, and the n = 1 rank test is correctly UNTESTED.
- All dated facts checked are accurate, and every URL resolves.
- The lesson ("qualification should have been checked before scoring and was not") is stated plainly.

---

# Confirm round: head `315e620` (rebased on `45a70cf`)

Reviewer: same independent executor. Friday 20 November 2026, about 2:00 PM ET.

## Checks
- The branch is rebased: `45a70cf` is an ancestor of `315e620`, so there are no conflicts. The rebase changed the SHAs (prereg `5d0c11a` became `d70c540`; Part A `7ce323a` became `50350e0`). QUALIFICATION.md and the CLAIM_MAP note give both SHAs.
- `check_consistency.py` at nice 19: **RESULT: PASS** (FAIL 0).
- `pytest tools/` at nice 19: see the result line at the end of this section.
- Tally arithmetic is correct. Recomputed from the tally block: OPEN 78, PROVED 84, NOT A TEST… 30, PRIOR ART 28, MATH-CORRECTED 22, NOT EVIDENCE 20, WITHDRAWN 11, INCONCLUSIVE 7, SIM-FAIL 6, DECIDED 5, SIM-INCONCLUSIVE 3, SIM-PASS 3. Sum 297 = 294 + 3 new rows (P23–P25). The 30 retyped rows are 10 former PROXY-PASS + 18 PROXY-FAIL + P19/P21. The checker recomputes this from the rows and passes.
- The BSIS figures match the Ofgem PDFs, which I downloaded and read:
  - 2015 Final Proposals (published 19/03/2015): the 2013–15 scheme ran at 25% / £25m per annum, and Ofgem first proposed keeping it; the 2015–17 scheme is 30% / ±£30m a year.
  - April-2017 Final Proposals (published 01/03/2017): ±£10m cap and floor, 10% sharing factor, and the stated change "from ±£30m to ±£10m and the sharing factor from 30% to 10%".
  - My first-round "25–30%" covered 2013–17 and "10%/±£10m" covered 2017/18, so both figures stand. QUALIFICATION.md states all three periods correctly, with dates and URLs.

## First-round items
| Item | Status |
|---|---|
| M1 asymmetry | **Fixed in principle**: passes and misses retyped together; P18/P20 named as the same class. Overbreadth issues below (C1–C3). |
| M2 item (a) | **Fixed.** "Not established", BSIS sourced and checked, and the post-miss gloss disowned. |
| M3 honest verdict | **Fixed.** N_e = 1 ⇒ (c)–(d) substantive; (e) uses outturn inertia; the requirement is called a design choice; R is informational. The suggested verdict sentence was adopted. |
| M4 "law" | **Fixed in labels, JSON and tests.** Leftovers: see C5. |
| M5 ruin-slack caveat | **Added everywhere the gap is quoted**, but the wording names one mechanism too specifically (C4). My first-round suggested wording ("may be redundancy") caused this, and I correct it below. |
| M6 "patient" | **Fixed.** Not a status; in prose glossed "examined to prescribe; no inefficiency shown". |
| M7 rebase | **Fixed.** |
| S1 blinding | **Fixed** (disclosed in QUALIFICATION.md). |
| S2 GB S = 5 vs not qualified | **Fixed** (SELECTION_SCORES note and RESULTS: no grid in the set qualifies, so Part C cannot test the hypothesis). |
| S3 missing sources | **Fixed** as a dated note: MISSING, S totals are lower bounds, Pass 1 table not rescored. Acceptable. |
| S4 S_N ambiguity | **Disclosed**, not rescored. Acceptable. |
| S5 class, not system | **Fixed.** |
| S6 reachable commit | **Fixed** (`b311a40`; `36416d2` on #110 head, squash-merged as `e1be66e`). |
| S7 B3 headline | **Fixed** (UNTESTED/INCONCLUSIVE). |

## New findings

**C1 (must-fix). Two reasons collapse into one status, losing a distinction.** Before, the status column said why a row was not evidence: the instrument failed validity gates (PROXY). Now it says only "qualification not established". For many rows the proxy failure is the *stronger and independent* reason. For example, K10 is "out of the theorem's domain", H9 fails MV2/3/5/6/7/9, and N10 is "non-discriminating". Those reasons now sit only inside the cell text. A reader scanning the status column can no longer tell a row that is not evidence for two reasons from one that might become a test if someone just recorded qualification. Fix with one of these:
- (a) A compound status, for example `NOT A TEST (qualification not established; proxy: passed)` / `(…; proxy: failed)`, kept consistent with THEORY's status words.
- (b) A separate column for the original proxy result.

The tally should still be able to report how many former passes and fails there were. This is not cosmetic: the repo's rule is that results are reported as passed/failed on proxy (THEORY lines 53 and 174), and the new label hides that.

**C2 (must-fix). THEORY.md does not define the new status and still says the opposite.** THEORY is canonical ("where anything else disagrees, this file governs"). Its status words and lines 53 and 174 still say field results "are reported as passed or failed on proxy". The new status is defined only in FRAMEWORK.md and CLAIM_MAP. Either add it to THEORY's status words, with the rule (any field claim without a recorded pre-test qualification check), or don't make it the headline status. This also changes a repo-wide labeling convention that Chad set ("passed/failed on proxy"). Flag it to him for an explicit go before merge, rather than treating it as reviewer-approved.

**C3 (should-fix). Overbreadth: the PR flags no row as plausibly qualifiable.** "Not established" is the right word for every row except P19/P21, and the PR uses it correctly. P19/P21 are the only cells that say "not qualified", and they have substance (N_e = 1, T_red, inertia). Nothing else is labeled NOT QUALIFIED without substance, which is good. But the blanket wording treats E. coli and an MTurk lab task alike. Add a one-line "qualification prospect" per row, or grouped per class, naming the missing check. My reading:
- *Plausibly qualifiable; the check is to record σ, N_e and T_red from literature before any re-score:* the E. coli rows P1, P3, P4, P13. Bacteria are the definition's own example class ("cells and microbes: measured"). σ could come from the measured growth-rate cost of chemotaxis machinery, N_e is very large, and T_red comes from generation time. Long-evolved biological rows (H2 forgetting exponent, H12 glucose, H18 immune, H9 measles) are possible but each needs a class-specific σ and N_e.
- *Possibly qualifiable as the firm class (σ from profit or survival elasticity, N_e of competing firms with entry and exit):* H11 banks, H14 firms, H17 inventory buffers, perhaps H15 open source.
- *Substantively unlikely, or closer to GB's position:* H7 (one firm, Enron), N1/N2 (people inside firms), N5 (self-tracking), N10/N14/N17/N20 (GitHub, Wikipedia, Wikidata edit series), N23 (lab subjects on MTurk, no selection), K10 (languages, flagged out of domain; N_e undefined like the excluded classes), H13 (populations; check whether it falls in the excluded nation-state class), P18/P20 (same class as GB; continental TSOs share harmonised products, so design lineages are few and not competing).

These are reviewer judgments, not verdicts. They should go in as "prospect" notes, not statuses. They would turn the retype from erasure into a work queue: the next real test is a class where qualification can be recorded first, which is most likely E. coli.

**C4 (must-fix; ties to PR #115). The ruin caveat names redundancy too specifically, and in one place asserts it.** Every copy says "the gap may be [unmodelled] redundancy the cost's design space cannot represent". RESULTS_GRIDDX line 21 is stronger: "The gap of 3 **may therefore be** redundancy." Two problems:
- In-model, robustness gives bigger buffers and more *same-speed* copies, not new layers at new speeds. Draft PR #115's CT37–40 says so, and the repo's own `theory/STORE_NOISE.md` E1-c ("copies, not new time constants") already said it.
- The locked GRID-2 counting rule groups same-speed products as one layer (DC and DM count as one). So same-speed redundancy could not raise K_obs in the first place.

Redundancy is therefore an unlikely explanation of a gap in *distinct speeds*. Replace it everywhere (CLAIM_MAP v2.65 note and rows P19, P24; RESULTS_GRIDDX lines 21, 35, 47; SYNTHESIS lines 20, 63, 81; PREREG_GRIDDX implementation addendum line 250) with:
> "B1 assumes ruin slack; GB's ruin constraint binds (FRCR DC sized for an 1,800 MW largest loss). The gap may reflect costs or constraints the design space does not represent (e.g. ruin-binding reserve sizing, short-duration fast units, actuation limits); it is not shown to be excess, and no mechanism is established."

Drop "therefore". This corrects my own first-round M5 wording.

**C5 (should-fix). Leftover "law" text.** The superseded label "…not a test of the law" is kept as "history" in CLAIM_MAP P19/P21 cells and in DEVIATIONS DV-GRIDDX-A. That label was never on main: it existed only inside this unmerged PR. Preserving it as history therefore preserves nothing public, and it puts "law" outside the hypothesis sentence in maintained files. Drop it from the CLAIM_MAP cells. In DEVIATIONS, either reword DV-GRIDDX-A or quote the label once inside A.1 as the withdrawn draft wording. The PREREG §A.4 copy is locked text and may stay.

**C6 (should-fix). DV-GRIDDX-A is stale.** It still says "no sourced σ … exist[s]", which contradicts (a) "not established". DV-GRIDDX-A.1 corrects it, but a reader of A alone is misled. Add "(corrected by A.1)" inline.

**C7 (nit).** DEVIATIONS and the RESULTS dated notes cite only the original `5d0c11a`. After the force-push it is reachable only through GitHub's PR history. Add `d70c540` wherever only the old SHA appears.

**C8 (nit).** "Examined to prescribe; no inefficiency shown" is good. Also say once, in RESULTS_GRIDDX B1, that "diagnosis" means a reading under B1's premises only.

## Labels
- "cost" is used throughout; no "bill".
- UNTESTED, INCONCLUSIVE and MISSING are used correctly.
- No "law" in any new label, JSON headline or test-checked text. Leftovers are listed in C5. "Law firm" and "power law" are fine.
- No overstatement in the headline. The one overstatement left is C4's "therefore".

## Confirm verdict: **READY-WITH-FIXES**, with conditions

Merge after C1, C2 and C4 are fixed. C2 needs Chad's explicit go, because it changes his "passed/failed on proxy" labeling convention for 30 rows. C3, C5 and C6 should go in the same pass; they are wording-only. The GB Part A verdict, the BSIS correction, the symmetric application and the Part B/C UNTESTED/INCONCLUSIVE results are now sound.

**pytest result (`315e620`, nice 19):** 99 passed in 283 s; the box was heavily loaded.

---

# Final confirm: head `fe3a080` (on main `45a70cf`)

Reviewer: same independent executor. Friday 20 November 2026, about 2:15 PM ET.

## Checks
- Branch: `45a70cf` (current main) is an ancestor, so there are no conflicts.
- `check_consistency.py` at nice 19: **RESULT: PASS** (FAIL 0).
- `pytest tools/` at nice 19: **99 passed** (279 s; the box was loaded).
- Tally: 10 + 18 + 2 compound NOT A TEST rows. Total 297 = 294 + P23–P25. The checker recomputes from the rows. Only P19 and P21 carry "not qualified"; every other retyped row says "qualification not established".

## C1–C8
| Item | Status |
|---|---|
| C1 compound status | **Fixed.** `NOT A TEST (qualification not established; proxy: passed/failed)` and `NOT A TEST (not qualified; proxy: failed)` for P19/P21. The proxy result is back in the status column and the tally splits it. MV-gate reasons stay in the cells. |
| C2 THEORY | **Fixed in text.** THEORY lines 53 and 174 now say field results are "first gated on qualification under the pre-written definition (§3), then reported as passed or failed on proxy", and define NOT A TEST with both compound forms. The §3 definition itself is **unchanged**, so no post-hoc edit to the gate. Nit: the status-word list on line 5 still lists only Proved / Known / Open / Passed-failed on proxy; add *Not a test*. **Merge condition, not a text defect:** this changes the labeling convention Chad set for 30 rows and adds a gate to the canonical THEORY. The PR text does not record his go, so get it explicitly before merge. |
| C3 prospects | **Fixed.** All 30 rows carry "Qualification prospect (reviewer judgment, not a verdict)". E. coli (P1 etc.) is marked plausibly qualifiable, with the check named (σ, N_e, T_red from literature before any re-score). Firms are "possibly", and lab, edit-series, language and grid rows are "unlikely". Nothing is upgraded to a status. |
| C4 ruin caveat | **Fixed.** No "redundan…" remains anywhere in measurement/, theory/measured/, README, STATUS or THEORY, and "therefore" is gone. The reviewer wording ("may reflect costs or constraints the design space does not represent (e.g. ruin-binding reserve sizing, short-duration fast units, actuation limits); it is not shown to be excess, and no mechanism is established") appears in CLAIM_MAP (3), SYNTHESIS (3), RESULTS_GRIDDX (3) and the PREREG addendum (1). That matches "neither explained nor shown to be waste". |
| C5 "law" leftovers | **Fixed.** "not a test of the law" is gone from CLAIM_MAP, DEVIATIONS, SYNTHESIS, RESULTS and JSON. It remains only in the locked PREREG §A.4 text and in the addendum that supersedes it, both acceptable, and in tests that assert its absence. No new "law" outside the hypothesis sentence. |
| C6 DV-GRIDDX-A | **Fixed** ("corrected by A.1" in the heading and inline). |
| C7 SHAs | **Fixed** (`d70c540` added next to `5d0c11a`). |
| C8 diagnosis gloss | **Fixed** (RESULTS_GRIDDX B1: "a reading under B1's premises only"). |

## No new errors found, with two nits
- N-a. RESULTS_GRIDDX line 23 still says "not a demonstrated inefficiency **in money**". Read next to the caveat it is fine, but "in money" faintly implies an inefficiency in kind. Suggest dropping "in money". (PREREG line 92 has the same phrase as locked text; leave it.)
- N-b. THEORY line 5 status words: add *Not a test* (see C2).

## Final verdict: **READY**, conditional on Chad's go for the C2 convention change
The text is correct. Merge once Chad explicitly approves the THEORY/CLAIM_MAP labeling change (field results gated on qualification; 30 rows now under compound NOT A TEST statuses). If he declines, revert to PROXY-PASS/PROXY-FAIL and keep the "qualification not established" notes and the prospects in the cells. Nits N-a and N-b can ride along or follow.
