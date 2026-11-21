# Independent hostile review: PR #132 (night record 20–21 Nov 2026 and T30)

**Reviewer:** independent (wrote none of `history/2026-11-21_NIGHT.md`, the OPEN_WORK T30 row, or the as-of / §8 edits in this PR). Same bot family as the author executor, and later the same night; not a blind second executor. The verdict rests on the checks below, not on the author's summary.
**Date:** Saturday 21 November 2026, started about 5:05 AM ET, finished about 5:20 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/132
**Clone:** fresh `/tmp/gtao-rev132` (not the author workdir), `pull/132/head` at `3fdbf232cffe9d69b5975a8e7e7cbc68cac07322`, merge-base equals `origin/main` `c035ab2e9a10cb56629816e099a9ce05c199fcc8`. Clean tree at review start. Nothing pushed or merged by this review until the verdict is written. `/workspace/looper` and `/workspace/gtao-evo` were not touched.

**Verdict: READY**

The PR is docs-only. It is a short plain record of already-merged PRs #121–#131, plus an unlocked OPEN_WORK row (T30) for a candidate next path. It is not a lock, not a prereg, and not a re-score. Every merge SHA and merge time in the record matches `git log` on `main`. The official results, review/confirm labels, and the numerical claims that were checked all match the merged files. The four DOIs in the record re-verify on the Crossref API this session. `CORE.md` is byte-identical to `origin/main`. The law-of-adaptive-organization hypothesis sentence is unchanged. The T30 assessment greps first, credits EVO1 and T7, and does not overclaim what the opened Avida PDF or the opened lab-paper abstracts can establish.

Nits below are not should-fixes and do not block a merge.

---

## What was checked

- Fresh clone at the stated head; `git merge-base` equals `origin/main` `c035ab2`; `git diff --stat origin/main...HEAD` is two files only: `history/2026-11-21_NIGHT.md` (new) and `OPEN_WORK.md` (header, T30, §8 pointer). One commit, author Chad Mitchell `<chad39@gmail.com>`.
- `CORE.md`, `THEORY.md`, and `README.md` are each byte-identical to `origin/main`. `CORE.md` SHA-256 is `aee235cb2a9b7d46a0e82c97825984eb3f5dcb160bdd283c90df552616284a7a`. The hypothesis sentence is the same string in each: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."
- All eleven full merge SHAs in the night-record table were compared to `git log --merges` on `main`, including committer times converted to America/New_York (UTC−5). All eleven match, including that #124 merged (12:55:13 AM) before #123 (1:03:31 AM).
- Official results were re-read in the merged files: `core/keystone_checks/waterfill_2026-11-20/RESULTS.md`; `core/bridge_2026-11-21/RESULTS.md` and `DEVIATIONS_2026-11-21.md`; `theory/measured/ecoli/MEASURE_RESULT_2026-11-21.md` and `DEVIATIONS_2026-11-21.md`; `theory/measured/ecoli/QUALIFICATION_2026-11-21.md`; `core/sim1_2026-11-21/RESULTS.md`; `theory/measured/grid_cross_2026-11-21/RESULTS.md`; `formal/lean/README.md`; `theory/VIS1F_DROP_2026-11-21.md`; `theory/PRICE_FREE_2026-11-21.md`; `theory/DISCRIMINATING_CANDIDATES_2026-11-21.md`.
- Review and confirm verdicts for PRs #121–#131 were read from the first `**Verdict:**` line of each file under `reviews/wf_2026-11-20/`, `thermo_2026-11-21/`, `ecoli_qual_2026-11-21/`, `lean_2026-11-21/`, `sim1_2026-11-21/` (including `CONFIRM2.md`), `ecoli_measure_2026-11-21/`, `grid_cross_2026-11-21/`, `discrim_2026-11-21/`, `vis1f_2026-11-21/`, and `pricefree_2026-11-21/`.
- `git grep` on `origin/main` for Avida, Ofria & Wilke, and doi `10.1162/106454604773563612` returned no hits. EVO1 (W2) and T7 are already in `OPEN_WORK.md` and are credited in the record.
- DOIs `10.1162/106454604773563612`, `10.1038/nature03842`, `10.1534/genetics.107.085399`, and `10.1126/science.1154456` queried on `https://api.crossref.org/works/{doi}` this session.
- The CaltechAUTHORS PDF of Ofria & Wilke 2004, already fetched this night (`OFRal04.pdf`, 205,948 bytes), was re-hashed: SHA-256 `ae0e395b3156154d6f6aa7b57d72953b5195b6caadfe0500be28186336af9bbc`, matching the record. The Avida environment / merit / experimenter-control claims were checked against the extracted text of that PDF (sections 3.3, 3.4, and 4).
- `python3 tools/check_open_work.py` and `python3 tools/check_consistency.py` were already run on the author head (PASS, 0 FAIL). This review did not re-run `pytest tools/` (146 passed on the author head; this PR adds no tests).

---

## SHA and time check

All eleven table rows match `git log` exactly.

| PR | Record SHA | `git log` SHA | Record time (ET) | `git log` `%cI` |
|---|---|---|---|---|
| #121 | `4398bbdc434b766d4b761aa86d8b8836b0ef8c4c` | same | Sat 21 Nov 2026, 12:04:05 AM | 2026-11-21T00:04:05-05:00 |
| #122 | `17277348dd0f3492489400fca3c76c8e9bd46e43` | same | 12:39:16 AM | 2026-11-21T00:39:16-05:00 |
| #124 | `d63ac233b3e7fb3622732303dae2adb2200615ed` | same | 12:55:13 AM | 2026-11-21T00:55:13-05:00 |
| #123 | `fba28278a1cbd82431451f3417e6279a0516530b` | same | 1:03:31 AM | 2026-11-21T01:03:31-05:00 |
| #125 | `75b58fec282c102efa31b57477301636c6f551fb` | same | 1:27:16 AM | 2026-11-21T01:27:16-05:00 |
| #126 | `54a45629280edc9dfe0275d04eaf19626aa4523d` | same | 1:39:44 AM | 2026-11-21T01:39:44-05:00 |
| #127 | `ac079ea0b2724cec34f30d83e3b3c551c6877c07` | same | 2:22:57 AM | 2026-11-21T02:22:57-05:00 |
| #128 | `ecf6e77172797585bf199e184bf19997455bd094` | same | 2:34:20 AM | 2026-11-21T02:34:20-05:00 |
| #129 | `e2bfc2ba730cee102c612ed8da20bfde0a1aafc3` | same | 3:24:46 AM | 2026-11-21T03:24:46-05:00 |
| #130 | `d42220dff45e11cf238b58faa3cd016e4c7a536c` | same | 3:58:45 AM | 2026-11-21T03:58:45-05:00 |
| #131 | `c035ab2e9a10cb56629816e099a9ce05c199fcc8` | same | 4:41:05 AM | 2026-11-21T04:41:05-05:00 |

---

## Result and review-label check

- **#121 / T25.** Official PRIMARY Model S 1882/6440 = 29.22% and rhythmic+mixed 87/264 = 32.95%, HOLE 70/70, overall fail, no rescue: match `RESULTS.md`. Independent review READY-WITH-FIXES, confirm READY: match.
- **#122 / T27.** Official FAIL, P1 and P2 passed 3/3, P3 failed 0/3, no rescue: match. The ill-posed-gate lesson, including the pilot Boltzmann masses 0.908 / 0.090 at β = 0.5 under the locked 0.10 floor, is in `RESULTS.md` and is correctly labelled as not a rescue. The mid-run library rewrite and the standing hash-lock rule are in `DEVIATIONS_2026-11-21.md`. Reviews match.
- **#124.** Qualification literature check, overall NOT ESTABLISHED, not a re-score: match. Reviews match. Merged before #123, as the record says.
- **#123 / T19.** PARTIAL Lean formalization, no `sorry` / `admit` / `axiom` / `native_decide` / `unsafe` / `implemented_by` in project sources, and the named fragments (CT20 layer bound, CT10, CT4 first-bit in right-slope form) are in `formal/lean/README.md`. The record correctly says formalization cannot establish the CORE §3 hypothesis. Reviews match.
- **#125 / T28.** Official PASSED, P1–P4 3/3; P1–P3 are implementation-and-box checks of theorems; P1 and P3 could not have failed under the stated model; P4 is the only numerical test: match `RESULTS.md`. Independent review READY-WITH-FIXES; same-session confirm READY, disclosed; #126 CONFIRM2 CONFIRMED: match.
- **#126.** Blind confirm of #125 plus residual tidy (OPEN_WORK, `test_lean.py`, litmap, reviews README, a stale note in the E. coli qualification file): matches the merge commit contents. No new official score, as stated.
- **#127.** Overall NOT ESTABLISHED; *N_e* ESTABLISHED at conservative 1.7960 × 10^8 (Sung et al. 2016); σ, ε, power, and *T_red* NOT ESTABLISHED; P1/P3 cannot exclude R3 because τ_v = 1.160 s lies in the locked Arm B τ* box [1.093, 1.171] s; no re-score: match. Reviews match.
- **#128.** Official comparison not run; P25 still UNTESTED; underpowered bars −0.80 / −0.66 / −0.52 at n = 5, 6, 8, locked thresholds not relaxed; dated pre-data typo deviation: match `RESULTS.md` / `DEVIATIONS_2026-11-21.md`. Reviews match, including the confirm's judgment that the deviation was a legitimate pre-data correction and not moving the goalposts.
- **#129–#131.** Unlocked shortlist, VIS-1F drop under the written pre-Pass-1 rule, and price-free classification: match the merged notes. The PRICE_FREE distinctive remainder (comparative static in *w* of *S* + *w E* when ruin binds, after Stephens / Caraco / Dall & Johnstone are credited; 1/α when α ≠ 2; onset exponent set by sensing technology, not by α) matches `theory/PRICE_FREE_2026-11-21.md` §2 and §4 after the S1–S2 fixes. Reviews match.

The bottleneck section is grounded in `OPEN_WORK.md` §8, `PRICE_FREE`, and `STATUS.md`'s sentence that stakes *w* have never been measured validly, and it does not overstate those files.

---

## T30 / DOI check

Crossref this session:

- `10.1162/106454604773563612` — 2004, Ofria, Wilke, *Artificial Life* 10:191–229. Matches the record.
- `10.1038/nature03842` — 2005, Dekel, Alon, *Nature* 436:588–592. Matches.
- `10.1534/genetics.107.085399` — 2008, Stoebel, Dean, Dykhuizen, *Genetics* 178:1653–1660. Matches. (An often-typed neighbouring DOI, `10.1534/genetics.108.089847`, is not a Crossref work and is not used here.)
- `10.1126/science.1154456` — 2008, Tagkopoulos, Liu, Tavazoie, *Science* 320:1313–1317. Matches, and is correctly used only as a DOI that was opened at abstract level and then set aside, already being in `litmap/`.

The Avida claims in the record stay inside the opened PDF: experimenter-set population size, mutation rates, instruction set, and an environment of resources and reactions with merit effects; merit as CPU speed; competition for space. The record does not invent a closed-form fitness equation that the paper does not state.

The lab-paper claims stay inside the opened official abstracts, and the record says plainly that the full texts were blocked. Dekel & Alon is not treated as a ready-made test of GTAO (*h*, *w*). Stoebel is not treated as an evolution-to-optimum study. What such a test can and cannot establish is stated at the right scope: in-model or lab conditions under known prices, not the law in the wild; not a replacement for T7 or EVO1.

T30 is a fair new OPEN_WORK row. It is not a lock.

---

## Nits (not should-fixes)

1. OPEN_WORK T29's "Where" column still names branch `vis1f-2026-11-21` after PR #130 has merged. That pointer was already stale on `main` and is not a false claim in the night record. It can be tidied later.
2. The T25 official results *table* labels the failed gates **FAIL**; the record, like OPEN_WORK, says **FAILED**. The numbers are the same.
3. This review is same-family and later the same night as the author pass, on a fresh clone. That is disclosed. It is not a blind confirm by a second executor.

---

## Merge recommendation

Docs-only, accurate on the checks above, `CORE.md` and the law sentence unchanged. Ready to merge with a merge commit, after this review is committed to the branch.
