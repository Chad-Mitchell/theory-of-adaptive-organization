# Confirm review: PR #129 at e2c0681 (M1–M2 and S1–S6 fix, rebased on ecf6e77)

**Reviewer:** confirm pass on a fresh clone. This confirm wrote none of the shortlist, the OPEN_WORK T29 row, the VIS-1F outline, the first independent review, or the M1–M2 / S1–S6 fix commit. Same bot family, not a blind second executor; the verdict is from this fresh re-read and re-check, not from memory of the edits.
**Date:** Saturday 21 November 2026, started about 3:16 AM ET, finished about 3:25 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/129
**Clone:** fresh `/tmp/gtao-confirm-pr` (not the first-review clone and not the author workdir), branch `discrim-2026-11-21` at head `e2c0681a2a59f504a228b3eb2e9bed38369e2aef`. Parents: shortlist replay `b281181a9fa37832830ce69d89c0df6929d59a5e`, then the review-fix `e2c0681`. Merge-base equals current `origin/main` `ecf6e77172797585bf199e184bf19997455bd094`. Clean tree at confirm start. Nothing merged at the start of this confirm. `/workspace/looper` and `/workspace/gtao-evo` were not touched. Compute at nice 19. Existing elan toolchain was reused; Mathlib cache was already present (lake reported no files to download).

**Verdict: READY**

This is still an unlocked shortlist and a draft outline, not a lock, and it does not re-score P1, P3, P4, P13, P25, or any other locked row. `CORE.md` is byte-identical to `origin/main`. The law-of-adaptive-organization sentence is unchanged. The branch is rebased onto `ecf6e77`. GRID-CROSS OPEN_WORK rows are kept. The van Hateren world source is corrected. CT12's 1/α is no longer advertised as the VIS-1F prediction. Lemma B2's precision-effort elasticity α/(2α−1) matches THEORY. The pre-Pass-1 gate is now written in operational form and closes the price-free structural-claim loophole the first review named. Candidate 1 is kept first only as a Pass 1 attempt, with an explicit drop rule, and is not overstated as a shown discriminator. Checkers PASS. `tools/check_lean.sh` exits 0 and prints `check_lean.sh: OK`. `pytest tools/` is **146 passed**. No new problem that would reopen the review. Residuals below do not block a merge of this unlocked note.

At confirm start the PR was open, head `e2c0681`, base `ecf6e77`, two commits, four files, +412 / −4.

---

## What was checked

- Fresh clone at the stated head; `git merge-base --is-ancestor origin/main HEAD` (true); `git diff --stat origin/main...HEAD` (two commits, four files). Working tree clean. `/workspace/looper` and `/workspace/gtao-evo` not opened.
- OPEN_WORK row inventory against `origin/main`: no main row dropped; only T29 added. W14 and T3 bodies compared line by line. As-of line checked for `main` `ecf6e77` and for PR #128 described as merged, official comparison not run, P25 still UNTESTED.
- `theory/DISCRIMINATING_CANDIDATES_2026-11-21.md` re-read in full against `/workspace/review-archive/rev129_REVIEW.md` (M1, M2, S1–S6, and the nits). SHA-256 of `reviews/discrim_2026-11-21/REVIEW.md` equals the archive copy (`600c0a6693b052237d7ca550c44abca30f5ff18b63bf5d6e8e193b124dea8923`; files are byte-identical).
- Lemma B2 in THEORY.md Appendix B.3 (line 347) compared to the elasticity written in the shortlist. CT12 setting and the 1 < α < 3 interval checked at THEORY B.3. The written γ → α map checked against the CT12 structure function.
- Ranking honesty and the VIS-1F drop rule. The written Pass 1 gate read for concreteness and loopholes (error band, γ → α map, (h, w) rule, L3 / finite K\*, no price-free path).
- `git diff origin/main...HEAD -- CORE.md THEORY.md` empty. `CORE.md` SHA-256 `aee235cb2a9b7d46a0e82c97825984eb3f5dcb160bdd283c90df552616284a7a` equals `origin/main`. The hypothesis sentence is unchanged in CORE.md and THEORY.md: “**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**” Diff file list is only `OPEN_WORK.md`, `reviews/README.md`, `reviews/discrim_2026-11-21/REVIEW.md`, and the shortlist. No locked results file is touched.
- Every DOI in the shortlist (21 unique, including the four efficient-coding DOIs added in the fix) queried on `https://api.crossref.org/works/{doi}` this session with User-Agent `GTAO-confirm-review/0.1`; all returned a works record. Issued years in the §6 table match Crossref `issued`.
- `python3 tools/check_open_work.py`; `python3 tools/check_consistency.py`; `tools/check_lean.sh`; `python3 -m pytest tools/ -q`, all at nice 19.

---

## M1 — rebased; GRID-CROSS rows kept

`origin/main` `ecf6e77` is an ancestor of `e2c0681`. The only added OPEN_WORK identifier versus main is T29. W14 is present. T3 still carries the GRID-CROSS update. The as-of line states that `main` is `ecf6e77` and that PR #128 is merged, official comparison not run, P25 still UNTESTED. The shortlist header says the same.

W14 and T3 are not byte-identical to main: both were updated from “Confirm review not yet filed” / “needs reviewer (confirm of PR #128)” to “Confirm review READY … PR #128 merged as `ecf6e77`. Official comparison not run; P25 still UNTESTED,” and the W14 phrase “S1–S7 applied in this PR” was narrowed to “S1–S7 applied,” which is right once this branch is no longer the #128 branch. Those are status updates after a completed merge, not a drop of GRID-CROSS rows and not a re-score of P25.

---

## M2 — van Hateren world source corrected

The shortlist no longer says the intensity series are “from the blowfly.” Candidate 1 and the VIS-1F outline state that van Hateren 1997 measured intensity with a device worn on a headband by a freely walking person, then played the series back to *Calliphora vicina* on an LED; that fly-in-habitat series would have been ideal and were not obtained with sufficient accuracy; and that the mismatch is three-way: human-walking world, *Calliphora* responses, *D. melanogaster* N_e. The earlier phrase “flying Diptera, acting in natural light-intensity time series” is quoted as an overstatement. The §6 short title is “natural intensity time series, played to the blowfly,” which matches the paper’s actual procedure. This confirm did not re-open the PDF; the wording was checked against the first review’s quotations, which had been checked against that file.

---

## S1 — right theorem class; elasticity matches THEORY; ranking not overstated

CT12 is stated as exact reset reads, structure function E(X_{t+τ} − X_t)² = q·τ^{α−1}, open interval 1 < α < 3, and is not the primary VIS-1F arm. Continuous early vision is pointed at Lemma B2 / CT21. THEORY.md line 347 (Lemma B2) says precision effort with a linear price is proportional to w^{α/(2α−1)} q^{1/(2α−1)}. The shortlist quotes that formula and correctly gives the stakes elasticity 2/3 at α = 2. The written γ → α map (temporal PSD ∝ 1/f^γ maps to α = γ, with a logarithmic special case at γ = 1) is the map implied by that structure function; van Hateren’s “γ here close to 1” is treated as putting α at or outside the proved CT12 interval. Filter shape is expected to collapse into whitening unless independently sourced (h, w) moves the cutoff or count. CT12 is dropped unless a discrete exact-reset read is defined and the fitted α, including its error band, lies strictly inside (1, 3).

The ranking is unchanged and is honestly framed. Line 53 and §4 say candidate 1 remains first as the best next *Pass 1 attempt*, not as a shown discriminator, and not because 1/α versus ½ is already in reach. The explicit drop rule is: if Pass 1 cannot source (h, w) independently of the design, or if L3 leaves both a finite K\* and a priced cutoff undefined, or if no rival lies outside the pre-written band, candidate 1 is not locked. No other shortlisted candidate is claimed as a shown discriminator either. That is the right strength of claim for an unlocked shortlist.

---

## S2 — gate written; price-free loophole closed; leftover recipe is named, not fudged

§5 now specifies, before any official Pass 1 fit: the error-band procedure (estimator and windows to be named; coverage from section-to-section variability or a preregistered bootstrap of the same traces; digitization error if spectra are taken from figures; propagation into design units by a preregistered interval-arithmetic or sensitivity rule; numerical width not chosen after seeing the traces and not loosened later); the γ → α map, used only for a CT12 arm; the (h, w) rule (prices must be independently sourced, not taken from the kernels, cutoffs, or counts being predicted; if they cannot, Pass 1 stops; “There is no alternative ‘declared price-free structural claim’ path”); and finite K\* given L3 (if a preregistered model-selection rule finds no separated real corners, K\* is undefined; the fallback is a priced cutoff only if (h, w) are independently sourced and a cutoff is well-defined; if neither can be defined, Pass 1 stops). Official Pass 1 scoring is not started. The outline remains unlocked and unhashed.

The gate is concrete enough, as a *procedure*, to be locked before any official Pass 1 fit, and it closes the loophole the first review named. Two recipe choices are still deliberately not invented in this unlocked note: the specific PSD estimator, windows, and interval-arithmetic rule, and the FRAMEWORK §9 item 8 model-selection rule for corners versus a continuum, which the outline says must be finalized before any K count. Those are residuals to be named in a later lock, before any official Pass 1 computation, not a path around the gate. They do not block merging an unlocked draft that already forbids starting official Pass 1 now.

---

## S3–S6 and nits

**S3.** Laughlin 1981 (doi 10.1515/znc-1981-9-1040), Atick & Redlich 1990 (10.1162/neco.1990.2.3.308) and 1992 (10.1162/neco.1992.4.2.196), and van Hateren 1992a (10.1007/bf00188924) are credited in candidate 1 and listed in §6 as Crossref works records, full texts not fetched. All four resolved on Crossref this session (issued 1981, 1990, 1992, 1992).

**S4.** The Ni 2020 wording is now “that WT (chemotaxis) advantage vanished when the culture was stirred.”

**S5.** Beekman’s fetch is written as Europe PMC XML HTTP 500, plus the PMC reCAPTCHA wall. The numbers 600 and 0.0052 are quoted as coming from the first version, marked not re-verified, and are not used in the N\* arithmetic. Dornhaus is likewise marked not re-opened.

**S6.** TESTBEDS #2 (learning rate), #3 (central-bank calendars), and #6 (weather cycles) are briefly disposed in §3, with the intro’s claim that the TESTBEDS ranking was searched.

**Nits.** Sung Table 1 is labelled a subset (three species omitted). Honda’s ∼4.4-fold figure is attributed to the published 2022 XML and the preprint. N\*(ρ) is CT14 (square-root technology); CT16 is the telling price; both sit in Result 4. The 7–15× store-versus-mode range is the §1a / `meq_roots.out` band, with the §2 point estimate 1.5 and 6.9 days distinguished. Smaller N_e is stated to widen ε.

---

## CORE, law sentence, locked rows, DOIs, checkers

`CORE.md` is byte-identical to `origin/main` (SHA-256 `aee235cb2a9b7d46a0e82c97825984eb3f5dcb160bdd283c90df552616284a7a`). The law sentence in CORE.md line 24 and THEORY.md line 41 is byte-identical to main. THEORY.md has no diff versus main. No locked measured-results file, CLAIM_MAP row, or prereg is in the diff.

All 21 unique DOIs in the shortlist returned a Crossref works record this session, including `10.1016/S0042-6989(97)00105-3` (van Hateren 1997, issued 1997-12). Table issued years match, including Ni issued 2019-12-23 listed as 2019 and Juusola issued 2000-12-12 listed as 2000. Full texts were not re-fetched in this confirm.

`python3 tools/check_open_work.py` PASS. `python3 tools/check_consistency.py` PASS (0 FAIL; frozen-record INFO hits only). `tools/check_lean.sh` OK (`lake exe cache get` already decompressed; `lake build` completed, 4047 jobs). `python3 -m pytest tools/ -q`: **146 passed** in 2:43.

---

## Residuals (do not block)

- The unlocked gate still leaves the exact estimator, windows, interval-arithmetic rule, and the corners-versus-continuum model-selection rule to be named before any official Pass 1 fit. The note already forbids inventing those numbers here and forbids starting official Pass 1 in this revision.
- This confirm did not re-open Beekman, Dornhaus, or the van Hateren PDF; it checked the repaired wording against the first review and against Crossref. That is enough for a wording fix on an unlocked note.
- W14 / T3 / the reviews/README GRID-CROSS row were updated for the already-merged PR #128 confirm. Scientific GRID-CROSS status is unchanged (official comparison not run; P25 UNTESTED).

---

## Recommendation

Merge as an unlocked shortlist and OPEN_WORK T29. Do not lock VIS-1F, and do not start official Pass 1 scoring, until the remaining Pass 1 recipe (estimator, windows, interval rule, and the model-selection rule for K) is named in a later lock, before any official fit. Nothing here changes a locked result.
