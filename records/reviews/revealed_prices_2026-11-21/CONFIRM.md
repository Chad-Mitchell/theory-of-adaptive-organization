# Confirm review: PR #133 at b8e4c39 (B1–B4 and S1–S5 applied)

**Reviewer:** blind confirm pass on a fresh clone. This confirm wrote none of `theory/REVEALED_PRICES_2026-11-21.md`, the `CORE.md` / `STATUS.md` / `OPEN_WORK.md` edits, the first independent review, or the fix commits. Same bot family, disclosed. The verdict is from this fresh re-read and re-check, not from memory of the edits.
**Date:** Saturday 21 November 2026, started about 8:49 AM ET, finished about 8:54 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/133
**Clone:** fresh `/workspace/conf133/theory-of-adaptive-organization` (not the first-review clone `/workspace/rev133` and not an author workdir), branch `revealed-prices-2026-11-21` at head `b8e4c39bc5497243967fd19ffc635e57468942b7`. Commits on the branch: note `25809f9`, §3.2/§5 correction `799d44e` (the first-review head), first review `7341b6b`, then review-fix commits `1f0b91e` (B1, B2, S1–S4), `5d1d6bc` (B3), and `b8e4c39` (B4, S5). Merge-base equals current `origin/main` `a65b64e4f6863900c8d789f51e590dad67dd8a41` (PR #132). Clean tree at confirm start. Nothing merged at the start of this confirm. `/workspace/looper` and `/workspace/gtao-evo` were not touched.

**Verdict: READY**

The revealed-prices note is not a lock, not a prereg, not a result, and not an applied change to the kill rule (§8 remains a proposal awaiting Chad's decision C7). All four blockers and all five should-fixes from the first review are applied and are correct. The law-of-adaptive-organization hypothesis sentence is unchanged in `THEORY.md`, `CORE.md`, `README.md`, and the note. `THEORY.md`, `measurement/FRAMEWORK.md`, `measurement/CLAIM_MAP_v2.md`, and `README.md` are byte-identical to `origin/main`. Only the `CORE.md` header line changed; the body, including §2's current wording and the hypothesis sentence, is unchanged. Checkers PASS. No new problem that would reopen the review. Residuals below do not block a merge of this unlocked note and status refresh.

At confirm start the PR was open, head `b8e4c39`, base `a65b64e`, six commits, five files, +226 / −3.

---

## What was checked

- Fresh clone at the stated head; `git merge-base` equals `origin/main` `a65b64e`; `git diff --stat origin/main...HEAD` at confirm start (five files: `CORE.md`, `OPEN_WORK.md`, `STATUS.md`, `reviews/revealed_prices_2026-11-21/REVIEW.md`, `theory/REVEALED_PRICES_2026-11-21.md`). Working tree clean at start. `/workspace/looper` and `/workspace/gtao-evo` not opened.
- First review at `reviews/revealed_prices_2026-11-21/REVIEW.md` compared to HEAD and to the pre-fix tree (`799d44e`). B1–B4 and S1–S5 checked against `THEORY.md` at `a65b64e` (lines 11, 36, 41, 43, 48, 51, 53, 101, 111, 153, 159, 472), `measurement/FRAMEWORK.md` §9 items 1–3, `theory/meq_checks/scope_checks.py` §1b, and `git log` on `main` (`CLAIM_MAP` v2.67 note at line 77 / PR #117 `b12af70`; v2.68 / PR #116 `a1a98aa`; tally OPEN 84, PROVED (in-model) 94, MATH-CORRECTED 23, PRIOR ART 32, total 318).
- The hypothesis sentence is the same string in `THEORY.md` (line 41), `CORE.md` (line 24), `README.md` (line 9), and the note (lines 3 and 106): "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."
- Proposed §8 replacements match the current phrasing of THEORY lines 53, 111, and 159 and of `CORE.md` §2; none of those canonical passages was edited.
- `python3 tools/check_open_work.py` PASS. `python3 tools/check_consistency.py` PASS (0 FAIL; 23 frozen-record INFO hits; 2 pre-existing soft length WARNs on THEORY.md and README.md already present on `main`).

---

## B1 — fixed; technology-ratio count is +t; CT34 scoped to one currency

§3.2 now states the count in a single common currency: `t` technologies with `r_j` primitive prices give `Σ r_j + 1` absolute prices (the primitives plus the top stake) and `Σ(r_j − 1) + t` independent ratios (within-technology ratios plus `t`, including the `t − 1` cross-technology scale ratios). The two-read-technology case `r_1 = r_2 = 1` is `p = 2`, which now agrees with §3.4. If layers use separate currencies with unmeasured exchange rates, `p` grows with `K`. The single-currency and exactness or weak-coupling premises are required, and a shared driver (CT34 (iv)) or own-interest layers (CX2) revert to the unlinked count.

That is the algebra the first review asked for, and it matches `THEORY.md` line 472 (`J = F(x) + G(y; θ(x))` in one currency).

---

## B2 — fixed; scale invariance restricted; binding-ruin scale ratio counted

§1 item 1 now restricts pure price-ratio identification to the ruin-absent or ruin-slack regime. When ruin binds, the feasible set depends on `J/B`, `y/B`, and `w/B` (via `σ² ∝ w²`); if `B` and `y` are observed while prices are known only up to scale, one overall scale ratio (e.g. `w/B`) remains free. §3.1 includes that ratio in `p`. This matches `THEORY.md` line 101 (CT24) and `scope_checks.py` §1b.

---

## B3 — fixed; §8 items 1–2 align with §3.1; item 4 is symmetric

Item 1 now uses `n_fit ≥ p` with full-rank identification, `n_score ≥ 1`, and overidentifying degrees of freedom `n_fit + n_score − p ≥ 1`, counting price ratios, any binding-ruin scale ratio, and nuisance parameters. CT34 linking may be claimed only where its premises are verified before data; R2 and R3 must be computed before data. That agrees with §3.1 and no longer contradicts the §3.4 `m = 2` worked count. Item 2 keeps FRAMEWORK §9 item 3's single pre-comparison re-measurement rule for independently measured non-price inputs and forbids re-fitting locked prices after scoring.

Item 4 no longer allows unqualified gradient tests to count for support while barring a kill. Two symmetric C7 options are stated: Option A (recommended) treats §4 tests as PF17-corollary tests only, earning neither `CORE.md` §3 support nor a kill; Option B admits a power-checked class test only if pass and fail carry symmetric weight. Absolute §3 qualification remains required for single-design or band-miss kills. This is consistent with `THEORY.md` line 51 ("not evidence either way"). The amendment is not applied.

---

## B4 — fixed; CLAIM_MAP attribution and field blockers match `main`

`STATUS.md` now says PR #117 bumped CLAIM_MAP to v2.67 before PR #116 bumped it to v2.68, and that none of #118–#132 bumped the version (#124 and #127 edited *E. coli* prospect notes without changing v2.68 or the 318 tally). That matches `git log` on `main` (`b12af70`, `a1a98aa`, then the #124/#127 commits). The field-path summary no longer says every attempt stopped only on fitness-unit prices: VIS-1F is blocked on `(h, w)` and L3, *E. coli* on missing `σ` and `T_red` alongside an R3 fail on P1/P3, and GRID-CROSS on missing pre-control `d1`. The note's §1 matches that record.

---

## S1–S5 — fixed

1. **S1.** §3.4 now says that with unmeasured stakes under one technology, `p` equals the number of distinct unmeasured stake levels (and stays 1 if relative stakes are measured). The old `p = 2 if not` error is gone.
2. **S2.** §3.1 labels `n_fit ≥ p` as the order condition and requires full rank `p` in the fit-set equations. §8 item 1 repeats the rank requirement.
3. **S3.** §5 now reads CT34 as single-currency cooperative partial minimization (`J*_T(θ(x))` is a constant upkeep `h` only when `θ` is independent of `x`, and a value function when it is not). Own-interest layers are referred to CX2, not to CT34. §6 no longer claims the CT34-based count as this repository's; dynamic-programming / partial-minimization counting is credited as standard (Rust 1987; Bellman 1957), with only the mapping onto `J` and CT34's exclusions treated as repository-specific.
4. **S4.** §0 cites THEORY line 36 for "only dimensionless ratios matter" (verified on this clone; the quote is in that bullet). Ng & Russell 2000 is titled *"Algorithms for Inverse Reinforcement Learning"*, ICML 2000, pp. 663–670. The Hall, Humphries & Kramer 2007 row now says renewal was manipulated on artificial patches, the natural world spectrum was not measured, and no public data were found.
5. **S5.** `STATUS.md` now attributes `history/2026-11-21_NIGHT.md` to PRs #121–#131, with PR #132 as the record itself.

---

## No overclaim; kill rule and hypothesis untouched

The file is still a fair-test standard and a proposed amendment, not a new law and not a lock. §9 still finds no qualifying public dataset and locks nothing. §10 still says the note adds no evidence and does not change the odds. Canonical kill-rule wording in `THEORY.md`, `FRAMEWORK.md`, and `CORE.md` §2 is unchanged. The hypothesis sentence is unchanged.

---

## Checkers (this clone)

- `python3 tools/check_open_work.py` — PASS (union missing from OPEN_WORK.md: 0)
- `python3 tools/check_consistency.py` — PASS (0 FAIL)

---

## Residuals (do not block)

1. **§2 "Dropped" list still uses the pre-B3 parenthetical** that absolute qualification is "not required for a fair test" as a precondition for *support* and "remains a precondition for a *kill*; §8". The sentence was already in the reviewed head `799d44e` and was not listed as a blocker; §8 item 4 is now the symmetric C7 choice, including recommended Option A under which qualification remains required for `CORE.md` §3 support. The parenthetical points at §8. It is drafting looseness in the dropped-requirements list, not a reopened B3.
2. **`STATUS.md` "in review" and OPEN_WORK W15 "needs confirm review"** will be slightly stale once this confirm is on the branch and the PR is merged. C7 remains "proposed, not applied," which stays correct. `reviews/README.md` was not updated to index this review folder (same as several earlier same-day notes; not requested by the first review).
3. **OPEN_WORK lists C7 above C6.** Cosmetic ID order only.

---

## Recommendation

Merge is appropriate. B1–B4 and S1–S5 are applied and correct, the hypothesis sentence and canonical kill-rule wording are untouched, no locked test was run or re-scored, and both checkers PASS. This is not a lock, and it does not adopt C7.
