# PROCESS: what the repo's history teaches, as first principles

Wednesday 18 November 2026, late evening ET (America/New_York). Grok Bot executor for Chad Mitchell, via Ace (pt1957u). **Not independent.** The author of this file worked inside the process it describes.

## 1. Sources and the numbers they give

Everything below comes from `git log`, the 94 pull requests (`gh pr list`), the review files, `queue/LEDGER.jsonl`, the CLAIM_MAP notes and BRIEF §6, all read this session. **All counts are at `601344e`, the tree before this pass** (main now has more commits; recount with `git rev-list --count 601344e`). The commit counts, PR counts and the 62% were recomputed in the independent review (`INDEPENDENT_REVIEW.md`); rows marked † were corrected there.

| Quantity | Value | Source |
|---|---|---|
| Commits / PRs | 414 commits; 94 PRs: 93 merged, 1 closed (#16) | `git log`, `gh pr list` |
| Non-merge commits by day (ET) | 14 Nov: 4; 15 Nov: 238; 18 Nov: 40 | `git log --no-merges` |
| Non-merge commits whose subject mentions ledger, queue or pick | 176 of 282 (62%); many of these also carry a result | commit subjects (`git log --no-merges --format=%s 601344e \| grep -Eic 'ledger\|queue\|pick'`) |
| † Non-merge commits that touch **only** `queue/`, `QUEUE.md`, `STATUS.md` or `BRIEF.md` | 99 of 282 (35%) | `git show --name-only` per commit |
| Commits fixing in-file timestamps | 11 | commit subjects |
| † THEORY versions | 28 dated versions from v1.0 to v1.4.26 (counting v1.4.3a; v1.4.12 unused), on 3 calendar days (Sat 14, Sun 15 and Wed 18 November) | THEORY header |
| Review verdicts (explicit verdict lines, excluding this pass; a hand count, not reproducible from one command) | 25 "with fixes" (PASS-WITH-FIXES, READY-WITH-FIXES, "PASS with three narrow fixes"), 1 FAIL (fixable), 0 clean whole-review passes, 0 rejections | `rg -i verdict reviews/` |
| † Scored SG outcomes logged `status_changed` true | 6 of the first 11 (09:40 AM–1:45 PM ET, 15 Nov; the 11th, entry 61, added N18); 0 of the remaining 37 (2:53–8:19 PM ET, 15 Nov). Of those 37, none changed an existing row's status; three added a new row (N21, N22, N23), which the 15 Nov ruling in QUEUE rule 3d counts as a change (only entry 171 was re-read that way). "Scored" = protocol-2 outcome not marked `scored: false` | `queue/LEDGER.jsonl`, CLAIM_MAP v2.12–v2.37 notes |
| Valid Tier-1 field tests run | 0 | CLAIM_MAP, FRAMEWORK |
| Agent-memory beliefs the files contradicted | 10 | BRIEF §6 |

## 2. The error types that recurred, and what caught them

From the WITHDRAWN and MATH-CORRECTED rows, the review files and the corrections recorded in the changelogs:

| # | Error type | Examples | Caught by |
|---|---|---|---|
| E1 | **Universal overstatement** ("iff", "every", "always", "only where", "≥ 2") | D3, F9, F11, K12 ("iff scale-free"), E5 (V ≥ 2), K18, F5, J1, J8, B10; the T7 "only where/if scale-free" wording still in BOOKENDS and REACH until this pass (LOCK_AUDIT S4) | Independent referees (most); this audit |
| E2 | **Novelty overclaim, later credited** | K13 headline, N11, N38, the SG clock, most of the spectrum map | Prior-art sweeps |
| E3 | **Misread or miscited source** | C3 (Alonso et al. 2008), J12, J13; cosmic web "no hubs" (a random-points number read as the web's); Laughlin 10⁵ vs 10⁴; England 2013 vs 2015 | Referees who opened the source |
| E4 | **Proxy that does not measure the quantity** | MATCH1 (need hazard vs a recall curve), D3 redness sign (H19), SENSE-CELL (N24), F1 τ (operating leverage), measles (μ, not q), DRIFT1 (event rates, not q) | The measurement framework (FRAMEWORK, MV gates) |
| E5 | **A rule changed after seeing data** | glucose sampling-corrected targets; the torus toy test ruled INVALID after its result | Locked preregs read literally; referees |
| E6 | **Independence mislabelled** | reach REVIEW.md called independent (fixed in v1.4.24); `theory/SCALE_ENDS.md:5` still called a same-executor pass "independent" until **this pass**, caught by the new checker rule R1 | Independent review 1; checker R1 |
| E7 | **Answering from memory** | the ten rows of BRIEF §6 (Theorem G vs T8, the gates, Laughlin, England, the black-hole time, the stale "silent on black holes", ANTS1, measles) | Reading the files (BRIEF audit) |
| E8 | **Stale pointers, counts, dates and statuses** | version pointers, FRAMEWORK paths, the 167-row count table, C3b "unfinished", unescaped table pipes that hid 99 LITMAP verdicts; **this pass itself** dated its files "19 November, early morning" from a stale sense of the time and merged them at 10:57 PM ET on 18 November (fixed in a follow-up PR) | The checker (versions); this audit (the rest) |
| E9 | **Scope framed wrong, in both directions** | under: "silent on black holes"; over: "the virus redefines life", "time is fractal" (N46 WITHDRAWN) | Chad (under); referees and labels (over) |
| E10 | **Numerical slips** | the black-hole time stated without its (M/M☉)³ scaling; effort units erratum; store coefficient c | Referees re-deriving numbers |

**The pattern.**
- Errors that make claims **bigger** (E1, E2, E9 over) were the most common, and were caught only by someone other than the author.
- Errors that make the record **inconsistent** (E6, E7, E8) were caught cheaply, by machines and by re-reading files, whenever someone looked.
- Errors that make tests **say the wrong thing** (E4, E5) were caught by rules written in advance (the measurement framework, preregistration).

## 3. What paid off, and what was wasted

**Paid off:**
1. **Preregistration read literally.** Locked kill rules and the anti-rescue rule stopped every post-hoc rescue that was attempted (E5).
2. **The measurement framework.** Relabelling "killed" as PROXY-FAIL, with the failed gate named, made every field result honest. It is the single biggest credibility asset in the repo.
3. **Independent referees before merge.** Every review with an explicit verdict (about 26) found something to fix, and the one FAIL (BOOKENDS math) was fixed before merge.
4. **Credit-first prior-art sweeps.** Each demoted a novelty claim. Each also made the remaining claims believable to an expert.
5. **One canonical file plus a mutation-tested checker.** Cheap, and it caught real errors, including one this pass (E6).

**Wasted or low-yield:**
1. **Bookkeeping.** 62% of non-merge commits mention the ledger, queue or a pick in their subject, and 35% touch nothing but queue and status files. The SG ranking protocol consumed much of that, yet its own locked prediction (N9) was never scored, and the scorer crashes on ledger entry 156 because one field was renamed (`claim_map_status_changed`). An exploratory scoring in scratch, not a verdict, gives INCONCLUSIVE under the locked rule either way (QUEUE SG-SCORE).
2. **Version churn.** 28 THEORY versions, many of them wording-only, each forcing pointer bumps across five files. It is the main source of E8.
3. **Underpowered tests run before the power gate existed.** ONA-MORE, SPF-RIGIDITY and C3b. MV10 was written after them.
4. **Reach work.** Cosmic web, wormholes and torus produced 15 rows, mostly PRIOR ART, CONDITIONAL, OPEN or WITHDRAWN. None moves the core bet. They answer Chad's scope, which is binding, and they were worth one careful pass. The marginal pass was not.
5. **Simulations that pass by construction** (POOLSIM). They cost a review each and are NOT EVIDENCE.

**Missed entirely:**
1. No Tier-1 test has ever run. The binding constraint (measuring stakes, N13) was named on 15 November, and no data acquisition has started since.
2. No human expert has read any part of the theory.
3. No review has covered THEORY.md as a whole.
4. Externally timestamped preregistration (MV9) still waits on Chad's go-ahead for an outside account. Until then no test can reach Tier 1, so this one procedural decision blocks the science.

## 4. First principles (causal, not descriptive)

| # | Principle | Evidence | Rule it implies |
|---|---|---|---|
| P1 | **Claims drift toward their strongest phrasing; only an outside reader pulls them back.** The pull is strongest on quantifiers. | E1 is the largest class; all of it was caught by others | Any new "iff / only / every / always / never" must cite a proof of both directions or name the counterexample search. **Judgment rule** (no regex can tell a proved "iff" from an overclaim). |
| P2 | **Novelty is the most perishable label.** | Every swept "new" claim lost ground (E2) | Default novelty label is "not found in a search of X on date D"; "new" needs a dated sweep. **Judgment rule.** |
| P3 | **A proxy tests the mapping, not the theory.** | E4 | Already binding: MV1–MV10. |
| P4 | **An author cannot certify its own work, and same-family reviewers are second readers, not blind graders.** | E6; B1 | **Checker R1:** no self-review called independent. Lock needs one reviewer outside the bot family. |
| P5 | **Memory is a cache; the files are the record.** | E7 (ten corrections) | Already QUEUE rule 1 (read at use). |
| P6 | **Derived numbers rot unless a machine recomputes them.** | E8: counts, pointers, pipes | **Checker R2** (CLAIM_MAP tally), **R3** (table cells), **R5** (stale "private") plus the existing version checks. |
| P7 | **Process overhead grows to fill the budget unless capped.** | 35% of commits pure bookkeeping (62% mention it); SG never scored | Fold ledger and queue edits into the result PR; cap process-only commits at about a quarter. Score a locked process bet when its trigger is reached, or withdraw it. **Judgment rule.** |
| P8 | **Breadth is cheap to produce and expensive to verify, and it does not move the bet.** | Reach rows | Every new area names the core row (N13, J6, J9, J16) it could move; if none, one note and stop. **Judgment rule.** |
| P9 | **Rules written after the data are rescue.** | E5 | Already binding (prereg, anti-rescue). |
| P10 | **The bottleneck is measurement, not mathematics.** | 0 Tier-1 tests in 94 PRs; no existing row changed status in the 37 scored outcomes after the first 11 | Freeze the text (lock) and move the effort to data: SAME-SYSTEM-AQN, N51 (LOOSE_ENDS L1) and the MV9 decision. |
| P11 | **Words that name a GTAO claim "law" invite the overclaim the project has banned.** | S10 (√N "law" in four maintained files) | **Checker R4.** |

**The theory applied to itself (P10, heuristic only).** By Theorem G, a checked copy is worth keeping current only while drift × check cost is below the copy's value; past the freeze edge, freeze it. The canonical text's measured "drift" fell from 6 status-changing outcomes in the first 11 to none in the remaining 37 (three only added rows). That argues for freezing now.

**Limits of that count:**
- `status_changed` is a narrow outcome measure: premise tightenings and gates mattered without changing a status.
- The later items were chosen by a ranking that favoured reviews.
- So the count is suggestive, not a measurement.

## 5. Rules added to the checker (all mutation-tested)

| Rule | What fails | Test mutation | Error type |
|---|---|---|---|
| R1 | A maintained doc calls a review independent when its own header says it is not | BRIEF: "The independent review `reviews/reach_2026-11-18/REVIEW.md` passed." | E6 |
| R2 | The CLAIM_MAP current tally differs from the rows (all sections A–N) | Total changed to a wrong number | E8 |
| R3 | A table row's cell count differs from its header's (an unescaped pipe drops a cell on GitHub) | A three-cell row under a two-cell header | E8 |
| R4 | A named GTAO relation is called a "law" (√N, trail-fade, shared-memory, read-rate, freeze-or-hold, three-cost) | "Colonies follow the √N law." | E1/E9; J3 |
| R5 | The repository is called private in the present tense | "The repository is private." | E8 |

The first run of R1 found a real error, `theory/SCALE_ENDS.md:5`, fixed in this PR. R2 and R3 found no remaining errors, because this pass had already fixed them by hand.

**Not checkable, so kept as judgment:** P1 (overstated "iff"), P2 (novelty), P7 (overhead cap) and P8 (breadth). They belong in reviewer checklists, not in regexes. A regex for "iff" would flag every proved one.

## 6. Recommendations, in order

1. **Get one whole-document hostile read** from a reviewer outside this bot family, ideally a human with a background in control or information economics. This is the remaining lock condition (LOCK_AUDIT B1).
2. **Decide MV9.** Whether to create an outside timestamping account (OSF or Zenodo) for preregistrations is Chad's call; no account was created in this pass. Without it, no test can reach Tier 1.
3. **Lock at v1.5:** tag it, and from then on change THEORY only for errors (with an erratum) or for status changes driven by tests.
4. **Spend the next effort on data:** SAME-SYSTEM-AQN, or the N51 lab test, which is the cheapest valid test in reach.
5. **Score or withdraw N9 (SG).** Fix the field-name crash in a reviewed PR first.
