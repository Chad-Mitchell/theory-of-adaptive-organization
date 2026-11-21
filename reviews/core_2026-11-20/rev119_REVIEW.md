# Independent hostile review: PR #119 (one-page core and keystone checks)

**Reviewer:** independent (wrote none of the PR, CORE.md, keystone note, checks, prereg, results, OPEN_WORK edits, recovered reviews, or `reviews/rhythm_2026-11-20/REVIEW.md`).
**Date:** Friday 20 November 2026, started 9:12 PM ET, finished 9:25 PM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/119
**Clone:** fresh `/workspace/rev119` at head `aa6ab2925b83b17390ac669426a0eb556a9930a7`, base `ff14a87cb2dcc267b954eaf87e25859f0de31797` (merge-base equals base). Detached HEAD, clean tree. Nothing pushed or merged. `/workspace/looper` was not touched. Compute at nice 19.

**Verdict: READY-WITH-FIXES**

CORE.md’s load-bearing claims match the stored evidence. Official IMP-N60 / cymatics / fractal gates recompute from the locked predictions and stored designs. The keystone is scoped to Model S with numerical convexity; IMP-N60 is left failed; the fractal miss is in-model only. Checkers and `pytest tools/` pass. Nothing was dropped from OPEN_WORK relative to main’s queue. One official writeup number is wrong and must be corrected; several pointer and typo issues should be fixed in the same pass. None of those flip a gate or the CORE status sentence.

---

## What was checked

- Fresh clone at the stated head/base; diff `ff14a87..aa6ab29`; CORE.md, `core/KEYSTONE_NOTE.md`, `core/keystone_checks/*`, `reviews/rhythm_2026-11-20/REVIEW.md`, OPEN_WORK.md, README.md, `tools/check_consistency.py`, and `reviews/recovered/`.
- Independent rescore of headline numbers from `rhythm_im_run.json`, `imp_n60_predictions.json`, `s5_rerun.json`, and `rhythm_rule.json` (no new inclusion rule, no optimizer rerun of the full library).
- SHA-256 of the locked prereg and predictions files against the hashes recorded in those files, the results, the deviations, the keystone note, and the prior rhythm review.
- OPEN_WORK table IDs and §7 tokens against base `ff14a87`; `process/queue/items.json` and `process/QUEUE.md` unchanged; `python3 tools/check_open_work.py`.
- Wording: “law” / “theory of everything” / “bill”; Looper and private paths; CORE claims vs evidence (Model S scope, IMP-N60 fail, fractal fail in-model only).
- `python3 tools/check_consistency.py` and `python3 -m pytest tools/ -q`.

There is no `OPEN_WORK/QUEUE/items.json` on main or on this head. The live equivalents are `OPEN_WORK.md` plus frozen `process/queue/items.json`.

---

## Integrity

- `RHYTHM_PREREG.md` SHA-256 `e0b4f2b6f31743fdffe05f0f3eeedfb3d169824136a5671bfdce28ee11fd50ce`. Matches the file on disk and every recorded citation (results, deviations, run JSON, predictions file, KEYSTONE_NOTE §5, prior review).
- `imp_n60_predictions.json` SHA-256 `b625a8ad57c3d861d5f0202b36125c4fa405b34260b9c46fdf72a9279d135bb3`. Matches the file on disk and every recorded citation. Written 6:22:45 PM ET; official start 6:22:50 PM ET; locked note is poles, variances, N, R only.
- A brief that cites `b625a8ad…` as the prereg hash is mixing the two files. The prereg is `e0b4f2b6…`. Both files are unedited relative to the hashes recorded with the run.
- CLAIM_MAP is unchanged (v2.68; 318 rows). Consistency checker PASS (0 FAILs; existing soft length warnings on THEORY.md and README.md). Open-work checker PASS: 62 items.json not-DONE + QUEUE.md not-DONE, union missing from OPEN_WORK.md = 0.
- `pytest tools/`: **125 passed** in 260 s. The “125 tests” tally in CORE.md and OPEN_WORK.md is correct (main’s OPEN_WORK header still said 118; this PR’s count matches the suite).
- D1–D4 are process/numerical-guard deviations dated during the run. D5 is post-data and discloses runner scoring bugs rather than changing the rule. Official Model-S numbers are the independent rescore, as claimed, and they recompute.

---

## CORE.md claims vs evidence

CORE §4 and the matching paragraphs in KEYSTONE_NOTE §1–§5 and OPEN_WORK W9/T18 are consistent with the stored runs and with `reviews/rhythm_2026-11-20/REVIEW.md` (SCORING CORRECT), except for the first-order J typo treated as B1 below (that typo is not repeated in CORE.md or the keystone status table).

Independent rescore (this review):

| Claim | Stored / official | This rescore | Status |
|---|---|---|---|
| Model S convexity, merged solver, 120 worlds | 120/120 at 10⁻⁴ and 10⁻⁶, also K=0..J; no E below E_∞ | same, from `s5_rerun.json` | holds, numerical only |
| N60-as-written vs argmin, argmin ≥ 1 | 18,941/18,941 | 18,941/19,320 total, 379 holes, 0 other misses | holds |
| K*=0 hole | 379/19,320, 39 worlds, R ≤ 1.41 | 379 holes, 39 worlds, R ∈ [0.10, 1.4125] | holds |
| Rhythm increment formula false | two oscillators, R=3, formula 2 vs argmin 3 | first-order J = (7.376, 7.839, **7.105**, 7.428), argmin 3 | holds |
| IMP-N60 PRIMARY | 58/189 cost, 51/189 composition | **58/189 cost, 51/189 composition** (7 cost-only: 3 on `seed2_two_light`, 4 on `1osc_z0.25_N0.04`) | holds, FAIL |
| MUST | predicted C*=4, argmin C*=3, hybrid J=6.2486, E=0.041022 | same; tag `nr1_nf1`; two-resonator J=7.006 | holds, FAIL |
| SANITY | 7/8; kill on `1osc_z1.0_N0.04`, ε=1.086×10⁻³ | 7/8, ε=1.086430×10⁻³ | holds, FAIL |
| Model-S regression | IMP-N60 5,890/19,320 = 30.5%; N60-from-0 19,320/19,320 | **5,890/19,320 = 30.4865%**; N60-from-0 19,320; C*=0 in all 379 holes and in 160 cells with argmin ≥ 1; over-includes 13,264; other under-includes 6 | holds, FAIL |
| Cymatics locking | median-of-medians 0.03986 < 0.05; 3/7 light worlds miss individually | 0.039859; misses: `1osc_z0.08_N0.04` 0.213, `2osc_close2_light_light` 0.094, `2osc_sep15_light_light` 0.236 | holds, aggregate PASS |
| Cymatics jumps | stakes 2/41, C=1→3→4; frequency 1/31, C=2→3; no chatter | same; jump indices isolated | holds, PASS; CT41 link correctly called a loose analogy only |
| Fractal / holographic | (1) 3/24 primary cells at R=100,300; (2) α=1 CVs 0.996–1.984; (3) 90/90; in-model at N=0.05 | (1) **3/24**, only Γ=10, J=2, R=300; (2) CVs 0.9955–1.9841; extra-arm max 2.4387; (3) 90/90, all 15 convex | holds, FAIL on (1)(2), in-model only |
| Pair-rule rescue | does not recover odd K* (argmin 3) | first-order even/pair is not 3 at R=3 | holds |

Further scope checks that pass:

- “Law” in CORE.md appears only in the hypothesis sentence. README uses the same hypothesis sentence plus the allowed term “power-law.” OPEN_WORK C3 discusses the “Proposed law” label as awaiting Chad, and does not assert a law.
- No “theory of everything” in the PR’s new prose. Consistency wording scan: 0 FAILs on 29 maintained docs.
- The predictive keystone is stated as proved or numerically supported only in Model S, and there only given convexity, which remains unproved. The increment formula is stated **false** for rhythms. IMP-N60 is **FAILED**, misspecified (isolated V_m vs joint increments), and not rescued. The holographic/fractal miss is explicitly in-model at N=0.05 and is not claimed as a test of a spatial or high-dimensional MERA picture.
- Field-test language is not used for these in-model checks. Scorecard still says untested, not refuted; no qualifying system yet.

---

## Blockers

**B1. Official results quote the wrong first-order-only J on the MUST world.**

`core/keystone_checks/RHYTHM_RESULTS.md` §4 says the first-order-only argmin at `seed2_two_light`, R=3, is “K=3, J=8.105.” §9 repeats “MUST J=6.25 vs first-order J=8.10.” The prior rhythm review repeated “J=8.10.” Those figures are wrong.

From the stored first-order curve in `rhythm_rule.json` and E_∞=0.03788281801526715, J(K)=K+R E_K/E_∞ at R=3 is:

| K | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| J | 7.376 | 7.839 | **7.105** | 7.428 | 8.133 |

The first-order-only argmin is K=3, **J=7.1047**, which already agrees with KEYSTONE_NOTE §2’s worked example (7.376, 7.839, 7.105, 7.428). J=8.105 is exactly 1+7.105, the same off-by-one cost error class as D5a. It is not K=5 (that is 8.133).

The official MUST gate does not use this number and does not flip: predicted C*=4, argmin C*=3, hybrid J=6.2486, E=0.041022 are correct, and 6.2486 still beats the true first-order J=7.105. Kind-matching still helps. Fix the quoted first-order J in RESULTS §4 and §9. The prior review’s repetition should be footnoted or left as a recovered error; do not silently “correct” that file’s historical text without a note. Do not touch the prereg, predictions, or gates.

---

## Should-fixes

**S1. OPEN_WORK W11 cites a nonexistent T24.** W11 ends “Follow-ups as new preregs, not rescues: T21–T24.” There is no T24. The items added in this PR are T19 (Lean, parked), T20 (fairer holographic check), T21 (observer-kind prereg), T22 (per-world locking), T23 (SANITY rerun under D3). §5’s prose already lists T19–T23 correctly. Change W11 to T20–T23, or T19–T23 if Lean is meant to be included.

**S2. `reviews/README.md` is stale on a maintained page.** It still says the core-page drafts “are not in this repository yet (pending a CORE PR).” This PR is that CORE PR and adds `CORE.md`. After merge the index would be false. Update the `core_2026-11-20/` row, and add rows for `reviews/rhythm_2026-11-20/` (SCORING CORRECT) and `reviews/recovered/` (with the provenance caveat).

**S3. Pointers around the new one-page core are incomplete, and the README lead is less scoped than CORE §4.** The README now says “The theory on one page: CORE.md,” then immediately states the unscoped claim that systems are built “in layers matched to the time scales of the world,” including “a rhythm counts two layers by degree.” CORE §4 correctly limits the *predictive* keystone to Model S with unproved numerical convexity, and rejects a pair-count rule as a recovery of K*. Degree remains the right *mode* convention; it is not a shortcut that recovers argmin J for rhythms. The lead sentence was already on main; placing “the theory on one page” above it now makes the gap sharper. Either add a short pointer to CORE §4’s scope, or do not let the first screen outrun the page it just advertised. STATUS.md, also a pointer file, was not updated: its canonical-file list still omits CORE.md. (STATUS’s pre-existing “Looper README wording” sentence is not introduced by this PR and is not required of this change, but it should not be copied forward.)

**S4. New files mention `/workspace/looper` and other box-private paths.** All Looper hits in this PR are “not touched / not searched” clauses, not Looper content or personal data. No emails, phones, or personal names beyond the already-public author line were found in the new files. Still, newly authored `reviews/recovered/PROVENANCE.md` names `/workspace/looper`, `/home/box`, `/cursor/stores`, Grok Bot agent-asset dumps, and `sand-box-store-pack`. The rhythm review header also names `/workspace/looper`. For a public CC0 repo, trim newly authored provenance to say the search excluded a private tree, without writing that path or other box-internal locations. Do not rewrite already-recovered historical referee files just to remove a “looper untouched” clause; note it in provenance if needed. W6’s claim that only “not touched” clauses appear is accurate.

**S5. Leftover “this hygiene PR” wording in OPEN_WORK W5.** W5 still says it was “DONE in this hygiene PR.” That was true on main when #118 landed; it is now a stale deictic in the CORE PR. Say “DONE in the hygiene PR (#118).”

---

## OPEN_WORK completeness

No table IDs or §7 tokens present on main (`ff14a87`) are missing on this head. Added: W11 (DONE), T19–T23. `process/queue/items.json` is byte-identical to main. The frozen-queue remainder list is intact; `SENSE-CELL` and `CAUSAL-KAPPA-LENIENCY-REVIEW` remain listed with the existing discrepancy note. Checker PASS.

---

## Private / Looper / wording

- No “theory of everything.”
- “Law” only in the hypothesis sentence (plus “power-law” and the awaiting-Chad “Proposed law” label row).
- No Looper data, personal information, or `/workspace/looper` tree access. Path mentions: see S4.
- Recovered reviews are labeled recovered, with provenance for missing reports (reviews 26 and 26 r2, review 27 REVIEW3, review 29 itself, a #115 re-review). That residual was already on W6 and is not a drop.

---

## What does not block

- Convexity in Model S remains unproved. CORE and the keystone note say so. The 24 wide-search real-pole worlds are correctly excluded from the 120/120 count.
- Official SANITY MSEs on collapsed-Ω rows remain unsecured under D3; the barely-PASS on `1osc_z0.25_N0.04` is not secure. This is already disclosed, T23 is queued, and the 7/8 kill stands either way.
- The prior rhythm review is SCORING CORRECT on the gates. It missed B1 (J=8.105) and repeated it. That does not reopen the gates.
- Formalization (T19) is correctly parked until the keystone sentence is stable, and is correctly described as unable to earn the §3 hypothesis.
- Follow-ups T20–T23 are new preregs, not rescues of IMP-N60. That is the right posture.

---

## Required before merge

Apply B1 (correct J=8.105 → 7.105 in RESULTS §4 and §9, without touching the prereg, predictions, or gates). Apply S1–S3 in the same pass if possible; S4–S5 are smaller and can be residual if time is tight, but S2 will be false the moment this merges.

No push or merge was made from this review. Working clone: `/workspace/rev119`. This report: `/workspace/review-archive/rev119_REVIEW.md`.
