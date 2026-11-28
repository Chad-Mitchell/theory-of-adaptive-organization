# Confirm review: PR #131 at 8a9d016 (S1–S2 and nits applied)

**Reviewer:** confirm pass on a fresh clone. This confirm wrote none of `theory/PRICE_FREE_2026-11-21.md`, the OPEN_WORK §8 pointer, the first independent review, or the S1–S2 / nits fix commit. Same bot family, not a blind second executor; the verdict is from this fresh re-read and re-check, not from memory of the edits.
**Date:** Saturday 21 November 2026, started about 4:35 AM ET, finished about 4:41 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/131
**Clone:** fresh `/tmp/gtao-pr131` (not the first-review clone and not the author workdir), branch `pricefree-2026-11-21` at head `8a9d0164e856f12a2f0525011eb802d754a8e0ab`. Commits on the branch: classification `0be10b36b69a1becbb7ff0809063db258e65fc03`, then the first review `112bb5d`, then the review-fix `8a9d016`. Merge-base equals current `origin/main` `d42220dff45e11cf238b58faa3cd016e4c7a536c`. Clean tree at confirm start. Nothing merged at the start of this confirm. `/workspace/looper` and `/workspace/gtao-evo` were not touched. Compute at nice 19. Existing elan toolchain was reused; Mathlib cache was already present (lake reported no files to download).

**Verdict: READY**

The price-free classification is not a lock, not a prereg, and not a re-score. The two should-fixes and the four nits from the first review are applied. `CORE.md` is byte-identical to `origin/main` (SHA-256 `aee235cb2a9b7d46a0e82c97825984eb3f5dcb160bdd283c90df552616284a7a`). The law-of-adaptive-organization hypothesis sentence is unchanged in `CORE.md`, `THEORY.md`, and `README.md` (those three files are byte-identical to `origin/main`). The quoted S3 exponents match `theory/GENERAL_THEOREM.md` lines 310–316 as interval / *T*\* exponents; the three prior-art DOIs resolve on Crossref as cited; the qualitative ruin-binding reversal is no longer sold as unique. Checkers PASS. `tools/check_lean.sh` exits 0 and prints `check_lean.sh: OK`. `pytest tools/` is **146 passed**. No new problem that would reopen the review. Residuals below do not block a merge of this unlocked classification.

At confirm start the PR was open, head `8a9d016`, base `d42220d`, three commits, four files, +296 / −1.

---

## What was checked

- Fresh clone at the stated head; `git merge-base` equals `origin/main` `d42220d`; `git diff --stat origin/main...HEAD` at confirm start (three commits, four files: `OPEN_WORK.md`, `reviews/README.md`, `reviews/pricefree_2026-11-21/REVIEW.md`, `theory/PRICE_FREE_2026-11-21.md`). Working tree clean at start. `/workspace/looper` and `/workspace/gtao-evo` not opened.
- First review at `/workspace/review-archive/rev131_REVIEW.md` compared to the should-fix list (S1, S2, nits PF7 / PR10 / PF10 / PR11). Fixes checked against the pre-fix tree (`0be10b3`) and against HEAD `8a9d016`.
- S3 exponents re-read at `theory/GENERAL_THEOREM.md` lines 310–316. PF7 / PF10 / PR11 citations re-read at `THEORY.md` lines 87, 101, 164, 335–339, and 357. PR10 re-read at `theory/LAYERS.md` lines 53 and 57.
- `CORE.md`, `THEORY.md`, and `README.md` are each byte-identical to `origin/main`. The hypothesis sentence is the same string in each: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."
- The four-file diff versus `origin/main` does not touch `CORE.md`, `THEORY.md`, `CLAIM_MAP_v2.md`, `STATUS.md`, `FRAMEWORK.md`, or any locked results, prereg, or deviations file.
- DOIs `10.1016/S0003-3472(81)80128-5`, `10.1016/S0003-3472(80)80142-4`, and `10.1098/rstb.2002.1061` queried on `https://api.crossref.org/works/{doi}` this session.
- `python3 tools/check_open_work.py` PASS. `python3 tools/check_consistency.py` PASS (0 FAIL; 23 frozen-record INFO hits; soft length WARNs on THEORY.md and README.md already present on `main`). `bash tools/check_lean.sh` OK (`lake exe cache get`, then `lake build` completed successfully, 4047 jobs). `python3 -m pytest tools/ -q`, with `~/.elan/bin` on `PATH`, at nice 19: **146 passed** in 2:08.

---

## S1 — fixed; exponents match GENERAL_THEOREM.md lines 310–316

Pre-fix PF8 and the §0 S3 bullet called S3's exponents "refresh-rate exponents" and then quoted −*p*/(1+*pH*) on σ and 1/(1+*pH*) on *c*/*w*. Those are the exponents of the interval *T\**, not of the refresh rate 1/*T\**.

HEAD wording is interval / *T\**. PF8 now reads: "interval (*T\**) exponents depend only on the loss exponent *p* and Hurst *H*, not on the currency; for (*p*, *H*) they are −*p*/(1+*pH*) on σ and 1/(1+*pH*) on *c*/*w* (refresh-rate exponents are the negatives)." The §0 bullet matches. The quoted numbers are unchanged.

That is what `theory/GENERAL_THEOREM.md` lines 310–316 state. Line 312 gives *T\* = [c(pH + 1)/(pH · m_p · w σ^p)]^{1/(1+pH)}*; line 313 gives the interval exponents on σ and on *c*/*w*; line 314 gives the worked values (−1, −⅔, −⅘) as *T\** exponents on σ. The refresh-rate exponents are the negatives, as the fix now says. PF7's look-rate signs were already correct and are unchanged.

---

## S2 — prior art credited; 'distinctive' downgraded; DOIs confirmed

§2 item 1 and §3.1 now name Stephens 1981, Caraco, Martindale & Whittam 1980, and Dall & Johnstone 2002. The heading of the short list is now "What, if anything, remains distinctive to *J*'s structure (after prior art)." §3.1 states plainly that the qualitative reversal when a survival constraint binds is not unique to *J*. What remains distinctive is the comparative static in the stake *w* of *S* + *w E*, with the reserve-pays-*J* / *w*²-variance mechanism. The scoped "expected-cost optimizers without a feasibility set that depends on *w*" sentence is kept. OPEN_WORK §8 carries the same credit and the same remainder. That is the first review's required downgrade, not a silent withdrawal of the in-model claim.

Crossref this session:

| DOI | Crossref issued | Bibliographic check |
|---|---|---|
| 10.1016/S0003-3472(81)80128-5 | 1981-05 | Stephens, D.W., *The logic of risk-sensitive foraging preferences*, *Anim. Behav.* 29:628–629 — matches. No abstract in Crossref. |
| 10.1016/S0003-3472(80)80142-4 | 1980-08 | Caraco, Martindale & Whittam, *An empirical demonstration of risk-sensitive foraging preferences*, *Anim. Behav.* 28:820–830 — matches. No abstract in Crossref. |
| 10.1098/rstb.2002.1061 | 2002-11-29 | Dall, Sasha R. X. & Johnstone, Rufus A., *Managing uncertainty: information and insurance under the risk of starvation*, *Phil. Trans. R. Soc. Lond. B* 357:1519–1526 — matches. Abstract present. |

The quoted Dall sentence, "gathering information is a luxury while insurance is a necessity," is in the Crossref abstract, as is the claim that sampling declines with lower reserves and late in the bout. The file records the Stephens and Caraco PDFs as not opened and their abstracts as absent from Crossref, which is correct. No number is taken from those two papers.

---

## Nits — applied

1. **PF7.** The 1/α elasticity is now proved in the CT12 setting, citing lines 335–339 (exact reset reads, 1 < α < 3, squared error), not THEORY line 101. The status cell says the elasticity is not claimed with read noise or for a world with its own time scale. Line 101 remains the CT24 share-failure paragraph, and is still used only for PF9 / PR11, where it belongs.
2. **PR10.** The (*C*/*h*)^{1/3} *L*^{2/3} scaling and the withdrawn-as-store-count remark are now cited at `theory/LAYERS.md` line 57. Line 53 is the leftover rational-spectrum sentence, and is no longer cited here.
3. **PF10.** The *h* > 0 small-ρ exponent now records the case split at THEORY line 357: it stays −(1−*b*)/(1−*a*) if *a* > *b*, and becomes −1 if *a* ≤ *b*. Either way it remains price-free, as the first review already noted.
4. **PR11.** The identity that real internal prices equal multipliers is now a definition (CX5; THEORY line 101). The testable content is that real systems allocate so as to satisfy the *K* − 1 equalities. That matches the THEORY wording.

---

## No overclaim; no locked row re-scored

The file is still a classification of existing theorems, not a new law and not a lock. The bottom line is unchanged in substance: the law is testable in the field without absolute (*h*, *w*) in principle, and only on a short list; no qualifying public no-account dataset yet scores one of those claims; the bottleneck has narrowed but has not been cleared; "the law is not shown to be field-testable, with or without absolute prices." PF2 remains on the short list only after the prior-art remainder is stated. No official row is re-scored. `CORE.md` and the law sentence were not edited.

---

## Checkers and tests (this clone)

- `python3 tools/check_open_work.py` — PASS (union missing from OPEN_WORK.md: 0)
- `python3 tools/check_consistency.py` — PASS (0 FAIL)
- `bash tools/check_lean.sh` — OK
- `python3 -m pytest tools/ -q` — **146 passed** in 2:08

---

## Residuals (do not block)

1. **This confirm did not re-open the Dall & Johnstone PMC HTML (`PMC1693060`).** The quotes in §2 item 1 are from the abstract, and the Crossref abstract fetched this session contains them. That is enough for a fix-confirm. The Stephens and Caraco PDFs were not opened in the fix commit and were not opened here.
2. **The PF2 table row itself does not name the prior art.** Credit lives where the first review asked for it, in §2 item 1, §3.1, the sources table, and OPEN_WORK §8. Not a gap in the required fix.

---

## Recommendation

Merge is appropriate. The two should-fixes and the four nits are applied, the three DOIs resolve as cited, CORE and the law sentence are untouched, and no locked row is re-scored. This is not a lock, and it does not start official scoring of a price-free field test.
