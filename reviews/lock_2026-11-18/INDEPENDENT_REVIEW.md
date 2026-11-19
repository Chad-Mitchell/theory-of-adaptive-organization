# INDEPENDENT_REVIEW: hostile-but-fair review of the lock pass (PRs #95, #96)

Wednesday 18 November 2026, about 11:00–11:20 PM ET (America/New_York). Reviewed tree: `main` at `e4274aa` (THEORY v1.4.27, CLAIM_MAP v2.46). Requested by Chad Mitchell (pt1957u), via Ace. Fixes applied in the same PR: THEORY v1.4.28, CLAIM_MAP v2.47. Nothing was posted or sent, and no account was created.

**Independence.** This reviewer is a fresh Grok Bot executor. It wrote none of `reviews/lock_2026-11-18/` (LOCK_AUDIT, NARRATIVE, PROCESS, LOOSE_ENDS, README), none of the README rewrite, none of CLAIM_MAP N51–N53 and none of checker rules R1–R5. It is from the **same bot family** as every author and earlier reviewer, so it is a second reader, not a blind grader, and it does **not** meet LOCK_AUDIT condition 3 (a whole-document read by someone outside the family). It did not read THEORY.md end to end; it read the sections the lock pass cites.

**Read:** README (first, before any other file, in three personas), `git show 601344e:README.md`, THEORY header, status block, §0, §1 (N2, N6), §2.3, §6, §7, §9, §10 (citations), §13; `theory/THEOREMS.md` T3a; CLAIM_MAP N27, N51–N53, F13, J9, the tally; all five lock-pass files; `tools/check_consistency.py` and its test; `queue/LEDGER.jsonl`; BRIEF §6. **Sources opened:** Bloom, Garicano, Sadun & Van Reenen 2014 (abstract, Crossref and OpenAlex); Kaplow 1992 (Duke LJ full-text PDF, contents page and pp. 557–590 with notes; the fetch was truncated before §IV.C); Juni, Gureckis & Maloney 2016 (abstract); Sheridan 1970 (abstract); Baker & Hubbard 2004 (abstract); Crossref records for Senders 1964, Krauss & Scherrer 2007, Acemoglu et al. 2007, Kirkwood 1977, Boraas, Seale & Boxhorn 1998, Herron et al. 2019 (art. 2328) and Maister 1976. Every bibliographic detail cited in LOOSE_ENDS matched its record.

## Verdict

**PASS-WITH-FIXES. The lock pass's verdict, "lockable, not locked", is sound and is confirmed.** The README rewrite is a real improvement: the keep / burn / know table makes the frame click in under a minute for all three personas. But the rewrite opened with a sentence its own table contradicts, dropped three qualifiers that a token check could not see, and kept the cross-scale bet off the first screen. LOOSE_ENDS understated the prior art for N53 (Kaplow 1992 has a section on change over time) and left out a rival and a needed distinction for N52. PROCESS's counts are mostly right, but four of them are off or cannot be reproduced. Rules R1–R5 work on their planted cases; R1 had one false negative that matters (it did not see the lock-pass files as self-reviews) and one false positive. No BLOCKER beyond the existing B1. All SHOULD-FIX items are applied in this PR. No CLAIM_MAP status changes.

## 1. README as a cold reader (read first, before any other file)

"First screen" here means lines 1–28 of the README at `e4274aa`: the headline, the one-table idea, the bill and the five implications.

| Persona | What the core idea is after the first screen | Did it click? |
|---|---|---|
| **Physicist** | Things that persist fall into three classes: frozen (no upkeep), held by a throughput (no model), and trackers that pay for memory, error and reads; GTAO adds no new physics, and the black-hole and atom rows are placements, not derivations. | **Yes as a frame, correctly not as physics.** The black-hole row (Bekenstein-saturating memory, almost none of it readable) is stated accurately. Two snags: line 5's "Everything that lasts has to pay" is contradicted three lines later by the Keep row ("What it pays: Nothing"), which is the first thing this reader catches. And with the old caveat "no proof in the formal layer depends on the second law" dropped, line 11 makes the second law look load-bearing, which invites the "physics vocabulary on a decision model" reaction NARRATIVE itself predicts. |
| **Biologist** | Cells, immune systems and colonies are trackers. How often to sense, how long to remember and how many memory stores to keep are set by how the environment's change is spread over timescales. The sensing case is credited to Mora & Nemenman. | **Mostly yes.** The credit is visible early, which buys trust. "Spectral slope α" is not defined on the first screen. The geometric-random-walk premise for Mora & Nemenman (why α = 2 applies there) was dropped. The "who must be in charge" bullet connects well to social insects. The bet that the *same* relations hold at every level appears only at line 32. |
| **Organization theorist** | A firm is a knower paying memory, error and read costs; levels pay above a group-size threshold (T3a); "no one in charge" holds only when shared memory is privately rewarded; large trackers federate. | **Partly.** T3a and the J9 bullet land at once. The light-delay bullet reads as irrelevant to firms ("on Earth this is a latency cost"), and the firm-scale analogue (decision latency, LOOSE_ENDS L3) is not on the README. The answer to "what is here beyond team theory?" is on the second screen ("What is new, and what is not"), which is acceptable. |

**Does the cross-scale bet click?** Not on the first screen at `e4274aa`: line 5 says the bill "shapes the design of any adaptive organization", but the falsifiable claim (the same relations, with inputs measured on each system, at every level, for strongly selected systems) first appears at line 32. **Fixed:** line 5 now states it.

**Accuracy against THEORY and CLAIM_MAP.** Every number, label and status on the README was checked against its source: the read-rate rule (THEORY §0, exact reset reads), T3a (THEOREMS T3a: the closed form is the h = 0 case of a sufficient condition, so "at zero upkeep … is sufficient" is right), Theorem G and T8 (THEORY §3 freeze-or-hold row; F13), J9 (THEORY §6), N25–N29 (THEORY §2.3), the kill conditions (THEORY §1 N6, §9), the drift-barrier rule (§7), LAT-1, the horizon numbers, and the scoreboard rows against CLAIM_MAP H/K. All match, apart from the items below.

## 2. LOOSE_ENDS and CLAIM_MAP N51–N53

- **N51 (attention exponent).** The logic holds. With reset reads and error growing as ℓ^{α−1} (the same law LAT-1 uses), minimizing c·r + w·q·r^{−(α−1)} gives r ∝ (w·q/c)^{1/α}. Because fBm is self-similar, the exponent is the same under hold-last-value and under optimal prediction (only the constant changes), so a learner who extrapolates trends does not break it. The kill condition is honest, since it is scoped to learned human sampling and not to N13. Citations are accurate. One nit: Juni, Gureckis & Maloney 2016 sample a **static** target, so they supply the paradigm, not a drifting-world precedent (now said). **Short prior-art sweep** (web searches for optimal sampling of fBm with costly observations, and for lab tests of costly sampling of drifting processes): found work on estimating fBm parameters under sampling constraints and on rational-inattention lab tasks, but nothing testing a 1/α stakes elasticity. "Not found in a short search" stands. Label OPEN is right.
- **N52 (cheap lookup and levels).** The citations are accurate. Bloom et al. 2014's abstract: information technology "is a decentralizing force, whereas communication technology is a centralizing force". Three gaps, all now in LOOSE_ENDS §2 and the N52 note: (a) "lookup" must be coded as an **information-acquisition** cost, because a fall in communication cost predicts the opposite direction; (b) a **rival for the enforcement half**: cheaper information also cheapens monitoring, and Baker & Hubbard 2004 find on-board computers went with less independent contracting and larger firms, so enforcement and governance can move through a channel GTAO does not model; (c) the step from per-fact T8 to whole levels is **extrapolated, not derived**. Garicano's layers are themselves knowledge-pooling layers, so only the enforcement contrast is left as GTAO's. G is lowered from medium to low–medium. Label OPEN is kept.
- **N53 (rules versus standards).** **Prior art understated.** LOOSE_ENDS and the N53 row said Kaplow 1992 covers "frequency, not drift". The paper's contents list §IV.C, "Changing Rules and Standards over Time" (pp. 616–618). Its n. 25 says "the possibility of changing circumstances is considered in Section IV(C)", and n. 63 discusses acts "about which little is known, as when there is a technological advance". The body of §IV.C could not be read (the retrieved text stops near p. 590), so how far Kaplow goes is unverified. What GTAO adds is at most a measured drift rate kept separate from frequency, plus the three-way freeze / hold / lookup map. G is lowered to low. The N53 note is corrected, and an N52-N53-SWEEP queue item is added. Label OPEN is kept.
- **Kill conditions.** All three are stated before any data and name the direction. N52's kill now needs the information-versus-communication coding, or a divergence cannot be scored. Fine as OPEN hypotheses. None is near preregistration (MV1–MV10 are still owed, as the rows say).
- **Section pointers.** LOOSE_ENDS cited "THEORY §12" as the prior-art list three times. §12 is "Source files", and the citations are in §10. Fixed.
- **The self-application counts** (LOOSE_ENDS end; PROCESS §1 and §4) could not be reproduced as written; see §3.

## 3. PROCESS.md and LOCK_AUDIT.md

Recomputed from git, `gh pr list` and the ledger. All PROCESS counts are as of `601344e` (the tree before the pass), which the file did not say; that is now stated.

| PROCESS claim | Recomputed | Verdict |
|---|---|---|
| 414 commits | `git rev-list --count 601344e` = 414 (421 at `e4274aa`) | Right, at 601344e |
| 94 PRs: 93 merged, 1 closed (#16) | 94 at 601344e (96 now, 95 merged, #16 closed) | Right, at 601344e |
| Non-merge by day: 4 / 238 / 40 | 4 / 238 / 40 (ET) | Right |
| 176 of 282 (62%) mention ledger, queue or pick | 176 of 282 by subject regex | Right as a *mention* count; **misused as "bookkeeping"**. Many of those commits carry results ("SPF-NOISE-PROXY: RESULTS …, ledger 31 outcome"). Commits that touch **only** queue, status or brief files: **99 of 282 (35%)**. Both now reported. |
| 27 THEORY versions "in 4 calendar days, two of them working days" | **28** dated versions v1.0–v1.4.26 (v1.4.3a counted; v1.4.12 unused), on **3** calendar days: Sat 14, Sun 15 and Wed 18 Nov, only one of them a weekday | Wrong; fixed |
| 6 of the first 11 scored outcomes `status_changed`; 0 of the next 40, from 12:45 PM; four added rows (N18, N21–N23) | With "scored" = a protocol-2 outcome not marked `scored: false`: 6 of the first 11 (09:40 AM–1:45 PM; the 11th, entry 61, added N18); **0 of the remaining 37** (2:53–8:19 PM, 15 Nov), of which **three** added rows (N21–N23) | The direction holds; the denominator, window and added-row count were wrong or rested on an unstated filter. Fixed. |
| 25 "with fixes", 1 FAIL | A hand count; `rg -i verdict reviews/` gives many non-verdict hits. Not reproducible from one command | Marked as a hand count |
| 10 corrected memory beliefs (BRIEF §6) | 10 rows | Right |

**Are the principles fair?** Mostly yes. P1–P6, P9 and P10 are well supported by the error table. P7 overstated its evidence (62% "bookkeeping"); the honest figure is 35% pure bookkeeping, which still supports a cap. "Reach work … the marginal pass was not [worth it]" is a fair judgment, and the file correctly calls Chad's scope binding. P10's self-application of Theorem G is properly flagged as a heuristic.

**Is "lockable, not locked" sound?** **Yes.** Condition 1 (consistency) is met; the checker passes. Condition 2 (no known error) was not quite met at `e4274aa`, given the SHOULD-FIX items below, and is met after this PR as far as this reader can find. Condition 3 (a whole-document read by a reviewer outside the bot family) is not met, and this review does not meet it. Condition 4 (a freeze rule) is Chad's call. LOCK_AUDIT's closing claim that the README "now says it on the first screen" was not true at `e4274aa`: the first screen said "not peer reviewed" but not "not independently reviewed as a whole". It does now.

## 4. Checker rules R1–R5

Each rule was probed with planted sentences in a temp copy (`probe.sh`-style; results below are from that run).

| Rule | Works on its test? | Problems found | Fix |
|---|---|---|---|
| R1 self-review called independent | Yes | **False negative:** the header regex missed "**Not independent**" mid-line and "This audit … is not independent", so LOCK_AUDIT, LOOSE_ENDS, NARRATIVE and PROCESS were not treated as self-reviews: "The lock audit `reviews/lock_2026-11-18/LOCK_AUDIT.md` is an independent review." **passed**. **False positive:** "Independent review 2 superseded the earlier pass in `reviews/reach_2026-11-18/REVIEW.md`." **failed**. It also missed "`X`, which is independent". | Header marks widened (and NARRATIVE's header bolded to match); flag only when "independent" is within 60 characters before the citation with no contrast word between (superseded, replaced, corrected, unlike, than, earlier, re-derived, checked, reviewed), or when the citation is followed by "(which/that) is independent". Four new tests, including one must-not-flag sentence; the original S19 wording is still caught. |
| R2 CLAIM_MAP tally | Yes; recount gives 227 | None found. It counts by first status word, so "PROVED (in-model); PRIOR ART close" counts as PROVED, which is the documented rule | — |
| R3 table cell counts | Yes | Strict: a row with *fewer* cells than its header renders fine on GitHub (empty cells) but is flagged. That is harmless hygiene; the failure message's "escape a pipe" advice is wrong for that case | NIT, not changed |
| R4 named relation called "law" | Yes | **False positive:** "the square-root law of Maister (1976)" (a published inventory term, verified on Crossref) is flagged. **False negative:** "√N scaling law" passes | Inventory and Maister context exempted; "scaling" allowed between; tests for both |
| R5 repo called private | Yes | **False negative:** "The repository remains private." passes | "remains" and "stays" added; test added |

After the fixes: `tools/check_consistency.py` PASS, `tools/test_check_consistency.py` PASS (every planted error caught, both clean sentences pass), `pytest tools/` PASS.

## 5. Findings

At `e4274aa`; every fix is applied in this PR unless marked.

| # | Sev | Where | Finding | Fix |
|---|---|---|---|---|
| B1 | BLOCKER (for lock; carried over) | `THEORY.md:4` | No whole-document read by a reviewer outside the bot family. This review does not change that. | Open (QUEUE WHOLE-THEORY-REVIEW; a note says this review does not discharge it) |
| S1 | SHOULD-FIX | `README.md:5` | "Everything that lasts has to pay" is contradicted by the Keep row ("What it pays: Nothing"; N25: frozen, h = 0). | "To last, a thing must either sit where almost nothing can knock it loose or pay to stay; …" |
| S2 | SHOULD-FIX | `README.md:5` | The cross-scale bet, the claim that can die, is not on the first screen. | Line 5 states it, with "strongly selected" and "same relations, not the same constants" |
| S3 | SHOULD-FIX | `README.md:11` | Dropped caveat (old README spine): "no proof in the formal layer depends on the second law" (THEORY §2.3, night-1 physics review). | Restored |
| S4 | SHOULD-FIX | `README.md:17` | Overclaim: "carrying a model and acting ahead **pays**"; old README and THEORY §0 say "can pay". | "can pay" |
| S5 | SHOULD-FIX | `README.md:7`; `LOCK_AUDIT.md:56` | LOCK_AUDIT says the README states the not-independently-reviewed status on the first screen; it did not. | "not independently reviewed as a whole" added to line 7; LOCK_AUDIT annotated |
| S6 | SHOULD-FIX | `LOOSE_ENDS.md:69–71`; `CLAIM_MAP_v2.md:407` | Kaplow 1992 is described as "frequency, not drift"; it has §IV.C "Changing Rules and Standards over Time" and notes on changing circumstances. | Corrected in both places; G lowered; sweep queued |
| S7 | SHOULD-FIX | `LOOSE_ENDS.md:48–55`; `CLAIM_MAP_v2.md:406` | N52 omits Bloom's information-versus-communication split, the monitoring rival (Baker & Hubbard 2004), and that the step from T8 to levels is not derived. | Added in both places; G lowered |
| S8 | SHOULD-FIX | `LOOSE_ENDS.md:5, 36, 54` | "THEORY §12" for prior art; the list is §10. | §10 |
| S9 | SHOULD-FIX | `PROCESS.md:13, 53, 75`; `LOOSE_ENDS.md` | "62% bookkeeping" counts subject mentions, including results commits. | 62% kept as a mention count; 35% pure bookkeeping added and used for P7 |
| S10 | SHOULD-FIX | `PROCESS.md:15, 54`; `LOCK_AUDIT.md:38` | "27 versions in 4 calendar days, two of them working days": it is 28 versions on 3 days, one of them a weekday. | Corrected |
| S11 | SHOULD-FIX | `PROCESS.md:17, 78, 81`; `LOOSE_ENDS.md:106–107`; `lock README:28` | Ledger yield counts ("next 40 from 12:45 PM", four added rows) not reproducible; the window overlaps the first 11. | Restated with the filter: 0 of the remaining 37, three added rows |
| S12 | SHOULD-FIX | `tools/check_consistency.py:237, 250` | R1 false negative (lock-pass files not seen as self-reviews) and false positive. | Fixed, with tests |
| S13 | SHOULD-FIX | `tools/check_consistency.py:314, 316` | R4 false positive (inventory "square-root law") and false negative ("√N scaling law"); R5 misses "remains private". | Fixed, with tests |
| S14 | SHOULD-FIX | `PROCESS.md:7–17` | Counts are given without saying they are at `601344e`; main now has 421 commits and 96 PRs. | Baseline stated |
| S15 | SHOULD-FIX | `NARRATIVE.md:50` | "Nothing true was dropped": the token check cannot see dropped qualifiers (S3, S4, N1). | Annotated |
| N1 | NIT | `README.md:44` | Mora & Nemenman's geometric-random-walk premise (why α = 2) was dropped. | Restored |
| N2 | NIT | `README.md:24` | "spectral slope α" undefined for a cold reader. | Defined inline |
| N3 | NIT | `LOOSE_ENDS.md:38` | Juni et al. 2016 is a static-target task. | Said so |
| N4 | NIT | `PROCESS.md:16` | Review-verdict tally is a hand count. | Marked |
| N5 | NIT | `README.md:27` | Org-theorist reading: the light-delay bullet has no firm-scale handle (decision latency, LOOSE_ENDS L3). | Not changed: putting decision latency on the README would add a claim that THEORY does not make; recommend for v1.5 |
| N6 | NIT | `tools/check_consistency.py` R3 | Rows with fewer cells than the header are flagged, and the message's advice does not fit that case. | Not changed |

## 6. What is still open

- **B1**: a whole-document hostile read by a reviewer outside this bot family, ideally a human (QUEUE WHOLE-THEORY-REVIEW). Contacting anyone needs Chad's go.
- **Kaplow §IV.C** in full, plus the legal-obsolescence and temporary-legislation literature (N53), and an organizational-economics sweep for N52 (QUEUE N52-N53-SWEEP).
- MV9 (an external timestamp account) and the lock tag (v1.5) are Chad's decisions; no account was created.
- SG-SCORE (the locked Q0 prediction) is still unscored.
