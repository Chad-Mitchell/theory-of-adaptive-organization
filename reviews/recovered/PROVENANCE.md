# Recovered review reports — provenance (20 Nov 2026, about 6:30 PM ET)

Search covered the working machine (except a private tree, which was not touched), temporary directories, agent stores, and named work-clone directories for reviews 26–29. Also searched leftover temporary review-28 and review-29 patch files, PR #118 / hygiene copies, and agent-asset text dumps. Trash was empty or missing. One unreadable archive pack was not listable. Transcript tools were used on this run's own session and on stored parent-transcript assets; they did not yield the missing full files for reviews 26 or 29.

Review 28's preamble is the key pointer: prior reviews lived in the review-26 work clone as `REVIEW.md` (NOT READY) and `REVIEW2.md` (READY-WITH-FIXES at `dfe9d0b`). Those clones are gone. Review 27's first report lived in the review-27 work clone as `REVIEW.md` (PR #110, not the map). Review 29 lived in the review-29 work clone as `REVIEW.md` (PR #112, v2.5.4-premise); that clone is gone (a path listing still names that file).

## Recovered

| File here | What it is | Source | SHA-256 | Notes |
|---|---|---|---|---|
| `REVIEW28_PR111.md` | Review 28, full text | A temporary copy of the review-28 report, written 20 Nov 2026 12:53 PM ET; matches the 12:53 agent-asset copy | `b31148facbacb25925f173a1326145f2fb18468faf367b376a140ee406508832` | Final independent check of PR #111 at `3ce9751`. Verdict READY-WITH-FIXES. |
| `REVIEW28_PR111.hygiene-copy.md` | Later copy used in the hygiene / PR #118 tree | The PR #118 tree's copy of review 28 (same bytes as a later hygiene working copy) | `64a5bb297df4c9b2da48145c011eeed27b3618bf457f81b89e98857d93512002` | 31 bytes shorter than the 12:53 file (among other small edits, a clause in the header saying a private tree was left untouched is absent). Not the original referee file. |
| `REVIEW27_PR110_first.md` | Review 27, first report only | Extracted from a Read-tool dump of the review-27 work clone's `REVIEW.md`, stored as agent asset `26abb26f…205.txt` (20 Nov 2026, 1:10 PM ET timestamp on a nearby asset is not this file's; this asset's mtime is whatever the store recorded). Line-number prefixes stripped. | `69c8f54759d6c466d3f7e17461a55d0ac9e6ad5b83eb095b73151a966d2291e9` | PR #110 at `99323e3`, verdict READY-WITH-FIXES. Ends at item S-14. Does **not** include the later REVIEW2 or REVIEW3 sections that were appended to the same path. |
| `REVIEW27_PR110_REVIEW2_fragments.md` | Fragments of review 27's REVIEW2 | Quoted from a parent-session transcript asset `f6dd9885…txt` (12:19 PM ET, 20 Nov 2026) | `4197da13f4967e868cb4d103a5368af4ed636736642513e52f40af5d6b60950c` | Verdict READY-WITH-FIXES at head `da0a5a6`; M1, M3, M4, M5 resolved; M2 resolved in substance with R2-1 (Tjalma wording). **Not the referee's file.** REVIEW3 was commissioned; its text was not found. |
| `REVIEW30_PR115.md` | Independent review of PR #115 (called review 30 in the CHANGELOG) | The PR #115 review work clone (byte-identical to the hygiene copy) | `db28a26b6043162943f41818104c8902d034101d8c88ef2483454359e9fbacc8` | Head `7c1dc22`, about 2:30 PM ET, READY-WITH-FIXES. This is the first #115 review, not a later re-review. |
| `REVIEW_PR113.md` | Independent review of PR #113 | A temporary copy of the PR #113 review (14:09 ET) | `3c90fc4de6ea3fec7fb3eb4f5e784ef29de6a802d8d835015d72bbdedf302215` | Recovered because it sits in the same #111–#115 set; not one of the four named missing files. |
| `review29_author_patches/` | Author-side patches dated 1:21 PM ET | Temporary author-side patch files from applying review 29's fixes | (several files) | **Not review 29.** These are leftover diffs/files from applying review 29's fixes (README, THEORY, CLAIM_MAP, CHANGELOG, STORE_NOISE, threshold check). They do not contain the referee's report. |

## Not recovered (unrecoverable from the search)

- **Review 26** (the review-26 work clone's `REVIEW.md`): first independent review of PR #111 / v2.5-map, verdict **NOT READY** (about 11:30 AM ET per CHANGELOG v2.5.1). The clone directory is gone. No full-text copy was found in temporary directories, hygiene copies, agent assets, or transcripts. Secondary evidence only: CHANGELOG v2.5.1 (the author's summary of the blockers) and review 28's references to "review 26's world" (`review_work/d_greedy_partial.jsonl`, also gone) and to REVIEW2 items.
- **Review 26 round 2** (the same clone's `REVIEW2.md`, READY-WITH-FIXES at `dfe9d0b`, about 12:20 PM ET per CHANGELOG v2.5.2). Gone with the same clone. Review 28 §A is a *status table against those items*, not the review itself.
- **Review 27 REVIEW2 and REVIEW3** (appended to the review-27 work clone's `REVIEW.md` after head moved to `da0a5a6` and later): only the fragments file above. The clone is gone.
- **Review 29** (the review-29 work clone's `REVIEW.md`): independent review of PR #112 / v2.5.4-premise, verdict READY-WITH-FIXES. The clone is gone; a path listing still names the file. CHANGELOG v2.5.4 and `review29_author_patches/` record what the author changed, not the referee's words. The "any-SNR bound (review 29's first-order argument)" is cited but the argument's original writeup was not found as a standalone report.
- **A #115 re-review** (a second pass after the review-30 fixes): not found. What *was* found is the first #115 review (review 30, recovered above). The CHANGELOG describes the subsequent edits as "the fixes are a self-check." If a later independent confirm existed, it was not found in this search.

The review-28 work clone is also gone; only the report and leftover temporary review-28 working files remain.

Historical referee files recovered here (for example review 28's original header) may mention that a private tree was left untouched. Those files were not rewritten just to remove that clause.

## Author patches after review 29 (not the report)

Files in `review29_author_patches/`, all dated 20 Nov 2026, 1:21 PM ET, copied from the temporary review-29 patch files:

| File | SHA-256 |
|---|---|
| `r29fix_README.md` | `0564bb4cf9e6c4833b9cf0a566ef91dc7ef2769ca570ed3c1ad525d849d853a0` |
| `r29fix_THEORY.md` | `a936be6a8c35d4fa3fb408ce709691ea141b5c37e4101905289eaba93fba3f10` |
| `r29fix_measurement_CLAIM_MAP_v2.md` | `259f973e4ff002348baca2351cd45380c75297e0e23e7d15cf632c160e71b44b` |
| `r29fix_reference_CHANGELOG.md` | `3900adfaeaba93c57eb70b09ccf5e154f9ce18967e25da9cb26633dc8461209e` |
| `r29fix_theory_STORE_NOISE.md` | `e250d831427dd2183f7b08fe1e48d2b02278183005de23756e6d08a28ebd8e53` |
| `r29fix_theory_store_noise_threshold_check.json` | `8f400baf892653e24567d0ccf308136b4fb83b75876131185358d01ec86a4e98` |
| `r29fix_theory_store_noise_threshold_check.py` | `42a9d044dc118bce385026d6240328b82111c4d7ac731456a87703c9f197da4a` |
| `r29fix_tools_test_store_noise.py` | `aeeb54843b90baf783f7b7e50d96e279d71225176e69e4b4ae8c36a965b3cd86` |

## Search close (20 Nov 2026, 7:03 PM ET)

A second pass at resume time did not turn up the review-26 work clone, `REVIEW2.md` for that review, the review-27 work clone (beyond the first-report extract already here), the review-29 report, or a #115 re-review. The missing items listed above remain unrecoverable from the search. A private tree was not searched or touched.

**Inventory against the original request** (reviews 26, 27, 29, and a #115 re-review, as cited by review 28):

| Requested | Status |
|---|---|
| Review 26 (`REVIEW.md` in the review-26 work clone, NOT READY) | **Unrecoverable** |
| Review 26 round 2 (`REVIEW2.md` at `dfe9d0b`) | **Unrecoverable** (review 28 §A is a status table against it, not the text) |
| Review 27 first report (PR #110) | **Recovered** (`REVIEW27_PR110_first.md`) |
| Review 27 REVIEW2 / REVIEW3 | **Fragments only** / unrecoverable |
| Review 28 (cited the others) | **Recovered** (`REVIEW28_PR111.md`) |
| Review 29 (PR #112) | **Unrecoverable** (author patches only) |
| #115 re-review | **Unrecoverable**; the first #115 review (review 30) was recovered |
