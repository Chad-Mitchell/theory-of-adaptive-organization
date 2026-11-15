# MEASURE-SELF results: A Theory of Adaptive Organization applied to Ace's own memory

Run 2026-11-15, ~8:15–8:45 AM ET. Prereg locked and committed before any outcome was computed:
private repo `Chad-Mitchell/theory-of-adaptive-organization`, branch `night2-self-prereg`, commit `4a651d0`
(2026-11-15 08:15:33 −05:00), file `reviews/night2/SELF/PREREG.md` (copy: `PREREG.md` here).
Code: `analyze.py` (locked tests), `explore_postlock.py`, `explore_backoff.py` (POST-LOCK, exploratory), `p5_code.py` (exploratory, unblinded).
Raw outputs: `results.json`, `explore_postlock.json`, `explore_backoff.json`, `p5.json`.
**Status: not yet blind-refereed (QUEUE item 6).** Aggregate statistics only; no personal content.

## Data and n
- Looper store journal: 98 items (meta-log excluded), 264 versions, 16 Ace-initiated, 102 change events after merging same-message parts, 1,445 item-days, Oct 16 – Nov 15. Median drift 0.105 changes/day (≈ one change per 9.5 days). Stakes tiers (keyword rule): 21 high / 64 mid / 13 low.
- Morning-return routine: 5 runs (Nov 11–15), 34 surfacings of 12 distinct items.
- Documented misses: 56 `mistake`/`correction` records in the archived raw log (Oct 24 – Nov 5); 52 are misses.
- Looper git history: 1,201 commits (all branches).
- Not available: Grok Bot transcripts (search returned no readable record from this run), so context-loss (summary) events and re-asked questions could only be counted through the miss log, not directly.

## Locked results

| # | Prediction (GTAO source) | Result | Key numbers | n | Measurement validity |
|---|---|---|---|---|---|
| P1 | Item change is bursty, not one steady pace (§2 regime B) | **PASS** | median within-item CV of gaps 0.82 vs Poisson null median 0.61, 95% band 0.45–0.76; p = 0.002 | 24 items with ≥3 events | PARTIAL: change = when Chad told Ace (push), not when the world changed |
| P1b | Chance of change falls with time since last change, slope in [−1.0, −0.5] (MATCH1 band) | **INCONCLUSIVE** | slope −0.39, 95% CI −0.63 to −0.10 (decreasing, but weaker than the band; CI overlaps it) | 1,454 item-days, 80 events | PARTIAL; pooled across items, so between-item differences push the slope more negative (bias toward the band) |
| P2 | Ace's attention ∝ drift^½ × stakes^½ (read-frequency result, class R) | **INCONCLUSIVE** | drift elasticity 0.30 (CI −0.01 to 0.60); stakes 2.0 (CI 0.6 to 6.2). **Deadline rival wins decisively**: AIC deadline 60.6 vs GTAO 150.8, GTAO+deadline 62.0, recency 154.5, uniform 167.3. Items with a window in the week were surfaced 2.75 times on average vs 0.017 for the rest | 71 items, 5 runs | Attention VALID (exact log); stakes PROXY (keyword rule); low power |
| P3a | Drift is a stable property of an item (precondition for any drift-based schedule) | **FAIL** | Spearman ρ between Oct 16–31 and Nov 1–15 change rates = −0.06 (CI −0.36 to 0.26) | 42 items, 36 later events | PARTIAL (statement times) |
| P3b | Checking ∝ √(drift × stakes) beats uniform and rivals out of sample (equal budget) | **FAIL** | stakes-weighted staleness lag: GTAO/uniform = 1.20 (CI 1.01–1.37), i.e. 20% *worse*; stakes-only/uniform ≈ 0.96 (best); GTAO beats linear (0.65) and recency (0.51). Same at 3- and 14-day budgets (3-day CI lower bound 1.00) | 42 items | PARTIAL: a counterfactual pull policy; Ace mostly learns by push |
| P4a | Closed items are effectively frozen (T8 freeze edge) | **PASS** | 0 of 21 done/cancelled items changed again (95% CI 0–15.5%) | 21 | VALID |
| P4b | Frozen history is cheap and occasionally needed (R4/T8 keep-all) | descriptive | 15 reverts/restores in 1,201 commits (1.25 per 100) | 1,201 | VALID |

## Exploratory (unblinded or POST-LOCK; no pass/fail)
- **P5 miss mechanisms** (unblinded: I had read the miss texts before locking). Of 52 misses: stale working copy S 16, tooling/code bug T 12, judgment/inference J 12, never written N 4, return/routing R 4, promise without edit P 2, context loss C 2. Memory-caused (S, N, C, R, P) = 28; **S + C = 18 of 28 (64%, Wilson CI 46–79%)**, 35% of all misses. Second coder (keyword rule, also written by me after reading, so not independent) agreed 82%, κ = 0.78; it gives S + C = 14 of 49.
  - Nearly every S miss is one of two kinds: (a) acting or asking from what Ace believed without rereading a source that cost seconds to read (re-asking Chad about items the log had closed, rewriting a note from memory, saying it couldn't do something it could); (b) a derived copy (doc, diagram, routine, page) not updated after its source changed. These are the theory's R5 "copy error grows with hops and staleness" and T8's lookup edge: when reading is nearly free, the theory says read at the moment of use. **The policy was right; doing it was what failed.**
- **E1:** changes do *not* cluster near an item's window (36.7% within 2 days of the window vs 38.9% expected by time share). The bursts come from conversation, not deadlines.
- **E2 (POST-LOCK):** a regime-B schedule (check soon after each change, then back off geometrically) also **lost** to uniform: 1.43× worse at the 7-day budget, 1.13–1.79× across budgets. Most later changes were dormant items coming back to life, which no item-history schedule predicts.
- **E3:** write ratio. 271 journal versions against 2,950 recorded discards, almost all bookkeeping or historical excerpts. No restatement data exists, so the write rule (R2) can't be validated.

## What this says about the theory (honest read)
1. **Supported here:** the drift is bursty (P1). Closed items freeze (P4a). The theory's lookup edge (T8: read at use when reading is cheap) and copy-hops rule (R5) explain the largest single block of documented memory misses (exploratory).
2. **Not supported here:** the √-law allocation. It needs drift to be a stable, predictable property of an item, and in this environment it isn't (P3a). Out of sample, √(drift × stakes) checking did worse than uniform. Ace's actual attention follows deadlines, not drift. As locked, P3b is a FAIL. One reconciliation is that the √ law is a regime-A (single-pace) prediction while P1 says this environment is regime B, but that is post-hoc. The regime-B schedule I tried also lost.
3. **What this test can't separate:** Ace built Looper from GTAO-derived rules and wrote this test. A "pass" on attention would only show that Ace follows its own rule. The miss coding is unblinded. Drift is measured from what Chad chose to tell, so it partly measures Chad's conversation, not the world.
4. **On Chad's anecdote of better-than-baseline performance:** there is no valid baseline in these data. The miss log stopped at the Nov 9 migration, and the new store has no outcome or miss log, so the miss rate before and after the GTAO-derived redesign can't be compared. That comparison is the thing worth instrumenting (below).

## Design recommendations for Ace's memory (derived; each with a measurable target)
1. **Hard read-at-use gate (T8 lookup edge, R5).** Before asserting stored state, asking Chad anything, or saying "I can't", run `looper.py show`/grep the log and check tools. Make it a code step in the operating loop, not a habit. Target: S-type misses, 16 of 52 (31%) of documented misses. At 90% compliance, expect ≈ 28% fewer documented misses. Measure re-asked questions and "without checking" misses per week.
2. **Hold no derived copies (R5 hops).** Docs, diagrams, routines and pages reference ids and are generated on read, never pasted text. This is already the post-Nov-9 design for routines. Extend it to STATE.md-style summaries by stamping each with its source commit and `as of` time, and rereading the source when the stamp is older than the source's last change. Target: the ≈ 7 copy-propagation misses (≈ 13%).
3. **Freeze closed items (P4a).** Leave done/cancelled items out of sweeps and the default `show` (keep them recoverable). 0 of 21 ever changed, so this saves read cost as the store grows at no measured risk. Keep every git version: restores happen about 1.25 times per 100 commits, and storage is about free.
4. **Pull checks: uniform in time, weighted by stakes, triggered by deadlines.** Don't schedule by estimated drift (P3a/P3b). Keep the deadline-driven morning return (it matches the winning rival) and add a stakes floor: every high-stakes open item gets surfaced or confirmed at least weekly. Expected benefit vs uniform is about 4% lower stakes-weighted staleness lag (counterfactual, CI not computed). It's small. The big lever is item 1.
5. **Handle bursts (P1).** When Chad touches a topic, reread that topic's items and related ones in the same turn, and expect follow-ups for a few days. The chance of a change the day after a change is about 2.1× the chance after a quiet week (slope −0.39). Don't add a back-off schedule (E2 lost).
6. **Instrument what's missing (the measurement-validity gap).** (a) `outcomes.jsonl`: one line per return with item id, used/ignored/late. Today the Saints-vs-house clash has been surfaced 4 times with no recorded outcome. (b) A miss record type with a mechanism code (S/N/C/R/P/J/T), as the old log had. (c) A read log: which items each judgment read. Without (c), read frequency per item can't be measured, and prediction 1 can only be tested through the morning return. These three give a valid before/after test of whether the GTAO-derived design beats baseline, and that is the honest version of Chad's anecdote.

## Limitations
Small n (5 attention runs, 24–71 items, 52 misses). Self-selection (Ace designed the system and the test). Stakes is a keyword proxy with no independent rating. Drift comes from push statements. The migration rebuilt the journal from the raw log on Nov 9, so version timing before then reflects statement times as reconstructed. Transcripts weren't available, so context-loss events weren't counted directly. P5 and the E analyses are exploratory. Nothing here is evidence about adaptive organizations in general. It's evidence about one assistant's memory over one month.
