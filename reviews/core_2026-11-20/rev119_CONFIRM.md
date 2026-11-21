# Confirm review: PR #119 at 9b3d465

**Reviewer:** independent (wrote the first review of `aa6ab29`; wrote none of the fix commit).
**Date:** Friday 20 November 2026, started 9:27 PM ET, finished 9:34 PM ET (America/New_York).
**Clone:** `/workspace/rev119`, fetched `pull/119/head`, checked out `9b3d46504d9d053b10d6d6cd2f4b17925ab771d1` (parent `aa6ab2925b83b17390ac669426a0eb556a9930a7`; base still `ff14a87`). Clean detached HEAD. Nothing pushed or merged. `/workspace/looper` was not touched. Compute at nice 19.

**Verdict: CONFIRMED**

B1 and S1–S5 are fixed correctly. The prereg and predictions hashes are unchanged. Checkers and `pytest tools/` pass. No new problem that would reopen the review. Residuals below are historical or pre-existing and do not block.

The fix commit is `9b3d465` (“Apply PR #119 review: MUST J typo, pointers, provenance paths”). It touches only OPEN_WORK.md, README.md, STATUS.md, `core/keystone_checks/RHYTHM_RESULTS.md`, `reviews/README.md`, `reviews/recovered/PROVENANCE.md`, and a byte-identical copy of the first review at `reviews/core_2026-11-20/rev119_REVIEW.md`. No prereg, predictions, run JSON, inclusion rule, or gate table was edited.

---

## B1 — fixed

`RHYTHM_RESULTS.md` §4 now gives the first-order-only MUST argmin as K=3, **J=7.105**, and notes agreement with KEYSTONE_NOTE §2. §9 now says “MUST J=6.25 vs first-order K=3, J=7.105.” The official MUST figures that the gate uses (predicted C*=4, argmin C*=3, hybrid J=6.2486, E=0.041022, two-resonator J=7.006) are untouched. A parenthetical records that the earlier writeup and the prior rhythm review quoted J=8.105 / 8.10 (= 1+7.105, same class as D5a), that the gate does not flip, and that the prior review file is left unedited as a historical record. That is the right treatment.

## S1 — fixed

OPEN_WORK W11 now ends “Follow-ups as new preregs, not rescues: T20–T23.” There is still no T24. T19 (Lean) remains parked in §5 and is correctly omitted from that “new preregs” range.

## S2 — fixed

`reviews/README.md` no longer says the core drafts are “not in this repository yet.” The `core_2026-11-20/` row states that CORE.md is in the repository and also points at `rev119_REVIEW.md` (READY-WITH-FIXES). New rows cover `rhythm_2026-11-20/REVIEW.md` (SCORING CORRECT) and `recovered/` (with the provenance caveat). A blank line still separates those rows from the `pr118_hygiene` row; that break was already on main and is not new.

## S3 — fixed

README now scopes the lead: “The predictive keystone is scoped there (§4): it is numerically supported only in Model S, given convexity, which remains unproved; a rhythm is a two-state mode by degree, but a pair-count does not recover the cheapest design.” The “Matched is not equal” sentence and the following bullet make the same point and point at CORE §4. STATUS.md’s canonical-file list now starts with `CORE.md` — “the theory on one page. The predictive keystone is scoped in §4.”

## S4 — fixed in the newly authored provenance

`reviews/recovered/PROVENANCE.md` no longer names `/workspace/looper`, `/home/box`, `/cursor/stores`, or `sand-box-store-pack`. The search is described generically (“a private tree, which was not touched”). Historical referee files were not rewritten; provenance notes that some of them mention a private tree left untouched. OPEN_WORK W6 was updated to match. That is what S4 asked for.

## S5 — fixed

W5 now reads “**DONE** in the hygiene PR (#118).”

---

## Hashes, checkers, tests

- `RHYTHM_PREREG.md` SHA-256 `e0b4f2b6f31743fdffe05f0f3eeedfb3d169824136a5671bfdce28ee11fd50ce` — unchanged vs `aa6ab29` and vs every recorded citation.
- `imp_n60_predictions.json` SHA-256 `b625a8ad57c3d861d5f0202b36125c4fa405b34260b9c46fdf72a9279d135bb3` — unchanged.
- `python3 tools/check_consistency.py`: RESULT: PASS (0 FAILs). Soft length warnings only (THEORY.md 10471; README.md 1468, up from 1405 because of the scope sentences; advisory, not a failure). Frozen-record INFO hits 23 (was 22); wording FAILs still 0. The extra INFO is the committed first-review file, which is a dated record.
- `python3 tools/check_open_work.py`: RESULT: PASS (union missing = 0).
- `python3 -m pytest tools/ -q`: **125 passed** in 350 s.

The first review committed at `reviews/core_2026-11-20/rev119_REVIEW.md` is byte-identical to `/workspace/review-archive/rev119_REVIEW.md` (SHA-256 `944d4409f6ece024aab94ccf281960f9513243e2e70dfeae70f765018cdba69d`).

---

## Residuals (do not block)

- `reviews/rhythm_2026-11-20/REVIEW.md` still names `/workspace/gtao-core` and `/workspace/looper` in its header, and still quotes J=8.10. That file is the prior independent scoring review; the author correctly left it unedited, as B1 required for the J typo and as S4 required for historical referee text.
- The committed first review of `aa6ab29` also names `/workspace/looper`, because that is the review text. It should stay unedited.
- STATUS.md’s standing-rules sentence “Looper README wording needs Chad's approval” is pre-existing on main and was not introduced or copied forward by this fix. The “As of” / “Where the theory stands” paragraphs still lead with THEORY v2.9; the canonical-file list now carries CORE.md, which is what S3 asked for.
- OPEN_WORK H1, H3, H4, H7, H8, and C6 still say “this hygiene PR.” S5 asked only for W5.

No new “law” (beyond the hypothesis sentence), no “theory of everything,” no Looper content, and no change to official gates.

No push or merge was made. This report: `/workspace/review-archive/rev119_CONFIRM.md`.
