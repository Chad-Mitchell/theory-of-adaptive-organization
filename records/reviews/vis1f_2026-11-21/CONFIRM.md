# Confirm review: PR #130 at 4b0c3d4 (S1–S3 and nits applied)

**Reviewer:** confirm pass on a fresh clone. This confirm wrote none of the drop note, the OPEN_WORK T29 rewrite, the first independent review, or the S1–S3 / nits fix commit. Same bot family, not a blind second executor; the verdict is from this fresh re-read and re-check, not from memory of the edits.
**Date:** Saturday 21 November 2026, started about 3:53 AM ET, finished about 4:00 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/130
**Clone:** fresh `/tmp/gtao-confirm130` (not the first-review clone and not the author workdir), branch `vis1f-2026-11-21` at head `4b0c3d4db45f0b76dcbbcdde45874232e39b03e4`. Commits on the branch: drop `04a1988f46f171e229d9887c7e876304ef0db9da`, then the first review `d204d61168ec64d7320b91c934c08999c48de69f`, then the review-fix `4b0c3d4`. Merge-base equals current `origin/main` `e2bfc2ba730cee102c612ed8da20bfde0a1aafc3`. Clean tree at confirm start. Nothing merged at the start of this confirm. `/workspace/looper` and `/workspace/gtao-evo` were not touched. Compute at nice 19. Existing elan toolchain was reused; Mathlib cache was already present (lake reported no files to download).

**Verdict: READY**

The VIS-1F drop stands under the written pre-Pass-1 rule. It is not a lock, and it is not an official Pass 1 fit. No locked row is re-scored. `CORE.md` is byte-identical to `origin/main` (SHA-256 `aee235cb…284a7a`). The law-of-adaptive-organization hypothesis sentence is unchanged in `CORE.md`, `THEORY.md`, and `README.md` (those three files are byte-identical to `origin/main`). The three should-fixes from the first review are applied, and the two nits are applied. The drop note remains honest. The fitness-unit-price lesson is scoped and does not overclaim. Checkers PASS. `tools/check_lean.sh` exits 0 and prints `check_lean.sh: OK`. `pytest tools/` is **146 passed**. No new problem that would reopen the review. Residuals below do not block a merge of this unlocked drop note.

At confirm start the PR was open, head `4b0c3d4`, base `e2bfc2b`, three commits, four files, +237 / −2.

---

## What was checked

- Fresh clone at the stated head; `git merge-base` equals `origin/main` `e2bfc2b`; `git diff --stat origin/main...HEAD` (three commits, four files: `OPEN_WORK.md`, `reviews/README.md`, `reviews/vis1f_2026-11-21/REVIEW.md`, `theory/VIS1F_DROP_2026-11-21.md`). Working tree clean at start. `/workspace/looper` and `/workspace/gtao-evo` not opened.
- First review at `/workspace/review-archive/rev130_REVIEW.md` compared to `reviews/vis1f_2026-11-21/REVIEW.md`: SHA-256 `18334f6e83a3c4d0b08c0b3beb6fe2f70a57e6518dfa4ab59a3267fd79bc69c5`; the two files are byte-identical.
- S1, S2, S3, and both nits checked against the pre-fix tree (`04a1988` / `d204d61`) and against HEAD `4b0c3d4`.
- Drop-note honesty: written rule quoted, both sides still fire, no lock, no official fit, candidate 2 not sold as a discriminator, Markow & Manning still unused as *w*, no invented price.
- `CORE.md`, `THEORY.md`, `README.md`, `STATUS.md`, `measurement/FRAMEWORK.md`, `measurement/CLAIM_MAP_v2.md`, and the shortlist `theory/DISCRIMINATING_CANDIDATES_2026-11-21.md` are each byte-identical to `origin/main`. The hypothesis sentence is the same string in each of those core pages.
- DOI `10.1242/jeb.001040` queried on `https://api.crossref.org/works/{doi}` this session.
- `python3 tools/check_open_work.py` PASS. `python3 tools/check_consistency.py` PASS (0 FAIL; frozen-record INFO hits only; soft length WARNs already on main). `bash tools/check_lean.sh` OK (`lake exe cache get`, then `lake build` completed successfully, 4047 jobs). `python3 -m pytest tools/ -q`, with `~/.elan/bin` on `PATH`, at nice 19: **146 passed** in 2:00.

---

## S1 — fixed; Crossref confirms Matthew Cobb

Pre-fix §2.2 and the §6 table attributed doi `10.1242/jeb.001040` to Niven, Anderson & Laughlin. HEAD names Matthew Cobb, "VISION COSTS," *J. Exp. Biol.* 210(15): vii (2007), and states that this is not the Niven, Anderson & Laughlin 2007 source; that remains the *PLoS Biol.* paper, doi `10.1371/journal.pbio.0050116`, opened in §2.1. The §6 table matches.

Crossref this session returned: title "VISION COSTS"; author Matthew Cobb; container *Journal of Experimental Biology*; issued 2007-08-01; volume 210, issue 15, pages vii–vii; type journal-article. The author fix is correct. The file is still recorded as Crossref only (publisher PDF HTTP 403) and is not used. No number was taken from it.

---

## S2 — five-column T29 row restored

On `04a1988` and `d204d61`, the OPEN_WORK T29 row had four columns: Item and State were collapsed, and the gate sat in the State slot. HEAD has five columns: Item / State / Gate / Where (plus the ID).

- **Item** names the discriminating-candidate work after E. coli P1/P3 could not exclude R3 and the cross-grid test is underpowered and data-blocked.
- **State** records that VIS-1F is **DROPPED** under the written pre-Pass-1 rule, without a lock and without an official Pass 1 fit; that (h, w) could not both be sourced independently of the design; that L3 leaves both a finite K* and a priced cutoff undefined; and that the next Pass 1 attempt, not a lock, is candidate 2, "still not a shown discriminator; high risk of collapse into Ni et al. 2020 and Honda et al. 2022."
- **Gate** is `in progress-able`.
- **Where** points at the drop note, the unchanged shortlist, and branch `vis1f-2026-11-21`.

Candidate 2 is not sold as a discriminator. Locked rows are not re-scored in the State text.

---

## S3 — lesson scoped, no overclaim

OPEN_WORK now has a short §8, titled "Lessons (scoped; not a completed survey)." The sentence is that independently sourcing fitness-unit prices (*h*, *w*) may be the binding obstacle for most field tests of the law. It is attributed to this VIS-1F pre-Pass-1 check together with the existing `STATUS.md` sentence that stakes *w* have never been measured validly. It says it is not a completed survey of field tests, and that it does not change `CORE.md` or the law-of-adaptive-organization hypothesis sentence.

That matches the first review's scope. "May be" and "not a completed survey" keep it from reading as a finished inventory. `CORE.md` and the hypothesis sentence were not edited. `process/QUEUE.md` was not edited (frozen, and not where lessons live).

---

## Nits — applied

1. Niven 2007's *D. melanogaster* brightest-stimulus rate is now written \(197 \pm 31\) bits s\(^{-1}\) (n = 26), in the range phrase and in the per-species list, in line with *Calliphora*, *Sarcophaga*, and *D. virilis*. The pre-fix "about 200" wording is gone.
2. "Model S is the right noise class" is marked as an inference from the SN1 record, not a quotation from it.

---

## Drop note still honest; no locked row re-scored

The note still quotes the written drop rule from the shortlist and does not loosen it. Both sides still fire: (h, w) cannot both be sourced independently of the design in commensurate fitness units, and L3 leaves both a finite K* and a priced cutoff undefined. No official Pass 1 fit was run. No PREREG was locked. Markow & Manning 1980 is still opened and refused as *w* (loss only at the extremes). No price is invented. Qualification of the class is still not shown. Candidate 2 is the next unlocked Pass 1 attempt, with the shortlist's collapse risk left in place.

The four-file diff versus `origin/main` does not touch `CORE.md`, `THEORY.md`, `CLAIM_MAP_v2.md`, `STATUS.md`, `FRAMEWORK.md`, the shortlist, or any locked results, prereg, or deviations file. Nothing here re-scores P1, P3, P4, P13, P25, SN1, BIO1, or any other locked row.

---

## Checkers and tests (this clone)

- `python3 tools/check_open_work.py` — PASS
- `python3 tools/check_consistency.py` — PASS (0 FAIL)
- `bash tools/check_lean.sh` — OK
- `python3 -m pytest tools/ -q` — **146 passed** in 2:00

---

## Residuals (do not block)

1. **After merge, the OPEN_WORK as-of line will still describe this PR as not merged**, and T29's Where will still name branch `vis1f-2026-11-21`. Ordinary header lag, the same class earlier PRs have cleaned up later. Not a conflict and not a gate change.
2. **This confirm did not re-open the Laughlin 1998, Niven 2007, or Markow & Manning 1980 PDFs.** The first review opened those files and checked the quoted numbers. This pass Crossref-verified the Cobb DOI, checked the repaired wording and table against the pre-fix tree, and confirmed that no locked file moved. That is enough for a fix-confirm of an unlocked drop note.

---

## Recommendation

Merge is appropriate. The drop stands under the written rule, the three should-fixes and both nits are applied, CORE and the law sentence are untouched, and no locked row is re-scored. This is not a lock, and it does not start official Pass 1 scoring. Candidate 2 remains an unlocked next attempt, not a shown discriminator.
